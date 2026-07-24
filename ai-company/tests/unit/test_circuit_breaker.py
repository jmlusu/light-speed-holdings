"""Tests for PRE-09 — circuit breaker pattern for LLM providers.

Covers:
  - Initial state and transitions (CLOSED → OPEN → HALF_OPEN → CLOSED)
  - Threshold and timing logic
  - Availability checks
  - Reset behavior
"""

from __future__ import annotations

import time


from ai_company.llm.circuit_breaker import CircuitBreaker, CircuitState


# ── Initial State ───────────────────────────────────────────────────


class TestStartsClosed:
    def test_default_state_is_closed(self) -> None:
        cb = CircuitBreaker()
        assert cb.state == CircuitState.CLOSED
        assert cb.is_closed is True
        assert cb.is_available is True

    def test_custom_threshold(self) -> None:
        cb = CircuitBreaker(failure_threshold=5)
        assert cb._failure_count == 0
        assert cb.failure_threshold == 5
        assert cb.state == CircuitState.CLOSED

    def test_custom_recovery_timeout(self) -> None:
        cb = CircuitBreaker(recovery_timeout=30.0)
        assert cb.recovery_timeout == 30.0


# ── Opens After Threshold ──────────────────────────────────────────


class TestOpensAfterThresholdFailures:
    def test_stays_closed_below_threshold(self) -> None:
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        assert cb.state == CircuitState.CLOSED
        cb.record_failure()
        assert cb.state == CircuitState.CLOSED

    def test_opens_at_threshold(self) -> None:
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN
        assert cb.is_closed is False
        assert cb.is_available is False

    def test_opens_above_threshold(self) -> None:
        cb = CircuitBreaker(failure_threshold=2)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

    def test_single_failure_threshold(self) -> None:
        cb = CircuitBreaker(failure_threshold=1)
        cb.record_failure()
        assert cb.state == CircuitState.OPEN


# ── Half Open After Recovery Timeout ───────────────────────────────


class TestHalfOpenAfterRecoveryTimeout:
    def test_stays_open_before_timeout(self) -> None:
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=60.0)
        cb.record_failure()
        assert cb.state == CircuitState.OPEN
        # Immediately check — should still be OPEN
        assert cb.state == CircuitState.OPEN

    def test_transitions_to_half_open(self) -> None:
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.1)
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

        # Wait for recovery timeout
        time.sleep(0.15)

        # State should transition to HALF_OPEN
        assert cb.state == CircuitState.HALF_OPEN
        assert cb.is_available is True
        assert cb.is_closed is False

    def test_half_open_resets_success_count(self) -> None:
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)
        cb.record_failure()
        time.sleep(0.1)
        state = cb.state  # triggers transition to HALF_OPEN
        assert state == CircuitState.HALF_OPEN
        assert cb._success_count == 0


# ── Closes on Success in Half Open ─────────────────────────────────


class TestClosesOnSuccessInHalfOpen:
    def test_single_success_closes(self) -> None:
        cb = CircuitBreaker(
            failure_threshold=1,
            recovery_timeout=0.05,
            success_threshold=1,
        )
        cb.record_failure()
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_success()
        assert cb.state == CircuitState.CLOSED
        assert cb.is_closed is True
        assert cb._failure_count == 0

    def test_multiple_successes_needed(self) -> None:
        cb = CircuitBreaker(
            failure_threshold=1,
            recovery_timeout=0.05,
            success_threshold=3,
        )
        cb.record_failure()
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_success()
        assert cb.state == CircuitState.HALF_OPEN
        cb.record_success()
        assert cb.state == CircuitState.HALF_OPEN
        cb.record_success()
        assert cb.state == CircuitState.CLOSED


# ── Reopens on Failure in Half Open ────────────────────────────────


class TestReopensOnFailureInHalfOpen:
    def test_failure_in_half_open_reopens(self) -> None:
        cb = CircuitBreaker(
            failure_threshold=2,
            recovery_timeout=0.05,
            success_threshold=2,
        )
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN

        # One success, then a failure
        cb.record_success()
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_failure()
        assert cb.state == CircuitState.OPEN
        assert cb.is_available is False

    def test_failure_in_half_open_resets_success_count(self) -> None:
        cb = CircuitBreaker(
            failure_threshold=1,
            recovery_timeout=0.05,
            success_threshold=3,
        )
        cb.record_failure()
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_success()
        cb.record_success()
        cb.record_failure()  # Reopens

        # After reopening and waiting again, should start fresh
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN
        assert cb._success_count == 0


# ── Success Resets Failure Count ───────────────────────────────────


class TestSuccessResetsFailureCount:
    def test_success_in_closed_resets_count(self) -> None:
        cb = CircuitBreaker(failure_threshold=5)
        cb.record_failure()
        cb.record_failure()
        assert cb._failure_count == 2

        cb.record_success()
        assert cb._failure_count == 0

    def test_can_survive_more_failures_after_reset(self) -> None:
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        cb.record_success()
        # Failure count is reset, so these two shouldn't open the circuit
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.CLOSED

    def test_mixed_success_failure_pattern(self) -> None:
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_success()
        cb.record_failure()
        cb.record_success()
        cb.record_failure()
        # Each failure was reset by the next success; never hit 3 consecutive
        assert cb.state == CircuitState.CLOSED


# ── Reset Returns to Closed ────────────────────────────────────────


class TestResetReturnsToClosed:
    def test_reset_from_open(self) -> None:
        cb = CircuitBreaker(failure_threshold=1)
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

        cb.reset()
        assert cb.state == CircuitState.CLOSED
        assert cb._failure_count == 0
        assert cb._success_count == 0

    def test_reset_from_half_open(self) -> None:
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)
        cb.record_failure()
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN

        cb.reset()
        assert cb.state == CircuitState.CLOSED
        assert cb._failure_count == 0
        assert cb._success_count == 0

    def test_reset_allows_failures_again(self) -> None:
        cb = CircuitBreaker(failure_threshold=2)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

        cb.reset()
        # Should need 2 failures again to open
        cb.record_failure()
        assert cb.state == CircuitState.CLOSED
        cb.record_failure()
        assert cb.state == CircuitState.OPEN


# ── Is Available ───────────────────────────────────────────────────


class TestIsAvailableInClosedAndHalfOpen:
    def test_available_in_closed(self) -> None:
        cb = CircuitBreaker()
        assert cb.is_available is True

    def test_not_available_in_open(self) -> None:
        cb = CircuitBreaker(failure_threshold=1)
        cb.record_failure()
        assert cb.is_available is False

    def test_available_in_half_open(self) -> None:
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)
        cb.record_failure()
        time.sleep(0.1)
        assert cb.state == CircuitState.HALF_OPEN
        assert cb.is_available is True

    def test_unavailable_transitions_through_states(self) -> None:
        cb = CircuitBreaker(
            failure_threshold=2,
            recovery_timeout=0.05,
            success_threshold=1,
        )
        # CLOSED → available
        assert cb.is_available is True

        cb.record_failure()
        cb.record_failure()
        # OPEN → unavailable
        assert cb.is_available is False

        time.sleep(0.1)
        # HALF_OPEN → available
        assert cb.is_available is True

        cb.record_success()
        # CLOSED → available
        assert cb.is_available is True


# ── Edge Cases ─────────────────────────────────────────────────────


class TestEdgeCases:
    def test_success_in_open_state_ignored(self) -> None:
        """Success recorded while OPEN doesn't change state (only HALF_OPEN matters)."""
        cb = CircuitBreaker(failure_threshold=2)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

        # This shouldn't happen in normal usage, but verify it doesn't crash
        cb.record_success()
        assert cb.state == CircuitState.OPEN

    def test_is_closed_property_uses_state(self) -> None:
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)
        assert cb.is_closed is True

        cb.record_failure()
        assert cb.is_closed is False

        time.sleep(0.1)
        assert cb.is_closed is False  # HALF_OPEN is not closed

        cb.record_success()
        assert cb.is_closed is True  # Back to CLOSED

    def test_large_recovery_timeout(self) -> None:
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=999999.0)
        cb.record_failure()
        assert cb.state == CircuitState.OPEN
        # Should NOT transition even after a small sleep
        time.sleep(0.01)
        assert cb.state == CircuitState.OPEN
