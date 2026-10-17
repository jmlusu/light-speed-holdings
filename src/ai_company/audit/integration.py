"""Audit trail integration — writes events at key executor checkpoints."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from ai_company.audit.events import AuditEvent, AuditEventType
from ai_company.audit.writer import AuditWriter

logger = logging.getLogger(__name__)

_writer: AuditWriter | None = None


def init_audit(audit_dir: str | Path | None = None, database: Any = None) -> AuditWriter:
    """Initialise the global audit writer. Idempotent — returns existing writer if already set.

    When *audit_dir* is ``None`` the canonical audit trail path is used
    (``ai_company.paths.get_audit_path()``), identical to the AuditWriter
    default, so the executor writes the same file every other audit entry
    point reads (ticket #59). *database* is passed through to the
    :class:`AuditWriter` so events are mirrored to SQLite when the data layer
    is active (Sprint 2, S2.1).
    """
    global _writer
    if _writer is None:
        _writer = AuditWriter(audit_dir, database=database)
    return _writer


def get_writer() -> AuditWriter | None:
    """Return the current writer, or None if audit is not initialised."""
    return _writer


def _coerce_payload(value: Any, field: str) -> dict[str, Any]:
    """Coerce an ``AuditEvent`` payload field to a dict.

    The LLM output is untyped (GAP-019): a tool step whose ``args`` is a bare
    string (e.g. ``args: "-"``) must not crash ``AuditEvent`` construction,
    which would fail the entire task. Non-dict payloads are enveloped so the
    event is still recorded with the offending value preserved.
    """
    if isinstance(value, dict):
        return value
    return {"_raw_value": repr(value), "_field": field}


def _write_event(event: AuditEvent) -> None:
    """Append an audit event, best-effort. The audit trail is infrastructure
    and must never crash the executor loop."""
    if _writer is None:
        return
    try:
        _writer.write(event)
    except Exception:  # noqa: BLE001 - audit is best-effort infrastructure
        logger.error("Failed to record audit event %s", event.event_type, exc_info=True)


def log_tool_call(
    task_id: str,
    agent_id: str,
    tool: str,
    args: Any,
    result: Any,
) -> None:
    """Record a TOOL_CALL event after a tool executes."""
    if _writer is None:
        return
    _write_event(
        AuditEvent(
            event_type=AuditEventType.TOOL_CALL,
            task_id=task_id,
            agent_id=agent_id,
            tool=tool,
            args=_coerce_payload(args, "args"),
            result=_coerce_payload(result, "result"),
        )
    )


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

    _write_event(
        AuditEvent(
            event_type=event_type,
            task_id=task_id,
            agent_id=agent_id,
            metadata={"old_status": old_status, "new_status": new_status},
        )
    )


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
        event_type = AuditEventType.HITL_APPROVED if approved else AuditEventType.HITL_DENIED
    _write_event(
        AuditEvent(
            event_type=event_type,
            task_id=task_id,
            agent_id=agent_id,
            tool=tool,
        )
    )


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
    _write_event(
        AuditEvent(
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
    )
