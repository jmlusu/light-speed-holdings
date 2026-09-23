# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

- [x] T002 Author canonical narrative at `docs/NARRATIVE-AND-POSITIONING.md`.
- [x] T003 Build claims index/ledger/audit under `research/site-claims-*.{md,yaml}`.
- [x] T004 Expand `docs/content-architecture/entities/` registry and related analyses (`analysis_taxonomy.md`, `knowledge-model-analysis.md`, `seo-specialist-analysis.md`).
- [x] T005 Reconcile site claims (tally 67, claim:034 re-badge, claim:024 fix, wire `evidence_references` into 16 entities).
- [x] T006 Resolve stash-pop conflicts in `docs/AGENT-REGISTRY-TABLE.md`, `hr/onboarding_requests.yaml`, `orchestrator/approvals.yaml` (keep Updated upstream / 152 agents).

## Validation

- [x] T007 Run `scripts/validate-drift.ps1` — passed (87 files).
- [x] T008 Run `tests/docs/test_doc_drift.py` — passed.
- [x] T009 Run `pwsh scripts/lint-ecl.ps1` — passed.
- [x] T010 Re-run YAML parse on conflict-resolved files — OK.
- [x] T011 Run `bun run build` — green.

## Deferred Tasks

- None.
