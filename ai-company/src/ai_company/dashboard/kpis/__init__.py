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

ALL_COLLECTORS: list[type[KPICollector]] = [
    EngineeringKPICollector,
    HRKPICollector,
    FinanceKPICollector,
    MarketingKPICollector,
    SalesKPICollector,
    CustomerSuccessKPICollector,
    LegalKPICollector,
]


def collect_all_kpis(project_root: Path | None = None) -> dict[str, Any]:
    """Run every department collector and return an aggregated snapshot.

    Returns
    -------
    dict
        Top-level keys: ``collected_at`` (ISO timestamp) and ``departments``
        (dict keyed by department id containing each collector's output).
    """
    root = project_root or Path(__file__).resolve().parents[3]

    departments: dict[str, Any] = {}
    for collector_cls in ALL_COLLECTORS:
        collector = collector_cls(project_root=root)
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
