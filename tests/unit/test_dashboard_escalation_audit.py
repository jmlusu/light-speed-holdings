"""Tests for GAP-008 — escalation / HITL decisions persisted to audit trail.

Verifies that escalation events and HITL decisions are written to the
JSONL audit log via the existing audit writer.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_company.audit.events import AuditEventType
from ai_company.audit.integration import (
    init_audit,
    log_escalation,
    log_hitl_decision,
)

_AUDIT_DIR = ".opencode/audit"


@pytest.fixture()
def audit_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Isolated audit dir; reset the global writer between tests."""
    import ai_company.audit.integration as audit_mod

    monkeypatch.chdir(tmp_path)
    audit_mod._writer = None
    d = tmp_path / _AUDIT_DIR
    init_audit(audit_dir=str(d / "audit.jsonl"))
    yield d
    audit_mod._writer = None


def _read_events(audit_dir: Path) -> list[dict]:
    import json

    path = audit_dir / "audit.jsonl"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def test_escalation_event_persisted(audit_dir: Path) -> None:
    """log_escalation writes an ESCALATION event to the audit trail."""
    log_escalation(
        task_id="t-1",
        from_agent="agent-a",
        to_agent="human-ceo",
        reason="repeated tool failure",
        rule_id="r-9",
    )
    events = _read_events(audit_dir)
    assert len(events) == 1
    evt = events[0]
    assert evt["event_type"] == AuditEventType.ESCALATION.value
    assert evt["task_id"] == "t-1"
    assert evt["args"]["from_agent"] == "agent-a"
    assert evt["args"]["to_agent"] == "human-ceo"
    assert evt["metadata"]["resolved"] is False


def test_hitl_decision_denied_persisted(audit_dir: Path) -> None:
    """log_hitl_decision persists a denial as a hitl_denied event."""
    log_hitl_decision(task_id="t-2", agent_id="agent-b", tool="write", approved=False)
    events = _read_events(audit_dir)
    assert len(events) == 1
    assert events[0]["event_type"] == AuditEventType.HITL_DENIED.value
    assert events[0]["task_id"] == "t-2"
    assert events[0]["tool"] == "write"


def test_hitl_decision_parked_persisted(audit_dir: Path) -> None:
    """log_hitl_decision with approved=None persists a hitl_parked event."""
    log_hitl_decision(task_id="t-3", agent_id="agent-c", tool="execute", approved=None)
    events = _read_events(audit_dir)
    assert events[0]["event_type"] == AuditEventType.HITL_PARKED.value


def test_escalation_resolution_persisted(audit_dir: Path) -> None:
    """A resolved escalation records resolved=True in metadata."""
    log_escalation(
        task_id="t-4",
        from_agent="agent-d",
        to_agent="human-ceo",
        reason="fixed",
        resolved=True,
    )
    events = _read_events(audit_dir)
    assert events[0]["metadata"]["resolved"] is True
