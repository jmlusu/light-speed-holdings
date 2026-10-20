# Spec

## Intake Review

- Intake type: Small Change
- Input shape: requirement-first (gap identified in the audit of the deck QA work)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: the deck tooling under `scripts/presentation/` is not linted by CI. The `Lint (ruff)` job covers `src/` and `tests/` only, so the scripts that generate, verify and render the client deck were policed solely by the local pre-commit hook - which `--no-verify` can bypass, exactly the situation the CI gate exists to prevent ("Local pre-commit hooks can be bypassed with --no-verify, so this server-side gate is the enforced source of truth").
- Current behavior: `uv run ruff check src/ tests/` in `.github/workflows/ci.yml`. `scripts/presentation/` held two pre-existing ruff findings (`scripts/presentation/verify-deck.py`: unsorted imports, no newline at end of file), so it could not simply be added to the scope.
- Source of evidence: the read-only audit of the deck QA change (PR #483), which measured the CI lint scope and the two findings; the pre-existing findings predate this work (blob `948c63e3` is identical on the base commit and on `main`).

## User Scenarios And Success

- Primary user/system scenario: a change to the deck tooling that introduces a lint error is proposed. The server-side gate must reject it, exactly as it would for a change under `src/`.
- Success criteria:
  - The `Lint (ruff)` job covers `scripts/presentation/`.
  - `scripts/presentation/` is lint-clean, so the widened scope is green on the first run.
  - No other area's files are touched.
- Acceptance criteria: `ruff check scripts/presentation/` clean, `ruff format --check scripts/presentation/` clean, CI green with the widened scope, and no behaviour change in the deck tooling.

## Non-Goals

- Widening the CI lint scope to the whole `scripts/` tree. Eleven findings remain in `scripts/maintenance/` (throwaway and debug scripts, some of them under active work elsewhere); that is a separate cleanup with a different owner.
- Adding `ruff format --check` to CI. The repository has known format drift under `src/` (see `docs/STATUS.md`), so a format gate would fail on unrelated files.
- Changing any deck behaviour.

## Constraints

- `main` is protected: branch, PR, required checks green before merge.
- Files under active work by other sessions must not be touched. The eleven `scripts/maintenance/` findings are left alone for that reason.
- ECL allows one active change; `haomtgv-blueprint-hero-and-page-wiring` was parked with the harness script and is resumed after this change closes.

## Assumptions

- `ruff` resolves to the same pinned version locally and in CI, so a clean local run means a clean CI run.

## Open Questions

- None.

## Resolved Clarifications

- The two pre-existing findings in `verify-deck.py` are fixed as part of this change rather than excluded: the file is in the directory this work owns, it is not under anyone's active edit, and excluding it would leave the scope fragile.
