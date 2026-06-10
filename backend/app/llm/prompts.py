"""Centralized prompt templates and management (PromptManager)."""
from __future__ import annotations

RESUME_ANALYSIS_PROMPT = """You are an expert career coach and resume reviewer.
Analyze the resume text below and return a structured JSON object.

Return ONLY valid JSON (no markdown, no code fences) with this exact shape:
{{
  "professional_summary": "string",
  "key_skills": ["string"],
  "technical_skills": ["string"],
  "soft_skills": ["string"],
  "strengths": ["string"],
  "weaknesses": ["string"],
  "missing_skills": ["string"],
  "career_recommendations": ["string"]
}}

Resume:
\"\"\"
{resume_text}
\"\"\"
"""

ATS_SCORE_PROMPT = """You are an Applicant Tracking System (ATS) evaluator.
Score the resume below. All scores are integers from 0 to 100.

Return ONLY valid JSON (no markdown, no code fences) with this exact shape:
{{
  "overall_score": 0,
  "skills_score": 0,
  "experience_score": 0,
  "keyword_score": 0,
  "formatting_score": 0,
  "explanation": "string",
  "suggestions": ["string"]
}}

Resume:
\"\"\"
{resume_text}
\"\"\"
"""

RAG_ANSWER_PROMPT = """You are a helpful assistant answering questions strictly
about a candidate's resume. Use ONLY the context provided below. If the answer
is not present in the context, reply exactly: "That information is not in the
resume." Do not invent details.

Context:
\"\"\"
{context}
\"\"\"

Question: {question}
Answer:"""


class PromptManager:
    """Renders prompt templates with provided variables."""

    @staticmethod
    def resume_analysis(resume_text: str) -> str:
        return RESUME_ANALYSIS_PROMPT.format(resume_text=resume_text)

    @staticmethod
    def ats_score(resume_text: str) -> str:
        return ATS_SCORE_PROMPT.format(resume_text=resume_text)

    @staticmethod
    def rag_answer(context: str, question: str) -> str:
        return RAG_ANSWER_PROMPT.format(context=context, question=question)
