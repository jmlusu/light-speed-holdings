"""KPI collectors for each department — live data from operational files."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from ai_company.dashboard.kpis.base import KPICollector
from ai_company.dashboard.kpis.customer_success import CustomerSuccessKPICollector
from ai_company.dashboard.kpis.engineering import EngineeringKPICollector
from ai_company.dashboard.kpis.finance import FinanceKPICollector
from ai_company.dashboard.kpis.hr import HRKPICollector
from ai_company.dashboard.kpis.legal import LegalKPICollector
from ai_company.dashboard.kpis.marketing import MarketingKPICollector
from ai_company.dashboard.kpis.sales import SalesKPICollector
from ai_company.data.database import Database
from ai_company.paths import get_project_root

ALL_COLLECTORS: list[type[KPICollector]] = [
    EngineeringKPICollector,
    HRKPICollector,
    FinanceKPICollector,
    MarketingKPICollector,
    SalesKPICollector,
    CustomerSuccessKPICollector,
    LegalKPICollector,
]


def collect_all_kpis(
    project_root: Path | None = None,
    database: Database | None = None,
) -> dict[str, Any]:
    """Run every department collector and return an aggregated snapshot.

    Parameters
    ----------
    project_root:
        Project root for the file-based collectors. ``None`` resolves the
        real ``ai-company`` root deterministically (``get_project_root``).
    database:
        Optional SQLite database; when populated it is the preferred source
        for tasks / costs / escalations (Sprint 2, Item 2).

    Returns
    -------
    dict
        Top-level keys: ``collected_at`` (ISO timestamp) and ``departments``
        (dict keyed by department id containing each collector's output).
    """
    root = project_root or get_project_root()

    departments: dict[str, Any] = {}
    for collector_cls in ALL_COLLECTORS:
        collector = collector_cls(project_root=root, database=database)
        result = collector.collect()
        departments[collector.department] = result

    return {
        "collected_at": datetime.now().isoformat(),
        "departments": departments,
    }


__all__ = [
    "ALL_COLLECTORS",
    "KPICollector",
    "collect_all_kpis",
]
