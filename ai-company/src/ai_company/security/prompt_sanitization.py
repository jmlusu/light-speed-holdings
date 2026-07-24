"""Prompt sanitization — prevent injection attacks on agent tasks."""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

# Security audit logger (separate from app logs)
_security_logger = logging.getLogger("ai_company.security.prompt_sanitization")


# Known injection patterns (case-insensitive)
INJECTION_PATTERNS = [
    # Instruction override attempts
    r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+instructions?",
    r"ignore\s+all\s+(the\s+)?rules",
    r"disregard\s+(all\s+)?(previous|prior|above)\s+(instructions?|rules?|guidelines?)",
    r"forget\s+(all\s+)?(previous|prior|above)\s+(instructions?|rules?)",
    r"forget\s+(everything|all|your\s+instructions?)",

    # Role manipulation
    r"you\s+are\s+now\s+(a|an|the)\s+",
    r"act\s+as\s+(a|an|the)\s+",
    r"pretend\s+you\s+are\s+",
    r"roleplay\s+as\s+",
    r"from\s+now\s+on\s+you\s+are\s+",
    r"(act|behave|pretend)\s+(as\s+if|like)\s+you\s+(have|don.t|do\s+not)\s+(have|have\s+any)",
    r"(switch|change)\s+to\s+(debug|admin|root|developer)\s+mode",

    # System prompt extraction
    r"(show|reveal|display|output|print|echo)\s+(me\s+)?(your|the)\s+(system\s+)?(prompt|instructions?|rules?|guidelines?)",
    r"what\s+(are|is)\s+your\s+(system\s+)?(prompt|instructions?|rules?)",
    r"repeat\s+(your|the)\s+(system\s+)?(prompt|instructions?|rules?)",
    r"repeat\s+(all|everything)\s+(your|the)\s+(instructions?|rules?)",

    # Data exfiltration
    r"(send|email|post|upload|transfer|exfiltrate)\s+(all\s+)?(data|files?|secrets?|keys?|credentials?|passwords?|conversation)",
    r"(send|email|post|upload)\s+(to|at)\s+(external|outside|remote)",
    r"curl\s+.*\s+(POST|PUT|PATCH)\s+",
    r"curl\s+(POST|PUT|PATCH)\s+",
    r"wget\s+.*--post\s+",
    r"wget\s+--post\s+",
    r"(curl|wget|fetch)\s+(https?://)",

    # Privilege escalation
    r"(sudo|su|runas|as\s+admin|elevated|root|administrator)",
    r"change\s+(permissions?|ownership|access)",

    # Prompt leaking to third parties
    r"(share|send|give|forward)\s+(this|your|the)\s+(prompt|instruction|task)\s+(with|to)",
    r"(share|send|give|forward)\s+(your|the)\s+(instructions?|rules?|prompt)\s+(with|to)",
]

MAX_PROMPT_LENGTH = 10000


class PromptSanitizer:
    """Sanitize user prompts to prevent injection attacks.

    Usage:
        sanitizer = PromptSanitizer()
        sanitized, was_safe = sanitizer.sanitize(user_prompt)
        if not was_safe:
            return sanitized
    """

    def __init__(
        self,
        patterns: list[str] | None = None,
        max_length: int = MAX_PROMPT_LENGTH,
    ) -> None:
        """Initialize the prompt sanitizer.

        Args:
            patterns: Custom regex patterns to detect (case-insensitive).
                      If None, uses default INJECTION_PATTERNS. If empty list,
                      no pattern detection is used (disables pattern detection).
            max_length: Maximum allowed prompt length in characters.
        """
        if patterns is None:
            patterns = INJECTION_PATTERNS
        self._patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self._max_length = max_length

    def check(self, prompt: str) -> tuple[bool, str]:
        """Check if a prompt contains injection attempts.

        Args:
            prompt: The user prompt to check.

        Returns:
            (is_safe, reason) tuple. is_safe is True if the prompt is safe.
            reason provides details about why the prompt was blocked.
        """
        if not prompt or not prompt.strip():
            return True, ""

        # Length check
        if len(prompt) > self._max_length:
            return False, f"Prompt exceeds maximum length ({len(prompt)} > {self._max_length})"

        # Pattern matching
        for pattern in self._patterns:
            match = pattern.search(prompt)
            if match:
                logger.warning(
                    "Prompt injection detected: pattern='%s' matched='%s' prompt_preview='%s'",
                    pattern.pattern, match.group(), prompt[:100],
                )
                _security_logger.warning(
                    "Prompt injection blocked: pattern=%s match=%s",
                    pattern.pattern, match.group(),
                )
                return False, f"Prompt injection detected: {match.group()}"

        return True, ""

    def sanitize(self, prompt: str) -> tuple[str, bool]:
        """Sanitize a prompt. Returns (sanitized_prompt, was_safe).

        If the prompt is safe, it's returned as-is wrapped in XML tags.
        If unsafe, a blocked response is returned.
        """
        is_safe, reason = self.check(prompt)

        if is_safe:
            # Wrap in XML boundary markers for LLM context isolation
            return f"<USER_TASK>{prompt}</USER_TASK>", True

        # Return a blocked response
        return f"[BLOCKED: Prompt injection detected — {reason}]", False

    @property
    def max_length(self) -> int:
        """Return the configured maximum prompt length."""
        return self._max_length

    @property
    def pattern_count(self) -> int:
        """Return the number of configured injection patterns."""
        return len(self._patterns)


# Module-level convenience
_default_sanitizer: PromptSanitizer | None = None


def get_sanitizer() -> PromptSanitizer:
    """Return the module-level singleton sanitizer."""
    global _default_sanitizer
    if _default_sanitizer is None:
        _default_sanitizer = PromptSanitizer()
    return _default_sanitizer


def check_prompt(prompt: str) -> tuple[bool, str]:
    """Quick check: (is_safe, reason)."""
    return get_sanitizer().check(prompt)


def sanitize_prompt(prompt: str) -> tuple[str, bool]:
    """Quick sanitize: (result, was_safe)."""
    return get_sanitizer().sanitize(prompt)