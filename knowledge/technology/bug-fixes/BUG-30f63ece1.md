# fix(tests): re-point KPI tests to kpis package after shim removal

**ID:** BUG-30f63ece1
**Date:** 2026-09-26
**Resolved:** closed
**Commit:** 30f63ece1d6b17ef0e8beba446a9743e1aa0ec3b
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Commit 0d74cd7 deleted the deprecated `ai_company.dashboard.kpi_collector`
shim, but five tests in `test_pipeline.py` and `test_kpi_collectors.py`
still imported it: the intended re-point was lost in a pre-commit
stash/restore cycle during that commit (the same mechanism that had
earlier reverted uncommitted website changes). All other stale imports
had been cleaned; only these five remained, so they failed with
ModuleNotFoundError as soon as the module was gone.

## Fix (filled by the resolving engineer)

Re-pointed `test_collect_engineering_kpis` to
`EngineeringKPICollector(project_root=...).collect()` and
`test_collect_all_kpis` to `kpis.collect_all_kpis(project_root=...)`,
exactly what the shim delegated to. Deleted `test_save_snapshot` and
`TestKpiSnapshotFilename` (they tested `save_snapshot`, which died with
the shim and had no remaining callers) and
`test_operations_logs_warning_on_corrupt_dlq` (tested the deleted
`kpis.operations` collector).

## Files Changed

- tests/integration/test_pipeline.py
- tests/unit/test_kpi_collectors.py

## Diagnostic Commands

- `uv run pytest tests/integration/test_pipeline.py tests/unit/test_kpi_collectors.py`
- `git grep -n "kpi_collector" -- tests/ src/`

## Verification

Full suite green after the fix: `uv run pytest` → 2552 passed, 2
skipped, 67 deselected (3 dead-code tests removed); ruff and mypy clean
(230 files); `bun run build` succeeded; targeted run 45/45 passed.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
