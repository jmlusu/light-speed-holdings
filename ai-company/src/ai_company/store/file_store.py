"""FileStore — atomic, lock-safe persistence for JSON and YAML files.

Provides a single abstraction for all file-backed state:
- Atomic writes via temp-file-then-rename
- File locking for concurrent access (``msvcrt`` on Windows, ``fcntl`` on POSIX)
- JSON and YAML read/write with validation
- Backup creation on every write

Used by MessageBus, Scheduler, ApprovalGate, MemoryStore, and WorkflowEngine.
"""

from __future__ import annotations

import io
import json
import logging
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# ── Platform-specific file locking ────────────────────────────────────

if os.name == "nt":
    import msvcrt

    def _lock_file(f: io.TextIOWrapper) -> None:
        """Acquire an exclusive lock on an open file (Windows)."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            # If we can't acquire non-blocking, retry with blocking
            try:
                msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
            except OSError:
                logger.warning("Could not acquire file lock on %s", f.name)

    def _unlock_file(f: io.TextIOWrapper) -> None:
        """Release a file lock (Windows)."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
else:
    import fcntl

    def _lock_file(f: io.TextIOWrapper) -> None:
        """Acquire an exclusive lock on an open file (POSIX)."""
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # type: ignore[attr-defined]
        except OSError:
            logger.warning("Could not acquire file lock on %s", f.name)

    def _unlock_file(f: io.TextIOWrapper) -> None:
        """Release a file lock (POSIX)."""
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)  # type: ignore[attr-defined]
        except OSError:
            pass


# ── FileStore ─────────────────────────────────────────────────────────


class FileStore:
    """Atomic, lock-safe file persistence for JSON and YAML.

    Args:
        base_dir: Root directory for all stored files.
        backup: Whether to create ``.bak`` copies after every write.
    """

    def __init__(self, base_dir: str | Path, backup: bool = True) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.backup = backup

    # ── Atomic write ──────────────────────────────────────────────────

    def _atomic_write(self, path: Path, data: str) -> None:
        """Write *data* to *path* atomically via temp-file-then-rename.

        On failure the temp file is cleaned up and the exception re-raised.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_fd: int | None = None
        tmp_path: str = ""
        try:
            tmp_fd, tmp_path = tempfile.mkstemp(
                dir=str(path.parent), suffix=".tmp"
            )
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            tmp_fd = None  # Closed by fdopen
            os.replace(tmp_path, str(path))
        except Exception:
            if tmp_fd is not None:
                try:
                    os.close(tmp_fd)
                except OSError:
                    pass
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

        if self.backup:
            self._write_backup(path)

    def _write_backup(self, path: Path) -> None:
        """Write a ``.bak`` copy of the file after every successful write."""
        bak_path = path.with_suffix(path.suffix + ".bak")
        try:
            bak_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        except OSError:
            logger.warning("Failed to write backup %s", bak_path)

    # ── Lock context manager ────────────────────────────────────────────

    @contextmanager
    def lock(self, rel_path: str | Path, timeout: float = 5.0):
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
    def lock_atomic(self, rel_path: str | Path, timeout: float = 5.0):
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

        with open(full_path, "r", encoding="utf-8") as f:
            _lock_file(f)
            try:
                raw = f.read()
            finally:
                _unlock_file(f)

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("Corrupt JSON file %s — returning None.", full_path)
            return None

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
        The read-modify-write is serialised via a lock file to prevent races.
        """
        full_path = self.base_dir / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = full_path.with_suffix(full_path.suffix + ".lock")

        # Serialise concurrent access via a separate lock file
        with open(lock_path, "w", encoding="utf-8") as lock_f:
            _lock_file(lock_f)
            try:
                # Read
                if full_path.exists():
                    raw = full_path.read_text(encoding="utf-8")
                    try:
                        current = json.loads(raw)
                    except json.JSONDecodeError:
                        current = None
                else:
                    current = None

                # Update
                new_data = updater(current)

                # Write
                content = json.dumps(new_data, indent=2, default=str)
                self._atomic_write(full_path, content)
            finally:
                _unlock_file(lock_f)

        return new_data

    # ── YAML helpers ──────────────────────────────────────────────────

    def read_yaml(self, rel_path: str | Path) -> Any:
        """Read and parse a YAML file. Returns ``None`` if missing."""
        full_path = self.base_dir / rel_path
        if not full_path.exists():
            return None

        with open(full_path, "r", encoding="utf-8") as f:
            _lock_file(f)
            try:
                raw = f.read()
            finally:
                _unlock_file(f)

        try:
            return yaml.safe_load(raw)
        except yaml.YAMLError:
            logger.warning("Corrupt YAML file %s — returning None.", full_path)
            return None

    def write_yaml(self, rel_path: str | Path, data: Any) -> None:
        """Atomically write *data* as YAML to *rel_path*."""
        full_path = self.base_dir / rel_path
        content = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
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
