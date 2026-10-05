# Architecture Steering File

## Overview

This file defines the architectural principles, patterns, and constraints that apply across all 10 projects in the AI-10 Portfolio. Every project must follow these guidelines. Project-specific deviations require an Architecture Decision Record (ADR) and human approval.

---

## 1. Modular Architecture

Each project is structured as a set of independently testable, deployable modules with clear ownership boundaries.

**Rules:**
- No circular dependencies between modules
- Each module exposes a typed public interface; internal implementation is private
- Modules communicate through defined interfaces, not direct internal calls
- Module boundaries align with domain boundaries (e.g., ingestion, retrieval, evaluation are separate)
- Keep domain logic separate from infrastructure code (database, HTTP clients, message queues)

**Standard module categories:**
- `api/` — HTTP handlers, request/response schemas, routing
- `domain/` — Core business logic, entities, use cases
- `adapters/` — Provider-specific integrations (AI providers, databases, queues)
- `workers/` — Async background processing
- `sdk/` — Client-facing SDKs where applicable
- `evaluation/` — AI quality measurement
- `tests/` — All test types

---

## 2. API and Domain Separation

**Rules:**
- API layer translates HTTP requests into domain calls; it does not contain business logic
- Domain layer contains business rules and is independent of HTTP, databases, and AI providers
- Domain entities are plain data objects; no ORM or provider dependencies leak into them
- API versioning is explicit: all routes start with `/v1/`
- API contracts are documented in OpenAPI format before implementation

**Error contract:**
- All APIs return a consistent error envelope: `{ "error": { "code": string, "message": string, "request_id": string } }`
- HTTP status codes follow standard semantics (400 = client error, 401 = unauthenticated, 403 = forbidden, 404 = not found, 422 = validation error, 429 = rate limited, 500 = server error)
- Never expose stack traces or internal details in error responses
- All errors include a `request_id` for correlation

---

## 3. Provider Abstraction

All AI provider integrations (LLMs, embedding models, speech-to-text, vision) are placed behind interfaces.

**Rules:**
- Define a provider interface (abstract class or protocol) in the domain or adapters layer
- Concrete provider implementations live in `adapters/` — never directly in domain or API layers
- Provider selection is configuration-driven, not hardcoded
- Every provider adapter logs request/response metadata (model, tokens used, latency) without logging sensitive payload content
- Budget and retry limits are enforced at the provider adapter boundary
- Fallback behavior on provider failure must be explicit: either fail-closed or fail-open with documented justification

**Supported provider pattern:**
```
domain/ports/llm_provider.py  — interface
adapters/openai_adapter.py    — concrete implementation
adapters/anthropic_adapter.py — concrete implementation
config/providers.yaml         — provider selection
```

---

## 4. Database Boundaries

**Rules:**
- Each project owns its own schema; no cross-project joins
- All schema changes are managed through versioned migrations (Alembic for Python, Flyway/Liquibase for Java)
- No raw SQL in domain or API layers; use query builders or ORMs with typed models
- Database credentials are always environment variables, never hardcoded
- All tables include: `id`, `created_at`, `updated_at` at minimum
- Soft deletes preferred over hard deletes for auditable entities
- Indexes defined in migration files, not applied manually
- Connection pools are sized explicitly; defaults are documented

**Vector database:**
- pgvector is the default; Pinecone/Weaviate/Qdrant are allowed via adapter
- Embedding model version is stored alongside each embedding
- Re-indexing strategy is documented when model versions change

---

## 5. Async Processing

Use async processing for: document ingestion, embedding generation, AI inference on large inputs, report generation, alert delivery, and any operation that may exceed 5 seconds.

**Rules:**
- Use message queues (Redis Streams, RabbitMQ, or similar) for async work items
- Every async job has: a unique job ID, status tracking (pending/running/completed/failed), retry count, and expiry
- Async jobs are idempotent: running the same job twice produces the same outcome
- Dead-letter queues capture permanently failed jobs
- Job status is queryable via API
- Async worker failures are observable: logged, metered, and alertable

---

## 6. Event-Driven Processing

Use event-driven patterns where components need to react to state changes without tight coupling.

**Rules:**
- Events are named in past tense: `document.ingested`, `trace.completed`, `alert.triggered`
- Event schemas are versioned and documented
- Event consumers are idempotent
- Events include: `event_id`, `event_type`, `timestamp`, `source`, `payload`
- Do not use events for synchronous request/response flows

---

## 7. Error Handling

**Rules:**
- Never swallow exceptions silently; always log with context
- Distinguish between: recoverable errors (retry), permanent errors (fail), and ambiguous errors (alert + human review)
- Use structured error types: do not use generic `Exception` at domain boundaries
- AI-generated outputs that fail validation are treated as permanent errors and logged with the raw output for debugging
- External service failures trigger circuit breakers or exponential backoff with jitter
- All error paths are tested explicitly

---

## 8. Observability

Every project must be observable from day one.

**Required signals:**
- **Structured logs:** JSON format, include `request_id`, `trace_id`, `user_id` (or anonymized), `event_type`, `duration_ms`, `status`
- **Metrics:** Request count, error rate, latency percentiles (p50/p95/p99), queue depth, worker throughput
- **AI metrics:** Token usage per request, model latency, cost estimate, evaluation scores
- **Traces:** Distributed tracing on multi-step workflows (OpenTelemetry compatible)
- **Health endpoints:** `GET /health` (liveness) and `GET /ready` (readiness) on every service

**Rules:**
- No secrets, PII, or full AI payloads in logs
- All log lines include a correlation ID
- Dashboards are documented in `docs/operations/`
- Alerting rules are version-controlled

---

## 9. Scalability

Design for horizontal scalability from the start even if deployed as a monolith initially.

**Rules:**
- No in-process state that cannot be reconstructed from the database
- Session state stored externally (Redis or database)
- Background workers are stateless; they read from queue and write to database
- Rate limiting is applied at the API gateway or middleware level, not in domain logic
- Configuration for scale (worker count, pool size, cache TTL) is environment-variable-driven

---

## 10. Security Boundaries

Security controls are enforced at defined boundaries, not scattered through application code.

**Boundaries:**
- **Ingress boundary:** Input validation, rate limiting, authentication
- **Authorization boundary:** Permission checks before any domain operation
- **Provider boundary:** Budget enforcement, output validation, prompt injection detection
- **Storage boundary:** Encryption at rest, access controls, audit logging
- **Egress boundary:** Output sanitization, PII redaction, secret scanning

**Rules:**
- Authentication is checked before any authenticated endpoint is reached
- Authorization is checked inside the domain layer, not only at the API layer
- Never trust input from external sources (users, files, web content, AI output) without validation
- Prompt injection detection is applied to all user-supplied text that reaches an LLM
- All security boundary violations are logged and alertable

---

## 11. Technology Defaults

These are the default technology choices. Deviations require an ADR.

| Concern | Default |
|---|---|
| Backend language | Python 3.11+ |
| API framework | FastAPI |
| Database | PostgreSQL with pgvector |
| Cache / queue | Redis |
| Migrations | Alembic |
| Testing | pytest |
| Linting / formatting | ruff, black |
| Type checking | mypy |
| Frontend | React + TypeScript |
| Containerization | Docker + docker-compose |
| CI | GitHub Actions |
| Metrics | Prometheus-compatible |
| Tracing | OpenTelemetry |
| Secret management | Environment variables; Vault for production |

---

## 12. Architecture Decision Records

Every material architectural decision must be documented as an ADR.

**ADR format:**
```
# ADR-XXX: Title
Status: Proposed | Accepted | Deprecated | Superseded
Date: YYYY-MM-DD
Context: What problem are we solving?
Decision: What did we decide?
Consequences: What are the trade-offs?
Alternatives considered: What else was evaluated?
```

Store ADRs in `docs/architecture/`.
