"""Sales department KPI collector."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector


class SalesKPICollector(KPICollector):
    """Collects live metrics for the Sales department."""

    department = "sales"

    def collect(self) -> dict[str, Any]:
        pipeline = self._load_json("orchestrator/sales/pipeline.json")
        leads = self._load_json("orchestrator/sales/leads.json")
        tasks = self._get_tasks()

        # Count sales-related tasks
        sales_receivers = {"sales", "business_developer"}
        sales_tasks = [
            t for t in tasks if t.get("receiver_id") in sales_receivers
        ]
        completed_sales = sum(
            1 for t in sales_tasks if t.get("status") == "completed"
        )
        total_sales = len(sales_tasks)
        task_completion_rate = (
            round((completed_sales / total_sales * 100), 1)
            if total_sales > 0
            else 0.0
        )

        # Pipeline metrics
        pipeline_list = pipeline if isinstance(pipeline, list) else []
        total_pipeline_value = sum(p.get("value", 0) for p in pipeline_list)
        won_deals = sum(1 for p in pipeline_list if p.get("stage") == "won")
        total_deals = len(pipeline_list)
        win_rate = (
            round((won_deals / total_deals * 100), 1) if total_deals > 0 else 0.0
        )

        # Leads
        lead_list = leads if isinstance(leads, list) else []
        new_leads = sum(1 for lead in lead_list if lead.get("status") == "new")

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "pipeline_value": self._kpi(total_pipeline_value, None, "$"),
                "total_deals": self._kpi(total_deals, None, "count"),
                "win_rate": self._kpi(win_rate, 25, "%"),
                "new_leads": self._kpi(new_leads, None, "count"),
                "sales_task_completion": self._kpi(
                    task_completion_rate, 85, "%",
                ),
                "total_sales_tasks": self._kpi(total_sales, None, "count"),
            },
        }
