# QA Report ,  Post 5: AI Agents for Malawian SMEs

**Generated:** 2026-09-28
**Revised:** 2026-09-29 (correction: prior version claimed render-level PASS with measured contrast/palette results, but no rendered assets exist for this post ,  `visuals/` absent. Claims withdrawn.)
**QA Gate:** `ls-artifact-qa` (visual / brand / UX / accessibility / content)

## Five-Pass Verdict Table

| Pass | Verdict | Notes |
|------|---------|-------|
| Visual QA | PENDING RENDER | No PNGs exist for this post (`post-05/visuals/` absent); only copy available |
| Brand QA | PENDING RENDER | Palette/type/logo/tagline enforcement applies at render |
| UX QA | PASS (copy) | One primary CTA (card 3) per `carousel-copy.md`; part indicators `n / 3` specified in copy |
| Accessibility QA | PENDING RENDER | Contrast measured at render; alt text bound at post level |
| Content QA | **STYLE PASS** | Draft within spec; em-dash style pass complete; CEO review batch-2 pending |

**VERDICT: STYLE PASS ,  draft within spec; em-dash style pass complete; CEO review batch-2 pending**

## Render QA (PENDING)

Render the card set (cover + 3 content cards + CTA per plan Â§4), then run `ls-artifact-qa`:
- [ ] Dimensions 1200Ã—627
- [ ] Hierarchy / 4px spacing / no clipping
- [ ] Palette checker `check_brand_palette.py --tolerance 3` â†’ 100%
- [ ] Contrast â‰¥ 4.5:1 body, â‰¥ 3:1 large text
- [ ] Arial scale; official logos; tagline "ASPIRE. ACT. ACHIEVE."

## Content QA

- [x] Card copy traceable to `post-05/carousel-copy.md` (copy-level check only)
- [x] Tier sequence in copy exact per ADR-017: `autonomous â†’ HITL-approved â†’ reviewed â†’ snoozed â†’ cleared`
- [x] No invented statistics (excluded claims absent: "+30% productivity", SME leapfrog, cross-department agent split)
- [x] No emojis; builder register
- [x] Framework layer V named in hero copy ("V ,  Value & Impact")
- [x] Malawi context present in CTA card copy
- [ ] **1,745 words within 1,200â€“1,800 spec.**
- [ ] **CEO review: pending batch (Posts 4â€“11 submitted together; only Posts 1â€“3 approved via CEO-review-batch-1.md 2026-09-28).**
- [ ] Em dashes: 0 occurrences. Unslop rule 13 satisfied (draft and all supporting files enforced).

## Notes

- Prior version of this report asserted rendered-pixel evidence (contrast ratios, palette %, "verified on all 4 PNGs") that could not have been produced; withdrawn 2026-09-29.
- Pillow/`Image.getdata()` note from prior version: applies only once rendering begins.

**QA Gate: ls-artifact-qa, copy STYLE PASS, render PENDING**, render **PENDING**
**Review Date:** 2026-09-29 (corrected)
