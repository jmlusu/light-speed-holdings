"""Integration tests for GET /api/tasks/paginated endpoint.

Covers:
  - Default pagination returns correct page with default page_size
  - Custom page and page_size parameters work
  - Response includes total, page, page_size, total_pages, counts_by_status
  - Page beyond total_pages returns empty items
  - Page size boundary values and clamping
  - Priority, status, agent, and department filters
  - Multiple filters combine with AND logic
  - Sort by created_at, priority, receiver_id (asc/desc)
  - Invalid sort_by/sort_dir defaults
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
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


def _seed_tasks(workspace: Path, tasks: list[dict]) -> None:
    """Write tasks directly into the workspace inbox."""
    inbox = workspace / ".opencode" / "inbox.json"
    inbox.write_text(json.dumps(tasks), encoding="utf-8")


def _make_task(
    *,
    id: str = "task-1",
    receiver_id: str = "test-agent",
    instruction: str = "Build the feature",
    status: str = "pending",
    priority: str = "medium",
    sender_id: str = "human-ceo",
    created_at: str = "",
) -> dict:
    """Build a minimal task dict for seeding."""
    if not created_at:
        created_at = datetime.now(timezone.utc).isoformat()
    return {
        "id": id,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "instruction": instruction,
        "status": status,
        "priority": priority,
        "created_at": created_at,
    }


# ═══════════════════════════════════════════════════════════════════════
# Pagination Tests
# ═══════════════════════════════════════════════════════════════════════


class TestPagination:
    """Verify pagination query parameters and response shape."""

    def test_default_pagination_returns_first_page(self, client: TestClient, workspace: Path) -> None:
        """Default page=1, page_size=20 should return the first page."""
        tasks = [_make_task(id=f"t-{i}", instruction=f"Task number {i} for testing") for i in range(5)]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated")
        assert resp.status_code == 200
        data = resp.json()
        assert data["page"] == 1
        assert data["page_size"] == 20
        assert data["total"] == 5
        assert data["total_pages"] == 1
        assert len(data["items"]) == 5

    def test_custom_page_and_page_size(self, client: TestClient, workspace: Path) -> None:
        """Custom page and page_size should slice correctly."""
        tasks = [_make_task(id=f"t-{i}", instruction=f"Task {i} for pagination test") for i in range(25)]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?page=2&page_size=10")
        assert resp.status_code == 200
        data = resp.json()
        assert data["page"] == 2
        assert data["page_size"] == 10
        assert data["total"] == 25
        assert data["total_pages"] == 3
        assert len(data["items"]) == 10

    def test_response_includes_metadata_fields(self, client: TestClient, workspace: Path) -> None:
        """Response must include total, page, page_size, total_pages, counts_by_status."""
        tasks = [_make_task(id="t-1", status="pending")]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated")
        data = resp.json()
        for field in ("total", "page", "page_size", "total_pages", "counts_by_status"):
            assert field in data, f"Missing metadata field: {field}"

    def test_counts_by_status_reflects_unpaginated_set(self, client: TestClient, workspace: Path) -> None:
        """counts_by_status should count across all matching tasks, not just the page."""
        tasks = [
            _make_task(id="t-1", status="pending"),
            _make_task(id="t-2", status="pending"),
            _make_task(id="t-3", status="completed"),
            _make_task(id="t-4", status="in_progress"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?page_size=10")
        data = resp.json()
        assert data["total"] == 4
        assert data["counts_by_status"]["pending"] == 2
        assert data["counts_by_status"]["completed"] == 1
        assert data["counts_by_status"]["in_progress"] == 1

    def test_page_beyond_total_returns_empty_items(self, client: TestClient, workspace: Path) -> None:
        """Requesting a page past the end should return empty items with correct metadata."""
        tasks = [_make_task(id="t-1", instruction="Only one task for this test")]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?page=100&page_size=10")
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 1
        assert data["page"] == 100

    def test_page_size_clamped_to_allowed_values(self, client: TestClient, workspace: Path) -> None:
        """Page size not in {10, 20, 50, 100} should default to 20."""
        tasks = [_make_task(id=f"t-{i}", instruction=f"Task {i} for clamping test") for i in range(5)]
        _seed_tasks(workspace, tasks)

        # page_size=1 is below minimum (ge=10 in Query), so FastAPI rejects it
        resp_too_small = client.get("/api/tasks/paginated?page_size=1")
        assert resp_too_small.status_code == 422

        # page_size=200 is above maximum (le=100 in Query), so FastAPI rejects it
        resp_too_large = client.get("/api/tasks/paginated?page_size=200")
        assert resp_too_large.status_code == 422

    def test_page_size_10_boundary(self, client: TestClient, workspace: Path) -> None:
        """page_size=10 should work as a valid boundary value."""
        tasks = [_make_task(id=f"t-{i}", instruction=f"Boundary task {i}") for i in range(15)]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?page_size=10")
        assert resp.status_code == 200
        assert resp.json()["page_size"] == 10
        assert len(resp.json()["items"]) == 10

    def test_page_size_50_boundary(self, client: TestClient, workspace: Path) -> None:
        """page_size=50 should work as a valid boundary value."""
        tasks = [_make_task(id=f"t-{i}", instruction=f"Fifty-size task {i}") for i in range(30)]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?page_size=50")
        assert resp.status_code == 200
        assert resp.json()["page_size"] == 50
        assert len(resp.json()["items"]) == 30

    def test_page_size_100_boundary(self, client: TestClient, workspace: Path) -> None:
        """page_size=100 should work as a valid boundary value."""
        tasks = [_make_task(id=f"t-{i}", instruction=f"Hundred-size task {i}") for i in range(100)]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?page_size=100")
        assert resp.status_code == 200
        assert resp.json()["page_size"] == 100
        assert len(resp.json()["items"]) == 100

    def test_empty_inbox_returns_empty_items(self, client: TestClient, workspace: Path) -> None:
        """An empty inbox should return empty items with total=0."""
        _seed_tasks(workspace, [])

        resp = client.get("/api/tasks/paginated")
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["total_pages"] == 1


# ═══════════════════════════════════════════════════════════════════════
# Filter Tests
# ═══════════════════════════════════════════════════════════════════════


class TestFiltering:
    """Verify that query filters return only matching tasks."""

    def test_status_filter(self, client: TestClient, workspace: Path) -> None:
        """status=completed should return only completed tasks."""
        tasks = [
            _make_task(id="t-1", status="pending"),
            _make_task(id="t-2", status="completed"),
            _make_task(id="t-3", status="in_progress"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?status=completed")
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["status"] == "completed"

    def test_priority_filter(self, client: TestClient, workspace: Path) -> None:
        """priority=high should return only high-priority tasks."""
        tasks = [
            _make_task(id="t-1", priority="low"),
            _make_task(id="t-2", priority="high"),
            _make_task(id="t-3", priority="high"),
            _make_task(id="t-4", priority="critical"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?priority=high")
        data = resp.json()
        assert data["total"] == 2
        assert all(t["priority"] == "high" for t in data["items"])

    def test_agent_filter(self, client: TestClient, workspace: Path) -> None:
        """agent=lead-backend should return tasks where receiver_id matches."""
        tasks = [
            _make_task(id="t-1", receiver_id="lead-backend", instruction="Build REST endpoint"),
            _make_task(id="t-2", receiver_id="lead-frontend", instruction="Fix CSS layout"),
            _make_task(id="t-3", sender_id="lead-backend", instruction="Review PR"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?agent=lead-backend")
        data = resp.json()
        # Should match t-1 (receiver) and t-3 (sender)
        assert data["total"] == 2

    def test_department_filter(self, client: TestClient, workspace: Path) -> None:
        """department=Technology should return tasks to agents in Technology dept."""
        # lead-backend is in Technology dept per the workspace fixture
        tasks = [
            _make_task(id="t-1", receiver_id="lead-backend", instruction="Build API endpoint"),
            _make_task(id="t-2", receiver_id="test-agent", instruction="Write test suite"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?department=Technology")
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["receiver_id"] == "lead-backend"

    def test_multiple_filters_combine_with_and(self, client: TestClient, workspace: Path) -> None:
        """Multiple filters should be combined with AND logic."""
        tasks = [
            _make_task(id="t-1", status="pending", priority="high", receiver_id="lead-backend", instruction="High priority backend task"),
            _make_task(id="t-2", status="completed", priority="high", receiver_id="lead-backend", instruction="Completed high priority task"),
            _make_task(id="t-3", status="pending", priority="low", receiver_id="lead-backend", instruction="Low priority pending task"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?status=pending&priority=high")
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["id"] == "t-1"

    def test_empty_filter_returns_all(self, client: TestClient, workspace: Path) -> None:
        """No filters should return all tasks."""
        tasks = [
            _make_task(id=f"t-{i}", instruction=f"All tasks test {i}") for i in range(10)
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated")
        assert resp.json()["total"] == 10


# ═══════════════════════════════════════════════════════════════════════
# Sort Tests
# ═══════════════════════════════════════════════════════════════════════


class TestSorting:
    """Verify sort_by and sort_dir query parameters."""

    def test_sort_by_created_at_asc(self, client: TestClient, workspace: Path) -> None:
        """sort_by=created_at&sort_dir=asc should sort oldest first."""
        tasks = [
            _make_task(id="t-1", created_at="2025-01-01T00:00:00Z", instruction="First task created"),
            _make_task(id="t-2", created_at="2025-06-01T00:00:00Z", instruction="Second task created"),
            _make_task(id="t-3", created_at="2025-03-01T00:00:00Z", instruction="Third task created"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?sort_by=created_at&sort_dir=asc")
        data = resp.json()
        ids = [t["id"] for t in data["items"]]
        assert ids == ["t-1", "t-3", "t-2"]

    def test_sort_by_created_at_desc(self, client: TestClient, workspace: Path) -> None:
        """sort_by=created_at&sort_dir=desc should sort newest first."""
        tasks = [
            _make_task(id="t-1", created_at="2025-01-01T00:00:00Z", instruction="Oldest task"),
            _make_task(id="t-2", created_at="2025-06-01T00:00:00Z", instruction="Newest task"),
            _make_task(id="t-3", created_at="2025-03-01T00:00:00Z", instruction="Middle task"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?sort_by=created_at&sort_dir=desc")
        data = resp.json()
        ids = [t["id"] for t in data["items"]]
        assert ids == ["t-2", "t-3", "t-1"]

    def test_sort_by_priority_respects_order(self, client: TestClient, workspace: Path) -> None:
        """sort_by=priority&sort_dir=asc should order: critical < high < medium < low."""
        tasks = [
            _make_task(id="t-1", priority="medium", instruction="Medium priority task"),
            _make_task(id="t-2", priority="low", instruction="Low priority task"),
            _make_task(id="t-3", priority="critical", instruction="Critical priority task"),
            _make_task(id="t-4", priority="high", instruction="High priority task"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?sort_by=priority&sort_dir=asc")
        data = resp.json()
        priorities = [t["priority"] for t in data["items"]]
        assert priorities == ["critical", "high", "medium", "low"]

    def test_sort_by_priority_desc(self, client: TestClient, workspace: Path) -> None:
        """sort_by=priority&sort_dir=desc should order: low < medium < high < critical."""
        tasks = [
            _make_task(id="t-1", priority="critical", instruction="Critical task"),
            _make_task(id="t-2", priority="low", instruction="Low task"),
            _make_task(id="t-3", priority="high", instruction="High task"),
            _make_task(id="t-4", priority="medium", instruction="Medium task"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?sort_by=priority&sort_dir=desc")
        data = resp.json()
        priorities = [t["priority"] for t in data["items"]]
        assert priorities == ["low", "medium", "high", "critical"]

    def test_sort_by_receiver_id_alphabetical(self, client: TestClient, workspace: Path) -> None:
        """sort_by=receiver_id should sort alphabetically."""
        tasks = [
            _make_task(id="t-1", receiver_id="zebra-agent", instruction="Task for zebra"),
            _make_task(id="t-2", receiver_id="alpha-agent", instruction="Task for alpha"),
            _make_task(id="t-3", receiver_id="middle-agent", instruction="Task for middle"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?sort_by=receiver_id&sort_dir=asc")
        data = resp.json()
        receivers = [t["receiver_id"] for t in data["items"]]
        assert receivers == ["alpha-agent", "middle-agent", "zebra-agent"]

    def test_invalid_sort_by_defaults_to_created_at(self, client: TestClient, workspace: Path) -> None:
        """Invalid sort_by should default to created_at."""
        tasks = [
            _make_task(id="t-1", created_at="2025-01-01T00:00:00Z", instruction="Earliest task"),
            _make_task(id="t-2", created_at="2025-06-01T00:00:00Z", instruction="Latest task"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?sort_by=nonexistent_field&sort_dir=asc")
        data = resp.json()
        ids = [t["id"] for t in data["items"]]
        assert ids == ["t-1", "t-2"]

    def test_invalid_sort_dir_defaults_to_desc(self, client: TestClient, workspace: Path) -> None:
        """Invalid sort_dir should default to desc."""
        tasks = [
            _make_task(id="t-1", created_at="2025-01-01T00:00:00Z", instruction="Oldest task"),
            _make_task(id="t-2", created_at="2025-06-01T00:00:00Z", instruction="Newest task"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?sort_by=created_at&sort_dir=invalid")
        data = resp.json()
        ids = [t["id"] for t in data["items"]]
        # Default is desc, so newest first
        assert ids == ["t-2", "t-1"]


# ═══════════════════════════════════════════════════════════════════════
# Edge Cases
# ═══════════════════════════════════════════════════════════════════════


class TestEdgeCases:
    """Edge case tests for the paginated endpoint."""

    def test_comma_separated_status_filter(self, client: TestClient, workspace: Path) -> None:
        """Comma-separated status values should filter to the union."""
        tasks = [
            _make_task(id="t-1", status="pending"),
            _make_task(id="t-2", status="completed"),
            _make_task(id="t-3", status="in_progress"),
            _make_task(id="t-4", status="failed"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?status=pending,completed")
        data = resp.json()
        assert data["total"] == 2
        statuses = {t["status"] for t in data["items"]}
        assert statuses == {"pending", "completed"}

    def test_comma_separated_priority_filter(self, client: TestClient, workspace: Path) -> None:
        """Comma-separated priority values should filter to the union."""
        tasks = [
            _make_task(id="t-1", priority="low"),
            _make_task(id="t-2", priority="high"),
            _make_task(id="t-3", priority="critical"),
            _make_task(id="t-4", priority="medium"),
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?priority=high,critical")
        data = resp.json()
        assert data["total"] == 2
        priorities = {t["priority"] for t in data["items"]}
        assert priorities == {"high", "critical"}

    def test_pagination_preserves_filter_across_pages(self, client: TestClient, workspace: Path) -> None:
        """Filtering should work correctly across multiple pages."""
        tasks = [
            _make_task(id=f"t-{i}", status="pending" if i % 2 == 0 else "completed", instruction=f"Cross-page task {i}")
            for i in range(25)
        ]
        _seed_tasks(workspace, tasks)

        resp = client.get("/api/tasks/paginated?status=pending&page=1&page_size=10")
        data = resp.json()
        assert all(t["status"] == "pending" for t in data["items"])
        # 13 pending tasks (indices 0,2,4,...,24) -> 2 pages
        assert data["total_pages"] == 2
