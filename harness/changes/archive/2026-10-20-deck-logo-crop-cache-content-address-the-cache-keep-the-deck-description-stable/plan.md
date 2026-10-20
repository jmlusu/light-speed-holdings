# Plan

## Technical Approach

1. **Content-address the cache.** `_cropped_logo()` computes a SHA-256 digest of the source asset and caches the crop under `ai-venture-studio-lockup-880x713-<sha8>.png`. Different content can never share a cache entry, whatever the timestamps say.
2. **Keep the deck stable.** `logo()` sets the picture's `descr` explicitly to `ai-venture-studio-lockup-880x713.png` (the stable name, returned alongside the cache path), so the content-addressed cache file name never reaches the deck XML. python-pptx sets `descr` from the file name, so this override is required.
3. **Regression tests.** Two new cases in `tests/presentation/test_venture_studio_deck.py`:
   - `test_crop_cache_is_content_addressed`: two same-size assets with different content and the same old mtime produce different cache paths and different pixels, while the stable name is identical.
   - `test_built_deck_uses_the_stable_picture_description`: the built deck carries `descr="ai-venture-studio-lockup-880x713.png"` and no content-addressed suffix.
4. **Documentation.** `docs/known-issues.md` row (permanent record), `CHANGELOG.md` entry, `docs/STATUS.md` handoff entry.

## Impacted Modules And Files

- `scripts/presentation/generate-ai-venture-studio-deck.py` - `_cropped_logo()` returns `(cache path, stable name)`; `logo()` overrides `descr`; `hashlib` and `pathlib.Path` imported.
- `tests/presentation/test_venture_studio_deck.py` - two new tests, `os` import.
- `docs/known-issues.md`, `CHANGELOG.md`, `docs/STATUS.md` - documentation.
- `harness/changes/**` - ECL record.

## Interfaces, Data, Permissions

- `_cropped_logo()` is a private helper; its return type changes from `str` to `tuple[str, str]`. No public API, data model or permission change.
- The deck's on-disk representation is unchanged: the committed .pptx stays byte-identical (the drift guard proves it).

## Spec Gaps Found From Planning

- None.

## Risks And Mitigations

- **The deck could drift** if the `descr` override is dropped. Mitigation: `test_built_deck_uses_the_stable_picture_description` asserts the exact description, and the drift guard compares the committed deck against a fresh build.
- **Temp-dir growth**: each distinct asset version leaves one cached crop. Mitigation: the files are small (a few hundred KB) and the cache name is content-addressed, so a repeated build reuses the same file.
- **The change could silently alter the deck.** Mitigation: the committed deck is not regenerated; the drift guard fails if the output changed.

## Verification Plan

- `uv run ruff check` and `uv run ruff format --check` on the touched files.
- `uv run pytest tests/presentation -q` (10 tests).
- `uv run --with python-pptx python scripts/presentation/verify-venture-studio-deck.py` (11 checks) and `uv run --with pymupdf python scripts/presentation/render-venture-studio-deck.py` (rendered pixels) on the committed deck.
- `git diff --exit-code -- ai_venture_studio_client_presentation.pptx` to prove the artifact is unchanged.
- `pwsh scripts/maintenance/lint-ecl.ps1` and `pwsh scripts/maintenance/check-index-freshness.ps1`.
- Full non-e2e pytest suite.
- CI on the PR.
