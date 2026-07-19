"""KPI data retention — configurable policy, automatic cleanup, and archival.

This module manages the lifecycle of KPI history data:

- **Retention policy**: Configure how many days snapshots are kept (default 90).
- **Automatic cleanup**: Remove expired snapshots from the history store.
- **Archive**: Compress expired snapshots into a gzipped JSON file before
  deletion for optional future reference.
"""

from __future__ import annotations

import gzip
import json
import logging
import os
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from ai_company.dashboard.analytics import KPIHistoryStore

logger = logging.getLogger(__name__)


@dataclass
class RetentionPolicy:
    """Configurable retention policy for KPI history data.

    Parameters
    ----------
    max_days:
        Maximum age (in days) for stored snapshots. Older entries are
        eligible for cleanup. Default is 90 days.
    archive_enabled:
        If ``True``, expired data is archived to a compressed file before
        deletion. Default is ``True``.
    archive_dir:
        Directory where archive files are written. Defaults to
        ``dashboard/kpi_archive``.
    """

    max_days: int = 90
    archive_enabled: bool = True
    archive_dir: Path | None = None

    def __post_init__(self) -> None:
        if self.max_days < 1:
            raise ValueError("max_days must be >= 1")
        if self.archive_dir is None:
            self.archive_dir = Path("dashboard/kpi_archive")


# ---------------------------------------------------------------------------
# Retention engine
# ---------------------------------------------------------------------------


class RetentionEngine:
    """Enforces a retention policy on a :class:`KPIHistoryStore`.

    Usage::

        store = KPIHistoryStore()
        policy = RetentionPolicy(max_days=30)
        engine = RetentionEngine(store, policy)
        archived, deleted = engine.cleanup()
    """

    def __init__(
        self,
        history_store: KPIHistoryStore,
        policy: RetentionPolicy | None = None,
    ) -> None:
        self._store = history_store
        self._policy = policy or RetentionPolicy()

    @property
    def policy(self) -> RetentionPolicy:
        """Return the current retention policy."""
        return self._policy

    def update_policy(self, policy: RetentionPolicy) -> None:
        """Replace the current retention policy."""
        self._policy = policy

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def cleanup(self) -> tuple[int, int]:
        """Remove expired entries from the history store.

        Returns
        -------
        tuple[int, int]
            ``(archived_count, deleted_count)`` — number of entries
            archived and number of entries deleted.
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=self._policy.max_days)
        cutoff_iso = cutoff.isoformat()

        total_archived = 0
        total_deleted = 0

        for department in self._store.list_departments():
            entries = self._store.get_history(department, limit=0)
            expired = [e for e in entries if e.timestamp < cutoff_iso]

            if not expired:
                continue

            # Archive if enabled
            if self._policy.archive_enabled:
                archived_count = self._archive_expired(department, expired)
                total_archived += archived_count

            # Delete expired entries by rewriting the file
            deleted_count = self._remove_expired(department, expired)
            total_deleted += deleted_count

            # Invalidate cache
            self._store._cache.pop(department, None)  # noqa: SLF001

        return total_archived, total_deleted

    # ------------------------------------------------------------------
    # Archive
    # ------------------------------------------------------------------

    def archive_department(self, department: str) -> int:
        """Archive all history for a department, removing it from the store.

        Returns the number of entries archived.
        """
        entries = self._store.get_history(department, limit=0)
        if not entries:
            return 0

        archived_count = self._archive_expired(department, entries)
        # Clear the department
        self._store.clear(department)
        return archived_count

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _archive_expired(
        self,
        department: str,
        entries: list[Any],
    ) -> int:
        """Write expired entries to a compressed archive file."""
        archive_dir = self._policy.archive_dir
        if archive_dir is None:
            return 0

        archive_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        archive_path = archive_dir / f"{department}_archive_{ts}.json.gz"

        records = [entry.__dict__ if hasattr(entry, "__dict__") else entry for entry in entries]

        with gzip.open(archive_path, "wt", encoding="utf-8") as fh:
            json.dump(records, fh, indent=2, default=str)

        logger.info(
            "Archived %d entries for '%s' to %s",
            len(records),
            department,
            archive_path,
        )
        return len(records)

    def _remove_expired(
        self,
        department: str,
        expired: list[Any],
    ) -> int:
        """Rewrite the department history file without expired entries."""
        path = self._store._department_path(department)  # noqa: SLF001
        if not path.exists():
            return 0

        # Build a set of (timestamp, kpi_key) tuples for quick lookup
        expired_keys: set[tuple[str, str]] = {
            (e.timestamp, e.kpi_key) for e in expired
        }

        # Read all lines, skip expired ones
        remaining: list[str] = []
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    key = (data.get("timestamp", ""), data.get("kpi_key", ""))
                    if key not in expired_keys:
                        remaining.append(line)
                except (json.JSONDecodeError, TypeError):
                    # Preserve malformed lines as-is
                    remaining.append(line)

        # Write back using a temp file for atomicity
        fd, tmp_path = tempfile.mkstemp(
            dir=path.parent,
            prefix=f"{department}_",
            suffix=".tmp",
        )
        os.close(fd)  # Close the file descriptor immediately
        try:
            with open(tmp_path, "w", encoding="utf-8") as fh:
                for line in remaining:
                    fh.write(line + "\n")
            shutil.move(tmp_path, path)
        finally:
            # Clean up temp file if something went wrong
            tmp = Path(tmp_path)
            if tmp.exists():
                tmp.unlink()

        return len(expired)

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> dict[str, Any]:
        """Return retention statistics for all departments.

        Returns a dict with keys:

        - ``policy``: the current policy dict
        - ``departments``: per-department entry counts
        - ``total_entries``: sum across departments
        - ``expired_entries``: count of entries past the retention period
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=self._policy.max_days)
        cutoff_iso = cutoff.isoformat()

        total_entries = 0
        total_expired = 0
        dept_stats: dict[str, dict[str, int]] = {}

        for department in self._store.list_departments():
            entries = self._store.get_history(department, limit=0)
            count = len(entries)
            expired = sum(1 for e in entries if e.timestamp < cutoff_iso)

            dept_stats[department] = {
                "entries": count,
                "expired": expired,
            }
            total_entries += count
            total_expired += expired

        return {
            "policy": {
                "max_days": self._policy.max_days,
                "archive_enabled": self._policy.archive_enabled,
                "archive_dir": str(self._policy.archive_dir) if self._policy.archive_dir else None,
            },
            "departments": dept_stats,
            "total_entries": total_entries,
            "expired_entries": total_expired,
        }


def run_cleanup(
    history_store: KPIHistoryStore,
    policy: RetentionPolicy | None = None,
) -> tuple[int, int]:
    """Convenience function to run cleanup once.

    Parameters
    ----------
    history_store:
        The history store to clean.
    policy:
        Retention policy. Defaults to 90 days with archiving.

    Returns
    -------
    tuple[int, int]
        ``(archived_count, deleted_count)``.
    """
    engine = RetentionEngine(history_store, policy or RetentionPolicy())
    return engine.cleanup()


__all__ = [
    "RetentionEngine",
    "RetentionPolicy",
    "run_cleanup",
]
