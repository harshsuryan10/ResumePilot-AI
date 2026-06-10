"""Schemas for resume analysis and ATS scoring."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AnalysisResult(BaseModel):
    professional_summary: str = ""
    key_skills: List[str] = Field(default_factory=list)
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    career_recommendations: List[str] = Field(default_factory=list)


class AnalysisReport(AnalysisResult):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    user_id: str
    resume_id: str
    created_at: Optional[datetime] = None


class ATSScoreResult(BaseModel):
    overall_score: int = 0
    skills_score: int = 0
    experience_score: int = 0
    keyword_score: int = 0
    formatting_score: int = 0
    explanation: str = ""
    suggestions: List[str] = Field(default_factory=list)


class ATSReport(ATSScoreResult):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    user_id: str
    resume_id: str
    created_at: Optional[datetime] = None
