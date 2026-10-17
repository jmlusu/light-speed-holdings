"""
Audit evidence export job for evidence separation.

Default mode streams the canonical AuditWriter JSONL trail
(``.opencode/audit/audit.jsonl`` + rotated siblings) to
``reports/evidence/audit-<date>.jsonl`` for auditor read-only access.

``--db`` selects the legacy SQLite exporters (``audit/audit.db``) which remain
for explicit back-compat only; the decoy database is no longer the source of
truth and is untracked.

See AGENTS.md §9.3 Audit Evidence Separation.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from ai_company.audit.integrity import ordered_audit_files
from ai_company.paths import get_audit_path

logger = logging.getLogger(__name__)


def export_audit_trail(
    path: str | Path | None = None,
    output_dir: str = "reports/evidence",
    date: str | None = None,
) -> int:
    """Export one UTC date's events from the canonical AuditWriter trail.

    Args:
        path: Trail file. Defaults to ``get_audit_path()``. The active file
            and its rotated siblings are both read (oldest → newest).
        output_dir: Directory to write the export file.
        date: UTC date (YYYY-MM-DD). Defaults to today (UTC).

    Returns:
        Number of events exported. Zero means a quiet day: no output file is
        written.

    Raises:
        FileNotFoundError: The trail (and any rotated files) does not exist.
        ValueError: *date* is not a valid ``YYYY-MM-DD`` string.
    """
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    else:
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date().isoformat()
        except ValueError as exc:
            raise ValueError(f"Invalid date {date!r}, expected YYYY-MM-DD") from exc

    root = Path(path) if path is not None else get_audit_path()
    files = ordered_audit_files(root)
    if not files and not root.exists():
        raise FileNotFoundError(f"Audit trail not found: {root}")

    matched: list[str] = []
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as fh:
            for raw in fh:
                if not raw.strip():
                    continue
                try:
                    record = json.loads(raw)
                except json.JSONDecodeError:
                    logger.warning("Skipping malformed line in %s", fpath.name)
                    continue
                if not isinstance(record, dict):
                    continue
                ts = record.get("timestamp")
                if not isinstance(ts, str):
                    logger.warning("Skipping line without timestamp in %s", fpath.name)
                    continue
                try:
                    event = datetime.fromisoformat(ts)
                except ValueError:
                    logger.warning("Skipping unparseable timestamp %r in %s", ts, fpath.name)
                    continue
                if event.tzinfo is not None:
                    event = event.astimezone(timezone.utc)
                if event.date().isoformat() != date:
                    continue
                matched.append(raw if raw.endswith("\n") else raw + "\n")

    if not matched:
        logger.info("0 events for %s; no export file written", date)
        return 0

    output_path = Path(output_dir) / f"audit-{date}.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.writelines(matched)
    logger.info("Exported %d audit trail events to %s", len(matched), output_path)
    return len(matched)


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
    """CLI entry point for manual export.

    Default mode streams the canonical JSONL trail for one UTC date.
    ``--db`` selects the legacy SQLite exporters for back-compat.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Export audit evidence to JSONL for evidence separation"
    )
    parser.add_argument(
        "--db",
        default=None,
        help="Legacy SQLite audit database (default: canonical JSONL trail)",
    )
    parser.add_argument("--output", default="reports/evidence", help="Output directory")
    parser.add_argument("--date", help="Date string (YYYY-MM-DD), defaults to today (UTC)")
    parser.add_argument(
        "--all-tables", action="store_true", help="Export all tables (requires --db)"
    )
    parser.add_argument(
        "--start-date", help="Start date for range export (YYYY-MM-DD), requires --db"
    )
    parser.add_argument("--end-date", help="End date for range export (YYYY-MM-DD), requires --db")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if args.db is None:
        if args.all_tables or args.start_date or args.end_date:
            parser.error("--all-tables/--start-date/--end-date require --db")
        try:
            count = export_audit_trail(path=None, output_dir=args.output, date=args.date)
        except (FileNotFoundError, ValueError) as exc:
            logger.error("%s", exc)
            raise SystemExit(1) from exc
        print(f"Exported {count} records")
        return

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
