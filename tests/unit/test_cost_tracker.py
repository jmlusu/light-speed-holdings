"""Unit tests for CostTracker budget persistence across restarts.

These tests verify that the CostTracker replays its JSONL cost log on
construction so that daily and per-task budget accumulators survive a
process restart (GAP-009 / S2-07).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from ai_company.llm.cost_tracker import CostTracker


def _make_tracker(tmp_path: Path, **kwargs: object) -> CostTracker:
    """Create a CostTracker writing into ``tmp_path/results``."""
    return CostTracker(
        results_dir=str(tmp_path / "results"),
        export_path=str(tmp_path / "orchestrator" / "cost_tracker.json"),
        **kwargs,
    )


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


class TestGetUsageSummary:
    """The filtered summary query (ticket #9 / T012) must honour all filters."""

    def _tracker_with_records(self, tmp_path: Path) -> CostTracker:
        tracker = _make_tracker(tmp_path)
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="agent_a",
            task_id="task-1",
            prompt_tokens=1_000,
            completion_tokens=500,
        )
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="agent_b",
            task_id="task-2",
            prompt_tokens=2_000,
            completion_tokens=800,
        )
        tracker.record_usage(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic",
            agent_name="agent_a",
            task_id="task-3",
            prompt_tokens=3_000,
            completion_tokens=1_000,
        )
        return tracker

    def test_unfiltered_returns_all(self, tmp_path: Path) -> None:
        tracker = self._tracker_with_records(tmp_path)
        summary = tracker.get_usage_summary()
        assert summary["call_count"] == 3
        assert summary["total_prompt_tokens"] == 6_000
        assert summary["total_completion_tokens"] == 2_300
        assert summary["total_tokens"] == 8_300
        assert len(summary["by_model"]) == 2
        assert len(summary["by_agent"]) == 2

    def test_filter_by_model(self, tmp_path: Path) -> None:
        tracker = self._tracker_with_records(tmp_path)
        summary = tracker.get_usage_summary(model="gpt-4o-mini")
        assert summary["call_count"] == 2
        assert set(summary["by_agent"]) == {"agent_a", "agent_b"}
        assert summary["by_agent"]["agent_a"]["prompt_tokens"] == 1_000

    def test_filter_by_agent(self, tmp_path: Path) -> None:
        tracker = self._tracker_with_records(tmp_path)
        summary = tracker.get_usage_summary(agent_name="agent_a")
        assert summary["call_count"] == 2
        assert summary["total_prompt_tokens"] == 4_000
        assert set(summary["by_model"]) == {"gpt-4o-mini", "claude-3-5-sonnet-20241022"}

    def test_filter_by_date_range(self, tmp_path: Path) -> None:
        tracker = self._tracker_with_records(tmp_path)
        summary = tracker.get_usage_summary(start_date="9999-01-01")
        assert summary["call_count"] == 0
        summary2 = tracker.get_usage_summary(end_date="1970-01-01")
        assert summary2["call_count"] == 0

    def test_combined_filters(self, tmp_path: Path) -> None:
        tracker = self._tracker_with_records(tmp_path)
        summary = tracker.get_usage_summary(model="gpt-4o-mini", agent_name="agent_b")
        assert summary["call_count"] == 1
        assert summary["total_prompt_tokens"] == 2_000
        assert list(summary["by_agent"]) == ["agent_b"]


class TestDailyBudgetExceeded:
    """Guardrail #15 — daily_budget_exceeded() drives executor auto-suspend."""

    def test_no_budget_is_never_exceeded(self, tmp_path: Path) -> None:
        tracker = _make_tracker(tmp_path)
        assert tracker.daily_budget_exceeded() is False

    def test_exceeded_when_today_spend_reaches_cap(self, tmp_path: Path) -> None:
        tracker = _make_tracker(tmp_path, daily_budget_usd=100.0)
        today = datetime.now(timezone.utc).date().isoformat()
        tracker._daily_cost[today] = 100.0
        assert tracker.daily_budget_exceeded() is True

    def test_not_exceeded_below_cap(self, tmp_path: Path) -> None:
        tracker = _make_tracker(tmp_path, daily_budget_usd=100.0)
        today = datetime.now(timezone.utc).date().isoformat()
        tracker._daily_cost[today] = 50.0
        assert tracker.daily_budget_exceeded() is False


class TestNegativeTokensClamped:
    """Negative token counts must be clamped to zero, not recorded as-is."""

    def test_record_usage_clamps_negative_tokens(self, tmp_path: Path) -> None:
        tracker = _make_tracker(tmp_path)
        record = tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="agent_a",
            task_id="task-neg",
            prompt_tokens=-100,
            completion_tokens=-50,
        )
        assert record.prompt_tokens == 0
        assert record.completion_tokens == 0
        assert record.cost_usd == 0.0
        # The accumulators must not be skewed by negative spend.
        assert tracker.get_usage_summary(agent_name="agent_a")["total_cost_usd"] == 0.0

    def test_calculate_cost_clamps_negative_tokens(self, tmp_path: Path) -> None:
        tracker = _make_tracker(tmp_path)
        assert tracker._calculate_cost("gpt-4o-mini", -100, -50) == 0.0

    def test_rebuild_clamps_negative_tokens(self, tmp_path: Path) -> None:
        results = tmp_path / "results"
        results.mkdir(parents=True, exist_ok=True)
        log_path = results / "cost_log.jsonl"
        bad = {
            "timestamp": "2026-07-20T12:00:00",
            "model": "gpt-4o-mini",
            "provider": "openai",
            "agent_name": "agent_a",
            "task_id": "task-neg",
            "prompt_tokens": -200,
            "completion_tokens": -100,
            "cost_usd": 0.0,
            "iteration": 1,
            "metadata": {},
        }
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(bad) + "\n")

        restarted = _make_tracker(tmp_path)
        assert len(restarted._records) == 1
        assert restarted._records[0].prompt_tokens == 0
        assert restarted._records[0].completion_tokens == 0


class TestRecordsBounded:
    """The in-memory record list is capped to prevent unbounded growth."""

    def test_record_usage_trims_to_cap(self, tmp_path: Path) -> None:
        from ai_company.llm.cost_tracker import _MAX_RECORDS, UsageRecord

        tracker = _make_tracker(tmp_path)
        stub = UsageRecord(
            timestamp="2026-07-20T12:00:00",
            model="gpt-4o-mini",
            provider="openai",
            agent_name="agent_a",
            task_id="stub",
            prompt_tokens=1,
            completion_tokens=1,
            cost_usd=0.0,
        )
        # Oversized working set (at the cap already); a new record must trim
        # the oldest entry so the list never exceeds the cap.
        tracker._records.extend([stub] * _MAX_RECORDS)
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="agent_a",
            task_id="task-cap",
            prompt_tokens=10,
            completion_tokens=5,
        )
        assert len(tracker._records) == _MAX_RECORDS
        # The newest record survives the trim.
        assert tracker._records[-1].task_id == "task-cap"

    def test_rebuild_trims_to_cap(self, tmp_path: Path) -> None:
        from ai_company.llm.cost_tracker import _MAX_RECORDS

        results = tmp_path / "results"
        results.mkdir(parents=True, exist_ok=True)
        log_path = results / "cost_log.jsonl"

        # Write one more line than the cap.
        with open(log_path, "w", encoding="utf-8") as f:
            for i in range(_MAX_RECORDS + 5):
                rec = {
                    "timestamp": f"2026-07-20T12:{i % 60:02d}:00",
                    "model": "gpt-4o-mini",
                    "provider": "openai",
                    "agent_name": "agent_a",
                    "task_id": f"task-{i}",
                    "prompt_tokens": 1,
                    "completion_tokens": 1,
                    "cost_usd": 0.0,
                    "iteration": 1,
                    "metadata": {},
                }
                f.write(json.dumps(rec) + "\n")

        restarted = _make_tracker(tmp_path)
        assert len(restarted._records) == _MAX_RECORDS
        # Oldest records dropped, newest kept.
        assert restarted._records[0].task_id == "task-5"
        assert restarted._records[-1].task_id == f"task-{_MAX_RECORDS + 4}"


class TestExportSummary:
    """The aggregated summary export to orchestrator/cost_tracker.json."""

    def test_export_summary_file_created(self, tmp_path: Path) -> None:
        _make_tracker(tmp_path)
        export_file = tmp_path / "orchestrator" / "cost_tracker.json"
        assert export_file.exists()
        data = json.loads(export_file.read_text())
        assert data["total_spent"] == 0.0
        assert data["llm_spend"] == 0.0
        assert data["call_count"] == 0

    def test_export_summary_after_record_usage(self, tmp_path: Path) -> None:
        tracker = _make_tracker(tmp_path, daily_budget_usd=10.0)
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="agent_a",
            task_id="task-1",
            prompt_tokens=1000,
            completion_tokens=500,
        )
        export_file = tmp_path / "orchestrator" / "cost_tracker.json"
        data = json.loads(export_file.read_text())
        assert data["total_spent"] > 0
        assert data["llm_spend"] == data["total_spent"]
        assert data["call_count"] == 1
        assert "agent_a" in data["by_agent"]
        assert "gpt-4o-mini" in data["by_model"]
        assert len(data["daily_trend"]) >= 1
        assert data["currency"] == "USD"

    def test_export_summary_rebuilt_on_restart(self, tmp_path: Path) -> None:
        tracker = _make_tracker(tmp_path)
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="openai",
            agent_name="agent_a",
            task_id="task-1",
            prompt_tokens=1000,
            completion_tokens=500,
        )
        first_export = json.loads((tmp_path / "orchestrator" / "cost_tracker.json").read_text())

        # New tracker pointing at same results dir replays the log and re-exports.
        CostTracker(
            results_dir=str(tmp_path / "results"),
            export_path=str(tmp_path / "orchestrator" / "cost_tracker.json"),
        )
        restarted_export = json.loads((tmp_path / "orchestrator" / "cost_tracker.json").read_text())
        assert restarted_export["call_count"] == first_export["call_count"]
        assert restarted_export["total_spent"] == pytest.approx(first_export["total_spent"])
