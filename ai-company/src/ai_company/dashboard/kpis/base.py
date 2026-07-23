"""Abstract base class for department KPI collectors."""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class KPICollector(ABC):
    """Base class every department collector must subclass.

    Subclasses set a ``department`` class attribute and implement
    :meth:`collect` to return a dict whose top-level ``"kpis"`` key
    holds the live metric values.
    """

    department: str = ""  # Override in subclass, e.g. "engineering"

    def __init__(
        self,
        project_root: Path | None = None,
        message_bus: Any | None = None,
    ) -> None:
        # Default to three levels up from this file → ai-company/
        self.root: Path = project_root or Path(__file__).resolve().parents[3]
        self._message_bus = message_bus

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

    def _get_tasks(self) -> list[dict[str, Any]]:
        """Return task dicts from the MessageBus if available, else from file.

        GAP-011 fix: routes task reads through the MessageBus when one is
        injected, falling back to direct ``inbox.json`` reads for backward
        compatibility with legacy callers.
        """
        if self._message_bus is not None:
            try:
                return self._message_bus.get_all_tasks_raw()
            except Exception as exc:
                logger.warning("MessageBus read failed, falling back to file: %s", exc)
        return self._load_json(".opencode/inbox.json")

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
