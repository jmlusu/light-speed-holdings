# LS-MEM — Security Verification Report

**Project:** LightSpeed Holdings
**Date:** 2026-09-26
**Status:** Independent security audit complete (2026-09-26) — verdict: APPROVE-WITH-FINDINGS; pending CEO approval (§7)
**Security classification:** Internal
**Related:** `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md` §33 (source of the 20 questions), `docs/security/LS-MEM-THREAT-MODEL.md`, `docs/LS-MEM-USER-GUIDE.md`
**Locked decisions:** dual skill paths (`.agents/skills` + `.opencode/skills`); new SQLite engine + one-way bridge from the legacy JSON `MemoryStore`

**Method.** Every answer below was produced by reading the cited source line(s) and, where
behavioral, by executing it (test run or controlled smoke run) on **2026-09-26** on
Windows/PowerShell. `Evidence (code)` is `path:line`, verified by reading.
`Evidence (tests)` names real test classes/methods confirmed to exist in the suite. Where
something could not be verified, the answer says **not verified** or **not available**
rather than claiming behavior. Environment: Python 3.12, repo
`C:\Users\jmlus\light-speed-holdings`, suite run with `uv run pytest tests/memory -q -rs`.

---

## 1. Required questions (handoff §33)

### Q1 — What network requests can LS-MEM make?

**Answer.** In the default, shipped configuration: **none**. The engine performs no
socket, DNS, or HTTP activity during CRUD, search, lifecycle, rebuild, integrity, export,
or audit operations. The only network-capable code in `lsmem/` is the **optional,
disabled-by-default** Ollama embedder, whose endpoint **defaults to** a single loopback URL
(`http://127.0.0.1:11434`) but is configurable via config — today disabled, unwired, and
never invoked by the engine or CLI (Q4/Q12, corrected 2026-09-26 §6.4). The skill scripts
shell out to the local `ai-company` binary only.

- `Evidence (code)`: `src/ai_company/lsmem/vector.py:11,22-30,43` (httpx used solely for
  `http://127.0.0.1:11434`, model `nomic-embed-text`); default `enabled: False` in
  `src/ai_company/lsmem/engine.py:123-130` and `vector.py:111-114`;
  no `httpx`/`requests`/`socket` usage elsewhere in `lsmem/` (grep of `src/ai_company/lsmem`
  for `httpx|requests|urllib|socket` matches only `vector.py`); gateway default
  `enabled: False`, `src/ai_company/lsmem/gateway.py:27,44-55`.
  `OllamaVectorStore` is referenced only by `vector.py`, `lsmem/__init__.py` (export) and
  tests — not by `engine.py` or `cli.py` (grep verified 2026-09-26).
- `Evidence (tests)`: `tests/memory/test_offline.py::TestOfflineOperation`
  (`test_crud_operations_offline`, `test_search_offline`, `test_lifecycle_offline`,
  `test_rebuild_fts_offline`, `test_integrity_check_offline`);
  `tests/memory/test_offline.py::TestNetworkDeny`
  (`test_no_outbound_connections_on_remember` — patches `socket.socket` and asserts
  `connect()` never called; `test_no_dns_resolution_on_startup` — patches
  `socket.getaddrinfo`, allows only `localhost`/`127.0.0.1`/`::1`).

### Q2 — What network requests can LS-MEM never make by default?

**Answer.** By default LS-MEM can make **no** request to any host — local or remote. The
gateway's external-access block is off (`enabled: False`) with **all four data classes
denied** (`public`, `internal`, `confidential`, `restricted` → `False`), so even if a
caller attempted an egress decision it would be denied with reason "disabled".
Specifically never, by default: cloud LLM APIs (OpenAI, Anthropic, Google, DeepSeek, Kimi),
non-loopback vector databases, telemetry/telemetry endpoints, any non-loopback HTTP host,
and DNS resolution of external hosts at startup.

- `Evidence (code)`: `gateway.py:27` (`enabled: False` default),
  `gateway.py:31-38` (`data_classes_allowed` all `False`; `from_dict` fallback
  `gateway.py:56-64`), gate-1 check
  `gateway.py:139-150`; `engine.py:107-122` (default `external_access` config block with
  empty `approved_providers`/`approved_domains`/`approved_operations`);
  `test_offline.py:145-159` (no `connect()`), `test_offline.py:183-194` (no external DNS).
- `Evidence (tests)`: `tests/memory/test_integration.py::TestGatewayFiveGate::test_gate1_disabled_denies`;
  `tests/memory/test_offline.py::TestNetworkDeny::test_gateway_blocks_external_by_default`
  (asserts `allowed is False`, reason contains "disabled").

### Q3 — What dependencies were added?

**Answer.** **None.** LS-MEM introduced zero new entries to `pyproject.toml`
`[project] dependencies`. It uses only libraries the project already declared: `typer`,
`rich`, `pyyaml` (imported as `yaml`), `httpx` (already present, used only by the optional
Ollama vector store), plus the Python standard library (`sqlite3`, `json`, `hashlib`,
`re`, `pathlib`, `datetime`, `dataclasses`, `subprocess` in skill scripts).

- `Evidence (code)`: `pyproject.toml:14-35` (full dependency list — predates LS-MEM; no
  `lsmem`-specific additions); imports across `src/ai_company/lsmem/*.py` resolve to that
  list (grep of `^import |^from ` in `lsmem/`: stdlib, `typer`, `rich`, `yaml`, `httpx`,
  and intra-package `ai_company.*` only).
- `Evidence (tests)`: `pyproject.toml:42-55` (`dev` extra: `pytest`, `ruff`, `mypy`,
  `bandit`, `safety` — tooling, not runtime).
- Note: `sqlite3`, `httpx`, `cryptography` were **already** project dependencies for other
  components; LS-MEM did not add them.

### Q4 — What network behavior do those dependencies have?

**Answer.** By themselves: `typer`/`rich`/`pyyaml` are pure local libraries with **no
network behavior**. `httpx` is an HTTP client that *can* make network requests, but within
LS-MEM it is instantiated only by `OllamaVectorStore` and pointed exclusively at the
loopback URL `http://127.0.0.1:11434` (default port, configurable endpoint but default is
loopback); the embedder is `enabled: False` by default and, even if enabled, is not called
by the engine/CLI today (Q1). No dependency performs telemetry, auto-update, or phone-home
behavior in this codebase.

- `Evidence (code)`: `vector.py:11` (`import httpx`), `vector.py:22-30,43`
  (`http://127.0.0.1:11434`, model `nomic-embed-text`), `vector.py:111-114`
  (`enabled: False` default); `engine.py:123-130` (config default).
- `Evidence (tests)`: `tests/memory/test_ollama_optional.py::test_init_defaults`,
  `test_disabled_returns_empty`, `test_is_healthy_check`.

### Q5 — Where is memory stored?

**Answer.** Two independent stores:

1. **LS-MEM (current):** workspace-local SQLite at `<workspace>/.lightspeed/memory/memory.db`
   (records + FTS5 index, WAL mode) plus a separate hash-chained audit DB at
   `<workspace>/.lightspeed/memory/audit/audit.db`, optional config at
   `<workspace>/.lightspeed/memory/config.yaml`. The CLI always resolves from
   `Path.cwd()` — no global write path is used by the CLI. All of these are gitignored.
2. **Legacy JSON store (separate CLI `ai-company knowledge …`):** `<workspace>/memory/*.json`
   (and `memory/vector_index/`), also gitignored.

- `Evidence (code)`: `src/ai_company/lsmem/cli.py:30,34,51-59` (cwd, config, db, audit
  paths); `engine.py:272` (WAL), `engine.py:303` (schema creation);
  `src/ai_company/memory/engine.py:85-90` (`MemoryStore(base_dir="memory")`);
  `src/ai_company/cli/main.py:45-46` (wiring: `memory` → lsmem, `knowledge` → legacy).
- `Evidence (tests)`: `tests/memory/test_engine_crud.py` (writes/reads inside a temp
  workspace db); observed directory listing of a real smoke workspace on 2026-09-26
  (`.lightspeed/memory/memory.db`, `memory.db-wal`, `audit/audit.db`, `config.yaml`).

### Q6 — Can memory enter Git?

**Answer.** **No** — every memory file location is explicitly ignored by `.gitignore`,
and tests enforce that both the patterns exist and actually take effect (including a
history scan for accidental commits and a guard that LS-MEM source contains no
`git add`/`git commit`/`git push` commands — read-only local `git rev-parse` in
`injector.py:263-265` is permitted; corrected 2026-09-26 §6.4).

- `Evidence (code)`: `.gitignore:91-96` (`.lightspeed/memory*`, `memory.db*` etc.),
  `.gitignore:73-74` (`memory/*.json`, `memory/vector_index/`).
- `Evidence (tests)`: `tests/memory/test_git_safety.py::test_gitignore_contains_lsmem_patterns`,
  `test_gitignore_effective` (fresh repo + `git check-ignore`-style assertion),
  `test_no_memory_db_in_git_history`, `test_lsmem_code_no_git_commands`.

### Q7 — Can memory enter GitHub automatically?

**Answer.** **No automatic path exists.** LS-MEM itself has no network code (Q1), git
ignores cover every memory location (Q6), and no workflow/hook in the repo stages,
commits, or pushes memory files. `git status --porcelain` after operations shows nothing
memory-related (verified during smoke runs). A human could deliberately `git add -f` a
file — that is an explicit override outside LS-MEM's control, and the history scan test
would fail if such a commit landed.

- `Evidence (code)`: `.gitignore:91-96,73-74`; grep of `src/ai_company/lsmem/` and
  `.agents/skills/ls-memory/` for `git push|git commit|git add` → no matches (verified
  2026-09-26); skill scripts invoke only the `ai-company` CLI
  (`.agents/skills/ls-memory/scripts/memory-store:11-13`).
- `Evidence (tests)`: `tests/memory/test_git_safety.py::test_no_memory_db_in_git_history`,
  `test_lsmem_code_no_git_commands`.

### Q8 — Can memory reach OpenAI?

**Answer.** **No.** There is no OpenAI endpoint, client, or SDK reference in `lsmem/`
(grep for `openai` in `src/ai_company/lsmem/` → no matches). If a hypothetical caller
bypassed the code and attempted an egress decision naming provider `openai`, gate 2
(unapproved provider) or gate 1 (gateway disabled) denies it.

- `Evidence (code)`: grep `openai` in `src/ai_company/lsmem/` → 0 matches;
  `gateway.py:152-165` (provider allow-list gate, empty by default);
  `engine.py:113-116` (empty `approved_providers`).
- `Evidence (tests)`: `tests/memory/test_integration.py::TestGatewayFiveGate::test_gate2_unapproved_provider_blocked`
  (provider `openai` → `allowed is False`, reason contains "provider").

### Q9 — Can memory reach Anthropic?

**Answer.** **No.** Same evidence as Q8: no Anthropic client in `lsmem/`; the only place
the string `anthropic` appears is test *fixtures* exercising the deny path.

- `Evidence (code)`: grep `anthropic` in `src/ai_company/lsmem/` → 0 matches (the URL
  `https://api.anthropic.com/...` appears only in test fixture data,
  `tests/memory/test_integration.py:76`).
- `Evidence (tests)`: `tests/memory/test_integration.py::TestGatewayFiveGate::test_gate1_disabled_denies`
  (default config denies that exact destination).

### Q10 — Can memory reach Google?

**Answer.** **No.** No Google client/endpoints in `lsmem/` (grep `google` → 1 match only:
the benign redaction *pattern name* `google_oauth` — no Google client, endpoint, or
credential handling anywhere); any egress attempt is denied by gates 1/2 as above.

- `Evidence (code)`: grep `google` in `src/ai_company/lsmem/` → 1 match,
  `redaction.py:150` (pattern name only); `gateway.py:139-165`.
- `Evidence (tests)`: `tests/memory/test_integration.py::TestGatewayFiveGate::test_gate1_disabled_denies`
  (applies to any destination, including Google endpoints).

### Q11 — Can memory reach another cloud provider?

**Answer.** **No.** Egress is default-deny at gate 1 (`enabled: False`) with empty
provider/domain/operation allow-lists; no HTTP client other than the loopback-only Ollama
embedder exists in the package. No cloud SDK (`boto3`, `azure-*`, `google-cloud-*`) is a
dependency (Q3).

- `Evidence (code)`: `gateway.py:27,44-55,139-165`; `engine.py:107-122`;
  `pyproject.toml:14-35` (no cloud SDKs).
- `Evidence (tests)`: `tests/memory/test_integration.py::TestGatewayFiveGate::test_gate1_disabled_denies`,
  `test_gate3_unapproved_domain_blocked` (destination
  `https://evil.example.com/exfil` → denied).

### Q12 — Can memory reach an external vector database?

**Answer.** **No.** LS-MEM's vector support is the local `OllamaVectorStore`, whose only
endpoint defaults to loopback (`http://127.0.0.1:11434`), it is disabled by default, and
it is not wired into the engine/CLI (Q1). There is no Pinecone/Weaviate/pgvector/Chroma/
cloud-vector client anywhere in the package or dependency list.

- `Evidence (code)`: `vector.py:11,22-30,111-114`; grep `pinecone|weaviate|chroma|qdrant|pgvector`
  across `src/` and `pyproject.toml` → 0 matches (verified 2026-09-26).
- `Evidence (tests)`: `tests/memory/test_ollama_optional.py::test_init_defaults`
  (loopback endpoint default), `test_disabled_returns_empty`.

### Q13 — How are API keys protected?

**Answer.**

1. **Never in git:** `.env` and secret files are ignored (`.gitignore:4-7` — `.env`,
   `.env.*`, with `.env.example` negated).
2. **Never in memory records:** a secret embedded in memory content is redacted before it
   reaches disk (Q14), so keys stored "in memory" are canonical tokens, not live values.
3. **Rotation procedure:** documented at `AGENTS.md §11` (90-day rotation, `.env` local
   only, staged/production secret stores, health verification, revoke-old) plus
   `docs/DASHBOARD_KEY_ROTATION.md` for dashboard RBAC keys. LS-MEM itself reads **no**
   API keys — it has no key-consuming integration (grep for `api_key|API_KEY` in `lsmem/`
   → only redaction *patterns*, no key reads).
4. **Key material handling for the repo's other components** (dashboard, LLM providers)
   is out of LS-MEM scope and governed by the rotation procedure above.

- `Evidence (code)`: `.gitignore:4-7`; `src/ai_company/lsmem/redaction.py:68-159`
  (pattern table *detects* secrets, never stores them; `redaction.py:19-30` is the
  `SecretType` enum); grep `os.environ|getenv` in `lsmem/` →
  no key reads (verified 2026-09-26); `AGENTS.md §11`.
- `Evidence (tests)`: `tests/memory/test_redaction.py` (19 tests covering detection,
  redaction, classification upgrade).

### Q14 — How are secrets redacted?

**Answer.** A three-layer pipeline runs **before any write** and again **at export**:

1. **Detection:** `SecretScanner` wraps the existing `PIIDetector` and adds high-signal
   extensions (AWS keys, GitHub/Slack/Stripe tokens, private-key headers, generic
   `sk-`/`ghp_`-style patterns, env-style assignments) — `redaction.py:12,67-72`.
   **Every** matched substring is replaced with the canonical token regardless of
   confidence (`redaction.py:253-264` — both confidence branches emit
   `[REDACTED_SECRET]`); a match with confidence ≥ 0.8 *additionally* sets
   `has_restricted`, which forces classification `RESTRICTED`
   (`redaction.py:257-267` → applied at `engine.py:385-387`).
   `HIGH_CONFIDENCE_TYPES` (`redaction.py:161-165`) is defined but **never
   referenced** — the ≥ 0.8 rule is the actual enforcement (§6 F-09; corrected
   2026-09-26 §6.4).
2. **Redaction:** matched substrings are replaced with canonical tokens such as
   `[REDACTED_SECRET]` — replaced values are never persisted (verified in smoke: a memory
   remembered with a fake AWS key stores only the token; test
   `test_engine_crud.py::test_remember_with_secret` asserts classification
   `RESTRICTED` + absence of the raw secret).
3. **Re-scan:** export re-scans every row and upgrades any late-found secret to
   `RESTRICTED` (`engine.py:1095-1101`), and `RESTRICTED` rows are excluded from export
   unless `--include-restricted` (`engine.py:1086-1087`). `RESTRICTED` rows are also
   excluded from `search` (`engine.py:819`).

Pipeline order: secret scan → auto-classify → constitutional veto → value scoring
(`engine.py:366-400`).

- `Evidence (code)`: `redaction.py:12,68-159,161-165,253-267`;
  `engine.py:366-400,538,819,1086-1101`.
- `Evidence (tests)`: `tests/memory/test_redaction.py` (19 tests);
  `tests/memory/test_engine_crud.py::test_remember_with_secret`;
  smoke-verified 2026-09-26 (secret → `RESTRICTED`, raw value absent from db).

### Q15 — How are external requests approved?

**Answer.** Through the **5-gate default-deny permission gateway**
(`architecture §9.1`, implemented in `gateway.py`): (1) gateway enabled? (2) provider
approved? (3) domain/destination approved? (4) operation approved? (5) data classification
allowed? If all five pass, the request is **not auto-granted** — it returns
`requires_human_approval=True` with a one-time `approval_token` held in the gateway's
pending queue; a human approves via `submit_human_approval(token, approver, approved=True)`
or the `ai-company memory permission approve --token … --by …` command.

**Verified limits (honest status):**
- The approval queue is **in-process memory only** (`gateway.py:119`), so a token raised
  in one process cannot be approved from a separate CLI invocation — a fresh process
  always reports `No pending approvals` (verified in smoke 2026-09-26).
- Nothing in `src/` calls `PermissionGateway.evaluate()` outside tests (grep verified) —
  because LS-MEM currently performs **no egress at all** (Q1), there is no production
  transmit path to gate. The mechanism is correct and tested; it is **not yet wired to a
  real transfer**, and cross-process approval is **not available**.

- `Evidence (code)`: `gateway.py:121-165` (evaluate + 5 gates), `gateway.py:119,220-233`
  (pending approvals + audit payload), `cli.py:592-646` (permission subcommands);
  grep `.evaluate(` in `src/` → no caller of `PermissionGateway.evaluate()` outside
  tests (the only other match is the unrelated dashboard `AlertEngine.evaluate`,
  `src/ai_company/dashboard/data_service.py:887`).
- `Evidence (tests)`: `tests/memory/test_integration.py::TestGatewayFiveGate`
  (10 tests: each gate blocks individually, all-pass → human approval required,
  approve grants, deny blocks, invalid token blocks, local ops always allowed);
  `tests/memory/test_offline.py::TestGatewayOffline::test_human_approval_flow`,
  `test_classification_enforcement`.

### Q16 — How are approved transfers audited?

**Answer.** Two layers:

1. **Designed:** every gateway decision carries a pre-built audit event
   (`event_type` `gateway_request` / `gateway_approved` / `gateway_denied`,
   `gateway.py:92,221,268,287,325`), the audit schema accepts and **preferentially
   retains** those event types (365-day gateway retention vs 90-day CRUD,
   `audit.py:49-51,61-62,408,417`), and all audit rows are SHA-256 hash-chained so
   tampering with an entry breaks `verify_chain()`.
2. **Verified status today:** memory-lifecycle events **are** persisted and chained —
   smoke run showed a real chain (`memory_create`, `memory_update`, `export` with
   actor/timestamp/correlation IDs; `verify` → `Audit chain OK`). However, **no code
   path currently writes `gateway_*` events to the audit DB** (grep for
   `gateway_approved|gateway_request` writes → only declarations in `audit.py` and payload
   construction in `gateway.py`; no `log()` caller). Since there are no transfers (Q15),
   this is a **latent gap, not an audited-but-missing event** — flagged for the
   independent audit: wire `gateway.evaluate()` → `AuditLog.log()` when egress is wired.

- `Evidence (code)`: `gateway.py:92,220-233,267-303`; `audit.py:44-56` (`EVENT_TYPES`),
  `audit.py:61-62` (retention), `audit.py:157` (`log()`), `audit.py:248` (`query()`),
  `audit.py:297` (`verify_chain()`), `audit.py:408,417` (retention split);
  `engine.py:495` (`_audit` — used for memory events).
- `Evidence (tests)`: `tests/memory/test_audit_chain_head.py` (9 tests: chain head
  persistence, `verify_chain`, tamper detection); smoke 2026-09-26
  (`ai-company memory audit` → 4-event table, chain OK).

### Q17 — What happens if permission is ambiguous?

**Answer.** **Deny.** Locked decision 3 of the gateway: "When uncertain → BLOCK"
(`gateway.py:114` docstring). Concretely:

- Gateway disabled (the default) → deny with reason "disabled" regardless of other inputs.
- Classification not in the allowed set / not recognized → deny (gate 5); unknown
  classifications are additionally rejected earlier at remember-time with `ValueError`
  (`engine.py:531-535`, `VALID_CLASSIFICATIONS` at `engine.py:230`).
- Missing/invalid/expired approval token → deny (`gateway.py:255-262`).
- Local operations are the only unconditional allow (`check_local_operation`,
  `gateway.py:346-353`) — they never leave the machine.

- `Evidence (code)`: `gateway.py:114,139-165,255-262,346-353`; `engine.py:230,531-535`.
- `Evidence (tests)`: `tests/memory/test_integration.py::TestGatewayFiveGate::test_gate5_classification_blocked`,
  `test_invalid_approval_token_blocks`;
  `tests/memory/test_offline.py::TestGatewayOffline::test_classification_enforcement`.

### Q18 — What happens when internet access is unavailable?

**Answer.** **Nothing breaks — LS-MEM is designed to be fully functional offline.**
Store, search, get, forget/purge/restore, pin/verify, lifecycle, status, integrity,
rebuild-fts, export, and audit all operate on the local SQLite file with zero network
dependency (verified by the offline test suite and by smoke runs on a normal workstation).
There is no "connectivity check" that could hang or degrade startup, no DNS at
initialization, and no fallback-to-cloud behavior.

- `Evidence (code)`: `engine.py` has no network imports outside the disabled Ollama
  config (`engine.py:123-130`); `cli.py` commands are pure local I/O.
- `Evidence (tests)`: `tests/memory/test_offline.py::TestOfflineOperation` (5 tests:
  CRUD, search, lifecycle, rebuild-fts, integrity — all pass with network patches
  asserting no calls), `TestNetworkDeny` (no `connect()`, no external DNS).

### Q19 — What happens when Ollama is unavailable?

**Answer.** Degradation is graceful and effectively invisible: Ollama is **disabled by
default**, and when the embedder is disabled or the endpoint is unreachable, `embed()`
returns an empty embedding list instead of raising — search simply continues as **FTS5
lexical search**, which is the only search mode wired into the engine today (Q1). The
health probe (`is_healthy()`) reports status without blocking operations.

- `Evidence (code)`: `vector.py:111-114` (disabled default), `vector.py` embed path
  returns `[]` when disabled/unhealthy; `engine.py:123-130`;
  `cli.py:152` (search documented as FTS5).
- `Evidence (tests)`: `tests/memory/test_ollama_optional.py::test_disabled_returns_empty`,
  `test_is_healthy_check`, `test_from_config`; offline suite runs with no Ollama present
  (`test_offline.py` passes on a machine with no Ollama — observed in the 102-passed run).

### Q20 — How can the user completely delete LS-MEM?

**Answer.** Stop any running LS-MEM processes (default setup has no daemon — each CLI
call is short-lived), then delete the data directories, then confirm git state:

```powershell
Remove-Item -Recurse -Force .lightspeed\memory    # memory.db*, audit/audit.db, config.yaml
Remove-Item -Recurse -Force .\memory              # legacy JSON store (optional)
git status --porcelain                            # should show no memory files
```

This removes records, FTS index, audit log, and config; the next command recreates an
empty schema. Also delete `~/.lightspeed/memory` if you ever created one (config default
mentions it at `engine.py:69`, but the CLI only uses the workspace path, `cli.py:51`).
For per-record deletion instead: `forget` (archivable, restorable) → `purge --confirm`
(terminal state: `status='PURGED'`, `engine.py:919-926` — a **soft transition**: the row
and its content remain at rest and are still retrievable via `memory get`, which has no
status filter (`engine.py:615`), while `search` excludes non-`ACTIVE` rows
(`engine.py:816`); complete erasure of a record requires deleting the store files per
the procedure above — execution-confirmed 2026-09-26, §6 F-02/§6.2c). To uninstall
the *code*, remove the package/skill directories —
out of scope here. Full procedure with verification steps: `docs/LS-MEM-USER-GUIDE.md` §6.7.

- `Evidence (code)`: `cli.py:51-59` (all paths under `<workspace>/.lightspeed/memory`),
  `engine.py:69` (global path default, unused by CLI);
  `.gitignore:91-96,73-74`; `engine.py:874-941,919-926,615,816`
  (forget/purge, soft-purge write, post-purge retrieval, search exclusion).
- `Evidence (tests)`: `tests/memory/test_engine_crud.py::TestEngineDeletion`
  (forget/restore semantics); directory layout + delete verified in smoke 2026-09-26.

---

## 2. Dependencies added

| Dependency | Added by LS-MEM? | Network behavior |
|------------|------------------|------------------|
| (none) | **No** — zero new `pyproject.toml` entries | — |
| `typer`, `rich`, `pyyaml` | No (pre-existing) | None (pure local) |
| `httpx<0.29.0` | No (pre-existing) | HTTP client; LS-MEM uses it **only** for loopback Ollama (`vector.py:43`), disabled by default, not wired to engine/CLI |
| `sqlite3` (stdlib) | n/a | None (local file) |

Full declared list: `pyproject.toml:14-35`.

---

## 3. Deviations from handoff

| Handoff requirement | Status | Resolution |
|---------------------|--------|------------|
| §18: expose memory via `.opencode/tools/memory-*` scripts | **Not implemented — decided deviation** | Decision 2026-09-26: the canonical runtime tool vocabulary is fixed at 7 tools (`read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task`) per `AGENTS.md §8`; unknown tools are rejected by ToolRunner. Adding `memory-*` tool entries would violate that locked vocabulary. The equivalent surface ships as **ls-memory skill scripts** (`.agents/skills/ls-memory/scripts/` + `.opencode/skills/ls-memory/` mirror), which invoke the CLI via `bash`. |
| Handoff §27: user-guide procedures (backup, restore, export, migrate, rebuild, corruption, delete) | **Delivered** | `docs/LS-MEM-USER-GUIDE.md` §6, each verified 2026-09-26 where testable |
| Handoff §33: this report with test evidence | **Delivered (this file)** | Independent audit delivered with verdict (§6); CEO approval pending (§7) |
| Schema migration tool | **Gap documented, not deviated silently** | No migration framework exists (schema v1 only) — stated in guide §6.4a and Q20 context; requires a future workstream |

---

## 4. Test evidence

### Suite run (2026-09-26, `uv run pytest tests/memory -q -rs`)

| Result | Count | Detail |
|--------|-------|--------|
| **Passed** | **102** | 7 files: `test_engine_crud.py`, `test_audit_chain_head.py`, `test_git_safety.py`, `test_offline.py`, `test_ollama_optional.py`, `test_redaction.py`, `test_integration.py`, `test_dual_path_hash.py` |
| **Skipped** | **1** | `tests/memory/test_dual_path_hash.py:93` — "Global skill copy not present (optional)" (only runs when a global ls-memory skill exists) |
| Failed | 0 | |
| Duration | 6.97s | |

Representative security-relevant tests (all passing):

| Concern | Test |
|---------|------|
| No outbound I/O on remember | `test_offline.py::TestNetworkDeny::test_no_outbound_connections_on_remember` |
| No external DNS at startup | `test_offline.py::TestNetworkDeny::test_no_dns_resolution_on_startup` |
| Gateway default-deny | `test_offline.py::TestNetworkDeny::test_gateway_blocks_external_by_default` |
| 5-gate chain, each gate blocks | `test_integration.py::TestGatewayFiveGate` (10 tests) |
| Human approval flow | `test_offline.py::TestGatewayOffline::test_human_approval_flow` |
| Secret redaction | `test_redaction.py` (19 tests) + `test_engine_crud.py::test_remember_with_secret` |
| Git exclusion of memory | `test_git_safety.py` (5 tests) |
| Audit chain integrity | `test_audit_chain_head.py` (9 tests) |
| Offline operation | `test_offline.py::TestOfflineOperation` (5 tests) |
| Bridge import safety | `test_integration.py::TestBridgeImport` (3 tests) |
| Dual skill-path parity | `test_dual_path_hash.py` (4 + 1 optional) |

### Lint / static checks

| Check | Result |
|-------|--------|
| `uv run ruff check src/ai_company/lsmem/` | **All checks passed!** (2026-09-26) |
| `uv run ruff format --check src/ai_company/lsmem/` | Warning: `audit.py:121` would reformat (formatting only; **not fixed** — out of WS-C scope) |
| `mypy` full-run | **not verified** in this workstream (run per-repo pre-commit hooks; not executed here) |
| `bandit` full-run | **run by the independent CISO audit (§6.5, 2026-09-26)** — High 0 / Medium 7 / Low 37, all 7 Mediums triaged non-exploitable |

### Manual smoke evidence (2026-09-26, temp workspace)

| Check | Outcome |
|-------|---------|
| 15-command CLI surface | All commands executed successfully with `$env:PYTHONUTF8=1` |
| Backup → purge → restore-from-file cycle | Record `PURGED` → file restored → `ACTIVE`, integrity OK |
| Secret content at rest | Fake AWS key stored as `[REDACTED_SECRET]`, classification `RESTRICTED`, raw value absent |
| Content-level corruption vs `integrity_check` | **Detected gap:** structural check passes while content bytes are corrupt (documented Q14/guide §6.6) |
| Legacy bridge import (dry-run + real) | `ImportStats(imported=1)`; record searchable after real import |
| Audit chain | 4 events, `verify` → chain OK |

---

## 5. Known gaps and residual risks (for the independent auditor)

1. **Gateway events not persisted** — `gateway_*` audit event types are declared and
   retention-split, but no code writes them (Q16). Latent: no egress exists yet.
2. **Cross-process approval unavailable** — pending approvals are in-memory per process
   (`gateway.py:119`); `memory permission list` in a fresh CLI always shows none (Q15).
3. **Content corruption invisible to `integrity_check`** — structural validation only;
   mitigated by backup/restore procedure (guide §6.6).
4. **Ollama embedder unwired** — `OllamaVectorStore` unused by engine/CLI (Q1/Q19);
   semantic search not available until wired.
5. **Windows cp1252 encode crash** — piping CLI output without `PYTHONUTF8=1` raises
   `UnicodeEncodeError` on `✓` (guide §7); UX defect, no data impact. **Fixed
   2026-09-26 post-audit:** `cli.py:_ensure_utf8_stdio` reconfigures stdio to
   UTF-8 (`errors="replace"`) at import; regression tests in
   `tests/memory/test_cli_stdio.py`; default-console `remember`/`status` verified
   exit 0 without `PYTHONUTF8`.
6. **No schema migration framework** (guide §6.4a).
7. **Cosmetic:** purge error text says `--confirm-purge` while the flag is
   `--confirm` (`engine.py:910` vs `cli.py:298`). (The `ruff format` drift on
   `audit.py:121` reported at audit time was reformatted 2026-09-26.)

None of the above contradicts a "no data leaves the machine" claim — all seven gaps are
local correctness/robustness items.

---

## 6. Independent security audit

**Status: complete — verdict: APPROVE-WITH-FINDINGS.**

- **Owner:** CISO of record — Jack Mlusu (Human CEO), per `AGENTS.md §9.2`.
- **Scope:** this report's Q1–Q20 answers and citations, the §5 gaps, the threat-model
  register in `docs/security/LS-MEM-THREAT-MODEL.md`, and the LS-MEM package source
  (`src/ai_company/lsmem/`, 3,499 lines).
- **Method:** independent re-read of every cited `path:line` (10 corrections applied in
  place, §6.4), full `bandit` run over the package (§6.5), re-run of the test suite, and
  adversarial spot-checks executed in an isolated temp workspace
  (`%TEMP%\opencode\lsmem-ciso-audit`, fresh SQLite DBs). **No source code was changed**
  (no Critical/High finding existed, per the remediation rules) and nothing was committed;
  the repo was not modified except this file.
- **Findings:** 11 total — **0 Critical, 0 High, 7 Medium, 4 Low** (§6.3). MEDIUM/LOW →
  documented here; the two CEO-level design acceptances are routed to §7.

### 6.1 Command outputs (verbatim, 2026-09-26)

```
uv run pytest tests/memory -q
→ 102 passed, 1 skipped in 16.83s

uv run pytest tests/memory/test_audit_chain_head.py -q
→ 9 passed in 1.22s

uv run ruff check src/ai_company/lsmem/
→ All checks passed!

uv run bandit -r src/ai_company/lsmem/
→ Total lines of code: 3,499
   Issues by severity:  High 0 | Medium 7 | Low 37
   Issues by confidence: High 29 | Medium 11 | Low 4
   Files skipped: 0 | #nosec skipped: 0
```

### 6.2 Adversarial spot-checks (recorded outputs)

**(a) Audit-chain tamper suite** — fresh DB, 3 hash-chained events, `tamper_test.py`:

| # | Scenario | `verify_chain` | Verdict |
|---|----------|----------------|---------|
| A | clean chain (control) | `True` | PASS |
| B | tail row `details` mutated, `chain_head` present | `False` | **DETECTED** — head mismatch (`audit.py:327-332`) |
| C | tail row mutated **+ `audit_meta.chain_head` deleted** | `True` | **UNDETECTED** — head re-derived from the tampered tail (`audit.py:329-330`, `_derive_chain_head:130-141`) → F-05 |
| D | mid-chain row mutated | `False` | **DETECTED** — `prev_hash` break (`audit.py:318`) |

**(b) FTS5 injection probes** — adversarial queries via `memory search --json`:

| Query | Result |
|-------|--------|
| `kubernetes"` | exit 1 — unhandled `sqlite3.OperationalError: fts5: syntax error …` raised at `engine.py:858`, raw traceback with source paths through `cli.py:155` → F-04 |
| `foo" OR "1"="1` | same crash — **no injection** |
| `' OR 1=1 --` | same crash — **no injection** |
| `1; DROP TABLE memories;--` | same crash — table intact (verified after) |
| `kubernetes OR postgres` | exit 0 — correct boolean union |
| `NEAR(...)`, `NOT`, trailing `*` | exit 0 — operators work as documented |

Post-attack state: both records still returned by `search '*'` — **no SQL injection, no
data loss; the failure mode is an unhandled-exception UX/robustness defect only (F-04).**

**(c) Purge lifecycle:**

| Step | Output |
|------|--------|
| `memory purge <id>` (no flag) | exit 1 — `✗ Purge requires explicit confirmation (--confirm-purge)` — message names a non-existent flag; the real flag is `--confirm` (`engine.py:910` vs `cli.py:298`) → F-08 |
| `memory purge <id> --confirm` | exit 0 — `✓ Purged` |
| `memory get <id>` after purge | exit 0 — **full content returned**, `"status": "PURGED"` (no status filter, `engine.py:615`) → execution-confirmed F-02 |
| `memory search "…"` after purge | `[]` — PURGED excluded (`engine.py:816`) |
| raw SQLite row | content bytes still present at rest |

**(d) Permission gateway + classification filter (fresh processes):**

- `memory permission list` → `No pending approvals` (exit 0) — in-memory per-process
  queue; cross-process approve impossible → F-06.
- `memory permission approve --token deadbeef-fake-token --by auditor` →
  `✗ Denied: Invalid or expired approval token` — deny-by-default holds for fabricated
  tokens (`gateway.py:255-262`).
- `memory search "kubernetes" -c PUBLIC` → **returns the INTERNAL record** (exit 0);
  `-c RESTRICTED` → also returns it — the caller's filter value is discarded
  (`engine.py:829-831` binds the literal `!= 'RESTRICTED'`) → execution-confirmed F-03.

### 6.3 Findings register

| ID | Severity | Location | Finding / recommendation | Status |
|----|----------|----------|--------------------------|--------|
| F-01 | MEDIUM | `engine.py:650-661` | `update()`'s caller-supplied `classification` overwrites the pipeline's RESTRICTED upgrade (line 655 sets it from the secret scan, lines 658-661 replace it with the caller value) → secret content is still redacted at rest, but loses its RESTRICTED label and therefore re-enters `search`/`export` (which exclude only RESTRICTED). Recommend: never let the caller downgrade below the pipeline result. | documented (deferred fix) |
| F-02 | MEDIUM | `engine.py:919-926`, `615`, `816` | Purge is a **soft lifecycle transition** (`status='PURGED'`), not row erasure: content remains retrievable via `get` and at rest (execution-confirmed §6.2c), excluded only from `search`. Consistent with `retention.md` (PURGED = terminal state), but Q20 previously overstated it as "hard delete". Recommend: correct user-guide wording; optional secure-erase command as a future workstream. | documented (Q20 corrected) |
| F-03 | MEDIUM | `engine.py:829-831` | `search --classification <X>` discards the caller value (always appends `classification != 'RESTRICTED'` with a literal) — `-c PUBLIC` returns non-PUBLIC rows (execution-confirmed §6.2d). Recommend: bind the filter value as a parameter + validate. | documented (deferred fix) |
| F-04 | MEDIUM | `engine.py:858`, `cli.py:155` | Malformed FTS syntax raises an uncaught `sqlite3.OperationalError` → full traceback with source paths, exit 1 (§6.2b). No injection or data loss. Recommend: catch and emit a sanitized `✗` error. | documented |
| F-05 | MEDIUM (design) | `audit.py:329-330`, `130-141` | Chain head lives inside the same audit DB; if the `audit_meta` row is deleted the head is re-derived from the (possibly tampered) tail → tail tamper undetected (scenario C); mid-chain tamper still detected (D). No external anchoring exists. Recommend: anchor the head outside the audit DB (file or periodic notarization). | **deferred → §7** |
| F-06 | MEDIUM (latent) | `gateway.py:119,244-262` | Approval queue is a per-process dict with no TTL; cross-process approve impossible (§6.2d); no production `evaluate()` caller exists today, so no live impact. Recommend: persistent approval store + token expiry **before** any egress is wired. | documented → §7 |
| F-07 | MEDIUM (latent) | `gateway.py:221,268,287` | `gateway_*` audit events are constructed but never written (no `AuditLog.log()` caller for them) — gap confirmed. Blocking condition: wire gateway → `log()` before first egress. | documented (extends §5 gap 1) |
| F-08 | LOW | `engine.py:910` vs `cli.py:298` | Purge error text names `--confirm-purge`; the actual flag is `--confirm` (execution-confirmed §6.2c). Cosmetic but misleading in a security-relevant flow. | documented (extends §5 gap 7) |
| F-09 | LOW | `redaction.py:161-165`, `classification.py:112` | Dead security constants: `HIGH_CONFIDENCE_TYPES` and `can_downgrade` are defined but never referenced → false-assurance risk (Q14 previously implied they were enforced). Actual enforcement is the ≥ 0.8 rule (`redaction.py:257-267`). Recommend: wire or delete. | documented (Q14 corrected) |
| F-10 | LOW | bandit B608 ×6: `audit.py:286`, `bridge.py:345`, `engine.py:671,838,848,1090` | f-string SQL fragments — all built from internal literals with **parameterized values** (`?` placeholders); user input is never concatenated (each site read individually, §6.5). No exploitable SQLi. | accepted |
| F-11 | LOW | bandit B310: `vector.py:63` | `urllib.request.urlopen` to a **configurable** endpoint — default loopback, disabled, unwired; the only `urlopen` in the package. Recommend: enforce loopback-only if/when wired. | accepted (Q1 corrected) |

### 6.4 Citation corrections applied (re-verification, 2026-09-26)

| # | Was (claimed) | Now (verified) |
|---|---------------|----------------|
| 1 | Q1: embedder "scoped to a single loopback URL" | endpoint **defaults to** loopback but is configurable (`vector.py:29,111-114`) — aligned with Q4/Q12 |
| 2 | Q2: `gateway.py:44-55` = `data_classes_allowed` all `False` | `gateway.py:31-38` (field default) + `56-64` (`from_dict` fallback); 44-55 covers only enabled/approved-* defaults |
| 3 | Q6: "source contains no `git` commands" | only `git add`/`commit`/`push` are forbidden (`test_git_safety.py:105`); read-only `git rev-parse` permitted (`injector.py:263-265`); grep of the three verbs → 0 matches |
| 4 | Q10: grep `google` → 0 matches | 1 match: benign pattern name `google_oauth` (`redaction.py:150`); no Google client/endpoint |
| 5 | Q13: `redaction.py:19-30` = "patterns detect secrets" | pattern table is `redaction.py:68-159`; 19-30 is the `SecretType` enum |
| 6 | Q13/Q14/§4: `test_redaction.py` = 17 tests | **19 tests** (collected 2026-09-26) |
| 7 | Q14: "confidence ≥ 0.8 triggers redaction; `HIGH_CONFIDENCE_TYPES` forces RESTRICTED" | every match is redacted at any confidence (`redaction.py:253-264`); ≥ 0.8 *additionally* forces RESTRICTED (`257-267` → `engine.py:385-387`); `HIGH_CONFIDENCE_TYPES` is unreferenced (F-09) |
| 8 | Q15: grep `evaluate(` → only the definition | `.evaluate(` has no production caller (other match is the unrelated dashboard `AlertEngine.evaluate`, `dashboard/data_service.py:887`) |
| 9 | Q17: `check_local_operation` at `gateway.py:306-310` | `gateway.py:346-353` (306-310 is `get_pending_approvals`) |
| 10 | Q20: purge = "hard delete, row erased" | soft `status='PURGED'` (`engine.py:919-926`); content via `get` (615) and at rest; excluded from `search` (816) — execution-confirmed (F-02) |

All other citations (including `cli.py:30,34,51-59,152,592-646`, `.gitignore:4-7,73-74,91-96`,
`pyproject.toml:14-35,42-55`, `engine.py:69,107-122,230,272,303,495,531-535,816-819,1095-1101`,
`audit.py` chain internals, and every named test method) were re-read line-by-line and left
unchanged.

### 6.5 Bandit triage

`uv run bandit -r src/ai_company/lsmem/` (2026-09-26): 3,499 lines —
**High 0, Medium 7, Low 37.**

| Rule | Location | Verdict |
|------|----------|---------|
| B608 SQL injection | `audit.py:286` | parameterized `WHERE … = ?` (266-294) — safe |
| B608 | `bridge.py:345` | internal column keys, parameterized values — safe |
| B608 | `engine.py:671` | UPDATE SET over internal keys — safe |
| B608 | `engine.py:838` | match-all SQL; `where_clause` from internal conditions — safe |
| B608 | `engine.py:848` | FTS `MATCH ?` parameterized (852/856) — safe |
| B608 | `engine.py:1090` | export WHERE internal literals + params — safe |
| B310 URL open | `vector.py:63` | loopback default, disabled, unwired — F-11 accepted |

Low findings: B101 `assert` statements, B105 pattern-name false positives
(`redaction.py`), B404/B607/B603 `subprocess` for `git rev-parse` (`injector.py`) —
no exploitable issue. **No user-controlled string is concatenated into SQL anywhere in
the package** (verified per site).

### 6.6 Verdict

**APPROVE-WITH-FINDINGS.**

The core security claims hold under adversarial testing: no egress paths (Q1–Q12
re-verified), deny-by-default gateway exercised including a fabricated-token attempt,
secrets redacted at rest, git exclusion enforced, mid-chain audit tampering detected, and
the purge/search lifecycle behaves as §6.3 documents once Q20's wording is corrected.
No Critical/High finding exists, so per the remediation rules no code was changed. The
seven Medium findings are integrity/robustness items — two execution-confirmed bugs
(F-02, F-03), one crash-mode defect (F-04), one label-loss path (F-01), one audit-anchor
design gap (F-05), and two latent gateway gaps (F-06, F-07) — none of which contradicts
the "no data leaves the machine" claim. Residual-risk acceptances and report sign-off
remain with the approvers in §7.

| Date | Reviewer | Findings | Sign-off |
|------|----------|----------|----------|
| 2026-09-26 | AI CISO (independent audit session) | 11 findings — 0 Critical / 0 High / 7 Medium / 4 Low; 10 citation corrections applied (§6.4); 0 source changes | **APPROVE-WITH-FINDINGS** — pending ratification by CISO of record Jack Mlusu (Human CEO, `AGENTS.md §9.2`) |

---

## 7. Approval

**Status: pending — HITL sign-off required before this workstream is declared complete.**

Items awaiting CEO/CISO approval (from §6):

1. Ratify the §6 verdict **APPROVE-WITH-FINDINGS** (11 findings, 0 Critical/High,
   10 citation corrections, 0 source changes).
2. Accept residual risk **F-05** — the audit chain has no anchor outside the audit DB
   (tail tamper undetected if `audit_meta.chain_head` is deleted); external anchoring
   is deferred.
3. Accept residual risk **F-06** — approval queue remains in-process (no cross-process
   approve, no token TTL) until a persistent store is built; this becomes **mandatory
   before any egress is wired**, together with F-07 (gateway events → `AuditLog.log()`).
4. Direct follow-ups (documented, not blocking this approval): deferred one-line fixes
   F-01/F-03, sanitized FTS error F-04, purge message text F-08, dead constants F-09.

| Approver | Role | Date | Decision |
|----------|------|------|----------|
| Jack Mlusu | Human CEO / CISO | — | **Pending** |
