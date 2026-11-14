# opencode.db Reliability Fix Plan — 2026-11-08

**Author:** platform-reliability-engineer, LightSpeed Holdings
**Working directory:** `C:\Users\jmlus\light-speed-holdings`
**Database in scope (plan only, no writes performed):** `C:\Users\jmlus\.local\share\opencode\opencode.db`
**Evidence baseline:**

- `reports/opencode-db-audit-2026-11-08.md` — chief-of-staff read-only audit
- `reports/opencode-db-analytics-2026-11-08.md` — read-only trajectory analytics

**Status: PLAN ONLY.** No `DELETE/UPDATE/INSERT/VACUUM/REINDEX` was executed against `opencode.db` while producing this report. All steps below require the maintenance window in §9 and a pre-change snapshot.

---

## 0. Defect ledger (baseline, evidence-pinned)

| ID | Defect | Evidence (baseline snapshot) | Size / impact | Owner |
|---|---|---|---|---|
| D1 | WAL checkpoint severely behind | `opencode.db` 3,222,466,560 B (~3.00 GiB / ~3.07 GB in tasking) + `opencode.db-wal` 3,163,682,112 B (~2.95 GiB / ~3.01 GB) + `opencode.db-shm` 98,304 B. WAL ≈ 98% of DB. `journal_mode=wal`, `page_size=4096`, `page_count=786735`. | ~6.4 GB live footprint; crash-recovery / backup copies 2×; checkpoint can block writers. | platform-reliability-engineer |
| D2 | `.bak` backup never pruned | `opencode.db.bak` 38,533,844,992 B (~35.89 GiB / ~38.5 GB), `2026-11-01 16:56:41`, pre-v2. `kv.migration.v1-v2={"phase":"completed"}` since then. | ~38.5 GB — 6× live DB; largest single reclaim. | platform-reliability-engineer |
| D3 | Freelist tiny, bloat is live pages | `freelist_count=1996` (~7.6–8 MB), `auto_vacuum=0 (NONE)`, `integrity_check=ok`. | `VACUUM` alone reclaims ≤ ~8 MB. Bloat is live rows (`part` 670,664, `message` 153,182), not free space. | platform-reliability-engineer |
| D4 | Orphaned in-flight tool calls | `part` tool: `completed 185,183`, `error 3,435`, `running 93`, `pending 2`. By tool: `task running 51`, `bash running 30`, `question running 10`, `write pending 2`. No sweeper observed. | 95 non-terminal rows inflate error/queue accounting; stuck tasks mislead orchestration. | platform-reliability-engineer |
| D5 | Cache metering broken | `SUM(tokens_cache_write)=0` in `session`, `session_v2`, `message`, and `step-finish` JSON (`$.tokens.cache.write=0`); `SUM(tokens_cache_read)=15,210,842,514` (v1) + `809,948,648` (v2). Cache-read/input = 8.95× (v1), 9.72× (v2). `step-finish` with `cache.read>0`: 120,113 / 132,342 (90.8%). | Hit-rate / savings dashboards unusable; cost $5.59 on 1.7B input hides burn. | llm-platform-owner + platform-reliability-engineer |
| D6 | v2 writers empty: `session_part`, `blob` | `session_message 9,161–9,284`, `session_part 0`, `blob 0`, `blob_ref 0`, `file parts 144` (57 sessions) inline base64 in `part.data`. `job 0`, `schedule 0`, `session_inbox 0`. | v2 consumers joining `session_part` silently return zero; images inflate `part.data` JSON. | orchestration-owner |
| D7 | Event-store orphans | `event 0` vs `event_sequence 3,527` (audit) / `3,530` (analytics) — drift = live DB. | Sequence ledger without events; cannot reconstruct aggregates. | orchestration-owner |
| D8 | Session-less project sprawl | `project 72`, only 5 distinct `project_id` in `session`; **67/72 session-less** (worktree/temp: `C:/tmp`, `~/.local/share/opencode/worktree/9930fa/*`, `Temp/opencode/uploads/*`). `project_directory 7`, `worktree 7`. | Join noise; `project` table becomes unusable for ownership. | registry-owner |
| D9 | Oversize tool outputs, no cap | Completed outputs `>50,000 chars: 1,641`; `>100,000: 5`; max `131,055` chars (`read` `open-design/.../deploy.ts`), `grep` flood 130,806 chars. `grep` error “Ripgrep JSON record exceeded 65536 bytes” ×140. | 64 KB JSON ceiling is the de-facto overflow limit; tool-output spill re-read 288× (`tool_14ff7869e0017hJqN3xYM5Lft7`). | platform-reliability-engineer |
| D10 | Hot-file re-read storm | `read 52,581` ops / 7,163 distinct; `1,442` files touched >10× (any of read/edit/write), `1,101` read >10×. Top: `dashboard/api.py 974×` (758 read-only), `company-registry.yaml 763×` (655), `AGENTS.md 552×` (425), `harness/changes/active/summary.md 466×` (284). | ≥30% of `read` volume is redundant session-start context; drives cache-read burn (15.2B). | platform-reliability-engineer |
| D11 | Temp accumulation | `C:\Users\jmlus\AppData\Local\Temp\opencode`: **31,217 files**, only **228 modified in last 7 days**. | Stale accumulation; approved temp dir becomes a disk leak. | platform-reliability-engineer |
| D12 | Mega-sessions / long tail | Top v1: `ses_f1ad097c… 23.1M input + 377.7M cache-read`; v2 top: `ses_e584330d… 26.8M input + 132.8M cache-read (“Prompt contents”)`. `compaction parts 5,444`. `build` = 61/94 v2 sessions (65%). | Burn concentrated in handful of sessions; v1 frozen 2026-10-22, v2 live 2026-11-01+. | vp-engineering |

---

## 1. Priority order (do in this sequence)

| Order | Task | Reclaim / risk reduction | Why first |
|---|---|---|---|
| P0-1 | WAL checkpoint TRUNCATE runbook (§2) | WAL 3.01 GiB → ~0; restores backup fidelity | Crash safety + makes every later step measurable |
| P0-2 | `.bak` delete/archive policy (§3) | 38.5 GiB, 1 command | Zero code risk, largest disk win |
| P0-3 | Orphan sweeper dry-run + apply (§4) | 95 rows → terminal; unblocks queue accounting | Small, reversible, proves JSON-update path |
| P0-4 | Temp 7-day sweeper (§5) | ~31k files, ~99% stale | Filesystem-only, no DB risk |
| P1-1 | Cache metering fix (§6) | Fixes 15.21B read vs 0 write | Blocks all cost/cache dashboards |
| P1-2 | Output cap 64 KB (§7) | Kills 1,641 >50k + 140 ripgrep overflows | Stops new bloat at the source |
| P1-3 | Hot-file session dedup (§8) | −30% `read` volume target | Stops cache-read burn multiplier |
| P2-1 | VACUUM strategy + archive v1 (§9) | Live-page bloat, not freelist | Needs P0 snapshot first |
| P2-2 | Blob migration (§10) | 144 inline files; prevents recurrence | Needs backup + dedup |
| P2-3 | Project GC (§11) | 67 rows | Low risk after snapshot |
| P2-4 | Event-sequence GC + v2 writer completion (§12) | 3,530 orphans; `session_part 0` | Schema decision; do not rush before P2-1 |
| P3 | Mega-session budget + token alerts (§13) | Token burn | Depends on P1-1 metering |

---

## 2. P0-1 — WAL checkpoint TRUNCATE runbook

### Goal

WAL `~3.01 GiB` → `< 50 MB` steady state; `wal_checkpoint(TRUNCATE)` returns `busy=0`, `wal` frames truncated, `opencode.db-wal` length collapses.

### Preconditions

- OpenCode process stopped (no writer). Verify: `Get-Process opencode` empty + `opencode.db-shm` lock releasable. Checkpoint against a live writer returns `busy=1` — do not force with `PRAGMA journal_mode=DELETE`.
- Pre-change snapshot exists (§9.1). `integrity_check=ok` already proven; re-verify before checkpoint.

### Steps

```powershell
# 0. Snapshot (see §9.1 for full .backup command). Confirm sizes:
Get-ChildItem "$env:USERPROFILE\.local\share\opencode\opencode.db*" |
  Select-Object Name, Length, LastWriteTime
```

```sql
-- 1. Verify before (read-only first)
PRAGMA journal_mode;
PRAGMA page_size;
PRAGMA page_count;
PRAGMA freelist_count;
PRAGMA integrity_check;          -- expect: ok
PRAGMA wal_checkpoint(PASSIVE);  -- expect: 0|N|N (busy=0); proves readability

-- 2. Checkpoint + truncate (MUST run with opencode stopped)
PRAGMA wal_checkpoint(TRUNCATE);
-- Return: busy|log|checkpointed. Success: busy=0, wal frames → 0.
-- Retry up to 5× with 2 s sleep if busy=1 (writer still attached).

-- 3. Cap future WAL growth
PRAGMA journal_size_limit = 268435456;  -- 256 MB (256*1024*1024)
PRAGMA synchronous = NORMAL;            -- WAL default; do NOT set OFF
PRAGMA temp_store = MEMORY;
PRAGMA cache_size = -64000;             -- 64 MB page cache
```

```powershell
# 4. Verify after
Get-ChildItem "$env:USERPROFILE\.local\share\opencode\opencode.db*" |
  Select-Object Name, Length, LastWriteTime
# Expect: opencode.db-wal length drops toward 0; opencode.db may grow
# slightly (frames folded in). Total (DB+WAL) drops only if frames were
# free pages — freelist is only 7.6 MB, so expect total ≈ unchanged;
# the win is durability + backup fidelity, not reclaim.
```

### Scheduling

- One-off: maintenance window (§9.3).
- Periodic: add to daemon cadence — `PRAGMA wal_checkpoint(PASSIVE)` every 5 min; `TRUNCATE` hourly. Alert if `wal > 10% × DB` for >15 min.
- Longer term: `PRAGMA auto_vacuum=INCREMENTAL` requires a rebuild (`VACUUM INTO`); only change with P2-1 (§9), never via bare `PRAGMA` on live DB.

### Risks / rollback

- **Risk:** `TRUNCATE` while a reader holds a snapshot blocks; command returns `busy=1` and does nothing (safe, retryable).
- **Risk:** Force-closing OpenCode mid-write leaves WAL uncheckpointed — SQLite replays WAL on next open, so no data loss if `.bak`/snapshot exists; do **not** delete `-wal`/`-shm` manually.
- **Rollback:** close DB, restore from §9.1 `opencode.db.pre-checkpoint-<ts>.db` via `.backup` reverse copy; re-run `PRAGMA integrity_check`.

### Verification (gates)

```sql
PRAGMA wal_checkpoint(TRUNCATE);  -- busy must be 0
PRAGMA journal_mode;              -- wal
PRAGMA freelist_count;            -- ≈1996 pre; unchanged expected
PRAGMA integrity_check;           -- ok
```

| Check | Pass | Fail action |
|---|---|---|
| `busy` from `wal_checkpoint(TRUNCATE)` | `0` | Stop writers, retry; do not delete WAL |
| `opencode.db-wal` length | `< 50 MB` after TRUNCATE + reopen | Re-run TRUNCATE; investigate checkpoint thread |
| `integrity_check` | `ok` | Restore snapshot; do not proceed to P2 |
| Session/message/part counts (§9.4) | ±0 vs snapshot | Restore snapshot; checkpoint should be count-neutral |

---

## 3. P0-2 — `.bak` delete / archive policy

### Policy

- `opencode.db.bak` (38.5 GiB, 2026-11-01, pre-v2) is a **pre-migration snapshot that was never pruned**. V2 switchover is complete (`kv.migration.v1-v2 = completed`, 91–94 v2 sessions, `integrity_check=ok`).
- **Rule:** retain **one** rolling backup (`opencode.db.bak` ≤ 48 h old) + one cold archive per month. Anything older or larger than `2×` live DB without a retention tag is archived off-volume or deleted.
- **No in-place deletion without a verified fresh snapshot** (§9.1). The §9.1 snapshot *is* the replacement `.bak`.

### Steps

```powershell
# 0. Prove v2 stable (read-only)
sqlite3 -readonly "$env:USERPROFILE\.local\share\opencode\opencode.db" `
  "SELECT COUNT(*) FROM session_v2; SELECT value FROM kv WHERE key='migration.v1-v2'; PRAGMA integrity_check;"
# Expect: v2 >= 90, completed, ok

# 1. Fresh snapshot (replaces .bak). See §9.1. Verify its integrity + size.

# 2. Archive (recommended, cold storage) — move, do not copy-then-forget
$src = "$env:USERPROFILE\.local\share\opencode\opencode.db.bak"
$dst = "\\cold-storage\backups\opencode\opencode.db.bak.2026-11-01"
Move-Item -LiteralPath $src -Destination $dst -Force
# If no cold storage: delete after two consecutive backups verified
# Remove-Item -LiteralPath $src -Force

# 3. Enforce going forward: retention sweeper (weekly, read-only report first)
Get-ChildItem "$env:USERPROFILE\.local\share\opencode\opencode.db.bak*" |
  Sort-Object LastWriteTime | Format-Table Name, Length, LastWriteTime
```

### PowerShell retention sweeper (dry-run default)

```powershell
param([switch]$Apply)
$dir = "$env:USERPROFILE\.local\share\opencode"
$keepDays = 30
Get-ChildItem "$dir\opencode.db.bak*" | ForEach-Object {
  $age = (Get-Date) - $_.LastWriteTime
  $action = if ($Apply -and $age.Days -gt $keepDays) { "DELETED" } else { "KEPT (dry-run)" }
  if ($Apply -and $age.Days -gt $keepDays) { Remove-Item -LiteralPath $_.FullName -Force }
  [pscustomobject]@{ Name=$_.Name; LengthGB=[math]::Round($_.Length/1GB,2);
    AgeDays=$age.Days; Action=$action }
} | Format-Table -AutoSize
```

### Risks / rollback

- **Risk:** deleting the only pre-v2 copy if post-v2 data proves corrupt — mitigated by the fresh §9.1 snapshot taken *after* v2 stability proof.
- **Risk:** `Move-Item` across drives copies then deletes; power loss mid-move can leave both or neither — use `robocopy /MOVE` for cross-volume with `/J` (unbuffered) + verify hash before deleting source.
- **Rollback:** archive copy is the rollback; or restore fresh snapshot (§9.1).

### Verification

```powershell
Get-ChildItem "$env:USERPROFILE\.local\share\opencode\opencode.db.bak*" | Format-Table Name, Length
# Expect: 0 or 1 rolling .bak, total .bak < 2× DB size (not 12×)
# Disk free: +~38.5 GiB if archived off-volume / deleted
```

---

## 4. P0-3 — Orphan sweeper (running / pending)

### Goal

`running 93 + pending 2 → 0` non-terminal rows, without rewriting history for rows the sweeper cannot classify.

### Design (DLQ-grade, mirrors HITL expiry sweep)

- TTL: `running > 1 h` (no heartbeat) → `error` with `"orphaned: no terminal update within 1h"`; `pending > 24 h` → `error` with `"orphaned: pending exceeded 24h"`.
- Preserve original `state.output`, `state.input`, timestamps; only flip `state.status` + append `state.error`. Never `DELETE` orphan rows — analytics must still see them.
- Dry-run first: report by `(tool, age_bucket)`; apply in maintenance window with snapshot.

### Dry-run (read-only)

```sql
SELECT json_extract(data,'$.tool') AS tool,
       json_extract(data,'$.state.status') AS status,
       COUNT(*) AS n,
       MIN(datetime(time_created/1000,'unixepoch','localtime')) AS oldest,
       MAX(datetime(time_created/1000,'unixepoch','localtime')) AS newest
FROM part
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status') IN ('running','pending')
GROUP BY tool, status
ORDER BY n DESC;
-- Expect (baseline): task/running 51, bash/running 30, question/running 10,
-- write/pending 2. Total 95.
```

### Apply (maintenance window, after §9.1 snapshot)

```sql
-- 1. Mark running > 1h as error (uses time_updated if present, else time_created)
-- JSON update via json_set; keep all other keys.
UPDATE part
SET data = json_set(
               data,
               '$.state.status', 'error',
               '$.state.error', 'orphaned: running exceeded 1h without terminal update (sweeper ' || date('now') || ')',
               '$.state.orphaned', 1
             ),
    time_updated = (strftime('%s','now') * 1000)
WHERE json_extract(data,'$.type') = 'tool'
  AND json_extract(data,'$.state.status') = 'running'
  AND (COALESCE(time_updated, time_created) < (strftime('%s','now') - 3600) * 1000);

-- 2. Mark pending > 24h
UPDATE part
SET data = json_set(
               data,
               '$.state.status', 'error',
               '$.state.error', 'orphaned: pending exceeded 24h (sweeper ' || date('now') || ')',
               '$.state.orphaned', 1
             ),
    time_updated = (strftime('%s','now') * 1000)
WHERE json_extract(data,'$.type') = 'tool'
  AND json_extract(data,'$.state.status') = 'pending'
  AND (COALESCE(time_updated, time_created) < (strftime('%s','now') - 86400) * 1000);

-- 3. Verify
SELECT json_extract(data,'$.state.status'), COUNT(*)
FROM part WHERE json_extract(data,'$.type')='tool' GROUP BY 1;
-- Expect: running 0, pending 0, error 3435 + 95 = 3530.
```

> **Fallback if `json_set` on `$.state` path is unsupported in your SQLite build:** use the provider's documented JSON-patch path in `opencode` source; do not string-replace `data` with `REPLACE(data,'"status":"running"','"status":"error"')` — key order is not guaranteed.

### Recurring control

- Daemon job every 15 min: run the dry-run `SELECT` as a metric (`orphaned_tool_calls`). Alert if `running+pending > 5` for >15 min.
- Executor must write `time_updated` on every state transition (resilience: `running` without heartbeat is itself the bug — add heartbeat on long `bash`/`task` calls).

### Risks / rollback

- **Risk:** flipping a still-executing call to `error` creates a double-write when the worker finishes. Mitigated by 1 h TTL + the fact that all 95 baseline orphans predate the audit by days/weeks.
- **Rollback:** `UPDATE` is from the §9.1 snapshot (`ATTACH` the snapshot DB and copy `part.data` back for the 95 `id`s, or restore the whole DB).

### Verification

| Check | Pass |
|---|---|
| `running` + `pending` after apply | `0` |
| `error` count delta | `+95` (3435 → 3530) |
| `integrity_check` | `ok` |
| `message`/`session` counts | unchanged |

---

## 5. P0-4 — Temp sweeper (31,217 files)

### Policy

- Retain `Temp\opencode` files `≤ 7 days` old or `> 1 GB` total? No — retain `≤ 7 days` only. Only 228 files were touched in the last 7 days; the other ~31k are stale.
- Never delete the directory itself; delete **contents** older than 7 days. Pin allowlist: never delete files open by a running OpenCode (`-ErrorAction SilentlyContinue`, log + retry next run).

### Steps (dry-run first)

```powershell
param([switch]$Apply)
$root = "$env:LOCALAPPDATA\Temp\opencode"
if (-not (Test-Path $root)) { "Temp\opencode not found: $root"; exit }
$cutoff = (Get-Date).AddDays(-7)
$all = Get-ChildItem $root -Recurse -File -ErrorAction SilentlyContinue
$stale = $all | Where-Object { $_.LastWriteTime -lt $cutoff }
"total=$($all.Count) stale=$($stale.Count) sizeGB=$([math]::Round(($stale | Measure-Object Length -Sum).Sum/1GB,2))"
if ($Apply) {
  $stale | ForEach-Object {
    try { Remove-Item -LiteralPath $_.FullName -Force -ErrorAction Stop }
    catch { "SKIPPED (locked): $($_.FullName) — $($_.Exception.Message)" }
  }
} else {
  "DRY-RUN only. Re-run with -Apply to delete."
}
```

Run with `-Apply` in the maintenance window; schedule weekly thereafter (newest 7 days preserved).

### Risks / rollback

- **Risk:** deleting a file a live session expects to re-read (e.g. the 288× `tool-output` spill). Mitigated: 7-day window + allowlist for open handles + P1-3 dedup reduces re-reads.
- **Rollback:** none needed (temp is regenerable); keep a 48 h recycle-bin move (`Move-Item` to `$env:USERPROFILE\.local\share\opencode\tool-output\quarantine-<date>\`) for the first run, purge after 14 days.

### Verification

```powershell
(Get-ChildItem "$env:LOCALAPPDATA\Temp\opencode" -Recurse -File).Count
# Expect: ≈ hundreds (228 fresh + new writes), not 31,217
```

---

## 6. P1-1 — Cache metering fix (`cache_creation` → `tokens_cache_write`)

### Problem

Every recorder writes `cache_write = 0` while `cache_read = 15.21B` (v1) / `0.81B` (v2). Evidence proves it is a recorder/provider mapping gap, not “no cache writes”:

- `session.tokens_cache_write = 0`, `message $.tokens.cache.write = 0`, `step-finish $.tokens.cache.write = 0` — all three ledgers agree on zero.
- Provider usage objects (Anthropic-family) name the write side `cache_creation_input_tokens` (or `cache_creation`), not `cache.write`. The recorder is reading the wrong key and persisting `0`.

### Fix (recorder)

1. In the LLM client / usage normalizer, map:
   - `cache_creation_input_tokens` / `cache_creation` → `tokens_cache_write` **and** `$.tokens.cache.write`
   - `cache_read_input_tokens` / `cache_read` → `tokens_cache_read` **and** `$.tokens.cache.read`
2. Persist the **raw provider usage object** verbatim in `step-finish` (`$.tokens.raw`) so future key renames are diagnosable without a backfill.
3. Add a regression test: synthetic usage `{input:100, cache_read:900, cache_creation:50}` must yield `cache_write=50`, never `0`.
4. Historical data: **do not backfill** `cache_write` from inference — mark history as `cache_write=unknown (pre-fix)`. Recompute the honest metric going forward:

```sql
-- Honest cache metric (works with cache_write=0 history)
-- hit_rate = cache_read / (input + cache_read)
SELECT SUM(tokens_input) AS input_tok,
       SUM(tokens_cache_read) AS cache_read_tok,
       SUM(tokens_cache_write) AS cache_write_tok,
       SUM(tokens_cache_read) * 1.0 / NULLIF(SUM(tokens_input) + SUM(tokens_cache_read),0) AS hit_rate
FROM session;
-- Baseline proof: 15,210,842,514 / (1,699,925,967 + 15,210,842,514) = 0.899 (89.9% of prefix tokens served from cache)
```

### Dashboard change

- Replace any “cache savings / hit-rate” panel that divides by `cache_write` with the `hit_rate` formula above + a `cache_write_coverage = % rows with cache_write>0` gauge (will read `0%` until the recorder fix ships, then climbs — the coverage gauge *is* the fix progress metric).
- Per-agent burn table must show `input + cache_read` (the true token load), not `input` alone.

### Risks / rollback

- **Risk:** mapping a non-Anthropic provider’s `cache_creation` differently (e.g. OpenAI prompt-cache write counters differ). Mitigated by storing `$.tokens.raw` and testing per provider.
- **Rollback:** recorder is forward-only; no schema migration. Revert is a code revert + redeploy, no DB change.

### Verification

| Check | Pass |
|---|---|
| New `step-finish` rows after fix | `$.tokens.cache.write > 0` for cached steps |
| `SUM(tokens_cache_write)` (new sessions only) | `> 0` |
| `hit_rate` | in `0..1`, ≈ `0.9` for long sessions |
| Unit test | ` cache_creation:50 → cache_write:50` |

---

## 7. P1-2 — Tool-output cap at 64 KB (65,536 chars)

### Problem

- Hard limit is already 65,536 bytes in the ripgrep JSON path — `grep` produced `140` “Ripgrep JSON record exceeded 65536 bytes” errors because the cap is enforced as a **failure**, not a **truncation**.
- Tail: `1,641` outputs `>50k`, `5` outputs `>100k`, max `131,055` chars. Mostly `grep` “Found 100 matches (more matches available)” floods over `brand/` + `docs/` + `.opencode/skills/`.

### Design

- Cap **all** tool outputs at **64 KB (65,536 chars)** at the executor boundary (`tool_runner`):
  - `output` stored in `part.data` = first 64 KB + `…[truncated N chars]`
  - Full output (if any) spilled to `tool-output/<tool_call_id>.txt` (existing spill dir) + `$.state.output_ref = "tool-output/<id>.txt"` pointer.
  - `$.state.output_truncated = 1`, `$.state.output_original_length = N` for analytics.
- `grep`/`glob` must request `max_results ≤ 100` and set a server-side `max_output_bytes = 65536` so the JSON record never exceeds the limit.
- Spilled files: summarize-on-write, never re-read verbatim (see also P1-3). The 288× re-read of `tool_14ff7869e0017hJqN3xYM5Lft7` must be impossible after this lands (second read returns the pointer + a `ToolOutputAlreadySummarized` error).

### Backfill (optional, low priority)

Do not rewrite 1,641 historical rows in place. Instead, archive them (§9) — the cold DB retains full fidelity; live DB keeps them until archived.

### Risks / rollback

- **Risk:** an agent needing the truncated tail must re-run the tool with a narrower query — acceptable by design (truncation error message includes the narrowing hint).
- **Rollback:** raise the cap via config (`tool-output.max-bytes`) and redeploy; no DB migration.

### Verification

```sql
-- After deploy, in a 7-day window anchored to MAX(time_created):
SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status')='completed'
  AND length(json_extract(data,'$.state.output')) > 65536;
-- Pass: 0. Pre-fix baseline over full history: 1641 rows > 50k (informational).
SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.state.error') LIKE '%65536%';
-- Pass (new window): 0
```

---

## 8. P1-3 — Hot-file session dedup / context cache

### Problem

- `1,442` files touched >10×; `1,101` read >10×. Top trio re-read on session start:
  `dashboard/api.py 974×`, `company-registry.yaml 763×`, `AGENTS.md 552×`, plus ECL files `summary.md 466×`, `tasks.md 303×`.
- These are **session-start context**, not new information. Re-reading them drives the 15.2B cache-read burn.

### Design

1. **Session-start injection (once):** `AGENTS.md`, `company-registry.yaml`, `docs/STATUS.md`, ECL `summary.md`/`tasks.md`, `harness/evolution/pending.md` (if present) are injected into the system prompt via the memory/recall loop — not re-issued as `read` tool calls.
2. **Per-session read dedup:** within a session, the second `read` of the same `(path, mtime, size)` returns a pointer `{"ref": "<first-read part_id>", "note": "unchanged since mtime ..."}` with zero disk I/O. If `mtime` changed, re-read and overwrite the cache entry.
3. **Cross-session TTL cache (optional):** hash-content cache keyed by `(path, hash)` with 1 h TTL for `company-registry.yaml` / `AGENTS.md` / `brand/tokens.json`. Cache stores the text, not the `part.data`.
4. **Tool-output spill summary:** `tool-output/*` reads return the summary + pointer; direct re-read is rejected with a hint to re-run the producer tool (pairs with §7).

### Target

- `read` ops −30% within 14 days (52,581 baseline → ≤ ~37k per equivalent window).
- Top-10 hot files re-read count −50%.

### Risks / rollback

- **Risk:** stale context if a file changed mid-session and `mtime` granularity misses it — mitigated by also checking `size`; sub-second changes still re-read if `size` differs.
- **Rollback:** config flag `read-dedup.enabled=false`; no DB change.

### Verification

```sql
-- Re-run after 14 days (anchor to new MAX(time_created)):
SELECT json_extract(data,'$.state.input.filePath') AS p, COUNT(*) AS n
FROM part WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='read'
GROUP BY p HAVING n>10 ORDER BY n DESC LIMIT 20;
-- Compare api.py / registry / AGENTS.md counts vs baseline 758 / 655 / 425 (read-only).
-- Pass: each down >= 50%.
```

---

## 9. P2-1 — VACUUM strategy + archive v1 sessions

### Why not bare `VACUUM`

- `freelist_count=1996` (~7.6–8 MB) ⇒ `VACUUM` reclaims at most ~8 MB. Bloat is **live pages**: `part` 670,664 rows + `message` 153,182 rows holding JSON.
- `auto_vacuum=0 (NONE)` ⇒ future deletes also never reclaim without manual `VACUUM` / `incremental_vacuum`.
- Correct strategy: **archive cold v1 sessions → `VACUUM INTO` a compacted primary → switch `auto_vacuum=INCREMENTAL` on the new DB.**

### Archive scope (default)

- v1 `session` where `time_created < 2026-09-01` (≈ 30 days before the v1 tail) **and** `time_archived IS NULL` is *not* the criterion — use age. Estimated majority of 670k parts. Keep:
  - All `session_v2` / `session_message` (live schema, 94 / 9,284 rows).
  - v1 sessions from 2026-09-01→2026-10-22 (63 days) + any session with `parent_id IS NOT NULL` chains touching kept sessions.
  - Mega-sessions (`tokens_input > 5M`) **stay live** (needed for P3 burn analysis) even if old; archive a copy, keep the live row.

### Steps (maintenance window)

```sql
-- 0. Pre-count (dry-run)
SELECT COUNT(*) FROM session WHERE time_created < (strftime('%s','2026-09-01')*1000);
SELECT COUNT(*) FROM part WHERE session_id IN (
  SELECT id FROM session WHERE time_created < (strftime('%s','2026-09-01')*1000));

-- 1. Fresh snapshot copy (see §9.1) — this IS the archive source.
--    Production: sqlite3 "opencode.db" ".backup 'archive/opencode-v1-2026-11-08.db'"

-- 2. In the LIVE db (opencode closed): extract cold sessions to archive db
ATTACH DATABASE 'archive/opencode-v1-2026-11-08.db' AS cold;
-- (Create cold tables via same DDL; then copy row-by-row in FK order:
--  session → message → part → todo → session_part → blob_ref)
-- Recommended: use the applier's ".backup"-then-delete pattern:
--   copy kept rows only into a NEW primary via VACUUM INTO, then swap.

-- 3. Compacted primary (the actual VACUUM)
--    After deleting/archiving cold rows in a CLONE (never deletes on live first):
VACUUM INTO 'opencode.compact.db';
-- Verify:
PRAGMA integrity_check;  -- on compact db, expect ok
PRAGMA page_count; PRAGMA freelist_count;
-- Then (in window): stop opencode, replace opencode.db with opencode.compact.db,
-- keep the §9.1 snapshot as rollback.

-- 4. Future-proofing on the new primary (one-time, before reopening):
PRAGMA page_size = 4096;
PRAGMA journal_mode = WAL;
PRAGMA auto_vacuum = INCREMENTAL;   -- needs the VACUUM INTO rebuild above
PRAGMA incremental_vacuum;          -- reclaim after future deletes
PRAGMA journal_size_limit = 268435456;
```

> **Do not** run `PRAGMA auto_vacuum=INCREMENTAL` on the existing 3 GB file — it is a no-op without a rebuild and will mislead. The rebuild is the step.

### Sizes / expectations

- If cold v1 is ~70% of `part` rows, compacted primary lands at roughly **0.8–1.2 GiB** (estimate only — measure `VACUUM INTO` output; the 12.5 GB `.bak` proves the pre-v2 shape was far larger than live pages, so do not rely on the `.bak` size as a predictor).
- Freelist after compact: `0` (fresh `VACUUM INTO`).

### Risks / rollback

- **Risk:** splitting `parent_id` chains (child in live, parent in cold) breaks tree queries. Mitigated by the chain-closure rule above; verify with:
```sql
SELECT COUNT(*) FROM session c
WHERE c.parent_id IS NOT NULL
  AND c.parent_id NOT IN (SELECT id FROM session)
  AND c.parent_id NOT IN (SELECT parent_id FROM cold.session);
-- Pass: 0 (every parent resolvable in live or cold)
```
- **Risk:** `VACUUM INTO` needs free disk `≥ DB size + WAL`. Pre-flight: `Get-PSDrive` + confirm `> 12 GB` free (3 GB DB + 3 GB WAL + 3 GB compact + 3 GB snapshot) before starting.
- **Rollback:** `opencode.db` is untouched until the swap; the snapshot covers the swap. Keep swap `opencode.db.pre-compact-<ts>` for 30 days.

### Verification (gates — §9.4 table)

---

## 10. P2-2 — Blob migration (144 inline `file` parts → `blob`/`blob_ref`)

### Problem

- `blob 0`, `blob_ref 0`, but `file parts 144` (57 sessions) hold **inline base64** (`outstanding_tasks.md`, `image.png`) in `part.data`. Multi-MB images inflate JSON and prevent dedup.
- `session_part 0` means v2 has no equivalent path yet — migrating v1 files alone is not sufficient; the v2 writer must be fixed (§12).

### Migration (idempotent, dry-run first)

```powershell
# 1. Pseudocode — implement as a Python applier (test on snapshot clone only)
# for each part where json_extract(data,'$.type')='file':
#   payload = extract data_url / b64 field from part.data  # schema probe first
#   bytes = base64_decode(payload)
#   h = sha256(bytes).hexdigest()
#   INSERT OR IGNORE INTO blob(hash, mime, bytes_len, data) VALUES (h, mime, len, bytes)
#   UPDATE part SET data = json_set(data, '$.blob_hash', h, '$.data', NULL_or_pointer)
#   INSERT OR IGNORE INTO blob_ref(session_id, message_id, hash) VALUES (...)
# 2. Second run must be a no-op (count of parts still carrying inline b64 → 0)
```

```sql
-- Probe before writing any code:
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='file';
SELECT substr(data,1,200) FROM part WHERE json_extract(data,'$.type')='file' LIMIT 5;
-- Confirm which JSON key holds the base64 (data_url? mime? bytes?) before coding the migrator.
```

### New-file policy

- All new attachments go to `blob`/`blob_ref` at write time; `part.data` stores the **hash only**. Add a `CHECK (length(data) < 1e6)`-style guard in the writer (not a DB CHECK — JSON is schemaless — enforced in the recorder + a test).
- Dedup is free: same image attached twice = one `blob` row (hash PK).

### Risks / rollback

- **Risk:** migrator misparses the base64 key and destroys the only copy. Mitigated: run on the snapshot clone, `integrity_check` + row-for-row `blob.bytes == decoded length` assertion, then swap.
- **Risk:** `blob` `data` is `BLOB`, not text — backup/restore tools must preserve binary. Verify the `.backup` round-trip on the clone.
- **Rollback:** snapshot restore; migrator is re-runnable (idempotent).

### Verification

```sql
SELECT COUNT(*) FROM blob;       -- expect: <= 144 distinct hashes (files may dedup)
SELECT COUNT(*) FROM blob_ref;   -- expect: 144
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='file'
  AND data LIKE '%data:image%' OR data LIKE '%base64%';
-- expect: 0 remaining inline payloads (after migrator adapts to actual key)
PRAGMA integrity_check;           -- ok
```

---

## 11. P2-3 — Project GC (67 session-less projects)

### Policy

- Delete `project` rows with **zero sessions in `session` and `session_v2`** older than **30 days**, **after** confirming no `worktree`/`project_directory` dependency blocks the delete (FK `ON DELETE` behavior must be probed first).
- Keep: main `9930faf505f3a0275fc48912f28e4e9e96e066c2` (`C:/Users/jmlus/light-speed-holdings`) + `light-speed-holdings-integration` + any project with a live `worktree` row.
- Project sprawl adds new rows eagerly (~10 on 2026-11-03/04 alone) — add a creation guard: `project` is only created when the first `session` is persisted.

### Dry-run

```sql
SELECT p.id, p.directory, p.worktree, p.time_created, p.time_updated,
       (SELECT COUNT(*) FROM session s WHERE s.project_id=p.id) AS v1_sessions,
       (SELECT COUNT(*) FROM session_v2 s WHERE s.project_id=p.id) AS v2_sessions
FROM project p
WHERE NOT EXISTS (SELECT 1 FROM session s WHERE s.project_id=p.id)
  AND NOT EXISTS (SELECT 1 FROM session_v2 s WHERE s.project_id=p.id)
ORDER BY p.time_created;
-- Expect: ~67 rows (72 - 5).
```

### Apply (window, after snapshot)

```sql
-- Probe FK behavior first (do not assume):
PRAGMA foreign_key_list(session);
PRAGMA foreign_key_list(project_directory);
PRAGMA foreign_key_list(worktree);
-- If any FK is RESTRICT and blocks, delete children first or set
-- PRAGMA foreign_keys=OFF in the window transaction (restore ON after).

BEGIN IMMEDIATE;
DELETE FROM project
WHERE NOT EXISTS (SELECT 1 FROM session WHERE project_id=project.id)
  AND NOT EXISTS (SELECT 1 FROM session_v2 WHERE project_id=project.id)
  AND time_created < (strftime('%s','now') - 30*86400) * 1000;
SELECT changes();  -- expect ~67 (baseline; live count may drift)
COMMIT;
```

### Risks / rollback

- **Risk:** deleting a project a queued `todo`/`permission` still references (`permission 29`, `todo 2,771`). The `NOT EXISTS` guard only covers `session`/`session_v2` — re-run the dry-run join for `todo`/`permission`/`worktree` before applying; any hit keeps the project.
- **Rollback:** snapshot restore.

### Verification

```sql
SELECT COUNT(*) FROM project;  -- expect: ~5 (main + integration + 3 others)
SELECT COUNT(*) FROM project p
WHERE NOT EXISTS (SELECT 1 FROM session s WHERE s.project_id=p.id)
  AND NOT EXISTS (SELECT 1 FROM session_v2 s WHERE s.project_id=p.id);
-- expect: 0 (or only projects < 30 days old, by design)
```

---

## 12. P2-4 — Event-sequence GC + v2 writer completion

### Event orphans

- `event 0` vs `event_sequence 3,530` (3,527 in audit — live drift). No events were ever recorded, so sequences are pure ledger noise.
- **Do not delete yet.** First confirm no consumer reads `event_sequence` expecting `event`:
  - Grep the codebase for `event_sequence` / `event\.` joins (the `job`/`schedule`/`session_inbox` tables are also all `0` — the scheduler subsystem has never run).
  - If no reader exists: archive (`.backup` the two tables to cold) then `DELETE FROM event_sequence WHERE aggregate_id NOT IN (SELECT aggregate_id FROM event)` — which, with `event=0`, is **all 3,530 rows**. Keep one cold copy.
- If a reader exists: stop the writers, backfill `event` from `session_message` (the only live event-like stream), then GC.

```sql
-- Dry-run
SELECT COUNT(*) FROM event_sequence es
WHERE NOT EXISTS (SELECT 1 FROM event e WHERE e.aggregate_id = es.aggregate_id);
-- Expect: 3530 (all orphans at baseline)
```

### v2 completion (`session_part 0`)

- The v2 recorder writes `session_message` (9,284) but never `session_part`. Options:
  1. **Complete v2:** make the recorder populate `session_part` from the same `part` payloads (with the §7 cap + §10 blob indirection applied), then cut readers over.
  2. **Freeze v1 as canonical:** document that `message`/`part` remain authoritative and `session_part` is deprecated — stop dual-schema query burden.
- Until the call is made, every audit joins both schemas. **Platform-reliability-engineer must not guess** — escalate to `vp_engineering` for the v2-cutover decision.
- Related: `opencode-.db` (765,952 B, 2026-10-30, v1-shim table list) was **not deep-audited**. Schedule a follow-up audit before deciding whether its data migrates into the archive (§9) or is retired.

### Risks / rollback

- **Risk:** deleting `event_sequence` rows a future auditor needs for sequence reconstruction. Mitigated by cold-archive copy.
- **Rollback:** snapshot / cold copy restore.

### Verification

```sql
SELECT (SELECT COUNT(*) FROM event) AS events,
       (SELECT COUNT(*) FROM event_sequence) AS seqs;
-- After GC (if no reader): events=0, seqs=0, cold copy exists.
-- After v2 completion: session_part > 0 and equals session_message type distribution.
```

---

## 13. P3 — Mega-session budget + token alerts

### Problem

- Top sessions burn `23M input + 377M cache-read` (v1) and `26.8M input` (v2 “Prompt contents”) — each > 10× the median session. `build` dominates v2 (65%).
- Cost ($5.59) is meaningless under free models; token budgets are the only honest signal (Oct-22 directive already knew this).

### Controls

1. **Hard session token budget:** `input + cache_read > 50M` per session → force compaction mid-session, not after next step. Log `compaction` parts (5,444 baseline) as the enforcement signal.
2. **Split rule:** `build` sessions projected > 20M input must be split into subagent tasks at 10M.
3. **Token-based alerts (per agent / per day),** from the honest metric (§6):
```sql
SELECT date(time_created/1000,'unixepoch','localtime') AS d,
       agent,
       SUM(tokens_input + tokens_cache_read) AS tok_load,
       SUM(tokens_cache_write) AS cache_write_tok
FROM session
GROUP BY d, agent
ORDER BY tok_load DESC;
-- Alert: tok_load > 100M / agent / day, or > 500M / day fleet-wide.
-- Include session_v2 in the same view (separate UNION, never summed naively).
```
4. **Dashboard burn table:** per-agent session count, input, cache-read, hit_rate (§6), compaction count.

### Risks / rollback

- **Risk:** over-aggressive compaction degrades long-task quality — threshold is a tuning parameter (`session.budget-tokens`), not a constant in code.
- **Rollback:** config flag; no DB change.

### Verification

- 14 days post-deploy: zero sessions `> 50M` tok_load without a compaction part; per-agent burn table live.

---

## 14. Maintenance window

### 14.1 Duration

- **Estimate 2–4 hours** end-to-end (snapshot 10–20 min at 3 GB + WAL, checkpoint seconds, `VACUUM INTO` 20–60 min, archive copy 20–40 min, verification 15 min). Book **4 hours** with a 1-hour buffer.
- Disk free requirement **before** starting: `> 12 GB` free on the DB volume (DB + WAL + snapshot + compact + archive). `.bak` archive (§3) should land first to satisfy this.

### 14.2 Procedure (ordered, with gates)

| Step | Action | Gate |
|---|---|---|
| 0 | Announce window; stop OpenCode daemon + all writers (`Get-Process opencode` empty) | Writer check |
| 1 | §3 `.bak` archive (if not already done) — frees 38.5 GB | `Get-PSDrive` free > 12 GB |
| 2 | §9.1 fresh snapshot (`opencode.db.pre-fix-<ts>.db`) + `integrity_check=ok` on the **snapshot** | Snapshot hash matches live |
| 3 | §2 `wal_checkpoint(TRUNCATE)` + `journal_size_limit=256MB` | `busy=0`, WAL < 50 MB |
| 4 | §4 orphan sweeper apply (95 rows) | `running+pending=0` |
| 5 | §5 Temp sweeper `-Apply` (7-day cutoff) | Temp count ≈ fresh only |
| 6 | §11 project GC (after FK probe) | `project ≈ 5` new projects blocked at creation |
| 7 | §12 event-sequence archive + GC (only if no reader found) | Cold copy exists; seqs = 0 or documented keep |
| 8 | §9 archive cold v1 → `VACUUM INTO` compact → swap (with pre-compact rollback copy) | `integrity_check=ok`, counts §9.4, swap fallback ready |
| 9 | §10 blob migrator on **clone**, verify, then on primary (or defer to window 2) | `blob_ref=144`, inline payloads = 0 |
| 10 | Reopen OpenCode; smoke test: new session, new tool call, `wal_checkpoint(PASSIVE)` | New `step-finish` rows, WAL stable |
| 11 | §6/§7/§8 recorder deploys (code, not DB) + regression tests | §6–§8 verification tables |
| 12 | 14-day re-audit (this report as baseline) | Gaps table below |

Steps 9 (blob) and the §9 archive swap may be split into a **second window** if disk/time is tight — steps 0–7 alone reclaim ~38.5 GB + ~31k temp files and are fully reversible.

### 14.3 Rollback plan

- **Any step:** abort window, OpenCode stays closed. DB files are either untouched (steps 1–7 are on the snapshot/clone or idempotent JSON updates) or restored from:
  - Pre-fix snapshot: `~/.local/share/opencode/opencode.db.pre-fix-<ts>.db` (step 2)
  - Pre-compact copy: `~/.local/share/opencode/opencode.db.pre-compact-<ts>.db` (step 8)
  - `.bak` archive: cold-storage path in §3
- **Verification after any rollback:** `PRAGMA integrity_check = ok` + full counts (§9.4) match the pre-window snapshot ± live drift documented at window start (record the actual counts — do not reuse this report's baseline, the DB is live).
- **Never** delete `-wal` / `-shm` manually as a “rollback” — that *is* data loss if the WAL holds uncheckpointed frames.

---

## 15. Verification matrix (gates for closing the window)

### 15.1 PRAGMAs

```sql
PRAGMA page_size;            -- 4096 (unchanged)
PRAGMA page_count;           -- post-compact expected: much lower (report actual)
PRAGMA freelist_count;       -- pre: 1996; post-compact: 0
PRAGMA journal_mode;         -- wal
PRAGMA auto_vacuum;          -- pre: 0 (NONE); post-compact: 2 (INCREMENTAL)
PRAGMA journal_size_limit;   -- 268435456 (256 MB)
PRAGMA integrity_check;      -- ok (REQUIRED, no exceptions)
PRAGMA wal_checkpoint(TRUNCATE);  -- busy=0 (REQUIRED)
```

### 15.2 Counts (record actuals at window start and after each step)

```sql
SELECT 'session='||(SELECT COUNT(*) FROM session) ||
       ' session_v2='||(SELECT COUNT(*) FROM session_v2) ||
       ' message='||(SELECT COUNT(*) FROM message) ||
       ' part='||(SELECT COUNT(*) FROM part) ||
       ' session_message='||(SELECT COUNT(*) FROM session_message) ||
       ' session_part='||(SELECT COUNT(*) FROM session_part) ||
       ' project='||(SELECT COUNT(*) FROM project) ||
       ' todo='||(SELECT COUNT(*) FROM todo) ||
       ' event='||(SELECT COUNT(*) FROM event) ||
       ' event_sequence='||(SELECT COUNT(*) FROM event_sequence) ||
       ' blob='||(SELECT COUNT(*) FROM blob) ||
       ' blob_ref='||(SELECT COUNT(*) FROM blob_ref);
-- Orphans:
SELECT json_extract(data,'$.state.status') AS st, COUNT(*)
FROM part WHERE json_extract(data,'$.type')='tool' GROUP BY st;
-- Expect: running=0, pending=0, error=3530 (baseline 3435+95), completed=185183
```

### 15.3 Filesystem

```powershell
Get-ChildItem "$env:USERPROFILE\.local\share\opencode\opencode.db*" |
  Select-Object Name, @{n='GB';e={[math]::Round($_.Length/1GB,2)}}, LastWriteTime
(Get-ChildItem "$env:LOCALAPPDATA\Temp\opencode" -Recurse -File).Count
# Expect: WAL < 0.05 GB; .bak total < 2× DB; Temp count ≈ hundreds.
```

### 15.4 Post-deploy (code fixes)

| Task | Gate (14 days after deploy) |
|---|---|
| §6 cache metering | `cache_write>0` on new sessions; `hit_rate` sane; coverage gauge climbing |
| §7 output cap | 0 outputs > 65,536 chars; 0 “65536” errors in window |
| §8 dedup | Top-10 hot-path reads −50% vs 758/655/425 baseline |
| §13 budget | 0 sessions > 50M tok_load without compaction |

---

## 16. Risks — consolidated

| Risk | Steps | Mitigation |
|---|---|---|
| `VACUUM INTO` runs out of disk mid-run | §9 | Pre-flight `>12 GB` free; archive `.bak` first (§3); `VACUUM INTO` writes a *new* file, live DB untouched |
| Checkpoint blocks on live reader | §2 | Writer check at gate 0; `busy=1` is safe/retryable — never delete WAL |
| Orphan flip races a still-running worker | §4 | 1 h / 24 h TTL; baseline orphans are days old |
| Blob migrator corrupts payloads | §10 | Run on clone; byte-length assertion; idempotent re-run |
| Project GC deletes referenced project | §11 | FK probe + joins on `todo`/`permission`/`worktree` before apply |
| Event-sequence GC removes needed data | §12 | Cold-archive copy; reader grep first |
| Cache-fix mapping wrong per provider | §6 | Store `$.tokens.raw`; per-provider tests |
| Truncation breaks an agent needing the tail | §7 | Spill file + re-run hint; cap is configurable |
| Stale context via dedup `mtime` miss | §8 | Check `size` too; TTL cache off by default |

---

## 17. What to escalate

- **v1-vs-v2 canonical decision** (§12, `session_part 0`): architecture — `vp_engineering`.
- **`subagent_depth` (40× + reproduced in audit):** not a DB fix; orchestrator-class agents need a raised depth or direct-work carve-out — `vp_engineering`.
- **`rg` missing (474×), PowerShell antipatterns (1,500+), `edit` semantic failures (816):** agent-runtime fixes, not storage — `platform-engineer` / `cto`.

---

## 18. Tasks for the executor (prioritized checklist)

- [ ] **T1** Announce window; stop writers; pre-flight disk > 12 GB (owner: platform-reliability-engineer, window gate 0/1)
- [ ] **T2** Archive `opencode.db.bak` 38.5 GB → cold storage; install retention sweeper (§3, P0-2)
- [ ] **T3** Fresh snapshot `.backup` + `integrity_check` on snapshot (§9.1, gate 2)
- [ ] **T4** `wal_checkpoint(TRUNCATE)` runbook + `journal_size_limit=256MB` + 5-min PASSIVE cadence (§2, P0-1)
- [ ] **T5** Orphan sweeper dry-run → apply (95 rows, `error` + `$.state.orphaned=1`) + 15-min `orphaned_tool_calls` metric (§4, P0-3)
- [ ] **T6** Temp 7-day sweeper `-Apply` + weekly schedule (§5, P0-4)
- [ ] **T7** Cache metering: map `cache_creation` → `cache_write`, persist `$.tokens.raw`, fix dashboards to `hit_rate` formula, add regression test (§6, P1-1, owner: llm-platform-owner)
- [ ] **T8** Tool-output cap 64 KB at executor boundary + `grep` max-results; spill + summary (§7, P1-2)
- [ ] **T9** Hot-file session dedup + session-start injection (§8, P1-3)
- [ ] **T10** Archive cold v1 (< 2026-09-01) → `VACUUM INTO` compact → swap; set `auto_vacuum=INCREMENTAL` (§9, P2-1)
- [ ] **T11** Blob migrator clone→primary; `part.data` stores hash only (§10, P2-2)
- [ ] **T12** Project GC (~67 rows) + creation guard (§11, P2-3)
- [ ] **T13** Event-sequence archive + GC; v2-cutover decision; `opencode-.db` follow-up audit (§12, P2-4, needs `vp_engineering` call)
- [ ] **T14** Mega-session 50M token budget + per-agent token alerts (§13, P3)
- [ ] **T15** 14-day re-audit against §15 matrix; close or re-file gaps

---

*Prepared as plan only. No database was modified. All counts, sizes, and SQL above trace to `reports/opencode-db-audit-2026-11-08.md` and `reports/opencode-db-analytics-2026-11-08.md` (live-DB drift ±3 sessions / ±3 event_sequence noted in both sources). Restore/rollback artifacts named in §14.3 must exist before any `UPDATE`/`DELETE`/`VACUUM` runs.*
