# Kiro Implementation Prompt

**Project:** P10 — LLM Guard and Prompt Injection Defense Platform
**Jira:** P10-7
**AI-SDLC Phase:** BUILD
**Title:** Output scanning and content validation

---

## Objective

Implement Jira ticket P10-7: **Output scanning and content validation** for the LLM Guard and Prompt Injection Defense Platform.

Inspect the existing codebase before making any changes. Implement only what is specified in the Jira ticket. Write automated tests. Report actual (not estimated) results.

---

## Context

**Project folder:** `enterprise-prompt-security/`
**Project spec:** `.kiro/specs/project-10/spec.md`
**Requirements:** `enterprise-prompt-security/specs/requirements.md`
**Design:** `enterprise-prompt-security/specs/design.md`
**Full ticket spec:** `docs/jira/project-10/P10-tickets-full.csv` — row P10-7
**Steering files:** `.kiro/steering/` (architecture.md, engineering.md, security.md, testing.md)

The Jira CSV row contains: Description, Business Value, Technical Notes, Acceptance Criteria, Testing Requirements, Security Requirements, and Definition of Done. Read all columns before writing a line of code.

---

## Dependencies

- P10-06 completed and merged before starting this ticket

---

## Implementation Requirements

1. Read the full ticket from `docs/jira/project-10/P10-tickets-full.csv` row P10-7
2. Inspect the existing codebase at `enterprise-prompt-security/`
3. Implement the feature described in Description and Technical Notes columns
4. Follow the architecture in `.kiro/specs/project-10/spec.md`
5. Apply engineering standards from `.kiro/steering/engineering.md`
6. Apply security controls from `.kiro/steering/security.md`

---

## Technical Constraints

- Python 3.11+, FastAPI, PostgreSQL, Redis
- All new dependencies pinned to exact versions
- No secrets or credentials in code, logs, or configuration files
- Domain layer must not import from adapters directly
- All external input validated at the API boundary
- No content (user data, documents, AI responses) in structured logs

---

## Files to Inspect

Before writing code:
- `enterprise-prompt-security/` — complete current project structure
- `.kiro/specs/project-10/spec.md` — section covering this feature
- `enterprise-prompt-security/specs/requirements.md` — functional requirements
- `enterprise-prompt-security/specs/design.md` — design decisions
- `docs/jira/project-10/P10-tickets-full.csv` — this ticket's specification

---

## Expected Changes

All code, test, and documentation changes required to satisfy the acceptance criteria. Structure follows the existing project conventions. Do not add features beyond what the ticket specifies.

---

## Acceptance Criteria

Read from `docs/jira/project-10/P10-tickets-full.csv` row P10-7 — "Acceptance Criteria" column. Every numbered criterion must be evidenced.

---

## Testing

As specified in the "Testing Requirements" column of the Jira ticket. At minimum:
- Unit tests: all new domain logic
- Integration tests: all new API endpoints
- Security tests: as specified in "Security Requirements" column

Run `pytest tests/ -v` and include the full output in the report.

---

## AI-SDLC Verification

Before completing this ticket:
1. `pytest tests/ -v` — include exact terminal output
2. `ruff check .` — must pass with no errors
3. No secrets in any committed file (scan with detect-secrets if available)
4. Docs updated (README, API.md, ARCHITECTURE.md) if this change affects them
5. Every acceptance criterion checked off individually

---

## Human Approval Required

- Architecture decisions that deviate from `.kiro/specs/project-10/spec.md`
- Security exceptions (document and get explicit approval)
- Ambiguous requirements — stop and ask rather than guess

---

## Definition of Done

- All acceptance criteria met and evidenced with actual test output
- Code reviewed by a human reviewer (never self-approved)
- Tests actually executed — actual results reported (never invented)
- No unresolved critical defects
- Traceability: P10-7 → `docs/jira/project-10/kiro-prompts/PROJECT-10-007.md` → implementation → tests

---

## Output Report

Kiro must provide:
- **Files created:** list
- **Files modified:** list
- **Files deleted:** list
- **Tests executed:** `pytest tests/ -v` exact output
- **Test results:** N passed, N failed, N skipped
- **Evaluation results:** (where applicable)
- **Security checks:** what was checked
- **Performance observations:** (where relevant)
- **Known limitations:** (honest list)
- **Remaining risks:** (honest list)
- **Jira status recommendation:** Ready for Code Review (or blocked, with reason)
