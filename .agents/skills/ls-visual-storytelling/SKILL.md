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

## Brand Rules

- Infographic palette = LightSpeed tokens (navy dominant; cyan accents; red for the key number/CTA). Recolor any generated asset to brand tokens.
- Logo: official asset, clear space respected, `™` on first company mention.
- Text: Arial, sizes from brand scale; no more than 3 weights per graphic.
- Whitespace: a graphic with everything bold has no hierarchy — reserve empty space around the key figure.

## Workflow

1. Load `ls-design-system`; collect the facts with sources.
2. Draft the visual narrative (eight beats) and get it right before building.
3. Choose the medium via the table above.
4. Build the graphic; enforce brand tokens after any generated rendering.
5. QA with `ls-artifact-qa`: hierarchy, contrast, typography, brand, accuracy.
6. Deliver: the graphic file(s) + the headline + the source trail for the key stat + CTA text.

## QA Gates

- [ ] Headline, key statistic, and CTA present and accurate
- [ ] Key stat has a traceable source
- [ ] Brand palette enforced (post-render for generated assets)
- [ ] Clear visual hierarchy — one dominant element, real whitespace
- [ ] Text on brand scale, legible at final size
- [ ] Logo official + clear space; `™` on first mention
- [ ] No invented numbers
