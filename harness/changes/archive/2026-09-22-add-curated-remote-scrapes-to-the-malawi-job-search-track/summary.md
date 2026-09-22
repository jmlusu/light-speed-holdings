---
title: "Add curated remote scrapes to the Malawi job-search track"
slug: "add-curated-remote-scrapes-to-the-malawi-job-search-track"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules: ["athena"]
files: ["src/ai_company/athena/scheduler/jobs.py"]
tags: ["athena", "scheduler", "malawi", "remote"]
validation_status: "pass"
validation_results:
  - "ruff check src/: PASS"
  - "mypy src/: PASS"
  - "pytest (athena suite): 22 passed"
  - "scripts/lint-ecl.ps1: PASS"
  - "PR #356 CI: 16/16 checks PASS (ruff, mypy, pytest ubuntu+windows, ECL Harness Lint, bandit, uv-audit, generated-files drift, archify, graph build, version sync, site build, CI Gate; E2E non-blocking green)"
created_at: "2026-09-22"
updated_at: "2026-09-22"
session_id: "667df7c7-4f77-4f1a-891f-ab306cd83650"
owner_agent: "jmlus"
claimed_at: "2026-09-22"
---

# Summary

## Outcome

The Malawi job-search track now deliberately captures international remote roles. `init_scheduler` in `src/ai_company/athena/scheduler/jobs.py` registers two curated `ScrapeConfig` entries that mirror each Malawi query ("software engineer", "data scientist") against the three dedicated remote-only boards (`REMOTE_OK`, `WE_WORK_REMOTELY`, `REMOTE_CO`) with `location="Remote"`. Scheduler-only change; no models, API, or frontend touched.

## Decisions

- Scope confirmed with the user: curated Malawi+Remote scheduled scrapes (small scheduler change), not a structured remote flag/filter.
- New remote configs are restricted to the dedicated remote-only sources to keep remote results curated; consultancy and general boards (LinkedIn/Indeed/Glassdoor) are excluded because configs 1-2 already fan out across all sources.
- Existing configs (Lilongwe local x2, "remote software engineer" all-sources, "freelance developer" consultancy) left unchanged — no behavior regression.
- Duplication is not a concern: `run_scrape_config` dedups by `source_job_id`, so a re-found remote job updates rather than inserts.

## Validation

- `uv run ruff check src/ai_company/athena/scheduler/jobs.py` — passed.
- `uv run mypy src/ai_company/athena/scheduler/jobs.py` — passed.
- `uv run pytest tests/unit/test_athena_api.py tests/unit/test_athena_matching.py tests/unit/test_athena_scorer.py tests/unit/test_athena_store.py tests/integration/test_scheduler_verification.py tests/test_scheduler_integration.py` — 22 passed.
- `pwsh scripts/lint-ecl.ps1` — passed.
- PR #356 branched to `main`: all 16 CI checks green (runs `35708892251`/`35708892213`). One transient failure — `Test (ubuntu-latest)` `test_dashboard_response_time_consistency` (20 dashboard calls, one 353ms cold spike blew the `<50ms` SD gate; test is independent of scheduler code) — re-ran the job and it passed (5m35s). Windows tests, full ubuntu suite (2454 passed), ECL Harness Lint, E2E, and Vercel all green.

## Next Step

- Await user decision to merge PR #356 into `main`; then update `docs/STATUS.md` and close this change via `scripts/harness-change.ps1 close completed`.
