"""Health and readiness endpoints.

GET /health  — liveness probe: returns 200 if the process is alive.
GET /ready   — readiness probe: returns 200 only when DB and Redis are reachable.
"""

import structlog
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db, get_redis

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str


class ReadinessCheck(BaseModel):
    status: str
    checks: dict[str, str]


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Returns 200 if the process is alive. Does not check dependencies.",
)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/ready",
    response_model=ReadinessCheck,
    summary="Readiness probe",
    description="Returns 200 only when all critical dependencies are reachable.",
)
async def ready() -> JSONResponse:
    checks: dict[str, str] = {}
    all_ok = True

    # Check database
    try:
        async for db in get_db():
            await db.execute(text("SELECT 1"))
            checks["db"] = "ok"
            break
    except Exception as exc:
        logger.warning("readiness.db_check_failed", error=str(exc))
        checks["db"] = "error"
        all_ok = False

    # Check Redis
    try:
        redis = await get_redis()
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as exc:
        logger.warning("readiness.redis_check_failed", error=str(exc))
        checks["redis"] = "error"
        all_ok = False

    http_status = status.HTTP_200_OK if all_ok else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(
        status_code=http_status,
        content={"status": "ready" if all_ok else "degraded", "checks": checks},
    )
