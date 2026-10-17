"""Hard deadlines and bulkhead isolation for the hardening layer.

Org-health scorers (and later daemon/scheduler calls) run through these
helpers so a slow or hung callee can never block the dashboard thread. Worker
threads are daemon threads and ``shutdown(wait=False)`` returns immediately —
a hung callee is abandoned, never awaited.
"""

from __future__ import annotations

import logging
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class Bulkhead:
    """Process-limited thread pool with hard per-call deadlines.

    Bounds how many calls run concurrently (``max_workers``) and how many may
    wait behind them (``queue_cap``). When the queue is full the oldest
    not-yet-started call is cancelled (drop-oldest) so memory stays bounded
    under load.

    Worker threads are daemon and ``shutdown(wait=False)`` never blocks the
    caller on a hung callee.
    """

    def __init__(self, max_workers: int, queue_cap: int = 20) -> None:
        self._executor = ThreadPoolExecutor(
            max_workers=max(1, int(max_workers)),
            thread_name_prefix="bulkhead",
        )
        self._queue_cap = max(1, int(queue_cap))
        self._lock = threading.Lock()
        self._pending: list[Future[Any]] = []
        self._is_shutdown = False

    def submit(self, fn: Callable[..., T], /, *args: Any, **kwargs: Any) -> Future[T]:
        """Submit *fn* to the pool, drop-oldest when the queue is full."""
        with self._lock:
            if self._is_shutdown:
                raise RuntimeError("bulkhead has been shut down")
            self._pending = [f for f in self._pending if not f.done()]
            while len(self._pending) >= self._queue_cap:
                if not self._drop_oldest_unstarted():
                    break
            future = self._executor.submit(fn, *args, **kwargs)
            self._pending.append(future)
        return future

    def call(self, fn: Callable[..., T], /, timeout_s: float, *args: Any, **kwargs: Any) -> T:
        """Submit *fn* and wait up to *timeout_s*; raises ``TimeoutError`` on exceed."""
        future = self.submit(fn, *args, **kwargs)
        return future.result(timeout=timeout_s)

    def _drop_oldest_unstarted(self) -> bool:
        """Cancel the oldest not-yet-started call; True if one was dropped.

        Running calls are skipped — only queued (unstarted) calls can be shed
        without losing in-flight work.
        """
        for idx, future in enumerate(self._pending):
            if future.done():
                continue
            if future.cancel():
                logger.warning("Bulkhead queue full — dropped oldest pending call")
                self._pending.pop(idx)
                return True
        return False

    def shutdown(self, wait: bool = False) -> None:
        """Release the pool; with ``wait=False`` a hung worker is never awaited."""
        with self._lock:
            self._is_shutdown = True
            self._executor.shutdown(wait=wait, cancel_futures=True)


def call_with_timeout(
    fn: Callable[..., T],
    /,
    timeout_s: float,
    *args: Any,
    **kwargs: Any,
) -> T:
    """Run *fn* in a daemon worker with a hard *timeout_s* deadline.

    Raises ``TimeoutError`` when *fn* does not finish in time; the stuck
    worker is abandoned rather than awaited so the caller is never blocked.
    """
    bulkhead = Bulkhead(max_workers=1)
    try:
        return bulkhead.call(fn, timeout_s, *args, **kwargs)
    finally:
        bulkhead.shutdown(wait=False)
