---
name: ls-brand-advertising
description: "Specializes in commercial creative for LightSpeed Holdings: digital ads, display ads, social ads, billboards, flyers, posters, event banners, email headers, campaign graphics, product launches, and service promotions. Builds the Attention -> Problem -> Promise -> Proof -> Differentiation -> CTA persuasion arc and enforces per-platform ad dimensions automatically. Uses the official logo + brand palette and routes visual generation through k-dense-infographics / ComfyUI image generation. Trigger on: 'ad', 'banner ad', 'display ad', 'campaign creative', 'billboard', 'poster', 'flyer', 'promotion graphic'."
---

# LightSpeed Brand Advertising

Commercial creative that sells — always on-brand and always dimension-correct for its platform.

## Preconditions

1. Load `ls-design-system` — ad creative must never deviate from brand tokens or the official logo.
2. Clarify the offer: what product/service (`company/`, offers in the registry — Offer A website/branding, Offer B WhatsApp/AI chat, Offer C NGO M&E, Offer E platform licensing), the target segment, and the single conversion goal.
3. Build the persuasion arc before any visual.

## The Persuasion Arc (Mandatory)

```
Attention ──► Problem ──► Promise ──► Proof ──► Differentiation ──► CTA
```

- **Attention:** the headline hook — one line, ≤8 words, no clickbait.
- **Problem:** the pain the audience actually feels (evidence-led, not invented).
- **Promise:** the specific outcome the offer delivers.
- **Proof:** a verifiable fact, number, or client result from `results/`/registry/brief.
- **Differentiation:** why LightSpeed over alternatives (turnkey AI-native org, cost transparency, HITL governance, local Malawi/SADC presence).
- **CTA:** one action — visit, download, book, contact. Contact: Jack Mlusu, jmlusu@gmail.com, +265 (0) 980 016 004, lightspeedholdings.com when appropriate.

## Ad Formats & Dimensions (Enforce Automatically)

| Platform / Medium | Spec |
|-------------------|------|
| LinkedIn (feed) | 1200×627 |
| Instagram (feed) | 1080×1080 |
| Instagram (story) | 1080×1920 |
| Facebook (feed) | 1200×628 |
| X / Twitter | 1600×900 |
| YouTube (display) | 300×250 / 728×90 / 160×600 |
| Google Display | 300×250, 728×90, 336×280, 970×250 |
| Website hero | match site breakpoints (1200×~600) |
| Print — billboard | 12:5 or spec from brief |
| Print — flyer / poster | A4 (210×297mm) / A3; 300dpi, CMYK or vector preferred |
| Event banner | spec from venue |

## Branded Ad Anatomy

- Navy-dominant creative; logo (official asset) placed per clear-space rules; white or cyan headline; red reserved for the CTA or one accent.
- Text-safe areas respected (keep content ≥15% inset from edges for social).
- Minimal copy per ad — the ARc has 6 beats but they compress to: hook, promise+proof line, CTA.
- No generic stock-photo AI vibe; prefer brand-consistent graphics (diagrams, KPI callouts, product visuals) over random imagery.

## Visual Generation

- **Photographic / illustration assets**: Delegate to `media-generation-owner` subagent via `task` with a generation brief (dimensions per platform table, art direction reference, brand palette constraints `{navy:#070A40, red:#E63946, cyan:#00BFFF, lightGrey:#F2F2F2}`). The owner executes via ComfyUI MCP driver (`comfyui-mcp`, API-first Comfy Cloud mode — 0 local RAM). For infographic-style brand visuals: use `k-dense-infographics` then recolor to brand palette. For KPI / simple diagrams: use `ls-diagramming`. Post-generation, always run `ls-artifact-qa`.

- **Social platform profile/banner assets**: Static — see `ls-social-media-design`, reuse `static/brand/social/*` rather than regenerating.

- **Generation brief format** (passed to `media-generation-owner` via `task`):

```json
{
  "mode": "api",                         // api (default, 0 local RAM) | local (opt-in, health_check first)
  "model": "gemini-2.5-flash-image",    // nano-banana / Gemini image gen
  "prompt": "...",                       // art-direction briefed prompt
  "dimensions": "1080x1080",           // per platform table
  "brandPalette": ["#070A40", "#E63946", "#00BFFF", "#F2F2F2"],
  "clearSpace": "official logo clear-space rules",
  "outputPath": "docs/assets/campaign-2026-q3/",
  "expiresAt": "2026-12-31T23:59:59Z"
}
```

- Run `ls-artifact-qa` after generation: brand colors, logo rules, dimensions, contrast, text fit, no clipping, arc complete.

- **Never** use non-brand color grades; red reserved for accent / CTA only.

## Workflow

1. Load `ls-design-system`, restate offer/segment/goal.
2. Draft the persuasion arc in text (approve before visuals if a big campaign).
3. Generate visuals at exact platform dimensions.
4. Composite copy + logo + CTA on the creatives, respecting clear space and safe zones.
5. Run `ls-artifact-qa`: brand colors, logo rules, dimensions, contrast, text fit, no clipping.
6. Deliver: final files (by platform), the arc, copy block, and CTA tracking plan.

## QA Gates

- [ ] Dimension-exact per platform (list above)
- [ ] Logo is official asset, clear space respected
- [ ] Brand palette only; red reserved for accent/CTA
- [ ] Text within safe zones, no clipping/overflow
- [ ] Arc complete: attention→problem→promise→proof→differentiation→CTA
- [ ] Proof is a real, traceable fact
- [ ] Contrast ≥ 4.5:1 for copy
