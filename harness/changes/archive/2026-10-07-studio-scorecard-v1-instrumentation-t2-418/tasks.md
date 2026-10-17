# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. (Done 2026-10-07 — spec/plan written, user-approved cuts recorded.)

## Implementation

- [x] T002 [P] Additive `Task` studio fields in `src/ai_company/models/models.py` with safe defaults. Validation: existing task tests pass unmodified.
- [x] T003 [P] New `company/studio_tracker.yaml` (ventures A/B/C + `studio-core`, gate timestamps, CFO section). Validation: collector reads it; missing timestamps → `no_data`.
- [x] T004 `StudioScorecardCollector` in `src/ai_company/dashboard/kpis/studio.py` + register in `ALL_COLLECTORS`. Validation: unit tests for ATC/correction/velocity/capital math incl. empty-store `no_data`.
- [x] T005 MessageBus + executor + ApprovalGate emission wiring (additive only). Validation: seeded task round-trips `venture_id`/`model_id`/`cost_usd`; no existing tests break.
- [x] T006 `GET /api/v1/studio-scorecard` + dashboard page/section. Validation: endpoint returns live-or-`no_data`; page renders with zero hard-coded metrics.

## Validation

- [x] T007 Full gates: `ruff check src/`, `mypy src/`, full non-e2e `pytest`, `validate-drift.ps1`, `lint-ecl.ps1`. Validation: all green, results recorded in `summary.md`.
- [ ] T008 ECL close (`close completed`) + resolution comment on #418 with links. Validation: archive exists, issue closed, map #416 decision entry proposed.

## Deferred Tasks

- None.
