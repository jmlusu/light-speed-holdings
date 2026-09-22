# Plan

## Technical Approach

`AthenaStore._serialize` in `src/ai_company/athena/store.py` is the single conversion point for every record saved to the JSONL stores. It already special-cases the non-JSON-serializable types in the models (UUID, datetime, HttpUrl, Enum). Add one branch:

```python
if isinstance(data, Decimal):
    return str(data)
```

plus `from decimal import Decimal`. This is lossless: the JSONL record stores `"2500"`/`"5000"` as strings, and the pydantic `SalaryRange` model re-coerces `str` -> `Decimal` on load. Because `_serialize` is shared by `AthenaDB` and every store (jobs, applications, user_profiles, scrape_jobs), the fix covers all four at once.

## Impacted Modules And Files

- `src/ai_company/athena/store.py` - Decimal import + `_serialize` branch (the fix).
- `tests/unit/test_athena_store.py` - new `test_job_store_roundtrip_decimal_salary` (regression).

## Interfaces, Data, Permissions

- No API/route/schema changes. JSONL on-disk values for Decimal fields change from impossible (crash) to string form; load path unchanged (pydantic already accepts both).
- No permission changes.

## Spec Gaps Found From Planning

- None for this change. Lower-priority backlog: pydantic `class Config` deprecation warnings in `athena/api/schemas.py` (Pydantic v2 `ConfigDict` migration) and `datetime.utcnow()` deprecation in `store.py` - out of scope.

## Risks And Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Existing JSONL records already holding Decimal values as numbers break | Low | Low | `_serialize` only runs on writes; load uses pydantic coercion which accepts both `int`/`str` |
| `str(Decimal)` loses trailing precision semantics | Low | Low | Round-trip test asserts exact equality of min/max |

## Verification Plan

- `ruff check src/ai_company/athena/store.py`
- `mypy src/ai_company/athena/store.py`
- `pytest tests/unit/test_athena_store.py -q` (CRUD + new Decimal round-trip)
- Full athena suite: `pytest tests/unit/test_athena_*.py -q`
- Quick-start re-run: seed a job with `salary_range` through `POST /api/v1/athena/jobs` and confirm 200 + persisted job.
