# Plan

## Technical Approach

- Single Markdown data-model document with YAML schema-version block, SQL DDL
  for the core `memories` table, FTS5 virtual-table mapping, and a migration
  policy (forward-only, version-gated).

## Impacted Modules And Files

- `docs/architecture/LS-MEM-DATA-MODEL.md` (new, 381 lines).
- No src/ changes in this change.

## Interfaces, Data, Permissions

- Data contract: schema consumed by `src/ai_company/lsmem/engine.py` in the
  Implementation change.
- Storage location `.lightspeed/memory/` (gitignored).

## Spec Gaps Found From Planning

- None; handoff §8 is explicit about types and fields.

## Risks And Mitifications

- Risk: doc/code drift between this document and engine DDL. Mitigation:
  Implementation change validates DDL against this doc (test coverage in
  `tests/memory/`).

## Verification Plan

- Handoff §8 checklist walkthrough (types, fields, versioning).
- `pwsh scripts/lint-ecl.ps1`.
