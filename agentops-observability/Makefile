.PHONY: dev test lint type-check migrate migrate-down install install-dev clean

# ---- Local development ----

dev:
	docker-compose up -d postgres redis
	uvicorn api.main:app --reload --port 8000

dev-full:
	docker-compose up

# ---- Dependencies ----

install:
	pip install .

install-dev:
	pip install -e ".[dev]"

# ---- Database ----

migrate:
	alembic upgrade head

migrate-down:
	alembic downgrade -1

migrate-history:
	alembic history --verbose

# ---- Testing ----

test:
	pytest tests/ -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-cov:
	pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

# ---- Code quality ----

lint:
	ruff check .
	black --check .

format:
	ruff check --fix .
	black .

type-check:
	mypy api/ domain/ database/ adapters/ --ignore-missing-imports

# ---- Security ----

scan-secrets:
	detect-secrets scan > .secrets.baseline

audit:
	pip-audit

# ---- Cleanup ----

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
