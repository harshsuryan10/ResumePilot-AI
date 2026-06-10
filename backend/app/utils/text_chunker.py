"""Text chunking utility for RAG ingestion."""
from __future__ import annotations

from typing import List


class TextChunker:
    """Splits text into overlapping chunks for embedding."""

    def __init__(self, chunk_size: int = 800, overlap: int = 120) -> None:
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        words = text.split()
        if not words:
            return []

        chunks: List[str] = []
        step = self.chunk_size - self.overlap
        for start in range(0, len(words), step):
            window = words[start : start + self.chunk_size]
            if window:
                chunks.append(" ".join(window))
            if start + self.chunk_size >= len(words):
                break
        return chunks
