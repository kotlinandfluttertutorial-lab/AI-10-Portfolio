# Design — Smart Customer Service Assistant

## Context and constraints
Support teams spend time searching policies, classifying tickets, and drafting repetitive responses while maintaining accuracy and escalation controls.

## Component view
Conversation gateway → intent and sentiment signals → customer/ticket context → knowledge retrieval → response draft → policy checks → agent approval/send. Ticket events feed analytics.

## Technology and boundaries
Python, FastAPI, PostgreSQL, Redis, RAG service, React/TypeScript, WebSockets, Docker

Keep these boundaries explicit:
- **API layer:** authentication, request validation, response mapping.
- **Domain layer:** workflow state, business rules, permissions, and invariants.
- **Application services:** coordinate use cases and transactions.
- **Adapters:** database, model provider, external APIs, queue, and storage.
- **Workers:** long-running or retryable operations.
- **UI:** user workflows only; never rely on client-side checks for authorization.

## Data and lifecycle
Entities: Customer, Conversation, Message, Ticket, Intent, SuggestedReply, KnowledgeArticle, Escalation, Feedback

For each entity, document ownership, indexes, lifecycle states, retention, and deletion. Use migrations and avoid storing raw sensitive prompts or files in telemetry by default.

## API design
Endpoints: POST /conversations; POST /messages; GET /tickets/{id}; POST /tickets/{id}/classify; POST /replies/{id}/approve; GET /analytics

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
Threats: Incorrect advice, privacy exposure, over-automation, stale policies, biased sentiment classification

Enforce authorization server-side. Redact secrets and sensitive fields from logs. Verify webhook signatures where applicable. Apply rate limits and size limits to public or expensive endpoints.

## Observability
Capture request IDs, workflow IDs, state transitions, duration, provider latency, errors, and cost-relevant usage. Avoid high-cardinality labels and sensitive payload capture.

## Testing design
Use unit, adapter contract, integration, end-to-end, security, and evaluation tests. Pin deterministic fixtures; mock nondeterministic providers in ordinary CI and run controlled live-provider checks separately.

## Deployment
Use environment-based configuration, health/readiness checks, migrations, container image scanning, and documented rollback steps.
