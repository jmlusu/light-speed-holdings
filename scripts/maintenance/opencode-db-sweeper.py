#!/usr/bin/env python3
"""Orphan sweeper for opencode.db tool-call rows (P0-3).

Marks rows stuck in ``running`` (>1 h) or ``pending`` (>24 h) as ``error``
with ``$.state.orphaned = 1``, mirroring the HITL expiry-sweep pattern
(plan: reports/opencode-db-reliability-fix-2026-11-08.md section 4).

    python scripts/maintenance/opencode-db-sweeper.py                  # dry-run
    python scripts/maintenance/opencode-db-sweeper.py --apply          # apply
    python scripts/maintenance/opencode-db-sweeper.py --db <path> --dry-run --json

Design:
    - DRY-RUN IS THE DEFAULT. ``--apply`` is required for any UPDATE.
    - Dry-run opens the DB read-only (``mode=ro`` URI + ``query_only``)
      and only runs SELECTs; it cannot write even if asked to.
    - Apply runs in a single ``BEGIN IMMEDIATE`` transaction, preserves
      ``state.input``/``state.output``/timestamps, only flips
      ``state.status`` + appends ``state.error`` + sets
      ``state.orphaned = 1`` + bumps ``time_updated``. Never DELETEs rows.
    - Uses ``json_set`` (not string REPLACE): key order is not guaranteed.

Baseline (reports/opencode-db-audit-2026-11-08.md): running 93, pending 2.
All 93 running rows predate the audit by days/weeks, so the 1 h TTL cannot
flip a still-executing call in practice. Apply only in a maintenance window
with writers stopped + a fresh snapshot (see opencode-db-maintenance.ps1).
"""

from __future__ import annotations

import argparse
import contextlib
import json
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = str(Path.home() / ".local" / "share" / "opencode" / "opencode.db")
RUNNING_TTL_SECONDS = 3600  # 1 h
PENDING_TTL_SECONDS = 86400  # 24 h

BREAKDOWN_SQL = """
SELECT json_extract(data,'$.tool') AS tool,
       json_extract(data,'$.state.status') AS status,
       COUNT(*) AS n,
       MIN(datetime(time_created/1000,'unixepoch','localtime')) AS oldest,
       MAX(datetime(time_created/1000,'unixepoch','localtime')) AS newest
FROM part
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status') IN ('running','pending')
GROUP BY tool, status
ORDER BY n DESC
"""

RUNNING_STALE_SQL = """
SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status')='running'
  AND (COALESCE(time_updated, time_created) < (strftime('%s','now') - ?) * 1000)
"""

PENDING_STALE_SQL = """
SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status')='pending'
  AND (COALESCE(time_updated, time_created) < (strftime('%s','now') - ?) * 1000)
"""

STATUS_SQL = """
SELECT json_extract(data,'$.state.status') AS st, COUNT(*)
FROM part WHERE json_extract(data,'$.type')='tool' GROUP BY st
"""

UPDATE_RUNNING_SQL = """
UPDATE part
SET data = json_set(
             data,
             '$.state.status', 'error',
             '$.state.error', 'orphaned: running exceeded '
                 || (? / 3600) || 'h without terminal update '
                 || '(orphan sweeper ' || date('now') || ')',
             '$.state.orphaned', 1
           ),
    time_updated = (strftime('%s','now') * 1000)
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status')='running'
  AND (COALESCE(time_updated, time_created) < (strftime('%s','now') - ?) * 1000)
"""

UPDATE_PENDING_SQL = """
UPDATE part
SET data = json_set(
             data,
             '$.state.status', 'error',
             '$.state.error', 'orphaned: pending exceeded 24h '
                 || '(orphan sweeper ' || date('now') || ')',
             '$.state.orphaned', 1
           ),
    time_updated = (strftime('%s','now') * 1000)
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status')='pending'
  AND (COALESCE(time_updated, time_created) < (strftime('%s','now') - ?) * 1000)
"""


def connect_readonly(db_path: str) -> sqlite3.Connection:
    """Read-only connection: URI mode=ro + query_only (defence in depth)."""
    # Windows sqlite URIs need forward slashes (file:C:/path?mode=ro).
    uri_path = db_path.replace("\\", "/")
    uri = f"file:{uri_path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    with contextlib.suppress(sqlite3.Error):
        conn.execute("PRAGMA query_only=1;")
    return conn


def dry_run(db_path: str, running_ttl: int, pending_ttl: int) -> dict:
    conn = connect_readonly(db_path)
    try:
        breakdown = conn.execute(BREAKDOWN_SQL).fetchall()
        running_stale = conn.execute(RUNNING_STALE_SQL, (running_ttl,)).fetchone()[0]
        pending_stale = conn.execute(PENDING_STALE_SQL, (pending_ttl,)).fetchone()[0]
        statuses = conn.execute(STATUS_SQL).fetchall()
    finally:
        conn.close()
    return {
        "mode": "dry-run",
        "running_stale": running_stale,
        "pending_stale": pending_stale,
        "would_update": running_stale + pending_stale,
        "breakdown": [
            {"tool": t, "status": s, "n": n, "oldest": o, "newest": ne}
            for t, s, n, o, ne in breakdown
        ],
        "status_totals": [{"status": s, "n": n} for s, n in statuses],
    }


def apply(db_path: str, running_ttl: int, pending_ttl: int) -> dict:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE;")
        # RUNNING takes (shown_hours, filter_seconds): both are the TTL. The
        # message renders `? / 3600` as the hour count. PENDING takes one
        # param (filter only; "24h" is hardcoded in prose).
        cur = conn.execute(UPDATE_RUNNING_SQL, (running_ttl, running_ttl))
        running_rows = cur.rowcount
        cur = conn.execute(UPDATE_PENDING_SQL, (pending_ttl,))
        pending_rows = cur.rowcount
        conn.execute("COMMIT;")
        statuses = conn.execute(STATUS_SQL).fetchall()
        integrity = conn.execute("PRAGMA integrity_check;").fetchone()[0]
    finally:
        conn.close()
    return {
        "mode": "apply",
        "running_updated": running_rows,
        "pending_updated": pending_rows,
        "status_totals": [{"status": s, "n": n} for s, n in statuses],
        "integrity_check": integrity,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=DEFAULT_DB, help=f"opencode.db path (default: {DEFAULT_DB})")
    ap.add_argument(
        "--running-seconds",
        type=int,
        default=RUNNING_TTL_SECONDS,
        help="running TTL in seconds (default 3600 = 1h)",
    )
    ap.add_argument(
        "--pending-seconds",
        type=int,
        default=PENDING_TTL_SECONDS,
        help="pending TTL in seconds (default 86400 = 24h)",
    )
    ap.add_argument("--dry-run", action="store_true", help="default mode: report only (no writes)")
    ap.add_argument(
        "--apply", action="store_true", help="actually UPDATE (maintenance window only)"
    )
    ap.add_argument("--json", action="store_true", help="emit JSON summary")
    args = ap.parse_args()

    if args.apply and args.dry_run:
        print("error: --apply and --dry-run are mutually exclusive", file=sys.stderr)
        return 2
    if not Path(args.db).exists():
        print(f"error: DB not found: {args.db}", file=sys.stderr)
        return 1

    if args.apply:
        result = apply(args.db, args.running_seconds, args.pending_seconds)
    else:
        result = dry_run(args.db, args.running_seconds, args.pending_seconds)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["mode"] == "dry-run":
            print(
                f"DRY-RUN (read-only): running>{args.running_seconds}s={result['running_stale']} "
                f"pending>{args.pending_seconds}s={result['pending_stale']} "
                f"would_update={result['would_update']}"
            )
            for row in result["breakdown"]:
                print(
                    f"  {row['tool']}/{row['status']}: n={row['n']} oldest={row['oldest']} newest={row['newest']}"
                )
            print(f"  status totals: {result['status_totals']}")
            print(
                "  Re-run with --apply in a maintenance window (writers stopped, snapshot taken) to UPDATE."
            )
        else:
            print(
                f"APPLY: running_updated={result['running_updated']} pending_updated={result['pending_updated']}"
            )
            print(f"  status totals: {result['status_totals']}")
            print(f"  integrity_check: {result['integrity_check']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
