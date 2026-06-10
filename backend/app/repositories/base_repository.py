"""Generic async repository implementing the Repository Pattern over Motor."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase


class BaseRepository:
    """Reusable CRUD operations for a single MongoDB collection."""

    collection_name: str = ""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        if not self.collection_name:
            raise ValueError("collection_name must be set on the repository subclass.")
        self._db = database

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._db[self.collection_name]

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def _to_object_id(value: Any) -> ObjectId:
        if isinstance(value, ObjectId):
            return value
        return ObjectId(str(value))

    async def create(self, document: Dict[str, Any]) -> Dict[str, Any]:
        document.setdefault("created_at", self._now())
        document.setdefault("updated_at", self._now())
        result = await self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return document

    async def find_by_id(self, doc_id: Any) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one({"_id": self._to_object_id(doc_id)})

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one(query)

    async def find_many(
        self,
        query: Dict[str, Any],
        *,
        sort: Optional[List[Tuple[str, int]]] = None,
        skip: int = 0,
        limit: int = 0,
    ) -> List[Dict[str, Any]]:
        cursor = self.collection.find(query)
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return await cursor.to_list(length=limit or None)

    async def count(self, query: Dict[str, Any]) -> int:
        return await self.collection.count_documents(query)

    async def update_by_id(
        self, doc_id: Any, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        updates["updated_at"] = self._now()
        return await self.collection.find_one_and_update(
            {"_id": self._to_object_id(doc_id)},
            {"$set": updates},
            return_document=True,
        )

    async def delete_by_id(self, doc_id: Any) -> bool:
        result = await self.collection.delete_one(
            {"_id": self._to_object_id(doc_id)}
        )
        return result.deleted_count > 0
