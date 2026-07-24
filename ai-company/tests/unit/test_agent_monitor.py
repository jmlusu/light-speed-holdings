"""Tests for PRE-20 — agent behavior monitoring (data model + anomaly detection)."""

from __future__ import annotations

import time
from typing import Any

from ai_company.security.agent_monitor import (
    DEFAULT_THRESHOLDS,
    AgentAction,
    AgentBehaviorMonitor,
    AnomalyReport,
    check_agent_anomalies,
    get_agent_monitor,
    record_agent_action,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FAKE_NOW = 1_700_000_000.0


def _make_monitor(
    thresholds: dict[str, int] | None = None,
    window_seconds: int = 3600,
) -> AgentBehaviorMonitor:
    """Create a fresh monitor with optional overrides."""
    return AgentBehaviorMonitor(thresholds=thresholds, window_seconds=window_seconds)


# ---------------------------------------------------------------------------
# AgentAction dataclass
# ---------------------------------------------------------------------------


class TestAgentAction:
    """Validate the AgentAction data record."""

    def test_defaults(self) -> None:
        before = time.time()
        action = AgentAction(agent_id="dev", action_type="tool_calls")
        after = time.time()

        assert action.agent_id == "dev"
        assert action.action_type == "tool_calls"
        assert before <= action.timestamp <= after
        assert action.details == {}
        assert action.success is True

    def test_custom_values(self) -> None:
        action = AgentAction(
            agent_id="cto",
            action_type="llm_calls",
            timestamp=FAKE_NOW,
            details={"model": "gpt-4", "tokens": 1234},
            success=False,
        )
        assert action.timestamp == FAKE_NOW
        assert action.details["model"] == "gpt-4"
        assert action.success is False


# ---------------------------------------------------------------------------
# AnomalyReport dataclass
# ---------------------------------------------------------------------------


class TestAnomalyReport:
    """Validate AnomalyReport construction and serialization."""

    def test_to_dict(self) -> None:
        report = AnomalyReport(
            agent_id="cto",
            action_type="tool_calls_per_hour",
            count=150,
            threshold=100,
            window_start=FAKE_NOW,
            window_end=FAKE_NOW + 3600,
            severity="critical",
        )
        d = report.to_dict()

        assert d["agent_id"] == "cto"
        assert d["action_type"] == "tool_calls_per_hour"
        assert d["count"] == 150
        assert d["threshold"] == 100
        assert d["severity"] == "critical"
        assert len(d) == 7  # all fields present

    def test_severity_warning(self) -> None:
        report = AnomalyReport(
            agent_id="dev",
            action_type="llm_calls",
            count=55,
            threshold=50,
            window_start=FAKE_NOW,
            window_end=FAKE_NOW + 3600,
            severity="warning",
        )
        assert report.to_dict()["severity"] == "warning"


# ---------------------------------------------------------------------------
# Action recording
# ---------------------------------------------------------------------------


class TestActionRecording:
    """Ensure actions are recorded and accessible."""

    def test_record_single_action(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("dev", "tool_calls")

        actions = monitor.get_recent_actions(agent_id="dev")
        assert len(actions) == 1
        assert actions[0].agent_id == "dev"
        assert actions[0].action_type == "tool_calls"

    def test_record_multiple_actions(self) -> None:
        monitor = _make_monitor()
        for _ in range(5):
            monitor.record_action("cto", "llm_calls", details={"tokens": 100})

        actions = monitor.get_recent_actions(agent_id="cto", action_type="llm_calls")
        assert len(actions) == 5

    def test_record_failed_action(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("dev", "tool_calls", success=False)

        actions = monitor.get_recent_actions(agent_id="dev")
        assert len(actions) == 1
        assert actions[0].success is False

    def test_record_with_details(self) -> None:
        monitor = _make_monitor()
        monitor.record_action(
            "dev",
            "memory_access",
            details={"path": "/data/secrets.enc", "action": "read"},
        )

        recent = monitor.get_recent_actions(agent_id="dev")
        assert recent[0].details["path"] == "/data/secrets.enc"

    def test_history_stored_internally(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("dev", "tool_calls")
        monitor.record_action("dev", "tool_calls")

        # Direct access to _history for verification
        assert len(monitor._history["dev"]["tool_calls"]) == 2


# ---------------------------------------------------------------------------
# Threshold / anomaly detection
# ---------------------------------------------------------------------------


class TestThresholdDetection:
    """Validate that anomalies fire when thresholds are exceeded."""

    def test_no_anomaly_under_threshold(self) -> None:
        monitor = _make_monitor(thresholds={"tool_calls_per_hour": 100})
        for _ in range(50):
            monitor.record_action("dev", "tool_calls_per_hour")

        report = monitor.check_anomaly("dev", "tool_calls_per_hour")
        assert report is None

    def test_anomaly_at_threshold_plus_one(self) -> None:
        monitor = _make_monitor(thresholds={"tool_calls_per_hour": 100})
        for _ in range(101):
            monitor.record_action("dev", "tool_calls_per_hour")

        report = monitor.check_anomaly("dev", "tool_calls_per_hour")
        assert report is not None
        assert report.count == 101
        assert report.threshold == 100

    def test_warning_severity(self) -> None:
        """Count > threshold but <= threshold * 2 → warning."""
        monitor = _make_monitor(thresholds={"tool_calls": 50})
        for _ in range(75):  # 75 > 50, 75 <= 100
            monitor.record_action("dev", "tool_calls")

        report = monitor.check_anomaly("dev", "tool_calls")
        assert report is not None
        assert report.severity == "warning"

    def test_critical_severity(self) -> None:
        """Count > threshold * 2 → critical."""
        monitor = _make_monitor(thresholds={"tool_calls": 50})
        for _ in range(105):  # 105 > 100
            monitor.record_action("dev", "tool_calls")

        report = monitor.check_anomaly("dev", "tool_calls")
        assert report is not None
        assert report.severity == "critical"

    def test_unknown_action_type_defaults_to_100(self) -> None:
        """Actions not in thresholds default to 100."""
        monitor = _make_monitor()
        for _ in range(101):
            monitor.record_action("dev", "custom_action_type")

        report = monitor.check_anomaly("dev", "custom_action_type")
        assert report is not None
        assert report.threshold == 100

    def test_check_anomalies_for_agent(self) -> None:
        monitor = _make_monitor(thresholds={"tool_calls": 10, "llm_calls": 5})
        for _ in range(12):
            monitor.record_action("cto", "tool_calls")
        for _ in range(6):
            monitor.record_action("cto", "llm_calls")

        anomalies = monitor.check_anomalies(agent_id="cto")
        action_types = {a.action_type for a in anomalies}
        assert "tool_calls" in action_types
        assert "llm_calls" in action_types

    def test_check_anomalies_all_agents(self) -> None:
        monitor = _make_monitor(thresholds={"tool_calls": 2})
        monitor.record_action("agent_a", "tool_calls")
        monitor.record_action("agent_a", "tool_calls")
        monitor.record_action("agent_a", "tool_calls")  # 3 > 2

        monitor.record_action("agent_b", "tool_calls")
        monitor.record_action("agent_b", "tool_calls")
        monitor.record_action("agent_b", "tool_calls")
        monitor.record_action("agent_b", "tool_calls")  # 4 > 2

        anomalies = monitor.check_anomalies()
        agent_ids = {a.agent_id for a in anomalies}
        assert "agent_a" in agent_ids
        assert "agent_b" in agent_ids


# ---------------------------------------------------------------------------
# Set / update thresholds
# ---------------------------------------------------------------------------


class TestThresholdConfiguration:
    """Test dynamic threshold changes."""

    def test_set_threshold(self) -> None:
        monitor = _make_monitor(thresholds={"tool_calls": 100})
        monitor.set_threshold("tool_calls", 5)
        assert monitor.thresholds["tool_calls"] == 5

    def test_add_new_threshold(self) -> None:
        monitor = _make_monitor()
        monitor.set_threshold("custom_action", 200)
        assert monitor.thresholds["custom_action"] == 200

    def test_custom_thresholds_override_defaults(self) -> None:
        monitor = _make_monitor(thresholds={"tool_calls": 10})
        assert "tool_calls" not in DEFAULT_THRESHOLDS or monitor.thresholds["tool_calls"] == 10


# ---------------------------------------------------------------------------
# Agent summaries
# ---------------------------------------------------------------------------


class TestAgentSummaries:
    """Validate summary generation for agents."""

    def test_summary_empty_agent(self) -> None:
        monitor = _make_monitor()
        summary = monitor.get_agent_summary("nonexistent")

        assert summary["agent_id"] == "nonexistent"
        assert summary["actions"] == {}
        assert summary["total_actions"] == 0

    def test_summary_with_actions(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("dev", "tool_calls")
        monitor.record_action("dev", "tool_calls")
        monitor.record_action("dev", "llm_calls")

        summary = monitor.get_agent_summary("dev")
        assert summary["actions"]["tool_calls"] == 2
        assert summary["actions"]["llm_calls"] == 1
        assert summary["total_actions"] == 3

    def test_summary_respects_window(self) -> None:
        monitor = _make_monitor(window_seconds=1)

        # Record action
        monitor.record_action("dev", "tool_calls")

        # Wait for window to expire
        time.sleep(1.1)

        summary = monitor.get_agent_summary("dev")
        assert summary["total_actions"] == 0

    def test_all_summaries(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("agent_a", "tool_calls")
        monitor.record_action("agent_b", "llm_calls")

        summaries = monitor.get_all_summaries()
        assert "agent_a" in summaries
        assert "agent_b" in summaries
        assert summaries["agent_a"]["total_actions"] == 1
        assert summaries["agent_b"]["total_actions"] == 1

    def test_window_seconds_in_summary(self) -> None:
        monitor = _make_monitor(window_seconds=7200)
        summary = monitor.get_agent_summary("dev")
        assert summary["window_seconds"] == 7200


# ---------------------------------------------------------------------------
# Window pruning
# ---------------------------------------------------------------------------


class TestWindowPruning:
    """Validate that old entries are pruned from the history window."""

    def test_old_actions_pruned_on_record(self) -> None:
        monitor = _make_monitor(window_seconds=1)

        # Record first batch
        for _ in range(5):
            monitor.record_action("dev", "tool_calls")

        # Wait for window expiry
        time.sleep(1.1)

        # Record one new action — triggers pruning of the old ones
        monitor.record_action("dev", "tool_calls")

        # Only 1 action should remain in the window
        summary = monitor.get_agent_summary("dev")
        assert summary["actions"]["tool_calls"] == 1

    def test_old_actions_pruned_on_check(self) -> None:
        monitor = _make_monitor(window_seconds=1)

        for _ in range(5):
            monitor.record_action("dev", "tool_calls")

        time.sleep(1.1)

        # check_anomaly also prunes when it reads
        report = monitor.check_anomaly("dev", "tool_calls")
        assert report is None  # all old actions pruned, 0 < threshold


# ---------------------------------------------------------------------------
# Reset
# ---------------------------------------------------------------------------


class TestReset:
    """Validate that reset clears all state."""

    def test_reset_clears_history(self) -> None:
        monitor = _make_monitor()
        for _ in range(10):
            monitor.record_action("dev", "tool_calls")

        monitor.reset()

        actions = monitor.get_recent_actions(agent_id="dev")
        assert len(actions) == 0

    def test_reset_clears_actions_log(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("dev", "tool_calls")
        monitor.reset()

        all_actions = monitor.get_recent_actions()
        assert len(all_actions) == 0

    def test_reset_all_summaries_empty(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("dev", "tool_calls")
        monitor.reset()

        summaries = monitor.get_all_summaries()
        assert len(summaries) == 0

    def test_no_anomalies_after_reset(self) -> None:
        monitor = _make_monitor(thresholds={"tool_calls": 2})
        for _ in range(5):
            monitor.record_action("dev", "tool_calls")

        monitor.reset()
        anomalies = monitor.check_anomalies()
        assert len(anomalies) == 0


# ---------------------------------------------------------------------------
# get_recent_actions — filtering & ordering
# ---------------------------------------------------------------------------


class TestRecentActions:
    """Validate filtering and ordering of get_recent_actions."""

    def test_limit(self) -> None:
        monitor = _make_monitor()
        for _ in range(50):
            monitor.record_action("dev", "tool_calls")

        result = monitor.get_recent_actions(limit=10)
        assert len(result) == 10

    def test_filter_by_agent(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("agent_a", "tool_calls")
        monitor.record_action("agent_b", "tool_calls")

        result = monitor.get_recent_actions(agent_id="agent_a")
        assert len(result) == 1
        assert result[0].agent_id == "agent_a"

    def test_filter_by_action_type(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("dev", "tool_calls")
        monitor.record_action("dev", "llm_calls")

        result = monitor.get_recent_actions(action_type="llm_calls")
        assert len(result) == 1
        assert result[0].action_type == "llm_calls"

    def test_ordering_most_recent_first(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("dev", "tool_calls")
        time.sleep(0.01)
        monitor.record_action("dev", "llm_calls")

        result = monitor.get_recent_actions()
        # llm_calls should be first (more recent)
        assert result[0].action_type == "llm_calls"
        assert result[1].action_type == "tool_calls"

    def test_combined_filters(self) -> None:
        monitor = _make_monitor()
        monitor.record_action("agent_a", "tool_calls")
        monitor.record_action("agent_a", "llm_calls")
        monitor.record_action("agent_b", "tool_calls")

        result = monitor.get_recent_actions(agent_id="agent_a", action_type="tool_calls")
        assert len(result) == 1
        assert result[0].agent_id == "agent_a"
        assert result[0].action_type == "tool_calls"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Edge cases: empty history, multiple agents, multiple action types."""

    def test_empty_history_no_anomalies(self) -> None:
        monitor = _make_monitor()
        anomalies = monitor.check_anomalies()
        assert anomalies == []

    def test_empty_history_no_summary(self) -> None:
        monitor = _make_monitor()
        summaries = monitor.get_all_summaries()
        assert summaries == {}

    def test_multiple_agents_independent(self) -> None:
        monitor = _make_monitor(thresholds={"tool_calls": 3})

        for _ in range(4):
            monitor.record_action("agent_a", "tool_calls")

        monitor.record_action("agent_b", "tool_calls")

        anomalies = monitor.check_anomalies()
        # Only agent_a should trigger
        agent_ids = {a.agent_id for a in anomalies}
        assert "agent_a" in agent_ids
        assert "agent_b" not in agent_ids

    def test_multiple_action_types_independent(self) -> None:
        monitor = _make_monitor(
            thresholds={"tool_calls": 3, "llm_calls": 2}
        )

        for _ in range(4):
            monitor.record_action("dev", "tool_calls")

        for _ in range(3):
            monitor.record_action("dev", "llm_calls")

        anomalies = monitor.check_anomalies(agent_id="dev")
        action_types = {a.action_type for a in anomalies}
        assert "tool_calls" in action_types
        assert "llm_calls" in action_types

    def test_threshold_at_exact_boundary(self) -> None:
        """Exactly at threshold should NOT be an anomaly (must exceed)."""
        monitor = _make_monitor(thresholds={"tool_calls": 5})
        for _ in range(5):
            monitor.record_action("dev", "tool_calls")

        report = monitor.check_anomaly("dev", "tool_calls")
        assert report is None

    def test_zero_threshold(self) -> None:
        """Even one action exceeds a zero threshold."""
        monitor = _make_monitor(thresholds={"tool_calls": 0})
        monitor.record_action("dev", "tool_calls")

        report = monitor.check_anomaly("dev", "tool_calls")
        assert report is not None
        assert report.severity == "critical"  # 1 > 0 * 2


# ---------------------------------------------------------------------------
# Module-level singleton helpers
# ---------------------------------------------------------------------------


class TestModuleSingleton:
    """Validate the module-level convenience functions."""

    def test_get_agent_monitor_returns_same_instance(self) -> None:
        m1 = get_agent_monitor()
        m2 = get_agent_monitor()
        assert m1 is m2

    def test_record_agent_action_uses_singleton(self) -> None:
        monitor = get_agent_monitor()
        monitor.reset()  # clean slate

        record_agent_action("singleton_agent", "tool_calls")
        actions = monitor.get_recent_actions(agent_id="singleton_agent")
        assert len(actions) == 1

    def test_check_agent_anomalies_uses_singleton(self) -> None:
        monitor = get_agent_monitor()
        monitor.reset()

        # No actions → no anomalies
        result = check_agent_anomalies()
        assert isinstance(result, list)

    def test_singleton_tracks_across_calls(self) -> None:
        monitor = get_agent_monitor()
        monitor.reset()

        record_agent_action("dev", "tool_calls")
        record_agent_action("dev", "tool_calls")

        summary = monitor.get_agent_summary("dev")
        assert summary["total_actions"] == 2


# ---------------------------------------------------------------------------
# Logger verification (smoke)
# ---------------------------------------------------------------------------


class TestLogging:
    """Ensure logger is called when anomalies are found."""

    def test_warning_logged(self, caplog: Any) -> None:
        import logging

        monitor = _make_monitor(thresholds={"tool_calls": 1})
        for _ in range(3):
            monitor.record_action("dev", "tool_calls")

        with caplog.at_level(logging.WARNING, logger="ai_company.security.agent_monitor"):
            monitor.check_anomalies(agent_id="dev")

        assert "Agent behavior anomaly" in caplog.text
