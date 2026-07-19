"""Thread-safe JSONL writer for audit events."""

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


class AuditWriter:
    """Append-only writer that serializes AuditEvents to a JSONL file.

    Writes are atomic: data goes to a temporary file first, then is
    renamed into place so readers never see a partial line.
    """

    def __init__(self, path: str | Path = ".opencode/audit.jsonl") -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    @property
    def path(self) -> Path:
        """Return the path of the JSONL file."""
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
            self._atomic_append(payload)

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
