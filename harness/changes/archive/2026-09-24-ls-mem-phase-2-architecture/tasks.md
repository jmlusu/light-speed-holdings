# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`

## Setup / Intake

- [x] T001 Intake: confirm Phase 2 scope (architecture doc + ADR-025 + gitignore) from handoff §7/§31/§34. (Done 2026-09-24)
- [x] T002 [P] Lock CEO-locked decisions (dual path, discovery authority, ADR-025 coexistence, network deny, Restricted, redaction token, Ollama, storage path) in summary. (Done 2026-09-24)

## Phase 1 (threat model — predecessor)

- [x] T003 Author `docs/security/LS-MEM-THREAT-MODEL.md` (handoff §6 threats + control map + gitignore gap). Validation: exit criteria checkboxes. (Done 2026-09-24)
- [x] T004 CEO/security review sign-off on threat model. (Done 2026-09-24 — approved; Status → Approved)

## Implementation

- [x] T005 [P] Author `docs/adr/025-lsmem-sqlite-engine-coexistence.md`. Validation: Status Accepted; notes separate series vs `docs/architecture/adr/025-*`. (Done 2026-09-24)
- [x] T006 Author `docs/architecture/LS-MEM-ARCHITECTURE.md` covering all 18 §7 subsystems + FM1–FM8 + offline §18 + traceability matrix. Validation: 18/18 section mapping. (Done 2026-09-24 — 633 lines)
- [x] T007 [P] Add `.lightspeed/memory/` + sidecars to `.gitignore`. Validation: grep gitignore. (Done 2026-09-24)
- [x] T008 [P] Cross-link ADR-025 ↔ architecture §1/§C1; fix path collision note. (Done 2026-09-24 — line 13 + §Engine coexistence)

## Validation

- [x] T009 `pwsh scripts/lint-ecl.ps1` green (docs/harness change). (Done 2026-09-24 — pass while active; re-verified after archive reconstruct)
- [x] T010 Verify 18/18 traceability + ADR Accepted + threat model Approved + gitignore present. (Done 2026-09-24)
- [x] T011 Fix threat-model Status line drift if still "Draft for review". (Done 2026-09-24 — Status + exit checkbox → Approved)

## Review / Close

- [x] T012 Spec + plan review approved (CEO-locked constraints reflected in spec/plan). (Done 2026-09-24)
- [x] T013 Update `docs/STATUS.md` (Phase 2 complete; archive path; not "not yet archived"). (Done 2026-09-24)
- [x] T014 Reconstruct ECL archive after concurrent-session race; recover `ref/memory-engine-brief.md`; reindex INDEX.json. (Done 2026-09-24)
- [x] T015 Final `pwsh scripts/lint-ecl.ps1` after reindex. (Done 2026-09-24)

## Deferred Tasks

- None (Phase 3+ is a separate ECL change).
