# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. (Completed: small-fix intake captured in spec.md, approach in plan.md)

## Implementation

- [x] T002 Add `from decimal import Decimal` + Decimal branch in `AthenaStore._serialize` in `src/ai_company/athena/store.py`. Verified: quick-start seed job with salary 2500-5000 returns 200 and persists.
- [x] T003 Add regression test `test_job_store_roundtrip_decimal_salary` in `tests/unit/test_athena_store.py`. Verified: `pytest tests/unit/test_athena_store.py` - 2 passed.

## Validation

- [x] T004 Lint: `ruff check src/ai_company/athena/store.py` - PASS.
- [x] T005 Type check: `mypy src/ai_company/athena/store.py` - PASS.
- [x] T006 Full athena suite: `pytest tests/unit/test_athena_*.py -q` - 6 passed.
- [x] T007 End-to-end smoke (quick-start): profile, job with salary_range, match, ATS score, stats, scheduler status all 200.

## Commit

- [ ] T010 Commit `src/ai_company/athena/store.py`, `tests/unit/test_athena_store.py`, `harness/changes/active/` on branch `fix/athena-store-decimal-serialization`; push; open PR -> main.
- [ ] T011 Close and archive ECL change via harness script after merge. Run `scripts/lint-ecl.ps1` before commit.

## Deferred Tasks

- Pydantic v2 `ConfigDict` migration for `athena/api/schemas.py` deprecation warnings.
- `datetime.utcnow()` deprecation in `athena/store.py`.
