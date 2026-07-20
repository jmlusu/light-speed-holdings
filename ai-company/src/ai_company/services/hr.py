"""Human Resources department service layer.

Provides workforce management, onboarding, and reporting with
MessageBus integration for task delegation.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from ai_company.models.task import TaskPriority
from ai_company.services.base import BaseService

logger = logging.getLogger(__name__)


class HRService(BaseService):
    """Service layer for the Human Resources department.

    Manages agent workforce, onboarding, deactivation, and reporting.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(department_id="hr", **kwargs)

    # ── Workforce management ──────────────────────────────────────────

    def list_agents(self, status: str = "") -> list[dict[str, Any]]:
        """List all agents in the workforce, optionally filtered by status."""
        data = self._load_data("roster.yaml")
        agents = data.get("agents", [])
        if status:
            agents = [a for a in agents if a.get("status") == status]
        return agents

    def onboard(
        self,
        agent_id: str,
        role: str,
        department: str,
        seniority: str = "mid",
        reports_to: str = "",
    ) -> dict[str, Any]:
        """Onboard a new agent to the workforce.

        Creates the roster entry, then delegates onboarding tasks.
        """
        data = self._load_data("roster.yaml")
        agents = data.get("agents", [])

        for agent in agents:
            if agent["id"] == agent_id:
                raise ValueError(f"Agent '{agent_id}' already exists")

        new_agent = {
            "id": agent_id,
            "role": role,
            "department": department,
            "seniority": seniority,
            "reports_to": reports_to,
            "status": "onboarding",
            "onboarded_at": datetime.now().isoformat(),
        }
        agents.append(new_agent)
        data["agents"] = agents
        self._save_data("roster.yaml", data)

        self.record_event(
            f"Agent '{agent_id}' onboarded as {role} in {department}",
            tags=["agent", "onboarded", department],
            agent_id=agent_id,
        )

        # Delegate onboarding tasks
        tasks = [
            f"Set up agent '{agent_id}' access and permissions for {department}.",
            f"Generate agent spec card for '{agent_id}' ({role}, {seniority}).",
            f"Assign '{agent_id}' to report to {reports_to or department + '-lead'}.",
        ]
        for instruction in tasks:
            self.create_task(
                receiver_id="hr-specialist",
                instruction=instruction,
                priority=TaskPriority.MEDIUM,
            )

        logger.info("Agent '%s' onboarded. %d onboarding tasks created.", agent_id, len(tasks))
        return new_agent

    def activate(self, agent_id: str) -> dict[str, Any]:
        """Activate an agent (complete onboarding or reactivate)."""
        data = self._load_data("roster.yaml")
        agents = data.get("agents", [])

        agent = next((a for a in agents if a["id"] == agent_id), None)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found")

        old_status = agent.get("status", "")
        agent["status"] = "active"
        agent["activated_at"] = datetime.now().isoformat()
        data["agents"] = agents
        self._save_data("roster.yaml", data)

        self.record_event(
            f"Agent '{agent_id}' activated (was: {old_status})",
            tags=["agent", "activated"],
            agent_id=agent_id,
        )
        return agent

    def deactivate(self, agent_id: str, reason: str = "") -> dict[str, Any]:
        """Deactivate an agent from the workforce."""
        data = self._load_data("roster.yaml")
        agents = data.get("agents", [])

        agent = next((a for a in agents if a["id"] == agent_id), None)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found")

        old_status = agent.get("status", "")
        agent["status"] = "inactive"
        agent["deactivated_at"] = datetime.now().isoformat()
        agent["deactivation_reason"] = reason
        data["agents"] = agents
        self._save_data("roster.yaml", data)

        self.record_event(
            f"Agent '{agent_id}' deactivated (was: {old_status}): {reason or 'unspecified'}",
            tags=["agent", "deactivated"],
            agent_id=agent_id,
        )

        # Create handoff task if needed
        if reason:
            self.create_task(
                receiver_id="chief-of-staff",
                instruction=(
                    f"Agent '{agent_id}' has been deactivated. "
                    f"Reason: {reason}. "
                    f"Please review and reassign any pending tasks."
                ),
                priority=TaskPriority.HIGH,
            )

        return agent

    # ── Reporting ─────────────────────────────────────────────────────

    def get_workforce_report(self) -> dict[str, Any]:
        """Generate workforce statistics report."""
        data = self._load_data("roster.yaml")
        agents = data.get("agents", [])

        total = len(agents)
        active = sum(1 for a in agents if a.get("status") == "active")
        onboarding = sum(1 for a in agents if a.get("status") == "onboarding")
        inactive = sum(1 for a in agents if a.get("status") == "inactive")

        by_department: dict[str, int] = {}
        for a in agents:
            dept = a.get("department", "Unknown")
            by_department[dept] = by_department.get(dept, 0) + 1

        by_seniority: dict[str, int] = {}
        for a in agents:
            s = a.get("seniority", "mid")
            by_seniority[s] = by_seniority.get(s, 0) + 1

        return {
            "total_agents": total,
            "active": active,
            "onboarding": onboarding,
            "inactive": inactive,
            "by_department": by_department,
            "by_seniority": by_seniority,
        }

    def get_summary(self) -> dict[str, Any]:
        """HR department summary."""
        return {
            **super().get_summary(),
            **self.get_workforce_report(),
        }
