# opencode.db Trajectory Analytics — Read-Only Evidence (2026-11-08)

**Database:** `C:\Users\jmlus\.local\share\opencode\opencode.db`
**File size:** `3,222,466,560` bytes (~3.0 GiB, per `Get-Item` at run time)
**Last write time observed:** `2026-11-08 14:19:26 (+02:00)` — live database; counts below are a snapshot.
**Report date:** 2026-11-08
**Workspace:** `C:\Users\jmlus\light-speed-holdings`
**Method:** `sqlite3 -readonly` only. No `INSERT`/`UPDATE`/`DELETE`/`VACUUM`; every metric is a `SELECT` with `json_extract()`. SQL is reproduced verbatim in §10 so the report is independently re-derivable.
**Skill template used:** `memory-search` — `part.data` JSON paths (`$.type`, `$.tool`, `$.state.status`, `$.state.input`, `$.state.output`, `$.state.error`, `$.tokens.cache.read`), last-30-days window via `(SELECT MAX(time_created) FROM part) - 30*86400*1000`, repeated-failure grouping by `(tool, substr(error,1,160)) HAVING n>1`, large-output scan via `length(json_extract(...))`.

> **Schema mapping note (opencode vs. skill template).** The skill template describes a `mimocode.db` with `task` / `task_event` / `actor_registry` tables and `message.agent_id`. This `opencode.db` has **none of those** (`task`, `task_event`, `actor_registry` do not exist; `message` has no `agent_id` column — agent is inside `message.data` JSON). Mapping used here and stated for every metric:
>
> - **sessions** = `session` (primary) + `session_v2` (secondary, reported separately, never summed)
> - **messages** = `message` (primary) + `session_message` (secondary)
> - **parts** = `part` (primary) + `session_part` (empty, `0`)
> - **tasks** = `todo` (closest equivalent; `job` is `0`)
> - **actors** = distinct `session.agent` (primary) + distinct `session_v2.agent`
>
> Do not add primary + secondary counts together.

**Time base:** `time_created` is Unix **milliseconds**. Data span is `2026-08-05` → `2026-10-22` (see §1). All datetimes below are `datetime(time_created/1000,'unixepoch','localtime')`. The “last 30 days” window is anchored to the **DB maximum** (`2026-09-22 12:59:05` → `2026-10-22 12:59:05`), not wall-clock `now()` (`2026-11-08`), because the DB contains no rows after `2026-10-22`. Wall-clock last-30-days (`2026-10-09` → `2026-11-08`) would only cover the final 13 days of data.

**Live-DB drift warning:** counts moved during this audit (`session_v2` `91 → 94`, `session_message` `9172 → 9284` between the first probe and the §1 batch). Cause was not determined from available evidence. Treat §1 as the frozen snapshot; later batches (§2–§9) ran minutes later and may differ by tens of rows. This is expected for a live DB and does not affect rates by more than rounding.

---

## 1. Totals — sessions, messages, parts, tasks, actors

### 1.1 Table counts

| Table | Rows | Role in this report |
|---|---:|---|
| `session` | **3,131** | Primary sessions |
| `session_v2` | **94** | Secondary sessions (not summed) |
| `message` | **153,182** | Primary messages |
| `session_message` | **9,284** | Secondary messages (not summed) |
| `part` | **670,664** | Primary parts |
| `session_part` | **0** | Empty; confirms `part` is authoritative |
| `todo` | **2,771** | **Tasks** |
| `job` | **0** | No async jobs recorded |
| `project` | **72** | Projects |
| `project_directory` | **7** | — |
| `worktree` | **7** | — |
| `event` / `blob` / `schedule` / `session_inbox` | **0 each** | Empty; no events/blobs/schedules/inbox |
| `event_sequence` | **3,530** | Sequence bookkeeping only |

**Derived:** `2,122` sessions have `parent_id IS NOT NULL` (subagent/child sessions); `5` distinct `project_id` values appear in `session`; `3,114/3,131` sessions have ≥1 message; `3,113/3,131` have ≥1 part (17–18 sessions are message/part-empty).

### 1.2 Time ranges (localtime)

| Table | Min | Max |
|---|---|---|
| `session` | 2026-08-05 22:53:46 | 2026-10-22 12:59:05 (`time_updated` max 12:59:06) |
| `message` | 2026-08-05 22:53:47 | 2026-10-22 12:59:05 |
| `part` | 2026-08-05 22:53:47 | 2026-10-22 12:59:05 |
| `todo` | 2026-08-06 20:34:49 | 2026-10-22 12:06:18 |

Window definition row (from `part` max):

| `part_max_ms` | `part_max_local` | `30d window start` |
|---:|---|---|
| 1792666745854 | 2026-10-22 12:59:05 | **2026-09-22 12:59:05** |

### 1.3 Message roles and part types

**Messages by `json_extract(data,'$.role')`:**

| Role | n | % of messages |
|---|---:|---:|
| `assistant` | 133,944 | 87.4% |
| `user` | 19,238 | 12.6% |

**Parts by `json_extract(data,'$.type')`:**

| Part type | n |
|---|---:|
| `tool` | 188,713 |
| `step-start` | 135,963 |
| `step-finish` | 132,342 |
| `reasoning` | 119,892 |
| `text` | 73,820 |
| `patch` | 13,579 |
| `compaction` | 5,444 |
| `agent` | 767 |
| `file` | 144 |

### 1.4 Actors (agents)

Distinct values:

| Source | Distinct agents |
|---|---:|
| `session.agent` | **123** |
| `session_v2.agent` | **20** |

Top 30 `session.agent` by session count:

| `agent` | Sessions |
|---|---:|
| build | 876 |
| explore | 357 |
| general | 235 |
| plan | 133 |
| chief-of-staff | 123 |
| qa-lead | 76 |
| backend-engineer | 70 |
| cto | 64 |
| frontend-engineer | 56 |
| lead-frontend | 49 |
| ceo-advisor | 47 |
| test-engineering-lead | 40 |
| devops-lead | 39 |
| senior-frontend-engineer | 37 |
| product-designer | 35 |
| technical-documentation-lead | 34 |
| senior-backend-engineer | 30 |
| memory-owner | 29 |
| dashboard-owner | 29 |
| cmo | 29 |
| human-ceo | 26 |
| qa-automation-engineer | 25 |
| coo | 23 |
| brand-strategist | 22 |
| board-chair | 21 |
| frontend-architect | 20 |
| registry-owner | 19 |
| release-manager | 18 |
| orchestration-owner | 18 |
| caio | 18 |

### 1.5 Tasks (`todo`)

| `status` | n |
|---|---:|
| `completed` | 2,039 |
| `pending` | 550 |
| `in_progress` | 177 |
| `cancelled` | 2 |
| `pending - requires staging` | 1 |
| `incomplete` | 1 |
| `blocked - Docker not available` | 1 |

### 1.6 Session token aggregates (from `session.*`)

| `SUM(tokens_input)` | `SUM(tokens_output)` | `SUM(tokens_reasoning)` | `SUM(tokens_cache_read)` | `SUM(tokens_cache_write)` | `SUM(cost)` |
|---:|---:|---:|---:|---:|---:|
| 1,699,925,967 | 65,346,163 | 34,073,428 | **15,210,842,514** | **0** | 5.59 |

> **Anomaly:** `tokens_cache_write` is `0` everywhere while cache reads total 15.2B (see §7). Either the provider never reports writes or the recorder drops them. Treat cache-write evidence as “not recorded”, not “zero cache cost”.

---

## 2. Tool calls — breakdown by tool and status

Total tool parts: **188,713** = `completed 185,183` + `error 3,435` + `running 93` + `pending 2`.
Overall error share (of tool parts): `3,435 / 188,713 = 1.82%`. `running` + `pending` (`95` rows) are non-terminal residue — likely abandoned/killed calls (see §8).

### 2.1 Error-rate table (sorted by absolute errors)

| Tool | Completed | Error | Other* | Total | Err % |
|---|---:|---:|---:|---:|---:|
| `read` | 51,621 | **959** | 1 | 52,581 | 1.82% |
| `edit` | 15,591 | **949** | 0 | 16,540 | 5.74% |
| `bash` | 78,506 | **387** | 30 | 78,923 | 0.49% |
| `task` | 1,649 | **351** | 51 | 2,051 | **17.11%** |
| `glob` | 11,585 | **225** | 0 | 11,810 | 1.91% |
| `grep` | 14,960 | **196** | 0 | 15,156 | 1.29% |
| `webfetch` | 643 | **102** | 0 | 745 | **13.69%** |
| `write` | 5,249 | **63** | 3 | 5,315 | 1.19% |
| `websearch` | 771 | **59** | 0 | 830 | 7.11% |
| `skill` | 500 | **26** | 0 | 526 | 4.94% |
| `question` | 517 | 18 | 10 | 545 | 3.30% |
| `agents_coordinate_bots` | 16 | 16 | 0 | 32 | 50.0% |
| `agents_show_widget` | 3 | 11 | 0 | 14 | 78.57% |
| `todowrite` | 2,949 | 10 | 0 | 2,959 | 0.34% |
| `agents_propose_team_memory` | 11 | 8 | 0 | 19 | 42.11% |
| `agents_assignment_status` | 70 | 7 | 0 | 77 | 9.09% |
| `resend_create-broadcast` | 0 | 5 | 0 | 5 | 100% |
| `agents_session_search` | 102 | 5 | 0 | 107 | 4.67% |
| `agents_retry_thread` | 6 | 5 | 0 | 11 | 45.45% |
| `rea_inspect_analysis_view` | 0 | 3 | 0 | 3 | 100% |
| `composio_COMPOSIO_MULTI_EXECUTE_TOOL` | 10 | 3 | 0 | 13 | 23.08% |
| `agents_attach_file` | 4 | 3 | 0 | 7 | 42.86% |
| `rea_capture_browser_scenario` | 1 | 2 | 0 | 3 | 66.67% |
| `computer_page` | 1 | 2 | 0 | 3 | 66.67% |
| `agents_tool_result_read` | 1 | 2 | 0 | 3 | 66.67% |
| `agents_session_read` | 7 | 2 | 0 | 9 | 22.22% |
| `agents_propose_profile` | 4 | 2 | 0 | 6 | 33.33% |

\* `Other` = `running` + `pending`. All remaining tools have ≤1 error; full `(tool × status)` matrix is in the SQL appendix (queries A2–A3) and the raw cell dumps (`...-02.txt` lines 10–223).

**Top-10 by volume (all statuses):** `bash` 78,923; `read` 52,581; `edit` 16,540; `grep` 15,156; `glob` 11,810; `write` 5,315; `todowrite` 2,959; `task` 2,051; `websearch` 830; `webfetch` 745.

**Reading:**
- `task`, `webfetch`, `websearch` are the highest-rate *frequent* tools (17.1%, 13.7%, 7.1%). Low-volume 100% failures are single-burst issues (e.g. `resend_create-broadcast` 0/5), not systemic risk.
- `bash` dominates volume but is resilient (0.49% error); its 30 `running` rows are the largest stuck-process cohort.

---

## 3. Top failed tools and error messages — last 30 days

Window: `part.time_created > MAX(part.time_created) - 30*86400*1000` → **2026-09-22 12:59:05 → 2026-10-22 12:59:05**.

### 3.1 Top failed tools (last 30 days)

| Tool | Failures (30d) | All-time errors | 30d share |
|---|---:|---:|---:|
| `edit` | **602** | 949 | 63.4% |
| `read` | **490** | 959 | 51.1% |
| `bash` | 247 | 387 | 63.8% |
| `glob` | 206 | 225 | 91.6% |
| `task` | 196 | 351 | 55.8% |
| `grep` | 144 | 196 | 73.5% |
| `webfetch` | 48 | 102 | 47.1% |
| `write` | 25 | 63 | 39.7% |
| `skill` | 22 | 26 | 84.6% |
| `websearch` | 18 | 59 | 30.5% |
| `agents_coordinate_bots` | 16 | 16 | 100% |
| `agents_show_widget` | 11 | 11 | 100% |
| `todowrite` | 9 | 10 | 90% |
| `question` | 8 | 18 | 44.4% |
| `agents_propose_team_memory` | 8 | 8 | 100% |
| `agents_assignment_status` | 7 | 7 | 100% |
| `resend_create-broadcast` | 5 | 5 | 100% |
| `agents_session_search` | 5 | 5 | 100% |
| `agents_retry_thread` | 5 | 5 | 100% |
| `rea_inspect_analysis_view` | 3 | 3 | 100% |

`glob` and `skill` failures are heavily concentrated in the last 30 days (91.6% / 84.6%) — current regressions, not historical. `edit` and `read` are the absolute leaders both periods.

### 3.2 Top error messages (last 30 days, `substr(error,1,160)`)

| Tool | Error (truncated to 160 chars) | n (30d) |
|---|---|---:|
| `edit` | Could not find oldString in the file. It must match exactly, including whitespace, indentation, and line endings. | **379** |
| `glob` | ripgrep execution failed | **199** |
| `grep` | Ripgrep JSON record exceeded 65536 bytes | **117** |
| `task` | Tool execution aborted | **101** |
| `edit` | No changes to apply: oldString and newString are identical. | 89 |
| `edit` | Found multiple matches for oldString. Provide more surrounding context to make the match unique. | 43 |
| `edit` | The edit tool was called with invalid arguments: SchemaError (Missing key at ["filePath"]). … | 43 |
| `bash` | Tool execution aborted | 34 |
| `edit` | SchemaError (Missing key at ["oldString"]). … | 17 |
| `write` | The user has specified a rule which prevents you from using this specific tool call. … | 16 |
| `bash` | SchemaError (Missing key at ["command"]). … | 15 |
| `read` | SchemaError (Missing key at ["filePath"]). … | 14 |
| `task` | Task cancelled | 14 |
| `grep` | ripgrep execution failed | 13 |
| `read` | The user rejected permission to use this specific tool call. | 12 |
| `skill` | Skill "one-skill-to-rule-them-all" not found. Available skills: … | 12 |
| `agents_coordinate_bots` | The originating room task is no longer running | 11 |
| `websearch` | Transport error (POST https://mcp.exa.ai/mcp) | 11 |
| `read` | Cannot read binary file: C:\Users\jmlus\light-speed-holdings\.env.example | 8 |
| `agents_propose_team_memory` | detail is at most 600 characters | 7 |
| `bash` | Unknown: ChildProcess.kill (… powershell.EXE …) — 7 each × 3 distinct commands (`$out=…`, `Get-NetTCPConnection…`, `Get-Process uvicorn…`) | 7×3 |
| `read` | File not found: …\harness\changes\active\summary.md | 7 |
| `read` | File not found: …\harness\evolution\pending.md | 6 |
| `webfetch` | Transport error (GET http://localhost:1441) | 6 |
| `task` | Subagent depth limit reached (1). … | 6 |

**Reading:** the top 4 messages account for `796` of `~2,030` last-30-day failures. `edit` argument mismatches (exact-match + uniqueness + no-op + schema) total `568` in-window — the single largest defect class. Ripgrep (`glob`/`grep`) failures total `~329` in-window and both implicate the ripgrep backend, not prompts.

### 3.3 Tool error totals (all time)

| Tool | Errors (all time) |
|---|---:|
| `read` | 959 |
| `edit` | 949 |
| `bash` | 387 |
| `task` | 351 |
| `glob` | 225 |
| `grep` | 196 |
| `webfetch` | 102 |
| `write` | 63 |
| `websearch` | 59 |
| `skill` | 26 |
| `question` | 18 |
| `agents_coordinate_bots` | 16 |
| `agents_show_widget` | 11 |
| `todowrite` | 10 |
| `agents_propose_team_memory` | 8 |
| `agents_assignment_status` | 7 |
| `resend_create-broadcast` | 5 |
| `agents_session_search` | 5 |
| `agents_retry_thread` | 5 |
| `rea_inspect_analysis_view` | 3 |

---

## 4. Repeated failures (all time, `HAVING n>1`) — defects: recurring

| Tool | Error (160-char prefix) | n | Sessions | First seen | Last seen |
|---|---|---:|---:|---|---|
| `edit` | Could not find oldString … match exactly … | **588** | **221** | 2026-08-07 | 2026-10-21 |
| `glob` | ripgrep execution failed | 216 | 33 | 2026-08-08 | 2026-10-22 |
| `edit` | No changes to apply: oldString and newString are identical. | 154 | 97 | 2026-08-10 | 2026-10-21 |
| `grep` | Ripgrep JSON record exceeded 65536 bytes | 140 | 107 | 2026-08-07 | 2026-10-22 |
| `task` | Tool execution aborted | 104 | 35 | 2026-09-04 | 2026-10-22 |
| `task` | Task cancelled | 91 | 27 | 2026-08-07 | 2026-10-16 |
| `edit` | Found multiple matches for oldString … | 74 | 51 | 2026-08-06 | 2026-10-22 |
| `edit` | SchemaError (Missing key at ["filePath"]) | 65 | 13 | 2026-08-18 | 2026-10-13 |
| `bash` | Tool execution aborted | 48 | 46 | 2026-08-06 | 2026-10-20 |
| `websearch` | StatusCode: non 2xx (429 POST https://search.parallels.ai/mcp) | 41 | 3 | 2026-09-13 | 2026-09-13 |
| `task` | Subagent depth limit reached (1) … | 40 | 10 | 2026-08-07 | 2026-10-07 |
| `write` | User rule prevents this tool call … | 29 | 20 | 2026-08-16 | 2026-10-07 |
| `write` | SchemaError (Missing key at ["filePath"]) | 24 | 11 | 2026-08-29 | 2026-10-21 |
| `bash` | Unknown: ChildProcess.kill (powershell … `cd C:\…`) | 21 | 7 | 2026-08-07 | 2026-10-16 |
| `edit` | SchemaError (Missing key at ["oldString"]) | 21 | 16 | 2026-08-16 | 2026-10-15 |
| `read` | File not found: …\harness\changes\active\summary.md | 21 | 20 | 2026-08-07 | 2026-10-12 |
| `read` | User rejected permission … | 21 | 12 | 2026-08-10 | 2026-10-22 |
| `bash` | SchemaError (Missing key at ["command"]) | 20 | 16 | 2026-08-16 | 2026-10-14 |
| `grep` | ripgrep execution failed | 20 | 18 | 2026-08-06 | 2026-10-19 |
| `read` | File not found: …\harness\evolution\pending.md | 19 | 19 | 2026-08-07 | 2026-10-11 |
| `read` | SchemaError (Missing key at ["filePath"]) | 19 | 13 | 2026-08-07 | 2026-10-20 |
| `grep` | Invalid ripgrep match output | 16 | 11 | 2026-08-06 | 2026-10-18 |
| `skill` | Skill "one-skill-to-rule-them-all" not found … | 12 | 10 | 2026-09-23 | 2026-09-23 |
| `agents_coordinate_bots` | Originating room task is no longer running | 11 | 5 | 2026-10-20 | 2026-10-22 |
| `websearch` | Transport error (POST https://mcp.exa.ai/mcp) | 11 | 3 | 2026-10-03 | 2026-10-03 |

**Recurring-defect reading:**
- Long-lived, cross-session: `edit` oldString mismatch (`588`, 221 sessions, 75-day span) and ripgrep record overflow (`140`, 107 sessions) are systemic — not one-off prompt errors.
- Bursty: `websearch` 429 (`41` in <1 hour, 2026-09-13) and `skill-not-found` (`12` in <5 hours, 2026-09-23) are single-incident bursts that self-resolved.
- Harness coupling: `harness/.../summary.md` + `pending.md` “File not found” (`21` + `19`) reflects agents probing a harness path outside its active state — low severity, high signal for prompt/context hygiene.

---

## 5. Files read >10 times (from `read` tool `$.state.input.filePath`)

Method: `GROUP BY json_extract(data,'$.state.input.filePath') HAVING COUNT(*)>10` over all `read` parts (**52,581** calls, **7,163** distinct paths). Note `filePath` is the *requested* path (directory reads and `tool-output` blobs included), not a canonicalized file.

**1,100 distinct paths were read more than 10 times.**

Top 20 (full >10 list is 50 rows in raw dump; top here serves as the required top-10+):

| # | `filePath` | Reads |
|---:|---|---:|
| 1 | `C:\Users\jmlus\light-speed-holdings\src\ai_company\dashboard\api.py` | **758** |
| 2 | `C:\Users\jmlus\light-speed-holdings\company-registry.yaml` | **655** |
| 3 | `C:\Users\jmlus\light-speed-holdings\AGENTS.md` | **425** |
| 4 | `C:\Users\jmlus\light-speed-holdings` (directory read) | 394 |
| 5 | `C:\Users\jmlus\light-speed-holdings\docs\STATUS.md` | 362 |
| 6 | `C:\Users\jmlus\light-speed-holdings\src\ai_company\dashboard\static\js\app.js` | 356 |
| 7 | `C:\Users\jmlus\light-speed-holdings\src\App.tsx` | 328 |
| 8 | `C:\Users\jmlus\light-speed-holdings\src\ai_company\dashboard\app.py` | 304 |
| 9 | `C:\Users\jmlus\.local\share\opencode\tool-output\tool_14ff7869e0017hJqN3xYM5Lft7` (opencode cache/blob path) | 288 |
| 10 | `C:\Users\jmlus\light-speed-holdings\harness\changes\active\summary.md` | 284 |
| 11 | `…\src\components\FloatingNav.tsx` | 258 |
| 12 | `…\src\data\siteContent.ts` | 257 |
| 13 | `…\src\ai_company\executor\loop.py` | 257 |
| 14 | `…\package.json` | 221 |
| 15 | `…\src\ai_company\model_router.py` | 211 |
| 16 | `…\docs\ECL.md` | 204 |
| 17 | `…\src\ai_company\generator.py` | 203 |
| 18 | `…\vite.config.ts` | 198 |
| 19 | `…\.github\workflows\ci.yml` | 191 |
| 20 | `…\src\ai_company\orchestrator\message_bus.py` | 186 |

Further high-signal reads (>100): `executor/agent_loop.py` 178, `HomePage.tsx` 173, `dashboard/data_service.py` 167, `harness/.../tasks.md` 167, `FloatingNav`/`generator`/`daemon` cluster, `athena/server.ts` 118 (outside-workspace, see §9), `brand/tokens/brand-tokens.json` 118.

**Reading:** `dashboard\api.py` + `company-registry.yaml` + `AGENTS.md` are the canonical hot trio (registry-as-source-of-truth is used as documented). The `tool-output` blob at #9 (288 reads) indicates agents re-reading large truncated tool outputs instead of re-running the tool — a cache/proxy pattern worth auditing.

---

## 6. Files created / edited (`write` + `edit` tool calls)

| Metric | Count |
|---|---:|
| `write` calls (all statuses) | **5,315** |
| Distinct `write` `filePath` | **4,262** |
| `edit` calls (all statuses) | **16,540** |
| Distinct `edit` `filePath` | **2,568** |
| `write` + `edit` calls combined | **21,855** |
| `write` with `NULL filePath` | 32 (schema violations — see §8) |
| `edit` with `NULL filePath` | 71 (schema violations — see §8) |

### 6.1 Top 20 files written

| # | `filePath` | Writes |
|---:|---|---:|
| 1 | `…\harness\changes\active\summary.md` | 52 |
| 2 | `…\harness\changes\active\tasks.md` | 48 |
| 3 | `…\harness\changes\active\plan.md` | 46 |
| 4 | `…\harness\changes\active\spec.md` | 44 |
| 5 | *(NULL filePath — missing argument)* | 32 |
| 6 | `…\harness\changes\active\reviews\review.md` | 26 |
| 7 | `…\.opencode\skills\archify\examples\message-bus.architecture.json` | 14 |
| 8 | `…\src\components\FloatingNav.tsx` | 11 |
| 9 | `…\ecosystem.config.cjs` | 10 |
| 10 | `…\scripts\build\generate-favicons.py` | 9 |
| 11 | `…\lightspeed-main-site\src\components\LightSpeedCore.astro` | 9 |
| 12 | `…\survey\free-tier-cloud-deployment\sources.tsv` | 8 |
| 13 | `…\tests\unit\test_ecl_change_lifecycle.py` | 7 |
| 14 | `…\src\components\HeroSection.tsx` | 7 |
| 15 | `C:\Users\jmlus\AppData\Local\Temp\opencode\pr-body.md` (outside) | 7 |
| 16 | `…\src\pages\HomePage.tsx` | 6 |
| 17 | `…\src\components\AboutSection.tsx` | 6 |
| 18 | `…\src\components\AiCompanyBuilder\AgentGrid.tsx` | 6 |
| 19 | `…\scripts\capture-fix.ps1` | 6 |
| 20 | `…\_tmp_window_scan.py` | 6 |

`write` is harness-heavy: the top 6 rows are all `harness/changes/active/*` (ECL change lifecycle), which is by design.

### 6.2 Top 20 files edited

| # | `filePath` | Edits |
|---:|---|---:|
| 1 | `…\src\ai_company\dashboard\api.py` | **216** |
| 2 | `…\src\data\siteContent.ts` | 134 |
| 3 | `…\harness\changes\active\summary.md` | 130 |
| 4 | `…\src\components\FloatingNav.tsx` | 129 |
| 5 | `…\AGENTS.md` | 127 |
| 6 | `…\company-registry.yaml` | 108 |
| 7 | `…\src\ai_company\dashboard\static\js\app.js` | 90 |
| 8 | `…\docs\STATUS.md` | 90 |
| 9 | `…\harness\changes\active\tasks.md` | 88 |
| 10 | `…\src\ai_company\archify\converter.py` | 83 |
| 11 | `…\src\App.tsx` | 83 |
| 12 | `…\README.md` | 82 |
| 13 | `…\src\ai_company\executor\loop.py` | 79 |
| 14 | `C:\Users\jmlus\athena\src\components\views\DocumentStudioView.tsx` (outside) | 78 |
| 15 | `C:\Users\jmlus\athena\frontend\src\pages\athena\DocumentStudio.tsx` (outside) | 78 |
| 16 | `…\src\components\AskLightSpeed.tsx` | 77 |
| 17 | `…\src\components\HeroSection.tsx` | 75 |
| 18 | `…\src\ai_company\dashboard\app.py` | 74 |
| 19 | `…\src\ai_company\executor\agent_loop.py` | 71 |
| 20 | *(NULL filePath)* | 71 |

`dashboard\api.py` is both the most-read (758) and most-edited (216) file — the highest-churn surface in the DB.

---

## 7. Cache reads

Searched `part.data` for `cache` / `cacheRead` forms and summed the structured fields. All three stores agree — there is no hidden second cache.

| Probe | Count |
|---|---:|
| `step-finish` parts (`$.type='step-finish'`) | 132,342 |
| … with `$.tokens.cache.read > 0` | **120,113** (90.8%) |
| Sum `$.tokens.cache.read` (step-finish) | **15,210,842,514** |
| Sum `$.tokens.cache.write` (step-finish) | **0** |
| Sum `$.tokens.input` (step-finish) | 1,699,925,967 |
| Sum `$.tokens.output` (step-finish) | 65,346,163 |
| `part.data LIKE '%cache%'` | 151,751 |
| `part.data LIKE '%cacheRead%' OR '%cache_read%'` | 61 (camel/snake variants — rare; canonical form is `$.tokens.cache.read`) |
| `message` rows with `$.tokens.cache.read > 0` | **120,115** |
| Sum `message` cache read | 15,211,024,018 (differs from step-finish by 181,504 — live-DB drift + rounding; orders match) |
| Sum `message` cache write | **0** |
| Sessions with `tokens_cache_read > 0` (`session.*`) | **2,824 / 3,131** (90.2%) |
| Sum `session.tokens_cache_read` | **15,210,842,514** (exactly equals step-finish sum) |
| Sum `session.tokens_cache_write` | **0** |

**Cache hit framing:** cache reads are `~8.9×` input tokens (`15.21B / 1.70B`). Only `(132,342 − 120,113) = 12,229` step-finish parts have zero cache reads (early/cold sessions).

**Top 10 sessions by `tokens_cache_read`:**

| Session | Directory | Cache read | Input | Output |
|---|---|---:|---:|---:|
| `ses_f1ad097c3ffeVswldO0n1S03CK` | `light-speed-holdings` | **377,687,040** | 23,135,370 | 135,754 |
| `ses_ec69e11ecffeP2H1ELrwXsDoGd` | `light-speed-holdings` | 184,521,632 | 8,930,740 | 299,188 |
| `ses_f2c106213ffeUqir20GBDbRChT` | `light-speed-holdings` | 160,256,960 | 9,860,352 | 254,421 |
| `ses_f2a05aab5ffeS03q66MyAfi5ob` | `light-speed-holdings` | 159,150,400 | 15,529,616 | 246,781 |
| `ses_f01fa228effeAaAwBnXW55Lwo0` | `athena` | 146,366,432 | 12,854,781 | 244,140 |
| `ses_ea71bb558ffeQeKIyl8do6LAwi` | `light-speed-holdings` | 142,417,552 | 7,607,226 | 253,995 |
| `ses_fef729edbffe6GFeR3v7Y0eTAV` | `light-speed-holdings` | 133,519,536 | 7,500,582 | 234,162 |
| `ses_eed7f72ddffeFRrLQsBW733Zat` | `light-speed-holdings` | 131,539,564 | 9,860,159 | 93,256 |
| `ses_f1b449f94ffe37Arttxz11HhX0` | `light-speed-holdings` | 123,389,536 | 15,660,074 | 210,140 |
| `ses_ef4f9ba66ffeRpsdwWFErp1ISu` | `athena` | 121,901,915 | 10,977,537 | 205,055 |

> **Anomaly:** cache-write is uniformly `0` across `session`, `message`, and `part` while reads are 15.2B. The recorded cache-write signal is unusable — do not report “0 writes” as a finding about the provider.

---

## 8. Defects and anomalies

### 8.1 Tool errors (summary)

- **3,435** tool parts have `status='error'` (1.82% of tool parts). Top tools: `read` 959, `edit` 949, `bash` 387, `task` 351, `glob` 225, `grep` 196 (§2–§3). Recurring groups in §4.
- **Repeated failures** are the dominant defect: the top-10 repeated `(tool, error)` groups sum to **>1,400** errors. `edit` exact-match + ripgrep overflow are the two systemic classes.

### 8.2 Repeated `bash` stdout errors (skill-template probe)

Completed `bash` calls whose `output LIKE '%error%'` (case-sensitive): **22,619 / 78,506** (`28.8%`). This is a *keyword hit*, not a failure — most are PowerShell error strings in otherwise-completed commands. Do not treat as error rate; use `status='error'` (`387`) for true `bash` failures.

### 8.3 Timeouts

- Naive `data LIKE '%timeout%'` (error **or** output): **9,995** — **noisy, do not cite**. Most hits are completed outputs merely mentioning “timeout”.
- **Refined:** `status='error' AND error LIKE '%timeout%'`: **66**. Top: `bash` SchemaError mentioning timeout argument (`3`), `ChildProcess.kill` PowerShell kills (`~8` across distinct commands), 1× `FileSystem.access … failed after 30.0s timeout:not running`. True timeout failures are rare; PowerShell `ChildProcess.kill` is the more common kill signature (see §4).

### 8.4 Large outputs

| Probe | Count |
|---|---:|
| Completed tool outputs `>50,000` chars | **1,641** |
| Completed tool outputs `>100,000` chars | **5** |

**Top 15 largest completed outputs (`length($.state.output)`):**

| Tool | Length | Preview (100 chars) | Session |
|---|---:|---|---|
| `read` | **131,055** | `<path>…\open-design\apps\daemon\src\deploy.ts</path>` | `ses_efc5d2b69…` |
| `grep` | 130,806 | `Found 100 matches (more matches available) …\.opencode\skills\arch…` | `ses_f2fe38398…` |
| `grep` | 121,716 | `Found 100 matches …\brand-strategy-valida…` | `ses_f2fe38398…` |
| `grep` | 113,369 | `Found 100 matches …\brand\digital\social\…` | `ses_f2fe3c900…` |
| `grep` | 105,173 | `Found 100 matches …\static\brand\CHANGELO…` | `ses_f2a4a06b5…` |
| `grep` | 96,262 | `Found 100 matches …brand\digital\social…` | `ses_f30fd1a31…` |
| `grep` | 95,749 | `Found 100 matches …` | `ses_f2fe3c900…` |
| `grep` | 92,200 | `Found 100 matches …\dashboard\kpi_history…` | `ses_f2fe3c900…` |
| `grep` | 89,913 | `Found 100 matches …\brand\LightSpeed Hold…` | `ses_f8c838f86…` |
| `grep` | 89,816 | `Found 100 matches …\.ai-company\state\DAS…` | `ses_f89c24f15…` |
| `read` | 88,837 | `<path>…\open-design\packages\contracts\…\mapper…` | `ses_f143de803…` |
| `grep` | 87,157 | `Found 100 matches …\docs\AI_PROVIDER_COMP…` | `ses_ea2ba4d10…` |
| `grep` | 87,082 | `Found 100 matches …` | `ses_ea2ba4d10…` |
| `grep` | 85,304 | `Found 100 matches …\.pre-commit-config.ya…` | `ses_ec4ea2648…` |
| `grep` | 84,687 | `Found 100 matches …\brand\tokens.md: Li…` | `ses_f1b25d7e4…` |

Pattern: large outputs are almost all `grep` “Found 100 matches (more matches available)” floods over `brand/` + `docs/` + `.opencode/skills/`. Capping `grep` matches would remove most of the >50k tail.

### 8.5 Non-terminal residue

| Status | Count | Leading tool |
|---|---:|---|
| `running` | **93** | `task` 51, `bash` 30, `question` 10 |
| `pending` | **2** | `write` 2 |

`93` `running` parts never reached `completed`/`error` — killed/abandoned sessions. `task` dominates (51/93), consistent with its 17.1% error rate and `Tool execution aborted` / `Task cancelled` bursts.

### 8.6 Schema violations (missing required arguments)

`edit`/`write`/`read`/`bash` SchemaError groups (all-time recurring, §4):
- `edit` missing `filePath` 65 + `oldString` 21; `write` missing `filePath` 24; `read` missing `filePath` 19; `bash` missing `command` 20.
- `NULL filePath` in group-by: `write` 32, `edit` 71 — attempts with no target path. These fail validation before execution; agents should be pre-validated, not post-errored.

### 8.7 Other anomalies

- **Empty secondary tables:** `session_part` (0) while `session_message` has 9,284 rows — the v2 part writer is not populating `session_part`. Any consumer joining `session_part` will silently return zero.
- **`event` (0) vs `event_sequence` (3,530):** sequence rows exist without their events — orphan bookkeeping.
- **17–18 sessions** have no messages/parts (created but never used).
- **Cache-write = 0** (§7) — recorder/provider gap.

---

## 9. Artifacts outside `C:\Users\jmlus\light-speed-holdings`

**Strict definition:** path `NOT LIKE 'C:\Users\jmlus\light-speed-holdings%'` (backslashes; `json_extract` returns unescaped single backslash) for `filePath`/`workdir`, and `directory != 'C:/Users/jmlus/light-speed-holdings'` (forward slashes) for `session.directory`. Historical sibling `light-speed-holdings-main` is therefore counted as outside — correct per the current workspace, but see the note below: early DB rows reference `light-speed-holdings-main` as the then-active workspace, so a portion of “outside” is workspace-move, not stray writes.

### 9.1 Sessions by directory

| Scope | Sessions | % |
|---|---:|---:|
| Inside `C:/Users/jmlus/light-speed-holdings` (exact) | **2,811** | 89.8% |
| Outside (any other `directory`) | **320** | 10.2% |

**134 distinct `session.directory` values.** Top directories:

| `directory` | Sessions |
|---|---:|
| `C:/Users/jmlus/light-speed-holdings` | 2,811 |
| `C:/Users/jmlus/athena` | 114 |
| `C:/Users/jmlus/.openmausbot/providers/opencode/discovery` | 17 |
| `C:/Users/jmlus/.openmausbot/task-workspaces/…` (each) | 9, 5, 5, 3, 3, 2, 2 … |
| `C:/` | 7 |
| `C:/Users/jmlus/.openmausbot/JobSearch` | 6 |
| `C:/Users/jmlus/social-media-automation-os` | 5 |
| `C:/Users/jmlus/light-speed-holdings-main/ai-company` | 5 |
| `C:/Users/jmlus/light-speed-holdings-main` | 5 |
| `C:/Users/jmlus/.openmausbot` | 5 |
| `C:/Users/jmlus` | 5 |
| `C:/Users/jmlus\AppData/Roaming/Open Design/…` | 4, 2, 2 |

`athena` (114 sessions) is the only other substantive workspace; the rest are `openmausbot` task workspaces, `Temp/opencode` sandboxes, and root-level probes.

### 9.2 File-tool paths outside workspace

| Tool | Total calls | Outside (strict) | Inside | Outside % |
|---|---:|---:|---:|---:|
| `read` | 52,581 | **8,154** | 44,404 | 15.5% |
| `write` | 5,315 | **1,960** | 3,355 | **36.9%** |
| `edit` | 16,540 | **3,226** | 13,314 | 19.5% |

Most of the read total includes `NULL filePath` not matching `LIKE` — but the strict outside counts above exclude `NULL` correctly (see appendix SQL; `NOT LIKE` with `NULL` yields no row, so outside counts are of *named* outside paths only; the difference `total − inside − outside` = `NULL` + unclassified, e.g. read `52,581 − 44,404 − 8,154 = 23` NULL/edge rows).

**Top outside reads (25):**

| `filePath` | Reads |
|---|---:|
| `C:\Users\jmlus\.local\share\opencode\tool-output\tool_14ff7869e0017hJqN3xYM5Lft7` | 288 |
| `C:\Users\jmlus\athena\server.ts` | 118 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\DocumentStudio.tsx` | 117 |
| `C:\Users\jmlus\athena\backend\src\athena\api\routes.py` | 105 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\Dashboard.tsx` | 99 |
| `C:\Users\jmlus\athena\backend\src\athena\api\app.py` | 99 |
| `C:\Users\jmlus\athena\src\components\views\DocumentStudioView.tsx` | 96 |
| `C:\Users\jmlus\.openmausbot\JobSearch\Master_Resume\Jacob_Mlusu_Master_Resume.md` | 96 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\JobList.tsx` | 86 |
| `C:\Users\jmlus\athena\frontend\src\lib\athena\types.ts` | 76 |
| `C:\Users\jmlus\athena\backend\src\athena\store.py` | 65 |
| `C:\Users\jmlus\athena\frontend\src\App.tsx` | 63 |
| `C:\Users\jmlus\athena\package.json` | 62 |
| `C:\Users\jmlus\athena\frontend\src\lib\athena\api.ts` | 61 |
| `C:\Users\jmlus\athena\frontend\e2e\playwright.config.ts` | 56 |
| `C:\Users\jmlus\athena\backend\src\athena\api\schemas.py` | 53 |
| `C:\Users\jmlus\.openmausbot\JobSearch\Site_Playbooks\jobs.mw.md` | 53 |
| `C:\Users\jmlus\athena\backend\pyproject.toml` | 52 |
| `C:\Users\jmlus\athena\.github\workflows\ci.yml` | 49 |
| `C:\Users\jmlus\athena\backend\src\athena\scheduler\jobs.py` | 48 |
| `C:\Users\jmlus\AppData\Local\Temp\opencode\extract_docx.py` | 48 |
| `C:\Users\jmlus\athena\frontend\src\components\athena\AthenaLayout.tsx` | 47 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\FormFillerModal.tsx` | 45 |
| `C:\Users\jmlus\athena\frontend\e2e\tests\visual-regression.spec.ts` | 42 |
| `C:\Users\jmlus\athena\backend\src\athena\automation\submitter.py` | 42 |

Outside reads are concentrated in `athena` (its own workspace) + `openmausbot/JobSearch` + the opencode tool-output cache. These map to the 114 `athena` sessions — not spillover from workspace sessions.

**Top outside writes (25):**

| `filePath` | Writes |
|---|---:|
| `C:\Users\jmlus\AppData\Local\Temp\opencode\pr-body.md` | 7 |
| `C:\Users\jmlus\athena\frontend\e2e\tests\visual-regression.spec.ts` | 6 |
| `C:\Users\jmlus\AppData\Local\Temp\opencode\issue_body.md` | 6 |
| `C:\Users\jmlus\athena\SPEC.md` | 5 |
| `C:\Users\jmlus\athena\test-server.mjs` | 4 |
| `C:\Users\jmlus\athena\tasks\todo.md` | 4 |
| `C:\Users\jmlus\athena\seed_staging.py` | 4 |
| `C:\Users\jmlus\athena\frontend\src\index.css` | 4 |
| `C:\Users\jmlus\athena\frontend\Dockerfile` | 4 |
| `C:\Users\jmlus\athena\backend\src\athena\lockfile.py` | 4 |
| `C:\Users\jmlus\athena\.env.example` | 4 |
| `…\Temp\opencode\wt-cj-ecl-close\harness\qa\tmp_contact.cjs` | 4 |
| `C:\Users\JMLUS\social-media-automation-os\apps\worker\Dockerfile` | 4 |
| `C:\Users\JMLUS\social-media-automation-os\apps\api\Dockerfile` | 4 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\FormFillerModal.tsx` | 3 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\Dashboard.tsx` | 3 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\ApplicantProfile.tsx` | 3 |
| `C:\Users\jmlus\athena\frontend\src\components\athena\ui\index.ts` | 3 |
| `C:\Users\jmlus\athena\docs\DATA_STORES.md` | 3 |
| `C:\Users\jmlus\athena\backend\tests\test_ai_providers.py` | 3 |
| `C:\Users\jmlus\athena\backend\Dockerfile` | 3 |
| `C:\Users\jmlus\athena\ARCHITECTURE.md` | 3 |
| `C:\Users\jmlus\athena\.github\workflows\e2e.yml` | 3 |
| `C:\Users\jmlus\athena\.github\workflows\ci.yml` | 3 |

**Top outside edits (25):**

| `filePath` | Edits |
|---|---:|
| `C:\Users\jmlus\athena\src\components\views\DocumentStudioView.tsx` | 78 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\DocumentStudio.tsx` | 78 |
| `C:\Users\jmlus\athena\server.ts` | 67 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\JobList.tsx` | 58 |
| `C:\Users\jmlus\athena\backend\src\athena\api\routes.py` | 50 |
| `C:\Users\jmlus\athena\backend\src\athena\api\app.py` | 48 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\FormFillerModal.tsx` | 38 |
| `C:\Users\jmlus\athena\backend\src\athena\store.py` | 37 |
| `C:\Users\jmlus\athena\frontend\src\components\athena\AthenaLayout.tsx` | 36 |
| `C:\Users\jmlus\athena\frontend\src\pages\athena\Dashboard.tsx` | 34 |
| `C:\Users\jmlus\athena\frontend\e2e\playwright.config.ts` | 32 |
| `C:\Users\jmlus\athena\backend\src\athena\automation\submitter.py` | 29 |
| `C:\Users\jmlus\athena\frontend\src\App.tsx` | 28 |
| `…\Temp\opencode\wf-map-body.md` | 23 |
| `C:\Users\jmlus\athena\frontend\src\components\athena\MetricCard.tsx` | 22 |
| `C:\Users\jmlus\athena\src\components\views\PipelineView.tsx` | 21 |
| `C:\Users\jmlus\athena\src\App.tsx` | 21 |
| `C:\Users\jmlus\athena\e2e\aistudio\real-data.spec.ts` | 21 |
| `…\Temp\opencode\ls-haomtgv-fixes\src\components\haomtgv\HaomtgvBlueprintHero.tsx` | 21 |
| `C:\Users\jmlus\athena\frontend\src\components\athena\AutomationControls.tsx` | 20 |
| `C:\Users\jmlus\athena\src\components\charts\MetricsAndBarChart.tsx` | 19 |

### 9.3 Bash workdir outside workspace

| Probe | Count |
|---|---:|
| `bash` calls with `workdir IS NOT NULL` | 31,226 / 78,923 (39.6%) |
| … with `workdir NOT LIKE 'C:\Users\jmlus\light-speed-holdings%'` | **5,063** (16.2% of with-workdir) |

Top 20 `bash` workdirs:

| `workdir` | Calls |
|---|---:|
| `C:\Users\jmlus\light-speed-holdings` | 22,999 |
| `C:\Users\jmlus\light-speed-holdings\ai-company` | 2,104 |
| `C:\Users\jmlus\athena` | 2,003 |
| `C:\Users\jmlus\social-media-automation-os` | 451 |
| `C:\Users\jmlus\athena\frontend` | 371 |
| `C:\Users\jmlus\athena\backend` | 358 |
| `C:\Users\jmlus\light-speed-holdings\lightspeed-main-site` | 210 |
| `…\Temp\opencode\wt-cj-ecl-close` | 161 |
| `/c/Users/jmlus/light-speed-holdings` (Git Bash path form) | 139 |
| `C:\Users\jmlus\light-speed-holdings-p0` | 135 |
| `…\Temp\opencode\mimo-integration` | 126 |
| `…\Temp\opencode\d6-relocation` | 121 |
| `C:\Users\jmlus\.openmausbot` | 89 |
| `C:\Users\JMLUS\social-media-automation-os` | 89 |
| `C:\Users\jmlus` | 82 |
| `C:\Users\jmlus\light-speed-holdings\jev` | 61 |
| `…\Temp\opencode\wt-deck-qa` | 56 |
| `…\light-speed-holdings\marketing-site` | 48 |
| `…\light-speed-holdings\jev\jev` | 46 |
| `…\light-speed-holdings\.worktrees\httpx2-migration-1012a` | 45 |

**Note on `light-speed-holdings-main`:** early `read`/`bash` samples reference `C:\Users\jmlus\light-speed-holdings-main` (and `...-main\ai-company`). Current `session.directory` counts show only 10 sessions there (`5 + 5`), so the strict-outside file-path tallies in §9.2 are dominated by `athena`/`Temp`/`tool-output`, not by the `-main` move. No finding of mass writes outside either workspace was observed — outside activity is almost entirely `athena` work plus temp/scratch writes (`pr-body.md`, `issue_body.md`, `wf-map-body.md`).

### 9.4 `project.worktree` (72 projects)

Most recent `project` rows point at `C:/tmp`, `Temp/opencode/uploads/...`, `.config/opencode`, and `.local/share/opencode/worktree/9930fa/*` scratch worktrees — i.e. project records are heavily scratch/worktree-based, not only the main checkout. `project_directory` and `worktree` each hold 7 rows. This corroborates that outside paths are expected scratch work, not necessarily escapes.

---

## 10. SQL proof (exact queries)

All run as `sqlite3 -readonly -header -column "C:\Users\jmlus\.local\share\opencode\opencode.db"` (via `Get-Content *.sql | sqlite3 -readonly …` batch files). `time_created` is ms; `datetime(.../1000,'unixepoch','localtime')` is used for display. JSON paths use `json_extract()` per the skill template.

### A. Totals (§1)

```sql
SELECT 'session' AS tbl, COUNT(*) AS n FROM session
UNION ALL SELECT 'session_v2', COUNT(*) FROM session_v2
UNION ALL SELECT 'message', COUNT(*) FROM message
UNION ALL SELECT 'session_message', COUNT(*) FROM session_message
UNION ALL SELECT 'part', COUNT(*) FROM part
UNION ALL SELECT 'session_part', COUNT(*) FROM session_part
UNION ALL SELECT 'todo', COUNT(*) FROM todo
UNION ALL SELECT 'job', COUNT(*) FROM job
UNION ALL SELECT 'project', COUNT(*) FROM project;

SELECT datetime(MIN(time_created)/1000,'unixepoch','localtime') AS session_min,
       datetime(MAX(time_created)/1000,'unixepoch','localtime') AS session_max
FROM session;

SELECT json_extract(data,'$.role') AS role, COUNT(*) AS n
FROM message GROUP BY role ORDER BY n DESC;

SELECT json_extract(data,'$.type') AS part_type, COUNT(*) AS n
FROM part GROUP BY part_type ORDER BY n DESC;

SELECT COUNT(DISTINCT agent) AS distinct_session_agents FROM session;
SELECT agent, COUNT(*) AS n FROM session GROUP BY agent ORDER BY n DESC LIMIT 30;
SELECT status, COUNT(*) AS n FROM todo GROUP BY status ORDER BY n DESC;
SELECT SUM(tokens_input) AS sum_input, SUM(tokens_output) AS sum_output,
       SUM(tokens_reasoning) AS sum_reasoning,
       SUM(tokens_cache_read) AS sum_cache_read,
       SUM(tokens_cache_write) AS sum_cache_write, SUM(cost) AS sum_cost
FROM session;
```

### B. Tool breakdown (§2)

```sql
SELECT json_extract(data,'$.state.status') AS status, COUNT(*) AS n
FROM part WHERE json_extract(data,'$.type')='tool' GROUP BY status ORDER BY n DESC;

SELECT json_extract(data,'$.tool') AS tool,
       json_extract(data,'$.state.status') AS status, COUNT(*) AS n
FROM part WHERE json_extract(data,'$.type')='tool' GROUP BY tool, status;

SELECT tool, SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) AS completed_n,
       SUM(CASE WHEN status='error' THEN 1 ELSE 0 END) AS error_n,
       COUNT(*) AS total_n,
       ROUND(100.0*SUM(CASE WHEN status='error' THEN 1 ELSE 0 END)/COUNT(*),2) AS err_pct
FROM (SELECT json_extract(data,'$.tool') AS tool,
             json_extract(data,'$.state.status') AS status
      FROM part WHERE json_extract(data,'$.type')='tool')
GROUP BY tool ORDER BY error_n DESC;
```

### C. Last-30-day failures (§3)

```sql
SELECT MAX(time_created) AS part_max_ms,
       datetime(MAX(time_created)/1000,'unixepoch','localtime') AS part_max_local
FROM part;

SELECT json_extract(data,'$.tool') AS tool, COUNT(*) AS failures
FROM part
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status')='error'
  AND time_created > (SELECT MAX(time_created) FROM part) - 30*86400*1000
GROUP BY tool ORDER BY failures DESC LIMIT 20;

SELECT json_extract(data,'$.tool') AS tool,
       substr(json_extract(data,'$.state.error'),1,160) AS error_msg, COUNT(*) AS n
FROM part
WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.state.status')='error'
  AND time_created > (SELECT MAX(time_created) FROM part) - 30*86400*1000
GROUP BY tool, error_msg ORDER BY n DESC LIMIT 30;
```

### D. Repeated failures (§4) — skill-template pattern

```sql
SELECT json_extract(data,'$.tool') AS tool,
       substr(json_extract(data,'$.state.error'),1,160) AS error_msg,
       COUNT(*) AS n, COUNT(DISTINCT session_id) AS sessions,
       datetime(MIN(time_created)/1000,'unixepoch','localtime') AS first_seen,
       datetime(MAX(time_created)/1000,'unixepoch','localtime') AS last_seen
FROM part
WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.state.status')='error'
GROUP BY tool, error_msg HAVING n>1 ORDER BY n DESC LIMIT 30;
```

Also (skill template: completed `bash` stdout errors):
```sql
SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='bash'
  AND json_extract(data,'$.state.status')='completed'
  AND json_extract(data,'$.state.output') LIKE '%error%';
```

### E. Files read / written (§5–§6)

```sql
SELECT COUNT(*) AS read_total FROM part
WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='read';

SELECT COUNT(DISTINCT json_extract(data,'$.state.input.filePath')) AS distinct_files_read
FROM part WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='read';

SELECT json_extract(data,'$.state.input.filePath') AS filePath, COUNT(*) AS n
FROM part WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='read'
GROUP BY filePath HAVING n>10 ORDER BY n DESC LIMIT 50;

SELECT json_extract(data,'$.state.input.filePath') AS filePath, COUNT(*) AS n
FROM part WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='write'
GROUP BY filePath ORDER BY n DESC LIMIT 20;
-- same pattern with 'edit' for §6.2
```

### F. Cache (§7)

```sql
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='step-finish';
SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.type')='step-finish' AND json_extract(data,'$.tokens.cache.read')>0;
SELECT SUM(json_extract(data,'$.tokens.cache.read')) AS read_sum,
       SUM(json_extract(data,'$.tokens.cache.write')) AS write_sum
FROM part WHERE json_extract(data,'$.type')='step-finish';
SELECT COUNT(*) FROM part WHERE data LIKE '%cache%';
SELECT COUNT(*) FROM part WHERE data LIKE '%cacheRead%' OR data LIKE '%cache_read%';
SELECT COUNT(*) FROM message WHERE json_extract(data,'$.tokens.cache.read')>0;
SELECT SUM(tokens_cache_read) FROM session;
```

### G. Defects: large outputs / timeouts / residue (§8)

```sql
SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.state.status')='completed'
  AND length(json_extract(data,'$.state.output'))>50000;

SELECT json_extract(data,'$.tool') AS tool,
       length(json_extract(data,'$.state.output')) AS out_len,
       substr(json_extract(data,'$.state.output'),1,100) AS preview, session_id
FROM part
WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.state.status')='completed'
ORDER BY out_len DESC LIMIT 15;

SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.state.status')='error'
  AND json_extract(data,'$.state.error') LIKE '%timeout%';

SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.state.status')='running';
```

### H. Outside workspace (§9)

```sql
SELECT COUNT(*) FROM session WHERE directory != 'C:/Users/jmlus/light-speed-holdings';
SELECT directory, COUNT(*) AS n FROM session GROUP BY directory ORDER BY n DESC LIMIT 25;

SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='read'
  AND json_extract(data,'$.state.input.filePath') NOT LIKE 'C:\Users\jmlus\light-speed-holdings%';
-- same NOT LIKE pattern for write/edit; and for bash workdir:
SELECT COUNT(*) FROM part
WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='bash'
  AND json_extract(data,'$.state.input.workdir') NOT LIKE 'C:\Users\jmlus\light-speed-holdings%';
SELECT json_extract(data,'$.state.input.workdir') AS wd, COUNT(*) AS n
FROM part WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='bash'
GROUP BY wd ORDER BY n DESC LIMIT 20;
```

**Repro:** run any block above via
`Get-Content <file.sql> | sqlite3 -readonly "C:\Users\jmlus\.local\share\opencode\opencode.db"`.
Raw column dumps for every batch were captured to `C:\Users\jmlus\AppData\Local\Temp\opencode\opencode-analytics-*.txt` (01, 02, 02b, 02c, 03a, 03a2, 03b, 03c, 03d, 03d2) and are not committed.

---

## 11. Caveats — what was not verified

- **Not verified:** whether `session` rows flagged `time_archived` should be excluded from “active” counts; no archived-status filter was applied.
- **Not verified:** `session_v2` / `session_message` semantics (94 / 9,284 rows) — reported separately; no join was attempted between v1 and v2 keys.
- **Not verified:** message-level `agent` distribution (JSON `$.agent` in `message.data`) — actor counts are from `session.agent` (123 distinct) only. The count may differ at message grain.
- **Not verified:** cost/token accuracy — `session.cost` sums to 5.59 and cache-write is `0`; both are treated as recorder outputs, not audited billing.
- **Partial runs:** the full `(tool × status)` matrix and 50-row `>10` read list were captured as raw text dumps; this file reproduces the top-20 tables. Full 188,713-part tool matrix is available via query B above.
- **Live-DB drift:** see header. Re-run §10 queries to get a fresh snapshot; expect small deltas.

## 12. Execution integrity

- Requested: read-only trajectory audit with eight metric families, evidence file, structured counts + top-10 lists, exact SQL.
- Attempted: all queries via `sqlite3 -readonly` against `C:\Users\jmlus\.local\share\opencode\opencode.db`; `--help`/schema probes confirmed 3.0 GiB DB, `VAR`/live writes observed.
- Actually happened: 01 / 02 / 02b / 02c / 03a (partial) / 03a2 / 03b / 03c / 03d (partial) / 03d2 batches completed; two long batches exceeded the 120s shell timeout and were split and completed. No writes to the DB; temp SQL/TXT files were written to `AppData\Local\Temp\opencode`, not to the DB.
- Independently verified: every number in §1–§9 appears verbatim in a captured raw dump (or is arithmetic on such numbers: percentages, differences, 30d shares). SQL in §10 reproduces them.
- Remains unknown: cause of intra-audit row growth with old timestamps (`session_v2` +3, `session_message` +112 while `MAX(time_created)` stayed at 2026-10-22). No explanation is offered without evidence.
