# Plan

## Technical Approach

1. **Single source of truth.** Add `scripts/presentation/deck_geometry.py` with the deck's design intent: the logo crop box and source size, the aspect, the cover and closing lockup placement, the tagline and cover-title top edges, and the `MIN_GAP_IN` clear-space invariant. The generator, the verifier and the render gate import from it instead of repeating the numbers.
2. **Harden the generator.** `_cropped_logo()` refuses a brand asset whose size differs from `LOGO_SRC_SIZE` and re-cuts its cached crop whenever the source asset is newer than the cache. The crop file keeps a stable name because it ends up in the deck as the picture's description, so it must not vary between machines.
3. **Tighten the verifier.** `check_logo` asserts the exact shared placement (x, y, width, bottom) of both lockups instead of the loose "top-left / lower half" heuristics, keeping the srcRect, aspect and clearance checks.
4. **Extend the render gate.** Add a cover probe (the cover lockup was never pixel-checked) that finds the artwork as "not navy background and not the `#02062F` plate" and asserts it stays inside its frame and clear of the cover title. Measure the closing clearance against the declared tagline top edge so font substitution cannot mask a real overlap, and add a "tagline position" check that the rendered cyan tagline sits where it was declared.
5. **Regression suite.** Add `tests/presentation/` with a `conftest.py` that puts `scripts/presentation` on `sys.path` and `test_venture_studio_deck.py` with 8 tests: the generated deck passes every check; the logo is pre-cropped; the frame matches the shared geometry; the committed deck matches the generator output (drift guard, media compared by pixels); the pre-fix srcRect geometry, a frame overrunning the tagline, and a logo landing on text are each rejected; the generator refuses an unexpected logo size.
6. **CI enforcement.** Add `Deck QA (structure)` (verifier + `pytest tests/presentation`) and `Deck QA (rendered pixels)` (LibreOffice export + pixel probes) to `.github/workflows/ci.yml`, and add both to the `CI Gate` aggregate `needs`.
7. **Governance.** Update `docs/deck-generation.md`, `docs/STATUS.md` and `CHANGELOG.md`; close this ECL change so it lands in `harness/changes/archive/` with a regenerated `INDEX.json`.

## Impacted Modules And Files

- `scripts/presentation/deck_geometry.py` (new) - shared design intent.
- `scripts/presentation/generate-ai-venture-studio-deck.py` - imports the shared geometry, places the lockups from it, hardens the crop.
- `scripts/presentation/verify-venture-studio-deck.py` - imports the shared geometry, asserts the exact placement.
- `scripts/presentation/render-venture-studio-deck.py` - imports the shared geometry, adds the cover probe, font-tolerant clearance, tagline position check.
- `tests/presentation/conftest.py`, `tests/presentation/test_venture_studio_deck.py` (new) - regression suite.
- `.github/workflows/ci.yml` - two new jobs, wired into the gate.
- `docs/deck-generation.md`, `docs/STATUS.md`, `CHANGELOG.md` - documentation.
- `harness/changes/**` - ECL record for this change.

## Interfaces, Data, Permissions

- No public API, data model, permission or registry change. The deck tools stay under `scripts/presentation/` and are invoked by path, as before.
- `deck_geometry.py` is imported by name, which requires the tools to keep living in one directory (they do).

## Spec Gaps Found From Planning

- The audit asked for the render job to be added to `ci.yml`. Running LibreOffice on every PR adds install time to unrelated work, so the job installs LibreOffice only when `soffice` is missing, and both new jobs are wired into the `CI Gate` aggregate so they are real merge blockers rather than advisory checks.
- The audit's recommendation to key the crop cache on the source mtime was implemented as "stable file name plus re-cut when the source is newer" instead. A hash- or mtime-based file name would leak into the deck's picture description and make the artifact differ between machines, which would break the drift guard.

## Risks And Mitigations

- **CI font substitution** could make the rendered tagline sit at a different height than on Windows. Mitigation: clearance is measured against the declared tagline top edge; the rendered position is checked separately with a 0.12 in tolerance.
- **A deck job that fails for environmental reasons** (missing LibreOffice, apt hiccup) would block every PR. Mitigation: the render job installs LibreOffice only when absent, the gate is deterministic, and the negative control (pre-fix deck fails 3 checks) proves the checks are not vacuous.
- **Drift guard false positives** from PNG encoder differences. Mitigation: media is compared by decoded pixels, not file bytes.
- **The gate could be weakened to make a test pass.** Mitigation: the pre-fix deck is kept as a negative control and must keep failing.

## Verification Plan

- `uv run ruff check scripts/presentation/ tests/presentation/`
- `uv run pytest tests/presentation -q`
- `uv run --with python-pptx python scripts/presentation/verify-venture-studio-deck.py` on the rebuilt deck (expect `ALL 11 CHECKS PASSED`).
- `uv run --with pymupdf python scripts/presentation/render-venture-studio-deck.py` on the rebuilt deck (expect all checks pass) and on the pre-fix deck (expect failures).
- `pwsh scripts/maintenance/lint-ecl.ps1` and `pwsh scripts/maintenance/check-index-freshness.ps1`.
- Full non-e2e pytest suite.
- CI on the PR: both new required jobs green.
