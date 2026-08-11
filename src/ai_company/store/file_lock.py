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

The holder writes an ownership token (PID + host) into the sidecar and runs
a lightweight daemon heartbeat thread that refreshes the token and the
sidecar mtime roughly every ``stale_after / 3`` seconds for the whole time
the lock is held.  A *stale* lock is therefore identified reliably:

- a sidecar whose recorded PID is verifiably dead (POSIX) is broken at once;
- a sidecar whose mtime has not been refreshed within *stale_after* seconds
  (either because the holder crashed or because it is on Windows where the
  PID cannot be inspected cheaply) is broken after *stale_after*.

Without the heartbeat, a live holder whose critical section exceeds
*stale_after* would have its lock stolen and two processes could both
believe they held the lock -- corrupting the shared state.  The heartbeat
removes that failure mode.
"""

from __future__ import annotations

import contextlib
import errno
import json
import logging
import os
import socket
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

logger = logging.getLogger(__name__)

# Default polling interval (seconds) between lock-acquire attempts.
_DEFAULT_POLL_INTERVAL = 0.02
# Default total time (seconds) to wait before giving up.
_DEFAULT_TIMEOUT = 10.0
# A lock sidecar not refreshed within this many seconds is assumed orphaned
# and is broken.
_DEFAULT_STALE_AFTER = 30.0


class FileLockError(Exception):
    """Raised when a file lock cannot be acquired within *timeout*."""


def _pid_alive(pid: int) -> bool:
    """Best-effort liveness check for a PID.

    On Windows we cannot cheaply probe another process, so we report alive
    and rely on the mtime/heartbeat staleness check instead.
    """
    if os.name == "nt" or pid <= 0:
        return True
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _is_stale(lock_path: Path, stale_after: float) -> bool:
    """Return True if the lock sidecar looks orphaned.

    The sidecar is examined in this order:

    1. If its recorded owner PID is readable and verifiably dead (POSIX),
       the lock is stale immediately.
    2. Otherwise, if it has not been refreshed (mtime older than
       *stale_after*), it is stale -- this is the fallback on Windows where
       the sidecar may be held open and unreadable by others.

    A live holder refreshes the mtime via its heartbeat, so a lock that is
    merely held for a long time is never misclassified as stale.
    """
    raw = ""
    if os.name != "nt":
        # Only inspect the owner PID on POSIX, where reading an open
        # sidecar is safe and unlink-of-open works. On Windows a reader
        # handle would collide with the holder's unlink, and PIDs of other
        # processes cannot be probed cheaply anyway -- the mtime/heartbeat
        # check below is the authoritative signal there.
        try:
            raw = lock_path.read_text(encoding="utf-8")
        except OSError:
            raw = ""
    if raw:
        try:
            payload = json.loads(raw)
            pid = payload.get("pid")
            if isinstance(pid, int):
                return bool(not _pid_alive(pid))
        except (json.JSONDecodeError, AttributeError):
            pass
    try:
        age = time.time() - lock_path.stat().st_mtime
    except OSError:
        return False
    return age > stale_after


def _write_owner_token(fd: int) -> None:
    """Write the ownership token (PID + host + timestamp) to *fd*."""
    payload = json.dumps(
        {
            "pid": os.getpid(),
            "host": socket.gethostname(),
            "t": time.time(),
        }
    )
    with contextlib.suppress(OSError):
        os.write(fd, payload.encode("utf-8"))


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

    While held, a daemon thread refreshes the sidecar's ownership token and
    mtime every ``stale_after / 3`` seconds so long-running critical
    sections are never mistaken for crashed locks.

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
    heartbeat_stop: Optional[threading.Event] = None
    heartbeat_thread: Optional[threading.Thread] = None

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
                    raise FileLockError(f"Failed to acquire lock: {exc}") from exc
                # Lock held by someone else.  Break an orphaned lock.
                if _is_stale(lock_path, stale_after):
                    logger.warning(
                        "Breaking stale lock %s (orphaned).",
                        lock_path,
                    )
                    with contextlib.suppress(OSError):
                        lock_path.unlink()
                    continue
                if time.monotonic() >= deadline:
                    raise FileLockError(
                        f"Could not acquire lock {lock_path} within {timeout}s."
                    ) from exc
                time.sleep(poll_interval)

        # We hold the lock.  Record ownership and start the heartbeat.
        _write_owner_token(fd)
        interval = max(stale_after / 3.0, 0.5)

        def _beat() -> None:
            while not heartbeat_stop.wait(interval):  # type: ignore[union-attr]
                _write_owner_token(fd)  # type: ignore[arg-type]

        heartbeat_stop = threading.Event()
        heartbeat_thread = threading.Thread(
            target=_beat,
            name=f"file-lock-heartbeat-{lock_path.name}",
            daemon=True,
        )
        heartbeat_thread.start()
        yield
    finally:
        if heartbeat_stop is not None:
            heartbeat_stop.set()
        if heartbeat_thread is not None:
            heartbeat_thread.join(timeout=1.0)
        if fd is not None:
            with contextlib.suppress(OSError):
                os.close(fd)
        if acquired:
            # Retry the unlink on Windows where another thread's transient
            # open handle (e.g. a failed O_EXCL attempt) can briefly block it.
            for _ in range(10):
                try:
                    lock_path.unlink()
                    break
                except FileNotFoundError:
                    break
                except OSError:
                    time.sleep(0.02)
            else:
                logger.warning("Failed to remove lock file %s", lock_path)
