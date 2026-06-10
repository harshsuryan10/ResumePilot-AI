"""Security utilities: password hashing and JWT token management."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class SecurityService:
    """Encapsulates hashing and JWT operations (single responsibility)."""

    def hash_password(self, plain_password: str) -> str:
        return _pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(plain_password, hashed_password)

    def _create_token(
        self,
        subject: str,
        token_type: str,
        secret: str,
        expires_delta: timedelta,
        extra_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        now = datetime.now(timezone.utc)
        payload: Dict[str, Any] = {
            "sub": subject,
            "type": token_type,
            "iat": now,
            "exp": now + expires_delta,
        }
        if extra_claims:
            payload.update(extra_claims)
        return jwt.encode(payload, secret, algorithm=settings.jwt_algorithm)

    def create_access_token(
        self, subject: str, extra_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        return self._create_token(
            subject=subject,
            token_type=ACCESS_TOKEN_TYPE,
            secret=settings.jwt_secret_key,
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
            extra_claims=extra_claims,
        )

    def create_refresh_token(self, subject: str) -> str:
        return self._create_token(
            subject=subject,
            token_type=REFRESH_TOKEN_TYPE,
            secret=settings.jwt_refresh_secret_key,
            expires_delta=timedelta(days=settings.refresh_token_expire_days),
        )

    def decode_token(self, token: str, token_type: str) -> Optional[Dict[str, Any]]:
        """Decode and validate a token. Returns the payload or None if invalid."""
        secret = (
            settings.jwt_secret_key
            if token_type == ACCESS_TOKEN_TYPE
            else settings.jwt_refresh_secret_key
        )
        try:
            payload = jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            return None
        if payload.get("type") != token_type:
            return None
        return payload


security_service = SecurityService()
