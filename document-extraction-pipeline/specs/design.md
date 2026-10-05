# Design — Intelligent Invoice and Contract Processing System

## Context and constraints
Operations teams manually extract business fields from semi-structured documents and need validation, exception handling, and auditable exports.

## Component view
Upload → malware/type validation → OCR/layout extraction → schema-based field extraction → deterministic validation → confidence routing → reviewer queue → export/integration.

## Technology and boundaries
Python, FastAPI, OCR adapter, Pydantic, PostgreSQL, object storage, Celery/RQ, React/TypeScript, Docker

Keep these boundaries explicit:
- **API layer:** authentication, request validation, response mapping.
- **Domain layer:** workflow state, business rules, permissions, and invariants.
- **Application services:** coordinate use cases and transactions.
- **Adapters:** database, model provider, external APIs, queue, and storage.
- **Workers:** long-running or retryable operations.
- **UI:** user workflows only; never rely on client-side checks for authorization.

## Data and lifecycle
Entities: Document, ExtractionJob, FieldResult, ValidationRule, ReviewTask, Correction, ExportBatch, AuditEvent

For each entity, document ownership, indexes, lifecycle states, retention, and deletion. Use migrations and avoid storing raw sensitive prompts or files in telemetry by default.

## API design
Endpoints: POST /documents; POST /extraction-jobs; GET /jobs/{id}; GET /review-queue; PATCH /review-tasks/{id}; POST /exports

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
Threats: OCR errors, hallucinated fields, inconsistent schemas, malicious files, low-confidence automation

Enforce authorization server-side. Redact secrets and sensitive fields from logs. Verify webhook signatures where applicable. Apply rate limits and size limits to public or expensive endpoints.

## Observability
Capture request IDs, workflow IDs, state transitions, duration, provider latency, errors, and cost-relevant usage. Avoid high-cardinality labels and sensitive payload capture.

## Testing design
Use unit, adapter contract, integration, end-to-end, security, and evaluation tests. Pin deterministic fixtures; mock nondeterministic providers in ordinary CI and run controlled live-provider checks separately.

## Deployment
Use environment-based configuration, health/readiness checks, migrations, container image scanning, and documented rollback steps.
