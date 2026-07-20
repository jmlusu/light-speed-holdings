"""Sales department service layer.

Provides lead management, deal pipeline, and forecasting with
MessageBus integration for task delegation.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from ai_company.models.task import TaskPriority
from ai_company.services.base import BaseService

logger = logging.getLogger(__name__)


class SalesService(BaseService):
    """Service layer for the Sales department.

    Manages leads, deals, pipeline, and forecasting.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(department_id="sales", **kwargs)

    # ── Lead management ───────────────────────────────────────────────

    def list_leads(self, status: str = "") -> list[dict[str, Any]]:
        """List all leads, optionally filtered by status."""
        data = self._load_data("pipeline.yaml")
        leads = data.get("leads", [])
        if status:
            leads = [ld for ld in leads if ld.get("status") == status]
        return leads

    def add_lead(
        self,
        lead_id: str,
        name: str,
        source: str = "website",
        contact_email: str = "",
        company: str = "",
    ) -> dict[str, Any]:
        """Add a new sales lead."""
        data = self._load_data("pipeline.yaml")
        leads = data.get("leads", [])

        for lead in leads:
            if lead["id"] == lead_id:
                raise ValueError(f"Lead '{lead_id}' already exists")

        new_lead = {
            "id": lead_id,
            "name": name,
            "source": source,
            "contact_email": contact_email,
            "company": company,
            "status": "new",
            "created_at": datetime.now().isoformat(),
        }
        leads.append(new_lead)
        data["leads"] = leads
        self._save_data("pipeline.yaml", data)

        self.record_event(
            f"Lead '{name}' added from {source}",
            tags=["lead", "created", source],
            lead_id=lead_id,
        )

        # Delegate qualification task
        self.create_task(
            receiver_id="sales-specialist",
            instruction=(
                f"Qualify new lead '{name}' from {source}. "
                f"Company: {company or 'unknown'}. "
                f"Research their needs and prepare an initial outreach."
            ),
            priority=TaskPriority.MEDIUM,
        )

        return new_lead

    def update_lead_status(self, lead_id: str, new_status: str) -> dict[str, Any]:
        """Update lead status (new -> qualified -> meeting -> proposal -> closed)."""
        data = self._load_data("pipeline.yaml")
        leads = data.get("leads", [])

        lead = next((ld for ld in leads if ld["id"] == lead_id), None)
        if not lead:
            raise ValueError(f"Lead '{lead_id}' not found")

        old_status = lead.get("status", "")
        lead["status"] = new_status
        lead["updated_at"] = datetime.now().isoformat()
        data["leads"] = leads
        self._save_data("pipeline.yaml", data)

        self.record_event(
            f"Lead '{lead['name']}' status: {old_status} -> {new_status}",
            tags=["lead", "status_change", new_status],
            lead_id=lead_id,
        )
        return lead

    # ── Deal management ───────────────────────────────────────────────

    def list_deals(self, stage: str = "") -> list[dict[str, Any]]:
        """List all deals, optionally filtered by pipeline stage."""
        data = self._load_data("pipeline.yaml")
        deals = data.get("deals", [])
        if stage:
            deals = [d for d in deals if d.get("stage") == stage]
        return deals

    def add_deal(
        self,
        deal_id: str,
        name: str,
        value: float = 0.0,
        lead_id: str = "",
        owner: str = "",
    ) -> dict[str, Any]:
        """Add a new deal to the pipeline."""
        data = self._load_data("pipeline.yaml")
        deals = data.get("deals", [])

        for deal in deals:
            if deal["id"] == deal_id:
                raise ValueError(f"Deal '{deal_id}' already exists")

        new_deal = {
            "id": deal_id,
            "name": name,
            "value": value,
            "lead_id": lead_id,
            "owner": owner,
            "stage": "prospecting",
            "created_at": datetime.now().isoformat(),
        }
        deals.append(new_deal)
        data["deals"] = deals
        self._save_data("pipeline.yaml", data)

        self.record_event(
            f"Deal '{name}' created (${value:,.2f})",
            tags=["deal", "created"],
            deal_id=deal_id, value=value,
        )

        # Delegate discovery call task
        self.create_task(
            receiver_id="sales-specialist",
            instruction=(
                f"Schedule and conduct discovery call for deal '{name}' "
                f"(${value:,.2f}). Identify key stakeholders and pain points."
            ),
            priority=TaskPriority.MEDIUM if value < 50000 else TaskPriority.HIGH,
        )

        return new_deal

    def advance_deal(self, deal_id: str, new_stage: str) -> dict[str, Any]:
        """Move a deal to the next pipeline stage."""
        data = self._load_data("pipeline.yaml")
        deals = data.get("deals", [])

        deal = next((d for d in deals if d["id"] == deal_id), None)
        if not deal:
            raise ValueError(f"Deal '{deal_id}' not found")

        old_stage = deal.get("stage", "")
        deal["stage"] = new_stage
        deal["updated_at"] = datetime.now().isoformat()
        data["deals"] = deals
        self._save_data("pipeline.yaml", data)

        self.record_event(
            f"Deal '{deal['name']}' stage: {old_stage} -> {new_stage}",
            tags=["deal", "stage_change", new_stage],
            deal_id=deal_id,
        )
        return deal

    # ── Pipeline summary ──────────────────────────────────────────────

    def get_pipeline_summary(self) -> dict[str, Any]:
        """Get pipeline summary with total value, active deals, etc."""
        data = self._load_data("pipeline.yaml")
        deals = data.get("deals", [])
        leads = data.get("leads", [])

        active_stages = ["prospecting", "qualification", "proposal", "negotiation"]
        active_deals = [d for d in deals if d.get("stage") in active_stages]
        total_value = sum(d.get("value", 0) for d in active_deals)
        closed_won = [d for d in deals if d.get("stage") == "closed_won"]
        closed_won_value = sum(d.get("value", 0) for d in closed_won)

        return {
            "total_leads": len(leads),
            "new_leads": sum(1 for ld in leads if ld.get("status") == "new"),
            "total_deals": len(deals),
            "active_deals": len(active_deals),
            "pipeline_value": total_value,
            "closed_won": len(closed_won),
            "closed_won_value": closed_won_value,
        }

    def get_summary(self) -> dict[str, Any]:
        """Sales department summary."""
        return {
            **super().get_summary(),
            **self.get_pipeline_summary(),
        }
