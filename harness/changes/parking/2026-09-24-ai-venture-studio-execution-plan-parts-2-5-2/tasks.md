# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`

## Setup / Intake

- [x] T001 Capture CEO decisions and open docs-only ECL for Parts 2–5 — done 2026-09-24.
- [x] T002 Survey source docs (Pharos, competitive-landscape, ADR-030/033, KPI guide, pricing) — done 2026-09-24.

## Implementation

- [x] T003 Write `docs/venture-studio/02-sector-positioning.md` (Part 2) — done; category, matrix, competitive shape, positioning, Reservations.
- [x] T004 Write `docs/venture-studio/03-operating-model.md` (Part 3) — done; engine, portfolio A–C, stage gates.
- [x] T005 Write `docs/venture-studio/04-technical-architecture.md` (Part 4) — done; mesh, directives, in-repo map.
- [x] T006 Write `docs/venture-studio/05-kpi-scorecard.md` (Part 5) — done; four metrics + instrumentation plan.
- [x] T007 Write `docs/venture-studio/README.md` index — done; links Parts 2–5 + sources.

## Validation

- [x] T008 Confirm no brand token / ADR-020 / registry edits in this ECL — pass (docs-only tree under docs/venture-studio/).
- [x] T009 `pwsh scripts/lint-ecl.ps1` + harness validate — run at close.
- [x] T010 Update `docs/STATUS.md` with Parts 2–5 shipped entry — done at close.

## Deferred Tasks

- Part 5 collectors / Studio Scorecard dashboard UI — separate implementation ECL.
- P2 public registry transform — parked under architecture v2 follow-up.
