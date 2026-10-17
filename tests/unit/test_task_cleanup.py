"""Tests for demo/test task detection, cleanup, and API filtering.

Covers the refined detection contract:
  - task id contains ``proj-acme-chatbot`` (Acme demo) OR
  - instruction contains ``proj-acme-chatbot`` OR
  - instruction starts with ``Test `` (capital T, trailing space) OR
  - task id starts with ``test-``/``verify-`` (lowercase)

Deliberately NOT a marker: the task receiver/agent name. Routing a real
task to the real ``test-agent`` receiver is legitimate and must not flag
the task as demo/test.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from ai_company.data.database import Database
from ai_company.data.task_store import TaskStore
from ai_company.models.task import Task, TaskPriority, TaskStatus


@pytest.fixture
def db(tmp_path: Path) -> Database:
    """Create a temporary database."""
    database = Database(tmp_path / "cleanup_tasks.db")
    database.init_schema()
    yield database
    database.close()


@pytest.fixture
def store(db: Database) -> TaskStore:
    """Create a TaskStore backed by the test database."""
    return TaskStore(db)


def _task(
    task_id: str = "real-task-001",
    instruction: str = "Gather requirements and draft the proposal",
    receiver: str = "chief-of-staff",
    sender: str = "human-ceo",
    **overrides: object,
) -> Task:
    """Helper to build a Task with realistic defaults."""
    return Task(
        id=task_id,
        sender_id=sender,
        receiver_id=receiver,
        instruction=instruction,
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM,
        **overrides,
    )


# ═══════════════════════════════════════════════════════════════════════
# is_test_task — detection contract
# ═══════════════════════════════════════════════════════════════════════


class TestIsTestTask:
    """Verify the refined demo/test markers are the only detection heuristic."""

    def test_marks_acme_demo_when_id_mentions_project(self) -> None:
        assert (
            TaskStore.is_test_task({"id": "proj-acme-chatbot-001", "instruction": "Build backend"})
            is True
        )

    def test_marks_acme_demo_when_instruction_mentions_project(self) -> None:
        assert (
            TaskStore.is_test_task(
                {"id": "uuid-1234", "instruction": "[proj-acme-chatbot-001] QA review"}
            )
            is True
        )

    def test_marks_test_instruction_prefix(self) -> None:
        assert (
            TaskStore.is_test_task({"id": "uuid-1234", "instruction": "Test placeholder task"})
            is True
        )

    @pytest.mark.parametrize("task_id", ["test-0001", "test-dummy", "verify-test-2", "verify-1"])
    def test_marks_test_and_verify_id_prefixes(self, task_id: str) -> None:
        assert TaskStore.is_test_task({"id": task_id, "instruction": "Do real work"}) is True

    def test_marks_task_with_multiple_overlapping_markers_once(self) -> None:
        task = {
            "id": "test-0001",
            "instruction": "Test proj-acme-chatbot demo",
        }
        assert TaskStore.is_test_task(task) is True

    # ── Refined negatives: must NOT be flagged ────────────────────────

    def test_not_flagged_when_routed_to_real_test_agent(self) -> None:
        """A real task routed to the `test-agent` receiver is legitimate."""
        task = {
            "id": "uuid-1234",
            "receiver_id": "test-agent",
            "instruction": "Ship the new analytics dashboard",
        }
        assert TaskStore.is_test_task(task) is False

    def test_not_flagged_when_instruction_mentions_lowercase_test(self) -> None:
        """Lowercase 'test the X' is real work, not the `Test ` marker."""
        assert (
            TaskStore.is_test_task(
                {"id": "uuid-1", "instruction": "test the new payment integration"}
            )
            is False
        )

    def test_not_flagged_for_testing_verb_instruction(self) -> None:
        """'Testing...' does not start with `Test ` (no trailing space)."""
        assert (
            TaskStore.is_test_task({"id": "uuid-1", "instruction": "Testing the new module"})
            is False
        )

    def test_not_flagged_for_test_id_with_underscore(self) -> None:
        """Only `test-`/`verify-` prefixes count, not bare 'test' substrings."""
        assert TaskStore.is_test_task({"id": "test_agent_work", "instruction": "Do work"}) is False
        assert TaskStore.is_test_task({"id": "contest-entry", "instruction": "Do work"}) is False

    def test_not_flagged_for_capital_T_dash_id(self) -> None:
        """Prefix matching is lowercase-only per the contract."""
        assert TaskStore.is_test_task({"id": "Test-Marker", "instruction": "Do work"}) is False

    def test_not_flagged_for_real_instructions(self) -> None:
        """A set of realistic instructions must never be marked dummy."""
        realistic = [
            "Run the end-to-end acceptance suite for the deploy",
            "Write comprehensive unit tests for the new parser",
            "Verify the rollout is clean before Friday",
            "Review PR #42 and merge if CI passes",
            "Deploy the chatbot to staging and monitor initial usage",
        ]
        for instruction in realistic:
            assert (
                TaskStore.is_test_task(
                    {"id": f"task-{realistic.index(instruction)}", "instruction": instruction}
                )
                is False
            ), instruction


# ═══════════════════════════════════════════════════════════════════════
# TaskStore.cleanup_test_tasks / test_task_breakdown / purge_all_tasks
# ═══════════════════════════════════════════════════════════════════════


class TestCleanupTestTasks:
    """Verify cleanup removes only demo/test rows and keeps real ones."""

    def _seed(
        self,
        store: TaskStore,
        *,
        acme_ids: int = 2,
        acme_instr: int = 1,
        test_instr: int = 2,
        test_ids: int = 1,
        verify_ids: int = 1,
        real: int = 3,
    ) -> None:
        for i in range(acme_ids):
            store.send_task(
                _task(task_id=f"proj-acme-chatbot-{i:03d}", instruction="Build the chatbot module")
            )
        for i in range(acme_instr):
            store.send_task(
                _task(
                    task_id=f"uuid-acme-{i}",
                    instruction="[proj-acme-chatbot-001] Review Acme Corp deliverable",
                )
            )
        for i in range(test_instr):
            store.send_task(
                _task(task_id=f"uuid-test-{i}", instruction=f"Test scratch task number {i}")
            )
        for i in range(test_ids):
            store.send_task(_task(task_id=f"test-{i:04d}", instruction="Probe the endpoint"))
        for i in range(verify_ids):
            store.send_task(_task(task_id=f"verify-{i:04d}", instruction="Smoke run"))
        for i in range(real):
            store.send_task(
                _task(
                    task_id=f"real-task-{i:04d}",
                    instruction=f"Implement real feature {i}",
                    receiver="test-agent" if i == 0 else "chief-of-staff",
                )
            )

    def test_breakdown_counts_classes_and_overlap(self, store: TaskStore) -> None:
        # One task matches BOTH the acme marker and the 'Test ' prefix.
        store.send_task(
            _task(
                task_id="proj-acme-chatbot-overlap",
                instruction="Test proj-acme-chatbot overlap",
            )
        )
        self._seed(store, acme_ids=0, acme_instr=0, test_instr=0, test_ids=0, verify_ids=0, real=0)

        counts = store.test_task_breakdown()
        assert counts["acme_demo"] == 1
        assert counts["test_instruction"] == 1
        assert counts["test_id"] == 0
        assert counts["total"] == 1  # one distinct row despite two classes

    def test_cleanup_removes_matching_rows_and_keeps_real(self, store: TaskStore) -> None:
        self._seed(store)
        before = store.count()
        assert before == 2 + 1 + 2 + 1 + 1 + 3

        counts = store.test_task_breakdown()
        assert counts["total"] == 7
        assert counts["acme_demo"] == 3
        assert counts["test_instruction"] == 2
        assert counts["test_id"] == 2  # test-0000 + verify-0000

        deleted = store.cleanup_test_tasks()
        assert deleted == 7
        assert store.count() == 3

        remaining = [t.id for t in store.get_all_tasks()]
        assert set(remaining) == {"real-task-0000", "real-task-0001", "real-task-0002"}
        # The real task routed to `test-agent` (real-task-0000) survives cleanup.
        assert [t.id for t in store.get_inbox("test-agent")] == ["real-task-0000"]

    def test_cleanup_keeps_test_agent_routed_real_task(self, store: TaskStore) -> None:
        """A real task routed to `test-agent` survives cleanup."""
        store.send_task(
            _task(task_id="real-42", receiver="test-agent", instruction="Audit the deploy")
        )
        store.send_task(_task(task_id="test-42", instruction="Test scratch row"))

        assert store.test_task_breakdown()["total"] == 1
        assert store.cleanup_test_tasks() == 1
        tasks = store.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == "real-42"
        assert tasks[0].receiver_id == "test-agent"

    def test_cleanup_does_not_remove_lowercase_test_instruction(self, store: TaskStore) -> None:
        """'test the endpoint' (lowercase) is real work and survives cleanup."""
        store.send_task(_task(task_id="real-ssh", instruction="test the new SSH key rotation"))
        assert store.test_task_breakdown()["total"] == 0
        assert store.cleanup_test_tasks() == 0
        assert store.count() == 1

    def test_cleanup_is_idempotent_on_clean_db(self, store: TaskStore) -> None:
        assert store.cleanup_test_tasks() == 0
        assert store.test_task_breakdown()["total"] == 0

    def test_purge_all_tasks(self, store: TaskStore) -> None:
        self._seed(store)
        assert store.purge_all_tasks() == 10
        assert store.count() == 0


# ═══════════════════════════════════════════════════════════════════════
# dashboard.api._read_all_tasks(include_test=...)
# ═══════════════════════════════════════════════════════════════════════


@pytest.fixture()
def api_module():
    """The dashboard api module (imported lazily so app setup stays optional)."""
    from ai_company.dashboard import api as dash_api

    return dash_api


def _task_dict(task_id: str, instruction: str, receiver: str = "chief-of-staff") -> dict[str, str]:
    return {"id": task_id, "instruction": instruction, "receiver_id": receiver}


class TestReadAllTasksFilter:
    """Verify _read_all_tasks default filtering and include_test override."""

    def test_default_filters_demo_and_test_but_keeps_test_agent_task(
        self, api_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import ai_company.dashboard.data_service as data_service

        tasks = [
            _task_dict("proj-acme-chatbot-001", "Build chatbot"),
            _task_dict("uuid-1", "Test scratch task"),
            _task_dict("test-0001", "Ping backend"),
            _task_dict("real-a", "Implement invoicing module", receiver="test-agent"),
            _task_dict("real-b", "Prepare board pack"),
        ]
        monkeypatch.setattr(data_service, "get_all_tasks", lambda *a, **k: tasks)

        filtered = api_module._read_all_tasks()
        assert {t["id"] for t in filtered} == {"real-a", "real-b"}

        included = api_module._read_all_tasks(include_test=True)
        assert {t["id"] for t in included} == {
            "proj-acme-chatbot-001",
            "uuid-1",
            "test-0001",
            "real-a",
            "real-b",
        }

    def test_bus_fallback_is_also_filtered(
        self, api_module, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import ai_company.dashboard.data_service as data_service

        class _FakeBus:
            def get_all_tasks_raw(self) -> list[dict[str, str]]:
                return [
                    _task_dict("inbox-test-01", "Test leftover row"),
                    _task_dict("inbox-real-01", "Handle support ticket", receiver="test-agent"),
                ]

        monkeypatch.setattr(data_service, "get_all_tasks", lambda *a, **k: None)
        monkeypatch.setattr(api_module, "get_bus", lambda: _FakeBus())

        filtered = api_module._read_all_tasks()
        assert [t["id"] for t in filtered] == ["inbox-real-01"]

        included = api_module._read_all_tasks(include_test=True)
        assert {t["id"] for t in included} == {"inbox-test-01", "inbox-real-01"}

    def test_reads_through_sqlite_and_filters(
        self, api_module, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """End-to-end: a seeded SQLite DB is filtered by _read_all_tasks."""
        from ai_company.data import init_database, reset_database

        reset_database()
        db = init_database(tmp_path / "api.db")
        store = TaskStore(db)
        try:
            store.send_task(_task("proj-acme-chatbot-001", "Build chatbot"))
            store.send_task(_task("test-0001", "Ping backend"))
            store.send_task(_task("real-a", "Implement invoicing", receiver="test-agent"))

            filtered = api_module._read_all_tasks()
            assert [t["id"] for t in filtered] == ["real-a"]

            included = api_module._read_all_tasks(include_test=True)
            assert {t["id"] for t in included} == {"proj-acme-chatbot-001", "test-0001", "real-a"}
        finally:
            reset_database()


# ═══════════════════════════════════════════════════════════════════════
# GET /api/v1/tasks — default vs ?include_test=true
# ═══════════════════════════════════════════════════════════════════════


@pytest.fixture()
def api_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """TestClient isolated in a temp workspace with a seeded SQLite DB."""
    from fastapi.testclient import TestClient

    from ai_company.dashboard import api as dash_api
    from ai_company.dashboard.app import app
    from ai_company.dashboard.repository import get_state_store, reset_state_store
    from ai_company.data import init_database, reset_database

    reset_database()
    reset_state_store()
    monkeypatch.chdir(tmp_path)
    get_state_store(tmp_path)
    monkeypatch.setattr(dash_api, "_bus", None)

    db = init_database(tmp_path / "api.db")
    store = TaskStore(db)
    store.send_task(_task("proj-acme-chatbot-001", "Build chatbot module"))
    store.send_task(_task("test-0001", "Ping the backend"))
    store.send_task(_task("verify-0001", "Smoke run"))
    store.send_task(_task("uuid-1", "Test scratch instruction"))
    store.send_task(_task("real-a", "Implement invoicing module", receiver="test-agent"))
    store.send_task(_task("real-b", "Prepare CEO board pack"))

    yield TestClient(app, raise_server_exceptions=False)

    reset_database()
    reset_state_store()


class TestTasksEndpointIncludeTest:
    """Acceptance A2: default hides demo/test; include_test=true restores."""

    def test_default_hides_demo_and_test_tasks(self, api_client) -> None:
        resp = api_client.get("/api/v1/tasks")
        assert resp.status_code == 200
        ids = {t["id"] for t in resp.json()}
        assert ids == {"real-a", "real-b"}  # incl. the real test-agent-routed task

    def test_include_test_restores_them(self, api_client) -> None:
        resp = api_client.get("/api/v1/tasks", params={"include_test": "true"})
        assert resp.status_code == 200
        ids = {t["id"] for t in resp.json()}
        assert ids == {
            "proj-acme-chatbot-001",
            "test-0001",
            "verify-0001",
            "uuid-1",
            "real-a",
            "real-b",
        }

    def test_paginated_default_hides_them(self, api_client) -> None:
        resp = api_client.get("/api/v1/tasks/paginated")
        assert resp.status_code == 200
        body = resp.json()
        ids = {t["id"] for t in body["items"]}
        assert ids == {"real-a", "real-b"}
        assert body["total"] == 2

    def test_paginated_include_test_restores_them(self, api_client) -> None:
        resp = api_client.get("/api/v1/tasks/paginated", params={"include_test": "true"})
        assert resp.status_code == 200
        body = resp.json()
        ids = {t["id"] for t in body["items"]}
        assert ids == {
            "proj-acme-chatbot-001",
            "test-0001",
            "verify-0001",
            "uuid-1",
            "real-a",
            "real-b",
        }
        assert body["total"] == 6


# ═══════════════════════════════════════════════════════════════════════
# Scheduler + BaseService guards
# ═══════════════════════════════════════════════════════════════════════


class TestSchedulerGuard:
    """Scheduler refuses to enqueue tasks matching the detection contract."""

    def test_skips_test_tasks_but_sends_real_ones(self, tmp_path: Path) -> None:
        from ai_company.orchestrator.message_bus import MessageBus
        from ai_company.orchestrator.scheduler import Scheduler

        cfg = tmp_path / "scheduler.yaml"
        scheduler = Scheduler(str(cfg))
        scheduler.add_task(
            "real-job",
            "Real recurring work",
            interval_minutes=30,
            task_template={
                "receiver_id": "test-agent",
                "instruction": "Audit the deployment pipeline",
            },
        )
        scheduler.add_task(
            "demo-job",
            "Demo job",
            interval_minutes=30,
            task_template={
                "receiver_id": "chief-of-staff",
                "instruction": "Test scratch placeholder",
            },
        )
        now = datetime.now()
        for scheduled in scheduler.tasks:
            scheduled.next_run = now - timedelta(minutes=1)

        bus = MessageBus(storage_path=str(tmp_path / "inbox.json"))
        created = scheduler.create_pending_tasks(bus)

        assert len(created) == 1
        tasks = bus.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].instruction == "Audit the deployment pipeline"
        assert tasks[0].receiver_id == "test-agent"


class TestBaseServiceGuard:
    """BaseService.create_task refuses demo/test instructions."""

    def test_create_task_rejects_test_marker_and_sends_real(self, tmp_path: Path) -> None:
        from ai_company.services.base import BaseService

        sent: list[Task] = []

        class _FakeBus:
            def send_task(self, task: Task) -> None:
                sent.append(task)

            def get_pending_tasks(self) -> list[Task]:
                return []

        svc = BaseService(
            "test-dept",
            bus=_FakeBus(),  # type: ignore[arg-type]
            data_dir=str(tmp_path),
            memory_dir=str(tmp_path / "memory"),
            audit_path=str(tmp_path / "audit"),
        )

        with pytest.raises(ValueError, match="test/demo"):
            svc.create_task(receiver_id="chief-of-staff", instruction="Test scratch task")

        assert sent == []

        task = svc.create_task(
            receiver_id="test-agent",
            instruction="Implement the new reconciliation report",
        )
        assert len(sent) == 1
        assert sent[0].id == task.id
        assert sent[0].receiver_id == "test-agent"
