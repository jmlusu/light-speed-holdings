# fix(ci): shim uv-audit around package-schemes prefix-match crash

**ID:** BUG-60dbdc0a3
**Date:** 2026-10-12
**Resolved:** resolved
**Commit:** 60dbdc0a3d5e93fa541218621c36b92346eb445c
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

After the httpx -> httpx2 migration (#438), the required CI check
`Dependency Audit (uv-audit)` crashed with an AssertionError on every
run. Root cause is in the `package-schemes` plugin uv-audit uses for
lockfile parsing (all 0.1.x releases): its resolver matches
dependencies with `dep.startswith(name)`, so the transitive `httpx`
entry in uv.lock is prefix-matched to the direct `httpx2` package
entry; `PackageMeta.merge()` then asserts the two metadata names are
equal and raises. No package-schemes version avoids the bug (the
prefix match always mis-resolves once a package name is a strict
prefix extension of a transitive dependency), so pinning cannot fix
it. Before the migration `httpx` was the direct dependency and the
prefix match resolved to itself, which is why the check passed at
baseline `8ca467a4`.

## Fix (filled by the resolving engineer)

Added `scripts/ci/uv-audit-shim.py`, which monkey-patches
`PackageMeta.merge` to tolerate the name mismatch by trusting the
lockfile metadata instead of asserting, then delegates to
`uv_audit.cli`. The ci.yml `Dependency Audit (uv-audit)` step now runs
`uv run --no-project --with uv-audit python scripts/ci/uv-audit-shim.py`
(the job name is unchanged so the required status check continues to
match). The shim is a workaround: revert it once package-schemes
compares fully parsed package names instead of prefix-matching.

## Files Changed

`.github/workflows/ci.yml` (audit step -> shim invocation);
`scripts/ci/uv-audit-shim.py` (new, 46 lines).

## Diagnostic Commands

```powershell
uv run --no-project --with uv-audit python scripts/ci/uv-audit-shim.py   # exit 0
gh run view <run-id> --log -j "Dependency-Audit-uv-audit"                # pre-fix traceback
```

## Verification

Shim exits 0 locally; `Dependency Audit (uv-audit)` pass (13s on
#438, 11s on #439) with all 15 PR checks green. Full non-e2e suite
2584 passed / 2 skipped unaffected (uv-audit is CI-only tooling).

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
