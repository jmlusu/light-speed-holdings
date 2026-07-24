"""Agent behavior KPI collector — monitors agent activity patterns."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector

logger = logging.getLogger(__name__)


class AgentBehaviorKPICollector(KPICollector):
    """Collect agent behavior metrics for the dashboard."""

    department = "agent_behavior"

    def __init__(
        self,
        project_root: Path | None = None,
        message_bus: Any | None = None,
    ) -> None:
        super().__init__(project_root=project_root, message_bus=message_bus)

    def collect(self) -> dict[str, Any]:
        """Collect agent behavior KPIs."""
        try:
            from ai_company.security.agent_monitor import get_agent_monitor

            monitor = get_agent_monitor()
            summaries = monitor.get_all_summaries()
            anomalies = monitor.check_anomalies()

            # Calculate aggregate metrics
            total_agents = len(summaries)
            active_agents = sum(
                1 for s in summaries.values()
                if s.get("total_actions", 0) > 0
            )
            total_actions = sum(
                s.get("total_actions", 0) for s in summaries.values()
            )
            anomaly_count = len(anomalies)
            critical_anomalies = sum(
                1 for a in anomalies if a.severity == "critical"
            )

            # Per-action-type aggregates
            action_totals: dict[str, int] = {}
            for summary in summaries.values():
                for action_type, count in summary.get("actions", {}).items():
                    action_totals[action_type] = action_totals.get(action_type, 0) + count

            return {
                "department": self.department,
                "kpis": {
                    "total_agents_monitored": self._kpi(total_agents, None, "agents"),
                    "active_agents": self._kpi(active_agents, None, "agents"),
                    "total_actions": self._kpi(total_actions, None, "actions"),
                    "anomaly_count": self._kpi(anomaly_count, 0, "anomalies", higher_is_better=False),
                    "critical_anomalies": self._kpi(critical_anomalies, 0, "anomalies", higher_is_better=False),
                    "action_breakdown": action_totals,
                    "agent_summaries": summaries,
                },
            }
        except Exception as exc:
            logger.warning("Failed to collect agent behavior KPIs: %s", exc)
            return {
                "department": self.department,
                "kpis": {},
                "error": str(exc),
            }
