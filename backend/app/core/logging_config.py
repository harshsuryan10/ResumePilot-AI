"""Structured application logging configuration."""
from __future__ import annotations

import logging
import sys

from app.core.config import settings

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_configured = False


def configure_logging() -> None:
    """Configure root logging once for the whole application."""
    global _configured
    if _configured:
        return

    level = logging.DEBUG if settings.debug else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT))

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)

    # Quiet noisy third-party loggers.
    for noisy in ("pymongo", "httpx", "chromadb", "sentence_transformers"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a named logger, ensuring logging is configured."""
    configure_logging()
    return logging.getLogger(name)
