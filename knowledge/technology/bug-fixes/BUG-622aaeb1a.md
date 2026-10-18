# fix(test): strip ANSI in autonomous help assertions under CI

**ID:** BUG-622aaeb1a
**Date:** 2026-10-18
**Resolved:** resolved
**Commit:** 622aaeb1ad6b87e36e50f4d9a6fecd329be70566 (squashed into main as af3d2e4d via PR #477)
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

CI failure on PR #477, run 39129731226: `tests/unit/test_dashboard_autonomous.py::test_autonomous_help_renders` failed on both ubuntu-latest and windows-latest with the Rich help renderer's ANSI codes in output. Local runs passed.

## Root Cause (filled by the resolving engineer)

Rich forces color output when the `GITHUB_ACTIONS` environment variable is set, emitting ANSI escape sequences into the captured help text. The test asserted `--no-executor` was a contiguous substring of the raw output, which failed because ANSI codes were interleaved around the flag text. Same root cause as previously documented in `tests/unit/test_cli_lazy.py` and `tests/cli/test_cli_archify.py`.

## Fix (filled by the resolving engineer)

Added a `_strip_ansi()` helper (via `re`) to `tests/unit/test_dashboard_autonomous.py` and asserted against the stripped output in both `test_autonomous_help_renders` and the `--no-executor` help test, matching the existing `_strip_ansi` precedent in the other two test files.

## Files Changed

- `tests/unit/test_dashboard_autonomous.py` (+19/−5): `_ANSI_ESCAPE` regex, `_strip_ansi()` helper, both help tests assert on stripped output.

## Diagnostic Commands

- `git -C C:\Users\jmlus\light-speed-holdings log --all -S "_strip_ansi" -- tests/`
- Reproduce: set `GITHUB_ACTIONS=true` locally and run the two help tests without the fix — they fail; with the fix, they pass.
- Proof of interleaving: raw help contains ANSI (`has_ansi: True`, `raw_has_flag: False`); stripped help contains the flag (`plain_has_flag: True`).

## Verification

- Local: `uv run pytest tests/unit/test_dashboard_autonomous.py` — 10 passed (before and after); simulated CI via `$env:GITHUB_ACTIONS='true'` — both help tests PASS with the fix.
- CI: run 39129541295 green on ubuntu-latest and windows-latest after the fix commit; full PR #477 checks green on run 39130346841 after branch update; squash-merged to main as af3d2e4d.

## Link an Issue

No linked issue. Conventional-commit fix without an issue reference.
