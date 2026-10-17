# USE CASES Section — Media Assets Plan

Based on `docs/directives/WEBSITE TRANSFORMATION & REPOSITORY CONSOLIDATION DIRECTIVE.md` §20 MEDIA PLACEMENT STRATEGY (lines 1334-1339), the USE CASES section requires four media asset types. Below is a structured plan for each, mapping to the LightSpeed Creative Production Stack skills and enforcing brand tokens from `ls-design-system` (navy `#070A40`, red `#DC3641`, cyan `#00BFFF`, Arial type scale, 4px grid).

---

## 1. Interactive Visual Cards

**Skill/Agent:** `ls-frontend-design`

**Specific Output Format:** HTML/React component rendered in the repo-root Vite React SPA (`src/pages/use-cards.tsx` or similar). Each card is an interactive element featuring:
- Hero headline (navy, Arial display size)
- CTA button (primary: navy; secondary/accent: red)
- Supporting cyan accent line or tagline
- Lambdereal content (real stats, not lorem ipsum) pulled from `results/` or `company/`

**Key Brand Requirements (from `ls-design-system`):**
- Colors: navy `#070A40` as primary surface/card background; cyan `#00BFFF` for accent lines/links; red `#DC3641` for primary CTA emphasis
- Typography: Arial 700 for headline, Arial 400 for body; type scale respected (36/32/28/24/18/16/14/13/12 pt)
- Spacing: 4px base unit; vertical rhythm ≥64px between sections; 12-col grid, 24px gutter, 48px margin, max-width 1200px
- Logo: official asset imported from `brand/logos/`; `™` on first mention
- No AI slop: real content only, no fake testimonial photos, no dense card walls, contrast ≥4.5:1

**Technical Requirements:**
- Built with React + Tailwind 4 (per repo-root SPA pattern)
- Interactions via framer-motion: subtle fade/slide reveals on scroll (opacity + translateY ~16px, 0.4–0.6s), hover states on cards/buttons (border/bg/translate, 150ms)
- Icons from lucide-react only
- Responsive: stack at <768px, no horizontal scroll, tap targets ≥44px
- Playwright QA per `ls-artifact-qa` visual + brand + accessibility checks
- Accessible: semantic headings (h1→h2→h3 order), alt text on images, focus states, nav landmark
- Content from verified sources only (no lorem ipsum, no invented quotes)

---

## 2. Workflow Diagrams

**Skill/Agent:** `ls-diagramming`

**Specific Output Format:** Mermaid flowchart rendered to SVG/PNG. Diagrams illustrate the end-to-end process for each use case (agent hierarchy → task generation → orchestration → QA). Output includes:
- Source `.mmd` file (validated Mermaid syntax)
- Rendered SVG/PNG (preferred for web embedding)
- Optional Kroki fallback URL if mermaid-cli unavailable

**Key Brand Requirements (from `ls-design-system`):**
- Palette: navy `#070A40` for primary node fills; white/`#F2F2F2` for supporting nodes; cyan `#00BFFF` for accent/highlight edges; red `#DC3641` reserved for CTAs, warnings, or the "ask"
- Edges: dark-grey `#6B7280`; highlighted paths cyan
- Labels: Arial; node labels 12–14pt, edge labels 10–11pt
- Never embed a non-brand chart theme inside a LightSpeed artifact

**Technical Requirements:**
- Tool chosen by the tool-choice matrix (Mermaid `flowchart` for process maps; do not default everything to one tool)
- Node count ≤~15 per diagram (if more, split into multiple diagrams)
- One clear flow direction; no crossing edge "spaghetti"
- Labels readable at final display size
- Brand palette applied post-render via `k-dense-mermaid-skill` (validates syntax, renders, auto-fixes) or Kroki (`https://kroki.io/mermaid/svg/<encoded>`)
- Deliver source `.mmd`/SVG + rendered file (SVG/PNG) + a note on the chosen engine
- Brand palette enforcement: run `uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py <image> --tolerance 3` on rendered output; must PASS before delivery

---

## 3. Before/After Process Maps

**Skill/Agent:** `ls-visual-storytelling`

**Specific Output Format:** SVG comparison visual (before/after panels) or HTML one-pager. Each map contrasts the pre-Lightspeed process with the LightSpeed-enabled workflow. Structure follows the visual narrative template:
- Headline: the core claim the graphic proves
- Key statistic: the single most compelling number, shown big
- Context: the frame making the stat meaningful ("before Lightspeed" / "after Lightspeed")
- Problem visualization: the pain made visual (bottleneck, falling line)
- Comparison: before vs. after
- Implication: "so what" — what the pattern means
- Opportunity: where the opening is
- CTA: one action (e.g., "explore this use case")

**Key Brand Requirements (from `ls-design-system`):**
- Palette: navy `#070A40` dominant; cyan `#00BFFF` secondary accents; red `#DC3641` reserved for the key number/CTA; greys `#6B7280` / `#F2F2F2` / `#9CA3AF` for supporting text; white `#FFFFFF` for backgrounds
- Type: Arial, sizes from the brand scale; no more than 3 text weights per graphic
- Whitespace: deliberate negative space around the key figure; a graphic with everything bold has no hierarchy
- Logo: official asset, clear space respected, `™` on first company mention
- Tagline: "ASPIRE. ACT. ACHIEVE." correct

**Technical Requirements:**
- Brand palette enforcement: AI-generated renders are NOT guaranteed to use LightSpeed tokens. Every render MUST be post-processed:
  1. Remap to the LS palette so every visible color comes from `brand/tokens/brand-tokens.json`
  2. Run the palette checker: `uv run python .agents/skills/ls-visual-storytelling/scripts/check_brand_palette.py <image> --tolerance 3` — must PASS (exits 0) before submission
  3. Then submit to `ls-artifact-qa`; Brand QA requires the palette checker green before APPROVE
- Two-panel layout (before | after) with consistent sizing
- Source facts traced to `company/`, `results/`, or research outputs — never invented statistics
- QA with `ls-artifact-qa` checklist: hierarchy, contrast, typography, brand, accuracy
- Deliver: the graphic file(s) + the headline + the source trail for the key stat + CTA text

---

## 4. Evidence/Status Indicators

**Skill/Agent:** `ls-presentation-design`

**Specific Output Format:** KPI-style status badges / indicator components (HTML/CSS or PPTX-adaptable). Each indicator shows the status/evidence tier for a use case (e.g., "Validated", "Pilot", "Theoretical") with associated metrics. Format follows the presentation design system KPI card pattern:
- Light-grey rounded rect (`#F2F2F2`)
- Big navy figure (`#070A40`)
- Dark-grey label (`#6B7280`)
- One primary action or metric per badge

**Key Brand Requirements (from `ls-design-system`):**
- Palette: navy `#070A40` dominant figure; cyan `#00BFFF` accent highlights; red `#DC3641` for flags/alerts; greys `#6B7280` / `#F2F2F2` / `#9CA3AF`; white `#FFFFFF` background
- Typography: Arial scale (KPI card label: dark-grey `#6B7280`, 12pt; big figure from brand scale)
- Layout: KPI card pattern — light-grey rounded rect, big navy figure, dark-grey label (per `generate-pitch-deck.py` traction slide)
- Red accent (`#DC3641`) used sparingly for CTA or warning state within the badge
- One idea per badge; ≤6 metrics/badge (adapted from deck slide rules)

**Technical Requirements:**
- If HTML/CSS: built as reusable component in the Vite React SPA, styled with Tailwind 4 + brand tokens (`--ls-navy: #070A40`, `--ls-red: #DC3641`, `--ls-cyan: #00BFFF`, `--ls-grey-light: #F2F2F2`)
- If PPTX: generated via `static/brand/templates/generate-pitch-deck.py` pattern or fill `static/brand/templates/pitch-deck.pptx` while preserving layout
- Data traced to `company/` or `results/` — no invented statistics
- Brand palette enforced: all colors resolve to `brand-tokens.json` values only
- QA with `ls-artifact-qa` before delivery: visual + brand + UX + accessibility + content passes
- Accessible: color not the only signal (patterns/labels accompany color); contrast ≥4.5:1 for body text
- Speaker notes analog: each badge has a brief caption explaining the status tier and supporting metric

---
