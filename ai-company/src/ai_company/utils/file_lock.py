"""Cross-platform file locking utilities for concurrent access.

Provides atomic file operations with proper locking to prevent race conditions
when multiple processes access shared state files (JSON, YAML).
"""

from __future__ import annotations

import logging
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

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
    import msvcrt
    import time

    fd = None
    start_time = time.monotonic()

    try:
        while True:
            try:
                fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR)
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if fd is not None:
                    os.close(fd)
                    fd = None
                elapsed = time.monotonic() - start_time
                if elapsed >= timeout:
                    raise FileLockError(
                        f"Could not acquire lock on {lock_path} within {timeout}s"
                    )
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
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except (OSError, IOError):
                if fd is not None:
                    os.close(fd)
                    fd = None
                elapsed = time.monotonic() - start_time
                if elapsed >= timeout:
                    raise FileLockError(
                        f"Could not acquire lock on {lock_path} within {timeout}s"
                    )
                time.sleep(poll_interval)

        logger.debug("Acquired file lock: %s", lock_path)
        yield

    finally:
        if fd is not None:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
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
) -> Generator[tempfile._TemporaryFileWrapper, None, None]:
    """Write to a temp file, then atomically rename on exit.

    This prevents partial writes from corrupting the target file.
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

        # Atomic rename
        os.replace(tmp_path, str(path))
        tmp_path = None

    finally:
        if tmp_fd is not None:
            os.close(tmp_fd)
        if tmp_path is not None:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
