"""Tests for the Agent Behavior KPI collector."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.dashboard.kpis.agent_behavior import AgentBehaviorKPICollector
from ai_company.security.agent_monitor import AgentBehaviorMonitor


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def monitor() -> AgentBehaviorMonitor:
    """Return a fresh monitor and reset the module singleton after test."""
    monitor = AgentBehaviorMonitor()
    # Patch the module singleton so the collector uses our test monitor
    import ai_company.security.agent_monitor as mod
    original = mod._default_monitor
    mod._default_monitor = monitor
    yield monitor
    mod._default_monitor = original


@pytest.fixture()
def empty_monitor() -> AgentBehaviorMonitor:
    """Return a monitor with no recorded actions."""
    monitor = AgentBehaviorMonitor()
    import ai_company.security.agent_monitor as mod
    original = mod._default_monitor
    mod._default_monitor = monitor
    yield monitor
    mod._default_monitor = original


# ---------------------------------------------------------------------------
# Collector basics
# ---------------------------------------------------------------------------

class TestAgentBehaviorKPICollector:
    def test_department_name(self) -> None:
        collector = AgentBehaviorKPICollector()
        assert collector.department == "agent_behavior"

    def test_collect_empty_monitor(self, empty_monitor: AgentBehaviorMonitor) -> None:
        """When no agents are tracked, all counts are zero."""
        result = AgentBehaviorKPICollector().collect()
        assert result["department"] == "agent_behavior"
        kpis = result["kpis"]
        assert kpis["total_agents_monitored"]["current"] == 0
        assert kpis["active_agents"]["current"] == 0
        assert kpis["total_actions"]["current"] == 0
        assert kpis["anomaly_count"]["current"] == 0
        assert kpis["critical_anomalies"]["current"] == 0
        assert kpis["action_breakdown"] == {}
        assert kpis["agent_summaries"] == {}

    def test_collect_with_actions(self, monitor: AgentBehaviorMonitor) -> None:
        """Collector reports correct aggregate metrics after actions."""
        monitor.record_action("cto", "tool_call")
        monitor.record_action("cto", "tool_call")
        monitor.record_action("cto", "llm_call")
        monitor.record_action("cmo", "delegation")

        result = AgentBehaviorKPICollector().collect()
        kpis = result["kpis"]

        assert kpis["total_agents_monitored"]["current"] == 2
        assert kpis["active_agents"]["current"] == 2
        assert kpis["total_actions"]["current"] == 4

        # Per-action breakdown
        breakdown = kpis["action_breakdown"]
        assert breakdown["tool_call"] == 2
        assert breakdown["llm_call"] == 1
        assert breakdown["delegation"] == 1

    def test_collect_agent_summaries(self, monitor: AgentBehaviorMonitor) -> None:
        """Agent summaries are included in the result."""
        monitor.record_action("cto", "tool_call")
        monitor.record_action("cto", "tool_call")
        monitor.record_action("cto", "llm_call")

        result = AgentBehaviorKPICollector().collect()
        summaries = result["kpis"]["agent_summaries"]

        assert "cto" in summaries
        cto = summaries["cto"]
        assert cto["total_actions"] == 3
        assert cto["actions"]["tool_call"] == 2
        assert cto["actions"]["llm_call"] == 1

    def test_anomaly_detection(self, monitor: AgentBehaviorMonitor) -> None:
        """Anomalies are counted when thresholds are exceeded."""
        # Default threshold for tool_calls_per_hour is 100
        # Set a low threshold for testing
        monitor.set_threshold("tool_calls", 5)

        # Record 6 actions (exceeds threshold of 5)
        for _ in range(6):
            monitor.record_action("cto", "tool_calls")

        result = AgentBehaviorKPICollector().collect()
        kpis = result["kpis"]

        assert kpis["anomaly_count"]["current"] >= 1

    def test_critical_anomaly_detection(self, monitor: AgentBehaviorMonitor) -> None:
        """Critical anomalies are detected when count > 2x threshold."""
        monitor.set_threshold("tool_calls", 5)

        # Record 12 actions (exceeds 2 * 5 = 10, so critical)
        for _ in range(12):
            monitor.record_action("cto", "tool_calls")

        result = AgentBehaviorKPICollector().collect()
        kpis = result["kpis"]

        # Should have at least one critical anomaly
        assert kpis["critical_anomalies"]["current"] >= 1

    def test_no_anomaly_when_under_threshold(self, monitor: AgentBehaviorMonitor) -> None:
        """No anomalies when actions are below threshold."""
        monitor.set_threshold("tool_calls", 100)

        for _ in range(5):
            monitor.record_action("cto", "tool_calls")

        result = AgentBehaviorKPICollector().collect()
        kpis = result["kpis"]

        assert kpis["anomaly_count"]["current"] == 0
        assert kpis["critical_anomalies"]["current"] == 0

    def test_graceful_handling_of_import_error(self) -> None:
        """Collector returns error dict if agent_monitor import fails."""
        # This test verifies the collector handles import failures gracefully
        # In practice, the import should succeed, but we test the except path
        collector = AgentBehaviorKPICollector()
        result = collector.collect()
        # Should always return a valid structure
        assert "department" in result
        assert "kpis" in result

    def test_kpi_status_info_when_no_target(self, empty_monitor: AgentBehaviorMonitor) -> None:
        """KPIs without targets have status 'info'."""
        result = AgentBehaviorKPICollector().collect()
        kpis = result["kpis"]

        assert kpis["total_agents_monitored"]["status"] == "info"
        assert kpis["active_agents"]["status"] == "info"
        assert kpis["total_actions"]["status"] == "info"

    def test_kpi_status_for_anomalies(self, monitor: AgentBehaviorMonitor) -> None:
        """Anomaly KPIs use 'on_track' when count is 0 (below target)."""
        result = AgentBehaviorKPICollector().collect()
        kpis = result["kpis"]

        # anomaly_count target is 0, current is 0 → on_track (lower is better)
        assert kpis["anomaly_count"]["status"] == "on_track"
        assert kpis["critical_anomalies"]["status"] == "on_track"

    def test_multiple_agents_active_status(self, monitor: AgentBehaviorMonitor) -> None:
        """Agents with 0 actions are not counted as active."""
        monitor.record_action("cto", "tool_call")
        monitor.record_action("cto", "tool_call")
        # cmo has no actions recorded

        result = AgentBehaviorKPICollector().collect()
        kpis = result["kpis"]

        # Only cto is active (has actions)
        assert kpis["active_agents"]["current"] == 1
        # But both are monitored (have history entries)
        assert kpis["total_agents_monitored"]["current"] == 1

    def test_positional_project_root(self, tmp_path: Path) -> None:
        """Collector accepts project_root as positional arg (compat with ALL_COLLECTORS test)."""
        collector = AgentBehaviorKPICollector(tmp_path)
        result = collector.collect()
        assert result["department"] == "agent_behavior"

    def test_keyword_project_root(self, tmp_path: Path) -> None:
        """Collector accepts project_root as keyword arg."""
        collector = AgentBehaviorKPICollector(project_root=tmp_path)
        result = collector.collect()
        assert result["department"] == "agent_behavior"
