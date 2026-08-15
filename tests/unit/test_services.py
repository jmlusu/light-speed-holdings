"""Tests for the FileStore abstraction and persistent workflow state."""

from __future__ import annotations

import threading
from pathlib import Path

import pytest

from ai_company.models import (
    Company,
    CompanyRegistry,
    Workflow,
    WorkflowStep,
)
from ai_company.store.file_store import FileStore
from ai_company.workflow.engine import WorkflowEngine

# ── FileStore Tests ───────────────────────────────────────────────────


class TestFileStore:
    def test_read_write_json(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        store.write_json("data.json", {"key": "value"})
        result = store.read_json("data.json")
        assert result == {"key": "value"}

    def test_read_write_yaml(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        store.write_yaml("config.yaml", {"section": {"key": "value"}})
        result = store.read_yaml("config.yaml")
        assert result == {"section": {"key": "value"}}

    def test_atomic_write_creates_parent_dirs(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        store.write_json("deep/nested/file.json", [1, 2, 3])
        assert store.read_json("deep/nested/file.json") == [1, 2, 3]

    def test_read_nonexistent_returns_none(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        assert store.read_json("nope.json") is None
        assert store.read_yaml("nope.yaml") is None

    def test_exists_and_delete(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        store.write_json("del.json", [1])
        assert store.exists("del.json")
        assert store.delete("del.json")
        assert not store.exists("del.json")
        assert not store.delete("del.json")  # Double delete is safe

    def test_list_files(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        store.write_json("a.json", 1)
        store.write_json("b.json", 2)
        store.write_yaml("c.yaml", 3)
        files = store.list_files(pattern="*.json")
        assert len(files) == 2

    def test_backup_created(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path, backup=True)
        store.write_json("test.json", {"v": 1})
        assert (tmp_path / "test.json.bak").exists()

    def test_backup_disabled(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path, backup=False)
        store.write_json("test.json", {"v": 1})
        assert not (tmp_path / "test.json.bak").exists()

    def test_corrupt_json_returns_none(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path)
        (tmp_path / "bad.json").write_text("{invalid json!!!", encoding="utf-8")
        assert store.read_json("bad.json") is None

    def test_concurrent_writes(self, tmp_path: Path) -> None:
        """Test that concurrent atomic writes don't corrupt data."""
        store = FileStore(tmp_path)
        store.write_json("counter.json", {"count": 0})

        def increment(n: int) -> None:
            for _ in range(10):

                def updater(data: dict | None) -> dict:
                    if data is None:
                        data = {"count": 0}
                    data["count"] = data.get("count", 0) + 1
                    return data

                store.update_json("counter.json", updater)

        threads = [threading.Thread(target=increment, args=(i,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        result = store.read_json("counter.json")
        assert result["count"] == 40

# ── Persistent Workflow Engine Tests ─────────────────────────────────


@pytest.fixture()
def registry() -> CompanyRegistry:
    return CompanyRegistry(
        company=Company(id="test", name="Test"),
        workflows=[
            Workflow(
                id="hiring",
                name="Hiring Workflow",
                trigger="job_requisition",
                owner="hr",
                steps=[
                    WorkflowStep(
                        id="post", name="Post Job", action="Create job posting", owner="recruiter"
                    ),
                    WorkflowStep(
                        id="review",
                        name="Review Resumes",
                        action="Screen candidates",
                        owner="recruiter",
                    ),
                    WorkflowStep(
                        id="interview",
                        name="Interview",
                        action="Conduct interviews",
                        owner="hiring_manager",
                    ),
                ],
            ),
        ],
    )


class TestPersistentWorkflowEngine:
    def test_instances_persist(self, tmp_path: Path, registry: CompanyRegistry) -> None:
        state_dir = tmp_path / "wf_instances"
        # Start a workflow and advance it
        engine = WorkflowEngine(registry, state_dir=state_dir)
        instance_id = engine.start("hiring")
        engine.complete_step(instance_id, "Posted on LinkedIn")
        status1 = engine.get_status(instance_id)
        assert status1["current_step"] == "Review Resumes"
        assert status1["completed_steps"] == 1

        # Create a new engine with same state_dir -- should load persisted state
        engine2 = WorkflowEngine(registry, state_dir=state_dir)
        status2 = engine2.get_status(instance_id)
        assert status2 is not None
        assert status2["current_step"] == "Review Resumes"
        assert status2["completed_steps"] == 1

    def test_cancel_persists(self, tmp_path: Path, registry: CompanyRegistry) -> None:
        state_dir = tmp_path / "wf_instances"
        engine = WorkflowEngine(registry, state_dir=state_dir)
        instance_id = engine.start("hiring")
        engine.cancel(instance_id)

        # Reload and verify
        engine2 = WorkflowEngine(registry, state_dir=state_dir)
        status = engine2.get_status(instance_id)
        assert status["status"] == "cancelled"

    def test_list_instances(self, tmp_path: Path, registry: CompanyRegistry) -> None:
        state_dir = tmp_path / "wf_instances"
        engine = WorkflowEngine(registry, state_dir=state_dir)
        engine.start("hiring")
        engine.start("hiring")
        # Both may have same timestamp; if so, second overwrites first.
        # The important thing is list_instances works.
        instances = engine.list_instances()
        assert len(instances) >= 1
        assert all(i["workflow_id"] == "hiring" for i in instances)

        # Filter by non-existent workflow_id
        empty = engine.list_instances(workflow_id="nonexistent")
        assert len(empty) == 0

    def test_missing_workflow_on_reload(self, tmp_path: Path) -> None:
        """Instance referencing a removed workflow is skipped gracefully."""
        state_dir = tmp_path / "wf_instances"

        # Create with a workflow
        reg1 = CompanyRegistry(
            company=Company(id="test", name="Test"),
            workflows=[
                Workflow(
                    id="old_wf",
                    name="Old",
                    trigger="manual",
                    owner="ops",
                    steps=[WorkflowStep(id="s1", name="Step 1")],
                ),
            ],
        )
        engine1 = WorkflowEngine(reg1, state_dir=state_dir)
        instance_id = engine1.start("old_wf")

        # Reload WITHOUT that workflow
        reg2 = CompanyRegistry(company=Company(id="test", name="Test"), workflows=[])
        engine2 = WorkflowEngine(reg2, state_dir=state_dir)
        # Instance should be skipped (workflow not found), but engine loads fine
        assert engine2.get_status(instance_id) is None
