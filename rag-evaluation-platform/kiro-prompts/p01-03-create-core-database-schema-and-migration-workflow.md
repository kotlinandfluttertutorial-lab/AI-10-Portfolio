# Kiro Prompt — P01-03: Create core database schema and migration workflow

**Project:** Enterprise Knowledge Intelligence Platform  
**Jira ticket:** `P01-03`  
**Priority:** High  
**Related spec:** `../.kiro/specs/core-workflow.md`  
**Project requirements:** `../specs/requirements.md`  
**Project design:** `../specs/design.md`

## Prompt

You are implementing Jira ticket `P01-03` for **Enterprise Knowledge Intelligence Platform**.

### Context
Organizations need grounded answers over internal documents, with traceable citations and measurable retrieval and generation quality.

### Task
Model and migrate the core entities: Workspace, Document, DocumentVersion, Chunk, Embedding, Query, RetrievedPassage, Answer, Citation, EvaluationRun, Feedback. Include ownership boundaries, indexes, timestamps, and lifecycle constraints.

### Instructions
1. Inspect the repository, current implementation, steering files, and linked specifications before making changes.
2. Identify dependencies and the smallest coherent implementation that satisfies this ticket.
3. Follow the established architecture and stack: Python 3.12, FastAPI, PostgreSQL + pgvector, object storage, React/TypeScript, Docker, pytest, OpenTelemetry.
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
