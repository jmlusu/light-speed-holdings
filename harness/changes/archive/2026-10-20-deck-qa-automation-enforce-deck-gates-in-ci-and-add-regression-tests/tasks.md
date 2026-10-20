# Tasks

## Format

- ``- [ ] T001 [P?] [US?] Action with target path and validation note``
- ``[P]`` means parallel-safe. ``[US1]`` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review ``spec.md`` and ``plan.md`` gates before implementation. (Spec and plan written; plan approved in ``reviews/review.md``.)
- [x] T002 Park the unrelated active ECL change ``haomtgv-blueprint-hero-and-page-wiring`` with ``harness-change.ps1 park`` so the single active slot is free, and resume it after this change closes. (Parked to ``harness/changes/parking/2026-10-20-haomtgv-blueprint-hero-and-page-wiring``; resume run in the close step.)

## Implementation

- [x] T003 Add ``scripts/presentation/deck_geometry.py`` with the shared design intent (crop box, source size, aspect, cover and closing lockup placement, tagline and cover-title top edges, ``MIN_GAP_IN``). Validation: module imports and the three tools import from it.
- [x] T004 Update ``scripts/presentation/generate-ai-venture-studio-deck.py`` to import the shared geometry, place both lockups from it, refuse a brand asset whose size is not ``LOGO_SRC_SIZE``, and re-cut the cached crop when the source is newer. Validation: generator rebuilds the deck; the rebuilt deck is byte-identical to the committed one.
- [x] T005 Update ``scripts/presentation/verify-venture-studio-deck.py`` to assert the shared placement for both lockups. Validation: ``ALL 11 CHECKS PASSED`` on the rebuilt deck; 2/11 fail on the pre-fix deck.
- [x] T006 Extend ``scripts/presentation/render-venture-studio-deck.py`` with the cover probe, the declared-edge clearance and the tagline position check. Validation: all render checks pass on the rebuilt deck; 3 checks fail on the pre-fix deck.
- [x] T007 Add ``tests/presentation/conftest.py`` and ``tests/presentation/test_venture_studio_deck.py``. Validation: ``pytest tests/presentation`` 8 passed.
- [x] T008 Add ``Deck QA (structure)`` and ``Deck QA (rendered pixels)`` to ``.github/workflows/ci.yml`` and wire both into the ``CI Gate`` aggregate. Validation: workflow parses; both jobs green on the PR.
- [x] T009 Update ``docs/deck-generation.md``, ``docs/STATUS.md`` and ``CHANGELOG.md``. Validation: ``lint-ecl.ps1`` and the docs drift check pass.

## Validation

- [x] T010 Run ``uv run ruff check scripts/presentation/ tests/presentation/`` and the full non-e2e pytest suite. Validation: ruff clean; pytest green.
- [x] T011 Run both deck gates against the rebuilt deck and against the pre-fix deck as a negative control. Validation: rebuilt deck passes every check; pre-fix deck fails.
- [x] T012 Run ``pwsh scripts/maintenance/lint-ecl.ps1`` and ``pwsh scripts/maintenance/check-index-freshness.ps1``. Validation: both PASS.
- [x] T013 Open the PR, wait for the required checks, squash-merge, and clean up the branch and worktree. Validation: PR merged into ``main``; branch and worktree removed; the parked HAOMTGV change resumed.

## Deferred Tasks

- None.
