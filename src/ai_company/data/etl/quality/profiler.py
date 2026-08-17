"""Data Profiler.

Analyzes data distributions, completeness, and patterns for quality monitoring.
"""

from __future__ import annotations

import logging
from collections import Counter
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


def profile_records(records: list[dict[str, Any]], sample_size: int = 10000) -> dict[str, Any]:
    """Generate a statistical profile of records.

    Args:
        records: Records to profile
        sample_size: Maximum records to analyze (for performance)

    Returns:
        Profile dict with column stats, completeness, distributions
    """
    if not records:
        return {"record_count": 0, "columns": {}}

    # Sample if needed
    import random

    original_count = len(records)
    if len(records) > sample_size:
        records = random.sample(records, sample_size)

    # Collect column stats
    columns: dict[str, dict] = {}
    for record in records:
        for key, value in record.items():
            if key not in columns:
                columns[key] = {
                    "count": 0,
                    "null_count": 0,
                    "type_counts": Counter(),
                    "sample_values": [],
                    "min": None,
                    "max": None,
                    "unique_estimate": set(),
                }
            col = columns[key]
            col["count"] += 1
            if value is None or value == "":
                col["null_count"] += 1
            else:
                col["type_counts"][type(value).__name__] += 1
                if len(col["sample_values"]) < 5:
                    col["sample_values"].append(value)
                # Track unique values (up to 1000)
                if len(col["unique_estimate"]) < 1000:
                    col["unique_estimate"].add(str(value)[:100])
                # Min/max for numeric
                if isinstance(value, (int, float)):
                    if col["min"] is None or value < col["min"]:
                        col["min"] = value
                    if col["max"] is None or value > col["max"]:
                        col["max"] = value

    # Finalize profile
    profile: dict[str, Any] = {
        "record_count": original_count,
        "sampled": len(records) < original_count,
        "profiled_at": datetime.now(timezone.utc).isoformat(),
        "columns": {},
    }

    for key, col in columns.items():
        profile["columns"][key] = {
            "count": col["count"],
            "null_count": col["null_count"],
            "null_pct": round(col["null_count"] / col["count"] * 100, 2) if col["count"] > 0 else 0,
            "types": dict(col["type_counts"]),
            "sample_values": col["sample_values"],
            "min": col["min"],
            "max": col["max"],
            "unique_count_estimate": len(col["unique_estimate"]),
        }

    return profile


def profile_kpi_values(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Profile KPI time-series records."""
    profile = profile_records(records)

    # Add KPI-specific analysis
    if records:
        departments = Counter(r.get("department") for r in records)
        kpi_keys = Counter(r.get("kpi_key") for r in records)
        statuses = Counter(r.get("status") for r in records)

        profile["kpi_summary"] = {
            "departments": dict(departments),
            "kpi_keys": dict(kpi_keys),
            "statuses": dict(statuses),
            "total_departments": len(departments),
            "total_kpi_keys": len(kpi_keys),
        }

    return profile


def profile_cost_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Profile cost records with spend analysis."""
    profile = profile_records(records)

    if records:
        total_cost = sum(r.get("cost_usd", 0) for r in records)
        by_model: Counter[str] = Counter()
        by_provider: Counter[str] = Counter()
        by_agent: Counter[str] = Counter()

        for r in records:
            by_model[r.get("model", "unknown")] += r.get("cost_usd", 0)
            by_provider[r.get("provider", "unknown")] += r.get("cost_usd", 0)
            by_agent[r.get("agent_name", "unknown")] += r.get("cost_usd", 0)

        profile["cost_summary"] = {
            "total_cost_usd": round(total_cost, 6),
            "record_count": len(records),
            "avg_cost_per_call": round(total_cost / len(records), 6) if records else 0,
            "by_model": {m: round(c, 6) for m, c in by_model.most_common(10)},
            "by_provider": {p: round(c, 6) for p, c in by_provider.most_common()},
            "by_agent": {a: round(c, 6) for a, c in by_agent.most_common(10)},
        }

    return profile


def detect_drift(
    baseline_profile: dict[str, Any],
    current_profile: dict[str, Any],
    threshold_pct: float = 10.0,
) -> list[dict[str, Any]]:
    """Detect statistical drift between baseline and current profiles.

    Args:
        baseline_profile: Profile from reference period
        current_profile: Profile from current period
        threshold_pct: Percentage change threshold for alerting

    Returns:
        List of drift alerts
    """
    alerts: list[dict[str, Any]] = []

    baseline_cols = baseline_profile.get("columns", {})
    current_cols = current_profile.get("columns", {})

    all_columns = set(baseline_cols.keys()) | set(current_cols.keys())

    for col in all_columns:
        base = baseline_cols.get(col, {})
        curr = current_cols.get(col, {})

        # Null rate drift
        base_null = base.get("null_pct", 0)
        curr_null = curr.get("null_pct", 0)
        if base_null > 0:
            null_change = abs(curr_null - base_null) / base_null * 100
        else:
            null_change = 100 if curr_null > 0 else 0

        if null_change > threshold_pct:
            alerts.append(
                {
                    "type": "null_rate_drift",
                    "column": col,
                    "baseline_null_pct": base_null,
                    "current_null_pct": curr_null,
                    "change_pct": round(null_change, 2),
                    "severity": "high" if null_change > 50 else "medium",
                }
            )

        # Type distribution drift
        base_types = base.get("types", {})
        curr_types = curr.get("types", {})
        if base_types != curr_types:
            alerts.append(
                {
                    "type": "type_distribution_drift",
                    "column": col,
                    "baseline_types": base_types,
                    "current_types": curr_types,
                    "severity": "medium",
                }
            )

        # Volume drift
        base_count = base.get("count", 0)
        curr_count = curr.get("count", 0)
        if base_count > 0:
            volume_change = abs(curr_count - base_count) / base_count * 100
            if volume_change > threshold_pct:
                alerts.append(
                    {
                        "type": "volume_drift",
                        "column": col,
                        "baseline_count": base_count,
                        "current_count": curr_count,
                        "change_pct": round(volume_change, 2),
                        "severity": "medium",
                    }
                )

    return alerts


__all__ = [
    "profile_records",
    "profile_kpi_values",
    "profile_cost_records",
    "detect_drift",
]
