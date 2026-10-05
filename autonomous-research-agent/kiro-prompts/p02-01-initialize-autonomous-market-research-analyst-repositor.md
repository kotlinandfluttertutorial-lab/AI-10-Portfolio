# Kiro Prompt — P02-01: Initialize Autonomous Market Research Analyst repository and developer tooling

**Project:** Autonomous Market Research Analyst  
**Jira ticket:** `P02-01`  
**Priority:** High  
**Related spec:** `../.kiro/specs/core-workflow.md`  
**Project requirements:** `../specs/requirements.md`  
**Project design:** `../specs/design.md`

## Prompt

You are implementing Jira ticket `P02-01` for **Autonomous Market Research Analyst**.

### Context
Research work is fragmented across sources and requires repeatable planning, evidence collection, synthesis, and citation.

### Task
Create the application skeleton, local run commands, environment template, linting, formatting, type checks, and test conventions.

### Instructions
1. Inspect the repository, current implementation, steering files, and linked specifications before making changes.
2. Identify dependencies and the smallest coherent implementation that satisfies this ticket.
3. Follow the established architecture and stack: Python, FastAPI, LangGraph, PostgreSQL, Redis, search provider adapter, React/TypeScript, Docker.
4. Keep domain logic separate from external provider or infrastructure code.
5. Validate all external inputs and model/provider outputs. Apply least privilege and avoid logging secrets or sensitive payloads.
6. Add or update automated tests for normal behavior, edge cases, and expected failures.
7. Update API, architecture, configuration, or user documentation if this change affects them.
8. Do not invent credentials, provider capabilities, or successful test results. Use mocks or clearly documented local substitutes when external services are unavailable.
9. If requirements conflict or a contract is missing, stop and report the specific ambiguity rather than making a risky assumption.

### Acceptance criteria
- The implementation satisfies the Jira ticket description.
- Automated tests cover the main success path and relevant failure/authorization cases.
- Existing tests remain passing; do not delete or weaken tests to obtain a pass.
- Errors and workflow status are actionable and observable.
- Documentation and traceability are updated where needed.

### Expected output
- Implemented code and tests.
- Any required migration/configuration/documentation changes.
- A concise completion report listing files changed, commands run, actual test results, assumptions, risks, and remaining work.

## AI-SDLC controls

Follow `../../AI-SDLC/AI-SDLC-MASTER.md`.
- Confirm the ticket meets Definition of Ready before implementation.
- Keep changes ticket-scoped and preserve Jira → spec → prompt → PR → test evidence traceability.
- Human review is required before merge; never self-approve or deploy to production.
- Report actual test commands/results and distinguish unrun checks from passing checks.
- Escalate ambiguous requirements, architecture changes, or material security/privacy risks.
