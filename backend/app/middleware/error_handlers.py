"""Centralized exception handlers producing standardized error responses."""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppException
from app.core.logging_config import get_logger
from app.schemas.common import ErrorResponse

logger = get_logger("app.errors")


def register_exception_handlers(app: FastAPI) -> None:
    """Attach standardized exception handlers to the FastAPI app."""

    @app.exception_handler(AppException)
    async def _app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error_code=exc.error_code,
                message=exc.message,
                details=exc.details,
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error_code="validation_error",
                message="Request validation failed.",
                details=exc.errors(),
            ).model_dump(),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http_exception_handler(
        _: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error_code="http_error",
                message=str(exc.detail),
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def _unhandled_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error_code="internal_error",
                message="An unexpected error occurred.",
            ).model_dump(),
        )
