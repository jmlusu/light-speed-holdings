# fix: JSX syntax error in FloatingNav.tsx - missing closing } for showGovernance expression

**ID:** BUG-a1fe8548e
**Date:** 2026-10-11
**Resolved:** resolved
**Commit:** a1fe8548efcb13f0fe155b7985dd24ffa0df7b15
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Merge conflict resolution `bb3059c0` placed the governance overlay JSX
outside the `return (` statement and left the file with mojibake and
spliced/duplicated lines. Commit `a1fe8548` (this record's commit) closed
the missing `}` but did not restore a structurally valid component, so
`npx tsc --noEmit` continued to fail (TS1128 and duplicate
`governanceOverlay` definitions). The conflict resolution had separately
dropped the 7 page imports from `src/App.tsx`.

## Fix (filled by the resolving engineer)

Resolved by commit `8c324ec5`: full rewrite of
`src/components/FloatingNav.tsx` (correct `return (<>...</header>
{showGovernance && (...)}</>);` with named + default exports) and
re-adding the 7 page imports to `src/App.tsx`. See BUG-8c324ec50 for
the complete record.

## Files Changed

- `src/components/FloatingNav.tsx`
- `src/App.tsx`

## Diagnostic Commands

```powershell
npx tsc --noEmit
```

## Verification

`npx tsc --noEmit` → exit 0 after `8c324ec5`; full Phase 2 gate
(pytest 2580 passed, ruff, mypy, build, lint-ecl) all green on branch
`reconcile/local-main-2026-10-11`.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
