"""Platform formatters for Pharos publish rails (LinkedIn / Substack).

Each formatter returns a dict of platform-ready content plus diagnostics
(word/char counts, truncation warnings). Formatting is deterministic and
dependency-free so the queue and MCP tools can produce artifacts offline.
"""

from __future__ import annotations

import re
from typing import Any

# LinkedIn hard-caps long posts; keep artifacts comfortably under the ceiling
# so the adapter does not clip text mid-sentence.
LINKEDIN_CHAR_LIMIT = 3000
SUBSTACK_WORD_LIMIT = 8000


def _word_count(text: str) -> int:
    words = re.findall(r"\S+", text)
    return len(words)


def format_linkedin(
    title: str, body: str, *, max_chars: int = LINKEDIN_CHAR_LIMIT
) -> dict[str, Any]:
    """Render a LinkedIn-ready artifact from *title* + *body*.

    Returns::

        {"platform": "linkedin", "text": ..., "char_count": int,
         "word_count": int, "truncated": bool}

    When the combined text exceeds ``max_chars``, ``truncated`` is True and the
    ``text`` is hard-clipped at a word boundary with a continuation marker —
    never silently dropped mid-word.
    """
    combined = f"{title.strip()}\n\n{body.strip()}".strip()
    char_count = len(combined)
    truncated = char_count > max_chars
    if truncated:
        # Clip at the last word boundary under the limit, then append a clear
        # continuation marker so the operator knows the queue holds the full text.
        clipped = combined[: max_chars - 8]
        space = clipped.rfind(" ")
        if space > 0:
            clipped = clipped[:space]
        text = clipped + "\n\n[continued in queue]"
    else:
        text = combined
    return {
        "platform": "linkedin",
        "text": text,
        "char_count": len(text),
        "word_count": _word_count(text),
        "truncated": truncated,
    }


def format_substack(
    title: str, body: str, *, max_words: int = SUBSTACK_WORD_LIMIT
) -> dict[str, Any]:
    """Render a Substack-ready artifact (markdown).

    Substack takes markdown natively; body is passed through as-is so writers
    keep their heading/emphasis structure. Only a length diagnostic is
    produced — content is never rewritten here.
    """
    from_markdown = f"# {title.strip()}\n\n{body.strip()}\n"
    word_count = _word_count(body)
    return {
        "platform": "substack",
        "markdown": from_markdown,
        "word_count": word_count,
        "char_count": len(from_markdown),
        "truncated": word_count > max_words,
    }


__all__ = [
    "LINKEDIN_CHAR_LIMIT",
    "SUBSTACK_WORD_LIMIT",
    "format_linkedin",
    "format_substack",
]
