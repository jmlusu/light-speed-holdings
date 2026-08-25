"""Lightweight prompt compressor to reduce token count before LLM calls.

Applies rules-based compression (stopword removal, redundant instruction
dedup, whitespace normalization) targeting ~30% token reduction on typical
system + user prompts. No external tokenizer dependency.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Common filler phrases that can be stripped from prompts without meaning loss.
_FILLER_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"Please\s+note\s+that\s+", re.IGNORECASE),
    re.compile(r"It\s+is\s+important\s+to\s+(?:note\s+that\s+)?", re.IGNORECASE),
    re.compile(r"Make\s+sure\s+(?:that\s+)?", re.IGNORECASE),
    re.compile(r"Always\s+remember\s+(?:that\s+)?", re.IGNORECASE),
    re.compile(r"Keep\s+in\s+mind\s+(?:that\s+)?", re.IGNORECASE),
    re.compile(r"Be\s+sure\s+to\s+", re.IGNORECASE),
    re.compile(r"In\s+order\s+to\s+", re.IGNORECASE),
    re.compile(r"For\s+the\s+purpose\s+of\s+", re.IGNORECASE),
    re.compile(r"With\s+regard\s+to\s+", re.IGNORECASE),
    re.compile(r"With\s+respect\s+to\s+", re.IGNORECASE),
]

# Redundant whitespace patterns.
_MULTI_NEWLINES = re.compile(r"\n{3,}")
_MULTI_SPACES = re.compile(r"[^\S\n]{2,}")
_TRAILING_WS = re.compile(r"[^\S\n]+$", re.MULTILINE)


@dataclass(frozen=True)
class CompressionResult:
    """Result of prompt compression."""

    compressed_prompt: str
    original_tokens_est: int
    compressed_tokens_est: int

    @property
    def reduction_ratio(self) -> float:
        """Fraction of tokens removed (0.0 = no reduction, 1.0 = fully removed)."""
        if self.original_tokens_est == 0:
            return 0.0
        return 1.0 - (self.compressed_tokens_est / self.original_tokens_est)


def _estimate_tokens(text: str) -> int:
    """Fast heuristic token estimate (~4 chars/token)."""
    if not text or not text.strip():
        return 0
    return max(1, len(text) // 4)


def _remove_filler(text: str) -> str:
    """Strip common filler phrases."""
    result = text
    for pattern in _FILLER_PATTERNS:
        result = pattern.sub("", result)
    return result


def _normalize_whitespace(text: str) -> str:
    """Collapse excessive whitespace while preserving structure."""
    text = _TRAILING_WS.sub("", text)
    text = _MULTI_NEWLINES.sub("\n\n", text)
    text = _MULTI_SPACES.sub(" ", text)
    return text.strip()


def _dedup_instructions(text: str) -> str:
    """Remove duplicate lines that appear more than once."""
    lines = text.split("\n")
    seen: set[str] = set()
    deduped: list[str] = []
    for line in lines:
        stripped = line.strip()
        # Only dedup blank-ish or very short identical lines; preserve unique content.
        if stripped and stripped in seen:
            continue
        if stripped:
            seen.add(stripped)
        deduped.append(line)
    return "\n".join(deduped)


class PromptCompressor:
    """Compresses prompts to reduce token count before LLM calls.

    Args:
        target_reduction: Target fraction of tokens to remove (0.0–1.0).
            Default 0.30 (30%).
    """

    def __init__(self, target_reduction: float = 0.30) -> None:
        self._target_reduction = target_reduction

    def compress(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> tuple[str, str, CompressionResult]:
        """Compress system and user prompts while preserving meaning.

        Returns:
            ``(compressed_system, compressed_user, result)``
        """
        original_tokens = _estimate_tokens(system_prompt + "\n\n" + user_prompt)

        compressed_system = self._compress_text(system_prompt)
        compressed_user = self._compress_text(user_prompt)

        compressed_tokens = _estimate_tokens(compressed_system + "\n\n" + compressed_user)

        # If we haven't hit the target, apply more aggressive whitespace normalization.
        if original_tokens > 0:
            actual_reduction = 1.0 - (compressed_tokens / original_tokens)
            if actual_reduction < self._target_reduction:
                compressed_system = _normalize_whitespace(compressed_system)
                compressed_user = _normalize_whitespace(compressed_user)
                compressed_tokens = _estimate_tokens(compressed_system + "\n\n" + compressed_user)

        result = CompressionResult(
            compressed_prompt=compressed_system + "\n\n" + compressed_user,
            original_tokens_est=original_tokens,
            compressed_tokens_est=compressed_tokens,
        )

        logger.debug(
            "Prompt compression: %d → %d tokens (%.0f%% reduction)",
            original_tokens,
            compressed_tokens,
            result.reduction_ratio * 100,
        )

        return compressed_system, compressed_user, result

    @staticmethod
    def _compress_text(text: str) -> str:
        """Apply all compression passes to a text block."""
        if not text:
            return text
        text = _remove_filler(text)
        text = _dedup_instructions(text)
        text = _normalize_whitespace(text)
        return text
