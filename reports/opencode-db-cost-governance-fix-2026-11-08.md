# opencode.db — Cost / Ownership / Governance Fix Plan — 2026-11-08

**Author:** vp-engineering (absorbs CTO execution layer), LightSpeed Holdings
**Date:** 2026-11-08
**Status:** Plan only — no code, DB, or outside-workspace files changed. This report is the sole artifact (inside workspace).
**Sources (read-only evidence):**

- `reports/opencode-db-audit-2026-11-08.md` — chief-of-staff locate/size/integrity/trajectory audit (3.0 GiB live DB, WAL 2.95 GiB, `.bak` 38.5 GB, 72 projects)
- `reports/opencode-db-security-2026-11-08.md` — ciso security audit (ACL/orphan-SID, credential exposure, third-party transmission, retention)
- `reports/opencode-db-analytics-2026-11-08.md` — trajectory analytics (tool/file/cache breakdowns)
- `docs/APPROVED-VENDORS.md` v1.0 2026-09-23 + AGENTS.md §9.2 Skill Third-Party Transmission Ban (90-day window, CEO/CISO re-sign)
- Existing cost stack (inspected, not modified): `src/ai_company/data/cost_analytics.py` (`CostAnalytics`), `src/ai_company/llm/cost_tracker.py` (`CostTracker` + `MODEL_COSTS`), `src/ai_company/llm/opencode_usage.py` (read-only `opencode.db` → `cost_records` importer), `src/ai_company/cli/executor.py` (`_resolve_budgets` / `guardrails.yaml: llm_budgets`), `src/ai_company/dashboard/kpis/finance.py` (`FinanceKPICollector`), `src/ai_company/dashboard/api.py` (cost sections from `orchestrator/cost_tracker.json`)

**Scope:** Cost, ownership, and governance fixes only. At-rest encryption, ACL lockdown, secret redaction, and credential rotation are owned by ciso per the security audit R1–R3 and are referenced as dependencies, not duplicated, here. No files outside `C:\Users\jmlus\light-speed-holdings` are written by this plan (operations on `~/.local/share/opencode/opencode.db*`, `Temp\opencode`, sibling repos are described as gated maintenance-window steps requiring explicit operator action).

---

## 0. Executive summary

opencode.db is a ~6.4 GB live store (3.00 GiB DB + 2.95 GiB WAL) plus a 38.5 GB pre-v2 `.bak`, holding 95 days of verbatim trajectories (2026-08-05 → 2026-11-08). Token burn is massive and **invisible to current cost controls**: 15.21B cache-reads at 8.95× input (v1) / 9.72× (v2), with `cache_write = 0` everywhere and total paid cost of only $5.59 because the dominant models are priced $0.00 in `MODEL_COSTS`. A single session burned 377M cache-reads; the worst v2 session burned 26.8M input tokens. Meanwhile 1,442 files are re-read >10× (`api.py` 974×), 13,126 file ops happen outside the workspace, `Temp\opencode` accrues 31,217 files with no retention job, and 72 `project` rows exist with no budget or GC policy.

Current controls cannot catch this: `CostAnalytics` and executor budgets are **USD-only** (`daily_budget_usd` / `task_budget_usd`, default `None` = unlimited in `guardrails.yaml`), and `FinanceKPICollector.budget_utilization` divides `total_spent` by `total_budget` — both collapse to noise under free models. The fix is to add **token-based budgets** alongside USD budgets for every session/agent/day, surface a **renormalized cache dashboard** that does not depend on the broken `cache_write` signal, bound **hot-file re-reads** at the session layer, **allowlist** legitimate sibling-repo work while blocking stray writes, and put **retention/Temp/WAL** on a schedule with named owners.

**What success looks like in 30 days:** no session exceeds a hard token cap without explicit override; cache-read volume and WAL size are dashboarded with alerts; hot-file reads fall ≥30%; Temp file count stops growing; every outside-workspace write is attributable to an allowlisted repo; every third-party transmission is either approved in `APPROVED-VENDORS.md` or suspended.

---

## 1. Defect baseline (evidence-traced)

| # | Defect | Evidence | Why it matters |
|---|--------|----------|----------------|
| D1 | 15.21B cache-reads (v1) + 809.9M (v2), 8.95× / 9.72× input; `cache_write = 0` in `session`, `session_v2`, and all 132k `step-finish` rows | audit §4.2, analytics §7 | Cannot compute true hit-rate; current dashboards must not use `cache_write`. Cache is prefix-reuse on long sessions, not savings. |
| D2 | Top session `ses_f1ad097c` "Athena Implementation" — 377,687,040 cache-reads / 23.1M input; v2 top `ses_e584330d` "Prompt contents" — 26.8M input / 132.8M cache-reads | audit §4.2, analytics §7 | Mega-sessions dominate burn; `build` = 61/94 v2 sessions (65%). |
| D3 | $5.59 total cost on 1.7B input tokens; 317 v1 sessions at $0.00; `big-pickle` single line $1.925 | audit §4.1–4.3 | Cost and tokens are decoupled under free models (`nemotron-3.5-lightning-free` 815, `mimo-v2.6-flash-free` 542, `crouton-alpha-free` 25 in v2). USD alerts never fire. |
| D4 | 1,442 files touched >10× (1,101 read >10×); `api.py` 974×, `company-registry.yaml` 763×, `AGENTS.md` 552×, `summary.md` 466×; tool-output spill re-read 288× | audit §5.2, analytics §5 | Session-start context is re-read from disk per tool call instead of injected once. |
| D5 | 13,126 outside-workspace file ops (17.7%); 7,071 bash calls mention `athena`/`Temp\opencode`; 114 athena sessions; 320 outside sessions (10.2%) | audit §7.2, analytics §9 | Athena + `social-media-automation-os` are legitimate siblings, but `.openmausbot` workspaces, `C:/` probes, and `Temp` sandboxes are intermixed with no boundary. |
| D6 | `Temp\opencode` 31,217 files, only 228 in last 7 days | audit §7.2 | Stale accumulation; no sweeper. |
| D7 | WAL 2.95 GiB (~98% of DB); `.bak` 38.5 GB (2026-11-01); 0 archived sessions; 95-day retention; 72 projects (67 session-less) | audit §1/§8, security §0/§4 | No retention, checkpoint, or project-GC policy. Freelist ~8 MB proves bloat is live pages, not free space — deletes alone won't shrink without vacuum + archive. |
| D8 | No token budgets, no retention, no per-session caps; `daily_budget_usd`/`task_budget_usd` default unlimited | `cost_analytics.py:32-44`, `executor.py:104-142` (guardrails fallback `None`) | Governance gap: caps exist as code paths but are unset and USD-shaped. |
| D9 | Third-party transmission unverified: `resend_*` ~35 (incl. `list-api-keys` 1), `composio_*` ~27, `websearch` 830 (parallel.ai/exa), 141 webfetch hosts; none cross-checked against `APPROVED-VENDORS.md` | security §3 | AGENTS.md §9.2 90-day ban is unapplied to opencode.db traffic. Active allowlist covers only cmem/0x0.st/Telegram/NotebookLM/Workers/kie.ai/Greptile (retired) + Xiaomi MiMo + Google AI/Comfy (active); Resend/Composio/search providers are absent. |
| D10 | `part` 1.82 GB / 670k rows; 28 parts >1 MB; 1,337 >100 kB; attachments inline base64 (144 `file` parts, 0 `blob` rows) | security §2.5, audit §5.4 | Large tool outputs drive both DB size and cache-read inflation. |

---

## 2. Design principles

1. **Token budgets are primary; USD budgets are secondary.** Free-model traffic makes USD a floor of $0. Every session/agent/day gets a token budget (`input + cache_read + output`, with cache_read counted at full weight — see §4) alongside existing USD caps. Existing `CostAnalytics.check_budget` signature is extended, not replaced, for backward compatibility.
2. **Never meter what the provider doesn't report.** `cache_write` is 0 as a recorder/provider quirk (audit §4.2). The dashboard reports `cache_read` volume, `cache_read_ratio = cache_read / (input + cache_read)`, and `burn_multiplier = (input + cache_read) / input` — never a fake hit-rate derived from writes. Documented in `docs/` so future queries don't repeat the error.
3. **Bound work before it runs, not after it burns.** Per-session caps checked at each `step-finish` (the row that already aggregates tokens), with early compaction triggered *before* the next step, not after context exhaustion. 5,444 compactions in v1 prove the current threshold fires too late.
4. **Cache the hot files at the session layer, not the DB layer.** Session-start context (AGENTS.md, STATUS.md, ECL `summary.md`/`tasks.md`, `company-registry.yaml`) is injected once via the memory/recall loop; repeat reads within a session return a pointer to the in-session copy, not disk I/O.
5. **Allowlist outside-workspace work; default-deny the rest.** Legitimate siblings (`athena`, `social-media-automation-os`) are explicitly allowed per-session so multi-repo work stays possible, but every outside file op is attributed, logged, and alerted. `.openmausbot`, `C:/` root probes, and raw `Temp` writes are denied by default.
6. **Every metric has a dashboard, every dashboard has an owner, every owner has a target.** No KPI without a named accountable owner (see RACI §7) and a verification query (see §8).

---

## 3. Prioritized tasks

### P0 — Stop the bleed (this week)

#### GO-1. Per-session token budget + hard cap (llm-platform-owner, Accountable; dashboard-owner, Responsible for surfacing)

- **What:** Add `session_token_budget` (default: 5M `input + cache_read` per session, warn at 70%, compact at 85%, block next LLM call at 100% without override) and `daily_agent_token_budget` (default: 50M per agent per day, warn at 80%) to `guardrails.yaml` alongside existing `daily_budget_usd`/`task_budget_usd`. Extend `CostAnalytics.record_usage` / `check_budget` to check **both** token and USD budgets; denied calls return `(False, "Session token budget exceeded: …")` and log to the existing `alert_store` with `kpi_key="token_budget_utilization"`.
- **Why 5M?** Median v1 session input is far below 5M, but the top tier (23M, 19M, 15M) all exceed it — the cap is aimed at mega-sessions, not normal work. v2 top session (26.8M input) would block after 5M and force an early split/compaction. Tune after 14 days of telemetry (see GO-2); do not ship with `None` (unlimited).
- **Compaction coupling:** When a session hits 85% of its token budget, trigger compaction *before* the next `step-finish` is its final step — i.e., compaction is a pre-step gate, not a post-step reaction. Count forced compactions as a KPI (target: rising early, falling total cache-read per session).
- **Mega-session split rule:** `build` sessions crossing 50% of budget with >100 `step-finish` rows must split remaining work into a child `task` (parent becomes summary + pointers). This directly addresses the 377M cache-read session shape.
- **Free-model accounting:** Token budgets apply regardless of model price. `MODEL_COSTS` $0.00 entries stay for USD forecasting but must not bypass token checks. A "paid-equivalent burn" shadow price (e.g., `mimo-v2.5` list price) is recorded for reporting so a free session at 377M cache-reads still shows non-zero burn.
- **Files to change (for implementers):** `src/ai_company/data/cost_analytics.py` (extend `record_usage`, `check_budget`, add `check_token_budget`, `session_budget_status`), `src/ai_company/llm/cost_tracker.py` (call token check before USD check), `config/company/guardrails.yaml` (new keys, non-None defaults), `src/ai_company/dashboard/alert_store.py` (new alert kind), `src/ai_company/dashboard/kpis/finance.py` (`FinanceKPICollector` gains `token_budget_utilization` alongside `budget_utilization`).
- **Verification:** §8 V1.

#### GO-2. Cache hit-rate dashboard — renormalized (dashboard-owner, Accountable; llm-platform-owner, Responsible for metering)

- **What:** New dashboard section "Cache & Token Burn" fed by `opencode_usage.normalize_*` (already imports `opencode.db` → `cost_records` as `source=opencode-desktop`) extended with `cache_read`, `session_id`, `agent` columns that already exist in `cost_records` but are not surfaced per-session.
- **Metric definitions (frozen — do not compute hit-rate from `cache_write`):**

  | KPI | Definition | Target |
  |-----|-----------|--------|
  | `cache_read` volume (7d, by agent/model/session) | `SUM(cache_read)` from `cost_records` where `source='opencode-desktop'` | Trend down 30% in 30 days |
  | `cache_read_ratio` | `cache_read / (input + cache_read)` per session/day | < 0.90 (today's aggregate is ~0.90 = 15.2B/16.9B) |
  | `burn_multiplier` | `(input + cache_read) / max(input,1)` per session | < 5× (today 9.95× combined) |
  | `cache_write_reported` (Boolean) | Whether any provider in window reported `cache_write > 0` | `False` triggers an "unmetered provider" banner — never chart 0 as efficiency |
  | `top_sessions_by_burn` | Top 10 sessions by `input + cache_read`, with agent + model | Reviewed weekly; any session > budget cap escalated |
  | `compaction_rate` | `compaction` parts / total steps, 7d | < 2% (today ~4% of step-finish) |

- **Display rule:** When `cache_write_reported = False` (today's reality), the chart title is "Cache-read volume (writes unmetered)" and the hit-rate tile is hidden with a tooltip explaining the provider quirk. This prevents the #1 analytics error documented in both audits.
- **Verification:** §8 V2.

#### GO-3. WAL + backup containment (vp-engineering, Accountable; dashboard-owner, Responsible for alert; ciso, Consulted for backup encryption)

- **What:**
  - **Checkpoint + size alert (dashboard):** KPI `wal_size_pct = wal_bytes / db_bytes`. Alert at >10%, page at >50%. Today: ~98% — critical. Source: filesystem size probe in `KPICollector` (read-only `Get-Item`), not DB query (WAL size is a file property).
  - **Backup rule:** No `.bak` older than the retention window (30 days, see GO-7) may live beside the live DB in plaintext. The 38.5 GB `opencode.db.bak` (2026-11-01) is either (a) verified restorable + moved to encrypted cold storage, or (b) deleted in a maintenance window after confirming v2 stability (94 sessions, integrity `ok`). ciso owns the encryption/storage decision; vp-engineering owns the maintenance-window scheduling and verification.
  - **Deduplicate footprint:** Live footprint budget: DB < 1 GiB, WAL < 10% of DB, `.bak` 0 plaintext files > retention. Any backup copy counts toward retention, not as an exempt copy (security §4: breach blast radius = 44.9 GB, not 3 GB).
- **Maintenance-window discipline:** Checkpoint (`PRAGMA wal_checkpoint(TRUNCATE)`) and any `.bak` move happen only in a window with opencode closed, preceded by a fossilized snapshot (`.backup` to a hash-checked file) so the action is reproducible (audit §8 P1-5; data cannot be recovered from a live-WAL copy).
- **Verification:** §8 V3.

### P1 — This sprint (2 weeks)

#### GO-4. Hot-file cache + per-session read dedup (llm-platform-owner, Accountable)

- **What:**
  - **Session-start injection:** `AGENTS.md`, `docs/STATUS.md`, `harness/changes/active/summary.md` + `tasks.md`, `company-registry.yaml`, and the top-20 hot files (§1 D4) are injected once at session start via the existing memory/recall loop (`## Relevant Past Work` pattern). Agents are instructed that re-reading an injected file in the same session returns a pointer, not a disk read.
  - **Per-session LRU read cache:** The `read` tool wrapper keys on `(session_id, normalized_path, mtime)` and returns the cached content on a hit. A repeat read of the same path with unchanged mtime is logged as a `cache_hit` (KPI) but does not re-emit file bytes into the prompt — this is the single largest lever for `read` volume (52,581 reads; ≥30% reduction estimated in audit §8 P3-14).
  - **Staleness guard:** Cache entry invalidates on mtime change or `edit`/`write` to that path within the session (self-invalidation, no TTL guessing).
  - **Tool-output spill rule:** Files under `~/.local/share/opencode/tool-output/` are summarized on write and capped at 50 KB; re-reads return the summary + byte offset, not the full body. Directly retires the 288× spill re-read.
  - **Blob migration (deferring, not blocking):** New `file` attachments go to `blob`/`blob_ref` (hash in `part.data`, bytes in blob store) instead of inline base64. Backfill of the 144 historical inline attachments is a P2 migration, not P1.
- **KPI:** `hot_file_reads` = count of `read` calls to the top-100 hot-file set per day; `dedup_hit_rate` = hits / repeat reads. Targets in §6.
- **Verification:** §8 V4.

#### GO-5. Outside-artifact governance — sibling allowlist (vp-engineering, Accountable; ciso, Responsible for enforcement policy; dashboard-owner, Responsible for logging dashboard)

- **Allowlist (initial, explicit):**

  | Path | Status | Rationale |
  |------|--------|-----------|
  | `C:\Users\jmlus\light-speed-holdings\**` | **Allow** (primary workspace) | 89.8% of sessions; canonical root |
  | `C:\Users\jmlus\athena\**` | **Allow per-session** (114 sessions, top hot files outside) | Legitimate sibling; DocumentStudio + API work is intentional multi-repo |
  | `C:\Users\jmlus\social-media-automation-os\**` | **Allow per-session** (5 sessions) | Legitimate sibling; Dockerfiles/apps work |
  | `C:\Users\jmlus\AppData\Local\Temp\opencode\**` | **Allow sandbox-only** (scratch, pr-body/issue_body, worktree temps) | Approved temp location; governed by GO-6 retention |
  | `C:\Users\jmlus\.openmausbot\**` | **Deny by default** (log + alert) | 17 `discovery` sessions + JobSearch/task-workspace sprawl; job-search content is PII-adjacent (security §4) |
  | `C:\` root, `C:\Users\jmlus\` home listing | **Deny** | Root-level probes (7 sessions) have no legitimate need |
  | `~/.local/share/opencode/tool-output/**`, `opencode.db*`, `auth.json` | **Deny agent read/write** (filesystem policy, not prompt policy) | Security R2/R4: agent must not ingest credentials or re-read spills verbatim |

- **Enforcement point:** Path policy at the `read`/`edit`/`write`/`bash` tool boundary (pre-execution check of `filePath`/`workdir` against the allowlist + session's declared `directory`). Out-of-allowlist requests are **logged (path + tool + session, never content), counted in `outside_write_attempts`, and denied** — not silently redirected. The policy file lives in `company/` so it is versioned with the registry, and its hash is included in the dashboard governance footer (if the policy changes, the dashboard shows it).
- **Attribution requirement:** Every outside-workspace op must carry the session's `project_id` + `directory` so the 13,126-op baseline can be re-measured per-repo (athena vs social-media vs openmausbot) instead of as a single "outside" bucket.
- **Review cadence:** Monthly vp-engineering review of `outside_write_attempts` by prefix; any new legitimate sibling is added via PR + registry update, not by loosening the default.
- **Verification:** §8 V5.

#### GO-6. Temp cleanup policy (dashboard-owner, Accountable; vp-engineering, Responsible for sweeper scheduling)

- **What:**
  - **Retention:** Files under `AppData\Local\Temp\opencode` older than **7 days** are deleted (only 228 files were fresh at audit time; 30,989 are stale). Exclusion: files referenced by an active (non-archived, <7-day-old) session are kept until session age exceeds 7 days.
  - **Sweeper:** Daily `governance_interval` job (executor already has a daily governance tick) runs the retention sweep and logs `temp_files_deleted`, `temp_bytes_reclaimed`, `temp_files_remaining` to the dashboard. Sweeper never follows symlinks/junctions and never deletes outside `Temp\opencode`.
  - **Quota alert:** `temp_file_count` KPI with warn at 5,000, page at 10,000 (today 31,217 = 3× page threshold).
  - **Write-side discipline:** New temp writes must use session-prefixed directories (`Temp\opencode/<session_id>/…`) so attribution and sweeping are trivial; flat writes to `Temp\opencode/` root are logged as `undisciplined_temp_write`.
- **Verification:** §8 V6 (count drops from 31,217 to <5,000 within 7 days of enablement).

### P2 — This month (30 days)

#### GO-7. Retention + archive + project GC (vp-engineering, Accountable; llm-platform-owner, Responsible for archive job; data-privacy-officer, Consulted)

- **What:**
  - **Tiered retention:** `part`/`message` bodies 30 days → session metadata (tokens/cost/agent/model/dates) permanent. Purge sets `time_archived`, then `VACUUM` (freelist is ~8 MB so vacuum alone does nothing — archive of live rows is the reclaim mechanism; consider `PRAGMA auto_vacuum=INCREMENTAL` for future deletes, audit §8 P1-3).
  - **Target:** Live DB consistently < 1 GiB; trajectory payload (`part` 1.82 GB) halves within 2 retention cycles.
  - **Project GC:** The 67 session-less `project` rows (worktree/temp sprawl) are deleted if they have zero sessions and no `activity` in 30 days. Only 5 projects ever hosted sessions; the rest are noise that inflates every project join.
  - **Orphan sweep (parity with HITL expiry sweep):** `running` tool calls > 1 h → `error (orphaned)`; currently 93 `running` + 2 `pending` with no sweeper.
- **Verification:** §8 V7.

#### GO-8. Vendor approval workflow — close the §9.2 gap (ciso, Accountable; vp-engineering, Responsible for inventory + suspension; CEO/CISO of record, Approvers)

- **What:** Cross-check every third-party host in security §3 against `docs/APPROVED-VENDORS.md`:

  | Traffic | Calls | In allowlist? | Action |
  |---------|-------|---------------|--------|
  | Resend (`resend_*`, incl. `list-api-keys`) | ~35 | **No** | Suspend `list-api-keys` immediately; submit Tier A vendor row (host, data class, auth, ≤90-day window) or remove tool |
  | Composio (`composio_*`, incl. `MULTI_EXECUTE_TOOL`) | ~27 | **No** | Suspend `MULTI_EXECUTE_TOOL` pending approval; record payload classes per call |
  | `parallel.ai` search (429 bursts, 41) / `mcp.exa.ai` (11 errors) / `google_search` | 830+ | **No** (search provider routing is not Tier B public research) | Record selected search provider in governance footer; approve or switch |
  | `webfetch` 141 hosts | 745 | Tier B only if public docs | Hosts serving local project files are **not** Tier B — reclassify; 8 userinfo + 93 query-string URLs retroactively logged (names only) |

- **Workflow (per `APPROVED-VENDORS.md` Exception procedure):** PR opens a new row → CEO records approval as CISO of record → skill/tool installs only after row is active → expiry without renewal = remove + treat as unauthorized. Dashboard gains a "Transmission register" view: host + tool + payload class + approval status, never payload values. Ledger is reviewable monthly by ciso.
- **Tool-output hygiene:** `websearch`/`webfetch` outputs that contain tokens are redacted at persistence (security R2) — ciso defines patterns, llm-platform-owner implements the filter in the write path.
- **Verification:** §8 V8. No third-party tool runs without an active row.

### P3 — Next quarter (90 days)

#### GO-9. Cost forecasting on tokens + paid-equivalent burn

- Forecast daily **tokens** (not just USD) over 14-day lookback → 7-day projection (`CostAnalytics.forecast_daily` extended with `forecast_daily_tokens`). Paid-equivalent burn applies list prices to free models so finance sees shadow cost. Alert when projected 7-day tokens exceed the weekly token budget.
- **Owner:** llm-platform-owner (forecast), finance (shadow-price list), dashboard-owner (display).
- **KPI:** `forecast_accuracy` = |projected − actual| / actual, weekly.

#### GO-10. Session v2 telemetry parity

- `session_part = 0` while `session_message = 9,161` means v2 tool-call analytics don't exist (audit §6.3-3). Complete the v2 writers or freeze v1 as canonical and stop dual-schema queries. Until resolved, every token KPI joins **both** schemas explicitly (never summed) per analytics schema-mapping note.
- **Owner:** llm-platform-owner with cto escalation for schema decision.

---

## 4. Token budget specification (normative)

**Metered quantity per session:**
`session_burn = tokens_input + tokens_cache_read + tokens_output + tokens_reasoning`
(cache_read counted at full weight — a cache-read token still consumes context window and provider compute; discounting it is what allowed 377M reads to look "cheap".)

**Budget tiers (defaults — tune after 14 days of telemetry):**

| Tier | Budget (session_burn) | Action |
|------|----------------------|--------|
| Warn | 70% (3.5M) | Dashboard banner + `alert_store` warn |
| Compact | 85% (4.25M) | Pre-step compaction forced; session continues |
| Hard cap | 100% (5M) | Next LLM call denied; session must split or get override |

**Overrides:** A human may raise a single session's cap via CLI flag (`--session-token-budget`) recorded in the session metadata (`budget_override`, reason, actor). Overrides are KPI'd (`override_rate` target < 5%) — a high override rate means the default is wrong, not that overrides are bad.

**Daily agent budget:** 50M `session_burn` per agent per day (warn 80%, deny new sessions at 100% for that agent). `build` at 65% of v2 sessions will hit this first and is the evidentiary check that the cap bites.

**USD budgets stay** (`daily_budget_usd` / `task_budget_usd`) for paid models; both checks run, the tighter gate wins. In `guardrails.yaml` both token and USD keys are required (no `None` = unlimited default — absence is a startup error, not silently unlimited).

**Immutability:** Budget keys live in `config/company/guardrails.yaml`, versioned in git. Changing them requires a PR (cf. AGENTS.md §18 CEO-Override only for `AGENTS.md`/`opencode.json` — guardrails are engineering-owned).

---

## 5. Hot-file governance (normative)

**Hot-file set (from audit evidence):** `src/ai_company/dashboard/api.py`, `company-registry.yaml`, `AGENTS.md`, `harness/changes/active/summary.md`, `docs/STATUS.md`, `src/ai_company/dashboard/static/js/app.js`, `src/App.tsx`, `src/components/FloatingNav.tsx`, `src/data/siteContent.ts`, dashboard `app.py`, `src/ai_company/executor/loop.py`, `harness/changes/active/tasks.md`, `package.json`, `src/ai_company/model_router.py`, `src/ai_company/generator.py` (+ Athena equivalents for athena sessions).

**Rules:**

1. Session-start injection (GO-4) covers the hot-file set; re-reads within a session serve the LRU copy.
2. `grep`/`glob` over `brand/` + `docs/` + `.opencode/skills/` is capped at 50 matches (the >100k-char "Found 100 matches" floods are the large-output tail — analytics §8.4: 1,641 outputs >50k chars). Truncation is surfaced, not silent.
3. `read` outputs are capped at 50 KB per call (tail beyond goes to a spill file that is summarized per GO-4).
4. Every dedup hit increments `dedup_hit_rate`; a falling hit rate means sessions aren't reusing injected context (prompt bug, not cache bug).

---

## 6. KPI register (all KPIs dashboarded, owned, alerted)

| KPI | Owner | Source | Target (30 days) | Alert |
|-----|-------|--------|-------------------|-------|
| `cache_read_ratio` (7d) | dashboard-owner | `cost_records` (`source=opencode-desktop`) | < 0.90 | > 0.92 for 3 days |
| `burn_multiplier` (per session, p95) | llm-platform-owner | `session.tokens_input/cache_read` | < 5× | any session > 10× |
| `top_session_burn` (max `session_burn`) | llm-platform-owner | `session` + `session_v2` | < 5M (hard cap) | > 5M without override record |
| `token_budget_utilization` (daily, by agent) | llm-platform-owner | `CostAnalytics` | `build` < 80% | > 80% (warn), > 100% (deny logged) |
| `budget_utilization` (USD, existing) | finance | `cost_tracker.json` / `cost_records` | < 90% | > 90% |
| `wal_size_pct` | dashboard-owner | Filesystem probe (`opencode.db-wal` / `opencode.db`) | < 10% | > 10% warn, > 50% page |
| `db_size_gb` + `bak_plaintext_files` | vp-engineering | Filesystem probe | DB < 1 GiB; 0 `.bak` > 30d | Any `.bak` > 30d, DB > 2 GiB |
| `hot_file_reads` (per day, top-100 set) | llm-platform-owner | `part` `read` tool | −30% vs baseline | +20% week-over-week |
| `dedup_hit_rate` | llm-platform-owner | Read-wrapper counter | > 0.30 | < 0.20 |
| `outside_write_attempts` (by repo prefix) | vp-engineering | Path-policy log | 100% attributed; 0 denied-success | Any denied-path write succeeds |
| `temp_file_count` + `temp_bytes_reclaimed` | dashboard-owner | Filesystem probe | < 5,000 files | > 10,000 |
| `project_count` / `session_less_projects` | vp-engineering | `project` table | session-less < 10 | > 20 |
| `transmission_register` (hosts without active approval) | ciso | Tool logs vs `APPROVED-VENDORS.md` | 0 | Any unapproved transmission |
| `override_rate` (budget overrides / sessions) | vp-engineering | Session metadata | < 5% | > 10% (tune default) |

KPI definitions are stored in `company/config/kpis.yaml` (versioned with the registry) so the dashboard, alerts, and this report share one definition.

---

## 7. Ownership — RACI

| Decision / deliverable | vp-engineering | dashboard-owner | llm-platform-owner | ciso | CTO / CEO |
|---|---|---|---|---|---|
| Overall cost/governance program + phasing | **A** | C | C | C | I (escalation) |
| Session token budget + hard cap (GO-1) | C | R (surface) | **A/R** | I | I |
| Cache dashboard (GO-2) | C | **A/R** | R (metering, `opencode_usage`) | I | I |
| WAL / `.bak` maintenance window (GO-3) | **A/R** (schedule + verify) | R (alert) | I | C (backup encryption) | A (window approval) |
| Hot-file cache + dedup (GO-4) | C | C | **A/R** | I | I |
| Outside-workspace allowlist (GO-5) | **A/R** | R (logging view) | C | R (policy) | A (new sibling approval) |
| Temp sweeper (GO-6) | R (scheduling) | **A/R** | I | I | I |
| Retention / archive / project GC (GO-7) | **A/R** | C | R (archive job) | C | I (privacy: data-privacy-officer C) |
| Vendor approval per §9.2 (GO-8) | R (inventory/suspend) | R (register view) | C | **A** | **A** (CEO/CISO of record signs) |
| Token forecasting + shadow burn (GO-9) | I | R | **A/R** | I | I (finance C) |
| v2 telemetry parity (GO-10) | C | I | **A/R** | I | A (schema decision) |

**Span-of-control note (operating guideline):** Every specialist deliverable above has exactly one Accountable. vp-engineering coordinates cross-team dependencies and blockers, and reports engineering health weekly to CTO — including GO-* status against KPI targets. Architectural decisions (e.g., v2 schema freeze, new sibling-repo approval) escalate to cto per the vp-engineering charter.

---

## 8. Verification (independent evidence, not assertion)

Run after each phase. All DB queries are `sqlite3 -readonly` against a **snapshot** (`.backup` copy), never the live WAL — re-running against live DB gives drift-affected counts (audit §9.2).

| # | Verification | Command / query pattern | Pass criterion |
|---|-------------|------------------------|----------------|
| V1 | Token budgets enforced | New session > 5M `session_burn` → check `alert_store` for `token_budget_utilization` deny + session metadata for `budget_override` | 0 uncapped sessions > 5M in 14 days; `override_rate` reported |
| V2 | Cache dashboard honest | Dashboard "Cache & Token Burn" vs `SELECT SUM(cache_read), SUM(input) FROM cost_records WHERE source='opencode-desktop'` | Numbers match; hit-rate tile hidden while `cache_write_reported=False` |
| V3 | WAL + backup contained | `Get-Item opencode.db-wal, opencode.db, opencode.db.bak` + `PRAGMA wal_checkpoint` result | `wal_size_pct` < 10%; 0 plaintext `.bak` > 30d |
| V4 | Hot-file dedup working | `SELECT lower(filePath), COUNT(*) FROM part WHERE tool='read' GROUP BY 1 HAVING COUNT(*)>10` (7d window) + `dedup_hit_rate` KPI | Top-100 hot reads −30%; `dedup_hit_rate` > 0.30 |
| V5 | Outside allowlist enforced | `SELECT substr(lower(filePath),1,45), COUNT(*) … WHERE filePath NOT LIKE '%light-speed-holdings%' GROUP BY 1` + `outside_write_attempts` log | 100% attributed; 0 writes outside allowlist succeed |
| V6 | Temp sweeper effective | `(Get-ChildItem Temp\opencode -Recurse -File).Count` + sweeper log | < 5,000 files; daily `temp_bytes_reclaimed` > 0 |
| V7 | Retention effective | `SELECT COUNT(*) FROM project WHERE id NOT IN (SELECT DISTINCT project_id FROM session)`; `SELECT COUNT(*) FROM session WHERE time_archived IS NOT NULL`; `PRAGMA page_count` | session-less < 10; archived counts rising; DB < 1 GiB after vacuum |
| V8 | Vendor approvals current | Join transmission register (host + tool) against `docs/APPROVED-VENDORS.md` active rows | 0 transmissions without active row; `resend_list-api-keys` / `composio_MULTI_EXECUTE` suspended or approved |
| V9 | Suite health | `uv run ruff check src/ && uv run mypy src/ && uv run pytest` | Green; no new bare `except`, no `as` assertions (per repo standards) |

Evidence discipline (AGENTS.md §15): every verification run notes what was requested, what was attempted, what actually happened, and what remains unknown. Live-DB drift between queries is expected and stated, never presented as stable.

---

## 9. Phased timeline

| Phase | Window | Scope | Gate to next phase |
|-------|--------|-------|-------------------|
| **Phase 0 — Govern** | Days 0–3 | This plan approved by CTO; GO-1/2 budgets drafted in `guardrails.yaml`; vendor inventory sent to ciso (GO-8); `.bak` decision recorded (GO-3) | Plan + budget defaults + vendor inventory signed off |
| **Phase 1 — Cap** | Week 1 | GO-1 (token budgets + hard cap + pre-step compaction), GO-2 (cache dashboard), GO-3 (WAL alert + `.bak` containment). **P0 complete.** | V1–V3 green; no uncapped session > 5M in 7 days |
| **Phase 2 — Bound** | Weeks 2–4 | GO-4 (hot-file cache/dedup), GO-5 (outside allowlist), GO-6 (Temp sweeper), GO-8 (vendor approvals executed). **P1 complete.** | V4–V6 + V8 green; hot reads −30%; Temp < 5k; 0 unapproved transmissions |
| **Phase 3 — Retain** | Month 2 | GO-7 (retention + archive + project GC + orphan sweep), GO-10 progress (v2 parity design). | V7 green; DB < 1 GiB sustained 14 days |
| **Phase 4 — Forecast** | Month 3 | GO-9 (token forecasting + paid-equivalent shadow burn), budget tuning from `override_rate` telemetry, 90-day re-audit scheduled. | Forecast accuracy reported; budgets tuned; next audit date booked |

**Re-audit checkpoint (14 days after Phase 1):** Re-run the three 2026-11-08 audit queries (WAL size, cache-read totals, hot-file counts) against a fresh snapshot and diff against this plan's baselines. Keep the three audit reports as the baseline series.

---

## 10. Risks and dependencies

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Hard cap blocks legitimate long investigations (e.g., Athena mega-builds) | Work stall if budget too tight | Override path (`--session-token-budget`) + `override_rate` tuning loop; Phase 1 observes before Phase 2 hardens |
| `cache_write` remains 0 (provider never reports writes) | Dashboard can't show savings | Design assumes this permanently (GO-2 renormalized metrics); banner explains, never fakes hit-rate |
| Sibling allowlist blocks real multi-repo work | Athena sessions break | Allowlist is per-session and PR-extensible; denied attempts are logged, not crashed |
| Retention purge deletes data someone needs | Evidence loss | 30-day window + snapshot before any purge; archive preserves metadata permanently |
| Vendor suspension breaks automations (Resend/Composio) | Workflow interruption | ciso-owned risk call: `list-api-keys` suspends immediately (secret exfiltration class); lower-risk tools get a 7-day approval sprint before suspension |
| WAL checkpoint during live sessions corrupts or misses frames | Data loss | Maintenance-window only, opencode closed, snapshot-first (GO-3) |

---

## 11. What is *not* in this plan (out of scope, owned elsewhere)

- **At-rest encryption (BitLocker/EFS), orphan-SID removal, credential rotation, secret redaction** — ciso, security audit R1–R3 P0. Referenced as dependencies; vp-engineering schedules windows but does not implement.
- **Egress allowlist for shell/webfetch (IWR/curl)** — ciso + dashboard-owner (security R4 P1). This plan meters the traffic; the proxy/filter is the security team's control.
- **Prompt-injection / memory-poisoning quarantine** — ciso (security R6 P2). Token budgets reduce the blast radius but don't filter recall.
- **Edit/regex/PowerShell defect fixes** — audit §8 P2 items 6–11. High value, orthogonal to cost/governance; scheduled separately so cost work isn't blocked.

---

## 12. Appendix — Baseline numbers (for re-measurement)

| Metric | Baseline (2026-11-08) | Source |
|--------|----------------------|--------|
| `SUM(tokens_cache_read)` v1 / v2 | 15,210,842,514 / 809,948,648 | audit §4.2 |
| `SUM(tokens_cache_write)` | 0 | audit §4.2 |
| Cache-read / input | 8.95× (v1) / 9.72× (v2) | audit §4.2 |
| Top session cache-read | 377,687,040 | audit §4.2, analytics §7 |
| Total cost | $5.59 (v1) | audit §4.1 |
| Hot files >10× | 1,442 (1,101 read-only); `api.py` 974× | audit §5.2 |
| Outside file ops | 13,126 (17.7%) | audit §7.2 |
| Temp files | 31,217 (228 fresh) | audit §7.2 |
| WAL / DB | 3,163,682,112 / 3,222,466,560 (~98%) | audit §1, security §0 |
| `.bak` | 38,533,844,992 B (2026-11-01) | audit §1 |
| Projects | 72 (5 with sessions) | audit §1, security §4 |
| `part` payload | 1,820 MB / 670,664 rows | security §2.5 |

Re-measurement queries for every row are in the companion audits' SQL appendices (analytics §10 verbatim; audit §9.1) and must be re-run against a snapshot.
