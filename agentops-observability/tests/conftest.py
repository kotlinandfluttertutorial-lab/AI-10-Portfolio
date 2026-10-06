"""Shared pytest fixtures for the AgentOps test suite."""

import os

import pytest
from fastapi.testclient import TestClient

# Set test environment variables BEFORE importing application modules
# so that Settings validation does not fail on missing real values.
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/agentops_test")
os.environ.setdefault("DATABASE_URL_SYNC", "postgresql://test:test@localhost:5432/agentops_test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/1")
os.environ.setdefault("JWT_SECRET", "test-secret-key-that-is-long-enough-for-tests-32chars")
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("LOG_LEVEL", "WARNING")


@pytest.fixture(scope="session")
def app_client() -> TestClient:
    """Return a synchronous TestClient for unit and smoke tests.

    Does NOT require a running database — use for endpoint contract tests
    that don't exercise DB code paths.
    """
    from api.main import create_app  # import after env vars are set

    test_app = create_app()
    return TestClient(test_app, raise_server_exceptions=True)
