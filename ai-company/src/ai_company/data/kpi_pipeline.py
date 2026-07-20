"""KPI analytics pipeline — aggregation, time-series, and anomaly detection.

Replaces the file-based ``KPIHistoryStore`` in ``dashboard/analytics.py``
with efficient SQLite queries and adds anomaly detection capabilities.
"""

from __future__ import annotations

import json
import logging
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

from ai_company.data.database import Database

logger = logging.getLogger(__name__)


class KPIPipeline:
    """KPI data pipeline backed by SQLite.

    Provides:
      - Ingestion of KPI snapshots into the time-series store.
      - Aggregation across departments and time windows.
      - Anomaly detection via Z-score and moving-average methods.
      - Rollup statistics (daily, weekly, monthly).

    Args:
        database: An initialised :class:`Database` instance.
    """

    def __init__(self, database: Database) -> None:
        self._db = database

    # ── Ingestion ─────────────────────────────────────────────────────

    def ingest_snapshot(self, snapshot: dict[str, Any]) -> int:
        """Ingest a KPI snapshot (as returned by ``collect_all_kpis()``).

        Returns the number of KPI entries stored.
        """
        collected_at = snapshot.get("collected_at", datetime.now(timezone.utc).isoformat())
        departments: dict[str, Any] = snapshot.get("departments", {})
        count = 0

        for dept_id, dept_data in departments.items():
            kpis: dict[str, Any] = dept_data.get("kpis", {})
            for kpi_key, kpi_value in kpis.items():
                target = kpi_value.get("target")
                self._db.execute(
                    """INSERT INTO kpi_values
                       (timestamp, department, kpi_key, current_value, target_value, unit, status)
                       VALUES (?,?,?,?,?,?,?)""",
                    (
                        collected_at,
                        dept_id,
                        kpi_key,
                        float(kpi_value.get("current", 0)),
                        float(target) if target is not None else None,
                        kpi_value.get("unit", ""),
                        kpi_value.get("status", "info"),
                    ),
                )
                count += 1

        self._db.commit()
        return count

    def ingest_individual(
        self,
        department: str,
        kpi_key: str,
        current_value: float,
        target_value: float | None = None,
        unit: str = "",
        status: str = "info",
        timestamp: str | None = None,
    ) -> None:
        """Ingest a single KPI data point."""
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        self._db.execute(
            """INSERT INTO kpi_values
               (timestamp, department, kpi_key, current_value, target_value, unit, status)
               VALUES (?,?,?,?,?,?,?)""",
            (ts, department, kpi_key, current_value, target_value, unit, status),
        )
        self._db.commit()

    # ── Query API ─────────────────────────────────────────────────────

    def get_history(
        self,
        department: str,
        kpi_key: str | None = None,
        *,
        since: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Retrieve KPI history for a department, optionally filtered by KPI."""
        conditions = ["department = ?"]
        params: list[Any] = [department]

        if kpi_key is not None:
            conditions.append("kpi_key = ?")
            params.append(kpi_key)
        if since is not None:
            conditions.append("timestamp >= ?")
            params.append(since)

        where = " AND ".join(conditions)
        params.append(limit)

        return self._db.fetchall(
            f"""SELECT * FROM kpi_values
                WHERE {where}
                ORDER BY timestamp DESC
                LIMIT ?""",
            tuple(params),
        )

    def get_latest(self, department: str, kpi_key: str | None = None) -> list[dict[str, Any]]:
        """Return the most recent snapshot for a department."""
        if kpi_key:
            return self._db.fetchall(
                """SELECT * FROM kpi_values
                   WHERE department = ? AND kpi_key = ?
                   ORDER BY timestamp DESC LIMIT 1""",
                (department, kpi_key),
            )

        # Get the latest timestamp for this department
        row = self._db.fetchone(
            "SELECT MAX(timestamp) as ts FROM kpi_values WHERE department = ?",
            (department,),
        )
        if not row or not row.get("ts"):
            return []

        return self._db.fetchall(
            "SELECT * FROM kpi_values WHERE department = ? AND timestamp = ?",
            (department, row["ts"]),
        )

    def list_departments(self) -> list[str]:
        """Return department IDs that have stored KPI data."""
        rows = self._db.fetchall(
            "SELECT DISTINCT department FROM kpi_values ORDER BY department"
        )
        return [r["department"] for r in rows]

    def list_kpi_keys(self, department: str | None = None) -> list[str]:
        """Return distinct KPI keys, optionally for a department."""
        if department:
            rows = self._db.fetchall(
                "SELECT DISTINCT kpi_key FROM kpi_values WHERE department = ? ORDER BY kpi_key",
                (department,),
            )
        else:
            rows = self._db.fetchall(
                "SELECT DISTINCT kpi_key FROM kpi_values ORDER BY kpi_key"
            )
        return [r["kpi_key"] for r in rows]

    # ── Aggregation ───────────────────────────────────────────────────

    def aggregate(
        self,
        department: str,
        period: Literal["daily", "weekly", "monthly"] = "daily",
        *,
        kpi_key: str | None = None,
        days: int = 30,
    ) -> list[dict[str, Any]]:
        """Compute rollup statistics for a department.

        Returns one row per (kpi_key, period_bucket) with min, max, mean, count.
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        conditions = ["department = ?", "timestamp >= ?"]
        params: list[Any] = [department, cutoff]

        if kpi_key:
            conditions.append("kpi_key = ?")
            params.append(kpi_key)

        where = " AND ".join(conditions)

        # Use SQLite date functions for bucketing
        if period == "daily":
            bucket_expr = "date(timestamp)"
        elif period == "weekly":
            bucket_expr = "date(timestamp, 'weekday 0', '-6 days')"
        elif period == "monthly":
            bucket_expr = "date(timestamp, 'start of month')"
        else:
            raise ValueError(f"Unknown period: {period}")

        rows = self._db.fetchall(
            f"""SELECT
                    kpi_key,
                    {bucket_expr} as period_start,
                    MIN(current_value) as min_value,
                    MAX(current_value) as max_value,
                    AVG(current_value) as mean_value,
                    COUNT(*) as sample_count,
                    unit
                FROM kpi_values
                WHERE {where}
                GROUP BY kpi_key, period_start
                ORDER BY kpi_key, period_start""",
            tuple(params),
        )

        # Round float values
        for row in rows:
            row["min_value"] = round(row["min_value"], 4)
            row["max_value"] = round(row["max_value"], 4)
            row["mean_value"] = round(row["mean_value"], 4)

        return rows

    def aggregate_cross_department(
        self,
        period: Literal["daily", "weekly", "monthly"] = "daily",
        days: int = 7,
    ) -> dict[str, list[dict[str, Any]]]:
        """Aggregate KPIs across all departments. Returns a dict keyed by department."""
        departments = self.list_departments()
        result: dict[str, list[dict[str, Any]]] = {}
        for dept in departments:
            result[dept] = self.aggregate(dept, period, days=days)
        return result

    # ── Anomaly detection ─────────────────────────────────────────────

    def detect_anomalies(
        self,
        department: str,
        kpi_key: str,
        *,
        z_threshold: float = 2.0,
        window: int = 30,
    ) -> list[dict[str, Any]]:
        """Detect anomalous KPI values using Z-score method.

        Scans the last *window* data points and flags those whose Z-score
        exceeds *z_threshold* in absolute value.

        Returns a list of anomaly dicts with the data point and its z-score.
        """
        rows = self._db.fetchall(
            """SELECT * FROM kpi_values
               WHERE department = ? AND kpi_key = ?
               ORDER BY timestamp DESC
               LIMIT ?""",
            (department, kpi_key, window),
        )

        if len(rows) < 3:
            return []

        values = [r["current_value"] for r in rows]
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = math.sqrt(variance) if variance > 0 else 0

        if std == 0:
            return []

        anomalies: list[dict[str, Any]] = []
        for row in reversed(rows):  # chronological order
            z_score = (row["current_value"] - mean) / std
            if abs(z_score) > z_threshold:
                anomalies.append({
                    "timestamp": row["timestamp"],
                    "value": row["current_value"],
                    "z_score": round(z_score, 4),
                    "mean": round(mean, 4),
                    "std": round(std, 4),
                    "direction": "high" if z_score > 0 else "low",
                })

        return anomalies

    def detect_anomalies_all(
        self,
        *,
        z_threshold: float = 2.0,
        days: int = 30,
    ) -> list[dict[str, Any]]:
        """Run anomaly detection across all departments and KPI keys."""
        results: list[dict[str, Any]] = []
        for dept in self.list_departments():
            for kpi_key in self.list_kpi_keys(dept):
                anomalies = self.detect_anomalies(
                    dept, kpi_key, z_threshold=z_threshold, window=days
                )
                for a in anomalies:
                    a["department"] = dept
                    a["kpi_key"] = kpi_key
                results.extend(anomalies)
        return results

    def moving_average_anomaly(
        self,
        department: str,
        kpi_key: str,
        *,
        lookback: int = 5,
        deviation_pct: float = 25.0,
        window: int = 30,
    ) -> list[dict[str, Any]]:
        """Detect anomalies using a simple moving average.

        Flags data points that deviate more than *deviation_pct*% from
        the rolling average of the preceding *lookback* points.
        """
        rows = self._db.fetchall(
            """SELECT * FROM kpi_values
               WHERE department = ? AND kpi_key = ?
               ORDER BY timestamp ASC
               LIMIT ?""",
            (department, kpi_key, window),
        )

        if len(rows) < lookback + 1:
            return []

        anomalies: list[dict[str, Any]] = []
        values = [r["current_value"] for r in rows]

        for i in range(lookback, len(values)):
            window_values = values[i - lookback : i]
            avg = sum(window_values) / len(window_values)
            if avg == 0:
                continue

            deviation = abs(values[i] - avg) / avg * 100
            if deviation > deviation_pct:
                anomalies.append({
                    "timestamp": rows[i]["timestamp"],
                    "value": values[i],
                    "moving_average": round(avg, 4),
                    "deviation_pct": round(deviation, 2),
                    "direction": "high" if values[i] > avg else "low",
                })

        return anomalies

    # ── Trend analysis ────────────────────────────────────────────────

    def get_trend(
        self,
        department: str,
        kpi_key: str,
        *,
        period_minutes: int = 60,
    ) -> dict[str, Any] | None:
        """Compare current vs previous snapshot for a KPI.

        Returns a trend dict with direction, absolute and percentage changes.
        """
        rows = self._db.fetchall(
            """SELECT * FROM kpi_values
               WHERE department = ? AND kpi_key = ?
               ORDER BY timestamp DESC
               LIMIT 2""",
            (department, kpi_key),
        )

        if len(rows) < 2:
            return None

        current = rows[0]
        previous = rows[1]

        abs_change = current["current_value"] - previous["current_value"]
        pct_change = (
            round((abs_change / previous["current_value"]) * 100, 2)
            if previous["current_value"] != 0
            else None
        )

        if abs_change > 0:
            direction = "up"
        elif abs_change < 0:
            direction = "down"
        else:
            direction = "flat"

        return {
            "kpi_key": kpi_key,
            "department": department,
            "current_value": current["current_value"],
            "previous_value": previous["current_value"],
            "absolute_change": round(abs_change, 4),
            "percentage_change": pct_change,
            "direction": direction,
            "unit": current.get("unit", ""),
        }

    # ── Migration ─────────────────────────────────────────────────────

    def import_from_ndjson(self, department: str, ndjson_path: str | Path) -> int:
        """Import KPI history from a legacy ``*_history.ndjson`` file.

        Returns the number of entries imported.
        """
        path = Path(ndjson_path)
        if not path.exists():
            logger.warning("Legacy KPI history file not found: %s", path)
            return 0

        count = 0
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    self.ingest_individual(
                        department=department,
                        kpi_key=data.get("kpi_key", ""),
                        current_value=float(data.get("current", 0)),
                        target_value=float(data["target"]) if data.get("target") is not None else None,
                        unit=data.get("unit", ""),
                        status=data.get("status", "info"),
                        timestamp=data.get("timestamp", ""),
                    )
                    count += 1
                except (json.JSONDecodeError, KeyError, ValueError) as exc:
                    logger.warning("Skipping malformed KPI history line: %s", exc)

        logger.info("Imported %d KPI entries for %s from %s", count, department, path)
        return count

    # ── Stats ─────────────────────────────────────────────────────────

    def total_entries(self) -> int:
        """Return the total number of KPI data points stored."""
        return self._db.table_count("kpi_values")

    def entries_by_department(self) -> dict[str, int]:
        """Return entry counts per department."""
        rows = self._db.fetchall(
            "SELECT department, COUNT(*) as cnt FROM kpi_values GROUP BY department"
        )
        return {r["department"]: r["cnt"] for r in rows}

    # ── Export ────────────────────────────────────────────────────────

    def export_to_ndjson(self, department: str, ndjson_path: str | Path) -> Path:
        """Export KPI history for a department to legacy NDJSON format.

        Returns the path of the written file.
        """
        path = Path(ndjson_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        rows = self._db.fetchall(
            """SELECT * FROM kpi_values
               WHERE department = ?
               ORDER BY timestamp ASC""",
            (department,),
        )

        with open(path, "w", encoding="utf-8") as fh:
            for row in rows:
                record = {
                    "timestamp": row["timestamp"],
                    "kpi_key": row["kpi_key"],
                    "current": row["current_value"],
                    "target": row["target_value"],
                    "unit": row["unit"],
                    "status": row["status"],
                }
                fh.write(json.dumps(record, default=str) + "\n")

        logger.info("Exported %d KPI entries for %s to %s", len(rows), department, path)
        return path

    def export_all_departments_ndjson(self, base_dir: str | Path) -> int:
        """Export all departments to individual NDJSON files.

        Returns the total number of entries exported.
        """
        base = Path(base_dir)
        base.mkdir(parents=True, exist_ok=True)
        total = 0

        for dept in self.list_departments():
            path = base / f"{dept}_history.ndjson"
            self.export_to_ndjson(dept, path)
            rows = self._db.fetchall(
                "SELECT COUNT(*) as cnt FROM kpi_values WHERE department = ?",
                (dept,),
            )
            total += rows[0]["cnt"] if rows else 0

        return total
