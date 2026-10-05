# Design — AI Pull Request Review and Quality Assistant

## Context and constraints
Reviewers need contextual, actionable feedback on pull requests without noisy comments, secret exposure, or unsafe automated changes.

## Component view
GitHub webhook → signature verification → diff/context fetch → static checks → LLM review with repository rules → finding deduplication and severity policy → draft PR comments/check run.

## Technology and boundaries
Python, FastAPI, GitHub App API, LLM provider adapter, static analysis tools, PostgreSQL, queue worker, Docker

Keep these boundaries explicit:
- **API layer:** authentication, request validation, response mapping.
- **Domain layer:** workflow state, business rules, permissions, and invariants.
- **Application services:** coordinate use cases and transactions.
- **Adapters:** database, model provider, external APIs, queue, and storage.
- **Workers:** long-running or retryable operations.
- **UI:** user workflows only; never rely on client-side checks for authorization.

## Data and lifecycle
Entities: Repository, Installation, PullRequest, ReviewRun, Finding, RuleSet, Comment, WebhookEvent

For each entity, document ownership, indexes, lifecycle states, retention, and deletion. Use migrations and avoid storing raw sensitive prompts or files in telemetry by default.

## API design
Endpoints: POST /webhooks/github; POST /repositories/{id}/review-rules; GET /reviews/{id}; POST /reviews/{id}/publish; GET /health

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
Threats: Prompt injection in code/comments, false positives, secret leakage, webhook replay, excessive permissions

Enforce authorization server-side. Redact secrets and sensitive fields from logs. Verify webhook signatures where applicable. Apply rate limits and size limits to public or expensive endpoints.

## Observability
Capture request IDs, workflow IDs, state transitions, duration, provider latency, errors, and cost-relevant usage. Avoid high-cardinality labels and sensitive payload capture.

## Testing design
Use unit, adapter contract, integration, end-to-end, security, and evaluation tests. Pin deterministic fixtures; mock nondeterministic providers in ordinary CI and run controlled live-provider checks separately.

## Deployment
Use environment-based configuration, health/readiness checks, migrations, container image scanning, and documented rollback steps.
