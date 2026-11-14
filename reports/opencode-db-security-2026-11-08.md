# opencode.db Security Audit — 2026-11-08

**Auditor:** ciso (CISO) for LightSpeed Holdings
**Working directory:** `C:\Users\jmlus\light-speed-holdings`
**Database audited (read-only):** `C:\Users\jmlus\.local\share\opencode\opencode.db`
**Audit date (local):** 2026-11-08
**Method:** `sqlite3 -readonly` only (`C:\sqlite\sqlite3.exe` 3.50.4, SQLite 3.50.4) + filesystem `Get-ChildItem` / `icacls` / `cipher`. **No writes to the database.** Every `sqlite3` invocation used `-readonly`. **No secret values were read, dumped, or reproduced in this report — counts and hostnames only.** Queries that list identifiers return key/type/host names and value *lengths*, never values.
**Companion analytics (not this report):** `reports/opencode-db-audit-2026-11-08.md` (chief-of-staff locate/size/integrity audit, same day). This report is the security slice: exposure, transmission, retention, permissions, injection. It does not duplicate the full schema dump.
**Live-DB drift:** the DB grew during the audit (new sessions created by the audit session itself). Row counts are a point-in-time snapshot; `session_v2` moved 91 → 97 between queries. Variances are expected live-DB drift, not errors.

> **Read-only compliance:** No `INSERT/UPDATE/DELETE/VACUUM/CREATE` was issued. No WAL checkpoint was forced. No file was copied. All content queries are `SELECT COUNT(*) … LIKE …` / `json_extract(...,'$.type'|'$.tool')` aggregates, or `LENGTH()`/`datetime()` metadata. URL-host extraction strips path/query/fragment/port in SQL and returns *hostnames with counts only* — full URLs, query strings, and userinfo are never printed.

---

## 0. Inventory — what was audited

| File | Bytes (decimal) | LastWrite (evidence) | In scope |
|---|---|---|---|
| `C:\Users\jmlus\.local\share\opencode\opencode.db` | 3,222,466,560 (≈3.00 GiB) | 2026-11-08 14:01:10 (live) | ✅ audited (read-only) |
| `opencode.db-wal` | 3,163,682,112 (≈2.95 GiB) | 2026-11-08 14:01:11 (live) | ✅ measured |
| `opencode.db-shm` | 32,768 | 2026-11-08 12:38:29 | measured |
| `opencode.db.bak` | 38,533,844,992 (≈35.89 GiB) | 2026-11-01 16:56:41 | ✅ measured (backup sprawl) |
| `opencode-.db` + `-wal` (980,592) + `-shm` (32,768) | 765,952 | 2026-10-30 09:30:53 | listed only (stale v1-shim, per companion audit) |
| `auth.json` | 2,051 | 2026-10-26 22:34:24 | size/ACL only — **contents not inspected** |
| `mcp-auth.json` | 1,412 | 2026-10-22 13:11:52 | size/ACL only — **contents not inspected** |
| `log\opencode.log` | 84,500,966 (≈80.6 MB) | live | size only |
| `storage\`, `tool-output\`, `worktree\`, `repos\`, `shell\` | — | Sep–Nov 2026 | existence only |

**Effective exposure footprint ≈ 44.9 GB** (live DB + WAL ≈ 6.4 GB, plus 38.5 GB `.bak`). The `.bak` alone is ~12× the live DB.

**Creation / retention span:** DB created 2026-08-05 21:38:37. Old-schema content (session/message/part) spans **2026-08-05 → 2026-10-22 (77 days)**. Current v2 content spans **2026-11-01 → 2026-11-08**. Total corpus ≈ **95 days of raw trajectories**.

**Pragmas (proof):** `page_count=786735`, `page_size=4096`, `freelist_count=1863` (~7.6 MB free — **not** bloat; the DB is full of live trajectory rows), `journal_mode=wal`, `integrity_check=ok`.

---

## 1. File permissions and at-rest protection

### 1.1 ACLs (`icacls` / `Get-Acl`, evidence 2026-11-08)

All of `opencode.db`, `opencode.db.bak`, `auth.json`, `mcp-auth.json`, and the parent `.local\share\opencode` directory share the same effective ACL (inherited, marked `(I)` = inherited):

| Principal | Rights | Access |
|---|---|---|
| `JRMTHINKPAD\jmlus` (SID `…-1001`, the owner) | FullControl (F) | Allow |
| `NT AUTHORITY\SYSTEM` | FullControl (F) | Allow |
| `BUILTIN\Administrators` | FullControl (F) | Allow |
| `S-1-5-21-2913538908-3024988640-2666040046-1003` (unresolved SID) | **ReadAndExecute (RX)** | Allow |

- Parent directory carries `(OI)(CI)` inheritance, so every child (DB, WAL sidecars, `.bak`, `auth.json`, `mcp-auth.json`, `log\opencode.log`) inherits the `…-1003` RX entry.
- `whoami /user` confirms the audit ran as `jrmthinkpad\jmlus (…-1001)`. `Get-CimInstance Win32_UserAccount` lists only `Administrator (…-500)`, `jmlus (…-1001)`, `WsiAccount (…-1002)`, plus built-ins — **no `…-1003` account exists**. `ProfileList` has profiles for `…-1001` and `…-1002` only. `…-1003` is an **orphaned/stale ACE** (deleted user, renamed account, or prior profile) that still grants read+execute on the entire trajectory store.
- No Deny ACEs were observed. No explicit owner-only lockdown was observed.

**Risk:** any principal able to assume `…-1003` (or any future account that Windows reassigns that RID on this machine — unlikely but possible on a shared laptop) or any process running as that SID can read the full corpus, including credentials and the 38.5 GB backup, without elevation. Even without reassignment, a stale allow-right on a credential-bearing store fails least-privilege and will confuse future reviewers ("who is 1003?").

### 1.2 Encryption at rest

- `cipher /c` reports `opencode.db` as **unencrypted (`U`)** — no EFS. New files in the directory are not encrypted.
- SQLite plain-file storage has **no built-in at-rest encryption** unless a codec (SQLCipher) is in use; the audited file is a plain SQLite database (`integrity_check=ok`, readable by `sqlite3 -readonly`). **Protection rests solely on NTFS ACLs.**
- The `credential` and `account` tables carry token column names (`credential.value`, `account.access_token`, `account.refresh_token`) by design. **Whether `credential.value` is additionally encrypted at the application layer cannot be determined from counts alone, and this audit deliberately did not inspect values to find out.** Treat all 22 credential rows as plaintext-at-rest until OpenCode vendor documentation or a DPAPI/key-provider check proves otherwise.

### 1.3 Adjacent token files (metadata only)

- `auth.json` (2,051 B) and `mcp-auth.json` (1,412 B) sit in the same directory under the same inherited ACLs. Their **contents were not read**. File names and sizes are consistent with stored auth tokens. They inherit the same `…-1003` RX exposure as the DB and must be treated as High sensitivity by proximity.

---

## 2. Sensitive data exposure — keyword counts only (no values dumped)

**Scope as requested:** `part.data` searched for `sk-`, `api[_-]?key`, `secret`, `password`. Results below are **keyword hits, not confirmed live credentials**. High counts are expected because the corpus includes code, config references, env-var names, RBAC key documentation, and security research — *and* because `tool` parts store command output (e.g., `.env` reads, config reads, grep results) that can embed live values. The audit cannot distinguish "mention of `api_key`" from "value of `API_KEY=…`" without sampling values, which it refuses to do. Treat every pattern as **potentially-plaintext credential material in the DB** until a redaction pass proves otherwise.

### 2.1 Raw pattern counts

| Pattern (SQL `LIKE`, ASCII case-insensitive) | `part` rows hitting | Distinct sessions hit |
|---|---|---|
| `%sk-%` | **12,747** | **2,000 / 3,131 (64%)** |
| `%secret%` | **12,524** | 1,939 (62%) |
| `%password%` | **2,195** | 838 (27%) |
| `%api_key%` | **15,288** | 1,914 (61%) |
| `%api-key%` | 5,223 | — |
| `%apikey%` | 879 | — |

Table totals for context: `part=670,664`, `message=153,182`, `session=3,131`, `session_v2≈97 (live)`, `session_message=9,194`, `session_part=0`, `todo=2,771`, `credential=22`, `account=0`, `kv=5`, `blob=0`.

Other text columns (same four patterns, `msg=`/`sm=` prefixes):

| Pattern | `message` rows | `session_message` rows (v2, 7 days only) |
|---|---|---|
| `%sk-%` | 3,086 | 345 |
| `%secret%` | 982 | 213 |
| `%password%` | 240 | 45 |
| `%api_key%` | 1,078 | 280 |

Even a 7-day v2 window already accumulates hundreds of hits per pattern — the exposure is **ongoing, not legacy-only**.

### 2.2 Where the hits live (by `part` type — `json_extract(data,'$.type')`, safe field)

`part` type distribution (total 670,664): `tool 188,713` · `step-start 135,963` · `step-finish 132,342` · `reasoning 119,892` · `text 73,820` · `patch 13,579` · `compaction 5,444` · `agent 767` · `file 144`.

Breakdown by type (hits concentrate in **`tool`** — i.e., tool inputs *and* captured tool outputs):

| Pattern | `tool` | `text` | `reasoning` | `patch` |
|---|---|---|---|---|
| `%sk-%` | **8,793** | 1,944 | 1,880 | 130 |
| `%secret%` | **8,539** | 1,749 | 2,160 | 76 |
| `%password%` | 1,595 | 351 | 249 | — |
| `%api_key%` | **10,641** | 1,803 | 2,770 | 74 |

**Interpretation:** assistant `text`/`reasoning` discussion alone would be Medium risk (model can echo context). Dominance of `tool` parts is worse: captured `bash`/`read`/`grep` outputs are stored verbatim in `part.data` and survive in the 1.8 GB `part` payload (see §4). A single compromised backup therefore replays every `.env`/config read in the window.

### 2.3 Credential-bearing tables (lengths only, never values)

- `credential`: **22 rows**. Value lengths: avg **119 B**, max **651 B** — sizes consistent with API keys/tokens. Labels are generic and duplicated (10× "API key" sharing timestamp `2026-10-22 11:24:59`, consistent with a bulk import/migration; plus single rows labelled `Groq`, `Cohere`, `Google`, `Ollama (local)`, `Default`, and 6× `OpenCode Console*` dated 2026-10-28 → 2026-11-03). **Values were never selected.**
- `account`: **0 rows** (tokens live in `auth.json` / `credential` instead).
- `kv`: **5 rows, 10.8 MB total** — one value is **11,273,128 B** (`models-dev:v2:catalog`, 2026-10-27; a model catalog cache, not a secret, but it means the KV store retains large opaque blobs). Other keys (names only): `migration.v1-v2` (21 B), `websearch:provider` (8 B), `plugin:…:model-has-image-support` (5 B), `models-dev:v2:catalog:meta` (176 B).

### 2.4 Agent access to credential files (counts only)

| Action (read-only query on `part`) | Count |
|---|---|
| `read` tool targeting a `*.env` path (`…filePath LIKE '%.env%'`) | **309** reads |
| `read` tool targeting `*auth.json*` | 1 |
| `read` tool targeting `*opencode.db*` | 0 |
| `bash` parts mentioning `.env` / `Get-Content …env…` | **4,394** |
| `bash` parts mentioning `opencode.db` / `auth.json` | **218** |

The agent routinely reads `.env` files, and 218 shell parts touch the DB/auth paths (audit probes such as this one account for some, but the baseline is a standing ability to ingest live credential material into trajectories). Combined with §2.1, **the DB must be classified as a secrets-bearing store**, even where individual keyword hits are benign mentions.

### 2.5 Large-payload tails

- `part.data` total **1,820.0 MB**, avg **2,846 B**, max **4,912,367 B** (~4.7 MB single part).
- `message.data` total **786.0 MB**, avg **5,385 B**.
- `session_message.data` total **55.0 MB**, avg **6,293 B**.
- Parts >100 kB: **1,337** (1153 `tool`, 83 `patch`, 47 `file`); parts >1 MB: **28**. Tool outputs dominate the tails — exactly where embedded file/config dumps live.

---

## 3. Third-party transmission traces

**Question:** what left the machine, to which hosts, over which channels — and in what form? Hostnames below are aggregated from `$.state.input.url` with path/query/port stripped in SQL. **No full URLs, query strings, or userinfo values are reproduced.**

### 3.1 `webfetch` tool calls — 745 calls, 744 with URLs, 141 distinct hosts

Tool census (`json_extract(data,'$.tool')`, 188,713 `tool` parts): `bash 78,923` · `read 52,581` · `edit 16,540` · `grep 15,156` · `glob 11,810` · `websearch 830` · **`webfetch 745`** · plus `question`, `skill`, `task`, etc. `webfetch` input keys: `url, format`. `websearch` input keys: `query, numResults` (queries go to the provider — content not inspected).

Webfetch URL hygiene (744 URLs):

| Property | Count | Note |
|---|---|---|
| `https://` | **727** | |
| `http://` | **17** | **all 17 are localhost / private / first-party** (see below) — no plain-HTTP egress to third parties observed |
| Non-http(s) (`file:`, `data:`, `ftp:`) | 0 | all URLs are http(s) |
| URLs with userinfo (`user:pass@host`) | **8** | credential-in-URL risk — URLs themselves not reproduced |
| URLs with query string (`?`) | **93** | query tokens can leak to the host |
| URLs containing `localhost` | **13** | internal fetch |
| `10.*` / `192.168.*` / `169.254.169.254` (crude `LIKE`) | 0 | no cloud-metadata hits observed |

Top webfetch hosts (host + count, query/port stripped):

| Host | Count | Host | Count |
|---|---|---|---|
| `raw.githubusercontent.com` | 98 | `r.jina.ai` | 15 |
| `foaster.ai` | 70 | `eden.so` | 15 |
| `github.com` | 53 | `www.webuild-ai.com` | 14 |
| `opencode.ai` | 37 | `huggingface.co` | 14 |
| `resend.com` | 34 | `localhost` | 13 |
| `api.github.com` | 28 | `careersmw.com` / `lightspeedholdings.vercel.app` | 13 / 12 |
| `www.linkedin.com` | 20 | `developers.notion.com` | 10 |
| `www.bcg.com` | 17 | … | … |
| `html.duckduckgo.com` | 16 | 141 distinct hosts total | |

All 17 `http://` fetches target: `localhost:1441 (9)`, `localhost:4173 (3)`, `localhost:3000 (1)`, `127.0.0.1:8420 (1)` (CEO Dashboard production port), `172.30.96.1:1440/1441 (1 each)` (private WSL/Docker IP, Vite ports), `lightspeedholdings.ai (1)`. Singleton internal hosts also include `localhost:3000`. **No third-party plain-HTTP egress was observed; the 8 userinfo URLs and 93 query-string URLs remain the transmission concern** — a token in either form is delivered to the target host and stored in `part.data` in the clear.

### 3.2 Other external tool traffic

| Tool family | Calls | What leaves the machine | Audit note |
|---|---|---|---|
| `websearch` / `google_search` | 830 / 2 | free-text queries (+ provider metadata) | query text not inspected; treat as PII-adjacent |
| `resend_*` | ~35 (`list-contacts 5`, `create-contact 5`, `create-broadcast 5`, `add-contact-to-segment 5`, `list-segments 4`, `list-domains 4`, `create-domain 2`, `verify-domain/send-email/get-*/list-api-keys 1 each`) | contact PII, segments, domain config, and — via `resend_list-api-keys` (1 call) — **API-key material via a third-party tool** | input keys observed are `context, llm_model, conversation_id` only (values not inspected). Any `list-api-keys` output captured in `part.data` is a high-value secret artifact. |
| `composio_*` | ~27 (`MULTI_EXECUTE_TOOL 13`, `SEARCH_TOOLS 5`, `MANAGE_CONNECTIONS/GET_TOOL_SCHEMAS 3 each`, …) | tool-routing payloads to Composio | `MULTI_EXECUTE_TOOL` input keys: `tools, sync_response_to_workbench, current_step, current_step_metric` (values not inspected). |
| `agents_vm_exec` / `agents_*` | 19 / ~250 | remote-execution and orchestration calls | `agents_vm_exec` (19) is an execution-boundary crossing — command content not inspected. |

Against AGENTS.md §9.2 (Skill Third-Party Transmission Ban — local code/diffs/docs/prompts/memory to third-party hosts only if the vendor is allow-listed in `docs/APPROVED-VENDORS.md` within its 90-day window): **this audit did not cross-check Resend/Composio/Google against the allowlist and makes no compliance claim.** That cross-check is a required follow-up (see Recommendations).

### 3.3 Shell egress (a second, larger transmission channel)

`bash` tool parts (78,923): `curl 718` · `Invoke-WebRequest 1,121` · `Invoke-RestMethod 529` · any `https://` 6,704 · any `http://` 3,681. Most of this is legitimate `gh`/npm/package/registry traffic, but it means **webfetch counts understate total egress by an order of magnitude**. A transmission control that only governs `webfetch` will miss the dominant channel. Output bodies (which can contain set-cookie, tokens, or fetched page content) are retained in `part.data` alongside inputs.

---

## 4. Data retention size and privacy risk (raw trajectories)

| Measure | Value (evidence) |
|---|---|
| Live DB | **3.00 GiB** (786,735 × 4 KiB pages) |
| WAL | **2.95 GiB** (98% of DB size — checkpoint severely behind) |
| `.bak` backup | **35.89 GiB** (Nov 1 — 12× live DB; single full copy of ~95 days of history) |
| `part` payload | **1,820 MB** / 670,664 rows |
| `message` payload | **786 MB** / 153,182 rows |
| `session_message` payload | **55 MB** / 9,194 rows |
| `dbstat` top consumers | `part 2,055 MB` (+indexes ~95 MB), `message 813 MB`, `session_message 64 MB`, `kv 11 MB`, `instruction_blob 4.3 MB (373 cells)` |
| Retention span | **2026-08-05 → 2026-11-08 (~95 days)**, 3,131 old sessions (Aug 938 / Sep 1,038 / Oct 1,155) + ~97 v2 sessions (Nov) |
| Archive enforcement | **0** archived sessions (`time_archived IS NOT NULL` = 0 in both schemas) |
| Project sprawl | **72 `project` rows** (main `light-speed-holdings` + 70 worktree/temp projects; per companion audit, only 5 projects ever had sessions) |

**Privacy assessment:** the DB is a **verbatim, timestamped, project-linked record of every prompt, reasoning trace, tool input/output, patch, and file read** for 95 days — including 309 `.env` reads, personal paths, job-search content (`careersmw.com`, `ntchito.com`, `jobs.mw` hosts in webfetch), and security-research prompts. It is the functional equivalent of a full session recorder with no redaction layer. Consequences:

1. **Breach blast radius = 44.9 GB**, not 3 GB. The `.bak` and WAL each independently reconstitute the corpus.
2. **Right-to-erasure / GDPR risk:** no per-session purge is evidenced; freelist is only 7.6 MB, so *deleted* rows are not the problem — *retained* rows are. There is no archive or expiry job (0 archived).
3. **Memory-system ingestion risk:** trajectories containing prompt-injection phrases (§5) and secrets (§2) are the same store the harness recalls from. Unfiltered recall can re-surface live credentials into future prompts (LLM02/LLM07) — the exact failure mode `security-and-hardening` warns against ("Keep secrets and other users' data out of prompts").

---

## 5. Anomalies — prompt injection and internal-fetch patterns

**Method:** counts only, patterns chosen as standard injection probes. Hits are **keyword frequencies, not confirmed attacks**. Much of the volume is clearly benign (security research, red-team playbooks, skill documentation, AGENTS.md/operating standards that themselves contain "system prompt", "override", "ignore prior" guidance). The finding is therefore **exposure of untrusted instruction-like content at scale in a store that is also a memory source**, not a claim of compromise.

| Pattern (`%…%` LIKE on `part.data`) | `part` rows | `message` rows | Distinct `part` sessions |
|---|---|---|---|
| `%ignore%prior%` | **3,412** | 730 | 1,182 |
| `%ignore%previous%` | 1,853 | — | — |
| `%override%instruction%` | 2,162 | — | — |
| `%system prompt%` | **2,077** | 384 | 768 |
| `%jailbreak%` | 317 | 253 | — |
| `%new instructions%` | 129 | — | — |
| `%ignore all%` | 56 | — | — |
| `%disregard%` | 32 | — | — |
| `%you are now %` | 22 | — | — |
| `%DAN mode%` | 0 | — | — |

By type, `%ignore%prior%` splits `tool 2,056` / `reasoning 737` / `text 619`; `%system prompt%` splits `reasoning 989` / `tool 892` / `text 196` (i.e., the model is *discussing* system prompts in reasoning traces — the most echo-prone location). Session-message (v2, 7 days) already shows `ignore%prior% 158` and `system prompt% 150` — the pattern persists into the current schema.

**Internal-fetch anomalies (from §3.1, restated for the anomaly register):** 13 `localhost` webfetch URLs, `127.0.0.1:8420` (dashboard prod port), `172.30.96.1:1440/1441` (private IP). In context these are almost certainly dev-server probes (Vite on 1440/1441 per AGENTS.md §12), **not** SSRF attacks. They are logged here because the same capability (`webfetch` + `bash` `Invoke-WebRequest` 1,121) can reach any internal service — the audit found no metadata-endpoint (`169.254.169.254`) or `file:`/`data:` scheme abuse, but the channel is unconstrained.

**No evidence of a successful breach** was sought or found: this audit did not inspect whether any injection phrase was *acted on*, and `state.status` distribution for `tool` parts (`completed 185,183` / `error 3,435` / `running 93` / `pending 2`) shows no anomaly. Do not read §5 counts as "3,412 attacks". Read them as "3,412 places where instruction-overriding language sits in the retained record".

---

## 6. Prioritized risks

| # | Severity | Risk | Evidence | Exploit / impact path |
|---|---|---|---|---|
| **R1** | 🔴 **P0 — Critical** | Unencrypted credential-bearing store (22 `credential` rows + `auth.json` + trajectories) protected only by NTFS ACLs, plus a 38.5 GB plaintext backup | DB 3.00 GiB + WAL 2.95 GiB + `.bak` 35.89 GiB, `cipher=U`, `credential=22` (avg 119 B) | Laptop theft, backup copy/attach, malware read, or ACL misassignment ⇒ full 95-day corpus + API keys in one file |
| **R2** | 🔴 **P0 — Critical** | Secrets plausibly embedded verbatim in tool outputs across 64% of sessions; agent routinely ingests live credentials | `sk- 12,747` / `api_key 15,288` (2000/1914 sessions), `read .env 309`, `bash env 4,394`, `bash db/auth 218` | Any R1 disclosure or any future memory-recall poisoning re-surfaces live values; rotation scope is "every key ever seen by the agent" |
| **R3** | 🟠 **P1 — High** | Orphaned SID `…-1003` holds inherited **RX** on DB, `.bak`, and both auth JSONs | `icacls` on file + parent; SID has no live account/profile | Latent unauthorized read; RID-reuse or profile confusion would silently grant access; fails least-privilege audit |
| **R4** | 🟠 **P1 — High** | Unconstrained egress: `webfetch` (141 hosts, 8 userinfo URLs, 93 query-string URLs) + shell `IWR 1,121 / curl 718 / IRM 529` + Resend/Composio/Google routing | §3 counts; `resend_list-api-keys 1`, `composio_MULTI_EXECUTE 13` | Token-in-URL/query ⇒ host logging leaks secrets; shell egress bypasses any webfetch-only control; third-party transmission ban (§9.2) unverified |
| **R5** | 🟡 **P2 — Medium** | No retention, archive, or erasure enforcement: 0 archived sessions, 95-day verbatim retention, 72 projects, WAL checkpoint ~98% behind | `time_archived=0`, span Aug 5–Nov 8, `wal 2.95 GiB` | GDPR/erasure non-compliance; `.bak`+WAL duplication doubles retention; crash-consistent recovery relies on an un-checkpointed WAL |
| **R6** | 🟡 **P2 — Medium** | Prompt-injection language at scale in a memory-sourced store | `ignore%prior% 3,412`, `system prompt% 2,077`, `jailbreak 317`, split across `tool/reasoning/text` | Poisoned recall into future sessions (LLM01/LLM02/LLM07); reasoning-trace discussion maximizes echo risk |
| **R7** | 🟢 **P3 — Low** | Opportunistic items: 11 MB KV catalog blob, 80 MB log, stale `opencode-.db` shim, internal-host fetches without allowlist | `kv 10.8 MB`, `log 80.6 MB`, `opencode-.db 765 KB`, localhost/private fetches §3.1 | Minor bloat/confusion; internal fetches are dev probes, not attacks, but are unlogged as exceptions |

---

## 7. Recommendations (in priority order)

### P0 — do now

1. **Remove the orphaned ACE and lock down ACLs to owner-only.**
   `icacls "C:\Users\jmlus\.local\share\opencode" /remove "S-1-5-21-2913538908-3024988640-2666040046-1003"` (and the same for `C:\Users\jmlus\.local` parent if inherited there), then `icacls <path> /inheritance:r`. Verify with `icacls` that only `jmlus`, `SYSTEM`, `Administrators` remain. Re-check after any profile creation.
2. **Classify the DB + `.bak` + `auth.json` as secrets-bearing and encrypt at rest.**
   Enable BitLocker (preferred, whole-volume) or EFS on `opencode.db*`, `auth.json`, `mcp-auth.json`. Move `opencode.db.bak` (38.5 GB) into encrypted storage or delete it after verifying a restore; never leave a second plaintext copy beside the live DB. Record the decision in `docs/governance-audit.md` if root-config-adjacent.
3. **Determine whether `credential.value` is encrypted; rotate if plaintext.**
   Consult OpenCode vendor docs / source for the credential provider (DPAPI vs plaintext). Until proven encrypted, **rotate all 22 `credential` values and the `auth.json`/`mcp-auth.json` tokens** — assume any key the agent ever read (`.env` ×309, `bash env` ×4,394) may be in the corpus. Rotation covers, at minimum, provider keys labelled `API key`, `Groq`, `Cohere`, `Google`, `OpenCode Console*`, plus `.env` values visible to `read`/`bash`. (This audit did not inspect values; rotation scope is therefore "everything reachable", not a value-level list.)
4. **Stop ingesting credentials into trajectories.**
   Deny the `read` tool and `bash` file-reads on `.env*`, `auth.json`, `mcp-auth.json`, `opencode.db*` (filesystem policy, not prompt policy). Apply a pre-persistence redaction filter over `part.data` (patterns: `sk-…`, `api[_-]?key\s*[:=]`, `secret`, `password`, `AKIA…`, `ghp_…`, `xox[baprs]-…`, `Bearer …`, `BEGIN … PRIVATE KEY`) that replaces the *value* with `[REDACTED]` before insert. Backfill the filter for any future vacuum run (do not edit history in place without a migration + audit note).

### P1 — do this week

5. **Put egress behind an allowlist; fix URL hygiene.**
   `webfetch`: deny `http://` except `localhost/127.0.0.1/private-test` (all 17 current `http` uses already qualify — enforce it), **reject URLs containing userinfo (`@`)** (8 observed), strip or reject query strings that look like tokens (93 observed — log host + param *names* only, never values), and keep a default-deny for `169.254.169.254`, `file:`, `data:`.
   `bash`: proxy/allowlist `Invoke-WebRequest`/`Invoke-RestMethod`/`curl` to approved package/registry hosts; alert on private-IP egress beyond the known dev ranges (`172.30.96.1:1440/1441`, `127.0.0.1:8420`).
6. **Verify third-party transmission against AGENTS.md §9.2 before further use.**
   Cross-check `resend_*`, `composio_*`, `google_search`/`websearch` providers against `docs/APPROVED-VENDORS.md` and its 90-day windows. Suspend any non-approved tool (notably `resend_list-api-keys` / `resend_send-email` / `composio_MULTI_EXECUTE_TOOL`) pending CEO/CISO sign-off. Log every transmission (host + tool + payload class) — never payload values.
7. **Checkpoint the WAL and shrink the live footprint.**
   `PRAGMA wal_checkpoint(TRUNCATE)` via a controlled maintenance window (not during live sessions), then `VACUUM` (with a space check — VACUUM needs ~DB-size free space) to reclaim the 7.6 MB freelist and compact `part` indexes (~95 MB). Investigate why the WAL grew to 98% of DB size (long-running transaction / backup copy holding the checkpoint back).

### P2 — do this month

8. **Enforce retention.**
   Set a hard retention (e.g., 30 days for `part`/`message` bodies, longer for session metadata only), schedule `time_archived` + purge jobs, and scope by project (delete the 70 temp/worktree projects that never hosted sessions). After purge, `VACUUM`. Target: live DB consistently <1 GiB, no `.bak` older than the retention window in plaintext.
9. **Quarantine injection-bearing trajectories from memory recall.**
   Tag any session/part matching `%ignore%prior|previous%`, `%system prompt%`, `%jailbreak%`, `%disregard%`, `%override%instruction%` as `untrusted-instructions` and exclude it from the `## Relevant Past Work` injector pending human review. This treats benign research correctly (reviewers can re-admit) while blocking poisoned-recall paths.
10. **Clean up stale artifacts.**
    Remove or archive `opencode-.db` (765 KB, Oct 30, v1-shim) and compress/rotate `log\opencode.log` (80 MB). Trim `kv.models-dev:v2:catalog` (11 MB) on a TTL if the catalog provider allows it.

### Verification (after remediation)

- [ ] `icacls` on DB/`.bak`/auth files shows **no `…-1003` ACE**; `cipher /c` or BitLocker shows encrypted (or volume encrypted).
- [ ] `sqlite3 -readonly` counts for §2 patterns collapse for *new* data (redaction working) — historical counts remain until retention purge; do not re-run LIKE scans that dump values.
- [ ] `webfetch` logs show 0 userinfo URLs, 0 third-party `http`, and an allowlist hit-rate report by host.
- [ ] `docs/APPROVED-VENDORS.md` sign-off exists (or tool removal) for Resend/Composio/Google.
- [ ] `PRAGMA wal_checkpoint` reports 0 frames; `journal_mode` remains `wal`; DB size <1 GiB after VACUUM + retention.

---

## 8. Methodology and limits (what this audit did *not* do)

- **Did not** `SELECT data` / `SELECT value` / read `auth.json` contents / print full URLs — by design. Every content query is a `COUNT(*)` with `LIKE`, a `json_extract(…,'$.type'|'$.tool')` grouping, a `LENGTH()`/`datetime()` metadata check, or a host-only URL parse. Hostnames and tool names are reported because they are required for transmission audit and are not secrets.
- **Did not** test whether any keyword hit is a *live* credential, any injection phrase was *acted on*, any Resend/Composio vendor is *approved*, or `credential.value` is *encrypted*. Each is flagged as an assumption/follow-up rather than asserted.
- **Did not** copy the DB, force a checkpoint, or vacuum — a read-only audit must not perturb a live WAL. Sizes and counts are therefore live-drift snapshots.
- Crude `LIKE` probes for private IPs (`%10.%`, `%192.168.%`, `%169.254.169.254%`) are **false-negative-prone** (e.g., `10.` matches many strings; IPv6/decimal-encoded IPs are missed). The "0" results mean "no hits under these probes", not "proven absent". A production egress proxy should enforce this properly.

---

*End of report. Counts and hostnames only; no secret values in this file.*
