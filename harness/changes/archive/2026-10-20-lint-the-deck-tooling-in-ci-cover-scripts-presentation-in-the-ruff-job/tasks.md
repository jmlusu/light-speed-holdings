# Tasks

## Format

- ``- [ ] T001 [P?] [US?] Action with target path and validation note``
- ``[P]`` means parallel-safe. ``[US1]`` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review ``spec.md`` and ``plan.md`` gates before implementation. (Spec and plan written; plan approved in ``reviews/review.md``.)
- [x] T002 Park the unrelated active ECL change ``haomtgv-blueprint-hero-and-page-wiring`` with ``harness-change.ps1 park`` to free the single active slot, and resume it after this change closes. (Parked to ``harness/changes/parking/2026-10-20-haomtgv-blueprint-hero-and-page-wiring``; resume run in the close step.)
- [x] T003 Measure the lint state of ``scripts/`` to size the change. Validation: 13 findings, 2 in ``scripts/presentation/`` and 11 in ``scripts/maintenance/`` (left alone - other owners' files).

## Implementation

- [x] T004 Make ``scripts/presentation/`` lint- and format-clean: fix the import order and the missing newline in ``scripts/presentation/verify-deck.py`` and apply the repo's formatter. Validation: T008.
- [x] T005 Extend the ``Lint (ruff)`` job in ``.github/workflows/ci.yml`` to cover ``scripts/presentation/``, with a comment recording why. Validation: the job is green on the PR.
- [x] T006 Add entries to ``CHANGELOG.md`` and ``docs/STATUS.md``. Validation: ``lint-ecl.ps1`` and the docs drift check.

## Validation

- [x] T007 Run ``uv run pytest tests/presentation -q`` and ``uv run pytest tests/performance -q``. Validation: both green.
- [x] T008 Run ``uv run ruff check scripts/presentation/`` and ``ruff format --check scripts/presentation/``. Validation: all checks passed, 5 files already formatted.
- [x] T009 Run the full non-e2e pytest suite, ``lint-ecl.ps1`` and ``check-index-freshness.ps1``. Validation: suite green, both scripts PASS.
- [x] T010 Open the PR, wait for the required checks, squash-merge, and clean up the branch and worktree; resume the parked HAOMTGV change. Validation: PR merged into ``main``; branch and worktree removed; HAOMTGV back in ``harness/changes/active/``.

## Deferred Tasks

- Eleven ruff findings remain in ``scripts/maintenance/`` (unsorted imports, unused imports, a blind except, two simplify suggestions). They are outside the deck tooling and some of those files are under active work elsewhere; widening the CI lint scope to all of ``scripts/`` is a separate cleanup.
