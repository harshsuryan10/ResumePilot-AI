"""Application-wide exception types and standardized error payloads."""
from __future__ import annotations

from typing import Any, Optional


class AppException(Exception):
    """Base application exception mapped to a standardized HTTP error."""

    status_code: int = 500
    error_code: str = "internal_error"
    message: str = "An unexpected error occurred."

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        details: Optional[Any] = None,
    ) -> None:
        self.message = message or self.message
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code
        self.details = details
        super().__init__(self.message)


class NotFoundError(AppException):
    status_code = 404
    error_code = "not_found"
    message = "Resource not found."


class ValidationError(AppException):
    status_code = 422
    error_code = "validation_error"
    message = "Invalid input."


class AuthenticationError(AppException):
    status_code = 401
    error_code = "authentication_error"
    message = "Authentication failed."


class AuthorizationError(AppException):
    status_code = 403
    error_code = "authorization_error"
    message = "You are not authorized to perform this action."


class ConflictError(AppException):
    status_code = 409
    error_code = "conflict"
    message = "Resource already exists."


class ExternalServiceError(AppException):
    status_code = 502
    error_code = "external_service_error"
    message = "An external service failed."
