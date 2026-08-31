"""Customer Success department KPI collector."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector


class CustomerSuccessKPICollector(KPICollector):
    """Collects live metrics for the Customer Success department."""

    department = "customer_success"

    def _check_sop_status(self) -> tuple[bool, float]:
        """Check if Customer Success SOP exists and is current (updated within 90 days)."""
        sop_path = self.root / "docs" / "sop" / "customer-success-sop.md"
        is_current, freshness, _error = self._sop_freshness(sop_path, "Customer Success")
        return is_current, freshness if freshness is not None else 0.0

    def _compute_ticket_resolution_time(
        self, tickets: list[dict[str, Any]]
    ) -> tuple[float | None, str | None]:
        """Compute average ticket resolution time in hours from ticket timestamps.

        Returns:
            Tuple of (avg_resolution_hours, error_message). error_message is None on success.
        """
        return self._compute_avg_duration(
            tickets,
            ["resolved"],
            "created_at",
            "resolved_at",
            no_items_msg="No resolved tickets with timestamps available",
            no_pairs_msg="No valid timestamp pairs found in resolved tickets",
            item_label="ticket",
        )

    def collect(self) -> dict[str, Any]:
        tickets = self._load_json("orchestrator/cs/tickets.json")
        surveys = self._load_json("orchestrator/cs/surveys.json")
        tasks = self._tasks_from_sqlite()
        if tasks is None:
            tasks = self._tasks_from_bus()

        # Count CS-related tasks
        cs_receivers = {
            "customer-success",
            "support_agent",
            "customer_success_owner",
            "customer_success",
        }
        cs_tasks = [t for t in tasks if t.get("receiver_id") in cs_receivers]
        completed_cs = sum(1 for t in cs_tasks if t.get("status") == "completed")
        total_cs = len(cs_tasks)
        task_completion_rate = round((completed_cs / total_cs * 100), 1) if total_cs > 0 else 0.0

        # Ticket metrics
        ticket_list = tickets if isinstance(tickets, list) else []
        open_tickets = sum(1 for t in ticket_list if t.get("status") in ("open", "in_progress"))
        resolved_tickets = sum(1 for t in ticket_list if t.get("status") == "resolved")
        total_tickets = len(ticket_list)

        # Compute ticket resolution time from timestamps
        avg_resolution_time, resolution_error = self._compute_ticket_resolution_time(ticket_list)
        if avg_resolution_time is not None:
            resolution_quality = "real"
            resolution_error = None
        else:
            resolution_quality = "error"
            # Use default target as fallback but mark as error
            avg_resolution_time = 0.0

        # Survey / satisfaction
        survey_list = surveys if isinstance(surveys, list) else []
        scores = [s.get("score", 0) for s in survey_list if s.get("score")]
        avg_satisfaction = round(sum(scores) / len(scores), 1) if scores else 0.0

        # SOP Compliance
        sop_current, sop_freshness = self._check_sop_status()

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "ticket_resolution_time": self._kpi(
                    avg_resolution_time,
                    4,
                    "hours",
                    data_quality=resolution_quality,
                    error=resolution_error,
                ),
                "open_tickets": self._kpi(open_tickets, 0, "count", higher_is_better=False),
                "resolved_tickets": self._kpi(resolved_tickets, None, "count"),
                "total_tickets": self._kpi(total_tickets, None, "count"),
                "customer_satisfaction": self._kpi(avg_satisfaction, 9, "score"),
                "cs_task_completion": self._kpi(task_completion_rate, 90, "%"),
                "total_cs_tasks": self._kpi(total_cs, None, "count"),
                # SOP Compliance
                "sop_current": self._kpi(1 if sop_current else 0, 1, "bool"),
                "sop_freshness_pct": self._kpi(sop_freshness, 100, "%"),
            },
        }
