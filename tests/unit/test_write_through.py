"""Tests for the SQLite write-through mirror (Sprint 2, S2.1).

Runtime components (MessageBus, AuditWriter, CostTracker) mirror their
mutations into the SQLite data layer when a usable database is supplied,
while keeping the legacy file path as primary and fully working when no
database is present.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_company.audit.events import AuditEvent, AuditEventType
from ai_company.audit.writer import AuditWriter
from ai_company.data import (
    AuditStore,
    CostAnalytics,
    TaskStore,
    init_database,
)
from ai_company.llm.cost_tracker import CostTracker
from ai_company.models.task import Task
from ai_company.orchestrator.message_bus import MessageBus


@pytest.fixture(autouse=True)
def _anchor_data_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Anchor DASHBOARD_DATA_DIR so a default-constructed MessageBus (e.g.
    the executor's internal bus) stays in the per-test tmp dir instead of
    the real project ``.opencode`` directory."""
    monkeypatch.setenv("DASHBOARD_DATA_DIR", str(tmp_path))


@pytest.fixture
def db(tmp_path: Path):
    database = init_database(tmp_path / "ai_company.db")
    yield database
    database.close()


def _make_task(task_id: str = "task-001") -> Task:
    return Task(
        id=task_id,
        name="Mirror test",
        sender_id="human-ceo",
        receiver_id="cto",
        instruction="Do the thing",
        status="pending",
    )


class TestMessageBusWriteThrough:
    def test_send_task_mirrors_to_sqlite(self, tmp_path: Path, db) -> None:
        bus = MessageBus(str(tmp_path / "inbox.json"), database=db)
        bus.send_task(_make_task())

        store = TaskStore(db)
        mirrored = store.get_task_by_id("task-001")
        assert mirrored is not None
        assert mirrored.receiver_id == "cto"

        # File path remains the primary store.
        inbox = json.loads((tmp_path / "inbox.json").read_text(encoding="utf-8"))
        assert len(inbox) == 1

    def test_update_status_mirrors_to_sqlite(self, tmp_path: Path, db) -> None:
        bus = MessageBus(str(tmp_path / "inbox.json"), database=db)
        bus.send_task(_make_task())

        updated = bus.update_task_status("task-001", "completed", result="done")
        assert updated is not None
        assert updated.status.value == "completed"

        store = TaskStore(db)
        mirrored = store.get_task_by_id("task-001")
        assert mirrored is not None
        assert mirrored.status.value == "completed"

    def test_delete_task_mirrors_to_sqlite(self, tmp_path: Path, db) -> None:
        bus = MessageBus(str(tmp_path / "inbox.json"), database=db)
        bus.send_task(_make_task())
        assert TaskStore(db).get_task_by_id("task-001") is not None

        deleted = bus.delete_task("task-001")
        assert deleted is not None
        assert TaskStore(db).get_task_by_id("task-001") is None

    def test_without_database_writes_file_only(self, tmp_path: Path, db) -> None:
        bus = MessageBus(str(tmp_path / "inbox.json"))
        bus.send_task(_make_task())

        # No mirror happened: SQLite stays empty.
        assert TaskStore(db).get_all_tasks() == []
        assert len(json.loads((tmp_path / "inbox.json").read_text(encoding="utf-8"))) == 1


class TestAuditWriterWriteThrough:
    def test_write_mirrors_to_sqlite(self, tmp_path: Path, db) -> None:
        writer = AuditWriter(str(tmp_path / "audit.jsonl"), database=db)
        event = AuditEvent(
            event_type=AuditEventType.TOOL_CALL,
            agent_id="cto",
            task_id="task-001",
            tool="bash",
        )
        writer.write(event)

        assert AuditStore(db).count() == 1
        # JSONL primary store still written.
        assert (tmp_path / "audit.jsonl").exists()

    def test_write_batch_mirrors_to_sqlite(self, tmp_path: Path, db) -> None:
        writer = AuditWriter(str(tmp_path / "audit.jsonl"), database=db)
        events = [
            AuditEvent(event_type=AuditEventType.TASK_CREATED, agent_id="ceo", task_id="t-1"),
            AuditEvent(event_type=AuditEventType.TASK_COMPLETED, agent_id="cto", task_id="t-1"),
        ]
        writer.write_batch(events)

        assert AuditStore(db).count() == 2

    def test_without_database_writes_file_only(self, tmp_path: Path, db) -> None:
        writer = AuditWriter(str(tmp_path / "audit.jsonl"))
        writer.write(AuditEvent(event_type=AuditEventType.TOOL_CALL, agent_id="cto", task_id="t-1"))

        assert AuditStore(db).count() == 0
        assert (tmp_path / "audit.jsonl").exists()


class TestCostTrackerWriteThrough:
    def test_record_usage_mirrors_to_sqlite(self, tmp_path: Path, db) -> None:
        tracker = CostTracker(
            results_dir=str(tmp_path / "results"),
            database=db,
            export_path=str(tmp_path / "orchestrator" / "cost_tracker.json"),
        )
        record = tracker.record_usage(
            model="gpt-4o-mini",
            provider="test-provider",
            agent_name="cto",
            task_id="task-001",
            prompt_tokens=100,
            completion_tokens=50,
        )

        analytics = CostAnalytics(db)
        assert analytics.total_records() == 1
        assert analytics.get_task_total("task-001") == record.cost_usd

        # JSONL primary store still written.
        log_path = tmp_path / "results" / "cost_log.jsonl"
        assert log_path.exists()
        assert len(log_path.read_text(encoding="utf-8").strip().splitlines()) == 1

    def test_without_database_writes_file_only(self, tmp_path: Path, db) -> None:
        tracker = CostTracker(
            results_dir=str(tmp_path / "results"),
            export_path=str(tmp_path / "orchestrator" / "cost_tracker.json"),
        )
        tracker.record_usage(
            model="gpt-4o-mini",
            provider="test-provider",
            agent_name="cto",
            task_id="task-001",
            prompt_tokens=100,
            completion_tokens=50,
        )

        assert CostAnalytics(db).total_records() == 0
        assert (tmp_path / "results" / "cost_log.jsonl").exists()


class TestExecutorWiring:
    def test_executor_passes_database_to_components(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.executor.loop import Executor

        db = init_database(tmp_path / "ai_company.db")
        try:
            executor = Executor(
                config_path=str(tmp_path / "company" / "models.yaml"),
                registry_path=str(tmp_path / "company" / "agent-registry.json"),
                agents_dir=str(tmp_path / ".opencode" / "agents"),
                results_dir=str(tmp_path / "results"),
                database=db,
            )

            # MessageBus and CostTracker mirrors are armed.
            assert executor.bus._task_store is not None
            assert executor.cost_tracker._cost_analytics is not None

            # A task sent through the wired bus lands in SQLite.
            executor.bus.send_task(_make_task("task-exec"))
            assert TaskStore(db).get_task_by_id("task-exec") is not None
        finally:
            db.close()

    def test_executor_without_database_keeps_file_only(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _setup_executor_files(tmp_path)
        _create_agent_spec(tmp_path, "test-agent")

        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )

        assert executor.bus._task_store is None
        assert executor.cost_tracker._cost_analytics is None


# ── Helpers (mirror the minimal fixtures from test_executor.py) ──────


def _setup_executor_files(tmp_path: Path) -> None:
    _setup_model_files(tmp_path)
    (tmp_path / ".opencode").mkdir(exist_ok=True)
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / "orchestrator" / "approvals.yaml").write_text("requests: []", encoding="utf-8")


def _setup_model_files(tmp_path: Path) -> None:
    models = {
        "providers": {
            "fast": {"provider": "opencode", "model": "big-pickle"},
            "standard": {"provider": "opencode", "model": "big-pickle"},
            "premium": {"provider": "opencode", "model": "big-pickle"},
        },
        "tiers": {
            "fast": {
                "description": "Fast",
                "providers": [{"provider": "opencode", "model": "big-pickle"}],
            },
            "standard": {
                "description": "Standard",
                "providers": [{"provider": "opencode", "model": "big-pickle"}],
            },
            "premium": {
                "description": "Premium",
                "providers": [{"provider": "opencode", "model": "big-pickle"}],
            },
        },
        "routing": [
            {"agent_type": "Board", "tier": "fast"},
            {"agent_type": "Executive", "tier": "standard"},
            {"agent_type": "Specialist", "tier": "standard"},
        ],
    }
    (tmp_path / "company").mkdir(exist_ok=True)
    (tmp_path / "company" / "models.yaml").write_text(json.dumps(models), encoding="utf-8")


def _create_agent_spec(tmp_path: Path, agent_name: str) -> None:
    agents_dir = tmp_path / ".opencode" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    spec = f"""\
---
name: {agent_name}
description: A test agent
tools: ["read", "write", "execute"]
mode: subagent
permission:
  read: allow
  write: allow
---

# Test Agent

## Identity

Type: Specialist

Department: Test

Reports To: ceo

---

## Mission

Execute test tasks.
"""
    (agents_dir / f"{agent_name}.md").write_text(spec, encoding="utf-8")
