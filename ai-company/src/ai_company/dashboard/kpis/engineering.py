"""Engineering department KPI collector — reads inbox.json, escalation.yaml, scheduler.yaml."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector


class EngineeringKPICollector(KPICollector):
    """Collects live metrics for the Engineering / Technology department."""

    department = "engineering"

    def collect(self) -> dict[str, Any]:
        tasks: list[dict] = self._get_tasks()
        escalations = self._load_yaml("orchestrator/escalation.yaml")
        scheduler = self._load_yaml("orchestrator/scheduler.yaml")

        total = len(tasks)
        pending = sum(1 for t in tasks if t.get("status") == "pending")
        in_progress = sum(1 for t in tasks if t.get("status") == "in_progress")
        completed = sum(1 for t in tasks if t.get("status") == "completed")
        failed = sum(1 for t in tasks if t.get("status") == "failed")

        completion_rate = round((completed / total * 100), 1) if total > 0 else 0.0
        failure_rate = round((failed / total * 100), 1) if total > 0 else 0.0

        events: list[dict] = escalations.get("events", [])
        open_escalations = [e for e in events if not e.get("resolved", False)]
        total_escalations = len(events)
        escalation_rate = (
            round((total_escalations / total * 100), 1) if total > 0 else 0.0
        )

        scheduled = scheduler.get("tasks", [])

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
                    len(open_escalations), 0, "count", higher_is_better=False,
                ),
                "total_tasks": self._kpi(total, None, "count"),
                "scheduled_tasks": self._kpi(len(scheduled), None, "count"),
            },
        }
