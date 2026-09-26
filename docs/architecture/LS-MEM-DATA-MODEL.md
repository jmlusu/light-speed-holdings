# LS-MEM Phase 3 — Data Model

**Project:** LightSpeed Holdings — LIGHTSPEED MEMORY (LS-MEM)
**Date:** 2026-09-24
**Status:** Phase 3 Data Model (depends on approved Phase 1 threat model + Phase 2 architecture)
**Security classification:** Internal
**Prerequisites:**
- Phase 1: `docs/security/LS-MEM-THREAT-MODEL.md` (Approved — CEO/security sign-off 2026-09-24)
- Phase 2: `docs/architecture/LS-MEM-ARCHITECTURE.md` (18/18 subsystems + interface specs)
- Governance: `docs/adr/019-memory-knowledge-governance.md` (ADR-019 TTLs, staleness, supersede, pin, constitutional veto)
- Coexistence: **ADR-025** (`docs/adr/025-lsmem-sqlite-engine-coexistence.md` — Accepted; JSON MemoryStore retained + one-way import bridge)

---

## 1. Schema Versioning

```yaml
# .lightspeed/memory/config.yaml
schema_version: 1
engine: sqlite+fts5
created_at: "2026-09-24T00:00:00Z"
migration_history: []
```

All DDL changes must increment `schema_version` and add a forward-only migration in `migrations/`.

---

## 2. Core Memory Table (13 Types)

```sql
CREATE TABLE memories (
    -- Identity
    id              TEXT PRIMARY KEY,              -- UUID v4
    type            TEXT NOT NULL,                 -- one of 13 types below
    title           TEXT NOT NULL,
    content         TEXT NOT NULL,                 -- redacted if RESTRICTED hit

    -- Provenance
    source          TEXT NOT NULL,                 -- agent_id | human | import | consolidation | system
    project         TEXT NOT NULL,                 -- workspace/project identifier
    created_by      TEXT NOT NULL,                 -- agent_id or "human"
    created_at      TEXT NOT NULL,                 -- ISO 8601 UTC
    updated_at      TEXT NOT NULL,                 -- ISO 8601 UTC

    -- Classification (locked decision 3: Restricted never plaintext)
    classification  TEXT NOT NULL DEFAULT 'INTERNAL',  -- PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED
    confidence      REAL NOT NULL DEFAULT 0.5,     -- 0.0–1.0
    tags            TEXT DEFAULT '[]',             -- JSON array of strings

    -- Governance (ADR-019 mapping)
    ttl_days        INTEGER,                       -- NULL = no expiry; per-type default from ADR-019
    stale_at        TEXT,                          -- ISO 8601; set when staleness detected (180 days default)
    superseded_by   TEXT,                          -- FK to memories.id (newest-wins conflict resolution)
    pinned          INTEGER NOT NULL DEFAULT 0,    -- 1 = curator pin exempt from age pruning
    constitutional_block BOOLEAN NOT NULL DEFAULT 0, -- ADR-019 veto flag
    verified_by     TEXT,                          -- NEW for Tier 3: human verifier agent_id/timestamp
    tier            INTEGER NOT NULL DEFAULT 1,    -- 1=Tier1 (score 2), 2=Tier2 (score 3-4), 3=Tier3 (score 5, human-verified)

    -- External Access
    approved_for_external_use BOOLEAN NOT NULL DEFAULT 0,
    external_approval_token   TEXT,               -- opaque token from gateway when approved

    -- Lifecycle
    status          TEXT NOT NULL DEFAULT 'ACTIVE', -- ACTIVE | SUPERSEDED | ARCHIVED | EXPIRED | PURGED
    deleted_at      TEXT,                          -- ISO 8601; set on forget/purge
    delete_actor    TEXT,                          -- who deleted

    -- FTS / Vector
    fts_rowid       INTEGER,                       -- FTS5 rowid for join
    vector_id       TEXT,                          -- optional vector index reference

    -- Audit linkage
    correlation_id  TEXT NOT NULL                  -- UUID v4; groups related operations
);

CREATE INDEX idx_mem_project_type ON memories(project, type);
CREATE INDEX idx_mem_classification ON memories(classification);
CREATE INDEX idx_mem_status ON memories(status);
CREATE INDEX idx_mem_stale_at ON memories(stale_at);
CREATE INDEX idx_mem_correlation ON memories(correlation_id);
CREATE INDEX idx_mem_verified_by ON memories(verified_by);
```

---

## 3. 13 Memory Types (Handoff §8)

| # | Type | Description | Default TTL (days) | ADR-019 Governance Notes |
|---|------|-------------|-------------------|--------------------------|
| 1 | **observation** | Raw fact, event, or data point captured during work | 365 | Tier 1 default; staleness at 180d; pin for institutional facts |
| 2 | **decision** | Explicit choice with rationale, alternatives, trade-offs | 730 | Tier 2+; constitutional veto applies; pin = immutable |
| 3 | **architecture** | System/component design, interface contracts, data flows | 1095 | Tier 2+; supersede on major refactor; verified_by required for Tier 3 |
| 4 | **requirement** | Functional/non-functional requirement, acceptance criteria | 730 | Tier 2; supersede on scope change; trace to decision |
| 5 | **preference** | User/agent preference, style guide, convention | 365 | Tier 1; low-confidence; supersede on explicit override |
| 6 | **task** | Work item, milestone step, action item | 180 | Tier 1; auto-expire on completion; purge after 90d |
| 7 | **milestone** | Significant delivery, release, or phase gate | 1095 | Tier 2+; pin by default; verified_by for Tier 3 |
| 8 | **bug** | Defect, regression, or unexpected behavior | 365 | Tier 1; supersede on fix; link to decision/solution |
| 9 | **solution** | Verified fix, workaround, or pattern | 730 | Tier 2+; verified_by for Tier 3; supersede on better solution |
| 10 | **lesson** | Postmortem insight, anti-pattern, or retrospective finding | 730 | Tier 2+; constitutional veto applies; pin for org-wide lessons |
| 11 | **entity** | Person, org, system, component, or concept reference | 1095 | Tier 1; rarely superseded; update on rename |
| 12 | **document** | Artifact reference (spec, RFC, contract, report) | 1095 | Tier 1; version tracked via superseded_by |
| 13 | **session** | Session context, injected memories, continuity anchor | 30 | Tier 1; auto-expire; never pinned |

---

## 4. 6 → 13 Type Mapping (Import Bridge)

The one-way import bridge (ADR-025 Decision Rule 3) maps legacy JSON `MemoryStore` types to LS-MEM:

| JSON MemoryStore Type (6) | LS-MEM Type (13) | Mapping Logic | Confidence Default |
|---------------------------|------------------|---------------|-------------------|
| `episodic` | `observation` | Direct — raw episodic captures | 0.7 |
| `semantic` | `lesson` | Consolidated knowledge → lesson | 0.8 |
| `procedural` | `solution` | How-to / procedure → verified solution | 0.8 |
| `relational` | `entity` | Relationships → entity references | 0.7 |
| `temporal` | `session` | Time-bound context → session anchors | 0.6 |
| `aggregate` | `decision` | Synthesized conclusions → decisions | 0.8 |

**Mapping Rules:**
1. Each JSON record produces **exactly one** LS-MEM record (no fan-out).
2. `content` field copied verbatim; secret scanner re-runs on import (may upgrade classification to RESTRICTED).
3. `provenance` field → `source` = "import"; `created_by` = original agent_id or "legacy".
4. ADR-019 governance fields mapped per §5 below.
5. `verified_by` = NULL (imported records start at Tier 1; human review promotes to Tier 3).
6. Dry-run mode (`--dry-run`) emits proposed rows as JSONL to stdout; writes nothing.

---

## 5. ADR-019 Governance Column Mapping (ADR-025 Decision Rule 4)

| ADR-019 Concept | LS-MEM Column | Mapping Notes |
|-----------------|---------------|---------------|
| **TTL per type** | `ttl_days` | Default from table §3; NULL = infinite; configurable in `config.yaml` |
| **Staleness detection (180d)** | `stale_at` | Computed on write: `created_at + 180 days` (or type-specific); refreshed on access |
| **Conflict → supersede (newest-wins)** | `superseded_by` | On `remember` with same `(project, type, title)`: old row `status`=SUPERSEDED, `superseded_by`=new_id |
| **Pinned entries win** | `pinned` (BOOLEAN) | `pin` CLI sets `pinned=1`; pinned rows excluded from age pruning and auto-supersede |
| **Constitutional capture veto** | `constitutional_block` | `CONSTITUTIONAL_BLOCKLIST` patterns in content → `constitutional_block=1`, `status`=ARCHIVED, audit `vetoed` |
| **Curator pin/unpin** | `pinned` + `verified_by` | Pin = `pinned=1`; Unpin = `pinned=0`; Tier 3 requires `verified_by` non-null |
| **Tier 3 `verified_by` gap** | `verified_by` + `tier=3` | **NEW** — human verifier agent_id + ISO timestamp; required for Tier 3 promotion |

**Tier Thresholds (from recon §9, ADR-019):**
- Score 0–1 → **Discard** (not persisted)
- Score 2 → **Tier 1** (`tier=1`, `ttl_days` default)
- Score 3–4 → **Tier 2** (`tier=2`, `ttl_days` extended +50%)
- Score 5 → **Tier 3** (`tier=3`, `verified_by` required, `ttl_days` = NULL/infinite, `pinned=1` by default)

---

## 6. Lifecycle States

| State | Meaning | Transitions | Retention |
|-------|---------|-------------|-----------|
| **ACTIVE** | Normal, searchable, injectable | → SUPERSEDED (on conflict), → ARCHIVED (stale + not pinned), → EXPIRED (TTL elapsed), → PURGED (operator) | Per `ttl_days` |
| **SUPERSEDED** | Replaced by newer version | → ARCHIVED (age), → PURGED | 90 days after supersede |
| **ARCHIVED** | Stale/vetoed; excluded from recall/search | → PURGED (operator or age) | 1 year |
| **EXPIRED** | TTL elapsed; not pinned | → PURGED (auto after grace period) | 30 days grace |
| **PURGED** | Hard-deleted; physically removed | Terminal | Immediate (WAL checkpoint) |

**Transition Rules:**
- `forget` (soft-delete): `status`=ARCHIVED, `deleted_at`=now, `delete_actor`=caller; reversible within 90 days via `memory-store --restore <id>`.
- `purge` (hard-delete): Requires elevated confirmation (`--confirm-purge`); physical row + FTS entry removed; `status`=PURGED; audit `memory_purged`.
- Tier 3 (human-verified) `purge` requires **two** independent confirmations (operator + Architecture Lead).
- Pinned entries (`pinned=1`) **never** transition to SUPERSEDED/ARCHIVED/EXPIRED automatically — only via explicit operator action.

---

## 7. FTS5 Virtual Table

```sql
CREATE VIRTUAL TABLE memories_fts USING fts5(
    title, content,
    content='memories',
    content_rowid='rowid',
    tokenize='unicode61 remove_diacritics 1 tokenchars "_"'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER memories_ai AFTER INSERT ON memories BEGIN
    INSERT INTO memories_fts(rowid, title, content) VALUES (new.rowid, new.title, new.content);
END;

CREATE TRIGGER memories_ad AFTER DELETE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, title, content) VALUES ('delete', old.rowid, old.title, old.content);
END;

CREATE TRIGGER memories_au AFTER UPDATE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, title, content) VALUES ('delete', old.rowid, old.title, old.content);
    INSERT INTO memories_fts(rowid, title, content) VALUES (new.rowid, new.title, new.content);
END;
```

**Search Query Pattern:**
```sql
SELECT m.*, bm25(memories_fts) AS rank
FROM memories_fts
JOIN memories m ON m.rowid = memories_fts.rowid
WHERE memories_fts MATCH ? AND m.status = 'ACTIVE' AND m.classification != 'RESTRICTED'
  AND (m.superseded_by IS NULL) AND (m.constitutional_block = 0)
ORDER BY rank + (m.tier * 10) + (julianday('now') - julianday(m.updated_at)) * -0.1
LIMIT ?;
```

---

## 8. Audit Table (Tamper-Evident Chain)

```sql
CREATE TABLE audit_log (
    event_id        TEXT PRIMARY KEY,              -- UUID v4
    event_type      TEXT NOT NULL,                 -- enum (see §10.1 schema)
    timestamp       TEXT NOT NULL,                 -- ISO 8601 UTC
    actor           TEXT NOT NULL,                 -- agent_id or "human"
    correlation_id  TEXT NOT NULL,                 -- UUID v4; links related ops
    details         TEXT DEFAULT '{}',             -- JSON
    payload_hash    TEXT NOT NULL,                 -- sha256:...
    prev_hash       TEXT NOT NULL                  -- sha256:... (chain)
);

CREATE INDEX idx_audit_correlation ON audit_log(correlation_id);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_actor ON audit_log(actor);
```

**Chain Verification**: `memory-audit verify` reads all records in timestamp order, recomputes `sha256(canonical_json(prev_record))`, compares to `prev_hash`. Any mismatch → FAIL.

---

## 9. External Transfer Audit Minimum (Handoff §21)

For `event_type = 'gateway_approved'` or `'export'` with external destination, `details` JSON must include:
```json
{
  "request_id": "uuid",
  "agent": "agent_id",
  "provider": "provider_name",
  "operation": "embedding|inference|retrieval|storage|notification",
  "destination": "domain_or_endpoint",
  "data_classification": "PUBLIC|INTERNAL|CONFIDENTIAL|RESTRICTED",
  "payload_hash": "sha256:...",
  "approved_by": "human_identity",
  "approved_at": "ISO8601",
  "result_stored_locally": true
}
```

---

## 10. Config Schema (`schemas/config.schema.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["schema_version", "engine", "storage", "fts", "injection", "audit", "gateway"],
  "properties": {
    "schema_version": { "type": "integer", "minimum": 1 },
    "engine": { "type": "string", "const": "sqlite+fts5" },
    "storage": {
      "type": "object",
      "required": ["workspace_path", "global_path"],
      "properties": {
        "workspace_path": { "type": "string", "default": ".lightspeed/memory" },
        "global_path": { "type": "string", "default": "~/.lightspeed/memory" }
      }
    },
    "fts": {
      "type": "object",
      "properties": {
        "tokenizer": { "type": "string", "default": "unicode61" },
        "remove_diacritics": { "type": "boolean", "default": true },
        "tokenchars": { "type": "string", "default": "_" },
        "stopwords": { "type": "array", "items": { "type": "string" }, "default": ["the","a","an","and","or","but","in","on","at","to","for","of","with","by"] }
      }
    },
    "injection": {
      "type": "object",
      "required": ["max_memories", "max_tokens", "min_value_score", "exclude_superseded", "exclude_vetoed"],
      "properties": {
        "max_memories": { "type": "integer", "default": 15, "minimum": 1, "maximum": 50 },
        "max_tokens": { "type": "integer", "default": 2000, "minimum": 500 },
        "min_value_score": { "type": "integer", "default": 2, "minimum": 1, "maximum": 5 },
        "exclude_superseded": { "type": "boolean", "default": true },
        "exclude_vetoed": { "type": "boolean", "default": true }
      }
    },
    "audit": {
      "type": "object",
      "properties": {
        "retention_days_crud": { "type": "integer", "default": 90 },
        "retention_days_gateway": { "type": "integer", "default": 365 }
      }
    },
    "gateway": { "$ref": "gateway.schema.json" }
  }
}
```

---

## 11. Memory Schema for Export/Import (`schemas/memory.schema.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "type", "title", "content", "source", "project", "created_by", "created_at", "updated_at", "classification", "confidence", "tags", "status", "correlation_id"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "type": { "type": "string", "enum": ["observation","decision","architecture","requirement","preference","task","milestone","bug","solution","lesson","entity","document","session"] },
    "title": { "type": "string", "minLength": 1 },
    "content": { "type": "string" },
    "source": { "type": "string" },
    "project": { "type": "string" },
    "created_by": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" },
    "classification": { "type": "string", "enum": ["PUBLIC","INTERNAL","CONFIDENTIAL","RESTRICTED"] },
    "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "tags": { "type": "array", "items": { "type": "string" } },
    "ttl_days": { "type": ["integer", "null"] },
    "stale_at": { "type": ["string", "null"], "format": "date-time" },
    "superseded_by": { "type": ["string", "null"], "format": "uuid" },
    "pinned": { "type": "boolean" },
    "constitutional_block": { "type": "boolean" },
    "verified_by": { "type": ["string", "null"] },
    "tier": { "type": "integer", "enum": [1,2,3] },
    "approved_for_external_use": { "type": "boolean" },
    "external_approval_token": { "type": ["string", "null"] },
    "status": { "type": "string", "enum": ["ACTIVE","SUPERSEDED","ARCHIVED","EXPIRED","PURGED"] },
    "deleted_at": { "type": ["string", "null"], "format": "date-time" },
    "delete_actor": { "type": ["string", "null"] },
    "correlation_id": { "type": "string", "format": "uuid" }
  }
}
```

---

## 12. Implementation Phasing (Post-Phase 3)

| Step | Deliverable | Depends On |
|------|-------------|------------|
| 5 | SQLite Memory Engine (`engine.py`) | This data model + Phase 2 arch |
| 6 | FTS5 Search (`search.py`) | Schema §7 |
| 7 | Privacy + Classification (`privacy.py`, `classification.py`) | Schema §2–§3 |
| 8 | Secret Detection (`redaction.py`) | Schema §2 `classification` + PIIDetector |
| 9 | Forget/Delete (`delete.py`) | Schema §6 lifecycle |
| 10 | Audit (`audit.py`) | Schema §8–§9 |
| 11 | OpenCode Skill (`SKILL.md` + policies) | All above |
| 12 | OpenCode Tools (`scripts/`) | Skill + CLI |
| 13 | Session Continuity (`injector.py`) | Schema §2 + §12.1 hook |
| 14 | Ollama Semantic Search (`vector.py`) | Schema §7 FTS + optional vector |
| 15 | Permission Gateway (`gateway.py`) | Schema §2 `approved_for_external_use` + §10.1 |
| 16 | External Transfer Approval | Gateway + audit |
| 17 | Security Testing (Phase 5 suite) | All above |
| 18 | Documentation (`USER-GUIDE.md`) | All above |
| 19 | Independent Security Audit | Threat model + 17 |
| 20 | Human Approval (CEO/CISO) | 19 |

---

## 13. Traceability

| Requirement | Section |
|-------------|---------|
| 13 memory types (handoff §8) | §3 |
| Minimum fields (handoff §8) | §2 |
| 6→13 mapping (ADR-025 Rule 3) | §4 |
| ADR-019 governance preservation (ADR-025 Rule 4) | §5 |
| Tier 3 `verified_by` gap (recon §3) | §5 (NEW column) |
| Lifecycle states (handoff §12, threat T28) | §6 |
| FTS5 schema (handoff §13) | §7 |
| Audit tamper-evidence (handoff §21) | §8 |
| External transfer minimum (handoff §21) | §9 |
| Config schema (architecture §9.1, §10.1, §12.1) | §10 |
| Export schema (handoff §8, §27) | §11 |

---

**Next:** Implementation begins with Step 5 — SQLite Memory Engine (`src/ai_company/lsmem/engine.py`).
