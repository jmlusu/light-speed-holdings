# fix: resolve leftover merge conflicts in CI workflow and luxury linter

**ID:** BUG-dd7ffa0f5
**Date:** 2026-11-23
**Resolved:** resolved
**Commit:** dd7ffa0f57fddd6dbb568fbc0a1355509eb78aa0
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(N/A - generated from commit dd7ffa0f5.)

The CI workflow on `main` produced a run with zero jobs and conclusion
`failure` (run 45081488439); the workflow file could not be parsed.

## Root Cause (filled by the resolving engineer)

Earlier merges (c594ad02 and 45289770) staged `.github/workflows/ci.yml`
and `docs/compliance/luxury-linter.py` without resolving their conflict
markers. Nested `<<<<<<< HEAD` / `=======` / `>>>>>>>` blocks made ci.yml
invalid YAML, so GitHub Actions created no jobs. `luxury-linter.py` also
contained duplicate `count_accent_places` and `main` definitions and was
missing the scoped-linting improvements from the site-copy branch.

## Fix (filled by the resolving engineer)

- Removed all conflict markers from `.github/workflows/ci.yml` and kept the
  scoped `Run luxury linter` step (docs/standards, docs/theme,
  docs/compliance).
- Restored the complete improved `luxury-linter.py` implementation from
  commit 3cf17e77 (the site-copy branch tip), preserving its relaxed
  procedural line-length threshold and multi-root CLI.

## Files Changed

- `.github/workflows/ci.yml`
- `docs/compliance/luxury-linter.py`

## Diagnostic Commands

- `gh run view 45081488439 --json status,conclusion,jobs`
- `uv run python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`
- `uv run python docs/compliance/luxury-linter.py docs/standards docs/theme docs/compliance`
- `git diff b011908b 3cf17e77 -- docs/compliance/luxury-linter.py`

## Verification

- `ci.yml` parses as YAML with 15 jobs.
- The scoped luxury linter run exits 0 (2 documents checked, 1 exempt).
- All pre-commit hooks passed on commit dd7ffa0f5, including `check yaml`
  and `check for merge conflicts`.
- No `<<<<<<<` / `>>>>>>>` markers remain in tracked files.
