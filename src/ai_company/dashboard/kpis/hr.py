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
        registry_path = self.root / "company" / "agent-registry.json"
        dept_path = self.root / "company" / "departments.yaml"

        registry: list[dict[str, Any]] = self._load_json("company/agent-registry.json")
        departments_data = self._load_yaml("company/departments.yaml")

        # Track data quality
        registry_missing = not registry_path.exists()
        dept_missing = not dept_path.exists()

        if registry_missing and dept_missing:
            quality = "error"
            error_msg = "Both agent-registry.json and departments.yaml missing"
        elif registry_missing or dept_missing:
            quality = "fallback"
            error_msg = "One or more source files missing"
        else:
            quality = "real"
            error_msg = None

        total_agents = len(registry)

        # Agents by department
        dept_counter: Counter[str] = Counter()
        for agent in registry:
            dept = agent.get("department") or "unassigned"
            dept_counter[dept] += 1
        agents_by_department = dict(dept_counter)

        # Department coverage: how many declared departments have at least one agent
        declared_depts = departments_data.get("departments", [])
        departments_with_agents = sum(1 for d in declared_depts if d.get("totalAgents", 0) > 0)
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
                "total_agents": self._kpi(
                    total_agents, None, "count", data_quality=quality, error=error_msg
                ),
                "agents_by_department": {
                    "current": agents_by_department,
                    "target": None,
                    "unit": "breakdown",
                    "status": "info",
                    "data_quality": quality,
                    "error": error_msg,
                },
                "department_coverage": self._kpi(
                    coverage_pct, 100, "%", data_quality=quality, error=error_msg
                ),
                "declared_departments": self._kpi(
                    total_declared, None, "count", data_quality=quality, error=error_msg
                ),
            },
        }
