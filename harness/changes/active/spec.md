# Spec

## Intake Review

- Intake type: Small Change
- Input shape: observed-bug-first (found during Athena quick-start walkthrough)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Seeding a job with a `salary_range` crashes the store write (`TypeError: Object of type Decimal is not JSON serializable`), so any real job with salary data would fail on the dashboard too.
- Current behavior: `AthenaStore._serialize` handles UUID, datetime, HttpUrl, Enum, but not pydantic `Decimal`; `json.dumps` in `_save_all` raises.
- Source of evidence: `POST /api/v1/athena/jobs` during the quick-start returning the crash; `store.py` traceback.

## User Scenarios And Success

- Primary user/system scenario: An agent or the dashboard persists a job that includes a salary range (e.g. Senior AI Engineer, 2500-5000 USD monthly).
- Success criteria: Job persists to `company/athena/jobs.jsonl` and round-trips with identical salary values.
- Acceptance criteria:
  - `AthenaStore` persists and reloads a `Job` with a `salary_range` unchanged.
  - Regression test covers the round-trip.

## Non-Goals

- Not changing the storage format or schema.
- Not touching frontend, routes, or other modules.
- Not reworking `_serialize` into a full custom JSON encoder.

## Constraints

- Single-file source change preference (small fix).
- No format breakage for existing JSONL records.

## Assumptions

- Returning Decimal as its string form and relying on pydantic coercion is acceptable (verified by the round-trip test).

## Open Questions

- None.

## Resolved Clarifications

- Owner approved committing the fix + regression test as a new (retrospectively documented) ECL change rather than a bare no-change commit.
