"""Tests for the Audit trail package."""

from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest

from ai_company.audit.events import AuditEvent, AuditEventType
from ai_company.audit.reader import AuditReader
from ai_company.audit.writer import AuditWriter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_event(**overrides: object) -> AuditEvent:
    """Return an AuditEvent with sensible defaults for testing."""
    defaults: dict[str, object] = {
        "event_type": AuditEventType.TOOL_CALL,
        "agent_id": "test-agent",
        "task_id": "task-001",
        "tool": "bash",
        "args": {"cmd": "ls"},
        "result": {"exit_code": 0},
        "metadata": {"session": "abc"},
        "severity": "info",
    }
    defaults.update(overrides)
    return AuditEvent(**defaults)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# AuditEvent tests
# ---------------------------------------------------------------------------


class TestAuditEvent:
    """Verify AuditEvent creation and validation."""

    def test_create_minimal(self) -> None:
        event = AuditEvent(
            event_type=AuditEventType.TASK_CREATED,
            agent_id="ceo",
        )
        assert event.event_type == AuditEventType.TASK_CREATED
        assert event.agent_id == "ceo"
        # Defaults
        assert event.task_id == ""
        assert event.tool is None
        assert event.args == {}
        assert event.result == {}
        assert event.metadata == {}
        assert event.severity == "info"
        # Auto-generated
        assert event.event_id  # non-empty UUID
        assert event.timestamp  # ISO 8601 string

    def test_create_full(self) -> None:
        event = _make_event(
            event_type=AuditEventType.HITL_APPROVED,
            agent_id="lead-backend",
            task_id="task-999",
            tool="editor",
            args={"path": "foo.py"},
            result={"status": "ok"},
            metadata={"round": 2},
            severity="warning",
        )
        assert event.event_type == AuditEventType.HITL_APPROVED
        assert event.task_id == "task-999"
        assert event.tool == "editor"
        assert event.args == {"path": "foo.py"}
        assert event.result == {"status": "ok"}
        assert event.metadata == {"round": 2}
        assert event.severity == "warning"

    def test_event_id_is_unique(self) -> None:
        a = AuditEvent(event_type=AuditEventType.ERROR, agent_id="a")
        b = AuditEvent(event_type=AuditEventType.ERROR, agent_id="a")
        assert a.event_id != b.event_id

    def test_timestamp_is_iso(self) -> None:
        event = AuditEvent(event_type=AuditEventType.DELEGATION, agent_id="x")
        # ISO 8601 strings contain 'T'
        assert "T" in event.timestamp

    def test_extra_fields_ignored(self) -> None:
        event = AuditEvent(
            event_type=AuditEventType.TOOL_RESULT,
            agent_id="y",
            surprise="hello",
        )
        assert not hasattr(event, "surprise")

    def test_serialization_round_trip(self) -> None:
        original = _make_event()
        data = original.model_dump()
        restored = AuditEvent.model_validate(data)
        assert original.event_id == restored.event_id
        assert original.event_type == restored.event_type
        assert original.agent_id == restored.agent_id


# ---------------------------------------------------------------------------
# AuditWriter tests
# ---------------------------------------------------------------------------


class TestAuditWriter:
    """Verify AuditWriter atomic writes and batch support."""

    def test_write_creates_file(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        writer = AuditWriter(path=log_file)
        event = _make_event()
        writer.write(event)
        assert log_file.exists()
        lines = log_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["agent_id"] == "test-agent"

    def test_write_creates_parent_dirs(self, tmp_path: Path) -> None:
        deep_path = tmp_path / "a" / "b" / "c" / "audit.jsonl"
        writer = AuditWriter(path=deep_path)
        writer.write(_make_event())
        assert deep_path.exists()

    def test_write_batch(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        writer = AuditWriter(path=log_file)
        events = [_make_event(task_id=f"t-{i}") for i in range(5)]
        writer.write_batch(events)
        lines = log_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 5

    def test_write_batch_empty(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        writer = AuditWriter(path=log_file)
        writer.write_batch([])
        assert not log_file.exists()

    def test_atomic_write_no_tmp_residue(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        writer = AuditWriter(path=log_file)
        writer.write(_make_event())
        # After write completes, no .audit-tmp-* files should remain.
        tmp_files = list(tmp_path.glob(".audit-tmp-*"))
        assert tmp_files == []

    def test_concurrent_writes(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        writer = AuditWriter(path=log_file)
        errors: list[Exception] = []

        def _write_events(agent: str, count: int) -> None:
            try:
                for i in range(count):
                    writer.write(_make_event(agent_id=agent, task_id=f"{agent}-{i}"))
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=_write_events, args=(f"agent-{j}", 10))
            for j in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        lines = log_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 40


# ---------------------------------------------------------------------------
# AuditReader tests
# ---------------------------------------------------------------------------


class TestAuditReader:
    """Verify AuditReader filtering and graceful error handling."""

    @pytest.fixture()
    def log_file(self, tmp_path: Path) -> Path:
        """Write a few diverse events and return the log path."""
        path = tmp_path / "audit.jsonl"
        writer = AuditWriter(path=path)
        events = [
            _make_event(
                event_type=AuditEventType.TOOL_CALL,
                agent_id="backend",
                task_id="t-1",
            ),
            _make_event(
                event_type=AuditEventType.TASK_COMPLETED,
                agent_id="backend",
                task_id="t-1",
            ),
            _make_event(
                event_type=AuditEventType.HITL_APPROVED,
                agent_id="frontend",
                task_id="t-2",
            ),
            _make_event(
                event_type=AuditEventType.ERROR,
                agent_id="devops",
                task_id="t-3",
                severity="error",
            ),
        ]
        writer.write_batch(events)
        return path

    def test_read_all(self, log_file: Path) -> None:
        reader = AuditReader(path=log_file)
        events = reader.read_all()
        assert len(events) == 4

    def test_read_by_task(self, log_file: Path) -> None:
        reader = AuditReader(path=log_file)
        events = reader.read_by_task("t-1")
        assert len(events) == 2
        assert all(e.task_id == "t-1" for e in events)

    def test_read_by_agent(self, log_file: Path) -> None:
        reader = AuditReader(path=log_file)
        events = reader.read_by_agent("backend")
        assert len(events) == 2
        assert all(e.agent_id == "backend" for e in events)

    def test_read_by_type(self, log_file: Path) -> None:
        reader = AuditReader(path=log_file)
        events = reader.read_by_type("tool_call")
        assert len(events) == 1
        assert events[0].event_type == AuditEventType.TOOL_CALL

    def test_read_by_type_invalid(self, log_file: Path) -> None:
        reader = AuditReader(path=log_file)
        with pytest.raises(ValueError, match="tool_callkk"):
            reader.read_by_type("tool_callkk")

    def test_read_since(self, log_file: Path) -> None:
        reader = AuditReader(path=log_file)
        all_events = reader.read_all()
        # Use the timestamp of the third event as the cutoff.
        cutoff = all_events[2].timestamp
        recent = reader.read_since(cutoff)
        assert len(recent) >= 2

    def test_empty_file(self, tmp_path: Path) -> None:
        path = tmp_path / "empty.jsonl"
        path.touch()
        reader = AuditReader(path=path)
        assert reader.read_all() == []

    def test_missing_file(self, tmp_path: Path) -> None:
        reader = AuditReader(path=tmp_path / "nope.jsonl")
        assert reader.read_all() == []


# ---------------------------------------------------------------------------
# Malformed line handling
# ---------------------------------------------------------------------------


class TestMalformedLines:
    """Verify that the reader skips bad lines gracefully."""

    def test_malformed_json_skipped(self, tmp_path: Path) -> None:
        path = tmp_path / "audit.jsonl"
        good = _make_event(agent_id="good-agent")
        good_line = json.dumps(good.model_dump(), ensure_ascii=False)
        path.write_text(
            "not valid json\n" + good_line + "\n{broken: true}\n",
            encoding="utf-8",
        )
        reader = AuditReader(path=path)
        events = reader.read_all()
        assert len(events) == 1
        assert events[0].agent_id == "good-agent"

    def test_blank_lines_skipped(self, tmp_path: Path) -> None:
        path = tmp_path / "audit.jsonl"
        good = _make_event(agent_id="x")
        path.write_text(
            "\n\n" + json.dumps(good.model_dump()) + "\n\n",
            encoding="utf-8",
        )
        reader = AuditReader(path=path)
        assert len(reader.read_all()) == 1

    def test_only_malformed_returns_empty(self, tmp_path: Path) -> None:
        path = tmp_path / "audit.jsonl"
        path.write_text("garbage\ncorrupt\n", encoding="utf-8")
        reader = AuditReader(path=path)
        assert reader.read_all() == []


# ---------------------------------------------------------------------------
# Round-trip integration
# ---------------------------------------------------------------------------


class TestRoundTrip:
    """End-to-end: writer produces, reader consumes."""

    def test_full_round_trip(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"
        writer = AuditWriter(path=log_file)
        reader = AuditReader(path=log_file)

        events = [
            _make_event(
                event_type=AuditEventType.TASK_CREATED,
                agent_id="chief-of-staff",
                task_id="rt-1",
            ),
            _make_event(
                event_type=AuditEventType.DELEGATION,
                agent_id="chief-of-staff",
                task_id="rt-1",
            ),
            _make_event(
                event_type=AuditEventType.TOOL_CALL,
                agent_id="lead-backend",
                task_id="rt-1",
            ),
            _make_event(
                event_type=AuditEventType.TASK_COMPLETED,
                agent_id="lead-backend",
                task_id="rt-1",
            ),
        ]

        writer.write_batch(events)

        # Full read
        assert len(reader.read_all()) == 4

        # Filter by task
        assert len(reader.read_by_task("rt-1")) == 4

        # Filter by agent
        assert len(reader.read_by_agent("lead-backend")) == 2
        assert len(reader.read_by_agent("chief-of-staff")) == 2

        # Filter by type
        assert len(reader.read_by_type("delegation")) == 1

    def test_append_preserves_existing(self, tmp_path: Path) -> None:
        log_file = tmp_path / "audit.jsonl"

        # First write
        w1 = AuditWriter(path=log_file)
        w1.write(_make_event(agent_id="first"))
        assert len(AuditReader(path=log_file).read_all()) == 1

        # Second write appends
        w2 = AuditWriter(path=log_file)
        w2.write(_make_event(agent_id="second"))
        all_events = AuditReader(path=log_file).read_all()
        assert len(all_events) == 2
        agents = {e.agent_id for e in all_events}
        assert agents == {"first", "second"}
