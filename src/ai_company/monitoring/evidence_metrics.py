"""
Prometheus metrics for evidence store monitoring.

Provides metrics for evidence store sizes, event counts, and rotation events.
See AGENTS.md §9.3 and docs/adr/008-evidence-separation.md.
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, TypedDict

from prometheus_client import REGISTRY, Counter, Gauge, Histogram

logger = logging.getLogger(__name__)

# ── Evidence Store Metrics ──────────────────────────────────────────────

# Store size in bytes
evidence_store_size_bytes = Gauge(
    "evidence_store_size_bytes",
    "Current size of evidence store file in bytes",
    ["store"],
    registry=REGISTRY,
)

# Total events written to store
evidence_store_events_total = Counter(
    "evidence_store_events_total",
    "Total number of events written to evidence store",
    ["store", "event_type"],
    registry=REGISTRY,
)

# Rotation events
evidence_store_rotation_total = Counter(
    "evidence_store_rotation_total",
    "Total number of store rotations performed",
    ["store", "result"],
    registry=REGISTRY,
)

# Store file age (seconds since last modification)
evidence_store_age_seconds = Gauge(
    "evidence_store_age_seconds",
    "Age of evidence store file in seconds since last modification",
    ["store"],
    registry=REGISTRY,
)

# Rotation duration histogram
evidence_store_rotation_duration_seconds = Histogram(
    "evidence_store_rotation_duration_seconds",
    "Duration of store rotation in seconds",
    ["store"],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0),
    registry=REGISTRY,
)


# ── Store Definitions ───────────────────────────────────────────────────


class StoreConfig(TypedDict):
    """Shape of a single evidence-store definition."""

    path: str
    retention_days: int
    max_size_bytes: int


EVIDENCE_STORES: dict[str, StoreConfig] = {
    "escalation_events": {
        "path": "orchestrator/escalation_events.jsonl",
        "retention_days": 30,
        "max_size_bytes": 100 * 1024 * 1024,  # 100 MB
    },
    "dead_letter": {
        "path": "orchestrator/dead_letter.jsonl",
        "retention_days": 90,
        "max_size_bytes": 100 * 1024 * 1024,  # 100 MB
    },
    "audit_export": {
        "path": "reports/evidence/audit-*.jsonl",  # glob pattern
        "retention_days": 90,
        "max_size_bytes": 50 * 1024 * 1024,  # 50 MB per file
    },
}


# ── Store Inspection Helpers ─────────────────────────────────────────────


def resolve_store_files(path_spec: str) -> list[Path]:
    """Resolve a store path spec (fixed path or glob pattern) to existing files."""
    if "*" in path_spec:
        return sorted(p for p in Path().glob(path_spec) if p.is_file())
    candidate = Path(path_spec)
    return [candidate] if candidate.is_file() else []


def count_store_events(path: Path) -> int:
    """Count newline-delimited records in a JSONL store without buffering it."""
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


# ── Metrics Collection ──────────────────────────────────────────────────


def collect_evidence_store_metrics() -> dict[str, Any]:
    """
    Collect current metrics for all evidence stores.

    Returns:
        Dict mapping store names to their current metrics.
    """
    results: dict[str, Any] = {}
    now = time.time()

    for store_name, config in EVIDENCE_STORES.items():
        files = resolve_store_files(config["path"])

        total_size = sum(f.stat().st_size for f in files)
        total_events = sum(count_store_events(f) for f in files)
        latest_mtime = max((f.stat().st_mtime for f in files), default=0.0)
        age_seconds = now - latest_mtime if latest_mtime else 0.0

        # Update Prometheus metrics
        evidence_store_size_bytes.labels(store=store_name).set(total_size)
        evidence_store_events_total.labels(store=store_name, event_type="total").inc(
            0
        )  # no-op, just ensure metric exists
        evidence_store_age_seconds.labels(store=store_name).set(age_seconds)

        max_size = config["max_size_bytes"]
        results[store_name] = {
            "size_bytes": total_size,
            "event_count": total_events,
            "age_seconds": age_seconds,
            "max_size_bytes": max_size,
            "retention_days": config["retention_days"],
            "usage_pct": (total_size / max_size) * 100 if max_size > 0 else 0,
        }

    return results


def record_evidence_write(store: str, event_type: str = "default", count: int = 1) -> None:
    """Record that events were written to an evidence store."""
    evidence_store_events_total.labels(store=store, event_type=event_type).inc(count)
    # Update size metric asynchronously (approximate)
    config = EVIDENCE_STORES.get(store)
    if config is None:
        return
    path = config["path"]
    if "*" not in path:
        p = Path(path)
        if p.is_file():
            evidence_store_size_bytes.labels(store=store).set(p.stat().st_size)


def record_rotation(store: str, success: bool, duration_seconds: float) -> None:
    """Record a rotation event."""
    result = "success" if success else "failure"
    evidence_store_rotation_total.labels(store=store, result=result).inc()
    evidence_store_rotation_duration_seconds.labels(store=store).observe(duration_seconds)

    if success:
        logger.info(
            "Evidence store rotation completed: store=%s duration=%.2fs", store, duration_seconds
        )
    else:
        logger.warning(
            "Evidence store rotation failed: store=%s duration=%.2fs", store, duration_seconds
        )


def check_store_alerts() -> list[str]:
    """
    Check evidence stores for alert conditions.

    Returns:
        List of alert messages (empty if no alerts).
    """
    alerts: list[str] = []

    for store_name, config in EVIDENCE_STORES.items():
        max_size = config["max_size_bytes"]
        total_size = sum(f.stat().st_size for f in resolve_store_files(config["path"]))

        if total_size > max_size:
            alerts.append(
                f"Evidence store {store_name} exceeds max size: {total_size / 1024 / 1024:.1f}MB > {max_size / 1024 / 1024:.1f}MB"
            )
        elif total_size > max_size * 0.8:
            alerts.append(
                f"Evidence store {store_name} at {total_size / max_size * 100:.0f}% capacity ({total_size / 1024 / 1024:.1f}MB / {max_size / 1024 / 1024:.1f}MB)"
            )

    return alerts


def get_store_metrics() -> dict[str, Any]:
    """Get all store metrics for /metrics endpoint."""
    return {
        "stores": collect_evidence_store_metrics(),
        "alerts": check_store_alerts(),
    }


# Auto-update metrics on import if not in test mode
if not os.environ.get("PYTEST_CURRENT_TEST"):
    try:
        collect_evidence_store_metrics()
    except (OSError, ValueError, KeyError) as exc:
        logger.debug("Failed to collect initial evidence store metrics: %s", exc)
