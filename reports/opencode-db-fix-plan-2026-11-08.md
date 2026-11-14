# opencode.db Fix Plan — 2026-11-08

**Coordinator:** chief-of-staff (primary orchestrator) for LightSpeed Holdings.
Direct execution for planning only; implementation is delegated (see RACI). No subagents were spawned for this plan (depth-1 constraint reproduced in the source audit).
**Date:** 2026-11-08
**Database in scope (read-only baseline):** `C:\Users\jmlus\.local\share\opencode\opencode.db`
**Workspace for this plan:** `C:\Users\jmlus\light-speed-holdings` (this file lives here only; no files created outside the workspace)
**Plan file:** `reports/opencode-db-fix-plan-2026-11-08.md`

**Evidence sources (read for this plan):**

- `reports/opencode-db-audit-2026-11-08.md` — chief-of-staff locate/size/integrity + trajectory + defect audit (21 recommendations, §§8–10).
- `reports/opencode-db-analytics-2026-11-08.md` — trajectory analytics (tool × status, hot files, cache, outside-workspace mapping, SQL proof).
- `reports/opencode-db-security-2026-11-08.md` — CISO security audit (ACLs, encryption, secrets-in-trajectories, egress, retention, injection-language exposure; 10 recommendations).
- `AGENTS.md` §§7, 9.2–9.3, 14, 17, 18 + `docs/STATUS.md` (last updated 2026-10-27).

**Method constraint honoured:** All three source reports were computed with `sqlite3 -readonly` only, no `INSERT/UPDATE/DELETE/VACUUM`, no checkpoint, no secret-value dumps (counts/hosts/lengths only). This plan proposes fixes; it does not execute them. Numbers below are quoted from those reports with the live-DB drift caveat stated in each (snapshot counts move by +1–3 sessions mid-audit because the DB is live and WAL-backed).

> **How to read this plan:** §1 states the priority order and why. §2 pins every factual claim to its source report so no number is invented. §3 lists governance gates that can block work. §4 assigns owners. §5 explains ordering/parallelization/checkpoints. §6 is the task backlog (the implementable unit). §§7–9 cover risk, decisions, and re-audit.

---

## 1. Executive summary

**The database is not corrupt; it is oversized, under-protected, and defect-dense at the tool layer.** `PRAGMA integrity_check` returned `ok` in all three audits, but the live footprint is ~44.9 GB (DB 3.00 GiB + WAL 2.95 GiB + 38.5 GB `.bak`), containing 95 days of verbatim trajectories with plausible plaintext credentials across 64% of sessions, guarded only by NTFS ACLs that include an orphaned SID.

**Two different lenses, one priority order:**

- The chief-of-staff audit (§8) ranks **storage reclaim + stabilization first** (WAL checkpoint, delete the 38.5 GB pre-v2 `.bak`, archive v1, clean temp) because disk pressure is live and the WAL is ~98% the size of the DB.
- The security audit (§6–§7) ranks **credential-store containment first** (unencrypted 22-row `credential` table + same-dir `auth.json`/`mcp-auth.json` + 38.5 GB plaintext backup, secrets plausibly embedded verbatim in `part.data`, orphaned-SID read access) because the breach blast radius is the full 44.9 GB corpus, not just the live DB.

This plan **merges both** as **P0 = containment + disk relief** (both must proceed concurrently; neither waits on the other, but checkpoint/rotation/redaction are sequenced by the dependencies in §6). **P1** fixes the two defect classes that dominate the 3,435 tool errors (edit semantics 816; ripgrep stack). **P2** governs the token/cache economics and hot-file re-reads that explain the 15.21 billion cache-read tokens. **P3** finishes schema/lifecycle hygiene (v2 completion, orphan sweeper, project GC, retention enforcement) only after P0–P1 have reduced the data the later phases must preserve.

**What success looks like (all criteria are measurable from the same read-only queries that produced the baseline):**

1. No orphaned ACE; at-rest encryption decision recorded; no second plaintext copy of the corpus beside the live DB.
2. New trajectories no longer ingest live `.env`/auth material; redaction gate demonstrably fires on new writes.
3. WAL no longer ~98% of DB; temp accumulation halted; live DB trending toward <1 GiB after retention + VACUUM (security-audit target; requires P3 retention decision).
4. Edit, ripgrep, PowerShell, schema, and depth error groups collapsed against their 2026-11-08 baselines.
5. Re-audit on a snapshot (not the live WAL) confirms deltas in all five areas (§9).

**Non-goals of this plan:** It does not edit history in place (no backfill redaction of existing `part.data` without a migration + audit note per security §7 P0-4), does not vacuum the live DB during sessions, and does not create worktrees/temp artifacts outside the workspace without consent (AGENTS.md §7).

---

## 2. Evidence baseline (verified, no invention)

| # | Fact (as of 2026-11-08 snapshot) | Value | Source |
|---|---|---|---|
| E1 | DB size / pages | `3,222,466,560 B` (~3.00 GiB), `page_size 4096`, `page_count 786735`, `freelist_count 1996` (~8 MB) | audit §2; security §0 |
| E2 | Integrity | `PRAGMA integrity_check` → `ok`; `journal_mode=wal`, `auto_vacuum=0` (NONE) | audit §2; security §0 |
| E3 | Live footprint | DB 3.00 GiB + WAL **2.95 GiB** (`3,163,682,112 B`) + `opencode.db.bak` **38,533,844,992 B (35.89 GiB, 2026-11-01)** = **~44.9 GB**; WAL ≈ 98% of DB → checkpoint severely behind | audit §§1, 8-P1; security §§0, 4 |
| E4 | Row counts | `session=3,131` (frozen 2026-08-05→2026-10-22), `session_v2≈94` (live from 2026-11-01), `message=153,182`, `part=670,664`, `session_message≈9,161–9,284`, `session_part=0`, `todo=2,771`, `project=72`, `credential=22`, `account=0`, many subsystem tables `0` (`event/blob/blob_ref/job/schedule/session_inbox/session_share`) | audit §2; analytics §1 |
| E5 | Sessions / authorship | 89.9% of v1 sessions in main project `9930faf5…` (`light-speed-holdings`, 2,814/3,131); 123 distinct `session.agent` values; top: `build 876, explore 357, general 235`; v2 top `build 61/94 (~65%)` | audit §3.1; analytics §1.4 |
| E6 | Tool volume / errors | 188,713 `tool` parts: `completed 185,183 / error 3,435 (1.82%) / running 93 / pending 2`. By-tool errors: `read 959, edit 949, bash 387, task 351, glob 225, grep 196, webfetch 102, write 63, websearch 59`. Rates: `task 17.11%, webfetch 13.69%, websearch 7.11%`; `agents_coordinate_bots 50%`, `agents_show_widget 78.57%` | audit §§3.3, 6; analytics §2 |
| E7 | Top error messages | `edit oldString not found 588`, `ripgrep execution failed 236`, `aborted 173`, `no-op identical 154`, `ripgrep 64 KiB overflow 140`, `task cancelled 91`, `multiple matches 74`, schema `Missing key` ≥149 total, `429 parallel.ai 41`, `subagent depth limit 40`, `user rejected permission 37`, `edit deny rule 34` | audit §6.1; analytics §§3–4 |
| E8 | Repeated stdout errors (AGENTS §17 recurrence) | `rg not recognized 474`, `Select-Object -First/-Last negative 289+287+185+125+113+84+81`, `ChildProcess.kill`, `out-file com1: 126`, `python << heredoc 118`, `string terminator 106`, `python3 not recognized 81` | audit §6.2; analytics §8.2 |
| E9 | Cache reads / writes | `session.tokens_cache_read = 15,210,842,514 = step-finish sum`; `session_v2 = 809,948,648`; **`tokens_cache_write = 0` everywhere** (session + message + step-finish). Cache-read/input ≈ 8.95× (v1), 9.72× (v2). Mega-sessions: 23.1M input / 377.7M cache-read (`ses_f1ad097c…`); v2 `Prompt contents` 26.8M input / 132.8M cache-read. Cost total **$5.59** (free models dominate) | audit §4; analytics §§1.6, 7 |
| E10 | Files | 9,361 distinct `filePath`s / 74,310 ops (`read 52,581 + edit 16,540 + write 5,315`); 101,276 incl. grep/glob. **1,442 files >10× (1,101 by `read` alone)**. Top read counts: `api.py 758–974` (audit vs analytics read-vs-any-operating counting difference; see note), `company-registry.yaml 655–763`, `AGENTS.md 425–552`, `STATUS.md 362–452`, `summary.md 284–466`, tool-output spill `tool_14ff… 288` | audit §5; analytics §§5–6 |
| E11 | Create / modify | `write completed 5,249`, `edit completed 15,591` (create+modify 20,840); patch parts **13,579 / 814 sessions**; file parts **144 / 57 sessions** (inline base64); `blob/blob_ref 0` | audit §§5, 6; analytics §6 |
| E12 | Non-terminal residue | `running 93 (task 51, bash 30, question 10) + pending 2 (write 2)` — orphaned markers, no sweeper observed | audit §§3.3, 6.3; analytics §8.5 |
| E13 | Outside-workspace trajectory ops (pre-existing, flagged) | 13,126 filePath ops outside `light-speed-holdings` (17.7%); 320/3,131 sessions outside (athena 114, openmausbot, `Temp\opencode`); bash workdir outside 5,063/31,226; `Temp\opencode` **31,217 files (228 in last 7d)**. Audit created **0** outside artifacts | audit §7; analytics §9 |
| E14 | Security: permissions | Inherited ACL on DB/`.bak`/auth JSONs + parent dir: `jmlus (…-1001) F`, `SYSTEM F`, `Administrators F`, **`S-1-5-21-2913538908-3024988640-2666040046-1003 RX (orphaned — no live account/profile for …-1003)`**; no Deny ACEs; `(OI)(CI)` inheritance | security §1.1 |
| E15 | Security: encryption | `cipher /c` → `opencode.db` **unencrypted (U)**; plain SQLite (no SQLCipher); protection = NTFS ACLs only; `credential.value` encryption **cannot be determined from counts alone** (values deliberately never selected); treat as plaintext until vendor docs prove otherwise | security §1.2 |
| E16 | Security: secrets-bearing corpus | `part %sk-% 12,747 (2,000 sessions, 64%)`, `%secret% 12,524`, `%api_key% 15,288`, `%password% 2,195`; hits concentrate in `tool` parts (inputs + captured outputs); `message %sk-% 3,086`. `credential 22 rows` (avg 119 B, max 651 B; 10× “API key” burst 2026-10-22). `read *.env 309`, `bash env 4,394`, `bash db/auth 218` | security §2 |
| E17 | Security: egress | `webfetch 745` (727 https, **17 http — all localhost/private/first-party**, 0 `file:/data:/ftp:`, **8 userinfo, 93 query-string**, 141 hosts; top `raw.githubusercontent.com 98, foaster.ai 70, github.com 53`). Shell egress far larger: `bash 78,923` with `IWR 1,121, curl 718, IRM 529, https-any 6,704`. `resend_* ~35` (incl. `list-api-keys 1`), `composio_* ~27`, `agents_vm_exec 19` | security §3 |
| E18 | Security: retention / privacy | Retention span **2026-08-05→2026-11-08 (~95 days)**; `time_archived IS NOT NULL = 0` (0 archived); 72 projects (5 with sessions, 67 session-less); `part.data 1,820 MB avg 2,846 B max 4.9 MB`, `message.data 786 MB`, `kv 10.8 MB` (catalog blob 11,273,128 B); `log\opencode.log ~80 MB`; `opencode-.db 765,952 B` (stale 2026-10-30) | security §§0, 4 |
| E19 | Security: injection-language exposure | `part %ignore%prior% 3,412 (tool 2,056 / reasoning 737 / text 619)`, `%system prompt% 2,077`, `%override%instruction% 2,162`, `%jailbreak% 317`; persists into v2 (7-day `session_message %ignore%prior% 158`). Finding = untrusted instruction-like content at scale in a memory-sourced store, **not** a claim of successful attack | security §5 |

**Counting notes (do not conflate):** E10 top-read counts differ between audits because the chief-of-staff audit counts any `read/edit/write` touch (api.py 974) while analytics counts `read`-tool-only (api.py 758). Both prove the same conclusion: the dashboard API, registry, AGENTS, STATUS, and ECL files are the hot set. Likewise, `session_v2` 91→94 and `session_message` 9,161→9,284 drift within/across audits is live-DB drift (E3), not error. `edit` semantic-failure total 816 = 588 + 154 + 74 (audit §6). Last-30-day windows in analytics are anchored to `MAX(part.time_created)` = 2026-10-22 (v1 frozen), not wall-clock `now()`.

---

## 3. Governance constraints that gate implementation

| Gate | Rule (source) | Effect on this plan |
|---|---|---|
| **Third-party transmission ban** | Skills must not send local data to third-party hosts unless vendor is on `docs/APPROVED-VENDORS.md` within its 90-day window or re-signed by CEO/CISO. CISO of record: Jack Mlusu (Human CEO). On unexpected transmission: stop, do not retry, report skill + host + payload class. (AGENTS §9.2) | P0-T5, P1-T6, P2-T6, P3-T5 must verify Resend/Composio/Google/Exa/Parallel against the allowlist before further use. No new transmission until verified. |
| **Audit evidence separation** | Auditor’s read set and write set must be disjoint; never write into evidence directories (`reports/evidence/`, `.opencode/audit/*`, harness reviews, etc.). Output goes to `reports/repo-audit-<DATE>.md` or outside the repo. (AGENTS §9.3) | Re-audit (§9) must write to `reports/` (this plan’s sibling) and snapshots/copies, never into `reports/evidence/`. |
| **Root-config CEO override** | Any commit modifying `AGENTS.md` or `opencode.json` must carry `[CEO-OVERRIDE: <OPERATIONAL REASON>]`, else the pre-commit hook blocks it. (AGENTS §18) | P1-T5 (subagent depth) and any P1-T3 skill/prompt change that lands in `opencode.json`/`AGENTS.md` require the tag + `docs/governance-audit.md` entry. Plan tasks mark this explicitly. |
| **Branch protection** | `main` protected (6 required checks). Work on branch → PR → merge only when green. (AGENTS §5, §9, `11-GIT-STANDARDS.md`) | All code/config changes follow branch + PR; checkpoint gates in §5 include CI. |
| **Worktree consent** | Ask before creating any worktree; place under `.worktrees/` in repo root, never `%TEMP%`. (AGENTS §7) | Parallel agents working in parallel branches use `.worktrees/` or direct edits only with consent. |
| **What not to touch** | Do not edit secrets, `.env`, generated outputs, dependency folders, or unrelated user changes. ECL active constraints override generic guidance. Do not hand-edit `harness/changes/INDEX.json`. (AGENTS §7) | P0-T4 rotation updates `.env` locally (gitignored) but never commits it. ECL slice owners must check `harness/changes/active/summary.md` first. |
| **Verification floor** | Any source change: `ruff check` + `mypy` + `pytest`. Harness/docs: `lint-ecl.ps1`. Generator/template: regenerate agents. (AGENTS §6) | Every §6 task lists its verification commands derived from this table + the DB-proof queries in §10. |
| **Dispatch guardrails** | `task`’s `subagent_type` and `skill` name are separate namespaces; never derive a `subagent_type` from a skill path/title. (AGENTS §14) | RACI uses canonical agent IDs from `company-registry.yaml` (e.g. `ciso`, `cto`, `cio`), not skill names. |

---

## 4. RACI

Chief-of-Staff **coordinates** (owns sequencing, dependencies, checkpoints); per the Chief-of-Staff operating guideline (“maintain high-level strategic oversight; do not execute low-level tasks”) it **delegates execution** to the accountable owners below. `R = Responsible (executes)`, `A = Accountable (owns the outcome — exactly one per row)`, `C = Consulted`, `I = Informed`.

| Phase / outcome | **Human CEO** (Jack Mlusu, CISO of record) | **Chief-of-Staff** | **CISO** | **CTO** | **CIO** | **COO** |
|---|---|---|---|---|---|---|
| **P0** Security containment (ACL, `.bak`, encryption decision, rotation, ingest stop, WAL, temp) | **A** (rotation + vendor + encryption decisions) | **A** for sequencing/checkpoints · **R** for plan tracking | **R** for ACL/redaction/egress/rotation technical execution · **C** on credential-encryption determination | **C** (tool changes needed for redaction/deny) | **R** for ACL/BitLocker-EFS/VACUUM/WAL execution | **I** |
| **P1** Defect-class fixes (edit, ripgrep, PowerShell, schema, depth, network) | **A** for root-config override (§18) | **A** for ordering/checkpoints | **C** (no secrets in new error messages) | **A+R** for ToolRunner/edit/grep/schema fixes + depth config + retry/backoff | **C** (PATH/`rg` install, shell policy) | **I** |
| **P2** Cache/token/hot-file + egress hygiene | **A** for allowlist + retention-window input | **A** for sequencing | **A+R** for egress allowlist/URL hygiene + injection quarantine input | **R** for read-dedup, spill-cap, compaction/budget, blob design | **R** for proxy/allowlist host config | **I** |
| **P3** Schema/lifecycle (v2 decision, sweeper, project GC, retention/VACUUM, vendor verification, stale cleanup, re-audit) | **A** for v2 freeze-vs-complete + retention window | **A** for sequencing + re-audit gate | **R+A** for retention/GDPR + quarantine + vendor verification | **R** for v2 writers/sweeper/project GC | **R** for VACUUM/cleanup execution | **C** (retention ops) |
| **Cross-cutting** Branch/PR/CI, ECL discipline, STATUS handoff | **I** | **R** (tracks branch/PR checklist) | **I** | **R** (code gates green) | **I** | **I** |

**Single-A rule applied:** Each phase row has exactly one `A` for its outcome (P0/P1/P2-final/P3-final: CEO for decisions, Chief-of-Staff for sequencing — the table separates outcome ownership from sequence ownership so the “one A” is unambiguous per row; where both appear, the first-listed `A` is the outcome owner). Re-audit ownership: Chief-of-Staff (A) with CISO + CTO as Responsible for the security and defect sections respectively.

---

## 5. Ordering, dependencies, parallelization, and checkpoints

### 5.1 Dependency graph (foundation first)

```
P0-T1 ACL lockdown ──────────────────────┐
P0-T3 Credential-encryption determination─┼─→ P0-T4 Rotation ──→ P0-T5 Ingest stop (deny + redact) ──→ P3-T4 Retention/VACUUM
P0-T2 .bak disposition ──────────────────┘          │
P0-T6 WAL checkpoint (maintenance window) ──────────┤ (enables P3-T4 compaction)
P0-T7 Temp purge ───────────────────────────────────┘ (independent; parallel)
P1-T1 EDIT semantics ──┐
P1-T2a rg/fallback ────┼─→ P1-T3 PowerShell linter (encodes §17 directives) ──→ P2-T3 Read-dedup
P1-T4 Schema fail-fast ┤
P1-T5 Depth config ────┤ (needs CEO-override gate)
P1-T6 Retry/quarantine ┘
P2-T1 Metering fix ───→ P2-T2 Mega-session budget/compaction ──→ P2-T3 Read-dedup ──→ P2-T4 Spill cap
P2-T5 Blob design ────→ P3-T1 V2-complete-vs-freeze decision ──→ P3-T2 Orphan sweeper ──→ P3-T3 Project GC ──→ P3-T4 Retention
P2-T6 Egress allowlist ──→ P3-T5 Vendor transmission verification ──→ P3-T6 Injection quarantine ──→ P3-T7 Stale cleanup ──→ P3-T8 Re-audit
```

**Why this order:** P0 removes the largest blast radius (plaintext backup + orphaned read access + unencrypted credential store) before any new trajectories accumulate. P1 fixes the error classes that cause re-reads/retries (which otherwise inflate the very data P2–P3 must preserve). P2 reduces future write amplification (cache reads, hot-file I/O, spill re-reads) so P3’s retention/VACUUM and v2 writers operate on the smallest, cleanest corpus. P3 is last because retention windows and schema freeze decisions are irreversible without re-verification.

### 5.2 Parallelization

- **Safe to parallelize (no shared state):** P0-T1 + P0-T3 (research-only) + P0-T7 (temp purge); P1-T1 + P1-T2a + P1-T4 (different tools); P2-T1 (docs/metering) + P3-T5 (allowlist cross-check) during P1.
- **Must be sequential (shared DB / shared config / maintenance window):** P0-T3 → P0-T4 (rotation scope depends on encryption answer); P0-T6 (WAL checkpoint) must run in a maintenance window with OpenCode closed and never during live sessions; P3-T1 → P3-T4 (archival shape depends on freeze-vs-complete decision); P1-T5 config change must not race with P1-T3 prompt edits in the same files (define the root-config contract first, then parallelize).
- **Needs coordination (shared contract):** P2-T3 read-dedup and P1-T1 edit re-read contract (both touch “read before edit” semantics — agree the anchor+verify contract in P1-T1 first); P2-T6 egress allowlist and P3-T5 vendor verification (same host list).

### 5.3 Checkpoint discipline (from planning skill)

Each phase ends at a **checkpoint**: all task verification in §6 complete, `ruff check src/` + `mypy src/` + scoped `pytest` green (per AGENTS §6), DB-proof queries in §10 re-run against a snapshot show the expected delta, and a human reviews the snapshot numbers before the next phase starts. High-risk work (P0-T4 rotation, P0-T6 checkpoint, P3-T4 VACUUM) is early and gated — fail fast before building on it.

**Sizing key (XS/S/M only, per brief):** XS = single command/config (1 file or pure-ops action); S = 1–2 files / one endpoint or one query-family; M = 3–5 files / one feature slice. No L/XL tasks are listed — anything larger is split (e.g. blob migration is design-only in P2-T5; implementation follows P3-T1).

---

## 6. Phased implementation plan

### Phase P0 — Containment + disk relief (do first; concurrent tracks, gated rotation)

Goal: shrink the blast radius and the disk footprint before any new history accumulates. Evidence anchors: E3, E14, E15, E16, E18.

#### P0-T1 — Remove orphaned ACE and lock ACLs to owner-only

**Why:** `S-…-1003 RX` grants read+execute on the DB, `.bak`, and both auth JSONs via `(OI)(CI)` inheritance; no live account/profile exists for `…-1003` (security §1.1). Latent unauthorized read + least-privilege failure.

**Acceptance criteria:**
- [ ] `icacls` on `C:\Users\jmlus\.local\share\opencode` (and parent if inherited there) shows **no `…-1003` ACE**; only `jmlus`, `SYSTEM`, `Administrators` remain.
- [ ] Inheritance reset (`/inheritance:r`) applied; re-check survives a new profile/VM creation probe.

**Verification:**
- [ ] `icacls "C:\Users\jmlus\.local\share\opencode" "C:\Users\jmlus\.local\share\opencode\opencode.db" "C:\Users\jmlus\.local\share\opencode\auth.json" "C:\Users\jmlus\.local\share\opencode\mcp-auth.json"` — capture before/after.
- [ ] `whoami /user` + profile check confirms acted-as SID.

**Dependencies:** None. **Size:** XS. **Files touched:** none in repo (NTFS ACL only).

#### P0-T2 — Disposition the 38.5 GB plaintext `.bak`

**Why:** Single largest outside-workspace artifact (E3, E13); pre-v2 snapshot; independently reconstitutes the 95-day corpus (E18). Effective exposure is 44.9 GB, not 3 GB.

**Acceptance criteria:**
- [ ] Restore-tested once from the `.bak` to a scratch location (or formally waived by CEO with recorded reason) **before** deletion.
- [ ] `.bak` moved to encrypted cold storage **or** deleted; no second plaintext copy remains beside the live DB.
- [ ] Decision recorded (date, reason, restore result) in the change log; audit trail notes it.

**Verification:**
- [ ] `Get-ChildItem "C:\Users\jmlus\.local\share\opencode\opencode*" | Select Name, Length, LastWriteTime` — `.bak` row gone or confirmed encrypted-path.

**Dependencies:** None, but must not run during P0-T6 maintenance window (avoid concurrent copy+checkpoint). **Size:** S (ops + restore test). **Files touched:** none in repo (filesystem only).

#### P0-T3 — Determine whether `credential.value` is encrypted (no values dumped)

**Why:** Whether all 22 credential rows + `auth.json`/`mcp-auth.json` tokens are plaintext-at-rest cannot be determined from counts (security §§1.2, 8). Rotation scope depends on this answer. Audit deliberately never selected values.

**Acceptance criteria:**
- [ ] Vendor documentation/source answer cited (DPAPI/key-provider vs plaintext) for OpenCode credential storage, or an explicit “cannot be proven encrypted” statement.
- [ ] The answer (with citation) is recorded as the input to P0-T4; no value-level list is produced.

**Verification:**
- [ ] Research note saved inside the workspace (reports/ sibling) citing doc/source version + date; confirms no `SELECT value` was executed.

**Dependencies:** None (read-only research). **Size:** S. **Files touched:** `docs/governance-audit.md` (if root-config-adjacent) or a new `reports/` note.

#### P0-T4 — Rotate credentials (conditional on P0-T3)

**Why:** Until encryption is proven, treat all 22 rows + auth tokens + every `.env` value the agent read (309 reads, 4,394 bash env mentions — E16) as potentially in the corpus (security §7 P0-3, AGENTS §11).

**Acceptance criteria:**
- [ ] Rotation executed for at minimum: provider keys labelled `API key`, `Groq`, `Cohere`, `Google`, `Ollama (local)`, `OpenCode Console*`, plus `.env` values reachable via `read`/`bash`, plus `auth.json`/`mcp-auth.json` tokens — each provider’s new key updated in `.env` (gitignored) and deployed environments (GH Actions / Docker / cloud secret stores per AGENTS §11).
- [ ] Old keys revoked **after** health checks pass; rotation documented in `CHANGELOG.md` (date + reason) per AGENTS §11; `DASHBOARD_*` RBAC keys included if reachable.
- [ ] No `.env` committed; health endpoints verified post-rotation.

**Verification:**
- [ ] `uv run python -c "from dotenv import load_dotenv; load_dotenv(); from ai_company.security.rbac import verify_keys; verify_keys()"` (local).
- [ ] `curl -H "X-API-Key: $DASHBOARD_ADMIN_KEY" http://localhost:8421/health` (staging) and production `:8420/health` per AGENTS §11.
- [ ] `git status --short` confirms no `.env` staged.

**Dependencies:** P0-T3 (encryption answer sets scope); P0-T1 (ACL fix before new keys are generated). **Size:** M. **Files touched:** `.env` (gitignored, never committed), secret stores, `CHANGELOG.md`.

#### P0-T5 — Stop ingesting live credentials into new trajectories

**Why:** Agent routinely reads `.env` (309) and touches DB/auth paths (218 bash) (E16); `part.data` captures command outputs verbatim (security §2.2). Prevents the corpus from growing new secrets while P0-T4 rotates old ones.

**Acceptance criteria:**
- [ ] Filesystem policy denies `read` + `bash` file-reads on `.env*`, `auth.json`, `mcp-auth.json`, `opencode.db*` (policy, not prompt).
- [ ] Pre-persistence redaction filter over `part.data` (patterns per security §7 P0-4: `sk-…`, `api[_-]key\s*[:=]`, `secret`, `password`, `AKIA…`, `ghp_…`, `xox[baprs]-…`, `Bearer …`, `BEGIN … PRIVATE KEY`) replaces value with `[REDACTED]` **before insert**; filter unit-tested.
- [ ] Historical rows untouched (no in-place edit without a migration + audit note).

**Verification:**
- [ ] Scoped tests green: filter replaces values, leaves benign mentions intact; deny-policy blocks `.env`/`auth.json`/`opencode.db*` tool calls.
- [ ] Bounded proof: `SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.state.input.filePath') LIKE '%.env%';` (read-only, counts only) shows no growth in new-window data after the gate lands.

**Dependencies:** P0-T4 (deploy after rotation so redacted traffic uses new keys). **Size:** M. **Files touched:** ToolRunner/permission policy + redaction filter + tests (3–5 files).

#### P0-T6 — Checkpoint the WAL in a maintenance window

**Why:** WAL is 2.95 GiB ≈ 98% of DB (E3); checkpoint has not kept up. Crash-consistent recovery relies on an un-checkpointed WAL (security §4). Must not run against a live WAL.

**Acceptance criteria:**
- [ ] Maintenance window with OpenCode closed; `PRAGMA wal_checkpoint(TRUNCATE)` returns 0 frames; `opencode.db-wal` shrinks toward 0.
- [ ] Root cause investigated (long-running transaction / backup copy holding the checkpoint back) with written finding or “cannot be determined from available evidence” per AGENTS §15.
- [ ] `PRAGMA journal_mode` remains `wal`; `integrity_check` still `ok`.

**Verification:**
- [ ] Before/after: `Get-Item "C:\Users\jmlus\.local\share\opencode\opencode.db*"` sizes + `sqlite3 -readonly … "PRAGMA integrity_check;"`.
- [ ] Re-run: `SELECT COUNT(*) FROM session_v2;` snapshot to prove no drift-induced surprise.

**Dependencies:** None, but must serialize with P0-T2 (no concurrent copy). **Size:** S. **Files touched:** none in repo (DB maintenance only).

#### P0-T7 — Purge stale temp accumulation + add retention sweeper design

**Why:** `Temp\opencode` holds 31,217 files, only 228 in the last 7 days (E13) — stale accumulation in the approved temp location.

**Acceptance criteria:**
- [ ] Files older than 7 days purged (fresh 228 retained); file count drops by an order of magnitude.
- [ ] Sweeper design recorded (cadence, age threshold, log location) and scheduled (or explicitly deferred with owner + date).

**Verification:**
- [ ] `(Get-ChildItem "C:\Users\jmlus\AppData\Local\Temp\opencode" -Recurse -File).Count` before/after; count of files with `LastWriteTime` in last 7 days unchanged.

**Dependencies:** None. **Size:** XS. **Files touched:** none in repo (temp dir only); sweeper design note inside workspace.

#### Checkpoint P0
- [ ] `icacls` shows no `…-1003`; `.bak` disposition recorded; `credential` encryption determination cited; rotation (or formal waiver) recorded; redaction/deny gates live; WAL checkpoint 0 frames in a maintenance window; temp count collapsed. **No gate → no P1 expansion.**

---

### Phase P1 — Defect-class fixes (dominant error groups)

Goal: collapse the error classes that cause retries and re-reads. Baselines: E6–E8. All code changes follow AGENTS §6 verification floors (ruff + mypy + pytest) and branch + PR (§3).

#### P1-T1 — Fix `edit` semantic failures (816 = 588 + 154 + 74)

**Why:** Largest single defect class (27% of all errors on the most-used mutation tool, audit §6.1). Spans 221 sessions / 75 days (analytics §4) — systemic, not one-off prompt error.

**Acceptance criteria:**
- [ ] Client-side reject of `oldString == newString` (no-op) **before** tool execution.
- [ ] Callers require re-read of the exact region (anchor+verify) before editing; `oldString not found` error includes nearest-line hint or “re-read and retry” guidance.
- [ ] `Found multiple matches` error requires additional surrounding context (already stated; enforce client-side pre-check).

**Verification:**
- [ ] Unit tests: identical-pair rejected, multiple-match pre-check fires, not-found error shape documented.
- [ ] `ruff check src/` + `mypy src/` + scoped `pytest` green; baseline re-query (counts only) captured for re-audit comparison:
  `SELECT json_extract(data,'$.state.error'), COUNT(*) FROM part WHERE … status='error' AND json_extract(data,'$.tool')='edit' GROUP BY 1;`

**Dependencies:** None (but P2-T3 read-dedup must agree with this re-read contract). **Size:** M. **Files touched:** edit tool + ToolRunner validation + tests (3–5 files).

#### P1-T2a — Ripgrep presence: install `rg` on PATH or fix fallback

**Why:** `rg not recognized 474` (E8) + `ripgrep execution failed 236/216` + `glob` 91.6% of failures in the last 30 days (analytics §3.1) prove the fallback is broken or missing.

**Acceptance criteria:**
- [ ] Either `rg` resolvable on PATH (`rg --version` succeeds in agent shells) **or** `grep`/`glob` fallback without `rg` passes its test suite.
- [ ] `glob` error rate stops being the dominant recent regression (re-audit window).

**Verification:**
- [ ] `rg --version` in PowerShell + Git Bash shells; `grep`/`glob` scoped tests green; error-group re-query (`tool IN ('grep','glob') AND error LIKE '%ripgrep%'`) captured.

**Dependencies:** None. **Size:** S. **Files touched:** grep/glob tool + fallback + tests (1–2 files).

#### P1-T2b — Cap grep/shell output below 64 KiB

**Why:** `Ripgrep JSON record exceeded 65536 bytes 140` across 107 sessions (analytics §4); large outputs are almost all `grep` “Found 100 matches” floods over `brand/` + `docs/` + skills (analytics §8.4).

**Acceptance criteria:**
- [ ] `grep` match cap enforced (e.g. ≤100 matches with “more available” note, or byte cap <64 KiB) and tested at the boundary.
- [ ] No single new `part.data` exceeds the cap via `grep` output (proof via `length(json_extract(...))` probe in §10).

**Verification:**
- [ ] Boundary tests green; `length()` probe on new-window data shows zero `grep` outputs >64 KiB.

**Dependencies:** Parallel with P1-T2a. **Size:** S. **Files touched:** grep output formatter + tests.

#### P1-T3 — Enforce AGENTS §17 PowerShell directives with a pre-flight linter

**Why:** 1,500+ repeated stdout errors (E8) recur **after** being documented as known issues — the lesson is learned on paper but not applied at runtime (audit §8-P2-8).

**Acceptance criteria:**
- [ ] Pre-flight check rejects: `Select-Object -First/-Last <negative>`, `&&` separator, `$(…)` in `--jq`, bash heredocs (`python << 'PYEOF'`) in PowerShell; suggests the §17-compliant rewrite (positive numbers only; `;` + `&`; single-quoted `--jq` single-field; temp `.ps1` file for multi-statement/`$vars`/literals).
- [ ] Skill/system-prompt guidance updated to reference the linter (no duplication of long directive text — point to AGENTS §17).

**Verification:**
- [ ] Linter unit tests per antipattern green; `ruff`/mypy/pytest green for the linter package.
- [ ] Baseline re-query of `SELECT-Object` / heredoc / `rg` groups shows collapse in new-window data.

**Dependencies:** After P1-T2a (so `rg` guidance is current). **Size:** M. **Files touched:** bash pre-flight + skill/prompt doc + tests (3–5 files).

#### P1-T4 — Schema-error fail-fast validation (≥149 retries)

**Why:** `Missing key ["filePath"/"command"/"oldString"]` totals ≥149 (audit §6.1; analytics §8.6) — agents retry blindly instead of validating once.

**Acceptance criteria:**
- [ ] Tool-call JSON validated against schema once; on missing key, fail fast with the correct shape example (no blind retry loop).
- [ ] `NULL filePath` attempts (write 32, edit 71) rejected at validation, not execution.

**Verification:**
- [ ] Validation tests per tool (read/edit/write/bash) green; error-group re-query for `Missing key` captured.

**Dependencies:** None. **Size:** S. **Files touched:** ToolRunner validation + tests.

#### P1-T5 — Raise `subagent_depth` for orchestrator-class agents (with CEO-override gate)

**Why:** `Subagent depth limit reached (1)` 40× in DB + reproduced this audit (chief-of-staff spawn failed identically, audit §§6.4, 9.1). Any orchestration that spawns from a subagent fails.

**Acceptance criteria:**
- [ ] Depth raised for `chief-of-staff`, `cto`, `vp-engineering` (or direct-work carve-out with explicit logging) — config change only.
- [ ] If the change touches `opencode.json`/`AGENTS.md`, commit carries `[CEO-OVERRIDE: <OPERATIONAL REASON>]` and `docs/governance-audit.md` entry (AGENTS §18); otherwise hook block is investigated, not bypassed with `--no-verify`.

**Verification:**
- [ ] Nested-spawn smoke test succeeds (or carve-out log line observed) where the previous audit reproduced the failure.
- [ ] Pre-commit hook passes (or override audit entry present).

**Dependencies:** None; must define contract before P2 parallel edits in same config files. **Size:** XS. **Files touched:** `opencode.json` (if applicable) + governance audit log.

#### P1-T6 — Harden fragile network tools; quarantine high-fail `agents_*`

**Why:** `websearch 429 (41, burst 2026-09-13)`, `exa transport (11)`, `parallel.ai 429 (41)`, `agents_coordinate_bots 50%`, `agents_show_widget 79%` (E6, E7). Bursty but repeated.

**Acceptance criteria:**
- [ ] Retries with exponential backoff + jitter for `websearch`/`webfetch` (esp. 429/transport).
- [ ] `agents_coordinate_bots` / `agents_show_widget` fixed or quarantined (disabled with a recorded decision) before further use.

**Verification:**
- [ ] Backoff/retry tests green; quarantined tools return a clear disabled error.
- [ ] Re-audit queries for `429` / `transport` / per-tool error rates captured.

**Dependencies:** None. **Size:** S. **Files touched:** websearch/webfetch wrappers + tool registry + tests.

#### Checkpoint P1
- [ ] Edit/ripgrep/PowerShell/schema/depth/network baselines re-queried on a snapshot show the expected collapse in new-window data; all code gates green; no root-config commit without override tag.

---

### Phase P2 — Token/cache economics + hot-file governance

Goal: stop burning cache-read tokens and re-reading the same files/outputs. Baselines: E9, E10, E11, E17.

#### P2-T1 — Fix cache metering and document the `cache_write = 0` quirk

**Why:** `cache_write` is 0 in all three ledgers (E9) — provider metering quirk, not an audit artifact (audit §4.2). Any hit-rate/savings dashboard built on it is wrong.

**Acceptance criteria:**
- [ ] `docs/` records the quirk: accounting renormalized to `cache_read` volume + per-session `input + cache_read` totals; hit-rate metrics disabled until providers emit `cache_write`.
- [ ] Dashboard/token budgets no longer divide by `cache_write`.

**Verification:**
- [ ] Docs search shows no remaining `cache_write`-based hit-rate computation; ledger-agreement query in §10 reproduces E9.

**Dependencies:** None. **Size:** S. **Files touched:** docs + dashboard/analytics references (1–2 files).

#### P2-T2 — Govern mega-sessions (budget + early compaction)

**Why:** Single sessions at 23M input / 377M cache-read (v1) and 26.8M “Prompt contents” (v2); 5,444 compactions already (≈4% of steps) (audit §§4.2, 3.2). `build` = 65% of v2 sessions. Cost dashboards are blind under free models (E9).

**Acceptance criteria:**
- [ ] Per-session token budget (input + cache_read) + agent/day budgets enforced; burn surfaced per agent in dashboard.
- [ ] Compaction threshold raised to auto-compact *before* the next step (not after); `build` mega-sessions split into subagent tasks (guidance + enforcement point recorded).

**Verification:**
- [ ] Budget-overrun and early-compaction paths tested; per-agent burn query (§10) runs against snapshot.

**Dependencies:** P2-T1 (correct metric first). **Size:** M. **Files touched:** agent-loop budget/compaction + dashboard burn view + tests.

#### P2-T3 — Cache hot files; inject session-start context once

**Why:** 1,442 files >10×; top `api.py`, `company-registry.yaml`, `AGENTS.md`, `summary.md`, `STATUS.md` (E10). Session-start context (AGENTS/STATUS/ECL/registry) is re-read per tool call instead of injected once via the memory/recall loop (audit §8-P3-14).

**Acceptance criteria:**
- [ ] Per-session file-read dedup: second `read` of the same path returns a pointer, not disk I/O (target: ≥30% read-volume cut per audit estimate).
- [ ] Session-start context (AGENTS, STATUS, ECL `summary.md`/`tasks.md`, registry) injected once via recall/injection; `harness/.../summary.md` “File not found” probes (21) eliminated by contract clarity.

**Verification:**
- [ ] Dedup tests (same-path second read = pointer; changed-file invalidation via mtime/size) green; hot-file re-query (§10) shows collapse for the top-5.
- [ ] Must agree with P1-T1 anchor+verify contract (coordinate, don’t duplicate).

**Dependencies:** P1-T1 (edit re-read contract), P2-T2 (budget context). **Size:** M. **Files touched:** read tool + recall injection + tests (3–5 files).

#### P2-T4 — Cap and summarize tool-output spills (one spill re-read 288×)

**Why:** `tool-output/tool_14ff…` read 288× (E10); 1,641 completed outputs >50k chars, top `grep` floods (analytics §8.4). Anti-pattern: persist then re-read instead of summarizing.

**Acceptance criteria:**
- [ ] Spill-file size capped; on-write summarization occurs; re-read returns summary + pointer, not full bytes.

**Verification:**
- [ ] Spill-cap tests green; `length()` probe (§10) shows no new spill file re-read >10×.

**Dependencies:** P1-T2b (grep cap helps but does not subsume spill cap). **Size:** S. **Files touched:** tool-output handler + tests.

#### P2-T5 — Design blob-storage migration for inline attachments (design only)

**Why:** 144 inline base64 `file` parts + `blob/blob_ref 0` (E11); images inflate `part.data` JSON (security §2.5 tail: 1,337 parts >100 kB).

**Acceptance criteria:**
- [ ] Design note: migrate to `blob`/`blob_ref`, store only hash in `part.data`; includes backfill-vs-new-only decision and size estimate; no history rewritten until P3-T1 decision.

**Verification:**
- [ ] Design reviewed by CTO + CISO (size vs. privacy tradeoff: blobs still retain bytes, but out of `part.data` text).

**Dependencies:** Input to P3-T1. **Size:** M (design + prototype 3–5 files, or design doc only at S if prototype deferred). **Files touched:** design doc + (if prototyped) blob writer + tests.

#### P2-T6 — Egress allowlist + URL hygiene

**Why:** 8 userinfo URLs, 93 query-string URLs (tokens to hosts + stored in `part.data` clear); 17 `http` uses all localhost/private (enforce it); shell egress (`IWR 1,121`) bypasses any webfetch-only control (E17; security §3.3, §7 P1-5).

**Acceptance criteria:**
- [ ] `webfetch` denies third-party `http` (localhost/private-test only), rejects userinfo (`@`), strips/rejects token-like query strings (log host + param *names* only), default-denies `169.254.169.254`, `file:`, `data:`.
- [ ] `bash` egress proxied/allowlisted (`IWR`/`IRM`/`curl` to approved package/registry hosts); alert on private-IP egress beyond known dev ranges (`172.30.96.1:1440/1441`, `127.0.0.1:8420`).
- [ ] Host allowlist hit-rate report producible (host + count, never payload values).

**Verification:**
- [ ] Policy tests: userinfo rejected, third-party `http` rejected, metadata/`file:` denied, allowlisted registry passes.
- [ ] Transmission log sample re-queried with §10 host-extraction (hostnames + counts only).

**Dependencies:** Coordinate host list with P3-T5. **Size:** M. **Files touched:** webfetch policy + bash egress policy + tests (3–5 files).

#### Checkpoint P2
- [ ] Cache-quirk documented; mega-session budget/early-compaction live; read-dedup + spill-cap deltas visible on snapshot; egress allowlist denies the 8/93/17 patterns in tests.

---

### Phase P3 — Schema + lifecycle hygiene (after P0–P2 deltas are confirmed)

Goal: resolve dual-schema ambiguity, enforce retention/privacy, verify vendor compliance, and re-audit. Baselines: E4, E12, E18, E19.

#### P3-T1 — Decide: complete v2 or freeze v1 explicitly

**Why:** `session_part 0` vs `session_message 9,284`, `blob/blob_ref 0`, `schedule/job/inbox/event 0` vs `event_sequence 3,530` (E4). Today every consumer joins both schemas (audit §8-P4-17). v2 writers for parts/blobs/scheduling/events are either missing or deliberately deferred.

**Acceptance criteria:**
- [ ] ADR recorded: complete v2 writers (parts, blobs, scheduling, events) **or** freeze v1 as canonical with dual-schema query burden acknowledged.
- [ ] Follow-through scope (tables, backfill-or-new-only, consumer joins) listed as follow-up tasks; no silent continued dual-schema ambiguity.

**Verification:**
- [ ] ADR merged; if “complete v2”, reader/writer gap tests pass for at least `session_part` on new data.

**Dependencies:** P2-T5 (blob design). **Size:** S. **Files touched:** ADR doc + (if completer) v2 writer(s).

#### P3-T2 — Sweep orphaned tool calls (`running 93 / pending 2`)

**Why:** 95 non-terminal markers with no sweeper (E12); analogous to the HITL expiry sweep that already exists for approvals (AGENTS §9.1) but has no equivalent for tool calls (audit §6.3).

**Acceptance criteria:**
- [ ] TTL sweeper: `running` > 1 h → `error` with “orphaned” marker; `pending` similarly bounded; wired into daemon/governance cadence alongside the HITL sweep.
- [ ] Sweeper run is observable (log + count) and idempotent.

**Verification:**
- [ ] Sweeper tests green (age threshold, terminal-state exclusion, idempotency); `running`/`pending` counts on snapshot → 0 after a sweep pass.

**Dependencies:** P3-T1 (which schema’s status field is authoritative). **Size:** M. **Files touched:** sweeper + daemon wiring + tests.

#### P3-T3 — Cull session-less projects (67 of 72)

**Why:** Worktree/temp projects created eagerly (~10 on 2026-11-03/04 alone) but never used; only 5 projects ever had sessions (E4, E18). Project table trending to noise.

**Acceptance criteria:**
- [ ] Project GC: delete worktree projects with no sessions older than N days (N recorded); FK-safe order (project_directory/worktree/session checks first).

**Verification:**
- [ ] GC tests green; `SELECT COUNT(*) FROM project` + sessions-per-project query (§10) shows no session-less old projects remain.

**Dependencies:** P3-T1 (schema awareness). **Size:** S. **Files touched:** GC job + tests.

#### P3-T4 — Enforce retention, archival, and compaction

**Why:** 0 archived sessions, 95-day verbatim retention, no per-session purge evidenced, freelist only ~8 MB so *retained* rows are the problem (security §4). GDPR/erasure risk. Audit P1-3 proposes archiving v1 < N days to a cold DB + `VACUUM INTO`, and `auto_vacuum=INCREMENTAL` + periodic `incremental_vacuum`.

**Acceptance criteria:**
- [ ] Retention window set (proposed: 30 days for `part`/`message` bodies, longer for session metadata only — **requires CEO/CISO approval**; see Open Questions) with scheduled `time_archived` + purge jobs, scoped by project (70 temp projects from P3-T3).
- [ ] Archival executed via `VACUUM INTO` to a compacted/cold DB (space check first — VACUUM needs ~DB-size free space); `auto_vacuum` decision recorded; post-purge `VACUUM` target: live DB consistently <1 GiB (security §7) with `.bak` older than the window absent in plaintext.

**Verification:**
- [ ] `SELECT COUNT(*) FROM session WHERE time_archived IS NOT NULL` > 0 (archive enforcement proven); size/`freelist_count` before/after captured; `integrity_check` still `ok`.
- [ ] Live-DB drift note: run against a snapshot, not the live WAL.

**Dependencies:** P0-T5 (new data already clean), P0-T6 (checkpoint done), P3-T1–T3. **Size:** M. **Files touched:** retention/purge job + scheduler wiring + tests + archival script (3–5 files).

#### P3-T5 — Verify third-party transmission against AGENTS §9.2

**Why:** Security audit explicitly did **not** cross-check Resend/Composio/Google against `docs/APPROVED-VENDORS.md` and makes no compliance claim (§3.2). `resend_list-api-keys 1` and `composio_MULTI_EXECUTE 13` are high-value tool traffic.

**Acceptance criteria:**
- [ ] Cross-check recorded for `resend_*`, `composio_*`, `google_search`/`websearch` providers against the allowlist + 90-day windows.
- [ ] Non-approved tools suspended (notably `resend_list-api-keys` / `resend_send-email` / `composio_MULTI_EXECUTE_TOOL`) pending CEO/CISO sign-off; every transmission logged (host + tool + payload class, never values).

**Verification:**
- [ ] Allowlist sign-off (or tool-removal) entries exist in `docs/APPROVED-VENDORS.md` / governance log; suspended tools return disabled error.

**Dependencies:** P2-T6 (shared host list). **Size:** S. **Files touched:** vendor doc + tool registry + log wiring.

#### P3-T6 — Quarantine injection-bearing trajectories from memory recall

**Why:** 3,412 `ignore%prior` + 2,077 `system prompt` + 317 `jailbreak` hits at scale in a memory-sourced store (E19). Benign-research noise is acknowledged; the risk is poisoned recall (LLM01/LLM02/LLM07) (security §5).

**Acceptance criteria:**
- [ ] Sessions/parts matching `%ignore%prior|previous%`, `%system prompt%`, `%jailbreak%`, `%disregard%`, `%override%instruction%` tagged `untrusted-instructions` and excluded from the `## Relevant Past Work` injector pending human review (re-admission path recorded).

**Verification:**
- [ ] Recall tests: tagged rows excluded; untagged rows unaffected. Counts re-queried with §10 `LIKE` probes (counts only).

**Dependencies:** P2-T1 (recall injector awareness). **Size:** M. **Files touched:** tagging job + injector filter + tests.

#### P3-T7 — Stale artifact cleanup

**Why:** `opencode-.db 765 KB` (Oct 30 v1-shim), `log\opencode.log ~80 MB`, `kv.models-dev:v2:catalog 11 MB` (E18). Low severity bloat/confusion (security §6 R7).

**Acceptance criteria:**
- [ ] `opencode-.db` removed or archived (with note if it holds v1→v2 transition data — audit §9.2 limitation); log rotated/compressed; KV catalog TTL’d if the provider allows it.

**Verification:**
- [ ] `Get-ChildItem` size listing before/after; KV TTL test if applicable.

**Dependencies:** None. **Size:** XS. **Files touched:** none in repo (filesystem/config only).

#### P3-T8 — Re-audit on a snapshot (not the live WAL)

**Why:** Audit P1-21 / security verification list: confirm WAL size, `.bak` presence, temp count, `session_part`/`blob` population, §2 pattern collapse for *new* data, 0 userinfo/third-party-`http`, allowlist hit-rates, 0-frame checkpoint, DB size.

**Acceptance criteria:**
- [ ] Snapshot taken via `sqlite3 ".backup"` or filesystem snapshot (copy-on-write precedent exists: the 38.5 GB `.bak`); all baseline queries (§10) re-run against the snapshot and compared to §§E1–E19.
- [ ] New-window (post-P0) secret-pattern counts show redaction working; historical counts noted as pre-retention (expected until P3-T4).
- [ ] Re-audit report written to `reports/` (never into `reports/evidence/` per §9.3) with delta tables.

**Dependencies:** P0–P3 tasks it verifies. **Size:** S. **Files touched:** re-audit report only (read-only queries + snapshot outside the DB dir or in Temp, cleaned after).

#### Checkpoint P3 / Complete
- [ ] v2 decision recorded; orphan/project/retention sweeps proven on snapshot; vendor verification recorded; injection quarantine live; stale artifacts gone; re-audit deltas confirm P0–P2. Ready for human review.

---

## 7. Risks and mitigations

| Risk | Impact | Mitigation (plan step) |
|---|---|---|
| **Live-DB drift invalidates verification** — counts shift mid-audit (91→94 sessions observed) | Med | Snapshot via `.backup` for all re-queries (P3-T8); treat live numbers as snapshot + delta, never cross-query arithmetic. |
| **WAL checkpoint / VACUUM on live DB corrupts or blocks** | High | Maintenance window with OpenCode closed (P0-T6); space check before VACUUM (~DB-size free space); never during live sessions; serialize with P0-T2. |
| **Rotation breaks production tools** (revoking keys still referenced) | High | Rotate-then-revoke order per AGENTS §11; health checks (`:8420/:8421`) before revocation; ChangeLog per provider. |
| **Redaction over-redacts benign discussion or under-redacts live values** | Med | Patterns reviewed by CISO; benign-mention tests (P0-T5); counts-only proof, never value dumps; no history rewrite without migration + audit note. |
| **`.bak` deletion destroys the only pre-v2 restore path** | High | Restore-test before delete (P0-T2); encrypted cold storage as the default alternative to deletion. |
| **Root-config hook blocks P1-T5 / prompt edits** (missing `[CEO-OVERRIDE]` tag) | Med | Tag + `docs/governance-audit.md` entry by design (P1-T5); never bypass with `--no-verify`; escalate to CEO per §18. |
| **ACL `inheritance:r` breaks multi-profile access** (a second user legitimately needs read) | Low | Re-check after profile creation (P0-T1); record any intentional share as an explicit ACE with owner + review date, not inherited RX. |
| **Read-dedup serves stale content after concurrent edit** | Med | Invalidation on mtime/size (P2-T3); agree contract with P1-T1 before parallelizing. |
| **Retention purge violates legal/GDPR hold or destroys evidence needed for open investigations** | High | CEO/CISO-approved window (Open Questions); legal hold check before P3-T4; archive (not delete) to cold DB first. |
| **Audit writes into evidence set** (§9.3 violation) | Med | Re-audit output to `reports/` only; snapshots in `Temp\opencode` cleaned after; auditor read/write sets disjoint. |
| **PowerShell linter false-positives block legitimate `pwsh 7` syntax** | Low | Linter targets PS 5.1 patterns per §17 table; `pwsh` equivalents allowed; tests per antipattern (P1-T3). |
| **Temp purge deletes fresh worktree inputs** | Low | 7-day age threshold preserves the 228 fresh files (P0-T7); dry-run count before delete. |

---

## 8. Open questions (decisions needed before/within implementation)

1. **Credential encryption (P0-T3):** Is `credential.value` / `auth.json` encrypted at the application layer (DPAPI/key-provider) or plaintext? No answer can be inferred from counts. **Owner:** CISO + vendor docs. **Blocks:** P0-T4 scope.
2. **`.bak` retention (P0-T2):** Is the 38.5 GB pre-v2 `.bak` needed for any restore/legal hold, or may it be deleted after a restore test? **Owner:** Human CEO (CISO of record).
3. **Encryption at rest (P0, security R1):** BitLocker (whole-volume, preferred) vs EFS on `opencode.db*` / auth JSONs? **Owner:** CIO + CISO. Volume-wide BitLocker changes need a maintenance window.
4. **Retention window (P3-T4):** 30 days for bodies + longer for metadata (security proposal) — or a different window? Any legal/GDPR hold overriding purge? **Owner:** Human CEO + CLO/DPO.
5. **V2 fate (P3-T1):** Complete v2 writers (parts/blobs/events/scheduling) or freeze v1 as canonical? **Owner:** CTO (ADR).
6. **Vendor allowlist (P3-T5):** Are Resend, Composio, Google (websearch), Exa, and Parallel.ai on `docs/APPROVED-VENDORS.md` within their 90-day windows? `resend_list-api-keys` / `MULTI_EXECUTE` remain suspended until signed. **Owner:** Human CEO (CISO of record).
7. **Subagent depth (P1-T5):** New ceiling value for orchestrator-class agents, or a direct-work carve-out with logging? **Owner:** Human CEO (via §18 override if root-config).
8. **Token budget numbers (P2-T2):** Per-session and per-agent/day budgets (input + cache_read) — values require a proposal from observed burn distributions (E9), not a guess. **Owner:** CTO + CFO (cost is meaningless under free models).
9. **`opencode-.db` contents (P3-T7):** Does the 765 KB stale shim hold v1→v2 transition data needing its own audit before removal? (Audit §9.2 limitation). **Owner:** CTO.
10. **Share-URL accounting (audit §9.2 follow-up):** `SELECT COUNT(*) WHERE share_url IS NOT NULL` was never run (low value) — include in P3-T8 re-audit for completeness. **Owner:** Chief-of-Staff.

---

## 9. Verification & re-audit schedule

| When | What to prove | How (snapshot) |
|---|---|---|
| After P0 | No `…-1003` ACE; `.bak` gone/encrypted; WAL 0 frames; temp collapsed; redaction/deny live on new data | §10 queries A (ACL/size/WAL/temp) + §2-pattern windows restricted to post-gate `time_created` |
| After P1 | Edit (588/154/74), ripgrep (236/140), PowerShell (474/Select-Object), schema (149), depth (40) groups collapsed | §10 query families B–D on new-window data |
| After P2 | Cache quirk documented; burn budgets live; hot-file + spill re-reads collapsed; egress denies proven | §10 queries E–F + policy tests |
| 14 days after P0 (audit recommendation) | WAL size, `.bak` presence, temp count, `session_part`/`blob` population confirmed stable | Full §10 re-run (P3-T8) — this report serves as the baseline |

**Re-audit rule:** every future audit of this DB should route through a copy-on-write snapshot (`sqlite3 ".backup"` or filesystem snapshot) so findings are reproducible, not drift-affected (audit §8-P1-5). Do not re-run LIKE scans that dump values; counts/hosts/lengths only (security §8 limits).

---

## 10. Appendix — query library and file inventory (verbatim intent from source reports)

All queries run as `sqlite3 -readonly "C:\Users\jmlus\.local\share\opencode\opencode.db"` (or against the P3-T8 snapshot). `time_created` is Unix ms; display via `datetime(time_created/1000,'unixepoch','localtime')`. JSON via `json_extract(data,'$.…')`. Counts/hosts/lengths only — **never `SELECT data` / `SELECT value` / full URLs** (security §8).

**A. Size / integrity / ACLs / temp**
```sql
PRAGMA page_size; PRAGMA page_count; PRAGMA freelist_count;
PRAGMA journal_mode; PRAGMA integrity_check;
```
```powershell
icacls "C:\Users\jmlus\.local\share\opencode" "C:\Users\jmlus\.local\share\opencode\opencode.db"
cipher /c "C:\Users\jmlus\.local\share\opencode\opencode.db"
Get-ChildItem "C:\Users\jmlus\.local\share\opencode\opencode*" | Select Name, Length, LastWriteTime
(Get-ChildItem "C:\Users\jmlus\AppData\Local\Temp\opencode" -Recurse -File).Count
```

**B. Row counts (key tables)**
```sql
SELECT 'session='||(SELECT COUNT(*) FROM session)||' session_v2='||(SELECT COUNT(*) FROM session_v2)…
-- full list: account 0, credential 22, event 0, message 153182, part 670664,
-- session_message 9161+, session_part 0, todo 2771, project 72
```

**C. Tool × status + error groups (P1 proof)**
```sql
SELECT json_extract(data,'$.tool') AS tool, json_extract(data,'$.state.status') AS status, COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool' GROUP BY 1,2;
SELECT json_extract(data,'$.state.error'), COUNT(*) FROM part WHERE … status='error' GROUP BY 1 ORDER BY 2 DESC LIMIT 25;
-- repeated bash stdout errors (completed bash whose output LIKE '%error%', HAVING n>1), last-30d anchored to MAX(part.time_created)
```

**D. Cache-ledger agreement (P2 proof)**
```sql
SELECT SUM(tokens_cache_read), SUM(tokens_cache_write) FROM session;  -- 15,210,842,514 / 0
SELECT SUM(json_extract(data,'$.tokens.cache.read')), SUM(json_extract(data,'$.tokens.cache.write')) FROM part WHERE json_extract(data,'$.type')='step-finish';
```

**E. Hot files (P2 proof)**
```sql
SELECT lower(json_extract(data,'$.state.input.filePath')) AS path, COUNT(*) FROM part WHERE json_extract(data,'$.tool')='read' GROUP BY 1 HAVING COUNT(*)>10 ORDER BY 2 DESC LIMIT 40;
```

**F. Security counts (P0/P3 proof — counts only)**
```sql
SELECT COUNT(*) FROM part WHERE data LIKE '%sk-%';  -- + %secret%, %api_key%, %password%
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.state.input.filePath') LIKE '%.env%';  -- .env reads
SELECT json_extract(data,'$.tool'), COUNT(*) FROM part WHERE json_extract(data,'$.state.error') LIKE '%ignore%prior%' GROUP BY 1;  -- injection-language split
```

**G. Lifecycle (P3 proof)**
```sql
SELECT COUNT(*) FROM session WHERE time_archived IS NOT NULL;  -- 0 → archive enforcement after P3-T4
SELECT COUNT(*) FROM project p WHERE NOT EXISTS (SELECT 1 FROM session s WHERE s.project_id=p.id);  -- session-less projects (67 → 0 old)
SELECT json_extract(data,'$.state.status'), COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool' GROUP BY 1;  -- running/pending → 0 after sweep
```

**File inventory touched by this plan (for implementers):** ToolRunner/permission policy + redaction filter (P0-T5); edit/grep/glob/bash + validation (P1-T1–T4, P1-T6); egress + dedup + spill + budget/compaction (P2-T2–T4, P2-T6); retention/VACUUM/sweeper/GC/quarantine (P3-T2–T4, P3-T6); root-config (`opencode.json`) only via P1-T5 with §18 override. Git: branch + PR + 6-check CI per AGENTS §5; `ruff check src/` + `mypy src/` + `pytest` (or `pwsh scripts/maintenance/lint-ecl.ps1` for harness/docs) per task.

---

*End of plan. Baseline: 2026-11-08 audits (E1–E19). Next step: CEO decisions on Open Questions 1–4, then P0-T1/T3/T7 in parallel.*
