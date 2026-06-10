"""Utility to robustly parse JSON out of LLM text responses."""
from __future__ import annotations

import json
import re
from typing import Any, Dict

from app.core.exceptions import ExternalServiceError

_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def parse_json_response(text: str) -> Dict[str, Any]:
    """Extract and parse a JSON object from a model response.

    Handles responses wrapped in markdown code fences or containing
    surrounding prose by locating the first balanced JSON object.
    """
    if not text:
        raise ExternalServiceError("The AI returned an empty response.")

    candidate = text.strip()

    fence_match = _FENCE_RE.search(candidate)
    if fence_match:
        candidate = fence_match.group(1).strip()

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass

    start = candidate.find("{")
    end = candidate.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = candidate[start : end + 1]
        try:
            return json.loads(snippet)
        except json.JSONDecodeError as exc:
            raise ExternalServiceError(
                "The AI response could not be parsed as JSON."
            ) from exc

    raise ExternalServiceError("The AI response did not contain valid JSON.")
