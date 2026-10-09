---
title: "Studio Scorecard v1 instrumentation (T2 #418)"
slug: "studio-scorecard-v1-instrumentation-t2-418"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: ["models", "orchestrator", "dashboard/kpis", "dashboard/api"]
files: ["src/ai_company/models/models.py", "company/studio_tracker.yaml", "src/ai_company/dashboard/kpis/studio.py", "src/ai_company/dashboard/api.py"]
tags: ["wayfinder", "t2-418", "studio-scorecard", "observability"]
validation_status: "pass"
created_at: "2026-10-07"
updated_at: "2026-10-07"
session_id: "b79de387-0a9a-4f00-b151-8f5027cf9161"
owner_agent: "jmlus"
claimed_at: "2026-10-07"
---

# Summary

## Outcome

T2 #418 in progress — Studio Scorecard v1 instrumentation (collectors + page + 30-day baseline). T1 signed sheet consumed as spec; user-approved cuts: full four metrics, `company/studio_tracker.yaml`, new page + API.

## Decisions

- ECL slot freed 2026-10-07: prior occupant (T4 #420, committed `3ab829fa`, self-declared complete) archived to `archive/2026-10-07-t4-competitive-landscape-oct-refresh-420` under explicit user confirmation; only lifecycle-state edits made to it (phase/validation/plan_review + one stale NEEDS-CLARIFICATION marker removal).
- Implementation is additive-only: optional `Task` fields, new tracker YAML, new collector + endpoint; no Org Health changes, no new alerts, no fabricated figures.

## Validation

- `ruff check src/` (+ new test file): PASS, 0 errors.
- `mypy src/`: PASS, 226 files, 0 errors (strict).
- `pytest -m "not e2e" --ignore=tests/e2e` (isolated `--basetemp`, `git status` snapshot before/after identical): **2521 passed / 2 skipped / 0 failed**, incl. 10 new `test_studio_scorecard.py` + updated dept-count assertion (8→9).
- `validate-drift.ps1`: PASS, 87 files, no drift (kpis.yaml SoT claims untouched).
- `lint-ecl.ps1`: PASS.
- Live smoke: collector on real inbox → ATC 41.5% (fallback quality, labeled), correction 0.0 measurement-only, capital withheld (unratified), ventures `no_data` with reasons, baseline Day 1/30.
- validation_status: pass.

## Next Step

- T008: `close completed` + resolution comment on #418.

