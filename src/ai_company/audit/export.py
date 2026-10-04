"""
Audit database export job for evidence separation.

Exports the audit database (audit/audit.db) to JSONL format in
reports/evidence/audit-<date>.jsonl for auditor read-only access.

See AGENTS.md §9.3 Audit Evidence Separation.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


def export_audit_log(
    db_path: str = "audit/audit.db",
    output_dir: str = "reports/evidence",
    date: str | None = None,
) -> int:
    """
    Export the audit_log table to JSONL format.

    Args:
        db_path: Path to the SQLite audit database.
        output_dir: Directory to write the export file.
        date: Date string for the export file (YYYY-MM-DD). Defaults to today.

    Returns:
        Number of records exported.
    """
    db = Path(db_path)
    if not db.exists():
        logger.warning("Audit database not found at %s", db_path)
        return 0

    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    output_path = Path(output_dir) / f"audit-{date}.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    exported = 0

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Export audit_log table
        cursor.execute("""
            SELECT rowid, event_id, event_type, timestamp, actor,
                   correlation_id, details, payload_hash, prev_hash
            FROM audit_log
            ORDER BY timestamp ASC
        """)

        with open(output_path, "w", encoding="utf-8") as f:
            for row in cursor:
                record = dict(row)
                # Convert rowid to string for JSON
                record["rowid"] = str(record["rowid"])
                # Ensure timestamp is ISO format
                ts = record.get("timestamp")
                if isinstance(ts, (int, float)):
                    record["timestamp"] = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
                line = json.dumps(record, separators=(",", ":"))
                f.write(line + "\n")
                exported += 1

        logger.info("Exported %d audit log records to %s", exported, output_path)

    return exported


def export_audit_log_for_date_range(
    db_path: str = "audit/audit.db",
    output_dir: str = "reports/evidence",
    start_date: str | None = None,
    end_date: str | None = None,
) -> int:
    """
    Export audit log records for a specific date range.

    Args:
        db_path: Path to the SQLite audit database.
        output_dir: Directory to write the export file.
        start_date: Start date (YYYY-MM-DD). If None, exports from beginning.
        end_date: End date (YYYY-MM-DD). If None, exports to now.

    Returns:
        Number of records exported.
    """
    db = Path(db_path)
    if not db.exists():
        logger.warning("Audit database not found at %s", db_path)
        return 0

    if start_date is None:
        start_date = "2000-01-01"
    if end_date is None:
        end_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    output_file = f"audit-{start_date}_to_{end_date}.jsonl"
    output_path = Path(output_dir) / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    exported = 0

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT rowid, event_id, event_type, timestamp, actor,
                   correlation_id, details, payload_hash, prev_hash
            FROM audit_log
            WHERE date(timestamp) BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """,
            (start_date, end_date),
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            for row in cursor:
                record = dict(row)
                record["rowid"] = str(record["rowid"])
                ts = record.get("timestamp")
                if isinstance(ts, (int, float)):
                    record["timestamp"] = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
                line = json.dumps(record, separators=(",", ":"))
                f.write(line + "\n")
                exported += 1

        logger.info(
            "Exported %d audit log records to %s",
            exported,
            output_dir + f"/audit-{start_date}_to_{end_date}.jsonl",
        )

    return exported


def export_all_tables(
    db_path: str = "audit/audit.db",
    output_dir: str = "reports/evidence",
    date: str | None = None,
) -> dict[str, int]:
    """
    Export all tables in the audit database to separate JSONL files.

    Returns:
        Dictionary mapping table names to record counts.
    """
    db = Path(db_path)
    if not db.exists():
        logger.warning("Audit database not found at %s", db_path)
        return {}

    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    results: dict[str, int] = {}

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Get all tables
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = [str(row[0]) for row in cursor.fetchall()]

        for table in tables:
            if table in (
                "sqlite_sequence",
                "audit_fts",
                "audit_fts_data",
                "audit_fts_idx",
                "audit_fts_docsize",
                "audit_fts_config",
            ):
                continue  # Skip internal/FTS tables

            cursor.execute(f"SELECT * FROM {table} ORDER BY rowid ASC")
            col_names = [desc[0] for desc in cursor.description or ()]

            output_file = f"{table}-{date}.jsonl"
            output_path = Path(output_dir) / output_file

            exported = 0
            with open(output_path, "w", encoding="utf-8") as f:
                for row in cursor:
                    record = dict(zip(col_names, row, strict=True))
                    # Make values JSON-safe: blob columns become hex, rowid a string
                    for k, v in record.items():
                        if isinstance(v, bytes):
                            record[k] = v.hex()
                        elif k == "rowid":
                            record[k] = str(v)
                    line = json.dumps(record, separators=(",", ":"), default=str)
                    f.write(line + "\n")
                    exported += 1

            results[table] = exported
            logger.info("Exported %d records from %s to %s", exported, table, output_file)

    return results


def main() -> None:
    """CLI entry point for manual export."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Export audit database to JSONL for evidence separation"
    )
    parser.add_argument("--db", default="audit/audit.db", help="Path to audit database")
    parser.add_argument("--output", default="reports/evidence", help="Output directory")
    parser.add_argument("--date", help="Date string (YYYY-MM-DD), defaults to today")
    parser.add_argument("--all-tables", action="store_true", help="Export all tables")
    parser.add_argument("--start-date", help="Start date for range export (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date for range export (YYYY-MM-DD)")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if args.all_tables:
        results = export_all_tables(args.db, args.output, args.date)
        print(f"Exported: {results}")
    elif args.start_date and args.end_date:
        count = export_audit_log_for_date_range(
            args.db, args.output, args.start_date, args.end_date
        )
        print(f"Exported {count} records")
    else:
        count = export_audit_log(args.db, args.output, args.date)
        print(f"Exported {count} records")


if __name__ == "__main__":
    main()
