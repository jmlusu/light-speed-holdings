"""Agent performance tracking and prediction.

Tracks per-agent metrics (success rate, execution time, token usage,
cost) and builds a simple regression model to predict task completion
time.  Used for smarter task routing and SLA estimation.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class AgentMetrics:
    """Aggregated performance metrics for a single agent."""

    agent_id: str
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    total_execution_time_s: float = 0.0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    avg_execution_time_s: float = 0.0
    avg_tokens_per_task: float = 0.0
    avg_cost_per_task: float = 0.0
    success_rate: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TaskExecutionRecord:
    """A single task execution record for performance modeling."""

    task_id: str
    agent_id: str
    timestamp: str
    execution_time_s: float
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    success: bool
    priority: str = "medium"
    task_complexity: float = 0.5  # 0.0 (simple) to 1.0 (complex)
    model_used: str = ""
    iterations: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AgentPerformanceTracker:
    """Tracks and predicts agent performance metrics.

    Maintains per-agent statistics and a lightweight regression model
    for predicting task execution time based on task complexity and
    agent characteristics.

    Args:
        data_dir: Directory for persisting performance data.
    """

    def __init__(self, data_dir: str | Path = "results/performance") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self._records: list[TaskExecutionRecord] = []
        self._agent_metrics: dict[str, AgentMetrics] = {}
        self._model: Any = None  # sklearn regressor
        self._model_trained = False

        self._load_data()

    def record_execution(self, record: TaskExecutionRecord) -> None:
        """Record a task execution and update metrics.

        Args:
            record: The execution record to store.
        """
        self._records.append(record)
        self._update_agent_metrics(record)
        self._persist_record(record)

    def get_agent_metrics(self, agent_id: str) -> AgentMetrics | None:
        """Get aggregated metrics for a specific agent."""
        return self._agent_metrics.get(agent_id)

    def get_all_metrics(self) -> dict[str, AgentMetrics]:
        """Get metrics for all tracked agents."""
        return dict(self._agent_metrics)

    def get_top_agents(self, metric: str = "success_rate", top_k: int = 5) -> list[AgentMetrics]:
        """Get top agents ranked by a specific metric.

        Args:
            metric: Metric name to sort by.
            top_k: Number of top agents to return.
        """
        metrics = list(self._agent_metrics.values())
        if not metrics:
            return []

        def _sort_key(m: AgentMetrics) -> float:
            return getattr(m, metric, 0)

        metrics.sort(key=_sort_key, reverse=True)
        return metrics[:top_k]

    def predict_execution_time(
        self,
        agent_id: str,
        task_complexity: float,
        priority: str = "medium",
    ) -> float:
        """Predict task execution time for an agent given task complexity.

        Uses historical data for the agent, or falls back to global averages
        if insufficient data exists.

        Args:
            agent_id: The agent that will execute the task.
            task_complexity: Complexity score from 0.0 to 1.0.
            priority: Task priority level.

        Returns:
            Predicted execution time in seconds.
        """
        agent_records = [r for r in self._records if r.agent_id == agent_id]

        if len(agent_records) < 5:
            # Not enough data for regression — use global average with complexity adjustment
            global_avg = self._global_avg_execution_time()
            complexity_factor = 0.5 + task_complexity  # range [0.5, 1.5]
            return global_avg * complexity_factor

        # Build feature matrix: [complexity, priority_encoded]
        priority_map = {"low": 0, "medium": 0.5, "high": 0.8, "critical": 1.0}
        X = np.array([
            [r.task_complexity, priority_map.get(r.priority, 0.5)]
            for r in agent_records
        ])
        y = np.array([r.execution_time_s for r in agent_records])

        try:
            from sklearn.linear_model import Ridge

            model = Ridge(alpha=1.0)
            model.fit(X, y)

            features = np.array([[task_complexity, priority_map.get(priority, 0.5)]])
            prediction = model.predict(features)[0]
            return max(1.0, float(prediction))  # Floor at 1 second
        except ImportError:
            # Fallback: weighted average
            weights = np.array([r.task_complexity for r in agent_records])
            times = np.array([r.execution_time_s for r in agent_records])
            if weights.sum() > 0:
                return float(np.average(times, weights=weights + 0.01))
            return self._global_avg_execution_time()

    def estimate_sla(
        self,
        agent_id: str,
        task_complexity: float,
        priority: str = "medium",
        confidence: float = 0.9,
    ) -> dict[str, Any]:
        """Estimate SLA (Service Level Agreement) for a task.

        Args:
            agent_id: The assigned agent.
            task_complexity: Complexity score 0.0–1.0.
            priority: Task priority level.
            confidence: Confidence level for the estimate (0.5–0.99).

        Returns:
            Dict with predicted_time_s, upper_bound_s, and confidence.
        """
        agent_records = [r for r in self._records if r.agent_id == agent_id]
        predicted = self.predict_execution_time(agent_id, task_complexity, priority)

        if len(agent_records) < 3:
            return {
                "agent_id": agent_id,
                "predicted_time_s": round(predicted, 1),
                "upper_bound_s": round(predicted * 2.0, 1),
                "confidence": 0.5,
                "data_points": len(agent_records),
            }

        times = np.array([r.execution_time_s for r in agent_records])
        std = float(np.std(times))
        from scipy import stats as sp_stats  # type: ignore[import-untyped]

        z = sp_stats.norm.ppf(confidence)  # type: ignore[attr-defined]
        upper = predicted + z * std

        return {
            "agent_id": agent_id,
            "predicted_time_s": round(predicted, 1),
            "upper_bound_s": round(max(upper, predicted * 1.2), 1),
            "confidence": confidence,
            "data_points": len(agent_records),
        }

    def get_global_stats(self) -> dict[str, Any]:
        """Get global performance statistics across all agents."""
        if not self._records:
            return {"total_records": 0, "agents": 0}

        total_tasks = len(self._records)
        successful = sum(1 for r in self._records if r.success)
        total_cost = sum(r.cost_usd for r in self._records)
        total_tokens = sum(r.prompt_tokens + r.completion_tokens for r in self._records)
        avg_time = np.mean([r.execution_time_s for r in self._records])

        return {
            "total_records": total_tasks,
            "agents": len(self._agent_metrics),
            "global_success_rate": round(successful / total_tasks, 3) if total_tasks else 0,
            "global_avg_execution_time_s": round(float(avg_time), 2),
            "total_cost_usd": round(total_cost, 4),
            "total_tokens": total_tokens,
        }

    def save_metrics(self) -> None:
        """Persist all metrics and records to disk."""
        # Save records
        records_file = self.data_dir / "execution_records.json"
        with open(records_file, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in self._records], f, indent=2, default=str)

        # Save agent metrics
        metrics_file = self.data_dir / "agent_metrics.json"
        with open(metrics_file, "w", encoding="utf-8") as f:
            json.dump(
                {k: v.to_dict() for k, v in self._agent_metrics.items()},
                f,
                indent=2,
                default=str,
            )

    # ── Private helpers ────────────────────────────────────────────

    def _update_agent_metrics(self, record: TaskExecutionRecord) -> None:
        """Update aggregated metrics for the agent."""
        agent_id = record.agent_id
        if agent_id not in self._agent_metrics:
            self._agent_metrics[agent_id] = AgentMetrics(agent_id=agent_id)

        m = self._agent_metrics[agent_id]
        m.total_tasks += 1
        if record.success:
            m.successful_tasks += 1
        else:
            m.failed_tasks += 1

        m.total_execution_time_s += record.execution_time_s
        m.total_tokens += record.prompt_tokens + record.completion_tokens
        m.total_cost_usd += record.cost_usd

        m.avg_execution_time_s = m.total_execution_time_s / m.total_tasks
        m.avg_tokens_per_task = m.total_tokens / m.total_tasks
        m.avg_cost_per_task = m.total_cost_usd / m.total_tasks
        m.success_rate = m.successful_tasks / m.total_tasks

    def _global_avg_execution_time(self) -> float:
        """Compute global average execution time across all agents."""
        if not self._records:
            return 30.0  # Default assumption
        return float(np.mean([r.execution_time_s for r in self._records]))

    def _persist_record(self, record: TaskExecutionRecord) -> None:
        """Append a single record to the JSONL log."""
        log_file = self.data_dir / "execution_log.jsonl"
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record.to_dict(), default=str) + "\n")
        except OSError:
            pass

    def _load_data(self) -> None:
        """Load persisted records and metrics."""
        records_file = self.data_dir / "execution_records.json"
        if records_file.exists():
            try:
                with open(records_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._records = [TaskExecutionRecord(**r) for r in data]
            except (json.JSONDecodeError, KeyError, OSError) as exc:
                logger.warning("Failed to load execution records: %s", exc)

        metrics_file = self.data_dir / "agent_metrics.json"
        if metrics_file.exists():
            try:
                with open(metrics_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._agent_metrics = {k: AgentMetrics(**v) for k, v in data.items()}
            except (json.JSONDecodeError, KeyError, OSError) as exc:
                logger.warning("Failed to load agent metrics: %s", exc)
