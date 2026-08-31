"""Sprint 4 T019 — CEO dashboard task endpoint contracts.

Covers:
- GET /api/v1/dashboard/tasks: Task listing with filters
- GET /api/v1/dashboard/tasks/paginated: Paginated task listing
- POST /api/v1/tasks: Task creation (with API key)
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


class TestTasksListing:
    def test_tasks_list_basic_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Tasks should return a list"

    def test_tasks_list_basic_keyed(self, keyed: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Tasks should return a list"

    def test_tasks_list_with_status_filter_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks?status=completed")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Filtered tasks should return a list"
        # All returned tasks should have status=completed
        for task in data:
            assert task.get("status") == "completed", (
                f"Expected completed status, got {task.get('status')}"
            )

    def test_tasks_list_with_status_filter_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks?status=completed")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Filtered tasks should return a list"
        # All returned tasks should have status=completed
        for task in data:
            assert task.get("status") == "completed", (
                f"Expected completed status, got {task.get('status')}"
            )

    def test_tasks_list_with_agent_filter_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        # First get an agent name from the agents endpoint
        resp = client.get("/api/v1/dashboard/agents")
        assert resp.status_code == 200
        agents = resp.json()
        if len(agents) > 0:
            agent_name = agents[0]["name"]
            resp = client.get(f"/api/v1/dashboard/tasks?agent={agent_name}")
            assert resp.status_code == 200
            data = resp.json()
            assert isinstance(data, list), "Agent-filtered tasks should return a list"

    def test_tasks_list_with_agent_filter_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        # First get an agent name from the agents endpoint
        resp = client.get("/api/v1/dashboard/agents")
        assert resp.status_code == 200
        agents = resp.json()
        if len(agents) > 0:
            agent_name = agents[0]["name"]
            resp = client.get(f"/api/v1/dashboard/tasks?agent={agent_name}")
            assert resp.status_code == 200
            data = resp.json()
            assert isinstance(data, list), "Agent-filtered tasks should return a list"

    def test_tasks_list_empty_state_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that empty task list is handled gracefully."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks?status=completed&agent=nonexistent-agent")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Should return a list even when empty"
        assert len(data) == 0, "Should be empty with no matching tasks"

    def test_tasks_list_empty_state_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that empty task list is handled gracefully."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks?status=completed&agent=nonexistent-agent")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Should return a list even when empty"
        assert len(data) == 0, "Should be empty with no matching tasks"


class TestTasksPaginated:
    def test_paginated_tasks_return_shape_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks/paginated?page=1&page_size=10")
        assert resp.status_code == 200
        data = resp.json()
        # Validate PaginatedTasks shape
        assert "items" in data, "Should have items field"
        assert "total" in data, "Should have total field"
        assert "page" in data, "Should have page field"
        assert "page_size" in data, "Should have page_size field"
        assert "total_pages" in data, "Should have total_pages field"
        assert "counts_by_status" in data, "Should have counts_by_status field"
        # Items should be task dicts
        for item in data["items"]:
            assert "id" in item, "Task item should have id"
            assert "status" in item, "Task item should have status"

    def test_paginated_tasks_return_shape_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks/paginated?page=1&page_size=10")
        assert resp.status_code == 200
        data = resp.json()
        # Validate PaginatedTasks shape
        assert "items" in data, "Should have items field"
        assert "total" in data, "Should have total field"
        assert "page" in data, "Should have page field"
        assert "page_size" in data, "Should have page_size field"
        assert "total_pages" in data, "Should have total_pages field"
        assert "counts_by_status" in data, "Should have counts_by_status field"
        # Items should be task dicts
        for item in data["items"]:
            assert "id" in item, "Task item should have id"
            assert "status" in item, "Task item should have status"

    def test_pagination_consistency_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        # First page
        resp1 = client.get("/api/v1/dashboard/tasks/paginated?page=1&page_size=10")
        data1 = resp1.json()
        # Second page
        resp2 = client.get("/api/v1/dashboard/tasks/paginated?page=2&page_size=10")
        data2 = resp2.json()
        # total should be consistent
        assert data1["total"] == data2["total"], "Total should be consistent across pages"
        # total_pages should be consistent with total and page_size
        expected_pages = (data1["total"] + data1["page_size"] - 1) // data1["page_size"]
        assert data1["total_pages"] >= expected_pages, (
            f"total_pages {data1['total_pages']} should be >= {expected_pages}"
        )

    def test_pagination_consistency_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        # First page
        resp1 = client.get("/api/v1/dashboard/tasks/paginated?page=1&page_size=10")
        data1 = resp1.json()
        # Second page
        resp2 = client.get("/api/v1/dashboard/tasks/paginated?page=2&page_size=10")
        data2 = resp2.json()
        # total should be consistent
        assert data1["total"] == data2["total"], "Total should be consistent across pages"
        # total_pages should be consistent with total and page_size
        expected_pages = (data1["total"] + data1["page_size"] - 1) // data1["page_size"]
        assert data1["total_pages"] >= expected_pages, (
            f"total_pages {data1['total_pages']} should be >= {expected_pages}"
        )


class TestTaskCreation:
    def test_create_task_basic_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={
                "sender_id": "test-sender",
                "receiver_id": "test-receiver",
                "instruction": "Create a test task to verify endpoint functionality",
            },
        )
        # In isolated mode without API key, write endpoints may fail
        assert resp.status_code in (201, 401, 400), (
            f"Create task should return 201, 401, or 400, got {resp.status_code}"
        )

    def test_create_task_basic_keyed(self, keyed: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={
                "sender_id": "test-sender",
                "receiver_id": "test-receiver",
                "instruction": "Create a test task to verify endpoint functionality",
            },
        )
        assert resp.status_code == 201, f"Create task should return 201, got {resp.status_code}"

    def test_create_task_trivial_instruction_rejected_isolated(
        self, isolated: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Trivial instructions (≤5 chars, 'do x', 'test ...') should be rejected."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={
                "sender_id": "test-sender",
                "receiver_id": "test-receiver",
                "instruction": "do x",
            },
        )
        assert resp.status_code == 400, (
            f"Trivial instruction should be rejected, got {resp.status_code}"
        )

    def test_create_task_trivial_instruction_rejected_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Trivial instructions (≤5 chars, 'do x', 'test ...') should be rejected."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={
                "sender_id": "test-sender",
                "receiver_id": "test-receiver",
                "instruction": "do x",
            },
        )
        assert resp.status_code == 400, (
            f"Trivial instruction should be rejected, got {resp.status_code}"
        )

    def test_create_task_flow_tracking_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that created tasks are trackable via the flow endpoint."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.post(
            "/api/v1/tasks",
            json={
                "sender_id": "flow-test-sender",
                "receiver_id": "flow-test-receiver",
                "instruction": "Test task for flow tracking endpoint",
            },
        )
        assert resp.status_code == 201, f"Task creation should succeed, got {resp.status_code}"
        task_id = resp.json().get("id")
        if task_id:
            resp = client.get(f"/api/v1/tasks/{task_id}/flow")
            # Should return 200 or 404 (if flow not yet populated)
            assert resp.status_code in (200, 404)


class TestTaskFilters:
    def test_filter_by_priority_high_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test filtering tasks by priority=high."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks?priority=high")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Filtered tasks should return a list"
        # All returned tasks should have priority=high
        for task in data:
            assert task.get("priority") == "high", (
                f"Expected high priority, got {task.get('priority')}"
            )

    def test_filter_by_priority_medium_keyed(
        self, keyed: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test filtering tasks by priority=medium."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks?priority=medium")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Filtered tasks should return a list"
        # All returned tasks should have priority=medium
        for task in data:
            assert task.get("priority") == "medium", (
                f"Expected medium priority, got {task.get('priority')}"
            )

    def test_filter_by_department_keyed(self, keyed: None, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test filtering tasks by department."""
        monkeypatch.setenv("DASHBOARD_RATE_LIMIT", "100")
        app = create_app()
        client = TestClient(app)
        resp = client.get("/api/v1/dashboard/tasks?department=engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list), "Department-filtered tasks should return a list"
