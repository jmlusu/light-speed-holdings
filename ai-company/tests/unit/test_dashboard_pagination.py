"""Tests for the paginated tasks endpoint and POST /api/tasks validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ai_company.dashboard.app import app

client = TestClient(app, raise_server_exceptions=False)


def _seed_tasks(tmp_path: Path, count: int, **overrides: str) -> None:
    """Write *count* tasks into the inbox for a test."""
    tasks = []
    statuses = ["pending", "in_progress", "completed", "failed", "escalated"]
    priorities = ["low", "medium", "high", "critical"]
    agents = ["lead-engineering", "lead-marketing", "chief-of-staff"]
    for i in range(count):
        tasks.append({
            "id": f"task-{i:04d}",
            "sender_id": "human-ceo",
            "receiver_id": agents[i % len(agents)],
            "instruction": f"Implement feature {i} in the system",
            "status": statuses[i % len(statuses)],
            "priority": priorities[i % len(priorities)],
            "created_at": f"2026-07-{10 + (i % 20):02d}T10:00:00Z",
        })
    (tmp_path / ".opencode" / "inbox.json").write_text(json.dumps(tasks), encoding="utf-8")


@pytest.fixture()
def setup_pagination(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Minimal fixture: isolated workspace with seed tasks."""
    monkeypatch.chdir(tmp_path)

    from ai_company.dashboard.repository import get_state_store, reset_state_store

    reset_state_store()
    get_state_store(tmp_path)

    (tmp_path / "company").mkdir()
    registry = [
        {
            "name": "lead-engineering",
            "role": "Lead Engineer",
            "type": "specialist",
            "department": "Engineering",
            "reportsTo": "chief-of-staff",
            "directReports": [],
        },
        {
            "name": "lead-marketing",
            "role": "Marketing Lead",
            "type": "specialist",
            "department": "Marketing",
            "reportsTo": "chief-of-staff",
            "directReports": [],
        },
        {
            "name": "chief-of-staff",
            "role": "Chief of Staff",
            "type": "executive",
            "department": "Executive",
            "reportsTo": "human-ceo",
            "directReports": ["lead-engineering", "lead-marketing"],
        },
    ]
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(registry), encoding="utf-8"
    )
    (tmp_path / ".opencode").mkdir(exist_ok=True)
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
    for name in ("approvals.yaml", "escalation.yaml", "scheduler.yaml"):
        (tmp_path / "orchestrator" / name).write_text("{}", encoding="utf-8")


# ── Default pagination ─────────────────────────────────────────────


class TestDefaultPagination:
    def test_returns_empty_by_default(self, setup_pagination: None) -> None:
        resp = client.get("/api/tasks/paginated")
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 20
        assert data["total_pages"] == 1
        assert data["counts_by_status"] == {}

    def test_page_size_10(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 25)
        resp = client.get("/api/tasks/paginated?page_size=10")
        data = resp.json()
        assert len(data["items"]) == 10
        assert data["total"] == 25
        assert data["total_pages"] == 3

    def test_page_size_100(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 150)
        resp = client.get("/api/tasks/paginated?page_size=100")
        data = resp.json()
        assert len(data["items"]) == 100
        assert data["total"] == 150
        assert data["total_pages"] == 2

    def test_invalid_page_size_falls_back_to_20(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 30)
        resp = client.get("/api/tasks/paginated?page_size=15")
        data = resp.json()
        assert data["page_size"] == 20
        assert len(data["items"]) == 20

    def test_page_beyond_total_returns_empty(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 10)
        resp = client.get("/api/tasks/paginated?page=999")
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 10

    def test_total_pages_calculation(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 55)
        resp = client.get("/api/tasks/paginated?page_size=10")
        data = resp.json()
        assert data["total_pages"] == 6  # ceil(55/10)


# ── Filtering ──────────────────────────────────────────────────────


class TestFiltering:
    def test_filter_by_status_single(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 20)
        resp = client.get("/api/tasks/paginated?status=pending")
        data = resp.json()
        assert all(t["status"] == "pending" for t in data["items"])
        assert data["counts_by_status"].get("pending", 0) > 0

    def test_filter_by_status_multiple(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 20)
        resp = client.get("/api/tasks/paginated?status=pending,in_progress")
        data = resp.json()
        assert all(t["status"] in ("pending", "in_progress") for t in data["items"])

    def test_filter_by_priority(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 20)
        resp = client.get("/api/tasks/paginated?priority=high,critical")
        data = resp.json()
        assert all(t["priority"] in ("high", "critical") for t in data["items"])

    def test_filter_by_department(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 20)
        resp = client.get("/api/tasks/paginated?department=engineering")
        data = resp.json()
        for t in data["items"]:
            assert t["receiver_id"] == "lead-engineering"

    def test_filter_by_agent(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 20)
        resp = client.get("/api/tasks/paginated?agent=lead")
        data = resp.json()
        for t in data["items"]:
            assert "lead" in t["receiver_id"].lower() or "lead" in t["sender_id"].lower()

    def test_combined_filters(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 20)
        resp = client.get(
            "/api/tasks/paginated?status=pending&priority=critical&agent=lead"
        )
        data = resp.json()
        for t in data["items"]:
            assert t["status"] == "pending"
            assert t["priority"] == "critical"
            assert "lead" in t["receiver_id"].lower() or "lead" in t["sender_id"].lower()


# ── Sorting ────────────────────────────────────────────────────────


class TestSorting:
    def test_sort_by_created_at_desc(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 15)
        resp = client.get("/api/tasks/paginated?sort_by=created_at&sort_dir=desc")
        data = resp.json()
        dates = [t["created_at"] for t in data["items"]]
        assert dates == sorted(dates, reverse=True)

    def test_sort_by_created_at_asc(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 15)
        resp = client.get("/api/tasks/paginated?sort_by=created_at&sort_dir=asc")
        data = resp.json()
        dates = [t["created_at"] for t in data["items"]]
        assert dates == sorted(dates)

    def test_sort_by_priority(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 20)
        resp = client.get("/api/tasks/paginated?sort_by=priority&sort_dir=asc")
        data = resp.json()
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        priorities = [order[t["priority"]] for t in data["items"]]
        assert priorities == sorted(priorities)

    def test_sort_by_receiver_id(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 20)
        resp = client.get("/api/tasks/paginated?sort_by=receiver_id&sort_dir=asc")
        data = resp.json()
        ids = [t["receiver_id"] for t in data["items"]]
        assert ids == sorted(ids)


# ── Counts ─────────────────────────────────────────────────────────


class TestCountsByStatus:
    def test_counts_reflect_filters(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 20)
        resp = client.get("/api/tasks/paginated?priority=high")
        data = resp.json()
        total_from_counts = sum(data["counts_by_status"].values())
        assert total_from_counts == data["total"]

    def test_empty_result(self, setup_pagination: None) -> None:
        resp = client.get("/api/tasks/paginated?status=nonexistent")
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0


# ── Backward compatibility ─────────────────────────────────────────


class TestBackwardCompatibility:
    def test_old_endpoint_still_works(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 5)
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 5

    def test_both_endpoints_return_consistent_data(self, setup_pagination: None) -> None:
        _seed_tasks(Path("."), 10)
        old = client.get("/api/tasks").json()
        new = client.get("/api/tasks/paginated?page_size=100").json()
        assert len(old) == new["total"]
        old_ids = {t["id"] for t in old}
        new_ids = {t["id"] for t in new["items"]}
        assert old_ids == new_ids


# ── POST /api/tasks validation ────────────────────────────────────


class TestCreateTaskValidation:
    def test_reject_trivial_instruction(self, setup_pagination: None) -> None:
        resp = client.post(
            "/api/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "do x"},
        )
        assert resp.status_code == 400
        assert "too short" in resp.json()["detail"].lower()

    def test_reject_test_pattern(self, setup_pagination: None) -> None:
        resp = client.post(
            "/api/tasks",
            json={"receiver_id": "lead-engineering", "instruction": "test something here"},
        )
        assert resp.status_code == 400
        assert "placeholder" in resp.json()["detail"].lower()

    def test_accept_meaningful_instruction(self, setup_pagination: None) -> None:
        resp = client.post(
            "/api/tasks",
            json={
                "receiver_id": "lead-engineering",
                "instruction": "Build the new API endpoint for task pagination",
            },
        )
        assert resp.status_code == 201
        assert resp.json()["receiver_id"] == "lead-engineering"
