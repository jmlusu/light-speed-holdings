# Plan

## Technical Approach

- Add two `add_default_config(ScrapeConfig(...))` blocks to `init_scheduler` in `src/ai_company/athena/scheduler/jobs.py`, immediately after the existing "data scientist / Lilongwe, Malawi" config:
  - `query="software engineer"`, `location="Remote"`, `max_results=50`, `sources=[JobSource.REMOTE_OK, JobSource.WE_WORK_REMOTELY, JobSource.REMOTE_CO]`
  - `query="data scientist"`, `location="Remote"`, `max_results=50`, `sources=[JobSource.REMOTE_OK, JobSource.WE_WORK_REMOTELY, JobSource.REMOTE_CO]`
- Leave the existing four configs untouched.
- Overlap with configs 1-2 (which fan out across all 13 scrapers) does not duplicate DB rows: `run_scrape_config` dedups by `source_job_id`.

## Impacted Modules And Files

- `src/ai_company/athena/scheduler/jobs.py` — only code file changed (`init_scheduler`).
- `harness/changes/active/{summary,spec,plan,tasks,reviews/review}.md` — ECL change documentation.

## Interfaces, Data, Permissions

- No public API change: `ScrapeConfig` fields (`query`, `location`, `max_results`, `sources`) already exist; the scheduler daemon consumes `default_configs` unchanged.
- No schema/model/DB migration.

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

- Risk: curated remote configs could surface duplicates of roles already scraped by the all-sources Malawi configs. Mitigation: `run_scrape_config` updates by `source_job_id` rather than inserting duplicates.
- Risk: committing unrelated working-tree changes (approvals.yaml, executor loop, registry). Mitigation: stage only `scheduler/jobs.py` + ECL files explicitly.

## Verification Plan

- `uv run ruff check src/ai_company/athena/scheduler/jobs.py`
- `uv run mypy src/ai_company/athena/scheduler/jobs.py`
- `uv run pytest tests/unit/test_athena_api.py tests/unit/test_athena_matching.py tests/unit/test_athena_scorer.py tests/unit/test_athena_store.py tests/integration/test_scheduler_verification.py tests/test_scheduler_integration.py`
- `pwsh scripts/lint-ecl.ps1` for ECL harness files.
- Push branch and open PR to `main`; verify the 10 CI checks.
