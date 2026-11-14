# opencode.db Security Fix Plan — 2026-11-08

**Author:** ciso (CISO) for LightSpeed Holdings
**Sources:** `reports/opencode-db-security-2026-11-08.md` (security slice) + `reports/opencode-db-audit-2026-11-08.md` (analytics) — both read in full
**Scope:** fixes for defects R1–R6 only. No secret values are reproduced in this file.
**Framework:** `security-and-hardening` skill — threat-model-first (STRIDE), Always/Ask/Never tiers, OWASP LLM 2025 (LLM01/02/06/07/08).

> **Read-only compliance preserved by this plan:** this file creates no DB writes. All fix steps that touch `opencode.db` are gated behind a maintenance window (OpenCode closed) and a pre-change snapshot. Historical `part.data` is never edited in place without a migration + audit note.

---

## 1. Threat model (summary)

**Trust boundaries (untrusted → system):** (1) tool outputs (`bash`/`read`/`grep` bodies) persisted into `part.data`; (2) web content via `webfetch`/`websearch`; (3) shell egress (`Invoke-WebRequest`, `Invoke-RestMethod`, `curl`); (4) third-party tool routing (Resend/Composio); (5) filesystem (`*.env`, `auth.json`, `opencode.db*`).

**Assets:** `credential` table (22 rows), `auth.json` / `mcp-auth.json` tokens, `.env` values, 95-day trajectory corpus (3.00 GiB DB + 2.95 GiB WAL + 35.89 GiB `.bak`).

**STRIDE quick pass:**

| Threat | Vector in evidence | Mitigation in this plan |
|---|---|---|
| **I**nformation disclosure | plaintext DB/`.bak`/auth JSON, `…-1003` RX ACE, secrets in tool outputs, token-in-URL/query | §2 ACL + §3 encryption, §4 rotation, §5 redaction, §6 read-deny, §8 egress allowlist |
| **T**ampering | WAL 98% behind — crash-consistent only, no integrity job | §9 checkpoint + retention, `integrity_check` gate |
| **E**levation | LLM output passed to shell/PowerShell (78,923 `bash` parts); LLM01 prompt injection (`ignore%prior%` 3,412) | §6 read-deny, §8 allowlist, §10 injection quarantine, §2 least-privilege |
| **R**epudiation | 0 archived sessions, no purge log | §9 retention job emits an audit log row per run; §7 quarantine table |

**Key principle (LLM02/LLM07):** anything in `part.data` can be re-surfaced into a future prompt by the recall loop. The DB is therefore classified as a **secrets-bearing store**, not a benign log. The `security-and-hardening` rule — *"keep secrets and other users' data out of prompts"* — is enforced at three layers: prevent ingestion (§6), strip values pre-persistence (§5), and exclude poisoned recall (§10).

---

## 2. Defect → fix map

| ID | Severity | Defect (evidence) | Fix tasks |
|---|---|---|---|
| **R1** | 🔴 P0 Critical | 22 `credential` rows cipher=U unencrypted; DB (3.00 GiB) + WAL (2.95 GiB) + `.bak` 35.89 GiB on ACL-only protection; `auth.json`/`mcp-auth.json` adjacent | F-01 ACL lockdown, F-02 encryption, F-03 `.bak` disposal |
| **R2** | 🔴 P0 Critical | Secrets in trajectories (`sk-` 12,747 rows / 2,000 sessions; `api_key` 15,288); `.env` read 309×, 4,394 bash env touches; tool outputs stored verbatim (`tool` = 188,713 parts, dominates hits) | F-04 credential rotation, F-05 pre-persistence redaction, F-06 read-deny rules |
| **R3** | 🟠 P1 High | Orphaned SID `…-1003` RX on DB/`.bak`/auth JSON + parent inheritance; no Deny ACEs; no owner-only lockdown | F-01 (ACL lockdown) |
| **R4** | 🟠 P1 High | Unconstrained egress: `webfetch` 745 calls / 141 hosts / 8 userinfo URLs / 93 query-string URLs; shell `IWR` 1,121 / `curl` 718 / `IRM` 529; `resend_*` ~35 / `composio_*` ~27 **unverified vs `docs/APPROVED-VENDORS.md`** (confirmed 2026-11-08: neither vendor appears in the allow-list; only cmem.ai, 0x0.st, Telegram, NotebookLM, Workers, kie.ai, Greptile [retired], Xiaomi MiMo, Google AI/Gemini image, Comfy Cloud are listed) | F-07 webfetch/shell allowlist + URL hygiene, F-08 third-party suspension + sign-off |
| **R5** | 🟡 P2 Medium | 0 archived sessions; 1.8 GB `part` + 786 MB `message` retained 95 days; WAL checkpoint ~98% behind; 72 projects (67 session-less) | F-09 checkpoint + WAL discipline, F-10 30-day retention + archive job, F-11 stale-artifact purge |
| **R6** | 🟡 P2 Medium | Injection phrases stored in recallable DB: `ignore%prior%` 3,412, `override%instruction%` 2,162, `system prompt%` 2,077, `jailbreak` 317 — split across `tool`/`reasoning`/`text`; v2 (7 days) already shows `ignore%prior%` 158 / `system prompt%` 150 | F-12 injection quarantine from memory recall |

---

## 3. Prioritized task list

Order = execution order. P0 blocks P1; nothing in P1 starts until its P0 prerequisites are verified. Every task has an owner, an acceptance criterion, a verification command/query, and a rollback.

### P0 — do now (before next session batch)

| Seq | Task | Owner | Effort | Depends on |
|---|---|---|---|---|
| F-01 | Remove orphaned `…-1003` ACE; lock parent to owner-only | **ciso** + `security-compliance-lead` | 15 min | — |
| F-02 | Encrypt at rest: BitLocker (preferred) or EFS on `opencode.db*` + auth JSONs | **ciso** / `security-architect` | 1–2 h | F-01 |
| F-03 | Dispose of the 35.89 GiB plaintext `.bak` (shred or encrypted cold archive) | **ciso** / `devsecops-lead` | 30 min | F-02 |
| F-04 | Credential rotation runbook — rotate all 22 `credential` values + `auth.json`/`mcp-auth.json` tokens + every `.env` value the agent read | **ciso** / `incident-response-lead` | 2–4 h | F-01 |
| F-05 | Pre-persistence redaction filter over `part.data` (value → `[REDACTED]`) | **ai-security-specialist** / `security-architect` | 4–8 h | F-04 |
| F-06 | Read-deny rules: `read`/`bash` denied on `.env*`, `auth.json`, `mcp-auth.json`, `opencode.db*` | **ai-security-specialist** / `security-compliance-lead` | 2–4 h | F-05 |

### P1 — do this week

| Seq | Task | Owner | Effort | Depends on |
|---|---|---|---|---|
| F-07 | Egress allowlist for `webfetch` + shell (`IWR`/`IRM`/`curl`): https-only (dev-loopback exception), reject userinfo/query-token URLs, deny SSRF targets | **ciso** / `devsecops-lead` | 1–2 d | F-06 |
| F-08 | Suspend `resend_*` (incl. `list-api-keys`, `send-email`) + `composio_*` pending CEO/CISO + `docs/APPROVED-VENDORS.md` sign-off; log all transmissions (host + tool + payload class, never values) | **ciso** (as human-CEO delegation) | 1 h + sign-off latency | F-07 |
| F-09 | WAL checkpoint + `VACUUM` in a maintenance window; diagnose why WAL reached 98% of DB | **devsecops-lead** / `platform-reliability-engineer` | 1 h + monitoring | F-03 |

### P2 — do this month (≤30 days)

| Seq | Task | Owner | Effort | Depends on |
|---|---|---|---|---|
| F-10 | 30-day retention + archive job: `time_archived` + purge `part`/`message` bodies, project GC, post-purge `VACUUM` | **ciso** / `memory-owner` | 1–2 d | F-09 |
| F-11 | Purge stale artifacts: `opencode-.db` shim, `Temp\opencode` (>7 days), `log` rotation, KV catalog TTL | **devops-lead** | 2 h | F-09 |
| F-12 | Injection quarantine: tag `%ignore%prior\|previous%`, `%system prompt%`, `%jailbreak%`, `%disregard%`, `%override%instruction%` sessions/parts; exclude from `## Relevant Past Work` injector pending human review | **ai-safety-lead** / `ai-security-specialist` | 4–8 h | F-05 |

---

## 4. ACL hardening (F-01 → R3, part of R1)

**Steps (run from an elevated shell; OpenCode may stay open — ACL change is file metadata, not DB content):**

```powershell
# 1. Snapshot current ACLs (evidence before change)
icacls "C:\Users\jmlus\.local\share\opencode" | Out-File .\icacls-before-2026-11-08.txt
icacls "C:\Users\jmlus\.local\share\opencode\opencode.db" | Out-File .\icacls-db-before-2026-11-08.txt

# 2. Remove the orphaned SID everywhere it is inherited (parent + tree)
icacls "C:\Users\jmlus\.local\share\opencode" /remove "S-1-5-21-2913538908-3024988640-2666040046-1003" /T /Q

# 3. Break inheritance and re-assert owner-only (least privilege; deny-by-default per CISO operating guidelines)
icacls "C:\Users\jmlus\.local\share\opencode" /inheritance:r
icacls "C:\Users\jmlus\.local\share\opencode" /grant:r "JRMTHINKPAD\jmlus:(OI)(CI)F" "NT AUTHORITY\SYSTEM:(OI)(CI)F" "BUILTIN\Administrators:(OI)(CI)F"

# 4. Re-assert on the credential-bearing files explicitly (defence in depth — do not rely on inheritance alone)
icacls "C:\Users\jmlus\.local\share\opencode\opencode.db"      /inheritance:r /grant:r "JRMTHINKPAD\jmlus:F" "NT AUTHORITY\SYSTEM:F" "BUILTIN\Administrators:F"
icacls "C:\Users\jmlus\.local\share\opencode\opencode.db.bak"  /inheritance:r /grant:r "JRMTHINKPAD\jmlus:F" "NT AUTHORITY\SYSTEM:F" "BUILTIN\Administrators:F"
icacls "C:\Users\jmlus\.local\share\opencode\auth.json"       /inheritance:r /grant:r "JRMTHINKPAD\jmlus:F" "NT AUTHORITY\SYSTEM:F" "BUILTIN\Administrators:F"
icacls "C:\Users\jmlus\.local\share\opencode\mcp-auth.json"   /inheritance:r /grant:r "JRMTHINKPAD\jmlus:F" "NT AUTHORITY\SYSTEM:F" "BUILTIN\Administrators:F"
```

Also audit the `C:\Users\jmlus\.local` parent for the same SID (inheritance origin) and remove it there if present.

**Acceptance criteria:** `icacls` on the directory, DB, `.bak`, and both auth JSONs shows **no** `…-1003` entry; only `jmlus`, `SYSTEM`, `Administrators` remain; parent and children agree.
**Verification:**

```powershell
icacls "C:\Users\jmlus\.local\share\opencode"
icacls "C:\Users\jmlus\.local\share\opencode\opencode.db"
icacls "C:\Users\jmlus\.local\share\opencode\auth.json"
# Expect: no "S-1-5-21-...-1003" line anywhere.
```

**Rollback:** re-add is *not* recommended. If an application breaks (it should not — the removed SID has no live account), restore from the `icacls-before-2026-11-08.txt` snapshot by re-granting the exact ACE, file a defect, and re-run F-01 under `security-architect` guidance.

---

## 5. Encryption at rest (F-02 + F-03 → R1)

**Decision (deny-by-default):** BitLocker is preferred (whole-volume, covers DB + WAL + `.bak` + auth JSONs + any future copies). EFS is the fallback if BitLocker is unavailable.

**Option A — BitLocker (preferred):**

```powershell
# Check status (volume must report Protection Status: On)
manage-bde -status C:
# If off, enable (requires admin + restart):
manage-bde C: -protectors -add -type RecoveryPassword
manage-bde -turnon C:
```

**Option B — EFS on the data directory (fallback):**

```powershell
# Encrypt the opencode data dir (files + future children inherit via the directory flag)
cipher /e /s:"C:\Users\jmlus\.local\share\opencode"
# Cipher details for the DB specifically:
cipher /c "C:\Users\jmlus\.local\share\opencode\opencode.db"
# Expect: "E" (encrypted). Backup the EFS recovery cert before proceeding.
```

**F-03 — `.bak` disposal (part of R1):** the 38.5 GB `.bak` (2026-11-01) is a pre-v2 snapshot (~12× live DB). Two acceptable end states, in order of preference:

1. **Preferred — delete** after the F-09 checkpoint proves v2 is stable (integrity `ok`, `session_v2` writes healthy). Delete via `Remove-Item` (no recycle), then confirm the file is gone.
2. **Alternative — encrypted cold archive** if a restore point is genuinely required: copy to an encrypted volume / encrypted ZIP (AES-256, password in the secrets manager, never in a script), then delete the plaintext original and ACL-lockdown the archive.

Never leave two plaintext copies of the corpus side by side.

**Acceptance criteria:** `cipher /c` reports `E` **or** `manage-bde -status` reports the volume protected; no plaintext `.bak` exists under `~\.local\share\opencode\`.
**Verification:**

```powershell
cipher /c "C:\Users\jmlus\.local\share\opencode\opencode.db"
cipher /c "C:\Users\jmlus\.local\share\opencode\auth.json"
manage-bde -status C:
Test-Path "C:\Users\jmlus\.local\share\opencode\opencode.db.bak"   # Expect: False (or True only if EFS-covered AND in encrypted cold archive)
```

**Rollback:** BitLocker/EFS is forward-only; rollback = decrypt via `cipher /d` / `manage-bde -turnoff`. Do **not** decrypt without a compensating control (ACL lockdown F-01 is the minimum). Re-encrypt within 24 h of any rollback, or escalate to the CEO as a P0 regression.

---

## 6. Credential rotation runbook (F-04 → R2)

**Assumption (per security audit §7.3):** until OpenCode vendor documentation proves `credential.value` is encrypted at rest (e.g., DPAPI/key-provider), treat all 22 values as plaintext. Rotation scope is therefore **everything the agent could have ingested**, not a value-level list (values were never inspected — by design).

### Runbook

1. **Enumerate (metadata only, never values):** list credential labels + `LENGTH(value)` to confirm count is still 22 and catch additions:
   ```sql
   -- sqlite3 -readonly "C:\Users\jmlus\.local\share\opencode\opencode.db" (names/lengths only)
   SELECT label, LENGTH(value) AS len, datetime(time_created/1000,'unixepoch','localtime') AS created FROM credential ORDER BY label, created;
   ```
   *Do not `SELECT value`.* Labels already known: 10× `API key` (bulk import 2026-10-22), `Groq`, `Cohere`, `Google`, `Ollama (local)`, `Default`, 6× `OpenCode Console*` (2026-10-28 → 11-03).
2. **Rotate at the provider, not in the DB.** For each label, revoke the old key in the provider console and issue a new one. Order: highest-exposure first — `Google`, `Groq`, `Cohere`, 10× `API key`, 6× `OpenCode Console*`. `Ollama (local)` = local-only, rotate if it guards any non-local resource.
3. **Replace in the credential store** via the supported UI/CLI (never via direct SQL `UPDATE` in a live DB). Update `auth.json` / `mcp-auth.json` tokens the same way.
4. **Rotate every `.env` value the agent read.** Enumerate *which files* (paths only, never contents):
   ```sql
   SELECT lower(json_extract(data,'$.state.input.filePath')) AS p, COUNT(*) AS n
   FROM part WHERE json_extract(data,'$.type')='tool' AND json_extract(data,'$.tool')='read'
     AND lower(json_extract(data,'$.state.input.filePath')) LIKE '%.env%'
   GROUP BY 1 ORDER BY 2 DESC;
   -- Baseline was 309 .env reads; re-run to get the current file list.
   ```
   For each file, diff its keys against the provider consoles and rotate any key that was ever live. `.env.example` (template) is exempt after confirming it holds placeholders only.
5. **Assume residual exposure.** Even after rotation, the 95-day corpus embeds the *old* values. Rotation invalidates them; the corpus itself is still sensitive and must be handled by F-02/F-10 (§5/§9). Rotated-away values must never be reused.
6. **Record:** per §9.2 of `AGENTS.md`, log the rotation (date, provider, key label, new-key fingerprint — e.g., last-4 + SHA-256-prefix, never the value) in the runbook output; do not record values anywhere.

**Acceptance criteria:** all 22 `credential` values + both auth JSONs replaced with fresh keys; every `.env` file from the enumeration above audited and its live keys rotated; a rotation log exists with fingerprints only.
**Verification (post-rotation, read-only):**

```sql
SELECT COUNT(*) AS credential_rows, AVG(LENGTH(value)) AS avg_len, MAX(LENGTH(value)) AS max_len FROM credential;
-- Expect: count may differ (provider-driven), lengths sane; values never printed.
```

plus provider-console confirmation that old keys show as revoked (screenshot/log reference, not key material).
**Rollback:** none — rotation is irreversible by design. If a new key fails, re-issue from the provider; never revert to an old key. A rollback entry in this table means: keep the rotation log so the next rotation diffs against it.

---

## 7. Pre-persistence redaction (F-05 → R2) + read-deny (F-06 → R2)

### 7.1 Redaction filter (pre-persistence, value → `[REDACTED]`)

Apply **before** `part.data` insert — never after (post-hoc edits of history require a migration + audit note and are out of scope for the live filter). The filter must run on the persistence path, not in the prompt (the prompt is not a security boundary — LLM01).

**Patterns to replace (value portion only, keep the key name for debuggability):**

| # | Pattern (regex) | Notes |
|---|---|---|
| 1 | `sk-[A-Za-z0-9_-]{8,}` | OpenAI-style keys (12,747 hits justify a first-class rule) |
| 2 | `(?i)(api[_-]?key|apikey)\s*[:=]\s*\S+` | value → `[REDACTED]` (15,288 hits) |
| 3 | `(?i)(secret|password|passwd|pwd)\s*[:=]\s*\S+` | value → `[REDACTED]` |
| 4 | `AKIA[A-Z0-9]{16}` | AWS access key ID |
| 5 | `ghp_[A-Za-z0-9]{20,}` / `gho_…` / `github_pat_…` | GitHub tokens |
| 6 | `xox[baprs]-[A-Za-z0-9-]{10,}` | Slack tokens |
| 7 | `AIza[A-Za-z0-9_-]{30,}` | Google API keys |
| 8 | `Bearer\s+\S{10,}` | Authorization headers |
| 9 | `-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----` (DOTALL) | whole PEM block |
| 10 | `(?i)(dsn|connectionstring)\s*[:=]\s*\S+` | embedded DB credentials (defence in depth) |

**Implementation requirements (owner: `ai-security-specialist`):**
- The filter applies to `part.data` (all `$.type` — `tool` dominates, but `text`/`reasoning`/`patch` also hit) and to `message.data` / `session_message.data`.
- Replacement preserves key names and surrounding JSON structure: `API_KEY=sk-…` → `API_KEY=[REDACTED]`. JSON validity must be re-checked after replacement (parse-then-serialize, not blind regex-on-JSON — a broken JSON part is itself a defect; `edit` already shows 816 semantic failures from malformed payloads).
- The filter runs **even when** the caller is trusted (deny-by-default; "assume breach" per CISO operating guidelines). No allowlist bypass.
- **Backfill policy:** do not rewrite historical `part.data` in place. Historical exposure is retired by F-04 (rotation) + F-10 (retention purge). Any future backfill runs as a versioned migration with a before/after `COUNT(*)` audit note.

**Acceptance criteria:** a synthetic `part.data` containing one of each pattern (test values, never real keys) round-trips through the persistence path with values replaced and JSON still valid; a read-only recount for *new* rows shows the pattern collapse (§11).
**Verification (read-only, counts only):**

```sql
-- New-data-only collapse check: rows created in the last 24h should show ~0 for the value patterns.
SELECT COUNT(*) FROM part
WHERE time_created > (strftime('%s','now','-1 day') * 1000)
  AND (data LIKE '%sk-%' OR data LIKE '%api_key%');
-- Expect: 0 (or near-0 — benign key-name mentions may remain; value patterns must be gone).
```

**Rollback:** disable the filter only by versioned config revert, never by deleting the rule. Keep the redaction log (pattern IDs + counts, never values) so a false-positive review can re-admit benign mentions.

### 7.2 Read-deny rules (filesystem policy, not prompt policy)

Enforce in the tool/permission layer (not in the system prompt — LLM01: the prompt is not a boundary). Deny both the `read` tool and `bash` file-reads (`Get-Content`, `type`, `cat`, `python open()`) on:

- `*.env` (any extension variant: `.env`, `.env.*`, `*.env`), **except** `.env.example` (verify placeholders-only before exempting)
- `auth.json`, `mcp-auth.json` (any directory)
- `opencode.db`, `opencode.db-wal`, `opencode.db-shm`, `opencode.db.bak`, `opencode-.db*`
- `*.pem`, `*.key` (preventive — aligns with the `security-and-hardening` `.gitignore` baseline)

**Acceptance criteria:** an agent attempt to read a denied path fails with a permission error (visible in `part.state.error`, matching the existing `Automated permission policy` error class already present in the DB — 34 `rule prevents edit` instances prove the mechanism exists); legitimate reads (`.env.example`, source files) still succeed.
**Verification (read-only):**

```sql
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.tool')='read'
  AND lower(json_extract(data,'$.state.input.filePath')) LIKE '%.env%'
  AND time_created > (strftime('%s','now','-7 days') * 1000);
-- Expect: 0 new .env reads after enforcement (baseline: 309 lifetime).
```

Plus a manual negative test: attempt a `read` of a `.env` path in a throwaway session and confirm the permission error (test file contains no real secret — use a dummy with placeholder values).
**Rollback:** rules are config; revert by restoring the prior permission set. Any rollback re-opens R2 and must be re-approved by the CISO with a compensating control note.

---

## 8. Egress allowlist (F-07 → R4) + third-party suspension (F-08 → R4)

### 8.1 `webfetch` policy (SSRF pattern from `security-and-hardening`)

```python
# Admission rules (evaluated in code, not in the prompt):
#  1. scheme must be https: — EXCEPTION: http: allowed only for localhost / 127.0.0.1 / private
#     dev ranges already observed (localhost:1441, localhost:3000, 127.0.0.1:8420, 172.30.96.1:1440/1441).
#     All 17 current http: fetches already qualify — enforce the rule, do not relax it.
#  2. URLs containing userinfo (user:pass@host) → REJECT (8 observed).
#  3. Query strings: reject or strip params whose *names* look like tokens
#     (key, token, secret, api_key, auth, session). Log host + param NAMES only, never values (93 observed).
#  4. Deny: 169.254.169.254 / 169.254.169.253 (cloud metadata), 10.0.0.0/8, 172.16.0.0/12,
#     192.168.0.0/16, fc00::/7, fe80::/10 — after DNS resolution, not string match.
#     (Audit §8 made the LIKE probes false-negative-prone; enforce at resolve time.)
#  5. Deny schemes: file:, data:, ftp: (0 observed — keep denied).
#  6. redirects: 'error' (do not follow a public URL into an internal one).
```

**TOCTOU note (from the skill):** DNS rebinding can swap a validated public IP for a private one between check and fetch. For high-risk callers, resolve once and connect to the pinned IP, or front the fetcher with a filtering agent. At minimum, re-validate on every redirect hop (rule 6 covers this).

### 8.2 Shell egress policy

The dominant channel is shell, not `webfetch` (IWR 1,121 / curl 718 / IRM 529 vs 745 webfetch). A webfetch-only control misses the larger surface.

- Proxy or allowlist `Invoke-WebRequest` / `Invoke-RestMethod` / `curl` to approved package/registry hosts (npm, PyPI, GitHub API, and the dev-loopback ranges in §8.1).
- Alert on any private-IP egress outside the known dev ranges (`172.30.96.1:1440/1441`, `127.0.0.1:8420`, `localhost` ports).
- Cap shell output stored in `part.data` below the 64 KB JSON ceiling that already caused 140 `Ripgrep JSON record exceeded 65536 bytes` errors (also fixes a §6.1 defect class).

### 8.3 Third-party transmission (F-08 — §9.2 compliance)

**Verdict (verified 2026-11-08 against `docs/APPROVED-VENDORS.md`):** `resend.com` (34 webfetch hosts + ~35 `resend_*` calls incl. `list-api-keys`, `send-email`), `composio_*` (~27 calls incl. `MULTI_EXECUTE_TOOL`), and `google_search`/`websearch` providers **do not appear** in the allow-list. Under AGENTS.md §9.2 they are **unauthorized until signed off**.

- **Suspend immediately:** `resend_list-api-keys`, `resend_send-email`, `resend_create-broadcast`, `composio_MULTI_EXECUTE_TOOL` (and any `composio_*` that forwards payloads) pending sign-off.
- **Sign-off path:** CEO (as CISO of record) opens a row in `docs/APPROVED-VENDORS.md` with `approved_at`, data class, host, auth, and `window_end` (≤90 days) per the Exception procedure. No row → no transmission.
- **Transmission log:** every allowed call logs host + tool + payload class (contact / segment / prompt metadata), never payload values. Payload *values* must never enter `part.data` (F-05 runs before persistence).

**Acceptance criteria:** (a) `webfetch` log shows 0 userinfo URLs and 0 third-party `http` over the next 7 days; (b) `docs/APPROVED-VENDORS.md` has rows for Resend/Composio/Google **or** the tools are removed/disabled; (c) shell-egress alert fires on a test private-IP attempt.
**Verification (read-only queries — hostnames allowed, URLs/values never printed):**

```sql
-- Userinfo URLs in new data (expect 0; baseline 8 lifetime):
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.tool')='webfetch'
  AND json_extract(data,'$.state.input.url') LIKE '%@%'
  AND time_created > (strftime('%s','now','-7 days') * 1000);

-- Third-party http in new data (expect 0; baseline: 17 total, all dev-loopback):
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool'
  AND json_extract(data,'$.tool')='webfetch'
  AND json_extract(data,'$.state.input.url') LIKE 'http://%'
  AND json_extract(data,'$.state.input.url') NOT LIKE '%localhost%'
  AND json_extract(data,'$.state.input.url') NOT LIKE '%127.0.0.1%'
  AND time_created > (strftime('%s','now','-7 days') * 1000);

-- Resend/Composio tool calls in new data (expect 0 while suspended):
SELECT COUNT(*) FROM part WHERE json_extract(data,'$.type')='tool'
  AND (json_extract(data,'$.tool') LIKE 'resend_%' OR json_extract(data,'$.tool') LIKE 'composio_%')
  AND time_created > (strftime('%s','now','-7 days') * 1000);
```

**Rollback:** F-08 suspension lifts only on a signed `docs/APPROVED-VENDORS.md` row (forward fix, not a rollback). F-07 allowlist changes roll back by config version; any rollback that re-opens private-IP or userinfo-URL egress needs CISO re-approval.

---

## 9. Retention, checkpoint, and footprint (F-09 + F-10 + F-11 → R5)

### 9.1 WAL checkpoint (F-09) — maintenance window, OpenCode closed

```powershell
# 1. Confirm OpenCode is closed (no live writers).
# 2. Snapshot (see §12) before any DB-mutating step.
# 3. Checkpoint:
& C:\sqlite\sqlite3.exe "C:\Users\jmlus\.local\share\opencode\opencode.db" "PRAGMA wal_checkpoint(TRUNCATE);"
# Expect: {"busy":0,"log":0,"checkpointed":0} and opencode.db-wal shrinking toward 0.
# 4. Compact (needs ~DB-size free space — verify first: 3.00 GiB free required):
& C:\sqlite\sqlite3.exe "C:\Users\jmlus\.local\share\opencode\opencode.db" "VACUUM;"
```

**Diagnose the root cause of the 98% WAL:** a long-running transaction or a backup copy holding the checkpoint back (the `.bak` copy at 35.89 GiB is the prime suspect — it may have held a read lock). After F-03 deletion, monitor WAL/DB ratio; alert if WAL > 10% of DB.

**Acceptance criteria:** `PRAGMA wal_checkpoint` reports 0 frames; `journal_mode` remains `wal`; WAL file < 10% of DB size and stable over 7 days.
**Verification (read-only):**

```sql
PRAGMA journal_mode;   -- expect: wal
PRAGMA freelist_count; -- expect: small (<1% of page_count after VACUUM)
PRAGMA integrity_check; -- expect: ok
```

```powershell
(Get-Item "C:\Users\jmlus\.local\share\opencode\opencode.db-wal").Length / (Get-Item "C:\Users\jmlus\.local\share\opencode\opencode.db").Length  # expect < 0.10
```

**Rollback:** checkpoint/VACUUM is not reversible and must not be. If integrity fails after a checkpoint, restore from the §12 snapshot and escalate — do not retry VACUUM on a suspect DB.

### 9.2 Retention + archive job (F-10) — 30-day rule

**Policy:** 30 days for `part`/`message`/`session_message` **bodies**; session **metadata** (id, project, agent, timestamps, token counts) retained 12 months for auditability with no content. The job runs weekly; every run emits a log line (rows archived, rows purged, DB size before/after).

**Archive mechanism (no in-place body edits):** move bodies out of the live DB into a cold archive DB (same schema, encrypted volume per F-02), then delete from live and `VACUUM`. Pseudocode:

```sql
-- 1. Identify expired bodies (bodies only; session rows stay):
--    sessions older than 30 days in session / session_v2:
SELECT id FROM session     WHERE time_created < (strftime('%s','now','-30 days') * 1000);
SELECT id FROM session_v2  WHERE time_created < (strftime('%s','now','-30 days') * 1000);
-- 2. Copy part/message/session_message rows for those sessions into the cold DB (.backup / ATTACH).
-- 3. Set session.time_archived + session_v2.time_archived (baseline: 0 archived — this job creates the first).
-- 4. DELETE body rows for archived sessions from the live DB.
-- 5. PRAGMA wal_checkpoint(TRUNCATE); VACUUM;
-- 6. Log: archived=N, purged=M, size_before, size_after. Alert if size_after > 1 GiB.
```

**Project GC:** delete the 67 session-less `project` rows (worktree/temp sprawl) older than 30 days; keep the 5 projects that ever hosted sessions. `SELECT COUNT(*) FROM project WHERE id NOT IN (SELECT DISTINCT project_id FROM session); -- expect: 67 at baseline`.

**Acceptance criteria:** live DB consistently < 1 GiB; no plaintext `.bak` older than the retention window; `time_archived IS NOT NULL` > 0 and growing weekly; 67 session-less projects removed.
**Verification (read-only):**

```sql
SELECT COUNT(*) AS sessions_older_than_30d FROM session
WHERE time_created < (strftime('%s','now','-30 days') * 1000)
  AND time_archived IS NULL;   -- expect: 0 after the first run
SELECT COUNT(*) AS unarchived_bodies FROM part p
JOIN session s ON s.id = p.session_id
WHERE s.time_archived IS NULL AND s.time_created < (strftime('%s','now','-30 days') * 1000);
-- expect: 0
```

**Rollback:** the archive is the rollback — purged bodies are recoverable from the cold DB within its retention. If the job mis-fires (wrong cutoff), stop the scheduler, restore bodies from the cold archive by `session_id`, and re-run with a corrected cutoff. Live-DB deletes without a cold copy are forbidden (the job's step 2 is mandatory).

### 9.3 Stale artifacts (F-11)

| Artifact | Action | Verification |
|---|---|---|
| `opencode-.db` (765 KB, 2026-10-30, v1-shim) + `-wal`/`-shm` | Delete after F-09 proves v2 stable (no deep audit was done — if table `.tables` shows unique transition data, cold-archive first) | `Test-Path` False |
| `C:\Users\jmlus\AppData\Local\Temp\opencode` (31,217 files; 228 in last 7 days) | Purge files older than 7 days; add a weekly sweeper | `(Get-ChildItem Temp\opencode -Recurse -File).Count` drops to freshness window |
| `log\opencode.log` (80.6 MB) | Enable log rotation (size cap + retain 3) | file size bounded |
| `kv.models-dev:v2:catalog` (11 MB) | TTL-cull on catalog refresh if the provider allows | `SELECT LENGTH(value) FROM kv WHERE key='models-dev:v2:catalog'` bounded |

---

## 10. Injection quarantine (F-12 → R6)

**Risk (LLM01/LLM07):** 3,412 `ignore%prior%`, 2,162 `override%instruction%`, 2,077 `system prompt%`, 317 `jailbreak` hits sit in the same store the harness recalls from. Benign security research dominates by volume — the control must quarantine without destroying legitimate research.

**Mechanism:** a `quarantine` flag (new column or sidecar table keyed by `(session_id, part_id)`) set by a read-only tagging job; the `## Relevant Past Work` injector excludes quarantined rows. Human review re-admits benign research (flag → cleared with reviewer + date).

**Tagging patterns (counts only, mirrors the audit):**

```sql
-- Candidates (read-only; run against a snapshot, not the live WAL):
SELECT COUNT(*) FROM part WHERE data LIKE '%ignore%prior%' OR data LIKE '%ignore%previous%';
SELECT COUNT(*) FROM part WHERE data LIKE '%override%instruction%' OR data LIKE '%system prompt%';
SELECT COUNT(*) FROM part WHERE data LIKE '%jailbreak%' OR data LIKE '%disregard%' OR data LIKE '%ignore all%' OR data LIKE '%new instructions%' OR data LIKE '%you are now %';
-- Baseline: 3,412 / 1,853 / 2,162 / 2,077 / 317 … (see security audit §5).
```

**Acceptance criteria:** injector query provably excludes quarantined rows (unit test with a synthetic flagged row); re-admission requires a named reviewer + date; v2 sessions (which already show 158 `ignore%prior%` in 7 days) are covered.
**Verification (read-only):**

```sql
-- Quarantined rows must be 0 in the injector's source set:
SELECT COUNT(*) FROM part p
WHERE p.quarantined = 1
  AND p.session_id IN (SELECT session_id FROM part WHERE ...)  -- injector scope check
  AND EXISTS (SELECT 1 FROM part q WHERE q.session_id = p.session_id); -- shape placeholder — see implementation
-- Simpler gate: the injector's candidate query returns 0 quarantined rows by construction (NOT EXISTS anti-join).
```

**Rollback:** quarantine is additive (a flag, never a delete). Rollback = clear the flag by review batch; never purge quarantined content — it is evidence.

---

## 11. Consolidated verification matrix

Re-run after each phase. All queries are `sqlite3 -readonly`; hostnames/counts only, never values or full URLs.

| Check | Command / query | P0 pass | P1 pass | P2 pass |
|---|---|---|---|---|
| ACL clean | `icacls` on dir + DB + `.bak` + auth JSONs | no `…-1003` | — | persists |
| At rest | `cipher /c opencode.db` / `manage-bde -status` | `E` or BitLocker On | — | persists |
| `.bak` | `Test-Path opencode.db.bak` | False (or EFS cold archive) | — | no plaintext >30 days |
| Credentials | `SELECT label, LENGTH(value) FROM credential` (names/lengths only) | post-rotation count/lengths, values never printed | — | — |
| Redaction (new data) | `SELECT COUNT(*) FROM part WHERE time_created > now-24h AND (data LIKE '%sk-%' …)` | — | ≈0 | ≈0 |
| Read-deny (new data) | `.env` read count, last 7 days | — | 0 | 0 |
| webfetch hygiene | userinfo / third-party-`http` / resend+composio counts, last 7 days | — | all 0 | all 0 |
| Vendor sign-off | `docs/APPROVED-VENDORS.md` rows | — | present or tools removed | current (≤90 days) |
| WAL / size | `PRAGMA wal_checkpoint; PRAGMA integrity_check;` + file-size ratio | — | 0 frames / `ok` / WAL <10% | DB <1 GiB, retention enforced |
| Retention | `time_archived` count + unarchived-old-bodies count | — | — | >0 / 0 |
| Quarantine | injector candidate set contains 0 quarantined rows | — | — | 0 |

Security review checklist (from the skill), opencode.db-specific pass:
- [ ] No secrets in `part.data` new writes (F-05) and no `.env`/auth/DB reads by agents (F-06)
- [ ] Least privilege at rest (F-01) + encryption (F-02)
- [ ] Server-side URL fetches allowlisted — no SSRF to internal services (F-07)
- [ ] LLM output treated as untrusted: tool permissions enforced in code, secrets kept out of the recall loop (F-05/F-06/F-12)
- [ ] New external integrations (Resend/Composio) approved before use (F-08)
- [ ] Retention + erasure enforced with an audit log (F-10)

---

## 12. Snapshot, sequencing, and rollback discipline

**Before any DB-mutating step (F-09/F-10):**

```powershell
# Controlled snapshot (OpenCode closed). Keep outside the workspace, encrypted, off the data volume.
& C:\sqlite\sqlite3.exe "C:\Users\jmlus\.local\share\opencode\opencode.db" ".backup 'C:\secure-archive\opencode-pre-fix-2026-11-08.db'"
```

`.backup` is preferred over a filesystem copy (WAL-consistent). Verify the snapshot (`PRAGMA integrity_check` → `ok`) before mutating. The snapshot is itself secrets-bearing (F-02 covers it: encrypted volume, owner-only ACL) and is pruned with the retention window (F-10).

**Sequence:**
1. F-01 ACL (safe, no restart) → F-02 encryption (needs reboot for BitLocker) → F-03 `.bak` disposal.
2. F-04 rotation (provider consoles; no DB mutation needed) → F-05 redaction (code/config) → F-06 read-deny (config) — verify each with the §11 queries before proceeding.
3. F-07/F-08 egress (config + vendor decision) → F-09 checkpoint (maintenance window, snapshot first).
4. F-10 retention (snapshot first; cold archive before any delete) → F-11 purge → F-12 quarantine (additive flag only).

**Per-task rollback is defined in §§4–10.** Global rule: **no task rolls back by re-exposing data** (never restore `.bak`, never un-rotate a key, never clear quarantine without review). If a fix fails, the rollback state is *the pre-fix snapshot under owner-only ACL on an encrypted volume* — which is strictly safer than the current plaintext posture.

**Escalation:** any rollback that re-opens R1/R2, any vendor sign-off dispute, or any `integrity_check` failure → CISO escalates to the Human CEO (CISO of record) per `AGENTS.md` §9.2; urgent operational issues coordinate via the Chief of Staff.

---

*End of plan. No secret values in this file. Counts and hostnames only, per the §9.2 transmission discipline.*
