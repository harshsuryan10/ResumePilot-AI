"""ChromaDB persistent vector store wrapper (VectorStoreService)."""
from __future__ import annotations

from typing import List, Optional

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class VectorStoreService:
    """Stores and retrieves resume chunk embeddings in ChromaDB.

    Each resume's chunks are namespaced by metadata (user_id, resume_id) so
    retrieval can be scoped strictly to a single user's resume.
    """

    _client = None  # shared persistent client

    def __init__(self, collection_name: str = "resume_chunks") -> None:
        self._collection_name = collection_name

    def _get_collection(self):
        if VectorStoreService._client is None:
            import chromadb

            logger.info(
                "Initializing ChromaDB persistent client at %s",
                settings.chroma_persist_dir,
            )
            VectorStoreService._client = chromadb.PersistentClient(
                path=settings.chroma_persist_dir
            )
        return VectorStoreService._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        *,
        user_id: str,
        resume_id: str,
        chunks: List[str],
        embeddings: List[List[float]],
    ) -> None:
        if not chunks:
            return
        collection = self._get_collection()
        ids = [f"{resume_id}:{i}" for i in range(len(chunks))]
        metadatas = [
            {"user_id": user_id, "resume_id": resume_id, "chunk_index": i}
            for i in range(len(chunks))
        ]
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        logger.debug("Stored %d chunks for resume %s", len(chunks), resume_id)

    def query(
        self,
        *,
        user_id: str,
        resume_id: str,
        query_embedding: List[float],
        top_k: int = 4,
    ) -> List[str]:
        collection = self._get_collection()
        result = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={"$and": [{"user_id": user_id}, {"resume_id": resume_id}]},
        )
        documents: Optional[List[List[str]]] = result.get("documents")
        if not documents or not documents[0]:
            return []
        return documents[0]

    def delete_resume(self, *, resume_id: str) -> None:
        collection = self._get_collection()
        collection.delete(where={"resume_id": resume_id})
        logger.debug("Deleted vectors for resume %s", resume_id)
