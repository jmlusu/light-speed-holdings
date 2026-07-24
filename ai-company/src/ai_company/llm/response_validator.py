"""LLM response validation — validate structure and content for safety."""

from __future__ import annotations

import re
import logging
from typing import Any

logger = logging.getLogger(__name__)

# Suspicious content patterns that should never appear in LLM responses
SUSPICIOUS_PATTERNS = [
    # Safety bypass attempts
    r"ignore\s+safety",
    r"bypass\s+(approval|safety|security)",
    r"override\s+(safety|security|approval)",
    r"disable\s+(safety|security|filter)",

    # Data exfiltration signals
    r"exfiltrate",
    r"(send|transmit|upload)\s+(all\s+)?(data|secrets?|keys?|credentials?)",
    r"(curl|wget|http)\s+.*\s+(POST|PUT|PATCH)",

    # Prompt injection in output
    r"<SYSTEM>",
    r"\[SYSTEM\]",
    r"system\s+prompt:",

    # Unauthorized actions — word boundaries prevent false matches on
    # substrings like "result" (contains "su") or "successfully".
    r"\bsudo\b",
    r"\bsu\b",
    r"\brunas\b",
    r"as\s+admin",
    r"chmod\s+777",
    r"rm\s+-rf\s+/",
]

# Required fields in a valid agent loop response
REQUIRED_FIELDS = ["plan", "result"]
VALID_STEP_FIELDS = ["tool", "args"]


class ResponseValidationError(Exception):
    """Raised when an LLM response fails validation."""

    def __init__(self, message: str, field: str = "", details: dict | None = None):
        super().__init__(message)
        self.field = field
        self.details = details or {}


class LLMResponseValidator:
    """Validate LLM responses for structure and safety.

    Checks:
    1. Required fields present
    2. Plan step structure
    3. Suspicious content detection
    4. Output length limits
    5. Tool call argument validation
    """

    def __init__(
        self,
        suspicious_patterns: list[str] | None = None,
        max_response_length: int = 50000,
        max_plan_steps: int = 20,
    ) -> None:
        self._patterns = [
            re.compile(p, re.IGNORECASE)
            for p in (suspicious_patterns if suspicious_patterns is not None else SUSPICIOUS_PATTERNS)
        ]
        self._max_response_length = max_response_length
        self._max_plan_steps = max_plan_steps

    def validate(self, response: dict[str, Any]) -> tuple[bool, str]:
        """Validate an LLM response.

        Returns:
            (is_valid, reason) tuple.
        """
        if not isinstance(response, dict):
            return False, f"Response must be dict, got {type(response).__name__}"

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in response:
                return False, f"Missing required field: {field}"

        # Validate plan structure
        plan = response.get("plan", [])
        if not isinstance(plan, list):
            return False, f"Plan must be list, got {type(plan).__name__}"

        if len(plan) > self._max_plan_steps:
            return False, f"Plan has {len(plan)} steps, max is {self._max_plan_steps}"

        for i, step in enumerate(plan):
            if not isinstance(step, dict):
                return False, f"Plan step {i} must be dict, got {type(step).__name__}"
            for field in VALID_STEP_FIELDS:
                if field not in step:
                    return False, f"Plan step {i} missing field: {field}"

        # Check response length
        result_str = str(response.get("result", ""))
        if len(result_str) > self._max_response_length:
            return False, f"Result length {len(result_str)} exceeds max {self._max_response_length}"

        # Check for suspicious content in result
        is_safe, reason = self._check_suspicious(result_str)
        if not is_safe:
            return False, f"Suspicious content in result: {reason}"

        # Check for suspicious content in plan steps
        for i, step in enumerate(plan):
            args_str = str(step.get("args", {}))
            is_safe, reason = self._check_suspicious(args_str)
            if not is_safe:
                return False, f"Suspicious content in plan step {i} args: {reason}"

        return True, "valid"

    def validate_strict(self, response: dict[str, Any]) -> dict[str, Any]:
        """Validate and raise on failure. Returns the response if valid."""
        is_valid, reason = self.validate(response)
        if not is_valid:
            raise ResponseValidationError(reason)
        return response

    def _check_suspicious(self, text: str) -> tuple[bool, str]:
        """Check text for suspicious patterns."""
        for pattern in self._patterns:
            match = pattern.search(text)
            if match:
                return False, f"Pattern '{pattern.pattern}' matched '{match.group()}'"
        return True, ""


# Module-level convenience
_default_validator: LLMResponseValidator | None = None


def get_response_validator() -> LLMResponseValidator:
    """Return the module-level singleton."""
    global _default_validator
    if _default_validator is None:
        _default_validator = LLMResponseValidator()
    return _default_validator


def validate_llm_response(response: dict[str, Any]) -> tuple[bool, str]:
    """Quick validation using the module-level singleton."""
    return get_response_validator().validate(response)