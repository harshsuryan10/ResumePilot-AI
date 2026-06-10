"""Aggregates all v1 API routers under a single router."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import analysis_routes, auth_routes, resume_routes

api_router = APIRouter()
api_router.include_router(auth_routes.router)
api_router.include_router(resume_routes.router)
api_router.include_router(analysis_routes.router)
