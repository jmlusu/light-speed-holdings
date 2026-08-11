"""Tests for the audit trail integration module."""

from __future__ import annotations

from pathlib import Path

import pytest

import ai_company.audit.integration as _audit_mod
from ai_company.audit.events import AuditEventType
from ai_company.audit.integration import (
    get_writer,
    init_audit,
    log_hitl_decision,
    log_task_status,
    log_tool_call,
)
from ai_company.audit.writer import AuditWriter


@pytest.fixture(autouse=True)
def _reset_writer() -> None:
    """Reset the module-global writer before every test."""
    _audit_mod._writer = None
    yield
    _audit_mod._writer = None


# ---------------------------------------------------------------------------
# init_audit / get_writer
# ---------------------------------------------------------------------------


class TestInitAudit:
    def test_init_creates_writer(self, tmp_path: Path) -> None:
        writer = init_audit(str(tmp_path / "audit"))
        assert isinstance(writer, AuditWriter)
        assert get_writer() is writer

    def test_init_is_idempotent(self, tmp_path: Path) -> None:
        w1 = init_audit(str(tmp_path / "a"))
        w2 = init_audit(str(tmp_path / "b"))
        assert w1 is w2

    def test_get_writer_returns_none_before_init(self) -> None:
        assert get_writer() is None


# ---------------------------------------------------------------------------
# log_tool_call
# ---------------------------------------------------------------------------


class TestLogToolCall:
    def test_writes_tool_call_event(self, tmp_path: Path) -> None:
        init_audit(str(tmp_path / "audit"))
        log_tool_call(
            task_id="t-1",
            agent_id="agent-a",
            tool="read",
            args={"path": "foo.py"},
            result={"status": "ok"},
        )
        writer = get_writer()
        assert writer is not None
        from ai_company.audit.reader import AuditReader

        events = AuditReader(path=writer.path).read_all()
        assert len(events) == 1
        assert events[0].event_type == AuditEventType.TOOL_CALL
        assert events[0].task_id == "t-1"
        assert events[0].agent_id == "agent-a"
        assert events[0].tool == "read"

    def test_noop_when_not_initialised(self) -> None:
        log_tool_call("t", "a", "read", {}, {})


# ---------------------------------------------------------------------------
# log_task_status
# ---------------------------------------------------------------------------


class TestLogTaskStatus:
    def test_in_progress_creates_task_created_event(self, tmp_path: Path) -> None:
        init_audit(str(tmp_path / "audit"))
        log_task_status("t-1", "agent-x", "pending", "in_progress")
        from ai_company.audit.reader import AuditReader

        writer = get_writer()
        assert writer is not None
        events = AuditReader(path=writer.path).read_all()
        assert len(events) == 1
        assert events[0].event_type == AuditEventType.TASK_CREATED
        assert events[0].metadata["old_status"] == "pending"
        assert events[0].metadata["new_status"] == "in_progress"

    def test_completed_creates_task_completed_event(self, tmp_path: Path) -> None:
        init_audit(str(tmp_path / "audit"))
        log_task_status("t-2", "agent-y", "in_progress", "completed")
        from ai_company.audit.reader import AuditReader

        writer = get_writer()
        assert writer is not None
        events = AuditReader(path=writer.path).read_all()
        assert len(events) == 1
        assert events[0].event_type == AuditEventType.TASK_COMPLETED

    def test_failed_creates_task_failed_event(self, tmp_path: Path) -> None:
        init_audit(str(tmp_path / "audit"))
        log_task_status("t-3", "agent-z", "in_progress", "failed")
        from ai_company.audit.reader import AuditReader

        writer = get_writer()
        assert writer is not None
        events = AuditReader(path=writer.path).read_all()
        assert len(events) == 1
        assert events[0].event_type == AuditEventType.TASK_FAILED

    def test_unknown_status_is_noop(self, tmp_path: Path) -> None:
        init_audit(str(tmp_path / "audit"))
        log_task_status("t-4", "agent-w", "pending", "queued")
        from ai_company.audit.reader import AuditReader

        writer = get_writer()
        assert writer is not None
        events = AuditReader(path=writer.path).read_all()
        assert len(events) == 0

    def test_noop_when_not_initialised(self) -> None:
        log_task_status("t", "a", "pending", "completed")


# ---------------------------------------------------------------------------
# log_hitl_decision
# ---------------------------------------------------------------------------


class TestLogHitlDecision:
    def test_approved_writes_hitl_approved(self, tmp_path: Path) -> None:
        init_audit(str(tmp_path / "audit"))
        log_hitl_decision("t-1", "agent-a", "write", approved=True)
        from ai_company.audit.reader import AuditReader

        writer = get_writer()
        assert writer is not None
        events = AuditReader(path=writer.path).read_all()
        assert len(events) == 1
        assert events[0].event_type == AuditEventType.HITL_APPROVED
        assert events[0].tool == "write"

    def test_denied_writes_hitl_denied(self, tmp_path: Path) -> None:
        init_audit(str(tmp_path / "audit"))
        log_hitl_decision("t-2", "agent-b", "execute", approved=False)
        from ai_company.audit.reader import AuditReader

        writer = get_writer()
        assert writer is not None
        events = AuditReader(path=writer.path).read_all()
        assert len(events) == 1
        assert events[0].event_type == AuditEventType.HITL_DENIED
        assert events[0].tool == "execute"

    def test_noop_when_not_initialised(self) -> None:
        log_hitl_decision("t", "a", "write", approved=True)
