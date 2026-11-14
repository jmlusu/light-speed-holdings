"""Session read-dedup cache skeleton (hot-file re-read storm, P1-3).

**Status: SKELETON — not wired into ``ToolRunner``.**

Problem (plan: ``reports/opencode-db-reliability-fix-2026-11-08.md``
section 8): 1,101 files are re-read >10x to fetch session-start context
(``dashboard/api.py`` 974x, ``company-registry.yaml`` 763x, ``AGENTS.md``
552x). Re-reading drives the 15.2B cache-read burn. This module gives the
executor a per-session, LRU-bounded, ``(mtime, size)``-validated cache so
the second ``read`` of an unchanged file returns a pointer instead of
re-reading from disk.

Relationship to existing code (deliberately non-overlapping):

- :class:`ai_company.executor.tool_validation.ToolOutputDeduper` dedupes
  by **content hash** with no eviction and no staleness signal. It is the
  right tool when the content is already in hand.
- :class:`SessionReadCache` dedupes by **file identity + (mtime, size)**
  with LRU eviction. It answers "has this path changed since I read it?"
  *before* the bytes are loaded -- the cheap pre-check that saves the
  re-read entirely. The two compose: cache hit -> pointer; cache miss ->
  read -> hash check in the deduper.
- :func:`ai_company.executor.tool_validation.truncate_to_cap` caps what
  the model *consumes*; this cache caps what the tool *fetches*. A cached
  pointer is a few hundred bytes, far under the 64 KB output cap.

Wiring plan (phase 2, requires harness coordination -- do not wire until
the executor owner approves scale semantics): ``ToolRunner._read`` checks
``SessionReadCache.for_path()``; on hit returns ``{"ref", "note",
"cached": True, ...}`` without ``read_text``; on miss reads and
``put()``s. Session-start context files (``AGENTS.md``,
``company-registry.yaml``, ECL ``summary.md``/``tasks.md``) should instead
be injected once via the memory/recall loop, not re-issued as ``read``
calls at all.

``mtime`` granularity: NTFS mtime + size together catch same-second
edits in practice; an edit preserving both size and mtime (clock skew,
backup restore) is possible in theory -- the hash deduper is the backstop,
and the cache stores the sha256 for optional cross-check. The cache never
serves content whose ``(mtime, size)`` changed.
"""

from __future__ import annotations

import hashlib
import threading
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

#: Default LRU bound: protects session memory against unbounded growth in
#: long sessions while comfortably covering a session's working set.
DEFAULT_MAX_ENTRIES: int = 256

#: Default freshness TTL (seconds). Entries older than this are revalidated
#: even if (mtime, size) still match -- cheap defence against clock skew.
DEFAULT_TTL_SECONDS: float = 3600.0


@dataclass(frozen=True)
class CacheEntry:
    """One cached read: content + the file identity it was read under."""

    path: str
    content: str
    mtime_ns: int
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class CacheHit:
    """A cache hit: pointer for the caller, never the full content."""

    ref_step: int
    path: str
    sha256: str
    size_bytes: int

    def pointer(self) -> dict[str, object]:
        """Tool-result-shaped pointer (few hundred bytes, zero disk I/O)."""
        return {
            "path": self.path,
            "cached": True,
            "ref": f"step-{self.ref_step}",
            "sha256": self.sha256,
            "note": (
                f"unchanged since step {self.ref_step} "
                "(mtime/size verified; re-read returns this pointer)"
            ),
        }


class SessionReadCache:
    """Per-session LRU read cache keyed by resolved path + (mtime, size).

    Thread-safe for the executor loop (single lock; metadata only --
    file I/O happens outside the lock in the caller).
    """

    def __init__(
        self,
        max_entries: int = DEFAULT_MAX_ENTRIES,
        ttl_seconds: float = DEFAULT_TTL_SECONDS,
    ) -> None:
        if max_entries < 1:
            raise ValueError("max_entries must be >= 1")
        self._max_entries = max_entries
        self._ttl_seconds = ttl_seconds
        self._lock = threading.Lock()
        self._entries: OrderedDict[str, CacheEntry] = OrderedDict()
        self._steps: dict[str, int] = {}

    def get(self, path: str, step: int) -> CacheHit | None:
        """Return a hit pointer if *path* is cached AND still fresh.

        Freshness is decided from the live file's ``(mtime, size)``:
        a hit requires exact equality with the cached entry. Stale or
        TTL-expired entries are evicted and reported as misses.
        """
        resolved = str(Path(path).resolve())
        try:
            st = Path(resolved).stat()
        except OSError:
            # Missing/unstatable: let the caller's normal read path report
            # the error; do not serve a cached answer for a vanished file.
            return None
        with self._lock:
            entry = self._entries.get(resolved)
            if entry is None:
                return None
            if entry.mtime_ns != st.st_mtime_ns or entry.size_bytes != st.st_size:
                del self._entries[resolved]
                self._steps.pop(resolved, None)
                return None
            self._entries.move_to_end(resolved)
            ref = self._steps.get(resolved, step)
            return CacheHit(
                ref_step=ref, path=resolved, sha256=entry.sha256, size_bytes=entry.size_bytes
            )

    def put(self, path: str, content: str, step: int) -> CacheEntry:
        """Cache *content* under *path*'s live (mtime, size); LRU-evicts."""
        resolved = str(Path(path).resolve())
        st = Path(resolved).stat()
        digest = hashlib.sha256(content.encode("utf-8", errors="replace")).hexdigest()
        entry = CacheEntry(
            path=resolved,
            content=content,
            mtime_ns=st.st_mtime_ns,
            size_bytes=st.st_size,
            sha256=digest,
        )
        with self._lock:
            self._entries[resolved] = entry
            self._entries.move_to_end(resolved)
            self._steps[resolved] = step
            while len(self._entries) > self._max_entries:
                evicted, _ = self._entries.popitem(last=False)
                self._steps.pop(evicted, None)
        return entry

    def invalidate(self, path: str) -> bool:
        """Drop *path* (call after a known write). Returns True if present."""
        resolved = str(Path(path).resolve())
        with self._lock:
            existed = resolved in self._entries
            self._entries.pop(resolved, None)
            self._steps.pop(resolved, None)
            return existed

    def reset(self) -> None:
        """Clear the cache (new sessions / tests)."""
        with self._lock:
            self._entries.clear()
            self._steps.clear()

    def __len__(self) -> int:
        with self._lock:
            return len(self._entries)
