"""Abstract LLM provider interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from app.utils.json_parser import parse_json_response


class LLMProvider(ABC):
    """Defines the contract for text-generation providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        temperature: float = 0.4,
        max_output_tokens: int = 2048,
    ) -> str:
        """Generate a text completion for the given prompt."""
        raise NotImplementedError

    def generate_json(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """Generate a completion and parse it into a JSON object."""
        raw = self.generate(
            prompt,
            system=system,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
        return parse_json_response(raw)
