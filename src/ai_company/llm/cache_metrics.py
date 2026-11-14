"""Renormalized cache metrics — never derive hit-rate from cache_write.

Provider usage objects (Anthropic-family) name the write side
``cache_creation_input_tokens`` / ``cache_creation``, not ``cache.write``.
Historical opencode.db rows therefore have ``cache_write = 0`` everywhere
while ``cache_read`` is billions. The honest metrics are:

- ``cache_read_ratio = cache_read / (input + cache_read)``
- ``burn_multiplier = (input + cache_read) / max(input, 1)``

``cache_write_reported`` is a boolean gate: while it is False the
dashboard must hide any hit-rate tile and show an "unmetered provider"
banner instead of charting 0 as efficiency.
"""

from __future__ import annotations

from typing import Any

# Keys that carry the cache-write side in provider usage payloads.
_CACHE_WRITE_KEYS = (
    "cache_creation_input_tokens",
    "cache_creation_tokens",
    "cache_creation",
    "cache_write",
    "tokens_cache_write",
    "cacheWriteTokens",
    "cache_write_tokens",
)
_CACHE_READ_KEYS = (
    "cache_read_input_tokens",
    "cache_read_tokens",
    "cache_read",
    "tokens_cache_read",
    "cacheReadTokens",
    "cache_read_tokens",
)


def _num(value: Any) -> int:
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def _coerce_cache_value(value: Any) -> int:
    """Cache values may be ints or nested dicts (e.g. ephemeral splits)."""
    if isinstance(value, dict):
        total = 0
        for sub in value.values():
            total += _coerce_cache_value(sub)
        return total
    return _num(value)


def extract_cache_write(usage: dict[str, Any] | Any) -> int:
    """Return cache-write tokens from any provider usage shape, else 0.

    Accepts the OpenCode ``tokens.cache.write`` nesting, flat Anthropic
    ``cache_creation_input_tokens`` / ``cache_creation`` (int or
    ``{ephemeral_5m_input_tokens, ephemeral_1h_input_tokens}`` dict),
    and session-table ``tokens_cache_write`` naming.
    """
    if not isinstance(usage, dict):
        return 0
    # Nested OpenCode shape: {"tokens": {"cache": {"write": N, "read": M}}}
    # Zero values are skipped so a stale cache.write=0 does not mask a
    # real top-level cache_creation=50 (the historical recorder bug).
    tokens = usage.get("tokens")
    if isinstance(tokens, dict):
        cache = tokens.get("cache")
        if isinstance(cache, dict):
            for key in ("write", "cache_creation", "cache_creation_input_tokens"):
                if key in cache:
                    value = _coerce_cache_value(cache[key])
                    if value:
                        return value
        for key in _CACHE_WRITE_KEYS:
            if key in tokens:
                value = _coerce_cache_value(tokens[key])
                if value:
                    return value
    cache = usage.get("cache")
    if isinstance(cache, dict):
        for key in ("write", "cache_creation", "cache_creation_input_tokens"):
            if key in cache:
                value = _coerce_cache_value(cache[key])
                if value:
                    return value
    for key in _CACHE_WRITE_KEYS:
        if key in usage:
            value = _coerce_cache_value(usage[key])
            if value:
                return value
    return 0


def extract_cache_read(usage: dict[str, Any] | Any) -> int:
    """Return cache-read tokens from any provider usage shape, else 0."""
    if not isinstance(usage, dict):
        return 0
    tokens = usage.get("tokens")
    if isinstance(tokens, dict):
        cache = tokens.get("cache")
        if isinstance(cache, dict):
            for key in ("read", "cache_read", "cache_read_input_tokens"):
                if key in cache:
                    return _coerce_cache_value(cache[key])
        for key in _CACHE_READ_KEYS:
            if key in tokens:
                return _coerce_cache_value(tokens[key])
    cache = usage.get("cache")
    if isinstance(cache, dict):
        for key in ("read", "cache_read", "cache_read_input_tokens"):
            if key in cache:
                return _coerce_cache_value(cache[key])
    for key in _CACHE_READ_KEYS:
        if key in usage:
            return _coerce_cache_value(usage[key])
    return 0


def normalize_provider_usage(usage: dict[str, Any]) -> dict[str, int]:
    """Normalize a raw provider usage dict to canonical cache fields.

    Regression: ``{input:100, cache_read:900, cache_creation:50}`` must
    yield ``cache_write=50``, never 0.
    """
    return {
        "cache_read": extract_cache_read(usage),
        "cache_write": extract_cache_write(usage),
    }


def compute_cache_metrics(
    *,
    input_tokens: int = 0,
    cache_read: int = 0,
    cache_write: int = 0,
    output_tokens: int = 0,
) -> dict[str, Any]:
    """Compute renormalized cache metrics for one aggregate.

    ``input_tokens`` here is the *uncached* input (provider ``input`` /
    session ``tokens_input``), i.e. ``prompt_tokens - cache_write`` for
    opencode-desktop records. Callers holding only ``cost_records`` rows
    should use :meth:`CostAnalytics.cache_metrics` which does that split.
    """
    inp = max(0, int(input_tokens or 0))
    cr = max(0, int(cache_read or 0))
    cw = max(0, int(cache_write or 0))
    denom = inp + cr
    return {
        "cache_read_volume": cr,
        "cache_write_volume": cw,
        "input_tokens": inp,
        "output_tokens": max(0, int(output_tokens or 0)),
        "cache_read_ratio": (cr / denom) if denom > 0 else 0.0,
        "burn_multiplier": (denom / max(inp, 1)) if denom > 0 else 0.0,
        "cache_write_reported": cw > 0,
        # Dashboard display rule: hide the hit-rate tile while writes are
        # unmetered; show the banner instead.
        "show_hit_rate_tile": cw > 0,
        "unmetered_banner": None
        if cw > 0
        else (
            "Cache-read volume (writes unmetered): provider reported "
            "cache_write=0, so no cache hit-rate is shown."
        ),
        "chart_title": "Cache & Token Burn" if cw > 0 else "Cache-read volume (writes unmetered)",
    }
