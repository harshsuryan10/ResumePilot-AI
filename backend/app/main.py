"""FastAPI application entrypoint for AI Resume Copilot."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging_config import configure_logging, get_logger
from app.database.mongodb import close_mongo_connection, connect_to_mongo
from app.middleware.error_handlers import register_exception_handlers
from app.middleware.middleware import (
    RequestLoggingMiddleware,
    SecureHeadersMiddleware,
)
from app.schemas.common import APIResponse

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Manage startup and shutdown lifecycle."""
    await connect_to_mongo()
    logger.info("%s started in %s mode.", settings.app_name, settings.environment)
    yield
    await close_mongo_connection()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="AI-powered resume analysis, ATS scoring, and career copilot.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SecureHeadersMiddleware)

    register_exception_handlers(app)

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/", tags=["Health"], summary="Service metadata")
    async def root() -> APIResponse[dict]:
        return APIResponse(
            message="OK",
            data={
                "service": settings.app_name,
                "environment": settings.environment,
                "docs": "/docs",
            },
        )

    @app.get("/health", tags=["Health"], summary="Health check")
    async def health() -> APIResponse[dict]:
        return APIResponse(message="OK", data={"status": "healthy"})

    return app


app = create_app()
