"""Sprint 4 KPI collector for the dashboard.

Provides a per-department collector that tracks Sprint 4
progress — milestone completion, burn-down, velocity, and
open task counts.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector
from ai_company.dashboard.sprint4 import sprint4_status


class Sprint4KPICollector(KPICollector):
    """Collects Sprint 4 KPI values for all departments."""

    department = "sprint4"

    def collect(self) -> dict[str, Any]:
        """Return Sprint 4 progress snapshot."""
        status = sprint4_status(project_root=self.root)

        milestones = status.get("milestones", [])
        overall = status.get("overall", {})
        velocity = status.get("velocity", {})
        burn_down = status.get("burn_down", [])

        # Build KPI dict using base._kpi helper conventions
        kpis: dict[str, Any] = {
            "sprint_completion_pct": self._kpi(
                overall.get("completion_pct", 0),
                100,
                "%",
            ),
            "completed_tasks": self._kpi(
                overall.get("completed", 0),
                None,
                "count",
            ),
            "in_progress_tasks": self._kpi(
                overall.get("in_progress", 0),
                None,
                "count",
            ),
            "pending_tasks": self._kpi(
                overall.get("pending", 0),
                None,
                "count",
            ),
            "failed_tasks": self._kpi(
                overall.get("failed", 0),
                0,
                "count",
                higher_is_better=False,
            ),
            "total_tasks": self._kpi(
                overall.get("total_tasks", 0),
                None,
                "count",
            ),
            "velocity_pct": self._kpi(
                velocity.get("velocity_pct", 0),
                100,
                "%",
            ),
            "points_completed": self._kpi(
                velocity.get("points_completed", 0),
                None,
                "points",
            ),
            "open_milestones": self._kpi(
                sum(
                    1
                    for m in milestones
                    if m.get("status") != "complete"
                ),
                0,
                "count",
                higher_is_better=False,
            ),
        }

        # Per-milestone KPIs
        for m in milestones:
            mid = m.get("id", "unknown")
            kpis[f"milestone_{mid}_pct"] = self._kpi(
                m.get("completion_pct", 0),
                100,
                "%",
            )

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": kpis,
            "metadata": {
                "sprint": "sprint4",
                "milestones": milestones,
                "burn_down": burn_down,
                "overall": overall,
                "velocity": velocity,
            },
        }
