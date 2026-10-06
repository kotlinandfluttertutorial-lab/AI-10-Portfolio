"""Portfolio-standard error envelope and FastAPI exception handlers."""

import uuid

import structlog
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = structlog.get_logger(__name__)


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str
    details: list[dict[str, str]] = []


class ErrorResponse(BaseModel):
    error: ErrorDetail


def make_error_response(
    code: str,
    message: str,
    request_id: str | None = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    details: list[dict[str, str]] | None = None,
) -> JSONResponse:
    rid = request_id or str(uuid.uuid4())
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": rid,
                "details": details or [],
            }
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    details = [
        {"field": ".".join(str(loc) for loc in e["loc"]), "message": e["msg"]}
        for e in exc.errors()
    ]
    logger.info(
        "request.validation_error",
        path=request.url.path,
        error_count=len(details),
        request_id=request_id,
    )
    return make_error_response(
        code="VALIDATION_ERROR",
        message="Request validation failed.",
        request_id=request_id,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details=details,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    logger.error(
        "request.unhandled_error",
        path=request.url.path,
        error=str(exc),
        request_id=request_id,
        exc_info=True,
    )
    return make_error_response(
        code="INTERNAL_ERROR",
        message="An unexpected error occurred. Please try again or contact support.",
        request_id=request_id,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
