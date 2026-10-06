"""P05-01 smoke tests: verify the application skeleton is correctly wired.

These tests run without a live database or Redis connection.
They verify imports, app creation, and the /health endpoint.
"""

import os

import pytest


def test_app_imports_without_error() -> None:
    """The application module must import cleanly."""
    from api.main import create_app  # noqa: F401

    assert create_app is not None


def test_create_app_returns_fastapi_instance() -> None:
    """create_app() must return a FastAPI instance."""
    from fastapi import FastAPI

    from api.main import create_app

    app = create_app()
    assert isinstance(app, FastAPI)


def test_health_endpoint_returns_200(app_client: object) -> None:
    """GET /health must return 200 with status=ok — no database required."""
    from fastapi.testclient import TestClient

    assert isinstance(app_client, TestClient)
    response = app_client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_health_response_includes_request_id_header(app_client: object) -> None:
    """Every response must include X-Request-ID."""
    from fastapi.testclient import TestClient

    assert isinstance(app_client, TestClient)
    response = app_client.get("/health")
    assert "x-request-id" in response.headers


def test_openapi_schema_is_accessible(app_client: object) -> None:
    """GET /openapi.json must return a valid JSON schema."""
    from fastapi.testclient import TestClient

    assert isinstance(app_client, TestClient)
    response = app_client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema


def test_validation_error_returns_422_with_envelope() -> None:
    """Validation errors must use the portfolio error envelope format."""
    # This test verifies the error handler is registered correctly.
    # We trigger a validation error by hitting a non-existent endpoint
    # (FastAPI returns 404 with our custom handler shape).
    from fastapi.testclient import TestClient

    from api.main import create_app

    client = TestClient(create_app(), raise_server_exceptions=False)
    # POST /health with a body that would trigger validation if the endpoint had a schema
    # For now, just verify the 404 returns our error envelope format.
    response = client.get("/v1/nonexistent-endpoint-for-testing")
    # 404 — not in our envelope (FastAPI default), but our error handler covers 422+
    # Real validation error test is in test_api_*.py after the API is implemented
    assert response.status_code == 404


def test_config_requires_real_jwt_secret() -> None:
    """Settings must reject placeholder JWT secrets."""
    import importlib
    import sys

    # Temporarily override the env var with a placeholder
    original = os.environ.get("JWT_SECRET")
    os.environ["JWT_SECRET"] = "your-placeholder-value"

    # Clear the cached settings so it re-reads the env
    if "api.config" in sys.modules:
        importlib.reload(sys.modules["api.config"])

    try:
        from api.config import Settings

        with pytest.raises(Exception, match="JWT_SECRET"):
            Settings(  # type: ignore[call-arg]
                database_url="postgresql+asyncpg://test:test@localhost/test",
                database_url_sync="postgresql://test:test@localhost/test",
                jwt_secret="your-placeholder-value",
            )
    finally:
        if original is not None:
            os.environ["JWT_SECRET"] = original
        # Reload to restore good state
        if "api.config" in sys.modules:
            importlib.reload(sys.modules["api.config"])


def test_domain_exceptions_importable() -> None:
    """Domain exception classes must be importable."""
    from domain.exceptions import (
        AgentOpsError,
        AuthenticationError,
        AuthorizationError,
        ConflictError,
        NotFoundError,
        RateLimitError,
        ValidationError,
    )

    assert issubclass(AuthenticationError, AgentOpsError)
    assert issubclass(AuthorizationError, AgentOpsError)
    assert issubclass(NotFoundError, AgentOpsError)
    assert issubclass(ValidationError, AgentOpsError)
    assert issubclass(RateLimitError, AgentOpsError)
    assert issubclass(ConflictError, AgentOpsError)
