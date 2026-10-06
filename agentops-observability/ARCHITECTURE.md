# Architecture — AI Agent Monitoring and Reliability Platform (P05)

**Version:** 1.0  
**Status:** Accepted  
**Last updated:** 2026-10-05

---

## 1. System Overview

AgentOps is an observability platform for AI agent workflows. It collects OpenTelemetry-compatible events from instrumented Python agents, stores normalized trace and span data, computes latency/cost/error metrics, fires configurable alerts, and renders a React dashboard.

The platform is not an AI system itself — it is infrastructure that makes AI systems observable. No LLM inference is required for the core platform.

---

## 2. Primary Flows

### 2a — Event Ingestion Flow

```
Instrumented Agent (Python)
      │
      │  HTTP POST /v1/events  (batch, OTLP-compatible JSON)
      ▼
┌─────────────────────┐
│   API — /v1/events  │  ← API key auth, rate limiting, payload size limit
│   (FastAPI)         │
└─────────┬───────────┘
          │  enqueue batch
          ▼
┌─────────────────────┐
│   Redis Stream      │  ← agentops:events stream, acknowledgement before processing
│   (ingestion queue) │
└─────────┬───────────┘
          │  consume
          ▼
┌─────────────────────┐
│  Normalization      │  ← parse events → TraceEvent | SpanEvent |
│  Worker             │     ModelCallEvent | ToolCallEvent
└─────────┬───────────┘
          │  write
          ▼
┌─────────────────────┐
│  PostgreSQL         │  ← traces, spans, model_calls, tool_calls tables
│  (trace store)      │
└─────────────────────┘
```

### 2b — Metric Aggregation Flow

```
PostgreSQL (trace store)
      │
      │  reads traces + spans every 5 minutes
      ▼
┌─────────────────────┐
│  Aggregation Worker │  ← computes p50/p95/p99 latency, error rate,
│                     │     token totals, cost estimates
└─────────┬───────────┘
          │  writes
          ▼
┌─────────────────────┐    ┌─────────────────────┐
│  metric_points      │    │  Alert Engine        │
│  (PostgreSQL)       │───▶│  (evaluates rules,   │
└─────────────────────┘    │   fires alert_events)│
                           └─────────────────────┘
```

### 2c — Dashboard Query Flow

```
React Dashboard
      │
      │  JWT auth  GET /v1/traces, GET /v1/metrics, GET /v1/alerts
      ▼
┌─────────────────────┐
│   API layer         │  ← project isolation enforced (project_id from JWT)
│   (FastAPI)         │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Domain layer       │  ← query builders, filter validation,
│                     │     business rules
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  PostgreSQL         │
└─────────────────────┘
```

---

## 3. Component Responsibilities

| Component | Location | Responsibilities |
|---|---|---|
| **API layer** | `api/` | HTTP routing, authentication, request validation, response mapping, rate limiting |
| **Domain layer** | `domain/` | Business rules, entity definitions, use cases, permissions, invariants |
| **Database session** | `database/` | SQLAlchemy async session factory, Alembic base, Redis client |
| **Adapters** | `adapters/` | External integrations (DB queries, Redis queue, alert delivery) |
| **Normalization worker** | `workers/normalization_worker.py` | Dequeue events → parse → write to trace store (idempotent) |
| **Aggregation worker** | `workers/aggregation_worker.py` | Compute periodic metrics, evaluate alert rules |
| **SDK** | `sdk/python/agentops/` | Python instrumentation library used by agent authors |
| **Frontend** | `frontend/` | React dashboard — reads from API only, never directly from DB |

**Boundaries enforced:**
- API layer does not contain business logic — it delegates to domain
- Domain layer has no imports from `api/`, `adapters/`, or `database/`
- Adapters do not contain business rules
- Frontend authorization is never trusted — all checks are server-side

---

## 4. Data Model (Key Entities)

```
projects          ←── api_keys
    │
    └── traces
           │
           └── spans
                  │
                  ├── model_calls
                  └── tool_calls

projects ──► metric_points
projects ──► alert_rules ──► alert_events
```

### Entity lifecycle states

| Entity | States |
|---|---|
| `traces` | `running → completed \| failed` |
| `spans` | `running → completed \| failed \| error` |
| `alert_events` | `triggered → resolved` |

---

## 5. API Design

All endpoints versioned under `/v1/`. Error responses follow the portfolio envelope:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable explanation.",
    "request_id": "req_abc123",
    "details": [{"field": "model", "message": "Field required."}]
  }
}
```

Key endpoints (full spec implemented in P05-04):
```
POST   /v1/events              — batch event ingestion (SDK → platform)
GET    /v1/traces              — list traces with filters + pagination
GET    /v1/traces/{id}         — trace with full span tree
GET    /v1/metrics             — time-series metrics
GET    /v1/metrics/summary     — cost/error/latency summary
CRUD   /v1/alert-rules         — alert rule management
GET    /v1/alerts              — triggered alerts
CRUD   /v1/projects            — project management
POST   /v1/projects/{id}/api-keys
GET    /health                 — liveness
GET    /ready                  — readiness (DB + Redis)
GET    /metrics                — Prometheus metrics
```

---

## 6. Security Architecture

```
[Client / SDK]
      │
      │  TLS
      ▼
[Rate Limiter + Payload Size Check]  ← enforced at API layer
      │
      │  X-API-Key or Authorization: Bearer <jwt>
      ▼
[Auth Middleware]  ← extracts identity, attaches project_id to request context
      │
      ▼
[API Handler]  ← validates request schema
      │
      ▼
[Domain Layer]  ← authorization check using project_id from context
      │          (never from request params)
      ▼
[Adapter / Database]  ← project_id always in WHERE clause
```

Key controls:
- API keys stored as bcrypt hashes — plain text returned only at creation
- Sensitive event payloads not stored by default (only metadata: token counts, latency, status)
- project_id is always sourced from the authenticated context — never a request parameter
- Rate limiting applied per API key (ingestion) and per user (dashboard)

---

## 7. Observability of the Platform Itself

The platform must be observable:
- Structured JSON logs (structlog) on every request with `request_id`, `project_id`
- Prometheus metrics at `/metrics`: `ingestion_events_total`, `worker_processing_time_ms`, `alert_evaluations_total`
- `GET /health` (liveness) and `GET /ready` (readiness, checks DB + Redis)
- Audit events for API key creation/revocation (append-only, admin-read-only)

---

## 8. Deployment Architecture

```
docker-compose (local):
  postgres:15    ← trace store, metric_points, alert rules
  redis:7        ← ingestion queue (Redis Streams), session/rate-limit cache
  api            ← FastAPI, uvicorn, 8000
  worker         ← normalization + aggregation workers
  frontend       ← Vite dev / nginx static (5173)
```

Production topology (documented in DEPLOYMENT.md — ticket P05-19):
- Separate scaling groups for API and workers
- Postgres with connection pooling (PgBouncer)
- Redis with persistence enabled
- Health checks and readiness probes on all containers

---

## 9. Failure Modes and Recovery

| Failure | Behavior |
|---|---|
| Database unavailable | `/ready` returns 503. API returns 503 on DB-dependent requests. Workers retry with backoff. |
| Redis unavailable | `/ready` returns 503. Ingestion returns 503. Workers retry with backoff. |
| Malformed event in queue | Event moved to dead-letter list (`agentops:events:dlq`). Logged with event_id. Normalization continues. |
| Aggregation worker crash | Worker restarts via process supervisor. Aggregation runs on the next 5-minute cycle. No data loss — metric_points are idempotent. |
| Alert delivery failure | Alert event marked `delivery_failed`. Retried up to 3 times with exponential backoff. |
| SDK can't reach platform | SDK fails silently by default (`safe_on_error=True`). Agent code continues unaffected. |

---

## 10. Scalability Notes

- Workers are stateless — they read from the queue and write to the database. Multiple worker instances can run safely.
- Redis Streams support consumer groups — multiple normalization workers can consume from the same stream in parallel.
- API is stateless — horizontal scaling behind a load balancer with no session affinity required.
- Metric aggregation uses time-bucketed writes to `metric_points` — idempotent on re-run.
- The schema is designed for future time-partitioning of `traces` and `spans` by `created_at`.

---

## 11. Key Design Decisions

See ADRs in `docs/architecture/`:
- `ADR-P05-001` — Redis Streams for event ingestion queue
- `ADR-P05-002` — PostgreSQL for trace storage (not a dedicated time-series DB)
- `ADR-P05-003` — API key hashing with bcrypt
