"""Sprint 4 T017 — CEO dashboard KPI endpoint contracts.

Covers:
- GET /api/v1/dashboard: CEO KPI snapshot shape and data completeness
- GET /api/v1/kpis/live: Live KPIs from 7 department collectors
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import create_app

from .conftest import provision_dashboard_data


@pytest.fixture()
def isolated(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Give every test a fresh app context: no API key, tmp data root + cwd."""
    monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
    monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    provision_dashboard_data(tmp_path)


class TestDashboardKPIs:
    def test_dashboard_snapshot_shape(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        # Core KPI fields
        assert "pending_tasks" in data
        assert "in_progress_tasks" in data
        assert "completed_tasks" in data
        assert "failed_tasks" in data
        assert "escalated_tasks" in data
        assert "pending_approvals" in data
        assert "open_escalations" in data
        assert "total_agents" in data
        assert "scheduled_tasks" in data
        assert "computed_at" in data
        # All values should be non-negative integers
        for key in (
            "pending_tasks",
            "in_progress_tasks",
            "completed_tasks",
            "failed_tasks",
            "escalated_tasks",
            "pending_approvals",
            "open_escalations",
            "total_agents",
            "scheduled_tasks",
        ):
            assert isinstance(data[key], int), f"{key} should be int, got {type(data[key])}"
        assert data["pending_tasks"] >= 0
        assert data["completed_tasks"] >= 0

    def test_live_kpis_live_endpoint(self, isolated: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/kpis/live")
        assert resp.status_code == 200
        data = resp.json()
        # Top-level contract: collected_at timestamp + departments dict keyed by id
        assert "collected_at" in data
        assert "departments" in data
        expected_departments = {
            "engineering",
            "hr",
            "finance",
            "marketing",
            "sales",
            "customer_success",
            "legal",
            "org_health",
        }
        # Each department collector output should be nested under departments
        for dept in expected_departments:
            assert dept in data["departments"], f"Department {dept} should be in live KPIs"
        # Each department entry exposes its kpis dict and its own id
        for dept in expected_departments:
            entry = data["departments"][dept]
            assert "kpis" in entry, f"{dept} should have kpis dict"
            assert entry.get("department") == dept, f"{dept} should report its own id"


class TestDashboardAgents:
    def test_list_agents_endpoint(self, isolated: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Agents should return a list"
        assert len(data) > 0, "Should have at least one agent"
        # Validate each agent has required fields
        for agent in data:
            assert "name" in agent, "Agent should have name field"
            assert "department" in agent, "Agent should have department field"
            assert "role" in agent, "Agent should have role field"
            assert "type" in agent, "Agent should have type field"

    def test_get_agent_by_name(self, isolated: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        # List agents first to get a valid name
        resp = client.get("/api/v1/agents")
        assert resp.status_code == 200
        agents = resp.json()
        assert len(agents) > 0
        agent_name = agents[0]["name"]
        # Get specific agent
        resp = client.get(f"/api/v1/agents/{agent_name}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == agent_name


class TestDashboardTasks:
    def test_list_tasks_endpoint(self, isolated: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/tasks")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Tasks should return a list"
        # Validate task items have required fields if present
        for task in data:
            # Task items should have at least an id and status
            assert "id" in task, "Task should have id field"
            assert "status" in task, "Task should have status field"

    def test_tasks_paginated_endpoint(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/tasks/paginated?page=1&page_size=10")
        assert resp.status_code == 200
        data = resp.json()
        # Validate PaginatedTasks shape
        assert "items" in data, "Should have items field"
        assert "total" in data, "Should have total field"
        assert "page" in data, "Should have page field"
        assert "page_size" in data, "Should have page_size field"
        assert "total_pages" in data, "Should have total_pages field"
        assert "counts_by_status" in data, "Should have counts_by_status field"
        # Validate items are task items
        for item in data["items"]:
            assert "id" in item, "Task item should have id"
            assert "status" in item, "Task item should have status"
