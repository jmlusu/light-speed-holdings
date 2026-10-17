# Plan — LS-MEM Phase 2 Architecture

## Technical approach

Docs-only design pass driven by handoff (§7, §31, §34), Phase 1 threat model, and
CEO-locked decisions. No runtime code.

1. **Phase 1 (predecessor):** Author threat model; route for CEO/security review; record approval.
2. **ADR:** Write ADR-025 (engine coexistence decision, one decision per ADR).
3. **Architecture:** Author `LS-MEM-ARCHITECTURE.md` with one section per §7 subsystem,
   failure-mode table FM1–FM8, offline summary, constraints, and traceability matrix.
4. **Hygiene:** `.gitignore` for memory storage + sidecars.
5. **Validation:** Confirm 18/18 mapping, ADR cross-refs, lint-ecl green; update STATUS.md.

## Impacted files

- Create: `docs/architecture/LS-MEM-ARCHITECTURE.md`
- Create: `docs/adr/025-lsmem-sqlite-engine-coexistence.md`
- Create/update: `docs/security/LS-MEM-THREAT-MODEL.md` (Phase 1)
- Update: `.gitignore` (`.lightspeed/memory/` + sidecars)
- Update: `docs/STATUS.md`
- Read-only: `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md`, `docs/SKILL_CURATION_POLICY.md`,
  `docs/adr/019-memory-knowledge-governance.md`, `src/ai_company/memory/*`, `AGENTS.md`

## Interfaces / data / permissions

- No runtime interfaces changed.
- No secrets committed; memory DB path never committed.
- Docs + gitignore only.

## Risks and mitigations

- Risk: missing a §7 subsystem → Mitigation: traceability matrix gate (18 rows required).
- Risk: ADR number collision with `docs/architecture/adr/025-...` → Mitigation: document separate series in both ADRs.
- Risk: threat-model status drift (Draft vs Approved) → Mitigation: single Status field + exit-criteria checkbox aligned at close.
- Risk: concurrent ECL active-slot race → Mitigation: reconstruct as archive + reindex; do not swap active while another session owns it.

## Verification plan

- File presence: architecture + ADR + threat model + gitignore entries.
- Traceability: grep §7 bullets ↔ architecture sections.
- `pwsh scripts/lint-ecl.ps1`
- No `src/` change → ruff/mypy/pytest not required for this ECL.
