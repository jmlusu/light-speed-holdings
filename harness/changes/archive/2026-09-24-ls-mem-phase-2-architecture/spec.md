# Spec — LS-MEM Phase 2 Architecture

## What

Author the Phase 2 architecture design for LightSpeed Memory (LS-MEM):

1. **Primary:** `docs/architecture/LS-MEM-ARCHITECTURE.md` covering all 18 handoff §7 subsystems:
   memory engine, storage, FTS5 search, optional vector search, Ollama integration,
   privacy layer, classification layer, secret scanner, permission gateway, audit
   subsystem, OpenCode integration, session initialization, memory injection,
   deletion (forget/purge), export, backup/recovery, failure behavior, offline behavior.
2. **Supporting ADR:** `docs/adr/025-lsmem-sqlite-engine-coexistence.md` — new SQLite+FTS5
   engine coexists with JSON `MemoryStore` via one-way import bridge (no replacement Phases 2–4).
3. **Phase 1 (predecessor, approved):** `docs/security/LS-MEM-THREAT-MODEL.md` — handoff §6
   threats with likelihood/impact/mitigation/test/residual; cross-cutting control map;
   gitignore gap called out; CEO/security sign-off.
4. **Hygiene:** `.gitignore` entries for `.lightspeed/memory/` + sidecars.

## Constraints (CEO-locked)

- Dual skill paths content-identical; discovery authority `.agents/skills/`.
- Network deny-by-default; offline-first (work fully offline).
- Restricted never plaintext; uncertain → BLOCK.
- Redaction `[REDACTED_SECRET]` canonical.
- Ollama optional after deterministic FTS; never cloud fallback.
- Storage `.lightspeed/memory/` gitignored; no auto-commit of memory DB.
- Docs-only for this ECL (no `src/` runtime change in Phase 2).

## Non-goals (Phase 2)

- Data model (Phase 3: `LS-MEM-DATA-MODEL.md`).
- Implementation steps 5–20 (handoff §34) — after Phase 3.
- Replacing JSON `MemoryStore`.
- External-provider / cloud embedding integration.

## Acceptance criteria

- [x] Architecture doc exists; all 18 §7 bullets map to a section (traceability matrix present).
- [x] ADR-025 Accepted; cross-referenced from architecture §1/§C1.
- [x] Threat model Phase 1 exit criteria met; CEO/security sign-off recorded.
- [x] `.gitignore` protects `.lightspeed/memory/`.
- [x] `pwsh scripts/lint-ecl.ps1` pass for docs/harness change.
- [x] Offline requirement documented (§18) and enforced by design constraints.
