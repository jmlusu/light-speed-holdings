"""Marketing department service layer.

Provides campaign management, content scheduling, and metrics tracking
with MessageBus integration for task delegation and memory recording.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from ai_company.models.task import TaskPriority
from ai_company.services.base import BaseService

logger = logging.getLogger(__name__)


class MarketingService(BaseService):
    """Service layer for the Marketing department.

    Manages campaigns, content scheduling, and metrics tracking.
    Integrates with MessageBus for delegating content creation tasks
    and records outcomes to memory.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(department_id="marketing", **kwargs)

    # ── Campaign management ───────────────────────────────────────────

    def list_campaigns(self) -> list[dict[str, Any]]:
        """List all marketing campaigns."""
        data = self._load_data("campaigns.yaml")
        return data.get("campaigns", [])

    def create_campaign(
        self,
        campaign_id: str,
        name: str,
        channel: str = "email",
        target_audience: str = "",
        budget: float = 0.0,
    ) -> dict[str, Any]:
        """Create a new marketing campaign.

        Creates the campaign record, then delegates a content planning
        task to the marketing specialist agent.
        """
        data = self._load_data("campaigns.yaml")
        campaigns = data.get("campaigns", [])

        # Check for duplicates
        for c in campaigns:
            if c["id"] == campaign_id:
                raise ValueError(f"Campaign '{campaign_id}' already exists")

        campaign = {
            "id": campaign_id,
            "name": name,
            "channel": channel,
            "target_audience": target_audience,
            "budget": budget,
            "status": "draft",
            "created_at": datetime.now().isoformat(),
            "metrics": {"impressions": 0, "clicks": 0, "conversions": 0},
        }
        campaigns.append(campaign)
        data["campaigns"] = campaigns
        self._save_data("campaigns.yaml", data)

        # Record in memory
        self.record_event(
            f"Campaign '{name}' created (channel={channel}, budget=${budget})",
            tags=["campaign", "created", channel],
            campaign_id=campaign_id,
        )

        # Delegate content planning task
        self.create_task(
            receiver_id="marketing-specialist",
            instruction=(
                f"Create content plan for campaign '{name}'. "
                f"Channel: {channel}. Target audience: {target_audience or 'general'}. "
                f"Budget: ${budget:,.2f}."
            ),
            priority=TaskPriority.MEDIUM,
        )

        logger.info("Campaign '%s' created and content task delegated.", name)
        return campaign

    def launch_campaign(self, campaign_id: str) -> dict[str, Any]:
        """Launch a marketing campaign (change status to active)."""
        data = self._load_data("campaigns.yaml")
        campaigns = data.get("campaigns", [])

        campaign = next((c for c in campaigns if c["id"] == campaign_id), None)
        if not campaign:
            raise ValueError(f"Campaign '{campaign_id}' not found")

        campaign["status"] = "active"
        campaign["launched_at"] = datetime.now().isoformat()
        data["campaigns"] = campaigns
        self._save_data("campaigns.yaml", data)

        self.record_event(
            f"Campaign '{campaign['name']}' launched",
            tags=["campaign", "launched"],
            campaign_id=campaign_id,
        )

        # Create monitoring task
        self.create_task(
            receiver_id="marketing-specialist",
            instruction=(
                f"Monitor campaign '{campaign['name']}' performance. "
                f"Track impressions, clicks, and conversions daily."
            ),
            priority=TaskPriority.LOW,
        )

        return campaign

    def pause_campaign(self, campaign_id: str) -> dict[str, Any]:
        """Pause a running campaign."""
        data = self._load_data("campaigns.yaml")
        campaigns = data.get("campaigns", [])

        campaign = next((c for c in campaigns if c["id"] == campaign_id), None)
        if not campaign:
            raise ValueError(f"Campaign '{campaign_id}' not found")

        campaign["status"] = "paused"
        campaign["paused_at"] = datetime.now().isoformat()
        data["campaigns"] = campaigns
        self._save_data("campaigns.yaml", data)

        self.record_event(
            f"Campaign '{campaign['name']}' paused",
            tags=["campaign", "paused"],
            campaign_id=campaign_id,
        )
        return campaign

    def update_metrics(
        self,
        campaign_id: str,
        impressions: int = 0,
        clicks: int = 0,
        conversions: int = 0,
    ) -> dict[str, Any]:
        """Update campaign metrics."""
        data = self._load_data("campaigns.yaml")
        campaigns = data.get("campaigns", [])

        campaign = next((c for c in campaigns if c["id"] == campaign_id), None)
        if not campaign:
            raise ValueError(f"Campaign '{campaign_id}' not found")

        metrics = campaign.get("metrics", {})
        metrics["impressions"] = metrics.get("impressions", 0) + impressions
        metrics["clicks"] = metrics.get("clicks", 0) + clicks
        metrics["conversions"] = metrics.get("conversions", 0) + conversions
        campaign["metrics"] = metrics
        data["campaigns"] = campaigns
        self._save_data("campaigns.yaml", data)
        return campaign

    def get_campaign_metrics(self, campaign_id: str) -> dict[str, Any]:
        """Get metrics for a specific campaign."""
        data = self._load_data("campaigns.yaml")
        campaigns = data.get("campaigns", [])

        campaign = next((c for c in campaigns if c["id"] == campaign_id), None)
        if not campaign:
            raise ValueError(f"Campaign '{campaign_id}' not found")
        return campaign.get("metrics", {})

    # ── Reporting ─────────────────────────────────────────────────────

    def get_summary(self) -> dict[str, Any]:
        """Marketing department summary."""
        campaigns = self.list_campaigns()
        active = [c for c in campaigns if c.get("status") == "active"]
        total_impressions = sum(c.get("metrics", {}).get("impressions", 0) for c in campaigns)
        total_clicks = sum(c.get("metrics", {}).get("clicks", 0) for c in campaigns)
        total_conversions = sum(c.get("metrics", {}).get("conversions", 0) for c in campaigns)

        return {
            **super().get_summary(),
            "total_campaigns": len(campaigns),
            "active_campaigns": len(active),
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "conversion_rate": (
                round(total_conversions / total_clicks * 100, 2)
                if total_clicks > 0
                else 0.0
            ),
        }
