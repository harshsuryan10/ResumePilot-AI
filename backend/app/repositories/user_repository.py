"""Repository for the `users` collection."""
from __future__ import annotations

from typing import Any, Dict, Optional

from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    collection_name = "users"

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return await self.find_one({"email": email.lower()})

    async def email_exists(self, email: str) -> bool:
        return await self.count({"email": email.lower()}) > 0
