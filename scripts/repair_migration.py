#!/usr/bin/env python3
"""Standalone script to detect and repair a broken database migration.

Checks the current schema version, detects missing tables, re-applies
migrations as needed, and verifies that ``database_is_usable()`` returns
``True`` afterwards.

Usage::

    uv run python scripts/repair_migration.py
    uv run python scripts/repair_migration.py --db-path data/ai_company.db
    uv run python scripts/repair_migration.py --dry-run   # detect only, no writes
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Ensure the project root is on sys.path so imports work when run directly.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from ai_company.data.database import (  # noqa: E402
    _REQUIRED_TABLES,
    SCHEMA_VERSION,
    Database,
    database_is_usable,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def _missing_tables(conn) -> set[str]:
    """Return the set of required tables that do not exist yet."""
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    names = {row["name"] for row in rows}
    return _REQUIRED_TABLES - names


def diagnose(db_path: Path) -> dict:
    """Inspect the database and return a diagnostic snapshot."""
    db = Database(db_path)
    conn = db.connect()
    version = db.get_schema_version()
    missing = _missing_tables(conn)
    usable = database_is_usable(db)
    db.close()
    return {
        "db_path": str(db_path),
        "schema_version": version,
        "target_version": SCHEMA_VERSION,
        "missing_tables": sorted(missing),
        "usable": usable,
    }


def repair(db_path: Path) -> bool:
    """Re-apply missing migrations and return True if the DB is now usable."""
    db = Database(db_path)
    db.init_schema()  # the fixed version handles missing-table detection
    usable = database_is_usable(db)
    db.close()
    return usable


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair a broken database migration.")
    parser.add_argument(
        "--db-path",
        type=Path,
        default=Path("data/ai_company.db"),
        help="Path to the SQLite database (default: data/ai_company.db)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Diagnose only; do not apply any migrations.",
    )
    args = parser.parse_args()

    db_path: Path = args.db_path

    if not db_path.exists():
        logger.error("Database file does not exist: %s", db_path)
        return 1

    # ── Diagnose ──
    info = diagnose(db_path)
    logger.info("Database: %s", info["db_path"])
    logger.info("Schema version: %d / %d", info["schema_version"], info["target_version"])
    if info["missing_tables"]:
        logger.warning("Missing required tables: %s", ", ".join(info["missing_tables"]))
    else:
        logger.info("All required tables present.")

    if info["usable"]:
        logger.info("Database is already usable — nothing to do.")
        return 0

    # ── Repair ──
    if args.dry_run:
        logger.info("Dry-run mode — skipping migration repair.")
        return 1

    logger.info("Repairing migration …")
    ok = repair(db_path)

    # ── Verify ──
    info_after = diagnose(db_path)
    logger.info(
        "Post-repair schema version: %d / %d",
        info_after["schema_version"],
        info_after["target_version"],
    )
    if info_after["missing_tables"]:
        logger.error(
            "Still missing tables after repair: %s", ", ".join(info_after["missing_tables"])
        )

    if ok:
        logger.info("✓ database_is_usable() returned True — repair succeeded.")
        return 0
    else:
        logger.error("✗ database_is_usable() still False — repair failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
