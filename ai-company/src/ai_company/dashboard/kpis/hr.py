"""HR department KPI collector — reads agent-registry.json and department data."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector


class HRKPICollector(KPICollector):
    """Collects live metrics for the Human Resources / People department."""

    department = "hr"

    def collect(self) -> dict[str, Any]:
        registry: list[dict] = self._load_json("company/agent-registry.json")
        departments_data = self._load_yaml("company/departments.yaml")

        total_agents = len(registry)

        # Agents by department
        dept_counter: Counter[str] = Counter()
        for agent in registry:
            dept = agent.get("department") or "unassigned"
            dept_counter[dept] += 1
        agents_by_department = dict(dept_counter)

        # Department coverage: how many declared departments have at least one agent
        declared_depts = departments_data.get("departments", [])
        departments_with_agents = sum(
            1 for d in declared_depts if d.get("totalAgents", 0) > 0
        )
        total_declared = len(declared_depts)
        coverage_pct = (
            round((departments_with_agents / total_declared * 100), 1)
            if total_declared > 0
            else 0.0
        )

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "total_agents": self._kpi(total_agents, None, "count"),
                "agents_by_department": {
                    "current": agents_by_department,
                    "target": None,
                    "unit": "breakdown",
                    "status": "info",
                },
                "department_coverage": self._kpi(coverage_pct, 100, "%"),
                "declared_departments": self._kpi(total_declared, None, "count"),
            },
        }
