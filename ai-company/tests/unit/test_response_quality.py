"""Tests for LLM response quality tracking (PRE-19 part 2)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.llm.response_quality import (
    ResponseQualityMetric,
    ResponseQualityTracker,
    get_response_quality_tracker,
    reset_response_quality_tracker,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_metric(
    *,
    agent_id: str = "test-agent",
    model: str = "test-model",
    validation_passed: bool = True,
    validation_reason: str = "",
    response_length: int = 100,
    plan_steps: int = 0,
    has_tool_calls: bool = False,
    suspicious_content_detected: bool = False,
    parse_success: bool = True,
) -> ResponseQualityMetric:
    """Create a ResponseQualityMetric with sensible defaults."""
    return ResponseQualityMetric(
        agent_id=agent_id,
        model=model,
        validation_passed=validation_passed,
        validation_reason=validation_reason,
        response_length=response_length,
        plan_steps=plan_steps,
        has_tool_calls=has_tool_calls,
        suspicious_content_detected=suspicious_content_detected,
        parse_success=parse_success,
    )


# ---------------------------------------------------------------------------
# Test: metric recording
# ---------------------------------------------------------------------------


class TestMetricRecording:
    """Metrics should be recorded and retrievable."""

    def test_record_single_metric(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        metric = _make_metric()
        tracker.record(metric)
        assert len(tracker._metrics) == 1
        assert tracker._metrics[0].agent_id == "test-agent"

    def test_record_multiple_metrics(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for i in range(5):
            tracker.record(_make_metric(response_length=i * 100))
        assert len(tracker._metrics) == 5

    def test_record_writes_jsonl(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        tracker.record(_make_metric(agent_id="jsonl-test"))
        log_file = tmp_path / "quality.jsonl"
        assert log_file.exists()
        lines = log_file.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["agent_id"] == "jsonl-test"
        assert data["validation_passed"] is True

    def test_record_appends_to_jsonl(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        tracker.record(_make_metric(agent_id="first"))
        tracker.record(_make_metric(agent_id="second"))
        lines = (tmp_path / "quality.jsonl").read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 2

    def test_jsonl_contains_all_fields(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        tracker.record(_make_metric(
            suspicious_content_detected=True,
            validation_reason="Suspicious content",
            has_tool_calls=True,
            plan_steps=3,
        ))
        data = json.loads((tmp_path / "quality.jsonl").read_text(encoding="utf-8").strip())
        assert data["suspicious_content_detected"] is True
        assert data["validation_reason"] == "Suspicious content"
        assert data["has_tool_calls"] is True
        assert data["plan_steps"] == 3

    def test_jsonl_write_failure_does_not_crash(self, tmp_path: Path) -> None:
        """Write errors are logged, not raised."""
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        # Corrupt the log file path to force a write error
        tracker._log_file = tmp_path / "nonexistent" / "deep" / "quality.jsonl"
        # This should not raise
        tracker.record(_make_metric())
        # Metric still stored in memory
        assert len(tracker._metrics) == 1


# ---------------------------------------------------------------------------
# Test: window pruning
# ---------------------------------------------------------------------------


class TestWindowPruning:
    """Old metrics should be pruned when the window overflows."""

    def test_pruning_after_double_window_size(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        tracker._window_size = 10
        # Pruning triggers when len > window_size * 2 (i.e., > 20).
        # At record 21, prune to last 10. Records 22-25 add 4 more → 14.
        for i in range(25):
            tracker.record(_make_metric(response_length=i))
        assert len(tracker._metrics) == 14

    def test_pruning_keeps_most_recent(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        tracker._window_size = 5
        # Pruning triggers when len > 10. At record 11, prune to last 5.
        # Records 12-15 add 4 more → 9.
        for i in range(15):
            tracker.record(_make_metric(response_length=i))
        lengths = [m.response_length for m in tracker._metrics]
        assert lengths == [6, 7, 8, 9, 10, 11, 12, 13, 14]

    def test_pruning_never_below_window_size(self, tmp_path: Path) -> None:
        """After pruning, metrics should be at least window_size."""
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        tracker._window_size = 5
        # Exactly at threshold (11 = 2*5 + 1)
        for i in range(11):
            tracker.record(_make_metric(response_length=i))
        assert len(tracker._metrics) == 5


# ---------------------------------------------------------------------------
# Test: rate calculations
# ---------------------------------------------------------------------------


class TestRateCalculations:
    """Rate methods should return correct values."""

    def test_validation_rate_all_pass(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for _ in range(10):
            tracker.record(_make_metric(validation_passed=True))
        assert tracker.get_validation_rate() == 1.0

    def test_validation_rate_all_fail(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for _ in range(10):
            tracker.record(_make_metric(validation_passed=False))
        assert tracker.get_validation_rate() == 0.0

    def test_validation_rate_mixed(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for _ in range(7):
            tracker.record(_make_metric(validation_passed=True))
        for _ in range(3):
            tracker.record(_make_metric(validation_passed=False))
        assert tracker.get_validation_rate() == pytest.approx(0.7)

    def test_suspicious_rate_none(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for _ in range(10):
            tracker.record(_make_metric(suspicious_content_detected=False))
        assert tracker.get_suspicious_rate() == 0.0

    def test_suspicious_rate_some(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for _ in range(20):
            tracker.record(_make_metric(suspicious_content_detected=False))
        tracker.record(_make_metric(suspicious_content_detected=True))
        assert tracker.get_suspicious_rate() == pytest.approx(1 / 21)

    def test_parse_success_rate(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for _ in range(9):
            tracker.record(_make_metric(parse_success=True))
        tracker.record(_make_metric(parse_success=False))
        assert tracker.get_parse_success_rate() == pytest.approx(0.9)

    def test_avg_response_length(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        tracker.record(_make_metric(response_length=100))
        tracker.record(_make_metric(response_length=200))
        tracker.record(_make_metric(response_length=300))
        assert tracker.get_avg_response_length() == pytest.approx(200.0)


# ---------------------------------------------------------------------------
# Test: agent filtering
# ---------------------------------------------------------------------------


class TestAgentFiltering:
    """Rate calculations should filter by agent_id when specified."""

    def test_validation_rate_by_agent(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        # Agent A: all pass
        for _ in range(5):
            tracker.record(_make_metric(agent_id="agent-a", validation_passed=True))
        # Agent B: all fail
        for _ in range(5):
            tracker.record(_make_metric(agent_id="agent-b", validation_passed=False))

        assert tracker.get_validation_rate("agent-a") == 1.0
        assert tracker.get_validation_rate("agent-b") == 0.0

    def test_summary_by_agent(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        tracker.record(_make_metric(agent_id="alpha", model="gpt-4"))
        tracker.record(_make_metric(agent_id="alpha", model="gpt-4"))
        tracker.record(_make_metric(agent_id="beta", model="claude-3"))

        summary = tracker.get_summary("alpha")
        assert summary["total"] == 2
        assert "gpt-4" in summary["models_used"]

    def test_alerts_by_agent(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        # Agent A: all good
        for _ in range(10):
            tracker.record(_make_metric(agent_id="agent-a", validation_passed=True))
        # Agent B: degraded
        for _ in range(8):
            tracker.record(_make_metric(agent_id="agent-b", validation_passed=False))

        alerts_a = tracker.check_alerts("agent-a")
        alerts_b = tracker.check_alerts("agent-b")
        assert len(alerts_a) == 0
        assert any(a["type"] == "validation_degradation" for a in alerts_b)

    def test_empty_tracker_returns_defaults(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        assert tracker.get_validation_rate() == 1.0
        assert tracker.get_suspicious_rate() == 0.0
        assert tracker.get_parse_success_rate() == 1.0
        assert tracker.get_avg_response_length() == 0.0
        assert tracker.get_summary() == {"total": 0}


# ---------------------------------------------------------------------------
# Test: summary generation
# ---------------------------------------------------------------------------


class TestSummaryGeneration:
    """Summary should include all expected fields."""

    def test_summary_fields(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        tracker.record(_make_metric(model="gpt-4", response_length=250))
        tracker.record(_make_metric(model="claude-3", response_length=350))

        summary = tracker.get_summary()
        assert "total" in summary
        assert "validation_rate" in summary
        assert "suspicious_rate" in summary
        assert "parse_success_rate" in summary
        assert "avg_response_length" in summary
        assert "models_used" in summary
        assert summary["total"] == 2
        assert summary["avg_response_length"] == pytest.approx(300.0)
        assert set(summary["models_used"]) == {"gpt-4", "claude-3"}

    def test_summary_empty(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        summary = tracker.get_summary()
        assert summary == {"total": 0}


# ---------------------------------------------------------------------------
# Test: alert generation
# ---------------------------------------------------------------------------


class TestAlertGeneration:
    """Alerts should fire when quality drops below thresholds."""

    def test_no_alerts_on_good_quality(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for _ in range(20):
            tracker.record(_make_metric(
                validation_passed=True,
                suspicious_content_detected=False,
                parse_success=True,
            ))
        assert tracker.check_alerts() == []

    def test_validation_degradation_warning(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        # 80% pass / 20% fail → rate 0.8 → warning (0.7 < 0.8 < 0.9)
        for _ in range(8):
            tracker.record(_make_metric(validation_passed=True))
        for _ in range(2):
            tracker.record(_make_metric(validation_passed=False))

        alerts = tracker.check_alerts()
        assert len(alerts) == 1
        assert alerts[0]["type"] == "validation_degradation"
        assert alerts[0]["severity"] == "warning"

    def test_validation_degradation_critical(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        # 40% failure rate → critical (<= 0.7)
        for _ in range(6):
            tracker.record(_make_metric(validation_passed=True))
        for _ in range(4):
            tracker.record(_make_metric(validation_passed=False))

        alerts = tracker.check_alerts()
        assert len(alerts) == 1
        assert alerts[0]["type"] == "validation_degradation"
        assert alerts[0]["severity"] == "critical"

    def test_suspicious_content_spike(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for _ in range(18):
            tracker.record(_make_metric(suspicious_content_detected=False))
        for _ in range(2):
            tracker.record(_make_metric(suspicious_content_detected=True))

        alerts = tracker.check_alerts()
        assert len(alerts) == 1
        assert alerts[0]["type"] == "suspicious_content_spike"
        assert alerts[0]["severity"] == "critical"

    def test_parse_failure_spike(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for _ in range(9):
            tracker.record(_make_metric(parse_success=True))
        for _ in range(1):
            tracker.record(_make_metric(parse_success=False))

        alerts = tracker.check_alerts()
        assert len(alerts) == 1
        assert alerts[0]["type"] == "parse_failure_spike"
        assert alerts[0]["severity"] == "warning"

    def test_multiple_alerts(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        # Degrade everything
        for _ in range(5):
            tracker.record(_make_metric(
                validation_passed=False,
                suspicious_content_detected=True,
                parse_success=False,
            ))
        alerts = tracker.check_alerts()
        types = {a["type"] for a in alerts}
        assert "validation_degradation" in types
        assert "suspicious_content_spike" in types
        assert "parse_failure_spike" in types

    def test_alert_includes_agent_id(self, tmp_path: Path) -> None:
        tracker = ResponseQualityTracker(log_dir=str(tmp_path))
        for _ in range(10):
            tracker.record(_make_metric(agent_id="bad-agent", validation_passed=False))
        alerts = tracker.check_alerts("bad-agent")
        assert len(alerts) > 0
        assert alerts[0]["agent_id"] == "bad-agent"


# ---------------------------------------------------------------------------
# Test: module-level singleton
# ---------------------------------------------------------------------------


class TestModuleSingleton:
    """Module-level singleton should work correctly."""

    def setup_method(self) -> None:
        reset_response_quality_tracker()

    def teardown_method(self) -> None:
        reset_response_quality_tracker()

    def test_get_tracker_returns_same_instance(self) -> None:
        t1 = get_response_quality_tracker()
        t2 = get_response_quality_tracker()
        assert t1 is t2

    def test_reset_creates_fresh_instance(self) -> None:
        t1 = get_response_quality_tracker()
        t1.record(_make_metric(agent_id="before-reset"))
        reset_response_quality_tracker()
        t2 = get_response_quality_tracker()
        assert t1 is not t2
        assert len(t2._metrics) == 0


# ---------------------------------------------------------------------------
# Test: ResponseQualityMetric dataclass
# ---------------------------------------------------------------------------


class TestQualityMetricDataclass:
    """ResponseQualityMetric should have sensible defaults."""

    def test_default_values(self) -> None:
        m = ResponseQualityMetric()
        assert m.agent_id == ""
        assert m.model == ""
        assert m.validation_passed is True
        assert m.validation_reason == ""
        assert m.response_length == 0
        assert m.plan_steps == 0
        assert m.has_tool_calls is False
        assert m.suspicious_content_detected is False
        assert m.parse_success is True

    def test_timestamp_auto_set(self) -> None:
        m = ResponseQualityMetric()
        assert m.timestamp > 0

    def test_explicit_values(self) -> None:
        m = ResponseQualityMetric(
            agent_id="custom",
            model="gpt-4o",
            validation_passed=False,
            validation_reason="bad",
            response_length=999,
            plan_steps=5,
            has_tool_calls=True,
            suspicious_content_detected=True,
            parse_success=False,
        )
        assert m.agent_id == "custom"
        assert m.model == "gpt-4o"
        assert m.validation_passed is False
        assert m.suspicious_content_detected is True
