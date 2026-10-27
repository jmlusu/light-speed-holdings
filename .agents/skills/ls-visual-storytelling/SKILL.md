---
name: ls-visual-storytelling
description: "Turns information into visual communication for LightSpeed thought leadership: infographics, timelines, maps, frameworks, data stories, executive one-pagers, explainer graphics, and visual abstracts. Pipeline: message -> visual narrative (headline -> key stat -> context -> problem visualization -> comparison -> implication -> opportunity -> CTA) -> medium choice -> render (article-illustrations for Grav hand-drawn, k-dense-infographics for professional infographics, Mermaid via ls-diagramming for structures, SVG/HTML one-pagers) -> ls-artifact-qa. Always on-brand. Trigger on: 'infographic', 'one-pager', 'data story', 'explainer graphic', 'visual abstract', 'tell this visually', 'visual for a stat'."
---

# LightSpeed Visual Storytelling

Turn information into a visual argument. You are the bridge between research/figures and a memorable graphic.

## Preconditions

1. Load `ls-design-system` — brand palette and logo apply to every output.
2. Source facts first. A visual story is only as good as its numbers; pull from `results/`, `company/`, research outputs (`k-dense-literature-review`, `research`), or the `ls-creative-director` brief. Never invent statistics for a graphic.

## The Visual Narrative Template

```
Headline ──► Key statistic ──► Context ──► Problem visualization ──► Comparison
   ──► Implication ──► Strategic opportunity ──► Call to action
```

- **Headline:** the one-sentence claim the graphic proves.
- **Key statistic:** the single most compelling number, shown big.
- **Context:** the frame that makes the stat meaningful ("vs. last year", "regional baseline").
- **Problem visualization:** the pain made visual (gap, bottleneck, falling line).
- **Comparison:** before/after or LightSpeed vs. alternative.
- **Implication:** "so what" — what the pattern means.
- **Opportunity:** where the opening is.
- **CTA:** one action (download whitepaper, contact, read the article).

Not every graphic needs all eight beats — but the headline, key stat, and CTA are non-negotiable.

## Medium Choice

| Deliverable | Route | Notes |
|-------------|-------|-------|
| Hand-drawn explainer illustrations | `article-illustrations` | Grav character IP; 16:9; white bg; black line art + red/orange/blue accents |
| Professional infographic | `k-dense-infographics` | 10 types; then enforce brand palette |
| Structure diagrams / frameworks | `ls-diagramming` | Mermaid/SVG in brand palette |
| Data story / stat callout | SVG or HTML one-pager | brand tokens; big numbers, clean layout |
| Executive one-pager | `static/brand/templates/one-pager.html` | branded HTML template; fill, don't rebuild |
| Timeline / map | `ls-diagramming` (gantt/timeline) | |
| Visual abstract | `k-dense-sci-schematics` or SVG | for research/technical content |

## Multi-Platform Export Matrix

One visual argument, several crops. Decide the narrative once, then re-lay-out per platform — never scale one canvas into another, because a 1080×1080 layout squeezed to 1600×900 breaks the type scale and the safe area.

| Deliverable | Canvas (px) | Ratio | Primary target | Notes |
|-------------|-------------|-------|----------------|-------|
| Infographic — square | `1080 × 1080` | 1:1 | Instagram, LinkedIn feed | Tightest crop: one stat + headline only, ≤40 words |
| Infographic — landscape | `1600 × 900` | 16:9 | X / Twitter | Widest: supports a 3-column comparison strip |
| Infographic — landscape (FB) | `1200 × 628` | ~1.91:1 | Facebook link/share | Shortest height: drop the comparison strip |
| Carousel — LinkedIn | `1080 × 1080` cards → PDF | 1:1 per page | LinkedIn document post | Multi-page PDF, one card per page, ≤10 pages |
| Carousel — Instagram | `1080 × 1080` PNGs | 1:1 | Instagram carousel | Ordered `card-1..N.png`, 3–10 slides, first card is the hook |
| Report | A4 PDF | 1:1.41 | Email, web, print | See `ls-document-design` |

Platform rules that survive the crop:

- **Safe area:** keep all text ≥ 64px from each edge at 1080 wide (≈6%). Instagram overlays UI on the bottom ~15% of a 1:1 and the right rail on Reels; nothing load-bearing goes there.
- **Legibility at thumbnail:** a 1600×900 graphic is seen at ~400px wide in-feed. The headline must read at 25% scale, so the key stat gets ≥ 25% of canvas height.
- **One file per platform, named for the platform.** `infographic-square-1080x1080.png`, `infographic-landscape-1600x900.png`, `infographic-landscape-1200x628.png`. A file called `final-v3.png` cannot be audited.
- **Same facts, same figures, same ordering** across every size. A number that changes between the square and the landscape means one of them is wrong.

### Carousel sets (LinkedIn PDF + Instagram PNGs)

A carousel is one argument cut into slides, not six small infographics:

1. **Card 1 is the hook** — headline + one stat, no body copy. It decides whether slides 2–N are seen.
2. **One idea per card.** If a card needs two headings, it is two cards.
3. **Cards 2–(N-1) build the case** — problem, comparison, implication. Number them (`02 / 06`) so a screenshot still reads in order.
4. **Final card is the CTA** — one action, one URL.
5. **Emit both formats from one source.** Render the card set once at 1080×1080, then export the same images as a multi-page PDF for LinkedIn and as ordered PNGs for Instagram. Two separately-built sets drift.

## Brand Rules

- Infographic palette = LightSpeed tokens (navy dominant; cyan accents; red for the key number/CTA). Recolor any generated asset to brand tokens.
- Logo: official asset, clear space respected, `™` on first company mention.
- Text: Arial, sizes from brand scale; no more than 3 weights per graphic.
- Whitespace: a graphic with everything bold has no hierarchy — reserve empty space around the key figure.

## Workflow

1. Load `ls-design-system`; collect the facts with sources.
2. Draft the visual narrative (eight beats) and get it right before building.
3. Choose the medium via the table above, then choose **every platform canvas** from the Multi-Platform Export Matrix before building — retro-fitting a 16:9 layout to 1:1 costs a rebuild.
4. Build the graphic; enforce brand tokens after any generated rendering.
5. QA with `ls-artifact-qa`: hierarchy, contrast, typography, brand, accuracy.
6. Deliver: the graphic file(s) at each platform size + the headline + the source trail for the key stat + CTA text.

For campaign work driven by `/generate-all-assets`, the deterministic renderer is already built — prefer it over a fresh Pillow/HTML layout:

```bash
uv run python scripts/generate_all_assets.py --campaign artifacts/campaigns/<slug>
```

It renders the square / landscape / Facebook infographics and the LinkedIn+Instagram carousel pair from the campaign's extraction table, with every pixel on a brand token, then self-gates with `check_brand_palette.py`.

## Brand Token Enforcement (post-render)

AI-generated renders are NOT guaranteed to use LightSpeed tokens. Every `k-dense-infographics` (or external) render MUST be post-processed before it ships:

1. **Remap to the LS palette.** Recolor the render so every visible color comes from `brand/tokens/brand-tokens.json` — navy #070A40 dominant, cyan #00BFFF secondary, red #E63946 reserved for the key number / CTA, plus greys #6B7280 / #F2F2F2 / #9CA3AF and white #FFFFFF for backgrounds and supporting text.
2. **Auto-check with the deterministic gate.** Run the palette checker on the remapped render:

   ```
   uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py <image> --tolerance 3
   ```

   The checker compares every visible pixel against the exact token palette and reports the percent off-palette (default tolerance 3% for anti-aliasing/gradients). It prints one line — PASS or FAIL — and exits 0 on pass / 1 on fail. A FAIL means the remap left visible off-brand pixels: fix the render and re-check until PASS.
3. **Then submit to Brand QA.** Only after the checker passes, pass the asset to `ls-artifact-qa`; its Brand QA requires the checker green before APPROVE.

### Carve-out: article-illustrations (Grav)

`article-illustrations` (Grav hand-drawn character IP: white background, black line art, red/orange/blue accents) is an independent, intentional visual style. It is deliberately OUT OF SCOPE for public-brand palette enforcement — do not remap Grav art to LightSpeed tokens and do not run it through the palette checker. All other routes in the Medium Choice table are in scope.

## QA Gates

- [ ] Headline, key statistic, and CTA present and accurate
- [ ] Key stat has a traceable source
- [ ] Brand palette enforced (post-render for generated assets)
- [ ] Clear visual hierarchy — one dominant element, real whitespace
- [ ] Text on brand scale, legible at final size
- [ ] Logo official + clear space; `™` on first mention
- [ ] No invented numbers
- [ ] Every required platform canvas rendered at its **exact** pixel size (not a scaled derivative)
- [ ] Headline readable at 25% scale; no load-bearing text inside the platform safe area
- [ ] Carousel: card 1 is the hook, one idea per card, final card carries the CTA, page order matches file order
