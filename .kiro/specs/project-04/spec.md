# Project Specification — P04: Voice-Based Appointment and Task Assistant

**Project ID:** P04  
**Folder:** `voice-task-assistant/`  
**Status:** Specified  
**AI-SDLC Phase:** SPECIFY → DESIGN  
**Version:** 1.0

---

## 1. Executive Summary

Scheduling appointments and managing tasks by voice is faster than typing but requires AI that can accurately understand intent, extract slot values, confirm ambiguity, and integrate with calendars and task managers. This platform delivers a voice-first assistant that handles multi-turn conversations for appointment booking and task management with confirmation before any write action.

---

## 2. Problem Statement

Voice interfaces for productivity tools are either too rigid (command-only) or too unreliable (misunderstood intents leading to wrong bookings). Users need a conversational assistant that confirms before acting, handles clarifying questions naturally, and integrates with real calendar and task systems.

---

## 3. Target Users

- Individuals managing personal or professional schedules
- Knowledge workers with busy calendars who prefer voice over typing
- Accessibility users who prefer voice interfaces

---

## 4. Personas

**Taylor — Busy Professional:** Books 5–10 meetings per week. Wants to say "Schedule a 30-minute call with Alex tomorrow at 3pm" and have it done. Needs confirmation before the event is created.

**River — Accessibility User:** Uses voice as their primary input. Needs clear, accurate slot confirmation and graceful error recovery when the assistant misunderstands.

---

## 5. User Journeys

**Primary (Taylor):**
1. Says: "Schedule lunch with Priya on Friday at noon"
2. Assistant recognizes: intent=create_event, attendee=Priya, day=Friday, time=noon, duration=default(60min)
3. Assistant confirms: "Create a 60-minute lunch with Priya on Friday October 9 at 12:00pm — shall I proceed?"
4. Taylor says "Yes" → event created in calendar
5. Taylor gets audio confirmation: "Done. Lunch with Priya added."

**Error recovery:**
1. Taylor says "Book a meeting with... tomorrow"
2. Assistant: "Who would you like to meet with?"
3. Taylor: "With Sam"
4. Assistant: "What time tomorrow?"

---

## 6. Business Goals

- Intent accuracy ≥ 90% on standard appointment and task utterances
- Task completion rate ≥ 80% in multi-turn conversations
- Zero calendar write actions without explicit confirmation
- Voice response latency < 1.5s from end of utterance

---

## 7. Functional Requirements

- FR-01: Accept audio input and transcribe via STT
- FR-02: Classify intent (create event, check schedule, add task, complete task, cancel event)
- FR-03: Extract slot values (date, time, duration, attendee, title, priority)
- FR-04: Maintain multi-turn conversation state
- FR-05: Ask clarifying questions for missing or ambiguous slots
- FR-06: Confirm all write actions (create, update, delete) before executing
- FR-07: Integrate with calendar API (create, read, update, delete events)
- FR-08: Integrate with task manager (create, read, complete tasks)
- FR-09: Generate audio response via TTS
- FR-10: Support barge-in (user can interrupt while assistant is speaking)

---

## 8. Non-Functional Requirements

- NFR-01: STT latency < 500ms for utterances under 10 seconds
- NFR-02: End-to-end response latency < 1.5s from end of utterance
- NFR-03: No calendar write without confirmation (hard constraint, tested in security tests)
- NFR-04: Conversation state persists across reconnections for 30 minutes
- NFR-05: Audio data not stored longer than the session

---

## 9. System Architecture

```
[Audio Input] → [STT (Whisper/Deepgram)] → [Intent + Slot Extractor]
                                                      ↓
                                          [Conversation State Manager]
                                                      ↓
                                     [Confirmation Gate] ← → [User]
                                                      ↓
                                       [Tool Executor (Calendar/Tasks)]
                                                      ↓
                                     [Response Generator] → [TTS] → [Audio Output]
```

---

## 10. Component Architecture

- `api/` — sessions, messages, events (SSE for streaming), health
- `domain/` — Session, Turn, Intent, Slot, ConversationState, ConfirmationRequest
- `adapters/` — Whisper STT adapter, TTS adapter (ElevenLabs/OpenAI), calendar adapter (Google/CalDAV), task adapter
- `workers/` — audio processing worker

---

## 11. Data Architecture

Core entities: Session, Turn, Intent, SlotExtraction, ConfirmationRequest, CalendarEvent, Task

---

## 12. Database Schema (Key Tables)

```sql
sessions(id, user_id, status, created_at, expires_at)
turns(id, session_id, role, transcript, intent, slots jsonb, created_at)
confirmation_requests(id, session_id, action_type, action_payload jsonb, status, created_at)
calendar_events(id, user_id, external_id, title, start_time, end_time, created_at)
tasks(id, user_id, external_id, title, due_date, completed, created_at)
```

---

## 13. API Specification

```
POST   /v1/sessions              — start a voice session
POST   /v1/sessions/{id}/audio   — submit audio chunk
POST   /v1/sessions/{id}/text    — submit text (fallback)
GET    /v1/sessions/{id}/stream  — SSE stream for responses
POST   /v1/confirmations/{id}/respond — confirm or cancel an action
GET    /v1/calendar/events       — list upcoming events
GET    /v1/tasks                 — list tasks
GET    /v1/health
```

---

## 14. AI Architecture

- STT: Whisper (via OpenAI API or local) — transcribes audio to text
- Intent + slot extractor: LLM with structured output `{ "intent": string, "slots": {...}, "confidence": float }`
- Response generator: LLM with conversation history and domain context
- TTS: OpenAI TTS or ElevenLabs — converts response text to audio

---

## 15. Prompt Architecture

- Intent extraction: system defines intents and slot types; output is structured JSON
- Response generation: system defines persona, tone, and confirmation rules; never write to calendar without explicit yes
- Clarification: system defines when to ask vs. infer

---

## 16. Agent Architecture

The assistant is a bounded multi-turn conversation agent:
- State machine: idle → listening → understanding → confirming → executing → responding
- Maximum clarification turns: 3 before fallback ("I'm having trouble understanding — would you like to try again?")
- All write tool calls require confirmation (hard requirement, enforced in state machine)
- No autonomous background actions

---

## 17. Tool Architecture

Available tools (allowlisted):
- `calendar.create_event(title, start, end, attendees)` — requires confirmation
- `calendar.get_events(start_date, end_date)` — read-only
- `calendar.update_event(id, changes)` — requires confirmation
- `calendar.delete_event(id)` — requires confirmation
- `tasks.create_task(title, due_date, priority)` — requires confirmation
- `tasks.complete_task(id)` — requires confirmation
- `tasks.list_tasks(filter)` — read-only

All write tools require a `ConfirmationRequest` to be acknowledged before execution.

---

## 18. Security Architecture

- JWT auth; users can only access their own sessions and calendar data
- No persistent audio storage; transcripts stored as text only (session-scoped, TTL 30 min)
- Calendar credentials: OAuth2 tokens stored encrypted, never in logs
- Confirmation gate: write tools cannot execute without `confirmation_requests.status = confirmed`
- PII: attendee names and event titles are not logged in structured logs

---

## 19. Evaluation Architecture

Metrics: intent accuracy, slot fill accuracy, task completion rate, clarification efficiency, confirmation bypass attempts (should always be 0)

---

## 20. Observability Architecture

- Metrics: `session_turns_total`, `intent_accuracy`, `tool_calls_total{tool}`, `stt_latency_seconds`, `tts_latency_seconds`
- Logs: turn events (no audio content, no attendee names in structured fields)

---

## 21. Deployment Architecture

```
docker-compose: postgres, redis (session state), api, audio-worker, frontend (React voice UI)
```

---

## 22. Testing Strategy

- Unit: intent extractor, slot extractor, state machine transitions
- Integration: multi-turn conversation flows with mocked STT/TTS/tools
- API: session CRUD, confirmation flow, stream endpoint
- Security: confirmation bypass attempts, unauthorized calendar access, session isolation
- E2E: "Schedule a meeting" → confirmation → calendar event created

---

## 23. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Unconfirmed calendar write | Low | Critical | Hard state machine requirement + security test |
| STT misrecognition of names/dates | High | Medium | Confirmation gate catches all slot values before action |
| TTS API latency > 1.5s | Medium | Medium | Streaming TTS + latency SLA monitoring |
| OAuth token expiry during session | Medium | Medium | Background token refresh before expiry |

---

## 24. Threat Model

Unauthorized calendar writes, session hijacking, PII exposure via transcript logs, OAuth token leakage. Full threat model: `docs/security/threat-model-P04.md`

---

## 25. Performance Requirements

- STT: < 500ms for ≤ 10s utterances
- End-to-end response: < 1.5s p95
- Confirmation-to-execution: < 500ms after user says "yes"

---

## 26. Cost Considerations

- Whisper: ~$0.006/minute audio
- TTS: ~$0.015/1K characters
- LLM intent/response: ~$0.01–0.05 per turn
- Per-session budget cap: $0.25 (configurable)

---

## 27. Definition of Done

- Intent accuracy ≥ 90%, task completion rate ≥ 80% on eval set
- Confirmation bypass test always fails (zero bypasses)
- E2E demo passes
- Security gate signed off

---

## 28. Release Criteria

- CI green, Docker Compose runs, human approval obtained

---

## 29. Future Roadmap

- Real-time streaming STT (word-level) for faster response
- Multi-language support
- Smart conflict detection ("you have a meeting at 3pm already")
- Proactive reminders ("Your 3pm call is in 10 minutes")
