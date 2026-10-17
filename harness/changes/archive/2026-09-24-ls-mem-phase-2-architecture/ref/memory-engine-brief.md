# Memory Engine Brief — LS-MEM Design Inputs (Grounded in Source)

**Purpose:** dense technical reference for the Memory Owner (AI Research) on the two coexisting memory engines: the existing JSON `MemoryStore` (6 types, ADR-019) and the proposed LS-MEM SQLite+FTS5 engine (13 types, 4 classifications, ADR-025). Every claim below is grounded in a file that was actually read; proposals that do not yet exist in code are marked **PROPOSED**.

**Scope of this file:** design inputs only. No implementation. One-way bridge direction and authority rules follow ADR-025 (Accepted 2026-09-24).

---

## 1. Existing JSON MemoryStore inventory (6 types)

### 1.1 The six types

From `src/ai_company/memory/engine.py` (module docstring + `_stores` dict init):

| # | Type | Meaning (engine.py L1–9) | Retention TTL (days, ADR-019 / `governance.py`) |
|---|------|--------------------------|--------------------------------------------------|
| 1 | `episodic` | events and experiences (what happened) | 90 |
| 2 | `semantic` | facts and knowledge (what is known) | 3650 |
| 3 | `procedural` | how-to knowledge (how to do things) | 3650 |
| 4 | `relational` | entity relationships (who knows whom) | 730 |
| 5 | `temporal` | time-based records (when things happened) | 365 |
| 6 | `aggregate` | summaries and rollups (patterns and insights) | 10950 |

`DEFAULT_RETENTION_TTL_DAYS` is a plain dict in `memory/governance.py` L28–35; unknown types fall back to 365 via `ttl_days_for()`. Staleness window is `DEFAULT_STALENESS_DAYS = 180` (not recalled + `access_count == 0` → flagged). Minimum content length for "knowledge vs noise" is `MIN_KNOWLEDGE_LENGTH = 40` chars (whitespace-normalized).

### 1.2 Record shape (`MemoryEntry`)

`engine.py` L40–72 — fields written to disk via `to_dict()`:

| Field | Type | Notes |
|-------|------|-------|
| `id` | str | `{memory_type}_{UTC %Y%m%d_%H%M%S_%f}` at construction; reloaded from disk if present |
| `memory_type` | str | one of the 6 keys; `store()` raises `ValueError` on unknown type |
| `content` | str | may be `ENC:<base64(...)>` when encryption enabled |
| `metadata` | dict | free-form; carries `status` (`pinned` / `superseded` / `stale`), `pinned`, `vetoed`, `veto_reason` |
| `agent_id` | str | writer attribution |
| `tags` | list[str] | used by `recall(tags=...)` set-intersection filter |
| `created_at` | ISO-8601 UTC | age → TTL / staleness |
| `access_count` | int | incremented on top-N `recall`/`search` hits; `> 0` exempts from staleness |
| `seq` | int | monotonic `itertools.count()` insertion order; persisted for deterministic recency sort |

There is **no** `title`, `classification`, `confidence`, `provenance`, `verified_by`, or `approved_for_external_use` on `MemoryEntry` today. Those are LS-MEM handoff §8 concepts and must be added on the SQLite side (ADR-025 Decision rule 4: add `verified_by` + institutional flag to close recon Tier-3 gap).

### 1.3 ADR-019 governance layer (`memory/governance.py`, 180 lines)

Implemented as dataclass `MemoryGovernance` + module-level `screen_capture()`. Source of truth: `docs/adr/019-memory-knowledge-governance.md` and ticket #229.

| Policy | Implementation | Behavior |
|--------|----------------|----------|
| Constitutional veto | `is_constitutionally_blocked()` / `capture_decision()` L96–124 | lower-cased substring match against `CONSTITUTIONAL_BLOCKLIST` = `["bypass safety", "ignore safety", "exfiltrate", "prompt injection: achieve", "extract secrets from"]` → `allowed: False, reason: "constitutional_block"` |
| Noise flag (soft) | `is_probable_noise()` | markers `unknown error`, `no output`, `command not found` → captured but `flagged: True` |
| Knowledge floor | `is_knowledge_worthy()` | normalized length ≥ 40 → else `flagged: True` (still captured — automatic capture, no human gate) |
| Capture path | `MemoryStore.store()` L189–211 | on hard veto, returns a **placeholder** `MemoryEntry` with `metadata["vetoed"]=True` and `veto_reason`; **nothing is persisted** |
| Conflict resolution | `resolve_conflict(existing, new)` L147–155 | default **newest wins**; loser → `status: "superseded"`; pinned existing wins and new stays active |
| Supersession | `mark_superseded()`; `MemoryStore.supersede()` / `resolve_conflict()` | superseded entries excluded from recall/search via `_exclude_vetoed()` (drops `vetoed` and `status in ("superseded",)`) |
| Curator pin | `is_pinned()`; `MemoryStore.pin` / `unpin` L236–260 | sets `metadata.status="pinned"` + `pinned=True`; pinned entries survive prune/digest and win conflicts |
| Staleness | `is_stale()` / `mark_stale_flag()` | `access_count==0` and age ≥ 180d → `metadata.setdefault("status","stale")` |
| TTL expiry | `is_expired(entry, type)` | age > type TTL → true (used by prune paths) |

**Design note for LS-MEM:** these five concepts (TTL, staleness, supersede, constitutional veto, pin) must appear as either schema columns + lifecycle states or an explicit mapping table in `docs/architecture/LS-MEM-DATA-MODEL.md` (ADR-025 rule 4). Pin semantics map onto Tier 3 / `verified_by` verification (recon §3 gap).

### 1.4 Public API surface (what existing consumers call)

From `engine.py` (methods confirmed present) + `integration.py`:

| Method | Signature (essence) | Role |
|--------|---------------------|------|
| `store(memory_type, content, **kwargs)` | returns `MemoryEntry` | write path; screens capture, encrypts, indexes |
| `recall(memory_type, query="", tags=None, agent_id="", limit=10, use_semantic=True)` | `list[MemoryEntry]` | type-scoped fetch; vector → substring fallback; bumps `access_count`; decrypts |
| `search(query, memory_type=None, limit=10)` | `list[MemoryEntry]` | cross-type keyword/TF score or single-type vector; excludes vetoed/superseded |
| `prune(max_age_days=None, max_entries_per_type=None)` | `int` count dropped | age + per-type caps; keeps pinned; syncs vector index |
| `consolidate_all()` / `consolidate(memory_type)` | `dict[str, int]` | dedup within type, digest episodic, flag stale |
| `count` / `stats()` | int / `dict[str,int]` | inventory |
| `pin` / `unpin` / `supersede` / `resolve_conflict` | `bool` | curator / conflict ops |
| `enable_vector_search` / `enable_encryption` | None | optional layers |
| Integration helpers | `init_memory(base_dir="memory")`, `get_store()`, `learning_enabled()`, `recall_context`, `semantic_search`, `record_task_outcome`, `record_knowledge`, `record_procedure`, `pin_memory`, `unpin_memory`, `governance_summary` | executor/CLI entry points; gated by `AI_COMPANY_LEARNING_ENABLED` |

Existing consumers that **must not break** during coexistence (ADR-025 rule 2): `ai-company memory` CLI (`cli/memory.py`), `ConsolidationScheduler`, executor pre-execute recall path, `memory/*.json` corpus readers.

### 1.5 JSON persistence & file locations

- Backend: `FileStore` (`src/ai_company/store/file_store.py`) — atomic write via `utils.file_lock.atomic_write`, optional `.bak` backup, quarantine `.corrupt-<ts>` + `.bak` recovery for corrupt JSON. `MemoryStore` constructs `FileStore(self.base_dir, backup=False)` — **MemoryStore itself disables `.bak`**.
- Path template: `{base_dir}/{memory_type}.json` (`_file_name`). Default `base_dir="memory"` (project-relative).
- On-disk corpus (confirmed present): `memory/episodic.json`, `memory/semantic.json`, `memory/procedural.json`, `memory/relational.json`, `memory/temporal.json`, `memory/aggregate.json`, plus `memory/metrics.json` (from `metrics.py`, not a memory type), `memory/embeddings/`, `memory/vector_index/`.
- Git: root `memory/*.json` and `memory/vector_index/` are gitignored (`.gitignore` lines 73–74 per recon; `.gitignore:91` also notes LS-MEM local store never commit).
- Each file is a JSON **array** of `MemoryEntry.to_dict()` objects; non-list / corrupt content is skipped or quarantined.

---

## 2. Reusable building blocks (read from source)

### 2.1 FTS5 — `data/database.py` + `data/audit_store.py` + `data/search.py`

- Schema migration **version 5** (`database.py` L360–396) creates:
  - External-content FTS5: `audit_events_fts(task_id, tool, args, result, metadata, content='audit_events', content_rowid='rowid')` with AFTER INSERT / DELETE / UPDATE triggers (delete-then-insert pattern).
  - Contentless-style table: `tasks_fts(instruction, description, name)`.
- Search pattern (`audit_store.search_events` L123–151): `JOIN ... f ON f.rowid = e.rowid WHERE audit_events_fts MATCH ?` ordered + `LIMIT`; on `sqlite3.OperationalError` / `AttributeError` → **fallback to LIKE** over `read_all()` rows.
- `data/search.py` same dual path for tasks and audit (MATCH → LIKE fallback on `instruction LIKE ? OR name LIKE ?`).
- Environment: SQLite 3.49.1 in project venv, **FTS5 available** (recon §2). No FTS index exists on memory content today — only audit + tasks.
- **Reuse for LS-MEM:** copy the create + trigger + MATCH + LIKE-fallback approach for a `memory_fts` virtual table over title/content/tags/provenance. Use parameter binding (bandit B608: no new suppressions). Do not invent a custom tokenizer beyond FTS defaults without measuring identifier/code-token recall (open risk §4.3).

### 2.2 PII / secret detection — `security/pii_detector.py`

- `PIIMatch` (type, value, start, end, …); `DetectionResult` (matches, masked text).
- Default detector API: `detect_and_mask_pii(content) -> DetectionResult` (L436); already used by `mcp/server.py` L437–439 as a pre-egress mask.
- `MaskingStrategy`: `FULL` → literal `[REDACTED]`; `PARTIAL` (default) → e.g. `a***z@domain`; `HASH`; `PLACEHOLDER` (per-type placeholders, fallback `[REDACTED]`).
- Coverage already includes API-key / private-key / AWS / GitHub / OpenAI / Anthropic shapes and PEM headers (recon §3.1). Phase 5 tests should probe JWT, `.env` assignment lines, connection strings, SSH PEM if gaps appear.
- **Gap vs threat model:** architecture locked token is `[REDACTED_SECRET]` (with `[REDACTED]` as legacy alias) — `LS-MEM-ARCHITECTURE.md` L19. There is **no** `SecretScanner` class and **no** `REDACTED_SECRET` string anywhere under `src/ai_company` (grep 2026-09-24). LS-MEM must either extend `PIIDetector` strategies or wrap it so the canonical token is what lands on disk. Current FULL strategy emits `[REDACTED]` only.

### 2.3 Content filter — `security/content_filter.py`

- `ThreatLevel` (SAFE / SUSPICIOUS / DANGEROUS / BLOCKED), `FilterResult`, `ContentFilter.scan()`.
- Complements secret scan with prompt-injection / exfiltration phrase screen (recon §3.2). Wire before persist, same pipeline stage as ADR-019 constitutional blocklist (they are different mechanisms — keep both; blocklist is memory-capture policy, content filter is adversarial-content screen).

### 2.4 At-rest encryption — `security/memory_encryption.py` + `encryption_key_manager.py`

- AES-256-GCM; wire format `ENC:<base64(nonce||ciphertext)>` (12-byte nonce).
- Key derivation: HKDF-SHA256 from master secret `MEMORY_ENCRYPTION_KEY` env (fallback `JWT_SECRET_KEY`); key metadata persisted at `security/memory_keys.json`; dual-key rotation window supported.
- `MemoryStore.enable_encryption(key_manager)` hooks `_encrypt_content` on write and `_decrypt_content` on recall/search/scoring. Plaintext legacy entries pass through unchanged (backward compat).
- Optional for LS-MEM `.lightspeed/memory/memory.db` when master secret present (recon §3.7). Restricted-class fields should never rely on FTS over ciphertext without a parallel plaintext-safe index strategy (open risk §4.5).

### 2.5 Consolidation / forgetting — `memory/consolidation.py` + `engine.consolidate_all`

- `ConsolidationConfig`: `tick_interval=50`, `entry_threshold=500`, `max_episodic_age_days=90`, `max_entries_per_type=2000`.
- `ConsolidationScheduler.on_tick()` called from executor loop; runs `consolidate_all()` + `prune()` (GAP-005).
- `consolidate_all()` (engine L582+): per-type dedup of duplicate content (keep earliest), `_digest_episodic(max_age_days=30)` (pinned exempt), `_flag_stale_entries()`.
- `prune()`: age + cap; pinned always kept; unpinned sorted by access then recency; vector index de-indexes dropped ids.
- **Forgetting is a feature:** LS-MEM lifecycle states ACTIVE → SUPERSEDED → ARCHIVED / EXPIRED must preserve these guarantees under ADR-025 rule 4.

### 2.6 Vector / semantic (optional layer) — `memory/vector_store.py`

- Layered **on top of** MemoryStore (not a separate store); cosine similarity with substring fallback; `_WRITE_LOCK` + `os.replace` retries; `sentence-transformers` (not Ollama) in current path.
- LS-MEM Phase 2: FTS5 primary; Ollama `nomic-embed-text` (localhost only) optional Tier-2 rerank; never cloud fallback (recon C3; architecture locked decision 5). Legacy `memory/vector_index/` stays for JSON store only.

### 2.7 Audit — `data/audit_store.py`

- `AuditStore.write` / `write_batch` → `audit_events` table; `search_events` + combined FTS+SQL filters + timeline queries.
- LS-MEM should append local audit events (hash + metadata only for external transfers; threat model export rules).

---

## 3. Proposed `src/ai_company/lsmem/` interface sketch

**PROPOSED layout** (recon §5 + ADR-025 rule 1). Package location `src/ai_company/lsmem/`; data dir `.lightspeed/memory/` (gitignored); skill content dual-path `.agents/skills/ls-memory/` + `.opencode/skills/ls-memory/` (byte-identical; discovery authority `.agents/skills/`).

```text
src/ai_company/lsmem/
  engine.py       # SQLite + FTS5 CRUD + lifecycle (stdlib sqlite3 only)
  scoring.py      # value score 0–5, tier routing, injection quota
  redaction.py    # pre-write secret scan → [REDACTED_SECRET]
  gateway.py      # permission gateway, default-deny
  audit.py        # local audit append (or thin wrapper over AuditStore)
  bridge.py       # one-way import: MemoryStore JSON → lsmem SQLite (dry-run default)
  cli.py          # typer; also thin scripts memory-store / memory-search / …

.lightspeed/memory/
  config.yaml
  memory.db       # NEVER git add/commit/push
  audit/
```

### 3.1 Core operations (handoff §12 — exact op names)

Agents must not need to understand the underlying database. Conceptual surface:

```text
memory.remember(...)   # screen (secret + content filter + ADR-019-style veto)
                        # → classify → score 0–5 → tier route → encrypt if needed → INSERT + FTS
memory.search(...)     # FTS5 MATCH (+ optional Ollama rerank) → rank → quota
memory.recall(...)     # session/scoped read; bump access_count; classification filter
memory.inspect(...)    # metadata/provenance/lifecycle/status for one id
memory.forget(...)     # soft-delete / status ARCHIVED + audit (Tier 3 extra confirm)
memory.purge(...)      # hard-delete row + FTS; elevated confirmation; audit actor
memory.export(...)     # re-redaction; default excludes RESTRICTED; human scope confirm
memory.status(...)     # counts, tier mix, size, last consolidation
memory.audit(...)      # local audit query
memory.rebuild(...)    # rebuild FTS (+ optional vector) index from base table
```

Naming bridge to existing store: JSON store already has `store`/`recall`/`search`/`prune`/`consolidate` — LS-MEM should keep those semantics where possible and add `remember` as the screened write (handoff name), so CLI/scripts can map 1:1.

### 3.2 Record schema (handoff §8 minimum fields — preserve concepts)

```json
{
  "id": "unique-id",
  "type": "decision",
  "title": "Decision title",
  "content": "Memory content",
  "source": "agent-session",
  "project": "light-speed-holdings",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "classification": "internal",
  "confidence": 1.0,
  "tags": [],
  "provenance": {},
  "created_by": "agent",
  "verified_by": null,
  "approved_for_external_use": false
}
```

Plus LS-MEM-specific: `status` (ACTIVE/SUPERSEDED/ARCHIVED/EXPIRED), `value_score` (0–5), `tier` (1–3), `access_count`, FTS rowid mapping. JSON `MemoryEntry` fields map: `content`→`content`, `tags`→`tags`, `agent_id`→`created_by`, `metadata.status`→`status`, `access_count`→`access_count`.

### 3.3 Four classifications (handoff §9)

| Tier | Name | Examples | Persistence rule |
|------|------|----------|------------------|
| 1 | PUBLIC | published site/docs/articles/marketing | normal |
| 2 | INTERNAL | architecture, roadmaps, agent instructions | normal |
| 3 | CONFIDENTIAL | clients, proposals, pricing, contracts, strategy | normal + gateway on egress |
| 4 | RESTRICTED | passwords, API keys, tokens, private keys, creds, highly sensitive PII | **never plaintext**; secret scan should prevent most; encrypt or refuse |

Ambiguous classification → BLOCK (threat model default posture).

### 3.4 Value score → tier routing (architecture L131; recon §9 tests)

| Score | Action |
|-------|--------|
| 0–1 | discard (do not persist long-term) |
| 2 | Tier 1 (short lifetime) |
| 3–4 | Tier 2 |
| 5 | Tier 3 (human-verified / institutional; requires `verified_by`) |

Only score ≥ 3 persists long-term (threat T08). Value scoring, lifecycle/supersession, hybrid retrieval, and secret redaction are system-directive requirements (recon header).

### 3.5 Permission gateway

- Default-deny before any cross-process / external read or write (threat T14–T18, T24; architecture component `gateway.py`).
- Network deny-by-default in engine core; only explicit `127.0.0.1`/`localhost` for Ollama; no `requests`/`httpx` in engine core for other origins.
- LS-MEM tools never call MCP; memory content not passed to MCP without gateway + human approval.
- Explicit markers (handoff §11): `<memory>`, `<no-memory>`, `<private>`, `<external-approved>` (or OpenCode-equivalent).

### 3.6 One-way import bridge (ADR-025 rule 3)

Direction: **JSON MemoryStore → LS-MEM only**. No silent dual-write. Default **dry-run** (report what would be imported; actual writes require explicit flag). Type mapping (6 → 13) must be documented in Phase 3 data model — see §5 of this brief for the proposed table; mapping is lossy and must be reviewed before first real import.

Authority during coexistence (ADR-025): JSON store authoritative for existing ADR-019 consumers (Phases 2–4+); LS-MEM authoritative for new `ls-memory` skill writes and post-import-confirmed rows. Long-term single-engine choice is a **future ADR**, not this generation of work.

### 3.7 CLI / skill packaging

- Primary: Python 3.12+, `typer`, exposed as `ai-company memory …` **and** thin `memory-store` / `memory-search` / … wrappers under skill `scripts/` (recon §8).
- Skill: `SKILL.md` YAML frontmatter, name `ls-memory`, dual content-identical deploy paths, hash-checked in tests (ADR-025 rule 5).
- Config: YAML; schema: JSON Schema. Zero new runtime deps for core (stdlib `sqlite3`, `json`, `hashlib`, `re`).

---

## 4. Open risks (numbered)

1. **Dual-store authority drift (C1 High, ADR-025 residual).** Two vocabularies (6 vs 13), two governance implementations, two write paths. Mitigation: authority table in Phase 3 data model + dry-run bridge + no dual-write; closes only on future consolidation ADR. Residual: operators/agents may read the wrong store until tooling forces the choice.

2. **6→13 type mapping is lossy.** `episodic`/`temporal` both collapse toward `session`/`task`/`observation`/`milestone`; `aggregate` has no obvious 13-type twin (maps to post-consolidation `lesson`/`document`?); `relational` splits into `entity` (+ edges in `provenance`?). Bad mapping silently corrupts migration. Mitigation: dry-run report showing every row’s proposed type; human review of edge cases before first real import; schema versioning on lsmem.

3. **FTS5 tokenizer vs code identifiers / camelCase / paths.** Default unicode61 tokenization splits on non-word chars — `ai_company.memory.engine` and `MemoryStore` may tokenize poorly vs natural language. Existing audit/tasks FTS has the same limitation and was accepted there, but memory recall is higher-stakes for executor quality. Mitigation: measure on real `memory/*.json` corpus before declaring FTS primary sufficient; consider token or trigram experiments only as FTS-side options, not new deps; keep LIKE/substring fallback like `audit_store`.

4. **Encryption key management.** Master secret fallback to `JWT_SECRET_KEY` couples memory confidentiality to JWT config; `security/memory_keys.json` metadata + rotation window must be documented for operators; FTS over encrypted `content` yields useless ranks (index plaintext title/tags only, or exclude Restricted from FTS). Risk of unrecoverable data if env secret lost.

5. **Dual-path skill hash drift.** `.agents/skills/ls-memory` vs `.opencode/skills/ls-memory` must stay byte-identical (threat open item 4). Process risk: one side edited, hash test fails late or is skipped. Mitigation: CI hash check mandatory; discovery remains `.agents/` only.

6. **`tree-ring-memory` semantic collision.** Skill already present in `.agents/skills/` (recon C7). Two local memory narratives can confuse agents about which tool to call. Mitigation: curation-policy difference note (tree-ring = lifecycle practice notes; ls-memory = engine + skill); consider retiring or cross-linking in skill descriptions.

7. **Redaction token mismatch.** Locked token `[REDACTED_SECRET]` vs existing `PIIDetector` FULL/PLACEHOLDER → `[REDACTED]`. Without a wrapper, exports and stores will disagree with threat-model acceptance tests. Mitigation: implement `redaction.py` as the single write-path gate that normalizes to `[REDACTED_SECRET]` (accept `[REDACTED]` on read).

8. **No secret-scanner symbol in code yet.** Grep for `SecretScanner|REDACTED_SECRET|secret.?scan` under `src/ai_company` is empty (only `detect_and_mask_pii`). Any brief or ticket that says “reuse the secret scanner” means “reuse `PIIDetector` + new wrapper,” not an existing scanner class.

9. **`.lightspeed/memory/` git-safety.** Recon flagged ignore gap; ADR-025 rule 7 says gitignored + test. Risk: partial ignore or agent `git add -f`. Mitigation: ignore rule + e2e test that `git status` stays clean after store (recon §9).

10. **Recall latency budget vs dual engines.** Executor pre-execute recall already hits JSON store; adding LS-MEM without a merge/quota policy risks doubled latency and double-counted context. Mitigation: single recall façade later; Phase 2 keep JSON path unchanged for executor; quota 5–15 results / ~1–2k tokens on LS-MEM injection path.

11. **ADR number collision note for orchestrator.** `docs/adr/025-lsmem-sqlite-engine-coexistence.md` (Accepted) is the memory ADR. A **different** file `docs/architecture/adr/025-agent-consolidation-152-to-90.md` also uses number 025 for agent roster consolidation. Do not cite “ADR-025” without the path. STATUS/handoff references to ADR-025 mean the LS-MEM coexistence ADR.

12. **Working-tree dirt (recon C5).** Unrelated modified files in the repo. Bridge/engine work must not stage or commit unrelated changes.

---

## 5. Reference files

| File | Why it matters |
|------|----------------|
| `src/ai_company/memory/engine.py` | 6 types, `MemoryEntry`, store/recall/search/prune/consolidate, encryption hooks |
| `src/ai_company/memory/governance.py` | ADR-019 policies: TTLs, staleness 180d, MIN_KNOWLEDGE_LENGTH=40, constitutional blocklist, supersede, pin |
| `src/ai_company/memory/consolidation.py` | `ConsolidationConfig` / scheduler wiring (GAP-005) |
| `src/ai_company/memory/vector_store.py` | optional semantic layer over MemoryStore |
| `src/ai_company/memory/integration.py` | `init_memory`, learning flag, recall_context, record_* helpers |
| `src/ai_company/store/file_store.py` | atomic JSON persistence, quarantine/`.bak` recovery |
| `memory/*.json` | live 6-type corpus (gitignored) |
| `src/ai_company/data/database.py` | `SCHEMA_VERSION=5`, FTS5 DDL + triggers for audit/tasks |
| `src/ai_company/data/audit_store.py` | FTS5 MATCH + LIKE fallback pattern |
| `src/ai_company/data/search.py` | tasks/audit FTS search |
| `src/ai_company/security/pii_detector.py` | PII/secret detect + mask strategies (`[REDACTED]`) |
| `src/ai_company/security/content_filter.py` | ThreatLevel / ContentFilter.scan |
| `src/ai_company/security/memory_encryption.py` | AES-256-GCM `ENC:` format |
| `src/ai_company/security/encryption_key_manager.py` | HKDF, `MEMORY_ENCRYPTION_KEY`, rotation |
| `docs/adr/019-memory-knowledge-governance.md` | governance ADR |
| `docs/adr/025-lsmem-sqlite-engine-coexistence.md` | Accepted: new engine + one-way bridge; 7 rules |
| `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md` | §8 13 types + record fields, §9 4 classifications, §10 redaction, §11 markers, §12 core ops, §13 FTS5/no vector DB |
| `docs/architecture/LS-MEM-RECONNAISSANCE.md` | reusables 1–10, conflicts C1–C9, package sketch, test strategy |
| `docs/architecture/LS-MEM-ARCHITECTURE.md` | locked decisions (dual path, bridge, `[REDACTED_SECRET]`, Ollama optional, storage path), value-score tiers |
| `docs/security/LS-MEM-THREAT-MODEL.md` | T01–T28, default-deny gateway, offline posture, export/redaction tests |
| `docs/SKILL_CURATION_POLICY.md` | skill discovery authority = `.agents/skills/`; third-party transmission ban |
| `docs/architecture/adr/025-agent-consolidation-152-to-90.md` | **different ADR-025** (agent roster) — citation hazard |
| `src/ai_company/cli/memory.py` | existing CLI surface (455 lines) to keep working |
| `harness/changes/parking/2026-09-24-ls-mem-phase-2-architecture/` | prior parked Phase 2 change (spec/plan/tasks stubs) |

---

## 6. Proposed 6→13 type mapping (for bridge dry-run)

**PROPOSED — not yet in a Phase 3 data model; requires human review before first real import.**

| Legacy type | Proposed LS-MEM type(s) | Notes / lossiness |
|-------------|-------------------------|-------------------|
| `episodic` | `session` + `observation` (+ `task` if outcome-like) | primary landing `session`; event-like rows `observation`; split heuristic needed (metadata presence of task ids?) |
| `semantic` | `architecture` \| `decision` \| `requirement` \| `entity` \| `document` | heuristic on tags/metadata; cannot auto-split safely without a classifier — default `document`, dry-run flags low-confidence |
| `procedural` | `lesson` (or `solution`) | how-to → `lesson`; resolved fix recipes → `solution` if `GOOD_PATTERN` metadata present |
| `relational` | `entity` | edges stuffed into `provenance`/`tags`; true graph edges deferred |
| `temporal` | `milestone` \| `session` | dated milestones → `milestone`; otherwise `session` timestamps |
| `aggregate` | `lesson` \| `document` | rollups → `lesson` when insight-like; else `document` |

Default when ambiguous: **`observation`** with `metadata.legacy_type` preserved and `confidence` lowered — never drop rows on import. Always copy `id` (or remap with mapping table), `created_at`, `access_count`, `status`, pinned/vetoed/superseded flags.

---

*End of brief. File count: 1. No other paths modified by this task.*
