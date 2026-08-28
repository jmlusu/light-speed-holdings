"""Org Health — composite organisational health scoring.

Loads band/weight configuration from ``config/org_health.yaml`` and computes
a weighted composite score from live operational data.  Component scores are
computed from the same data sources used by the dashboard KPI collectors
(tasks, KPIs, agents, costs, builds).
"""

from __future__ import annotations

import logging
import math
import threading
import time
from concurrent.futures import Future
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

from ai_company.data.database import Database
from ai_company.paths import get_project_root
from ai_company.reliability.breaker import ComponentBreaker
from ai_company.reliability.config import get_hardening_value, load_hardening_config
from ai_company.reliability.timeout import Bulkhead

logger = logging.getLogger(__name__)

_DEFAULT_CONFIG = "config/org_health.yaml"


# ── Data classes ────────────────────────────────────────────────────


@dataclass
class ComponentScore:
    """A single component within the composite org-health score."""

    name: str
    weight: float
    value: float | None  # 0-100, or None when no data is available
    sub_score: float | None  # same as value; kept for API shape compatibility

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": round(self.value, 2) if self.value is not None else None,
            "weight": self.weight,
            "sub_score": round(self.sub_score, 2) if self.sub_score is not None else None,
        }


@dataclass
class OrgHealthResult:
    """The full result of an org-health computation."""

    score: int  # 0-100, rounded
    band: str  # "green" | "amber" | "red"
    components: list[ComponentScore] = field(default_factory=list)
    collected_at: str = ""

    def to_dict(
        self,
        *,
        include_components: bool = True,
        trend: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        result: dict[str, Any] = {
            "score": self.score,
            "band": self.band,
            "collected_at": self.collected_at,
        }
        if include_components:
            result["components"] = [c.to_dict() for c in self.components]
        result["missing_components"] = [c.name for c in self.components if c.value is None]
        result["trend"] = trend or []
        return result


@dataclass
class Anomaly:
    """A detected anomaly in an org-health component score."""

    timestamp: str
    component: str
    previous_value: float
    current_value: float
    change_pct: float
    severity: str  # "info" | "warning" | "critical"
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "component": self.component,
            "previous_value": round(self.previous_value, 2),
            "current_value": round(self.current_value, 2),
            "change_pct": round(self.change_pct, 1),
            "severity": self.severity,
            "message": self.message,
        }


# ── Calculator ──────────────────────────────────────────────────────


class OrgHealthCalculator:
    """Computes composite org-health score from live operational data.

    Configuration is loaded once at init time from ``config/org_health.yaml``.
    Call :meth:`compute` with an optional database to get a fresh score.

    Since wayfinder ticket #170 the scoring pass is hardened: each component
    scorer runs in a bulkhead worker with a hard timeout and a per-component
    circuit breaker. A slow/failing scorer degrades fail-open to its last
    known-good value (or ``None`` on cold start) so it can never block the
    dashboard thread. Repeated :meth:`compute` calls within the dedup window
    return the last result. Thresholds come from ``company/config/hardening.yaml``.
    """

    def __init__(self, project_root: Path | None = None) -> None:
        self._root = project_root or get_project_root()
        self._config = self._load_config()
        self._bands: dict[str, dict[str, int]] = self._config.get("bands", {})
        self._component_defs: list[dict[str, Any]] = self._config.get("components", [])
        self._validate_weights()

        self._hardening = load_hardening_config(self._root)
        self._compute_lock = threading.Lock()
        self._last_compute: OrgHealthResult | None = None
        self._last_compute_at = 0.0
        self._breakers: dict[str, ComponentBreaker] = {}
        self._last_good: dict[str, float] = {}
        self._task_window_cache: tuple[list[dict[str, Any]], str] | None = None

    # ── Public API ───────────────────────────────────────────────────

    def compute(self, database: Database | None = None) -> OrgHealthResult:
        """Compute the current org-health score.

        Parameters
        ----------
        database:
            Optional SQLite database for live task/KPI data.

        Returns
        -------
        OrgHealthResult
            Composite score, band, and per-component breakdown.
            Components with no data have ``value=None`` and are excluded
            from the composite (the score reflects only available data).
        """
        call_timeout_s = float(
            get_hardening_value(self._hardening, "org_health.call_timeout_s", 3.0)
        )
        compute_timeout_s = float(
            get_hardening_value(self._hardening, "org_health.compute_timeout_s", 15.0)
        )
        dedup_s = float(get_hardening_value(self._hardening, "org_health.dedup_window_s", 5.0))
        pool_size = max(
            1,
            min(
                int(get_hardening_value(self._hardening, "org_health.worker_pool_size", 4)),
                len(self._component_defs),
            ),
        )

        with self._compute_lock:
            now = time.monotonic()
            if self._last_compute is not None and now - self._last_compute_at < dedup_s:
                return self._last_compute

            self._task_window_cache = None
            deadline = time.monotonic() + max(0.0, compute_timeout_s)
            components: list[ComponentScore] = []
            bulkhead = Bulkhead(max_workers=pool_size)
            try:
                submittable = {
                    comp_def["name"]: self._get_breaker(comp_def["name"]).is_available
                    for comp_def in self._component_defs
                }
                futures: dict[str, Future[float | None]] = {
                    name: bulkhead.submit(self._score_component, name, database)
                    for name, available in submittable.items()
                    if available
                }
                for comp_def in self._component_defs:
                    name = comp_def["name"]
                    weight = comp_def["weight"]
                    if name in futures:
                        value = self._scored_component(
                            name, futures[name], deadline, call_timeout_s
                        )
                    else:
                        # Breaker open — never queued: fail open without a call.
                        value = self._fail_open(name)
                    components.append(
                        ComponentScore(name=name, weight=weight, value=value, sub_score=value)
                    )
            finally:
                bulkhead.shutdown(wait=False)

            # Only include components with real data in the composite
            scored = [(c, c.value) for c in components if c.value is not None]
            if scored:
                total_weight = sum(c.weight for c, _ in scored)
                composite = sum(c.weight * v for c, v in scored) / total_weight
            else:
                composite = 0.0
            score = max(0, min(100, round(composite)))
            band = self._score_to_band(score)

            result = OrgHealthResult(
                score=score,
                band=band,
                components=components,
                collected_at=datetime.now(timezone.utc).isoformat(),
            )
            self._last_compute = result
            self._last_compute_at = time.monotonic()
            return result

    def get_bands(self) -> dict[str, dict[str, int]]:
        """Return the configured band thresholds."""
        return dict(self._bands)

    def get_component_defs(self) -> list[dict[str, Any]]:
        """Return the configured component definitions."""
        return list(self._component_defs)

    def detect_anomalies(
        self, history: list[dict[str, Any]], threshold: float = 2.0
    ) -> list[Anomaly]:
        """Detect anomalies using Z-score on component score deltas.

        Parameters
        ----------
        history:
            List of historical org-health snapshots, each containing a
            ``components`` list with ``name`` and ``value`` fields.
        threshold:
            Z-score threshold above which a value is considered anomalous.
            Default is 2.0 (roughly 95th percentile).

        Returns
        -------
        list[Anomaly]
            Detected anomalies sorted by severity (critical first).
        """
        anomalies: list[Anomaly] = []

        # Group component values by name across history entries
        by_component: dict[str, list[float]] = {}
        for entry in history:
            for comp in entry.get("components", []):
                name = comp.get("name", "")
                value = comp.get("value", 0)
                by_component.setdefault(name, []).append(value)

        # Calculate Z-scores for recent changes
        for name, values in by_component.items():
            if len(values) < 3:
                continue

            # Calculate mean and std of historical values (excluding latest)
            historical = values[:-1]
            mean = sum(historical) / len(historical)
            variance = sum((v - mean) ** 2 for v in historical) / len(historical)
            std = math.sqrt(variance)

            if std == 0:
                continue

            # Check latest value against historical distribution
            latest = values[-1]
            previous = values[-2]
            z_score = (latest - mean) / std
            change_pct = ((latest - previous) / previous * 100) if previous else 0

            if abs(z_score) > threshold:
                severity = "critical" if abs(z_score) > 3 else "warning"
                direction = "spike" if latest > previous else "drop"
                anomalies.append(
                    Anomaly(
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        component=name,
                        previous_value=previous,
                        current_value=latest,
                        change_pct=round(change_pct, 1),
                        severity=severity,
                        message=(
                            f"{name.replace('_', ' ').title()} {direction}: "
                            f"{previous:.0f}% → {latest:.0f}% ({change_pct:+.1f}%)"
                        ),
                    )
                )

        # Sort: critical first, then warning
        severity_order = {"critical": 0, "warning": 1, "info": 2}
        anomalies.sort(key=lambda a: severity_order.get(a.severity, 3))
        return anomalies

    # ── Component scoring ────────────────────────────────────────────

    def _scorers(self) -> dict[str, Callable[[Database | None], float | None]]:
        """Map configured component names to their scoring functions."""
        return {
            "task_success_rate": self._score_task_success_rate,
            "agent_utilization": self._score_agent_utilization,
            "cost_efficiency": self._score_cost_efficiency,
            "error_rate": self._score_error_rate,
        }

    def _score_component(self, name: str, database: Database | None) -> float | None:
        """Dispatch to the scorer for *name*, letting failures propagate.

        Deliberately exception-transparent: hardening (breaker + timeout +
        fail-open) is applied by :meth:`_scored_component`, so real scorer
        failures trip the per-component breaker instead of being swallowed
        as a plain ``None``.
        """
        scorer = self._scorers().get(name)
        if scorer is None:
            logger.warning("Unknown org-health component: %s — no data available", name)
            return None
        return scorer(database)

    def _scored_component(
        self,
        name: str,
        future: Future[float | None],
        deadline: float,
        call_timeout_s: float,
    ) -> float | None:
        """Apply breaker + timeout hardening to an in-flight scorer future.

        Returns:
            The scorer's value on success, or the last known-good value /
            ``None`` (fail-open) on timeout, failure, or an open circuit.
        """
        breaker = self._get_breaker(name)
        if not breaker.is_available:
            logger.warning(
                "Org health breaker for %s is open — using cached/None (fail-open)",
                name,
            )
            return self._fail_open(name)

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            breaker.record_failure()
            logger.warning(
                "Org health compute deadline exceeded for %s — using cached/None (fail-open)",
                name,
            )
            return self._fail_open(name)

        try:
            value = future.result(timeout=min(call_timeout_s, remaining))
        except TimeoutError:
            breaker.record_failure()
            logger.warning(
                "Org health component %s timed out after %.1fs — using cached/None (fail-open)",
                name,
                min(call_timeout_s, remaining),
            )
            return self._fail_open(name)
        except Exception:  # noqa: BLE001 - breaker records and degrades
            breaker.record_failure()
            logger.exception("Org health component %s raised — using cached/None (fail-open)", name)
            return self._fail_open(name)

        breaker.record_success()
        if value is not None:
            self._last_good[name] = value
        return value

    def _get_breaker(self, name: str) -> ComponentBreaker:
        """Return the per-component breaker, building it from config on first use."""
        breaker = self._breakers.get(name)
        if breaker is None:
            breaker = ComponentBreaker(
                name=name,
                failure_threshold=int(
                    get_hardening_value(
                        self._hardening,
                        "org_health.breaker.failure_threshold",
                        3,
                    )
                ),
                recovery_timeout_s=float(
                    get_hardening_value(
                        self._hardening,
                        "org_health.breaker.recovery_timeout_s",
                        60.0,
                    )
                ),
                success_threshold=int(
                    get_hardening_value(
                        self._hardening,
                        "org_health.breaker.success_threshold",
                        1,
                    )
                ),
            )
            self._breakers[name] = breaker
        return breaker

    def _fail_open(self, name: str) -> float | None:
        """Last known-good score for *name*, or ``None`` on cold start.

        Fail-open: a degraded scorer keeps serving its most recent healthy
        value so the composite reflects stale-but-true data rather than a
        fabricated number. With no history yet, ``None`` keeps the existing
        "no data this component" semantics (excluded from the composite).
        """
        cached = self._last_good.get(name)
        return cached if cached is not None else None

    def _window_tasks(self) -> tuple[list[dict[str, Any]], str]:
        """Fetch the 30-day task window once per compute.

        The three task-based scorers all read the same inbox window; sharing
        one fetch per compute avoids redundant whole-file reads and keeps the
        read count bounded when a component is slow (called under the compute
        lock, so it is thread-safe).
        """
        if self._task_window_cache is None:
            from ai_company.dashboard.data_service import _company_window_tasks

            self._task_window_cache = _company_window_tasks(self._root, days=30)
        return self._task_window_cache

    def _score_task_success_rate(self, database: Database | None) -> float | None:
        """Ratio of completed tasks to total tasks (0-100).

        Returns ``None`` when no tasks exist in the 30-day window so callers
        can distinguish "no data" from "zero success rate".
        """
        tasks, _ = self._window_tasks()
        total = len(tasks)
        if total == 0:
            return None
        completed = sum(1 for t in tasks if t.get("status") == "completed")
        return (completed / total) * 100

    def _score_agent_utilization(self, database: Database | None) -> float | None:
        """Active agents vs registered agents (0-100).

        Returns ``None`` when no agents are registered so callers can
        distinguish "no data" from "zero utilization".
        """
        from ai_company.dashboard.data_service import _count_registered_agents

        root = self._root
        total_registered = _count_registered_agents(root)
        if total_registered == 0:
            return None

        tasks, _ = self._window_tasks()
        active_agents = {
            agent
            for task in tasks
            for agent in (task.get("sender_id"), task.get("receiver_id"))
            if agent
        }
        if not active_agents:
            return 0.0
        return min(100.0, (len(active_agents) / total_registered) * 100)

    def _score_cost_efficiency(self, database: Database | None) -> float | None:
        """Budget utilization vs spend (0-100).

        Uses the cost summary from the data service.  If total budget is
        known, returns the ratio of remaining budget (inverted: lower
        spend = higher efficiency, but capped at 100).

        Returns ``None`` when no cost data or budget is available so callers
        can distinguish "no data" from "zero efficiency". Exceptions propagate
        to the hardening layer (breaker + fail-open) rather than being
        swallowed here.
        """
        from ai_company.dashboard.data_service import get_cost_summary

        summary = get_cost_summary(database=database)
        if summary is None:
            return None
        total_spent = float(summary.get("total_spent", 0) or 0)
        budget = float(summary.get("budget", 0) or 0)
        if budget <= 0:
            return None
        # Efficiency = 100 - (spent/budget * 100), clamped
        utilization = (total_spent / budget) * 100
        return max(0.0, min(100.0, 100.0 - utilization + 50.0))

    def _score_error_rate(self, database: Database | None) -> float | None:
        """Error/exception rate across agent operations (0-100, inverted).

        Lower error rate = higher score. Reads from task statuses in the
        message bus / audit trail. Returns 100 - (error_rate * 100).

        Returns ``None`` when no tasks exist in the window so callers can
        distinguish "no data" from "zero error rate". Exceptions propagate to
        the hardening layer (breaker + fail-open) rather than being swallowed
        here.
        """
        tasks, _ = self._window_tasks()
        total = len(tasks)
        if total == 0:
            return None
        error_tasks = sum(1 for t in tasks if t.get("status") in ("failed", "error", "cancelled"))
        error_rate = (error_tasks / total) * 100
        return max(0.0, 100.0 - error_rate)

    # ── Band mapping ─────────────────────────────────────────────────

    def _score_to_band(self, score: int) -> str:
        """Map a numeric score to its band label."""
        for band_name, bounds in self._bands.items():
            lo = bounds.get("min", 0)
            hi = bounds.get("max", 100)
            if lo <= score <= hi:
                return band_name
        return "red"  # Fallback

    # ── Config loading ───────────────────────────────────────────────

    def _load_config(self) -> dict[str, Any]:
        """Load and return the org-health YAML config."""
        config_path = self._root / _DEFAULT_CONFIG
        if not config_path.is_file():
            logger.warning("Org health config not found at %s, using defaults", config_path)
            return self._default_config()
        try:
            with open(config_path, encoding="utf-8") as fh:
                config = yaml.safe_load(fh) or {}
        except (yaml.YAMLError, OSError) as exc:
            logger.warning("Failed to load org health config: %s", exc)
            return self._default_config()
        if not isinstance(config, dict):
            return self._default_config()
        return config

    def _validate_weights(self) -> None:
        """Ensure component weights sum to 1.0."""
        total = sum(c.get("weight", 0) for c in self._component_defs)
        if abs(total - 1.0) > 0.01:
            logger.warning(
                "Org health component weights sum to %.3f, expected 1.0 — scores may be inaccurate",
                total,
            )

    @staticmethod
    def _default_config() -> dict[str, Any]:
        """Return a minimal default config when the YAML file is missing."""
        return {
            "bands": {
                "green": {"min": 80, "max": 100},
                "amber": {"min": 50, "max": 79},
                "red": {"min": 0, "max": 49},
            },
            "components": [
                {"name": "task_success_rate", "weight": 0.30},
                {"name": "agent_utilization", "weight": 0.25},
                {"name": "cost_efficiency", "weight": 0.25},
                {"name": "error_rate", "weight": 0.20},
            ],
        }
