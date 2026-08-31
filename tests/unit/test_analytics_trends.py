"""Contract tests for the pure trend / moving-average / anomaly helpers.

Covers :func:`ai_company.dashboard.analytics.compute_period_comparison`,
:func:`ai_company.dashboard.analytics.compute_moving_average`, and
:func:`ai_company.dashboard.analytics.detect_anomaly`.
"""

from __future__ import annotations

from ai_company.dashboard.analytics import (
    compute_moving_average,
    compute_period_comparison,
    detect_anomaly,
)


class TestComputePeriodComparison:
    def test_positive_change(self) -> None:
        assert compute_period_comparison(110.0, 100.0) == 10.0

    def test_negative_change(self) -> None:
        assert compute_period_comparison(90.0, 100.0) == -10.0

    def test_no_change(self) -> None:
        assert compute_period_comparison(100.0, 100.0) == 0.0

    def test_previous_zero_returns_none(self) -> None:
        assert compute_period_comparison(50.0, 0.0) is None

    def test_current_none_returns_none(self) -> None:
        assert compute_period_comparison(None, 100.0) is None

    def test_previous_none_returns_none(self) -> None:
        assert compute_period_comparison(100.0, None) is None


class TestComputeMovingAverage:
    def test_short_series_masks_head(self) -> None:
        assert compute_moving_average([1.0, 2.0, 3.0], window=3) == [None, None, 2.0]

    def test_window_one_is_identity(self) -> None:
        assert compute_moving_average([1.0, 2.0, 3.0], window=1) == [1.0, 2.0, 3.0]

    def test_window_greater_than_series_fully_masked(self) -> None:
        assert compute_moving_average([1.0, 2.0], window=5) == [None, None]

    def test_empty_series(self) -> None:
        assert compute_moving_average([], window=3) == []

    def test_invalid_window_returns_masked(self) -> None:
        assert compute_moving_average([1.0, 2.0], window=0) == [None, None]


class TestDetectAnomaly:
    def test_flags_isolated_spike(self) -> None:
        # A single 100 among ~10s exceeds 1.5 std from the global mean.
        flagged = detect_anomaly([10.0, 10.0, 10.0, 100.0, 10.0], std_devs=1.5)
        assert 3 in flagged

    def test_no_anomaly_in_stable_series(self) -> None:
        assert detect_anomaly([10.0, 10.5, 9.8, 10.2, 10.1], std_devs=2.0) == []

    def test_short_series_never_flags(self) -> None:
        # Fewer than 2 points can never form a window.
        assert detect_anomaly([1.0], std_devs=2.0) == []

    def test_empty_series(self) -> None:
        assert detect_anomaly([], std_devs=2.0) == []

    def test_flat_series_no_flag(self) -> None:
        # std==0 guard: zero variance must not divide by zero.
        assert detect_anomaly([5.0, 5.0, 5.0, 5.0], std_devs=2.0) == []
