"""Regression tests for dashboard KPI scorers (org health / scorecard)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from ai_company.dashboard.scorers import score_task_throughput


def _task(created_at: str, status: str = "completed") -> dict[str, str]:
    return {"created_at": created_at, "status": status}


def test_throughput_mixed_naive_and_aware_timestamps() -> None:
    """Known bug: mixed offset-naive/aware created_at crashed min() with
    TypeError and surfaced as the org-health task_throughput fail-open error
    in the dashboard logs."""
    now = datetime.now(timezone.utc)
    tasks = [
        _task((now - timedelta(days=5)).isoformat()),  # aware (+00:00)
        _task((now - timedelta(days=4)).replace(tzinfo=None).isoformat()),  # naive
        _task((now - timedelta(days=3)).isoformat()),
        _task("", "failed"),
        _task("not-a-date", "failed"),
    ]
    result = score_task_throughput(tasks, target_per_day=10.0)
    assert result is not None
    assert 0.0 <= result <= 100.0


def test_throughput_naive_only_timestamps() -> None:
    """Naive-only lists must also compute: `now (aware) - oldest` used to
    raise TypeError after min() succeeded."""
    now = datetime.now(timezone.utc)
    tasks = [_task((now - timedelta(days=2)).replace(tzinfo=None).isoformat())]
    result = score_task_throughput(tasks)
    assert result is not None


def test_throughput_all_aware_timestamps() -> None:
    now = datetime.now(timezone.utc)
    tasks = [
        _task((now - timedelta(days=1)).isoformat()),
        _task((now - timedelta(days=10)).isoformat()),
        _task((now - timedelta(days=10)).isoformat(), "failed"),
    ]
    result = score_task_throughput(tasks, target_per_day=10.0)
    assert result is not None
    assert 0.0 <= result <= 100.0


def test_throughput_without_usable_timestamps_returns_none() -> None:
    assert score_task_throughput([_task(""), _task("garbage")]) is None
    assert score_task_throughput([]) is None
