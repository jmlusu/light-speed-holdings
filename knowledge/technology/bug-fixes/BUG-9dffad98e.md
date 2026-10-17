# fix(brand): repair sync-brand.ps1 nesting bug, add -Prune/-Verify, prune+resync mirrors

**ID:** BUG-9dffad98e
**Date:** 2026-09-27
**Resolved:** resolved
**Commit:** 9dffad98e534e43d6148b81be2e2c5163c29e361
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

`scripts/build/sync-brand.ps1` copied canonical `brand/**` files into the mirror
trees with a path-nesting bug (writes landed under nested subdirectories)
and had no stale-file removal, so files deleted or renamed in canonical
`brand/**` lingered forever as stale mirror files. The mirrors had drifted
from canonical with no way to detect (`-Verify`) or clean (`-Prune`) it.

## Fix (filled by the resolving engineer)

Rewrote `scripts/build/sync-brand.ps1` with `-Prune` (delete mirror files with no
canonical counterpart) and `-Verify` (byte-compare, exit non-zero on drift)
modes; committed the previously untracked mirror assets; added a
`(print|dist|logos)` large-file exclude to `.pre-commit-config.yaml` so
generated brand artifacts don't trip the added-large-files hook.

## Files Changed

`scripts/build/sync-brand.ps1`, `.pre-commit-config.yaml`, mirror assets under
`static/brand/` + `public/brand/` (39-file purge landed alongside in
`a750bd3a`).

## Diagnostic Commands

```powershell
pwsh scripts/build/sync-brand.ps1 -Verify   # reported MISSING/DRIFT
git status --porcelain static/brand public/brand
```

## Verification

`uv run ruff check src/` clean, `uv run mypy src/` success,
`uv run pytest -q` 2566 passed; final `pwsh scripts/build/sync-brand.ps1 -Verify`
→ Verify OK after `ff0d33a7`.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
