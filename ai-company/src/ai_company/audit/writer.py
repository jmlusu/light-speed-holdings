"""Thread-safe JSONL writer for audit events with size-based log rotation."""

from __future__ import annotations

import json
import os
import tempfile
import threading
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from ai_company.audit.events import AuditEvent

# ── Rotation defaults ────────────────────────────────────────────────

DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10 MB per file
DEFAULT_KEEP_FILES = 5  # Keep last N rotated files


class AuditWriter:
    """Append-only writer that serializes AuditEvents to a JSONL file.

    Writes are atomic: data goes to a temporary file first, then is
    renamed into place so readers never see a partial line.

    Supports size-based log rotation: when the active log file exceeds
    ``max_bytes``, it is renamed to ``<base>.1.jsonl`` (shifting older
    rotated files up), and a fresh active file is created.
    """

    def __init__(
        self,
        path: str | Path = ".opencode/audit.jsonl",
        max_bytes: int = DEFAULT_MAX_BYTES,
        keep_files: int = DEFAULT_KEEP_FILES,
    ) -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._max_bytes = max_bytes
        self._keep_files = keep_files

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
        """Append multiple events in a single atomic write."""
        if not events:
            return

        lines = [json.dumps(event.model_dump(), ensure_ascii=False) for event in events]
        payload = "\n".join(lines) + "\n"

        with self._lock:
            self._maybe_rotate()
            self._atomic_append(payload)

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

        File naming convention::

            audit.jsonl       ← active (current)
            audit.1.jsonl     ← most recent rotation
            audit.2.jsonl     ← second most recent
            ...
            audit.N.jsonl     ← oldest (deleted when keep_files exceeded)
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
                try:
                    os.close(tmp_fd)
                except OSError:
                    pass
            # Clean up temp file if replace did not happen.
            if tmp_path is not None:
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

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

    def rotation_info(self) -> dict[str, int | list[str]]:
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
