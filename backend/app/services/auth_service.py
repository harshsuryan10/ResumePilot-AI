"""Authentication and user business logic (AuthService, UserService)."""
from __future__ import annotations

from typing import Any, Dict

from app.core.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
)
from app.core.security import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    security_service,
)
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    AuthResult,
    TokenPair,
    UserLoginRequest,
    UserPublic,
    UserRegisterRequest,
)


def _to_public(user: Dict[str, Any]) -> UserPublic:
    return UserPublic(
        _id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        created_at=user.get("created_at"),
    )


class UserService:
    """User-centric operations (single responsibility: user records)."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._users = user_repository

    async def get_by_id(self, user_id: str) -> Dict[str, Any]:
        user = await self._users.find_by_id(user_id)
        if not user:
            raise NotFoundError("User not found.")
        return user

    async def get_public_profile(self, user_id: str) -> UserPublic:
        return _to_public(await self.get_by_id(user_id))


class AuthService:
    """Registration, login and token refresh logic."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._users = user_repository

    def _issue_tokens(self, user_id: str) -> TokenPair:
        return TokenPair(
            access_token=security_service.create_access_token(user_id),
            refresh_token=security_service.create_refresh_token(user_id),
        )

    async def register(self, payload: UserRegisterRequest) -> AuthResult:
        email = payload.email.lower()
        if await self._users.email_exists(email):
            raise ConflictError("An account with this email already exists.")

        user = await self._users.create(
            {
                "name": payload.name.strip(),
                "email": email,
                "password_hash": security_service.hash_password(payload.password),
            }
        )
        user_id = str(user["_id"])
        return AuthResult(user=_to_public(user), tokens=self._issue_tokens(user_id))

    async def login(self, payload: UserLoginRequest) -> AuthResult:
        user = await self._users.get_by_email(payload.email.lower())
        if not user or not security_service.verify_password(
            payload.password, user["password_hash"]
        ):
            raise AuthenticationError("Invalid email or password.")
        user_id = str(user["_id"])
        return AuthResult(user=_to_public(user), tokens=self._issue_tokens(user_id))

    async def refresh(self, refresh_token: str) -> TokenPair:
        payload = security_service.decode_token(refresh_token, REFRESH_TOKEN_TYPE)
        if not payload or "sub" not in payload:
            raise AuthenticationError("Invalid or expired refresh token.")
        user = await self._users.find_by_id(payload["sub"])
        if not user:
            raise AuthenticationError("User no longer exists.")
        return self._issue_tokens(str(user["_id"]))

    @staticmethod
    def verify_access_token(token: str) -> str:
        payload = security_service.decode_token(token, ACCESS_TOKEN_TYPE)
        if not payload or "sub" not in payload:
            raise AuthenticationError("Invalid or expired access token.")
        return payload["sub"]
