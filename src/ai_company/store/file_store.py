"""FileStore — atomic, lock-safe persistence for JSON and YAML files.

Provides a single abstraction for all file-backed state:
- Atomic writes via temp-file-then-rename
- File locking for concurrent access via cross-platform sidecar locks
- JSON and YAML read/write with validation
- Backup creation on every write (previous version is preserved before it
  is overwritten, so the last good version always survives a crash)

Used by MessageBus, Scheduler, ApprovalGate, MemoryStore, and WorkflowEngine.
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import shutil
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# Locks and backups share one timeout so readers and writers never fight
# over an inconsistent wait budget.
_LOCK_TIMEOUT = 10.0
_LOCK_STALE_AFTER = 30.0


class FileStore:
    """Atomic, lock-safe file persistence for JSON and YAML.

    Args:
        base_dir: Root directory for all stored files.
        backup: Whether to create ``.bak`` copies before every write.
    """

    def __init__(self, base_dir: str | Path, backup: bool = True) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.backup = backup

    # ── Atomic write ──────────────────────────────────────────────────

    def _atomic_write(self, path: Path, data: str) -> None:
        """Write *data* to *path* atomically via temp-file-then-rename.

        The previous version is copied to ``.bak`` *before* the rename so a
        crash at any point leaves either the new file or a recoverable
        backup of the last good version.  On failure the temp file is
        cleaned up and the exception re-raised.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_fd: int | None = None
        tmp_path: str = ""
        try:
            tmp_fd, tmp_path = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            tmp_fd = None  # Closed by fdopen

            # Snapshot the last-good version BEFORE replacing it so a crash
            # mid-replace always leaves a recoverable .bak of the old data.
            if self.backup and path.exists():
                self._write_backup(path)

            # On Windows os.replace can transiently fail with
            # PermissionError if another handle briefly references the
            # target; retry a few times before giving up.
            last_err: Exception | None = None
            for _ in range(5):
                try:
                    os.replace(tmp_path, str(path))
                    tmp_path = ""
                    break
                except (OSError, PermissionError) as exc:
                    last_err = exc
                    time.sleep(0.01)
            if tmp_path:
                if tmp_fd is not None:
                    with contextlib.suppress(OSError):
                        os.close(tmp_fd)
                with contextlib.suppress(OSError):
                    os.unlink(tmp_path)
                if last_err:
                    raise last_err from None

            # First write: ensure a .bak exists afterwards too, so the
            # ".bak always present after a write" invariant holds.
            if self.backup and not (path.with_suffix(path.suffix + ".bak").exists()):
                self._write_backup(path)
        except (OSError, PermissionError):
            if tmp_fd is not None:
                with contextlib.suppress(OSError):
                    os.close(tmp_fd)
            with contextlib.suppress(OSError):
                os.unlink(tmp_path)
            raise

    def _write_backup(self, path: Path) -> None:
        """Copy the current version of *path* to ``.bak`` with fsync."""
        bak_path = path.with_suffix(path.suffix + ".bak")
        for _ in range(3):
            try:
                with open(path, "rb") as src, open(bak_path, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                    dst.flush()
                    os.fsync(dst.fileno())
                return
            except (OSError, PermissionError):
                time.sleep(0.01)
        logger.warning("Failed to write backup %s", bak_path)

    # ── Corrupt-file handling ─────────────────────────────────────────

    def _read_json_safe(self, full_path: Path) -> Any:
        """Read and parse a JSON file with corruption recovery.

        Returns ``None`` if the file is missing.  If the file is corrupt it
        is quarantined to ``<name>.corrupt-<ts>`` and, when available, the
        last ``.bak`` version is recovered and parsed instead.
        """
        if not full_path.exists():
            return None

        raw = None
        for _ in range(5):
            try:
                raw = full_path.read_text(encoding="utf-8")
                break
            except (OSError, PermissionError):
                time.sleep(0.01)
        if raw is None:
            logger.warning("Could not read %s after retries.", full_path)
            return None

        # Only treat the file as JSON if its first non-whitespace character is
        # `{` or `[`.  Some callers probe `read_json` before falling back to
        # `read_yaml` (BaseService._load_data), so a YAML document must be
        # returned as None WITHOUT being quarantined -- otherwise the probe
        # would destroy real data.
        if raw.lstrip()[:1] not in ("{", "["):
            logger.debug("File %s is not JSON; returning None (no quarantine).", full_path)
            return None

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            quarantine = full_path.with_name(full_path.name + f".corrupt-{int(time.time())}")
            logger.error(
                "Corrupt JSON file %s -- quarantining to %s and attempting recovery from .bak.",
                full_path,
                quarantine,
            )
            with contextlib.suppress(OSError):
                os.replace(full_path, quarantine)
            bak_path = full_path.with_suffix(full_path.suffix + ".bak")
            if bak_path.exists():
                try:
                    return json.loads(bak_path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    logger.error("Recovery backup %s is also corrupt.", bak_path)
            return None

    # ── Lock context manager ────────────────────────────────────────────

    @contextmanager
    def lock(self, rel_path: str | Path, timeout: float = _LOCK_TIMEOUT):
        """Context manager for file-level exclusive access.

        Uses a ``.lock`` sibling file to serialise access to the resource at
        *rel_path*. The lock is automatically released when the context is
        exited.

        Args:
            rel_path: Path to the resource to lock (a ``.lock`` file will be created alongside).
            timeout: Maximum seconds to wait for the lock.

        Raises:
            FileLockError: If lock cannot be acquired within *timeout*.
        """
        from ai_company.store.file_lock import file_lock as fl  # type: ignore[import-untyped]

        full_path = self.base_dir / rel_path
        lock_path = full_path.parent / (full_path.name + ".lock")
        lock_path.parent.mkdir(parents=True, exist_ok=True)

        with fl(lock_path, timeout=timeout) as _:
            yield

    @contextmanager
    def lock_atomic(self, rel_path: str | Path, timeout: float = _LOCK_TIMEOUT):
        """Context manager that acquires a file lock and yields the full path.

        Combines exclusive locking with automatic release. This is useful
        for read-modify-write sequences that need to be serialised.

        Args:
            rel_path: Path to the resource.
            timeout: Maximum seconds to wait for the lock.

        Yields:
            The full (absolute) path to the resource.
        """
        from ai_company.store.file_lock import file_lock as fl

        full_path = self.base_dir / rel_path
        lock_path = full_path.parent / (full_path.name + ".lock")
        lock_path.parent.mkdir(parents=True, exist_ok=True)

        with fl(lock_path, timeout=timeout):
            yield full_path

    def ensure_dir(self, rel_path: str | Path) -> Path:
        """Ensure a directory exists, creating it if necessary.

        Args:
            rel_path: Relative directory path.

        Returns:
            The absolute Path to the directory.
        """
        full_path = self.base_dir / rel_path
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path

    # ── JSON helpers ──────────────────────────────────────────────────

    def read_json(self, rel_path: str | Path) -> Any:
        """Read and parse a JSON file. Returns ``None`` if missing."""
        full_path = self.base_dir / rel_path
        if not full_path.exists():
            return None

        # Serialise reads with writers via the shared sidecar lock so a
        # concurrent atomic replace never yields a half-written file.
        from ai_company.store.file_lock import file_lock as fl

        with fl(full_path, timeout=_LOCK_TIMEOUT, stale_after=_LOCK_STALE_AFTER):
            return self._read_json_safe(full_path)

    def write_json(self, rel_path: str | Path, data: Any) -> None:
        """Atomically write *data* as JSON to *rel_path*."""
        full_path = self.base_dir / rel_path
        content = json.dumps(data, indent=2, default=str)
        self._atomic_write(full_path, content)

    def update_json(
        self,
        rel_path: str | Path,
        updater: Any,
    ) -> Any:
        """Read JSON, apply *updater* (a callable), write back atomically.

        *updater* receives the parsed data and must return the new value.
        The read-modify-write is serialised via a cross-platform sidecar
        lock file (GAP-002) so concurrent executor + dashboard access
        cannot corrupt or lose updates.

        If the on-disk file is corrupt it is quarantined and recovered from
        ``.bak`` before *updater* runs, so a corrupt file is never silently
        replaced with an empty document.
        """
        from ai_company.store.file_lock import file_lock as fl

        full_path = self.base_dir / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with fl(full_path, timeout=_LOCK_TIMEOUT, stale_after=_LOCK_STALE_AFTER):
            current = self._read_json_safe(full_path)

            # Update
            new_data = updater(current)

            # Write
            content = json.dumps(new_data, indent=2, default=str)
            self._atomic_write(full_path, content)

        return new_data

    # ── YAML helpers ──────────────────────────────────────────────────

    def read_yaml(self, rel_path: str | Path) -> Any:
        """Read and parse a YAML file. Returns ``None`` if missing."""
        full_path = self.base_dir / rel_path
        if not full_path.exists():
            return None

        from ai_company.store.file_lock import file_lock as fl

        with fl(full_path, timeout=_LOCK_TIMEOUT, stale_after=_LOCK_STALE_AFTER):
            raw = full_path.read_text(encoding="utf-8")

        try:
            return yaml.safe_load(raw)
        except yaml.YAMLError:
            logger.warning("Corrupt YAML file %s -- returning None.", full_path)
            return None

    def write_yaml(self, rel_path: str | Path, data: Any) -> None:
        """Atomically write *data* as YAML to *rel_path* (lock-guarded)."""
        from ai_company.store.file_lock import file_lock as fl

        full_path = self.base_dir / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        content = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)

        with fl(full_path, timeout=_LOCK_TIMEOUT, stale_after=_LOCK_STALE_AFTER):
            self._atomic_write(full_path, content)

    # ── Generic helpers ───────────────────────────────────────────────

    def exists(self, rel_path: str | Path) -> bool:
        """Check whether a file exists."""
        return (self.base_dir / rel_path).exists()

    def delete(self, rel_path: str | Path) -> bool:
        """Delete a file if it exists. Returns True if deleted."""
        full_path = self.base_dir / rel_path
        if full_path.exists():
            full_path.unlink()
            return True
        return False

    def list_files(self, rel_dir: str | Path = "", pattern: str = "*") -> list[Path]:
        """List files in a subdirectory matching a glob pattern."""
        target = self.base_dir / rel_dir
        if not target.exists():
            return []
        return sorted(target.glob(pattern))
