# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

### Track A: Version / Count Reconciliation [P]

- [x] T002 Update `docs/CHANGELOG.md` — add `## [0.4.0]` entry summarizing Sprints 4-7 (GAP-019, OAuth2, tool vocabulary, HITL expiry, governance, KPIs). Verify: `grep '## \[0.4.0\]' docs/CHANGELOG.md`
- [P] T003 Update `docs/API-REFERENCE.md` — fix version `0.1.0` → `0.4.0` (line 7). Verify: `grep 'Version: 0.4.0' docs/API-REFERENCE.md`
- [P] T004 Update `docs/USER-GUIDE.md` — correct agent count `27` → `127` (lines 45, 100). Verify: `grep '127 agents' docs/USER-GUIDE.md`
- [P] T005 Update `docs/DEVELOPER-GUIDE.md` — correct CLI count `24` → `30` (line 92). Verify: `grep '30 commands' docs/DEVELOPER-GUIDE.md`
- [P] T006 Update `docs/STATUS.md` — fix GAP resolved count `6` → `20` (line 79), test count `1805` → `1856` (lines 48, 73, 131), add Historical Audits section. Verify: `grep '20 of 20' docs/STATUS.md` and `grep '1856 tests' docs/STATUS.md`

### Track B: SOP Supersession + Missing Feature Docs [P]

- [P] T007 Mark `docs/sop-deployment.md` frontmatter `status: superseded` (v1 → superseded by v2). Verify: `grep 'status: superseded' docs/sop-deployment.md`
- [P] T008 Mark `docs/sop-incident-response.md` frontmatter `status: superseded` (v1 → superseded by v2). Verify: `grep 'status: superseded' docs/sop-incident-response.md`
- [P] T009 Update `docs/ORCHESTRATION-PLAN.md` — fix GAP-019 status from OPEN to CLOSED (line 468). Verify: `grep 'CLOSED' docs/ORCHESTRATION-PLAN.md`
- [x] T010 Add OAuth2 documentation to `docs/USER-GUIDE.md` + `docs/DEVELOPER-GUIDE.md` + `docs/API-REFERENCE.md`. Verify: `grep -i oauth2 docs/USER-GUIDE.md`
- [x] T011 Add ML module section to `docs/DEVELOPER-GUIDE.md`. Verify: `grep -i "ML module" docs/DEVELOPER-GUIDE.md`
- [x] T012 Add Security module section to `docs/DEVELOPER-GUIDE.md`. Verify: `grep -i "Security module" docs/DEVELOPER-GUIDE.md`
- [x] T013 Add Data Governance CLI section to `docs/USER-GUIDE.md`. Verify: `grep -i "governance" docs/USER-GUIDE.md`
- [x] T014 Add Structured Logging / Correlation IDs section to `docs/DEVELOPER-GUIDE.md` (GAP-018). Verify: `grep -i "correlation" docs/DEVELOPER-GUIDE.md`

## Validation

- [x] T015 Run `scripts/lint-ecl.ps1` — verify ECL structure valid.
- [x] T016 Run `uv run ruff check src/ tests/` — clean.
- [x] T017 Run `uv run mypy src/` — clean.
- [x] T018 Run `uv run pytest -q -m "not e2e"` — 1856 passed, 0 failures.
- [x] T019 Verify version consistency: pyproject.toml == API-REFERENCE.md == CHANGELOG.md == 0.4.0

## Deferred Tasks

- T020 Consolidate milestone deck tooling (3 docs → 1, 6 scripts → 2). Low priority — not Sprint 7 scope.
- T021 Merge/differentiate RECONCILIATION_PLAN.md vs DATA_RECONCILIATION_PLAN.md. Low priority — not Sprint 7 scope.
- T022 Add "Historical Audits" section to STATUS.md linking root CEO_* reports. Pending decision on whether PROJECT_STATUS.md should be single source of truth.
