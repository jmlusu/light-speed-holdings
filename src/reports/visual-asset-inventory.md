# Visual Asset Inventory: LightSpeed Holdings

**Audit Date**: November 3, 2026
**Paths updated**: November 24, 2026 — repointed to published AVIF variants after the production image regression.
**Auditor**: Visual Systems Designer

> Only files under `public/` are served by the web app. Paths beginning `/assets/images/`
> resolve to `public/assets/images/`. Build-time rasters under `src/assets/images/` are
> compilation inputs, not web URLs — page code must never reference them directly.

---

## 1. Hero & Architectural Imagery

| Asset Path | Type / Aspect | Description & Usage | Theme Alignment |
| :--- | :--- | :--- | :--- |
| `/assets/images/hero_cinematic_landscape_night_1793514971805.avif` | AVIF (16:9) | Aerial night mountain highway with cyan/red light trails | Dark Mode Hero |
| `/assets/images/hero_cinematic_landscape_day.avif` | AVIF (16:9) | Photorealistic daylight aerial mountain highway with morning sun | Light Mode Hero |

---

## 2. Capability & Practice Area Visuals

| Asset Path | Type / Aspect | Description & Usage |
| :--- | :--- | :--- |
| `/assets/images/solution_company_builder_1793514972767.avif` | AVIF (4:3) | AI Company Builder showcase thumbnail |
| `/assets/images/solution_workflow_collapsing_1793514973725.avif` | AVIF (4:3) | Workflow Collapsing showcase thumbnail (corrected from the mistyped `..._1793725.jpg` path) |
| `/assets/images/solution_agentic_automation_1793514973368.avif` | AVIF (4:3) | Agentic Automation showcase thumbnail |
| `/assets/images/solution_market_intelligence_1793514973546.avif` | AVIF (4:3) | Pharos Market Intelligence showcase thumbnail |
| `/assets/images/whitepaper_a_cover_clean_1793817703115.avif` | AVIF (16:9) | Published Pharos whitepaper cover (current) |

---

## 3. Brand & Vector Artwork

| Asset Path | Format | Usage |
| :--- | :--- | :--- |
| `/brand/logo/logo-dark-bg.svg` | SVG | Header & Hero logo on dark background |
| `/brand/logo/logo-light-bg.svg` | SVG | Header & Hero logo on light background |
| `/brand/logo/logo-favicon-transparent.png` | PNG | Header brand mark icon |
| `/assets/diagrams/haomtgv/haomtgv-progressive.svg` | SVG | HAOMTGV 7-Layer Architecture Diagram |

---

## 4. Source-only rasters (not served)

These JPGs exist under `src/assets/images/` but have **no published variant** under `public/`.
They are build inputs only; do not reference these paths from page code.

| Source raster | Description | Status |
| :--- | :--- | :--- |
| `src/assets/images/hero_architectural_overview_1793432691740.jpg` | Calm Intelligence Architecture overview | No published variant |
| `src/assets/images/ai_venture_studio_banner_1793432691866.jpg` | AI Venture Studio banner | No published variant |
| `src/assets/images/pharos_research_cover_1793432692045.jpg` | Pharos Research Whitepaper cover | No published variant; current published whitepaper cover listed in section 2 |

---

## 5. Asset Integrity & Fallback Policy

- All `<img>` tags include `referrerPolicy="no-referrer"` and descriptive `alt` text.
- Fallback CSS/SVG containers with cyan/red accents exist for all image slots to ensure zero broken image frames.
- No generated human portraits are used to represent real LightSpeed team members.
- `src/__tests__/media-registry.test.ts` fails the build if any quoted `/src/assets/**` image literal reappears in site source.
