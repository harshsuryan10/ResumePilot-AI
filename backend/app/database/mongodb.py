"""MongoDB connection management using Motor (async driver).

Implements a reusable service-layer client with lifecycle hooks and
index creation. A single MongoDB instance is shared across the app.
"""
from __future__ import annotations

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class MongoDB:
    """Holds the Motor client and database handle."""

    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None


mongodb = MongoDB()


async def connect_to_mongo() -> None:
    """Open the MongoDB connection and ensure indexes exist."""
    logger.info("Connecting to MongoDB at %s", settings.mongodb_db_name)
    mongodb.client = AsyncIOMotorClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=5000,
        uuidRepresentation="standard",
    )
    mongodb.database = mongodb.client[settings.mongodb_db_name]
    await _create_indexes()
    logger.info("MongoDB connection established.")


async def close_mongo_connection() -> None:
    """Close the MongoDB connection."""
    if mongodb.client is not None:
        mongodb.client.close()
        logger.info("MongoDB connection closed.")


def get_database() -> AsyncIOMotorDatabase:
    """Return the active database handle."""
    if mongodb.database is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo first.")
    return mongodb.database


async def _create_indexes() -> None:
    """Create collection indexes for performance and uniqueness."""
    db = get_database()
    await db["users"].create_index("email", unique=True)
    await db["resumes"].create_index("user_id")
    await db["resumes"].create_index([("user_id", 1), ("uploaded_at", -1)])
    await db["analyses"].create_index([("user_id", 1), ("created_at", -1)])
    await db["analyses"].create_index([("resume_id", 1), ("user_id", 1)], unique=True)
    await db["ats_scores"].create_index([("user_id", 1), ("created_at", -1)])
    await db["ats_scores"].create_index([("resume_id", 1), ("user_id", 1)], unique=True)
    await db["chat_history"].create_index([("user_id", 1), ("resume_id", 1)])
    logger.debug("MongoDB indexes ensured.")
