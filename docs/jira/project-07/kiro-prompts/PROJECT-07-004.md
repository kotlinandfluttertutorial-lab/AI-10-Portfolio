# Kiro Implementation Prompt

**Project:** P07 — AI Software Project Delivery Orchestrator
**Jira:** P07-4
**AI-SDLC Phase:** BUILD
**Title:** Implement versioned API foundation and error contract

---

## Objective

Implement Jira ticket P07-4: **Implement versioned API foundation and error contract** for the AI Software Project Delivery Orchestrator.

Inspect the existing codebase before making any changes. Implement only what is specified. Write tests. Report actual results.

---

## Context

**Project folder:** `multi-agent-delivery-orchestrator/`
**Project spec:** `.kiro/specs/project-07/spec.md`
**Requirements:** `multi-agent-delivery-orchestrator/specs/requirements.md`
**Design:** `multi-agent-delivery-orchestrator/specs/design.md`
**Full ticket:** `docs/jira/project-07/P07-tickets-full.csv` row P07-4
**Steering:** `.kiro/steering/` (architecture.md, engineering.md, security.md, testing.md)

---

## Dependencies

- P07-03 completed and merged

---

## Implementation Requirements

Read the full ticket specification from `docs/jira/project-07/P07-tickets-full.csv`. The Description, Technical Notes, Security Requirements, and Acceptance Criteria columns define exactly what to build. Follow the architecture from `.kiro/specs/project-07/spec.md`.

Non-negotiable rules:
- Inspect existing code before writing new code
- Never invent requirements beyond the Jira ticket
- Never claim tests passed without running them
- No secrets in code, logs, or config files
- Domain layer separate from infrastructure

---

## Technical Constraints

Python 3.11+, FastAPI, PostgreSQL, Redis. All new dependencies pinned. No secrets in logs. Follow existing patterns.

---

## Files to Inspect

- `multi-agent-delivery-orchestrator/` — full current structure
- `.kiro/specs/project-07/spec.md`
- `multi-agent-delivery-orchestrator/specs/requirements.md` and `multi-agent-delivery-orchestrator/specs/design.md`
- `docs/jira/project-07/P07-tickets-full.csv`

---

## Expected Changes

Code, tests, and documentation required to satisfy the Jira ticket acceptance criteria.

---

## Acceptance Criteria

See `docs/jira/project-07/P07-tickets-full.csv` row P07-4 — "Acceptance Criteria" column.

---

## Testing

Unit tests, integration tests, and security tests as specified in the Jira ticket. Run `pytest tests/ -v` and report exact output.

---

## AI-SDLC Verification

1. Run `pytest tests/ -v` — report exact output
2. Run `ruff check .` — must pass
3. Verify no secrets in committed files
4. Verify docs updated where needed

---

## Human Approval Required

Architecture deviations, security exceptions, ambiguous requirements.

---

## Definition of Done

- All Jira acceptance criteria evidenced with actual test output
- Human code review completed
- Tests executed and results recorded
- Traceability: P07-4 → this prompt → implementation → tests

---

## Output Report

Files created, files modified, test results (exact pytest output), security checks, known limitations, Jira status recommendation.
