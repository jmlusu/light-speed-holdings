"""Circuit breaker pattern for LLM providers and component calls."""

from __future__ import annotations

import threading
import time
from enum import Enum

from ai_company.dashboard.monitoring import inc_metric


class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing if recovered


class CircuitBreaker:
    """Tracks failures and prevents calls when the circuit is open.

    Thread-safe: every state transition holds an internal lock, so one breaker
    can back concurrent component scorers or provider calls.

    Args:
        failure_threshold: Consecutive failures before opening the circuit.
        recovery_timeout: Seconds to wait before probing again (half-open).
        success_threshold: Consecutive successes in half-open to close it.
        metric_prefix: Optional prefix for trip/half-open counters. When set,
            metrics are emitted as ``<metric_prefix>_circuit_breaker_trips_total``
            and ``<metric_prefix>_circuit_breaker_half_open_total``; when unset
            the legacy unlabelled counters are used (backward-compatible).
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 60.0,
        success_threshold: int = 1,
        metric_prefix: str | None = None,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self._metric_prefix = metric_prefix

        self._lock = threading.RLock()
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = 0.0

    def _maybe_half_open(self) -> None:
        """Transition to HALF_OPEN once the recovery timeout has elapsed."""
        if (
            self._state == CircuitState.OPEN
            and time.time() - self._last_failure_time >= self.recovery_timeout
        ):
            self._state = CircuitState.HALF_OPEN
            self._success_count = 0
            self._inc("circuit_breaker_half_open_total")

    @property
    def state(self) -> CircuitState:
        with self._lock:
            self._maybe_half_open()
            return self._state

    @property
    def is_available(self) -> bool:
        with self._lock:
            self._maybe_half_open()
            return self._state in (CircuitState.CLOSED, CircuitState.HALF_OPEN)

    def record_success(self) -> None:
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.success_threshold:
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
            elif self._state == CircuitState.CLOSED:
                self._failure_count = 0

    def record_failure(self, error_category: str | None = None) -> None:
        """Record a failed call, opening the circuit after the threshold.

        Args:
            error_category: Optional category (a ``ProviderErrorCategory``
                value such as ``"auth"``). Authentication failures are not
                counted: they indicate a configuration problem that retries
                will not self-heal, so tripping the breaker on them would
                blacklist the provider without a recovery path.
        """
        if error_category == "auth":
            return
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if (
                self._state == CircuitState.HALF_OPEN
                or self._failure_count >= self.failure_threshold
            ):
                if self._state != CircuitState.OPEN:
                    self._inc("circuit_breaker_trips_total")
                self._state = CircuitState.OPEN

    def _inc(self, suffix: str) -> None:
        if self._metric_prefix:
            inc_metric(f"{self._metric_prefix}_{suffix}")
        else:
            inc_metric(suffix)
