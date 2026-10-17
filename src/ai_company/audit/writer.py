"""Thread-safe JSONL writer for audit events with size-based log rotation."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import tempfile
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ai_company.data import AuditStore

import contextlib

from ai_company.audit.events import AuditEvent
from ai_company.paths import get_audit_path

logger = logging.getLogger(__name__)

# ── Rotation defaults ────────────────────────────────────────────────

DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10 MB per file
DEFAULT_KEEP_FILES = 5  # Keep last N rotated files

# ── Tamper-evident chain (C1) ────────────────────────────────────────
# Every written line carries two integrity fields injected at write time:
#
#   "__seq"        monotonic sequence number across the whole trail
#   "__prev_hash"  SHA-256 of the *previous line's raw bytes* (with its
#                  trailing newline), forming a hash chain
#
# The first line in a fresh trail references a zero hash.  The reader model
# ignores these keys (``extra="ignore"``), so existing consumers are
# unaffected; a verifier (``audit/integrity.py``) reconstructs the chain to
# detect insertions, deletions, and modifications within the retained window.
_ZERO_HASH = "0" * 64

# ── Payload bounds (ticket #71) ──────────────────────────────────────
# tool_call events embed raw tool args/results; grepping a binary file
# previously stored a ~300 KB mojibake blob in the trail. Bound every
# string and collection so a single event can never bloat the JSONL file.
DEFAULT_MAX_STRING_CHARS = 4096
DEFAULT_MAX_COLLECTION_ITEMS = 200
_TRUNCATION_MARKER = "... [audit-truncated]"


def _sanitize_for_audit(
    value: Any,
    *,
    max_string_chars: int = DEFAULT_MAX_STRING_CHARS,
    max_collection_items: int = DEFAULT_MAX_COLLECTION_ITEMS,
) -> Any:
    """Recursively bound an event payload before it is written to the trail.

    Strings longer than *max_string_chars* are truncated, ``bytes`` values
    are replaced with a size-only placeholder (never raw binary), and
    oversized collections are cut down — so a single tool result can never
    turn the canonical JSONL trail into a multi-MB blob (ticket #71).
    """
    if isinstance(value, str):
        if len(value) <= max_string_chars:
            return value
        return value[:max_string_chars] + _TRUNCATION_MARKER
    if isinstance(value, bytes):
        return f"<audit:bytes len={len(value)}>"
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for index, (key, item) in enumerate(value.items()):
            if index >= max_collection_items:
                sanitized["..."] = (
                    f"<audit:truncated {len(value) - max_collection_items} more items>"
                )
                break
            sanitized[str(key)] = _sanitize_for_audit(
                item,
                max_string_chars=max_string_chars,
                max_collection_items=max_collection_items,
            )
        return sanitized
    if isinstance(value, (list, tuple, set)):
        items = list(value)
        sanitized_list = [
            _sanitize_for_audit(
                item,
                max_string_chars=max_string_chars,
                max_collection_items=max_collection_items,
            )
            for item in items[:max_collection_items]
        ]
        if len(items) > max_collection_items:
            sanitized_list.append(
                f"<audit:truncated {len(items) - max_collection_items} more items>"
            )
        return sanitized_list
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    # Unknown objects (enums, custom types) — represent as bounded text.
    return _sanitize_for_audit(
        repr(value),
        max_string_chars=max_string_chars,
        max_collection_items=max_collection_items,
    )


class AuditWriter:
    """Append-only writer that serializes AuditEvents to a JSONL file.

    Writes are atomic: data goes to a temporary file first, then is
    renamed into place so readers never see a partial line.

    Supports size-based log rotation: when the active log file exceeds
    ``max_bytes``, it is renamed to ``<base>.1`` (shifting older
    rotated files up), and a fresh active file is created.
    """

    def __init__(
        self,
        path: str | Path | None = None,
        max_bytes: int = DEFAULT_MAX_BYTES,
        keep_files: int = DEFAULT_KEEP_FILES,
        database: Any = None,
    ) -> None:
        if path is None:
            # Root-aware default: resolve against the deterministic data root
            # (DASHBOARD_DATA_DIR / project root) instead of the CWD so audit
            # events can never be written into an unrelated working directory.
            # The canonical trail is the single JSONL file
            # ``<data root>/.opencode/audit`` (ticket #59).
            path = str(get_audit_path())
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._max_bytes = max_bytes
        self._keep_files = keep_files
        # Number of events appended since construction (ticket #71): lets the
        # executor smoke-check that a tick which did work also grew the trail.
        self.events_written = 0
        self._audit_store: AuditStore | None = None
        if database is not None:
            # Lazy import to avoid a circular import at module load
            # (data -> audit.events -> audit.__init__ -> writer -> data).
            from ai_company.data import AuditStore, database_is_usable

            if database_is_usable(database):
                self._audit_store = AuditStore(database)

    @property
    def path(self) -> Path:
        """Return the path of the active JSONL file."""
        return self._path

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def write(self, event: AuditEvent) -> None:
        """Append a single event to the log file (atomic)."""
        self.write_batch([event])

    def write_batch(self, events: list[AuditEvent]) -> None:
        """Append multiple events in a single atomic write.

        Each line is chained with ``__seq`` / ``__prev_hash`` integrity
        fields computed from the trail's current on-disk tail — computed
        *inside* the cross-process lock so distinct writer instances (in
        separate processes) keep the chain consistent.

        When a SQLite database was supplied at construction, the events are
        also mirrored to the ``audit_events`` table (best-effort) so the data
        layer stays live (Sprint 2, S2.1).
        """
        if not events:
            return

        # Cross-process safe append: the read-modify-write (rotation + atomic
        # append) is guarded by a sidecar lock so two *processes* (executor,
        # dashboard, worker) never both read-then-replace and silently drop
        # each other's events. The in-process threading lock serialises
        # threads sharing one writer instance; the file lock serialises
        # across process boundaries.
        with self._lock:
            from ai_company.store.file_lock import FileLockError
            from ai_company.store.file_lock import file_lock as _fl

            lock_path = self._path
            try:
                with _fl(lock_path, timeout=5.0, stale_after=30.0):
                    self._maybe_rotate()
                    payload = self._encode_events_chained(events)
                    self._atomic_append(payload)
            except FileLockError:
                logger.error(
                    "Could not acquire audit lock within 5.0s for %s; dropping %d "
                    "audit event(s) to avoid corrupting the trail.",
                    self._path,
                    len(events),
                )
                return
            self.events_written += len(events)

        if self._audit_store is not None:
            try:
                self._audit_store.write_batch(events)
            except Exception:  # noqa: BLE001 - mirror is best-effort
                logger.debug("SQLite audit mirror failed", exc_info=True)

    # ------------------------------------------------------------------
    # Tamper-evident serialization
    # ------------------------------------------------------------------

    def _encode_events_chained(self, events: list[AuditEvent]) -> str:
        """Serialize *events* as chained JSONL lines.

        The chain state (sequence + previous line hash) is derived from the
        current on-disk tail so it is correct even when another process
        appended since this writer was constructed.
        """
        seq, last_hash = self._disk_chain_state()
        lines: list[str] = []
        for event in events:
            seq += 1
            data = _sanitize_for_audit(event.model_dump())
            data["__seq"] = seq
            data["__prev_hash"] = last_hash or _ZERO_HASH
            raw = json.dumps(data, ensure_ascii=False) + "\n"
            last_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            lines.append(raw)
        return "".join(lines)

    def _disk_chain_state(self) -> tuple[int, str | None]:
        """Return ``(last_seq, hash_of_last_line_bytes)`` from disk.

        Reads the tail of the newest available file (the active file, or the
        most recent rotation if the active file is empty).  Falls back to
        ``(0, None)`` for an empty or absent trail.
        """
        source = self._pick_source_file()
        if source is None:
            return 0, None
        try:
            lines = source.read_bytes().splitlines(keepends=True)
        except OSError as exc:
            logger.warning("Could not read audit tail for chaining: %s", exc)
            return 0, None
        if not lines:
            return 0, None
        raw = lines[-1]
        try:
            seq = int(json.loads(raw.strip()).get("__seq", 0))
        except (json.JSONDecodeError, ValueError, TypeError):
            seq = 0
        return seq, hashlib.sha256(raw).hexdigest()

    def _pick_source_file(self) -> Path | None:
        """Return the file whose tail continues the chain.

        The active file wins when it has content; otherwise fall back to the
        newest rotated file (the just-rotated one) so a fresh writer right
        after rotation chains off the retained backlog instead of starting
        the sequence anew.
        """
        if self._path.exists() and self._path.stat().st_size > 0:
            return self._path
        rotated = self.list_rotated_files()
        if rotated:
            return rotated[0]
        return None

    # ------------------------------------------------------------------
    # Log rotation
    # ------------------------------------------------------------------

    def _maybe_rotate(self) -> None:
        """Rotate the log file if it exceeds ``max_bytes``."""
        if not self._path.exists():
            return

        size = self._path.stat().st_size
        if size < self._max_bytes:
            return

        self._rotate()

    def _rotate(self) -> None:
        """Shift rotated files up and create a fresh active log.

        File naming convention (with the canonical ``.opencode/audit`` path)::

            audit       ← active (current)
            audit.1     ← most recent rotation
            audit.2     ← second most recent
            ...
            audit.N     ← oldest (deleted when keep_files exceeded)
        """
        base = self._path.stem  # e.g. "audit"
        parent = self._path.parent
        suffix = self._path.suffix  # ".jsonl"

        # Remove oldest file if it would exceed keep limit
        oldest = parent / f"{base}.{self._keep_files}{suffix}"
        if oldest.exists():
            oldest.unlink()

        # Shift files up: N-1 → N, N-2 → N-1, ..., 1 → 2
        for i in range(self._keep_files - 1, 0, -1):
            src = parent / f"{base}.{i}{suffix}"
            dst = parent / f"{base}.{i + 1}{suffix}"
            if src.exists():
                os.replace(src, dst)

        # Rotate current active file to .1
        first_rotation = parent / f"{base}.1{suffix}"
        os.replace(self._path, first_rotation)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _atomic_append(self, data: str) -> None:
        """Write *data* to the end of the log file atomically.

        Strategy: read existing content, write everything to a
        same-directory temp file, then replace the target via
        ``os.replace`` (atomic on POSIX and NTFS).

        This avoids truncation if the process is interrupted between
        open and close of the real file.
        """
        target = self._path
        tmp_fd: int | None = None
        tmp_path: str | None = None

        try:
            # Create a temporary file in the same directory to guarantee
            # same-filesystem rename.
            tmp_fd, tmp_path = tempfile.mkstemp(
                dir=target.parent,
                prefix=".audit-tmp-",
                suffix=".jsonl",
            )

            # Collect existing bytes so we can reassemble in the temp file.
            existing = b""
            if target.exists():
                existing = target.read_bytes()

            with os.fdopen(tmp_fd, "wb") as tmp_file:
                tmp_fd = None  # fdopen owns it now
                tmp_file.write(existing)
                tmp_file.write(data.encode("utf-8"))

            # Atomic replace — readers see either the old or the new file,
            # never a partial write.
            os.replace(tmp_path, target)
            tmp_path = None  # replace succeeded, nothing to clean up

        finally:
            # Clean up temp file descriptor if fdopen was never called.
            if tmp_fd is not None:
                with contextlib.suppress(OSError):
                    os.close(tmp_fd)
            # Clean up temp file if replace did not happen.
            if tmp_path is not None:
                with contextlib.suppress(OSError):
                    os.remove(tmp_path)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def list_rotated_files(self) -> list[Path]:
        """Return sorted list of rotated log files (most recent first)."""
        base = self._path.stem
        parent = self._path.parent
        suffix = self._path.suffix
        files: list[Path] = []
        for i in range(1, self._keep_files + 1):
            p = parent / f"{base}.{i}{suffix}"
            if p.exists():
                files.append(p)
        return files

    def rotation_info(self) -> dict[str, int | list[str] | str]:
        """Return rotation status information."""
        active_size = self._path.stat().st_size if self._path.exists() else 0
        rotated = self.list_rotated_files()
        return {
            "active_file": str(self._path),
            "active_size_bytes": active_size,
            "max_bytes": self._max_bytes,
            "keep_files": self._keep_files,
            "rotated_count": len(rotated),
            "rotated_files": [str(f) for f in rotated],
        }
