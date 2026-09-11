"""Unit tests for the LLM provider circuit breaker."""

from __future__ import annotations

import threading

import pytest

from ai_company.dashboard import monitoring
from ai_company.llm.circuit_breaker import CircuitBreaker, CircuitState


def test_auth_failures_do_not_count():
    """AUTH failures are configuration problems, not transient faults.

    They must not increment the failure count, otherwise a misconfigured
    provider would trip the breaker without a self-healing path.
    """
    breaker = CircuitBreaker(failure_threshold=2)
    breaker.record_failure("auth")
    breaker.record_failure("auth")
    breaker.record_failure("auth")
    assert breaker.state == CircuitState.CLOSED
    assert breaker.is_available


def test_rate_limit_failures_count_toward_threshold():
    breaker = CircuitBreaker(failure_threshold=2)
    breaker.record_failure("rate_limit")
    breaker.record_failure("rate_limit")
    assert breaker.state == CircuitState.OPEN
    assert not breaker.is_available


def test_failure_threshold_opens_circuit():
    breaker = CircuitBreaker(failure_threshold=3)
    breaker.record_failure()
    breaker.record_failure()
    assert breaker.is_available
    breaker.record_failure()
    assert breaker.state == CircuitState.OPEN
    assert not breaker.is_available


def test_success_records_reset_failure_count():
    breaker = CircuitBreaker(failure_threshold=3)
    breaker.record_failure()
    breaker.record_failure()
    breaker.record_success()
    # One more failure must not trip the breaker (count was reset).
    breaker.record_failure()
    assert breaker.is_available


def test_half_open_success_closes_circuit():
    breaker = CircuitBreaker(failure_threshold=2, success_threshold=1)
    breaker.record_failure()
    breaker.record_failure()
    assert breaker.state == CircuitState.OPEN

    # Force the recovery timeout so the breaker probes in half-open state.
    breaker._state = CircuitState.HALF_OPEN
    breaker.record_success()
    assert breaker.state == CircuitState.CLOSED
    assert breaker.is_available


def test_half_open_failure_reopens_circuit():
    breaker = CircuitBreaker(failure_threshold=2)
    breaker.record_failure()
    breaker.record_failure()
    breaker._state = CircuitState.HALF_OPEN
    breaker.record_failure("server")
    assert breaker.state == CircuitState.OPEN


# ── metric_prefix (wayfinder #170) ──────────────────────────────────


def test_no_prefix_keeps_legacy_metric_names(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(monitoring, "_metrics", {})
    breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0)
    breaker.record_failure()
    _ = breaker.is_available  # trips half-open immediately (recovery_timeout=0)
    assert monitoring._metrics == {
        "circuit_breaker_trips_total": 1,
        "circuit_breaker_half_open_total": 1,
    }


def test_metric_prefix_scopes_counters(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(monitoring, "_metrics", {})
    breaker = CircuitBreaker(
        failure_threshold=1, recovery_timeout=0, metric_prefix="ai_company_org_health"
    )
    breaker.record_failure()
    _ = breaker.is_available  # half-open transition
    assert monitoring._metrics.get("ai_company_org_health_circuit_breaker_trips_total") == 1
    assert monitoring._metrics.get("ai_company_org_health_circuit_breaker_half_open_total") == 1
    # The unlabelled legacy counters stay untouched when a prefix is given.
    assert monitoring._metrics.get("circuit_breaker_trips_total") is None


# ── Thread safety (wayfinder #170) ──────────────────────────────────


def test_concurrent_calls_are_thread_safe() -> None:
    """Concurrent failures never lose updates and never corrupt state.

    8 threads x 200 iterations each record a failure and probe availability.
    Open breakers keep counting (there are no success resets here), so the
    final counter is exact: any lost update would make the assertion fail.
    """
    breaker = CircuitBreaker(failure_threshold=50, recovery_timeout=60.0)
    errors: list[Exception] = []

    def worker() -> None:
        try:
            for _ in range(200):
                breaker.record_failure("server")
                _ = breaker.is_available
        except Exception as exc:  # noqa: BLE001 - test collects instead of failing
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []
    assert breaker._failure_count == 8 * 200
    assert breaker.state is CircuitState.OPEN
    assert not breaker.is_available
