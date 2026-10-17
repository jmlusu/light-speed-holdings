# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Confirm handoff §8 requirements and Phase 1/2/ADR prerequisites in `docs/LS-MEM-OPENCODE-IMPLEMENTATION-HANDOFF.md`.

## Implementation

- [x] T002 Write versioned schema document at `docs/architecture/LS-MEM-DATA-MODEL.md` with 13 types, record fields, FTS5 mapping, migration policy.

## Validation

- [x] T003 Verify 13/13 types and minimum record fields against handoff §8; run `pwsh scripts/lint-ecl.ps1`.

## Deferred Tasks

- None.
