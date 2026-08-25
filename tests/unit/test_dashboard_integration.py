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
    (tmp_path / "company" / "departments.yaml").write_text(yaml.dump(departments), encoding="utf-8")

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
            "/api/v1/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Build API"},
        )
        assert resp.status_code == 201
        task = resp.json()
        assert task["receiver_id"] == "lead-engineering"
        assert task["status"] == "pending"

    def test_create_task_persists(self, setup_data: None) -> None:
        client.post(
            "/api/v1/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Build API"},
        )
        resp = client.get("/api/v1/tasks")
        assert resp.status_code == 200
        tasks = resp.json()
        assert len(tasks) == 1
        assert tasks[0]["instruction"] == "Build API"


# ── CEO Dashboard ──────────────────────────────────────────────────


class TestCEODashboard:
    """Tests for the /api/ceo-dashboard endpoint."""

    def test_ceo_dashboard_returns_all_sections(self, setup_data: None) -> None:
        resp = client.get("/api/v1/ceo-dashboard")
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
        resp = client.get("/api/v1/ceo-dashboard")
        data = resp.json()
        health = data["company_health"]
        assert "departments" in health

    def test_ceo_dashboard_agent_performance(self, setup_data: None) -> None:
        resp = client.get("/api/v1/ceo-dashboard")
        data = resp.json()
        perf = data["agent_performance"]
        assert perf["total_agents"] == 3
        assert "by_type" in perf
        assert "by_department" in perf

    def test_ceo_dashboard_cost_tracking(self, setup_data: None) -> None:
        resp = client.get("/api/v1/ceo-dashboard")
        data = resp.json()
        cost = data["cost_tracking"]
        assert cost["total_budget"] == 10000
        assert cost["total_spent"] == 5000
        assert cost["llm_spend"] == 1200

    def test_ceo_dashboard_task_pipeline(self, setup_data: None) -> None:
        # Add some tasks
        for status in ["pending", "completed", "failed"]:
            client.post(
                "/api/v1/tasks",
                json={"receiver_id": "lead-engineering", "instruction": f"Task {status}"},
            )

        resp = client.get("/api/v1/ceo-dashboard")
        data = resp.json()
        pipeline = data["task_pipeline"]
        assert pipeline["total"] == 3
        assert pipeline["pending"] >= 1


# ── Department Dashboard ───────────────────────────────────────────


class TestDepartmentDashboard:
    """Tests for /api/departments/{dept_name}/dashboard."""

    def test_engineering_dashboard(self, setup_data: None) -> None:
        resp = client.get("/api/v1/departments/engineering/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert data["department"] == "engineering"
        assert "kpis" in data
        assert "agents" in data
        assert "task_stats" in data
        assert "escalations" in data

    def test_engineering_dashboard_agents(self, setup_data: None) -> None:
        resp = client.get("/api/v1/departments/engineering/dashboard")
        data = resp.json()
        agent_names = [a["name"] for a in data["agents"]]
        assert "lead-engineering" in agent_names

    def test_department_not_found(self, setup_data: None) -> None:
        resp = client.get("/api/v1/departments/nonexistent/dashboard")
        assert resp.status_code == 404

    def test_department_dashboard_with_tasks(self, setup_data: None) -> None:
        # Add a task to engineering
        client.post(
            "/api/v1/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Build feature"},
        )
        resp = client.get("/api/v1/departments/engineering/dashboard")
        data = resp.json()
        assert data["task_stats"]["total"] >= 1


# ── KPI History Endpoint ──────────────────────────────────────────


class TestKPIHistory:
    """Tests for /api/kpis/history/{department}."""

    def test_history_empty(self, setup_data: None) -> None:
        resp = client.get("/api/v1/kpis/history/engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_history_with_stored_data(self, setup_data: None) -> None:
        # Trigger collection + storage
        client.get("/api/v1/kpis/collect")

        resp = client.get("/api/v1/kpis/history/engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        assert data[0]["department"] == "engineering"
        assert "kpi_key" in data[0]
        assert "current" in data[0]

    def test_history_filter_kpi_key(self, setup_data: None) -> None:
        client.get("/api/v1/kpis/collect")
        resp = client.get("/api/v1/kpis/history/engineering?kpi_key=total_tasks")
        assert resp.status_code == 200
        data = resp.json()
        for entry in data:
            assert entry["kpi_key"] == "total_tasks"


# ── KPI Trends Endpoint ───────────────────────────────────────────


class TestKPITrends:
    """Tests for /api/kpis/trends/{department}."""

    def test_trends_empty(self, setup_data: None) -> None:
        resp = client.get("/api/v1/kpis/trends/engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_trends_with_two_snapshots(self, setup_data: None) -> None:
        client.get("/api/v1/kpis/collect")
        client.get("/api/v1/kpis/collect")

        resp = client.get("/api/v1/kpis/trends/engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        assert "direction" in data[0]
        assert data[0]["direction"] in ("up", "down", "flat")

    def test_trends_filter_kpi_keys(self, setup_data: None) -> None:
        client.get("/api/v1/kpis/collect")
        client.get("/api/v1/kpis/collect")

        resp = client.get("/api/v1/kpis/trends/engineering?kpi_keys=total_tasks")
        assert resp.status_code == 200
        data = resp.json()
        for t in data:
            assert t["kpi_key"] == "total_tasks"


# ── KPI Alerts Endpoint ───────────────────────────────────────────


class TestKPIAlerts:
    """Tests for /api/kpis/alerts."""

    def test_alerts_returns_structure(self, setup_data: None) -> None:
        resp = client.get("/api/v1/kpis/alerts")
        assert resp.status_code == 200
        data = resp.json()
        assert "evaluated_at" in data
        assert "rules_evaluated" in data
        assert "alerts_fired" in data
        assert "alert_count" in data

    def test_alerts_default_rules_loaded(self, setup_data: None) -> None:
        resp = client.get("/api/v1/kpis/alerts")
        data = resp.json()
        assert data["rules_evaluated"] >= 5  # At least 5 default rules

    def test_alerts_store_snapshot(self, setup_data: None) -> None:
        # First collect + store
        client.get("/api/v1/kpis/collect")
        # Then alerts endpoint should also store
        resp = client.get("/api/v1/kpis/alerts")
        data = resp.json()
        assert "alert_count" in data


# ── KPI Collect Endpoint ──────────────────────────────────────────


class TestKPICollect:
    """Tests for /api/kpis/collect."""

    def test_collect_returns_all_departments(self, setup_data: None) -> None:
        resp = client.get("/api/v1/kpis/collect")
        assert resp.status_code == 200
        data = resp.json()
        assert "collected_at" in data
        assert "departments" in data
        depts = data["departments"]
        assert len(depts) == 8  # All 8 departments
        assert "engineering" in depts
        assert "hr" in depts
        assert "finance" in depts
        assert "marketing" in depts
        assert "sales" in depts
        assert "customer_success" in depts
        assert "legal" in depts
        assert "org_health" in depts

    def test_collect_stores_entries(self, setup_data: None) -> None:
        resp = client.get("/api/v1/kpis/collect")
        data = resp.json()
        assert "stored_entries" in data
        assert data["stored_entries"] > 0


# ── KPI Summary Stats Endpoint ────────────────────────────────────


class TestKPISummaryStats:
    """Tests for /api/kpis/summary-stats/{department}."""

    def test_summary_stats_empty(self, setup_data: None) -> None:
        resp = client.get("/api/v1/kpis/summary-stats/engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_summary_stats_after_collect(self, setup_data: None) -> None:
        client.get("/api/v1/kpis/collect")
        resp = client.get("/api/v1/kpis/summary-stats/engineering")
        assert resp.status_code == 200
        data = resp.json()
        if data:
            assert "min_value" in data[0]
            assert "max_value" in data[0]
            assert "mean_value" in data[0]
            assert "count" in data[0]

    def test_summary_stats_invalid_period(self, setup_data: None) -> None:
        resp = client.get("/api/v1/kpis/summary-stats/engineering?period=yearly")
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


# ── Org Chart ───────────────────────────────────────────────────────


class TestOrgChart:
    """Tests for the org chart feature."""

    def test_org_chart_api_returns_tree(self, setup_data: None) -> None:
        """Org chart API returns hierarchical tree data."""
        resp = client.get("/api/v1/org-chart")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_org_chart_api_has_required_fields(self, setup_data: None) -> None:
        """Org chart nodes have required fields."""
        resp = client.get("/api/v1/org-chart")
        data = resp.json()
        node = data[0]
        assert "name" in node
        assert "role" in node
        assert "type" in node
        assert "department" in node
        assert "children" in node

    def test_org_chart_page_renders(self, setup_data: None) -> None:
        """Org chart page renders successfully."""
        resp = client.get("/org-chart")
        assert resp.status_code == 200
        assert "Organization Chart" in resp.text

    def test_agent_reassignment(self, setup_data: None) -> None:
        """Agent can be reassigned to a different manager."""
        # Reassign lead-engineering to report to lead-marketing
        resp = client.patch(
            "/api/v1/agents/lead-engineering/reports-to",
            json={"reports_to": "lead-marketing"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert data["agent"] == "lead-engineering"
        assert data["reports_to"] == "lead-marketing"

    def test_agent_reassignment_updates_registry(self, setup_data: None) -> None:
        """Agent reassignment persists to the registry."""
        # Reassign
        client.patch(
            "/api/v1/agents/lead-engineering/reports-to",
            json={"reports_to": "lead-marketing"},
        )
        # Verify via API
        resp = client.get("/api/v1/agents/lead-engineering")
        assert resp.status_code == 200
        agent = resp.json()
        assert agent["reports_to"] == "lead-marketing"

    def test_agent_reassignment_org_chart_updates(self, setup_data: None) -> None:
        """Org chart reflects reassignment."""
        # Reassign
        client.patch(
            "/api/v1/agents/lead-engineering/reports-to",
            json={"reports_to": "lead-marketing"},
        )
        # Check org chart
        resp = client.get("/api/v1/org-chart")
        data = resp.json()
        # Find lead-marketing in the tree

        def find_agent(nodes: list) -> bool:
            for node in nodes:
                if node["name"] == "lead-marketing":
                    child_names = [c["name"] for c in node.get("children", [])]
                    return "lead-engineering" in child_names
                if node.get("children") and find_agent(node["children"]):
                    return True
            return False

        assert find_agent(data)

    def test_agent_reassignment_missing_reports_to(self, setup_data: None) -> None:
        """Agent reassignment fails without reports_to field."""
        resp = client.patch(
            "/api/v1/agents/lead-engineering/reports-to",
            json={},
        )
        assert resp.status_code == 400

    def test_agent_reassignment_not_found(self, setup_data: None) -> None:
        """Agent reassignment fails for non-existent agent."""
        resp = client.patch(
            "/api/v1/agents/nonexistent/reports-to",
            json={"reports_to": "chief-of-staff"},
        )
        assert resp.status_code == 404


# ── CEO Dashboard Hero ───────────────────────────────────────────


class TestCEOHero:
    """Tests for the CEO Dashboard Hero section."""

    def test_org_health_endpoint_returns_score(self, setup_data: None) -> None:
        """Org health endpoint returns score, band, and components."""
        resp = client.get("/api/v1/org-health")
        assert resp.status_code == 200
        data = resp.json()
        assert "score" in data
        assert "band" in data
        assert "components" in data
        assert isinstance(data["components"], list)
        assert data["band"] in ("green", "amber", "red")

    def test_org_health_score_range(self, setup_data: None) -> None:
        """Score must be between 0 and 100."""
        resp = client.get("/api/v1/org-health")
        data = resp.json()
        assert 0 <= data["score"] <= 100

    def test_org_health_components_have_values(self, setup_data: None) -> None:
        """Each component has a name and a value (numeric or None when no data)."""
        resp = client.get("/api/v1/org-health")
        data = resp.json()
        for comp in data["components"]:
            assert "name" in comp
            assert "value" in comp
            # Value is either a numeric score (0-100) or None (no data available)
            if comp["value"] is not None:
                assert isinstance(comp["value"], (int, float))
                assert 0 <= comp["value"] <= 100

    def test_org_health_with_trend_limit(self, setup_data: None) -> None:
        """Trend limit parameter is respected."""
        resp = client.get("/api/v1/org-health?trend_limit=10")
        assert resp.status_code == 200
        data = resp.json()
        assert "trend" in data
        assert isinstance(data["trend"], list)

    def test_org_health_without_components(self, setup_data: None) -> None:
        """Component detail can be excluded."""
        resp = client.get("/api/v1/org-health?component_detail=false")
        assert resp.status_code == 200
        data = resp.json()
        # When component_detail=false, components should not be included
        # or should be empty
        if "components" in data:
            assert len(data["components"]) == 0 or data["components"] is None


# ── Onboarding Studio ─────────────────────────────────────────────


class TestOnboardingStudio:
    """Tests for the Onboarding Studio UI and API endpoints."""

    def test_onboarding_page_renders(self, setup_data: None) -> None:
        """GET /onboarding returns 200 with onboarding template content."""
        resp = client.get("/onboarding")
        assert resp.status_code == 200
        html = resp.text
        assert "Agent Onboarding Studio" in html
        assert "onboardingStudio()" in html
        assert "onboarding.js" in html

    def test_onboarding_page_has_tab(self, setup_data: None) -> None:
        """Onboarding tab appears in navigation."""
        resp = client.get("/onboarding")
        assert resp.status_code == 200
        html = resp.text
        assert "Onboarding" in html
        assert "/onboarding" in html

    def test_onboarding_api_returns_list(self, setup_data: None) -> None:
        """GET /api/v1/onboarding returns a list (empty when no requests)."""
        resp = client.get("/api/v1/onboarding")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_onboarding_api_get_by_id_not_found(self, setup_data: None) -> None:
        """GET /api/v1/onboarding/{id} returns 404 for unknown request."""
        resp = client.get("/api/v1/onboarding/onb-nonexistent")
        assert resp.status_code == 404

    def test_onboarding_approve_not_found(self, setup_data: None) -> None:
        """POST /api/v1/onboarding/{id}/approve returns 400 for unknown request."""
        resp = client.post("/api/v1/onboarding/onb-nonexistent/approve")
        assert resp.status_code == 400

    def test_onboarding_reject_not_found(self, setup_data: None) -> None:
        """POST /api/v1/onboarding/{id}/reject returns 400 for unknown request."""
        resp = client.post(
            "/api/v1/onboarding/onb-nonexistent/reject",
            json={"reason": "test"},
        )
        assert resp.status_code == 400

    def test_onboarding_reject_without_body(self, setup_data: None) -> None:
        """POST /api/v1/onboarding/{id}/reject works without a body."""
        resp = client.post("/api/v1/onboarding/onb-nonexistent/reject")
        # Should still return 400 (not found), not 422 (validation error)
        assert resp.status_code == 400


# ── Task Decomposition ─────────────────────────────────────────────


class TestTaskDecomposition:
    """Tests for task decomposition endpoints (Kanban Decomposition feature #44)."""

    def _create_task(self) -> str:
        """Helper to create a task and return its ID."""
        resp = client.post(
            "/api/v1/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Implement API endpoint"},
        )
        assert resp.status_code == 201
        return resp.json()["id"]

    def test_get_subtasks_returns_empty_for_new_task(self, setup_data: None) -> None:
        """GET /api/v1/tasks/{id}/subtasks returns empty decomposition for a new task."""
        task_id = self._create_task()
        resp = client.get(f"/api/v1/tasks/{task_id}/subtasks")
        assert resp.status_code == 200
        data = resp.json()
        assert data["parent_id"] == task_id
        assert data["subtasks"] == []
        assert data["progress_pct"] == 0.0

    def test_get_subtasks_returns_404_for_unknown_task(self, setup_data: None) -> None:
        """GET /api/v1/tasks/{id}/subtasks returns 404 for unknown task."""
        resp = client.get("/api/v1/tasks/nonexistent-id/subtasks")
        assert resp.status_code == 404

    def test_decompose_task_returns_subtasks(self, setup_data: None) -> None:
        """POST /api/v1/tasks/{id}/decompose returns subtasks for an API task."""
        task_id = self._create_task()
        resp = client.post(f"/api/v1/tasks/{task_id}/decompose")
        assert resp.status_code == 200
        data = resp.json()
        assert data["parent_id"] == task_id
        assert len(data["subtasks"]) > 0
        assert data["progress_pct"] >= 0.0
        # Each subtask has required fields
        for subtask in data["subtasks"]:
            assert "id" in subtask
            assert "instruction" in subtask
            assert "status" in subtask
            assert subtask["status"] in ("pending", "in_progress", "completed")

    def test_decompose_task_returns_404_for_unknown_task(self, setup_data: None) -> None:
        """POST /api/v1/tasks/{id}/decompose returns 404 for unknown task."""
        resp = client.post("/api/v1/tasks/nonexistent-id/decompose")
        assert resp.status_code == 404

    def test_decompose_task_api_pattern(self, setup_data: None) -> None:
        """Task with 'api' in instruction decomposes into API-related subtasks."""
        resp = client.post(
            "/api/v1/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Build REST API endpoint"},
        )
        task_id = resp.json()["id"]
        resp = client.post(f"/api/v1/tasks/{task_id}/decompose")
        data = resp.json()
        # Should have subtasks related to API work
        instructions = [s["instruction"].lower() for s in data["subtasks"]]
        assert any("api" in i or "endpoint" in i or "route" in i for i in instructions)

    def test_decompose_task_test_pattern(self, setup_data: None) -> None:
        """Task with 'test' in instruction decomposes into testing subtasks."""
        resp = client.post(
            "/api/v1/tasks",
            json={
                "receiver_id": "lead-engineering",
                "instruction": "Write unit tests for the module",
            },
        )
        task_id = resp.json()["id"]
        resp = client.post(f"/api/v1/tasks/{task_id}/decompose")
        data = resp.json()
        instructions = [s["instruction"].lower() for s in data["subtasks"]]
        assert any("test" in i for i in instructions)

    def test_decompose_task_fix_pattern(self, setup_data: None) -> None:
        """Task with 'fix' in instruction decomposes into bug-fix subtasks."""
        resp = client.post(
            "/api/v1/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "Fix the login bug"},
        )
        task_id = resp.json()["id"]
        resp = client.post(f"/api/v1/tasks/{task_id}/decompose")
        data = resp.json()
        instructions = [s["instruction"].lower() for s in data["subtasks"]]
        assert any("reproduce" in i or "root cause" in i or "fix" in i for i in instructions)

    def test_decompose_task_persists_decomposition(self, setup_data: None) -> None:
        """After decomposition, GET /subtasks returns the stored decomposition."""
        task_id = self._create_task()
        # Decompose
        resp = client.post(f"/api/v1/tasks/{task_id}/decompose")
        assert resp.status_code == 200
        decomposed_data = resp.json()

        # Verify it's persisted
        resp = client.get(f"/api/v1/tasks/{task_id}/subtasks")
        assert resp.status_code == 200
        fetched_data = resp.json()
        assert len(fetched_data["subtasks"]) == len(decomposed_data["subtasks"])
        assert fetched_data["progress_pct"] == decomposed_data["progress_pct"]

    def test_decompose_progress_calculation(self, setup_data: None) -> None:
        """Progress percentage is correctly calculated from subtask statuses."""
        task_id = self._create_task()
        resp = client.post(f"/api/v1/tasks/{task_id}/decompose")
        data = resp.json()
        completed = sum(1 for s in data["subtasks"] if s["status"] == "completed")
        total = len(data["subtasks"])
        expected_pct = round((completed / total * 100), 1) if total > 0 else 0.0
        assert data["progress_pct"] == expected_pct

    def test_tasks_page_includes_decomposition(self, setup_data: None) -> None:
        """The tasks page HTML includes the slide-out panel elements."""
        resp = client.get("/tasks")
        assert resp.status_code == 200
        html = resp.text
        # Check for slide-out panel elements
        assert "taskDetailOpen" in html
        assert "openTaskDetail" in html
        assert "closeTaskDetail" in html
        assert "decomposeTask" in html
        assert "Decomposition" in html
        assert "taskDecomposing" in html


# ── Health Monitor ───────────────────────────────────────────────


class TestHealthMonitor:
    """Tests for the Health Monitor feature (Issue #45)."""

    def test_org_health_trend_endpoint(self, setup_data: None) -> None:
        """GET /api/v1/org-health/trend returns a list."""
        resp = client.get("/api/v1/org-health/trend")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_org_health_trend_with_limit(self, setup_data: None) -> None:
        """Trend endpoint respects the limit parameter."""
        resp = client.get("/api/v1/org-health/trend?limit=10")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        # Each entry should have timestamp and score
        for entry in data:
            assert "timestamp" in entry
            assert "score" in entry

    def test_org_health_anomalies_endpoint(self, setup_data: None) -> None:
        """GET /api/v1/org-health/anomalies returns a list."""
        resp = client.get("/api/v1/org-health/anomalies")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_org_health_anomalies_structure(self, setup_data: None) -> None:
        """Anomaly entries have the required fields when present."""
        resp = client.get("/api/v1/org-health/anomalies")
        data = resp.json()
        # With no history, anomalies should be empty
        assert len(data) == 0

    def test_kpis_page_includes_health_monitor(self, setup_data: None) -> None:
        """The KPIs page includes the Health Monitor section."""
        resp = client.get("/kpis")
        assert resp.status_code == 200
        html = resp.text
        assert "System Health Monitor" in html
        assert "healthMonitor()" in html
        assert "health-trend-chart" in html
        assert "health.js" in html

    def test_anomaly_detection_with_history(self, setup_data: None) -> None:
        """Anomaly detection works with historical data."""
        from ai_company.dashboard.org_health import OrgHealthCalculator

        calculator = OrgHealthCalculator()

        # Create synthetic history with small natural variation around 80
        history = []
        base_values = [79.0, 81.0, 80.5, 79.5, 80.0, 80.2, 79.8, 80.1, 79.9, 80.3]
        for i, val in enumerate(base_values):
            history.append(
                {
                    "timestamp": f"2025-01-01T{i:02d}:00:00",
                    "components": [
                        {"name": "task_success_rate", "value": val},
                        {"name": "agent_utilization", "value": 60.0 + (i % 3) * 0.5},
                    ],
                }
            )

        # Add a spike entry — dramatic drop well beyond normal variance
        history.append(
            {
                "timestamp": "2025-01-01T10:00:00",
                "components": [
                    {"name": "task_success_rate", "value": 20.0},  # Big drop
                    {"name": "agent_utilization", "value": 61.0},
                ],
            }
        )

        anomalies = calculator.detect_anomalies(history, threshold=2.0)

        # Should detect the task_success_rate anomaly
        assert len(anomalies) >= 1
        ts_anomaly = next(a for a in anomalies if a.component == "task_success_rate")
        assert ts_anomaly.severity in ("warning", "critical")
        assert ts_anomaly.previous_value == 80.3
        assert ts_anomaly.current_value == 20.0
        assert "drop" in ts_anomaly.message.lower()

    def test_anomaly_detection_no_anomalies(self, setup_data: None) -> None:
        """No anomalies detected when values are stable."""
        from ai_company.dashboard.org_health import OrgHealthCalculator

        calculator = OrgHealthCalculator()

        # Create synthetic history with small, stable variation
        history = []
        for i in range(10):
            history.append(
                {
                    "timestamp": f"2025-01-01T{i:02d}:00:00",
                    "components": [
                        {"name": "task_success_rate", "value": 80.0 + (i % 3) * 0.5},
                    ],
                }
            )
        # Last value also within normal range
        history.append(
            {
                "timestamp": "2025-01-01T10:00:00",
                "components": [
                    {"name": "task_success_rate", "value": 80.2},
                ],
            }
        )

        anomalies = calculator.detect_anomalies(history, threshold=2.0)
        assert len(anomalies) == 0

    def test_anomaly_detection_insufficient_data(self, setup_data: None) -> None:
        """No anomalies detected with fewer than 3 data points."""
        from ai_company.dashboard.org_health import OrgHealthCalculator

        calculator = OrgHealthCalculator()

        history = [
            {
                "timestamp": "2025-01-01T00:00:00",
                "components": [{"name": "task_success_rate", "value": 80.0}],
            },
            {
                "timestamp": "2025-01-01T01:00:00",
                "components": [{"name": "task_success_rate", "value": 20.0}],
            },
        ]

        anomalies = calculator.detect_anomalies(history, threshold=2.0)
        assert len(anomalies) == 0

    def test_anomaly_to_dict(self, setup_data: None) -> None:
        """Anomaly dataclass serializes to dict correctly."""
        from ai_company.dashboard.org_health import Anomaly

        anomaly = Anomaly(
            timestamp="2025-01-01T00:00:00",
            component="task_success_rate",
            previous_value=80.0,
            current_value=20.0,
            change_pct=-75.0,
            severity="critical",
            message="Task Success Rate drop: 80% → 20% (-75.0%)",
        )

        d = anomaly.to_dict()
        assert d["component"] == "task_success_rate"
        assert d["severity"] == "critical"
        assert d["previous_value"] == 80.0
        assert d["current_value"] == 20.0
        assert d["change_pct"] == -75.0
