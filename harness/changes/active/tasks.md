# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Create feature branch `feat/athena-malawi-track-remote` from `origin/main` (athena sources present at `371244b1`).

## Implementation

- [x] T002 Add two curated remote `ScrapeConfig`s to `init_scheduler` in `src/ai_company/athena/scheduler/jobs.py` (after the "data scientist / Lilongwe" config): `software engineer` and `data scientist`, both `location="Remote"`, `max_results=50`, `sources=[REMOTE_OK, WE_WORK_REMOTELY, REMOTE_CO]`. Validation: ruff + mypy clean on the file.

## Validation

- [x] T003 Run athena test suite: `uv run pytest tests/unit/test_athena_api.py tests/unit/test_athena_matching.py tests/unit/test_athena_scorer.py tests/unit/test_athena_store.py tests/integration/test_scheduler_verification.py tests/test_scheduler_integration.py` — all pass.
- [x] T004 Run `pwsh scripts/lint-ecl.ps1` on ECL files — pass.
- [x] T005 Push branch, open PR to `main` (#356), monitor CI — all 16 checks green; transient ubuntu perf-test flake re-ran and passed.

## Deferred Tasks

- None.
