---
title: "fix(athena): serialize Decimal salary ranges in JSONL store"
slug: "fix-athena-serialize-decimal-salary-ranges-in-jsonl-store"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules: ["athena"]
files: ["src/ai_company/athena/store.py", "tests/unit/test_athena_store.py"]
tags: ["fix", "athena", "bugfix", "serialization"]
validation_status: "pass"
created_at: "2026-09-22"
updated_at: "2026-09-22"
session_id: "035b10f4-82f5-4b0c-9093-84890fb6b542"
owner_agent: "jmlus"
claimed_at: "2026-09-22"
validation_results:
  - "ruff check src/ai_company/athena/store.py: PASS"
  - "mypy src/ai_company/athena/store.py: PASS"
  - "pytest tests/unit/test_athena_store.py: 2 passed"
  - "pytest tests/unit/test_athena_*.py (full athena suite): 6 passed"
---

# Summary

## Outcome

Fixed store serialization crash on pydantic `Decimal` fields. `POST /api/v1/athena/jobs` failed with `TypeError: Object of type Decimal is not JSON serializable` at `store.py:68` whenever a job carried a `salary_range` (`SalaryRange.min/max` are `Decimal`). Added a `Decimal` branch to `AthenaStore._serialize` (lossless `str()` round-trip; pydantic re-coerces on load), covering all four stores (jobs/applications/profiles/scrape_jobs). Added regression test `test_job_store_roundtrip_decimal_salary`. Full Athena quick-start then re-ran end-to-end with all endpoints returning 200.

## Decisions

- Serialize `Decimal` as `str(data)` in `_serialize` instead of `float(data)`: lossless round-trip, pydantic coerces `str` -> `Decimal` on load, and no precision loss on currency values.
- Bug fix exposed only via the Athena quick-start walkthrough (profile -> job -> match -> ATS score -> stats), not by the unit suite - hence the regression test.

## Validation

- `ruff check src/ai_company/athena/store.py`: PASS
- `mypy src/ai_company/athena/store.py`: PASS
- `pytest tests/unit/test_athena_store.py`: 2 passed (CRUD + new Decimal round-trip)
- Full athena suite: 6 passed
- Quick-start re-run: all quick-start endpoints 200 (jobs, profiles, seed job with salary 2500-5000, match 92.6 excellent, ATS score 63.3, stats/scheduler endpoints)

## Next Step

- Commit the fix + regression test + this ECL change via PR -> main (owner-approved).
