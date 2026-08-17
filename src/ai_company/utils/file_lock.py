"""Cross-platform file locking utilities for concurrent access.

Provides atomic file operations with proper locking to prevent race conditions
when multiple processes access shared state files (JSON, YAML).
"""

from __future__ import annotations

import logging
import os
import tempfile
import time
from contextlib import contextmanager, suppress
from pathlib import Path
from typing import IO, Any, Generator

logger = logging.getLogger(__name__)


class FileLockError(Exception):
    """Raised when a file lock cannot be acquired."""


@contextmanager
def file_lock(
    path: Path,
    timeout: float = 10.0,
    poll_interval: float = 0.1,
) -> Generator[None, None, None]:
    """Context manager that provides an exclusive file lock.

    Uses platform-specific locking:
    - Windows: msvcrt.locking()
    - Unix: fcntl.flock()

    Args:
        path: Path to the file to lock (creates .lock sibling).
        timeout: Maximum seconds to wait for the lock.
        poll_interval: Seconds between lock acquisition attempts.

    Raises:
        FileLockError: If the lock cannot be acquired within timeout.
    """
    import platform

    lock_path = Path(str(path) + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    if platform.system() == "Windows":
        yield from _windows_lock(lock_path, timeout, poll_interval)
    else:
        yield from _unix_lock(lock_path, timeout, poll_interval)


def _windows_lock(
    lock_path: Path,
    timeout: float,
    poll_interval: float,
) -> Generator[None, None, None]:
    """Windows file locking using msvcrt."""
    import msvcrt  # Windows-only module
    import time

    fd = None
    start_time = time.monotonic()

    try:
        while True:
            try:
                fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR)
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                break
            except OSError as exc:
                if fd is not None:
                    os.close(fd)
                    fd = None
                elapsed = time.monotonic() - start_time
                if elapsed >= timeout:
                    raise FileLockError(
                        f"Could not acquire lock on {lock_path} within {timeout}s"
                    ) from exc
                time.sleep(poll_interval)

        logger.debug("Acquired file lock: %s", lock_path)
        yield

    finally:
        if fd is not None:
            try:
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            except OSError:
                pass
            finally:
                os.close(fd)
        logger.debug("Released file lock: %s", lock_path)


def _unix_lock(
    lock_path: Path,
    timeout: float,
    poll_interval: float,
) -> Generator[None, None, None]:
    """Unix file locking using fcntl."""
    import fcntl
    import time

    fd = None
    start_time = time.monotonic()

    try:
        while True:
            try:
                fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR)
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)  # type: ignore[attr-defined]
                break
            except (OSError, IOError) as exc:
                if fd is not None:
                    os.close(fd)
                    fd = None
                elapsed = time.monotonic() - start_time
                if elapsed >= timeout:
                    raise FileLockError(
                        f"Could not acquire lock on {lock_path} within {timeout}s"
                    ) from exc
                time.sleep(poll_interval)

        logger.debug("Acquired file lock: %s", lock_path)
        yield

    finally:
        if fd is not None:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)  # type: ignore[attr-defined]
            except (OSError, IOError):
                pass
            finally:
                os.close(fd)
        logger.debug("Released file lock: %s", lock_path)


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
