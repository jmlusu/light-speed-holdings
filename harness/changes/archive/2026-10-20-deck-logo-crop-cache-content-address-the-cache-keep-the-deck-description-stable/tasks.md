# Tasks

## Format

- ``- [ ] T001 [P?] [US?] Action with target path and validation note``
- ``[P]`` means parallel-safe. ``[US1]`` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review ``spec.md`` and ``plan.md`` gates before implementation. (Spec and plan written; plan approved in ``reviews/review.md``.)
- [x] T002 Park the unrelated active ECL change ``haomtgv-blueprint-hero-and-page-wiring`` with ``harness-change.ps1 park`` to free the single active slot, and resume it after this change closes. (Parked to ``harness/changes/parking/2026-10-20-haomtgv-blueprint-hero-and-page-wiring``; resume run in the close step.)

## Implementation

- [x] T003 Make ``_cropped_logo()`` in ``scripts/presentation/generate-ai-venture-studio-deck.py`` content-addressed (SHA-256 prefix of the source in the cache file name) and return the stable deck name alongside the cache path. Validation: unit test T005.
- [x] T004 Set the picture ``descr`` to the stable name in ``logo()`` so the content-addressed cache name never reaches the deck XML. Validation: unit test T006 and the drift guard.
- [x] T005 Add ``test_crop_cache_is_content_addressed`` to ``tests/presentation/test_venture_studio_deck.py`` (same size, different content, same old mtime -> different crop). Validation: ``pytest tests/presentation``.
- [x] T006 Add ``test_built_deck_uses_the_stable_picture_description`` to ``tests/presentation/test_venture_studio_deck.py``. Validation: ``pytest tests/presentation``.
- [x] T007 Add the permanent-record row to ``docs/known-issues.md`` and entries to ``CHANGELOG.md`` and ``docs/STATUS.md``. Validation: ``lint-ecl.ps1`` and the docs drift check.

## Validation

- [x] T008 Run ``uv run ruff check`` / ``ruff format --check`` and ``pytest tests/presentation -q``. Validation: ruff clean, 10 passed.
- [x] T009 Run both deck gates on the committed deck and prove the artifact is unchanged (``git diff --exit-code -- ai_venture_studio_client_presentation.pptx``). Validation: 11/11 checks pass, all render checks pass, no artifact diff.
- [x] T010 Run the full non-e2e pytest suite, ``lint-ecl.ps1`` and ``check-index-freshness.ps1``. Validation: suite green, both scripts PASS.
- [x] T011 Open the PR, wait for the required checks, squash-merge, and clean up the branch and worktree; resume the parked HAOMTGV change. Validation: PR merged into ``main``; branch and worktree removed; HAOMTGV back in ``harness/changes/active/``.

## Deferred Tasks

- None.
