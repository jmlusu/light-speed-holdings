"""Unit tests for CostTracker budget persistence across restarts.

These tests verify that the CostTracker replays its JSONL cost log on
construction so that daily and per-task budget accumulators survive a
process restart (GAP-009 / S2-07).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.llm.cost_tracker import CostTracker


def _make_tracker(tmp_path: Path, **kwargs: object) -> CostTracker:
    """Create a CostTracker writing into ``tmp_path/results``."""
    return CostTracker(results_dir=str(tmp_path / "results"), **kwargs)


class TestRestartPersistence:
    """Budget state must survive a fresh CostTracker instance."""

    def test_daily_cost_survives_restart(self, tmp_path: Path) -> None:
        """_daily_cost totals are rebuilt from the JSONL log on __init__."""
        tracker = _make_tracker(tmp_path)

        # Record usage across two distinct tasks on the same day.
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="agent_a",
            task_id="task-1",
            prompt_tokens=10_000,
            completion_tokens=5_000,
        )
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="agent_b",
            task_id="task-2",
            prompt_tokens=20_000,
            completion_tokens=8_000,
        )

        # Snapshot the day key actually used by the tracker.
        day_key = next(iter(tracker._daily_cost))
        first_total = tracker._daily_cost[day_key]

        # Simulate a restart: brand-new tracker pointed at the same dir.
        restarted = _make_tracker(tmp_path)

        assert restarted._daily_cost[day_key] == pytest.approx(first_total)
        # Both tasks' spend should be present in the task accumulator.
        assert restarted._task_costs["task-1"] > 0
        assert restarted._task_costs["task-2"] > 0
        # Records were replayed too.
        assert len(restarted._records) == 2

    def test_task_cost_survives_restart(self, tmp_path: Path) -> None:
        """Per-task accumulator is rebuilt and budget checks reflect it."""
        daily_budget = 100.0
        task_budget = 0.10
        tracker = _make_tracker(
            tmp_path, daily_budget_usd=daily_budget, task_budget_usd=task_budget
        )

        tracker.record_usage(
            model="gpt-4o",
            provider="openai",
            agent_name="agent_a",
            task_id="expensive-task",
            prompt_tokens=100_000,
            completion_tokens=50_000,
        )

        task_total = tracker._task_costs["expensive-task"]

        # Restart and confirm the per-task budget state is preserved.
        restarted = _make_tracker(
            tmp_path, daily_budget_usd=daily_budget, task_budget_usd=task_budget
        )

        allowed, _reason = restarted.check_budget("expensive-task", proposed_cost=0.0)
        assert restarted._task_costs["expensive-task"] == pytest.approx(task_total)
        # Already over the per-task budget, so a further call must be blocked.
        assert allowed is False

    def test_restart_with_no_log_is_clean(self, tmp_path: Path) -> None:
        """A fresh results dir produces empty accumulators."""
        tracker = _make_tracker(tmp_path)
        assert tracker._daily_cost == {}
        assert tracker._task_costs == {}
        assert tracker._records == []

    def test_restart_skips_corrupt_lines(self, tmp_path: Path) -> None:
        """Malformed JSONL lines are ignored but valid lines still rebuild."""
        results = tmp_path / "results"
        results.mkdir(parents=True, exist_ok=True)
        log_path = results / "cost_log.jsonl"

        # Write one valid record line and two corrupt lines.
        valid = {
            "timestamp": "2026-07-20T12:00:00",
            "model": "gpt-4o-mini",
            "provider": "openai",
            "agent_name": "agent_a",
            "task_id": "task-x",
            "prompt_tokens": 10_000,
            "completion_tokens": 5_000,
            "cost_usd": 0.012,
            "iteration": 1,
            "metadata": {},
        }
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(valid) + "\n")
            f.write("this is not valid json\n")
            f.write("\n")  # blank line
            f.write("{not-json}\n")

        restarted = _make_tracker(tmp_path)
        assert len(restarted._records) == 1
        assert restarted._daily_cost["2026-07-20"] == pytest.approx(0.012)
        assert restarted._task_costs["task-x"] == pytest.approx(0.012)
