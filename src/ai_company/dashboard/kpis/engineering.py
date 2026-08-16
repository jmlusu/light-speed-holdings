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

    def _check_sop_status(self) -> tuple[bool, float]:
        """Check if Engineering SOP exists and is current (updated within 90 days)."""
        sop_path = self.root / "docs" / "sop" / "engineering-sop.md"
        if not sop_path.exists():
            return False, 0.0
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
                return is_current, round((90 - days_old) / 90 * 100, 1) if is_current else 0.0
        except (OSError, ValueError, AttributeError) as exc:
            logger.warning(
                "Failed to parse Engineering SOP freshness (%s): %s",
                sop_path,
                exc,
            )
        return False, 0.0

    def collect(self) -> dict[str, Any]:
        tasks = self._tasks_from_sqlite()
        if tasks is None:
            tasks = self._tasks_from_bus()
        events = self._escalations_from_sqlite()
        if events is None:
            events = self._load_yaml("orchestrator/escalation.yaml").get("events", [])
        scheduler = self._load_yaml("orchestrator/scheduler.yaml")

        total = len(tasks)
        pending = sum(1 for t in tasks if t.get("status") == "pending")
        in_progress = sum(1 for t in tasks if t.get("status") == "in_progress")
        completed = sum(1 for t in tasks if t.get("status") == "completed")
        failed = sum(1 for t in tasks if t.get("status") == "failed")

        completion_rate = round((completed / total * 100), 1) if total > 0 else 0.0
        failure_rate = round((failed / total * 100), 1) if total > 0 else 0.0

        open_escalations = [e for e in events if not e.get("resolved", False)]
        total_escalations = len(events)
        escalation_rate = round((total_escalations / total * 100), 1) if total > 0 else 0.0

        scheduled = scheduler.get("tasks", [])

        # SOP Compliance
        sop_current, sop_freshness = self._check_sop_status()

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "task_completion_rate": self._kpi(completion_rate, 95, "%"),
                "failure_rate": self._kpi(failure_rate, 0, "%", higher_is_better=False),
                "escalation_rate": self._kpi(escalation_rate, 5, "%", higher_is_better=False),
                "pending_tasks": self._kpi(pending, None, "count"),
                "in_progress_tasks": self._kpi(in_progress, None, "count"),
                "completed_tasks": self._kpi(completed, None, "count"),
                "failed_tasks": self._kpi(failed, 0, "count", higher_is_better=False),
                "open_escalations": self._kpi(
                    len(open_escalations),
                    0,
                    "count",
                    higher_is_better=False,
                ),
                "total_tasks": self._kpi(total, None, "count"),
                "scheduled_tasks": self._kpi(len(scheduled), None, "count"),
                # SOP Compliance
                "sop_current": self._kpi(1 if sop_current else 0, 1, "bool"),
                "sop_freshness_pct": self._kpi(sop_freshness, 100, "%"),
            },
        }
