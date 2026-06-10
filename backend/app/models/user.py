"""Domain models stored in MongoDB. These describe persisted documents."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.common import PyObjectId


class UserModel(BaseModel):
    """User document as stored in the `users` collection."""

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str
    email: EmailStr
    password_hash: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
