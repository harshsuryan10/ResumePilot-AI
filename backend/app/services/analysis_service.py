"""Resume analysis service backed by the configured LLM provider."""
from __future__ import annotations

from typing import Any, Dict

from fastapi.concurrency import run_in_threadpool

from app.core.exceptions import ExternalServiceError, NotFoundError
from app.core.logging_config import get_logger
from app.llm.base import LLMProvider
from app.llm.prompts import PromptManager
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.resume_repository import ResumeRepository

logger = get_logger(__name__)

_ANALYSIS_KEYS = (
    "professional_summary",
    "key_skills",
    "technical_skills",
    "soft_skills",
    "strengths",
    "weaknesses",
    "missing_skills",
    "career_recommendations",
)


class AnalysisService:
    """Generates structured, AI-driven feedback for a stored resume."""

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        resume_repository: ResumeRepository,
        llm_provider: LLMProvider,
    ) -> None:
        self._analyses = analysis_repository
        self._resumes = resume_repository
        self._llm = llm_provider

    async def analyze(
        self, resume_id: str, user_id: str, *, force: bool = False
    ) -> Dict[str, Any]:
        resume = await self._resumes.get_owned(resume_id, user_id)
        if not resume:
            raise NotFoundError("Resume not found.")

        if not force:
            existing = await self._analyses.find_by_resume(resume_id, user_id)
            if existing:
                return existing

        resume_text = resume.get("extracted_text", "")
        if not resume_text.strip():
            raise ExternalServiceError("Resume has no extracted text to analyze.")

        prompt = PromptManager.resume_analysis(resume_text)
        result = await run_in_threadpool(self._llm.generate_json, prompt)

        payload: Dict[str, Any] = {
            "resume_id": resume_id,
            "user_id": user_id,
        }
        for key in _ANALYSIS_KEYS:
            payload[key] = result.get(key, "" if key == "professional_summary" else [])

        existing = await self._analyses.find_by_resume(resume_id, user_id)
        if existing:
            return await self._analyses.update_by_id(existing["_id"], payload)
        return await self._analyses.create(payload)

    async def get_for_resume(self, resume_id: str, user_id: str) -> Dict[str, Any]:
        analysis = await self._analyses.find_by_resume(resume_id, user_id)
        if not analysis:
            raise NotFoundError("No analysis found for this resume.")
        return analysis
