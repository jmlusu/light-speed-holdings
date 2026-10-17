"""Token-bucket rate limiter for LLM providers.

Guards ``LLMClient`` calls so bursts of agent tasks don't hammer a provider
faster than it allows (429 / RATE_LIMIT). The bucket is thread-safe: the
executor loop and agent threads share one bucket per provider, so concurrent
tasks are paced as a group rather than each caller self-limiting in isolation.
"""

from __future__ import annotations

import threading
import time


class TokenBucket:
    """Fixed-rate token bucket with burst capacity.

    A bucket holds up to ``capacity`` tokens. Each ``acquire`` consumes one
    token; tokens refill at ``rate`` tokens/second, capped at ``capacity``.
    When empty, ``acquire`` waits up to ``timeout`` seconds for a refill.

    Args:
        rate: Tokens refilled per second (requests/second allowance).
        capacity: Maximum burst of tokens the bucket can hold.
    """

    def __init__(self, rate: float, capacity: float) -> None:
        if rate < 0 or capacity < 0:
            raise ValueError("rate and capacity must be non-negative")
        self.rate = float(rate)
        self.capacity = float(capacity)
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
        self._last_refill = now

    def try_acquire(self) -> bool:
        """Consume one token without blocking. Returns True on success."""
        with self._lock:
            self._refill()
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True
            return False

    def acquire(self, timeout: float = 0.0) -> bool:
        """Consume one token, waiting up to ``timeout`` seconds if empty.

        Returns True when a token was granted, False on timeout. ``timeout``
        of 0 performs a non-blocking ``try_acquire``.
        """
        deadline = time.monotonic() + timeout
        while True:
            if self.try_acquire():
                return True
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return False
            time.sleep(min(remaining, 0.05))
