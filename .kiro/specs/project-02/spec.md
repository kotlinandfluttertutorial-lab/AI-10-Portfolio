# Project Specification — P02: Autonomous Market Research Analyst

**Project ID:** P02  
**Folder:** `autonomous-research-agent/`  
**Status:** Specified  
**AI-SDLC Phase:** SPECIFY → DESIGN  
**Version:** 1.0

---

## 1. Executive Summary

Market research is time-consuming and error-prone when done manually. This platform deploys an autonomous research agent that accepts a research question, plans a multi-step investigation, searches the web and internal sources, collects and verifies evidence, and produces a structured report with citations — all with human review at the final step.

---

## 2. Problem Statement

Analysts spend days gathering market intelligence that could be automated. Manual research suffers from confirmation bias, incomplete source coverage, and inconsistent citation quality. Existing AI tools generate reports but cannot verify claims against actual sources.

---

## 3. Target Users

- Market analysts and strategists needing competitive intelligence
- Product managers researching market sizing and trends
- Executives needing rapid briefings on competitors or sectors

---

## 4. Personas

**Sam — Market Analyst:** Runs 5–10 research requests per week. Needs sourced, verifiable claims. Cannot submit a report that cites a hallucinated statistic.

**Priya — Product Manager:** Needs a quick competitive landscape summary. Wants a structured output she can paste into a deck.

**Jordan — Engineering Manager:** Deploys and maintains the platform. Needs observability on agent runs and cost tracking.

---

## 5. User Journeys

**Primary (Sam):**
1. Submits research question: "What are the top 3 CRM platforms by SMB market share in 2026?"
2. Agent plans 5–8 research steps, begins searching
3. Sam can monitor step progress in the UI
4. Agent produces a draft report with citations
5. Sam reviews, approves, and exports the report

**Admin (Jordan):**
1. Monitors agent run costs and step counts
2. Reviews failed runs and error logs
3. Adjusts step limits and search budgets

---

## 6. Business Goals

- Reduce research turnaround from days to hours
- Achieve claim accuracy ≥ 80% (claims verifiable against cited sources)
- Demonstrate bounded autonomous agent with human approval gate
- Zero hallucinated citations in released reports

---

## 7. Functional Requirements

- FR-01: Accept a research question and decompose into a step plan
- FR-02: Execute search tool calls (web search, internal knowledge base)
- FR-03: Collect and store evidence per step in an evidence store
- FR-04: Verify claims against source URLs before including in report
- FR-05: Generate structured report (markdown/PDF) with citations
- FR-06: Human review and approval before report is marked final
- FR-07: Track step count, token usage, and cost per run
- FR-08: Enforce maximum step count and cost budget per run
- FR-09: Allow run cancellation by the user
- FR-10: Export final report as PDF or markdown

---

## 8. Non-Functional Requirements

- NFR-01: Agent runs complete within 10 minutes for a standard 8-step plan
- NFR-02: Maximum 20 tool calls per research job (configurable)
- NFR-03: Maximum $2.00 AI cost per research job (configurable)
- NFR-04: No sensitive user data sent to web search tools
- NFR-05: All tool calls logged with sanitized arguments

---

## 9. System Architecture

```
[Research Request API]
        ↓
[Planner Agent] → step plan stored in ResearchJob
        ↓
[Execution Loop] → search/retrieve tools → evidence stored per step
        ↓
[Verification Agent] → checks claim-to-source alignment
        ↓
[Synthesis Agent] → draft report generation
        ↓
[Human Review Gate] → approve/reject
        ↓
[Report Export API]
```

---

## 10. Component Architecture

- `api/` — research-jobs, reports, approvals, tools, health
- `domain/` — ResearchJob, PlanStep, Source, Evidence, ToolCall, Finding, Report, ReviewDecision
- `adapters/` — web search adapter (Tavily/Serper), LLM planner adapter, LLM synthesis adapter
- `workers/` — research execution worker (runs the agent loop)
- `evaluation/` — claim accuracy runner, hallucination detector

---

## 11. Data Architecture

Core entities: ResearchJob, PlanStep, Source, Evidence, ToolCall, Finding, Report, ReviewDecision

Key relationships:
- ResearchJob 1:N PlanSteps
- PlanStep 1:N ToolCalls, 1:N Evidence
- Evidence N:M Sources
- ResearchJob 1:1 Report
- Report 1:1 ReviewDecision

---

## 12. Database Schema (Key Tables)

```sql
research_jobs(id, user_id, question, status, step_count, token_count, cost_usd, created_at)
plan_steps(id, job_id, step_index, description, status, tool_name, created_at)
tool_calls(id, step_id, tool_name, arguments_hash, result_summary, latency_ms, created_at)
sources(id, job_id, url, title, snippet, retrieved_at)
evidence(id, step_id, source_id, claim, verified, created_at)
reports(id, job_id, content_md, status, created_at)
review_decisions(id, report_id, reviewer_id, decision, notes, created_at)
```

---

## 13. API Specification

```
POST   /v1/research-jobs               — start a new research job
GET    /v1/research-jobs/{id}          — get job status and steps
DELETE /v1/research-jobs/{id}          — cancel a running job
POST   /v1/research-jobs/{id}/approve  — human approves the draft report
GET    /v1/reports/{id}                — get final report
GET    /v1/reports/{id}/export         — export as PDF or markdown
GET    /v1/health
GET    /v1/ready
```

---

## 14. AI Architecture

- Planner: LLM call that decomposes question into ordered steps with tool assignments
- Executor: ReAct loop — step description → tool call → evidence storage → next step
- Verifier: LLM call that checks each claim against its cited source text
- Synthesizer: LLM call that writes the structured report from verified evidence
- All LLM calls go through the provider adapter with budget enforcement

---

## 15. Prompt Architecture

- Planner prompt: system instructs to produce a JSON step plan; user provides question + constraints
- Executor prompt: system provides available tools and rules; user provides current step + evidence so far
- Verifier prompt: system instructs to verify claim against source; outputs `{ "verified": bool, "reason": string }`
- Synthesizer prompt: system instructs to write report from evidence only; never fabricate
- All prompt templates in `domain/prompts/`, versioned

---

## 16. Agent Architecture

- Single agent with planning → execution → verification → synthesis stages
- ReAct pattern: reason about the current step, select a tool, observe result, repeat
- Maximum iterations: configurable (default 20 tool calls)
- Circuit breaker: if 3 consecutive tool calls fail, pause and alert
- State persistence: every step result is written to the database before proceeding
- Recovery: interrupted jobs can be resumed from the last completed step

---

## 17. Tool Architecture

Available tools (allowlisted):
- `web_search(query)` — returns top 5 results with URL and snippet
- `fetch_page(url)` — fetches and extracts text from a URL
- `knowledge_base_search(query)` — searches internal documents (optional)

Rules:
- Tools are read-only — no write or execute tools
- Tool call arguments are validated before execution
- Tool results are truncated to 2000 tokens before being passed back to the agent
- All tool calls logged with sanitized arguments and result length

---

## 18. Security Architecture

- JWT authentication; users can only access their own research jobs
- Web search: queries are sanitized; no PII or internal credentials sent to external APIs
- Tool allowlist enforced: agent cannot call tools not in the allowlist
- Budget enforcement: agent halts when cost ceiling is reached
- Audit log: all tool calls, review decisions, and export events

---

## 19. Evaluation Architecture

```
evaluation/datasets/v1.0/  — research questions with ground-truth claims
evaluation/metrics/claim_accuracy.py   — % claims verifiable against cited sources
evaluation/metrics/source_coverage.py — % relevant sources found
evaluation/metrics/hallucination.py   — % claims with no source support
evaluation/runners/run_eval.py
evaluation/reports/
evaluation/regression/baseline.json
```

---

## 20. Observability Architecture

- Metrics: `research_jobs_total`, `research_steps_total`, `tool_calls_total{tool_name}`, `ai_cost_usd_total`, `job_duration_seconds`
- Logs: every step start/complete/fail with `job_id`, `step_id`, `tool_name`, `duration_ms`
- Alert: job cost > 80% of budget triggers a warning log
- Dashboard: jobs running, jobs completed today, average cost per job, error rate

---

## 21. Deployment Architecture

```
docker-compose:
  - postgres
  - redis (job queue)
  - api
  - worker (agent execution)
  - frontend (React)
```

---

## 22. Testing Strategy

- Unit: planner decomposition, verifier logic, report generation, budget enforcement
- Integration: full agent run with mocked tool adapters
- API: job CRUD, approval flow, export
- Security: tool allowlist enforcement, budget cap, user isolation
- E2E: submit question → approved report with verified citations

---

## 23. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Runaway agent (too many steps) | Medium | High | Hard step limit + cost cap |
| Hallucinated citations | Medium | High | Claim verification step + hallucination metric |
| External search API failure | High | Medium | Fallback to knowledge base; graceful degradation |
| Sensitive user query sent to web | Low | High | Query sanitization before external tool calls |

---

## 24. Threat Model

Key threats: prompt injection via search results, tool call argument injection, data exfiltration via crafted URLs, cost DoS via rapid job submission.

Mitigations: tool allowlist, argument validation, rate limiting on job submission, budget cap. Full threat model: `docs/security/threat-model-P02.md`

---

## 25. Performance Requirements

- Standard 8-step job completes in < 10 minutes
- Each tool call: timeout 30s, max 3 retries
- Report generation: < 60s for a 10-source report

---

## 26. Cost Considerations

- Web search API: ~$5/1000 searches (Tavily or similar)
- LLM (planner + verifier + synthesizer): ~$0.50–1.50 per job on GPT-4o
- Default budget cap: $2.00 per job; configurable per user

---

## 27. Definition of Done

- All 20 tickets accepted
- E2E demo: question → verified citations → approved report passes
- Claim accuracy ≥ 80% on eval dataset
- No hallucinated citations in final reports (verified = 100% in demo)
- Security: tool allowlist tested, budget cap tested

---

## 28. Release Criteria

- CI green, Docker Compose runs cleanly
- Human approval (Gate G5) obtained
- Known limitations documented (e.g., web search quality varies)

---

## 29. Future Roadmap

- Streaming step progress via WebSocket
- Citation quality scoring with LLM-as-judge
- Multi-agent parallel research branches
- Internal knowledge base as a first-class tool
- Report templates (competitive analysis, SWOT, trend summary)
