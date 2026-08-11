"""Unit tests for the LLM provider circuit breaker."""

from __future__ import annotations

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
