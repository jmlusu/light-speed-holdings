"""End-to-end tests for the task creation pipeline.

Verifies the complete flow:
  POST /api/tasks → MessageBus.send_task() → inbox.json persistence → GET /api/tasks

Covers:
  - MessageBus unit tests (persistence, read-back, correlation IDs)
  - API integration tests (POST creates, GET returns, field correctness)
  - Edge cases (missing fields, empty inbox)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from ai_company.models.task import Task
from ai_company.orchestrator.message_bus import MessageBus


# ═══════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════


@pytest.fixture()
def inbox_path(tmp_path: Path) -> Path:
    """Return a temporary inbox.json path for test isolation."""
    return tmp_path / "inbox.json"


@pytest.fixture()
def bus(inbox_path: Path) -> MessageBus:
    """Return a fresh MessageBus backed by a temp inbox."""
    return MessageBus(storage_path=str(inbox_path))


@pytest.fixture()
def api_client(tmp_path: Path):
    """Return a FastAPI TestClient with MessageBus pointing to temp dir."""
    from ai_company.dashboard import api as dash_api

    # Create a temp inbox and wire the bus to it
    temp_inbox = tmp_path / "inbox.json"
    test_bus = MessageBus(storage_path=str(temp_inbox))
    dash_api._bus = test_bus

    from ai_company.dashboard.app import create_app

    app = create_app()

    # Set DASHBOARD_DATA_DIR so StateStore uses the temp directory
    with patch.dict("os.environ", {"DASHBOARD_DATA_DIR": str(tmp_path)}):
        client = TestClient(app, raise_server_exceptions=False)
        yield client

    # Cleanup
    dash_api._bus = None


# ═══════════════════════════════════════════════════════════════════════
# Unit Tests — MessageBus Persistence
# ═══════════════════════════════════════════════════════════════════════


class TestMessageBusPersistence:
    """Verify that send_task() persists to inbox.json and get_all_tasks() reads back."""

    def test_send_task_persists_to_inbox_file(self, bus: MessageBus, inbox_path: Path) -> None:
        """send_task() should persist the task to inbox.json."""
        task = Task(
            id="test-1",
            sender_id="human-ceo",
            receiver_id="cto",
            instruction="Review architecture",
        )
        bus.send_task(task)

        assert inbox_path.exists()
        data = json.loads(inbox_path.read_text(encoding="utf-8"))
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == "test-1"

    def test_send_task_appends_to_existing(self, bus: MessageBus) -> None:
        """Multiple send_task() calls should append, not overwrite."""
        for i in range(3):
            task = Task(
                id=f"task-{i}",
                sender_id="human-ceo",
                receiver_id="cto",
                instruction=f"Task {i}",
            )
            bus.send_task(task)

        all_tasks = bus.get_all_tasks()
        assert len(all_tasks) == 3
        assert [t.id for t in all_tasks] == ["task-0", "task-1", "task-2"]

    def test_get_all_tasks_reads_back_correctly(self, bus: MessageBus) -> None:
        """get_all_tasks() should return Task objects with all fields intact."""
        task = Task(
            id="readback-1",
            sender_id="human-ceo",
            receiver_id="coo",
            instruction="Optimize operations",
            priority="high",
        )
        bus.send_task(task)

        all_tasks = bus.get_all_tasks()
        assert len(all_tasks) == 1
        t = all_tasks[0]
        assert t.id == "readback-1"
        assert t.sender_id == "human-ceo"
        assert t.receiver_id == "coo"
        assert t.instruction == "Optimize operations"
        assert t.status.value == "pending"
        assert t.priority.value == "high"

    def test_send_task_generates_correlation_id(self, bus: MessageBus) -> None:
        """send_task() should auto-generate a correlation_id if not provided."""
        task = Task(
            id="corr-1",
            sender_id="a",
            receiver_id="b",
            instruction="test",
        )
        assert task.correlation_id == ""  # Initially empty

        bus.send_task(task)

        # Read back from file to check correlation_id was set
        all_tasks = bus.get_all_tasks()
        assert all_tasks[0].correlation_id != ""

    def test_send_task_preserves_existing_correlation_id(self, bus: MessageBus) -> None:
        """send_task() should not overwrite an existing correlation_id."""
        task = Task(
            id="corr-2",
            sender_id="a",
            receiver_id="b",
            instruction="test",
            correlation_id="my-custom-corr-id",
        )
        bus.send_task(task)

        all_tasks = bus.get_all_tasks()
        assert all_tasks[0].correlation_id == "my-custom-corr-id"

    def test_empty_inbox_returns_empty_list(self, bus: MessageBus) -> None:
        """get_all_tasks() on an empty inbox should return an empty list."""
        all_tasks = bus.get_all_tasks()
        assert all_tasks == []

    def test_persistence_survives_new_bus_instance(self, inbox_path: Path) -> None:
        """Data should persist across different MessageBus instances."""
        bus1 = MessageBus(storage_path=str(inbox_path))
        task = Task(
            id="persist-1",
            sender_id="a",
            receiver_id="b",
            instruction="persistent task",
        )
        bus1.send_task(task)

        # Create a new bus instance pointing to the same file
        bus2 = MessageBus(storage_path=str(inbox_path))
        all_tasks = bus2.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == "persist-1"

    def test_get_pending_tasks_filters_correctly(self, bus: MessageBus) -> None:
        """get_pending_tasks() should only return tasks with status=pending."""
        bus.send_task(Task(id="p1", sender_id="a", receiver_id="b", instruction="pending"))
        bus.send_task(Task(id="p2", sender_id="a", receiver_id="b", instruction="also pending"))

        # Complete one task
        bus.update_task_status("p1", "completed")

        pending = bus.get_pending_tasks()
        assert len(pending) == 1
        assert pending[0].id == "p2"


# ═══════════════════════════════════════════════════════════════════════
# Integration Tests — API Endpoint
# ═══════════════════════════════════════════════════════════════════════


class TestTaskCreationAPI:
    """Verify POST /api/tasks creates a task and GET /api/tasks returns it."""

    def test_post_tasks_creates_task(self, api_client: TestClient) -> None:
        """POST /api/tasks should create a task and return 201."""
        response = api_client.post(
            "/api/tasks",
            json={
                "receiver_id": "cto",
                "instruction": "Review the architecture",
                "priority": "high",
                "sender_id": "human-ceo",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["receiver_id"] == "cto"
        assert data["instruction"] == "Review the architecture"
        assert data["priority"] == "high"
        assert data["sender_id"] == "human-ceo"
        assert data["status"] == "pending"
        assert "id" in data

    def test_post_tasks_persists_to_inbox(self, api_client: TestClient) -> None:
        """POST /api/tasks should persist the task so GET /api/tasks returns it."""
        # Create a task
        create_resp = api_client.post(
            "/api/tasks",
            json={
                "receiver_id": "coo",
                "instruction": "Optimize workflow",
                "priority": "medium",
            },
        )
        assert create_resp.status_code == 201
        task_id = create_resp.json()["id"]

        # Retrieve all tasks
        list_resp = api_client.get("/api/tasks")
        assert list_resp.status_code == 200
        tasks = list_resp.json()

        # Our created task should be in the list
        matching = [t for t in tasks if t["id"] == task_id]
        assert len(matching) == 1
        assert matching[0]["receiver_id"] == "coo"
        assert matching[0]["instruction"] == "Optimize workflow"

    def test_post_tasks_returns_all_required_fields(self, api_client: TestClient) -> None:
        """The response should contain all required TaskItem fields."""
        response = api_client.post(
            "/api/tasks",
            json={
                "receiver_id": "caio",
                "instruction": "Evaluate AI strategy",
                "priority": "critical",
            },
        )
        assert response.status_code == 201
        data = response.json()

        required_fields = ["id", "sender_id", "receiver_id", "instruction", "status", "priority"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_post_tasks_defaults(self, api_client: TestClient) -> None:
        """POST /api/tasks should apply correct defaults for optional fields."""
        response = api_client.post(
            "/api/tasks",
            json={
                "receiver_id": "cto",
                "instruction": "Deploy feature",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["sender_id"] == "human-ceo"  # Default
        assert data["priority"] == "medium"  # Default
        assert data["status"] == "pending"  # Always set on creation

    def test_post_tasks_generates_uuid(self, api_client: TestClient) -> None:
        """Each created task should have a unique UUID as its id."""
        resp1 = api_client.post(
            "/api/tasks",
            json={"receiver_id": "cto", "instruction": "Task A"},
        )
        resp2 = api_client.post(
            "/api/tasks",
            json={"receiver_id": "cto", "instruction": "Task B"},
        )
        assert resp1.status_code == 201
        assert resp2.status_code == 201
        assert resp1.json()["id"] != resp2.json()["id"]

    def test_post_tasks_missing_receiver_returns_422(self, api_client: TestClient) -> None:
        """POST /api/tasks without receiver_id should return 422."""
        response = api_client.post(
            "/api/tasks",
            json={
                "instruction": "Do something",
            },
        )
        assert response.status_code == 422

    def test_post_tasks_missing_instruction_returns_422(self, api_client: TestClient) -> None:
        """POST /api/tasks without instruction should return 422."""
        response = api_client.post(
            "/api/tasks",
            json={
                "receiver_id": "cto",
            },
        )
        assert response.status_code == 422

    def test_post_tasks_empty_body_returns_422(self, api_client: TestClient) -> None:
        """POST /api/tasks with empty body should return 422."""
        response = api_client.post("/api/tasks", json={})
        assert response.status_code == 422

    def test_get_tasks_filter_by_status(self, api_client: TestClient) -> None:
        """GET /api/tasks?status=pending should filter correctly."""
        # Create two tasks
        api_client.post(
            "/api/tasks",
            json={"receiver_id": "cto", "instruction": "Task 1"},
        )
        api_client.post(
            "/api/tasks",
            json={"receiver_id": "coo", "instruction": "Task 2"},
        )

        # Filter by status
        resp = api_client.get("/api/tasks?status=pending")
        assert resp.status_code == 200
        tasks = resp.json()
        assert all(t["status"] == "pending" for t in tasks)
        assert len(tasks) == 2

    def test_get_tasks_filter_by_agent(self, api_client: TestClient) -> None:
        """GET /api/tasks?agent=cto should filter by receiver_id."""
        api_client.post(
            "/api/tasks",
            json={"receiver_id": "cto", "instruction": "For CTO"},
        )
        api_client.post(
            "/api/tasks",
            json={"receiver_id": "coo", "instruction": "For COO"},
        )

        resp = api_client.get("/api/tasks?agent=cto")
        assert resp.status_code == 200
        tasks = resp.json()
        assert len(tasks) == 1
        assert tasks[0]["receiver_id"] == "cto"

    def test_post_tasks_empty_inbox_initially(self, api_client: TestClient) -> None:
        """GET /api/tasks on a clean inbox should return an empty list."""
        resp = api_client.get("/api/tasks")
        assert resp.status_code == 200
        assert resp.json() == []


# ═══════════════════════════════════════════════════════════════════════
# Integration Tests — Full Pipeline
# ═══════════════════════════════════════════════════════════════════════


class TestFullPipeline:
    """End-to-end tests covering the complete create→persist→read flow."""

    def test_create_then_read_full_cycle(self, api_client: TestClient) -> None:
        """Create a task, verify it persists, verify fields are complete."""
        # Step 1: Create
        create_resp = api_client.post(
            "/api/tasks",
            json={
                "receiver_id": "cto",
                "instruction": "Implement caching layer",
                "priority": "high",
                "sender_id": "human-ceo",
            },
        )
        assert create_resp.status_code == 201
        created = create_resp.json()

        # Step 2: Read back
        list_resp = api_client.get("/api/tasks")
        assert list_resp.status_code == 200
        all_tasks = list_resp.json()

        # Step 3: Find our task
        found = [t for t in all_tasks if t["id"] == created["id"]]
        assert len(found) == 1
        task = found[0]

        # Step 4: Verify all fields
        assert task["id"] == created["id"]
        assert task["sender_id"] == "human-ceo"
        assert task["receiver_id"] == "cto"
        assert task["instruction"] == "Implement caching layer"
        assert task["status"] == "pending"
        assert task["priority"] == "high"
        assert task["created_at"] is not None  # Should have a timestamp

    def test_multiple_tasks_accumulate(self, api_client: TestClient) -> None:
        """Multiple task creations should accumulate in the inbox."""
        instructions = [
            "Review PR #42",
            "Deploy to staging",
            "Update documentation",
            "Run security audit",
            "Optimize database queries",
        ]

        for inst in instructions:
            resp = api_client.post(
                "/api/tasks",
                json={"receiver_id": "cto", "instruction": inst},
            )
            assert resp.status_code == 201

        # Verify all tasks are present
        list_resp = api_client.get("/api/tasks")
        assert list_resp.status_code == 200
        tasks = list_resp.json()
        assert len(tasks) == len(instructions)

        task_instructions = {t["instruction"] for t in tasks}
        for inst in instructions:
            assert inst in task_instructions

    def test_task_lifecycle_via_api(self, api_client: TestClient) -> None:
        """Create a task and verify it can be read with correct initial state."""
        # Create
        resp = api_client.post(
            "/api/tasks",
            json={
                "receiver_id": "coo",
                "instruction": "Streamline operations",
                "priority": "critical",
            },
        )
        assert resp.status_code == 201
        task = resp.json()

        # Verify initial state
        assert task["status"] == "pending"
        assert task["priority"] == "critical"
        assert task["created_at"] is not None

        # Verify it shows up in GET
        list_resp = api_client.get("/api/tasks")
        assert list_resp.status_code == 200
        found = [t for t in list_resp.json() if t["id"] == task["id"]]
        assert len(found) == 1
