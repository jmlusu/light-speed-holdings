"""Finance department KPI collector — reads kpis.yaml config and cost data."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector


class FinanceKPICollector(KPICollector):
    """Collects live metrics for the Finance department."""

    department = "finance"

    def collect(self) -> dict[str, Any]:
        kpi_config = self._load_yaml("company/config/kpis.yaml")
        cost_data = self._load_json("orchestrator/cost_tracker.json")
        registry = self._load_json("company/agent-registry.json")

        finance_config = kpi_config.get("departments", {}).get("finance", {})
        kpi_defs = {k["id"]: k for k in finance_config.get("kpis", [])}

        total_agents = len(registry) if isinstance(registry, list) else 0

        # Budget utilisation from cost tracker if available
        total_budget: float = kpi_defs.get("budget_utilization", {}).get("target", 90)
        total_spent = 0.0
        if isinstance(cost_data, dict):
            total_budget = cost_data.get("total_budget", total_budget)
            total_spent = cost_data.get("total_spent", 0.0)
        elif isinstance(cost_data, list) and cost_data:
            # If it's a list of expense records, sum them
            total_spent = sum(item.get("amount", 0) for item in cost_data)

        budget_utilization = (
            round((total_spent / total_budget * 100), 1)
            if total_budget > 0
            else 0.0
        )

        # Estimated monthly LLM spend from cost tracker
        estimated_llm_spend: float = 0.0
        if isinstance(cost_data, dict):
            estimated_llm_spend = cost_data.get("llm_spend", 0.0)

        # Cost per agent
        cost_per_agent = (
            round(total_spent / total_agents, 2) if total_agents > 0 else 0.0
        )

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "budget_utilization": self._kpi(budget_utilization, 90, "%"),
                "estimated_llm_spend": self._kpi(
                    estimated_llm_spend, None, "$",
                ),
                "total_budget": self._kpi(total_budget, None, "$"),
                "total_spent": self._kpi(total_spent, None, "$"),
                "cost_per_agent": self._kpi(cost_per_agent, 50, "$/month"),
                "active_agents": self._kpi(total_agents, None, "count"),
            },
        }
