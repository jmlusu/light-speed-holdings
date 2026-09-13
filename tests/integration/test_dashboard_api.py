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
    # Force the shared bus and StateStore to be rebuilt against the isolated
    # workspace so reads are rooted at tmp_path, not the real repo.
    from ai_company.dashboard import api as dash_api
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    dash_api._bus = None
    reset_state_store()
    get_state_store(workspace)
    return TestClient(app, raise_server_exceptions=False)


class TestDashboardAPI:
    def test_list_agents_shape(self, client: TestClient) -> None:
        resp = client.get("/api/v1/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 3
        assert {"name", "role", "type"} <= set(data[0].keys())

    def test_get_agent_by_name(self, client: TestClient) -> None:
        resp = client.get("/api/v1/agents/test-agent")
        assert resp.status_code == 200
        assert resp.json()["name"] == "test-agent"

    def test_get_agent_not_found(self, client: TestClient) -> None:
        resp = client.get("/api/v1/agents/does-not-exist")
        assert resp.status_code == 404

    def test_org_chart_shape(self, client: TestClient) -> None:
        resp = client.get("/api/v1/org-chart")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        # chief-of-staff is the root (reports to human-ceo).
        assert data[0]["name"] == "chief-of-staff"
        assert "children" in data[0]

    def test_create_task_persists(self, client: TestClient, workspace: Path) -> None:
        resp = client.post(
            "/api/v1/tasks",
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
        client.post(
            "/api/v1/tasks",
            json={
                "receiver_id": "test-agent",
                "instruction": "Deploy the new widget to production",
            },
        )
        resp = client.get("/api/v1/tasks")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_dashboard_kpis_shape(self, client: TestClient) -> None:
        resp = client.get("/api/v1/dashboard")
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
        resp = client.get("/api/v1/ceo-dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert "task_pipeline" in data
        assert "agent_performance" in data
        assert data["agent_performance"]["total_agents"] == 3

    def test_metrics_endpoint_text(self, client: TestClient) -> None:
        resp = client.get("/metrics")
        assert resp.status_code == 200
        body = resp.text
        assert "ai_company_llm_requests_total" in body
        assert "ai_company_tasks_by_status" in body

    def test_backlog_endpoint_shape(self, client: TestClient) -> None:
        resp = client.get("/api/v1/backlog")
        assert resp.status_code == 200
        data = resp.json()
        expected = {
            "total",
            "by_status",
            "pending",
            "in_progress",
            "completed",
            "failed",
            "oldest_pending_age_s",
            "stale_pending_count",
            "dead_letter_count",
            "inbox_path",
        }
        assert expected <= set(data.keys())

    def test_backlog_page_route(self, client: TestClient) -> None:
        resp = client.get("/backlog")
        assert resp.status_code == 200
        assert "Task Backlog" in resp.text

    # ── C4: Reports page / API ─────────────────────────────────
    def _write_report(self, workspace: Path, rel: str, doc: dict) -> None:
        p = workspace / "results" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(__import__("json").dumps(doc), encoding="utf-8")

    def test_reports_page_route(self, client: TestClient) -> None:
        resp = client.get("/reports")
        assert resp.status_code == 200
        assert "Agent Reports" in resp.text

    def test_reports_api_lists_bundle(self, client: TestClient, workspace: Path) -> None:
        self._write_report(
            workspace,
            "demo/loop_result.json",
            {"name": "demo-run", "timestamp": "2026-08-14T10:00:00Z", "done": True},
        )
        resp = client.get("/api/v1/reports")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        rep = data["reports"][0]
        assert rep["name"] == "demo-run"
        assert rep["bundle"] == "demo"
        assert rep["done"] is True

    def test_reports_api_excludes_cost_shard_by_default(
        self, client: TestClient, workspace: Path
    ) -> None:
        self._write_report(
            workspace,
            "cost_log.jsonl",
            {"total_cost": 12.3, "timestamp": "2026-08-14T10:00:00Z"},
        )
        resp = client.get("/api/v1/reports")
        assert resp.json()["total"] == 0
        resp_cost = client.get("/api/v1/reports?include_cost=true")
        assert resp_cost.json()["total"] == 1

    def test_report_content_endpoint(self, client: TestClient, workspace: Path) -> None:
        self._write_report(
            workspace,
            "demo/loop_result.json",
            {"name": "demo-run", "detail": "payload"},
        )
        resp = client.get("/api/v1/reports/content?path=demo/loop_result.json")
        assert resp.status_code == 200
        data = resp.json()
        assert data["documents"][0]["detail"] == "payload"

    def test_report_content_rejects_traversal(self, client: TestClient, workspace: Path) -> None:
        resp = client.get("/api/v1/reports/content?path=../inbox.json")
        assert resp.status_code == 404

    # ── C4: Task Flow page / API ───────────────────────────────
    def test_task_flow_page_route(self, client: TestClient) -> None:
        resp = client.get("/task-flow")
        assert resp.status_code == 200
        assert "Task Flow" in resp.text

    def test_task_flow_endpoint_shape(self, client: TestClient) -> None:
        created = client.post(
            "/api/v1/tasks",
            json={"receiver_id": "test-agent", "instruction": "Trace this task"},
        ).json()
        tid = created["id"]
        resp = client.get(f"/api/v1/tasks/{tid}/flow")
        assert resp.status_code == 200
        data = resp.json()
        assert data["task_id"] == tid
        assert data["task"]["id"] == tid
        assert data["current_status"] == "pending"
        assert "timeline" in data
        assert "status_events" in data

    def test_task_flow_not_found(self, client: TestClient) -> None:
        resp = client.get("/api/v1/tasks/does-not-exist/flow")
        assert resp.status_code == 404
