---
title: "Deck QA automation: enforce deck gates in CI and add regression tests"
slug: "deck-qa-automation-enforce-deck-gates-in-ci-and-add-regression-tests"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: ["scripts/presentation", "tests/presentation", ".github/workflows"]
files:
  - "scripts/presentation/deck_geometry.py"
  - "scripts/presentation/generate-ai-venture-studio-deck.py"
  - "scripts/presentation/verify-venture-studio-deck.py"
  - "scripts/presentation/render-venture-studio-deck.py"
  - "tests/presentation/conftest.py"
  - "tests/presentation/test_venture_studio_deck.py"
  - ".github/workflows/ci.yml"
  - "docs/deck-generation.md"
  - "docs/STATUS.md"
  - "CHANGELOG.md"
tags: ["presentation", "qa", "ci"]
validation_status: "pass"
created_at: "2026-10-20"
updated_at: "2026-10-20"
session_id: "65b6d19b-96b4-4356-8907-6e5b4ab6a6d8"
owner_agent: "jmlus"
claimed_at: "2026-10-20"
---

# Summary

## Outcome

The AI Venture Studio client deck is now policed like the generated code it is. A read-only audit of PR #480 found that both deck gates were manual-only, that no regression test guarded the logo-over-tagline defect, and that the same design constants were hardcoded in three files; this change closes those gaps.

Delivered:

- `scripts/presentation/deck_geometry.py` - one source of truth for the lockup placement, the logo crop box and source size, and the `MIN_GAP_IN` clear-space invariant, shared by the generator, the structural verifier and the rendered-pixel gate.
- The generator now places both lockups from that module, refuses a brand asset whose size is not `LOGO_SRC_SIZE` (1254x1254) instead of cropping blindly, and re-cuts its cached crop whenever the source asset is newer, so a replaced logo cannot ship from a stale crop. The cached file keeps a stable name because it becomes the picture's description in the deck.
- The verifier asserts the exact shared placement of both lockups instead of loose "top-left / lower half" heuristics.
- The render gate gained a cover probe (the cover lockup was never pixel-checked) and measures clearance against the declared tagline top edge, so font substitution on CI cannot mask a real overlap; it also checks that the rendered cyan tagline sits where it was declared.
- `tests/presentation/` - 8 regression tests, including the pre-fix defect geometry, a frame that overruns the tagline, a logo that lands on text, and a drift guard that the committed deck is still the one the generator produces (media compared by pixels).
- CI: `Deck QA (structure)` and `Deck QA (rendered pixels)` (headless LibreOffice), both wired into the `CI Gate` aggregate, so a deck regression blocks the merge.

The rebuilt deck is byte-identical to the committed artifact, so the deck itself did not change.

## Decisions

- Shared geometry module rather than duplicating constants: the audit showed the same numbers hardcoded in three files, which is how a gate ends up asserting stale expectations.
- Stable crop cache file name plus a re-cut on a newer source, instead of a hash- or mtime-keyed name: the name lands in the deck as the picture's description, so a machine-specific name would make the artifact differ between machines and break the drift guard.
- Clearance measured against the declared tagline top edge, not the rendered glyph ascent: CI substitutes Arial with a metric-compatible font, and the invariant is layout, not font metrics.
- Both deck jobs live in `ci.yml` and join the `CI Gate` aggregate rather than a separate workflow: a separate workflow would not be a merge blocker.
- PyMuPDF stays an ad-hoc `uv run --with` overlay instead of a dev dependency: it pulls numpy and onnxruntime, and adding it would churn `uv.lock` for a job that needs it once.
- The unrelated `haomtgv-blueprint-hero-and-page-wiring` change was parked with the harness script to free the single active slot, and resumed after this change closed.

## Validation

- `ruff check` on the six touched files: **All checks passed!**; `ruff format --check`: **6 files already formatted**.
- `uv run pytest tests/presentation -q`: **8 passed**.
- `uv run --with python-pptx python scripts/presentation/verify-venture-studio-deck.py` on the rebuilt deck: **ALL 11 CHECKS PASSED** (exit 0).
- `uv run --with pymupdf python scripts/presentation/render-venture-studio-deck.py` on the rebuilt deck: **ALL RENDER CHECKS PASSED** (exit 0) - cover artwork x 0.65-2.55 in y 0.55-2.09 in inside frame y 0.55-2.09, cover clear space +0.41 in, closing artwork x 3.80-6.11 in y 5.19-5.89 in inside frame y 3.95-5.89, navy plate 2.9%, tagline rendered 6.35 in vs declared 6.24 in, closing clear space +0.35 in.
- Negative control, the pre-fix deck: verifier **2/11 CHECKS FAILED** (exit 1) and render gate **3 RENDER CHECK(S) FAILED** (exit 1) - cover artwork x 0.51-2.69 in y 0.40-2.23 in overflows frame y 0.55-2.09, closing artwork y 5.50-6.21 in overflows frame y 3.95-5.89, clear space +0.03 in.
- `pwsh scripts/maintenance/lint-ecl.ps1`: **ECL lint passed** (ps-antipattern scan 27 files, 0 failures, 0 warnings).
- Full non-e2e pytest suite (`uv run pytest --basetemp=<isolated> -q`): **2660 passed / 2 skipped / 67 deselected / 0 failed** (rc=0, 8m23s). The known side-effect file `src/data/generated/agent-registry.public.json` was restored before archive; the before/after `git status` snapshot showed no other change.
- CI on the PR: `Deck QA (structure)` and `Deck QA (rendered pixels)` green, all required checks green.

## Next Step

- Merge the PR, then confirm the parked HAOMTGV change is back in `harness/changes/active/`.
