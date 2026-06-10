"""Gemini LLM provider with retry logic.

Supports two transports:
  1. Vercel AI Gateway (OpenAI-compatible) when AI_GATEWAY_API_KEY is set.
  2. Google Generative AI SDK when GEMINI_API_KEY is set.

Both are loaded lazily so only the configured dependency is required.
"""
from __future__ import annotations

import time
from typing import Optional

import httpx

from app.core.config import settings
from app.core.exceptions import ExternalServiceError
from app.core.logging_config import get_logger
from app.llm.base import LLMProvider

logger = get_logger(__name__)


class GeminiProvider(LLMProvider):
    """Concrete LLM provider backed by Google Gemini."""

    def __init__(self, max_retries: int = 3, backoff_seconds: float = 1.5) -> None:
        self._max_retries = max_retries
        self._backoff = backoff_seconds

    def generate(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        temperature: float = 0.4,
        max_output_tokens: int = 2048,
    ) -> str:
        last_error: Optional[Exception] = None
        for attempt in range(1, self._max_retries + 1):
            try:
                if settings.use_ai_gateway:
                    return self._via_gateway(
                        prompt, system, temperature, max_output_tokens
                    )
                return self._via_google_sdk(
                    prompt, system, temperature, max_output_tokens
                )
            except Exception as exc:  # noqa: BLE001 - retried below
                last_error = exc
                logger.warning(
                    "LLM call failed (attempt %d/%d): %s",
                    attempt,
                    self._max_retries,
                    exc,
                )
                if attempt < self._max_retries:
                    time.sleep(self._backoff * attempt)

        raise ExternalServiceError(
            "The AI service is currently unavailable. Please try again."
        ) from last_error

    def _via_gateway(
        self,
        prompt: str,
        system: Optional[str],
        temperature: float,
        max_output_tokens: int,
    ) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = httpx.post(
            f"{settings.ai_gateway_base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.ai_gateway_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.ai_gateway_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_output_tokens,
            },
            timeout=60.0,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _via_google_sdk(
        self,
        prompt: str,
        system: Optional[str],
        temperature: float,
        max_output_tokens: int,
    ) -> str:
        import google.generativeai as genai

        if not settings.gemini_api_key:
            raise ExternalServiceError("No Gemini API key configured.")

        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            system_instruction=system,
        )
        result = model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            },
        )
        return result.text
