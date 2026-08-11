"""Token counting utilities for LLM cost tracking.

Providers that expose usage metadata (OpenAI-style ``usage`` fields,
Ollama ``prompt_eval_count``/``eval_count``) return authoritative token
counts. When no metadata is available we fall back to a lightweight
heuristic estimator (about 4 characters per token for English text) so
cost tracking stays functional without heavy third-party tokenizer
dependencies such as tiktoken.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any

# Approximate characters per token for English text, per model family.
# English is roughly 4 chars/token; some tokenizers are denser.  The
# values are deliberate approximations, not exact tokenizer results.
_CHARS_PER_TOKEN: dict[str, float] = {
    "default": 4.0,
    "claude": 3.5,  # Anthropic tokenizer is denser than 4 chars/token
    "llama": 4.0,
    "qwen": 3.0,  # Qwen has strong multilingual / CJK handling
    "deepseek": 3.5,
}

# CJK characters typically cost about one token each in multilingual
# tokenizers, so they are counted individually rather than by chars/4.
_CJK_RE = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")


@dataclass(frozen=True)
class TokenUsage:
    """Token counts for a single LLM call.

    Attributes:
        prompt_tokens: Tokens in the prompt / instruction.
        completion_tokens: Tokens in the model's completion.
    """

    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        """Prompt + completion tokens."""
        return self.prompt_tokens + self.completion_tokens


def _chars_per_token(model: str | None) -> float:
    """Return the approximate chars-per-token ratio for a model."""
    if not model:
        return _CHARS_PER_TOKEN["default"]
    lowered = model.lower()
    for key, value in _CHARS_PER_TOKEN.items():
        if key != "default" and key in lowered:
            return value
    return _CHARS_PER_TOKEN["default"]


def count_tokens(text: str, model: str | None = None) -> int:
    """Estimate the number of tokens in ``text``.

    Uses a character-based heuristic (default ~4 chars/token, adjusted
    per model family). CJK characters are counted individually.

    Args:
        text: The text to count.
        model: Optional model identifier used to pick the ratio.

    Returns:
        Estimated token count. Returns 0 for empty or whitespace-only
        input; non-empty text always yields at least 1.
    """
    if not text or not text.strip():
        return 0

    cjk_count = len(_CJK_RE.findall(text))
    non_cjk_chars = len(text) - cjk_count
    estimate = cjk_count + math.ceil(non_cjk_chars / _chars_per_token(model))
    return max(1, estimate)


def join_prompt(system_prompt: str, user_prompt: str) -> str:
    """Join system and user prompts into the single text sent to the model."""
    parts = [p for p in (system_prompt, user_prompt) if p]
    return "\n\n".join(parts)


def count_prompt_tokens(
    system_prompt: str,
    user_prompt: str,
    model: str | None = None,
) -> int:
    """Estimate the token count of the assembled prompt (system + user)."""
    return count_tokens(join_prompt(system_prompt, user_prompt), model)


def usage_from_response(
    response: Any,
    prompt_text: str = "",
    model: str | None = None,
) -> TokenUsage:
    """Build a :class:`TokenUsage` from a provider response.

    Prefers provider-reported usage metadata (OpenAI-style ``usage``
    field, or ``prompt_tokens``/``completion_tokens`` attributes) when a
    positive count is present. Falls back to the heuristic estimator
    otherwise.

    Args:
        response: The provider ``ChatResponse`` (or duck-typed equivalent).
        prompt_text: The full prompt text used for the heuristic fallback.
        model: Model identifier used for the heuristic fallback.

    Returns:
        TokenUsage populated from provider metadata or the heuristic.
    """
    usage = getattr(response, "usage", None) or {}
    if isinstance(usage, dict):
        prompt = usage.get("prompt_tokens")
        completion = usage.get("completion_tokens")
        if (
            isinstance(prompt, (int, float))
            and isinstance(completion, (int, float))
            and (prompt or completion)
        ):
            return TokenUsage(
                prompt_tokens=int(prompt or 0),
                completion_tokens=int(completion or 0),
            )

    # Providers may populate the explicit fields without a usage dict.
    prompt = getattr(response, "prompt_tokens", 0) or 0
    completion = getattr(response, "completion_tokens", 0) or 0
    if prompt or completion:
        return TokenUsage(prompt_tokens=int(prompt), completion_tokens=int(completion))

    # Heuristic fallback for providers that report no usage metadata.
    content = getattr(response, "content", "") or ""
    return TokenUsage(
        prompt_tokens=count_tokens(prompt_text or "", model),
        completion_tokens=count_tokens(content, model),
    )
