# Media Placement Strategy - Implementation Plan

Based on the MEDIA PLACEMENT STRATEGY directive and the LightSpeed creative production stack, this plan outlines the agents, skills, and outputs required for each section.

## Implementation Pipeline

All assets follow the LightSpeed creative production stack pipeline:

1. **ls-design-system** loaded first (brand tokens: navy #070A40, red #DC3641, cyan #00BFFF, Arial type scale, 4px grid)
2. **Production skill** creates the asset
3. **ls-artifact-qa** final gate (Visual QA, Brand QA, UX QA, Accessibility QA, Content QA)
4. **APPROVE** or **FIX → RENDER AGAIN → RE‑APPROVE**

---

## HOME Section

| # | Media Item | Skill/Agent | Output Format | Key Brand Requirements | Technical Requirements |
|---|-----------|------------|--------------|----------------------|----------------------|
| 1 | Hero | `ls-frontend-design` | Website hero section (HTML/React) | Navy dominant, cyan accent, red CTA, Arial scale, 4px grid | Vite React SPA, Tailwind 4, responsive (1200×~600), no AI slop, real content |
| 2 | H-A-O-M-T-G-V diagram | `ls-diagramming` | Mermaid SVG (Kroki rendered) | Navy primary, cyan/red accents, Arial labels, 4px grid | Mermaid flowchart, ≤15 nodes, brand palette enforced |
| 3 | AI Company Builder architecture | `ls-diagramming` | Architecture flowchart SVG | Navy dominant, show 5 layers, brand colors | `flowchart TD`, Registry→Generator→Output→Runtime→Governance |
| 4 | Africa AI economics | `ls-visual-storytelling` | Infographic SVG/HTML | Navy dominant, key stats, CTA, brand palette | Visual narrative template, sourced from results/ |
| 5 | Use Case thumbnails | `ls-frontend-design` | Image thumbnails (PNG) | Navy/red/cyan accents, consistent sizing | 16:9, ≤200KB, responsive, alt text |
| 6 | Pharos research visual | `ls-diagramming` | Research diagram SVG | Navy/red/cyan, citation-friendly | Show research findings, brand palette, traceable sources |

---

## WHAT WE DO Section

| # | Media Item | Skill/Agent | Output Format | Key Brand Requirements | Technical Requirements |
|---|-----------|------------|--------------|----------------------|----------------------|
| 1 | Process diagram | `ls-diagramming` | Mermaid flowchart SVG | Navy/red/cyan workflow steps, Arial labels | `flowchart TD`, ≤15 steps, brand palette |
| 2 | Engagement model | `ls-visual-storytelling` | Visual narrative SVG | Headline→key stat→CTA flow, brand palette | Eight-beat visual narrative template |
| 3 | Capability illustrations | `ls-diagramming` | Multi-diagram SVG set | Navy dominant, capability icons in brand colors | Individual diagrams per capability, 4px grid |

---

## AI COMPANY BUILDER Section

| # | Media Item | Skill/Agent | Output Format | Key Brand Requirements | Technical Requirements |
|---|-----------|------------|--------------|----------------------|----------------------|
| 1 | Org chart | `ls-diagramming` | Interactive org chart SVG | Navy shapes, red reporting lines, cyan subordination, Arial labels | Hierarchical layout, 4px grid spacing, hover details |
| 2 | H-A-O-M-T-G-V diagram | `ls-diagramming` | Acronym breakdown diagram SVG | Each letter defined, color-coded sections, interactive tooltips | Acronym definitions, brand palette throughout |
| 3 | Workflow animation | `ls-frontend-design` | Framer-motion HTML animation | Navy bg, red active steps, cyan completed, Arial labels | Sequential animation, play/pause controls, keyboard nav, responsive |
| 4 | Model routing | `ls-frontend-design` | Dashboard component (React) | Navy sidebar, red model selection, cyan categories, Arial scale | Model routing visualization, performance metrics, fallback logic, toggle rules |
| 5 | Governance architecture | `ls-presentation-design` | PPTX slide (10×7.5in) | Navy left rail (0.15in), red accent callouts, cyan highlights, Arial slide scale | Three-column: People/Processes/Technology, speaker notes, PDF export |
| 6 | Audit trail visualization | `ls-artifact-qa` | Interactive HTML dashboard | Navy panels, red violations, cyan verified items, Arial timestamps | Timeline view, filterable by actor/action/type, color-coding, QA markers, JSON export |

---

## SOLUTIONS Section (6 Solutions)

| Solution | Skill | Output | Key Brand | Technical |
|----------|-------|--------|-----------|----------|
| AI Company Builder | `ls-diagramming` | Inline Mermaid SVG via Kroki | Navy `#070A40`, cyan `#00BFFF`, Arial 12–14pt | `flowchart` TD, ≤15 nodes, audit trail flow |
| Digital Presence | `ls-diagramming` | Inline Mermaid SVG via Kroki | Navy `#070A40`, grey-light `#F2F2F2`, cyan accent | `flowchart`/`journey`, payment integration pipeline |
| Business Automation | `ls-diagramming` | Inline Mermaid SVG via Kroki | Navy `#070A40`, cyan paths, red CTA | `flowchart`, WhatsApp + document pipeline |
| Enterprise Deployment | `ls-diagramming` | Inline Mermaid SVG via Kroki | Navy `#070A40`, cyan RBAC, red 4 gates | `flowchart` TD with governance subgraphs |
| Boardroom Briefing | `ls-diagramming` | Inline Mermaid SVG via Kroki | Navy, cyan accents, 2×2 framework style | `flowchart` or custom SVG, executive narrative |
| Governance Solution | `ls-diagramming` | Inline Mermaid SVG via Kroki | Navy, red gates, cyan audit highlights | `flowchart` TD, 5-tier matrix + 4 gates |

**Common**: No `src` field — `ContentMedia` carries only `kind`, `alt`, `tone`. Alt format: `"[Diagram type] showing [key relationships/entities]"`. Brand palette enforced via `ls-design-system`. Inline SVG rendering — no image files.

**Execution Flow**: `ls-diagramming` generates Mermaid `.mmd` → `k-dense-mermaid-skill` validates + renders via Kroki (`https://kroki.io/mermaid/svg/<encoded>`) → Inline SVG injected → QA via `visual_check.cjs` at 3 viewports.

---

## USE CASES Section

| # | Media Item | Skill/Agent | Output Format | Key Brand Requirements | Technical Requirements |
|---|-----------|------------|--------------|----------------------|----------------------|
| 1 | Interactive visual cards | `ls-frontend-design` | HTML/React component in Vite SPA | Navy/red/cyan hierarchy, Arial scale, 4px grid, real content (no lorem ipsum) | One clear hero message, one primary CTA/viewport, vertical rhythm ≥64px, responsive <768px, semantic headings, lucide icons |
| 2 | Workflow diagrams | `ls-diagramming` | Mermaid flowchart → SVG/PNG | Navy/red/cyan steps, Arial labels, 4px grid | `flowchart TD`, ≤15 nodes, brand palette, no spaghetti edges |
| 3 | Before/after process maps | `ls-visual-storytelling` | SVG comparison visual or HTML one-pager | Brand palette enforced (post-render checker green), clear hierarchy, key stat/CTA | Eight-beat narrative, source traceable stats, palette checker `--tolerance 3` must PASS |
| 4 | Evidence/status indicators | `ls-presentation-design` | KPI-style badges (HTML/CSS or PPTX) | KPI cards: light-grey rounded rects, big navy figure, dark-grey label, Arial scale | Real facts from company/results, ≤6 bullets/slide, ≤12 words/bullet, speaker notes |

**Common Brand Enforcement**: Navy `#070A40`, Red `#DC3641`, Cyan `#00BFFF`, Arial type scale, 4px grid. All assets go through `ls-artifact-qa` gate before delivery.

---

## SECTORS Section

| # | Media Item | Skill/Agent | Output Format | Key Brand Requirements | Technical Requirements |
|---|-----------|------------|--------------|----------------------|----------------------|
| 1 | Sector-specific imagery | `ls-frontend-design` | HTML/CSS React component or PNG/SVG in Vite SPA | Navy primary, Red accent, Cyan secondary, Arial type scale, 4px grid, no AI slop | React + Tailwind 4, accessible, contrast ≥4.5:1, no stereotypes, official logo, `ls-artifact-qa` gate |
| 2 | Sector data visualizations | `ls-diagramming` | Rendered SVG or PNG (prefer SVG) | Navy dominant, cyan accents, red for CTAs/warnings, Arial labels 10-14pt, 4px grid | Mermaid/Kroki per type-choice matrix, ≤15 nodes, brand palette via `k-dense-mermaid-skill`, `ls-artifact-qa` brand QA |
| 3 | Relevant use-case illustrations | `ls-visual-storytelling` | SVG/HTML one-pager or professional infographic | Navy dominant, cyan secondary, red for key number/CTA, Arial scale (36/32/28/24/18/16/14/13/12), 4px grid | Facts sourced from results/company/research (never invented), post-render palette checker PASS, then `ls-artifact-qa` QA, headline/key stat/CTA non-negotiable |

**Cross-Cutting**: `ls-design-system` loaded first. All artifacts go through `ls-artifact-qa` final gate. No off-palette colors. AI-generated renders require post-processing and palette checker verification. Official logo from `brand/logo/`, tagline "ASPIRE. ACT. ACHIEVE." with `™`. Arial type scale only, 4px spacing base unit.

---

## INSIGHTS Section

| # | Media Item | Skill/Agent | Output Format | Key Brand Requirements | Technical Requirements |
|---|-----------|------------|--------------|----------------------|----------------------|
| 1 | Editorial hero imagery | `ls-creative-director` → `ls-frontend-design` | Hero image/header background (PNG/JPEG, 1920×1080px min) | Navy #070A40 background with red #DC3641 accent stripe, cyan #00BFFF 4px line, Arial type scale for overlay, official logo, clear space, no AI slop | RGB color space, web-optimized (≤200KB), responsive min 1440px wide, accessible alt text, Vite React + Tailwind 4 pipeline, final `ls-artifact-qa` review |
| 2 | Charts | `ls-diagramming` | Interactive/Static SVG chart (self-contained SVG with inline CSS) | All lines/areas from LS palette: navy, red, cyan; Arial axis labels; gridlines aligned to 4px; Background navy #070A40 with contrast; Red for primary series, Cyan for secondary/tertiary; Legend per 4px grid | SVG output, no external dependencies; Accessible: `<title>` and `<desc>` elements; Color blind safe (navy/red/cyan contrast); Data labels optional, inline tooltips preferred; Exportable via `ls-diagramming`; Must pass `ls-artifact-qa` visual check |
| 3 | Research diagrams | `ls-diagramming` | Mermaid diagram HTML / standalone SVG diagram | Navy #070A40 header/footer bands, red #DC3641 callout highlights, cyan #00BFFF accent elements, Arial type scale for labels/captions, 4px grid for connectors/arrows, optional LS logo watermark | Mermaid → PNG/SVG via `mmdc` or Kroki API; Dark/light theme support; Standalone HTML with inline SVG; Version-controlled flowchart/sequence/state diagram; Must pass `ls-artifact-qa` for technical accuracy and brand consistency; Keywords: architecture, process map, data flow, org structure, customer journey |
| 4 | Policy illustrations | `ls-document-design` | Illustrated policy page (PNG/SVG embedded in DOCX/Markdown, or standalone) | Navy #070A40 left rail (10×7.5in margin), red #DC3641 accent dividers, cyan #00BFFF callout headers, Arial type scale for body/headers, 4px grid for columns/gutters, official logo on cover, consistent with `ls-presentation-design` slide rules | Rendered via `k-dense-pptx` (python-pptx) or `k-dense-docx`; If web-embedded: PNG/SVG with transparent background; Inline CSS only (no external stylesheets); Color palette applied consistently; Must pass `ls-artifact-qa` for brand compliance; File naming: `policy-illustration-[topic]-[version]`; PPTX generated via `ls-presentation-design` pipeline; Image export from `ls-document-design` with proper web dimensions |

**Quality Assurance Workflow** (mandatory sequence for all 4 types):

1. **`ls-creative-director`** — initial brief intake and skill chain routing
2. **Creation** by the designated specialist skill
3. **`ls-artifact-qa`** — final gate: Visual QA (spacing, hierarchy, balance, contrast, whitespace, alignment), Brand QA (colors, type, logo, tagline), UX QA (CTA clarity, overflow, navigation, responsiveness, mobile), Accessibility QA (contrast, alt text, focus, headings), Content QA (claims, citations, consistency, grammar, numbers)
4. **Approval** → artifact released, or **FIX → RENDER AGAIN** → RE‑APPROVE

**Key Brand Enforcement** (all assets): Navy `#070A40` — primary; Red `#DC3641` — accent/CTA; Cyan `#00BFFF` — secondary; Arial type scale — all typography; 4px grid — all spacing/gutters/alignment. **No AI slop** — every asset must pass `ls-artifact-qa` gate.

---

## ABOUT Section

| # | Media Item | Skill/Agent | Output Format | Key Brand Requirements | Technical Requirements |
|---|-----------|------------|--------------|----------------------|----------------------|
| 1 | Human leadership | `ls-creative-director` | High-res photographic images (WebP), responsive sizes | Navy/red/cyan palette, Arial type scale, 4px grid, official logo with `™`, tagline "ASPIRE. ACT. ACHIEVE.", model releases, consistent African context (Lilongwe backdrop), alt text, performance budget ≤150 KB | WebP format, responsive sizes, consistent backdrop, alt text for accessibility, optimized for web performance |
| 2 | Malawi / Africa context | `ls-visual-storytelling` | SVG map diagram (primary) with WebP fallback | Navy dominant, cyan accents, red highlights, Arial typography, 4px grid, avoid choropleth stereotypes, correct Malawi→SADC→Africa progression | Correct geographic progression, no stereotypes, palette checker `check_brand_palette.py --tolerance 3` must PASS, accessible alt text, SVG/HTML format |
| 3 | Operating philosophy | `ls-diagramming` | SVG diagram (conceptual strategy framework) | Navy dominant, cyan/red accents, Arial type scale, 4px grid, max 3 weights, editorial style not default flowchart | SVG/HTML, 2px line weight, 8px radius nodes, dark/light mode compatible, palette checker PASS, figcaption for accessibility, vector format |

**Standard Pipeline**: optimize → variants → responsive sizes → manifest → deploy. All assets undergo `ls-artifact-qa` final gate before delivery.

---
