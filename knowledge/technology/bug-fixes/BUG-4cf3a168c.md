# fix(vercel): re-include data/*/registry.ts excluded by .vercelignore

**ID:** BUG-4cf3a168c
**Date:** 2026-10-12
**Resolved:** resolved
**Commit:** 4cf3a168cce180c32cada5a1a374a58148ee7906
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

`.vercelignore` has excluded `/data/` wholesale since c402a3a5. PR
#433 (commit 794e793b) then committed the 12 `data/*/registry.ts`
files that `vite.config.ts:51-62` aliases `@lightspeed/data/*` to.
GitHub check runs use a git checkout (which has the files) so they
passed, while Vercel strips `/data/` per `.vercelignore` before upload
-> ENOENT on `data/use-cases/registry.ts` during Vercel builds only.
Failure onset is exactly 794e793b; pre-#433 Vercel statuses predate
the aliased imports being routed. #433 fixed the `.gitignore` analog
for CI but left the `.vercelignore` counterpart broken.

## Fix (filled by the resolving engineer)

Replaced the bare `/data/` rule in `.vercelignore` with the whitelist
already used in `.gitignore:89-130`: exclude `/data/*`, re-include
each aliased `<dir>/` and its `<dir>/registry.ts` (12 dirs:
capabilities, claims, company, ctas, faqs, governance, insights,
media, metrics, sectors, solutions, use-cases). Runtime state
(orchestrator, agents, catalog, *.db) stays excluded. File edit
provenance was unattributed (mtime 2026-10-12 00:46 local) and was
disclosed in the PR #437 body / PR #436 body accordingly.

## Files Changed

`.vercelignore`.

## Diagnostic Commands

```powershell
git ls-tree 67f87b72 -- data                    # empty: pre-#433
git log --diff-filter=A -- data/company/registry.ts   # 794e793b
gh api repos/jmlusu/light-speed-holdings/commits/736ce9fb/status
```

## Verification

PR #436 Vercel check green ("Deployment has completed") — the
check that was red before; main CI run 38182775410 at 736ce9fb exit
0; combined commit status on main tip 736ce9fb: `Vercel = success`.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
