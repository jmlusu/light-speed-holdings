"""Per-component circuit breaker facade over ``llm.CircuitBreaker``."""

from __future__ import annotations

import logging
from typing import Any, Callable, TypeVar

from ai_company.llm.circuit_breaker import CircuitBreaker, CircuitState
from ai_company.reliability.timeout import call_with_timeout

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ComponentBreaker:
    """A named breaker binding :class:`CircuitBreaker` to one component.

    Thin facade so the hardening layer owns the wiring: availability checks,
    success/failure recording, and timeout orchestration all live here instead
    of in each caller. Behaviour follows the catalog §7 invariants: every
    timeout counts as a breaker failure; real exceptions trip the breaker and
    degrade (never silently swallow).
    """

    def __init__(
        self,
        name: str,
        *,
        failure_threshold: int = 3,
        recovery_timeout_s: float = 60.0,
        success_threshold: int = 1,
        metric_prefix: str | None = None,
    ) -> None:
        self.name = name
        self._breaker = CircuitBreaker(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout_s,
            success_threshold=success_threshold,
            metric_prefix=metric_prefix,
        )

    @property
    def state(self) -> CircuitState:
        return self._breaker.state

    @property
    def is_available(self) -> bool:
        return self._breaker.is_available

    def record_success(self) -> None:
        self._breaker.record_success()

    def record_failure(self) -> None:
        self._breaker.record_failure()

    def call(
        self,
        fn: Callable[..., T],
        /,
        timeout_s: float,
        *args: Any,
        default: T | None = None,
        **kwargs: Any,
    ) -> T | None:
        """Run *fn* with a *timeout_s* deadline, fail-open to *default* on failure.

        A timeout or exception is recorded as a breaker failure (eventually
        opening the circuit) and *default* is returned — the breaker itself is
        the escalation path, so nothing is swallowed silently.
        """
        if not self.is_available:
            logger.warning("Component breaker %s is open — fail-open to default", self.name)
            return default
        try:
            result = call_with_timeout(fn, timeout_s, *args, **kwargs)
        except TimeoutError:
            self.record_failure()
            logger.warning(
                "Component %s timed out after %.1fs — fail-open to default",
                self.name,
                timeout_s,
            )
            return default
        except Exception:  # noqa: BLE001 - breaker records and degrades
            self.record_failure()
            logger.exception("Component %s failed — fail-open to default", self.name)
            return default
        self.record_success()
        return result


__all__ = ["ComponentBreaker"]
