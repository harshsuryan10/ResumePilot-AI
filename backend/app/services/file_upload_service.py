"""File validation utilities (FileUploadService)."""
from __future__ import annotations

from app.core.config import settings
from app.core.exceptions import ValidationError

_PDF_MAGIC = b"%PDF-"


class FileUploadService:
    """Validates uploaded files before processing."""

    def validate_pdf(self, *, filename: str, content: bytes) -> None:
        if not filename.lower().endswith(".pdf"):
            raise ValidationError("Only PDF files are allowed.")
        if not content:
            raise ValidationError("The uploaded file is empty.")
        if len(content) > settings.max_upload_size_bytes:
            raise ValidationError(
                f"File exceeds the maximum size of {settings.max_upload_size_mb} MB."
            )
        if not content.startswith(_PDF_MAGIC):
            raise ValidationError("The file does not appear to be a valid PDF.")
