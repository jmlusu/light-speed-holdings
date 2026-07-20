"""Predictive scaling — forecast task volume and recommend resource adjustments.

Analyzes historical patterns in task volume, cost, and execution times
to predict future demand and recommend model tier adjustments.
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class ScalingRecommendation:
    """A resource scaling recommendation."""

    recommendation_type: str  # "tier_adjustment", "cost_forecast", "capacity预警"
    current_state: dict[str, Any]
    predicted_state: dict[str, Any]
    action: str
    confidence: float  # 0.0 to 1.0
    reasoning: str
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DailyMetrics:
    """Aggregated metrics for a single day."""

    date: str
    task_count: int = 0
    total_cost_usd: float = 0.0
    avg_execution_time_s: float = 0.0
    success_rate: float = 0.0
    by_agent: dict[str, int] = field(default_factory=dict)
    by_tier: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PredictiveScalingEngine:
    """Forecast task volume and recommend resource scaling.

    Analyzes historical operational data to predict future demand,
    forecast daily costs, and recommend model tier adjustments.

    Args:
        data_dir: Directory for reading performance/cost data.
        forecast_horizon_days: Number of days to forecast ahead.
        history_days: Number of historical days to use for forecasting.
    """

    def __init__(
        self,
        data_dir: str | Path = "results",
        forecast_horizon_days: int = 7,
        history_days: int = 30,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.forecast_horizon = forecast_horizon_days
        self.history_days = history_days

        self._daily_metrics: dict[str, DailyMetrics] = {}
        self._cost_log: list[dict[str, Any]] = []

        self._load_historical_data()

    def forecast_task_volume(self, days_ahead: int | None = None) -> list[dict[str, Any]]:
        """Forecast daily task volume for the next N days.

        Uses simple moving average with trend adjustment.

        Args:
            days_ahead: Number of days to forecast (defaults to forecast_horizon).

        Returns:
            List of dicts with date, predicted_count, confidence_interval.
        """
        horizon = days_ahead or self.forecast_horizon
        daily_counts = self._get_daily_counts()

        if len(daily_counts) < 3:
            # Not enough data — return flat forecast
            avg = np.mean(daily_counts) if daily_counts else 5.0
            return [
                {
                    "date": (datetime.now() + timedelta(days=i + 1)).strftime("%Y-%m-%d"),
                    "predicted_count": round(float(avg), 1),
                    "lower_bound": round(float(avg * 0.5), 1),
                    "upper_bound": round(float(avg * 2.0), 1),
                    "confidence": 0.3,
                }
                for i in range(horizon)
            ]

        counts = np.array(daily_counts[-self.history_days:])

        # Simple moving average
        window = min(7, len(counts))
        sma = float(np.mean(counts[-window:]))

        # Trend calculation (linear regression over recent window)
        x = np.arange(len(counts[-window:]))
        y = counts[-window:]
        if len(x) > 1:
            slope = float(np.polyfit(x, y, 1)[0])
        else:
            slope = 0.0

        # Std for confidence intervals
        std = float(np.std(counts))

        forecasts: list[dict[str, Any]] = []
        for i in range(horizon):
            predicted = max(0, sma + slope * (i + 1))
            margin = 1.96 * std * np.sqrt(1 + (i + 1) / window)

            forecasts.append({
                "date": (datetime.now() + timedelta(days=i + 1)).strftime("%Y-%m-%d"),
                "predicted_count": round(predicted, 1),
                "lower_bound": round(max(0, predicted - margin), 1),
                "upper_bound": round(predicted + margin, 1),
                "confidence": round(max(0.3, 1.0 - 0.1 * i), 2),
            })

        return forecasts

    def forecast_daily_costs(self, days_ahead: int | None = None) -> list[dict[str, Any]]:
        """Forecast daily costs for the next N days.

        Args:
            days_ahead: Number of days to forecast.

        Returns:
            List of dicts with date, predicted_cost_usd, breakdown.
        """
        horizon = days_ahead or self.forecast_horizon
        daily_costs = self._get_daily_costs()

        if len(daily_costs) < 3:
            avg = np.mean(daily_costs) if daily_costs else 0.0
            return [
                {
                    "date": (datetime.now() + timedelta(days=i + 1)).strftime("%Y-%m-%d"),
                    "predicted_cost_usd": round(float(avg), 4),
                    "lower_bound": 0.0,
                    "upper_bound": round(float(avg * 3.0), 4),
                }
                for i in range(horizon)
            ]

        costs = np.array(daily_costs[-self.history_days:])
        window = min(7, len(costs))
        sma = float(np.mean(costs[-window:]))
        std = float(np.std(costs))

        # Trend
        x = np.arange(len(costs[-window:]))
        y = costs[-window:]
        slope = float(np.polyfit(x, y, 1)[0]) if len(x) > 1 else 0.0

        forecasts: list[dict[str, Any]] = []
        for i in range(horizon):
            predicted = max(0, sma + slope * (i + 1))
            margin = 1.96 * std * np.sqrt(1 + (i + 1) / window)

            forecasts.append({
                "date": (datetime.now() + timedelta(days=i + 1)).strftime("%Y-%m-%d"),
                "predicted_cost_usd": round(predicted, 4),
                "lower_bound": round(max(0, predicted - margin), 4),
                "upper_bound": round(predicted + margin, 4),
            })

        return forecasts

    def recommend_tier_adjustments(self) -> list[ScalingRecommendation]:
        """Recommend model tier adjustments based on cost/quality patterns.

        Analyzes whether tasks are being over-provisioned (simple tasks
        on premium models) or under-provisioned (complex tasks on fast models).

        Returns:
            List of ScalingRecommendation objects.
        """
        recommendations: list[ScalingRecommendation] = []
        ts = datetime.now().isoformat()

        # Analyze cost efficiency
        if self._cost_log:
            tier_costs: dict[str, list[float]] = defaultdict(list)
            for entry in self._cost_log:
                tier = entry.get("tier", "standard")
                cost = entry.get("cost_usd", 0.0)
                tier_costs[tier].append(cost)

            for tier, costs in tier_costs.items():
                avg_cost = np.mean(costs) if costs else 0
                if tier == "fast" and avg_cost > 0.01:
                    recommendations.append(ScalingRecommendation(
                        recommendation_type="tier_adjustment",
                        current_state={"tier": tier, "avg_cost": round(avg_cost, 4)},
                        predicted_state={"tier": "fast", "target_cost": 0.005},
                        action="Consider using smaller models for fast-tier tasks to reduce costs.",
                        confidence=0.6,
                        reasoning=f"Fast-tier tasks averaging ${avg_cost:.4f} per call.",
                        timestamp=ts,
                    ))
                elif tier == "premium" and avg_cost < 0.001:
                    recommendations.append(ScalingRecommendation(
                        recommendation_type="tier_adjustment",
                        current_state={"tier": tier, "avg_cost": round(avg_cost, 6)},
                        predicted_state={"tier": "standard", "target_cost": 0.005},
                        action="Premium tier may be over-provisioned. Consider downgrading to standard.",
                        confidence=0.5,
                        reasoning=f"Premium-tier tasks averaging only ${avg_cost:.6f} per call.",
                        timestamp=ts,
                    ))

        return recommendations

    def get_capacity_forecast(self) -> dict[str, Any]:
        """Get overall capacity forecast combining volume and cost predictions."""
        volume_forecast = self.forecast_task_volume(7)
        cost_forecast = self.forecast_daily_costs(7)

        total_predicted_tasks = sum(f["predicted_count"] for f in volume_forecast)
        total_predicted_cost = sum(f["predicted_cost_usd"] for f in cost_forecast)

        return {
            "forecast_period_days": 7,
            "total_predicted_tasks": round(total_predicted_tasks, 0),
            "total_predicted_cost_usd": round(total_predicted_cost, 4),
            "avg_daily_tasks": round(total_predicted_tasks / 7, 1),
            "avg_daily_cost_usd": round(total_predicted_cost / 7, 4),
            "volume_by_day": volume_forecast,
            "cost_by_day": cost_forecast,
            "generated_at": datetime.now().isoformat(),
        }

    def save_forecasts(self, forecasts: dict[str, Any]) -> None:
        """Persist forecast data to disk."""
        out_dir = self.data_dir / "forecasts"
        out_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = out_dir / f"forecast-{ts}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(forecasts, f, indent=2, default=str)

    # ── Data loading ───────────────────────────────────────────────

    def _get_daily_counts(self) -> list[float]:
        """Get daily task counts from historical data."""
        if not self._daily_metrics:
            return []
        return [float(m.task_count) for m in sorted(self._daily_metrics.values(), key=lambda m: m.date)]

    def _get_daily_costs(self) -> list[float]:
        """Get daily cost totals from historical data."""
        if not self._daily_metrics:
            return []
        return [m.total_cost_usd for m in sorted(self._daily_metrics.values(), key=lambda m: m.date)]

    def _load_historical_data(self) -> None:
        """Load historical performance and cost data."""
        # Load cost log
        cost_log_path = self.data_dir / "cost_log.jsonl"
        if cost_log_path.exists():
            try:
                with open(cost_log_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                self._cost_log.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
            except OSError:
                pass

        # Aggregate into daily metrics
        for entry in self._cost_log:
            day = entry.get("timestamp", "")[:10]
            if not day:
                continue

            if day not in self._daily_metrics:
                self._daily_metrics[day] = DailyMetrics(date=day)

            m = self._daily_metrics[day]
            m.task_count += 1
            m.total_cost_usd += entry.get("cost_usd", 0.0)

            agent = entry.get("agent_name", "unknown")
            m.by_agent[agent] = m.by_agent.get(agent, 0) + 1

        # Load execution records
        perf_dir = self.data_dir / "performance"
        records_path = perf_dir / "execution_records.json"
        if records_path.exists():
            try:
                with open(records_path, "r", encoding="utf-8") as f:
                    records = json.load(f)

                for rec in records:
                    ts = rec.get("timestamp", "")[:10]
                    if ts and ts in self._daily_metrics:
                        m = self._daily_metrics[ts]
                        # Running average of execution times
                        if m.avg_execution_time_s == 0:
                            m.avg_execution_time_s = rec.get("execution_time_s", 0)
                        else:
                            m.avg_execution_time_s = (
                                m.avg_execution_time_s + rec.get("execution_time_s", 0)
                            ) / 2

                        if rec.get("success", True):
                            m.success_rate = min(1.0, m.success_rate + 0.01)
            except (json.JSONDecodeError, OSError):
                pass

        # Load KPI snapshots
        kpi_dir = self.data_dir.parent / "orchestrator" / "kpi_snapshots"
        if kpi_dir.exists():
            for snap_file in sorted(kpi_dir.glob("snapshot-*.json")):
                try:
                    with open(snap_file, "r", encoding="utf-8") as f:
                        snap = json.load(f)
                    day = snap.get("collected_at", "")[:10]
                    if day and day in self._daily_metrics:
                        eng = snap.get("departments", {}).get("engineering", {})
                        kpis = eng.get("kpis", {})
                        completion = kpis.get("task_completion_rate", {})
                        if "current" in completion:
                            self._daily_metrics[day].success_rate = completion["current"] / 100.0
                except (json.JSONDecodeError, OSError):
                    continue

        logger.info("Loaded historical data for %d days", len(self._daily_metrics))
