"""FastAPI dependency providers (dependency injection wiring)."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import AuthenticationError
from app.database.mongodb import get_database
from app.llm.base import LLMProvider
from app.llm.gemini_provider import GeminiProvider
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store_service import VectorStoreService
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.ats_repository import ATSRepository
from app.repositories.resume_repository import ResumeRepository
from app.repositories.user_repository import UserRepository
from app.services.analysis_service import AnalysisService
from app.services.ats_service import ATSService
from app.services.auth_service import AuthService, UserService
from app.services.file_upload_service import FileUploadService
from app.services.resume_parser import ResumeParser
from app.services.resume_service import ResumeService
from app.utils.text_chunker import TextChunker

_bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> AsyncIOMotorDatabase:
    return get_database()


def get_user_repository(
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


def get_auth_service(
    repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(repo)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    user_service: UserService = Depends(get_user_service),
) -> Dict[str, Any]:
    """Resolve the authenticated user from the bearer access token."""
    if credentials is None or not credentials.credentials:
        raise AuthenticationError("Missing authentication credentials.")
    user_id = AuthService.verify_access_token(credentials.credentials)
    return await user_service.get_by_id(user_id)


def get_current_user_id(
    user: Dict[str, Any] = Depends(get_current_user),
) -> str:
    return str(user["_id"])


# --- Resume module providers ---


def get_resume_repository(
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> ResumeRepository:
    return ResumeRepository(db)


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


def get_vector_store_service() -> VectorStoreService:
    return VectorStoreService()


def get_resume_service(
    repo: ResumeRepository = Depends(get_resume_repository),
    embeddings: EmbeddingService = Depends(get_embedding_service),
    vectors: VectorStoreService = Depends(get_vector_store_service),
) -> ResumeService:
    return ResumeService(
        resume_repository=repo,
        parser=ResumeParser(),
        file_validator=FileUploadService(),
        chunker=TextChunker(),
        embedding_service=embeddings,
        vector_store=vectors,
    )


# --- AI / Analysis providers ---

_llm_provider_singleton: LLMProvider | None = None


def get_llm_provider() -> LLMProvider:
    global _llm_provider_singleton
    if _llm_provider_singleton is None:
        _llm_provider_singleton = GeminiProvider()
    return _llm_provider_singleton


def get_analysis_repository(
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> AnalysisRepository:
    return AnalysisRepository(db)


def get_ats_repository(
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> ATSRepository:
    return ATSRepository(db)


def get_analysis_service(
    analysis_repo: AnalysisRepository = Depends(get_analysis_repository),
    resume_repo: ResumeRepository = Depends(get_resume_repository),
    llm: LLMProvider = Depends(get_llm_provider),
) -> AnalysisService:
    return AnalysisService(analysis_repo, resume_repo, llm)


def get_ats_service(
    ats_repo: ATSRepository = Depends(get_ats_repository),
    resume_repo: ResumeRepository = Depends(get_resume_repository),
    llm: LLMProvider = Depends(get_llm_provider),
) -> ATSService:
    return ATSService(ats_repo, resume_repo, llm)
