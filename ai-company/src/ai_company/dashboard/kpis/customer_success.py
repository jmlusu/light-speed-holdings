"""Customer Success department KPI collector."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector


class CustomerSuccessKPICollector(KPICollector):
    """Collects live metrics for the Customer Success department."""

    department = "customer_success"

    def collect(self) -> dict[str, Any]:
        tickets = self._load_json("orchestrator/cs/tickets.json")
        surveys = self._load_json("orchestrator/cs/surveys.json")
        tasks = self._get_tasks()

        # Count CS-related tasks
        cs_receivers = {"customer-success", "support_agent"}
        cs_tasks = [
            t for t in tasks if t.get("receiver_id") in cs_receivers
        ]
        completed_cs = sum(
            1 for t in cs_tasks if t.get("status") == "completed"
        )
        total_cs = len(cs_tasks)
        task_completion_rate = (
            round((completed_cs / total_cs * 100), 1) if total_cs > 0 else 0.0
        )

        # Ticket metrics
        ticket_list = tickets if isinstance(tickets, list) else []
        open_tickets = sum(
            1 for t in ticket_list if t.get("status") in ("open", "in_progress")
        )
        resolved_tickets = sum(
            1 for t in ticket_list if t.get("status") == "resolved"
        )
        total_tickets = len(ticket_list)

        # Survey / satisfaction
        survey_list = surveys if isinstance(surveys, list) else []
        scores = [s.get("score", 0) for s in survey_list if s.get("score")]
        avg_satisfaction = (
            round(sum(scores) / len(scores), 1) if scores else 0.0
        )

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "ticket_resolution_time": self._kpi(
                    0, 4, "hours",
                ),  # Needs timestamp diff to compute; default until time data
                "open_tickets": self._kpi(open_tickets, 0, "count", higher_is_better=False),
                "resolved_tickets": self._kpi(resolved_tickets, None, "count"),
                "total_tickets": self._kpi(total_tickets, None, "count"),
                "customer_satisfaction": self._kpi(avg_satisfaction, 9, "score"),
                "cs_task_completion": self._kpi(task_completion_rate, 90, "%"),
                "total_cs_tasks": self._kpi(total_cs, None, "count"),
            },
        }
