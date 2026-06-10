"""Repository for the `resumes` collection."""
from __future__ import annotations

from typing import Any, Dict, List

from app.repositories.base_repository import BaseRepository


class ResumeRepository(BaseRepository):
    collection_name = "resumes"

    async def list_for_user(
        self, user_id: str, *, skip: int = 0, limit: int = 20
    ) -> List[Dict[str, Any]]:
        return await self.find_many(
            {"user_id": user_id},
            sort=[("uploaded_at", -1)],
            skip=skip,
            limit=limit,
        )

    async def count_for_user(self, user_id: str) -> int:
        return await self.count({"user_id": user_id})

    async def get_owned(self, resume_id: str, user_id: str) -> Dict[str, Any] | None:
        return await self.find_one(
            {"_id": self._to_object_id(resume_id), "user_id": user_id}
        )
