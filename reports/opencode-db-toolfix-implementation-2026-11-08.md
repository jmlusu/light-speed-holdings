# opencode.db Tool-Failure Fixes — Implementation Report (2026-11-08)

**Author role:** senior-backend-engineer, LightSpeed Holdings
**Date:** 2026-11-08
**Status:** Implemented (P1 tooling fixes) — scoped verification green
**Source plan:** `reports/opencode-db-toolfix-2026-11-08.md` (T-01..T-12)

**Scope boundary (what was requested vs what actually happened):**
Requested: implement P1 fixes 1–7, run ruff/mypy/pytest scoped, create this
report, no files outside the workspace, no root-config edits without
override. Actually happened: all seven items implemented in-workspace
(see §1–§2); `opencode.json` / `AGENTS.md` were **not** edited (item 6
delivered as a proposal). Verification was pytest + ruff + mypy + live
scanner runs, below. No DB queries were run, so no new error-rate claims
are made — effectiveness must be measured by re-running the analytics SQL
at day 14 (T-12).

**Concurrency note (evidence):** a parallel subagent session was
implementing the same P1 batch in this checkout (it authored
`src/ai_company/executor/ps_linter.py`,
`src/ai_company/executor/tool_validation.py` core,
`src/ai_company/security/path_policy.py`, `egress.py`, `redact.py` and
the run-plan validation order). This session extended those files in
place rather than overwriting them; the merged result is what's on disk
now. Where a sibling feature already existed (PowerShell pre-flight in
`_execute`, read-dedup cache, webfetch retry loop), this session
refactored or completed it (jitter + injectable sleep, grep backend
chain, edit handler) instead of duplicating it.

---

## 1. What was implemented

| # | Item | Location |
|---|---|---|
| 1 | **Edit pre-flight**: `check_edit_preflight()` re-reads fresh bytes, rejects `NOOP` (old==new), `EDIT_NOT_FOUND`, `EDIT_AMBIGUOUS` (with first-3 line locations); `ToolRunner._edit` dispatches on it; content-shape identical overwrite also NOOPs | `tool_validation.py`, `tool_runner.py` |
| 2 | **Schema fail-fast**: `filePath`/`path`/`file_path` alias resolution (`resolve_file_path_arg`), NULL/blank/missing rejection with expected-shape hint (149-error class); `run_plan` rejects before dispatch | `tool_validation.py`, `tool_runner.py` |
| 3 | **rg fallback**: `Ensure-Ripgrep` in `dev.ps1` (status + setup, winget/scoop, never hard-fails); Python backend chain `rg → git grep → python` via `grep_backend()`; `rg` added to allowlist + `config/tool_allowlist.yaml`; grep record cap 64 KiB, line cap 500, match cap 100 (`tool_summarizer.py` + runner) | `scripts/dev/dev.ps1`, `tool_runner.py`, `tool_summarizer.py` |
| 4 | **PowerShell §17 linter**: `scan-ps-antipatterns.ps1` extended to the 5 FAIL patterns (negative `Select-Object`, `&&`, heredoc, `python3`, `$(--jq)`); runtime pre-flight in `tool_runner.py` via sibling `ps_linter.check_powershell_command` (do-not-execute reject). Target: rg 474× → 0, `Select-Object` 1,000+× → 0 over 14 d | `scripts/maintenance/scan-ps-antipatterns.ps1`, `ps_linter.py`, `tool_runner.py` |
| 5 | **Retry backoff + abort split**: `classify_tool_error()` (RATE_LIMITED / TARGET_UNREACHABLE / TRANSPORT_ERROR / BAD_REQUEST / USER_CANCELLED vs INFRA_ABORTED / DEPTH_LIMIT); `call_with_retry()` with 0.5 s→2 s→8 s exponential + ≤25% jitter, `Retry-After` floor, 3 attempts; `ToolRunner._webfetch` refactored onto it with injectable sleep | `tool_validation.py`, `tool_runner.py` |
| 6 | **subagent_depth=2**: NOT applied (root config, §18). Proposal doc with patch: `reports/opencode-db-toolfix-subagent-depth-2026-11-08.md`. Code-side: `depth_limit_fallback()` direct-execution envelope in `run_plan` for both error-result and exception paths | proposal report + `tool_validation.py` + `tool_runner.py` |
| 7 | **Deny audit + 50 KB cap + dedup**: `PERMISSION_DENIED` event type + `log_permission_deny()`; emitted for HITL denials (`hitl-denied`), path-sandbox escapes, command-allowlist rejections; `truncate_to_cap()` 50 KB (+head/tail spill marker) enforced in runner (`_cap_result_output`, `_read`) and summarizer (`summarize_tool_result`, `build_summarized_feedback`); `ToolOutputDeduper` pointer dedup (runner keeps sibling mtime/size read cache) | `audit/events.py`, `audit/integration.py`, `tool_validation.py`, `tool_runner.py`, `tool_summarizer.py` |

Also: `read` binary sniff (NUL-byte → `BINARY` code instead of a harness
error), `NOT_FOUND` code on missing files, `edit` 409 conflict carries
`error_code: CONFLICT`.

## 2. Files changed (this session)

- **Source:** `src/ai_company/executor/tool_validation.py` (extended),
  `src/ai_company/executor/tool_runner.py` (extended),
  `src/ai_company/executor/tool_summarizer.py`,
  `src/ai_company/audit/events.py`, `src/ai_company/audit/integration.py`,
  `config/tool_allowlist.yaml`
- **Scripts:** `scripts/dev/dev.ps1`, `scripts/maintenance/scan-ps-antipatterns.ps1`
- **Tests (new):** `tests/unit/test_tool_validation.py`,
  `tests/unit/test_tool_runner_toolfix.py`,
  `tests/unit/test_tool_summarizer_caps.py`
- **Reports (new):** this file,
  `reports/opencode-db-toolfix-subagent-depth-2026-11-08.md`
- **Not touched:** `AGENTS.md`, `opencode.json`, anything outside
  `C:\Users\jmlus\light-speed-holdings`.

## 3. Test evidence (actually run)

| Check | Command | Result |
|---|---|---|
| Ruff (scoped: 5 src + 3 test files) | `uv run ruff check …` | **All checks passed** |
| Mypy strict (4 src files) | `uv run mypy …tool_validation/tool_runner/tool_summarizer/integration` | **no issues found** |
| New tests | `pytest test_tool_validation / test_tool_runner_toolfix / test_tool_summarizer_caps` | **72 passed** |
| Regression | `pytest test_tool_summarizer / test_executor` | **66 passed** |
| Audit regression | `pytest test_audit / test_audit_integrity / test_audit_store` | **67 passed** |
| PS scanner (repo) | `pwsh -File scripts/maintenance/scan-ps-antipatterns.ps1` | **0 failures, 2 warnings** (pre-existing `Get-ChildItem` sort warnings in 2 unrelated scripts), exit 0 |
| PS scanner (fixture) | same, `-Path <tmp fixture with Select-Object -Last -30>` | **FAIL [select_negative], exit 1** as specified |

**Known gap (remains unknown until day-14 re-audit):** actual error-rate
deltas (edit 5.74%→<2%, schema 149→0, rg 474×→0, grep overflow 140→0)
cannot be claimed without re-running the analytics SQL against fresh
`opencode.db` data (T-12). All acceptance targets are listed in the
source plan §1; this report asserts only the local test evidence above.

## 4. Trade-offs (per team standard: every design decision has one)

| Decision | Trade-off |
|---|---|
| Repo-side shims instead of waiting for harness patches | Ships now, but duplicates logic that must be retired when upstream lands (keep `tool_validation.py` API stable for the port) |
| Depth fallback = direct execution, not retry | Deterministic failure made retriable-looking before; now explicit, but the parent agent silently does more work — mitigated by `fallback` flag + log |
| `call_with_retry` retries TARGET_UNREACHABLE | Matches "retry once then report" but triples every dead-localhost wait to ~3 attempts |
| 50 KB cap with head/tail sampling | Bounds context burn, but tail sampling can surface license/PII-adjacent text the head would not — acceptable vs the alternative (full flood) |
| `rg` install in `dev.ps1` warns instead of failing | Fresh clones self-heal; a broken host PATH still degrades silently to the slower backends |
