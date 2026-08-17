"""Engineering department KPI collector — tasks via MessageBus, escalation.yaml, scheduler.yaml."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector

logger = logging.getLogger(__name__)


class EngineeringKPICollector(KPICollector):
    """Collects live metrics for the Engineering / Technology department."""

    department = "engineering"

    def _check_sop_status(self) -> tuple[bool, float | None, str | None]:
        """Check if Engineering SOP exists and is current (updated within 90 days).

        Returns:
            Tuple of (is_current, freshness_pct, error_message). error_message is None on success.
        """
        sop_path = self.root / "docs" / "sop" / "engineering-sop.md"
        if not sop_path.exists():
            return False, None, "SOP file not found"
        try:
            import re

            content = sop_path.read_text(encoding="utf-8")
            match = re.search(r"Last Updated:\s*([A-Za-z]+\s+\d{4})", content)
            if match:
                from datetime import datetime as dt

                updated_dt = dt.strptime(match.group(1), "%B %Y")
                now = datetime.now()
                days_old = (now - updated_dt).days
                is_current = days_old <= 90
                return (
                    is_current,
                    round((90 - days_old) / 90 * 100, 1) if is_current else None,
                    None,
                )
        except (OSError, ValueError, AttributeError) as exc:
            logger.warning(
                "Failed to parse Engineering SOP freshness (%s): %s",
                sop_path,
                exc,
            )
            return False, None, f"Failed to parse SOP date: {exc}"
        return False, None, "SOP date not found or invalid"

    def collect(self) -> dict[str, Any]:
        # Track data sources for quality reporting
        tasks = self._tasks_from_sqlite()
        tasks_source = "sqlite" if tasks is not None else None
        if tasks is None:
            tasks = self._tasks_from_bus()
            if tasks:
                tasks_source = "message_bus"

        events = self._escalations_from_sqlite()
        events_source = "sqlite" if events is not None else None
        if events is None:
            events = self._load_yaml("orchestrator/escalation.yaml").get("events", [])
            if events:
                events_source = "file"

        scheduler = self._load_yaml("orchestrator/scheduler.yaml")

        total = len(tasks)
        pending = sum(1 for t in tasks if t.get("status") == "pending")
        in_progress = sum(1 for t in tasks if t.get("status") == "in_progress")
        completed = sum(1 for t in tasks if t.get("status") == "completed")
        failed = sum(1 for t in tasks if t.get("status") == "failed")

        completion_rate = round((completed / total * 100), 1) if total > 0 else None
        failure_rate = round((failed / total * 100), 1) if total > 0 else None

        open_escalations = [e for e in events if not e.get("resolved", False)]
        total_escalations = len(events)
        escalation_rate = round((total_escalations / total * 100), 1) if total > 0 else None

        scheduled = scheduler.get("tasks", [])

        # SOP Compliance
        sop_current, sop_freshness, sop_error = self._check_sop_status()

        # Determine data quality for task-based KPIs
        if tasks_source == "sqlite":
            tasks_quality = "real"
            tasks_error = None
        elif tasks_source == "message_bus":
            tasks_quality = "fallback"
            tasks_error = "Using MessageBus (SQLite unavailable)"
        else:
            tasks_quality = "error"
            tasks_error = "No task data available (SQLite and MessageBus both unavailable)"

        # Determine data quality for escalation-based KPIs
        if events_source == "sqlite":
            events_quality = "real"
            events_error = None
        elif events_source == "file":
            events_quality = "fallback"
            events_error = "Using escalation.yaml (SQLite unavailable)"
        else:
            events_quality = "error"
            events_error = "No escalation data available (SQLite and file both unavailable)"

        # SOP data quality
        sop_quality = "error" if sop_error else "real"

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "task_completion_rate": self._kpi(
                    completion_rate, 95, "%", data_quality=tasks_quality, error=tasks_error
                ),
                "failure_rate": self._kpi(
                    failure_rate,
                    0,
                    "%",
                    higher_is_better=False,
                    data_quality=tasks_quality,
                    error=tasks_error,
                ),
                "escalation_rate": self._kpi(
                    escalation_rate,
                    5,
                    "%",
                    higher_is_better=False,
                    data_quality=events_quality,
                    error=events_error,
                ),
                "pending_tasks": self._kpi(
                    pending, None, "count", data_quality=tasks_quality, error=tasks_error
                ),
                "in_progress_tasks": self._kpi(
                    in_progress, None, "count", data_quality=tasks_quality, error=tasks_error
                ),
                "completed_tasks": self._kpi(
                    completed, None, "count", data_quality=tasks_quality, error=tasks_error
                ),
                "failed_tasks": self._kpi(
                    failed,
                    0,
                    "count",
                    higher_is_better=False,
                    data_quality=tasks_quality,
                    error=tasks_error,
                ),
                "open_escalations": self._kpi(
                    len(open_escalations),
                    0,
                    "count",
                    higher_is_better=False,
                    data_quality=events_quality,
                    error=events_error,
                ),
                "total_tasks": self._kpi(
                    total, None, "count", data_quality=tasks_quality, error=tasks_error
                ),
                "scheduled_tasks": self._kpi(len(scheduled), None, "count"),
                # SOP Compliance
                "sop_current": self._kpi(
                    1 if sop_current else 0, 1, "bool", data_quality=sop_quality, error=sop_error
                ),
                "sop_freshness_pct": self._kpi(
                    sop_freshness, 100, "%", data_quality=sop_quality, error=sop_error
                ),
            },
        }
