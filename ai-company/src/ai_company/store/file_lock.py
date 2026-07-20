"""Cross-platform file locking utility (stdlib-only, no external deps).

This module provides :func:`file_lock`, a context manager that serialises
access to a shared resource (typically a JSON/YAML state file) across
threads *and* processes.  It is safe on Windows (``win32``) as well as
POSIX and uses only the Python standard library.

Approach
--------
A ``.lock`` *sidecar* file is created next to the resource.  The lock is
acquired by attempting an atomic, exclusive creation of that sidecar via
``os.open(path, O_CREAT | O_EXCL, ...)``.  On POSIX ``O_EXCL`` guarantees
no other process created it first; on Windows the create is atomic and
exclusive for the lifetime of the open handle.  If the create fails (lock
already held) we retry with a small back-off until *timeout* elapses, then
raise :class:`FileLockError`.

The sidecar is always removed in a ``finally`` block so the lock is
released even if the caller raises.  A *stale* lock (a sidecar whose
last-modified time is older than *stale_after* seconds) is broken so a
crashed holder cannot deadlock the system forever.  Staleness is inferred
from the sidecar's mtime only -- we never read or write the open sidecar
file, which would block under Windows share-mode contention.
"""

from __future__ import annotations

import errno
import logging
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

logger = logging.getLogger(__name__)

# Default polling interval (seconds) between lock-acquire attempts.
_DEFAULT_POLL_INTERVAL = 0.02
# Default total time (seconds) to wait before giving up.
_DEFAULT_TIMEOUT = 10.0
# A lock sidecar older than this is assumed orphaned and is broken.
_DEFAULT_STALE_AFTER = 30.0


class FileLockError(Exception):
    """Raised when a file lock cannot be acquired within *timeout*."""


def _is_stale(lock_path: Path, stale_after: float) -> bool:
    """Return True if the lock sidecar looks orphaned by age.

    Uses only the sidecar's modification time, never reading its contents,
    to avoid blocking on Windows where the holder keeps the file open.
    """
    try:
        age = time.time() - lock_path.stat().st_mtime
    except OSError:
        return False
    return age > stale_after


@contextmanager
def file_lock(
    path: str | Path,
    timeout: float = _DEFAULT_TIMEOUT,
    poll_interval: float = _DEFAULT_POLL_INTERVAL,
    stale_after: float = _DEFAULT_STALE_AFTER,
) -> Iterator[None]:
    """Acquire an exclusive cross-process lock for *path*.

    A ``.lock`` sidecar file is created next to *path*.  The context
    manager yields once the lock is held and releases it on exit.

    Args:
        path: The resource file to protect (a sidecar ``<name>.lock`` is
            created alongside it).
        timeout: Maximum seconds to wait for the lock.
        poll_interval: Seconds to wait between acquire attempts.
        stale_after: Seconds after which an un-refreshed lock is treated
            as orphaned and broken.

    Raises:
        FileLockError: If the lock cannot be acquired within *timeout*.
    """
    resource = Path(path)
    lock_path = resource.parent / (resource.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    deadline = time.monotonic() + timeout
    acquired = False
    fd: Optional[int] = None

    try:
        while True:
            try:
                # Atomic exclusive create -- succeeds only if the file does
                # not already exist.
                fd = os.open(
                    str(lock_path),
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                )
                acquired = True
                break
            except OSError as exc:
                # On Windows, O_EXCL on an existing file may raise
                # PermissionError (errno 13 / EACCES) or FileExistsError
                # (errno 17 / EEXIST) rather than a clean EEXIST.  Both
                # mean "lock already held".
                code = getattr(exc, "errno", None)
                if code not in (errno.EEXIST, errno.EACCES):
                    raise
                # Lock held by someone else.  Break an orphaned lock.
                if _is_stale(lock_path, stale_after):
                    logger.warning(
                        "Breaking stale lock %s (age exceeds %ss).",
                        lock_path,
                        stale_after,
                    )
                    try:
                        lock_path.unlink()
                    except OSError:
                        pass
                    continue
                if time.monotonic() >= deadline:
                    raise FileLockError(
                        f"Could not acquire lock {lock_path} within "
                        f"{timeout}s."
                    )
                time.sleep(poll_interval)
        yield
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass
        if acquired:
            try:
                lock_path.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                logger.warning("Failed to remove lock file %s", lock_path)
