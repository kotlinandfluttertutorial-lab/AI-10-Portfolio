"""FastAPI application factory for the AgentOps Observability platform."""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from api.config import get_settings
from api.errors import unhandled_exception_handler, validation_exception_handler
from api.logging_config import configure_logging
from api.middleware import RequestIDMiddleware
from api.routers import health

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown lifecycle."""
    settings = get_settings()
    configure_logging(settings.log_level)
    logger.info("agentops.starting", env=settings.app_env)
    yield
    logger.info("agentops.shutdown")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="AgentOps — AI Agent Monitoring and Reliability Platform",
        description="Collect, store, and visualize AI agent traces, metrics, costs, and alerts.",
        version="0.1.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Middleware (order matters — outermost first)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIDMiddleware)

    # Exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Prometheus metrics — exposed at /metrics
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")

    # Routers
    app.include_router(health.router)

    return app


# Module-level app instance used by uvicorn
app = create_app()
