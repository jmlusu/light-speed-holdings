# opencode.db Audit — 2026-11-08

**Auditor:** chief-of-staff (primary orchestrator) for LightSpeed Holdings
**Working directory:** `C:\Users\jmlus\light-speed-holdings`
**Database audited (read-only):** `C:\Users\jmlus\.local\share\opencode\opencode.db`
**Audit date (local):** 2026-11-08 ~13:58–14:20
**Method:** `sqlite3 -readonly` only + `memory-search` skill SQL templates. **No writes to the database.** This report is the only artifact created by the audit (inside the workspace).

> **Read-only compliance:** Every `sqlite3` invocation used `-readonly`. No `DELETE/UPDATE/INSERT/VACUUM` was issued against `opencode.db`. Filesystem checks were `Get-ChildItem`/`Test-Path` only. The live DB grew during the audit (new sessions at 13:58:45 + 14:03–14:15), so row counts are a point-in-time snapshot; variances of +1–3 sessions between queries are expected live-DB drift, not errors. The `opencode-.db` (765,952 bytes) was checked for `.tables` only.

---

## 1. Locate — where is opencode.db?

| Candidate path | Exists | Size / date (evidence) |
|---|---|---|
| `C:\Users\jmlus\light-speed-holdings` repo root (`*.db` recurse) | No `opencode.db` at root | Only test DBs: ~200× `test.db`/`test_pipeline.db`/`ai_company.db` (327,680 B each) under `.pytest_tmp_local/.pytest_tmp_targeted/.pytest_tmp_ci`, plus `data\ai_company.db` (323,584 B). No trajectory DB at root. |
| `~\.local\share\mimocode\mimocode.db` (`C:\Users\jmlus\.local\share\mimocode\mimocode.db`) | **False** | — |
| **`~\.local\share\opencode\opencode.db`** (`C:\Users\jmlus\.local\share\opencode\opencode.db`) | **TRUE — audited** | **3,222,466,560 B (~3.00 GiB / 3.22 GB)**, `LastWriteTime 2026-11-08 13:59:02` → `14:13:15` during audit (live). `CreationTime 2026-08-05 21:38:37`. |
| `~\.local\share\opencode\opencode-.db` | TRUE (secondary) | 765,952 B, `2026-10-30 09:30:53`. Tables: `account, account_state, control_account, credential, data_migration, event, event_sequence, message, migration, part, permission, project, project_directory, session, session_context_epoch, session_input, session_message, session_share, todo, workspace` (v1-shim / stale). Not re-audited in depth. |
| `~\.config\opencode\opencode.db` | False | — |
| `%APPDATA%\mimocode\mimocode.db`, `%APPDATA%\opencode\opencode.db` | False | — |
| `%LOCALAPPDATA%\mimocode\mimocode.db`, `%LOCALAPPDATA%\opencode\opencode.db` | False | — |
| `C:\Users\jmlus\AppData\Local\Temp\opencode\opencode.db` | False | — |
| `MIMOCODE_DB` / `OPENCODE_DB` env | Empty | `sqlite3 3.50.4` confirmed. |

**Companion files in `~\.local\share\opencode\` (same dir, bare `opencode*` listing):**

| File | Bytes | GB | LastWrite |
|---|---|---|---|
| `opencode.db` | 3,222,466,560 | 3.00 GiB (3.22 GB) | 2026-11-08 14:13:15 (live) |
| `opencode.db-wal` | 3,163,682,112 | 2.95 GiB (3.16 GB) | 2026-11-08 14:13:22 (live, grows during audit) |
| `opencode.db-shm` | 98,304 | — | 2026-11-08 14:06:05 |
| `opencode.db.bak` | **38,533,844,992** | **35.89 GiB (38.5 GB)** | 2026-11-01 16:56:41 |
| `opencode-.db` | 765,952 | — | 2026-10-30 |
| `opencode-.db-wal` | 980,592 | — | 2026-10-30 |
| `opencode-.db-shm` | 32,768 | — | 2026-11-08 14:03:09 |
| `auth.json` / `mcp-auth.json` / `log/` / `storage/` / `tool-output/` / `worktree/` / `repos/` / `shell/` | — | — | Various Sep–Nov 2026 |

**Effective on-disk footprint of the live DB ≈ 6.4 GB (DB + WAL), plus a 38.5 GB `.bak` backup = ~44.9 GB.** WAL is ~98% the size of the DB — checkpoint is severely behind (see §7, P1).

**Projects in DB:** 72 `project` rows. Main project `9930faf505f3a0275fc48912f28e4e9e96e066c2` → `C:/Users/jmlus/light-speed-holdings` (created 2026-08-06 17:59:56, updated 2026-10-27 13:38:37). Second: `light-speed-holdings-integration`. Remainder (70) are worktree/temp projects (e.g. `C:/tmp`, `~/.local/share/opencode/worktree/9930fa/*`, `~/.config/opencode`, `AppData/Local/Temp/opencode/uploads/*`). Only 5 distinct `project_id`s ever had `session` rows (worktree projects were created without sessions).

---

## 2. Schema, size, integrity

**Pragmas (proof):**

```sql
PRAGMA page_size;      -- 4096
PRAGMA page_count;     -- 786735  (= 786735*4096 ≈ 3.22 GB, matches file size)
PRAGMA freelist_count; -- 1996     (~8 MB free — bloat is live pages, not free pages)
PRAGMA journal_mode;   -- wal
PRAGMA user_version;   -- 0
PRAGMA schema_version; -- 101
PRAGMA encoding;       -- UTF-8
PRAGMA auto_vacuum;    -- 0 (NONE — no auto reclaim)
```

**Integrity:** `PRAGMA integrity_check;` → **`ok`**. Quick structure intact; the problem is size/GC, not corruption.

**Tables (30):** `.tables` →

```text
account  instruction_blob  permission       session_share
account_state  instruction_entry  project        session_v2
blob  instruction_state  project_directory  todo
blob_ref  job  schedule  workspace
control_account  kv  session  worktree
credential  message  session_inbox
event  migration  session_message
event_sequence  part  session_part
```

Full DDL dump captured via `SELECT sql FROM sqlite_master WHERE type='table'` (see Appendix A). Highlights:

- `session` (v1): `id, project_id, workspace_id, parent_id, slug, directory, path, title, version, share_url, summary_*, metadata, cost, tokens_input/output/reasoning/cache_read/cache_write, revert, permission, agent, model, time_created/updated/compacting/archived` + FK to `project`.
- `session_v2` (v2): same + `fork_session_id, fork_boundary, time_suspended, resume_attempts, time_idle/viewed/busy, idle_outcome` — the active schema since 2026-11-01.
- `message`: `id, session_id, time_created/updated, data` (`$.role`, `$.agent`, `$.mode`, `$.modelID`, `$.tokens`, `$.path.cwd`) + FK to `session`.
- `part`: `id, message_id, session_id, time_created/updated, data` (`$.type`, `$.tool`, `$.state.status/input/output/error`) + FK to `message`.
- `session_message` / `session_part`: v2 equivalents (`session_part` currently **0 rows** — v2 does not yet populate parts via this path).
- `blob(hash, mime, bytes, width, height, data)` + `blob_ref(session_id, message_id, hash, seq)` — attachments store (currently **0 rows**, see §5 links).
- `event(aggregate_id, seq, type, data, created)` + `event_sequence(aggregate_id, seq, owner_id)`, `job`, `schedule`, `session_inbox`, `todo(session_id, content, status, priority, position)`, `permission`, `project_directory`, `worktree`, `kv`, `migration`, `credential`, `instruction_*`, `account*`.

**Indexes (30 explicit + autoindexes):** present and sensible — e.g. `message_session_time_created_id_idx`, `part_message_id_id_idx`, `part_session_idx`, `session_project_idx`, `session_parent_idx`, `session_v2_parent/project/time_suspended/workspace_idx`, `session_message_session_seq/time_created/type_seq_idx`, `event_aggregate_seq/type_seq_idx`, `job_session/child_session/id_idx`, `schedule_due/session_idx`, `blob_ref_hash/session_seq_idx`, `permission_project_action_resource_idx`. No missing-index cliff on the hot joins; full table scans in this audit were `COUNT(*)`/`GROUP BY` over `part` (670k rows) which completed in seconds-to-minutes — indexes are not the bottleneck; **JSON extraction + WAL size** are.

**Migrations:** 59 `migration` rows, latest `20261030054400_job` (2026-10-30 22:34:07). `kv.migration.v1-v2 = {"phase":"completed"}` — v1→v2 migration is complete declaratively, but both `session`/`message`/`part` (v1, frozen 2026-10-22) and `session_v2`/`session_message` (v2, live from 2026-11-01) coexist. `opencode.db.bak` (38.5 GB, 2026-11-01) predates the v2 switchover and is almost certainly a pre-migration snapshot that was never pruned.

### Row counts (proof snapshot)

```sql
-- small tables
SELECT 'account='||(SELECT COUNT(*) FROM account) ...
-- account=0, account_state=0, blob=0, blob_ref=0, control_account=0,
-- credential=22, event=0, event_sequence=3527, instruction_blob=264,
-- instruction_entry=0, instruction_state=363, job=0, kv=5, migration=59,
-- permission=29, project=72, project_directory=7, schedule=0,
-- session_share=0, todo=2771, workspace=0, worktree=7

-- large tables
SELECT 'session='||(SELECT COUNT(*) FROM session) ...
-- session=3131, session_v2=91 (→92→94 during audit, live),
-- message=153182, part=670664,
-- session_message=9161, session_part=0, session_inbox=0
```

| Table | Rows | What it means |
|---|---|---|
| `session` (v1) | 3,131 | Frozen 2026-08-05 → 2026-10-22 12:59:05 |
| `session_v2` (v2) | 91–94 (live) | Live 2026-11-01 17:12:01 → 2026-11-08 13:58:45+ |
| `message` (v1) | 153,182 | assistant 133,944 / user 19,238 |
| `part` (v1) | 670,664 | tool 188,713; step-start 135,963; step-finish 132,342; reasoning 119,892; text 73,820; patch 13,579; compaction 5,444; agent 767; file 144 |
| `session_message` (v2) | 9,161 | assistant 8,068; idle 475; user 474; system 170; model-switched 74; synthetic 50; compaction 22; location-switched 11; agent-switched 8 |
| `session_part` (v2) | 0 | v2 not mirroring parts here yet |
| `event` / `blob` / `blob_ref` / `job` / `account*` / `schedule` / `session_inbox` / `session_share` | 0 | Stub / not-yet-used subsystems (see §7) |
| `event_sequence` | 3,527 | Aggregate sequence ledger intact |
| `todo` | 2,771 | completed 2,039 / pending 550 / in_progress 177 / cancelled 2 / +3 custom statuses |
| `instruction_state` | 363 | Matches ~363 v2-era sessions |
| `credential` | 22 | Live credentials (do not dump values) |
| `permission` | 29 | shell 27 / edit 1 / read 1 |
| `project` | 72 | 5 with sessions; 67 worktree/temp (mostly session-less) |
| `kv` | 5 | `migration.v1-v2`, `websearch:provider="random"`, `models-dev:v2:catalog(+meta)`, `plugin:…:model-has-image-support` |

**Sessions per day (v1 tail):** 2026-10-22:27, 10-21:77, 10-20:73, 10-19:6, 10-18:46, 10-17:45, 10-16:56, 10-15:20, 10-14:88, 10-13:42, 10-12:40, 10-11:37, 10-10:119, 10-09:46, 10-08:42, 10-07:102, 10-06:29, 10-05:46, 10-04:52, 10-03:54 (mid-Oct peak 119/day). **V2 per day:** 11-08:29 (partial day, includes this audit), 11-07:1, 11-06:12, 11-04:13, 11-03:12, 11-02:11, 11-01:16 (v2 ramp-up).

---

## 3. Trajectory analysis (sessions, messages, parts, tool calls)

### 3.1 Sessions & agents

**V1 agents (`session.agent`, top):** `build 876, explore 357, general 235, plan 133, chief-of-staff 123, qa-lead 76, backend-engineer 70, cto 64, frontend-engineer 56, lead-frontend 49, ceo-advisor 47, test-engineering-lead 40, devops-lead 39, senior-frontend-engineer 37, product-designer 35, technical-documentation-lead 34, senior-backend-engineer 30, memory-owner 29, dashboard-owner 29, cmo 29` (…40+ agents total).

**V2 agents (`session_v2.agent`, current):** `build 61, general 6, senior-backend-engineer 5, test-engineering-lead 3, explore 3, cto 2, thought-leadership-author 1, sales 1, qa-lead 1, product-marketing-manager 1, plan 1, market-analyst 1, lead-backend 1, default 1, creative-director 1, ciso 1, chief-of-staff 1, board-strategy 1, ai-safety-lead 1, agentic-policy-analyst 1, …` — `build` still dominates (61/94 ≈ 65%).

**Main-project concentration:** `project_id='9930faf5…' (light-speed-holdings)` → **2,814 of 3,131 v1 sessions (89.9%)**. V2: 92 of 94 sessions are the main project (remaining 2 in `1c15ac8c…` worktree). This DB is effectively a single-project trajectory warehouse — cross-project contamination risk is low, but session explosion is real.

**Recent V2 sessions (proof, `ORDER BY time_created DESC LIMIT 8`):**

```text
2026-11-08 14:15:13 | Run first real Desktop sync            | general
2026-11-08 14:13:52 | Fix D10 IntegrityError race            | senior-backend-engineer
2026-11-08 14:03:47 | P1 purge dummy and guard               | general
2026-11-08 14:03:47 | Fix defects D4-D12 in tracker          | senior-backend-engineer
2026-11-08 14:03:47 | Fix D6 D7 and wire SQLite sync         | lead-backend
2026-11-08 13:58:45 | Security audit opencode.db             | ciso
2026-11-08 13:58:45 | Locate and map opencode.db             | explore
2026-11-08 13:58:45 | Deep audit analytics opencode.db       | general
```

**Recent V1 sessions:** `2026-10-22 12:59:05 | New session - 2026-10-22T… | build` (×3 auto-titled), `2026-10-22 11:34:19 | Explore project structure (@explore subagent) | explore`, `2026-10-22 11:33:14 | DIRECTIVE: Fix agent session token burn and summary drift | build` — the Oct-22 directive corroborates the burn visible in §4.

### 3.2 Messages & parts

- `message` roles: `assistant 133,944 (87.4%), user 19,238 (12.6%)`. No `system` in v1; v2 `session_message` adds `system 170, idle 475, model-switched 74, synthetic 50, compaction 22`.
- **Part types (670,664):** `tool 188,713 (28.1%) | step-start 135,963 | step-finish 132,342 | reasoning 119,892 (17.9%) | text 73,820 (11.0%) | patch 13,579 (2.0%) | compaction 5,444 | agent 767 | file 144`.
- **Compaction pressure:** 5,444 compaction parts in v1 + 22 v2 compaction messages. With 132k step-finishs, ~4% of steps triggered compaction — long-running sessions are the norm, not the exception (see top-token sessions below).
- **File parts (144 across 57 sessions):** inline data-URL attachments (e.g. `outstanding_tasks.md` base64, `image.png` base64). These predate the `blob`/`blob_ref` store (both 0 rows) — attachments live in `part.data`, not in blob storage. That is a size driver: base64 images inline in JSON.
- **Patch parts (13,579 across 814 sessions):** `{"type":"patch","hash":"…","files":["C:/Users/jmlus/light-speed-holdings/.gitignore", …]}` — the ground truth for *what files changed per session*. `patch` coverage (814 sessions) is far broader than `session.summary_files` alone.

### 3.3 Tool calls (188,713 v1 tool parts)

**By tool (top):**

```text
bash 78,923 | read 52,581 | edit 16,540 | grep 15,156 | glob 11,810 |
write 5,315 | todowrite 2,959 | task 2,051 | websearch 830 | webfetch 745 |
question 545 | skill 526 | agents_list_threads 153 | agents_session_search 107 |
invalid 78 | agents_assignment_status 77 | agents_coordinate_bots 32 | agents_vm_exec 19 | …
```

**By status (188,713):** `completed 185,183 (98.1%) | error 3,435 (1.8%) | running 93 | pending 2`. `running 93` + `pending 2` are **orphaned in-flight markers** (no completion written) — see §7 P6.

**Tool × status (key, proof excerpt):**

```text
bash     completed 78,506 | error 387 | running 30
read     completed 51,621 | error 959 | running 1
edit     completed 15,591 | error 949
grep     completed 14,960 | error 196
glob     completed 11,585 | error 225
write    completed 5,249  | error 63  (of 5,315 total)
task     (see below) completed 2,149 | error 377 | running 51 (task+skill combined 2,577)
webfetch completed ~643 | error 102   websearch completed ~771 | error 59
todowrite error 10         question completed 517 | error 18 | running 10
agents_coordinate_bots completed 16 | error 16 (50% fail)
agents_show_widget error 11 | completed 3 (79% fail)
agents_propose_team_memory completed 11 | error 8
agents_assignment_status completed 70 | error 7
invalid completed 77 | error 1
```

Error-rate hotspots: `agents_coordinate_bots 50%`, `agents_show_widget 79%`, `computer_*` mostly n≤7 (noise), `agent-memory/propose` ~40%. Core file tools are healthy by comparison (`read 1.8%, edit 5.7%, bash 0.5%, grep 1.3%, glob 1.9%`).

Full `tool × status` dump (80 rows) and `tool` leaderboard (30 rows) are in Appendix B.

---

## 4. Tokens, cost & cache

### 4.1 Totals (proof)

```sql
SELECT COUNT(*), SUM(cost), SUM(tokens_input/output/reasoning/cache_read/cache_write)
FROM session;
-- 3131 | 5.591125755 | 1699925967 | 65346163 | 34073428 | 15210842514 | 0
SELECT COUNT(*), SUM(...) FROM session_v2;
-- ~94 (live) | 0.1304107902 | 83294817 | 1826476 | 1477855 | 809948648 | 0
SELECT COUNT(*), SUM(cost), SUM(tokens_input/output) FROM session
WHERE project_id='9930faf5…';
-- 2814 | 5.591125755 | 1538653924 | 59150548
```

- **All v1 cost sits in the main project** (5.5911 of 5.5911). The other 317 v1 sessions cost **$0.00** — free-provider sessions.
- **Last-7-days-of-available-data (to `MAX(time_created)`, not `now`, because v1 is frozen 2026-10-22):** 347 sessions, input 279,872,253, cache-read 1,875,630,618. `now`-relative 7-day query correctly returns 0 for v1.
- **Step-finish cross-check matches exactly:** `SUM(tokens.input)=1,699,925,967`, `SUM(cache.read)=15,210,842,514`, `SUM(cache.write)=0` over 132,342 step-finish parts — identical to the `session` column sums. The two ledgers are consistent.

### 4.2 Cache reads — the headline number

| Scope | `tokens_input` | `tokens_cache_read` | `tokens_cache_write` | Cache-read / input |
|---|---|---|---|---|
| `session` (all v1, 3,131) | 1,699,925,967 | **15,210,842,514** | **0** | **8.95×** |
| `session_v2` (live, ~94) | 83,294,817 | **809,948,648** | **0** | **9.72×** |
| v1 last-7d-of-data (347) | 279,872,253 | 1,875,630,618 | 0 | 6.70× |
| `step-finish` aggregate | 1,699,925,967 | 15,210,842,514 | 0 | 8.95× |

**Cache reads are detectable and massive (15.2B tokens), but `cache_write` is 0 everywhere** — in both the `session` columns *and* per-step `step-finish` JSON (`{"cache":{"write":0,"read":2048}}` samples). This is a **provider metering quirk, not an audit artifact**: the provider reports `cache.read` but never reports `cache.write`. You cannot compute a true cache hit-rate from `cache_write`; you can only report `cache_read` volume. Budgeting that assumes `cache_write>0` will misread this DB. Samples below show per-step reads of 2,048–8,704 tokens on tiny inputs (73–6,700), i.e. reads exceed live input — classic prefix-cache reuse on long sessions.

**Per-session cache burns (v1 top by input):**

```text
ses_f1ad097c… | Athena Implementation 28 September 2026        | 2026-09-28 | in 23,135,370  out 135,754  cache-r 377,687,040 | cost 0.00 | nemotron-3.5-lightning-free
ses_eb6b27c0… | Web App Re-Deployment                            | 2026-10-17 | in 19,005,330  out 96,439   cache-r 38,899,584  | cost 0.00 | mimo-v2.6-flash-free
ses_f1b449f9… | ATHENA Roadmap Step 2                              | 2026-09-27 | in 15,660,074  out 210,140  cache-r 123,389,536 | cost 0.00 | mimo-v2.6-flash-free
ses_f2a05aab… | Website Rebuild                                    | 2026-09-25 | in 15,529,616  out 246,781  cache-r 159,150,400 | cost 0.00 | nemotron-3.5-lightning-free
ses_eb651042… | Milestones                                         | 2026-10-17 | in 13,421,861  out 56,949   cache-r 20,454,624  | cost 0.00 | mimo-v2.6-flash-free
ses_f01fa228… | OCI/VPS Inquiry                                    | 2026-10-02 | in 12,854,781  out 244,140  cache-r 146,366,432 | cost 0.00 | nemotron-3-ultra-free
… (8 more ≥11M input, several with >66M cache-read; one Ollama session out >1.2M)
```

**V2 top by input (current era):**

```text
ses_e584330d… | Prompt contents                         | 2026-11-04 | in 26,836,564 out 340,484 cache-r 132,773,289 | cost 0.00
ses_e681e8c6… | LightSpeed home redesign session 9      | 2026-11-01 | in  2,619,021 out 102,104 cache-r  48,800,666 | cost 0.022
ses_e67b9ee6… | LightSpeed solutions index and detail   | 2026-11-01 | in  2,530,168 out  63,436 cache-r  42,737,050 | cost 0.021
ses_e44f4ec2… | Fix defects D4-D12 in tracker           | 2026-11-08 | in  2,530,043 out   9,668 cache-r          0 | cost 0.00  (cache-r 0 — fresh/small context)
ses_e4e769cf… | Monorepo duplicate artifacts            | 2026-11-06 | in  2,227,748 out  36,787 cache-r  33,079,072 | cost 0.00
… (5 more ≥1.8M input)
```

Single sessions exceed 23M input + 377M cache-read tokens. **Token burn is concentrated in a handful of mega-sessions** while cost stays ~$5.59 because most traffic is free-tier models (`nemotron-3.5-lightning-free 815, mimo-v2.6-flash-free 542, nemotron-3-ultra-free 345, big-pickle 898+121, mimo-v2.5-free 137` in v1; `nemotron-3.5-lightning-free 49, crouton-alpha-free 25, deepseek-v4.1-flash-free 9` in v2). Paid outlier: `Athena - Build 20 September 2026` cost $1.925 on `big-pickle` is the single largest cost line — cost and tokens are decoupled under free models, which hides burn from cost dashboards.

### 4.3 Models (v1 vs v2 shift)

- V1: `big-pickle 898+121, nemotron-3.5-lightning-free 815, mimo-v2.6-flash-free 542, nemotron-3-ultra-free 345, mimo-v2.5-free 137, longcat-2.5-preview-free 21, auto/best-free (omniroute) 19, muse-spark 1.3/1.2 34, laguna-s-2.1 43, deepseek-v4.1 11, oc/mimo-v2.5 (omniroute) 10, …`
- V2: `nemotron-3.5-lightning-free 49, crouton-alpha-free 20+5, deepseek-v4.1-flash-free (max) 9, auto/coding (omniroute, high) 3, nemotron-3.5-lightning-free (default) 2, big-pickle 2, grok-4.6 (xai, low) 1, auto/multimodal 1, …` — **Crouton Alpha era begins in v2** (25 sessions), nemotron-lightning remains the default.

---

## 5. Files — inspected, created, modified, re-read

Extraction key: `json_extract(part.data,'$.state.input.filePath')` for `read/edit/write`. `grep`/`glob` `path` fields are directories/patterns, counted separately (see §5.4). Bash file writes have no structured path field.

### 5.1 Totals (proof)

```sql
SELECT COUNT(DISTINCT lower(filePath)), COUNT(*) FROM part
WHERE tool IN ('read','edit','write') AND filePath IS NOT NULL;
-- 9361 distinct files | 74310 ops
-- read  52581 ops | 7135 distinct
-- edit  16540 ops | 2560 distinct
-- write  5315 ops | 4260 distinct
```

- **Files inspected (any filePath op): 9,361 distinct / 74,310 ops** (read 52,581 + edit 16,540 + write 5,315). With `grep` (15,156) and `glob` (11,810) directory searches, total file-touching tool calls = **101,276**.
- **Files created (write completed): 5,249 ops** (distinct paths not directly distinguished from overwrites by the tool name; `write` distinct = 4,260).
- **Files modified (edit completed): 15,591 ops** (distinct = 2,560).
- **Completed create+modify = 20,840 ops.** `patch` parts corroborate: **13,579 patches across 814 sessions** (subset that recorded a patch hash; not all edits emit a patch part).
- **Read errors:** `read` error 959 (see §6).

### 5.2 Files read >10 times (hot files)

```sql
SELECT lower(filePath), COUNT(*) FROM part WHERE tool IN ('read','edit','write')
GROUP BY 1 HAVING COUNT(*)>10 ORDER BY 2 DESC;  -- 1442 files
SELECT COUNT(*) FROM (… read-only GROUP BY … HAVING >10);  -- 1101 files
```

- **1,442 distinct files touched >10 times** (any of read/edit/write); **1,101 files read >10 times** (read-only threshold).
- **Top 40 (proof, lowercased):**

```text
974 | c:\users\jmlus\light-speed-holdings\src\ai_company\dashboard\api.py
763 | c:\users\jmlus\light-speed-holdings\company-registry.yaml
552 | c:\users\jmlus\light-speed-holdings\agents.md
466 | c:\users\jmlus\light-speed-holdings\harness\changes\active\summary.md
452 | c:\users\jmlus\light-speed-holdings\docs\status.md
446 | c:\users\jmlus\light-speed-holdings\src\ai_company\dashboard\static\js\app.js
416 | c:\users\jmlus\light-speed-holdings\src\app.tsx
398 | c:\users\jmlus\light-speed-holdings\src\components\floatingnav.tsx
395 | c:\users\jmlus\light-speed-holdings                          (directory read)
392 | c:\users\jmlus\light-speed-holdings\src\data\sitecontent.ts
378 | c:\users\jmlus\light-speed-holdings\src\ai_company\dashboard\app.py
336 | c:\users\jmlus\light-speed-holdings\src\ai_company\executor\loop.py
303 | c:\users\jmlus\light-speed-holdings\harness\changes\active\tasks.md
288 | c:\users\jmlus\.local\share\opencode\tool-output\tool_14ff7869e0017hjqn3xym5lft7  (tool-output spill!)
257 | c:\users\jmlus\light-speed-holdings\src\ai_company\model_router.py
255 | c:\users\jmlus\light-speed-holdings\src\ai_company\generator.py
249 | c:\users\jmlus\light-speed-holdings\src\ai_company\executor\agent_loop.py
241 | c:\users\jmlus\light-speed-holdings\src\pages\homepage.tsx
238 | c:\users\jmlus\light-speed-holdings\package.json
226 | c:\users\jmlus\light-speed-holdings\src\ai_company\orchestrator\message_bus.py
222 | c:\users\jmlus\light-speed-holdings\docs\ecl.md
220 | c:\users\jmlus\light-speed-holdings\.github\workflows\ci.yml
213 | c:\users\jmlus\light-speed-holdings\vite.config.ts
204 | c:\users\jmlus\light-speed-holdings\readme.md
202 | c:\users\jmlus\light-speed-holdings\src\components\herosection.tsx
202 | c:\users\jmlus\light-speed-holdings\src\ai_company\dashboard\templates\index.html
200 | c:\users\jmlus\light-speed-holdings\src\ai_company\dashboard\data_service.py
197 | c:\users\jmlus\light-speed-holdings\src\ai_company\dashboard\monitoring.py
197 | c:\users\jmlus\light-speed-holdings\src\index.css
197 | c:\users\jmlus\athena\frontend\src\pages\athena\documentstudio.tsx   (outside workspace!)
191 | c:\users\jmlus\light-speed-holdings\src\ai_company\models\models.py
187 | c:\users\jmlus\light-speed-holdings\pyproject.toml
186 | c:\users\jmlus\light-speed-holdings\harness\changes\active\spec.md
185 | c:\users\jmlus\athena\server.ts                                     (outside!)
184 | c:\users\jmlus\light-speed-holdings\src\ai_company\executor\tool_runner.py
183 | c:\users\jmlus\light-speed-holdings\harness\changes\active\plan.md
180 | c:\users\jmlus\light-speed-holdings\src\ai_company\llm\client.py
175 | c:\users\jmlus\light-speed-holdings\.gitignore
174 | c:\users\jmlus\athena\src\components\views\documentstudioview.tsx     (outside!)
172 | c:\users\jmlus\light-speed-holdings\src\ai_company\orchestrator\approval.py
```

**Interpretation:** The top-15 hot files are the dashboard API, registry, AGENTS, ECL harness files, and Vite frontend — the same files re-read on every session start. `harness/changes/active/summary.md` (466) and `tasks.md` (303) prove ECL context reload per session. One hot path is a **tool-output spill file re-read 288 times** — an anti-pattern (large output persisted then re-read instead of summarizing). Three of top-40 are Athena files (multi-repo interleaving).

### 5.3 Grep/glob (directory-level touches)

`grep 15,156 (14,960 completed)` and `glob 11,810 (11,585 completed)` search directories rather than single `filePath`s. Their `path` inputs overwhelmingly point at `C:\Users\jmlus\light-speed-holdings\ai-company\src` and frontend `src/` (samples in proof). `ripgrep execution failed 216` (read/glob errors) is the dominant grep/glob failure (see §6) — PowerShell `rg` missing (see bash-stdout `rg : The term 'rg' is not recognized … 474`).

### 5.4 Links (attachments / references)

| Link type | Count | Evidence |
|---|---|---|
| `blob` rows | 0 | Blob store unused; attachments inline in `part.data` |
| `blob_ref` rows | 0 | No blob links to resolve |
| `file` parts | 144 (57 sessions) | Inline base64 (`outstanding_tasks.md`, `image.png` samples) |
| `patch` parts | 13,579 (814 sessions) | File-change links per session (hash → `files[]`) |
| `session_share` | 0 | No shared-session URLs in DB |
| `session_v2.share_url` / `session.share_url` | Not separately counted (not in top-labels) | Recommend follow-up `SELECT COUNT(*) WHERE share_url IS NOT NULL` |

**“Links” answer: 0 blob links, 144 inline file attachments, 13,579 patch links.** Blob-storage migration never happened; inline base64 is the size driver for `part.data` (some `image.png` payloads are multi-KB–MB-scale base64).

---

## 6. Defects — failed tools, errors, anomalies (3,435 tool errors)

### 6.1 Tool-status errors (3,435 total)

```sql
SELECT json_extract(data,'$.state.status') st, COUNT(*) FROM part
WHERE json_extract(data,'$.type')='tool' GROUP BY 1;
-- completed 185183 | error 3435 | running 93 | pending 2
```

**Top error messages (proof, `GROUP BY error`):**

```text
588 | Could not find oldString in the file. It must match exactly, including whitespace/indentation/line-endings. (edit)
236 | ripgrep execution failed (grep/glob)
173 | Tool execution aborted (permission/abort)
154 | No changes to apply: oldString and newString are identical. (edit)
140 | Ripgrep JSON record exceeded 65536 bytes (grep output too large)
 91 | Task cancelled (task)
 74 | Found multiple matches for oldString. Provide more surrounding context… (edit)
 65 | edit SchemaError: Missing key ["filePath"] (bad input)
 41 | 429 POST https://search.parallel.ai/mcp (websearch rate limit)
 40 | Subagent depth limit reached (1). Increase "subagent_depth"… (task nesting — REPRODUCED during this audit: spawning a subagent failed with this exact error)
 37 | user rejected permission for this tool call
 34 | rule prevents edit (permission ruleset: edit deny * except .opencode/plans/*.md)
 24 | write SchemaError: Missing key ["filePath"]
 21 | edit SchemaError: Missing key ["oldString"]
 21 | File not found: …\harness\changes\active\summary.md
 20 | bash SchemaError: Missing key ["command"]
 19 | read SchemaError: Missing key ["filePath"]
 19 | File not found: …\harness\evolution\pending.md
 16 | Invalid ripgrep match output
 12 | Skill "one-skill-to-rule-them-all" not found (list of available skills follows)
 11 | Transport error (POST https://mcp.exa.ai/mcp)
 11 | originating room task is no longer running
 10 | File not found: …\docs\REMAINING-WORK-INVENTORY.md
  8 | Cannot read binary file: …\.env.example
  7 | detail is at most 600 characters
```

**By-tool error leaders:** `read 959 | edit 949 | bash 387 | task 351 | glob 225 | grep 196 | webfetch 102 | write 63 | websearch 59 | skill 26 | question 18`. Core loop-relevant: `edit` failures (588 + 154 + 74 = **816 edit-semantic failures**) exceed `read` file-not-found churn. `edit` is the single most defect-dense tool.

**Invalid-input SchemaErrors total ≥ 65+24+21+20+19 = 149** (edit/write/bash/read missing-key) — agents retrying malformed JSON/tool calls rather than validating once. Schema validation should fail fast with a repair hint.

### 6.2 Repeated bash stdout errors (completed bash calls whose output contains `error`, `HAVING n>1`)

```text
474 | rg : The term 'rg' is not recognized … (ripgrep not installed on Windows PATH)
289 | Select-Object : Cannot validate argument on parameter 'First'. The -30 argument is less than minimum 0 …
287 | Select-Object : … 'First'. The -20 argument …
185 | Select-Object : … 'First'. The -5 argument …
125 | Select-Object : … 'First'. The -50 argument …
113 | Select-Object : … 'First'. The -100 argument …
 84 | Select-Object : … 'Last'. The -20 argument …
 81 | Select-Object : … 'First'. The -80 argument …
260 | pytest session starts (Python 3.12.10, pytest-9.1.1)
126 | out-file : FileStream was asked to open a device … 'com1:'/'lpt1:'
118 | python << 'PYEOF' → Missing file specification after redirection (bash heredoc in PowerShell)
106 | The string is missing the terminator: ". (PowerShell quoting)
 81 | python3 : The term 'python3' is not recognized … (Windows uses python)
 78 | benchmark: 5.2.3
```

These are **exact recurrences of the AGENTS.md §17 known-issues** (PowerShell `Select-Object -First/-Last` negative values, `&&` separator, `$(…)` expansion, heredoc misuse). The `memory-search` template (“repeated stdout errors, last 7 days”) was run time-anchored to `MAX(time_created)` (because v1 is frozen) — the signal is months-long, not a 7-day blip. `rg` missing (474) is the #1 repeated env error; the team has been working around a missing binary for months.

### 6.3 Anomalies (not errors, but defects by another name)

1. **`running 93 / pending 2` orphaned tool calls** — never reached `completed`/`error`. No sweeper observed (cf. HITL expiry sweep policy for approvals — no equivalent for tool calls).
2. **`cache_write 0 everywhere` (§4)** — metering hole, not a crash, but every cost/cache dashboard downstream of this DB inherits it.
3. **`session_part 0` + `session_message 9,161` + `blob/blob_ref 0`** — v2 writes messages but not parts/attachments via the new tables; trajectory readers must still join the v1 `message`/`part` for detail, and there is no v2 tool-call ledger yet (only `session_message` type counts). Current-era tool analysis is therefore **v1-only**; v2 tool telemetry does not exist in this snapshot.
4. **Mega-sessions:** 23M input / 377M cache-read in one session; `26.8M input` “Prompt contents” in v2. Long sessions + compaction (5,444) + huge cache reads are the norm for `build`.
5. **Tool-output spill re-read 288×** (§5.2) — a 288-hit file under `~/.local/share/opencode/tool-output/` indicates one session dumped a huge tool output to disk and kept re-reading it.
6. **867 session-less projects** (72 − 5): worktree projects created eagerly (`worktree/9930fa/*` × ~10 on 2026-11-03/04 alone) but never used — project sprawl with zero sessions.
7. **`schedule 0 / job 0 / session_inbox 0`** — scheduler/inbox subsystems exist as tables but have never run (or were purged); `event 0` vs `event_sequence 3,527` (sequence without events) suggests an event-store migration that left sequences behind.
8. **Cost $5.59 on 1.7B input tokens** — free-model traffic makes cost-based spend alerts useless; token-based budgets are the only honest signal.

### 6.4 What was fixed during this audit

**Nothing in the DB — deliberately (read-only).** Defects identified: **3,435 tool errors + 2,300+ repeated stdout-error instances + 95 orphaned calls + 149 schema-error retries**. Defects fixed *in the DB*: **0**. Defects fixed *in this workspace*: **1 artifact created** (this report). The nested-subagent spawn attempted by this chief-of-staff session **failed with “Subagent depth limit reached (1)”** — the same error that appears 40 times in the DB — confirming the depth-1 constraint is live and hit even by orchestrators. Work was done directly instead (this is the honest fallback path).

---

## 7. Artifacts outside `C:\Users\jmlus\light-speed-holdings` — FLAG

**Flag: YES, outside-workspace artifacts exist and are flagged below. The audit itself created zero artifacts outside the workspace.**

### 7.1 Audit-created artifacts (this run)

- Created: `C:\Users\jmlus\light-speed-holdings\reports\opencode-db-audit-2026-11-08.md` (this file, inside workspace). `reports/` pre-existed (40 files, incl. `repo-audit-2026-11-01.md`, `token-consumption-audit-2026-10-28.md`).
- Created outside workspace: **none.** No files written to `~/.local/share/opencode`, `Temp\opencode`, `athena`, or any other outside path by this audit. (Pre-existing outside files below are not audit outputs.)

### 7.2 Pre-existing outside-workspace file operations in the trajectory (flagged, not audit-created)

```sql
SELECT COUNT(*) FROM part
WHERE tool IN ('read','edit','write') AND filePath IS NOT NULL
  AND lower(filePath) NOT LIKE '%light-speed-holdings%';
-- 13126 ops (17.7% of 74310 filePath ops)
```

Top outside prefixes (45-char, proof):

```text
838 | c:\users\jmlus\athena\frontend\src\pages\athe…      (Athena frontend pages)
635 | c:\users\jmlus\social-media-automation-os\app…    (second repo)
620 | c:\users\jmlus\athena\frontend\src\components…
457 | c:\users\jmlus\athena\backend\src\athena\api\…
432 | c:\users\jmlus\social-media-automation-os\pac…
359 | c:\users\jmlus\appdata\local\temp\opencode\d6…
350 | c:\users\jmlus\.local\share\opencode\tool-out…     (tool-output spill)
280 | c:\users\jmlus\athena\frontend\src\lib\athena…
239 | c:\users\jmlus\appdata\local\temp\opencode\ls…
224 | c:\users\jmlus\appdata\local\temp\opencode\wt…     (worktree temp)
205 | c:\users\jmlus\appdata\local\temp\opencode\fi…
185 | c:\users\jmlus\athena\server.ts
174 | c:\users\jmlus\athena\src\components\views\do…
143 | c:\users\jmlus\appdata\local\temp\opencode\wa…
132 | c:\users\jmlus\athena\backend\src\athena\docu…
… (.openmausbot\jobsearch\master_… 96, …\site_pl… 81, …)
```

- **Bash outside refs:** `7,071` bash calls whose `command` contains `athena` or `Temp\opencode` (`… LIKE '%athena%' OR '%Temp\\opencode%'`) — multi-repo bash work, not filePath ops.
- **On disk (verified `Test-Path`, not content):** `C:\Users\jmlus\athena` exists (`LastWriteTime 2026-10-07`), `C:\Users\jmlus\social-media-automation-os` exists. **These are legitimate sibling repos**, not stray audit artifacts — but trajectory file ops freely cross repo boundaries (`athena` appears in `session` titles, e.g. “Athena Implementation”, and in top hot files). Treat as intentional multi-repo work; flag for governance awareness, not as a violation, unless policy forbids cross-repo edits.
- **`Temp\opencode` is heavily used and polluted:** filesystem check (this audit) → **31,217 files total, 228 modified in last 7 days** under `C:\Users\jmlus\AppData\Local\Temp\opencode`. That directory is the approved temp location, but 31k files with only 228 in the last week means stale accumulation — cleanup candidate.
- **Opencode storage itself is outside the workspace by design:** `~/.local/share/opencode/` (6.4 GB live + 38.5 GB `.bak`). The 38.5 GB `.bak` (2026-11-01, pre-v2) is the largest single outside-workspace artifact and the top reclaim candidate.

**Verdict:** No audit-created outside artifacts. **Flagged (pre-existing):** (a) 13,126 trajectory file ops outside `light-speed-holdings` (athena + social-media-automation-os + temp + tool-output + .openmausbot), (b) 38.5 GB `.bak` backup outside the workspace, (c) 31,217 accumulated temp files. (a) is multi-repo work to govern; (b)+(c) are reclaim candidates.

---

## 8. Prioritized recommendations

### P1 — Reclaim + stabilize storage (do first; disk pressure is live)

1. **Checkpoint the WAL.** WAL (3.16 GB) ≈ DB size means `PRAGMA wal_checkpoint(TRUNCATE)` has not kept up. Run a maintenance window (opencode closed) `sqlite3 opencode.db "PRAGMA wal_checkpoint(TRUNCATE);"` and verify `opencode.db-wal` shrinks toward 0. Schedule periodic checkpoints; alert if WAL > 10% of DB.
2. **Delete or archive the 38.5 GB `.bak`.** `opencode.db.bak` (2026-11-01) is pre-v2. After confirming v2 is stable (it is — 94 sessions, integrity `ok`), move it off the data volume (archive to cold storage) or delete. Single action recovers ~38.5 GB — 6× the live DB.
3. **Vacuum / archive old sessions.** `freelist_count 1,996` (~8 MB) says bloat is *live* pages, not free space — `VACUUM` will reclaim little. Instead **archive v1 sessions older than N days** (e.g. move `session`+`message`+`part` for sessions < 2026-09-01 to a cold DB) and `VACUUM INTO` a compacted primary. `auto_vacuum=0` (NONE) means the DB never reclaims deleted pages automatically — consider `PRAGMA auto_vacuum=INCREMENTAL` + periodic `PRAGMA incremental_vacuum` for future deletes.
4. **Clean `Temp\opencode` (31,217 files).** Purge files older than 7 days (only 228 in last 7 days are fresh). Add a retention sweeper.
5. **Create the compensating control for the live-DB problem:** this audit ran against a **growing WAL-backed DB** (counts shifted +1–3 sessions mid-audit; `.bak` already exists as precedent). Route future audits through a **copy-on-write snapshot** (`sqlite3 ".backup"` or filesystem snapshot) so findings are reproducible, not drift-affected.

### P2 — Fix the defect classes that dominate the 3,435 errors

6. **Edit semantic failures (816):** `oldString not found 588 + identical 154 + multiple matches 74`. Require `edit` callers to re-read the exact region before editing (or use anchor+verify) and reject `old==new` client-side. This is the #1 defect — a 27% share of all errors on the most-used mutation tool.
7. **Ripgrep stack (236 + 140 + 16 + 474 `rg` missing):** install `rg` on PATH **or** fix the `grep`/`glob` fallback when `rg` is absent. The 474× “`rg` is not recognized” repeats prove the fallback is broken or missing. Also cap grep/shell output below 64 KB to avoid the 140× “JSON record exceeded 65536 bytes.”
8. **PowerShell antipatterns (1,500+ repeated stdout errors):** enforce the AGENTS.md §17 directives in agent skills/system prompt: never `Select-Object -First/-Last <negative>`, never `&&`, never `$(…)` in `--jq`, never bash heredocs in PowerShell (`python << 'PYEOF'` 118×). Add a pre-flight linter for bash commands. These are *learned* already (§17 documents them) but *repeated* — the lesson is not being applied at runtime.
9. **Schema-error retries (149):** validate tool-call JSON against the schema once; on `Missing key ["filePath"/"command"/"oldString"]`, fail fast with the correct shape instead of letting the agent retry blindly.
10. **Subagent depth (40× + reproduced this audit):** raise `subagent_depth` for orchestrator-class agents (chief-of-staff, cto, vp-engineering) or give them a direct-work carve-out with explicit logging. This audit itself hit the wall and fell back to direct execution — any orchestration that spawns subagents from a subagent will fail identically.
11. **Network/tool fragility:** `parallel.ai 429 (41)`, `exa transport (11)`, `agents_coordinate_bots 50% fail`, `agents_show_widget 79% fail` — add retries with backoff for `websearch`/`webfetch`, and quarantine or fix the two high-fail `agents_*` tools before further use.

### P3 — Token/cache economics + hot-file governance

12. **Meter cache correctly.** `cache_write` is 0 everywhere (provider quirk). Renormalize accounting to `cache_read` volume and per-session input+cache-read totals; do not build hit-rate or savings dashboards on `cache_write`. Require providers to emit `cache_write` or document the quirk in `docs/`.
13. **Govern mega-sessions.** Single sessions at 23M input / 377M cache-read (v1) and 26.8M “Prompt contents” (v2) dominate burn. Enforce a session token budget + early compaction (already 5,444 compactions — raise the threshold to auto-compact *before* the next step, not after), and split `build` mega-sessions into subagent tasks. Track burn per agent (`build` = 65% of v2 sessions) and surface it in the dashboard.
14. **Cache the hot files, don’t re-read them.** 1,442 files read >10× (1,101 by `read` alone), top `api.py 974×`, `company-registry.yaml 763×`, `agents.md 552×`, `summary.md 466×`. Session-start context (AGENTS, STATUS, ECL `summary.md`/`tasks.md`, registry) should be **injected once via the memory/recall loop**, not re-read per tool call. Add a per-session file-read dedup (second read of the same path returns a pointer, not disk I/O) — this alone could cut `read` volume by ≥30%.
15. **Stop re-reading tool-output spills.** One `tool-output/tool_14ff…` file read 288×. Tool-output files should be **summarized, not re-read**; cap spill file size and summarize on write.
16. **Use blob storage for attachments.** 144 inline base64 `file` parts + 0 `blob` rows means every image drag-in inflates `part.data` JSON. Migrate to `blob`/`blob_ref` and store only the hash in `part.data`.

### P4 — Schema + lifecycle hygiene

17. **Finish v2 (or freeze v1 explicitly).** `session_part 0`, `blob/blob_ref 0`, `schedule/job/inbox/event 0` vs `event_sequence 3,527`. Either complete the v2 writers (parts, blobs, scheduling, events) or document v1 as canonical and stop the dual-schema query burden. Until then, every audit must join both schemas (as this one did).
18. **Sweep orphaned tool calls.** `running 93 + pending 2` with no sweeper. Add a TTL sweeper (e.g. `running` > 1 h → `error` with “orphaned” marker) analogous to the HITL expiry sweep.
19. **Cull session-less projects.** 67 of 72 `project` rows have zero sessions (worktree sprawl, ~10 created 2026-11-03/04). Add project GC (delete worktree projects with no sessions older than N days) before the `project` table becomes noise.
20. **Token-based budgets.** Cost ($5.59) is meaningless under free models. Switch spend alerts to token budgets per agent/day (the data exists: `tokens_input + tokens_cache_read` per session, per day). The Oct-22 “DIRECTIVE: Fix agent session token burn” shows the org already knows — enforce it with a hard cap, not a directive.
21. **Schedule the next audit after P1.** Re-run this audit (especially WAL size, `.bak` presence, temp count, `session_part`/`blob` population) 14 days after checkpoint/`.bak` removal and confirm the deltas. Keep this report as the baseline.

---

## 9. Method & reproducibility (proof)

**Skill used:** `memory-search` — `C:\Users\jmlus\.config\opencode\skills\memory-search\SKILL.md` (schema tables, `json_extract` patterns, “Always `sqlite3 -readonly`”, `time_created` = Unix ms). Templates applied below; time-anchored variants used where v1 is frozen (see §6.2 note).

### 9.1 Queries executed (verbatim intent + key results)

1. **Locate:** PowerShell `Get-ChildItem *.db` (repo + `%USERPROFILE%` depth 4) + `Test-Path` each candidate → `opencode.db` 3,222,466,560 B at `~/.local/share/opencode/opencode.db`.
2. **Pragmas/idle schema:**
   ```sql
   PRAGMA page_size; PRAGMA page_count; PRAGMA freelist_count;
   PRAGMA journal_mode; PRAGMA user_version; PRAGMA schema_version;
   PRAGMA encoding; PRAGMA auto_vacuum;
   PRAGMA integrity_check;  -- ok
   .tables
   SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name;
   SELECT type,name,tbl_name FROM sqlite_master ORDER BY type,name;
   ```
3. **Row counts:** `SELECT COUNT(*)` per table (small tables batched, large tables separately with 300s timeout) — §2 table.
4. **Sessions/projects:**
   ```sql
   SELECT id,worktree,… FROM project ORDER BY time_updated DESC LIMIT 15;
   SELECT … FROM project WHERE worktree LIKE '%light-speed%';
   SELECT COUNT(*), MIN(time_created), MAX(time_created) FROM session;
   SELECT COUNT(*), MIN/MAX FROM session WHERE project_id='9930faf5…';
   SELECT COUNT(*), MIN/MAX FROM session_v2;
   SELECT agent, COUNT(*) FROM session GROUP BY 1 ORDER BY 2 DESC;  -- + session_v2 variant
   SELECT model, COUNT(*) FROM session GROUP BY 1;                 -- + session_v2 variant
   SELECT date(time_created/1000,'unixepoch','localtime') d, COUNT(*) FROM session GROUP BY d;
   SELECT id,title,…,tokens_input,cost,model FROM session ORDER BY tokens_input DESC LIMIT 10; -- + session_v2 variant
   ```
5. **Roles/parts/tools:**
   ```sql
   SELECT json_extract(data,'$.role'), COUNT(*) FROM message GROUP BY 1;
   SELECT json_extract(data,'$.type'), COUNT(*) FROM part GROUP BY 1;
   SELECT json_extract(data,'$.tool'), COUNT(*) FROM part WHERE $.type='tool' GROUP BY 1 ORDER BY 2 DESC LIMIT 30;
   SELECT json_extract(data,'$.state.status'), COUNT(*) FROM part WHERE $.type='tool' GROUP BY 1;
   SELECT json_extract(data,'$.tool'), json_extract(data,'$.state.status'), COUNT(*) FROM part WHERE $.type='tool' GROUP BY 1,2;
   ```
6. **Tokens/cache:**
   ```sql
   SELECT COUNT(*), SUM(cost), SUM(tokens_input), SUM(tokens_output),
          SUM(tokens_reasoning), SUM(tokens_cache_read), SUM(tokens_cache_write) FROM session;  -- + session_v2
   SELECT COUNT(*), SUM(tokens_input), SUM(tokens_cache_read) FROM session
   WHERE time_created > (SELECT MAX(time_created) FROM session) - 7*86400*1000;
   SELECT COUNT(*), SUM($.tokens.input), SUM($.tokens.cache.read), SUM($.tokens.cache.write)
   FROM part WHERE $.type='step-finish';
   ```
7. **Files:**
   ```sql
   SELECT COUNT(DISTINCT lower($.state.input.filePath)), COUNT(*) FROM part
   WHERE tool IN ('read','edit','write') AND filePath IS NOT NULL;
   SELECT $.tool, COUNT(*), COUNT(DISTINCT lower(filePath)) … GROUP BY 1;
   SELECT lower(filePath), COUNT(*) … GROUP BY 1 HAVING COUNT(*)>10 ORDER BY 2 DESC LIMIT 40;
   SELECT COUNT(*) FROM (… GROUP BY … HAVING >10);  -- 1442; read-only variant 1101
   SELECT COUNT(*) … WHERE tool IN ('edit','write') AND status='completed' GROUP BY 1;  -- 15591/5249
   SELECT COUNT(*) … WHERE tool IN ('read','edit','write') AND lower(filePath) NOT LIKE '%light-speed-holdings%';  -- 13126
   SELECT substr(lower(filePath),1,45), COUNT(*) … outside GROUP BY 1 ORDER BY 2 DESC LIMIT 30;
   SELECT COUNT(DISTINCT session_id), COUNT(*) FROM part WHERE $.type='patch';  -- 814 / 13579
   SELECT COUNT(DISTINCT session_id), COUNT(*) FROM part WHERE $.type='file';   -- 57 / 144
   ```
8. **Defects:**
   ```sql
   SELECT $.state.error, COUNT(*) FROM part WHERE $.type='tool' AND status='error' GROUP BY 1 ORDER BY 2 DESC LIMIT 25;
   SELECT $.tool, COUNT(*) FROM part WHERE $.type='tool' AND status='error' GROUP BY 1 ORDER BY 2 DESC LIMIT 15;
   -- memory-search “repeated stdout errors” template, time-anchored:
   SELECT substr($.state.output,1,160), COUNT(*) FROM part
   WHERE $.tool='bash' AND status='completed' AND $.state.output LIKE '%error%'
   GROUP BY 1 HAVING COUNT(*)>1 ORDER BY 2 DESC LIMIT 15;
   SELECT $.state.error, COUNT(*) FROM part WHERE tool IN ('read','glob') AND status='error' GROUP BY 1 LIMIT 15;
   ```
9. **Filesystem:**
   ```powershell
   Get-ChildItem reports\ | Format-Table Name, Length, LastWriteTime  # reports pre-existed
   Get-ChildItem ~\.local\share\opencode\opencode* | Select Name, Length, LastWriteTime  # 3.22 GB + 3.16 GB WAL + 38.5 GB .bak
   Test-Path C:\Users\jmlus\athena; Test-Path C:\Users\jmlus\social-media-automation-os
   (Get-ChildItem Temp\opencode -Recurse -File).Count  # 31217; last-7d 228
   git status --short  # workspace has unrelated dirty files (cost_tracker.json, dead_letter.jsonl, cli/llm.py, …) — left untouched
   sqlite3 -readonly opencode-.db ".tables"  # secondary DB table list only
   ```
10. **Subagent attempt:** `subagent(general, background, "Verify outside workspace artifacts")` → **error “Subagent depth limit reached (1)”** — documented, work done directly (honest fallback).

### 9.2 Limits (declared, not hidden)

- **Live DB drift:** `session_v2` count 91 → 92 → 94 across queries; `opencode.db` mtime updated mid-audit. Counts are snapshot-consistent within each query but not across time. V1 counts are stable (frozen since 2026-10-22).
- **Bash file writes are unstructured:** “files created/modified” via bash (78,923 calls) cannot be counted from `filePath`; the 20,840 create/modify figure covers only structured `edit`/`write` tools. Patch parts (13,579) are a lower bound on changed files.
- **Outside-workspace = trajectory evidence, not filesystem proof that a file exists today** (except where `Test-Path` verified `athena`/`social-media-automation-os` exist). `Temp\opencode` counts are filesystem truth for the temp dir.
- **No content dumps:** `credential.value`, `kv` catalogs, `part.data` payloads, and message text were sampled only by prefix/keys; no secrets or full user content are reproduced in this report.
- **`opencode-.db` not deep-audited** (765 KB, stale 2026-10-30). If it holds v1→v2 transition data, it needs its own audit.
- **Links** = blob/patch/share links above; `share_url` non-null count not separately queried (low value, noted as follow-up).

---

## 10. Structured summary (as requested)

| Item | Value (evidence) |
|---|---|
| **Agents invoked** | chief-of-staff (this session, direct execution); `memory-search` skill loaded; **1 nested subagent attempted (`general`, background verification) — FAILED with “Subagent depth limit reached (1)”**, documented verbatim in §6.4/§9.1(10). No other subagents successfully spawned (depth-1 constraint). |
| **Files inspected** | **9,361 distinct `filePath`s / 74,310 ops** (read 52,581 + edit 16,540 + write 5,315); 101,276 file-touching calls incl. grep/glob. |
| **Cache reads** | **15,210,842,514 tokens (session ledger) = 15,210,842,514 (step-finish ledger)**; v2 current-era **809,948,648**; `cache_write 0` everywhere (provider quirk). |
| **Files >10×** | **1,442 distinct (any read/edit/write)**, 1,101 by read alone. Top: `api.py 974`, `company-registry.yaml 763`, `agents.md 552`, `summary.md 466`, `status.md 452`. Full top-40 in §5.2. |
| **Files created** | **5,249 `write` completed ops** (4,260 distinct). Patch evidence: 13,579 patches / 814 sessions. |
| **Links** | **0 `blob_ref` links** (blob store empty), **144 inline `file` attachments** (57 sessions), **13,579 `patch` links** (814 sessions), 0 `session_share`. |
| **Files modified** | **15,591 `edit` completed ops** (2,560 distinct). Create+modify completed = **20,840**. |
| **Defects identified** | **3,435 tool errors (1.8% of 188,713)** + 2,300+ repeated bash stdout-error instances + 95 orphaned (`running`/`pending`) calls + 149 schema-error retries. Top: edit `oldString` 588, ripgrep 236, abort 173, identical 154, 64 KB overflow 273 (140+133), 429 rate-limit 41, subagent-depth 40. |
| **Defects fixed** | **0 in DB (read-only)**; 1 artifact created (this report); 1 nested-subagent attempt failed honestly (depth limit). |
| **Outside artifacts flag** | **YES — flagged.** Audit-created outside: **0**. Pre-existing outside flagged: **13,126 trajectory file ops outside `light-speed-holdings`** (athena, social-media-automation-os, `Temp\opencode`, `tool-output`, `.openmausbot`), **7,071 bash outside refs**, **38.5 GB `opencode.db.bak`**, **31,217 `Temp\opencode` files (228 in last 7d)**. Details §7. |
| **Recommendations** | 21 items, P1 storage (WAL checkpoint, delete 38.5 GB `.bak`, archive v1, clean temp) → P2 defect classes (edit, ripgrep/`rg`, PowerShell, schema, depth, network) → P3 cache/token/hot-file governance → P4 v2 completion, orphan sweep, project GC, token budgets. Prioritized §8. |
| **Proof** | Verbatim pragmas (`page_size 4096, page_count 786735, freelist 1996, journal wal, integrity ok`), row-count tables (§2), tool × status dumps (App. B), top-40 hot files (§5.2), error leaderboard + bash-stdout repeats (§6), outside-prefix leaderboard (§7.2), and §9 query log. No numbers without a query. |

---

## Appendix A — Full schema (DDL) & indexes

*Captured via `SELECT sql FROM sqlite_master WHERE type='table'` and `… WHERE type IN ('index','table')`. Abbreviated here for readability (full output retained in shell log `sh_1bb06bd5…out`); key DDL preserved in §2. Explicit indexes (30):*

```text
blob_ref_hash_idx, blob_ref_session_seq_idx, event_aggregate_seq_idx, event_aggregate_type_seq_idx,
job_child_session_idx, job_id_idx, job_session_idx, message_session_time_created_id_idx, part_message_id_id_idx,
part_session_idx, permission_project_action_resource_idx, schedule_due_idx, schedule_session_idx,
session_inbox_session_delivery_seq_idx, session_inbox_session_enqueued_seq_idx, session_message_session_seq_idx,
session_message_session_time_created_id_idx, session_message_session_type_seq_idx, session_message_time_created_idx,
session_parent_idx, session_part_session_message_idx, session_project_idx, session_v2_parent_idx,
session_v2_project_idx, session_v2_time_suspended_idx, session_v2_workspace_idx, session_workspace_idx, todo_session_idx
+ sqlite_autoindex_* (PKs) for all 30 tables
```

## Appendix B — Tool × status & file/part samples

**Tool leaderboard (30):** `bash 78923, read 52581, edit 16540, grep 15156, glob 11810, write 5315, todowrite 2959, task 2051, websearch 830, webfetch 745, question 545, skill 526, agents_list_threads 153, agents_session_search 107, invalid 78, agents_assignment_status 77, agents_coordinate_bots 32, agents_vm_exec 19, agents_propose_team_memory 19, computer_hotkey 16, computer_get_desktop_state 14, agents_show_widget 14, composio_MULTI_EXECUTE 13, agents_retry_thread 11, agents_session_read 9, agents_memory_log 8, agents_list_bots 8, computer_list_windows 7, agents_attach_file 7, computer_press_key 6` (+40 low-frequency tools down to n=1).

**Part-type samples:**
- `file`: `{"type":"file","mime":"text/plain","filename":"C:\Users\jmlus\.gemini\antigravity-ide\brain\…\outstanding_tasks.md","url":"data:text/plain;base64,…"}` + 2× `image/png` base64.
- `patch`: `{"type":"patch","hash":"ec35…","files":["C:/Users/jmlus/light-speed-holdings/.gitignore","C:/Users/jmlus/light-speed-holdings/ai-company/.gitignore"]}`.
- `step-finish`: `{"reason":"stop","tokens":{"total":8758,"input":6700,"output":10,"reasoning":0,"cache":{"write":0,"read":2048}}}`; `{"reason":"tool-calls","tokens":{"total":8848,"input":73,"output":46,"reasoning":25,"cache":{"write":0,"read":8704}}}`.
- `message` sample: `{"role":"assistant","mode":"build","agent":"build","path":{"cwd":"C:\Users\jmlus\light-speed-holdings-main",…},"modelID":"big-pickle","providerID":"opencode","tokens":{"input":0,…,"cache":{"read":0,"write":0}}, …}` (one sampled message also carried a stored 404 API-error body — error text persisted in `message.data`).

## Appendix C — Filesystem evidence

- `reports\` pre-existed with 40 entries (incl. `evidence/`, `rea-feasibility/`, `token-consumption-audit-2026-10-28.md`, `repo-audit-2026-11-01.md`); **no `opencode-db-audit-*.md` existed before this run** — this report is new.
- `opencode*` listing: `opencode.db 3,222,466,560 (2026-11-08 14:13)`, `opencode.db-wal 3,163,682,112 (14:13)`, `opencode.db-shm 98,304`, `opencode.db.bak 38,533,844,992 (2026-11-01)`, `opencode-.db 765,952 (2026-10-30)` + WAL/shm.
- `athena exists: True`, `social-media-automation-os exists: True`, `athena LastWriteTime 2026-10-07`.
- `Temp\opencode`: `exists True → 31,217 files total, 228 in last 7d`.
- `git status --short`: unrelated dirty files (`data/ai_company.db`, `cost_tracker.json`, `dead_letter.jsonl`, `src/ai_company/cli/llm.py`, `cost_analytics.py`, `database.py`, `cost_tracker.py`, `opencode_usage.py`, `?? BUG-115cb13bb.md`, `?? check-cost-tracker.py`) — **left untouched**.

---

*End of audit. Baseline for re-audit after P1. All counts reproducible via §9 queries against a copy-on-write snapshot (recommend snapshot over live WAL in future).*
