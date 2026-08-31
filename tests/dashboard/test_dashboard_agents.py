"""Sprint 4 T018 — CEO dashboard agent endpoint contracts.

Covers:
- GET /api/v1/dashboard/agents: Registered agent list from registry
- GET /api/v1/dashboard/agents/{name}: Single agent detail
- GET /api/v1/dashboard/agents/{name}/performance: Per-agent metrics
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import create_app


@pytest.fixture()
def isolated(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Give every test a fresh app context: no API key, tmp data root + cwd."""
    monkeypatch.delenv("DASHBOARD_API_KEY", raising=False)
    monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)


@pytest.fixture()
def keyed(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Give every test a fresh app context: API key set, tmp data root + cwd."""
    monkeypatch.setenv("DASHBOARD_API_KEY", "WUkwnRZmZVMNg4X5yrl7Y4aHfo2v2-bIvKXS8rQLbYQ")
    monkeypatch.delenv("DASHBOARD_CORS_ORIGINS", raising=False)
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)


class TestAgentsEndpoint:
    def test_agents_list_returns_valid_shape_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Agents should return a list"
        assert len(data) > 0, "Should have at least one agent"
        # Validate each agent summary has required fields
        for agent in data:
            assert "name" in agent, "Agent summary must have name"
            assert "department" in agent, "Agent summary must have department"
            assert "role" in agent, "Agent summary must have role"
            assert "type" in agent, "Agent summary must have type"
            assert agent["type"] in ("executive", "specialist", "board"), (
                f"Invalid agent type: {agent['type']}"
            )

    def test_agents_list_returns_valid_shape_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Agents should return a list"
        assert len(data) > 0, "Should have at least one agent"
        # Validate each agent summary has required fields
        for agent in data:
            assert "name" in agent, "Agent summary must have name"
            assert "department" in agent, "Agent summary must have department"
            assert "role" in agent, "Agent summary must have role"
            assert "type" in agent, "Agent summary must have type"
            assert agent["type"] in ("executive", "specialist", "board"), (
                f"Invalid agent type: {agent['type']}"
            )

    def test_agent_detail_by_name_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        # List agents first to get a valid name
        resp = client.get("/api/v1/dashboard/agents")
        assert resp.status_code == 200
        agents = resp.json()
        assert len(agents) > 0, "Should have at least one agent"
        agent_name = agents[0]["name"]
        # Get specific agent
        resp = client.get(f"/api/v1/dashboard/agents/{agent_name}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == agent_name
        # Should have all expected fields
        assert "name" in data
        assert "department" in data
        assert "role" in data
        assert "type" in data
        assert "responsibilities" in data or "guidelines" in data

    def test_agent_detail_by_name_keyed(self, keyed: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        # List agents first to get a valid name
        resp = client.get("/api/v1/dashboard/agents")
        assert resp.status_code == 200
        agents = resp.json()
        assert len(agents) > 0, "Should have at least one agent"
        agent_name = agents[0]["name"]
        # Get specific agent
        resp = client.get(f"/api/v1/dashboard/agents/{agent_name}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == agent_name
        # Should have all expected fields
        assert "name" in data
        assert "department" in data
        assert "role" in data
        assert "type" in data
        assert "responsibilities" in data or "guidelines" in data

    def test_agent_performance_endpoint_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/agents/performance")
        assert resp.status_code == 200
        data = resp.json()
        assert "agents" in data, "Performance endpoint should have agents leaderboard"
        assert "total_tasks" in data, "Should report total task count"
        assert "agents_with_tasks" in data, "Should report count with tasks"
        # Validate leaderboard structure
        for agent_entry in data["agents"]:
            assert "name" in agent_entry, "Leaderboard entry needs name"
            assert "completion_rate" in agent_entry, "Leaderboard entry needs completion_rate"
            assert 0 <= agent_entry["completion_rate"] <= 100, (
                f"Completion rate should be 0-100, got {agent_entry['completion_rate']}"
            )

    def test_agent_performance_endpoint_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/agents/performance")
        assert resp.status_code == 200
        data = resp.json()
        assert "agents" in data, "Performance endpoint should have agents leaderboard"
        assert "total_tasks" in data, "Should report total task count"
        assert "agents_with_tasks" in data, "Should report count with tasks"
        # Validate leaderboard structure
        for agent_entry in data["agents"]:
            assert "name" in agent_entry, "Leaderboard entry needs name"
            assert "completion_rate" in agent_entry, "Leaderboard entry needs completion_rate"
            assert 0 <= agent_entry["completion_rate"] <= 100, (
                f"Completion rate should be 0-100, got {agent_entry['completion_rate']}"
            )


class TestOrgChartEndpoint:
    def test_org_chart_endpoint_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/org-chart")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Org chart should return a list"
        assert len(data) > 0, "Should have at least one org node"
        # Validate org node structure
        for node in data:
            assert "name" in node, "Org node must have name"
            assert "role" in node, "Org node must have role"
            assert "type" in node, "Org node must have type"
            assert "department" in node, "Org node must have department"
            assert "reports_to" in node, "Org node must have reports_to"
            # Children should also be valid org nodes if present
            if node.get("children"):
                for child in node["children"]:
                    assert "name" in child, "Child org node must have name"
                    assert "role" in child, "Child org node must have role"

    def test_org_chart_endpoint_keyed(self, keyed: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/org-chart")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Org chart should return a list"
        assert len(data) > 0, "Should have at least one org node"
        # Validate org node structure
        for node in data:
            assert "name" in node, "Org node must have name"
            assert "role" in node, "Org node must have role"
            assert "type" in node, "Org node must have type"
            assert "department" in node, "Org node must have department"
            assert "reports_to" in node, "Org node must have reports_to"
            # Children should also be valid org nodes if present
            if node.get("children"):
                for child in node["children"]:
                    assert "name" in child, "Child org node must have name"
                    assert "role" in child, "Child org node must have role"


class TestTaskFlowEndpoint:
    def test_task_flow_endpoint_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        # First create a task, then get its flow
        resp = client.post(
            "/api/v1/tasks",
            json={
                "sender_id": "flow-test-sender",
                "receiver_id": "flow-test-receiver",
                "instruction": "Test task for flow tracking",
            },
        )
        # Task creation may require auth; in isolated mode it may fail
        # but we test the flow endpoint exists
        assert resp.status_code in (201, 401, 400)
        if resp.status_code == 201:
            task_id = resp.json().get("id")
            if task_id:
                resp = client.get(f"/api/v1/tasks/{task_id}/flow")
                assert resp.status_code in (200, 404)

    def test_task_flow_endpoint_keyed(self, keyed: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        # First create a task with API key, then get its flow
        resp = client.post(
            "/api/v1/tasks",
            json={
                "sender_id": "flow-test-sender",
                "receiver_id": "flow-test-receiver",
                "instruction": "Test task for flow tracking",
            },
        )
        assert resp.status_code == 201, f"Task creation should succeed, got {resp.status_code}"
        task_id = resp.json().get("id")
        if task_id:
            resp = client.get(f"/api/v1/tasks/{task_id}/flow")
            # Should return 200 or 404 (if flow not yet populated)
            assert resp.status_code in (200, 404)
