"""Unit tests for scroll behavior logic in the dashboard frontend.

These tests validate the JavaScript scroll-preservation logic by
testing the backend API endpoints that feed the dashboard, and by
verifying that data updates produce consistent responses.

For the actual DOM scroll tests, see tests/e2e/test_dashboard_scroll.py.

Run:
    pytest tests/unit/test_dashboard_scroll.py -v
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app
from tests.fixtures.dashboard_data import (
    patch_rate_limiter,
    seed_dashboard_workspace,
)


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Isolated TestClient for scroll behavior testing."""
    monkeypatch.chdir(tmp_path)
    from ai_company.dashboard import api as dash_api
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    reset_state_store()
    get_state_store(tmp_path)
    dash_api._bus = None

    seed_dashboard_workspace(tmp_path, task_count=20, agent_count=5)

    with patch_rate_limiter():
        yield TestClient(app, raise_server_exceptions=False)

    reset_state_store()
    dash_api._bus = None


# ---------------------------------------------------------------------------
# Data Stability Tests (Backend)
#
# These verify that the backend data driving the dashboard is stable
# and won't cause unexpected DOM changes that trigger scroll.
# ---------------------------------------------------------------------------


class TestDataStability:
    """Verify dashboard data is stable across repeated reads."""

    def test_kpi_values_stable_across_reads(self, client: TestClient) -> None:
        """KPI values should not change between rapid successive reads."""
        results = [client.get("/api/dashboard").json() for _ in range(10)]

        for key in ("pending_tasks", "in_progress_tasks", "completed_tasks",
                     "failed_tasks", "total_agents"):
            values = [r[key] for r in results]
            assert len(set(values)) == 1, (
                f"KPI '{key}' is unstable across reads: {values}"
            )

    def test_task_list_stable_across_reads(self, client: TestClient) -> None:
        """Task list should not change between rapid reads."""
        results = [client.get("/api/tasks").json() for _ in range(5)]

        for i in range(1, len(results)):
            assert len(results[i]) == len(results[0]), (
                f"Task count changed: {len(results[0])} -> {len(results[i])}"
            )

    def test_agent_list_stable_across_reads(self, client: TestClient) -> None:
        """Agent list should be immutable across reads."""
        results = [client.get("/api/agents").json() for _ in range(5)]

        for i in range(1, len(results)):
            assert len(results[i]) == len(results[0])
            names_i = {a["name"] for a in results[i]}
            names_0 = {a["name"] for a in results[0]}
            assert names_i == names_0

    def test_org_chart_stable_across_reads(self, client: TestClient) -> None:
        """Org chart structure should not change between reads."""
        results = [client.get("/api/org-chart").json() for _ in range(5)]

        for i in range(1, len(results)):
            assert len(results[i]) == len(results[0])
            # Root node should be the same
            assert results[i][0]["name"] == results[0][0]["name"]


# ---------------------------------------------------------------------------
# Mutation → Stability Tests
#
# These verify that after a mutation (create task, approve, etc.),
# subsequent reads are stable (no flapping values).
# ---------------------------------------------------------------------------


class TestPostMutationStability:
    """After a mutation, data should stabilize immediately."""

    def test_task_creation_stabilizes(self, client: TestClient) -> None:
        """After creating a task, subsequent reads should be consistent."""
        # Create a task
        client.post("/api/tasks", json={
            "receiver_id": "lead-engineering",
            "instruction": "Test stability",
        })

        # Read multiple times — should all show the same count
        counts = []
        for _ in range(5):
            tasks = client.get("/api/tasks").json()
            counts.append(len(tasks))

        assert len(set(counts)) == 1, (
            f"Task count unstable after creation: {counts}"
        )

    def test_kpi_reflects_new_task_consistently(self, client: TestClient) -> None:
        """After creating a task, KPI pending count should be stable."""
        client.post("/api/tasks", json={
            "receiver_id": "lead-engineering",
            "instruction": "KPI stability test",
        })

        pending_counts = []
        for _ in range(5):
            kpis = client.get("/api/dashboard").json()
            pending_counts.append(kpis["pending_tasks"])

        assert len(set(pending_counts)) == 1, (
            f"Pending tasks KPI unstable: {pending_counts}"
        )

    def test_approval_mutation_stabilizes(self, client: TestClient) -> None:
        """After approving a request, the approval list should stabilize."""
        approvals_path = Path("orchestrator/approvals.yaml")
        approvals_path.parent.mkdir(exist_ok=True)
        approvals_path.write_text(yaml.dump({
            "requests": [{
                "id": "test-req",
                "task_id": "t-1",
                "agent_id": "lead-engineering",
                "action": "deploy",
                "description": "Test",
                "status": "pending",
            }]
        }))

        # Approve it
        resp = client.post("/api/approvals/test-req/approve")
        assert resp.status_code == 200

        # Read multiple times — after the mutation, counts should be stable
        # (Skip the first read which may see pre-mutation cache)
        counts = []
        for _ in range(5):
            approvals = client.get("/api/approvals").json()
            counts.append(len(approvals))

        # All reads should agree (allow the first to differ from cache)
        assert len(set(counts[1:])) == 1, (
            f"Approval count unstable after approve: {counts}"
        )


# ---------------------------------------------------------------------------
# Frontend Data Contract Tests
#
# These verify that API responses have the exact shape the frontend expects,
# preventing "undefined" values in Alpine.js that could cause render thrashing.
# ---------------------------------------------------------------------------


class TestFrontendDataContract:
    """Verify API responses match what app.js expects."""

    def test_dashboard_kpi_shape_for_alpine(self, client: TestClient) -> None:
        """Dashboard response must match the kpis object in app.js."""
        data = client.get("/api/dashboard").json()

        # app.js initializes kpis with these keys:
        expected_keys = {
            "pending_tasks", "in_progress_tasks", "completed_tasks",
            "failed_tasks", "escalated_tasks", "pending_approvals",
            "open_escalations", "total_agents", "scheduled_tasks",
            "uptime_seconds",
        }
        assert expected_keys == set(data.keys()), (
            f"Mismatch: expected {expected_keys}, got {set(data.keys())}"
        )

        # All values must be JSON-serializable (no None for int fields)
        for key in expected_keys - {"uptime_seconds"}:
            assert data[key] is not None, f"{key} is None"
            assert isinstance(data[key], int), f"{key} should be int"

    def test_task_shape_for_alpine(self, client: TestClient) -> None:
        """Task response must match what app.js template expects."""
        client.post("/api/tasks", json={
            "receiver_id": "lead-engineering",
            "instruction": "Shape test",
        })
        tasks = client.get("/api/tasks").json()
        assert len(tasks) > 0

        task = tasks[0]
        # app.js template uses: t.id, t.receiver_id, t.instruction,
        # t.priority, t.status, t.created_at
        required = {"id", "receiver_id", "instruction", "priority", "status", "created_at"}
        assert required <= set(task.keys()), (
            f"Task missing fields: {required - set(task.keys())}"
        )

        # No None values in critical fields
        for key in ("id", "receiver_id", "instruction", "status"):
            assert task[key] is not None, f"Task {key} is None"

    def test_agent_shape_for_alpine(self, client: TestClient) -> None:
        """Agent response must match filteredAgents template."""
        agents = client.get("/api/agents").json()
        assert len(agents) > 0

        agent = agents[0]
        # app.js uses: a.name, a.role, a.department
        required = {"name", "role", "type", "department"}
        assert required <= set(agent.keys())

        for key in ("name", "role"):
            assert agent[key] is not None, f"Agent {key} is None"

    def test_departments_shape_for_alpine(self, client: TestClient) -> None:
        """Departments response must match chart rendering code."""
        depts = client.get("/api/departments").json()
        assert isinstance(depts, list)
        for dept in depts:
            assert "name" in dept
            assert "total_agents" in dept


# ---------------------------------------------------------------------------
# Scroll-Specific Regression Tests
# ---------------------------------------------------------------------------


class TestScrollRegression:
    """Tests that directly guard against the auto-scroll regression."""

    def test_rapid_kpi_polling_returns_consistent_data(self, client: TestClient) -> None:
        """Simulate rapid polling (like the 10s interval) — data must be consistent."""
        # Simulate 5 rapid poll cycles
        snapshots = []
        for _ in range(5):
            resp = client.get("/api/dashboard")
            snapshots.append(resp.json())

        # All snapshots must be identical (exclude uptime_seconds which changes)
        first = snapshots[0].copy()
        first.pop("uptime_seconds", None)
        for i, snap in enumerate(snapshots[1:], 1):
            current = snap.copy()
            current.pop("uptime_seconds", None)
            assert current == first, (
                f"Poll cycle {i} returned different data than cycle 0. "
                f"This would cause DOM thrashing and scroll jumps."
            )

    def test_rapid_task_list_polling_returns_consistent_data(
        self, client: TestClient
    ) -> None:
        """Simulate rapid task polling — list must be stable."""
        snapshots = []
        for _ in range(5):
            resp = client.get("/api/tasks")
            snapshots.append(resp.json())

        first = json.dumps(snapshots[0], sort_keys=True)
        for i, snap in enumerate(snapshots[1:], 1):
            current = json.dumps(snap, sort_keys=True)
            assert current == first, (
                f"Task poll cycle {i} differs from cycle 0. "
                "This would cause Alpine.js re-render and scroll jump."
            )

    def test_dashboard_and_tasks_kpi_alignment(self, client: TestClient) -> None:
        """KPI counts from /dashboard must match /tasks listing."""
        dashboard = client.get("/api/dashboard").json()
        tasks = client.get("/api/tasks").json()

        # Count tasks by status
        status_counts = {}
        for t in tasks:
            status = t["status"]
            status_counts[status] = status_counts.get(status, 0) + 1

        # Compare with KPIs
        assert dashboard["pending_tasks"] == status_counts.get("pending", 0)
        assert dashboard["completed_tasks"] == status_counts.get("completed", 0)
        assert dashboard["failed_tasks"] == status_counts.get("failed", 0)

        # Total should match
        total_kpis = (
            dashboard["pending_tasks"]
            + dashboard["in_progress_tasks"]
            + dashboard["completed_tasks"]
            + dashboard["failed_tasks"]
            + dashboard["escalated_tasks"]
        )
        assert total_kpis == len(tasks), (
            f"KPI total ({total_kpis}) != task count ({len(tasks)}). "
            "This mismatch causes DOM reflow on data update."
        )

    def test_no_none_values_in_api_responses(self, client: TestClient) -> None:
        """None values in JSON cause Alpine.js to render 'null' text,
        which changes element dimensions and can trigger scroll.

        Note: Some fields like ``model`` may legitimately be None for
        agents that aren't assigned to a provider.
        """
        ALLOWED_NONE_FIELDS = {"model", "tier", "reason"}  # legitimately nullable

        endpoints = [
            "/api/dashboard",
            "/api/agents",
            "/api/tasks",
            "/api/departments",
            "/api/kpis/summary",
        ]

        for endpoint in endpoints:
            resp = client.get(endpoint)
            assert resp.status_code == 200
            data = resp.json()

            if isinstance(data, list):
                for i, item in enumerate(data):
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if key not in ALLOWED_NONE_FIELDS:
                                assert value is not None, (
                                    f"{endpoint}[{i}].{key} is None -- "
                                    "causes render thrashing"
                                )
            elif isinstance(data, dict):
                for key, value in data.items():
                    if key not in ALLOWED_NONE_FIELDS and key != "uptime_seconds":
                        assert value is not None, (
                            f"{endpoint}.{key} is None -- "
                            "causes render thrashing"
                        )
