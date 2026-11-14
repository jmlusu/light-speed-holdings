# opencode.db Tool-Failure Fixes — Proposal (2026-11-08)

**Author role:** senior-backend-engineer, LightSpeed Holdings
**Date:** 2026-11-08
**Status:** Plan only — no code changes made in this task
**Sources (evidence):**
- `reports/opencode-db-analytics-2026-11-08.md` (188,713 tool parts, 3,435 errors = 1.82%)
- `reports/opencode-db-audit-2026-11-08.md` (§6 defects, §8 P2 recommendations 6–11)
- Workspace inspection 2026-11-08: `src/ai_company/executor/tool_runner.py`, `tool_summarizer.py`, `loop.py`, `agent_loop.py`, `scripts/maintenance/scan-ps-antipatterns.ps1`, `opencode.json`, `AGENTS.md` §17

**Scope boundary:** This report proposes fixes. It does not implement them. Per Evidence/Honesty Policy §15, every count below is taken from the two audits above; no new DB query was run for this plan. Files "likely touched" are proposals, not claims that a file was modified.

---

## 0. Executive summary

3,435 tool errors break down into a small number of systemic classes, not random noise. The top-10 recurring `(tool, error)` groups alone exceed 1,400 errors (analytics §4). Fixing the top 5 classes addresses ~70% of all errors:

| Rank | Defect class | Errors (all-time) | Share of 3,435 | Primary owner |
|---|---|---:|---:|---|
| 1 | `edit` semantic mismatch (oldString not found 588 + identical 154 + multi-match 74) | 816 | 23.8% | opencode harness (edit tool) + this repo (prompt/pre-flight) |
| 2 | `read` errors (959 total, incl. NULL filePath, harness-path probes, permission rejects) | 959* | 27.9%* | harness (schema) + this repo (context injection) |
| 3 | Ripgrep stack (`glob` 216 + `grep` overflow 140 + `grep` fail 20 + bash `rg` missing 474 stdout) | 850 | 24.7% | This host env + harness fallback |
| 4 | PowerShell antipatterns in `bash` stdout (`Select-Object -First/-Last <negative>` 1,162+; `&&`, heredoc, `python3`) | ~1,500+ stdout hits | — (stdout, not `status=error`) | This repo (AGENTS.md §17 enforcement) |
| 5 | `task` fragility (351 errors, 17.11%; aborted 104, cancelled 91, depth limit 40; 51 orphaned `running`) | 351 | 10.2% | Harness (depth/retry) + this repo (config) |
| 6 | Network rate-limit / transport (`websearch` 429 41x, exa transport 11x; `webfetch` 102 errors, 13.69%) | ~164 | 4.8% | Harness (retry/backoff) |
| 7 | Schema violations — NULL/missing required args (`edit` 65+21, `write` 24, `read` 19, `bash` 20) | 149 | 4.3% | Harness (fail-fast) + this repo (validator shim) |
| 8 | Output floods (`>50k` chars 1,641 completed outputs; `>100k` 5x; `grep` "Found 100 matches") | 1,641 | — (completed, wastes context) | Harness (cap) + this repo (`tool_summarizer.py`) |
| 9 | Permission denies (`write` rule prevents 29, user rejected 37) | 66 | 1.9% | This repo (`opencode.json` + audit) |

\* `read` 959 overlaps classes 7 and 9; do not sum ranks 1–9.

**Key architectural distinction (applies to every fix below):**

- **This repo** (`C:\Users\jmlus\light-speed-holdings`) can change: `AGENTS.md` §17, `opencode.json`, `src/ai_company/executor/*`, `scripts/maintenance/*`, `scripts/dev/*`, agent generator (`company-registry.yaml` → `.opencode/agents/*.md`), tests, docs.
- **opencode harness** (upstream, not in this repo) owns: the `edit`/`read`/`grep`/`glob`/`task`/`webfetch` tool implementations, JSON-schema validation, ripgrep backend, subagent depth enforcement, MCP transport retry, permission engine. Fixes there must be filed/patched upstream or via plugin/MCP shim; this repo can only *work around* them (pre-flight validation, fallback, config).

Each fix below states which side it lands on. Do not assume a harness fix is deployable from this repo.

**Governance note:** `AGENTS.md` and `opencode.json` are root config files. Per AGENTS.md §18, any commit touching either requires `[CEO-OVERRIDE: <reason>]` in the commit message, enforced by `scripts/lint/validate-root-config.ps1`. Tasks T-05 and T-09 touch these files — budget for the tag + audit-log entry.

---

## 1. Prioritized task list

| # | Task | Class | Effort | Priority | Repo / Harness |
|---|---|---|---|---|---|
| T-01 | `edit` pre-flight validation: re-read region + reject identical + enforce uniqueness before mutation | edit 816 | M (2–4 d) | **P0** | Harness patch; repo-side shim in `tool_runner.py` |
| T-02 | Schema fail-fast: reject NULL/missing `filePath`/`command`/`oldString` with repair hint, don't execute/retry blind | schema 149 | S (1 d) | **P0** | Harness; repo validator shim |
| T-03 | Install `rg` on PATH + verify; add `grep`/`glob` fallback when `rg` absent | rg 474 + 236 | S (0.5 d) | **P0** | Host env + this repo (`dev.ps1`) |
| T-04 | `grep` record-overflow fix: raise/cap per-record bytes + match limit (kills 140 overflow + 1,641 floods) | grep 140 + floods | M (2 d) | **P0** | Harness; repo cap in `tool_summarizer.py` |
| T-05 | PowerShell §17 enforcement: extend `scan-ps-antipatterns.ps1` + pre-flight bash lint + `.ps1` temp-file rule in prompt | PS ~1,500 stdout | S–M (1–2 d) | **P0** | This repo only |
| T-06 | Raise subagent depth for orchestrators + add direct-work fallback logging | task depth 40 | S (0.5 d config) | **P1** | `opencode.json` + harness |
| T-07 | Retry with exponential backoff + jitter for 429 / transport errors (`websearch`, `webfetch`) | 429 41x, fetch 102 | M (2–3 d) | **P1** | Harness / MCP plugin |
| T-08 | Task abort/cancel resilience: distinguish user-cancel vs infra-abort; sweeper for orphaned `running` (93) + `pending` (2) | task 195 + orphans | M (3 d) | **P1** | Harness; repo sweeper script |
| T-09 | Permission-deny audit: log + dashboard every deny; review `write`/`edit` rulesets | denies 66 | S (1 d) | **P1** | This repo (`opencode.json`, dashboard) |
| T-10 | Read-path hygiene: stop probing absent `harness/changes/active/summary.md` (21x) / `pending.md` (19x); inject context once | read churn | S–M (1–2 d) | **P2** | This repo (ECL prompt/context) |
| T-11 | Output cap enforcement end-to-end (tool → summarizer → `tool-output/` spill) | floods 1,641 | M (2 d) | **P2** | Harness + `tool_summarizer.py` |
| T-12 | Regression gate: re-run audit SQL (§10 of analytics report) 14 days after P0 lands; assert error-rate deltas | all | S (0.5 d) | **P2** | This repo (CI/docs) |

Effort scale: S = ≤1 d, M = 2–4 d. All estimates exclude upstream review/merge latency for harness patches.

---

## 2. Per-defect proposals

### T-01 — `edit` semantic failures: oldString not found 588x/221 sessions, no-op 154x, multi-match 74x

**Evidence:** Analytics §4 (588/221 sessions, 2026-08-07→10-21, systemic); audit §6.1 (588+154+74 = 816, 23.8% of all errors); edit error rate 5.74% (949/16,540, analytics §2.1) — highest among core file tools.

**Root cause (proposed, three sub-causes):**
1. **Stale context:** Agent edits against a remembered file image, not the current disk image. Whitespace/indentation/CRLF drift (Windows CRLF vs LF, trailing spaces) makes exact-match fail. No re-read of the target region at edit time.
2. **No client-side no-op check:** `oldString == newString` is only detected server-side after a full tool round-trip; 154 cases are pure waste.
3. **Under-specified anchor:** Short `oldString` matches N places; tool correctly refuses (ambiguous) but the caller had no uniqueness pre-check, so the round-trip is wasted.

**Fix (harness, preferred):** In the `edit` tool implementation, before mutation:
- (a) Re-read the file at call time and match against fresh bytes (do not trust a cached image).
- (b) Normalize only for *comparison* (report CRLF/LF divergence explicitly); require exact match for *mutation*.
- (c) Reject `oldString == newString` (after trimming? No — exact equality) with a `NOOP` error code distinct from mismatch, so callers can skip without a retry loop.
- (d) On multi-match, return the match count + first 3 locations (line numbers) instead of a bare refusal, so the agent can widen context in one step.
- (e) On not-found, return the nearest fuzzy anchor (e.g. "found 12/14 lines; line 42 differs: trailing space") — bounded to avoid leaking whole files.

**Fix (this repo, shim until harness lands):** Add a pre-flight validator in `src/ai_company/executor/tool_runner.py` (next to tier-rule check):
- Maintain a per-session `file:m​time+hash` cache populated by `read`; `edit` requests for a path not read in this session (or read >N tool calls ago) trigger a forced re-read or a warning injected into the tool result.
- Reject `old == new` in `ToolRunner` before dispatch (return structured `NOOP` result; log to audit trail via existing `log_tool_call`).
- Count occurrences of `oldString` in the cached content; if 0 → return `NOT_FOUND` + hint to re-read; if >1 → return `AMBIGUOUS` + locations. This converts a harness error (counted in the 949) into a cheap local check.

Also update agent prompt templates (`src/ai_company/executor/prompts.py`, `optimized_prompts.py`): "Re-read the exact region immediately before editing; include ≥3 lines of surrounding context; never copy `oldString` from a read older than this session."

**Files likely touched:**
- *Harness (upstream):* edit tool source (exact-match + error messages) — not in this repo.
- *This repo:* `src/ai_company/executor/tool_runner.py`, `src/ai_company/executor/prompts.py`, `src/ai_company/executor/optimized_prompts.py`, `tests/unit/test_tool_runner*.py` (new), `AGENTS.md` §17 (add edit rule).

**Acceptance criteria:**
- `edit` error rate < 2.0% measured over next 2 weeks of `opencode.db` (from 5.74%).
- `oldString not found` ≤ 150 and `no-op` ≤ 20 in the same window (from 588/154).
- Zero `edit` calls dispatched with `old == new` (verifiable in `tool_runner` audit log).

**Verification:**
- Unit tests: CRLF file, trailing-space file, duplicate-anchor file, `old==new` file — each asserts correct reject/accept + error code.
- Re-run analytics SQL B/D (`GROUP BY tool,status`; repeated-failure grouping) after 14 days; compare §4 table.
- `uv run ruff check src/ && uv run mypy src/ && uv run pytest` per AGENTS.md §6.

**Effort:** M (2–4 d: 0.5 d validator, 1 d prompts, 1 d tests, 0.5 d re-audit). Harness patch itself is upstream-sized; shim is the repo-deliverable.

---

### T-02 — Schema violations: NULL/missing `filePath` (edit 71 NULL / 65 missing-key, write 32/24, read 19, bash `command` 20)

**Evidence:** Analytics §4 + §6 (NULL `filePath` in GROUP BY), §8.6 (149 schema errors); audit §6.1 (≥149).

**Root cause:** Malformed tool-call JSON from the model is recorded as a full tool error and the agent retries blindly (no repair hint). Validation happens *after* persistence, not *before* execution. The model never sees the correct shape.

**Fix (harness, preferred):** Validate tool-call JSON against the tool's JSON Schema at dispatch; on `Missing key`, return a fail-fast structured error containing the missing key, the expected shape (one-line example), and the last valid call for that tool in the session. Never persist a `part` with `status=error` for a call that never executed — log it as `validation_rejected` separately so it does not pollute the error-rate denominator.

**Fix (this repo, shim):** Add `validate_tool_args(tool, args) -> list[str]` in `tool_runner.py` (or new `executor/tool_validation.py`):
- Required-arg table: `edit: [filePath, oldString, newString]`, `write: [filePath, content]`, `read: [filePath]`, `bash: [command]`, `grep/glob: [pattern/path per schema]`.
- Reject empty-string and `None` as missing (the NULL `filePath` cases).
- Return the same repair-hint shape the harness fix would, so porting later is trivial.

**Files likely touched:**
- *Harness:* tool dispatch + schema registry.
- *This repo:* `src/ai_company/executor/tool_runner.py` (or new `tool_validation.py`), `src/ai_company/models/models.py` if canonical tool args are modelled there, `tests/unit/test_tool_validation.py` (new).

**Acceptance criteria:**
- Schema-error count (Missing-key groups) = 0 in next 2-week window (from 149).
- No `part` rows with `NULL filePath` in `edit`/`write`/`read` after fix.
- Every validation rejection returns the missing key + expected shape (asserted in test).

**Verification:**
- Unit tests: each tool × (missing key, null key, empty key) → correct rejection.
- SQL: `SELECT COUNT(*) FROM part WHERE tool IN ('edit','write','read') AND json_extract(data,'$.state.input.filePath') IS NULL` → 0.
- Analytics §10 query D re-run.

**Effort:** S (1 d).

---

### T-03 — Ripgrep missing: bash `rg` not recognized 474x; `glob` ripgrep failed 216x; `grep` ripgrep failed 20x

**Evidence:** Audit §6.2 (474 stdout hits, "#1 repeated env error"); analytics §4 (glob 216/33 sessions, grep 20/18 sessions).

**Root cause:** `rg` is not on Windows `PATH` for the shell the agent's `bash` tool spawns. The instruction "install ripgrep" was never executed on this host, and `grep`/`glob` apparently lack a working fallback when `rg` is absent — or the fallback exists in the harness but the agent bypasses it by calling `rg` directly in `bash`.

**Fix (host + this repo, do both):**
1. Install ripgrep on the host (`winget install BurntSushi.ripgrep.MSVC` or `scoop install ripgrep`) and verify `Get-Command rg` inside the same PowerShell profile the `bash` tool uses (PS 5.1 vs pwsh 7 PATH differences are a known trap — see §17).
2. Add a PATH check to `scripts/dev/dev.ps1` (setup step): `if (-not (Get-Command rg)) { winget install … }` with a clear WARN if install fails, so fresh clones self-heal.
3. Document in `docs/DEVELOPMENT.md` (required host tools: `uv`, `rg`, `sqlite3`).
4. Belt-and-braces: in `src/ai_company/executor/tool_runner.py` allowlist, ensure `rg` is an allowed command prefix (check `_DEFAULT_ALLOWED_COMMANDS` / `config/tool_allowlist.yaml`) so the fix isn't blocked by the sandbox.

**Fix (harness, upstream):** `grep`/`glob` should detect missing `rg` at startup and fall back to a native implementation (or return a structured `RG_MISSING` error with install instructions instead of generic "ripgrep execution failed"). Generic failure messages are why 216 glob errors have no actionable signal.

**Files likely touched:**
- *This repo:* `scripts/dev/dev.ps1`, `docs/DEVELOPMENT.md`, `config/tool_allowlist.yaml`, `src/ai_company/executor/tool_runner.py` (allowlist only).
- *Host (not repo):* Windows PATH.
- *Harness:* grep/glob backend fallback.

**Acceptance criteria:**
- `rg --version` succeeds in the agent `bash` tool shell.
- `rg : The term 'rg' is not recognized` stdout hits = 0 in next window (from 474).
- `glob` error rate < 0.5% (from 1.91%).

**Verification:**
- `bash` tool: run `rg --version; rg -n "TODO" --max-count 1 src/` → exit 0.
- Re-run repeated-stdout-error SQL (audit §6.2 query) → rg group absent.
- `pwsh scripts/dev/dev.ps1 status` shows rg OK.

**Effort:** S (0.5 d, mostly host install + verification; fallback is upstream).

---

### T-04 — `grep` JSON record overflow 140x + invalid match output 16x

**Evidence:** Analytics §4 (140/107 sessions, 2026-08-07→10-22, systemic); §3.2 (117 in last 30 d).

**Root cause:** A single ripgrep JSON line (one match record, including context/long lines in `brand/`, `docs/`) exceeds 65,536 bytes. The harness parses ripgrep `--json` output record-by-record with a 64 KB line cap and errors out instead of truncating the record. Long lines (minified bundles, generated HTML, `.opencode/skills/*/examples/*.json`) make this a when-not-if failure.

**Fix (harness, preferred):** Raise the per-record cap (e.g. to 1 MB) AND truncate overlong match text at the producer (e.g. `rg --max-columns 500` / truncate field to 500 chars with `…`). Neither alone suffices: raising the cap without truncation still floods context; truncating without raising the cap still errors on pathological single lines.

**Fix (this repo, immediate mitigation):** Prompt + summarizer level:
- In agent templates, forbid unbounded `grep` over `brand/`, `docs/`, `.opencode/skills/` without `--max-count` / `include` filters; require a `path` scoped to the smallest subtree.
- In `src/ai_company/executor/tool_summarizer.py`, cap any single `grep` match line at 500 chars and cap total matches returned to the model at 100 with a `(N more matches available — narrow your pattern)` footer (the harness already emits this footer; enforce it repo-side too).

**Files likely touched:**
- *Harness:* grep backend (record size + column cap).
- *This repo:* `src/ai_company/executor/tool_summarizer.py`, `src/ai_company/executor/prompts.py`, `AGENTS.md` §17 (grep scoping rule).

**Acceptance criteria:**
- `Ripgrep JSON record exceeded 65536 bytes` = 0 (from 140).
- `Invalid ripgrep match output` = 0 (from 16).
- No completed `grep` output > 50 KB attributable to a single record.

**Verification:**
- Repro: `grep` a pattern matching a minified/generated file from §8.4 top-15 (e.g. `.opencode/skills/archify` examples) → returns truncated match, no error.
- Unit test in `tool_summarizer.py`: 200 KB single line → truncated to ≤500 chars with ellipsis, match count preserved.
- Analytics SQL D re-run.

**Effort:** M (2 d; 0.5 d summarizer, 0.5 d prompts, 1 d verification against the §8.4 corpus).

---

### T-05 — PowerShell antipatterns: `Select-Object -First/-Last <negative>` (−30: 289x, −20: 287x, −5: 185x, −50: 125x, −100: 113x, −80: 81x, Last −20: 84x), `&&`, heredoc, `python3`, quoting

**Evidence:** Audit §6.2 (exact recurrences of AGENTS.md §17, months-long signal); AGENTS.md §17 already documents the fixes but they are not enforced at runtime. `scripts/maintenance/scan-ps-antipatterns.ps1` currently checks only 2 patterns (backtick-`$`, unsorted `Get-ChildItem`) — none of the §17 bash antipatterns.

**Root cause:** Documentation without enforcement. The model is trained on bash/zsh idioms (`head -n -30`, `&&`, `<<EOF`) and PowerShell 5.1 rejects negative `Select-Object` args, `&&`, and bash heredocs. The lesson is in AGENTS.md but nothing intercepts the command before execution, and the existing scanner doesn't cover these patterns. Training the model harder is the slowest fix.

**Fix (this repo only — highest-leverage repo fix):**
1. **Extend `scripts/maintenance/scan-ps-antipatterns.ps1`** with FAIL patterns:
   - `Select-Object -(First|Last)\s+-\d+` (negative arg — the 1,162+ class)
   - `&&` as statement separator outside strings/comments
   - `<<\s*'?[A-Z]` heredoc redirection (`python << 'PYEOF'` 118x)
   - `\bpython3\b` on Windows (81x; use `python`)
   - `$(` inside double-quoted `--jq` argument (the §17 standing directive)
2. **Add a pre-flight bash lint in `tool_runner.py`:** before `bash` dispatch, regex-scan `command` for the same patterns; on hit, return `POWERSHELL_ANTIPATTERN` with the corrected form (e.g. `Select-Object -Last 30` → `| Select-Object -Skip 30` implied, or `@(...)` slicing) and **do not execute**. This converts a wasted shell round-trip into an instant local rejection — same pattern as T-01/T-02.
3. **Codify the `.ps1` temp-file rule** (already in §17): any multi-statement command with `$vars`/`$(…)`/nested quoting must be written to a temp `.ps1` and run via `powershell -File`. Add to `prompts.py` as a hard instruction, not a suggestion.
4. **Wire the scanner into CI** (`.github/workflows/ci.yml` or `.pre-commit-config.yaml`): `pwsh -File scripts/maintenance/scan-ps-antipatterns.ps1` on `scripts/**/*.ps1` + any `.ps1` in repo. Note: repo has no committed `.pre-commit-config.yaml` in the current checkout listing — confirm path before wiring; `lint-ecl.ps1` is the existing harness-script gate to mirror.

**Files likely touched (all this repo):**
- `scripts/maintenance/scan-ps-antipatterns.ps1` (extend)
- `src/ai_company/executor/tool_runner.py` (pre-flight lint)
- `src/ai_company/executor/prompts.py` (temp-`.ps1` rule)
- `AGENTS.md` §17 (add T-01/T-04/T-05 rules as one edit; requires `[CEO-OVERRIDE: …]` commit tag per §18)
- `.github/workflows/ci.yml` or `.pre-commit-config.yaml` (wire scanner)

**Acceptance criteria:**
- Scanner FAILs on a fixture `.ps1` containing each of the 5 patterns; passes on clean scripts.
- Pre-flight lint blocks `Get-ChildItem | Select-Object -First -30` without executing (unit test).
- `Select-Object` negative-arg stdout hits = 0 in next window (from 1,162+ summed).

**Verification:**
- `pwsh scripts/maintenance/scan-ps-antipatterns.ps1` → exit 0 on current repo (after fixing any hits it finds — it may find pre-existing violations; that is the point).
- Unit tests for each pattern. Re-run audit §6.2 SQL → groups absent.
- `uv run pytest` per §6.

**Effort:** S–M (1–2 d).

---

### T-06 — Task depth limit 40x ("Subagent depth limit reached (1)")

**Evidence:** Analytics §4 (40/10 sessions); audit §6.4 (reproduced live during the audit — chief-of-staff could not spawn a subagent and fell back to direct execution).

**Root cause:** Harness default `subagent_depth = 1` forbids any subagent spawning a subagent. Orchestrator-class agents (chief-of-staff, cto, vp-engineering, lead-backend) are designed to delegate, so depth-1 makes their core workflow fail by construction. The error is deterministic, not transient — retrying never helps.

**Fix:**
1. *Config (this repo):* In `opencode.json`, set depth explicitly per agent class, e.g. `agent.<orchestrator>.subagent_depth` (or the harness's equivalent key — confirm against `https://opencode.ai/config.schema.json`; current `opencode.json` in this repo sets only `default.maxContextTokens` and `default.autoReadFiles`) — raise orchestrators to 2, keep leaf agents at 1.
2. *Harness (upstream):* Document the intended delegation depth a agent card may assume; return a structured `DEPTH_LIMIT` error naming the current depth and the agent that must do the work directly.
3. *This repo (fallback):* In agent cards generated from `company-registry.yaml` (`templates/agents/agent.md.j2` → `.opencode/agents/*.md`), add: "If subagent spawn fails with depth-limit, execute directly and log the fallback" — the audit proved this fallback works and should be explicit, not improvised.

**Files likely touched:**
- *This repo:* `opencode.json` (requires `[CEO-OVERRIDE: …]`), `company-registry.yaml` (orchestrator agent cards), `templates/agents/agent.md.j2`, regenerated `.opencode/agents/*.md`.
- *Harness:* depth config schema.

**Acceptance criteria:**
- An orchestrator-class session can spawn depth-2 subagent; leaf agents still at depth 1 (test session).
- `Subagent depth limit reached` = 0 in next window (from 40).

**Verification:**
- Manual spawn test from a `chief-of-staff` session → success.
- Re-run analytics SQL D → depth group absent. `uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` per §6 (template change).

**Effort:** S (0.5 d config + regeneration; excludes upstream schema work).

---

### T-07 — Rate limits & transport: `websearch` 429 41x (2026-09-13 burst), exa transport 11x, `webfetch` 102 errors / 13.69%

**Evidence:** Analytics §4 (429 41/3 sessions, <1 h burst, self-resolved); §2.1 (`webfetch` 13.69%, `websearch` 7.11% — highest rates among frequent tools); §3.2 (exa transport, localhost:1441 fetch).

**Root cause:** Two sub-causes. (a) No client-side retry/backoff: a 429 is surfaced as a terminal error and the agent either gives up or retries immediately, re-hitting the limit. (b) `webfetch` failures are largely *target* failures (localhost dev server down, TLS/transport), not tool bugs — but the tool returns them identically, so the agent cannot distinguish "retry later" from "target is down, check port binding (AGENTS.md §12)".

**Fix (harness/plugin):**
- Retry `websearch`/`webfetch` on 429/5xx/transport with exponential backoff + jitter (e.g. 3 attempts: 0.5 s, 2 s, 8 s), honoring `Retry-After` when present. Classify terminal errors: `RATE_LIMITED` (retryable), `TARGET_UNREACHABLE` (retryable once, then report), `BAD_REQUEST` (not retryable).
- `kv.websearch:provider="random"` (audit §2) means provider flapping amplifies 429s — pin a provider for bursty workloads or add a circuit breaker after 3 consecutive 429s.

**Fix (this repo):**
- In `src/ai_company/executor/tool_runner.py` (or LLM client `src/ai_company/llm/client.py` if web tools route there): retry wrapper for `webfetch`-class calls with the backoff above; log retry count to the audit trail (`log_tool_call`).
- `opencode.json`: pin `websearch` provider instead of `random` (requires `[CEO-OVERRIDE: …]`).

**Files likely touched:**
- *Harness/plugin:* MCP `websearch`/`webfetch` implementations.
- *This repo:* `src/ai_company/executor/tool_runner.py` or `src/ai_company/llm/client.py`, `opencode.json`, `config/tool_allowlist.yaml` if applicable.

**Acceptance criteria:**
- 429 burst test (mock 429×2 then 200) → tool succeeds on 3rd attempt, no error recorded.
- `websearch` error rate < 2% (from 7.11%); `webfetch` < 5% (from 13.69%) excluding target-down cases.

**Verification:**
- Unit tests with mocked transport (429, 5xx, timeout, success-after-retry).
- Re-run analytics SQL D → 429 group absent or ≤5.
- Confirm `webfetch` to a down localhost returns `TARGET_UNREACHABLE` (not generic transport) — documented in test.

**Effort:** M (2–3 d, mostly retry wrapper + tests; harness side is upstream).

---

### T-08 — Task abort / cancel: aborted 104x, cancelled 91x; 93 orphaned `running` + 2 `pending`

**Evidence:** Analytics §4 (aborted 104/35 sessions, cancelled 91/27), §8.5 (93 `running`, led by `task` 51, `bash` 30); audit §6.3 (no sweeper).

**Root cause:** Two distinct causes share one label. `Task cancelled` is usually *user/agent-initiated* (legitimate). `Tool execution aborted` is *infra-initiated* (subagent killed, session torn down, `ChildProcess.kill` on PowerShell — analytics §3.2 shows 7×3 distinct `bash` kill commands). Without cause separation, neither is actionable. Orphaned `running` parts are killed sessions whose completion was never written and no TTL sweeper exists (unlike the HITL `EXPIRED` sweep the org already built, §9.1).

**Fix:**
1. *Harness:* split error codes: `USER_CANCELLED` vs `INFRA_ABORTED` (with `reason: subagent_killed | session_closed | child_process_kill | timeout`). Add a TTL sweeper: `running` > 1 h → `error` with `orphaned=true`.
2. *This repo:* Add a periodic sweeper script mirroring the HITL expiry sweep policy — `scripts/maintenance/sweep-orphaned-tool-calls.ps1` or a Python module `src/ai_company/executor/tool_sweeper.py` that runs against `opencode.db` (read-only snapshot first) and reports orphans; do NOT mutate the live DB from this repo without a maintenance window (audit §8 P1-1 already owns WAL checkpointing — coordinate, don't duplicate).

**Files likely touched:**
- *Harness:* task lifecycle + error taxonomy + sweeper.
- *This repo:* new `scripts/maintenance/sweep-orphaned-tool-calls.ps1` (or `.py`), `src/ai_company/executor/daemon.py` / `loop.py` (schedule), `tests/` for sweeper.

**Acceptance criteria:**
- New aborts carry a cause code; `INFRA_ABORTED` rate reported separately from `USER_CANCELLED`.
- Orphaned `running` > 1 h = 0 after sweeper runs (from 93).

**Verification:**
- Kill a `bash` child mid-run in a test session → `INFRA_ABORTED` with `child_process_kill`, not generic abort.
- Sweeper dry-run on current DB → reports 93 orphans; after maintenance window → 0.
- Analytics SQL G (`status='running'` count) re-run.

**Effort:** M (3 d; 1 d taxonomy, 1 d sweeper, 1 d coordination with P1 storage work).

---

### T-09 — Permission denies: `write` rule prevents 29x, user rejected 37x; `read` rejected 21x

**Evidence:** Analytics §4; audit §6.1 (34 `edit` rule-prevents, `edit` deny `*` except `.opencode/plans/*.md`); `opencode.json` currently `permission: {edit: allow, bash: allow}` — stricter than the audited ruleset (ruleset has since changed, or per-agent cards override it).

**Root cause:** Permission rulesets are inconsistent across layers (`opencode.json` vs generated agent cards vs harness defaults) and denials are silent — the agent sees "rule prevents" with no indication of *which* rule, *which* path, or *how to request an exception*. 29 `write` denials across 20 sessions is agents repeatedly hitting the same wall.

**Fix (this repo):**
1. Audit every deny: add structured deny logging (tool, path, matched rule, agent, session) to `src/ai_company/audit/` (`log_tool_call` already exists in `tool_runner.py` — extend the event).
2. Reconcile rulesets: single source of truth — `opencode.json` `permission` block should match what generated cards in `.opencode/agents/*.md` declare. Add a consistency check to `src/ai_company/generator.py` (fail generation if card permissions diverge from `opencode.json`).
3. Surface denies in the CEO Dashboard (`src/ai_company/dashboard/api.py` — already the most-read file, 758×; add a `/permits/denies` endpoint) so the Human CEO sees them without a DB dive.
4. Document the deny→exception path in `AGENTS.md` §7 (Safety Boundaries): what to do when blocked (park/escalate vs retry).

**Files likely touched (all this repo):**
- `src/ai_company/audit/integration.py` (deny event), `src/ai_company/executor/tool_runner.py` (emit deny), `opencode.json` (reconcile; `[CEO-OVERRIDE: …]`), `src/ai_company/generator.py` (consistency check), `src/ai_company/dashboard/api.py` (endpoint), `AGENTS.md` §7.

**Acceptance criteria:**
- 100% of denials emit a structured audit event with rule id + path.
- Generator fails on permission divergence (test: intentionally diverge → generation error).
- Dashboard `/permits/denies` returns last-30-d deny count.

**Verification:**
- Trigger a deny in a test session (outside-allowlist path) → audit event + dashboard row present.
- Re-run analytics SQL D → `rule prevents`/`rejected permission` groups each ≤5 in next window, or every remaining instance has a linked exception request.

**Effort:** S (1 d).

---

### T-10 — Read-path hygiene: harness-path probes (`summary.md` 21x, `pending.md` 19x), file-not-found 40x, binary-read 8x

**Evidence:** Analytics §4; §5 (1,100 files read >10×; `harness/changes/active/summary.md` read 284× but "File not found" 21× when no active change exists — context-loading rule AGENTS.md §4.3–4.5).

**Root cause:** Agents unconditionally probe `harness/changes/active/summary.md` and `harness/evolution/pending.md` at session start; when no active change/pending evolution exists, the read fails and is counted as a tool error. The existence check is not done before the read. Secondary: `read` on binary files (`.env.example` 8x) and non-existent docs (`REMAINING-WORK-INVENTORY.md` 10x) — no existence/type pre-check.

**Fix (this repo):**
1. `src/ai_company/executor/context.py`: before injecting ECL context, `Test-Path`-equivalent check; only read when present. Return `NO_ACTIVE_CHANGE` sentinel instead of attempting the read.
2. `tool_runner.py` `read` pre-flight: existence + binary sniff (NUL-byte check on first 8 KB) → structured `NOT_FOUND` / `BINARY` without a harness error record; suggest `bash`/`webfetch` alternative for binary.
3. Prompts (`prompts.py`): restate AGENTS.md §4 order as an explicit step — "Check `harness/changes/active/summary.md` exists before reading; if absent, read `docs/STATUS.md`."

**Files likely touched (this repo):**
- `src/ai_company/executor/context.py`, `src/ai_company/executor/tool_runner.py`, `src/ai_company/executor/prompts.py`, `tests/unit/test_context*.py`.

**Acceptance criteria:**
- `File not found: …/summary.md` and `…/pending.md` = 0 (from 40).
- `Cannot read binary file` = 0 (from 8).
- `read` error rate < 1.0% (from 1.82%).

**Verification:**
- Test session with no active change → clean startup, no read errors in trace.
- Analytics SQL D/E re-run.

**Effort:** S–M (1–2 d).

---

### T-11 — Output floods: >50k chars 1,641 completed outputs; >100k 5x; `grep` "Found 100 matches" dominates §8.4 top-15

**Evidence:** Analytics §8.4 (1,641 >50k; top-15 almost all `grep` floods over `brand/`+`docs/`+`.opencode/skills/`; largest 131,055 chars). Audit §5.2 (tool-output spill re-read 288×).

**Root cause:** No end-to-end output budget. `grep` returns 100 matches × long lines; `read` returns whole files; the result is persisted to `~/.local/share/opencode/tool-output/` and the *next* agent re-reads the spill instead of re-running the tool or summarizing it. Context burn is the downstream cost (analytics §7: cache reads 8.9× input).

**Fix:**
1. *Harness:* hard cap on tool output bytes returned to the model (e.g. 50 KB) with `truncated=true` + spill-file pointer. The `tool-output/` spill already exists — make the return value a summary + pointer by default, not the full text.
2. *This repo:* `src/ai_company/executor/tool_summarizer.py` already compresses verbose output (`count_tokens` budgets, per REA feasibility §03) — extend it: enforce a 50 KB cap with head/tail sampling + match-count footer for `grep`; summarize spill files on write; add per-session dedup (second `read` of same path+mtime returns a pointer: "unchanged since step N" — audit §8 P3-14 estimates ≥30% read-volume cut).
3. Prompts: "Never re-read a `tool-output/` spill file; re-run the tool or summarize from the first read."

**Files likely touched:**
- *Harness:* tool output pipeline + truncation.
- *This repo:* `src/ai_company/executor/tool_summarizer.py`, `src/ai_company/executor/context.py` (dedup), `src/ai_company/executor/prompts.py`, `tests/unit/test_tool_summarizer*.py`.

**Acceptance criteria:**
- Completed outputs >50k chars ≤ 100 in next window (from 1,641); >100k = 0.
- No `tool-output/` file read more than 5× per session (from 288×).
- `read` calls to the top-10 hot files (analytics §5) drop ≥20%.

**Verification:**
- Flood repro: unbounded `grep` over `brand/` → capped ≤50 KB with footer.
- Re-run analytics SQL G (large-output queries) — compare §8.4 table.

**Effort:** M (2 d; repo side; harness cap is upstream).

---

### T-12 — Regression gate (closes the loop)

**Fix (this repo):** Adopt analytics §10 SQL as a repeatable gate:
- `scripts/maintenance/audit-opencode-db.ps1` (new): runs queries B, D, G read-only against a snapshot (`sqlite3 ".backup"` copy, per audit §8 P1-5), emits a markdown delta vs this report's baseline, and FAILs CI if: total error rate > 1.0% (from 1.82%), `edit` errors > 2%, any §4 recurring group > 20, or `running` orphans > 10.
- Schedule 14 days after P0 lands; file the delta report as `reports/opencode-db-audit-<date>.md` following the existing naming convention.

**Files likely touched (this repo):** new `scripts/maintenance/audit-opencode-db.ps1`, `.github/workflows/ci.yml` (schedule/manual), `docs/STATUS.md` (baseline link).

**Acceptance criteria:** Gate runs green on current DB (documenting the baseline) and red on a fixture DB with injected errors.

**Verification:** Run gate twice (live DB copy) → identical counts; inject 10 synthetic error rows into the copy → gate FAILs.

**Effort:** S (0.5 d).

---

## 3. What not to do (negative constraints)

1. **Do not hand-edit `opencode.db`** to "fix" counts — it is a live WAL-backed store (audit §1); all verification is read-only snapshot + SQL.
2. **Do not log `cache_write` as a savings metric** — it is 0 everywhere (provider quirk, analytics §7); T-11 budgets must use `input + cache_read` volume.
3. **Do not fix PowerShell antipatterns by prompt alone** — 1,500+ repetitions after §17 documentation prove awareness ≠ enforcement (T-05 lint is mandatory).
4. **Do not raise `subagent_depth` globally** — scope to orchestrator agents (T-06); leaf agents at depth 2 multiplies spawn surface.
5. **Do not delete the 38.5 GB `.bak` or checkpoint the WAL in the same change** — audit §8 P1 owns storage; coordinate the maintenance window, don't interleave.

## 4. Suggested sequencing

**Week 1 (P0, repo-side):** T-03 (rg install, 0.5 d) → T-05 (PS lint, 1–2 d) → T-02 (schema validator, 1 d). These are independent, low-risk, and remove ~2,000+ stdout/error hits.
**Week 2 (P0, edit/grep):** T-01 shim + prompts → T-04 summarizer cap. File upstream harness issues for T-01/T-04 fixes in parallel.
**Week 3 (P1):** T-06 config → T-07 retry → T-09 deny audit. T-08 only after P1 storage window (audit §8).
**Week 4:** T-10, T-11, T-12 gate. Re-audit at day 14 (T-12) and publish delta.

## 5. Execution integrity

- Requested: plan-only proposals for 12 defect classes, write to `reports/opencode-db-toolfix-2026-11-08.md`, no code changes, prioritized tasks returned.
- Attempted: read both audit reports in full; inspected `tool_runner.py` (1–120), `scan-ps-antipatterns.ps1`, `opencode.json`, repo layout.
- Actually happened: this report created at the requested path. No source, config, or DB file was modified. No DB query was run; all counts are quoted from the two evidence reports.
- Independently verified: file paths above were confirmed to exist in the current checkout; `scan-ps-antipatterns.ps1` coverage (2 patterns) and `opencode.json` permission block were read directly.
- Remains unknown: exact harness-side file paths for the `edit`/`grep`/`task` tool implementations (upstream repo not inspected); `.pre-commit-config.yaml` presence in the current checkout (glob returned no match — confirm before T-05 wiring).
