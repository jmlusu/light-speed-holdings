"""Abstract base class for department KPI collectors."""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
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
            logger.debug("KPI database not usable; falling back to files", exc_info=True)
        return None

    def _tasks_from_sqlite(self) -> list[dict[str, Any]] | None:
        """Return all tasks from SQLite when populated, else ``None``."""
        db = self._usable_database()
        if db is None:
            return None
        try:
            from ai_company.data import TaskStore

            store = TaskStore(db)
            if store.count() > 0:
                return [task.model_dump() for task in store.get_all_tasks()]
        except Exception:  # noqa: BLE001 - read-through must never raise
            logger.debug("SQLite task read failed; using MessageBus", exc_info=True)
        return None

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
            logger.debug("MessageBus task read failed; using empty task list", exc_info=True)
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
            logger.debug("SQLite cost read failed; using cost_tracker.json", exc_info=True)
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
            logger.debug("SQLite escalation read failed; using escalation.yaml", exc_info=True)
        return None

    def _kpi(
        self,
        current: float | int,
        target: float | int | None,
        unit: str,
        *,
        higher_is_better: bool = True,
    ) -> dict[str, Any]:
        """Build a standard KPI value dict with automatic status inference."""
        if target is None:
            status = "info"
        elif higher_is_better:
            status = "on_track" if current >= target else "below_target"
        else:
            status = "on_track" if current <= target else "above_target"
        return {
            "current": current,
            "target": target,
            "unit": unit,
            "status": status,
        }
