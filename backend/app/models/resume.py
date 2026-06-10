"""Resume domain model and schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import PyObjectId


class ResumeModel(BaseModel):
    """Resume document stored in the `resumes` collection."""

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: str
    file_name: str
    file_size: int
    extracted_text: str
    uploaded_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ResumePublic(BaseModel):
    """Resume metadata returned to clients (text truncated separately)."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    user_id: str
    file_name: str
    file_size: int
    uploaded_at: Optional[datetime] = None
    text_preview: Optional[str] = None


class ResumeDetail(ResumePublic):
    extracted_text: str
