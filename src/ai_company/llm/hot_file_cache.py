"""Per-session hot-file cache + output caps (GO-4).

Session-start context (AGENTS.md, STATUS.md, ECL summary/tasks,
company-registry.yaml) is injected once; repeat reads within a session
serve the in-session copy keyed by mtime, not disk I/O. Tool outputs are
capped at 50 KB and grep results at 50 matches, with truncation surfaced.

D-1 dedup — where things live
-------------------------------
- Content LRU for injection: this module (``SessionHotFileCache``).
- Pointer pre-check for ToolRunner: ``executor/read_cache.SessionReadCache``
  (returns a step pointer, never content; single executor read-cache).
- Byte-cap implementation: ``executor/tool_validation.truncate_to_cap``
  (this module's :func:`cap_tool_output` delegates to it).
- Token cache metrics: ``llm/cache_metrics`` (canonical).
"""

from __future__ import annotations

import logging
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ai_company.executor.tool_validation import OUTPUT_CAP_BYTES

logger = logging.getLogger(__name__)

# Canonical truncation lives in executor/tool_validation.truncate_to_cap
# (D-1 dedup: one byte-cap implementation). TOOL_OUTPUT_CAP_BYTES mirrors
# tool_validation.OUTPUT_CAP_BYTES (both 50 KiB) for callers that import
# the cap from the llm cache module.
TOOL_OUTPUT_CAP_BYTES = OUTPUT_CAP_BYTES
GREP_RESULT_CAP = 50

# Session-start injection set (relative to project root, when present).
SESSION_START_FILES = (
    "AGENTS.md",
    "docs/STATUS.md",
    "harness/changes/active/summary.md",
    "harness/changes/active/tasks.md",
    "company-registry.yaml",
    "config/company/guardrails.yaml",
)

# Top hot files from the 2026-11-08 audit (D4), workspace-relative.
HOT_FILES = (
    "src/ai_company/dashboard/api.py",
    "company-registry.yaml",
    "AGENTS.md",
    "harness/changes/active/summary.md",
    "docs/STATUS.md",
    "src/ai_company/dashboard/static/js/app.js",
    "src/App.tsx",
    "src/components/FloatingNav.tsx",
    "src/data/siteContent.ts",
    "src/ai_company/dashboard/app.py",
    "src/ai_company/executor/loop.py",
    "harness/changes/active/tasks.md",
    "package.json",
    "src/ai_company/model_router.py",
    "src/ai_company/generator.py",
)


@dataclass
class CacheEntry:
    content: str
    mtime: float
    size_bytes: int


def cap_tool_output(text: str, cap_bytes: int = TOOL_OUTPUT_CAP_BYTES) -> tuple[str, bool]:
    """Truncate *text* to *cap_bytes*; returns ``(text, was_truncated)``.

    Delegates to :func:`tool_validation.truncate_to_cap` so there is a
    single byte-cap implementation (D-1). The returned text keeps the
    ``(str, bool)`` shape this module has always exposed.
    """
    from ai_company.executor.tool_validation import truncate_to_cap

    if text is None:
        return "", False
    result = truncate_to_cap(text, cap_bytes)
    return result.text, result.truncated


def cap_grep_results(results: list[Any], cap: int = GREP_RESULT_CAP) -> tuple[list[Any], bool]:
    """Cap grep/glob results at *cap*; truncation is surfaced, not silent."""
    if len(results) <= cap:
        return list(results), False
    return list(results[:cap]), True


def build_session_start_injection(root: str | Path) -> dict[str, str]:
    """Read session-start files once; missing files are skipped, not faked."""
    base = Path(root)
    injected: dict[str, str] = {}
    for rel in SESSION_START_FILES:
        path = base / rel
        try:
            if path.is_file():
                injected[rel] = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            logger.debug("Session-start injection skipped unreadable file: %s", rel, exc_info=True)
    return injected


class SessionHotFileCache:
    """Per-session LRU keyed by normalized path with mtime invalidation.

    Callers must use one instance per session; entries never leak across
    sessions. ``edit``/``write`` to a path should call :meth:`invalidate`.
    """

    def __init__(self, session_id: str, max_entries: int = 100) -> None:
        self.session_id = session_id
        self.max_entries = max(1, int(max_entries))
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.invalidations = 0

    @staticmethod
    def _key(path: str | Path) -> str:
        return str(Path(path)).replace("\\", "/").lower()

    @property
    def dedup_hit_rate(self) -> float:
        total = self.hits + self.misses
        return (self.hits / total) if total else 0.0

    def get(self, path: str | Path) -> str | None:
        """Return cached content on mtime hit, else None (miss)."""
        key = self._key(path)
        entry = self._cache.get(key)
        if entry is None:
            self.misses += 1
            return None
        try:
            current_mtime = Path(path).stat().st_mtime
        except OSError:
            self._cache.pop(key, None)
            self.misses += 1
            return None
        if current_mtime != entry.mtime:
            self._cache.pop(key, None)
            self.invalidations += 1
            self.misses += 1
            return None
        self._cache.move_to_end(key)
        self.hits += 1
        return entry.content

    def put(self, path: str | Path, content: str) -> None:
        """Store *content* (capped at 50 KB) keyed by path + current mtime."""
        key = self._key(path)
        capped, _ = cap_tool_output(content)
        try:
            mtime = Path(path).stat().st_mtime
        except OSError:
            mtime = 0.0
        self._cache[key] = CacheEntry(
            content=capped, mtime=mtime, size_bytes=len(capped.encode("utf-8", errors="ignore"))
        )
        self._cache.move_to_end(key)
        while len(self._cache) > self.max_entries:
            self._cache.popitem(last=False)

    def invalidate(self, path: str | Path) -> None:
        """Self-invalidation after edit/write within the session."""
        if self._cache.pop(self._key(path), None) is not None:
            self.invalidations += 1

    def clear(self) -> None:
        self._cache.clear()

    def stats(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "entries": len(self._cache),
            "hits": self.hits,
            "misses": self.misses,
            "invalidations": self.invalidations,
            "dedup_hit_rate": round(self.dedup_hit_rate, 4),
        }
