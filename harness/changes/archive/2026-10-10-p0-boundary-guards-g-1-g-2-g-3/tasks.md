# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

- [x] T002 [G-3] Add `configResolved` port-guard plugin to `vite.config.ts` plugins array; throws naming CEO Dashboard if resolved port ∈ {8420, 8421}.
- [x] T003 [G-2] Add Marketing-Port refuse to `src/ai_company/cli/dashboard.py` callback (adjacent to ADR-012 guard); `typer.Exit(1)`.
- [x] T004 [G-1] Create `tests/unit/test_port_assignments.py` asserting vite ports, PM2 ports, dashboard CLI default, compose mappings, and disjointness.

## Validation

- [x] T005 Run `uv run pytest tests/unit/test_port_assignments.py` — all pass.
- [x] T006 Run `uv run ruff check src/ && uv run mypy src/ && uv run pytest` — all green (port tests 7/7; 5 pre-existing ECL archive-quality failures unrelated).
- [x] T007 Run `pwsh scripts/maintenance/lint-ecl.ps1` — PASS (4 historical slug WARNs).

## Deferred Tasks

- None.
