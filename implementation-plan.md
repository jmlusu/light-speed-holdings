# Implementation Plan: LinkedIn Series Visuals for Posts 1-4

## Overview

Create/regenerate PNG visuals (1200x627) for the Pharos LinkedIn series posts 1-4, ensuring each card renders the correct content from `carousel-copy.md` with proper brand palette adherence.

## Current State Assessment

| Post | Visual Status | Files | Content Status |
|------|--------------|-------|----------------|
| **1** | ✅ Generated with content | hero + carousel-1/2/3 | QA-approved 2026-09-28 |
| **2** | ✅ Generated with content | hero + carousel-1/2/3 | QA-approved 2026-09-28 |
| **3** | ✅ Generated with content | hero + carousel-1/2/3 | QA-approved 2026-09-28 |
| **4** | ❌ Blank (solid dark grey) | hero + carousel-1/2/3/4/5 | Needs regeneration |

**Key Finding**: Posts 1-3 visuals actually contain rendered text and UI elements using the full brand palette (cyan `#00bfff`, white `#ffffff`, red `#dc3641`, navy `#070a40`, grey `#6b7280`). The dominant navy background may have created the impression of "blankness." Post 4's visuals are truly blank - all pixels are `#14141e` (dark grey), meaning the generator failed to render any card content.

## Root Cause

The generator script `static/brand/templates/generate-linkedin-series-visuals.py` has two limitations:

1. **Only 3 posts defined** (POSTS list has exactly 3 items for posts 1-3)
2. **Only 3 carousel cards per post** (build_cover, build_content_card, build_cta_card), but posts 4+ have 5 cards
3. **Post 4's 5-card structure** (framework overview + 4 detail cards + CTA) is not supported by the builder functions

## Implementation Plan

### Phase 1: Fix Generator Script for Post 4

**Objective**: Extend the generator to support post 4's 5-card structure and add remaining posts.

**Changes needed to `generate-linkedin-series-visuals.py`**:

1. **Expand POSTS array** to include posts 4-11 with their layer, title, stat, and card definitions
2. **Add build_frame_card() function** for cards 4 and 5 (framework explanation cards)
3. **Modify generate()** to produce 5 carousel cards per post instead of 3
4. **Update out_dir() and asset mapping** to handle 5 cards

**Post 4 Data Structure** (from `carousel-copy.md`):
- Layer: T (Orchestration & Organization) - or could be G or V depending on thematic fit
- Cover card: "H-A-O-M-T-G-V: One System" - the framework overview
- Card 2: "H: Human Purpose & Authority"
- Card 3: "A: Agentic Workforce"
- Card 4: "O: Orchestration"
- Card 5: CTA "Download the Monitor"

### Phase 2: Regenerate Visuals for Posts 1-4

**Objective**: Ensure all 4 posts have properly rendered visuals.

**Steps**:
1. Run `python static/brand/templates/generate-linkedin-series-visuals.py`
2. Verify output with `--verify` flag
3. Check all 4 posts have 6 files each (hero + 5 carousel cards)
4. Confirm brand palette compliance (0% off-palette)

### Phase 3: Verify QA Compliance

**Objective**: Ensure visuals pass the `ls-artifact-qa` gate.

**Checks**:
- Dimensions: 1200x627 per LinkedIn spec
- Brand palette: 100% on-palette (0% off-palette)
- Hierarchy: one dominant element per card
- Spacing: 4px base grid, 64px content inset
- No clipped text or overflow
- official logos and tagline "ASPIRE. ACT. ACHIEVE."
- Accessibility contrast ratios met

### Phase 4: Document Process for Posts 5-11 (Future Work)

**Objective**: Establish pattern for remaining posts.

**Notes**:
- Posts 5-11 follow similar 5-card pattern
- Each post maps to one of the three pillars: Company Builder, Use Cases, Policy
- Content exists in `carousel-copy.md` for all posts
- Generator needs periodic extension as new posts are added

## Success Criteria

- [ ] All 4 posts (1-4) have 6 PNG files each in `visuals/` directory
- [ ] All images are 1200x627 pixels (LinkedIn carousel spec)
- [ ] 100% brand palette compliance (verified via `check_brand_palette.py`)
- [ ] QA report verdict: APPROVE for all 4 posts
- [ ] Card copy traceable to `carousel-copy.md` verified visually
- [ ] No invented statistics or emojis in rendered text

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Font Arial not found on server | Rendering failure | Ensure `arial.ttf`/`arialbd.ttf` available; set `WINDIR` env var |
| Palette mismatch after generation | QA failure | Run `snap_to_palette()` on all outputs; verify with `check_brand_palette.py` |
| Card text overflow max lines exceeded | Cropped/ugly visuals | Increase max_lines parameter or truncate copy in `carousel-copy.md` |
| Generator crashes on certain card content | Partial visuals | Add try/except per card; fall back to text-only placeholder |

## Rollback Plan

If visuals fail QA after generation:
1. Restore previous visuals from git: `git checkout main -- docs/pharos/linkedin-series/post-XX/visuals/`
2. Debug the specific card causing issues
3. Fix generator script parameters (font sizes, line widths, colors)
4. Re-run generation
5. Re-QA before marking complete

## Timeline

- **Day 1**: Extend generator script for post 4 + 5 cards
- **Day 2**: Regenerate visuals for posts 1-4
- **Day 3**: Verify brand palette compliance
- **Day 4**: Run ls-artifact-qa visual QA gate
- **Day 5**: Sign-off and document for posts 5-11
