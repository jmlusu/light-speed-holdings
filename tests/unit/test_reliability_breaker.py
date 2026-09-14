"""Unit tests for the per-component breaker facade."""

from __future__ import annotations

import time

from ai_company.llm.circuit_breaker import CircuitState
from ai_company.reliability.breaker import ComponentBreaker


def test_call_success_records_and_returns() -> None:
    breaker = ComponentBreaker("task_success_rate", failure_threshold=3)
    assert breaker.call(lambda: 90.0, timeout_s=1.0) == 90.0
    assert breaker.is_available


def test_call_timeout_counts_as_failure_and_fail_opens() -> None:
    def hang() -> float:
        time.sleep(30.0)
        return 1.0

    breaker = ComponentBreaker("cost_efficiency", failure_threshold=1, recovery_timeout_s=60.0)
    assert breaker.call(hang, timeout_s=0.05, default=None) is None
    assert not breaker.is_available


def test_open_breaker_fail_opens_without_calling() -> None:
    calls: list[int] = []
    breaker = ComponentBreaker("a", failure_threshold=1, recovery_timeout_s=60.0)
    breaker.record_failure()
    assert not breaker.is_available

    def probe() -> int:
        calls.append(1)
        return 7

    assert breaker.call(probe, timeout_s=1.0, default=13) == 13
    assert calls == []


def test_call_exception_trips_breaker_and_fail_opens() -> None:
    def boom() -> float:
        raise RuntimeError("boom")

    breaker = ComponentBreaker("b", failure_threshold=1, recovery_timeout_s=60.0)
    assert breaker.call(boom, timeout_s=1.0, default=None) is None
    assert not breaker.is_available


def test_recovery_probes_after_timeout() -> None:
    breaker = ComponentBreaker(
        "c", failure_threshold=1, recovery_timeout_s=0.0, success_threshold=1
    )
    breaker.record_failure()
    # Zero recovery timeout: the first availability probe moves to half-open…
    assert breaker.is_available
    assert breaker.state is CircuitState.HALF_OPEN
    # …the half-open probe runs; success closes the circuit.
    assert breaker.call(lambda: 5, timeout_s=1.0, default=None) == 5
    assert breaker.state is CircuitState.CLOSED
    assert breaker.is_available
