#!/usr/bin/env python3
"""Retention / GC applier for opencode.db (P2/P3 lifecycle).

Covers (plan: reports/opencode-db-reliability-fix-2026-11-08.md
sections 9-11 + this task's retention/GC scope):

    archive   30-day archive via session.time_archived (mark, never delete)
    project   GC of session-less projects (>30d, no sessions in v1/v2 AND
              no permission/worktree/project_directory dependents)
    blob      inline file parts (144) -> blob/blob_ref (idempotent)
    vacuum    VACUUM INTO compact plan (prints steps; never VACUUMs live)

Default is DRY-RUN (read-only SELECTs). ``--apply`` performs UPDATE/INSERT/
DELETE inside a single transaction. Run ``--apply`` only:
    - in a maintenance window with OpenCode writers stopped,
    - with a fresh snapshot taken first (opencode-db-maintenance.ps1),
    - with ``--db`` pointing at the CLONE for the blob migrator's first run
      (verify blob.bytes == decoded length + integrity_check, then re-run
      against the primary).

Blob FK finding (probed 2026-11-08): ``blob_ref.session_id`` FK-references
``session_v2(id)``, but inline file parts live in the v1 ``part`` table
keyed by v1 ``session(id)``. A naive INSERT violates the FK. The migrator
therefore requires either (a) an explicit ``--allow-fk-off`` window
transaction with ``PRAGMA foreign_keys=OFF`` restored to ON after, or
(b) deferral until the v2 writer completion decision (vp_engineering).
Without one of those, ``--apply --mode blob`` refuses with exit 1.

VACUUM note: ``freelist_count ~ 1996`` (~8 MB) so VACUUM alone reclaims
almost nothing; bloat is live pages. The compact path is
archive -> VACUUM INTO new file -> verify -> swap. This script never runs
VACUUM; ``--mode vacuum`` prints the plan + disk pre-flight.

Usage:
    python scripts/maintenance/opencode-db-retention.py [options]
    python scripts/maintenance/opencode-db-retention.py --mode blob --dry-run --json
"""

from __future__ import annotations

import argparse
import base64
import binascii
import contextlib
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = str(Path.home() / ".local" / "share" / "opencode" / "opencode.db")
ARCHIVE_DAYS = 30
PROJECT_GC_DAYS = 30

# ---- SQL: archive -------------------------------------------------------

ARCHIVE_COUNT_SQL = """
SELECT COUNT(*) FROM session
WHERE time_archived IS NULL
  AND time_created < (strftime('%s','now') - ? * 86400) * 1000
"""

ARCHIVE_COUNT_V2_SQL = """
SELECT COUNT(*) FROM session_v2
WHERE time_archived IS NULL
  AND time_created < (strftime('%s','now') - ? * 86400) * 1000
"""

# Chain-closure check: archiving a parent while keeping a child breaks
# parent_id trees. Count children whose parent would be archived but the
# child would not (child kept, parent archived) -- those must be kept too.
CHAIN_BREAK_SQL = """
SELECT COUNT(*) FROM session c
WHERE c.time_archived IS NULL
  AND c.parent_id IS NOT NULL
  AND c.parent_id IN (
      SELECT id FROM session p
      WHERE p.time_archived IS NULL
        AND p.time_created < (strftime('%s','now') - ? * 86400) * 1000
  )
"""

ARCHIVE_UPDATE_V1_SQL = """
UPDATE session SET time_archived = (strftime('%s','now') * 1000)
WHERE time_archived IS NULL
  AND time_created < (strftime('%s','now') - ? * 86400) * 1000
  AND tokens_input <= ?
  -- Never archive a session with a live child (chain closure).
  AND id NOT IN (
      SELECT parent_id FROM session
      WHERE parent_id IS NOT NULL AND time_archived IS NULL
  )
"""

ARCHIVE_UPDATE_V2_SQL = """
UPDATE session_v2 SET time_archived = (strftime('%s','now') * 1000)
WHERE time_archived IS NULL
  AND time_created < (strftime('%s','now') - ? * 86400) * 1000
  AND tokens_input <= ?
  AND id NOT IN (
      SELECT parent_id FROM session_v2
      WHERE parent_id IS NOT NULL AND time_archived IS NULL
  )
"""

ARCHIVE_GUARDED_COUNT_V1_SQL = """
SELECT COUNT(*) FROM session
WHERE time_archived IS NULL
  AND time_created < (strftime('%s','now') - ? * 86400) * 1000
  AND tokens_input <= ?
  AND id NOT IN (
      SELECT parent_id FROM session
      WHERE parent_id IS NOT NULL AND time_archived IS NULL
  )
"""

# ---- SQL: project GC ----------------------------------------------------

PROJECT_DRYRUN_SQL = """
SELECT p.id, p.worktree, p.time_created,
       (SELECT COUNT(*) FROM session s WHERE s.project_id=p.id) AS v1_sessions,
       (SELECT COUNT(*) FROM session_v2 s WHERE s.project_id=p.id) AS v2_sessions,
       (SELECT COUNT(*) FROM permission WHERE project_id=p.id) AS permissions,
       (SELECT COUNT(*) FROM worktree WHERE project_id=p.id) AS worktrees,
       (SELECT COUNT(*) FROM project_directory WHERE project_id=p.id) AS directories
FROM project p
WHERE NOT EXISTS (SELECT 1 FROM session s WHERE s.project_id=p.id)
  AND NOT EXISTS (SELECT 1 FROM session_v2 s WHERE s.project_id=p.id)
ORDER BY p.time_created
"""

PROJECT_DELETE_SQL = """
DELETE FROM project
WHERE NOT EXISTS (SELECT 1 FROM session s WHERE s.project_id=project.id)
  AND NOT EXISTS (SELECT 1 FROM session_v2 s WHERE s.project_id=project.id)
  AND NOT EXISTS (SELECT 1 FROM permission WHERE project_id=project.id)
  AND NOT EXISTS (SELECT 1 FROM worktree WHERE project_id=project.id)
  AND NOT EXISTS (SELECT 1 FROM project_directory WHERE project_id=project.id)
  AND time_created < (strftime('%s','now') - ? * 86400) * 1000
  AND id NOT IN (?,?,?)
"""

# ---- SQL: blob migration ------------------------------------------------

FILE_PARTS_SQL = """
SELECT id, session_id, message_id, time_created, data
FROM part
WHERE json_extract(data,'$.type')='file'
"""

INLINE_URL_PREFIX = "data:"
B64_MARKER = ";base64,"


def connect_readonly(db_path: str) -> sqlite3.Connection:
    uri_path = db_path.replace("\\", "/")
    conn = sqlite3.connect(f"file:{uri_path}?mode=ro", uri=True)
    with contextlib.suppress(sqlite3.Error):
        conn.execute("PRAGMA query_only=1;")
    return conn


def parse_data_url(url: str) -> tuple[str, bytes] | None:
    """Parse ``data:<mime>;base64,<payload>`` -> (mime, bytes) or None."""
    if not url.startswith(INLINE_URL_PREFIX) or B64_MARKER not in url:
        return None
    mime, payload = url[len(INLINE_URL_PREFIX) :].split(B64_MARKER, 1)
    try:
        return mime, base64.b64decode(payload, validate=True)
    except (binascii.Error, ValueError):
        return None


def blob_mode_dryrun(conn: sqlite3.Connection) -> dict:
    rows = conn.execute(FILE_PARTS_SQL).fetchall()
    inline = 0
    external = 0
    unparsable = 0
    distinct_hashes: set[str] = set()
    total_bytes = 0
    for _id, _sess, _msg, _tc, data in rows:
        try:
            kind = json.loads(data).get("url", "")
        except json.JSONDecodeError:
            unparsable += 1
            continue
        parsed = parse_data_url(kind) if isinstance(kind, str) else None
        if parsed is None:
            if isinstance(kind, str) and kind.startswith(("http://", "https://")):
                external += 1
            else:
                unparsable += 1
            continue
        _mime, raw = parsed
        inline += 1
        total_bytes += len(raw)
        distinct_hashes.add(hashlib.sha256(raw).hexdigest())
    blob_count = conn.execute("SELECT COUNT(*) FROM blob;").fetchone()[0]
    blob_ref_count = conn.execute("SELECT COUNT(*) FROM blob_ref;").fetchone()[0]
    return {
        "file_parts": len(rows),
        "inline_base64": inline,
        "external_url": external,
        "unparsable": unparsable,
        "distinct_hashes": len(distinct_hashes),
        "inline_bytes": total_bytes,
        "blob_before": blob_count,
        "blob_ref_before": blob_ref_count,
    }


def blob_mode_apply(conn: sqlite3.Connection, allow_fk_off: bool) -> dict:
    """Idempotent migrator: file part -> blob row + blob_ref row + pointer.

    Second run is a no-op (inline count -> 0). Never deletes part rows.
    """
    fk_list = conn.execute("PRAGMA foreign_key_list(blob_ref);").fetchall()
    fk_targets = {(r[2], r[3]) for r in fk_list}  # (table, from-col)
    needs_fk_off = any(
        t == "fk_blob_ref_session_id_session_v2_id_fk" or t == "session_id" for t, _ in fk_targets
    ) or bool(
        conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='blob_ref'"
        ).fetchone()
        and sqlite_master_ddl_contains(conn, "session_v2")
    )
    if needs_fk_off and not allow_fk_off:
        raise SystemExit(
            "refusing blob apply: blob_ref.session_id FK-references session_v2(id) "
            "but file parts are keyed by v1 session(id). Re-run with --allow-fk-off "
            "in a window transaction (FKs restored to ON after) or defer until "
            "the v2 writer completion decision. See migration doc section 4."
        )
    restored_fk = False
    if needs_fk_off and allow_fk_off:
        conn.execute("PRAGMA foreign_keys=OFF;")
        restored_fk = True
    try:
        conn.execute("BEGIN IMMEDIATE;")
        rows = conn.execute(FILE_PARTS_SQL).fetchall()
        inserted_blobs = inserted_refs = pointed_parts = 0
        for part_id, sess, msg, _tc, data in rows:
            try:
                doc = json.loads(data)
            except json.JSONDecodeError:
                continue
            url = doc.get("url", "")
            parsed = parse_data_url(url) if isinstance(url, str) else None
            if parsed is None:
                continue
            mime, raw = parsed
            h = hashlib.sha256(raw).hexdigest()
            cur = conn.execute(
                "INSERT OR IGNORE INTO blob(hash, mime, bytes, width, height, data, time_created) "
                "VALUES (?,?,?,?,?,?,?)",
                (
                    h,
                    mime or "application/octet-stream",
                    len(raw),
                    None,
                    None,
                    sqlite3.Binary(raw),
                    int(__import__("time").time() * 1000),
                ),
            )
            inserted_blobs += cur.rowcount
            # seq: per-(session, message) ordinal in time_created order is
            # unnecessary for single-file messages; use 0-based row order
            # within the message via a counted insert (max+1 is overkill
            # for <=144 rows). PK is (session_id, message_id, hash).
            cur = conn.execute(
                "INSERT OR IGNORE INTO blob_ref(session_id, message_id, hash, seq) VALUES (?,?,?,?)",
                (sess, msg, h, 0),
            )
            inserted_refs += cur.rowcount
            # Pointer: replace the inline url with the hash (keep mime +
            # filename for fidelity; never destroy the only copy before the
            # blob row is committed -- this UPDATE is in the same txn).
            conn.execute(
                "UPDATE part SET data = json_set(data, '$.blob_hash', ?, '$.url', NULL, "
                "'$.blob_migrated', 1) WHERE id = ?",
                (h, part_id),
            )
            pointed_parts += 1
        conn.execute("COMMIT;")
    except BaseException:
        with contextlib.suppress(sqlite3.Error):
            conn.execute("ROLLBACK;")
        raise
    finally:
        if restored_fk:
            conn.execute("PRAGMA foreign_keys=ON;")
    integrity = conn.execute("PRAGMA integrity_check;").fetchone()[0]
    blob_count = conn.execute("SELECT COUNT(*) FROM blob;").fetchone()[0]
    blob_ref_count = conn.execute("SELECT COUNT(*) FROM blob_ref;").fetchone()[0]
    remaining = blob_mode_dryrun(conn)
    return {
        "inserted_blobs": inserted_blobs,
        "inserted_refs": inserted_refs,
        "pointed_parts": pointed_parts,
        "blob_before_ok": blob_count,
        "blob_ref": blob_ref_count,
        "remaining_inline": remaining["inline_base64"],
        "integrity_check": integrity,
    }


def sqlite_master_ddl_contains(conn: sqlite3.Connection, needle: str) -> bool:
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='blob_ref'"
    ).fetchone()
    return bool(row and row[0] and needle in row[0])


def vacuum_plan(conn: sqlite3.Connection, db_path: Path) -> dict:
    page_count = conn.execute("PRAGMA page_count;").fetchone()[0]
    page_size = conn.execute("PRAGMA page_size;").fetchone()[0]
    freelist = conn.execute("PRAGMA freelist_count;").fetchone()[0]
    db_bytes = page_count * page_size
    return {
        "page_count": page_count,
        "page_size": page_size,
        "freelist_count": freelist,
        "db_bytes": db_bytes,
        "freelist_bytes": freelist * page_size,
        "note": "VACUUM alone reclaims <= freelist_bytes; bloat is live pages. "
        "Compact path: archive cold v1 -> VACUUM INTO new file -> verify -> swap. "
        "Need free disk >= DB + WAL + compact + snapshot (~12 GB) before starting.",
        "compact_target": str(db_path.with_name(db_path.stem + ".compact.db")),
        "post_compact_pragmas": [
            "PRAGMA page_size = 4096;",
            "PRAGMA journal_mode = WAL;",
            "PRAGMA auto_vacuum = INCREMENTAL;",
            "PRAGMA incremental_vacuum;",
            "PRAGMA journal_size_limit = 268435456;",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument(
        "--mode",
        choices=["archive", "project", "blob", "vacuum", "all"],
        default="all",
        help="which GC to report/apply (default all)",
    )
    ap.add_argument("--dry-run", action="store_true", help="default: report only")
    ap.add_argument("--apply", action="store_true", help="actually mutate (window only)")
    ap.add_argument(
        "--allow-fk-off",
        action="store_true",
        help="blob mode only: window transaction with foreign_keys=OFF",
    )
    ap.add_argument("--archive-days", type=int, default=ARCHIVE_DAYS)
    ap.add_argument("--project-days", type=int, default=PROJECT_GC_DAYS)
    ap.add_argument(
        "--keep-mega-input-tokens",
        type=int,
        default=5_000_000,
        help="archive guard: keep sessions with tokens_input above this",
    )
    ap.add_argument(
        "--keep-project-id",
        action="append",
        default=[],
        help="project id never deleted by project GC (repeatable, up to 3)",
    )
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.apply and args.dry_run:
        print("error: --apply and --dry-run are mutually exclusive", file=sys.stderr)
        return 2
    if not Path(args.db).exists():
        print(f"error: DB not found: {args.db}", file=sys.stderr)
        return 1

    do_apply = args.apply
    out: dict = {"mode": "apply" if do_apply else "dry-run", "db": args.db, "sections": {}}

    conn = connect_readonly(args.db) if not do_apply else sqlite3.connect(args.db)

    if args.mode in ("archive", "all"):
        arch = {
            "v1_archivable_naive": conn.execute(ARCHIVE_COUNT_SQL, (args.archive_days,)).fetchone()[
                0
            ],
            "v2_archivable_naive": conn.execute(
                ARCHIVE_COUNT_V2_SQL, (args.archive_days,)
            ).fetchone()[0],
            "chain_at_risk": conn.execute(CHAIN_BREAK_SQL, (args.archive_days,)).fetchone()[0],
            "v1_archivable_guarded": conn.execute(
                ARCHIVE_GUARDED_COUNT_V1_SQL,
                (args.archive_days, args.keep_mega_input_tokens),
            ).fetchone()[0],
        }
        if do_apply:
            cur = conn.execute(
                ARCHIVE_UPDATE_V1_SQL, (args.archive_days, args.keep_mega_input_tokens)
            )
            arch["v1_archived_now"] = cur.rowcount
            cur = conn.execute(
                ARCHIVE_UPDATE_V2_SQL, (args.archive_days, args.keep_mega_input_tokens)
            )
            arch["v2_archived_now"] = cur.rowcount
            conn.commit()
        out["sections"]["archive"] = arch

    if args.mode in ("project", "all"):
        rows = conn.execute(PROJECT_DRYRUN_SQL).fetchall()
        session_less = len(rows)
        with_deps = sum(1 for r in rows if (r[5] or 0) or (r[6] or 0) or (r[7] or 0))
        keep_ids: list[str] = list(args.keep_project_id)[:3]
        while len(keep_ids) < 3:
            keep_ids.append("")
        # Also count keep-listed ids actually present in the dry-run set.
        keep_listed = sum(1 for r in rows if r[0] in keep_ids)
        proj = {
            "session_less_total": session_less,
            "with_dependents_keep": with_deps,
            "deletable_strict": session_less - with_deps,
            "keep_listed_in_set": keep_listed,
            "keep_ids": keep_ids,
            "deletable_after_keep": session_less - with_deps - keep_listed,
        }
        if do_apply:
            cur = conn.execute(
                PROJECT_DELETE_SQL, (args.project_days, keep_ids[0], keep_ids[1], keep_ids[2])
            )
            proj["deleted_now"] = cur.rowcount
            conn.commit()
        out["sections"]["project"] = proj
        out["sections"]["project_rows"] = [
            {
                "id": r[0],
                "worktree": r[1],
                "time_created": r[2],
                "v1": r[3],
                "v2": r[4],
                "permissions": r[5],
                "worktrees": r[6],
                "directories": r[7],
            }
            for r in rows[:5]
        ] + (
            [{"...": f"{session_less - 5} more (see --dry-run --json for full list in window)"}]
            if session_less > 5
            else []
        )

    if args.mode in ("blob", "all"):
        if do_apply:
            out["sections"]["blob"] = blob_mode_apply(conn, args.allow_fk_off)
        else:
            out["sections"]["blob"] = blob_mode_dryrun(conn)

    if args.mode in ("vacuum", "all"):
        out["sections"]["vacuum"] = vacuum_plan(conn, Path(args.db))

    if do_apply and args.mode in ("archive", "project"):
        out["integrity_check"] = conn.execute("PRAGMA integrity_check;").fetchone()[0]
    conn.close()

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(json.dumps(out["sections"], indent=2))
        print(f"({out['mode']}: {'writes applied' if do_apply else 'no writes performed'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
