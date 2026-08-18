"""Org Health KPI collector — computes and stores the composite health score."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector
from ai_company.data.database import Database

logger = logging.getLogger(__name__)


class OrgHealthKPICollector(KPICollector):
    """Collects the composite org-health score as a virtual KPI.

    Runs :class:`OrgHealthCalculator`, stores the composite score and
    each component score via ``KPIPipeline.ingest_individual``, and returns
    a snapshot compatible with ``collect_all_kpis()``.
    """

    department = "org_health"

    def __init__(
        self,
        project_root: Path | None = None,
        database: Database | None = None,
    ) -> None:
        super().__init__(project_root=project_root, database=database)

    def collect(self) -> dict[str, Any]:
        """Compute org health and return a KPI snapshot dict."""
        from ai_company.dashboard.org_health import OrgHealthCalculator

        calculator = OrgHealthCalculator(project_root=self.root)
        result = calculator.compute(database=self.database)

        kpis: dict[str, Any] = {}
        kpis["composite_score"] = {
            "current": result.score,
            "target": None,
            "unit": "score",
            "status": result.band,
        }
        for comp in result.components:
            kpis[f"component:{comp.name}"] = {
                "current": comp.value,
                "target": None,
                "unit": "score",
                "status": "info",
            }

        return {
            "department": self.department,
            "kpis": kpis,
        }
