"""Marketing department KPI collector."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector


class MarketingKPICollector(KPICollector):
    """Collects live metrics for the Marketing department."""

    department = "marketing"

    def collect(self) -> dict[str, Any]:
        campaigns = self._load_json("orchestrator/marketing/campaigns.json")
        content_log = self._load_json("orchestrator/marketing/content_log.json")
        tasks = self._get_tasks()

        # Count marketing-related tasks (receiver is cmo or marketing specialist)
        marketing_tasks = [
            t for t in tasks
            if t.get("receiver_id") in ("cmo", "content-creator", "content-writer", "growth-hacker")
        ]
        completed_marketing = sum(
            1 for t in marketing_tasks if t.get("status") == "completed"
        )
        total_marketing = len(marketing_tasks)
        task_completion_rate = (
            round((completed_marketing / total_marketing * 100), 1)
            if total_marketing > 0
            else 0.0
        )

        # Campaign count
        campaign_list = campaigns if isinstance(campaigns, list) else []
        active_campaigns = sum(
            1 for c in campaign_list if c.get("status") == "active"
        )

        # Content quality average
        content_list = content_log if isinstance(content_log, list) else []
        scores = [c.get("quality_score", 0) for c in content_list if c.get("quality_score")]
        avg_quality = (
            round(sum(scores) / len(scores), 1) if scores else 0.0
        )

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "campaign_generation_rate": self._kpi(
                    len(campaign_list), 5, "campaigns",
                ),
                "active_campaigns": self._kpi(active_campaigns, None, "count"),
                "content_quality_score": self._kpi(avg_quality, 8, "score"),
                "marketing_task_completion": self._kpi(
                    task_completion_rate, 90, "%",
                ),
                "total_marketing_tasks": self._kpi(total_marketing, None, "count"),
                "content_pieces_produced": self._kpi(len(content_list), None, "count"),
            },
        }
