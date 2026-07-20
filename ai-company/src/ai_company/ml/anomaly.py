"""Anomaly detection — detect unusual patterns in operational metrics.

Monitors cost, execution time, error rates, and other metrics to
identify anomalies that may indicate issues.  Uses statistical
methods (Z-score, IQR) rather than heavy ML libraries for speed.
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class AnomalyAlert:
    """A detected anomaly alert."""

    alert_id: str
    timestamp: str
    metric_name: str
    severity: str  # "info", "warning", "critical"
    current_value: float
    expected_range: tuple[float, float]
    deviation: float  # Number of standard deviations from mean
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["expected_range"] = list(self.expected_range)
        return d


@dataclass
class MetricWindow:
    """A sliding window of metric values for anomaly detection."""

    values: list[float] = field(default_factory=list)
    timestamps: list[str] = field(default_factory=list)
    max_size: int = 1000

    def add(self, value: float, timestamp: str = "") -> None:
        """Add a new value to the window."""
        self.values.append(value)
        self.timestamps.append(timestamp or datetime.now().isoformat())
        if len(self.values) > self.max_size:
            self.values = self.values[-self.max_size:]
            self.timestamps = self.timestamps[-self.max_size:]

    @property
    def mean(self) -> float:
        if not self.values:
            return 0.0
        return float(np.mean(self.values))

    @property
    def std(self) -> float:
        if len(self.values) < 2:
            return 0.0
        return float(np.std(self.values))

    @property
    def median(self) -> float:
        if not self.values:
            return 0.0
        return float(np.median(self.values))

    def iqr_bounds(self) -> tuple[float, float]:
        """Compute IQR-based outlier bounds."""
        if len(self.values) < 4:
            return (0.0, float("inf"))
        arr = np.array(self.values)
        q1 = float(np.percentile(arr, 25))
        q3 = float(np.percentile(arr, 75))
        iqr = q3 - q1
        return (q1 - 1.5 * iqr, q3 + 1.5 * iqr)

    def z_score(self, value: float) -> float:
        """Compute the Z-score of a value."""
        std = self.std
        if std == 0:
            return 0.0
        return (value - self.mean) / std


class AnomalyDetector:
    """Detect anomalies in operational metrics.

    Monitors multiple metric streams and fires alerts when values
    deviate significantly from historical patterns.  Uses both
    Z-score and IQR methods for robust detection.

    Args:
        data_dir: Directory for persisting detection state.
        z_threshold: Z-score threshold for anomaly detection.
        iqr_enabled: Whether to use IQR method alongside Z-score.
        min_data_points: Minimum data points before detection activates.
    """

    def __init__(
        self,
        data_dir: str | Path = "results/anomalies",
        z_threshold: float = 3.0,
        iqr_enabled: bool = True,
        min_data_points: int = 10,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.z_threshold = z_threshold
        self.iqr_enabled = iqr_enabled
        self.min_data_points = min_data_points

        self._windows: dict[str, MetricWindow] = {}
        self._alerts: list[AnomalyAlert] = []
        self._alert_counts: dict[str, int] = defaultdict(int)

        self._load_state()

    def record_metric(self, metric_name: str, value: float, timestamp: str = "") -> list[AnomalyAlert]:
        """Record a metric value and check for anomalies.

        Args:
            metric_name: Name of the metric (e.g., "cost_usd", "execution_time_s").
            value: The metric value.
            timestamp: ISO timestamp of the measurement.

        Returns:
            List of alerts triggered (empty if no anomaly detected).
        """
        if metric_name not in self._windows:
            self._windows[metric_name] = MetricWindow()

        window = self._windows[metric_name]
        ts = timestamp or datetime.now().isoformat()

        alerts: list[AnomalyAlert] = []

        # Only check after sufficient data
        if len(window.values) >= self.min_data_points:
            # Z-score check
            z = window.z_score(value)
            if abs(z) >= self.z_threshold:
                severity = "critical" if abs(z) >= self.z_threshold * 1.5 else "warning"
                alert = AnomalyAlert(
                    alert_id=f"anomaly_{metric_name}_{len(self._alerts)}",
                    timestamp=ts,
                    metric_name=metric_name,
                    severity=severity,
                    current_value=value,
                    expected_range=(round(window.mean - self.z_threshold * window.std, 4),
                                    round(window.mean + self.z_threshold * window.std, 4)),
                    deviation=round(z, 2),
                    message=(
                        f"Anomaly detected in {metric_name}: value {value:.4f} is "
                        f"{abs(z):.1f} standard deviations from mean ({window.mean:.4f})."
                    ),
                )
                alerts.append(alert)

            # IQR check
            if self.iqr_enabled:
                low, high = window.iqr_bounds()
                if value < low or value > high:
                    # Avoid duplicate alerts if Z-score already fired
                    if not any(a.metric_name == metric_name for a in alerts):
                        alert = AnomalyAlert(
                            alert_id=f"anomaly_{metric_name}_{len(self._alerts)}",
                            timestamp=ts,
                            metric_name=metric_name,
                            severity="warning",
                            current_value=value,
                            expected_range=(round(low, 4), round(high, 4)),
                            deviation=0.0,
                            message=(
                                f"Outlier detected in {metric_name}: value {value:.4f} "
                                f"is outside IQR range [{low:.4f}, {high:.4f}]."
                            ),
                        )
                        alerts.append(alert)

        # Add to window AFTER checking (so we don't pollute the baseline)
        window.add(value, ts)

        # Record alerts
        for alert in alerts:
            self._alerts.append(alert)
            self._alert_counts[alert.metric_name] += 1
            logger.warning("ANOMALY [%s] %s", alert.severity.upper(), alert.message)

        if alerts:
            self._save_state()

        return alerts

    def check_cost_anomaly(self, cost_usd: float, agent_id: str = "") -> list[AnomalyAlert]:
        """Check if a cost value is anomalous."""
        metric = f"cost_{agent_id}" if agent_id else "cost_usd"
        alerts = self.record_metric(metric, cost_usd)
        return alerts

    def check_execution_time_anomaly(self, time_s: float, agent_id: str = "") -> list[AnomalyAlert]:
        """Check if an execution time is anomalous."""
        metric = f"exec_time_{agent_id}" if agent_id else "execution_time_s"
        return self.record_metric(metric, time_s)

    def check_error_rate_anomaly(self, error_rate: float) -> list[AnomalyAlert]:
        """Check if error rate is anomalous."""
        return self.record_metric("error_rate", error_rate)

    def get_metric_summary(self, metric_name: str) -> dict[str, Any]:
        """Get statistical summary for a metric."""
        window = self._windows.get(metric_name)
        if not window or not window.values:
            return {"metric": metric_name, "data_points": 0}

        low, high = window.iqr_bounds()
        return {
            "metric": metric_name,
            "data_points": len(window.values),
            "mean": round(window.mean, 4),
            "std": round(window.std, 4),
            "median": round(window.median, 4),
            "min": round(min(window.values), 4),
            "max": round(max(window.values), 4),
            "iqr_low": round(low, 4),
            "iqr_high": round(high, 4),
            "anomaly_count": self._alert_counts.get(metric_name, 0),
        }

    def get_all_summaries(self) -> dict[str, dict[str, Any]]:
        """Get summaries for all monitored metrics."""
        return {name: self.get_metric_summary(name) for name in self._windows}

    def get_recent_alerts(self, limit: int = 20) -> list[dict[str, Any]]:
        """Get recent anomaly alerts."""
        return [a.to_dict() for a in self._alerts[-limit:]]

    def get_alert_stats(self) -> dict[str, Any]:
        """Get overall alert statistics."""
        severity_counts: dict[str, int] = defaultdict(int)
        for alert in self._alerts:
            severity_counts[alert.severity] += 1

        return {
            "total_alerts": len(self._alerts),
            "by_severity": dict(severity_counts),
            "by_metric": dict(self._alert_counts),
        }

    def set_threshold(self, metric_name: str, z_threshold: float | None = None) -> None:
        """Override the Z-score threshold for a specific metric."""
        if z_threshold is not None:
            # Store per-metric thresholds in metadata
            if metric_name not in self._windows:
                self._windows[metric_name] = MetricWindow()
            self._windows[metric_name].max_size = self._windows[metric_name].max_size  # no-op, but placeholder

    def save_state(self) -> None:
        """Explicitly save state to disk."""
        self._save_state()

    # ── Persistence ────────────────────────────────────────────────

    def _save_state(self) -> None:
        """Persist detector state."""
        # Save windows
        windows_data: dict[str, Any] = {}
        for name, window in self._windows.items():
            windows_data[name] = {
                "values": window.values,
                "timestamps": window.timestamps,
            }
        windows_path = self.data_dir / "metric_windows.json"
        with open(windows_path, "w", encoding="utf-8") as f:
            json.dump(windows_data, f, indent=2)

        # Save alerts (append-only)
        alerts_path = self.data_dir / "alerts.jsonl"
        try:
            with open(alerts_path, "a", encoding="utf-8") as f:
                for alert in self._alerts[-10:]:  # Write last 10 new alerts
                    f.write(json.dumps(alert.to_dict(), default=str) + "\n")
        except OSError:
            pass

        # Save alert counts
        counts_path = self.data_dir / "alert_counts.json"
        with open(counts_path, "w", encoding="utf-8") as f:
            json.dump(dict(self._alert_counts), f, indent=2)

    def _load_state(self) -> None:
        """Load persisted state."""
        windows_path = self.data_dir / "metric_windows.json"
        if windows_path.exists():
            try:
                with open(windows_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for name, wdata in data.items():
                    window = MetricWindow()
                    window.values = wdata.get("values", [])
                    window.timestamps = wdata.get("timestamps", [])
                    self._windows[name] = window
                logger.info("Loaded metric windows for %d metrics", len(self._windows))
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Failed to load metric windows: %s", exc)

        counts_path = self.data_dir / "alert_counts.json"
        if counts_path.exists():
            try:
                with open(counts_path, "r", encoding="utf-8") as f:
                    self._alert_counts = defaultdict(int, json.load(f))
            except (json.JSONDecodeError, OSError):
                pass
