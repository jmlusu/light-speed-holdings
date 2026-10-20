---
title: "Deck logo crop cache: content-address the cache, keep the deck description stable"
slug: "deck-logo-crop-cache-content-address-the-cache-keep-the-deck-description-stable"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: ["scripts/presentation", "tests/presentation"]
files:
  - "scripts/presentation/generate-ai-venture-studio-deck.py"
  - "tests/presentation/test_venture_studio_deck.py"
  - "docs/known-issues.md"
  - "docs/STATUS.md"
  - "CHANGELOG.md"
tags: ["presentation", "qa", "correctness"]
validation_status: "pass"
created_at: "2026-10-20"
updated_at: "2026-10-20"
session_id: "6f0e0a4c-4c93-4a3a-9b6e-6a0b0d5f1c22"
owner_agent: "jmlus"
claimed_at: "2026-10-20"
---

# Summary

## Outcome

Closes issue #485, the residual edge case the audit of PR #480 raised.

The deck generator cached its pre-cropped logo under a fixed name and re-cut it only when the source asset was *newer* than the cache. mtime is not content identity, so a replaced `brand/logo/logo-full.png` carrying an older timestamp (backup restore, artifact copy, a build step that sets timestamps) silently reused the stale crop and the deck shipped the wrong logo.

The cache is now content-addressed: `_cropped_logo()` keys the cached crop on a SHA-256 prefix of the source, so different content can never share a cache entry whatever the timestamps say. The deck-facing picture description is set explicitly to the stable name `ai-venture-studio-lockup-880x713.png`, so the content-addressed cache file name never reaches the deck XML and the artifact stays byte-identical across machines.

Two regression tests were added: `test_crop_cache_is_content_addressed` (two same-size assets with different content and the same old mtime produce different cache paths and different pixels, while the stable name is identical) and `test_built_deck_uses_the_stable_picture_description` (the built deck carries the stable description and no content-addressed suffix).

The committed deck is unchanged.

## Decisions

- Decouple the cache key from the artifact identity rather than choosing one. Content-addressing alone would have leaked the digest into the deck's picture description and made the artifact differ between machines, breaking the drift guard; a stable cache name alone would have left the stale-crop hole open.
- Set `descr` on the picture element after `add_picture`, because python-pptx derives it from the file name. The generator already performs raw XML surgery for the `a:clrChange` transparency effect, so this is consistent with the file.
- Keep the deck out of the change: the crop box, the placement and the content are untouched, and the committed .pptx is not regenerated. The drift guard proves a fresh build is still byte-identical.

## Validation

- `uv run ruff check` and `uv run ruff format --check` on the two touched files: **All checks passed!** / **2 files already formatted**.
- `uv run pytest tests/presentation -q`: **10 passed** (8 before, 2 added).
- `uv run --with python-pptx python scripts/presentation/verify-venture-studio-deck.py` on the committed deck: **ALL 11 CHECKS PASSED** (exit 0).
- `uv run --with pymupdf python scripts/presentation/render-venture-studio-deck.py` on the committed deck: **ALL RENDER CHECKS PASSED** (exit 0) - cover artwork x 0.65-2.55 in y 0.55-2.09 in inside frame y 0.55-2.09, cover clear space +0.41 in, closing artwork x 3.80-6.11 in y 5.19-5.89 in, navy plate 2.9%, tagline rendered 6.35 in vs declared 6.24 in, closing clear space +0.35 in.
- `git diff --exit-code -- ai_venture_studio_client_presentation.pptx`: **exit 0** - the committed artifact is unchanged.
- Full non-e2e pytest suite (`uv run pytest --basetemp=<isolated> -q`): **2662 passed / 2 skipped / 67 deselected / 0 failed** (rc=0, 8m55s). The known side-effect file `src/data/generated/agent-registry.public.json` was restored; the before/after `git status` snapshot showed no other change.
- `pwsh scripts/maintenance/lint-ecl.ps1`: **ECL lint passed** (ps-antipattern scan 27 files, 0 failures, 0 warnings).
- `pwsh scripts/maintenance/check-index-freshness.ps1` under Windows PowerShell 5.1: **PASS**.
- CI on the PR: all required checks green, including `Deck QA (structure)` and `Deck QA (rendered pixels)`.

## Next Step

- Merge the PR, then confirm the parked HAOMTGV change is back in `harness/changes/active/`.
- Issue #484 (the flaky `/api/v1/org-chart` performance gate) is tracked separately and is the next piece of work.
