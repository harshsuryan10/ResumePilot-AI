"""Embedding generation using sentence-transformers (EmbeddingService).

The model is loaded lazily and cached as a singleton to avoid the heavy
startup cost on every request.
"""
from __future__ import annotations

from typing import List, Optional

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """Generates dense vector embeddings for text using all-MiniLM-L6-v2."""

    _model = None  # class-level cache shared across instances

    def __init__(self, model_name: Optional[str] = None) -> None:
        self._model_name = model_name or settings.embedding_model

    def _get_model(self):
        if EmbeddingService._model is None:
            # Imported lazily so the dependency is only required when used.
            from sentence_transformers import SentenceTransformer

            logger.info("Loading embedding model: %s", self._model_name)
            EmbeddingService._model = SentenceTransformer(self._model_name)
        return EmbeddingService._model

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        model = self._get_model()
        vectors = model.encode(texts, normalize_embeddings=True)
        return [vector.tolist() for vector in vectors]

    def embed_text(self, text: str) -> List[float]:
        return self.embed_texts([text])[0]
