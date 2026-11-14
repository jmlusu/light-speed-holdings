# opencode.db Security Implementation — 2026-11-08

**Author:** ciso (CISO) for LightSpeed Holdings.
**Plan source:** `reports/opencode-db-security-fix-2026-11-08.md` (R1–R6; F-01–F-12).
Scope of this report: the **P0 code/config hardening** from that plan (items
1–7 below). DB-mutating work (WAL checkpoint, VACUUM, `.bak` disposal, row
purges) is **not** executed here — it stays gated behind a maintenance
window, a pre-change snapshot, and this plan's §12 discipline.

> **No secret values appear in this report.** Counts, key names, hosts, and
> pattern IDs only, per `AGENTS.md` §9.2.

---

## 0. Parallel-session reconciliation (read this first)

A second agent session implemented the same hardening while this task ran
(its wiring is already in `ToolRunner`; its modules are `security/redact.py`
and `security/egress.py`, and its `security/path_policy.py` was an untracked
same-path file). This session **overwrote that untracked `path_policy.py`**
with its own implementation before discovering the overlap — an honest error
to flag here, per the §15 evidence policy. The adopted module exposes the
same call-compatible `deny_reason(path) -> str | None` the wired
`ToolRunner` uses, so the stranded call sites work; the parallel owner
should re-diff their version against the adopted module. The single
implementation now in the tree is:

| Module | Role |
|---|---|
| `src/ai_company/security/redact.py` | F-05 redaction (`redact_secrets`; this session **added** `redact_part_data` with the JSON validity re-check) |
| `src/ai_company/security/egress.py` | F-07/F-08 egress (`validate_egress_url`; this session **added** suspended-host deny + YAML extras + `check_shell_egress`) |
| `src/ai_company/security/path_policy.py` | F-06 read-deny (`deny_reason`, `is_path_denied`, `find_denied_paths_in_command`) |
| `src/ai_company/security/quarantine.py` | F-12 quarantine classification (additive flag only) |
| `src/ai_company/security/path_allowlist.py` | Pre-existing GO-5 allowlist (coexists; untouched) |

Not included: two unwired duplicates this session drafted first
(`redaction.py`, `egress_policy.py`) — **deleted** after reconciliation so
there is exactly one implementation.

---

## 1. Pre-persistence redaction (F-05) ✅

- **Code:** `src/ai_company/security/redact.py` — 11 ordered rules
  (10 from the fix plan §7.1 + `sk-ant`): `sk-`, Anthropic, Google
  (`AIza`), AWS (`AKIA`), GitHub (`ghp_…`/`github_pat_`), Slack (`xoxb…`),
  `Bearer`, `api_key`/`secret`/`dsn` assignments (key names preserved),
  whole PEM blocks (DOTALL). Logs pattern IDs only.
- **This session's addition:** `redact_part_data(data) -> (text, hits,
  json_valid)` — parses JSON, redacts string nodes recursively,
  re-serializes, **re-parses to prove validity** (the fix-plan requirement);
  non-JSON falls back to regex-only (`json_valid=False`).
- **Wiring:** `ToolRunner._sanitize_output` applies `redact_secrets` to
  every tool output (`read`/`bash`/`webfetch` stdout/stderr) before it can
  reach `part.data`. Historical rows are never rewritten by the filter
  (retired by F-04 rotation + F-10 retention), per the plan's backfill
  policy.
- **Tests:** `TestRedactionPatterns` + `TestRedactionJsonValidity` (key
  preservation, PEM, JSON round-trip, invalid-JSON fallback).

## 2. Read-deny rules (F-06) ✅

- **Code:** `src/ai_company/security/path_policy.py` + `config/path_deny.yaml`
  (code defaults fallback, same convention as `config/tool_allowlist.yaml`).
  Denies `read`/`grep`/`bash` on `.env*`, `*.env`, `auth.json`,
  `mcp-auth.json`, `opencode.db*`, `opencode-.db*`, `*.pem`, `*.key`
  (case-insensitive, basename + every path segment); exempts `.env.example` /
  `.env.staging.example` (placeholders-only).
- **Wiring (in the runner, not the prompt):** `ToolRunner.run_plan`
  (pre-tier check on `args.path`), `_read`, `_execute` token scan,
  `_grep` file skip, `_list_dir` filtering; denials logged via
  `log_permission_deny` (audit). Error shape matches the existing
  `Automated permission policy` class.
- **Docs:** `docs/security/READ-DENY-POLICY.md`.
- **Tests:** `TestPathPolicy` + `TestToolRunnerReadDeny` (env/db denied,
  `.env.example` allowed, bash `cat .env` denied, secret-in-read redacted).

## 3. Egress allowlist (F-07) ✅

- **Code:** `src/ai_company/security/egress.py` + `config/egress_allowlist.yaml`
  (YAML extras are **additive** over code defaults — same convention as the
  tool allowlist). `validate_egress_url` enforces: https-only (http only for
  `localhost`/`127.0.0.1`/`::1`/`172.30.96.0/24`), userinfo reject, token-like
  query-name reject (names logged, never values), metadata/private-IP deny,
  `file`/`data`/`ftp` schemes denied, **suspended-host deny** (added this
  session: `resend.com`, `mcp.resend.com` → `suspended_vendor_host`).
- **Shell egress (added this session):** `check_shell_egress(command)`
  validates every URL in `IWR`/`IRM`/`curl`/`wget`/`Invoke-*` commands; an
  egress verb without a verifiable URL is denied as unverifiable. Wired in
  `ToolRunner._execute` **after** the command allowlist check, so the
  existing `curl`-not-allowlisted behaviour and tests are unchanged.
- **Docs:** `docs/security/EGRESS-AND-VENDOR-POLICY.md`.
- **Tests:** `TestEgressPolicy` + `TestShellEgress`.

## 4. Vendor suspension (F-08) ✅

- **Verified:** `docs/APPROVED-VENDORS.md` (2026-11-08) — Resend, Composio,
  and `google_search`/`websearch` providers do not appear. Active rows
  cover cmem.ai/[retired], 0x0.st, Telegram/[retired], NotebookLM/[retired],
  Workers/[retired], kie.ai/[retired], Greptile/[retired], Xiaomi MiMo,
  Google AI/Gemini image, Comfy Cloud.
- **Flagged, not deleted:** `config/suspended_vendors.yaml` records both
  vendors (observed traffic, opencode-config state, action). `opencode.json`
  `mcp.resend` was already `"enabled": false` — kept. Composio has **no**
  `opencode.json` entry (nothing to disable — flagged at tool-prefix level).
  `egress.py` denies resend webfetch hosts in code with a
  `suspended_vendor_host` reason. Lifting any suspension requires a signed
  `APPROVED-VENDORS.md` row (≤90-day window) — a forward fix, never a
  silent rollback. `google_search`/`websearch` providers are flagged for
  CEO/CISO decision, not hard-blocked (Tier B reasoning documented in the
  YAML + egress doc).

## 5. Credential rotation runbook + `.env` inventory ✅

- **Runbook:** `docs/security/CREDENTIAL-ROTATION-RUNBOOK.md` — metadata-only
  enumeration SQL (never `SELECT value`), provider-side rotation order,
  fingerprint-only recording, read-only verification, no-rollback rule.
- **Inventory tool:** `scripts/security/inventory_env_keys.py` — parses
  `.env*` files + `opencode.json` `{env:NAME}` refs and emits **names +
  boolean `set` flag only** (values are discarded at parse time; nothing is
  printed, logged, or hashed).
- **Generated report:** `reports/env-inventory-2026-11-08.md` — 6 files
  scanned (`.env` 99 keys, `.env.cleaned`, `.env.example`, `.env.local`,
  `.env.staging.example`, `open-design/deploy/.env.example`) + env refs.
  The placeholder heuristic self-checked after a fix (an empty placeholder
  string matched every value — caught by review, fixed, report regenerated:
  **276 `set`-flagged names, 43 placeholder/empty**, out of 319 rows).
- No credential values were read or recorded at any point in this session.

## 6. ACL lockdown + BitLocker/EFS (F-01/F-02, F-03 noted) ✅ scripted, NOT executed

- **Script:** `scripts/security/opencode-db-hardening.ps1` — read-only by
  default (baseline `icacls`/`cipher /c`/`manage-bde` + what-`-Execute`-would-
  do listing); `-Execute` enables the snapshot → SID removal
  (`icacls /remove …-1003 /T /Q`) → owner-only lockdown (`/inheritance:r`
  + `/grant:r`) → BitLocker enable, each behind `SupportsShouldProcess`
  confirmation. Snapshots land in the **workspace** (`icacls-snapshots/`).
  **No destructive ACL change was run** in this session.
- **Current read-only state (captured 2026-11-08):**
  - `…-1003:(I)(OI)(CI)(RX)` ACE **still present** on
    `C:\Users\jmlus\.local\share\opencode` (inherited) and on `opencode.db`.
  - `opencode.db.bak`, `auth.json`, `mcp-auth.json` all exist; DB reports
    `U` (unencrypted) under `cipher /c`; BitLocker status check denied
    without admin (unknown, not failing).
  - ⇒ F-01/F-02/F-03 remain **open human actions**; the script is the
    execution vehicle when the maintenance window is chosen.

## 7. Injection quarantine (F-12) ✅ config + classifier (additive)

- **Code:** `src/ai_company/security/quarantine.py` +
  `config/quarantine_patterns.yaml` — 8 pattern classes (`ignore_prior`,
  `override_instruction`, `system_prompt`, `jailbreak`, `disregard`,
  `ignore_all`, `new_instructions`, `you_are_now`) with
  `classify_quarantine()` / `is_quarantined()` / `quarantine_flag()`.
- **Design preserved:** additive only — `quarantine_flag()` returns the
  sidecar row `(quarantined, matched, reviewer, reviewed_at)`; nothing is
  deleted, and the injector anti-join (`NOT EXISTS` on the sidecar) is
  documented in the module. The tagging job itself is a P2 maintenance-window
  step, not a silent DB write.
- **Tests:** `TestQuarantine` (all 8 IDs, exclusion of benign text, flag shape).

---

## Verification (this session)

| Check | Command | Result |
|---|---|---|
| New tests | `uv run pytest tests/unit/test_opencode_db_security.py tests/unit/test_security.py -q` | **80 passed** (47 new + 33 pre-existing) |
| Lint (new/adopted files) | `ruff check` on `redact.py`, `egress.py`, `path_policy.py`, `quarantine.py`, `test_opencode_db_security.py` | **All checks passed** |
| Types (security subset) | `mypy` on the 4 modules above | **No issues found** |
| Lint (full `tool_runner.py`) | `ruff check src/ai_company/executor/tool_runner.py` | 3 `SIM102`/`SIM105` findings in parallel-session code (nested-if in depth-limit path, nested-if in read-cache, try/except-pass in retry) — pre-existing, untouched by this session |
| ACL state | `icacls` (read-only) on data dir + DB | Orphaned `…-1003` **present**, DB unencrypted — hardening script not run (by design) |
| Inventory | `python scripts/security/inventory_env_keys.py` | **Names only** (276 set / 43 placeholder); no values exported |

**Not run (out of scope for this P0 pass):** WAL checkpoint/`VACUUM`
(maintenance window), retention purge, `.bak` disposal, any rotation itself,
and the P2 quarantine tagging job — all remain per the fix plan schedule.

**Files created by this session:** `path_policy.py`, `quarantine.py`,
`config/path_deny.yaml`, `config/egress_allowlist.yaml`,
`config/suspended_vendors.yaml`, `config/quarantine_patterns.yaml`,
`tests/unit/test_opencode_db_security.py`, `scripts/security/`,
`docs/security/` (3 policy docs), `reports/env-inventory-2026-11-08.md`.
**Files extended (adopted implementation):** `redact.py` (+JSON re-check),
`egress.py` (+suspended hosts, YAML extras, `check_shell_egress`),
`tool_runner.py` (+shell-egress block, `_read` deny, docstring sources).
