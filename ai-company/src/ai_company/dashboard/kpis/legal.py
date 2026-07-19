"""Legal department KPI collector."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector


class LegalKPICollector(KPICollector):
    """Collects live metrics for the Legal department."""

    department = "legal"

    def collect(self) -> dict[str, Any]:
        contracts = self._load_json("orchestrator/legal/contracts.json")
        compliance = self._load_json("orchestrator/legal/compliance_log.json")
        tasks = self._load_json(".opencode/inbox.json")

        # Count legal-related tasks
        legal_tasks = [
            t for t in tasks if t.get("receiver_id") in ("legal", "clo")
        ]
        completed_legal = sum(
            1 for t in legal_tasks if t.get("status") == "completed"
        )
        total_legal = len(legal_tasks)
        task_completion_rate = (
            round((completed_legal / total_legal * 100), 1)
            if total_legal > 0
            else 0.0
        )

        # Contract metrics
        contract_list = contracts if isinstance(contracts, list) else []
        pending_review = sum(
            1 for c in contract_list if c.get("status") == "pending_review"
        )
        approved_contracts = sum(
            1 for c in contract_list if c.get("status") == "approved"
        )
        total_contracts = len(contract_list)

        # Compliance
        compliance_list = compliance if isinstance(compliance, list) else []
        passing = sum(
            1 for c in compliance_list if c.get("result") == "pass"
        )
        total_checks = len(compliance_list)
        compliance_score = (
            round((passing / total_checks * 100), 1) if total_checks > 0 else 0.0
        )

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "contract_review_time": self._kpi(
                    0, 2, "hours",
                ),  # Needs timestamp data; default until available
                "pending_contract_reviews": self._kpi(
                    pending_review, 0, "count", higher_is_better=False,
                ),
                "approved_contracts": self._kpi(approved_contracts, None, "count"),
                "total_contracts": self._kpi(total_contracts, None, "count"),
                "compliance_score": self._kpi(compliance_score, 100, "%"),
                "total_compliance_checks": self._kpi(total_checks, None, "count"),
                "legal_task_completion": self._kpi(task_completion_rate, 90, "%"),
                "total_legal_tasks": self._kpi(total_legal, None, "count"),
            },
        }
