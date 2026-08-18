"""SQLite Table Extractors.

Extractors for reading from the SQLite data layer tables.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from ai_company.data.database import Database
from ai_company.data.etl.base import ExtractionResult, Extractor

logger = logging.getLogger(__name__)


class SQLiteTableExtractor(Extractor[dict[str, Any]]):
    """Generic extractor for any SQLite table with timestamp column."""

    _TIMESTAMP_COLUMNS = {
        "tasks": "created_at",
        "audit_events": "timestamp",
        "memory_entries": "created_at",
        "escalation_events": "timestamp",
        "kpi_values": "timestamp",
        "cost_records": "timestamp",
    }

    def __init__(
        self,
        database: Database,
        table: str,
        timestamp_column: str | None = None,
    ):
        super().__init__(source_name=f"sqlite:{table}", database=database)
        self.table = table
        self.timestamp_column = timestamp_column or self._TIMESTAMP_COLUMNS.get(table, "created_at")

    def extract(
        self,
        since: str | None = None,
        limit: int | None = None,
        columns: list[str] | None = None,
        where: str | None = None,
        params: tuple[Any, ...] = (),
        **kwargs: Any,
    ) -> ExtractionResult[dict[str, Any]]:
        """Extract records from a SQLite table.

        Args:
            since: ISO timestamp for incremental extraction
            limit: Maximum records to return
            columns: Specific columns to select (default: all)
            where: Additional WHERE clause (without WHERE keyword)
            params: Parameters for the WHERE clause

        Returns:
            ExtractionResult with records
        """
        assert self.database is not None
        col_sql = ", ".join(columns) if columns else "*"

        conditions = []
        query_params: list[Any] = list(params)

        if since:
            conditions.append(f"{self.timestamp_column} >= ?")
            query_params.append(since)

        if where:
            conditions.append(where)

        where_sql = " WHERE " + " AND ".join(conditions) if conditions else ""
        limit_sql = f" LIMIT {limit}" if limit else ""

        sql = f"SELECT {col_sql} FROM {self.table}{where_sql} ORDER BY {self.timestamp_column} ASC{limit_sql}"

        try:
            rows = self.database.fetchall(sql, tuple(query_params))
            return ExtractionResult(
                records=rows,
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("Extraction failed for %s: %s", self.table, exc)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[str(exc)],
            )

    def extract_new_since_last_run(self, last_run_ts: str, batch_size: int = 1000) -> ExtractionResult[dict[str, Any]]:
        """Convenience method for incremental extraction since last pipeline run."""
        return self.extract(since=last_run_ts, limit=batch_size)


class TaskExtractor(SQLiteTableExtractor):
    """Extractor for tasks table with task-specific filters."""

    def __init__(self, database: Database):
        super().__init__(database, "tasks", "created_at")

    def extract_by_status(
        self,
        status: str,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="status = ?", params=(status,))

    def extract_by_receiver(
        self,
        receiver_id: str,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="receiver_id = ?", params=(receiver_id,))

    def extract_by_sender(
        self,
        sender_id: str,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="sender_id = ?", params=(sender_id,))

    def extract_completed_failed(
        self,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(
            since=since, limit=limit, where="status IN ('completed', 'failed')", params=()
        )


class AuditEventExtractor(SQLiteTableExtractor):
    """Extractor for audit_events table."""

    def __init__(self, database: Database):
        super().__init__(database, "audit_events", "timestamp")

    def extract_by_agent(
        self,
        agent_id: str,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="agent_id = ?", params=(agent_id,))

    def extract_by_type(
        self,
        event_type: str,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="event_type = ?", params=(event_type,))

    def extract_errors(
        self,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(
            since=since,
            limit=limit,
            where="event_type = 'error' OR severity IN ('error', 'critical')",
        )


class CostRecordExtractor(SQLiteTableExtractor):
    """Extractor for cost_records table."""

    def __init__(self, database: Database):
        super().__init__(database, "cost_records", "timestamp")

    def extract_by_agent(
        self,
        agent_name: str,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="agent_name = ?", params=(agent_name,))

    def extract_by_task(
        self,
        task_id: str,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(where="task_id = ?", params=(task_id,))

    def extract_by_model(
        self,
        model: str,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="model = ?", params=(model,))

    def extract_daily_aggregation(self, day: str) -> ExtractionResult[dict[str, Any]]:
        """Extract pre-aggregated daily cost summary."""
        assert self.database is not None
        sql = """
            SELECT
                date(timestamp) as day,
                model,
                SUM(cost_usd) as cost_usd,
                SUM(prompt_tokens) as prompt_tokens,
                SUM(completion_tokens) as completion_tokens,
                COUNT(*) as calls
            FROM cost_records
            WHERE date(timestamp) = ?
            GROUP BY day, model
        """
        try:
            rows = self.database.fetchall(sql, (day,))
            return ExtractionResult(
                records=rows,
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("Daily cost aggregation failed: %s", exc)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[str(exc)],
            )


class KPIValueExtractor(SQLiteTableExtractor):
    """Extractor for kpi_values table."""

    def __init__(self, database: Database):
        super().__init__(database, "kpi_values", "timestamp")

    def extract_by_department(
        self,
        department: str,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="department = ?", params=(department,))

    def extract_by_kpi(
        self,
        department: str,
        kpi_key: str,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(
            since=since,
            limit=limit,
            where="department = ? AND kpi_key = ?",
            params=(department, kpi_key),
        )

    def extract_latest_snapshot(self, department: str) -> ExtractionResult[dict[str, Any]]:
        """Get the most recent KPI snapshot for a department."""
        assert self.database is not None
        sql = """
            SELECT * FROM kpi_values
            WHERE department = ? AND timestamp = (
                SELECT MAX(timestamp) FROM kpi_values WHERE department = ?
            )
        """
        try:
            rows = self.database.fetchall(sql, (department, department))
            return ExtractionResult(
                records=rows,
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("Latest KPI snapshot extraction failed: %s", exc)
            return ExtractionResult(
                records=[],
                source=self.source_name,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                errors=[str(exc)],
            )


class EscalationEventExtractor(SQLiteTableExtractor):
    """Extractor for escalation_events table."""

    def __init__(self, database: Database):
        super().__init__(database, "escalation_events", "timestamp")

    def extract_pending(self, since: str | None = None, limit: int | None = None) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="resolved = 0")

    def extract_resolved(self, since: str | None = None, limit: int | None = None) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="resolved = 1")

    def extract_by_target_agent(
        self,
        to_agent: str,
        since: str | None = None,
        limit: int | None = None,
    ) -> ExtractionResult[dict[str, Any]]:
        return self.extract(since=since, limit=limit, where="to_agent = ?", params=(to_agent,))


__all__ = [
    "SQLiteTableExtractor",
    "TaskExtractor",
    "AuditEventExtractor",
    "CostRecordExtractor",
    "KPIValueExtractor",
    "EscalationEventExtractor",
]