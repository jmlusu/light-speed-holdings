"""Cross-platform file locking utilities for concurrent access.

Provides atomic file operations with proper locking to prevent race conditions
when multiple processes access shared state files (JSON, YAML).

The locking implementation (``file_lock`` and ``FileLockError``) is delegated
to :mod:`ai_company.store.file_lock`, the canonical robust cross-process
sidecar lock.  This module keeps :func:`atomic_write` locally and re-exports
the canonical lock so existing importers keep working unchanged.
"""

from __future__ import annotations

import os
import tempfile
import time
from contextlib import contextmanager, suppress
from pathlib import Path
from typing import IO, Any, Generator

from ai_company.store.file_lock import FileLockError
from ai_company.store.file_lock import file_lock as _store_file_lock

__all__ = ["FileLockError", "atomic_write", "file_lock"]


@contextmanager
def file_lock(
    path: str | Path,
    timeout: float = 10.0,
    poll_interval: float = 0.1,
    stale_after: float = 30.0,
) -> Generator[None, None, None]:
    """Context manager that provides an exclusive file lock.

    Thin wrapper delegating to the canonical implementation in
    :mod:`ai_company.store.file_lock` (cross-process sidecar lock).

    Args:
        path: Path to the file to lock (creates a ``.lock`` sibling).
        timeout: Maximum seconds to wait for the lock.
        poll_interval: Seconds between lock acquisition attempts.
        stale_after: Seconds after which an un-refreshed lock is treated as
            orphaned and broken.

    Raises:
        FileLockError: If the lock cannot be acquired within timeout.
    """
    with _store_file_lock(
        path,
        timeout=timeout,
        poll_interval=poll_interval,
        stale_after=stale_after,
    ):
        yield


@contextmanager
def atomic_write(
    path: Path,
    mode: str = "w",
    encoding: str = "utf-8",
    retries: int = 5,
) -> Generator[IO[Any], None, None]:
    """Write to a temp file, then atomically rename on exit.

    This prevents partial writes from corrupting the target file. On
    Windows ``os.replace`` can transiently fail with ``PermissionError``
    while another handle briefly references the target, so the rename is
    retried up to *retries* times before giving up.
    """
    tmp_fd = None
    tmp_path = None

    try:
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=str(path.parent),
            suffix=".tmp",
            prefix=path.stem + ".",
        )
        with os.fdopen(tmp_fd, mode, encoding=encoding) as f:
            tmp_fd = None  # fdopen takes ownership
            yield f
            # Flush before rename
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename (retried on Windows transient PermissionError)
        last_err: Exception | None = None
        tmp_target = str(tmp_path)
        for _ in range(max(1, retries)):
            try:
                os.replace(tmp_target, str(path))
                tmp_path = None
                break
            except (OSError, PermissionError) as exc:
                last_err = exc
                time.sleep(0.01)
        if tmp_path:
            raise last_err or OSError("Could not atomically replace file")

    finally:
        if tmp_fd is not None:
            os.close(tmp_fd)
        if tmp_path is not None:
            with suppress(OSError):
                os.unlink(tmp_path)
