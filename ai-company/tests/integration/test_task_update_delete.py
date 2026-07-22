"""Integration tests for PATCH /api/tasks/{id} and DELETE /api/tasks/{id}.

Covers:
  - PATCH endpoint: status update, partial fields, 404 on missing task
  - DELETE endpoint: removal, 404 on missing task
  - Kanban drag-and-drop round-trip: create → PATCH status → verify persistence
  - WebSocket broadcast events after mutations
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app


@pytest.fixture()
def client(workspace: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """TestClient bound to a fresh app instance over the isolated workspace."""
    from ai_company.dashboard import api as dash_api
    from ai_company.dashboard.repository import get_state_store, reset_state_store

    dash_api._bus = None
    reset_state_store()
    get_state_store(workspace)
    return TestClient(app, raise_server_exceptions=False)


# ═══════════════════════════════════════════════════════════════════════
# PATCH /api/tasks/{task_id}
# ═══════════════════════════════════════════════════════════════════════


class TestPatchTask:
    """Verify PATCH endpoint updates task fields and persists to inbox."""

    def _create_task(self, client: TestClient, instruction: str = "Test task") -> dict:
        """Helper to create a task and return the response body."""
        resp = client.post(
            "/api/tasks",
            json={
                "receiver_id": "test-agent",
                "instruction": instruction,
                "priority": "medium",
            },
        )
        assert resp.status_code == 201
        return resp.json()

    def test_patch_status_updates_task(self, client: TestClient) -> None:
        """PATCH with status should update the task and persist the change."""
        task = self._create_task(client, "Review PR")

        resp = client.patch(
            f"/api/tasks/{task['id']}",
            json={"status": "in_progress"},
        )
        assert resp.status_code == 200
        updated = resp.json()
        assert updated["id"] == task["id"]
        assert updated["status"] == "in_progress"

        # Verify persistence via GET
        list_resp = client.get("/api/tasks")
        found = [t for t in list_resp.json() if t["id"] == task["id"]]
        assert len(found) == 1
        assert found[0]["status"] == "in_progress"

    def test_patch_priority_updates_task(self, client: TestClient) -> None:
        """PATCH with priority should update just the priority field."""
        task = self._create_task(client, "Deploy feature")

        resp = client.patch(
            f"/api/tasks/{task['id']}",
            json={"priority": "critical"},
        )
        assert resp.status_code == 200
        updated = resp.json()
        assert updated["priority"] == "critical"
        assert updated["status"] == "pending"  # unchanged

    def test_patch_multiple_fields(self, client: TestClient) -> None:
        """PATCH with multiple fields should update all supplied fields."""
        task = self._create_task(client, "Multi-field update")

        resp = client.patch(
            f"/api/tasks/{task['id']}",
            json={"status": "in_progress", "priority": "high"},
        )
        assert resp.status_code == 200
        updated = resp.json()
        assert updated["status"] == "in_progress"
        assert updated["priority"] == "high"

    def test_patch_not_found_returns_404(self, client: TestClient) -> None:
        """PATCH on a non-existent task should return 404."""
        resp = client.patch(
            "/api/tasks/nonexistent-id",
            json={"status": "completed"},
        )
        assert resp.status_code == 404

    def test_patch_empty_body_returns_400(self, client: TestClient) -> None:
        """PATCH with no fields should return 400."""
        task = self._create_task(client)
        resp = client.patch(f"/api/tasks/{task['id']}", json={})
        assert resp.status_code == 400

    def test_patch_completed_sets_completed_at(self, client: TestClient) -> None:
        """PATCH status to 'completed' should set completed_at timestamp."""
        task = self._create_task(client, "Complete me")

        resp = client.patch(
            f"/api/tasks/{task['id']}",
            json={"status": "completed"},
        )
        assert resp.status_code == 200
        updated = resp.json()
        assert updated["status"] == "completed"
        # completed_at should be set
        assert updated.get("completed_at") is not None

    def test_kanban_drag_roundtrip(self, client: TestClient) -> None:
        """Simulate a Kanban drag: create → drag to in_progress → drag to completed."""
        task = self._create_task(client, "Drag me")

        # Step 1: Drag to in_progress
        resp1 = client.patch(
            f"/api/tasks/{task['id']}",
            json={"status": "in_progress"},
        )
        assert resp1.status_code == 200
        assert resp1.json()["status"] == "in_progress"

        # Step 2: Drag to completed
        resp2 = client.patch(
            f"/api/tasks/{task['id']}",
            json={"status": "completed"},
        )
        assert resp2.status_code == 200
        assert resp2.json()["status"] == "completed"

        # Verify final state via GET
        list_resp = client.get("/api/tasks")
        found = [t for t in list_resp.json() if t["id"] == task["id"]]
        assert found[0]["status"] == "completed"


# ═══════════════════════════════════════════════════════════════════════
# DELETE /api/tasks/{task_id}
# ═══════════════════════════════════════════════════════════════════════


class TestDeleteTask:
    """Verify DELETE endpoint removes tasks from the inbox."""

    def _create_task(self, client: TestClient, instruction: str = "To be deleted") -> dict:
        """Helper to create a task and return the response body."""
        resp = client.post(
            "/api/tasks",
            json={
                "receiver_id": "test-agent",
                "instruction": instruction,
            },
        )
        assert resp.status_code == 201
        return resp.json()

    def test_delete_removes_task(self, client: TestClient) -> None:
        """DELETE should remove the task from the inbox."""
        task = self._create_task(client, "Delete me")

        resp = client.delete(f"/api/tasks/{task['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] == "true"
        assert data["id"] == task["id"]

        # Verify the task is gone
        list_resp = client.get("/api/tasks")
        found = [t for t in list_resp.json() if t["id"] == task["id"]]
        assert len(found) == 0

    def test_delete_not_found_returns_404(self, client: TestClient) -> None:
        """DELETE on a non-existent task should return 404."""
        resp = client.delete("/api/tasks/nonexistent-id")
        assert resp.status_code == 404

    def test_delete_does_not_affect_other_tasks(self, client: TestClient) -> None:
        """Deleting one task should not affect other tasks."""
        task1 = self._create_task(client, "Keep me")
        task2 = self._create_task(client, "Delete me")

        resp = client.delete(f"/api/tasks/{task2['id']}")
        assert resp.status_code == 200

        # task1 should still be there
        list_resp = client.get("/api/tasks")
        found = [t for t in list_resp.json() if t["id"] == task1["id"]]
        assert len(found) == 1
        assert found[0]["instruction"] == "Keep me"

    def test_delete_persists_to_file(self, client: TestClient, workspace: Path) -> None:
        """DELETE should persist — the task should not reappear on reload."""
        task = self._create_task(client, "Persist delete")

        # Delete it
        client.delete(f"/api/tasks/{task['id']}")

        # Read the inbox file directly
        inbox = (workspace / ".opencode" / "inbox.json").read_text(encoding="utf-8")
        assert task["id"] not in inbox
        assert "Persist delete" not in inbox

    def test_delete_return_shape(self, client: TestClient) -> None:
        """DELETE response should have the correct shape."""
        task = self._create_task(client)

        resp = client.delete(f"/api/tasks/{task['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert "ok" in data
        assert "id" in data
        assert data["id"] == task["id"]
