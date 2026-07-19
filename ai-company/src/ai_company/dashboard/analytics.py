"""KPI analytics — history tracking, trend analysis, alert rules, and summary rollups.

This module provides the analytics layer on top of KPI snapshots collected
by the per-department collectors. It supports:

- **History tracking**: Store KPI snapshots over time and retrieve history
  for any department or specific KPI.
- **Trend analysis**: Compare current vs previous period values with
  direction, magnitude, and percentage change.
- **Alert rules**: Threshold-based rules that evaluate against the latest
  snapshot and fire alerts when conditions are violated.
- **Summary statistics**: Daily, weekly, and monthly rollups with min, max,
  mean, and count aggregates.
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class KPIHistoryEntry:
    """A single stored snapshot entry for one KPI in one department."""

    timestamp: str
    department: str
    kpi_key: str
    current: float
    target: float | None
    unit: str
    status: str


@dataclass
class TrendResult:
    """Result of a before/after comparison for a single KPI."""

    kpi_key: str
    department: str
    current_value: float
    previous_value: float
    absolute_change: float
    percentage_change: float | None
    direction: Literal["up", "down", "flat"]
    unit: str


@dataclass
class AlertRule:
    """A threshold rule that triggers when a KPI crosses a boundary.

    Parameters
    ----------
    name:
        Human-readable alert name (e.g. "High failure rate").
    department:
        Department this rule applies to. Use ``"*"`` for all departments.
    kpi_key:
        Which KPI to watch (e.g. ``"failure_rate"``).
    operator:
        Comparison operator: ``"gt"``, ``"lt"``, ``"gte"``, ``"lte"``, ``"eq"``.
    threshold:
        The numeric threshold value.
    severity:
        Alert severity level: ``"info"``, ``"warning"``, ``"critical"``.
    enabled:
        Whether this rule is active.
    """

    name: str
    department: str
    kpi_key: str
    operator: Literal["gt", "lt", "gte", "lte", "eq"]
    threshold: float
    severity: Literal["info", "warning", "critical"] = "warning"
    enabled: bool = True


@dataclass
class Alert:
    """A concrete alert that was fired."""

    rule_name: str
    department: str
    kpi_key: str
    current_value: float
    threshold: float
    operator: str
    severity: str
    fired_at: str
    message: str


@dataclass
class SummaryStatistics:
    """Rollup statistics for a KPI over a time window."""

    department: str
    kpi_key: str
    period: Literal["daily", "weekly", "monthly"]
    period_start: str
    period_end: str
    min_value: float
    max_value: float
    mean_value: float
    count: int
    unit: str


# ---------------------------------------------------------------------------
# The operator dispatch table
# ---------------------------------------------------------------------------

_OPERATORS: dict[str, Callable[[float, float], bool]] = {
    "gt": lambda v, t: v > t,
    "lt": lambda v, t: v < t,
    "gte": lambda v, t: v >= t,
    "lte": lambda v, t: v <= t,
    "eq": lambda v, t: v == t,
}


# ---------------------------------------------------------------------------
# KPI History Store
# ---------------------------------------------------------------------------


class KPIHistoryStore:
    """Stores and retrieves KPI snapshots over time.

    Snapshots are persisted as newline-delimited JSON (NDJSON) in a
    configurable directory, one file per department.

    Parameters
    ----------
    storage_dir:
        Directory under which department history files are stored.
        Defaults to ``dashboard/kpi_history`` relative to project root.
    """

    def __init__(self, storage_dir: Path | None = None) -> None:
        self._storage_dir = storage_dir or Path("dashboard/kpi_history")
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, list[KPIHistoryEntry]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def store_snapshot(self, snapshot: dict[str, Any]) -> int:
        """Persist all KPI values from a full snapshot dict.

        The snapshot should be in the format returned by
        ``collect_all_kpis()`` — a dict with ``"collected_at"`` and
        ``"departments"`` keys.

        Returns the number of KPI entries stored.
        """
        collected_at = snapshot.get("collected_at", datetime.now(timezone.utc).isoformat())
        departments: dict[str, Any] = snapshot.get("departments", {})
        stored_count = 0

        for dept_id, dept_data in departments.items():
            kpis: dict[str, Any] = dept_data.get("kpis", {})
            entries: list[KPIHistoryEntry] = []

            for kpi_key, kpi_value in kpis.items():
                entry = KPIHistoryEntry(
                    timestamp=collected_at,
                    department=dept_id,
                    kpi_key=kpi_key,
                    current=float(kpi_value.get("current", 0)),
                    target=(
                        float(kpi_value["target"])
                        if kpi_value.get("target") is not None
                        else None
                    ),
                    unit=kpi_value.get("unit", ""),
                    status=kpi_value.get("status", "info"),
                )
                entries.append(entry)

            self._append_entries(dept_id, entries)
            stored_count += len(entries)

            # Invalidate cache for this department
            self._cache.pop(dept_id, None)

        return stored_count

    def get_history(
        self,
        department: str,
        kpi_key: str | None = None,
        *,
        since: str | None = None,
        limit: int = 100,
    ) -> list[KPIHistoryEntry]:
        """Retrieve history for a department, optionally filtered by KPI.

        Parameters
        ----------
        department:
            Department id (e.g. ``"engineering"``).
        kpi_key:
            If provided, only entries for this specific KPI are returned.
        since:
            ISO timestamp filter — only entries at or after this time.
        limit:
            Maximum number of entries to return (newest first).

        Returns
        -------
        list[KPIHistoryEntry]
            Chronological entries (oldest first by default).
        """
        entries = self._load_entries(department)

        if kpi_key is not None:
            entries = [e for e in entries if e.kpi_key == kpi_key]

        if since is not None:
            entries = [e for e in entries if e.timestamp >= since]

        # Sort by timestamp ascending (oldest first) for trend purposes
        entries.sort(key=lambda e: e.timestamp)

        # Apply limit from the end (most recent)
        if limit > 0 and len(entries) > limit:
            entries = entries[-limit:]

        return entries

    def get_latest(
        self,
        department: str,
        kpi_key: str | None = None,
    ) -> list[KPIHistoryEntry]:
        """Return the most recent snapshot for a department."""
        entries = self._load_entries(department)
        if not entries:
            return []

        # Find the latest timestamp
        entries.sort(key=lambda e: e.timestamp)
        latest_ts = entries[-1].timestamp
        result = [e for e in entries if e.timestamp == latest_ts]

        if kpi_key is not None:
            result = [e for e in result if e.kpi_key == kpi_key]

        return result

    def list_departments(self) -> list[str]:
        """Return department ids that have stored history."""
        return [
            p.stem.replace("_history", "")
            for p in self._storage_dir.glob("*_history.ndjson")
        ]

    def count_entries(self, department: str) -> int:
        """Return the total number of stored entries for a department."""
        return len(self._load_entries(department))

    def clear(self, department: str | None = None) -> int:
        """Remove all entries for an optional department, or everything.

        Returns the number of entries removed.
        """
        if department is not None:
            path = self._department_path(department)
            count = self.count_entries(department)
            if path.exists():
                path.unlink()
            self._cache.pop(department, None)
            return count

        total = 0
        for dept in self.list_departments():
            total += self.clear(dept)
        return total

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _department_path(self, department: str) -> Path:
        return self._storage_dir / f"{department}_history.ndjson"

    def _append_entries(self, department: str, entries: list[KPIHistoryEntry]) -> None:
        path = self._department_path(department)
        with open(path, "a", encoding="utf-8") as fh:
            for entry in entries:
                fh.write(json.dumps(entry.__dict__) + "\n")

    def _load_entries(self, department: str) -> list[KPIHistoryEntry]:
        if department in self._cache:
            return self._cache[department]

        path = self._department_path(department)
        if not path.exists():
            return []

        entries: list[KPIHistoryEntry] = []
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    entries.append(KPIHistoryEntry(**data))
                except (json.JSONDecodeError, TypeError) as exc:
                    logger.warning("Skipping malformed history entry: %s", exc)

        self._cache[department] = entries
        return entries


# ---------------------------------------------------------------------------
# Trend Analysis
# ---------------------------------------------------------------------------


def compute_trends(
    history_store: KPIHistoryStore,
    department: str,
    *,
    kpi_keys: list[str] | None = None,
    previous_period_minutes: int = 60,
) -> list[TrendResult]:
    """Compare current vs previous period for one or all KPIs.

    Parameters
    ----------
    history_store:
        A :class:`KPIHistoryStore` instance with stored snapshots.
    department:
        Department id to analyze.
    kpi_keys:
        Optional list of specific KPIs to compare. If ``None``, all KPIs
        in the department are analyzed.
    previous_period_minutes:
        How far back to look for the "previous" period value.

    Returns
    -------
    list[TrendResult]
        One result per KPI with before/after comparison.
    """
    since = (
        datetime.now(timezone.utc) - timedelta(minutes=previous_period_minutes)
    ).isoformat()

    # Get the *two most recent snapshots* (current and previous)
    all_entries = history_store.get_history(department, limit=0)
    if not all_entries:
        return []

    # Group by timestamp
    by_ts: dict[str, dict[str, KPIHistoryEntry]] = {}
    for e in all_entries:
        by_ts.setdefault(e.timestamp, {})[e.kpi_key] = e

    timestamps = sorted(by_ts.keys())
    if len(timestamps) < 2:
        # Need at least two snapshots
        return []

    latest_ts = timestamps[-1]
    current_snapshot = by_ts[latest_ts]

    # Find previous snapshot — prefer one within the lookback window
    previous_snapshot: dict[str, KPIHistoryEntry] | None = None
    for ts in reversed(timestamps[:-1]):
        if ts >= since:
            previous_snapshot = by_ts[ts]
            break

    if previous_snapshot is None:
        # Fallback to the oldest available snapshot
        previous_snapshot = by_ts[timestamps[0]]

    # Determine which KPIs to analyze
    if kpi_keys is not None:
        keys = [k for k in kpi_keys if k in current_snapshot]
    else:
        keys = list(current_snapshot.keys())

    results: list[TrendResult] = []
    for kpi_key in keys:
        current_entry = current_snapshot[kpi_key]
        prev_entry = previous_snapshot.get(kpi_key)

        current_val = current_entry.current
        prev_val = prev_entry.current if prev_entry else 0.0

        abs_change = current_val - prev_val

        if prev_val != 0:
            pct_change = round((abs_change / prev_val) * 100, 2)
        else:
            pct_change = None

        if abs_change > 0:
            direction: Literal["up", "down", "flat"] = "up"
        elif abs_change < 0:
            direction = "down"
        else:
            direction = "flat"

        results.append(TrendResult(
            kpi_key=kpi_key,
            department=department,
            current_value=current_val,
            previous_value=prev_val,
            absolute_change=round(abs_change, 4),
            percentage_change=pct_change,
            direction=direction,
            unit=current_entry.unit,
        ))

    return results


# ---------------------------------------------------------------------------
# Alert Rules Engine
# ---------------------------------------------------------------------------


class AlertEngine:
    """Evaluates alert rules against live KPI snapshots.

    Parameters
    ----------
    rules:
        Initial set of alert rules. Can be added to later via
        :meth:`add_rule` or loaded from a JSON file.
    """

    def __init__(self, rules: list[AlertRule] | None = None) -> None:
        self._rules: list[AlertRule] = rules or []

    # ------------------------------------------------------------------
    # Rule management
    # ------------------------------------------------------------------

    def add_rule(self, rule: AlertRule) -> None:
        """Register a new alert rule."""
        self._rules.append(rule)

    def add_rules(self, rules: list[AlertRule]) -> None:
        """Register multiple alert rules."""
        self._rules.extend(rules)

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name. Returns ``True`` if removed."""
        for i, rule in enumerate(self._rules):
            if rule.name == name:
                self._rules.pop(i)
                return True
        return False

    def clear_rules(self) -> None:
        """Remove all registered rules."""
        self._rules.clear()

    def list_rules(self) -> list[AlertRule]:
        """Return a copy of the current rule set."""
        return list(self._rules)

    def load_rules_from_file(self, path: Path) -> int:
        """Load rules from a JSON file.

        Expected JSON structure::

            [
                {
                    "name": "...",
                    "department": "...",
                    "kpi_key": "...",
                    "operator": "gt|lt|gte|lte|eq",
                    "threshold": 0.0,
                    "severity": "info|warning|critical",
                    "enabled": true
                }
            ]

        Returns the number of rules loaded.
        """
        if not path.exists():
            logger.warning("Alert rules file not found: %s", path)
            return 0

        with open(path, "r", encoding="utf-8") as fh:
            raw_rules = json.load(fh)

        count = 0
        for raw in raw_rules:
            self._rules.append(AlertRule(
                name=raw["name"],
                department=raw.get("department", "*"),
                kpi_key=raw["kpi_key"],
                operator=raw["operator"],
                threshold=float(raw["threshold"]),
                severity=raw.get("severity", "warning"),
                enabled=raw.get("enabled", True),
            ))
            count += 1

        return count

    def save_rules_to_file(self, path: Path) -> None:
        """Persist the current rule set to a JSON file."""
        data = []
        for rule in self._rules:
            data.append({
                "name": rule.name,
                "department": rule.department,
                "kpi_key": rule.kpi_key,
                "operator": rule.operator,
                "threshold": rule.threshold,
                "severity": rule.severity,
                "enabled": rule.enabled,
            })

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def evaluate(
        self,
        snapshot: dict[str, Any],
    ) -> list[Alert]:
        """Evaluate all enabled rules against a KPI snapshot.

        Parameters
        ----------
        snapshot:
            A snapshot dict from ``collect_all_kpis()``.

        Returns
        -------
        list[Alert]
            Fired alerts. Empty list means everything is within thresholds.
        """
        departments: dict[str, Any] = snapshot.get("departments", {})
        fired: list[Alert] = []
        now = datetime.now(timezone.utc).isoformat()

        for rule in self._rules:
            if not rule.enabled:
                continue

            # Determine which departments this rule applies to
            if rule.department == "*":
                target_depts: list[str] = list(departments.keys())
            else:
                target_depts = [rule.department]

            for dept_id in target_depts:
                dept_data = departments.get(dept_id)
                if not dept_data:
                    continue

                kpis: dict[str, Any] = dept_data.get("kpis", {})
                kpi_value = kpis.get(rule.kpi_key)
                if kpi_value is None:
                    continue

                current_val = float(kpi_value.get("current", 0))
                operator_fn = _OPERATORS.get(rule.operator)
                if operator_fn is None:
                    logger.warning("Unknown operator '%s' in rule '%s'", rule.operator, rule.name)
                    continue

                if operator_fn(current_val, rule.threshold):
                    fired.append(Alert(
                        rule_name=rule.name,
                        department=dept_id,
                        kpi_key=rule.kpi_key,
                        current_value=current_val,
                        threshold=rule.threshold,
                        operator=rule.operator,
                        severity=rule.severity,
                        fired_at=now,
                        message=(
                            f"[{rule.severity.upper()}] {rule.name}: "
                            f"{dept_id}.{rule.kpi_key} = {current_val} "
                            f"({rule.operator} {rule.threshold})"
                        ),
                    ))

        return fired


# ---------------------------------------------------------------------------
# Summary Statistics (rollups)
# ---------------------------------------------------------------------------


def compute_summary(
    history_store: KPIHistoryStore,
    department: str,
    period: Literal["daily", "weekly", "monthly"] = "daily",
    *,
    kpi_keys: list[str] | None = None,
) -> list[SummaryStatistics]:
    """Compute rollup statistics for a department's KPI history.

    Parameters
    ----------
    history_store:
        A :class:`KPIHistoryStore` with stored snapshots.
    department:
        Department id.
    period:
        Aggregation window — ``"daily"``, ``"weekly"``, or ``"monthly"``.
    kpi_keys:
        Subset of KPIs to roll up. If ``None``, all KPIs are included.

    Returns
    -------
    list[SummaryStatistics]
        One summary per KPI for the most recent complete period.
    """
    all_entries = history_store.get_history(department, limit=0)
    if not all_entries:
        return []

    if kpi_keys is not None:
        all_entries = [e for e in all_entries if e.kpi_key in kpi_keys]

    now = datetime.now(timezone.utc)

    # Determine the start of the current period
    if period == "daily":
        period_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        period_start = now - timedelta(days=now.weekday())
        period_start = period_start.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "monthly":
        period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        raise ValueError(f"Unknown period: {period}")

    period_end = now

    # Filter entries within the period
    period_entries = [
        e for e in all_entries
        if e.timestamp >= period_start.isoformat()
        and e.timestamp <= period_end.isoformat()
    ]

    if not period_entries:
        return []

    # Group by KPI key
    by_kpi: dict[str, list[float]] = defaultdict(list)
    units: dict[str, str] = {}
    for entry in period_entries:
        by_kpi[entry.kpi_key].append(entry.current)
        units[entry.kpi_key] = entry.unit

    results: list[SummaryStatistics] = []
    for kpi_key, values in by_kpi.items():
        if not values:
            continue
        results.append(SummaryStatistics(
            department=department,
            kpi_key=kpi_key,
            period=period,
            period_start=period_start.isoformat(),
            period_end=period_end.isoformat(),
            min_value=round(min(values), 4),
            max_value=round(max(values), 4),
            mean_value=round(sum(values) / len(values), 4),
            count=len(values),
            unit=units.get(kpi_key, ""),
        ))

    return results


__all__ = [
    "Alert",
    "AlertEngine",
    "AlertRule",
    "KPIHistoryEntry",
    "KPIHistoryStore",
    "SummaryStatistics",
    "TrendResult",
    "compute_summary",
    "compute_trends",
]
