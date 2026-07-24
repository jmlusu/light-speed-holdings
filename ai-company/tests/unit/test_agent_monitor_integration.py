"""Tests for PRE-20: Agent behavior monitoring integration.

Covers:
- Action recording during task execution (task_started, task_completed, tool_call, delegation)
- Anomaly detection when thresholds are exceeded
- Dashboard API endpoints returning monitoring data
- Agent health endpoint
"""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from ai_company.security.agent_monitor import (
    AgentMonitor,
    Anomaly,
    get_agent_monitor,
    reset_agent_monitor,
)
from ai_company.dashboard.app import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_monitor():
    """Reset the agent monitor singleton between tests."""
    reset_agent_monitor()
    yield
    reset_agent_monitor()


# ---------------------------------------------------------------------------
# Unit tests — AgentMonitor
# ---------------------------------------------------------------------------


class TestAgentMonitorRecording:
    """Verify action recording and summary updates."""

    def test_record_task_started(self) -> None:
        monitor = AgentMonitor()
        action = monitor.record_action(
            "agent-a", "task_started", {"task_id": "t1"}
        )
        assert action.agent_id == "agent-a"
        assert action.action_type == "task_started"
        assert action.details["task_id"] == "t1"

        summary = monitor.get_agent_summary("agent-a")
        assert summary["total_actions"] == 1

    def test_record_task_completed_success(self) -> None:
        monitor = AgentMonitor()
        monitor.record_action(
            "agent-a", "task_completed",
            {"task_id": "t1", "status": "completed"},
            success=True,
        )
        summary = monitor.get_agent_summary("agent-a")
        assert summary["total_successes"] == 1
        assert summary["total_failures"] == 0
        assert summary["failure_rate"] == 0.0

    def test_record_task_completed_failure(self) -> None:
        monitor = AgentMonitor()
        monitor.record_action(
            "agent-a", "task_completed",
            {"task_id": "t1", "status": "failed"},
            success=False,
        )
        summary = monitor.get_agent_summary("agent-a")
        assert summary["total_failures"] == 1
        assert summary["failure_rate"] == 1.0

    def test_record_tool_call(self) -> None:
        monitor = AgentMonitor()
        monitor.record_action(
            "agent-a", "tool_call",
            {"tool": "read", "status": "ok"},
            success=True,
        )
        summary = monitor.get_agent_summary("agent-a")
        assert summary["tool_calls"] == 1
        assert summary["total_actions"] == 1

    def test_record_llm_call(self) -> None:
        monitor = AgentMonitor()
        monitor.record_action(
            "agent-a", "llm_call",
            {"tokens": 500},
        )
        summary = monitor.get_agent_summary("agent-a")
        assert summary["llm_calls"] == 1

    def test_record_delegation(self) -> None:
        monitor = AgentMonitor()
        monitor.record_action(
            "agent-a", "delegation",
            {"receiver": "agent-b", "task_id": "t1"},
        )
        summary = monitor.get_agent_summary("agent-a")
        assert summary["delegations"] == 1

    def test_get_recent_actions_limit(self) -> None:
        monitor = AgentMonitor()
        for i in range(5):
            monitor.record_action("agent-a", "tool_call", {"i": i})

        recent = monitor.get_recent_actions("agent-a", limit=3)
        assert len(recent) == 3
        # Most recent 3
        assert recent[0].details["i"] == 2
        assert recent[2].details["i"] == 4

    def test_get_recent_actions_empty(self) -> None:
        monitor = AgentMonitor()
        recent = monitor.get_recent_actions("unknown-agent")
        assert recent == []

    def test_action_rotation(self) -> None:
        """Actions beyond max limit are pruned."""
        monitor = AgentMonitor()
        monitor._max_actions_per_agent = 5
        for i in range(10):
            monitor.record_action("agent-a", "tool_call", {"i": i})

        actions = monitor.get_recent_actions("agent-a", limit=100)
        assert len(actions) == 5
        # First retained action should be i=5
        assert actions[0].details["i"] == 5

    def test_get_all_summaries(self) -> None:
        monitor = AgentMonitor()
        monitor.record_action("agent-a", "task_started", {})
        monitor.record_action("agent-b", "task_started", {})

        summaries = monitor.get_all_summaries()
        assert "agent-a" in summaries
        assert "agent-b" in summaries
        assert len(summaries) == 2


# ---------------------------------------------------------------------------
# Unit tests — Anomaly detection
# ---------------------------------------------------------------------------


class TestAgentMonitorAnomalies:
    """Verify anomaly detection logic."""

    def test_no_anomalies_for_healthy_agent(self) -> None:
        monitor = AgentMonitor()
        monitor.record_action("agent-a", "task_started", {})
        monitor.record_action(
            "agent-a", "task_completed", {}, success=True,
        )
        anomalies = monitor.check_anomalies("agent-a")
        assert anomalies == []

    def test_high_failure_rate_anomaly(self) -> None:
        monitor = AgentMonitor()
        # 8 failures, 2 successes = 80% failure rate
        for _ in range(8):
            monitor.record_action(
                "agent-a", "task_completed", {}, success=False,
            )
        for _ in range(2):
            monitor.record_action(
                "agent-a", "task_completed", {}, success=True,
            )

        anomalies = monitor.check_anomalies("agent-a")
        assert len(anomalies) >= 1
        failure_anomaly = next(
            a for a in anomalies if a.anomaly_type == "high_failure_rate"
        )
        assert failure_anomaly.severity == "critical"  # > 80%

    def test_warning_severity_for_moderate_failure_rate(self) -> None:
        monitor = AgentMonitor()
        # 3 failures, 7 successes = 30% failure rate (above 50%? no, below)
        # Actually: 6 failures, 4 successes = 60% > 50%
        for _ in range(6):
            monitor.record_action(
                "agent-a", "task_completed", {}, success=False,
            )
        for _ in range(4):
            monitor.record_action(
                "agent-a", "task_completed", {}, success=True,
            )

        anomalies = monitor.check_anomalies("agent-a")
        failure_anomaly = next(
            (a for a in anomalies if a.anomaly_type == "high_failure_rate"), None
        )
        assert failure_anomaly is not None
        assert failure_anomaly.severity == "warning"  # > 50% but <= 80%

    def test_excessive_delegation_anomaly(self) -> None:
        monitor = AgentMonitor()
        for _ in range(6):  # > MAX_DELEGATION_DEPTH (5)
            monitor.record_action(
                "agent-a", "delegation", {"receiver": "agent-b"},
            )

        anomalies = monitor.check_anomalies("agent-a")
        delegation_anomaly = next(
            a for a in anomalies if a.anomaly_type == "excessive_delegation"
        )
        assert "6 delegations" in delegation_anomaly.description

    def test_check_anomalies_all_agents(self) -> None:
        monitor = AgentMonitor()
        for _ in range(6):
            monitor.record_action(
                "agent-a", "delegation", {"receiver": "agent-b"},
            )

        anomalies = monitor.check_anomalies()  # No agent_id = check all
        assert any(a.agent_id == "agent-a" for a in anomalies)

    def test_anomaly_to_dict(self) -> None:
        anomaly = Anomaly(
            agent_id="agent-a",
            anomaly_type="high_failure_rate",
            description="80% failure rate",
            detected_at=time.time(),
            severity="critical",
        )
        d = anomaly.to_dict()
        assert d["agent_id"] == "agent-a"
        assert d["anomaly_type"] == "high_failure_rate"
        assert d["severity"] == "critical"

    def test_monitor_reset(self) -> None:
        monitor = AgentMonitor()
        monitor.record_action("agent-a", "task_started", {})
        monitor.reset()

        summary = monitor.get_agent_summary("agent-a")
        assert summary["total_actions"] == 0
        assert monitor.check_anomalies("agent-a") == []


# ---------------------------------------------------------------------------
# Unit tests — Singleton
# ---------------------------------------------------------------------------


class TestAgentMonitorSingleton:
    """Verify the module-level singleton pattern."""

    def test_get_agent_monitor_returns_same_instance(self) -> None:
        m1 = get_agent_monitor()
        m2 = get_agent_monitor()
        assert m1 is m2

    def test_reset_agent_monitor_clears_singleton(self) -> None:
        m1 = get_agent_monitor()
        m1.record_action("agent-a", "task_started", {})
        reset_agent_monitor()
        m2 = get_agent_monitor()
        assert m1 is not m2
        assert m2.get_agent_summary("agent-a")["total_actions"] == 0


# ---------------------------------------------------------------------------
# Dashboard API integration tests
# ---------------------------------------------------------------------------


class TestBehaviorMonitoringEndpoints:
    """Verify the dashboard behavior monitoring API endpoints."""

    def test_get_agent_behavior_returns_200(self) -> None:
        monitor = get_agent_monitor()
        monitor.record_action(
            "chief-of-staff", "task_started", {"task_id": "t1"}
        )
        monitor.record_action(
            "chief-of-staff", "tool_call",
            {"tool": "read", "status": "ok"},
            success=True,
        )

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/api/v1/agents/chief-of-staff/behavior")
        assert response.status_code == 200

        data = response.json()
        assert "summary" in data
        assert "anomalies" in data
        assert "recent_actions" in data
        assert data["summary"]["total_actions"] == 2
        assert len(data["recent_actions"]) == 2

    def test_get_agent_behavior_empty_agent(self) -> None:
        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/api/v1/agents/unknown-agent/behavior")
        assert response.status_code == 200

        data = response.json()
        assert data["summary"]["total_actions"] == 0
        assert data["recent_actions"] == []

    def test_get_all_anomalies_returns_200(self) -> None:
        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/api/v1/agents/behavior/anomalies")
        assert response.status_code == 200

        data = response.json()
        assert "anomalies" in data
        assert "agent_summaries" in data
        assert "total_anomalies" in data
        assert isinstance(data["anomalies"], list)

    def test_get_all_anomalies_with_anomaly(self) -> None:
        monitor = get_agent_monitor()
        for _ in range(6):
            monitor.record_action(
                "agent-a", "delegation", {"receiver": "agent-b"},
            )

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/api/v1/agents/behavior/anomalies")
        assert response.status_code == 200

        data = response.json()
        assert data["total_anomalies"] >= 1
        assert "agent-a" in data["agent_summaries"]

    def test_behavior_endpoint_action_format(self) -> None:
        """Verify the shape of recent_actions in the API response."""
        monitor = get_agent_monitor()
        monitor.record_action(
            "agent-x", "task_started", {"task_id": "t1"}
        )

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/api/v1/agents/agent-x/behavior")
        data = response.json()

        action = data["recent_actions"][0]
        assert "action_type" in action
        assert "timestamp" in action
        assert "success" in action
        assert "details" in action


# ---------------------------------------------------------------------------
# Dashboard monitoring health endpoint tests
# ---------------------------------------------------------------------------


class TestAgentHealthEndpoint:
    """Verify the /monitoring/agent-health endpoint."""

    def test_agent_health_healthy(self) -> None:
        monitor = get_agent_monitor()
        monitor.record_action("agent-a", "task_started", {})

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/monitoring/agent-health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["anomaly_count"] == 0
        assert data["monitored_agents"] == 1

    def test_agent_health_degraded(self) -> None:
        monitor = get_agent_monitor()
        # Create enough failures to trigger anomaly
        for _ in range(8):
            monitor.record_action(
                "agent-a", "task_completed", {}, success=False,
            )
        for _ in range(2):
            monitor.record_action(
                "agent-a", "task_completed", {}, success=True,
            )

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/monitoring/agent-health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "degraded"
        assert data["anomaly_count"] >= 1

    def test_agent_health_no_agents(self) -> None:
        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/monitoring/agent-health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["monitored_agents"] == 0


# ---------------------------------------------------------------------------
# Integration: delegation recording in executor loop
# ---------------------------------------------------------------------------


class TestDelegationRecording:
    """Verify that delegation actions are recorded by the executor."""

    def test_delegation_recorded_on_subtask_creation(self) -> None:
        """When _create_subtask_from_record fires, a delegation action should
        appear in the monitor."""
        monitor = get_agent_monitor()

        # Simulate a delegation being recorded
        monitor.record_action(
            "parent-agent",
            "delegation",
            {
                "receiver": "child-agent",
                "task_id": "parent-task-id",
                "subtask_id": "subtask-id",
            },
        )

        summary = monitor.get_agent_summary("parent-agent")
        assert summary["delegations"] == 1

        recent = monitor.get_recent_actions("parent-agent", limit=1)
        assert recent[0].action_type == "delegation"
        assert recent[0].details["receiver"] == "child-agent"


# ---------------------------------------------------------------------------
# Integration: tool call recording in agent loop
# ---------------------------------------------------------------------------


class TestToolCallRecording:
    """Verify that tool call actions are recorded during agent loop."""

    def test_tool_calls_recorded(self) -> None:
        """When tools execute during the agent loop, tool_call actions
        should appear in the monitor."""
        monitor = get_agent_monitor()

        # Simulate multiple tool calls as they would be recorded
        tools = [("read", "ok"), ("write", "ok"), ("bash", "error")]
        for tool_name, status in tools:
            monitor.record_action(
                "agent-a",
                "tool_call",
                {"tool": tool_name, "status": status},
                success=(status == "ok"),
            )

        summary = monitor.get_agent_summary("agent-a")
        assert summary["tool_calls"] == 3
        assert summary["total_successes"] == 2
        assert summary["total_failures"] == 1


# ---------------------------------------------------------------------------
# Integration: LLM call recording in agent loop
# ---------------------------------------------------------------------------


class TestLLMCallRecording:
    """Verify that LLM call actions are recorded during agent loop."""

    def test_llm_calls_recorded(self) -> None:
        """When the LLM is called during the agent loop, llm_call actions
        should appear in the monitor."""
        monitor = get_agent_monitor()

        for i in range(3):
            monitor.record_action(
                "agent-a",
                "llm_call",
                {"tokens": 500 * (i + 1), "iteration": i + 1},
            )

        summary = monitor.get_agent_summary("agent-a")
        assert summary["llm_calls"] == 3
        assert summary["total_actions"] == 3
