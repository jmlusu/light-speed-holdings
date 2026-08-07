"""Periodic KPI snapshot scheduler — cron-style collection in the daemon.

Sprint 2, Item 3 of docs/CEO-DASHBOARD-OPERATIONALIZATION-PLAN.md.  The
executor daemon calls :meth:`KPISnapshotScheduler.run_due` on every poll
tick; once the configured interval has elapsed, :func:`run_snapshot`
collects all department KPIs and ingests the snapshot into SQLite via
``KPIPipeline``.  Collection is best-effort and never raises.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

from ai_company.data.database import Database

logger = logging.getLogger(__name__)

DEFAULT_SNAPSHOT_INTERVAL_SECONDS = 300.0


def run_snapshot(
    database: Database | None = None,
    project_root: Path | None = None,
) -> int:
    """Collect all department KPIs and ingest them into SQLite.

    Returns the number of KPI entries stored, or ``0`` when the SQLite
    data layer is unavailable.
    """
    from ai_company.dashboard.kpis import collect_all_kpis
    from ai_company.data import KPIPipeline, database_is_usable, get_database

    db = database or get_database()
    if db is None or not database_is_usable(db):
        logger.debug("KPI snapshot skipped: SQLite database unavailable")
        return 0

    snapshot = collect_all_kpis(project_root=project_root, database=db)
    pipeline = KPIPipeline(db)
    stored = pipeline.ingest_snapshot(snapshot)
    logger.info(
        "KPI snapshot stored %d entries across %d departments",
        stored,
        len(snapshot.get("departments", {})),
    )
    return stored


class KPISnapshotScheduler:
    """Time-gated wrapper around :func:`run_snapshot` for the daemon loop.

    Args:
        interval_seconds: Minimum seconds between snapshots. ``<= 0``
            disables collection (``run_due`` always returns ``0``).
        database: SQLite database to collect from and store into. ``None``
            falls back to the module-level database singleton.
        project_root: Project root for the KPI collectors. ``None`` uses
            :func:`ai_company.paths.get_project_root`.
    """

    def __init__(
        self,
        interval_seconds: float = DEFAULT_SNAPSHOT_INTERVAL_SECONDS,
        database: Database | None = None,
        project_root: Path | None = None,
    ) -> None:
        self.interval_seconds = interval_seconds
        self.database = database
        self.project_root = project_root
        self._last_run: float = 0.0

    def run_due(self, now: float | None = None) -> int:
        """Run a snapshot if the interval has elapsed; return entries stored.

        ``0`` means no snapshot was taken (too soon or disabled).
        """
        if self.interval_seconds <= 0:
            return 0
        current = now if now is not None else time.time()
        if current - self._last_run < self.interval_seconds:
            return 0
        self._last_run = current
        try:
            return run_snapshot(
                database=self.database,
                project_root=self.project_root,
            )
        except Exception:  # noqa: BLE001 - collection is best-effort
            logger.exception("KPI snapshot failed; will retry next interval")
            return 0

    def reset(self) -> None:
        """Force the next ``run_due`` call to take a snapshot."""
        self._last_run = 0.0


__all__ = [
    "DEFAULT_SNAPSHOT_INTERVAL_SECONDS",
    "KPISnapshotScheduler",
    "run_snapshot",
]
