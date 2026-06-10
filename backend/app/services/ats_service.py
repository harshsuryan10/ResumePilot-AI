"""ATS (Applicant Tracking System) scoring service."""
from __future__ import annotations

from typing import Any, Dict

from fastapi.concurrency import run_in_threadpool

from app.core.exceptions import ExternalServiceError, NotFoundError
from app.core.logging_config import get_logger
from app.llm.base import LLMProvider
from app.llm.prompts import PromptManager
from app.repositories.ats_repository import ATSRepository
from app.repositories.resume_repository import ResumeRepository

logger = get_logger(__name__)

_SCORE_KEYS = (
    "overall_score",
    "skills_score",
    "experience_score",
    "keyword_score",
    "formatting_score",
)


def _clamp_score(value: Any) -> int:
    try:
        score = int(round(float(value)))
    except (TypeError, ValueError):
        return 0
    return max(0, min(100, score))


class ATSService:
    """Computes a 0-100 ATS compatibility score for a stored resume."""

    def __init__(
        self,
        ats_repository: ATSRepository,
        resume_repository: ResumeRepository,
        llm_provider: LLMProvider,
    ) -> None:
        self._ats = ats_repository
        self._resumes = resume_repository
        self._llm = llm_provider

    async def score(
        self, resume_id: str, user_id: str, *, force: bool = False
    ) -> Dict[str, Any]:
        resume = await self._resumes.get_owned(resume_id, user_id)
        if not resume:
            raise NotFoundError("Resume not found.")

        if not force:
            existing = await self._ats.find_by_resume(resume_id, user_id)
            if existing:
                return existing

        resume_text = resume.get("extracted_text", "")
        if not resume_text.strip():
            raise ExternalServiceError("Resume has no extracted text to score.")

        prompt = PromptManager.ats_score(resume_text)
        result = await run_in_threadpool(self._llm.generate_json, prompt)

        payload: Dict[str, Any] = {
            "resume_id": resume_id,
            "user_id": user_id,
            "explanation": result.get("explanation", ""),
            "suggestions": result.get("suggestions", []),
        }
        for key in _SCORE_KEYS:
            payload[key] = _clamp_score(result.get(key))

        existing = await self._ats.find_by_resume(resume_id, user_id)
        if existing:
            return await self._ats.update_by_id(existing["_id"], payload)
        return await self._ats.create(payload)

    async def get_for_resume(self, resume_id: str, user_id: str) -> Dict[str, Any]:
        report = await self._ats.find_by_resume(resume_id, user_id)
        if not report:
            raise NotFoundError("No ATS score found for this resume.")
        return report
