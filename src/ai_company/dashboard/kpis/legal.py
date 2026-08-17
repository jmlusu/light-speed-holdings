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

    def _check_sop_status(self) -> tuple[bool, float | None, str | None]:
        """Check if Legal SOP exists and is current (updated within 90 days).

        Returns:
            Tuple of (is_current, freshness_pct, error_message). error_message is None on success.
        """
        sop_path = self.root / "docs" / "sop" / "legal-sop.md"
        if not sop_path.exists():
            return False, None, "SOP file not found"
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
                return (
                    is_current,
                    round((90 - days_old) / 90 * 100, 1) if is_current else None,
                    None,
                )
        except (OSError, ValueError, AttributeError) as exc:
            logger.warning(
                "Failed to parse Legal SOP freshness (%s): %s",
                sop_path,
                exc,
            )
            return False, None, f"Failed to parse SOP date: {exc}"
        return False, None, "SOP date not found or invalid"

    def _compute_contract_review_time(
        self, contracts: list[dict[str, Any]]
    ) -> tuple[float | None, str | None]:
        """Compute average contract review time in hours from contract timestamps.

        Returns:
            Tuple of (avg_review_hours, error_message). error_message is None on success.
        """
        reviewed_contracts = [
            c
            for c in contracts
            if c.get("status") in ("approved", "rejected")
            and c.get("created_at")
            and c.get("reviewed_at")
        ]

        if not reviewed_contracts:
            return None, "No reviewed contracts with timestamps available"

        review_times = []
        for contract in reviewed_contracts:
            try:
                created = datetime.fromisoformat(contract["created_at"].replace("Z", "+00:00"))
                reviewed = datetime.fromisoformat(contract["reviewed_at"].replace("Z", "+00:00"))
                diff_hours = (reviewed - created).total_seconds() / 3600
                if diff_hours >= 0:  # Only count valid positive durations
                    review_times.append(diff_hours)
            except (ValueError, AttributeError) as exc:
                logger.warning(
                    "Failed to parse timestamps for contract %s: %s", contract.get("id"), exc
                )

        if not review_times:
            return None, "No valid timestamp pairs found in reviewed contracts"

        avg_review = round(sum(review_times) / len(review_times), 1)
        return avg_review, None

    def collect(self) -> dict[str, Any]:
        contracts = self._load_json("orchestrator/legal/contracts.json")
        compliance = self._load_json("orchestrator/legal/compliance_log.json")

        tasks = self._tasks_from_sqlite()
        tasks_source = "sqlite" if tasks is not None else None
        if tasks is None:
            tasks = self._tasks_from_bus()
            if tasks:
                tasks_source = "message_bus"

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
            round((completed_legal / total_legal * 100), 1) if total_legal > 0 else None
        )

        # Contract metrics
        contract_list = contracts if isinstance(contracts, list) else []
        pending_review = sum(1 for c in contract_list if c.get("status") == "pending_review")
        approved_contracts = sum(1 for c in contract_list if c.get("status") == "approved")
        total_contracts = len(contract_list)

        # Compute contract review time from timestamps
        avg_review_time, review_error = self._compute_contract_review_time(contract_list)
        if avg_review_time is not None:
            review_quality = "real"
            review_error = None
        else:
            review_quality = "error"
            # Use default target as fallback but mark as error
            avg_review_time = 0.0

        # Compliance
        compliance_list = compliance if isinstance(compliance, list) else []
        passing = sum(1 for c in compliance_list if c.get("result") == "pass")
        total_checks = len(compliance_list)
        compliance_score = round((passing / total_checks * 100), 1) if total_checks > 0 else None

        # SOP Compliance
        sop_current, sop_freshness, sop_error = self._check_sop_status()

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

        # Data quality for contract/compliance (file-based)
        contracts_missing = not (self.root / "orchestrator" / "legal" / "contracts.json").exists()
        compliance_missing = not (
            self.root / "orchestrator" / "legal" / "compliance_log.json"
        ).exists()
        if contracts_missing and compliance_missing:
            legal_file_quality = "error"
            legal_file_error = "Legal data files missing"
        elif contracts_missing or compliance_missing:
            legal_file_quality = "fallback"
            legal_file_error = "Some legal data files missing"
        else:
            legal_file_quality = "real"
            legal_file_error = None

        # SOP data quality
        sop_quality = "error" if sop_error else "real"

        return {
            "department": self.department,
            "collected_at": datetime.now().isoformat(),
            "kpis": {
                "contract_review_time": self._kpi(
                    avg_review_time,
                    2,
                    "hours",
                    data_quality=review_quality,
                    error=review_error,
                ),
                "pending_contract_reviews": self._kpi(
                    pending_review,
                    0,
                    "count",
                    higher_is_better=False,
                    data_quality=legal_file_quality,
                    error=legal_file_error,
                ),
                "approved_contracts": self._kpi(
                    approved_contracts,
                    None,
                    "count",
                    data_quality=legal_file_quality,
                    error=legal_file_error,
                ),
                "total_contracts": self._kpi(
                    total_contracts,
                    None,
                    "count",
                    data_quality=legal_file_quality,
                    error=legal_file_error,
                ),
                "compliance_score": self._kpi(
                    compliance_score,
                    100,
                    "%",
                    data_quality=legal_file_quality,
                    error=legal_file_error,
                ),
                "total_compliance_checks": self._kpi(
                    total_checks,
                    None,
                    "count",
                    data_quality=legal_file_quality,
                    error=legal_file_error,
                ),
                "legal_task_completion": self._kpi(
                    task_completion_rate, 90, "%", data_quality=tasks_quality, error=tasks_error
                ),
                "total_legal_tasks": self._kpi(
                    total_legal, None, "count", data_quality=tasks_quality, error=tasks_error
                ),
                # SOP Compliance
                "sop_current": self._kpi(
                    1 if sop_current else 0, 1, "bool", data_quality=sop_quality, error=sop_error
                ),
                "sop_freshness_pct": self._kpi(
                    sop_freshness, 100, "%", data_quality=sop_quality, error=sop_error
                ),
            },
        }
