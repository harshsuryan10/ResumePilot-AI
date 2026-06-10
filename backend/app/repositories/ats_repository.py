"""Repository for persisting ATS scoring results."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.repositories.base_repository import BaseRepository


class ATSRepository(BaseRepository):
    """Data access for the `ats_scores` collection."""

    collection_name = "ats_scores"

    async def find_by_resume(self, resume_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        return await self.find_one({"resume_id": resume_id, "user_id": user_id})

    async def list_by_user(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.find_many(
            {"user_id": user_id},
            sort=[("created_at", -1)],
            limit=limit,
        )
