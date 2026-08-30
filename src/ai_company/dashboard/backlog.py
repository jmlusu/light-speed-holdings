"""Backlog / queue observability for the CEO dashboard (C3).

Computes a single JSON-able snapshot of the task queue — depth, status
spread, oldest pending age, staleness, and dead-letter depth — so both the
REST API (``GET /api/v1/backlog``) and the ``dashboard queue`` CLI command
can render the same ground truth.

All reads go through :class:`MessageBus` (never raw inbox file access), so
the view honours the same locking/quarantine guarantees as the rest of the
app.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_STALE_THRESHOLD_S = 24 * 3600  # pending older than 24h is "stale"


def _parse_ts(value: Any) -> datetime | None:
    """Parse an ISO-8601 timestamp (naive strings are assumed UTC)."""
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _oldest_pending_info(tasks: list[dict[str, Any]]) -> tuple[float | None, str | None]:
    """Return ``(age_seconds, created_at)`` of the oldest pending task."""
    now = datetime.now(timezone.utc)
    oldest_age: float | None = None
    oldest_ts: str | None = None
    for task in tasks:
        if task.get("status") != "pending":
            continue
        created = _parse_ts(task.get("created_at"))
        if created is None:
            continue
        age = (now - created).total_seconds()
        if oldest_age is None or age > oldest_age:
            oldest_age = age
            oldest_ts = task.get("created_at")
    return oldest_age, oldest_ts


def backlog_summary(
    data_root: str | Path | None = None,
    *,
    stale_threshold_s: float = DEFAULT_STALE_THRESHOLD_S,
) -> dict[str, Any]:
    """Return a queue snapshot rooted at *data_root*.

    When *data_root* is omitted it resolves to the dashboard's configured
    state root, so the CLI and API stay consistent with the running app.
    """
    if data_root is None:
        from ai_company.dashboard.repository import get_state_store

        data_root = get_state_store().base_dir
    root = Path(data_root)

    from ai_company.executor.dead_letter import DeadLetterQueue
    from ai_company.orchestrator.message_bus import MessageBus

    inbox_path = root / ".opencode" / "inbox.json"
    bus = MessageBus(str(inbox_path))
    tasks = bus.get_all_tasks_raw()

    by_status: dict[str, int] = {}
    for task in tasks:
        status = str(task.get("status", "pending"))
        by_status[status] = by_status.get(status, 0) + 1

    now = datetime.now(timezone.utc)
    stale_pending = 0
    for task in tasks:
        if task.get("status") != "pending":
            continue
        created = _parse_ts(task.get("created_at"))
        if created is not None and (now - created).total_seconds() > stale_threshold_s:
            stale_pending += 1

    oldest_age_s, oldest_created_at = _oldest_pending_info(tasks)

    dlq_path = root / ".opencode" / "dead_letter.json"
    try:
        dead_letter_count = len(DeadLetterQueue(str(dlq_path)).list_entries())
    except Exception:  # noqa: BLE001 - DLQ may be missing/malformed; stay readable
        logger.debug("DLQ read failed at %s", dlq_path, exc_info=True)
        dead_letter_count = 0

    return {
        "total": len(tasks),
        "by_status": by_status,
        "pending": by_status.get("pending", 0),
        "in_progress": by_status.get("in_progress", 0),
        "waiting_approval": by_status.get("waiting_approval", 0),
        "completed": by_status.get("completed", 0),
        "failed": by_status.get("failed", 0),
        "escalated": by_status.get("escalated", 0),
        "cancelled": by_status.get("cancelled", 0),
        "oldest_pending_age_s": oldest_age_s,
        "oldest_pending_created_at": oldest_created_at,
        "stale_pending_count": stale_pending,
        "stale_threshold_s": stale_threshold_s,
        "dead_letter_count": dead_letter_count,
        "inbox_path": str(inbox_path),
        "computed_at": now.isoformat(),
    }
