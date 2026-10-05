# Portfolio Operations Guide

This document covers shared operational patterns, runbook templates, and CI/CD documentation for the AI-10 Portfolio.

## Local Development (All Projects)

Every project follows the same local dev workflow:

```bash
# 1. Clone and enter project folder
cd <project-folder>

# 2. Copy and configure environment
cp .env.example .env
# Edit .env: add your API keys and database credentials

# 3. Start dependencies
docker-compose up -d db redis

# 4. Install Python dependencies
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-dev.txt

# 5. Run database migrations
alembic upgrade head

# 6. Start the API server
uvicorn api.main:app --reload --port 8000

# 7. (Optional) Start background workers
python workers/main.py
```

Frontend projects add:
```bash
cd frontend
npm install
npm run dev
```

## Running Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests (requires Docker)
docker-compose -f docker-compose.test.yml up -d
pytest tests/integration/ -v
docker-compose -f docker-compose.test.yml down

# All tests with coverage
pytest --cov=. --cov-report=html

# Security tests only
pytest tests/security/ -v -m security

# AI evaluation
python evaluation/runners/run_eval.py --dataset evaluation/datasets/v1.0/eval_set.jsonl
```

## CI/CD Pipeline (GitHub Actions)

Every project has `.github/workflows/ci.yml` that runs on every PR and push to main:

```
1. Lint (ruff)
2. Type check (mypy)
3. Secret scan (detect-secrets)
4. Dependency vulnerability scan (pip-audit)
5. Unit tests
6. Integration tests (Docker services)
7. API contract tests (schemathesis)
8. Security tests
9. Build Docker image
10. (On main merge) Push image to registry
```

The pipeline blocks merge on any step failure.

## Health Monitoring

All services expose:
- `GET /health` — liveness probe (process alive)
- `GET /ready` — readiness probe (dependencies reachable)
- `GET /metrics` — Prometheus metrics

Key metrics to monitor:
- `http_requests_total` by status code (error rate)
- `http_request_duration_seconds` p99 (latency)
- `ai_tokens_used_total` (cost tracking)
- `queue_depth` (async job backlog)
- `worker_errors_total` (worker failure rate)

## Runbook Template

Store project runbooks in each project's `OPERATIONS.md`. Use this template:

```markdown
## Runbook: [Alert Name or Issue Type]

**Severity:** [P1/P2/P3]
**Team:** [Who responds]

### Symptoms
- [Observable symptom 1]
- [Observable symptom 2]

### Immediate Actions
1. [First thing to check]
2. [First thing to try]

### Investigation Steps
1. Check logs: `kubectl logs ... | grep ERROR`
2. Check metrics dashboard: [link or query]
3. Check recent deployments: `git log --oneline -5`

### Resolution
- [Common cause 1 → fix]
- [Common cause 2 → fix]

### Escalation
If not resolved in [N minutes], escalate to [team/person].

### Post-Incident
- [ ] Incident report filed
- [ ] Runbook updated if new learnings
- [ ] Regression test added if a bug was found
```

## Deployment Checklist

Before every production deployment:
```
[ ] CI pipeline passed (all checks green)
[ ] Security gate checklist completed
[ ] Database migrations tested on a staging database
[ ] Rollback plan documented and tested
[ ] Health checks passing on the new image
[ ] Observability (dashboards, alerts) confirmed working
[ ] Release notes prepared
[ ] Human approval obtained (Gate G5)
[ ] Deployment performed during a low-traffic window
[ ] Post-deployment health check passed
[ ] Jira tickets marked Released
```

## Cost Management

Track and alert on:
- `ai_tokens_used_total` per model per day
- Cost estimate per request (calculated from token counts × per-token price)
- Monthly cost trend vs. budget

Set alerts when:
- Daily token usage exceeds 150% of the 7-day average
- Cost per request for a specific operation exceeds 2× the baseline
