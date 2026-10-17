"""Learning metrics — tracks whether agents are improving over time.

Instruments the learning pipeline to measure:
- Token efficiency (avg tokens per task, should decrease)
- Iteration efficiency (avg iterations per task, should decrease)
- Error recurrence (repeated errors across sessions, should decrease)
- Memory hit rate (similarity scores from recall_context)
- Knowledge growth (entries by type over time)
- Consolidation health (prune/dedup/digest counts)

Data is persisted to ``memory/metrics.json`` and append-only.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class TaskMetrics:
    """Metrics recorded after a single task execution."""

    task_id: str
    agent_id: str
    status: str  # completed, failed, timeout
    iterations: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    memory_recall_count: int = 0
    memory_avg_similarity: float = 0.0
    tool_names: list[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


@dataclass
class LearningSnapshot:
    """Aggregated learning health snapshot."""

    # Token efficiency
    avg_tokens_per_task: float = 0.0
    token_trend: str = "stable"  # improving, degrading, stable

    # Iteration efficiency
    avg_iterations_per_task: float = 0.0
    iteration_trend: str = "stable"

    # Error recurrence
    error_rate: float = 0.0
    error_trend: str = "stable"

    # Memory health
    memory_hit_rate: float = 0.0
    memory_avg_similarity: float = 0.0

    # Knowledge growth
    episodic_count: int = 0
    semantic_count: int = 0
    procedural_count: int = 0
    aggregate_count: int = 0

    # Consolidation health
    last_consolidation: str = ""
    entries_pruned_total: int = 0
    episodic_digested_total: int = 0

    # Overall
    total_tasks_recorded: int = 0
    snapshot_timestamp: float = field(default_factory=time.time)


class LearningMetricsCollector:
    """Collects and persists learning metrics for the continuous learning system.

    Appends task-level metrics and periodically computes aggregated snapshots.
    """

    def __init__(self, base_dir: str = "memory") -> None:
        self._base_dir = Path(base_dir)
        self._metrics_file = self._base_dir / "metrics.json"
        self._task_metrics: list[dict[str, Any]] = []
        self._snapshots: list[dict[str, Any]] = []
        self._entries_pruned_total = 0
        self._episodic_digested_total = 0
        self._load()

    def _load(self) -> None:
        """Load persisted metrics from disk."""
        self._entries_pruned_total = 0
        self._episodic_digested_total = 0
        if self._metrics_file.exists():
            try:
                data = json.loads(self._metrics_file.read_text(encoding="utf-8"))
                self._task_metrics = data.get("task_metrics", [])
                self._snapshots = data.get("snapshots", [])
                self._entries_pruned_total = int(data.get("entries_pruned_total", 0))
                self._episodic_digested_total = int(data.get("episodic_digested_total", 0))
            except (json.JSONDecodeError, OSError):
                logger.debug("Could not load metrics file, starting fresh")

    def _save(self) -> None:
        """Persist metrics to disk (atomic write)."""
        self._base_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "task_metrics": self._task_metrics[-1000:],  # Keep last 1000
            "snapshots": self._snapshots[-100:],  # Keep last 100 snapshots
            "entries_pruned_total": self._entries_pruned_total,
            "episodic_digested_total": self._episodic_digested_total,
        }
        tmp = self._metrics_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.replace(self._metrics_file)

    def record_task(self, metrics: TaskMetrics) -> None:
        """Record metrics for a completed task."""
        self._task_metrics.append(asdict(metrics))
        self._save()

    def record_memory_recall(self, count: int, avg_similarity: float) -> None:
        """Record memory recall stats for the current task context."""
        # Appended to the most recent task metric if available
        if self._task_metrics:
            self._task_metrics[-1]["memory_recall_count"] = count
            self._task_metrics[-1]["memory_avg_similarity"] = avg_similarity
            self._save()

    def record_consolidation(
        self,
        entries_pruned: int = 0,
        episodic_digested: int = 0,
        semantic_deduped: int = 0,
    ) -> None:
        """Record consolidation run stats as running totals."""
        self._entries_pruned_total += entries_pruned
        self._episodic_digested_total += episodic_digested
        self._save()

    def compute_snapshot(self, store: Any = None) -> LearningSnapshot:
        """Compute an aggregated learning health snapshot.

        Args:
            store: Optional MemoryStore to query for knowledge counts.

        Returns:
            The computed LearningSnapshot.
        """
        tasks = self._task_metrics
        snap = LearningSnapshot()
        snap.entries_pruned_total = self._entries_pruned_total
        snap.episodic_digested_total = self._episodic_digested_total

        if not tasks:
            self._snapshots.append(asdict(snap))
            self._save()
            return snap

        # Token efficiency
        token_tasks = [t for t in tasks if t.get("total_tokens", 0) > 0]
        if token_tasks:
            snap.avg_tokens_per_task = sum(t["total_tokens"] for t in token_tasks) / len(
                token_tasks
            )
            # Trend: compare last 10 vs previous 10
            if len(token_tasks) >= 20:
                recent = sum(t["total_tokens"] for t in token_tasks[-10:]) / 10
                prev = sum(t["total_tokens"] for t in token_tasks[-20:-10]) / 10
                if recent < prev * 0.9:
                    snap.token_trend = "improving"
                elif recent > prev * 1.1:
                    snap.token_trend = "degrading"

        # Iteration efficiency
        iter_tasks = [t for t in tasks if t.get("iterations", 0) > 0]
        if iter_tasks:
            snap.avg_iterations_per_task = sum(t["iterations"] for t in iter_tasks) / len(
                iter_tasks
            )
            if len(iter_tasks) >= 20:
                recent = sum(t["iterations"] for t in iter_tasks[-10:]) / 10
                prev = sum(t["iterations"] for t in iter_tasks[-20:-10]) / 10
                if recent < prev * 0.9:
                    snap.iteration_trend = "improving"
                elif recent > prev * 1.1:
                    snap.iteration_trend = "degrading"

        # Error recurrence
        failed = [t for t in tasks if t.get("status") in ("failed", "timeout")]
        snap.error_rate = len(failed) / len(tasks) if tasks else 0.0
        if len(tasks) >= 20:
            recent_failures = sum(
                1 for t in tasks[-10:] if t.get("status") in ("failed", "timeout")
            )
            prev_failures = sum(
                1 for t in tasks[-20:-10] if t.get("status") in ("failed", "timeout")
            )
            if recent_failures < prev_failures:
                snap.error_trend = "improving"
            elif recent_failures > prev_failures:
                snap.error_trend = "degrading"

        # Memory hit rate
        recall_tasks = [t for t in tasks if t.get("memory_recall_count", 0) > 0]
        if recall_tasks:
            snap.memory_hit_rate = len(recall_tasks) / len(tasks)
            snap.memory_avg_similarity = sum(
                t.get("memory_avg_similarity", 0) for t in recall_tasks
            ) / len(recall_tasks)

        # Knowledge growth (from store)
        if store is not None:
            try:
                stats = store.stats()
                snap.episodic_count = stats.get("episodic", 0)
                snap.semantic_count = stats.get("semantic", 0)
                snap.procedural_count = stats.get("procedural", 0)
                snap.aggregate_count = stats.get("aggregate", 0)
            except Exception:  # noqa: BLE001
                pass

        snap.total_tasks_recorded = len(tasks)

        self._snapshots.append(asdict(snap))
        self._save()
        return snap

    def get_latest_snapshot(self) -> LearningSnapshot | None:
        """Return the most recent learning health snapshot."""
        if not self._snapshots:
            return None
        data = self._snapshots[-1]
        return LearningSnapshot(**data)

    def get_recent_tasks(self, limit: int = 10) -> list[dict[str, Any]]:
        """Return the most recent task metrics."""
        return self._task_metrics[-limit:]
