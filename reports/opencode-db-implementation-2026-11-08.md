# opencode.db — Implementation Report — 2026-11-08

**Coordinator:** chief-of-staff (primary orchestrator) for LightSpeed Holdings.
**Date:** 2026-11-08 (local).
**Database (read-only verification only):** `C:\Users\jmlus\.local\share\opencode\opencode.db` — 3,236,483,072 B (~3.01 GiB), WAL 3,163,682,112 B (~2.95 GiB), `.bak` 38,533,844,992 B (2026-11-01) — **no file outside the workspace was created, modified, checkpointed, or deleted during this task**; all DB evidence below is `sqlite3 -readonly` or `Get-ChildItem`/`icacls` reads (counts/sizes/hosts only, never values).

**Sources read first:** `reports/opencode-db-fix-plan-2026-11-08.md`,
`reports/opencode-db-security-fix-2026-11-08.md`, `reports/opencode-db-reliability-fix-2026-11-08.md`, `reports/opencode-db-toolfix-2026-11-08.md`, `reports/opencode-db-cost-governance-fix-2026-11-08.md`.

## 0. Session integrity note (execution-honesty disclosure)

Two material facts shape this report and are recorded per AGENTS.md §15:

1. **Subagent delegation failed (depth limit reproduced).** The coordinator attempted to spawn a helper subagent and got `Subagent depth limit reached (1)` — the exact failure the source audits document (40× in DB + live reproduction). Per the T-06 fallback plan, implementation proceeded by direct execution and is logged here.
2. **A sibling session was concurrently implementing in the same working tree** (file mtimes 18:30–18:42 local, overlapping this session). The tree therefore contains: (a) this session's additions, (b) the sibling session's additions (e.g. `src/ai_company/llm/cache_metrics.py`, `src/ai_company/llm/hot_file_cache.py`, `src/ai_company/security/path_allowlist.py`, cost/token code in `cost_analytics.py`/`cost_tracker.py`/`finance.py`/`cli/executor.py`, `scripts/maintenance/opencode-db-maintenance.ps1`, `opencode-db-bak-disposition.ps1`, `audit-opencode-db.ps1`, tests). Both sets are uncommitted on `main`'s working tree. Where the two overlap in responsibility (secret redaction, path deny, egress), the tree currently carries **two modules per concern** (`redact.py` + `redaction.py` history, `path_policy.py` + `path_allowlist.py`, `egress.py`, `quarantine.py` + `config/quarantine_patterns.yaml`) — dedup is an open decision (§5, D-1). The coordinator stopped editing shared source files once the collision was detected and only repaired one lost import (`re` in `redact.py`) that had broken `tool_runner` import.

**What this coordinator authored this session:** `src/ai_company/security/redact.py` (incl. import repair), `path_policy.py`, `egress.py`, `quarantine.py`, `src/ai_company/executor/tool_validation.py`, `ps_linter.py`, ToolRunner wiring edits (validation + read-deny + PS pre-flight + grep truncation + egress/retry + read cache + redaction in `_sanitize_output`), scripts `opencode-snapshot.ps1`, `opencode-wal-checkpoint.ps1`, `sweep-temp-opencode.ps1`, `sweep-orphaned-tool-calls.ps1`, `opencode-project-gc.ps1`, docs `opencode-db-p0-runbook.md`, `opencode-db-cache-metrics.md`, `opencode-db-blob-design.md`, `docs/adr/ADR-opencode-v2.md`, tests `test_tool_validation.py`, `test_redact.py`, `test_ps_linter.py`, plus fixes (ps_linter `jq` pattern; sweep-temp sort; project-GC schema). Everything else in the diff is the sibling session's work, verified by import/test below but not claimed here.

## 1. Checkpoint status

| Checkpoint | State | Rationale |
|---|---|---|
| **P0 containment/disk** | **Not closed.** Code ready; all filesystem/DB actions runbook-only. | ACL orphan ACE still present; `.bak` still beside live DB; WAL 97.8% of DB; rotation/encryption decisions pending. Nothing destructive was run. |
| **P1 defect classes** | **Code complete in tree (uncommitted).** | Validation, PS lint, grep caps, schema fail-fast, retry/backoff implemented + 225 scoped tests pass. `rg` binary itself still missing on host (ready-for-window install via `dev.ps1`). Depth raise needs CEO override (blocked-human-decision). |
| **P2 cache/hot-file/egress** | **Code complete in tree (uncommitted).** | Token budgets (5M/50M), renormalized cache metrics, read dedup, spill caps, egress allowlist implemented. Blob migration design-only. |
| **P3 lifecycle** | **Runbooks + dry-run scripts ready; decisions pending.** | Sweeper/GC/retention/quarantine implemented as dry-run scripts + ADR draft; window actions need snapshot + CEO/CTO decisions. |

**Read-only verification, 2026-11-08 (this task):** `session=3131, session_v2=128, part=670664, credential=22, project=72, session_part=0, blob=0, archived=0`; tool status `completed 185183 / error 3435 / running 93 / pending 2` (orphan split now `task 51, bash 30, question 10, read 1, write 1` — same 95 total); `SUM(tokens_cache_read)=15,210,842,514 / SUM(tokens_cache_write)=0`; `.env` reads 309; `sk-` rows 12,747; userinfo webfetch 8; `cipher` → `U` (unencrypted); `icacls` orphan `…-1003 (I)(OI)(CI)(RX)` still present; Temp total 31,285 (stale 30,989); `opencode-.db` 765,952 B still present; `log\opencode.log` 31,205,430 B (rotated down from ~80 MB baseline). Live drift noted (session_v2 94→128; Temp +68).

**Fixture feasibility (no real snapshot taken):** `scripts/maintenance/opencode-snapshot.ps1 -WhatIf` verified; `.backup` source size 3,236,483,072 B. A real snapshot **was not created**: writing a 3 GB secrets-bearing copy into the workspace would itself expand the blast radius and pollute git; the script refuses workspace paths and targets an operator encrypted volume.

## 2. Per-task states

### P0 — containment/disk

| Task | State | Result |
|---|---|---|
| P0-T1 ACL lockdown (F-01) | **runbook-only** | Verified ACE present; runbook `docs/opencode-db-p0-runbook.md` §F-01. No change made. |
| P0-T2 `.bak` disposition (F-03) | **runbook-only** | 38.5 GB still beside live DB; restore-test-then-delete/archive documented; sibling script `opencode-db-bak-disposition.ps1` dry-run default. No change made. |
| P0-T3 credential-encryption determination | **blocked-human-decision** | Cannot verify encryption from available evidence (no `SELECT value` was run); treat all 22 as plaintext. Fix plan Open Question 1 remains with CISO/vendor docs. |
| P0-T4 rotation (F-04) | **blocked-human-decision** | Provider-console rotation + `.env` audit + fingerprint log documented; needs CEO approval of scope (P0-T3). |
| P0-T5 ingest stop: deny + redact (F-05/F-06) | **implemented** | `security/path_policy.py` (deny `.env`/`auth.json`/`opencode.db*`/`*.pem`, `.env.example` exempt), `security/redact.py` (10 secret patterns, key-name preserved, IDs-only logging), wired into `ToolRunner` (validation + `_sanitize_output` + bash token check). Tests: `tests/unit/test_redact.py` pass. |
| P0-T6 WAL checkpoint (F-09) | **ready-for-window** | Script `opencode-wal-checkpoint.ps1` (dry-run default; refuses with writers); needs snapshot + window. Verified current ratio 97.8%. |
| P0-T7 temp purge + sweeper design | **ready-for-window** | `sweep-temp-opencode.ps1` (7-day cutoff, dry-run verified: 31,285 total / 30,989 stale / ~494 MB). No deletion run. |

### P1 — defect classes

| Task | State | Result |
|---|---|---|
| P1-T1 EDIT semantics (816) | **implemented** | `check_edit_preflight` (NOOP / NOT_FOUND / AMBIGUOUS with ≤3 line locations) + `edit_rejection_hint`; ToolRunner validates + `edit` no-op reject pre-dispatch. |
| P1-T2a rg/fallback (474+236) | **implemented (repo) / ready-for-window (host)** | Pure-Python `grep`/`glob` fallback in ToolRunner; `rg` added to `_DEFAULT_ALLOWED_COMMANDS` + `config/tool_allowlist.yaml` + `dev.ps1` install check with winget fallback. `rg` binary still missing on host (verified). |
| P1-T2b grep cap 64 KiB (140) | **implemented** | Match lines capped (500 chars + record byte cap) in `ToolRunner._grep` and `tool_summarizer._summarize_grep` (`cap_grep_line`, `GREP_MATCH_CAP`); scan shipped with `truncated_lines` count. |
| P1-T3 PowerShell §17 lint (~1,500) | **implemented** | `executor/ps_linter.py` (5 patterns + rewrite hints) wired as ToolRunner pre-flight; `scan-ps-antipatterns.ps1` extended (+62 lines, 0 failures on `scripts/maintenance`). Fixture tests pass (225 suite). |
| P1-T4 schema fail-fast (149) | **implemented** | `validate_tool_args` rejects missing/None/empty required keys with shape example, `validation_rejected` flag, never executes. Tests pass. |
| P1-T5 subagent depth (40) | **blocked-human-decision** | Repro preserved (this session's spawn failure). Raising depth in `opencode.json` requires `[CEO-OVERRIDE: …]` + `docs/governance-audit.md` entry. No config changed. |
| P1-T6 retry/quarantine (429/transport) | **implemented** | `_webfetch` retries 429/5xx/transport with exponential backoff + `Retry-After` (3 attempts, injected sleep), classifies `RATE_LIMITED` / `TARGET_UNREACHABLE` / `BAD_REQUEST`; delegation to depth fallback implemented in `run_plan` (`classify_tool_error` + `depth_limit_fallback`). `agents_*` quarantine: the tools do not exist in this repo's canonical vocabulary; recorded as n/a here, harness-side. |

### P2 — cache/hot-file/egress

| Task | State | Result |
|---|---|---|
| P2-T1 cache metering (`cache_write=0`) | **implemented (dashboard) / blocked (recorder)** | Renormalized metrics frozen (`cache_read_ratio`, `burn_multiplier`, `cache_write_reported` banner): `CostAnalytics.cache_metrics()` + `llm/cache_metrics.py` + `docs/opencode-db-cache-metrics.md`. Recorder mapping fix is upstream harness work. |
| P2-T2 mega-session budgets | **implemented** | `session_token_budget: 5000000`, `daily_agent_token_budget: 50000000`, warn/compact/block ratios in `config/company/guardrails.yaml`; `CostAnalytics` token-budget checks + executor resolution; `finance.py` gains `token_budget_utilization` KPI. Deploy behind the same PR (tune after 14d telemetry). |
| P2-T3 read dedup / session injection | **implemented** | Per-session read cache `(session_id, path) -> (mtime_ns, size, content)` with self-invalidation on write; second unchanged read returns cached content (no disk I/O). |
| P2-T4 spill cap | **implemented** | `truncate_to_cap` / 64 KB output caps at executor boundary with spill pointer + `[line truncated]` accounting (integrated via ToolRunner + summarizer). |
| P2-T5 blob design (144 inline) | **runbook-only (design doc)** | `docs/opencode-db-blob-design.md`; blocked on P3-T1 decision. |
| P2-T6 egress allowlist + URL hygiene | **implemented** | `security/egress.py` (https-only except loopback/dev, userinfo reject, token-query reject, metadata/private deny, `file:`/`data:`/`ftp:` deny, regression) wired into `_webfetch`; register helper (`host + tool + class, never values`). Shell egress `IWR`/`curl` allowlist is host-proxy work (runbook), partially covered by ToolRunner allowlist. |

### P3 — schema/lifecycle

| Task | State | Result |
|---|---|---|
| P3-T1 v2-vs-freeze decision | **blocked-human-decision** | Draft ADR `docs/adr/ADR-opencode-v2.md`; owner CTO. |
| P3-T2 orphan sweeper (95) | **ready-for-window** | `sweep-orphaned-tool-calls.ps1` (dry-run verified; `-Apply` = window + snapshot). |
| P3-T3 project GC (66 session-less) | **ready-for-window** | `opencode-project-gc.ps1` dry-run returns **0 candidates** under the 30-day rule — all 66 session-less projects are <30 days old. GC deletes nothing today. |
| P3-T4 retention/VACUUM | **runbook-only** | 30-day body retention + cold archive + `VACUUM INTO` procedure in P0 runbook; needs CEO/CISO retention window (Open Question 4) + 12 GB pre-flight. |
| P3-T5 vendor verification (§9.2) | **blocked-human-decision** | Cross-check done: Resend/Composio/Google/Exa/Parallel are **absent** from `docs/APPROVED-VENDORS.md` → unauthorized pending CEO/CISO rows; tools suspended pending sign-off. No doc edited (CEO sign-off required). |
| P3-T6 injection quarantine (3,412+) | **implemented (filter) / ready-for-window (tagging job)** | `security/quarantine.py` + `config/quarantine_patterns.yaml` + injector exclusion helper; the tagging job that writes flags must run on a snapshot in the window. |
| P3-T7 stale cleanup | **ready-for-window** | `opencode-.db` (765,952 B) + log rotation + KV TTL documented; `opencode-.db` needs the transition-data audit first (Open Question 9). |
| P3-T8 re-audit on snapshot | **runbook-only** | `scripts/maintenance/audit-opencode-db.ps1` (read-only snapshot queries) + this report as baseline; full re-audit after the window. |

## 3. Files created/modified

**Created by this coordinator (this session):**
`src/ai_company/security/redact.py`, `path_policy.py`, `egress.py`, `quarantine.py`,
`src/ai_company/executor/tool_validation.py`, `ps_linter.py`,
`scripts/maintenance/opencode-snapshot.ps1`, `opencode-wal-checkpoint.ps1`,
`sweep-temp-opencode.ps1`, `sweep-orphaned-tool-calls.ps1`, `opencode-project-gc.ps1`,
`docs/opencode-db-p0-runbook.md`, `docs/opencode-db-cache-metrics.md`, `docs/opencode-db-blob-design.md`, `docs/adr/ADR-opencode-v2.md`,
`tests/unit/test_tool_validation.py`, `test_redact.py`, `test_ps_linter.py`,
`reports/opencode-db-implementation-2026-11-08.md` (this file).
**Modified by this coordinator:** `src/ai_company/executor/tool_runner.py` (imports, cache, validation, deny, PS lint, grep caps, egress+retry, read cache, redaction), `tool_validation.py`/`redact.py` follow-up repair (jq pattern; lost `re` import), `scripts/maintenance/sweep-temp-opencode.ps1` (sort), `opencode-project-gc.ps1` (schema fix).

**Also modified in the tree by the sibling session (not claimed here):** `company/config/kpis.yaml`, `config/company/guardrails.yaml`, `src/ai_company/data/cost_analytics.py`, `src/ai_company/llm/cost_tracker.py`, `src/ai_company/llm/opencode_usage.py`, `src/ai_company/dashboard/kpis/finance.py`, `src/ai_company/cli/executor.py`, `src/ai_company/audit/*`, `src/ai_company/llm/cache_metrics.py`, `src/ai_company/llm/hot_file_cache.py`, `src/ai_company/security/path_allowlist.py`, `config/tool_allowlist.yaml`, `config/*allowlist*/*deny*/*quarantine*`, `scripts/dev/dev.ps1`, `scripts/maintenance/scan-ps-antipatterns.ps1`, `audit-opencode-db.ps1`, `opencode-db-maintenance.ps1`, `opencode-db-bak-disposition.ps1`, `tests/unit/test_hot_file_cache.py`, `test_path_allowlist.py`, `test_token_governance.py`, `test_opencode_db_security.py`, `data/ai_company.db` (64 MB working file, should not be committed).

**Outside the workspace:** none created/modified. No snapshot DB was created (see §1). No `main`-branch commit was made (branch protection: push via branch + PR).

## 4. Verification evidence

- **Scoped tests:** `pytest tests/unit/test_tool_validation.py tests/unit/test_redact.py tests/unit/test_ps_linter.py tests/unit/test_tool_vocabulary.py tests/unit/test_tool_summarizer.py tests/unit/test_agent_loop.py tests/unit/test_hot_file_cache.py tests/unit/test_path_allowlist.py tests/unit/test_token_governance.py tests/unit/test_opencode_db_security.py tests/unit/test_opencode_usage.py` → **225 passed** (1 initial run: 222 passed, 3 failed on the `jq` pattern; pattern generalized, re-run **225 passed**).
- **`ruff check`** on `src/ai_company/executor/`, `src/ai_company/security/`, `cost_analytics.py`, `cache_metrics.py`, `hot_file_cache.py`, `opencode_usage.py`, and the three new test files → **passed** at final run (earlier run showed 16 style nits in the merged code; sibling session has since cleaned them).
- **`mypy`** on `tool_validation.py` / `redact.py` → **passed**. **Not claimed:** full `ruff check src/ && mypy src/ && pytest` (AGENTS.md §6 floor) — the full suite was not run this session; required before PR merge.
- **Scripts (read-only/dry-run):** `sweep-temp-opencode.ps1` → `total=31285 stale=30989 staleBytes=493945030` (dry-run); `sweep-orphaned-tool-calls.ps1` → orphan counts confirmed (93 running + 2 pending); `opencode-wal-checkpoint.ps1` → `WAL/DB 97.8%` (dry-run); `opencode-project-gc.ps1` → **0 candidates** (after schema fix); `opencode-snapshot.ps1 -WhatIf` → OK (source 3,236,483,072 B); `scan-ps-antipatterns.ps1 -Path scripts/maintenance` → 0 failures, 1 warning (sibling's `opencode-db-bak-disposition.ps1` missing Sort-Object — style WARN only).
- **DB read-only proofs:** counts/sizes/ACL/cipher quoted in §1; `credential 22` rows counted by label+length only (no values selected); `PRAGMA integrity_check` was not re-run this session (prior audits `ok`; checkpoint window must re-verify).

## 5. Rollback

- **Code (this coordinator):** revert the listed files (`git checkout --` / `git status` clean is the pre-state; new files delete). New modules are additive; ToolRunner edits are localized to the validation/deny/lint/egress/cache/redaction hooks. No migrations, no DB writes — nothing to roll back in the live store.
- **Config:** `guardrails.yaml` token budgets are sibling-session changes; revert by restoring prior file (budget semantics default back to USD-only). No root-config (`AGENTS.md`/`opencode.json`) changes were made — no `[CEO-OVERRIDE]` was required or used.
- **Windows/DB:** no ACL change, checkpoint, `.bak` move, rotation, or encryption state exists to roll back. The P0 runbook defines each step's rollback (snapshot restore; never re-expose data).

## 6. Open decisions

- **D-1 (dedup):** two modules per concern (`redact.py` vs `redaction*`, `path_policy.py` vs `path_allowlist.py` + `config/path_deny.yaml`). Pick one canonical pair, delete the other, and re-run the 225 tests. Owner: CTO/ciso; blocks PR.
- **D-2 (P0-T3/T4, Q1–Q3):** credential-encryption determination, rotation scope, BitLocker-vs-EFS, `.bak` restore-vs-delete. Owner: Human CEO (CISO of record) with CISO/CIO.
- **D-3 (P3-T1/Q5):** complete-v2 vs freeze-v1. Owner: CTO (ADR `docs/adr/ADR-opencode-v2.md`).
- **D-4 (P3-T4/Q4):** retention window (30-day bodies proposed) + legal/GDPR hold check. Owner: Human CEO + CLO/DPO.
- **D-5 (P3-T5/Q6):** Resend/Composio/Google/Exa/Parallel allowlist rows or removal. Owner: Human CEO (CISO of record).
- **D-6 (P1-T5/Q7):** orchestrator subagent-depth value (config + `[CEO-OVERRIDE]`). Owner: Human CEO.
- **D-7 (P3-T7/Q9):** `opencode-.db` transition-data audit before removal. Owner: CTO.
- **D-8 (concurrency):** two sessions editing one tree without a branch. Recommend: move remaining work to a branch/worktree and serialize merges; never commit `data/ai_company.db`.
