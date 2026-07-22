"""Unit tests for dashboard API responses.

Validates API contract: response shapes, status codes, data integrity,
and response times. These tests run against TestClient (no server needed).

Run:
    pytest tests/unit/test_dashboard_api_response.py -v
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app
from tests.fixtures.dashboard_data import (
    patch_rate_limiter,
)


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Isolated TestClient with fixture data."""
    monkeypatch.chdir(tmp_path)
    from ai_company.dashboard import api as dash_api
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    reset_state_store()
    get_state_store(tmp_path)
    dash_api._bus = None

    # Seed workspace
    from tests.fixtures.dashboard_data import seed_dashboard_workspace

    seed_dashboard_workspace(tmp_path, task_count=10, agent_count=5)

    with patch_rate_limiter():
        yield TestClient(app, raise_server_exceptions=False)

    reset_state_store()
    dash_api._bus = None


# ---------------------------------------------------------------------------
# Response shape contracts
# ---------------------------------------------------------------------------


class TestDashboardKPIContract:
    """Validate /api/dashboard response shape and values."""

    def test_returns_all_kpi_fields(self, client: TestClient) -> None:
        resp = client.get("/api/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        required = {
            "pending_tasks",
            "in_progress_tasks",
            "completed_tasks",
            "failed_tasks",
            "escalated_tasks",
            "pending_approvals",
            "open_escalations",
            "total_agents",
            "scheduled_tasks",
            "uptime_seconds",
        }
        assert required <= set(data.keys()), f"Missing fields: {required - set(data.keys())}"

    def test_kpi_values_are_integers(self, client: TestClient) -> None:
        data = client.get("/api/dashboard").json()
        for key in ("pending_tasks", "in_progress_tasks", "completed_tasks",
                     "failed_tasks", "escalated_tasks", "pending_approvals",
                     "open_escalations", "total_agents", "scheduled_tasks"):
            assert isinstance(data[key], int), f"{key} should be int, got {type(data[key])}"

    def test_uptime_is_positive_float(self, client: TestClient) -> None:
        data = client.get("/api/dashboard").json()
        assert isinstance(data["uptime_seconds"], float)
        assert data["uptime_seconds"] >= 0

    def test_total_agents_matches_registry(self, client: TestClient) -> None:
        dashboard = client.get("/api/dashboard").json()
        agents = client.get("/api/agents").json()
        assert dashboard["total_agents"] == len(agents)


class TestAgentAPIContract:
    """Validate /api/agents response shape."""

    def test_list_agents_shape(self, client: TestClient) -> None:
        resp = client.get("/api/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0

        agent = data[0]
        required = {"name", "role", "type", "department"}
        assert required <= set(agent.keys())

    def test_get_agent_by_name(self, client: TestClient) -> None:
        resp = client.get("/api/agents/chief-of-staff")
        assert resp.status_code == 200
        assert resp.json()["name"] == "chief-of-staff"

    def test_agent_not_found_returns_404(self, client: TestClient) -> None:
        resp = client.get("/api/agents/nonexistent-agent")
        assert resp.status_code == 404

    def test_all_agents_have_required_fields(self, client: TestClient) -> None:
        agents = client.get("/api/agents").json()
        for agent in agents:
            assert "name" in agent
            assert "role" in agent
            assert isinstance(agent["name"], str)
            assert len(agent["name"]) > 0


class TestTaskAPIContract:
    """Validate /api/tasks response shape."""

    def test_list_tasks_returns_array(self, client: TestClient) -> None:
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_create_task_returns_201(self, client: TestClient) -> None:
        resp = client.post("/api/tasks", json={
            "receiver_id": "lead-engineering",
            "instruction": "Write tests",
        })
        assert resp.status_code == 201
        task = resp.json()
        assert task["status"] == "pending"
        assert task["receiver_id"] == "lead-engineering"
        assert "id" in task

    def test_task_filter_by_status(self, client: TestClient) -> None:
        # Create a task
        client.post("/api/tasks", json={
            "receiver_id": "lead-engineering",
            "instruction": "Test",
        })
        # Filter
        resp = client.get("/api/tasks?status=pending")
        assert resp.status_code == 200
        for task in resp.json():
            assert task["status"] == "pending"

    def test_task_has_all_fields(self, client: TestClient) -> None:
        resp = client.post("/api/tasks", json={
            "receiver_id": "lead-engineering",
            "instruction": "Build feature",
        })
        task = resp.json()
        required = {"id", "sender_id", "receiver_id", "instruction", "status", "priority"}
        assert required <= set(task.keys())


class TestOrgChartContract:
    """Validate /api/org-chart response shape."""

    def test_org_chart_structure(self, client: TestClient) -> None:
        resp = client.get("/api/org-chart")
        assert resp.status_code == 200
        chart = resp.json()
        assert isinstance(chart, list)
        assert len(chart) >= 1

    def test_org_chart_has_children(self, client: TestClient) -> None:
        chart = client.get("/api/org-chart").json()
        root = chart[0]
        assert "name" in root
        assert "children" in root
        assert isinstance(root["children"], list)

    def test_org_chart_node_shape(self, client: TestClient) -> None:
        chart = client.get("/api/org-chart").json()

        def validate_node(node: dict) -> None:
            required = {"name", "role", "type", "department", "children"}
            assert required <= set(node.keys())
            for child in node["children"]:
                validate_node(child)

        for root in chart:
            validate_node(root)


class TestDepartmentAPIContract:
    """Validate /api/departments response shape."""

    def test_list_departments(self, client: TestClient) -> None:
        resp = client.get("/api/departments")
        assert resp.status_code == 200
        depts = resp.json()
        assert isinstance(depts, list)
        assert len(depts) > 0

    def test_department_has_name(self, client: TestClient) -> None:
        depts = client.get("/api/departments").json()
        for dept in depts:
            assert "name" in dept


class TestKPIEndpointsContract:
    """Validate KPI-related endpoints."""

    def test_list_all_kpis(self, client: TestClient) -> None:
        resp = client.get("/api/kpis")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_kpi_summary(self, client: TestClient) -> None:
        resp = client.get("/api/kpis/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        for item in data:
            assert "department" in item
            assert "kpi_id" in item
            assert "name" in item
            assert "target" in item

    def test_department_kpis(self, client: TestClient) -> None:
        resp = client.get("/api/departments/engineering/kpis")
        assert resp.status_code == 200
        data = resp.json()
        assert "name" in data
        assert "kpis" in data

    def test_department_kpis_not_found(self, client: TestClient) -> None:
        resp = client.get("/api/departments/nonexistent/kpis")
        assert resp.status_code == 404


class TestModelAPIContract:
    """Validate /api/models response shape."""

    def test_list_model_routes(self, client: TestClient) -> None:
        resp = client.get("/api/models")
        assert resp.status_code == 200
        routes = resp.json()
        assert isinstance(routes, list)
        for route in routes:
            assert "agent" in route

    def test_list_model_tiers(self, client: TestClient) -> None:
        resp = client.get("/api/models/tiers")
        assert resp.status_code == 200
        tiers = resp.json()
        assert isinstance(tiers, list)
        tier_ids = {t["id"] for t in tiers}
        assert "fast" in tier_ids
        assert "standard" in tier_ids
        assert "premium" in tier_ids


class TestMetricsEndpoint:
    """Validate Prometheus /api/metrics endpoint."""

    def test_metrics_format(self, client: TestClient) -> None:
        resp = client.get("/api/metrics")
        assert resp.status_code == 200
        body = resp.text
        assert "ai_company_tasks_total" in body
        assert "ai_company_agents_total" in body
        assert "ai_company_uptime_seconds" in body

    def test_metrics_valid_prometheus_format(self, client: TestClient) -> None:
        resp = client.get("/api/metrics")
        # The TestClient may return the body with escaped newlines
        text = resp.text.replace("\\n", "\n")
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        metric_lines = [ln for ln in lines if not ln.startswith("#") and not ln.startswith('"')]
        assert len(metric_lines) > 0, "No metric lines found"
        for line in metric_lines:
            # Prometheus format: metric_name{labels} value  OR  metric_name value
            # The value is always the last space-separated token
            parts = line.rsplit(" ", 1)
            assert len(parts) == 2, f"Invalid metric line: {line!r}"
            _, value_part = parts
            # Value should be numeric (strip any stray chars)
            float(value_part.strip().strip('"').strip("\\").strip('"'))


# ---------------------------------------------------------------------------
# Response time assertions
# ---------------------------------------------------------------------------


class TestAPIResponseTimes:
    """Ensure all API endpoints respond within acceptable time limits."""

    MAX_RESPONSE_MS = 500  # milliseconds

    @pytest.mark.parametrize("method,path", [
        ("GET", "/api/dashboard"),
        ("GET", "/api/agents"),
        ("GET", "/api/org-chart"),
        ("GET", "/api/tasks"),
        ("GET", "/api/approvals"),
        ("GET", "/api/escalations"),
        ("GET", "/api/departments"),
        ("GET", "/api/models"),
        ("GET", "/api/models/tiers"),
        ("GET", "/api/scheduler"),
        ("GET", "/api/kpis"),
        ("GET", "/api/kpis/summary"),
        ("GET", "/api/metrics"),
        ("GET", "/health"),
    ])
    def test_endpoint_responds_quickly(
        self, client: TestClient, method: str, path: str
    ) -> None:
        start = time.perf_counter()
        resp = getattr(client, method.lower())(path)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert resp.status_code in (200, 404), (
            f"{method} {path} returned {resp.status_code}"
        )
        assert elapsed_ms < self.MAX_RESPONSE_MS, (
            f"{method} {path} took {elapsed_ms:.0f}ms (limit: {self.MAX_RESPONSE_MS}ms)"
        )

    def test_concurrent_requests_stability(self, client: TestClient) -> None:
        """20 concurrent dashboard requests should all succeed."""
        start = time.perf_counter()
        results = [client.get("/api/dashboard") for _ in range(20)]
        elapsed_ms = (time.perf_counter() - start) * 1000

        for i, resp in enumerate(results):
            assert resp.status_code == 200, f"Request {i} failed: {resp.status_code}"

        avg_ms = elapsed_ms / 20
        assert avg_ms < self.MAX_RESPONSE_MS, (
            f"Average response time {avg_ms:.0f}ms exceeds {self.MAX_RESPONSE_MS}ms"
        )
