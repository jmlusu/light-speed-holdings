"""Tests for the daily briefing generator."""

from __future__ import annotations

import json
from pathlib import Path

from ai_company.models.task import Task, TaskStatus
from ai_company.orchestrator.briefing import BriefingGenerator
from ai_company.orchestrator.message_bus import MessageBus


def _write_registry(path: Path, agents: list[dict]) -> None:
    path.write_text(json.dumps(agents), encoding="utf-8")


def _make_bus(tmp_path: Path) -> MessageBus:
    return MessageBus(storage_path=str(tmp_path / "inbox.json"))


class TestBriefingGenerator:
    def test_generates_empty_briefing_when_no_data(self, tmp_path: Path) -> None:
        generator = BriefingGenerator(
            registry_path=str(tmp_path / "registry.json"),
            output_path=str(tmp_path / "briefing.md"),
            bus=_make_bus(tmp_path),
        )
        active, pending = generator.generate()
        assert (active, pending) == (0, 0)
        content = (tmp_path / "briefing.md").read_text(encoding="utf-8")
        assert "# Daily Executive Briefing" in content
        assert "No pending tasks." in content

    def test_generates_briefing_with_pending_task(self, tmp_path: Path) -> None:
        _write_registry(
            tmp_path / "registry.json",
            [
                {
                    "name": "lead-backend",
                    "role": "Lead Backend Engineer",
                    "department": "Engineering",
                    "reportsTo": "CTO",
                }
            ],
        )
        bus = _make_bus(tmp_path)
        bus.send_task(
            Task(
                id="t-1",
                sender_id="ceo",
                receiver_id="lead-backend",
                instruction="Review the auth refactor",
            )
        )
        generator = BriefingGenerator(
            registry_path=str(tmp_path / "registry.json"),
            output_path=str(tmp_path / "briefing.md"),
            bus=bus,
        )
        active, pending = generator.generate()
        assert (active, pending) == (1, 1)
        content = (tmp_path / "briefing.md").read_text(encoding="utf-8")
        assert "## Action Required: Lead Backend Engineer (`lead-backend`)" in content
        assert "**Department:** Engineering | **Reports To:** CTO" in content
        assert "TASK ID: t-1" in content
        assert "FROM: ceo" in content
        assert "INSTRUCTION: Review the auth refactor" in content

    def test_completed_tasks_are_excluded(self, tmp_path: Path) -> None:
        _write_registry(
            tmp_path / "registry.json",
            [{"name": "lead-backend", "role": "Lead Backend Engineer"}],
        )
        bus = _make_bus(tmp_path)
        bus.send_task(
            Task(
                id="t-1",
                sender_id="ceo",
                receiver_id="lead-backend",
                instruction="Old task",
                status=TaskStatus.COMPLETED,
            )
        )
        generator = BriefingGenerator(
            registry_path=str(tmp_path / "registry.json"),
            output_path=str(tmp_path / "briefing.md"),
            bus=bus,
        )
        active, pending = generator.generate()
        assert (active, pending) == (0, 0)
        content = (tmp_path / "briefing.md").read_text(encoding="utf-8")
        assert "No pending tasks." in content

    def test_pending_task_for_unknown_agent_is_skipped(self, tmp_path: Path) -> None:
        _write_registry(
            tmp_path / "registry.json",
            [{"name": "lead-backend", "role": "Lead Backend Engineer"}],
        )
        bus = _make_bus(tmp_path)
        bus.send_task(
            Task(
                id="t-1",
                sender_id="ceo",
                receiver_id="ghost-agent",
                instruction="Orphan task",
            )
        )
        generator = BriefingGenerator(
            registry_path=str(tmp_path / "registry.json"),
            output_path=str(tmp_path / "briefing.md"),
            bus=bus,
        )
        active, pending = generator.generate()
        assert (active, pending) == (0, 1)

    def test_multiple_agents_and_tasks_counted(self, tmp_path: Path) -> None:
        _write_registry(
            tmp_path / "registry.json",
            [
                {"name": "lead-backend", "role": "Lead Backend Engineer"},
                {"name": "lead-security", "role": "Lead Security Engineer"},
            ],
        )
        bus = _make_bus(tmp_path)
        bus.send_task(Task(id="t-1", sender_id="ceo", receiver_id="lead-backend", instruction="A"))
        bus.send_task(Task(id="t-2", sender_id="ceo", receiver_id="lead-backend", instruction="B"))
        bus.send_task(Task(id="t-3", sender_id="ceo", receiver_id="lead-security", instruction="C"))
        generator = BriefingGenerator(
            registry_path=str(tmp_path / "registry.json"),
            output_path=str(tmp_path / "briefing.md"),
            bus=bus,
        )
        active, pending = generator.generate()
        assert (active, pending) == (2, 3)
        content = (tmp_path / "briefing.md").read_text(encoding="utf-8")
        assert content.count("## Action Required:") == 2

    def test_creates_output_directory(self, tmp_path: Path) -> None:
        out = tmp_path / "nested" / "briefing.md"
        generator = BriefingGenerator(
            registry_path=str(tmp_path / "registry.json"),
            output_path=str(out),
            bus=_make_bus(tmp_path),
        )
        generator.generate()
        assert out.exists()
