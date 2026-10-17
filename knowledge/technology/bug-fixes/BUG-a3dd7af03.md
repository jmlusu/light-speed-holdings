# fix(ecl): resolve duplicate session IDs in INDEX.json

**ID:** BUG-a3dd7af03
**Date:** 2026-10-11
**Resolved:** resolved
**Commit:** a3dd7af037c5fd3a58904ef4718720d3a36e414c
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Commit `a3dd7af0` (this record's commit) deduplicated session IDs but
missed two pairs where **distinct** archive changes — different slugs and
paths — were recorded under one session ID each:

- `acf21912-6a5a-4666-bceb-3f7d773aed1d` shared by
  `.../2026-09-23-client-site-phase-1...` and
  `.../2026-09-23-client-site-phase-3-trust-evidence-and-related-content`
- `0ef66804-66ce-4568-ac4f-2841f9d012f7` shared by
  `.../ls-mem-implementation...` and
  `.../2026-09-25-ls-mem-phase-3-data-model`

`tests/unit/test_ecl_change_lifecycle.py::test_no_duplicate_session_ids`
asserts uniqueness across entries with `location == "archive"`, so both
pairs failed. Root source of truth is each change's `summary.md`
(`harness-change.ps1:180` reads `$meta["session_id"]` during reindex), not
INDEX.json itself.

## Fix (filled by the resolving engineer)

Resolved by commit `8c324ec5`: assigned fresh UUIDs to the two phase-3
`summary.md` files — `eccdfd71-0cb6-4a34-bbbb-6605e2204911` (client-site
phase-3) and `cdab4616-e15c-4221-9504-9767c32e0eaf` (ls-mem phase-3) —
keeping the originals on the alphabetically-first changes, then applied
the matching 2-line edit to `harness/changes/INDEX.json` preserving the
committed entry order. Full reindex output was format churn (unsorted
pwsh ordering) and was deliberately discarded. See BUG-8c324ec50.

## Files Changed

- `harness/changes/archive/2026-09-23-client-site-phase-3-trust-evidence-and-related-content/summary.md`
- `harness/changes/archive/2026-09-25-ls-mem-phase-3-data-model/summary.md`
- `harness/changes/INDEX.json`

## Diagnostic Commands

```powershell
uv run pytest tests/unit/test_ecl_change_lifecycle.py -q
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/maintenance/lint-ecl.ps1
```

## Verification

- `test_ecl_change_lifecycle.py` → 6 passed (incl.
  `test_no_duplicate_session_ids` and `test_reindex_preserves_integrity`)
- Full `uv run pytest` → 2580 passed, 2 skipped, exit 0
- `pwsh scripts/maintenance/lint-ecl.ps1` → ECL lint passed, exit 0

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
