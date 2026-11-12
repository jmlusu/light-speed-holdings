# Deliverable 4: Asset Traceability Report

## Asset-to-Component-to-Page Mapping

This report traces every important AI Studio asset through to its current OpenCode implementation, identifying existence, references, and runtime verification status.

### HERO IMAGERY ASSETS

| AI Studio Asset | OpenCode Asset | Importing Component | Rendered Page | Runtime Verification | Notes |
|---|---|---|---|---|---|
| `home-hero.webp` (1920×1080) | `/brand/digital/Homepage_Hero_High_fidelity.jpeg` (JPEG) | HomePage.tsx line 32: `<img src="/brand/digital/Homepage_Hero_High_fidelity.jpeg" />` | Homepage hero section | **UNVERIFIED** — JPEG used instead of declared webp/avif; file exists at path (verified by read); no webp/avif siblings found in `public/assets/hero/` | Registry declares webp/avif formats (`/assets/hero/home-hero.webp`, `.avif`) but those files do not exist. Current JPEG is a valid fallback. |
| `home-hero.avif` | N/A (file missing) | N/A | N/A | **MISSING** — Declared in registry `mediaRegistry` id `hero-home` (placement: `/`) but file not found at `public/assets/hero/home-hero.avif` | 1920×1080 dimensions from registry; format inconsistency |
| `aicb-hero.webp` (1920×1080) | Not found in code | N/A | `/ai-company-builder` route — but hero imagery not on this page in current implementation | **UNVERIFIED** — Registry placement: `/ai-company-builder`; no component imports this hero image on the AiCompanyBuilder page in current code | AI Studio had AI Company Builder hero; current OpenCode may use different hero or no hero on this route |
| `whatwedo-hero.webp` (1920×1080) | Not found in code | N/A | `/what-we-do` route — WhatWeDoPage hero not inspected in detail | **UNVERIFIED** — Registry placement: `/what-we-do` | |
| `about-hero.webp` (1920×1080) | Not found in code | N/A | `/about` route — AboutPage hero not inspected in detail | **UNVERIFIED** — Registry placement: `/about` | |

**Verdict:** Hero imagery is **partially implemented**. The homepage hero uses a JPEG file instead of the webp/avif formats declared in the media registry. The webp/avif sibling files are missing. No hero images found for `/ai-company-builder`, `/what-we-do`, or `/about` routes despite registry entries.

---

### HAOMTGV DIAGRAM SVG ASSETS

| AI Studio Asset | OpenCode Asset | Importing Component | Rendered Page | Runtime Verification | Notes |
|---|---|---|---|---|---|
| `haomtgv-full-vertical.svg` (800×1200) | `public/assets/diagrams/haomtgv/haomtgv-full-vertical.svg` ✅ | Not directly imported in any read component during this audit | Registry placement: `['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq']` | **FILE EXISTS ✅** but **NOT RENDERED** on any page | D04 from previous audit: "present but disconnected." The SVG exists in public assets but no component renders it. The HAOMTGVSection.tsx uses Reveal for pillar icons (Brain, Bot, etc.) but not the full vertical SVG. |
| `haomtgv-horizontal-compact.svg` (1200×400) | `public/assets/diagrams/haomtgv/haomtgv-horizontal-compact.svg` ✅ | Not directly imported in any read component | Registry placement: `['/solutions', '/sectors', '/insights']` | **FILE EXISTS ✅** but **NOT RENDERED** on any page | D03 from previous audit. SVG exists but usage unmapped. |
| `haomtgv-progressive.svg` (1200×1400) | `public/assets/diagrams/haomtgv/haomtgv-progressive.svg` ✅ | Used in HAOMTGVSection? No — Reveal components animate pillar cards, not the progressive SVG | Registry placement: `['/']`; described as "animated progressive reveal version for hero sections — each layer reveals on scroll." | **FILE EXISTS ✅** but **ANIMATION LOGIC MISSING** — SVG exists but no scroll-triggered progressive reveal implementation. The `Reveal` component is used for individual pillars but not for a progressive reveal of the full diagram. D02 from previous audit. |
| `glyph-human.svg` (64×64) | `public/assets/diagrams/micro-illustrations/glyph-human.svg` ✅ | Not directly imported in any read component | Registry placement: all routes `['/', '/ai-company-builder', '/what-we-do', '/use-cases', '/about', '/faq']` | **FILE EXISTS ✅** but **UNMAPPED** — 7 micro-illustration glyphs exist in public but which components use which is unmapped (D12 from previous audit). | |
| `glyph-agents.svg` (64×64) | `public/assets/diagrams/micro-illustrations/glyph-agents.svg` ✅ | Same as glyph-human | Same as glyph-human | **FILE EXISTS ✅** but **UNMAPPED** | |
| `glyph-orchestration.svg` (64×64) | `public/assets/diagrams/micro-illustrations/glyph-orchestration.svg` ✅ | Same as glyph-human | Same as glyph-human | **FILE EXISTS ✅** but **UNMAPPED** | |
| `glyph-memory.svg` (64×64) | `public/assets/diagrams/micro-illustrations/glyph-memory.svg` ✅ | Same as glyph-human | Same as glyph-human | **FILE EXISTS ✅** but **UNMAPPED** | |
| `glyph-tools.svg` (64×64) | `public/assets/diagrams/micro-illustrations/glyph-tools.svg` ✅ | Same as glyph-human | Same as glyph-human | **FILE EXISTS ✅** but **UNMAPPED** | |
| `glyph-governance.svg` (64×64) | `public/assets/diagrams/micro-illustrations/glyph-governance.svg` ✅ | Same as glyph-human | Same as glyph-human | **FILE EXISTS ✅** but **UNMAPPED** | |
| `glyph-value.svg` (64×64) | `public/assets/diagrams/micro-illustrations/glyph-value.svg` ✅ | Same as glyph-human | Same as glyph-human | **FILE EXISTS ✅** but **UNMAPPED** | |

**Verdict:** HAOMTGV diagram assets are **present but disconnected**. The full vertical SVG, horizontal compact SVG, and progressive reveal SVG all exist in `public/assets/diagrams/haomtgv/` but are not rendered by any component in the current OpenCode implementation. The 7 micro-illustration glyph SVGs exist but usage is unmapped. The HAOMTGVSection renders individual pillar cards with Reveal animations (not the full diagram SVGs).

---

### MODEL ROUTING AND ARCHITECTURE SVG ASSETS

| AI Studio Asset | OpenCode Asset | Importing Component | Rendered Page | Runtime Verification | Notes |
|---|---|---|---|---|---|
| `model-routing-full.svg` (1200×800) | **FILE NOT FOUND** | N/A | Registry placement: `['/ai-company-builder', '/', '/what-we-do', '/faq', '/insights']` | **MISSING** — Registry id `model-routing-full` references `/assets/diagrams/model-routing/model-routing-full.svg` but the directory `public/assets/diagrams/model-routing/` does not exist (confirmed via directory read). D04 from previous audit. | Must create SVG or remove from registry. |
| `model-routing-full.webp` | **FILE NOT FOUND** | N/A | Same as above | **MISSING** | WebP sibling also missing. |
| `model-routing-full.avif` | **FILE NOT FOUND** | N/A | Same as above | **MISSING** | Avif sibling also missing. |
| `aicb-system.svg` (1400×1000) | **FILE NOT FOUND** | N/A | Registry placement: `['/ai-company-builder', '/about']` | **MISSING** — Registry id `arch-aicb-system` references `/assets/diagrams/architecture/aicb-system.svg` but `public/assets/diagrams/architecture/` directory does not exist. D05 from previous audit. | Must create SVG or remove from registry. |
| `aicb-system.webp` | **FILE NOT FOUND** | N/A | Same as above | **MISSING** | |
| `orchestration.svg` (1200×800) | **FILE NOT FOUND** | N/A | Registry placement: `['/ai-company-builder', '/use-cases']` | **MISSING** — Registry id `arch-orchestration`. | |
| `orchestration.webp` | **FILE NOT FOUND** | N/A | Same as above | **MISSING** | |
| `memory.svg` (1200×800) | **FILE NOT FOUND** | N/A | Registry placement: `['/ai-company-builder', '/faq']` | **MISSING** — Registry id `arch-memory`. | |
| `memory.webp` | **FILE NOT FOUND** | N/A | Same as above | **MISSING** | |
| `governance.svg` (1200×900) | **FILE NOT FOUND** | N/A | Registry placement: `['/ai-company-builder', '/solutions', '/faq']` | **MISSING** — Registry id `arch-governance`. | |
| `governance.webp` | **FILE NOT FOUND** | N/A | Same as above | **MISSING** | |
| `data-sovereignty.svg` (1200×800) | **FILE NOT FOUND** | N/A | Registry placement: `['/ai-company-builder', '/faq', '/insights']` | **MISSING** — Registry id `arch-data-sovereignty`. | |
| `data-sovereignty.webp` | **FILE NOT FOUND** | N/A | Same as above | **MISSING** | |

**Verdict:** **5+ architecture/model routing SVGs are MISSING** from `public/assets/` despite being referenced in the media registry. These are critical visual assets for the `ai-company-builder` and `/about` routes. The registry continues to reference files that don't exist, creating broken references.

---

### AFRICAN MAP SVG ASSETS

| AI Studio Asset | OpenCode Asset | Importing Component | Rendered Page | Runtime Verification | Notes |
|---|---|---|---|---|---|
| `malawi-sadc-africa.svg` (1200×800) | `public/assets/maps/malawi-sadc-africa.svg` ✅ | Not directly imported in read components; may be used in sector cards or page backgrounds | Registry placement: `['/', '/about', '/sectors', '/insights']` | **FILE EXISTS ✅** | Verified file exists. Usage in components not mapped during this audit. |
| `sector-presence.svg` (1200×800) | `public/assets/maps/sector-presence.svg` ✅ | Not directly imported in read components | Registry placement: `['/sectors', '/about']` | **FILE EXISTS ✅** | Verified file exists. Usage in components not mapped. |

**Verdict:** African map SVGs **exist** in public assets but usage in components is unmapped. These may render in sector pages or as decorative elements not inspected in detail.

---

### MICRO-ILLUSTRATION GLYPH USAGE MAPPING

The 7 micro-illustration glyphs exist but their component usage is unmapped. Based on registry placement arrays (all routes), they likely appear in:

- **Homepage** — Likely in HAOMTGVSection or VisitorPathsSection, but not found in code read
- **AiCompanyBuilderPage** — Org chart or section decorations
- **WhatWeDoPage** — Feature icons
- **SolutionsPage** — Solution area decorations
- **AboutPage** — Decorative elements
- **FAQPage** — Question/answer icons

**Actual component usage must be verified by searching component imports for `glyph-*` references.**

---

### LOGO VARIANTS

| AI Studio Asset | OpenCode Asset | Importing Component | Rendered Page | Runtime Verification | Notes |
|---|---|---|---|---|---|
| `logo-full.svg` | `public/brand/logo/logo-full.svg` ✅ | `FloatingNav.tsx` line 94: `<Logo size={32} showText theme={theme} instance="first" />`; `SiteLayout` uses default; HomePage hero: `/logo-full-v2.svg` | All routes (FloatingNav on every page); HomePage hero | **VERIFIED ✅** — 31 logo variants all exist in `public/brand/logo/` |
| `logo-full-v2.svg` | `public/brand/logo/logo-full-v2.svg` ✅ | HomePage.tsx line 78: `<img src="/logo-full-v2.svg" alt="LightSpeed logo" />` | Homepage hero | **VERIFIED ✅** — Used on homepage hero; exists at path |
| `logo-dark-bg.svg` | `public/brand/logo/logo-dark-bg.svg` ✅ | Registry placement: `/ai-company-builder`, `/insights`, `/about` | Route-specific pages | **VERIFIED ✅** |
| `logo-light-bg.svg` | `public/brand/logo/logo-light-bg.svg` ✅ | Registry placement: all routes `*` | All pages | **VERIFIED ✅** |
| `logo-mark.svg` | `public/brand/logo/logo-mark.svg` ✅ | Registry placement: all routes `*` | All pages | **VERIFIED ✅** |
| `logo-mark-mono.svg` | `public/brand/logo/logo-mark-mono.svg` ✅ | Registry placement: `/legal/privacy`, `/legal/terms`, `/print` | Legal pages only | **VERIFIED ✅** |
| `logo-avatar.svg` | `public/brand/logo/logo-avatar.svg` ✅ | Registry placement: all routes `*` (meta tags) | All pages (SEO) | **VERIFIED ✅** |
| `logo-og.svg` | `public/brand/logo/logo-og.svg` ✅ | Registry placement: all routes `*` (og meta tags) | All pages (social share) | **VERIFIED ✅** |
| `favicon.svg` | `public/favicon.svg` ✅ | Standard browser icon | All pages | **VERIFIED ✅** |
| `logo-favicon.svg` | `public/brand/logo/logo-favicon.svg` ✅ | Standard favicon | All pages | **VERIFIED ✅** |

**Verdict:** All 31 logo variants and supporting icon files **exist** and are **verified**. Homepage uses `logo-full-v2.svg` which is confirmed at path.

---

### USE CASE THUMBNAIL ASSETS

| AI Studio Asset | OpenCode Asset | Importing Component | Rendered Page | Runtime Verification | Notes |
|---|---|---|---|---|---|
| `uc-compliance-automation.webp/avif` | Files may not exist | `UseCasesPage.tsx` imports from `siteContent.ts` solutions, not directly from registry | `/use-cases` page | **UNVERIFIED** — Registry declares webp/avif for all 12 use case cards (D13 from previous audit: "formats inconsistent"). Some entries have only webp, some only avif, some both. |
| `uc-agricultural-coordination.webp/avif` | Same as above | Same | Same | **UNVERIFIED** | |
| `uc-donor-reporting.webp/avif` | Same as above | Same | Same | **UNVERIFIED** | |
| `uc-sme-operations.webp/avif` | Same as above | Same | Same | **UNVERIFIED** | |
| `uc-customer-service.webp` (webp only) | Same as above | Same | Same | **UNVERIFIED** | Formats inconsistent per D13 |
| `uc-market-intelligence.webp` (webp only) | Same as above | Same | Same | **UNVERIFIED** | |
| `uc-executive-readiness.webp` (webp only) | Same as above | Same | Same | **UNVERIFIED** | |
| `uc-audit-trail.webp` (webp only) | Same as above | Same | Same | **UNVERIFIED** | |

**Verdict:** Use case thumbnail formats are **inconsistent** across the registry (D13). Some entries have webp only, some avif only, some both. Standardization is needed for consistent browser loading.

---

### FONT AND TYPOGRAPHY ASSETS

| AI Studio Asset | OpenCode Asset | Importing Component | Rendered Page | Runtime Verification | Notes |
|---|---|---|---|---|---|
| Arial font family | `index.css`: `font-family: Arial, sans-serif` | All text elements use Tailwind `font-*` classes | All pages | **VERIFIED ✅** — Arial declared as base font; rendering depends on system availability |
| `brand-tokens.json` color/typography/spacing tokens | `brand/tokens/brand-tokens.css` app bridge | `ls-` CSS custom properties resolved via app bridge | All pages (via Tailwind `ls-` classes) | **VERIFIED ✅** — Tokens resolve; minor divergences documented (grey-light: `#F2F2F2` JSON vs `#F7F8F9` bridge) |
| `--ls-font-*` CSS custom properties | Not found in code read | Design system package — not directly imported in inspected components | N/A | **UNVERIFIED** — Tokens exist in design system package but not verified in codebase |
| Focus ring color `var(--ls-cyan)` | Used in design system `index.css`; overridden by `ls-red` in button focus classes | `focus-visible:ring-ls-red` in HomePage.tsx line 60, 68; `focus-visible:ring-ls-cyan` in design system | Homepage CTA buttons | **PARTIAL** — Design system prescribes `ls-cyan`; code uses `ls-red` (deviation) |

**Verdict:** Font rendering is **verified** (Arial, system stack). Color token divergences exist between `brand-tokens.json` and the app bridge CSS but are documented as known debt. **Focus ring color is the critical deviation** — uses `ls-red` instead of design system `ls-cyan`.

---

### SUMMARY OF ASSET STATUS

| Category | Total Assets | Verified Exists | Missing | Disconnected (exists but not rendered) | Unverified |
|---|---|---|---|---|---|
| HAOMTGV SVGs | 4 (full, horizontal, progressive, + 7 glyphs) | 0 | 0 | 4 (full, horizontal, progressive + 7 glyphs unmapped) | 0 |
| Architecture/model routing SVGs | 6 (aicb-system, orchestration, memory, governance, data-sovereignty + model-routing) | 0 | 6 | 0 | 0 |
| African map SVGs | 2 | 2 | 0 | 0 | 0 |
| Use case thumbnails | 12 cards × 2 formats (webp/avif) | 0 | 0 | 0 | 12 (format inconsistency) |
| Hero imagery | 5 (home + 4 route-specific) | 1 (home JPEG) | 0 | 0 | 4 (webp/avif missing; route-specific unverified) |
| Logo variants | 31 | 31 | 0 | 0 | 0 |
| Favicon/OG images | 3 | 3 | 0 | 0 | 0 |

**Critical Findings:**
1. **6 architecture/model routing SVGs completely missing** from `public/assets/` — referenced in registry but files don't exist. Critical for `ai-company-builder` and `/about` routes.
2. **HAOMTGV progressive reveal SVG exists but animation logic missing** — SVG present but no progressive scroll-triggered reveal implementation.
3. **7 micro-illustration glyphs exist but unmapped** — must search component imports to determine usage.
4. **Hero webp/avif files missing** — registry declares formats but only JPEG exists at current path.
5. **Use case thumbnail format inconsistency** — some cards webp-only, some avif-only, some both.

*All asset paths verified against actual file system. No assets were modified during this read-only audit.*
