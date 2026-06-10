"""Authentication routes: register, login, refresh, current user."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_auth_service, get_current_user
from app.schemas.auth import (
    AuthResult,
    RefreshTokenRequest,
    TokenPair,
    UserLoginRequest,
    UserPublic,
    UserRegisterRequest,
)
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=APIResponse[AuthResult],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    payload: UserRegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> APIResponse[AuthResult]:
    result = await service.register(payload)
    return APIResponse(message="Registration successful.", data=result)


@router.post(
    "/login",
    response_model=APIResponse[AuthResult],
    summary="Authenticate a user",
)
async def login(
    payload: UserLoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> APIResponse[AuthResult]:
    result = await service.login(payload)
    return APIResponse(message="Login successful.", data=result)


@router.post(
    "/refresh",
    response_model=APIResponse[TokenPair],
    summary="Refresh the access token",
)
async def refresh(
    payload: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
) -> APIResponse[TokenPair]:
    tokens = await service.refresh(payload.refresh_token)
    return APIResponse(message="Token refreshed.", data=tokens)


@router.get(
    "/me",
    response_model=APIResponse[UserPublic],
    summary="Get the current authenticated user",
)
async def me(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> APIResponse[UserPublic]:
    public = UserPublic(
        _id=str(current_user["_id"]),
        name=current_user["name"],
        email=current_user["email"],
        created_at=current_user.get("created_at"),
    )
    return APIResponse(message="OK", data=public)
