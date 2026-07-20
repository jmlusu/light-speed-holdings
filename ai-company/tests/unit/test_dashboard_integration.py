"""Tests for dashboard integration: task broadcasts, CEO dashboard, department
dashboards, KPI analytics endpoints, and WebSocket subscription filtering.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app

client = TestClient(app, raise_server_exceptions=False)


# ── Helpers ─────────────────────────────────────────────────────────


class FakeWebSocket:
    """Minimal mock for a WebSocket connection."""

    def __init__(self) -> None:
        self.sent: list[str] = []
        self.accepted = False
        self.closed = False

    async def accept(self) -> None:
        self.accepted = True

    async def send_text(self, data: str) -> None:
        if self.closed:
            raise RuntimeError("Connection closed")
        self.sent.append(data)

    async def send_json(self, data: dict[str, Any]) -> None:
        self.sent.append(json.dumps(data, default=str))

    async def receive_json(self) -> dict[str, Any]:
        raise asyncio.CancelledError  # simulates client disconnect


@pytest.fixture()
def setup_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Create fixture data files for integration tests.

    Rebinds the dashboard ``StateStore`` singleton to ``tmp_path`` so all
    state I/O is rooted at the isolated workspace — independent of the
    current working directory (fixes the ``relative_to`` path bug).
    """
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    monkeypatch.chdir(tmp_path)
    reset_state_store()
    get_state_store(tmp_path)

    # Company directory
    (tmp_path / "company").mkdir()
    registry = [
        {
            "name": "chief-of-staff",
            "role": "Chief of Staff",
            "type": "executive",
            "department": "Executive",
            "reportsTo": "human-ceo",
            "directReports": ["lead-engineering", "lead-marketing"],
            "description": "Coordinates all departments",
        },
        {
            "name": "lead-engineering",
            "role": "Lead Engineer",
            "type": "specialist",
            "department": "Engineering",
            "reportsTo": "chief-of-staff",
            "directReports": [],
            "description": "Leads engineering efforts",
        },
        {
            "name": "lead-marketing",
            "role": "Marketing Lead",
            "type": "specialist",
            "department": "Marketing",
            "reportsTo": "chief-of-staff",
            "directReports": [],
            "description": "Leads marketing efforts",
        },
    ]
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(registry), encoding="utf-8"
    )

    # Departments
    departments = {
        "departments": [
            {
                "name": "Executive",
                "executive": "chief-of-staff",
                "agents": ["chief-of-staff"],
                "totalAgents": 1,
            },
            {
                "name": "Engineering",
                "executive": "lead-engineering",
                "agents": ["lead-engineering"],
                "totalAgents": 1,
            },
            {
                "name": "Marketing",
                "executive": "lead-marketing",
                "agents": ["lead-marketing"],
                "totalAgents": 1,
            },
        ]
    }
    (tmp_path / "company" / "departments.yaml").write_text(
        yaml.dump(departments), encoding="utf-8"
    )

    # Orchestrator
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / ".opencode").mkdir(exist_ok=True)
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator" / "approvals.yaml").write_text(
        yaml.dump({"requests": []}), encoding="utf-8"
    )
    (tmp_path / "orchestrator" / "escalation.yaml").write_text(
        yaml.dump({"rules": [], "events": []}), encoding="utf-8"
    )
    (tmp_path / "orchestrator" / "scheduler.yaml").write_text(
        yaml.dump({"tasks": []}), encoding="utf-8"
    )

    # Copy models.yaml
    import shutil
    real_models = Path(__file__).resolve().parents[2] / "company" / "models.yaml"
    if real_models.exists():
        shutil.copy2(str(real_models), str(tmp_path / "company" / "models.yaml"))

    # Copy kpis.yaml
    real_kpis = Path(__file__).resolve().parents[2] / "company" / "config" / "kpis.yaml"
    if real_kpis.exists():
        config_dir = tmp_path / "company" / "config"
        config_dir.mkdir(exist_ok=True)
        shutil.copy2(str(real_kpis), str(config_dir / "kpis.yaml"))

    # Cost tracker
    (tmp_path / "orchestrator" / "cost_tracker.json").write_text(
        json.dumps({"total_budget": 10000, "total_spent": 5000, "llm_spend": 1200}),
        encoding="utf-8",
    )


# ── Task broadcast integration ─────────────────────────────────────


class TestTaskBroadcast:
    """Verify that task creation triggers WebSocket broadcast."""

    def test_create_task_returns_task(self, setup_data: None) -> None:
        resp = client.post(
            "/api/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Build API"},
        )
        assert resp.status_code == 201
        task = resp.json()
        assert task["receiver_id"] == "lead-engineering"
        assert task["status"] == "pending"

    def test_create_task_persists(self, setup_data: None) -> None:
        client.post(
            "/api/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Build API"},
        )
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        tasks = resp.json()
        assert len(tasks) == 1
        assert tasks[0]["instruction"] == "Build API"


# ── CEO Dashboard ──────────────────────────────────────────────────


class TestCEODashboard:
    """Tests for the /api/ceo-dashboard endpoint."""

    def test_ceo_dashboard_returns_all_sections(self, setup_data: None) -> None:
        resp = client.get("/api/ceo-dashboard")
        assert resp.status_code == 200
        data = resp.json()

        assert "collected_at" in data
        assert "company_health" in data
        assert "agent_performance" in data
        assert "cost_tracking" in data
        assert "task_pipeline" in data
        assert "escalation_alerts" in data
        assert "pending_approvals" in data
        assert "scheduled_tasks" in data
        assert "uptime_seconds" in data

    def test_ceo_dashboard_company_health_has_departments(self, setup_data: None) -> None:
        resp = client.get("/api/ceo-dashboard")
        data = resp.json()
        health = data["company_health"]
        assert "departments" in health

    def test_ceo_dashboard_agent_performance(self, setup_data: None) -> None:
        resp = client.get("/api/ceo-dashboard")
        data = resp.json()
        perf = data["agent_performance"]
        assert perf["total_agents"] == 3
        assert "by_type" in perf
        assert "by_department" in perf

    def test_ceo_dashboard_cost_tracking(self, setup_data: None) -> None:
        resp = client.get("/api/ceo-dashboard")
        data = resp.json()
        cost = data["cost_tracking"]
        assert cost["total_budget"] == 10000
        assert cost["total_spent"] == 5000
        assert cost["llm_spend"] == 1200

    def test_ceo_dashboard_task_pipeline(self, setup_data: None) -> None:
        # Add some tasks
        for status in ["pending", "completed", "failed"]:
            client.post(
                "/api/tasks",
                json={"receiver_id": "lead-engineering", "instruction": f"Task {status}"},
            )

        resp = client.get("/api/ceo-dashboard")
        data = resp.json()
        pipeline = data["task_pipeline"]
        assert pipeline["total"] == 3
        assert pipeline["pending"] >= 1


# ── Department Dashboard ───────────────────────────────────────────


class TestDepartmentDashboard:
    """Tests for /api/departments/{dept_name}/dashboard."""

    def test_engineering_dashboard(self, setup_data: None) -> None:
        resp = client.get("/api/departments/engineering/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert data["department"] == "engineering"
        assert "kpis" in data
        assert "agents" in data
        assert "task_stats" in data
        assert "escalations" in data

    def test_engineering_dashboard_agents(self, setup_data: None) -> None:
        resp = client.get("/api/departments/engineering/dashboard")
        data = resp.json()
        agent_names = [a["name"] for a in data["agents"]]
        assert "lead-engineering" in agent_names

    def test_department_not_found(self, setup_data: None) -> None:
        resp = client.get("/api/departments/nonexistent/dashboard")
        assert resp.status_code == 404

    def test_department_dashboard_with_tasks(self, setup_data: None) -> None:
        # Add a task to engineering
        client.post(
            "/api/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Build feature"},
        )
        resp = client.get("/api/departments/engineering/dashboard")
        data = resp.json()
        assert data["task_stats"]["total"] >= 1


# ── KPI History Endpoint ──────────────────────────────────────────


class TestKPIHistory:
    """Tests for /api/kpis/history/{department}."""

    def test_history_empty(self, setup_data: None) -> None:
        resp = client.get("/api/kpis/history/engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_history_with_stored_data(self, setup_data: None) -> None:
        # Trigger collection + storage
        client.get("/api/kpis/collect")

        resp = client.get("/api/kpis/history/engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        assert data[0]["department"] == "engineering"
        assert "kpi_key" in data[0]
        assert "current" in data[0]

    def test_history_filter_kpi_key(self, setup_data: None) -> None:
        client.get("/api/kpis/collect")
        resp = client.get("/api/kpis/history/engineering?kpi_key=total_tasks")
        assert resp.status_code == 200
        data = resp.json()
        for entry in data:
            assert entry["kpi_key"] == "total_tasks"


# ── KPI Trends Endpoint ───────────────────────────────────────────


class TestKPITrends:
    """Tests for /api/kpis/trends/{department}."""

    def test_trends_empty(self, setup_data: None) -> None:
        resp = client.get("/api/kpis/trends/engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_trends_with_two_snapshots(self, setup_data: None) -> None:
        client.get("/api/kpis/collect")
        client.get("/api/kpis/collect")

        resp = client.get("/api/kpis/trends/engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        assert "direction" in data[0]
        assert data[0]["direction"] in ("up", "down", "flat")

    def test_trends_filter_kpi_keys(self, setup_data: None) -> None:
        client.get("/api/kpis/collect")
        client.get("/api/kpis/collect")

        resp = client.get("/api/kpis/trends/engineering?kpi_keys=total_tasks")
        assert resp.status_code == 200
        data = resp.json()
        for t in data:
            assert t["kpi_key"] == "total_tasks"


# ── KPI Alerts Endpoint ───────────────────────────────────────────


class TestKPIAlerts:
    """Tests for /api/kpis/alerts."""

    def test_alerts_returns_structure(self, setup_data: None) -> None:
        resp = client.get("/api/kpis/alerts")
        assert resp.status_code == 200
        data = resp.json()
        assert "evaluated_at" in data
        assert "rules_evaluated" in data
        assert "alerts_fired" in data
        assert "alert_count" in data

    def test_alerts_default_rules_loaded(self, setup_data: None) -> None:
        resp = client.get("/api/kpis/alerts")
        data = resp.json()
        assert data["rules_evaluated"] >= 5  # At least 5 default rules

    def test_alerts_store_snapshot(self, setup_data: None) -> None:
        # First collect + store
        client.get("/api/kpis/collect")
        # Then alerts endpoint should also store
        resp = client.get("/api/kpis/alerts")
        data = resp.json()
        assert "alert_count" in data


# ── KPI Collect Endpoint ──────────────────────────────────────────


class TestKPICollect:
    """Tests for /api/kpis/collect."""

    def test_collect_returns_all_departments(self, setup_data: None) -> None:
        resp = client.get("/api/kpis/collect")
        assert resp.status_code == 200
        data = resp.json()
        assert "collected_at" in data
        assert "departments" in data
        depts = data["departments"]
        assert len(depts) == 7  # All 7 departments
        assert "engineering" in depts
        assert "hr" in depts
        assert "finance" in depts
        assert "marketing" in depts
        assert "sales" in depts
        assert "customer_success" in depts
        assert "legal" in depts

    def test_collect_stores_entries(self, setup_data: None) -> None:
        resp = client.get("/api/kpis/collect")
        data = resp.json()
        assert "stored_entries" in data
        assert data["stored_entries"] > 0


# ── KPI Summary Stats Endpoint ────────────────────────────────────


class TestKPISummaryStats:
    """Tests for /api/kpis/summary-stats/{department}."""

    def test_summary_stats_empty(self, setup_data: None) -> None:
        resp = client.get("/api/kpis/summary-stats/engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_summary_stats_after_collect(self, setup_data: None) -> None:
        client.get("/api/kpis/collect")
        resp = client.get("/api/kpis/summary-stats/engineering")
        assert resp.status_code == 200
        data = resp.json()
        if data:
            assert "min_value" in data[0]
            assert "max_value" in data[0]
            assert "mean_value" in data[0]
            assert "count" in data[0]

    def test_summary_stats_invalid_period(self, setup_data: None) -> None:
        resp = client.get("/api/kpis/summary-stats/engineering?period=yearly")
        assert resp.status_code == 400


# ── WebSocket subscription filtering ───────────────────────────────


@pytest.mark.asyncio
async def test_subscription_filters_topics() -> None:
    """Subscribed clients only receive messages for topics they subscribe to.
    Unsubscribed clients (no explicit topics) still receive all messages
    for backward compatibility.
    """
    from ai_company.dashboard.ws import ConnectionManager

    mgr = ConnectionManager()
    ws_tasks = FakeWebSocket()  # Subscribes to "tasks" only
    ws_kpis = FakeWebSocket()  # Subscribes to "kpis" only

    await mgr.connect(ws_tasks)
    await mgr.connect(ws_kpis)

    # Subscribe ws_tasks to "tasks" topic only
    await mgr.subscribe(ws_tasks, ["tasks"])
    # Subscribe ws_kpis to "kpis" topic only
    await mgr.subscribe(ws_kpis, ["kpis"])

    # Broadcast a task message (has topic="tasks")
    await mgr.broadcast({"type": "task_update", "topic": "tasks", "payload": {}})

    # ws_tasks should receive it, ws_kpis should not
    assert len(ws_tasks.sent) == 1
    assert len(ws_kpis.sent) == 0

    # Broadcast a kpi message (has topic="kpis")
    await mgr.broadcast({"type": "kpi_update", "topic": "kpis", "payload": {}})

    assert len(ws_tasks.sent) == 1  # Still only 1
    assert len(ws_kpis.sent) == 1

    # Broadcast without topic → all receive
    await mgr.broadcast({"type": "system", "payload": {}})

    assert len(ws_tasks.sent) == 2
    assert len(ws_kpis.sent) == 2

    await mgr.disconnect(ws_tasks)
    await mgr.disconnect(ws_kpis)


@pytest.mark.asyncio
async def test_wildcard_subscription() -> None:
    """A client subscribed to '*' receives all topic-filtered messages."""
    from ai_company.dashboard.ws import ConnectionManager

    mgr = ConnectionManager()
    ws_wildcard = FakeWebSocket()
    await mgr.connect(ws_wildcard)
    await mgr.subscribe(ws_wildcard, ["*"])

    # Should receive topic-filtered messages
    await mgr.broadcast({"type": "task_update", "topic": "tasks", "payload": {}})
    await mgr.broadcast({"type": "kpi_update", "topic": "kpis", "payload": {}})

    assert len(ws_wildcard.sent) == 2

    await mgr.disconnect(ws_wildcard)


@pytest.mark.asyncio
async def test_unsubscribe_removes_topics() -> None:
    """Unsubscribing stops delivery for those topics."""
    from ai_company.dashboard.ws import ConnectionManager

    mgr = ConnectionManager()
    ws = FakeWebSocket()
    await mgr.connect(ws)
    await mgr.subscribe(ws, ["tasks", "kpis"])

    # Should receive both
    await mgr.broadcast({"type": "task_update", "topic": "tasks", "payload": {}})
    await mgr.broadcast({"type": "kpi_update", "topic": "kpis", "payload": {}})
    assert len(ws.sent) == 2

    # Unsubscribe from tasks
    async with mgr._lock:
        ws_topics = mgr._subscriptions.get(id(ws), set())
        ws_topics.discard("tasks")

    await mgr.broadcast({"type": "task_update", "topic": "tasks", "payload": {}})
    await mgr.broadcast({"type": "kpi_update", "topic": "kpis", "payload": {}})

    # Only kpi message received
    assert len(ws.sent) == 3

    await mgr.disconnect(ws)
