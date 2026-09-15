"""Abstract base class for department KPI collectors."""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from ai_company.data.database import Database
from ai_company.paths import get_project_root

logger = logging.getLogger(__name__)


class KPICollector(ABC):
    """Base class every department collector must subclass.

    Subclasses set a ``department`` class attribute and implement
    :meth:`collect` to return a dict whose top-level ``"kpis"`` key
    holds the live metric values.

    Args:
        project_root: Optional project root. ``None`` resolves it via
            :func:`ai_company.paths.get_project_root`.
        database: Optional SQLite database. When populated it is the
            preferred source for tasks / costs / escalations (Sprint 2,
            Item 2); collectors fall back to the legacy files otherwise.
    """

    department: str = ""  # Override in subclass, e.g. "engineering"

    def __init__(
        self,
        project_root: Path | None = None,
        database: Database | None = None,
    ) -> None:
        # Resolve the project root deterministically (see ai_company.paths)
        # so collectors read the real operational files regardless of CWD.
        self.root: Path = project_root or get_project_root()
        self.database: Database | None = database

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    def collect(self) -> dict[str, Any]:
        """Return ``{"department": ..., "kpis": {...}}`` with live metrics."""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _load_json(self, rel_path: str | Path) -> Any:
        """Load a JSON file relative to *project_root*.

        Returns ``[]`` for ``.json`` files or ``{}`` for missing data.
        Never raises on missing files — logs a debug message instead.
        """
        path = self.root / rel_path
        if not path.exists():
            logger.debug("JSON file not found, returning empty: %s", path)
            return []
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to read JSON %s: %s", path, exc)
            return []

    def _load_yaml(self, rel_path: str | Path) -> dict[str, Any]:
        """Load a YAML file relative to *project_root*.

        Returns ``{}`` when the file is absent or empty. Never raises.
        """
        path = self.root / rel_path
        if not path.exists():
            logger.debug("YAML file not found, returning empty: %s", path)
            return {}
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return yaml.safe_load(fh) or {}
        except (yaml.YAMLError, OSError) as exc:
            logger.warning("Failed to read YAML %s: %s", path, exc)
            return {}

    # ------------------------------------------------------------------
    # SQLite-first helpers (Sprint 2, Item 2)
    #
    # Each ``*_from_sqlite`` accessor returns ``None`` when the database is
    # unavailable or empty, signalling the caller to keep using the legacy
    # file store.  Mirrors ``dashboard.data_service`` read-through behaviour.
    # ------------------------------------------------------------------

    def _usable_database(self) -> Database | None:
        """Return a schema-initialised SQLite database, or ``None``."""
        from ai_company.data import get_database

        db = self.database or get_database()
        if db is None:
            return None
        try:
            if db.get_schema_version() > 0:
                return db
        except Exception:  # noqa: BLE001 - read-through must never raise
            logger.warning("KPI database not usable; falling back to files", exc_info=True)
        return None

    def _tasks_from_sqlite(self) -> list[dict[str, Any]] | None:
        """Return all tasks from SQLite when populated, else ``None``.

        Delegates to :func:`ai_company.dashboard.data_service.get_all_tasks`
        so the whole dashboard shares a single SQLite-first read-through
        (a missing or empty database yields ``None``, signalling the caller
        to fall back to the MessageBus).
        """
        from ai_company.dashboard.data_service import get_all_tasks

        return get_all_tasks(self.database)

    def _tasks_from_bus(self) -> list[dict[str, Any]]:
        """Return all task dicts through the shared dashboard MessageBus.

        GAP-011: the legacy read path opened ``.opencode/inbox.json``
        directly; the bus is now the single source of truth for task state.
        The bus is rooted at the dashboard StateStore base dir, which at
        boot equals the project root (or ``DASHBOARD_DATA_DIR``).

        Returns raw task dicts (same shape the file read produced) and
        ``[]`` when the inbox is missing or unreadable so collectors never
        raise and always produce their KPI shape.
        """
        try:
            from ai_company.dashboard.api import get_bus

            return get_bus().get_all_tasks_raw()
        except Exception:  # noqa: BLE001 - collectors must never raise
            logger.warning("MessageBus task read failed; using empty task list", exc_info=True)
            return []

    def _cost_from_sqlite(self) -> dict[str, Any] | None:
        """Return spend totals from SQLite when populated, else ``None``."""
        db = self._usable_database()
        if db is None:
            return None
        try:
            from ai_company.data import CostAnalytics

            cost = CostAnalytics(db)
            if cost.total_records() == 0:
                return None
            total_spent = cost.total_cost()
            return {"total_spent": total_spent, "llm_spend": total_spent}
        except Exception:  # noqa: BLE001 - read-through must never raise
            logger.warning("SQLite cost read failed; using cost_tracker.json", exc_info=True)
        return None

    def _revenue_from_sqlite(self) -> dict[str, Any] | None:
        """Return revenue summary from SQLite when populated, else ``None``."""
        db = self._usable_database()
        if db is None:
            return None
        try:
            from ai_company.data.revenue_analytics import RevenueAnalytics

            analytics = RevenueAnalytics(db)
            summary = analytics.get_revenue_attribution(period_days=30)
            return {
                "total_revenue": summary.total_revenue,
                "total_cost": summary.total_cost,
                "overall_roi": summary.overall_roi,
                "period_days": summary.period_days,
                "by_department": [
                    {
                        "department": a.department,
                        "revenue": a.revenue_attributed,
                        "cost": a.cost_incurred,
                        "roi": a.roi,
                        "tasks": a.tasks_completed,
                    }
                    for a in summary.by_department
                ],
            }
        except Exception:  # noqa: BLE001 - read-through must never raise
            logger.warning("SQLite revenue read failed; using fallback", exc_info=True)
        return None

    def _escalations_from_sqlite(self) -> list[dict[str, Any]] | None:
        """Return escalation events from SQLite when populated, else ``None``."""
        db = self._usable_database()
        if db is None:
            return None
        try:
            from ai_company.data import EscalationStore

            store = EscalationStore(db)
            if store.count() == 0:
                return None
            events = store.get_pending() + store.get_resolved()
            return [{**event, "resolved": bool(event.get("resolved", False))} for event in events]
        except Exception:  # noqa: BLE001 - read-through must never raise
            logger.warning("SQLite escalation read failed; using escalation.yaml", exc_info=True)
        return None

    def _kpi(
        self,
        current: float | int | None,
        target: float | int | None,
        unit: str,
        *,
        higher_is_better: bool = True,
        error: str | None = None,
        data_quality: str = "real",
    ) -> dict[str, Any]:
        """Build a standard KPI value dict with automatic status inference.

        Args:
            current: The current metric value, or None if unavailable.
            target: The target value for comparison, or None.
            unit: Unit of measurement (e.g., "%", "$", "count").
            higher_is_better: Whether higher values are better (for status).
            error: Optional error message if data collection failed.
            data_quality: One of "real" (live data), "fallback" (degraded source),
                or "error" (collection failed, value is default).
        """
        if current is None:
            status = "no_data"
        elif target is None:
            status = "info"
        elif higher_is_better:
            status = "on_track" if current >= target else "below_target"
        else:
            status = "on_track" if current <= target else "above_target"

        result = {
            "current": current,
            "target": target,
            "unit": unit,
            "status": status,
            "data_quality": data_quality,
        }
        if error:
            result["error"] = error
        return result

    def _sop_freshness(
        self, sop_path: Path, department: str
    ) -> tuple[bool, float | None, str | None]:
        """Check whether an SOP document is current (updated within 90 days).

        Parses a ``Last Updated: <Month Year>`` line and reports freshness as
        a percentage of the 90-day window remaining.  Shared by department
        collectors (engineering, legal, customer_success) so the SOP contract
        lives in exactly one module.

        Returns:
            ``(is_current, freshness_pct, error)`` where ``freshness_pct`` and
            ``error`` are ``None`` when unavailable / on success respectively.
        """
        import re

        if not sop_path.exists():
            return False, None, "SOP file not found"
        try:
            content = sop_path.read_text(encoding="utf-8")
            match = re.search(r"Last Updated:\s*([A-Za-z]+\s+\d{4})", content)
            if match:
                updated_dt = datetime.strptime(match.group(1), "%B %Y")
                now = datetime.now()
                days_old = (now - updated_dt).days
                is_current = days_old <= 90
                return (
                    is_current,
                    round((90 - days_old) / 90 * 100, 1) if is_current else None,
                    None,
                )
        except (OSError, ValueError, AttributeError) as exc:
            logger.warning("Failed to parse %s SOP freshness (%s): %s", department, sop_path, exc)
            return False, None, f"Failed to parse SOP date: {exc}"
        return False, None, "SOP date not found or invalid"

    def _compute_avg_duration(
        self,
        items: list[dict[str, Any]],
        statuses: list[str],
        start_key: str,
        end_key: str,
        *,
        no_items_msg: str,
        no_pairs_msg: str,
        item_label: str = "item",
    ) -> tuple[float | None, str | None]:
        """Compute the average hours between ``start`` and ``end`` timestamps.

        Filters *items* to those whose ``status`` is in *statuses* and which
        carry both timestamps, then averages the positive durations.  Returns
        ``(avg_hours, error)`` with ``error`` as ``None`` on success.  Shared
        by ticket / contract review-time collectors (F3) so the duration logic
        lives in exactly one module.
        """
        filtered = [
            it
            for it in items
            if it.get("status") in statuses and it.get(start_key) and it.get(end_key)
        ]
        if not filtered:
            return None, no_items_msg

        durations: list[float] = []
        for item in filtered:
            try:
                start = datetime.fromisoformat(item[start_key].replace("Z", "+00:00"))
                end = datetime.fromisoformat(item[end_key].replace("Z", "+00:00"))
                diff_hours = (end - start).total_seconds() / 3600
                if diff_hours >= 0:  # Only count valid positive durations
                    durations.append(diff_hours)
            except (ValueError, AttributeError) as exc:
                logger.warning(
                    "Failed to parse timestamps for %s %s: %s",
                    item_label,
                    item.get("id"),
                    exc,
                )

        if not durations:
            return None, no_pairs_msg
        return round(sum(durations) / len(durations), 1), None
