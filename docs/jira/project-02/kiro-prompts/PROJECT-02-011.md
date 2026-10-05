# Kiro Implementation Prompt

**Project:** P02 — Autonomous Market Research Analyst
**Jira:** P02-11
**AI-SDLC Phase:** BUILD
**Title:** Claim verification and citation validation

---

## Objective

Implement the feature described by Jira ticket P02-11: **Claim verification and citation validation** for the Autonomous Market Research Analyst project.

Inspect the existing codebase before making any changes. Implement the smallest coherent change that satisfies the acceptance criteria in the Jira ticket. Write tests. Report actual results.

---

## Context

**Project folder:** `autonomous-research-agent/`
**Project spec:** `.kiro/specs/project-02/spec.md`
**Requirements:** `autonomous-research-agent/specs/requirements.md`
**Design:** `autonomous-research-agent/specs/design.md`
**Jira ticket:** see `docs/jira/project-02/P02-tickets-full.csv` row P02-11 for full description, acceptance criteria, technical notes, and security requirements
**Architecture steering:** `.kiro/steering/architecture.md`
**Engineering steering:** `.kiro/steering/engineering.md`
**Security steering:** `.kiro/steering/security.md`
**Testing steering:** `.kiro/steering/testing.md`

---

## Dependencies

- P02-10 completed and merged before starting this ticket

---

## Implementation Requirements

Read the Jira ticket row for this ticket in `docs/jira/project-02/P02-tickets-full.csv`. The Description, Technical Notes, and Acceptance Criteria columns specify exactly what to implement. Follow the architecture in `.kiro/specs/project-02/spec.md` and the engineering standards in `.kiro/steering/engineering.md`.

Key rules from engineering steering:
1. Inspect the existing repository before changing any file
2. Never invent requirements beyond what is in the Jira ticket
3. Never claim tests passed without running them
4. Keep domain logic separate from API and adapter layers
5. Validate all external input at the boundary
6. No secrets or credentials in code, logs, or configuration files

---

## Technical Constraints

- Python 3.11+, FastAPI, PostgreSQL, Redis (technology defaults from `.kiro/steering/architecture.md`)
- All new dependencies pinned to exact versions in requirements.txt
- No secrets in logs or API responses
- Follow existing code patterns in the project
- Domain layer has no direct database or HTTP imports

---

## Files to Inspect

Before writing any code, inspect:
- `autonomous-research-agent/` — full current project structure
- `.kiro/specs/project-02/spec.md` — section covering this feature
- `autonomous-research-agent/specs/requirements.md` — requirements for this feature area
- `autonomous-research-agent/specs/design.md` — design decisions
- `docs/jira/project-02/P02-tickets-full.csv` — this ticket's full specification

---

## Expected Changes

Implement the code, tests, and documentation changes required by the Jira ticket. Typical changes for a BUILD-phase ticket:
- Domain logic in `autonomous-research-agent/domain/`
- API endpoint in `autonomous-research-agent/api/routers/`
- Adapter if needed in `autonomous-research-agent/adapters/`
- Unit tests in `autonomous-research-agent/tests/unit/`
- Integration tests in `autonomous-research-agent/tests/integration/`
- Documentation update if API or architecture changed

---

## Acceptance Criteria

See `docs/jira/project-02/P02-tickets-full.csv` row P02-11 — "Acceptance Criteria" column. Every criterion must be met and evidenced with actual test output.

---

## Testing

- Unit tests: main success path, edge cases, error paths
- Integration tests: API endpoints with valid and invalid inputs
- Security tests: where applicable (see "Security Requirements" column in the Jira CSV)
- Run: `pytest tests/ -v` and report exact output (never summarize)

---

## AI-SDLC Verification

Before completing:
1. Run `pytest tests/ -v` — report exact output including pass count
2. Run `ruff check .` — must pass
3. Verify no secrets in any committed file
4. Verify documentation updated where needed
5. Verify traceability: confirm this prompt, the Jira ticket, and the implementation are linked

---

## Human Approval Required

- Architecture deviations
- Security exceptions  
- Any requirement ambiguity found during implementation — stop and report rather than guess

---

## Definition of Done

- All acceptance criteria from the Jira ticket evidenced with actual test output
- Code reviewed by a human (never self-approved)
- Tests executed: actual results recorded
- No secrets or sensitive data in committed files
- Traceability: Jira P02-11 → this prompt → implementation → tests

---

## Output Report

Kiro must report:
- Files created (list)
- Files modified (list)
- Files deleted (list)
- Tests executed: `pytest` exact output
- Test results: N passed, N failed, N skipped
- Security checks performed
- Performance observations (if relevant)
- Known limitations
- Remaining risks
- **Jira status recommendation:** Ready for Code Review
