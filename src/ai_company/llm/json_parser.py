"""Shared JSON parsing utilities for LLM responses.

Extracts the duplicated 3-strategy JSON parsing logic from
``LLMClient._parse_response`` and ``AgentLoop._parse_agent_response``
into a single reusable function.
"""

from __future__ import annotations

import json
import re
from typing import Any


def _strip_trailing_commas(s: str) -> str:
    """Remove trailing commas from JSON objects and arrays, respecting strings."""
    result = []
    in_string = False
    escape = False
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            result.append(ch)
        else:
            if ch == '"':
                in_string = True
                result.append(ch)
            elif ch == ",":
                j = i + 1
                while j < n and s[j].isspace():
                    j += 1
                if j < n and s[j] in ("}", "]"):
                    i = j - 1
                else:
                    result.append(ch)
            else:
                result.append(ch)
        i += 1
    return "".join(result)


def _fix_invalid_escapes(s: str) -> str:
    """Fix unescaped backslashes in JSON strings (e.g. regex \\d -> \\\\d)."""
    result = []
    in_string = False
    escape = False
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if in_string:
            if escape:
                if ch in ('"', "\\", "/", "b", "f", "n", "r", "t", "u"):
                    result.append("\\")
                    result.append(ch)
                else:
                    result.append("\\")
                    result.append("\\")
                    result.append(ch)
                escape = False
            else:
                if ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                    result.append(ch)
                else:
                    result.append(ch)
        else:
            if ch == '"':
                in_string = True
                result.append(ch)
            else:
                result.append(ch)
        i += 1
    if escape:
        result.append("\\")
    return "".join(result)


def _safe_json_loads(text: str) -> dict[str, Any] | Any:
    """Load JSON with trailing comma and invalid escape repair."""
    cleaned = _fix_invalid_escapes(_strip_trailing_commas(text))
    return json.loads(cleaned)


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
        data = _safe_json_loads(content)
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, TypeError):
        pass

    # Attempt 2: extract from markdown code block
    match = re.search(r"```(?:json)?\s*\n(.*?)\n```", content, re.DOTALL)
    if match:
        try:
            data = _safe_json_loads(match.group(1))
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
                    data = _safe_json_loads(content[start : i + 1])
                    if isinstance(data, dict):
                        return data
                except (json.JSONDecodeError, TypeError):
                    start = -1

    return None
