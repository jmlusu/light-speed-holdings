# opencode.db Retention / GC — Migration Plan (30-day archive, project GC, VACUUM INTO, blob)

**Companion to:** `reports/opencode-db-reliability-fix-2026-11-08.md` §§9–11
**Applier script:** `scripts/maintenance/opencode-db-retention.py` (dry-run default)
**Status:** Plan + dry-run script only. No `UPDATE`/`DELETE`/`VACUUM` has run
against the live DB. A `--apply` run requires a maintenance window with
OpenCode writers stopped and a fresh snapshot (`opencode-db-maintenance.ps1`).

All counts below were re-probed read-only on 2026-11-08 against
`~/.local/share/opencode/opencode.db` (writers active — 6 OpenCode
processes; hence no writes). Live drift vs the audit baseline is
documented per section: the DB is live, so re-probe before every
`--apply` and do not reuse these numbers as a substitute for a fresh
dry-run.

---

## 1. 30-day archive via `time_archived` (mark, never delete)

**Schema (probed):** `session.time_archived` and `session_v2.time_archived`
both exist (`INTEGER`, nullable). Currently `COUNT(*) WHERE time_archived
IS NOT NULL = 0` — the archive flag is unused, so marking is additive and
reversible (un-archive = set back to `NULL`).

**Dry-run probe (verified 2026-11-08, `--mode archive --dry-run`):**

| Probe | Value |
|---|---|
| `session` older than 30 d, unarchived (naive) | 2,454 (`sections.archive.v1_archivable_naive`) |
| `session` before 2026-09-01 (plan §9 cold scope) | 938 sessions / 187,694 parts |
| `session_v2` older than 30 d, unarchived | 0 (v2 is all recent) |
| Chain risk (child live, parent archivable) | **1,783** live children point at archivable parents |
| `session` archivable **after guards** (chain + mega) | **2,182** (`sections.archive.v1_archivable_guarded`) |
| Mega-sessions among old (`tokens_input > 5M`) | 43 (kept live per `--keep-mega-input-tokens=5000000` default) |

**Apply semantics (script):**

```sql
-- v1 + v2, guarded by chain closure + mega-session keep.
UPDATE session SET time_archived = (strftime('%s','now')*1000)
WHERE time_archived IS NULL
  AND time_created < (strftime('%s','now') - 30*86400)*1000
  AND tokens_input <= 5000000
  AND id NOT IN (SELECT parent_id FROM session
                 WHERE parent_id IS NOT NULL AND time_archived IS NULL);
-- (same for session_v2)
```

- Chain closure is load-bearing: 1,783 live children point at archivable
  parents. The guard excludes 260 naive parents (2,454 → 2,193 before the
  mega filter, 2,182 after), so archiving the guarded set cannot hide a
  live child's parent. Do not drop the guard to "archive more" — the
  excluded parents stay live until their children age out.
- Mega-sessions (`tokens_input > 5M`, 43 among the old) **stay live** even
  if old — archive a cold copy in the §9 snapshot, keep the live row for
  token-burn analysis (plan §9, P3). Enforced by default via
  `--keep-mega-input-tokens=5000000`; override only with a recorded reason.
- Bloat is live pages (`part` 670,664 rows), not `time_archived` bookkeeping.
  Archiving alone reclaims **zero disk** until the VACUUM INTO compact (§3)
  moves cold rows out of the primary. Archive is the labelling step; compact
  is the reclaim step. Do not promise reclaim from archive alone.
- Verification after apply: `COUNT(*) WHERE time_archived IS NULL`
  drops by the dry-run count; `session`/`session_v2` totals unchanged;
  `integrity_check=ok`.

---

## 2. Project GC (session-less projects)

**Probed 2026-11-08:** `project 72`, distinct `project_id` in `session` = 5,
session-less (no rows in `session` **and** `session_v2`) = **66** (audit
baseline 67 — live drift of −1; re-probe before apply).

**FK/DDL finding (probed):** all project children are `ON DELETE CASCADE`
(`session`, `session_v2`, `permission`, `project_directory`, `worktree`).
Cascades are therefore *safe for the DB* but *destructive for data*: deleting
a project silently deletes its `permission` rows. The script enforces the
stricter plan rule — a project is deletable only if it has **zero sessions
in v1 and v2 AND zero permission/worktree/project_directory rows AND
`time_created` > 30 days old**. Live probe: **2 of the 66** session-less
projects have dependents and are **kept** by the strict rule, so the
deletable set is **64** (not 66). `todo` references `session`, not
`project`, so it cannot be orphaned by this GC.

**Keep-list note:** the plan names the main project
`9930faf505f3a0275fc48912f28e4e9e96e066c2` and
`light-speed-holdings-integration` as keepers. The main project has
sessions (safe). `light-speed-holdings-integration` is **currently
session-less** (probed: v1=0, v2=0, no dependents) but only ~18 days old,
so the 30-day age guard keeps it today — it would become deletable in
~12 days if it stays session-less. Pass
`--keep-project-id <main> --keep-project-id <integration-id>` in the
window to protect it by id regardless of age; confirm the integration id
fresh (ids drift with live writes).

**Creation guard (follow-up, not in script):** `project` rows are created
eagerly (10 new on 2026-11-03/04 alone). Add a guard so a `project` row is
only created when the first `session` is persisted — otherwise sprawl
recurs within weeks. Owner: registry-owner.

**Verification after apply:** `COUNT(*) FROM project` → ~6 (5 with sessions
+ recently-created session-less < 30 d); session-less count → 0 (except
< 30 d rows, by design). Keep the main project
`9930faf505f3a0275fc48912f28e4e9e96e066c2`
(`C:/Users/jmlus/light-speed-holdings`) + `light-speed-holdings-integration`
— both have sessions, so the strict rule never touches them, but assert
their presence in the window checklist.

---

## 3. VACUUM INTO compact plan (reclaim live-page bloat)

**Why not bare `VACUUM`:** `page_count=790,157`, `page_size=4096`,
`freelist_count=2,322` (≈ 9.5 MB; audit baseline 1,996 ≈ 8 MB),
`auto_vacuum=0 (NONE)`, `integrity_check=ok`. `VACUUM` alone reclaims at
most the freelist (~9 MB). Bloat is live rows. `auto_vacuum=INCREMENTAL`
is a no-op without a rebuild — never set it on the existing 3 GB file.

**Steps (maintenance window, writers stopped, snapshot verified):**

1. Mark archive (§1) on a **clone** of the DB; verify counts.
2. `.backup` the pre-compact DB → `opencode.db.pre-compact-<ts>.db`
   (keep 30 days; this is the swap rollback).
3. Copy **kept** rows only into a new primary file via `VACUUM INTO`:
   `VACUUM INTO 'opencode.compact.db';`
   (`VACUUM INTO` writes a *new* file; the live DB is untouched.)
4. Verify the compact file: `integrity_check=ok`, counts per
   `reports/opencode-db-reliability-fix-2026-11-08.md` §15.2, chain
   closure (`parent_id` resolvable in live or cold).
5. Swap (writers still stopped): replace `opencode.db` with
   `opencode.compact.db`, keep the pre-compact copy. Reopen OpenCode.
6. On the new primary only: `page_size=4096`, `journal_mode=WAL`,
   `auto_vacuum=INCREMENTAL`, `incremental_vacuum`,
   `journal_size_limit=268435456`.
7. Smoke test: new session + new tool call + `wal_checkpoint(PASSIVE)`;
   WAL stable (< 50 MB after first TRUNCATE).

**Disk pre-flight:** `> 12 GB` free on the DB volume (DB + WAL + snapshot +
compact + archive). Archive the 38.5 GB `.bak` first
(`opencode-db-bak-disposition.ps1`) to satisfy this. Probed free space
2026-11-08: ~128 GiB free on C: — room exists, but `.bak` disposal should
still land first so the window is not disk-fragile.

**Size expectation (estimate only — measure `VACUUM INTO` output):** if cold
v1 is ~28% of `part` rows (187,694 / 670,664 before 2026-09-01) the compact
primary lands near ~2 GiB; do not rely on the `.bak` size as a predictor.
Freelist after compact: `0`.

---

## 4. Blob migration (144 inline `file` parts → `blob`/`blob_ref`)

**Probed 2026-11-08:**

| Probe | Value |
|---|---|
| `part WHERE type='file'` | 144 (57 distinct sessions) |
| of those, `url LIKE 'data:%base64,%'` | 143 inline payloads |
| `blob` / `blob_ref` rows | 0 / 0 |
| Base64 key | `data.url` (`data:<mime>;base64,<payload>`); `data.mime`, `data.filename` |
| Producer examples | `text/plain` (`outstanding_tasks.md`), `image/png` (`image.png`) |

**DDL (probed):**

- `blob(hash TEXT PK, mime, bytes, width, height, data BLOB, time_created)`
- `blob_ref(session_id, message_id, hash, seq, PK(session_id,message_id,hash))`
- `blob_ref.session_id` FK → **`session_v2(id)`** (not v1 `session(id)`).

**FK blocker (must be decided, not guessed):** inline file parts are keyed by
v1 `session(id)` in `part`, but `blob_ref` only accepts v2 ids. A naive
`INSERT INTO blob_ref` violates the FK. Options:

1. **Window transaction with `PRAGMA foreign_keys=OFF`** (restore `ON`
   immediately after), documented as a deliberate v1→blob bridge until the
   v2 writer is fixed. The script implements this behind `--allow-fk-off`
   and refuses without it.
2. **Defer** until the v2-cutover decision (`session_part 0` — escalate to
   `vp_engineering` per plan §12). Migrating v1 files alone does not fix
   v2, which has no equivalent path yet.

Until that call is made, run the migrator only on a **clone**, verify
`blob.bytes == decoded length` row-by-row + `integrity_check=ok`, and keep
the primary untouched.

**Migrator semantics (idempotent):** for each file part with an inline data
URL: `bytes = base64_decode(payload)`, `hash = sha256(bytes)`,
`INSERT OR IGNORE INTO blob(...)` (dedup free: same image twice = one row —
143 payloads → ≤143 hashes), `INSERT OR IGNORE INTO blob_ref(...)`,
then `UPDATE part SET data = json_set(data, '$.blob_hash', hash,
'$.url', NULL, '$.blob_migrated', 1)` in the **same transaction** so the
pointer never lands without the blob. Second run is a no-op (inline → 0).
`width`/`height` are left `NULL` (recoverable from binary: PNG `IHDR`);
`seq` is `0` (single-file messages dominate; per-message ordinal is a
follow-up if multi-file messages need ordering).

**New-file policy:** all new attachments go to `blob`/`blob_ref` at write
time; `part.data` stores the hash only. Guard in the recorder (not a DB
`CHECK` — JSON is schemaless) + a test asserting `length(data) < 1e6`
for file parts.

**Verification:** `blob ≤ 143`, `blob_ref = 143` (minus dedup), remaining
inline `= 0`, `integrity_check=ok`. Backup/restore tools must preserve
`BLOB` binary — verify the `.backup` round-trip on the clone before the
primary run.

---

## 5. Window order (retention/GC slice)

Per plan §14: snapshot → checkpoint → orphan sweeper → temp purge →
project GC (after FK probe) → event-sequence archive+GC (only if no reader)
→ archive + VACUUM INTO + swap → blob on clone then primary (may split to a
second window). Steps 0–7 of §14 alone reclaim ~38.5 GB + ~98k temp files
and are fully reversible; blob (step 9) and the archive swap (step 8) may be
deferred to window 2 if disk/time is tight.

**Do-not-do list:** do not run `PRAGMA auto_vacuum=INCREMENTAL` on the live
3 GB file; do not `DELETE` orphan rows (analytics must see them); do not
delete `-wal`/`-shm` manually; do not run the blob migrator on the primary
before a clone round-trip; do not dispose the 38.5 GB `.bak` without the
fresh snapshot + cold copy.
