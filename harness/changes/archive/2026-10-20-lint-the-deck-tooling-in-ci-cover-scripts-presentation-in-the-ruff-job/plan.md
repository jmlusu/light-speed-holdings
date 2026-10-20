# Plan

## Technical Approach

1. **Make `scripts/presentation/` clean.** `scripts/presentation/verify-deck.py` carried two pre-existing ruff findings (unsorted import block, no newline at end of file) and format drift. Run `ruff check --fix` and `ruff format` on it: the import order changes, the file gains a trailing newline, and long lines are wrapped. No behaviour change - the rewrites are import ordering and line wrapping only.
2. **Widen the CI lint scope.** `.github/workflows/ci.yml` -> `Lint (ruff)` job: `uv run ruff check src/ tests/` becomes `uv run ruff check src/ tests/ scripts/presentation/`, with a comment explaining why the directory is included.
3. **Documentation.** `CHANGELOG.md` and `docs/STATUS.md` entries.

## Impacted Modules And Files

- `scripts/presentation/verify-deck.py` - import order, trailing newline, line wrapping (no behaviour change).
- `.github/workflows/ci.yml` - the ruff job's scope.
- `CHANGELOG.md`, `docs/STATUS.md` - documentation.
- `harness/changes/**` - ECL record.

## Interfaces, Data, Permissions

- No public API, data model, permission or behaviour change. `verify-deck.py`'s CLI contract and outputs are unchanged.

## Spec Gaps Found From Planning

- Widening the scope to the whole `scripts/` tree was considered and rejected: eleven findings remain in `scripts/maintenance/`, several of them in files under active work in other sessions. The scope stops at the directory this work owns.

## Risks And Mitigations

- **The widened scope could fail on an unrelated future change to `scripts/presentation/`.** That is the intended behaviour of a lint gate: a deck tool that breaks lint is a deck tool that should not merge.
- **`ruff format` reformatting `verify-deck.py` could change behaviour.** Mitigation: the diff was reviewed - it is import ordering, a trailing newline, and line wrapping of two long expressions. The script's checks and output are untouched.
- **The scope could silently rot.** Mitigation: the comment above the ruff step names the directory and the reason, so the next person to touch the deck tooling sees why it is covered.

## Verification Plan

- `uv run ruff check scripts/presentation/` and `uv run ruff format --check scripts/presentation/`.
- `uv run pytest tests/presentation -q` (the deck tooling's own suite) and `uv run pytest tests/performance -q` (unchanged, but the deck and perf gates must stay green).
- Full non-e2e pytest suite.
- `pwsh scripts/maintenance/lint-ecl.ps1` and `check-index-freshness.ps1`.
- CI on the PR: the `Lint (ruff)` job must pass with the widened scope, plus all other required checks.
