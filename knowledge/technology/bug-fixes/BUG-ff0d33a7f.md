# fix(brand): resync stale mirror files, fix canonical whitespace + Verify paths

**ID:** BUG-ff0d33a7f
**Date:** 2026-09-27
**Resolved:** resolved
**Commit:** ff0d33a7f877a094e86281c787d002edec1c7eef
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Three residual defects after `9d688fae`: (1) 31 mirror files were still
stale because the earlier resync hadn't covered them; (2) the canonical
source `brand/logos/icononly/fullcolor_logo_icon_nobackground.svg` contained
trailing whitespace, so every future sync would regenerate drift at the
source; (3) the `-Verify` path bug reported `$mirror$rel` instead of the
actual failing destination `$dst$rel`, pointing diagnostics at the wrong
tree and masking real failures.

## Fix (filled by the resolving engineer)

Resynced the 31 stale mirror files, stripped the whitespace in the
canonical SVG at source (not the mirror), and fixed the Verify message path
to `$dst$rel`.

## Files Changed

31 files under `static/brand/` + `public/brand/`,
`brand/logos/icononly/fullcolor_logo_icon_nobackground.svg`,
`scripts/sync-brand.ps1`.

## Diagnostic Commands

```powershell
pwsh scripts/sync-brand.ps1 -Verify   # was: wrong-path report / drift
```

## Verification

`pwsh scripts/sync-brand.ps1 -Verify` → **Verify OK** (mirrors byte-identical
to canonical, no nested directories); `bun run build` + `bun run test` green.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
