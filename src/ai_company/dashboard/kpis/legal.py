"""Legal department KPI collector."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector

logger = logging.getLogger(__name__)


class LegalKPICollector(KPICollector):
    """Collects live metrics for the Legal department."""

    department = "legal"

    def _check_sop_status(self) -> tuple[bool, float]:
        """Check if Legal SOP exists and is current (updated within 90 days)."""
        sop_path = self.root / "docs" / "sop" / "legal-sop.md"
        if not sop_path.exists():
            return False, 0.0
        try:
            import re

            content = sop_path.read_text(encoding="utf-8")
            match = re.search(r"Last Updated:\s*([A-Za-z]+\s+\d{4})", content)
            if match:
                from datetime import datetime as dt

                updated_dt = dt.strptime(match.group(1), "%B %Y")
                now = datetime.now()
                days_old = (now - updated_dt).days
                is_current = days_old <= 90
                return is_current, round((90 - days_old) / 90 * 100, 1) if is_current else 0.0
        except (OSError, ValueError, AttributeError) as exc:
            logger.warning(
                "Failed to parse Legal SOP freshness (%s): %s",
                sop_path,
                exc,
            )
        return False, 0.0

    def collect(self) -> dict[str, Any]:
        contracts = self._load_json("orchestrator/legal/contracts.json")
        compliance = self._load_json("orchestrator/legal/compliance_log.json")
        tasks = self._tasks_from_sqlite()
        if tasks is None:
            tasks = self._tasks_from_bus()

        # Count legal-related tasks
        legal_tasks = [
            t
            for t in tasks
            if t.get("receiver_id")
            in (
                "legal",
                "clo",
                "legal_advisor",
                "legal_owner",
                "compliance_officer",
                "data_privacy_officer",
            )
        ]
        completed_legal = sum(1 for t in legal_tasks if t.get("status") == "completed")
        total_legal = len(legal_tasks)
        task_completion_rate = (
            round((completed_legal / total_legal * 100), 1) if total_legal > 0 else 0.0
        )

        # Contract metrics
        contract_list = contracts if isinstance(contracts, list) else []
        pending_review = sum(1 for c in contract_list if c.get("status") == "pending_review")
        approved_contracts = sum(1 for c in contract_list if c.get("status") == "approved")
        total_contracts = len(contract_list)

        # Compliance
        compliance_list = compliance if isinstance(compliance, list) else []
        passing = sum(1 for c in compliance_list if c.get("result") == "pass")
        total_checks = len(compliance_list)
        compliance_score = round((passing / total_checks * 100), 1) if total_checks > 0 else 0.0

        # SOP Compliance
        sop_current, sop_freshness = self._check_sop_status()

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "contract_review_time": self._kpi(
                    0,
                    2,
                    "hours",
                ),  # Needs timestamp data; default until available
                "pending_contract_reviews": self._kpi(
                    pending_review,
                    0,
                    "count",
                    higher_is_better=False,
                ),
                "approved_contracts": self._kpi(approved_contracts, None, "count"),
                "total_contracts": self._kpi(total_contracts, None, "count"),
                "compliance_score": self._kpi(compliance_score, 100, "%"),
                "total_compliance_checks": self._kpi(total_checks, None, "count"),
                "legal_task_completion": self._kpi(task_completion_rate, 90, "%"),
                "total_legal_tasks": self._kpi(total_legal, None, "count"),
                # SOP Compliance
                "sop_current": self._kpi(1 if sop_current else 0, 1, "bool"),
                "sop_freshness_pct": self._kpi(sop_freshness, 100, "%"),
            },
        }
