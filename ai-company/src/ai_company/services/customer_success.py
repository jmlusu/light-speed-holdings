"""Customer Success department service layer.

Provides ticket management, satisfaction tracking, and escalation with
MessageBus integration for task delegation.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from ai_company.models.task import TaskPriority
from ai_company.services.base import BaseService

logger = logging.getLogger(__name__)


class CustomerSuccessService(BaseService):
    """Service layer for the Customer Success department.

    Manages support tickets, satisfaction tracking, and escalations.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(department_id="customer_success", **kwargs)

    # ── Ticket management ─────────────────────────────────────────────

    def list_tickets(self, status: str = "") -> list[dict[str, Any]]:
        """List all support tickets, optionally filtered by status."""
        data = self._load_data("tickets.yaml")
        tickets = data.get("tickets", [])
        if status:
            tickets = [t for t in tickets if t.get("status") == status]
        return tickets

    def create_ticket(
        self,
        ticket_id: str,
        subject: str,
        priority: str = "medium",
        customer: str = "",
        description: str = "",
    ) -> dict[str, Any]:
        """Create a new support ticket and delegate initial triage."""
        data = self._load_data("tickets.yaml")
        tickets = data.get("tickets", [])

        for ticket in tickets:
            if ticket["id"] == ticket_id:
                raise ValueError(f"Ticket '{ticket_id}' already exists")

        new_ticket = {
            "id": ticket_id,
            "subject": subject,
            "priority": priority,
            "customer": customer,
            "description": description,
            "status": "open",
            "created_at": datetime.now().isoformat(),
        }
        tickets.append(new_ticket)
        data["tickets"] = tickets
        self._save_data("tickets.yaml", data)

        self.record_event(
            f"Ticket '{subject}' created (priority={priority})",
            tags=["ticket", "created", priority],
            ticket_id=ticket_id,
        )

        # Delegate triage task for high-priority tickets
        if priority in ("high", "critical"):
            task_priority = TaskPriority.HIGH if priority == "high" else TaskPriority.CRITICAL
            self.create_task(
                receiver_id="customer-success-specialist",
                instruction=(
                    f"Urgent: Triage ticket '{subject}' ({priority} priority). "
                    f"Customer: {customer or 'unknown'}. "
                    f"Assess impact and propose resolution plan."
                ),
                priority=task_priority,
            )

        return new_ticket

    def update_ticket_status(
        self, ticket_id: str, new_status: str, resolution: str = ""
    ) -> dict[str, Any]:
        """Update ticket status (open -> in_progress -> resolved/closed)."""
        data = self._load_data("tickets.yaml")
        tickets = data.get("tickets", [])

        ticket = next((t for t in tickets if t["id"] == ticket_id), None)
        if not ticket:
            raise ValueError(f"Ticket '{ticket_id}' not found")

        old_status = ticket.get("status", "")
        ticket["status"] = new_status
        ticket["updated_at"] = datetime.now().isoformat()

        if new_status in ("resolved", "closed"):
            ticket["resolved_at"] = datetime.now().isoformat()
            if resolution:
                ticket["resolution"] = resolution

        data["tickets"] = tickets
        self._save_data("tickets.yaml", data)

        self.record_event(
            f"Ticket '{ticket['subject']}' status: {old_status} -> {new_status}",
            tags=["ticket", "status_change", new_status],
            ticket_id=ticket_id,
        )

        # Record knowledge from resolutions
        if new_status == "resolved" and resolution:
            self.record_knowledge(
                topic=ticket["subject"],
                content=f"Resolution for '{ticket['subject']}': {resolution}",
                tags=["resolution", ticket.get("priority", "medium")],
            )

        return ticket

    def escalate_ticket(self, ticket_id: str, reason: str = "") -> dict[str, Any]:
        """Escalate a ticket and create a priority task."""
        data = self._load_data("tickets.yaml")
        tickets = data.get("tickets", [])

        ticket = next((t for t in tickets if t["id"] == ticket_id), None)
        if not ticket:
            raise ValueError(f"Ticket '{ticket_id}' not found")

        ticket["status"] = "escalated"
        ticket["escalated_at"] = datetime.now().isoformat()
        ticket["escalation_reason"] = reason
        data["tickets"] = tickets
        self._save_data("tickets.yaml", data)

        self.record_event(
            f"Ticket '{ticket['subject']}' escalated: {reason}",
            tags=["ticket", "escalated"],
            ticket_id=ticket_id,
        )

        # Delegate escalation task to executive
        self.create_task(
            receiver_id="chief-of-staff",
            instruction=(
                f"Escalated ticket '{ticket['subject']}' requires executive attention. "
                f"Reason: {reason or 'unspecified'}. "
                f"Customer: {ticket.get('customer', 'unknown')}."
            ),
            priority=TaskPriority.HIGH,
        )

        return ticket

    # ── Reporting ─────────────────────────────────────────────────────

    def get_satisfaction_report(self) -> dict[str, Any]:
        """Generate customer satisfaction report."""
        data = self._load_data("tickets.yaml")
        tickets = data.get("tickets", [])

        total = len(tickets)
        open_count = sum(1 for t in tickets if t.get("status") == "open")
        in_progress = sum(1 for t in tickets if t.get("status") == "in_progress")
        resolved = sum(1 for t in tickets if t.get("status") in ("resolved", "closed"))
        escalated = sum(1 for t in tickets if t.get("status") == "escalated")

        by_priority: dict[str, int] = {}
        for t in tickets:
            p = t.get("priority", "medium")
            by_priority[p] = by_priority.get(p, 0) + 1

        return {
            "total_tickets": total,
            "open": open_count,
            "in_progress": in_progress,
            "resolved": resolved,
            "escalated": escalated,
            "resolution_rate": round(resolved / total * 100, 2) if total > 0 else 0.0,
            "by_priority": by_priority,
        }

    def get_summary(self) -> dict[str, Any]:
        """Customer Success department summary."""
        return {
            **super().get_summary(),
            **self.get_satisfaction_report(),
        }
