"""Analysis and ATS scoring routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import (
    get_analysis_service,
    get_ats_service,
    get_current_user_id,
)
from app.schemas.analysis import AnalysisReport, ATSReport
from app.schemas.common import APIResponse
from app.services.analysis_service import AnalysisService
from app.services.ats_service import ATSService

router = APIRouter(tags=["Analysis"])


def _analysis_report(doc: dict) -> AnalysisReport:
    return AnalysisReport(
        _id=str(doc["_id"]),
        user_id=doc["user_id"],
        resume_id=doc["resume_id"],
        created_at=doc.get("created_at"),
        professional_summary=doc.get("professional_summary", ""),
        key_skills=doc.get("key_skills", []),
        technical_skills=doc.get("technical_skills", []),
        soft_skills=doc.get("soft_skills", []),
        strengths=doc.get("strengths", []),
        weaknesses=doc.get("weaknesses", []),
        missing_skills=doc.get("missing_skills", []),
        career_recommendations=doc.get("career_recommendations", []),
    )


def _ats_report(doc: dict) -> ATSReport:
    return ATSReport(
        _id=str(doc["_id"]),
        user_id=doc["user_id"],
        resume_id=doc["resume_id"],
        created_at=doc.get("created_at"),
        overall_score=doc.get("overall_score", 0),
        skills_score=doc.get("skills_score", 0),
        experience_score=doc.get("experience_score", 0),
        keyword_score=doc.get("keyword_score", 0),
        formatting_score=doc.get("formatting_score", 0),
        explanation=doc.get("explanation", ""),
        suggestions=doc.get("suggestions", []),
    )


@router.post(
    "/resumes/{resume_id}/analyze",
    response_model=APIResponse[AnalysisReport],
    summary="Generate AI analysis for a resume",
)
async def analyze_resume(
    resume_id: str,
    force: bool = Query(False, description="Re-run analysis even if cached."),
    user_id: str = Depends(get_current_user_id),
    service: AnalysisService = Depends(get_analysis_service),
) -> APIResponse[AnalysisReport]:
    doc = await service.analyze(resume_id, user_id, force=force)
    return APIResponse(message="Analysis complete.", data=_analysis_report(doc))


@router.get(
    "/resumes/{resume_id}/analysis",
    response_model=APIResponse[AnalysisReport],
    summary="Get the stored analysis for a resume",
)
async def get_analysis(
    resume_id: str,
    user_id: str = Depends(get_current_user_id),
    service: AnalysisService = Depends(get_analysis_service),
) -> APIResponse[AnalysisReport]:
    doc = await service.get_for_resume(resume_id, user_id)
    return APIResponse(message="OK", data=_analysis_report(doc))


@router.post(
    "/resumes/{resume_id}/ats-score",
    response_model=APIResponse[ATSReport],
    summary="Compute the ATS compatibility score for a resume",
)
async def score_resume(
    resume_id: str,
    force: bool = Query(False, description="Re-run scoring even if cached."),
    user_id: str = Depends(get_current_user_id),
    service: ATSService = Depends(get_ats_service),
) -> APIResponse[ATSReport]:
    doc = await service.score(resume_id, user_id, force=force)
    return APIResponse(message="ATS score complete.", data=_ats_report(doc))


@router.get(
    "/resumes/{resume_id}/ats-score",
    response_model=APIResponse[ATSReport],
    summary="Get the stored ATS score for a resume",
)
async def get_ats_score(
    resume_id: str,
    user_id: str = Depends(get_current_user_id),
    service: ATSService = Depends(get_ats_service),
) -> APIResponse[ATSReport]:
    doc = await service.get_for_resume(resume_id, user_id)
    return APIResponse(message="OK", data=_ats_report(doc))
