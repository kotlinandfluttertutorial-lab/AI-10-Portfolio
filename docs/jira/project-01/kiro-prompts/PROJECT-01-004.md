# Kiro Implementation Prompt

**Project:** P01 — Enterprise Knowledge Intelligence Platform
**Jira:** P01-004
**AI-SDLC Phase:** BUILD
**Title:** Implement versioned API foundation and error contract

---

## Objective

Implement all core API endpoints under /v1/: POST workspaces, POST documents (upload), GET document, POST search, POST answers, POST evaluations, POST feedback, GET health, GET ready. All responses follow the portfolio error envelope from docs/api/api-style-guide.md. Add X-Request-ID middleware and pagination on collection endpoints.

---

## Context

**Project folder:** `rag-evaluation-platform/`
**Project spec:** `.kiro/specs/project-01/spec.md`
**Requirements:** `rag-evaluation-platform/specs/requirements.md`
**Design:** `rag-evaluation-platform/specs/design.md`
**Architecture steering:** `.kiro/steering/architecture.md`
**Engineering steering:** `.kiro/steering/engineering.md`
**Security steering:** `.kiro/steering/security.md`
**Testing steering:** `.kiro/steering/testing.md`

---

## Dependencies

- P01-03 completed and merged

---

## Implementation Requirements

Implement the feature described in the Objective following the architecture defined in `.kiro/specs/project-01/spec.md` and the standards in the steering files. Keep domain logic separate from API and adapter layers. Validate all external input. Use the provider adapter pattern for all AI calls.

---

## Technical Constraints

- Python 3.11+, FastAPI, PostgreSQL + pgvector, Redis
- All new dependencies pinned to exact versions
- No secrets or credentials in code or logs
- No document or query content in structured logs
- Domain layer has no direct database or HTTP imports — use adapters
- Follow existing code patterns in the project (inspect before writing)

---

## Files to Inspect

- `rag-evaluation-platform/` — full project structure
- `.kiro/specs/project-01/spec.md` — section covering this feature
- `rag-evaluation-platform/specs/requirements.md` — functional requirements
- `rag-evaluation-platform/specs/design.md` — design decisions

---

## Expected Changes

Implement the code changes required to satisfy the Objective and acceptance criteria. Write unit tests for all new domain logic. Write integration tests for any new API endpoints. Update documentation (README, API.md, ARCHITECTURE.md) if this change affects them.

---

## Acceptance Criteria

See docs/jira/project-01/P01-tickets-full.csv row P01-004 for the full acceptance criteria list.

---

## Testing

- Unit tests: cover main success path, edge cases, and error paths for all new domain logic
- Integration tests: cover new API endpoints with valid and invalid inputs
- Security tests: where applicable (auth, authorization, input validation)
- Run: `pytest tests/ -v` and report actual results

---

## AI-SDLC Verification

Before completing:
1. Run `pytest tests/ -v` — report exact output
2. Run `ruff check .` — must pass
3. Run `mypy` — must pass on changed files
4. Verify no secrets in any committed file
5. Verify documentation updated where needed
6. Report actual test counts and results — never claim tests passed without running them

---

## Human Approval Required

- Any deviation from the architecture in `.kiro/specs/project-01/spec.md`
- Security exceptions
- Architecture changes affecting other tickets

---

## Definition of Done

- All acceptance criteria evidenced with actual test output
- Code reviewed by a human (never self-approved)
- Tests executed and results recorded
- Documentation updated
- No secrets or sensitive data in committed files
- Traceability updated: Jira P01-004 → this prompt → implementation → tests

---

## Output Report

Kiro must report:
- Files created (list)
- Files modified (list)
- Test results: exact `pytest` output
- Security checks performed
- Known limitations
- **Jira status recommendation:** Ready for Code Review
