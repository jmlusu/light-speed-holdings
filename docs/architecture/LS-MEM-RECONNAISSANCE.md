# LS-MEM Phase 0 — Reconnaissance & Environment Audit

**Project:** LightSpeed Holdings
**Date:** 2026-09-23
**Status:** Complete (read-only audit; no system files modified except this report)
**Security classification:** Internal
**Handoff refs:** `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md`, system directive (4-tier hierarchy, value scoring 0–5, hybrid retrieval, lifecycle/supersession, secret redaction)

---

## 1. Current Architecture (relevant slice)

| Layer | Implementation | Location |
|-------|----------------|----------|
| Package / CLI | Python 3.12+ (Typer), package `ai-company` | `pyproject.toml`, `src/ai_company/` |
| Runtime | Python venv via `uv` (`.venv`), Windows 11 | project root |
| Existing memory engine | JSON `FileStore`-backed `MemoryStore`, 6 types (episodic, semantic, procedural, relational, temporal, aggregate) | `src/ai_company/memory/engine.py` |
| Existing memory governance | ADR-019 policy layer: constitutional veto, TTLs, staleness, conflict supersession, curator pin | `src/ai_company/memory/governance.py`, `docs/adr/019-memory-knowledge-governance.md` |
| Existing consolidation | `ConsolidationScheduler` + `MemoryStore.consolidate_all()` / `prune()` | `src/ai_company/memory/consolidation.py` |
| Existing semantic layer | `VectorStore` using `sentence-transformers` (not Ollama) with fallback to substring search | `src/ai_company/memory/vector_store.py` |
| Existing CLI | `ai-company memory` subcommands (list/add/search/…) | `src/ai_company/cli/memory.py` (455 lines) |
| Existing security modules | PII/secret pattern detector, content filter, AES memory encryption, RBAC | `src/ai_company/security/{pii_detector,content_filter,memory_encryption,encryption_key_manager,rbac}.py` |
| Existing FTS5 usage | SQLite FTS5 on audit events + tasks (not on memory) | `src/ai_company/data/database.py`, `audit_store.py`, `search.py` |
| Knowledge graph | graphify AST graph at `graphify-out/` | post-commit hook |
| Agent cards | Generated from `company-registry.yaml` → `.opencode/agents/*.md` | generator pipeline |
| Skills | OpenCode scans `.agents/skills/` at session start (verified in SKILL_CURATION_POLICY) | `.agents/skills/` (107 dirs) |
| OpenCode project config | `opencode.json` — local Ollama provider on `127.0.0.1:11434`, remote Resend MCP enabled | project root |

**Storage today:** root `memory/` directory with JSON type files (`semantic.json`, `episodic.json`, …), `memory/embeddings/`, `memory/vector_index/`. Git-ignored via `.gitignore` lines 73–74 (`memory/*.json`, `memory/vector_index/`).

---

## 2. Environment Audit

| Capability | Result |
|------------|--------|
| System Python | 3.11.9 (`python`) |
| Project venv Python | `.venv` present; `pyproject.toml` requires `>=3.12` |
| SQLite (system python) | 3.45.1, **FTS5 available** |
| SQLite (project venv) | **3.49.1, FTS5 available** |
| Node.js | v24.19.0 |
| uv | 0.12.5 |
| Ollama | 0.34.1 installed; models: `nomic-embed-text` (274 MB, embeddings), mistral-7b-32k, llama3.1-8b-32k, gemma4-12b-32k, qwen2.5-coder-7b-32k, deepseek-r1-64k |
| Ollama running now | No models loaded (`ollama ps` empty) — will auto-load on first embed call |
| sentence-transformers | Declared in project deps (`>=3.0`) + numpy |
| Network default posture | Handoff requires deny-by-default; project already has outbound deps (httpx, OTel, Resend MCP) — LS-MEM must not add new egress |

### Target deployment paths (from system directive)

| Target | Exists? | Notes |
|--------|---------|-------|
| `C:\Users\jmlus\.agents\skills\ls-memory` | **No** | Global skills root exists; ~31 user-scope skills present; no `ls-memory` |
| `C:\Users\jmlus\light-speed-holdings\.agents\skills\ls-memory` | **No** | Project skills root exists (107 skills); no `ls-memory` |

**Path conflict with handoff doc:** `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md` §18 places the skill at `.opencode/skills/ls-memory/`. The system directive and `docs/SKILL_CURATION_POLICY.md` both say OpenCode discovers skills from `.agents/skills/`. **Recommendation: implement under `.agents/skills/ls-memory` for both targets; treat `.opencode/skills/` as non-authoritative for discovery.** Confirm with CEO before diverging.

---

## 3. Components LS-MEM Can Reuse

1. **`PIIDetector` + API-key/private-key patterns** (`security/pii_detector.py`) — pre-write secret scan and `[REDACTED]` masking; already covers AWS, GitHub, OpenAI, Anthropic key shapes, private key PEM headers.
2. **`content_filter.py`** — prompt-injection / exfiltration phrase screen (complements secret scan).
3. **`MemoryGovernance` (ADR-019)** — retention TTLs, staleness, conflict→`superseded`, constitutional veto, pin semantics. Maps cleanly onto 4-tier model: episodic≈Tier 1 short, semantic/procedural≈Tier 2, aggregate≈consolidated, Tier 3 needs `verified_by` + institutional flag (gap).
4. **`MemoryStore.consolidate_all()` / `ConsolidationScheduler`** — dedup, digest, prune hooks for lifecycle manager.
5. **FTS5 patterns** in `data/database.py` + `audit_store.py` — proven create/search/fallback-to-LIKE approach to copy for memory FTS index.
6. **`VectorStore`** — local embedding index with graceful fallback; currently sentence-transformers, not Ollama (see conflicts).
7. **`memory_encryption.py` / `encryption_key_manager.py`** — optional at-rest encryption for `.lightspeed/memory/memory.db` if master secret present.
8. **`audit_store.py`** — local audit event persistence + FTS over audit.
9. **pytest + ruff + mypy + bandit** gates already wired (`pyproject.toml`, pre-commit) — LS-MEM tests inherit them.
10. **`.env` / `.env.example` conventions** — secrets live in gitignored env files, not code.

---

## 4. Potential Conflicts

| # | Conflict | Severity | Resolution direction |
|---|----------|----------|----------------------|
| C1 | **Two memory systems**: existing JSON `MemoryStore` (6 types) vs proposed SQLite FTS5 LS-MEM with 13 types + 4 tiers | High | Do not replace engine in Phase 2–4; either (a) LS-MEM as new local skill engine with import bridge from JSON store, or (b) extend `MemoryStore` to SQLite backend. Directive says build SQLite schema — prefer (a) with a documented migration path; ADR required. |
| C2 | Skill path: `.opencode/skills` (handoff) vs `.agents/skills` (directive + curation policy) | High | Prefer `.agents/skills/ls-memory`; note dual-path requirement is **global `C:\Users\jmlus\.agents\skills\` + project `.agents\skills\`**. |
| C3 | Existing semantic embeddings via sentence-transformers vs required Ollama embeddings | Medium | Keep FTS5 primary; Ollama `nomic-embed-text` optional Tier-2 rerank; never fall back to cloud; sentence-transformers path can remain for legacy `memory/vector_index`. |
| C4 | `.gitignore` lacks `.lightspeed/memory/` | High (Git safety) | Add ignore rule in Phase 2; do not commit DB. Note: root `memory/*.json` already ignored but directory itself not fully covered for new paths. |
| C5 | Working tree is heavily dirty (many unrelated modified/deleted files) | High (process) | **Do not stage or commit unrelated changes.** Only touch LS-MEM deliverables. Observation 0003 already warns about this exact failure. |
| C6 | Remote Resend MCP + remote model providers in `opencode.json` exist | Medium | LS-MEM itself must remain offline; do not route memory through MCP/LLM providers without permission gateway. |
| C7 | `tree-ring-memory` skill already in `.agents/skills/` | Medium | Semantic collision check per curation policy: document difference (tree-ring = lifecycle practice notes; ls-memory = engine + skill). |
| C8 | claude-mem-* skills deleted (uncommitted deletions in git status) | Info | Prior third-party memory stack retired 2026-09-23 — LS-MEM is the sanctioned replacement. |
| C9 | Global skill root `C:\Users\jmlus\.agents\skills` is outside this repo | Medium | Dual deployment means dual verification; project copy must not assume global paths for DB (DB should be workspace-relative `.lightspeed/memory/` per handoff; global skill needs its own data-dir resolution rule). |

---

## 5. Recommended Integration Points

```text
Phase 2+ implementation sketch (project):

.agents/skills/ls-memory/
  SKILL.md
  README.md
  policies/{privacy,classification,external-access,retention}.md
  schemas/memory.schema.json
  scripts/  (CLI entrypoints: memory-store/search/forget/status/…)
  tests/    (or repo tests/memory/)

src/ai_company/lsmem/          # optional shared Python package (preferred if reusing governance/pii)
  engine.py   # SQLite + FTS5
  scoring.py  # value score 0–5
  redaction.py
  gateway.py  # permission gateway
  audit.py
  cli.py      # wired into ai-company or standalone python -m

.lightspeed/memory/
  config.yaml
  memory.db          # gitignored
  audit/             # gitignored

docs/architecture/LS-MEM-{ARCHITECTURE,DATA-MODEL,RECONNAISSANCE}.md
docs/security/LS-MEM-{THREAT-MODEL,SECURITY-VERIFICATION,EXTERNAL-ACCESS}.md
tests/memory/
```

- **Session init injection:** keep lightweight; hook optional in executor recall path only after quota caps exist (`executor/loop.py` already has best-effort pre-exec recall).
- **Audit:** append to local audit store (hash + metadata only for external transfers).
- **Global vs project:** skill code is copy-synced; **memory DB is never shared across machines**; global skill resolves data dir as `<workspace>/.lightspeed/memory/` when opened in a project, else `~/.lightspeed/memory/` (document in user guide).

---

## 6. Security Observations

1. `.env` and `.env.*` ignored correctly; `.env.example` whitelisted.
2. Root `memory/*.json` ignored — good — but **`.lightspeed/memory/` is not yet ignored** (must add before any DB write).
3. Existing PII detector is the right pre-write gate; extend patterns for JWT, `.env` assignments, connection strings, SSH PEM if gaps found in Phase 5 tests.
4. `opencode.json` enables a **remote MCP (Resend)** — outside LS-MEM scope but relevant to threat model “unauthorized HTTP” boundary: LS-MEM tools must not call MCP.
5. No dedicated dependency allowlist tool beyond `docs/APPROVED-VENDORS.md` + skill curation policy — reuse those for any new package.
6. Prefer **stdlib `sqlite3` only** for core engine (zero new deps). Ollama HTTP client should be `urllib`/`httpx` localhost-only with explicit host allow `127.0.0.1`/`localhost`.
7. Bandit skips already documented in `pyproject.toml`; new SQL must use parameter binding (avoid new B608 suppressions).
8. Handoff Rule 5: never commit memory DB — enforce via `.gitignore` + test (git status clean after store).

---

## 7. Dependencies to Avoid

| Avoid | Why |
|-------|-----|
| Cloud vector DBs (Pinecone, Weaviate Cloud, Chroma cloud) | Violates local-first |
| OpenAI/Anthropic/Google embedding APIs | External AI default ban |
| Telemetry/analytics packages | No telemetry |
| New ORMs (SQLAlchemy) for v1 | stdlib sqlite3 sufficient |
| sentence-transformers **for new LS-MEM path** (optional later) | Heavy; Ollama already present; keep optional |
| Third-party “memory skills” (claude-mem, etc.) | Retired by skill curation policy |
| Auto `git add/commit` of memory paths | Git safety rule |

Allowed candidates (only if proven necessary): none for Phase 2–3 beyond existing project deps.

---

## 8. Proposed Implementation Language

- **Primary: Python 3.12+** (project convention, existing memory/security/audit code reuse, pytest/ruff/mypy/bandit gates).
- CLI: `typer` (already used) exposed as `ai-company memory …` **and** thin executable wrappers named `memory-store`, `memory-search`, etc. (directive names) under skill `scripts/`.
- Skill narrative: Markdown `SKILL.md` (YAML frontmatter, name `ls-memory`).
- Config: YAML (`pyyaml` already present).
- Schema: JSON Schema (`jsonschema` already present).

---

## 9. Proposed Test Strategy

| Suite | Location | Coverage |
|-------|----------|----------|
| Unit — scoring | `tests/memory/test_value_scoring.py` | 0–5 matrix, tier routing (0–1 discard, 2→T1, 3–4→T2, 5→T3) |
| Unit — redaction | `tests/memory/test_redaction.py` | API keys, JWT, private keys, `.env`, connection strings → `[REDACTED_SECRET]` before disk |
| Unit — lifecycle | `tests/memory/test_lifecycle.py` | status ACTIVE/SUPERSEDED/ARCHIVED/EXPIRED; supersession chain; no silent overwrite |
| Unit — gateway | `tests/memory/test_permission_gateway.py` | default deny; allowlist triple-check; ambiguous→BLOCK |
| Integration — FTS5 | `tests/memory/test_fts_search.py` | offline search, rank, quota 5–15 results / token cap |
| Integration — Ollama optional | `tests/memory/test_ollama_optional.py` | skip if down; no cloud fallback when down |
| Git safety | `tests/memory/test_git_safety.py` | after store: `git status` shows no `.lightspeed/memory` |
| E2E offline | marker `lsmem` or scripted | full CRUD + audit + export with network mocked/denied |
| Static | existing ruff/mypy/bandit | `uv run ruff check src/ && uv run mypy src/ && uv run pytest` |
| Dual-path verify | script | both skill dirs have identical SKILL.md + runnable scripts |

---

## 10. Deliverable Checklist (Phase 0)

- [x] Repository structure inspected
- [x] Git state inspected (dirty unrelated WIP — do not touch)
- [x] `.opencode` / `.agents/skills` / agents inventory
- [x] OpenCode config (`opencode.json`)
- [x] `.gitignore` gap identified (`.lightspeed/memory/`)
- [x] Package manifests (`pyproject.toml`, `package.json`)
- [x] Python/Node conventions
- [x] Existing security docs/modules
- [x] Existing memory architecture + ADR-019
- [x] Env-var conventions (`.env`, gitignored)
- [x] Ollama + `nomic-embed-text` present
- [x] Existing local AI integration (Ollama provider in opencode.json; sentence-transformers VectorStore)
- [x] OmniRoute: **not found** in this repo (no OmniRoute config files identified)
- [x] Logging: stdlib logging + dashboard logs; audit_store for structured audit
- [x] No credentials copied into this report

**Phase 0 exit:** ready for Phase 1 (threat model) pending CEO confirmation on skill path precedence (`.agents/skills` vs `.opencode/skills`) and engine strategy (new SQLite engine vs extend `MemoryStore`).
