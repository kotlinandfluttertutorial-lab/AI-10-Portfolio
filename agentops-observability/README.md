# AI Agent Monitoring and Reliability Platform

**Project ID:** P05  
**Status:** In Development (P05-01 complete — skeleton initialized)

AI engineers running production agent workflows lack a unified view of trace data, tool failures, token spend, latency, and evaluation outcomes. This platform collects OpenTelemetry-compatible events from instrumented agents, stores normalized traces, computes metrics, fires alerts, and renders dashboards.

---

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Node.js 20+ (for frontend development)

---

## Getting Started

```bash
# 1. Clone and enter the project folder
cd agentops-observability/

# 2. Copy and configure environment
cp .env.example .env
# Edit .env:
#   - Set JWT_SECRET to a real secret (generate: python -c "import secrets; print(secrets.token_hex(32))")
#   - DATABASE_URL, REDIS_URL are pre-configured for docker-compose defaults

# 3. Start dependencies (PostgreSQL + Redis)
docker-compose up -d postgres redis

# 4. Install Python dependencies
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

pip install -e ".[dev]"

# 5. Run database migrations
alembic upgrade head

# 6. Start the API server
uvicorn api.main:app --reload --port 8000

# 7. (Optional) Start the worker process
python -m workers.main

# 8. (Optional) Start the frontend (in a separate terminal)
cd frontend && npm install && npm run dev
```

**Verify it's working:**
```bash
curl http://localhost:8000/health
# → {"status":"ok"}

curl http://localhost:8000/ready
# → {"status":"ready","checks":{"db":"ok","redis":"ok"}}

curl http://localhost:8000/metrics
# → Prometheus metrics

# Open http://localhost:8000/docs for the interactive API explorer
```

---

## Running Tests

```bash
# Unit tests (no database required)
pytest tests/unit/ -v

# All tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=. --cov-report=html
```

---

## Code Quality

```bash
# Lint
ruff check .

# Format
black .

# Type check
mypy api/ domain/ database/ adapters/

# Or use make:
make lint
make type-check
```

---

## Environment Variables

All configuration is in `.env`. See `.env.example` for the full list with descriptions.

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | ✅ | Async PostgreSQL connection string |
| `DATABASE_URL_SYNC` | ✅ | Sync PostgreSQL connection string (Alembic) |
| `REDIS_URL` | ✅ | Redis connection string |
| `JWT_SECRET` | ✅ | JWT signing secret — must not be a placeholder |
| `LOG_LEVEL` | optional | `INFO` (default) |
| `APP_ENV` | optional | `development` / `production` / `test` |
| `MAX_EVENTS_PER_BATCH` | optional | Max events per ingestion call (default 1000) |

---

## Project Structure

```
agentops-observability/
├── api/                  — FastAPI application (routers, middleware, config, errors)
├── database/             — SQLAlchemy session factory, declarative base
├── domain/               — Business logic, entities, exceptions
├── adapters/             — External service integrations (DB, Redis, provider)
├── workers/              — Async background workers
├── migrations/           — Alembic migration scripts
├── frontend/             — React + TypeScript dashboard
├── tests/
│   ├── conftest.py       — Shared fixtures
│   └── unit/             — Unit tests (no DB/Redis required)
├── docker-compose.yml    — Local development stack
├── Dockerfile            — Multi-stage production image
├── pyproject.toml        — Dependencies and tooling config
├── Makefile              — Common commands
└── .env.example          — Configuration template
```

---

## Implementation Progress

| Ticket | Description | Status |
|---|---|---|
| P05-01 | Repository skeleton and developer tooling | ✅ Done |
| P05-02 | Architecture documentation | ⏳ Next |
| P05-03 | Database schema and migrations | ⏳ Pending |
| P05-04 | API foundation and error contract | ⏳ Pending |
| P05-05 | Authentication and authorization | ⏳ Pending |
| P05-06 | Project and API key management | ⏳ Pending |
| P05-07 | Agent instrumentation SDK | ⏳ Pending |
| P05-08 | OpenTelemetry-compatible event schema | ⏳ Pending |
| P05-09 | Trace and span ingestion | ⏳ Pending |
| P05-10 | Model call and tool call tracking | ⏳ Pending |
| P05-11 | Token and cost estimation | ⏳ Pending |
| P05-12 | Latency and error metrics | ⏳ Pending |
| P05-13 | Trace search and filtering | ⏳ Pending |
| P05-14 | Trace detail timeline | ⏳ Pending |
| P05-15 | Dashboard widgets | ⏳ Pending |
| P05-16 | AI evaluation harness | ⏳ Pending |
| P05-17 | Observability and audit events | ⏳ Pending |
| P05-18 | Security hardening and gate | ⏳ Pending |
| P05-19 | CI/CD and deployment docs | ⏳ Pending |
| P05-20 | Integrated demo and release report | ⏳ Pending |

---

## AI-SDLC Framework

Follow `../AI-SDLC/AI-SDLC-MASTER.md`. Use `.kiro/steering/` for project-specific standards.  
Open a ticket's Kiro prompt from `kiro-prompts/pXX-NN-*.md` to implement it with Kiro.

**Human approval required before:** production deployment, security exceptions, architecture changes, release (Gate G5).
