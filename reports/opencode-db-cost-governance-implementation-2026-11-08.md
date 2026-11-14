# opencode.db — Cost Governance Implementation — 2026-11-08

**Author:** llm-platform-owner, LightSpeed Holdings
**Date:** 2026-11-08
**Status:** Implemented + tested (workspace only; no files outside `C:\Users\jmlus\light-speed-holdings`)
**Plan source:** `reports/opencode-db-cost-governance-fix-2026-11-08.md` (GO-1…GO-6, §4–§5, §8 V1–V6)

## What was requested vs what actually happened

| # | Requested | Actually happened | Verified |
|---|-----------|-------------------|----------|
| 1 | Token hard cap 5M/session, daily 50M/agent, warn 70%/compact 85%/block 100% pre-step; extend `CostAnalytics.check_budget` (token+USD, tighter wins) | Implemented in `CostAnalytics` + `CostTracker`, defaults non-None, guardrails updated | `tests/unit/test_token_governance.py` (18 tests) |
| 2 | Cache dashboard renormalized metrics; hide hit-rate while `cache_write=0`; fix `cache_creation → tokens_cache_write` | `cache_metrics.py` + `CostAnalytics.cache_metrics()` + Finance KPIs + `opencode_usage` mapping fix | Same test file, cache-mapping tests |
| 3 | Hot-file cache/dedup: session-start injection, LRU+mtime, 50KB output cap, grep cap 50 | `llm/hot_file_cache.py` | `tests/unit/test_hot_file_cache.py` (12 tests) |
| 4 | Outside allowlist + attribution logging | `security/path_allowlist.py` + `config/company/path_allowlist.yaml` | `tests/unit/test_path_allowlist.py` (13 tests) |
| 5 | 14-day re-audit script vs `.backup` snapshot (PRAGMA/count gates) | `scripts/maintenance/audit-opencode-db.ps1` delegating to read-only analytics SQL | Synthetic-snapshot run, exit 0, report JSON written+removed |

## 1. Token hard cap (GO-1)

**Metered burn:** `input + cache_read + output + reasoning`, mapped onto
`cost_records` as `prompt_tokens + cache_read + completion_tokens`.
`cache_write` is already inside `prompt_tokens` for opencode-desktop rows
(`prompt = input + cache_write`), so it is not double-counted. Cache-read
counts at full weight — discounting it is what let 377M reads look cheap.

**Implementation:**
- `src/ai_company/data/cost_analytics.py`
  - `__init__(..., session_token_budget=5_000_000, daily_agent_token_budget=50_000_000)` — `None` is explicit opt-out only.
  - `session_token_total(session_id)`, `agent_daily_token_total(agent_name, day)`, `top_sessions_by_burn()`.
  - `session_budget_status(...) -> {level: ok|warn|compact|block, session_utilization, agent_daily_utilization}` — warn 70%, compact 85%, block 100%; daily agent warn 80%/block 100%; tighter gate wins.
  - `check_token_budget(...) -> (allowed, reason)`; `check_budget(task_id, proposed_cost=0, *, session_id="", agent_name="", proposed_tokens=0)` runs token gate **first**, then USD daily/task gates. `session_id` falls back to `task_id` (desktop `task_id == session_id`). Warn/compact return `allowed=True` with the action in the reason; block returns `False, "Session token budget exceeded: … (pre-step block at 100%)"`.
  - `budget_status()` now includes `token_budget_utilization`, `token_budget_level`, `session_burn`, and `cache` (renormalized metrics).
- `src/ai_company/llm/cost_tracker.py` — mirrors the same gate in-memory
  (`_session_tokens`, `_agent_daily_tokens`, `UsageRecord.session_burn`,
  `session_budget_status()`/`check_token_budget()`, extended
  `check_budget(..., session_id=, agent_name=, proposed_tokens=)`).
  Accumulators rebuild from `cost_log.jsonl` on restart (test:
  token accumulators survive restart). Note: a parallel agent added
  paid-equivalent shadow-cost fields to this same file during this run;
  both changes coexist (shadow untouched).
- `config/company/guardrails.yaml` — `session_token_budget: 5000000`,
  `daily_agent_token_budget: 50000000`, ratios 0.70/0.85/1.00/0.80, with
  the comment that absence must not mean unlimited.
- `src/ai_company/cli/executor.py` — new `_resolve_token_budgets()`
  (5M/50M defaults, YAML overrides); `_resolve_budgets()` kept at its
  3-tuple arity for existing callers.

**Free-model proof:** with `daily_budget_usd=None` (unlimited USD) and a
$0.00 record at 6M burn, `check_budget` still blocks on tokens
(`test_tighter_gate_wins_token_over_usd`).

## 2. Cache dashboard — renormalized (GO-2)

**New module `src/ai_company/llm/cache_metrics.py`:**
- `compute_cache_metrics(input, cache_read, cache_write, output)` →
  `cache_read_volume`, `cache_read_ratio = cache_read/(input+cache_read)`,
  `burn_multiplier = (input+cache_read)/max(input,1)`,
  `cache_write_reported` (bool), `show_hit_rate_tile` (False while
  writes unmetered), `unmetered_banner`, `chart_title`
  ("Cache-read volume (writes unmetered)" while unmetered).
- `extract_cache_write()` / `extract_cache_read()` /
  `normalize_provider_usage()` — accept `cache_creation`,
  `cache_creation_input_tokens`, `cache_creation_tokens`, nested
  `{ephemeral_5m, ephemeral_1h}` dicts (summed), OpenCode
  `tokens.cache.write`, and `tokens_cache_write`. Zero values are skipped
  so stale `cache.write=0` cannot mask a real top-level
  `cache_creation=50` (the historical recorder bug).

**Cache-write mapping fix (reliability P1-1):**
`src/ai_company/llm/opencode_usage.py` — `normalize_message_row` and
`normalize_session_row(raw_usage=...)` now route through the extractor.
Regression tests: `{input:100, cache_read:900, cache_creation:50} → cache_write=50`
(flat, Anthropic flat, nested ephemeral, session-row `raw_usage`, and
message-row top-level `cache_creation` shapes).

**Dashboard surfacing (feasible part):**
- `CostAnalytics.cache_metrics(days=7)` + `top_sessions_by_burn()` — SQL
  over `cost_records`; uncached input = `prompt_tokens - cache_write`.
- `src/ai_company/dashboard/kpis/finance.py` (`FinanceKPICollector`) now
  emits `token_budget_utilization`, `cache_read_volume`,
  `cache_read_ratio`, `burn_multiplier`, `cache_write_reported`, and
  `cache_unmetered_banner` (error text carries the banner while
  unmetered). KPI defs added to `company/config/kpis.yaml`.

## 3. Hot-file cache/dedup (GO-4)

`src/ai_company/llm/hot_file_cache.py`:
- `SESSION_START_FILES` (AGENTS.md, docs/STATUS.md, ECL summary/tasks,
  company-registry.yaml, guardrails.yaml) + `HOT_FILES` top-20 audit set.
- `build_session_start_injection(root)` — inject-once reader; missing
  files skipped, never faked.
- `SessionHotFileCache(session_id)` — per-session LRU (default 100
  entries) keyed by normalized path; `get()` hits only on unchanged
  `mtime`; `put()` stores 50KB-capped content; `invalidate()` for
  edit/write self-invalidation; `hits/misses/invalidations/dedup_hit_rate`
  stats. Sessions are isolated instances.
- `cap_tool_output(text, 50*1024)` and `cap_grep_results(results, 50)` —
  truncation is returned as a flag, never silent.

## 4. Outside allowlist (GO-5)

`src/ai_company/security/path_allowlist.py` + `config/company/path_allowlist.yaml`:
- **Allow:** `light-speed-holdings` (primary), `athena` +
  `social-media-automation-os` (per-session siblings), `Temp\opencode`
  sandbox-only (writes allowed; reads require the session-prefixed path).
- **Deny:** `.openmausbot`, `C:/` root / home listing, `opencode.db*`,
  `opencode-.db*`, `auth.json`/`mcp-auth.json`, `.local/share/opencode/**`
  (incl. `tool-output`), `.env` variants (except `.env.example`).
  Default-deny for anything else outside.
- `PathAllowlist.validate(path, tool)` returns `PathDecision` and appends
  an attribution record `{timestamp, session_id, project_id, directory,
  tool, path, allowed, category, reason}` — **path only, never content** —
  plus a warning log on denial. This module is complementary to the
  parallel agent's `security/path_policy.py` (credential-deny only);
  `path_allowlist` answers the sibling/boundary question.

## 5. Retention / 14-day re-audit hook

`scripts/maintenance/audit-opencode-db.ps1`:
- Mandatory `-SnapshotPath` (a `.backup` snapshot; the live DB is never
  touched — missing snapshot exits 1 with instructions).
- Runs read-only (`mode=ro`) analytics SQL via Python: `PRAGMA
  integrity_check` (gate: `ok`), `page_count`/`page_size`, table
  presence, per-table `SUM(tokens_cache_read/tokens_cache_write/tokens_input)`
  + session counts, and session-less project count.
- Baseline cache-read parameter defaults to the plan appendix v1 total
  (`15210842514`). Writes JSON to `-OutputPath` (default
  `reports/opencode-db-reaudit-YYYY-MM-DD.json`). Exit 0 on pass.
- Verified: synthetic snapshot (session + session_v2 + project tables)
  → `integrity: ok`, `pass: true`, exit 0; test artifacts removed.
  PowerShell anti-pattern scan: 17 files, 0 failures, 0 warnings.

## Verification evidence

```
uv run pytest tests/unit/test_token_governance.py tests/unit/test_hot_file_cache.py tests/unit/test_path_allowlist.py tests/unit/test_opencode_usage.py tests/unit/test_cost_tracker.py -q
70 passed

uv run pytest tests/unit/test_token_governance.py tests/unit/test_hot_file_cache.py tests/unit/test_path_allowlist.py tests/unit/test_opencode_usage.py tests/unit/test_cost_tracker.py tests/test_cost_tracker_integration.py tests/unit/test_llm_cost_wiring.py -q
89 passed

uv run ruff check <all touched src/test files>
All checks passed!

uv run ruff check src/   # 11 pre-existing findings, all in
                          # executor/tool_runner.py + executor/tool_validation.py
                          # (parallel-agent files, untouched by this change)
```

## Files changed / created

**Modified:** `src/ai_company/data/cost_analytics.py`,
`src/ai_company/llm/cost_tracker.py`, `src/ai_company/llm/opencode_usage.py`,
`src/ai_company/dashboard/kpis/finance.py`, `src/ai_company/cli/executor.py`,
`config/company/guardrails.yaml`, `company/config/kpis.yaml`

**Created:** `src/ai_company/llm/cache_metrics.py`,
`src/ai_company/llm/hot_file_cache.py`, `src/ai_company/security/path_allowlist.py`,
`config/company/path_allowlist.yaml`, `scripts/maintenance/audit-opencode-db.ps1`,
`tests/unit/test_token_governance.py`, `tests/unit/test_hot_file_cache.py`,
`tests/unit/test_path_allowlist.py`, this report.

## What remains unknown / out of scope

- No live `opencode.db` was read or written; re-audit numbers require a
  `.backup` snapshot taken in a maintenance window (opencode closed).
- Dashboard HTML tiles for "Cache & Token Burn" were not rebuilt — the
  KPI payload (incl. hit-rate-hide flag + banner) is the data contract
  the templates consume; template work is dashboard-owner's.
- `CostTracker`/`CostAnalytics` token defaults apply to new instances;
  existing CLI callers that construct trackers without token args get
  the governed 5M/50M defaults automatically.
- WAL/`.bak` containment (GO-3), Temp sweeper (GO-6), retention/archive
  (GO-7), and vendor approvals (GO-8) are separate owners per the plan RACI.
