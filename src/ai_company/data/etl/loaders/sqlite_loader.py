"""ETL Loaders.

Loaders for writing transformed data to targets (SQLite, files, etc.).
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai_company.data.database import Database
from ai_company.data.etl.base import Loader, LoadResult

logger = logging.getLogger(__name__)


class SQLiteUpsertLoader(Loader[dict[str, Any]]):
    """Generic SQLite upsert loader for any table."""

    def __init__(
        self,
        database: Database,
        table: str,
        primary_keys: list[str],
        target_name: str | None = None,
        json_columns: list[str] | None = None,
    ):
        super().__init__(target_name or f"sqlite:{table}", database)
        self.table = table
        self.primary_keys = primary_keys
        self.json_columns = set(json_columns or [])

    def _serialize_record(self, record: dict[str, Any]) -> dict[str, Any]:
        """Serialize dict/list values to JSON strings for configured columns."""
        result = {}
        for k, v in record.items():
            if k in self.json_columns and isinstance(v, (dict, list)):
                result[k] = json.dumps(v, default=str)
            else:
                result[k] = v
        return result

    def load(self, records: list[dict[str, Any]], **kwargs: Any) -> LoadResult:
        """Upsert records into SQLite table.

        Args:
            records: List of record dicts
            **kwargs: Additional options (batch_size, conflict_action)

        Returns:
            LoadResult with counts
        """
        assert self.database is not None
        if not records:
            return LoadResult(loaded_count=0, target=self.target_name)

        batch_size = kwargs.get("batch_size", 1000)
        loaded = 0
        failed = 0
        errors: list[str] = []

        # Build upsert SQL
        columns = list(records[0].keys())
        placeholders = ", ".join("?" for _ in columns)
        col_list = ", ".join(columns)

        # ON CONFLICT DO UPDATE SET ...
        pk_cols = ", ".join(self.primary_keys)
        update_cols = [c for c in columns if c not in self.primary_keys]
        update_clause = ", ".join(f"{c} = excluded.{c}" for c in update_cols)

        sql = f"""
            INSERT INTO {self.table} ({col_list})
            VALUES ({placeholders})
            ON CONFLICT({pk_cols}) DO UPDATE SET {update_clause}
        """

        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            try:
                params = [tuple(self._serialize_record(r).get(c) for c in columns) for r in batch]
                self.database.executemany(sql, params)
                self.database.commit()
                loaded += len(batch)
            except Exception as exc:  # noqa: BLE001
                logger.error("Batch upsert failed for %s: %s", self.table, exc)
                failed += len(batch)
                errors.append(str(exc))

        return LoadResult(
            loaded_count=loaded,
            failed_count=failed,
            target=self.target_name,
            errors=errors,
        )


class KPIValueLoader(SQLiteUpsertLoader):
    """Loader for kpi_values table with composite key."""

    def __init__(self, database: Database):
        super().__init__(
            database,
            "kpi_values",
            primary_keys=["department", "kpi_key", "timestamp"],
            target_name="sqlite:kpi_values",
        )

    def load(self, records: list[dict[str, Any]], **kwargs: Any) -> LoadResult:
        # kpi_values uses auto-increment id, so we don't include it in upsert
        # The composite unique key is (department, kpi_key, timestamp)
        return super().load(records, **kwargs)


class CostRecordLoader(SQLiteUpsertLoader):
    """Loader for cost_records table."""

    def __init__(self, database: Database):
        super().__init__(
            database,
            "cost_records",
            primary_keys=["id"],
            target_name="sqlite:cost_records",
        )

    def load(self, records: list[dict[str, Any]], **kwargs: Any) -> LoadResult:
        # cost_records has auto-increment id, use INSERT only (no upsert on PK)
        # For idempotency, we check for exact duplicates before insert
        return self._load_with_dedup(records, **kwargs)

    def _load_with_dedup(self, records: list[dict[str, Any]], **kwargs: Any) -> LoadResult:
        """Insert with duplicate detection on natural key."""
        assert self.database is not None
        if not records:
            return LoadResult(loaded_count=0, target=self.target_name)

        batch_size = kwargs.get("batch_size", 1000)
        loaded = 0
        failed = 0
        skipped = 0
        errors: list[str] = []

        # Natural key for deduplication
        nat_key_cols = ["timestamp", "model", "provider", "agent_name", "task_id", "cost_usd", "prompt_tokens", "completion_tokens"]

        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            for record in batch:
                try:
                    # Check if exists
                    where_clauses = [f"{col} = ?" for col in nat_key_cols]
                    params = [record.get(col) for col in nat_key_cols]
                    existing = self.database.fetchone(
                        f"SELECT 1 FROM {self.table} WHERE {' AND '.join(where_clauses)} LIMIT 1",
                        tuple(params),
                    )
                    if existing:
                        skipped += 1
                        continue

                    # Insert
                    columns = [c for c in record if c != "id"]
                    placeholders = ", ".join("?" for _ in columns)
                    col_list = ", ".join(columns)
                    sql = f"INSERT INTO {self.table} ({col_list}) VALUES ({placeholders})"
                    self.database.execute(sql, tuple(record[c] for c in columns))
                    loaded += 1
                except Exception as exc:  # noqa: BLE001
                    logger.error("Cost record insert failed: %s", exc)
                    failed += 1
                    errors.append(str(exc))

            self.database.commit()

        return LoadResult(
            loaded_count=loaded,
            failed_count=failed,
            skipped_count=skipped,
            target=self.target_name,
            errors=errors,
        )


class CostAggregationLoader(SQLiteUpsertLoader):
    """Loader for cost_aggregations table."""

    def __init__(self, database: Database):
        super().__init__(
            database,
            "cost_aggregations",
            primary_keys=["period", "period_key"],
            target_name="sqlite:cost_aggregations",
            json_columns=["by_model", "by_agent"],
        )


class AgentPerformanceMetricsLoader(SQLiteUpsertLoader):
    """Loader for agent_performance_metrics table."""

    def __init__(self, database: Database):
        super().__init__(
            database,
            "agent_performance_metrics",
            primary_keys=["agent_id", "period_days", "period_start"],
            target_name="sqlite:agent_performance_metrics",
            json_columns=["sent_by_status", "received_by_status", "audit_events", "tool_usage"],
        )


class FileLoader(Loader[dict[str, Any]]):
    """Base class for file-based loaders."""

    def __init__(self, target_name: str, output_dir: Path, file_prefix: str):
        super().__init__(target_name, database=None)
        self.output_dir = output_dir
        self.file_prefix = file_prefix
        self.output_dir.mkdir(parents=True, exist_ok=True)


class NDJSONLoader(FileLoader):
    """Loader for NDJSON (newline-delimited JSON) files."""

    def load(self, records: list[dict[str, Any]], **kwargs: Any) -> LoadResult:
        """Write records as NDJSON file."""
        if not records:
            return LoadResult(loaded_count=0, target=self.target_name)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"{self.file_prefix}_{timestamp}.ndjson"
        filepath = self.output_dir / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                for record in records:
                    f.write(json.dumps(record, default=str) + "\n")

            return LoadResult(
                loaded_count=len(records),
                target=f"file:{filepath}",
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("NDJSON write failed: %s", exc)
            return LoadResult(
                loaded_count=0,
                failed_count=len(records),
                target=f"file:{filepath}",
                errors=[str(exc)],
            )


class JSONLoader(FileLoader):
    """Loader for JSON array files."""

    def load(self, records: list[dict[str, Any]], **kwargs: Any) -> LoadResult:
        """Write records as JSON array file."""
        if not records:
            return LoadResult(loaded_count=0, target=self.target_name)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"{self.file_prefix}_{timestamp}.json"
        filepath = self.output_dir / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, default=str)

            return LoadResult(
                loaded_count=len(records),
                target=f"file:{filepath}",
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("JSON write failed: %s", exc)
            return LoadResult(
                loaded_count=0,
                failed_count=len(records),
                target=f"file:{filepath}",
                errors=[str(exc)],
            )


__all__ = [
    "SQLiteUpsertLoader",
    "KPIValueLoader",
    "CostRecordLoader",
    "CostAggregationLoader",
    "AgentPerformanceMetricsLoader",
    "FileLoader",
    "NDJSONLoader",
    "JSONLoader",
]
