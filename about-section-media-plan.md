# About Section Media Assets Plan

Based on the MEDIA PLACEMENT STRATEGY (Directive §20) and MEDIA ARCHITECTURE (Directive §19), the About section requires three specific media assets. This plan maps each asset to the appropriate LightSpeed skill, specifies output format, brand requirements, and technical requirements.

---

## 1. Human Leadership

| Item | Detail |
|------|--------|
| **Skill/Agent** | `ls-creative-director` — orchestrates leadership imagery production per Type J (Human/Leadership Imagery) |
| **Output Format** | High-resolution photographic images in WebP format (primary), with JPEG fallback; responsive sizes at 400w, 800w, 1200w, 1600w, 2000w |
| **Key Brand Requirements** (from ls-design-system) | - Color palette: Navy #070A40 dominant, red #DC3641 and cyan #00BFFF as accents <br> - Typography: Arial type scale (body 16pt/14pt, headings from scale) <br> - Spacing: 4px base grid <br> - Logo rules: Official logo asset only, never recreated; clear space 1× "L" height on all sides <br> - `™` on first mention of "LightSpeed Holdings Limited™" <br> - Tagline: "ASPIRE. ACT. ACHIEVE." spelled exactly <br> - Color rule: 80/10/10 navy/red/cyan on brand-dominant surfaces |
| **Technical Requirements** | - Model releases for all individuals photographed <br> - Consistent lighting, composition, and crop across all leadership images <br> - African context visible (office, Lilongwe backdrop) per Type J spec <br> - High DPI for print/digital <br> - Alt text describing leadership context (not generic "person") <br> - Images optimized via SVGO/imagensmart per pipeline <br> - Referenced in `data/media/registry.ts` and manifest <br> - Lazy-loaded on About page <br> - Meets performance budget: hero images ≤150 KB at 1920×1080 |

---

## 2. Malawi / Africa Context

| Item | Detail |
|------|--------|
| **Skill/Agent** | `ls-visual-storytelling` — produces map/hero imagery per Type A (Hero Imagery) and Type H (African Maps) |
| **Output Format** | SVG map diagram (primary) for scalability and brand compliance, with WebP hero imagery fallback; responsive vector format |
| **Key Brand Requirements** (from ls-design-system) | - Color palette: Navy #070A40 as dominant container color, cyan #00BFFF for connection lines, red #DC3641 for key accents <br> - Typography: Arial type scale for all labels and region names <br> - Spacing: 4px base grid; 12-column grid layout where applicable <br> - Logo rules: Official logo asset if included; clear space respected <br> - Color rule: Avoid standard choropleth defaults; use brand palette exclusively <br> - No fabricated scenes or misleading implications (honesty principle) |
| **Technical Requirements** | - SVG format with brand colors applied via currentColor or inline CSS <br> - Correct geographic progression: Malawi → SADC (16 member states) → Africa (54 countries) per Type H spec <br> - Do not imply operational presence in every country — show conceptual progression <br> - Avoid stereotypes: show modern infrastructure, not dirt roads/power lines as failure <br> - Accessible: descriptive alt text with text-based list alternative <br> - Responsive: scales from favicon size to full-page display <br> - Brand palette enforcement: post-render checker run via `uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py <image> --tolerance 3` <br> - Manifest entry in `public/assets/diagrams/maps/` with alt, width, height, placement, attribution |

---

## 3. Operating Philosophy

| Item | Detail |
|------|--------|
| **Skill/Agent** | `ls-diagramming` — creates conceptual diagram of operating philosophy as a strategy/framework diagram |
| **Output Format** | SVG diagram (vector, brand-colored) — per ls-diagramming style: consistent line weight (2px), rounded rect nodes (8px radius), dark/light mode compatible |
| **Key Brand Requirements** (from ls-design-system) | - Color palette: Navy #070A40 dominant, cyan #00BFFF secondary accents, red #DC3641 reserved for key number/CTA <br> - Typography: Arial type scale; sizes from brand scale (title-xl 32pt through caption 12pt) <br> - Spacing: 4px base scale (4/8/12/16/24/32/48/64/96); consistent node spacing <br> - Logo rules: Official logo asset if featured; `™` on first company mention <br> - Whitespace: reserve empty space around key figure/element <br> - Maximum 3 weights per graphic <br> - Editorial diagram style (not flowchart software default) |
| **Technical Requirements** | - SVG/HTML format (not raster) for crispness and accessibility <br> - Consistent line weight (2px) and node style (rounded rect, 8px radius) <br> - Annotation layer for key metrics/philosophy principles <br> - Dark/light mode compatible <br> - Brand palette enforcement: post-render palette checker must PASS <br> - Accessible: data table alternative for any encoded data <br> - Long description via `<figcaption>` or linked accessible version <br> - Manifest entry in `public/assets/diagrams/architecture/` <br> - responsive: inherits grid from parent container <br> - Meets accessibility contrast ratios per WCAG AA |

---

## Production Pipeline Reference

All three assets follow the standard LightSpeed asset pipeline:

```
Source (Figma/SVG/Photo/Code)
    ↓
Optimize (SVGO, imagemin, sharp)
    ↓
Generate Variants
    - WebP (primary for photos)
    - AVIF (modern)
    - SVG (diagrams, icons)
    - PNG fallback
    ↓
Responsive Sizes
    - 400w, 800w, 1200w, 1600w, 2000w
    ↓
Manifest Entry (data/media/registry.ts + public/assets/manifest.json)
    ↓
Deploy to public/assets/{type}/
    ↓
Reference in components from registry
```

All assets undergo `ls-artifact-qa` final gate before delivery, checking: visual hierarchy, brand palette, typography, accessibility, and content accuracy.

---

**Governance**: Per the Media Review Checklist, all assets must be: on-brand (colors, typography, tone), honest (no fabricated scenes), accessible (alt text, contrast, reduced motion), performant (optimized, responsive, lazy-loaded), strategically placed (per placement strategy), attributed (source, license, creator), and versioned (in manifest, git-tracked for SVGs).
