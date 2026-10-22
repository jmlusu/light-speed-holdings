# Tasks

## Format

- ``- [ ] T001 [P?] [US?] Action with target path and validation note``
- ``[P]`` means parallel-safe. ``[US1]`` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review ``spec.md`` and ``plan.md`` gates before implementation. (Spec and plan written; plan approved in ``reviews/review.md``.)
- [x] T002 Park the unrelated active ECL change ``haomtgv-blueprint-hero-and-page-wiring`` with ``harness-change.ps1 park`` to free the single active slot, and resume it after this change closes. (Parked to ``harness/changes/parking/2026-10-20-haomtgv-blueprint-hero-and-page-wiring``; resume run in the close step.)
- [x] T003 Measure the registry read and every endpoint in the gate to calibrate against real numbers. Validation: local measurements recorded in ``plan.md`` (registry read 8.4 ms; endpoint medians 10-90 ms).

## Implementation

- [x] T004 Recalibrate ``tests/performance/test_dashboard_performance.py``: warm-up request, 20 samples, median assertion against a per-endpoint budget table, load-tolerant ceiling. Validation: T010.
- [x] T005 Cache the registry read in ``src/ai_company/dashboard/api.py`` keyed on the file's path, mtime and size, returning per-call normalized copies. Validation: T011 and the benchmark in T012.
- [x] T006 Add ``tests/unit/test_dashboard_registry_cache.py`` covering read-once, immediate invalidation, normalization and caller isolation. Validation: 4 passed.
- [x] T007 Add the permanent-record row to ``docs/known-issues.md`` and entries to ``CHANGELOG.md`` and ``docs/STATUS.md``. Validation: ``lint-ecl.ps1`` and the docs drift check.

## Validation

- [x] T008 Run ``uv run ruff check`` / ``ruff format --check`` on the touched files and ``uv run mypy src/``. Validation: ruff clean, mypy 232 files clean.
- [x] T009 Run ``pytest tests/unit -k "dashboard or org_chart or registry"``. Validation: 414 passed.
- [x] T010 Run ``pytest tests/performance`` twice. Validation: 28 passed on both runs.
- [x] T011 Benchmark ``_load_registry()`` before and after. Validation: 8.4 ms -> 0.26 ms median (33x).
- [x] T012 Run the full non-e2e pytest suite, ``lint-ecl.ps1`` and ``check-index-freshness.ps1``. Validation: suite green, both scripts PASS.
- [x] T013 Open the PR, wait for the required checks, squash-merge, and clean up the branch and worktree; resume the parked HAOMTGV change. Validation: PR merged into ``main``; branch and worktree removed; HAOMTGV back in ``harness/changes/active/``.

## Deferred Tasks

- None.
