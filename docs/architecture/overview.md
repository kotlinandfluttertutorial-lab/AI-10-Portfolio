# Portfolio Architecture Overview

This document describes shared architectural principles, technology defaults, and cross-project decisions for the AI-10 Portfolio. Each project follows this framework and deviates only through a documented ADR.

## Shared Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| Backend | Python 3.11+, FastAPI | All 10 projects |
| Database | PostgreSQL 15 + pgvector | Vector search enabled |
| Cache / Queue | Redis | Sessions, rate limiting, async jobs |
| Migrations | Alembic | Versioned, reproducible |
| Containerization | Docker + docker-compose | Local dev and CI |
| CI | GitHub Actions | Lint, test, security scan, build |
| Frontend | React + TypeScript | Projects with UIs |
| Metrics | Prometheus-compatible | All services expose /metrics |
| Tracing | OpenTelemetry | Multi-step workflow tracing |
| Logging | Structured JSON | All services, no plaintext logs |

## Common Module Structure

Every project follows this layout:

```
project-folder/
├── api/            — FastAPI routers, request/response schemas
├── domain/         — Business logic, entities, use cases
├── adapters/       — AI providers, databases, external services
├── workers/        — Async background workers
├── evaluation/     — AI quality measurement
├── tests/
│   ├── unit/
│   ├── integration/
│   └── security/
├── migrations/     — Alembic migration scripts
├── docs/           — Project-specific docs
└── docker-compose.yml
```

## Cross-Project Decisions

### ADR-001: PostgreSQL + pgvector for all projects requiring vector search
Vector search is needed by P01 (RAG), P03 (support), P08 (search). Centralizing on pgvector reduces operational complexity vs. running a separate vector database. Projects that do not need vector search omit the extension.

### ADR-002: Redis for all async queues and rate limiting
Redis is already required for session management in most projects. Using Redis Streams for queues avoids a separate message broker. Dead-letter handling is implemented as a separate Redis list.

### ADR-003: FastAPI for all backend services
Consistent framework across all 10 projects enables skills reuse, shared middleware patterns, and consistent OpenAPI documentation generation.

### ADR-004: OpenTelemetry for distributed tracing
All multi-step workflows instrument spans using the OTel SDK. P05 (AgentOps) ingests these traces. Projects export to an OTLP-compatible collector.

### ADR-005: JWT + API key dual authentication
User-facing interfaces use JWT (short-lived, refresh rotation). Machine-to-machine integrations use API keys (scoped, hashed in database). Both are validated in shared middleware.

## Security Architecture (Cross-Project)

```
[Client] → [Rate Limiter] → [Auth Middleware] → [API Layer] → [Domain Layer (AuthZ)] → [DB]
                                                                      ↕
                                                           [Provider Adapter (AI)]
```

- Authentication: enforced at middleware level, before any handler
- Authorization: enforced at domain layer, after identity is known
- AI Provider calls: budget-enforced, retry-capped, output-validated
- Audit log: written from domain layer, append-only

## Project Folder Mapping

| ID | Spec Folder | Source Folder | Primary Language |
|---|---|---|---|
| P01 | `.kiro/specs/project-01/` | `rag-evaluation-platform/` | Python + React |
| P02 | `.kiro/specs/project-02/` | `autonomous-research-agent/` | Python |
| P03 | `.kiro/specs/project-03/` | `customer-support-copilot/` | Python + React |
| P04 | `.kiro/specs/project-04/` | `voice-task-assistant/` | Python |
| P05 | `.kiro/specs/project-05/` | `agentops-observability/` | Python + React |
| P06 | `.kiro/specs/project-06/` | `document-extraction-pipeline/` | Python + React |
| P07 | `.kiro/specs/project-07/` | `multi-agent-delivery-orchestrator/` | Python |
| P08 | `.kiro/specs/project-08/` | `enterprise-semantic-search/` | Python + React |
| P09 | `.kiro/specs/project-09/` | `github-code-review-ai/` | Python |
| P10 | `.kiro/specs/project-10/` | `enterprise-prompt-security/` | Python + React |
