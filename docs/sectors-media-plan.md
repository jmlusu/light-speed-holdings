# SECTORS Section Media Assets Plan

Based on the MEDIA PLACEMENT STRATEGY (Directive §20) and LightSpeed brand guidelines (ls-design-system), the following plan specifies the skills, formats, and brand/technical requirements for each of the three media asset categories in the SECTORS section.

---

## 1. Sector-Specific Imagery

| Attribute | Specification |
|-----------|---------------|
| **Skill / Agent** | `ls-frontend-design` — builds distinctive, on-brand LightSpeed websites and landing pages. Enforces the design system (navy/red/cyan, Arial type scale, 4px grid) and targets the repo-root Vite React SPA framework. |
| **Output Format** | HTML/CSS React component (or PNG/SVG asset) embedded in the SECTORS page layout. The imagery should be a visual hero/background element reflecting each sector's theme, designed as part of the Vite SPA page structure (`src/pages/SectorsPage.tsx` or equivalent). |
| **Key Brand Requirements** (from `ls-design-system`):<br>- **Navy #070A40** as primary surface/background color<br>- **Red #DC3641** as accent color for highlights/CTAs<br>- **Cyan #00BFFF** as secondary accent (links on dark, taglines)<br>- **Arial type scale** (display/headings: Arial 700; body: Arial 400)<br>- **4px grid/base unit** for all spacing and layout decisions<br>- Logo rules: official logo asset with clear space respected; `™` on first company mention<br>- 80/10/10 color distribution: ~80% navy, 10% red, 10% cyan on brand-dominant surfaces | |
| **Technical Requirements**<br>- Built within the repo-root Vite React SPA framework (React + Tailwind 4 + framer-motion + lucide + recharts)<br>- Responsive across breakpoints (stack at <768px, no horizontal scroll)<br>- Accessible: semantic HTML, alt text on all imagery, focus states, nav landmark<br>- Consistent spacing scale — no arbitrary margins (4px base, scale: 4/8/12/16/24/32/48/64/96)<br>- Contrast ≥ 4.5:1 for any overlaid text (navy on white passes; verify colored-on-color)<br>- Brand palette only — no off-palette colors, no invented type sizes<br>- Logo imported from `brand/logos/` (canonical); reference tokens via `brand/tokens/brand-tokens.css`<br>- Run through `ls-artifact-qa` visual + brand + accessibility checks before delivery<br>- No "AI slop" patterns: no rainbow gradients, dense meaningless cards, fake avatars, or invented quotes | |

---

## 2. Sector Data Visualizations

| Attribute | Specification |
|-----------|---------------|
| **Skill / Agent** | `ls-diagramming` — the LightSpeed diagram engine that produces technical, business, and strategy diagrams in the brand palette. Triggers on 'diagram', 'architecture diagram', 'flowchart', 'process map', '2x2', 'pipeline', 'data flow'. |
| **Output Format** | Rendered SVG or PNG data visualization/chart. Prefer SVG for scalability; PNG raster at ≥2× resolution for print if needed. Mermaid `flowchart` or `gantt`/`timeline` per diagram type (per the tool-choice matrix). |
| **Key Brand Requirements** (from `ls-design-system`):<br>- **Navy #070A40** for primary nodes/areas/fills<br>- **Red #DC3641** reserved for CTAs, warnings, the "ask", or accent highlights<br>- **Cyan #00BFFF** for accent/highlight elements (shield base, links on dark, taglines on navy)<br>- **Arial type scale** for labels: node labels 12–14pt, edge labels 10–11pt<br>- **4px grid/base unit** for spacing between diagram elements<br>- **Brand palette enforcement**: navy dominant; cyan accents; red reserved for key number/CTA; greys #6B7280 / #F2F2F2 / #9CA3AF for supporting text/backgrounds; white #FFFFFF for backgrounds<br>- Never embed a non-brand chart theme inside a LightSpeed artifact | |
| **Technical Requirements**<br>- Tool chosen by the Mermaid/Kroki matrix, not habit (see ls-diagramming tool-choice matrix)<br>- Node count fits the diagram's intent (≤~15 for architecture diagrams; more implies splitting)<br>- One clear flow direction; no crossing "edge spaghetti"<br>- Labels readable at final display size<br>- Brand palette applied via `k-dense-mermaid-skill` (validates syntax, renders, auto-fixes) or hand-built custom SVG with brand colors<br>- If Mermaid is too rigid (e.g., 2×2 strategy frameworks), hand-write custom SVG with brand palette<br>- Render SVG → PNG at ≥2× resolution for print if needed<br>- Deliver source (.mmd/SVG) + rendered file (SVG/PNG) + a note on the chosen engine<br>- Run through `ls-artifact-qa` brand QA before delivery<br>- KPI cards style: light-grey rounded rects, big navy figure, dark-grey label (per ls-presentation-design) | |

---

## 3. Relevant Use-Case Illustrations

| Attribute | Specification |
|-----------|---------------|
| **Skill / Agent** | `ls-visual-storytelling` — turns information into visual communication for LightSpeed thought leadership. Pipeline: message → visual narrative (headline → key stat → context → problem visualization → comparison → implication → opportunity → CTA) → medium choice → render → `ls-artifact-qa`. Triggers on 'infographic', 'one-pager', 'data story', 'explainer graphic', 'visual abstract', 'tell this visually'. |
| **Output Format** | SVG/HTML one-pager or professional infographic. Per the visual storytelling medium choice table: "Data story / stat callout" → SVG or HTML one-pager with brand tokens; or "Executive one-pager" → `static/brand/templates/one-pager.html` (branded HTML template, fill not rebuild). |
| **Key Brand Requirements** (from `ls-design-system`):<br>- **Navy #070A40** dominant palette<br>- **Cyan #00BFFF** secondary accent<br>- **Red #DC3641** reserved for the key number / CTA<br>- **Arial type scale** (sizes from brand scale: 36/32/28/24/18/16/14/13/12); no more than 3 weights per graphic<br>- **4px grid** for spacing and visual hierarchy<br>- **Visual narrative template**: headline, key statistic, context, problem visualization, comparison, implication, opportunity, CTA (headline, key stat, and CTA are non-negotiable)<br>- Logo: official asset, clear space respected, `™` on first company mention<br>- Whitespace: reserve empty space around the key figure; a graphic with everything bold has no hierarchy | |
| **Technical Requirements**<br>- Load `ls-design-system` first — brand palette and logo apply to every output<br>- Source facts first: pull key statistics from `results/`, `company/`, or research outputs (`k-dense-literature-review`, `research`); never invent statistics<br>- Draft the visual narrative (eight beats) and get it right before building<br>- Choose the medium via the table in ls-visual-storytelling (prefer SVG/HTML one-pager for web delivery)<br>- Build the graphic; enforce brand tokens after any generated rendering<br>- **Post-render brand enforcement**: remap to LS palette so every visible color comes from `brand/tokens/brand-tokens.json` — run `uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py <image> --tolerance 3`; must PASS before submission<br>- Then submit to `ls-artifact-qa`; Brand QA requires the palette checker green before APPROVE<br>- Deliver: the graphic file(s) + the headline + the source trail for the key stat + CTA text<br>- Non-negotiable: headline, key statistic (with traceable source), and CTA present and accurate<br>- No invented numbers; all facts grounded in evidence | |

---

## Cross-Cutting Directives (Applicable to All Three Items)

1. **`ls-design-system` MUST be loaded first** before any creative production work for all three asset categories. This is the canonical source of truth for brand tokens, typography, and spacing.

2. **All artifacts must be handed off to `ls-artifact-qa`** as the final gate before delivery. The QA checklist covers: visual QA (spacing, hierarchy, balance, contrast, whitespace, alignment), brand QA (colors, type, logo, tagline), UX QA (CTA clarity, overflow, navigation, responsiveness, mobile), and content QA (claims, citations, consistency, grammar, numbers).

3. **No off-palette colors** — every visible color must resolve to `brand-tokens.json` values only. AI-generated renders are NOT guaranteed to use LightSpeed tokens and must be post-processed and checker-verified before shipping.

4. **Logo rules** — always use official files from `brand/logo/` (canonical); never recreate, stretch, rotate, distort, or recolor the logo. Clear space = 1× "L" height on all sides.

5. **Tagline** — spelled exactly: **ASPIRE. ACT. ACHIEVE.** with `™` on first company mention.

6. **Type** — Arial only; sizes from the brand scale; do not invent sizes outside the scale (display/headings: 700; body: 400).

7. **Spacing** — base unit 4px; scale: 4/8/12/16/24/32/48/64/96. Web: 12-col grid, 24px gutter, 48px margin, max width 1200px. Slides: 10in × 7.5in; navy left rail 0.15in on content slides.

8. **Article-illustrations (Grav)** — deliberately OUT OF SCOPE for public-brand palette enforcement. Do not remap Grav art to LightSpeed tokens and do not run it through the palette checker. All other routes in the visual storytelling medium choice table ARE in scope.

---

*Plan generated per Directive §20 (MEDIA PLACEMENT STRATEGY) and the LightSpeed brand design system (ls-design-system SKILL.md).*
