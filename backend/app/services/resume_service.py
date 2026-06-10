"""Resume orchestration service: upload, parse, embed, store, manage."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from app.core.exceptions import NotFoundError
from app.core.logging_config import get_logger
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store_service import VectorStoreService
from app.repositories.resume_repository import ResumeRepository
from app.services.file_upload_service import FileUploadService
from app.services.resume_parser import ResumeParser
from app.utils.text_chunker import TextChunker

logger = get_logger(__name__)


class ResumeService:
    """Coordinates the full resume ingestion pipeline."""

    def __init__(
        self,
        resume_repository: ResumeRepository,
        parser: ResumeParser,
        file_validator: FileUploadService,
        chunker: TextChunker,
        embedding_service: EmbeddingService,
        vector_store: VectorStoreService,
    ) -> None:
        self._resumes = resume_repository
        self._parser = parser
        self._validator = file_validator
        self._chunker = chunker
        self._embeddings = embedding_service
        self._vectors = vector_store

    async def upload(
        self, *, user_id: str, filename: str, content: bytes
    ) -> Dict[str, Any]:
        """Validate, parse, persist, and index a resume PDF."""
        self._validator.validate_pdf(filename=filename, content=content)
        extracted_text = self._parser.extract_text(content)

        document = await self._resumes.create(
            {
                "user_id": user_id,
                "file_name": filename,
                "file_size": len(content),
                "extracted_text": extracted_text,
                "uploaded_at": datetime.now(timezone.utc),
            }
        )
        resume_id = str(document["_id"])

        # Build the vector index for RAG. Failures here should not block upload.
        try:
            self._index_resume(user_id, resume_id, extracted_text)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Vector indexing failed for resume %s: %s", resume_id, exc)

        return document

    def _index_resume(self, user_id: str, resume_id: str, text: str) -> None:
        chunks = self._chunker.chunk(text)
        embeddings = self._embeddings.embed_texts(chunks)
        self._vectors.add_chunks(
            user_id=user_id,
            resume_id=resume_id,
            chunks=chunks,
            embeddings=embeddings,
        )

    async def list_resumes(
        self, *, user_id: str, page: int, page_size: int
    ) -> Tuple[List[Dict[str, Any]], int]:
        skip = (page - 1) * page_size
        items = await self._resumes.list_for_user(
            user_id, skip=skip, limit=page_size
        )
        total = await self._resumes.count_for_user(user_id)
        return items, total

    async def get_resume(self, *, user_id: str, resume_id: str) -> Dict[str, Any]:
        resume = await self._resumes.get_owned(resume_id, user_id)
        if not resume:
            raise NotFoundError("Resume not found.")
        return resume

    async def delete_resume(self, *, user_id: str, resume_id: str) -> None:
        resume = await self.get_resume(user_id=user_id, resume_id=resume_id)
        await self._resumes.delete_by_id(resume["_id"])
        try:
            self._vectors.delete_resume(resume_id=resume_id)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Vector cleanup failed for resume %s: %s", resume_id, exc)
