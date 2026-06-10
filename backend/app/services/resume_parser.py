"""PDF text extraction service using PyMuPDF (ResumeParser)."""
from __future__ import annotations

import fitz  # PyMuPDF

from app.core.exceptions import ValidationError
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class ResumeParser:
    """Extracts and normalizes text from PDF resume bytes."""

    def extract_text(self, file_bytes: bytes) -> str:
        """Return cleaned plain text from a PDF byte stream."""
        try:
            document = fitz.open(stream=file_bytes, filetype="pdf")
        except Exception as exc:  # noqa: BLE001 - surface as validation error
            logger.warning("Failed to open PDF: %s", exc)
            raise ValidationError("The uploaded file is not a readable PDF.") from exc

        try:
            pages = [page.get_text("text") for page in document]
        finally:
            document.close()

        text = "\n".join(pages)
        cleaned = self._clean(text)
        if len(cleaned) < 30:
            raise ValidationError(
                "Could not extract meaningful text. The PDF may be scanned or empty."
            )
        return cleaned

    @staticmethod
    def _clean(text: str) -> str:
        lines = [line.strip() for line in text.splitlines()]
        non_empty = [line for line in lines if line]
        return "\n".join(non_empty)
