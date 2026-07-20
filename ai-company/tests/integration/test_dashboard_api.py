"""Integration test: dashboard REST API via FastAPI TestClient.

No real WebSocket broadcast is required; endpoints are exercised with a
TestClient pointed at the isolated workspace.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app


@pytest.fixture()
def client(workspace: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """TestClient bound to a fresh app instance over the isolated workspace."""
    # Force the shared bus to be rebuilt against the isolated inbox.
    from ai_company.dashboard import api as dash_api

    dash_api._bus = None
    return TestClient(app, raise_server_exceptions=False)


class TestDashboardAPI:
    def test_list_agents_shape(self, client: TestClient) -> None:
        resp = client.get("/api/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 3
        assert {"name", "role", "type"} <= set(data[0].keys())

    def test_get_agent_by_name(self, client: TestClient) -> None:
        resp = client.get("/api/agents/test-agent")
        assert resp.status_code == 200
        assert resp.json()["name"] == "test-agent"

    def test_get_agent_not_found(self, client: TestClient) -> None:
        resp = client.get("/api/agents/does-not-exist")
        assert resp.status_code == 404

    def test_org_chart_shape(self, client: TestClient) -> None:
        resp = client.get("/api/org-chart")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        # chief-of-staff is the root (reports to human-ceo).
        assert data[0]["name"] == "chief-of-staff"
        assert "children" in data[0]

    def test_create_task_persists(self, client: TestClient, workspace: Path) -> None:
        resp = client.post(
            "/api/tasks",
            json={"receiver_id": "test-agent", "instruction": "Build a widget"},
        )
        assert resp.status_code == 201
        task = resp.json()
        assert task["receiver_id"] == "test-agent"
        assert task["status"] == "pending"

        # The task should now appear in the inbox (via MessageBus).
        inbox = (workspace / ".opencode" / "inbox.json").read_text(encoding="utf-8")
        assert "Build a widget" in inbox

    def test_list_tasks_after_create(self, client: TestClient) -> None:
        client.post("/api/tasks", json={"receiver_id": "test-agent", "instruction": "X"})
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_dashboard_kpis_shape(self, client: TestClient) -> None:
        resp = client.get("/api/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        expected = {
            "pending_tasks",
            "in_progress_tasks",
            "completed_tasks",
            "failed_tasks",
            "total_agents",
        }
        assert expected <= set(data.keys())

    def test_ceo_dashboard_sections(self, client: TestClient) -> None:
        resp = client.get("/api/ceo-dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert "task_pipeline" in data
        assert "agent_performance" in data
        assert data["agent_performance"]["total_agents"] == 3

    def test_metrics_endpoint_text(self, client: TestClient) -> None:
        resp = client.get("/api/metrics")
        assert resp.status_code == 200
        body = resp.text
        assert "ai_company_tasks_total" in body
        assert "ai_company_agents_total" in body
