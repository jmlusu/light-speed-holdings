# Deck Generation Navigation

Pointer: static/brand/templates/generate-pitch-deck.py --- Adapted script that converts ai_venture_studio_client_presentation.md (Part 5) into a 13-slide PPTX using brand tokens from brand/tokens/.

Branches (trigger reaching):
- ai_venture_studio_client_presentation.md is present and complete ---> run uv run python static/brand/templates/generate-pitch-deck.py
- Presentation spec ai_venture_studio_client_presentation_deck_spec.md needs review first ---> read spec, verify slide count (13), then run script
- Brand compliance check brand/guidelines/brand-guidelines.md Sec. 9 must pass ---> verify navy rail, color palette, type scale before delivery
- CTO validation: PORTFOLIO D (Consumer Platforms) must appear in Slide 4 ---> confirmed via company-registry.yaml agent roles

Leading word: generate --- when this word is invoked in a prompt, the agent reaches the pointer and the three resources above.

One source of truth: company-registry.yaml --- agent roles and KPIs (ATC >90%, velocity <60d, correction ratio, 3x capital efficiency) are the single source of truth; the deck references these but the registry is authoritative.

Cut identity: The brand tokens (navy #070A40, red #E63946, cyan #00BFFF) and compliance checklist (Sec. 9) are also defined in brand/tokens/brand-tokens.json and brand/guidelines/brand-guidelines.md; this pointer directs to the primary references only.

## Render verification (AI Venture Studio deck)

Three scripts under `scripts/presentation/` form the pipeline. Run them in order:

1. `uv run --with python-pptx python scripts/presentation/generate-ai-venture-studio-deck.py` --- writes `ai_venture_studio_client_presentation.pptx`.
2. `uv run --with python-pptx python scripts/presentation/verify-venture-studio-deck.py [deck.pptx]` --- 11 structural QA checks (geometry, palette, bounds, logo frame, text collisions).
3. `uv run --with pymupdf python scripts/presentation/render-venture-studio-deck.py [deck.pptx]` --- headless LibreOffice PDF export, then pixel probes on the cover and closing slides: navy background, logo artwork inside its frame, no `#02062F` plate behind the logo, cyan tagline present and in position, logo/tagline clear space >= 0.15 in.

`scripts/presentation/deck_geometry.py` holds the design intent (lockup placement, crop box, clear-space minimum) that all three scripts share, so the generator and the gates cannot drift apart.

Step 3 needs LibreOffice. It looks for `soffice.com` on PATH, then the default Windows install path; override with `SOFFICE`. Use `soffice.com`, not `soffice.exe` --- the `.exe` hangs when invoked non-interactively. Renders land in `qa-render/` (`qa-*.png` is gitignored); pass `--keep-pdf` to retain the intermediate PDF.

Why structural checks are not enough: LibreOffice ignores `a:srcRect` on pictures and honours `a:clrChange`. A logo placed with source-rect cropping verifies fine in `python-pptx` but renders as the full uncropped square in LibreOffice, which pushes the lockup's baked-in tagline down over "ASPIRE. ACT. ACHIEVE." Therefore:

- Never crop the logo with `a:srcRect`; pre-crop the asset (`LOGO_SRC_BOX` in `deck_geometry.py`) so the picture frame equals the visible artwork in every renderer.
- Keep the `a:clrChange` transparency effect; it is what removes the logo's `#02062F` background on the navy slide.
- Check the *rendered pixels*, not just the XML: the frame can be correct while artwork spills out of it.

## Deck QA automation (AI Venture Studio deck)

`tests/presentation/test_venture_studio_deck.py` is the regression suite for the deck:

- the generated deck passes every structural check;
- the logo is pre-cropped (no `a:srcRect`, one 880x713 asset embedded);
- the committed `ai_venture_studio_client_presentation.pptx` still matches what the generator produces (drift guard, media compared by pixels so PNG encoder differences do not fail it);
- the pre-fix geometry (square frame + `a:srcRect`), a frame that overruns the tagline, and a logo that lands on text are each rejected;
- the generator refuses a brand asset whose size does not match `LOGO_SRC_SIZE`.

Run it with `uv run pytest tests/presentation -q`.

Both gates run in CI as required checks: `Deck QA (structure)` (verifier + the pytest suite) and `Deck QA (rendered pixels)` (LibreOffice export + pixel probes). A deck edit that breaks the render therefore blocks the merge instead of shipping to a client.
