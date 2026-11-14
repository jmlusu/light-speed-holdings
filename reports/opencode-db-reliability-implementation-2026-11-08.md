# opencode.db Reliability — P0 Disk + P3 Lifecycle Implementation — 2026-11-08

**Author:** platform-reliability-engineer, LightSpeed Holdings
**Working directory:** `C:\Users\jmlus\light-speed-holdings`
**Parent plan:** `reports/opencode-db-reliability-fix-2026-11-08.md`
**Status: IMPLEMENTED AS SCRIPTS + REPORT. No writes to the live DB.**

No `DELETE/UPDATE/INSERT/VACUUM/REINDEX` was executed against
`opencode.db`; no checkpoint was run; the 38.5 GB `.bak` was not copied or
deleted; no temp files were deleted. All six task items below were delivered
as dry-run-safe scripts (plus a src skeleton) with read-only verification
against the live DB. Nothing outside the workspace was written except
read-only inspection of `~/.local/share/opencode/` and
`%LOCALAPPDATA%\Temp\opencode`.

Writers were active throughout verification: **6 OpenCode processes**
(PIDs observed live). Every `-Apply`/`--apply` path therefore correctly
refuses to run now (see §1 gates).

---

## 0. Deliverables (files created)

| # | File | Task | Mode |
|---|---|---|---|
| 1 | `scripts/maintenance/opencode-db-maintenance.ps1` | WAL checkpoint runbook + script (P0) | dry-run default; `-Apply` with snapshot + writers-stopped + free-space gates |
| 2 | `scripts/maintenance/opencode-db-bak-disposition.ps1` | `.bak` inventory + disposal gate (P0) | dry-run default; copy-only by default, delete needs dual flag |
| 3 | `scripts/maintenance/opencode-db-sweeper.py` | Orphan sweeper (P0) | `--dry-run` default (read-only URI), `--apply` for window |
| 4 | `scripts/maintenance/opencode-temp-sweeper.ps1` | Temp 7-day purge + quota alerts (P0) | dry-run default; `-Apply` (+ `-QuarantineDir`) for window |
| 5a | `scripts/maintenance/opencode-db-retention.py` | Retention/GC applier: archive + project + blob + vacuum plan (P3) | dry-run default, `--apply` for window |
| 5b | `scripts/maintenance/opencode-db-retention-plan.md` | Migration doc (30-day archive, project GC, VACUUM INTO, blob) | doc |
| 6a | `src/ai_company/executor/read_cache.py` | Hot-file dedup skeleton (session LRU + mtime/size) | standalone skeleton, **not wired** into ToolRunner |
| 6b | `tests/unit/test_read_cache.py` | 7 regression tests for the skeleton | `pytest` |
| 7 | `reports/opencode-db-reliability-implementation-2026-11-08.md` | This report | — |

No existing files were modified. In particular the concurrent uncommitted
toolfix work (`src/ai_company/executor/tool_validation.py` untracked +
`tool_summarizer.py`/`tool_runner.py` modified — see §6) was **not touched**:
§6 reconciles with it instead of overwriting it.

---

## 1. WAL checkpoint runbook + script (P0-1)

**Script:** `scripts/maintenance/opencode-db-maintenance.ps1`

- **Dry-run (what ran here):** `sqlite3 -readonly` PRAGMAs only —
  `journal_mode`, `page_size`, `page_count`, `freelist_count`,
  `auto_vacuum`, `journal_size_limit`, `integrity_check`, plus row counts.
  No `wal_checkpoint`, `VACUUM`, or `journal_size_limit` write is executed
  without `-Apply`.
- **`-Apply` gates (all must pass or exit 1):** snapshot present with
  `integrity_check=ok` on the **snapshot**; **zero** OpenCode writer
  processes; free space ≥ `-MinFreeGB` (default 12 GB). Only then:
  `PRAGMA wal_checkpoint(TRUNCATE)` with 5× retry (2 s sleep; `busy=1` is
  safe/retryable), followed by `journal_size_limit=268435456` (256 MB),
  `synchronous=NORMAL`, `temp_store=MEMORY`, `cache_size=-64000`, then
  read-only verification (mode, limit, integrity, file sizes).
- **Runbook in script header:** writers stopped; one-off window + periodic
  `PASSIVE` every 5 min / `TRUNCATE` hourly; alert if WAL > 10% × DB;
  rollback = restore snapshot, never delete `-wal`/`-shm` manually;
  expected outcome is durability + backup fidelity, not reclaim (freelist
  is tiny, total DB+WAL ≈ unchanged after TRUNCATE).

**Verification (dry-run output, live DB 2026-11-08):**

| Check | Output |
|---|---|
| Files (pre) | `opencode.db 3,236,483,072 B`, `opencode.db-wal 3,163,682,112 B`, `opencode.db-shm 98,304 B` |
| `journal_mode` | `wal` |
| `page_size` / `page_count` | `4096` / `790157` |
| `freelist_count` | `990` (fluctuates with live writes; audit baseline 1,996) |
| `auto_vacuum` | `0` (NONE) |
| `journal_size_limit` | `-1` (unlimited — window will set 256 MB) |
| `integrity_check` | `ok` |
| Counts (readonly) | `session=3131 message=153182 part=670664` |
| Writers | 6 OpenCode processes → `-Apply` refusal path manually confirmed by logic; **no `-Apply` was attempted** |
| Volume free (C:) | ~129 GiB (pre-flight floor 12 GB is satisfiable after `.bak` disposal) |

Command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/maintenance/opencode-db-maintenance.ps1
# DRY-RUN: read-only PRAGMA only. To apply (maintenance window, writers
# stopped): add -Apply -SnapshotPath <opencode.db.pre-checkpoint-<ts>.db>
```

---

## 2. `.bak` disposition — inventory + gated script (P0-2)

**Script:** `scripts/maintenance/opencode-db-bak-disposition.ps1` (dry-run
inventory + v2-stability proof + snapshot gate; `-Apply` cold-copies via
`robocopy /J`, verifies byte-length, optionally SHA-256 with `-VerifyHash`;
deletion additionally requires **both** `-DeleteAfterVerify` and
`-ColdCopyVerified`). **The 38 GB file was NOT deleted in this task** —
the script is staged for the window once the fresh snapshot + cold copy
exist.

**Inventory (read-only, verified 2026-11-08):**

| Field | Value |
|---|---|
| Path | `C:\Users\jmlus\.local\share\opencode\opencode.db.bak` |
| Length | `38,533,844,992 B` = **35.89 GiB / 38.53 GB** |
| LastWriteTime | `2026-11-01 16:56:41` (pre-v2) |
| Age | **7 days** (retention threshold 30 days) |
| `.bak*` files | 1 file, 35.89 GiB combined |
| Live DB | `3,236,483,072 B` → source/live ratio **~11.9×** |
| v2 stability (readonly) | `session_v2=137` (live drift: 131→133→137 during the session), `migration.v1-v2={"phase":"completed"}`, `integrity_check=ok` |

**Decision-gate correction (important):** the script header originally
worded the retention rule as `older than 30 days AND >2× live DB`. At 7 days
old that `AND` would **defer** disposition — wrong for this file. The rule is
now `older OR >2× live DB`, and the disposition here is required by
**size + supersession** (pre-v2 snapshot, ~12× live, replaced by the fresh
snapshot), not by age. The 7-day age is recorded so the window checklist
does not mistake "young" for "retain".

**Window gate (all required before `-Apply`):** fresh post-v2 snapshot at
`-SnapshotPath` with `integrity_check=ok`; cold dest with free space ≥ source;
v2 stable (proven above); explicit operator approval recorded separately for
copy vs delete.

Command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/maintenance/opencode-db-bak-disposition.ps1
```

---

## 3. Orphan sweeper — SQL/Python with dry-run (P0-3)

**Script:** `scripts/maintenance/opencode-db-sweeper.py`

- **Dry-run default:** opens `file:<path>?mode=ro` + `PRAGMA query_only=1`
  and runs only `SELECT`s — structurally unable to write. `--apply` runs
  both `UPDATE`s in one `BEGIN IMMEDIATE` transaction: `json_set`
  `$.state.status='error'`, `$.state.error`, `$.state.orphaned=1`,
  `time_updated=now`. Preserves `state.input`/`state.output`/timestamps;
  never `DELETE`s. TTLs: `running>3600s`, `pending>86400s` (overridable).
- **Apply was NOT run** against the live DB in this task. The `UPDATE`
  path was proven on a synthetic in-memory DB: stale-running flipped to
  `error`/`orphaned=1` with output preserved; fresh-running untouched;
  `integrity_check=ok`.

**Verification (dry-run, live DB):**

| Probe | Value |
|---|---|
| `running` stale (>1 h) | **93** |
| `pending` stale (>24 h) | **2** |
| Would update | **95** |
| Breakdown | `task/running 51` (oldest 2026-08-07), `bash/running 30` (2026-08-08), `question/running 10` (2026-08-12), `write/pending 2` (2026-08-18), `read/running 1` (2026-08-08), `write/running 1` (2026-09-06) |
| Status totals | `completed 185183`, `error 3435`, `running 93`, `pending 2` (expect post-apply `error=3530`, `running=pending=0`) |

Note: the task brief's "93 running + 2 pending" is confirmed exactly,
including the two easily-missed rows (`read`/`write` running) that the
plan's top-3 breakdown omits.

Commands:

```powershell
uv run python scripts/maintenance/opencode-db-sweeper.py --dry-run --json
uv run python scripts/maintenance/opencode-db-sweeper.py --apply   # window only
```

---

## 4. Temp sweeper — 7-day purge with quota alerts (P0-4)

**Script:** `scripts/maintenance/opencode-temp-sweeper.ps1` (dry-run default;
`-Apply` deletes stale **files only**, never the root; locked files skipped
and logged; `-QuarantineDir` moves instead of deletes for the first run).

**Current counts (fresh, dry-run 2026-11-08):**

| Probe | Value |
|---|---|
| **Temp-owned total** (PS `Get-ChildItem`, junctions excluded — purge scope) | **31,285 files / 0.46 GiB** |
| Fresh ≤ 7 d | 296 files |
| Stale > 7 d | 30,989 files / 0.46 GiB (99.1% stale) |
| Quota (defaults 50,000 files / 2 GB) | `[OK]` files, `[OK]` size, `[WARNING]` stale share >90% (1 alert) |
| Junction-inclusive `cmd dir /s` total | 98,333 files / 1,414 MB — **inflated, do not use as purge scope** (see junction box) |

> **⚠️ JUNCTION SAFETY FINDING (new, blocks naive purge):** four
> `node_modules` junctions under `Temp\opencode` point at the **live
> workspace** `C:\Users\jmlus\light-speed-holdings\node_modules`:
> `audit-2026-10-25-turnstile-csp\vitest-negative-control\node_modules`,
> `...vitest-run\node_modules`, `...vitest-verify-patch\node_modules`,
> `headcheck\node_modules`. `cmd dir /s` and any junction-following walk
> (e.g. a Python `os.scandir` recursion) count the alias target ~4× as
> ~67k phantom Temp files (31k owned + 67k aliases ≈ 98k). **A purge that
> follows junctions deletes live workspace files through the alias.**
> The PS script reports all four junctions, excludes them from counts,
> and never traverses or `Remove-Item -Recurse`s them (uses
> non-following `Get-ChildItem`). Fresh-count approval must quote the
> **31,285 Temp-owned** figure (audit baseline 31,217 — near-zero drift),
> not the 98k junction-inclusive figure. **No mass deletion was performed.**

Commands:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/maintenance/opencode-temp-sweeper.ps1
# Window (after fresh-count approval):
powershell -ExecutionPolicy Bypass -File scripts/maintenance/opencode-temp-sweeper.ps1 `
  -Apply -QuarantineDir "$env:USERPROFILE\.local\share\opencode\tool-output\quarantine-20261108"
```

---

## 5. Retention/GC — migration doc + script (P2/P3)

**Doc:** `scripts/maintenance/opencode-db-retention-plan.md` (30-day archive
via `time_archived`, project GC, VACUUM INTO compact, 144→blob/blob_ref,
window order, do-not-do list). **Script:**
`scripts/maintenance/opencode-db-retention.py` (`--mode archive|project|blob|vacuum|all`,
dry-run default).

**Verification (dry-run `--mode all --json`, live DB):**

| Section | Values |
|---|---|
| Archive naive | `v1 2454`, `v2 0`, chain-at-risk **1783** live children → archivable parents |
| Archive **guarded** | **2182** (`chain closure` + `tokens_input ≤ 5M`; chain guard excludes 260 naive parents, mega guard keeps 43 old mega-sessions) |
| Project | `session_less 66` (audit 67, drift −1), `with_dependents_keep 2`, `deletable_strict 64`; keep-list via `--keep-project-id` (protects main + integration by id; integration is currently session-less but only ~18 d old so age-guarded today — protect by id in the window) |
| Blob | `file 144` (57 sessions), `inline base64 143`, `external 0`, `unparsable 1`, `distinct hashes 135`, `inline bytes 13,896,476`; `blob=0`, `blob_ref=0`; key is `data.url=data:<mime>;base64,...` |
| VACUUM | `page_count=790157`, `page_size=4096`, `freelist=990` (~4 MB), `DB=3,236,483,072 B`; plan: archive → `VACUUM INTO` new file → verify → swap → `auto_vacuum=INCREMENTAL` on the new primary only |

**Two schema findings the window must respect (both probed, both in-script):**

1. **Blob FK blocker:** `blob_ref.session_id` FK-references `session_v2(id)`,
   but inline parts are keyed by v1 `session(id)`. A naive insert violates
   the FK. The script refuses blob `--apply` without `--allow-fk-off`
   (window transaction, FKs restored to `ON`) or deferral until the
   `vp_engineering` v2-cutover decision. First run must be on a **clone**
   (`blob.bytes == decoded length` + `integrity_check`, then primary).
2. **Project cascades:** all project children are `ON DELETE CASCADE`, so
   the strict rule (zero sessions **and** zero permission/worktree/
   directory rows, >30 d) is load-bearing — without it, GC silently deletes
   permission rows. `todo` references `session`, not `project`, so it
   cannot be orphaned by this GC.

Commands:

```powershell
uv run python scripts/maintenance/opencode-db-retention.py --mode all --dry-run --json
# Window (clone first for blob):
uv run python scripts/maintenance/opencode-db-retention.py --mode archive --apply
uv run python scripts/maintenance/opencode-db-retention.py --mode blob --db <clone.db> --apply --allow-fk-off
```

---

## 6. Output cap 64 KB + hot-file dedup skeleton (src)

**Delivered:** `src/ai_company/executor/read_cache.py` (session LRU with
`(mtime, size)` freshness, thread-safe, optional TTL, hash cross-check) +
`tests/unit/test_read_cache.py` (7 tests, all pass). The skeleton is
**deliberately not wired** into `ToolRunner` — the docstring spells out the
phase-2 wiring plan (check before `read_text`, pointer on hit, `put` on
miss; session-start context injected once via recall instead of re-read).
It composes with, rather than replaces, the existing hash deduper
(`ToolOutputDeduper`) and summarizer cap (`truncate_to_cap`).

**Reconciliation with concurrent work (do not overwrite):** while this task
ran, uncommitted toolfix work landed in the tree
(`tool_validation.py` untracked, `tool_summarizer.py`/`tool_runner.py`
modified) implementing a **50 KB end-to-end summarizer cap** (`OUTPUT_CAP_BYTES
= 50*1024`), grep line/match caps, edit preflight, retry classification,
and the hash deduper. That cap is **stricter** than the requested 64 KB
(51,200 < 65,536) for this repo's executor→LLM path, and the 64 KB ceiling in
the plan is the **harness ripgrep JSON record** (`GREP_RECORD_CAP_BYTES =
64*1024` in the new `tool_validation.py`). The opencode.db tail (`1,641`
completed outputs >50k chars, re-probed 2026-11-08) is **harness-side
`part.data`** — this repo's summarizer never wrote to `opencode.db`
directly, so the repo cap prevents *new* repo-side bloat but does not
retroactively bound harness rows. Harness-side enforcement (executor
boundary spill + `$.state.output_truncated` + re-run hint) remains a
harness change, tracked in plan §7; the skeleton here is the repo-side
complement. No src files were modified to deliver this item, so no
concurrent work was clobbered.

**Verification:**

| Check | Result |
|---|---|
| `pytest test_read_cache.py + test_tool_summarizer.py + test_tool_vocabulary.py` | **44 passed** (7 new + 37 existing; summarizer 24/24 confirms the concurrent cap helpers import cleanly) |
| `ruff check` on new src + scripts + test | **All checks passed** |
| `mypy` on `read_cache.py` (+ `tool_validation.py`, `tool_summarizer.py`) | **Success, no issues** |
| `opencode.db` output tail (readonly, still un-capped harness-side) | `>50k chars: 1641` (unchanged — expected until harness §7 lands) |

---

## 7. Consolidated verification table (live DB, 2026-11-08)

| Check | Value | Gate |
|---|---|---|
| `journal_mode` / `page_size` / `page_count` / `freelist` / `auto_vacuum` / `journal_size_limit` | `wal` / `4096` / `790157` / `990` / `0` / `-1` | — |
| `integrity_check` | `ok` | REQUIRED — holds |
| Files | DB `3,236,483,072` / WAL `3,163,682,112` / SHM `98,304` / `.bak` `38,533,844,992` | WAL ~98% of DB → checkpoint window needed |
| Counts | `session=3131 session_v2=137 part=670664 project=72 event_sequence=3573 blob=0` | drift vs audit noted in §3/§5 |
| Orphans | `completed 185183 error 3435 running 93 pending 2` | sweeper would leave `error=3530`, `running=pending=0` |
| Temp (owned) | `31,285 files, 296 fresh, 30,989 stale` + 4 junctions (excluded) | purge pending approval |
| Disk (C:) | ~129 GiB free | 12 GB window floor satisfiable |

---

## 8. What was NOT done (explicit)

1. **No checkpoint / vacuum / journal-size change** against the live DB
   (writers active; script gates would refuse). Verify via
   `opencode-db-maintenance.ps1` dry-run only.
2. **No `.bak` deletion or copy** — inventory + disposition script staged;
   deletion gate documented (§2). The 38.5 GB file is untouched.
3. **No orphan mutation** — sweeper `--apply` proven on synthetic data
   only; live `--apply` awaits the window.
4. **No temp deletion** — fresh counts reported (§4); mass deletion awaits
   fresh-count approval quoting the Temp-owned figure.
5. **No `UPDATE`/`DELETE`/`VACUUM INTO` in retention** — all `--mode` runs
   were dry-run; `--apply` / swap await the window.
6. **No `ToolRunner` wiring** for the read cache — skeleton only (phase 2
   needs executor-owner approval on scale semantics).

## 9. Maintenance-window order (next window)

Per plan §14 + §§1–5 above: announce + stop writers → archive `.bak`
→ fresh snapshot + verify → checkpoint `TRUNCATE` + 256 MB cap → orphan
`--apply` → temp purge `-Apply` (quarantine first run) → project GC →
event-sequence archive+GC (only if no reader) → archive + `VACUUM INTO` +
swap → blob on clone then primary (deferrable to window 2) → reopen +
smoke test → 14-day re-audit against plan §15.

---

*Evidence:** all counts, sizes, PRAGMAs, and schema probes above trace to
read-only `sqlite3 -readonly` / `Get-Item` / `Get-ChildItem` / dry-run script
output captured 2026-11-08. The live DB drifts continuously (counts moved
during the session — e.g. `session_v2` 131→137, `freelist` 2322→990, Temp
re-counted 31,285 stable): re-probe before every `--apply`.*
