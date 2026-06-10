"""Shared Pydantic helpers: ObjectId support and standardized responses."""
from __future__ import annotations

from typing import Any, Generic, List, Optional, TypeVar

from bson import ObjectId
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema

T = TypeVar("T")


class PyObjectId(ObjectId):
    """Pydantic v2 compatible ObjectId type."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.no_info_plain_validator_function(cls.validate),
            json_schema=core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def validate(cls, value: Any) -> ObjectId:
        if isinstance(value, ObjectId):
            return value
        if isinstance(value, str) and ObjectId.is_valid(value):
            return ObjectId(value)
        raise ValueError("Invalid ObjectId")


class APIResponse(BaseModel, Generic[T]):
    """Standardized success response envelope."""

    success: bool = True
    message: str = "OK"
    data: Optional[T] = None


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Standardized paginated response envelope."""

    success: bool = True
    message: str = "OK"
    data: List[T] = Field(default_factory=list)
    pagination: PaginationMeta


class ErrorResponse(BaseModel):
    """Standardized error response envelope."""

    success: bool = False
    error_code: str
    message: str
    details: Optional[Any] = None
