"""Shared JSON parsing utilities for LLM responses.

Extracts the duplicated 3-strategy JSON parsing logic from
``LLMClient._parse_response`` and ``AgentLoop._parse_agent_response``
into a single reusable function.
"""

from __future__ import annotations

import json
import re
from typing import Any


def parse_llm_json(content: str) -> dict[str, Any] | None:
    """Parse LLM response content as JSON, with fallback extraction strategies.

    Attempts:
    1. Direct JSON parse
    2. Extract from markdown code block (````json ... ````)
    3. Find first ``{ ... }`` block from text

    Returns parsed dict or None if all strategies fail.
    """
    # Attempt 1: direct parse
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, TypeError):
        pass

    # Attempt 2: extract from markdown code block
    match = re.search(r"```(?:json)?\s*\n(.*?)\n```", content, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, TypeError):
            pass

    # Attempt 3: find first { ... } block
    depth = 0
    start = -1
    for i, ch in enumerate(content):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start >= 0:
                try:
                    data = json.loads(content[start : i + 1])
                    if isinstance(data, dict):
                        return data
                except (json.JSONDecodeError, TypeError):
                    start = -1

    return None
