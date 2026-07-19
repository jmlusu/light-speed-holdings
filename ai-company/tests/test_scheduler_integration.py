"""Tests for scheduler integration with the executor and message bus."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_company.orchestrator.message_bus import MessageBus
from ai_company.orchestrator.scheduler import Scheduler


class TestSchedulerPendingTasks:
    """Tests for create_pending_tasks()."""

    def test_creates_tasks_from_due_scheduled_items(self, tmp_path: Path) -> None:
        config_path = tmp_path / "scheduler.yaml"
        scheduler = Scheduler(config_path=str(config_path))
        bus = MessageBus(storage_path=str(tmp_path / ".opencode" / "inbox.json"))

        # Add a scheduled task that is already due (next_run in the past)
        scheduler.add_task(
            task_id="s-1",
            name="Daily Report",
            interval_minutes=60,
            task_template={
                "receiver_id": "lead-backend",
                "instruction": "Generate daily report",
                "priority": "high",
            },
        )
        # Force it to be due now
        scheduler.tasks[0].next_run = datetime.now() - timedelta(minutes=1)
        scheduler._save_config()

        created = scheduler.create_pending_tasks(bus)
        assert len(created) == 1

        # Verify the task was written to the inbox
        inbox = json.loads((tmp_path / ".opencode" / "inbox.json").read_text(encoding="utf-8"))
        assert len(inbox) == 1
        task = inbox[0]
        assert task["sender_id"] == "scheduler"
        assert task["receiver_id"] == "lead-backend"
        assert task["instruction"] == "Generate daily report"
        assert task["priority"] == "high"
        assert task["status"] == "pending"

    def test_creates_multiple_tasks(self, tmp_path: Path) -> None:
        config_path = tmp_path / "scheduler.yaml"
        scheduler = Scheduler(config_path=str(config_path))
        bus = MessageBus(storage_path=str(tmp_path / ".opencode" / "inbox.json"))

        for i in range(3):
            scheduler.add_task(
                task_id=f"s-{i}",
                name=f"Task {i}",
                interval_minutes=60,
                task_template={"receiver_id": "test-agent", "instruction": f"Do {i}"},
            )
            scheduler.tasks[i].next_run = datetime.now() - timedelta(minutes=1)
        scheduler._save_config()

        created = scheduler.create_pending_tasks(bus)
        assert len(created) == 3

        inbox = json.loads((tmp_path / ".opencode" / "inbox.json").read_text(encoding="utf-8"))
        assert len(inbox) == 3

    def test_skips_disabled_tasks(self, tmp_path: Path) -> None:
        config_path = tmp_path / "scheduler.yaml"
        scheduler = Scheduler(config_path=str(config_path))
        bus = MessageBus(storage_path=str(tmp_path / ".opencode" / "inbox.json"))

        scheduler.add_task(
            task_id="s-disabled",
            name="Disabled Task",
            interval_minutes=60,
            task_template={"receiver_id": "test-agent", "instruction": "Should not run"},
        )
        scheduler.tasks[0].enabled = False
        scheduler.tasks[0].next_run = datetime.now() - timedelta(minutes=1)
        scheduler._save_config()

        created = scheduler.create_pending_tasks(bus)
        assert len(created) == 0

        inbox = json.loads((tmp_path / ".opencode" / "inbox.json").read_text(encoding="utf-8"))
        assert len(inbox) == 0

    def test_uses_default_receiver_and_instruction(self, tmp_path: Path) -> None:
        config_path = tmp_path / "scheduler.yaml"
        scheduler = Scheduler(config_path=str(config_path))
        bus = MessageBus(storage_path=str(tmp_path / ".opencode" / "inbox.json"))

        scheduler.add_task(
            task_id="s-defaults",
            name="Defaults Task",
            interval_minutes=60,
            task_template={},
        )
        scheduler.tasks[0].next_run = datetime.now() - timedelta(minutes=1)
        scheduler._save_config()

        created = scheduler.create_pending_tasks(bus)
        assert len(created) == 1

        inbox = json.loads((tmp_path / ".opencode" / "inbox.json").read_text(encoding="utf-8"))
        task = inbox[0]
        assert task["receiver_id"] == "chief-of-staff"
        assert task["instruction"] == "Scheduled: Defaults Task"


class TestSchedulerMarkCompleted:
    """Tests for mark_completed()."""

    def test_updates_last_run_and_next_run(self, tmp_path: Path) -> None:
        config_path = tmp_path / "scheduler.yaml"
        scheduler = Scheduler(config_path=str(config_path))

        scheduler.add_task(
            task_id="s-complete",
            name="Complete Me",
            interval_minutes=30,
            task_template={},
        )

        scheduler.mark_completed("s-complete")

        task = scheduler.tasks[0]
        assert task.last_run is not None
        assert task.last_run > datetime.now() - timedelta(seconds=5)
        assert task.next_run is not None
        assert task.next_run > datetime.now() + timedelta(minutes=25)

    def test_persists_to_yaml(self, tmp_path: Path) -> None:
        config_path = tmp_path / "scheduler.yaml"
        scheduler = Scheduler(config_path=str(config_path))

        scheduler.add_task(
            task_id="s-persist",
            name="Persist Me",
            interval_minutes=60,
            task_template={},
        )
        scheduler.mark_completed("s-persist")

        # Reload and verify
        scheduler2 = Scheduler(config_path=str(config_path))
        task = scheduler2.tasks[0]
        assert task.last_run is not None
        assert task.next_run is not None


class TestSchedulerGetPending:
    """Tests for get_pending_tasks()."""

    def test_returns_only_enabled_and_due_tasks(self, tmp_path: Path) -> None:
        config_path = tmp_path / "scheduler.yaml"
        scheduler = Scheduler(config_path=str(config_path))

        # Due and enabled
        scheduler.add_task(
            task_id="s-due",
            name="Due Task",
            interval_minutes=60,
            task_template={},
        )
        scheduler.tasks[0].next_run = datetime.now() - timedelta(minutes=1)

        # Not due yet
        scheduler.add_task(
            task_id="s-future",
            name="Future Task",
            interval_minutes=60,
            task_template={},
        )
        scheduler.tasks[1].next_run = datetime.now() + timedelta(hours=1)

        # Due but disabled
        scheduler.add_task(
            task_id="s-disabled",
            name="Disabled Task",
            interval_minutes=60,
            task_template={},
        )
        scheduler.tasks[2].enabled = False
        scheduler.tasks[2].next_run = datetime.now() - timedelta(minutes=1)

        scheduler._save_config()

        pending = scheduler.get_pending_tasks()
        assert len(pending) == 1
        assert pending[0].id == "s-due"

    def test_no_tasks_returns_empty(self, tmp_path: Path) -> None:
        config_path = tmp_path / "scheduler.yaml"
        scheduler = Scheduler(config_path=str(config_path))

        pending = scheduler.get_pending_tasks()
        assert pending == []


class TestSchedulerFullCycle:
    """End-to-end: add scheduled task -> tick -> verify task created in inbox."""

    def test_full_cycle_add_schedule_tick_inbox(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _setup_test_files(tmp_path)

        # Set up scheduler with a due task — use the default config path
        # that the Executor's Scheduler will also read from
        config_path = tmp_path / "orchestrator" / "scheduler.yaml"
        scheduler = Scheduler(config_path=str(config_path))
        scheduler.add_task(
            task_id="s-cycle",
            name="Cycle Report",
            interval_minutes=60,
            task_template={
                "receiver_id": "test-agent",
                "instruction": "Run cycle report",
                "priority": "medium",
            },
        )
        scheduler.tasks[0].next_run = datetime.now() - timedelta(minutes=1)
        scheduler._save_config()

        # Create executor and tick
        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )

        mock_result = _FakeLoopResult(
            final_response="Cycle report done.",
            iterations=1,
            done=True,
        )
        executor.agent_loop.run = MagicMock(return_value=mock_result)

        executor.tick()

        # Verify scheduler task was converted to inbox task and processed
        inbox = json.loads(
            (tmp_path / ".opencode" / "inbox.json").read_text(encoding="utf-8")
        )
        # The task was created by scheduler and processed by executor
        cycle_tasks = [t for t in inbox if t["sender_id"] == "scheduler"]
        assert len(cycle_tasks) == 1
        assert cycle_tasks[0]["status"] == "completed"

        # Verify scheduler marks it completed (next_run rescheduled)
        scheduler2 = Scheduler(config_path=str(config_path))
        s_task = scheduler2.tasks[0]
        assert s_task.last_run is not None
        assert s_task.next_run > datetime.now() + timedelta(minutes=50)

    def test_tick_does_not_duplicate_non_due_tasks(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _setup_test_files(tmp_path)

        config_path = tmp_path / "scheduler.yaml"
        scheduler = Scheduler(config_path=str(config_path))
        scheduler.add_task(
            task_id="s-future-cycle",
            name="Future Cycle",
            interval_minutes=60,
            task_template={"receiver_id": "test-agent", "instruction": "Not yet"},
        )
        scheduler.tasks[0].next_run = datetime.now() + timedelta(hours=1)
        scheduler._save_config()

        from ai_company.executor.loop import Executor

        executor = Executor(
            config_path=str(tmp_path / "company" / "models.yaml"),
            registry_path=str(tmp_path / "company" / "agent-registry.json"),
            agents_dir=str(tmp_path / ".opencode" / "agents"),
            results_dir=str(tmp_path / "results"),
        )
        executor.agent_loop.run = MagicMock()

        count = executor.tick()
        assert count == 0
        executor.agent_loop.run.assert_not_called()


# ── Helpers ─────────────────────────────────────────────────────────


class _FakeLoopResult:
    def __init__(
        self,
        final_response: str = "Done.",
        iterations: int = 1,
        done: bool = True,
        error: str = "",
    ) -> None:
        self.final_response = final_response
        self.iterations = iterations
        self.tool_results: list = []
        self.total_prompt_tokens = 100
        self.total_completion_tokens = 50
        self.total_cost_usd = 0.001
        self.done = done
        self.error = error

    @property
    def total_tokens(self) -> int:
        return self.total_prompt_tokens + self.total_completion_tokens


def _setup_test_files(tmp_path: Path) -> None:
    (tmp_path / "company").mkdir(exist_ok=True)
    models = {
        "providers": {
            "opencode": {
                "backend": "openai_compatible",
                "default_model": "big-pickle",
                "api_base": "https://opencode.ai/api/v1",
            },
        },
        "tiers": {
            "fast": {
                "description": "Fast",
                "providers": [{"provider": "opencode", "model": "big-pickle"}],
            },
        },
        "routing": [
            {"agent_type": "Executive", "tier": "fast"},
            {"agent_type": "Specialist", "tier": "fast"},
        ],
    }
    (tmp_path / "company" / "models.yaml").write_text(
        json.dumps(models), encoding="utf-8"
    )

    registry = [
        {
            "name": "test-agent",
            "role": "Test Agent",
            "type": "Specialist",
            "department": "Test",
            "reportsTo": "ceo",
            "directReports": [],
            "description": "A test agent",
            "tools": ["read", "write"],
            "permission": "Execute",
        }
    ]
    (tmp_path / "company" / "agent-registry.json").write_text(
        json.dumps(registry), encoding="utf-8"
    )

    (tmp_path / ".opencode").mkdir(exist_ok=True)
    (tmp_path / ".opencode" / "inbox.json").write_text("[]", encoding="utf-8")
    (tmp_path / "orchestrator").mkdir(exist_ok=True)
    (tmp_path / "orchestrator" / "approvals.yaml").write_text(
        "requests: []", encoding="utf-8"
    )

    agents_dir = tmp_path / ".opencode" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    spec = """\
---
name: test-agent
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

---

## Responsibilities

- Read files
- Write files
- Execute commands

---

## Operating Guidelines

Be thorough.
"""
    (agents_dir / "test-agent.md").write_text(spec, encoding="utf-8")
