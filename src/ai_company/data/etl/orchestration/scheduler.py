"""Pipeline Orchestration.

Scheduler, monitor, and dead letter handling for ETL pipelines.
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from ai_company.data.database import Database

logger = logging.getLogger(__name__)


@dataclass
class PipelineSchedule:
    """Schedule configuration for a pipeline."""

    name: str
    pipeline_factory: Callable[[], Any]  # Callable that returns a Pipeline instance
    interval_seconds: float
    enabled: bool = True
    last_run: float = 0.0
    last_result: Any = None
    run_count: int = 0
    error_count: int = 0
    kwargs: dict[str, Any] = field(default_factory=dict)


class PipelineScheduler:
    """Time-gated scheduler for running pipelines on a cadence.

    Similar to KPISnapshotScheduler and GovernanceScheduler but generic
    for any Pipeline subclass.
    """

    def __init__(
        self,
        database: Database,
        tick_interval_seconds: float = 60.0,
    ):
        self.database = database
        self.tick_interval = tick_interval_seconds
        self._schedules: dict[str, PipelineSchedule] = {}
        self._running = False
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

    def add_pipeline(
        self,
        name: str,
        pipeline_factory: Callable[[], Any],
        interval_seconds: float,
        enabled: bool = True,
        **kwargs: Any,
    ) -> None:
        """Register a pipeline with a schedule.

        Args:
            name: Unique pipeline name
            pipeline_factory: Callable that returns a fresh Pipeline instance
            interval_seconds: Minimum seconds between runs
            enabled: Whether schedule is active
            **kwargs: Arguments passed to pipeline.run()
        """
        with self._lock:
            self._schedules[name] = PipelineSchedule(
                name=name,
                pipeline_factory=pipeline_factory,
                interval_seconds=interval_seconds,
                enabled=enabled,
                kwargs=kwargs,
            )
            logger.info("Registered pipeline schedule: %s every %.0fs", name, interval_seconds)

    def remove_pipeline(self, name: str) -> bool:
        """Remove a pipeline from the schedule."""
        with self._lock:
            if name in self._schedules:
                del self._schedules[name]
                logger.info("Removed pipeline schedule: %s", name)
                return True
            return False

    def run_due(self, now: float | None = None) -> dict[str, Any]:
        """Run all pipelines whose interval has elapsed.

        Args:
            now: Current timestamp (for testing)

        Returns:
            Dict of pipeline_name -> PipelineResult
        """
        current = now if now is not None else time.time()
        results = {}

        with self._lock:
            schedules = list(self._schedules.values())

        for schedule in schedules:
            if not schedule.enabled:
                continue
            if schedule.interval_seconds <= 0:
                continue
            if current - schedule.last_run < schedule.interval_seconds:
                continue

            # Run the pipeline
            logger.info("Running scheduled pipeline: %s", schedule.name)
            try:
                pipeline = schedule.pipeline_factory()
                result = pipeline.run(**schedule.kwargs)
                schedule.last_run = current
                schedule.last_result = result
                schedule.run_count += 1
                if not result.success:
                    schedule.error_count += 1
                results[schedule.name] = result
            except Exception as exc:  # noqa: BLE001
                logger.exception("Pipeline %s failed", schedule.name)
                schedule.error_count += 1
                results[schedule.name] = {"error": str(exc), "success": False}

        return results

    def run_once(self, name: str, **override_kwargs: Any) -> Any | None:
        """Manually trigger a single pipeline run."""
        with self._lock:
            schedule = self._schedules.get(name)
        if not schedule:
            logger.warning("Pipeline not found: %s", name)
            return None

        logger.info("Manual run of pipeline: %s", name)
        try:
            pipeline = schedule.pipeline_factory()
            kwargs = {**schedule.kwargs, **override_kwargs}
            result = pipeline.run(**kwargs)
            schedule.last_result = result
            if not result.success:
                schedule.error_count += 1
            else:
                schedule.run_count += 1
            return result
        except Exception as exc:  # noqa: BLE001
            logger.exception("Manual pipeline run failed: %s", name)
            return {"error": str(exc), "success": False}

    def get_status(self) -> dict[str, Any]:
        """Get status of all scheduled pipelines."""
        with self._lock:
            return {
                name: {
                    "enabled": s.enabled,
                    "interval_seconds": s.interval_seconds,
                    "last_run": datetime.fromtimestamp(s.last_run, tz=timezone.utc).isoformat()
                    if s.last_run > 0
                    else None,
                    "run_count": s.run_count,
                    "error_count": s.error_count,
                    "last_success": s.last_result.success if s.last_result else None,
                }
                for name, s in self._schedules.items()
            }

    def start(self) -> None:
        """Start the scheduler loop in a background thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("Pipeline scheduler started")

    def stop(self) -> None:
        """Stop the scheduler loop."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5.0)
        logger.info("Pipeline scheduler stopped")

    def _run_loop(self) -> None:
        while self._running:
            try:
                self.run_due()
            except Exception:  # noqa: BLE001
                logger.exception("Scheduler tick failed")
            time.sleep(self.tick_interval)


class PipelineMonitor:
    """Monitor pipeline health and emit alerts."""

    def __init__(self, database: Database):
        self.database = database

    def check_pipeline_health(self, scheduler: PipelineScheduler) -> dict[str, Any]:
        """Check health of all scheduled pipelines."""
        status = scheduler.get_status()
        now = time.time()

        alerts = []
        for name, info in status.items():
            if not info["enabled"]:
                continue

            last_run = info["last_run"]
            if last_run:
                last_run_ts = datetime.fromisoformat(last_run.replace("Z", "+00:00")).timestamp()
                interval = next(
                    (s.interval_seconds for s in scheduler._schedules.values() if s.name == name),
                    0,
                )
                if interval > 0 and now - last_run_ts > interval * 2:
                    alerts.append(
                        {
                            "severity": "warning",
                            "pipeline": name,
                            "message": f"Pipeline overdue: last run {last_run}, interval {interval}s",
                        }
                    )

            if info["error_count"] > 0 and info["run_count"] > 0:
                error_rate = info["error_count"] / info["run_count"]
                if error_rate > 0.5:
                    alerts.append(
                        {
                            "severity": "critical",
                            "pipeline": name,
                            "message": f"High error rate: {error_rate:.1%} ({info['error_count']}/{info['run_count']})",
                        }
                    )

        return {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "pipelines": status,
            "alerts": alerts,
            "healthy": len([a for a in alerts if a["severity"] == "critical"]) == 0,
        }

    def emit_metrics(self, scheduler: PipelineScheduler) -> dict[str, Any]:
        """Emit pipeline metrics for Prometheus/Grafana."""
        status = scheduler.get_status()
        metrics: dict[str, dict[str, Any]] = {
            "pipeline_runs_total": {},
            "pipeline_errors_total": {},
            "pipeline_last_run_seconds_ago": {},
            "pipeline_success": {},
        }

        now = time.time()
        for name, info in status.items():
            metrics["pipeline_runs_total"][name] = info["run_count"]
            metrics["pipeline_errors_total"][name] = info["error_count"]
            if info["last_run"]:
                last_run_ts = datetime.fromisoformat(
                    info["last_run"].replace("Z", "+00:00")
                ).timestamp()
                metrics["pipeline_last_run_seconds_ago"][name] = now - last_run_ts
            else:
                metrics["pipeline_last_run_seconds_ago"][name] = -1
            metrics["pipeline_success"][name] = 1 if info["last_success"] else 0

        return metrics


# Default scheduler factory for the daemon
def create_default_scheduler(database: Database) -> PipelineScheduler:
    """Create a scheduler with all default pipelines registered."""
    scheduler = PipelineScheduler(database)

    # Register KPI snapshot pipeline (every 5 minutes)
    from ai_company.data.etl.pipelines.kpi_snapshot import KPISnapshotPipeline

    scheduler.add_pipeline(
        "kpi_snapshot",
        lambda: KPISnapshotPipeline(database),
        interval_seconds=300.0,
        enabled=True,
    )

    # Register company KPI pipeline (every hour)
    from ai_company.data.etl.pipelines.kpi_snapshot import CompanyKPIPipeline

    scheduler.add_pipeline(
        "company_kpi",
        lambda: CompanyKPIPipeline(database),
        interval_seconds=3600.0,
        enabled=True,
        write_to_yaml=True,  # Update config YAML
    )

    # Register cost aggregations
    from ai_company.data.etl.pipelines.kpi_snapshot import CostAggregationPipeline

    scheduler.add_pipeline(
        "cost_daily",
        lambda: CostAggregationPipeline(database, period="daily"),
        interval_seconds=3600.0,
        enabled=True,
    )
    scheduler.add_pipeline(
        "cost_weekly",
        lambda: CostAggregationPipeline(database, period="weekly"),
        interval_seconds=86400.0,
        enabled=True,
    )
    scheduler.add_pipeline(
        "cost_monthly",
        lambda: CostAggregationPipeline(database, period="monthly"),
        interval_seconds=86400.0 * 7,
        enabled=True,
    )

    # Register agent performance (every 15 minutes)
    from ai_company.data.etl.pipelines.kpi_snapshot import AgentPerformancePipeline

    scheduler.add_pipeline(
        "agent_performance",
        lambda: AgentPerformancePipeline(database, days=30),
        interval_seconds=900.0,
        enabled=True,
    )

    # Register governance (daily)
    from ai_company.data.etl.pipelines.governance import (
        DeadLetterProcessingPipeline,
        GovernancePipeline,
        InboxPurgePipeline,
    )

    scheduler.add_pipeline(
        "governance",
        lambda: GovernancePipeline(database),
        interval_seconds=86400.0,
        enabled=True,
    )

    # Register DLQ processing (every 10 minutes)
    scheduler.add_pipeline(
        "dlq_processing",
        lambda: DeadLetterProcessingPipeline(database),
        interval_seconds=600.0,
        enabled=True,
        auto_retry=True,
        max_retries=3,
    )

    # Register inbox purge (every 6 hours)
    scheduler.add_pipeline(
        "inbox_purge",
        lambda: InboxPurgePipeline(database),
        interval_seconds=21600.0,
        enabled=True,
        max_age_days=30,
        statuses_to_purge=["completed", "failed"],
    )

    return scheduler


__all__ = [
    "PipelineSchedule",
    "PipelineScheduler",
    "PipelineMonitor",
    "create_default_scheduler",
]
