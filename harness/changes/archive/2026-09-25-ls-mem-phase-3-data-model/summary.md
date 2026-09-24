---
title: "LS-MEM Phase 3 Data Model"
slug: "ls-mem-phase-3-data-model"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "accepted"
spec_review: "approved"
plan_review: "approved"
modules: []
files:
  - docs/architecture/LS-MEM-DATA-MODEL.md
tags: ["lsmem", "memory", "data-model", "schema", "sqlite", "fts5"]
validation_status: "pass"
created_at: "2026-09-25"
updated_at: "2026-09-25"
session_id: "0ef66804-66ce-4568-ac4f-2841f9d012f7"
owner_agent: "jmlus"
claimed_at: "2026-09-25"
---

# LS-MEM Phase 3 — Data Model

> Retrospective ECL record. The work was executed on 2026-09-24 without an
> active change; this archive was created 2026-09-25 to close the process gap
> flagged in the reviewer consensus.

## Goal

Produce the Phase 3 memory data model per handoff §8
(`docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md`): a versioned schema document
at `docs/architecture/LS-MEM-DATA-MODEL.md` covering the 13 mandated memory
types and the minimum record fields, without hard-coding the example schema
where a better design is justified.

## Context / Current State

- Phase 0 recon, Phase 1 threat model (Approved), and Phase 2 architecture
  complete; Phase 2 archive: `2026-09-24-ls-mem-phase-2-architecture`.
- Governance inputs: ADR-019 (memory TTLs/staleness/supersede/pin), ADR-025
  (SQLite engine coexistence with JSON MemoryStore — Accepted).
- CEO-locked decisions from Phase 2 carry forward (dual skill paths, network
  deny-by-default, Restricted never plaintext, `[REDACTED_SECRET]` canonical,
  Ollama optional, storage `.lightspeed/memory/` gitignored).

## Outcome

- **`docs/architecture/LS-MEM-DATA-MODEL.md`** written (381 lines, dated
  2026-09-24):
  - Schema versioning policy: `schema_version: 1` in
    `.lightspeed/memory/config.yaml`; all DDL changes must increment the
    version and add a forward-only migration in `migrations/`.
  - Core `memories` table covering all 13 handoff §8 types
    (`observation`, `decision`, `architecture`, `requirement`, `preference`,
    `task`, `milestone`, `bug`, `solution`, `lesson`, `entity`, `document`,
    `session`) with identity, provenance, classification, confidence, tags,
    verification, and external-use-approval fields.
  - Secret/redaction columns and classification handling aligned with the
    Phase 1 threat model; FTS5 virtual-table mapping for search.
  - Cross-references to ADR-019, ADR-025, threat model, and Phase 2
    architecture.

## Decisions

1. Versioned schema with forward-only migrations (no silent DDL drift).
2. All 13 memory types modeled in one core table with a `type` constraint
   rather than per-type tables.
3. Record field set preserves every concept from handoff §8's example JSON
   (provenance, `verified_by`, `approved_for_external_use`, etc.) while
   adding storage columns justified by the threat model (classification,
   redaction state, soft-delete columns).
4. Schema document is the contract implemented by the Phase "Implementation"
   change (`src/ai_company/lsmem/engine.py` schema DDL).

## Validation

- Prerequisites referenced and approved: Phase 1 threat model, Phase 2
  architecture, ADR-019, ADR-025.
- Handoff §8 checklist: versioned schema (yes), 13 minimum types (yes,
  verified 13/13), minimum record fields (yes).
- `pwsh scripts/lint-ecl.ps1`: pass.

## Validation Results

| Gate | Result |
|------|--------|
| Data model doc exists (381 lines) | pass |
| 13/13 handoff §8 memory types present | pass |
| Schema versioning + migration policy | pass |
| Minimum record fields preserved | pass |
| ADR-019 / ADR-025 / threat-model cross-refs | pass |
| lint-ecl.ps1 (docs/harness) | pass |

## Handoff Notes / Audit Trail

- Retrospective record created 2026-09-25 (work done 2026-09-24); the
  process bypass was flagged by the Chief-of-Staff reviewer.
- `docs/architecture/LS-MEM-DATA-MODEL.md` is currently **untracked in git**
  (deliverable exists on disk; commit awaits explicit user instruction).
- Do not hand-edit `harness/changes/INDEX.json` — reindex only.
