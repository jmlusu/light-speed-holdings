# Media Architecture

**Version:** 1.0
**Status:** ACTIVE
**Created:** 2026-10-04
**Owner:** Creative Director / Media Generation Owner

---

## Purpose

This document defines the LightSpeed media architecture — the strategic system for creating, managing, and deploying all visual content across the public website. It implements Directive §19-20, establishing media types, placement strategy, and production pipelines.

**Core Principle:** Do NOT fill the website with generic stock photos. Create a LightSpeed media architecture. Every visual must be intentional, on-brand, and strategically placed.

---

## Media Type Taxonomy (Directive §19)

### Type A — Hero Imagery
**Purpose:** Cinematic African technology/business environments for hero sections
**Characteristics:**
- Modern African cityscape at dawn (Lilongwe, Blantyre, Johannesburg)
- Architectural geometry (government buildings, universities, tech hubs)
- Data center / compute imagery (local infrastructure)
- African executive in modern workspace (authentic, not stock)
- Subtle network architecture over physical African geography
- Macro architectural details (concrete, glass, light)
- Abstract geometric motion (slow, purposeful)

**Forbidden:** Cliché "African person staring at laptop" stock imagery

**Placement:** Home hero, AI Company Builder hero, What We Do hero, About hero

---

### Type B — H-A-O-M-T-G-V Infographic (Signature Diagram)
**Purpose:** The signature LightSpeed framework visualization
**Structure:**
```
HUMAN
   ↓
AGENTS (89 AI + 1 Human CEO)
   ↓
ORCHESTRATION (MessageBus, workflows)
   ↓
MEMORY (6-type store)
   ↓
TOOLS (isolated execution environments)
   ↓
GOVERNANCE (5-tier approval, audit)
   ↓
VALUE (measurable outcomes)
```
**Visual Grammar:**
- Feedback loops between Memory ↔ Tools ↔ Orchestration ↔ Governance
- Human layer positioned above system (not in flow)
- Value as business outcome at bottom
- Cyan connection lines, Red accent on Human, Navy containers
- Editorial diagram style (not flowchart software default)

**Placement:** Home (§17.04), AI Company Builder, What We Do, Use Cases, About, FAQ

**Variants:** Full vertical, horizontal compact, animated progressive reveal

---

### Type C — AI Company Builder Org Chart (Interactive)
**Purpose:** Explorable 90-role visualization
**Structure:**
```
Human CEO
    ↓
20 Departments (Executive, Technology, AI Research, Operations, etc.)
    ↓
Agent Clusters (by department)
    ↓
Workflows (9 definitions)
    ↓
Outputs (deliverables, decisions, artifacts)
```
**Interactivity:**
- Click department → expand agent cluster
- Click agent → show role, tools, approval level
- Hover workflow → highlight path
- Filter by agent type (executive/specialist/board)

**Placement:** AI Company Builder page (primary), Home (static thumbnail)

---

### Type D — Model Routing Infographic
**Purpose:** Visualize Africa-first AI economics (Directive §4, §19)
**Structure:**
```
LOCAL / OPEN-WEIGHT
    ↓
LOW-COST TASKS
    (classification, extraction, summarization, embeddings, repetitive workflows)

MID-TIER
    ↓
STANDARD REASONING
    (planning, synthesis, reasoning)

PREMIUM
    ↓
HIGH COMPLEXITY
    (exceptional reasoning, complex generation, difficult edge cases)

HUMAN
    ↓
FINAL AUTHORITY
    (decisions, approvals, accountability)
```
**Principle:** "Use the least expensive model that can reliably do the job."
**Visual:** Tiered horizontal bands, left-to-right flow, cost indicators
**No fabricated cost savings** — show principle, not specific numbers

**Placement:** AI Company Builder, Home, What We Do, FAQ

---

### Type E — Africa AI Economics Infographic
**Purpose:** Explain the economic architecture
**Comparison:**
| Approach | Cost | Latency | Sovereignty | Use Case |
|----------|------|---------|-------------|----------|
| Commercial API | High | Low | Low | Premium reasoning |
| Open-Weight API | Medium | Low | Medium | Standard tasks |
| Local Inference (Ollama) | Near-zero | Medium | **High** | Routine, high-volume |
| Hybrid Routing | Optimized | Optimized | Configurable | Production |

**Placement:** AI Company Builder, Home, About, FAQ

---

### Type F — Use Case Cards
**Purpose:** Distinct visual thumbnail for each use case
**Categories (Directive §19):**
- Compliance reporting
- Agricultural coordination
- Donor reporting
- Data cleaning
- SME operations
- Customer service
- Market intelligence
- Research synthesis
- Regulatory monitoring
- University research
- Policy analysis

**Visual Treatment:**
- Editorial diagrams over generic stock photos
- Consistent card format: thumbnail + title + status badge + sector tag
- Status badge uses honesty system (proven/pilot/fieldable/development)
- Hover → expand to show problem/workflow/value preview

**Placement:** Use Cases explorer, Home (featured), Solutions (related), Sectors (relevant)

---

### Type G — Architecture Diagrams
**Purpose:** Clean technical diagrams for system explanations
**Topics:**
- AI Company Builder system architecture
- H-A-O-M-T-G-V (Type B)
- Orchestration (MessageBus, executor)
- Memory (6-type store, recall loop)
- Tools (isolated environments, MCP)
- Governance (approval matrix, audit trail)
- Model routing (Type D)
- Data sovereignty (Zero-Cloud Boundary)

**Style:**
- SVG/HTML/CSS (not raster) for crispness, accessibility
- Brand colors only (navy, cyan, red, white, greys)
- Consistent line weight (2px), node style (rounded rect, 8px radius)
- Annotation layer for key metrics
- Dark/light mode compatible

**Placement:** AI Company Builder, Use Case detail, Sectors, About, FAQ

---

### Type H — African Maps
**Purpose:** Strategic geographic visualization
**Key Map:**
```
Malawi
    ↓
SADC (16 member states)
    ↓
Africa (54 countries)
```
**Variants:**
- Expansion concept (animated progression)
- Sector presence heatmap
- Use case deployment markers
- Partner/institution locations

**Rules:**
- Do not imply operational presence in every country
- Show conceptual progression, not current footprint
- Use brand colors; avoid standard choropleth defaults

**Placement:** Home, Sectors, About, Insights (Pharos Africa Watch)

---

### Type I — Research Visuals (Pharos)
**Purpose:** Editorial visual language for thought leadership
**Formats (Directive §40):**
- **Charts** — Recharts, brand-styled (navy/cyan/red)
- **Research Diagrams** — Custom SVG, editorial style
- **Policy Frameworks** — Structured diagrams, not tables
- **Annotated Maps** — Type H with research overlay
- **Evidence Matrices** — Claim ↔ Source grids
- **Model Comparison Diagrams** — Benchmark visualizations
- **Timelines** — Horizontal, milestone-based
- **Architecture Schematics** — Type G with research context

**Pharos Visual Language:** Consistent across all Pharos formats (Brief, Field Note, Research Note, Policy Note, System Map, Data Story, AI Economics, Africa Watch)

**Placement:** Insights listing, Insight articles, Home (featured), Solutions, About

---

### Type J — Human / Leadership Imagery
**Purpose:** Authentic leadership representation
**Requirements:**
- Actual LightSpeed leadership (Jack Mlusu, executives)
- Professional but not corporate-stock
- African context visible (office, Lilongwe backdrop)
- Consistent lighting, composition, crop
- High-resolution for print/digital

**Forbidden:** Generic executive stock imagery

**Placement:** About page, Home (leadership strip), Board/Advisor pages, Press kit

---

### Type K — Micro-Illustrations
**Purpose:** Reusable glyph system for HAOMTGV and UI
**Set:**
- H — Human (stylized figure with intent arrow)
- A — Agents (interlocking geometric forms)
- O — Orchestration (flow lines, nodes)
- M — Memory (layered cylinders)
- T — Tools (wrench/terminal hybrid)
- G — Governance (shield with check)
- V — Value (upward chart, diamond)

**Usage:** Inline with text, diagram nodes, card accents, loading states
**Format:** SVG, single-color (uses currentColor for theming)

---

## Media Placement Strategy (Directive §20)

| Page | Media Types | Priority |
|------|-------------|----------|
| **Home** | A (Hero), B (HAOMTGV), C (Org Chart thumb), E (Africa Economics), F (Use Case thumbs), I (Pharos visual) | Critical |
| **What We Do** | Process diagram, Engagement model, Capability illustrations (K) | High |
| **AI Company Builder** | C (Org Chart full), B (HAOMTGV), Workflow animation, D (Model Routing), G (Gov architecture), Audit trail viz | Critical |
| **Solutions** | Solution-specific diagrams (G), Capability illustrations (K) | High |
| **Use Cases** | F (Interactive cards), Workflow diagrams (G), Before/after process maps, Evidence/status indicators | Critical |
| **Sectors** | Sector-specific imagery (A), Sector data visualizations (I), Relevant use case illustrations (F) | High |
| **Insights** | Editorial hero (A), Charts (I), Research diagrams (I), Policy illustrations (I) | High |
| **About** | Human leadership (J), Malawi/Africa context (A/H), Operating philosophy (K) | High |
| **FAQ** | Minimal media; focus on clarity. HAOMTGV micro (K) if needed | Low |

---

## Production Pipeline

### Creation Tools
| Media Type | Primary Tool | Secondary |
|------------|--------------|-----------|
| Type A (Hero) | Photography (commissioned) / Midjourney v6 + Photoshop | — |
| Type B, C, D, E, G, H, K | **Archify** skill (SVG/HTML) / Figma → SVG | Manual SVG |
| Type F (Use Case Cards) | Archify + custom SVG templates | — |
| Type I (Pharos) | Archify / Recharts / k-dense-infographics skill | Python (matplotlib) → SVG |
| Type J (Leadership) | Photography (commissioned) | — |

### Asset Pipeline
```
Source (Figma/SVG/Photo/Code)
    ↓
Optimize (SVGO, imagemin, sharp)
    ↓
Generate Variants
    - WebP (primary)
    - AVIF (modern)
    - SVG (diagrams, icons)
    - PNG fallback
    ↓
Responsive Sizes
    - 400w, 800w, 1200w, 1600w, 2000w
    ↓
Manifest Entry (public/assets/manifest.json)
    ↓
Deploy to public/assets/{type}/
    ↓
Reference in data/media/registry.ts
```

### Manifest Schema
```json
{
  "id": "haomtgv-full-vertical",
  "type": "HAOMTGV_INFOGRAPHIC",
  "title": "H-A-O-M-T-G-V Framework",
  "src": {
    "webp": "/assets/diagrams/haomtgv-full-vertical.webp",
    "avif": "/assets/diagrams/haomtgv-full-vertical.avif",
    "svg": "/assets/diagrams/haomtgv-full-vertical.svg"
  },
  "alt": "H-A-O-M-T-G-V framework showing Human at top, flowing through Agents, Orchestration, Memory, Tools, Governance to Value",
  "width": 1200,
  "height": 1600,
  "placement": ["/", "/ai-company-builder", "/what-we-do", "/use-cases", "/about", "/faq"],
  "attribution": "LightSpeed Holdings Design Team"
}
```

---

## Asset Organization (public/assets/)

```
public/assets/
├── brand/                 # Logo variants, brand marks
│   ├── logo-full-color.svg
│   ├── logo-dark-bg.svg
│   ├── logo-light-bg.svg
│   ├── icon-mark.svg
│   ├── monochrome.svg
│   ├── favicon.svg
│   ├── social-avatar.svg
│   └── og-share.svg
├── diagrams/              # Type B, C, D, E, G, H, K
│   ├── haomtgv/
│   ├── org-chart/
│   ├── model-routing/
│   ├── africa-economics/
│   ├── architecture/
│   ├── maps/
│   └── micro-illustrations/
├── hero/                  # Type A
│   ├── home-hero.webp
│   ├── aicb-hero.webp
│   ├── whatwedo-hero.webp
│   └── about-hero.webp
├── use-cases/             # Type F
│   ├── compliance-reporting.webp
│   ├── agri-coordination.webp
│   └── ...
├── insights/              # Type I
│   ├── charts/
│   ├── diagrams/
│   └── pharos-formats/
├── sectors/               # Type A + H per sector
│   ├── financial-services/
│   ├── agriculture/
│   └── ...
├── leadership/            # Type J
│   ├── jack-mlusu.webp
│   └── ...
└── manifest.json          # Master asset index
```

---

## Pharos Media Program (Directive §40)

### Recurring Visual Formats
Each Pharos format has a consistent visual template:

| Format | Visual Template | Use Case |
|--------|-----------------|----------|
| **PHAROS BRIEF** | Hero image + 3 key metrics + 1 system map | Executive summaries |
| **PHAROS FIELD NOTE** | Annotated map + photo + 2 data points | Field observations |
| **PHAROS RESEARCH NOTE** | Chart + evidence matrix + model comparison | Research findings |
| **PHAROS POLICY NOTE** | Policy framework diagram + timeline + stakeholder map | Policy analysis |
| **PHAROS SYSTEM MAP** | Full architecture diagram (Type G) | System explanations |
| **PHAROS DATA STORY** | Multi-chart narrative + annotated map | Data-driven stories |
| **PHAROS AI ECONOMICS** | Model routing (Type D) + cost curves + tier breakdown | Economics analysis |
| **PHAROS AFRICA WATCH** | Map (Type H) + sector heatmap + trend lines | Regional monitoring |

### Template System
```tsx
// PharosArticleTemplate.tsx
<PharosTemplate format="RESEARCH_NOTE">
  <PharosHero image={heroImage} metrics={keyMetrics} />
  <PharosBody>
    <PharosChart data={chartData} />
    <PharosEvidenceMatrix claims={claims} sources={sources} />
    <PharosModelComparison models={models} />
  </PharosBody>
  <PharosFooter relatedUseCases={...} relatedSectors={...} cta={...} />
</PharosTemplate>
```

---

## Africa-First Visual Story (Directive §39)

### Visual Motifs (Authentic, Not Stereotypical)
| Motif | Representation | Avoid |
|-------|----------------|-------|
| African Infrastructure | Modern highways, fiber networks, data centers, solar farms | Dirt roads, power lines as failure |
| Regional Connectivity | SADC maps, fiber routes, trade corridors, mobile networks | Isolated villages |
| Mobile Money | Airtel Money, TNM Mpamba, M-Pesa interfaces, QR payments | Cash-only markets |
| Agriculture | Precision farming, drone monitoring, coop dashboards, irrigation tech | Subsistence farming only |
| Cities | Lilongwe, Blantyre, Johannesburg, Nairobi skylines, tech hubs | Slums as default |
| Universities | MUBAS, UNIMA labs, research centers, student hackathons | Colonial buildings only |
| Public Institutions | Modern ministries, MACRA, central banks, regulators | Bureaucracy stereotypes |
| Research Environments | AI labs, HPC clusters, field research stations | Empty classrooms |
| Data Systems | Dashboards, pipelines, governance dashboards, audit trails | Paper ledgers |
| Local Computing | Edge devices, Ollama on-prem, sovereign clouds | "No technology" |
| Multilingual Interfaces | Chichewa/English UI, voice interfaces, USSD | English-only |
| Low-Bandwidth Design | Progressive enhancement, offline-first, text-first | "Broken" experiences |
| Regional Maps | SADC, COMESA, AU boundaries, trade routes | Colonial borders only |

### Africa Should Be Shown As:
- **CAPABLE** — Modern infrastructure, skilled workforce
- **INNOVATIVE** — Homegrown solutions, leapfrogging
- **RESOURCEFUL** — Doing more with less, frugal innovation
- **CONNECTED** — Digital highways, mobile-first, regional integration
- **AMBITIOUS** — National AI strategies, space programs, unicorn aspirations
- **TECHNICALLY SOPHISTICATED** — AI research, fintech leadership, regulatory innovation

---

## Pinterest/Reference Implementation Rule (Directive §38)

**For each reference image, extract:**
1. **Composition** → Grid structures, asymmetry, rule of thirds
2. **Color** → Palette relationships, accent usage, neutrals
3. **Light** → Direction, quality, shadow treatment
4. **Material** → Texture, surface, depth cues
5. **Typography** → Scale, hierarchy, pairing, whitespace
6. **Spacing** → Rhythm, density, breathing room
7. **Image Treatment** → Crop, overlay, duotone, mask
8. **Motion** → Transition style, timing, easing
9. **Geometry** → Shapes, lines, patterns, repetition

**Then map into reusable LightSpeed components:**
- Not: "Put this Pinterest image in Hero"
- But: "This reference uses asymmetric composition with generous whitespace → apply to all section layouts"

**Result:** "LightSpeed has its own visual identity inspired by these references." NOT "LightSpeed copied these websites."

---

## Technical Specifications

### Image Formats
| Use Case | Primary | Fallback |
|----------|---------|----------|
| Photography | AVIF → WebP → JPEG | JPEG |
| Diagrams/Icons | SVG | PNG |
| Illustrations | SVG → WebP | PNG |
| UI Elements | SVG | PNG |

### Responsive Images
```html
<picture>
  <source type="image/avif" srcset="image-800.avif 800w, image-1200.avif 1200w" sizes="(max-width: 768px) 100vw, 50vw" />
  <source type="image/webp" srcset="image-800.webp 800w, image-1200.webp 1200w" sizes="(max-width: 768px) 100vw, 50vw" />
  <img src="image-1200.jpg" alt="Descriptive alt text" loading="lazy" width="1200" height="800" />
</picture>
```

### Performance Budgets
| Asset Type | Max Size | Dimensions |
|------------|----------|------------|
| Hero Image | 150 KB | 1920×1080 |
| Diagram (SVG) | 50 KB | Vector |
| Use Case Thumb | 30 KB | 400×300 |
| Pharos Chart | 40 KB | 800×600 |
| Logo | 10 KB | Vector |

### Accessibility
- **All images:** Descriptive `alt` text (not "image" or "diagram")
- **Diagrams:** Long description via `<figcaption>` or linked accessible version
- **Charts:** Data table alternative
- **Maps:** Text-based list alternative
- **Decorative:** `alt=""` + `aria-hidden="true"`

---

## Governance

### Media Review Checklist
- [ ] On-brand (colors, typography, tone)
- [ ] Honest (no fabricated scenes, no misleading implications)
- [ ] Accessible (alt text, contrast, reduced motion)
- [ ] Performant (optimized, responsive, lazy-loaded)
- [ ] Strategically placed (per placement strategy)
- [ ] Attributed (source, license, creator)
- [ ] Versioned (in manifest, git-tracked for SVGs)

### Asset Lifecycle
1. **Commission/Create** → Brief aligned with media type spec
2. **Review** → Creative Director + Brand approval
3. **Optimize** → Pipeline generates variants
4. **Register** → Entry in `data/media/registry.ts` + manifest
5. **Deploy** → Commit to `public/assets/`
6. **Reference** → Components import from registry
7. **Audit** → Quarterly review for relevance, performance, honesty

---

## Migration from Current State

### Current `public/assets/` Cleanup
| Current | Action |
|---------|--------|
| `catalog/` (A1-E2, industry-*, scenario-*, proof-*, offer-*) | **Archive** → `archive/assets/catalog/` — legacy offer/proof assets |
| `diagrams/` | **Audit** → Keep usable architecture diagrams; migrate to `diagrams/architecture/` |
| `illustrations/` | **Audit** → Keep on-brand; migrate to `diagrams/micro-illustrations/` or `hero/` |
| `insights/` | **Restructure** → `insights/charts/`, `insights/diagrams/`, `insights/pharos-formats/` |
| `metrics/` | **Migrate** → `diagrams/architecture/` or `insights/charts/` |
| `screenshots/` | **Delete** — not strategic media |
| `sectors/` | **Restructure** → `sectors/{id}/` with hero + data viz |
| `brand/` (duplicate) | **Consolidate** → `brand/` root only |

### New Asset Creation Priority (Phase 5)
1. **Type B** — HAOMTGV signature diagram (used on 6+ pages)
2. **Type A** — Home hero + AI Company Builder hero
3. **Type D** — Model routing infographic (key differentiator)
4. **Type C** — Org chart (interactive, AI Company Builder)
5. **Type F** — Use case thumbnails (12+ use cases)
6. **Type K** — Micro-illustrations (HAOMTGV glyphs)
7. **Type E** — Africa economics
8. **Type H** — Africa maps
9. **Type I** — Pharos templates (8 formats)
10. **Type J** — Leadership photography
11. **Type G** — Architecture diagrams (as needed per page)

---

*This document is living. Update as media architecture evolves during implementation.*
