"""Audit trail integration — writes events at key executor checkpoints."""

from __future__ import annotations

from typing import Any

from ai_company.audit.events import AuditEvent, AuditEventType
from ai_company.audit.writer import AuditWriter

_writer: AuditWriter | None = None


def init_audit(audit_dir: str = ".opencode/audit") -> AuditWriter:
    """Initialise the global audit writer. Idempotent — returns existing writer if already set."""
    global _writer
    if _writer is None:
        _writer = AuditWriter(audit_dir)
    return _writer


def get_writer() -> AuditWriter | None:
    """Return the current writer, or None if audit is not initialised."""
    return _writer


def log_tool_call(
    task_id: str,
    agent_id: str,
    tool: str,
    args: dict[str, Any],
    result: dict[str, Any],
) -> None:
    """Record a TOOL_CALL event after a tool executes."""
    if _writer is None:
        return
    event = AuditEvent(
        event_type=AuditEventType.TOOL_CALL,
        task_id=task_id,
        agent_id=agent_id,
        tool=tool,
        args=args,
        result=result,
    )
    _writer.write(event)


def log_task_status(
    task_id: str,
    agent_id: str,
    old_status: str,
    new_status: str,
) -> None:
    """Record a task lifecycle event based on the new status."""
    if _writer is None:
        return

    if new_status == "in_progress":
        event_type = AuditEventType.TASK_CREATED
    elif new_status == "completed":
        event_type = AuditEventType.TASK_COMPLETED
    elif new_status == "failed":
        event_type = AuditEventType.TASK_FAILED
    else:
        return

    event = AuditEvent(
        event_type=event_type,
        task_id=task_id,
        agent_id=agent_id,
        metadata={"old_status": old_status, "new_status": new_status},
    )
    _writer.write(event)


def log_hitl_decision(
    task_id: str,
    agent_id: str,
    tool: str,
    approved: bool | None = None,
) -> None:
    """Record an HITL approval, denial, or park event.

    ``approved`` is ``True`` for an approval, ``False`` for a denial, and
    ``None`` for a parked request awaiting a human decision (GAP-004).
    """
    if _writer is None:
        return
    if approved is None:
        event_type = AuditEventType.HITL_PARKED
    else:
        event_type = (
            AuditEventType.HITL_APPROVED if approved else AuditEventType.HITL_DENIED
        )
    event = AuditEvent(
        event_type=event_type,
        task_id=task_id,
        agent_id=agent_id,
        tool=tool,
    )
    _writer.write(event)


def log_escalation(
    task_id: str,
    from_agent: str,
    to_agent: str,
    reason: str,
    rule_id: str = "",
    resolved: bool = False,
) -> None:
    """Record an escalation event (GAP-008).

    Best-effort and exception-safe: if the audit writer has not been
    initialised (e.g. in lightweight unit tests) the call is a no-op.
    """
    if _writer is None:
        return
    event = AuditEvent(
        event_type=AuditEventType.ESCALATION,
        task_id=task_id,
        agent_id=to_agent or from_agent,
        args={
            "from_agent": from_agent,
            "to_agent": to_agent,
            "reason": reason,
            "rule_id": rule_id,
        },
        metadata={"resolved": resolved},
    )
    _writer.write(event)
