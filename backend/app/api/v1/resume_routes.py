"""Resume routes: upload, list, retrieve, delete."""
from __future__ import annotations

import math

from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from app.api.dependencies import get_current_user_id, get_resume_service
from app.schemas.common import (
    APIResponse,
    PaginatedResponse,
    PaginationMeta,
)
from app.models.resume import ResumeDetail, ResumePublic
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["Resumes"])

_PREVIEW_LEN = 240


def _to_public(doc: dict) -> ResumePublic:
    text = doc.get("extracted_text", "")
    return ResumePublic(
        _id=str(doc["_id"]),
        user_id=doc["user_id"],
        file_name=doc["file_name"],
        file_size=doc["file_size"],
        uploaded_at=doc.get("uploaded_at"),
        text_preview=text[:_PREVIEW_LEN],
    )


@router.post(
    "",
    response_model=APIResponse[ResumePublic],
    status_code=status.HTTP_201_CREATED,
    summary="Upload a resume PDF",
)
async def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    service: ResumeService = Depends(get_resume_service),
) -> APIResponse[ResumePublic]:
    content = await file.read()
    document = await service.upload(
        user_id=user_id,
        filename=file.filename or "resume.pdf",
        content=content,
    )
    return APIResponse(message="Resume uploaded.", data=_to_public(document))


@router.get(
    "",
    response_model=PaginatedResponse[ResumePublic],
    summary="List the current user's resumes",
)
async def list_resumes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    user_id: str = Depends(get_current_user_id),
    service: ResumeService = Depends(get_resume_service),
) -> PaginatedResponse[ResumePublic]:
    items, total = await service.list_resumes(
        user_id=user_id, page=page, page_size=page_size
    )
    return PaginatedResponse(
        data=[_to_public(item) for item in items],
        pagination=PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=max(1, math.ceil(total / page_size)),
        ),
    )


@router.get(
    "/{resume_id}",
    response_model=APIResponse[ResumeDetail],
    summary="Get a single resume with full text",
)
async def get_resume(
    resume_id: str,
    user_id: str = Depends(get_current_user_id),
    service: ResumeService = Depends(get_resume_service),
) -> APIResponse[ResumeDetail]:
    doc = await service.get_resume(user_id=user_id, resume_id=resume_id)
    detail = ResumeDetail(
        _id=str(doc["_id"]),
        user_id=doc["user_id"],
        file_name=doc["file_name"],
        file_size=doc["file_size"],
        uploaded_at=doc.get("uploaded_at"),
        text_preview=doc.get("extracted_text", "")[:_PREVIEW_LEN],
        extracted_text=doc.get("extracted_text", ""),
    )
    return APIResponse(message="OK", data=detail)


@router.delete(
    "/{resume_id}",
    response_model=APIResponse[None],
    summary="Delete a resume",
)
async def delete_resume(
    resume_id: str,
    user_id: str = Depends(get_current_user_id),
    service: ResumeService = Depends(get_resume_service),
) -> APIResponse[None]:
    await service.delete_resume(user_id=user_id, resume_id=resume_id)
    return APIResponse(message="Resume deleted.", data=None)
