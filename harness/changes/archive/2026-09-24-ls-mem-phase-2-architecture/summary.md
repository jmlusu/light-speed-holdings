---
title: "LS-MEM Phase 2 — Architecture"
slug: "ls-mem-phase-2-architecture"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "accepted"
spec_review: "approved"
plan_review: "approved"
modules: []
files:
  - docs/architecture/LS-MEM-ARCHITECTURE.md
  - docs/adr/025-lsmem-sqlite-engine-coexistence.md
  - docs/security/LS-MEM-THREAT-MODEL.md
  - .gitignore
tags: ["lsmem", "memory", "architecture", "security", "sqlite", "fts5"]
validation_status: "pass"
created_at: "2026-09-24"
updated_at: "2026-09-24"
---

# LS-MEM Phase 2 — Architecture

## Goal

Produce the Phase 2 architecture design for LightSpeed Memory (LS-MEM):
`docs/architecture/LS-MEM-ARCHITECTURE.md` covering all 18 mandated subsystems
(handoff §7), plus supporting ADR-025 (SQLite engine coexistence), Phase 1 threat
model approval, and `.gitignore` protection for `.lightspeed/memory/`.

## Context / Current State

- Handoff master plan: `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md` (§7 18 subsystems, §31, §34).
- Existing JSON `MemoryStore` in `src/ai_company/memory/` retained (ADR-025; no replacement Phases 2–4).
- Phase 0 recon + Phase 1 threat model complete before this change.
- CEO-locked decisions: dual skill paths (`.agents/skills/ls-memory/` + `.opencode/skills/ls-memory/`, content-identical); discovery authority `.agents/skills/`; network deny-by-default; Restricted never plaintext; uncertain → BLOCK; redaction `[REDACTED_SECRET]` canonical; Ollama optional after deterministic FTS, never cloud fallback; storage `.lightspeed/memory/` (gitignored).

## Outcome

- **Phase 1 threat model** written and approved: `docs/security/LS-MEM-THREAT-MODEL.md` (CEO/security sign-off 2026-09-24).
- **Phase 2 architecture** complete: `docs/architecture/LS-MEM-ARCHITECTURE.md` (633 lines, 18/18 §7 subsystems, traceability matrix, FM1–FM8, offline summary, ADR-025 cross-refs).
- **ADR-025** accepted: `docs/adr/025-lsmem-sqlite-engine-coexistence.md` (deciders incl. CEO; Status Accepted).
- **.gitignore**: `.lightspeed/memory/` + sidecars added.
- **Next:** Phase 3 — `docs/architecture/LS-MEM-DATA-MODEL.md` (versioned schema for 13 memory types).

## Decisions

1. Dual skill paths `.agents/skills/ls-memory/` AND `.opencode/skills/ls-memory/`, content-identical (hash-checked).
2. Discovery authority is `.agents/skills/` per `docs/SKILL_CURATION_POLICY.md`.
3. New SQLite+FTS5 engine + one-way import bridge FROM JSON `MemoryStore` (ADR-025). JSON store not replaced Phases 2–4.
4. Network deny-by-default; no HTTP/HTTPS/DNS egress without explicit approval gateway.
5. Restricted classification never written in plaintext; uncertain → BLOCK.
6. Redaction token `[REDACTED_SECRET]` canonical (legacy `[REDACTED]` accepted as alias).
7. Ollama is optional after deterministic FTS5 works; never cloud embedding fallback.
8. Storage root `.lightspeed/memory/` — gitignored (sidecars too).

## Validation

- lint-ecl: pass (when LS-MEM was active; restored after archive reconstruction).
- Architecture traceability: all 18 handoff §7 bullets mapped (§ matrix).
- ADR-025 path collision with `docs/architecture/adr/025-agent-consolidation-152-to-90.md` documented (different series, no conflict).
- Threat model exit criteria: threats + control map + gitignore gap + CEO/security sign-off.

## Validation Results

| Gate | Result |
|------|--------|
| Architecture 18/18 subsystems | pass |
| ADR-025 Accepted + cross-ref | pass |
| Threat model Phase 1 approved | pass |
| .gitignore .lightspeed/memory/ | pass |
| lint-ecl.ps1 (docs/harness) | pass |
| No src/ code change required | n/a |

## Handoff Notes / Audit Trail

- Active ECL files were destroyed by a concurrent-session race (active swapped, close archived to wrong slug).
- This archive was reconstructed 2026-09-24 from conversation content + surviving deliverables on disk.
- `ref/memory-engine-brief.md` recovered from erroneous duplicate archive `...-architecture-v2-0-2` before that folder was removed.
- Do not hand-edit `harness/changes/INDEX.json` — reindex only.
