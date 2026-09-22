# Spec

## Intake Review

- Intake type: Small Change
- Input shape: requirement-first
- Questions asked this round: 1 (scope of "add remote to the Malawi track")

## Goal And Evidence

- Real problem or user request: Add remote to the Malawi job-search track so the scheduled Malawi track deliberately captures international remote roles for its usual queries.
- Current behavior: `init_scheduler` registers 4 default `ScrapeConfig`s in `src/ai_company/athena/scheduler/jobs.py:330-358`. The two Malawi configs ("software engineer", "data scientist", location "Lilongwe, Malawi") use `sources=None`, which fans out across all 13 scrapers — including remote boards — so remote roles already surface, but incidentally and not curated to remote-only boards.
- Source of evidence: User request; `git show origin/main:src/ai_company/athena/scheduler/jobs.py`; `src/ai_company/athena/scrapers/*.py` source topology (remote.py hosts LINKEDIN/INDEED/GLASSDOOR/REMOTE_OK/WE_WORK_REMOTELY/REMOTE_CO; the three remote-only boards are REMOTE_OK/WE_WORK_REMOTELY/REMOTE_CO).

## User Scenarios And Success

- Primary user/system scenario: On each 4-hour scrape cycle, the Malawi track now finds curated remote software-engineer and data-scientist roles from RemoteOK, WeWorkRemotely, and Remote.co in addition to the local Malawi listings.
- Success criteria: `init_scheduler` registers two additional configs mirroring the Malawi queries with `location="Remote"` restricted to `[REMOTE_OK, WE_WORK_REMOTELY, REMOTE_CO]`; existing configs untouched.
- Acceptance criteria: ruff + mypy pass on the file; athena test suite passes; no model/API/frontend changes; ECL harness documents the change; PR to `main` runs the 10 CI checks.

## Non-Goals

- Structured remote/work-mode flag on `Job` and dashboard filtering — deferred.
- `location=remote` inside the malawijobs board scrapers — deferred.
- Changing the existing 4 default configs or their sources.

## Constraints

- Scheduler-only change; no edits to models, schemas, API routes, or frontend.
- Do not commit unrelated working-tree changes (e.g. `orchestrator/approvals.yaml`, executor loop, registry files).
- Commit only `src/ai_company/athena/scheduler/jobs.py` plus the ECL harness files for this change.
- PR to `main` is protected: 10 CI checks (ruff, mypy, pytest ubuntu+windows, ECL harness lint, bandit, uv-audit, generated-files drift, archify, version sync).

## Assumptions

- Local `main` was reconciled with `origin/main` (athena sources present in the working tree at `371244b1`).
- `JobSource.REMOTE_OK`, `JobSource.WE_WORK_REMOTELY`, `JobSource.REMOTE_CO` exist in `src/ai_company/athena/models/enums.py` (verified at lines 17-19).

## Open Questions

- None.

## Resolved Clarifications

- User selected "Curated Malawi+Remote scheduled scrapes (Recommended)" over a structured remote flag / dashboard filter for this round.
