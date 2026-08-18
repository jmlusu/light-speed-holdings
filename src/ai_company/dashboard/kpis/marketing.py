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

        tasks = self._tasks_from_sqlite()
        tasks_source = "sqlite" if tasks is not None else None
        if tasks is None:
            tasks = self._tasks_from_bus()
            if tasks:
                tasks_source = "message_bus"

        # Count marketing-related tasks (receiver is cmo or marketing specialist)
        marketing_tasks = [
            t
            for t in tasks
            if t.get("receiver_id") in ("cmo", "content_creator", "content_writer", "growth_hacker")
        ]
        completed_marketing = sum(1 for t in marketing_tasks if t.get("status") == "completed")
        total_marketing = len(marketing_tasks)
        task_completion_rate = (
            round((completed_marketing / total_marketing * 100), 1) if total_marketing > 0 else None
        )

        # Campaign count
        campaign_list = campaigns if isinstance(campaigns, list) else []
        active_campaigns = sum(1 for c in campaign_list if c.get("status") == "active")

        # Content quality average
        content_list = content_log if isinstance(content_log, list) else []
        scores = [c.get("quality_score", 0) for c in content_list if c.get("quality_score")]
        avg_quality = round(sum(scores) / len(scores), 1) if scores else None

        # Data quality for task-based KPIs
        if tasks_source == "sqlite":
            tasks_quality = "real"
            tasks_error = None
        elif tasks_source == "message_bus":
            tasks_quality = "fallback"
            tasks_error = "Using MessageBus (SQLite unavailable)"
        else:
            tasks_quality = "error"
            tasks_error = "No task data available (SQLite and MessageBus both unavailable)"

        # Data quality for campaign/content files
        campaigns_missing = not (
            self.root / "orchestrator" / "marketing" / "campaigns.json"
        ).exists()
        content_missing = not (
            self.root / "orchestrator" / "marketing" / "content_log.json"
        ).exists()
        if campaigns_missing and content_missing:
            marketing_file_quality = "error"
            marketing_file_error = "Marketing data files missing"
        elif campaigns_missing or content_missing:
            marketing_file_quality = "fallback"
            marketing_file_error = "Some marketing data files missing"
        else:
            marketing_file_quality = "real"
            marketing_file_error = None

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "campaign_generation_rate": self._kpi(
                    len(campaign_list),
                    5,
                    "campaigns",
                    data_quality=marketing_file_quality,
                    error=marketing_file_error,
                ),
                "active_campaigns": self._kpi(
                    active_campaigns,
                    None,
                    "count",
                    data_quality=marketing_file_quality,
                    error=marketing_file_error,
                ),
                "content_quality_score": self._kpi(
                    avg_quality,
                    8,
                    "score",
                    data_quality=marketing_file_quality,
                    error=marketing_file_error,
                ),
                "marketing_task_completion": self._kpi(
                    task_completion_rate,
                    90,
                    "%",
                    data_quality=tasks_quality,
                    error=tasks_error,
                ),
                "total_marketing_tasks": self._kpi(
                    total_marketing, None, "count", data_quality=tasks_quality, error=tasks_error
                ),
                "content_pieces_produced": self._kpi(
                    len(content_list),
                    None,
                    "count",
                    data_quality=marketing_file_quality,
                    error=marketing_file_error,
                ),
            },
        }
