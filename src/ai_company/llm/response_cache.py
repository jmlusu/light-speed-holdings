"""File-based LLM response cache to avoid redundant API calls.

Caches LLM responses keyed by (system_prompt, user_prompt, model, temperature)
with configurable TTL and max size. Only deterministic queries (temperature=0)
should be cached to avoid serving stale creative outputs.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

_DEFAULT_CACHE_DIR = ".cache/llm"
_DEFAULT_TTL_SECONDS = 3600
_DEFAULT_MAX_SIZE_MB = 100


@dataclass(frozen=True)
class CachedResponse:
    """A cache hit returned by ResponseCache.get()."""

    content: str
    tokens_saved: int
    cost_saved: float


class ResponseCache:
    """File-based cache for LLM responses.

    Args:
        cache_dir: Directory for cached response files.
        ttl_seconds: Time-to-live for cache entries.
        max_size_mb: Maximum cache directory size in MB.
    """

    def __init__(
        self,
        cache_dir: str | Path = _DEFAULT_CACHE_DIR,
        ttl_seconds: int = _DEFAULT_TTL_SECONDS,
        max_size_mb: int = _DEFAULT_MAX_SIZE_MB,
    ) -> None:
        self._cache_dir = Path(cache_dir)
        self._ttl = ttl_seconds
        self._max_size = max_size_mb * 1024 * 1024

    @staticmethod
    def _generate_key(
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
    ) -> str:
        """Generate a deterministic SHA-256 cache key."""
        raw = f"{system_prompt}\n{user_prompt}\n{model}\n{temperature}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
    ) -> CachedResponse | None:
        """Return a cached response if available and not expired."""
        key = self._generate_key(system_prompt, user_prompt, model, temperature)
        cache_path = self._cache_dir / f"{key}.json"

        if not cache_path.exists():
            return None

        try:
            age = time.time() - cache_path.stat().st_mtime
            if age > self._ttl:
                cache_path.unlink(missing_ok=True)
                return None

            data = json.loads(cache_path.read_text(encoding="utf-8"))
            return CachedResponse(
                content=data["content"],
                tokens_saved=data.get("tokens_saved", 0),
                cost_saved=data.get("cost_saved", 0.0),
            )
        except (json.JSONDecodeError, KeyError, OSError):
            return None

    def set(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        response_content: str,
        tokens_used: int = 0,
        cost_usd: float = 0.0,
    ) -> None:
        """Store a response in the cache."""
        key = self._generate_key(system_prompt, user_prompt, model, temperature)
        cache_path = self._cache_dir / f"{key}.json"

        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)

            # Evict oldest entries if cache exceeds size limit
            self._evict_if_needed()

            cache_path.write_text(
                json.dumps(
                    {
                        "content": response_content,
                        "tokens_saved": tokens_used,
                        "cost_saved": cost_usd,
                        "model": model,
                        "cached_at": time.time(),
                    }
                ),
                encoding="utf-8",
            )
        except OSError:
            logger.debug("Cache write failed for key %s", key[:12], exc_info=True)

    def clear(self) -> int:
        """Remove all cache entries. Returns number of files removed."""
        count = 0
        if not self._cache_dir.exists():
            return count
        for f in self._cache_dir.glob("*.json"):
            try:
                f.unlink()
                count += 1
            except OSError:
                pass
        return count

    def _evict_if_needed(self) -> None:
        """Remove oldest entries when total cache size exceeds the limit."""
        if not self._cache_dir.exists():
            return

        files = sorted(self._cache_dir.glob("*.json"), key=lambda f: f.stat().st_mtime)
        total = sum(f.stat().st_size for f in files)

        while total > self._max_size and files:
            oldest = files.pop(0)
            try:
                total -= oldest.stat().st_size
                oldest.unlink()
            except OSError:
                pass

    @property
    def stats(self) -> dict[str, int | float]:
        """Return cache statistics."""
        if not self._cache_dir.exists():
            return {"entries": 0, "size_mb": 0.0}
        files = list(self._cache_dir.glob("*.json"))
        total_bytes = sum(f.stat().st_size for f in files)
        return {"entries": len(files), "size_mb": round(total_bytes / (1024 * 1024), 3)}
