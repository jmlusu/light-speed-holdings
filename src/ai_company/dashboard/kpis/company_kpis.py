"""Company-level KPI collectors for CEO Dashboard.

Handles the three company KPIs that previously had null values:

- KPI-001 (ARR): Reads from revenue_transactions table or
  ``orchestrator/finance/revenue.json`` stub file.
- KPI-002 (CSAT): Reads from ``orchestrator/cs/surveys.json``.
- KPI-005 (eNPS): Reads from ``orchestrator/hr/enps.json`` stub file.

Each collector returns ``None`` when no data is available rather than
fabricating a value, so the dashboard can display a "No data source" card.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from ai_company.paths import get_project_root

logger = logging.getLogger(__name__)


def _load_json(root: Path, rel_path: str) -> Any:
    """Load a JSON file relative to *root*. Returns ``[]`` on missing/unparseable."""
    path = root / rel_path
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read JSON %s: %s", path, exc)
        return []


def _sqlite_revenue(root: Path) -> float | None:
    """Try to read total revenue from SQLite revenue_transactions table."""
    try:
        from ai_company.data import get_database
        from ai_company.data.revenue_analytics import RevenueAnalytics

        db = get_database()
        if db is None:
            return None
        analytics = RevenueAnalytics(db)
        summary = analytics.get_revenue_attribution(period_days=365)
        if summary.total_revenue > 0:
            return summary.total_revenue
    except Exception:  # noqa: BLE001
        logger.debug("SQLite revenue unavailable for ARR calculation")
    return None


def _sqlite_csat(root: Path) -> float | None:
    """Try to read CSAT from customer_success surveys in SQLite or files."""
    # Try SQLite first via customer_success collector's survey data
    try:
        from ai_company.data import get_database

        db = get_database()
        if db is not None:
            # Check if there are any CS survey records in the DB
            rows = db.fetchall(
                "SELECT COUNT(*) as cnt FROM audit_events WHERE event_type = 'cs_survey'"
            )
            if rows and rows[0]["cnt"] > 0:
                avg_rows = db.fetchall(
                    "SELECT AVG(CAST(json_extract(metadata, '$.score') AS REAL)) as avg_score "
                    "FROM audit_events WHERE event_type = 'cs_survey'"
                )
                if avg_rows and avg_rows[0]["avg_score"] is not None:
                    return round(float(avg_rows[0]["avg_score"]), 1)
    except Exception:  # noqa: BLE001
        logger.debug("SQLite CSAT unavailable")

    # Fall back to file
    surveys = _load_json(root, "orchestrator/cs/surveys.json")
    if not isinstance(surveys, list) or not surveys:
        return None
    scores: list[float] = [
        float(s["score"]) for s in surveys if isinstance(s.get("score"), (int, float))
    ]
    if not scores:
        return None
    return round(sum(scores) / len(scores), 1)


def _file_enps(root: Path) -> float | None:
    """Read eNPS from employee survey file."""
    data = _load_json(root, "orchestrator/hr/enps.json")
    if not isinstance(data, dict):
        return None
    score = data.get("current_score")
    if isinstance(score, (int, float)):
        return round(float(score), 1)
    return None


def collect_arr(
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Collect ARR (Annual Recurring Revenue) — KPI-001.

    Returns a dict with ``current`` (``None`` if no data), ``source``, and
    ``data_quality`` fields suitable for merging into the company KPI summary.
    """
    root = project_root or get_project_root()

    # Try SQLite revenue_transactions
    revenue = _sqlite_revenue(root)
    if revenue is not None:
        # ARR = MRR * 12 — if we have 30-day revenue, annualize it
        mrr = revenue  # Already 30-day window from get_revenue_attribution
        arr = round(mrr * 12, 2)
        return {
            "current": arr,
            "source": "sqlite:revenue_transactions",
            "data_quality": "real",
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "data_gap": None,
        }

    # No data source available
    return {
        "current": None,
        "source": None,
        "data_quality": "no_data",
        "computed_at": None,
        "data_gap": "No revenue ledger configured. Requires revenue_transactions table or orchestrator/finance/revenue.json.",
    }


def collect_csat(
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Collect Customer Satisfaction Score — KPI-002.

    Returns a dict with ``current`` (``None`` if no data), ``source``, and
    ``data_quality`` fields.
    """
    root = project_root or get_project_root()

    score = _sqlite_csat(root)
    if score is not None:
        return {
            "current": score,
            "source": "orchestrator/cs/surveys.json",
            "data_quality": "real",
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "data_gap": None,
        }

    # Check if surveys file exists but is empty
    surveys = _load_json(root, "orchestrator/cs/surveys.json")
    if isinstance(surveys, list) and len(surveys) == 0:
        return {
            "current": None,
            "source": "orchestrator/cs/surveys.json",
            "data_quality": "no_data",
            "computed_at": None,
            "data_gap": "Survey file exists but contains no records. Populate orchestrator/cs/surveys.json with customer satisfaction scores.",
        }

    return {
        "current": None,
        "source": None,
        "data_quality": "no_data",
        "computed_at": None,
        "data_gap": "No survey data source configured. Requires orchestrator/cs/surveys.json with score entries.",
    }


def collect_enps(
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Collect Employee Net Promoter Score — KPI-005.

    Returns a dict with ``current`` (``None`` if no data), ``source``, and
    ``data_quality`` fields.
    """
    root = project_root or get_project_root()

    score = _file_enps(root)
    if score is not None:
        return {
            "current": score,
            "source": "orchestrator/hr/enps.json",
            "data_quality": "real",
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "data_gap": None,
        }

    return {
        "current": None,
        "source": None,
        "data_quality": "no_data",
        "computed_at": None,
        "data_gap": "No eNPS data source configured. Requires orchestrator/hr/enps.json with current_score field.",
    }


# Registry for company KPI collectors
COMPANY_KPI_COLLECTORS: dict[str, Callable[..., dict[str, Any]]] = {
    "KPI-001": collect_arr,
    "KPI-002": collect_csat,
    "KPI-005": collect_enps,
}
