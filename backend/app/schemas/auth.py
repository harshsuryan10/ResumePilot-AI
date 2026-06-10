"""Request/response schemas for authentication and user endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    """User data safe to return to clients (no password hash)."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    name: str
    email: EmailStr
    created_at: Optional[datetime] = None


class AuthResult(BaseModel):
    user: UserPublic
    tokens: TokenPair
