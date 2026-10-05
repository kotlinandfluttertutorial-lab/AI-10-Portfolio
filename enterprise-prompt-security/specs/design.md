# Design — LLM Guard and Prompt Injection Defense Platform

## Context and constraints
LLM applications face prompt injection, sensitive-data exposure, unsafe tool use, and inconsistent policy enforcement across model workflows.

## Component view
Application gateway → identity/context policy → input scanners → model/tool policy enforcement → output scanners/redaction → audit events and security analytics.

## Technology and boundaries
Python, FastAPI, Pydantic, policy engine, PostgreSQL, Redis, React/TypeScript, Docker

Keep these boundaries explicit:
- **API layer:** authentication, request validation, response mapping.
- **Domain layer:** workflow state, business rules, permissions, and invariants.
- **Application services:** coordinate use cases and transactions.
- **Adapters:** database, model provider, external APIs, queue, and storage.
- **Workers:** long-running or retryable operations.
- **UI:** user workflows only; never rely on client-side checks for authorization.

## Data and lifecycle
Entities: Application, Policy, ScanRequest, Finding, SensitiveEntity, ToolPermission, AuditEvent, TestCase, SecurityRun

For each entity, document ownership, indexes, lifecycle states, retention, and deletion. Use migrations and avoid storing raw sensitive prompts or files in telemetry by default.

## API design
Endpoints: POST /v1/scan/input; POST /v1/scan/output; POST /v1/authorize-tool; CRUD /policies; POST /security-tests; GET /audit-events

Use consistent error shape:
`{"error": {"code": "VALIDATION_ERROR", "message": "Readable explanation", "request_id": "..."}}`

Use pagination for collections, request IDs for support, and idempotency keys for retried external events or side-effecting submissions.

## AI/provider integration
- Define a provider interface with typed inputs and outputs.
- Validate structured output at the boundary.
- Add timeouts, bounded retries, and provider error classification.
- Record model and prompt version when needed for evaluation.
- Keep untrusted content clearly separated from system instructions.
- Include fallback/review behavior for uncertain results.

## Security design
Threats: False negatives, bypass techniques, overblocking, sensitive logging, policy misconfiguration

Enforce authorization server-side. Redact secrets and sensitive fields from logs. Verify webhook signatures where applicable. Apply rate limits and size limits to public or expensive endpoints.

## Observability
Capture request IDs, workflow IDs, state transitions, duration, provider latency, errors, and cost-relevant usage. Avoid high-cardinality labels and sensitive payload capture.

## Testing design
Use unit, adapter contract, integration, end-to-end, security, and evaluation tests. Pin deterministic fixtures; mock nondeterministic providers in ordinary CI and run controlled live-provider checks separately.

## Deployment
Use environment-based configuration, health/readiness checks, migrations, container image scanning, and documented rollback steps.
