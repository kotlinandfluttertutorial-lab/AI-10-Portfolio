# Design — Autonomous Market Research Analyst

## Context and constraints
Research work is fragmented across sources and requires repeatable planning, evidence collection, synthesis, and citation.

## Component view
Research request → planner → bounded search/retrieval tools → evidence store → synthesis agent → citation verifier → human review → report export. Persist graph state and tool traces.

## Technology and boundaries
Python, FastAPI, LangGraph, PostgreSQL, Redis, search provider adapter, React/TypeScript, Docker

Keep these boundaries explicit:
- **API layer:** authentication, request validation, response mapping.
- **Domain layer:** workflow state, business rules, permissions, and invariants.
- **Application services:** coordinate use cases and transactions.
- **Adapters:** database, model provider, external APIs, queue, and storage.
- **Workers:** long-running or retryable operations.
- **UI:** user workflows only; never rely on client-side checks for authorization.

## Data and lifecycle
Entities: ResearchJob, PlanStep, Source, Evidence, ToolCall, Finding, Report, ReviewDecision

For each entity, document ownership, indexes, lifecycle states, retention, and deletion. Use migrations and avoid storing raw sensitive prompts or files in telemetry by default.

## API design
Endpoints: POST /research-jobs; GET /research-jobs/{id}; POST /research-jobs/{id}/approve; GET /reports/{id}; POST /tools/search

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
Threats: Untrusted web content, fabricated citations, runaway tool loops, source duplication, excessive cost

Enforce authorization server-side. Redact secrets and sensitive fields from logs. Verify webhook signatures where applicable. Apply rate limits and size limits to public or expensive endpoints.

## Observability
Capture request IDs, workflow IDs, state transitions, duration, provider latency, errors, and cost-relevant usage. Avoid high-cardinality labels and sensitive payload capture.

## Testing design
Use unit, adapter contract, integration, end-to-end, security, and evaluation tests. Pin deterministic fixtures; mock nondeterministic providers in ordinary CI and run controlled live-provider checks separately.

## Deployment
Use environment-based configuration, health/readiness checks, migrations, container image scanning, and documented rollback steps.
