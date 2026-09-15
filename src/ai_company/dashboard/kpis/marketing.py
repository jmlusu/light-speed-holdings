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
        pharos_subscribers = self._load_json("orchestrator/marketing/pharos_subscribers.json")

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

        # Pharos content intelligence — publications / pipeline / audience.
        now = datetime.now()
        posts_published_30d = 0
        drafts_in_pipeline = 0
        for c in content_list:
            status = c.get("status")
            if status == "published":
                published_at = c.get("published_at")
                if published_at:
                    try:
                        pub_date = datetime.fromisoformat(str(published_at))
                        if pub_date.tzinfo is not None:
                            pub_date = pub_date.astimezone().replace(tzinfo=None)
                        if (now - pub_date).days <= 30:
                            posts_published_30d += 1
                    except (ValueError, TypeError):
                        posts_published_30d += 1
            elif status == "draft":
                drafts_in_pipeline += 1

        if isinstance(pharos_subscribers, dict):
            subscriber_count = pharos_subscribers.get("subscribers")
            if not isinstance(subscriber_count, (int, float)):
                subscriber_count = None
        elif isinstance(pharos_subscribers, (int, float)):
            subscriber_count = pharos_subscribers
        else:
            subscriber_count = None

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
        subscribers_missing = not (
            self.root / "orchestrator" / "marketing" / "pharos_subscribers.json"
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

        # Pharos content data quality (subscriber target parity with
        # Pharos KPI-0003: 2,000 subscribers target).
        pharos_quality = "real"
        pharos_error = None
        if content_missing and subscribers_missing:
            pharos_quality = "error"
            pharos_error = "Pharos content + subscriber data files missing"
        elif content_missing or subscribers_missing:
            pharos_quality = "fallback"
            pharos_error = "Some Pharos content data files missing"

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
                "posts_published_30d": self._kpi(
                    posts_published_30d,
                    None,
                    "count",
                    data_quality=pharos_quality,
                    error=pharos_error,
                ),
                "drafts_in_pipeline": self._kpi(
                    drafts_in_pipeline,
                    None,
                    "count",
                    data_quality=pharos_quality,
                    error=pharos_error,
                ),
                "subscribers": self._kpi(
                    subscriber_count,
                    2000,
                    "count",
                    data_quality=pharos_quality,
                    error=pharos_error,
                ),
            },
        }
