"""Application configuration using pydantic-settings.

Loads environment variables from the process environment and an optional
.env file. A single cached Settings instance is exposed via get_settings().
"""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly typed application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "AI Resume Copilot"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "resume_copilot"

    # JWT
    jwt_secret_key: str = "change-me"
    jwt_refresh_secret_key: str = "change-me-too"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # AI / Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    ai_gateway_api_key: str = ""
    ai_gateway_base_url: str = "https://ai-gateway.vercel.sh/v1"
    ai_gateway_model: str = "google/gemini-2.5-flash"

    # Embeddings / Vector store
    embedding_model: str = "all-MiniLM-L6-v2"
    chroma_persist_dir: str = "./chroma_store"

    # Uploads
    max_upload_size_mb: int = 5
    upload_dir: str = "./uploads"

    @field_validator("cors_origins")
    @classmethod
    def _strip_origins(cls, value: str) -> str:
        return value.strip()

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def use_ai_gateway(self) -> bool:
        return bool(self.ai_gateway_api_key)


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()
