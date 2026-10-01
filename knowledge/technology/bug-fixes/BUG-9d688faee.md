# fix(brand): complete mirror prune+resync lost to stash in 9dffad9

**ID:** BUG-9d688faee
**Date:** 2026-09-27
**Resolved:** resolved
**Commit:** 9d688faee76a80060a3aa21211b0e50959894f14
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Pre-commit's stash→restore cycle for the hook stages: a slow synchronous
post-commit graph-rebuild hook (~27 min run) blocked the post-commit stage
before pre-commit could restore its stash; the hook process was
killed (shell timeout) and the restore never ran, silently reverting every
unstaged tracked edit — including the tracked prune deletions, logo
overwrites, and sync-brand script rewrite staged during `9dffad9`. The lost
work was recovered from the pre-commit stash patch
(`C:\Users\jmlus\.cache\pre-commit\patch*42748`) via
`git apply --exclude=open-design <patch>`.

## Fix (filled by the resolving engineer)

Re-applied and re-committed the recovered 194-file change set (tracked
prune deletions + canonical logo overwrites + `sync-brand.ps1` rewrite).
Root cause of the loss class was fixed separately in `c7609025` by
backgrounding that rebuild hook via a backgrounded hook wrapper so the hook
exits in <1 s and the stash restore always completes.

## Files Changed

~194 files: tracked mirror prune deletions, `brand/logos/*` overwrites,
`scripts/sync-brand.ps1`.

## Diagnostic Commands

```powershell
git stash list                              # empty - restore never ran
ls $env:LOCALAPPDATA\..\Local\pre-commit\patch*  # pre-commit cache patches
git apply --exclude=open-design <patch-42748>
```

## Verification

Recovered tree matched the intended prune+resync; hooks green
(ruff/mypy/pytest 2566 passed); full stash→restore cycle verified end-to-end
after `c7609025` (2.3 s, co-session files restored intact).

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
