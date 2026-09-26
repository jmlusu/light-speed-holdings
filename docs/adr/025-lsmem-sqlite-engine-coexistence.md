# ADR-025: LS-MEM SQLite Engine Coexistence with JSON MemoryStore

**Status:** Accepted
**Date:** 2026-09-24
**Deciders:** Human CEO (Jack Mlusu), CISO, Memory Owner, Solution Architect
**Technical Domain:** Memory / Local Storage / Security

## Context

LightSpeed Holdings currently operates **two memory systems** (one existing, one proposed):

- **Existing JSON `MemoryStore`** — lives at `src/ai_company/memory/` with **6 memory types** (episodic, semantic, procedural, relational, temporal, aggregate), governed by **ADR-019** (`docs/adr/019-memory-knowledge-governance.md`). ADR-019 provides the production policy layer: per-type TTL retention, staleness detection, conflict supersession (`newest-wins`, pinned entries exempt), constitutional capture veto (`CONSTITUTIONAL_BLOCKLIST`), and curator pin/unpin. Existing consumers (consolidation scheduler, CLI `ai-company memory`, executor recall path) already depend on this engine and its governance semantics.
- **Proposed LS-MEM engine** — new local-first SQLite + FTS5 memory system with **13 memory types** (observation, decision, architecture, requirement, preference, task, milestone, bug, solution, lesson, entity, document, session) and **4 data classifications** (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED), specified in `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md` and designed to ship behind the approved threat model.

**Recon conflict C1 (High)** — `docs/architecture/LS-MEM-RECONNAISSANCE.md` §4 flags the **coexistence risk**: dual sources of truth, migration confusion, and double maintenance if both engines run without an explicit relationship. Recon offers two resolution directions: (a) LS-MEM as a new engine with a one-way import bridge from the JSON store, or (b) extend `MemoryStore` with a SQLite backend. ADR required either way.

**Why not replace immediately:** `MemoryStore` is production-backed by ADR-019 governance (TTL, staleness, supersede, constitutional veto, pin). Replacing it mid-project risks data loss for the existing `memory/*.json` corpus and breaks existing consumers (consolidation, CLI, executor recall) before LS-MEM has demonstrated parity. The approved threat model (`docs/security/LS-MEM-THREAT-MODEL.md` line 8) **locks the decision**: *"dual skill paths (`.agents/skills` + `.opencode/skills`); new SQLite engine + bridge to existing JSON `MemoryStore`."* This ADR documents that CEO-locked decision; it does not re-open it.

**Cross-ref — dual skill paths are locked:** LS-MEM skill content ships as two content-identical copies — `.agents/skills/ls-memory/` and `.opencode/skills/ls-memory/` — per threat-model locked decisions. **Discovery authority remains `.agents/skills/`** (OpenCode scans that directory at session start; `.opencode/skills/` is non-authoritative for discovery) per `docs/SKILL_CURATION_POLICY.md`. The `.opencode/` copy exists for handoff-layout compatibility only and must stay hash-identical to the `.agents/` copy (threat-model open item 4).

## Decision

LS-MEM Phase 2 coexistence follows **recon option (a)** — a new engine plus a one-way import bridge. Seven numbered rules:

1. **New engine package location.** The LS-MEM engine lives in `src/ai_company/lsmem/` (proposed), with **SQLite + FTS5 as the primary storage and search layer** (stdlib `sqlite3`, no new ORM, no cloud vector DB). Workspace data dir is `.lightspeed/memory/`.

2. **JSON MemoryStore remains authoritative for its current consumers during Phases 2–4+.** All existing ADR-019 consumers (consolidation scheduler, `ai-company memory` CLI, executor recall path, `memory/*.json` corpus) continue to read and write the JSON `MemoryStore` unchanged until a future consolidation decision. LS-MEM does not take over these call sites in Phase 2–4.

3. **One-way import bridge: JSON MemoryStore → LS-MEM SQLite.** Migration direction is strictly **from** the existing JSON store **into** LS-MEM (mapping 6 legacy types into the 13-type schema), with the migration path documented in the Phase 3 data model (`docs/architecture/LS-MEM-DATA-MODEL.md`). **No silent dual-write**: writes never fan out to both engines implicitly; operators choose the write path explicitly. The bridge supports a **dry-run mode** (report what would be imported, write nothing).

4. **ADR-019 governance concepts must be preserved or mapped in the LS-MEM schema.** Retention TTLs, staleness detection, conflict supersession, constitutional veto, and curator pin/unpin semantics from `src/ai_company/memory/governance.py` must survive the transition — either as equivalent LS-MEM schema columns/lifecycle states or as an explicit documented mapping. **Tier mapping for the recon `verified_by` gap:** recon §3 notes Tier 3 (institutional/human-verified) needs a `verified_by` field that ADR-019 does not currently model — LS-MEM schema must add `verified_by` (and institutional flag) and map ADR-019's pin/curator-override semantics onto Tier 3 verification.

5. **Dual skill deploy paths must be content-identical.** `.agents/skills/ls-memory/` and `.opencode/skills/ls-memory/` are byte-identical copies of skill content, **hash-checked in tests** per threat-model open item 4. Discovery authority stays `.agents/skills/` per `docs/SKILL_CURATION_POLICY.md`.

6. **Long-term consolidation (choosing a single memory engine) is a future ADR, not this one.** Selecting one engine over the other — retiring `MemoryStore` or folding LS-MEM back into it — is **out of scope until LS-MEM is proven** in Phases 2–4+. That decision gets its own ADR with explicit trigger criteria (see Consequences).

7. **Never commit `.lightspeed/memory/`.** The memory DB and audit directory stay out of git (gitignored 2026-09-24; threat-model T21). LS-MEM code must never `git add` / `git commit` / `git push` memory paths (handoff Rule 5); enforced by `.gitignore` + a git-safety test.

## Alternatives Considered

### (A) Replace MemoryStore immediately with LS-MEM

**Pros:**
- Single engine from day one — no dual-source-of-truth risk (C1 fully closed)
- No bridge code to maintain
- Operators never need an authority table

**Cons:**
- Breaks every existing ADR-019 consumer (consolidation, CLI, executor recall) at once
- Risk of data loss migrating the live `memory/*.json` corpus before LS-MEM has proven parity
- LS-MEM ships before threat-model Phase 5 security gates (offline, secret, external-access, authorization, git tests) are green
- Violates the CEO-locked decision in the approved threat model

**Rejected reason:** Premature. ADR-019 governance is production-critical; replacing mid-project risks data loss and consumer breakage. Threat model locks option (a), not immediate replacement.

### (B) Extend MemoryStore with a SQLite backend (recon option b)

**Pros:**
- Keeps a single engine identity (`MemoryStore`) — no C1 dual-source issue
- Existing consumers keep the same import path and API surface
- Reuses ADR-019 governance code in place without a mapping layer

**Cons:**
- Conflicts with the system directive to build a SQLite schema for LS-MEM's 13-type / 4-classification model — retrofitting that onto the 6-type JSON store muddies both models
- Touches production ADR-019 code paths before LS-MEM security controls exist
- Harder to keep LS-MEM network-deny-by-default posture isolated when bundled into existing engine code
- Threat model explicitly locks "new SQLite engine + bridge," not "extend the old engine"

**Rejected reason:** Rejected by CEO-locked threat-model decision (line 8) and recon's preference for option (a) with a documented migration path.

### (C) Parallel independent systems with no bridge (status quo drift)

**Pros:**
- Zero near-term engineering cost — no bridge, no mapping
- Each system evolves independently with no coupling

**Cons:**
- Realizes the worst case of recon **conflict C1 (High)**: dual sources of truth with migration confusion and double maintenance
- Institutional knowledge fragments — no path to consolidate later
- Operators have no authority rule for which store answers which question
- Two governance models drift out of sync (ADR-019 vs LS-MEM lifecycle)

**Rejected reason:** Unmanaged drift is the exact High-severity conflict C1 exists to prevent. A one-way bridge is the minimum structure that keeps a migration story alive.

### Chosen: New engine + one-way bridge (recon option a)

**Pros:**
- Zero breakage of ADR-019 consumers during Phases 2–4+
- LS-MEM can ship behind full security gating (threat-model Phase 5 tests) without touching production memory code
- Clear, documented migration path (JSON → SQLite) with dry-run safety
- Matches CEO-locked threat-model decision

**Cons:**
- Temporary dual systems during coexistence window
- Bridge + schema-mapping code to maintain until consolidation
- Operators must consult an authority table to know which store is authoritative when

**Accepted because:** The cons are bounded and mitigated below; the alternatives either break production (A), violate the lock (B), or accept unmanaged High-severity drift (C).

## Consequences

### Positive

- **Zero breakage of ADR-019 consumers** — existing consolidation, CLI, and recall paths keep working unchanged through Phases 2–4+.
- **LS-MEM ships security-gated** — new engine can pass offline / secret / external-access / authorization / git tests before any consumer is migrated onto it.
- **Clear migration story** — one-way import bridge with dry-run mode and Phase 3 data-model documentation; no silent dual-write.
- **Governance continuity** — ADR-019 concepts (TTL, staleness, supersede, pin, constitutional veto) are preserved or explicitly mapped, with the recon `verified_by` gap closed via Tier mapping.

### Negative

- **Temporary dual systems** during coexistence — two stores, two type vocabularies (6 vs 13), two governance implementations.
- **Bridge code to maintain** — import path and schema/type mapping must be kept correct as LS-MEM schema evolves (schema versioning required).
- **Operator ambiguity** — without a clear authority rule, an agent or human may read stale state from the wrong store or write to both by mistake.

### Mitigations

- **ADR-025 authority table** (which store is authoritative for what): JSON `MemoryStore` = authoritative for existing ADR-019 consumers during Phases 2–4+; LS-MEM SQLite = authoritative for new `ls-memory` skill writes and anything imported through the bridge after import confirmation. Documented in the Phase 3 data model and the user guide.
- **Import bridge dry-run mode** — default to report-only; actual writes require an explicit flag, so no accidental mass import.
- **Future consolidation ADR trigger criteria** — open a follow-up ADR (not this one) when any of: (i) LS-MEM passes all Phase 5 security acceptance tests and runs in production for a full review cycle; (ii) all ADR-019 consumers have an approved migration plan; (iii) the authority table has been stable with no ambiguity incidents. Consolidation remains out of scope until then (Decision rule 6).

### Risk residual

- C1 (High) is **managed, not eliminated**, during coexistence — mitigations above reduce it to an operational (not architectural) concern; it fully closes only when the future consolidation ADR lands.

## References

- `docs/adr/019-memory-knowledge-governance.md` — existing MemoryStore governance (TTL, staleness, supersede, pin, constitutional veto)
- `docs/security/LS-MEM-THREAT-MODEL.md` — approved Phase 1 threat model; line 8 locked decisions (dual skill paths + new SQLite engine + bridge); open items 1 and 4
- `docs/architecture/LS-MEM-RECONNAISSANCE.md` — conflict C1 (High, coexistence) and C2 (skill path); option (a) vs (b); `verified_by` Tier gap (§3)
- `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md` — LS-MEM mission, 13 memory types, 4 classifications, Rule 5 (never commit memory DB), implementation sequence
- `docs/SKILL_CURATION_POLICY.md` — skill discovery authority = `.agents/skills/`; Third-Party Transmission Ban
- `src/ai_company/memory/governance.py` — ADR-019 policy layer implementation (mapping source for Decision rule 4)
- `docs/architecture/LS-MEM-DATA-MODEL.md` — Phase 3 deliverable (migration path + authority table home)
