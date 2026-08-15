"""Circuit breaker pattern for LLM providers."""

from __future__ import annotations

import time
from enum import Enum

from ai_company.dashboard.monitoring import inc_metric


class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing if recovered


class CircuitBreaker:
    """Tracks provider failures and prevents calls when circuit is open.

    Args:
        failure_threshold: Number of consecutive failures before opening circuit.
        recovery_timeout: Seconds to wait before trying again (half-open).
        success_threshold: Consecutive successes in half-open to close circuit.
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 60.0,
        success_threshold: int = 1,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = 0.0

    @property
    def state(self) -> CircuitState:
        if (
            self._state == CircuitState.OPEN
            and time.time() - self._last_failure_time >= self.recovery_timeout
        ):
            self._state = CircuitState.HALF_OPEN
            self._success_count = 0
            inc_metric("circuit_breaker_half_open_total")
        return self._state

    @property
    def is_available(self) -> bool:
        return self.state in (CircuitState.CLOSED, CircuitState.HALF_OPEN)

    def record_success(self) -> None:
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
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._state == CircuitState.HALF_OPEN or self._failure_count >= self.failure_threshold:
            if self._state != CircuitState.OPEN:
                inc_metric("circuit_breaker_trips_total")
            self._state = CircuitState.OPEN
