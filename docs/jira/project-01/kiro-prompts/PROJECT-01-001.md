# Kiro Implementation Prompt

**Project:** P01 — Enterprise Knowledge Intelligence Platform  
**Jira:** P01-01  
**AI-SDLC Phase:** BUILD  
**Title:** Initialize Enterprise Knowledge Intelligence Platform repository and developer tooling

---

## Objective

Create the complete application skeleton for the Enterprise Knowledge Intelligence Platform. This ticket establishes the repository structure, local development environment, tooling configuration, and CI pipeline that all subsequent tickets depend on. The result must be a fully runnable local stack that any developer can clone, configure, and start in under 15 minutes.

---

## Context

**Project folder:** `rag-evaluation-platform/`  
**Project spec:** `.kiro/specs/project-01/spec.md`  
**Requirements:** `rag-evaluation-platform/specs/requirements.md`  
**Design:** `rag-evaluation-platform/specs/design.md`  
**Architecture steering:** `.kiro/steering/architecture.md`  
**Engineering steering:** `.kiro/steering/engineering.md`  
**Technology defaults:** Python 3.11+, FastAPI, PostgreSQL + pgvector, Redis, React + TypeScript + Vite, Docker, GitHub Actions CI

---

## Dependencies

None — this is the foundation ticket.

---

## Implementation Requirements

1. **Backend skeleton:** FastAPI app in `api/` directory with: `main.py` (app factory), `routers/health.py` (GET /health, GET /ready), middleware for request ID injection, structured JSON logging (structlog or python-json-logger), Prometheus metrics stub (prometheus-fastapi-instrumentator)
2. **Database:** `docker-compose.yml` with postgres service (postgres:15 with pgvector extension init script), redis service, api service, worker service stub
3. **Migrations:** Alembic configured with `migrations/` directory, `alembic.ini`, initial empty migration
4. **Frontend:** React + TypeScript + Vite scaffold in `frontend/` directory with ESLint + Prettier configured
5. **Tooling:** `pyproject.toml` or `requirements.txt` + `requirements-dev.txt` with pinned versions. `ruff.toml` configuration. `mypy.ini`. `pytest.ini` with test discovery config
6. **Environment:** `.env.example` listing all required variables (DATABASE_URL, REDIS_URL, OPENAI_API_KEY, JWT_SECRET, LOG_LEVEL). `.gitignore` including `.env`
7. **Makefile:** targets: `make dev` (start docker-compose), `make test` (run pytest), `make lint` (ruff + mypy), `make migrate` (alembic upgrade head)
8. **CI:** `.github/workflows/ci.yml` with steps: checkout, setup-python, install-deps, ruff lint, mypy type-check, pytest, docker-compose build

---

## Technical Constraints

- Python 3.11+ only
- All dependencies pinned to exact versions
- No secrets in any committed file — `.env` in `.gitignore`
- pgvector extension enabled via `docker/init.sql`: `CREATE EXTENSION IF NOT EXISTS vector;`
- FastAPI app uses application factory pattern (`create_app()` function)
- Non-root user in Dockerfile
- `GET /health` returns `{"status": "ok"}` always; `GET /ready` checks DB and Redis connectivity

---

## Files to Inspect

Before creating any files, inspect:
- `rag-evaluation-platform/` — check if any files already exist
- `.kiro/steering/architecture.md` — technology defaults section
- `.kiro/steering/engineering.md` — dependency management and CI requirements

---

## Expected Changes

**Backend:**
- `rag-evaluation-platform/api/main.py`
- `rag-evaluation-platform/api/routers/health.py`
- `rag-evaluation-platform/domain/__init__.py`
- `rag-evaluation-platform/adapters/__init__.py`
- `rag-evaluation-platform/workers/__init__.py`
- `rag-evaluation-platform/migrations/env.py`, `alembic.ini`

**Infrastructure:**
- `rag-evaluation-platform/docker-compose.yml`
- `rag-evaluation-platform/Dockerfile`
- `rag-evaluation-platform/docker/init.sql`

**Frontend:**
- `rag-evaluation-platform/frontend/` (Vite scaffold)

**Config:**
- `rag-evaluation-platform/pyproject.toml`
- `rag-evaluation-platform/requirements.txt`, `requirements-dev.txt`
- `rag-evaluation-platform/.env.example`
- `rag-evaluation-platform/Makefile`
- `rag-evaluation-platform/.github/workflows/ci.yml`

**Tests:**
- `rag-evaluation-platform/tests/__init__.py`
- `rag-evaluation-platform/tests/test_health.py` (smoke test)

---

## Acceptance Criteria

1. `docker-compose up` starts postgres, redis, api, and frontend without errors
2. `pytest tests/` exits 0 with at least the smoke test passing
3. `ruff check .` passes with no errors
4. `mypy api/` passes with no errors
5. `GET /health` returns `200 {"status": "ok"}`
6. `GET /ready` returns `200` when DB and Redis are reachable, `503` otherwise
7. `.env.example` lists all required environment variables with descriptions
8. README documents exact clone→configure→run steps that work without prior knowledge

---

## Testing

- **Unit:** `tests/test_health.py` — smoke test that app creates without error, /health returns 200
- **Integration:** `tests/integration/test_health_integration.py` — /ready returns 200 with docker-compose running
- **CI:** GitHub Actions workflow runs lint + type-check + pytest on every push

---

## AI-SDLC Verification

Before completing:
1. Verify `docker-compose up` actually starts all services without errors
2. Verify `pytest` actually runs and passes
3. Verify `ruff` and `mypy` actually pass
4. Check `.gitignore` contains `.env`
5. Check `.env.example` has no real secret values — only placeholders like `your-secret-here`
6. Verify README setup steps are copy-pasteable and correct

---

## Human Approval Required

- Dependency version choices (if deviating from latest stable)
- Any architecture deviation from the spec

---

## Definition of Done

- [ ] All acceptance criteria met and evidenced
- [ ] All tests passing (commands and results reported)
- [ ] No secrets in committed files (verified)
- [ ] README setup steps work from a clean checkout
- [ ] CI pipeline runs and passes
- [ ] Human reviewer approved PR

---

## Output Report

Kiro must report:
- Files created (list)
- Files modified (list)
- Test command run and result: `pytest tests/ -v` → N passed
- Lint result: `ruff check .` → OK
- Type check result: `mypy api/` → Success
- Docker: `docker-compose up -d` → all services healthy
- Known limitations
- Remaining risks
- **Jira status recommendation:** Ready for Code Review
