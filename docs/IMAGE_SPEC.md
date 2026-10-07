# LightSpeed Holdings — Build-Ready Image Specification

**Owner:** Creative Director | **Status:** Ratified for Implementation | **Version:** 1.0
**Source of Truth:** This document. Aligned with `src/types.ts`, `harness/qa/visual_check.cjs`, `brand/tokens/brand-tokens.json`, and WCAG AA fix (#376).

---

## 0. Executive Summary

This specification is the single source of truth for all image/media handling across the LightSpeed Holdings client site (`src/`). It defines the **5-kind taxonomy**, **attribute contracts**, **sourcing rules**, **placement map**, **asset pipeline**, **QA gate**, **component integration patterns**, **rollout plan**, and **honesty integration** — so a frontend engineer can implement without further clarification.

**Key invariants:**
- Every image is typed via `data-ls-image-type` (one of 5 kinds)
- Brand assets are canonical at `brand/**`; mirrors at `static/brand/**` and `public/brand/**` are sync-only
- WCAG AA contrast: brand red is `#DC3641` (not `#E63946`) — verified in `brand-tokens.json`
- All media rendering is behind feature flag `VITE_CONTENT_MEDIA_ENABLED`
- `HonestyBadge` travels with media in the component layer — **never baked into the image file**

---

## 1. Taxonomy — 5 Kinds with Exact Field Shapes

Defined in `src/types.ts` (lines 219–270). Each kind is a discriminated union on `kind`.

| Kind | Interface | Required Fields | Optional Fields | Notes |
|------|-----------|-----------------|-----------------|-------|
| `screenshot` | `ScreenshotMedia` | `kind: 'screenshot'`, `src`, `alt`, `width`, `height`, `tone: 'light' \| 'dark'` | — | Real UI captures; `tone` drives container theming |
| `brand-mark` | `BrandMedia` | `kind: 'brand-mark'`, `src`, `alt: ''`, `width`, `height` | — | Official logos only; `alt` empty (decorative) |
| `diagram` | `DiagramMedia` | `kind: 'diagram'`, `alt`, `tone: 'light' \| 'dark'` | — | **No `src`** — rendered inline via `ls-diagramming` (Mermaid/SVG) |
| `metrics` | `MetricMedia` | `kind: 'metrics'`, `alt`, `tone: 'light' \| 'dark'` | — | **No `src`** — rendered inline via chart components (recharts) |
| `illustration` | `IllustrationMedia` | `kind: 'illustration'`, `src`, `alt`, `width`, `height`, `tone: 'light' \| 'dark'` | — | Hand-drawn (Grav IP) or generated; `tone` drives container |

### Aggregate Types

```ts
export type ContentMedia =
  | ScreenshotMedia
  | BrandMedia
  | DiagramMedia
  | MetricMedia
  | IllustrationMedia;

export interface ContentMediaSet {
  hero?: ContentMedia;
  gallery?: ContentMedia[];
  thumbnail?: ContentMedia;
}
```

**Discriminant rule:** Always switch on `media.kind` — never infer from presence of `src`.

---

## 2. Attribute Requirements — DOM Contract

Every rendered `<img>` or media container **must** carry these attributes for QA and accessibility.

### 2.1 Required Data Attributes (All Kinds)

| Attribute | Value | Enforced By |
|-----------|-------|-------------|
| `data-ls-image-type` | `screenshot \| brand-mark \| diagram \| metrics \| illustration` | `visual_check.cjs` + component render |
| `data-ls-logo-instance` | `true \| false` | `brand-mark` only — `true` for brand logos |
| `alt` | String (empty string `''` only for `brand-mark`) | `visual_check.cjs` (fails on missing) |
| `width` | Number (pixels, intrinsic) | `screenshot`, `brand-mark`, `illustration` |
| `height` | Number (pixels, intrinsic) | `screenshot`, `brand-mark`, `illustration` |
| `data-ls-tone` | `light \| dark` | All kinds — drives container theme |

### 2.2 Per-Kind Attribute Matrix

| Kind | `src` | `alt` | `width`/`height` | `tone` | `data-ls-logo-instance` |
|------|-------|-------|------------------|--------|-------------------------|
| `screenshot` | ✅ Required | ✅ Descriptive | ✅ Required | ✅ Required | `false` |
| `brand-mark` | ✅ Required | ✅ `''` (empty) | ✅ Required | ❌ Not used | `true` |
| `diagram` | ❌ **No src** | ✅ Descriptive | ❌ Not used | ✅ Required | `false` |
| `metrics` | ❌ **No src** | ✅ Descriptive | ❌ Not used | ✅ Required | `false` |
| `illustration` | ✅ Required | ✅ Descriptive | ✅ Required | ✅ Required | `false` |

### 2.3 Alt Text Quality Rules

- **Screenshot:** "LightSpeed Holdings [feature] dashboard showing [specific metric/view]" — specific, not "screenshot of dashboard"
- **Brand-mark:** `''` (empty) — logo is decorative; company name in nearby text
- **Diagram:** "[Diagram type] showing [key relationships/entities] — e.g., "System architecture diagram showing 90-agent orchestration, message bus, and approval gates"
- **Metrics:** "[Metric name] — [value] [unit] as of [date]" — e.g., "Automated regression tests — 1,247 tests as of 2026-09-30"
- **Illustration:** "Hand-drawn illustration of [concept] in Grav style" — references Grav character IP

**Forbidden:** "image", "photo", "picture", "graphic", empty alt on non-brand-mark.

---

## 3. Sourcing Rules — Where Assets Come From

### 3.1 Canonical Brand Files (6 Core Assets)

**Source:** `brand/logos/fulllogo/`, `brand/logos/icononly/`, `brand/logos/grayscale/`, `brand/logos/textonly/`
**Mirror (read-only at runtime):** `public/brand/logos/**` (served at `/brand/logos/...`)

| Asset | Canonical Path | Runtime Path | Use Case |
|-------|----------------|--------------|----------|
| Full Logo (Primary) | `brand/logos/fulllogo/Logo3_transparent.svg` | `/brand/logos/fulllogo/Logo3_transparent.svg` | Headers, covers, hero brand-mark |
| Full Logo (No Buffer) | `brand/logos/fulllogo/Logo3_transparent_nobuffer.svg` | `/brand/logos/fulllogo/Logo3_transparent_nobuffer.svg` | Tight layouts |
| Icon Only | `brand/logos/icononly/icononly_transparent.svg` | `/brand/logos/icononly/icononly_transparent.svg` | Avatars, favicons, thumbnails |
| Icon Only (No Buffer) | `brand/logos/icononly/icononly_transparent_nobuffer.svg` | `/brand/logos/icononly/icononly_transparent_nobuffer.svg` | Tight layouts |
| Text Only | `brand/logos/textonly/textonly_transparent.svg` | `/brand/logos/textonly/textonly_transparent.svg` | When icon already present |
| Grayscale | `brand/logos/grayscale/grayscale_transparent.svg` | `/brand/logos/grayscale/grayscale_transparent.svg` | B&W print, legal docs |

**Rule:** Never recreate, resize, or recolor logos in code. Use official SVG assets. Minimum screen sizes: Full logo 120px wide, Icon only 32px wide (per `brand-tokens.json`).

### 3.2 Fresh Playwright Screenshots (`screenshot` kind)

- **Generated by:** `ls-artifact-qa` skill via `visual_check.cjs` (Playwright Chromium)
- **Trigger:** CI on PR, or manual `node harness/qa/visual_check.cjs <url> --viewport 1280x800 --out out.png`
- **Stored at:** `public/assets/screenshots/<page>-<viewport>.png` (gitignored; regenerated per deploy)
- **Naming:** `<page-slug>-<viewport>-<timestamp>.png` — e.g., `what-we-do-1280x800-20260930.png`
- **Dimensions:** Must match declared `width`/`height` in `ContentMedia`

**Pipeline:** Screenshot → optimize (sharp, WebP fallback) → commit to `public/assets/screenshots/` → reference in data.

### 3.3 Inline Diagrams (`diagram` kind) — No Image File

- **Rendered by:** `ls-diagramming` skill → Mermaid → Kroki/Playwright → inline SVG
- **Source:** Mermaid source in component or data file (`mermaid` code fences)
- **Output:** Injected as `<svg>` or `<img src="data:image/svg+xml,...">` at render time
- **Brand restyle:** Always navy/red/cyan palette via `ls-design-system` tokens
- **No `src` field** — `ContentMedia` carries only `kind`, `alt`, `tone`

### 3.4 Inline Metrics (`metrics` kind) — No Image File

- **Rendered by:** Recharts components (`AreaChart`, `MetricCard`, etc.) in `src/components/athena/`
- **Data source:** Live metrics from `src/data/metrics.ts` (reads `company-registry.yaml`, test counts)
- **Output:** SVG/Canvas at render time
- **No `src` field** — `ContentMedia` carries only `kind`, `alt`, `tone`

### 3.5 Illustrations (`illustration` kind) — Grav IP / Generated

- **Source:** `article-illustrations` skill (Grav hand-drawn) or `k-dense-infographics` (AI-generated)
- **Stored at:** `public/assets/illustrations/<slug>.svg|.png`
- **Palette:** Must pass through `ls-design-system` (navy/red/cyan, Arial, 4px grid)
- **Dimensions:** Declared in `ContentMedia` — typically 800×600 (4:3) or 1200×675 (16:9)

---

## 4. Placement Map — Per Page/Component

Derived from Wayfinder map (#378) and current page components. Each entry specifies: **page**, **component**, **media slot**, **expected kind(s)**, **data source**.

| Page | Component | Slot | Expected Kind(s) | Data Source |
|------|-----------|------|------------------|-------------|
| `/` (Home) | `HeroSection` | hero | `illustration` \| `screenshot` | `siteContent.ts` hero media set |
| `/what-we-do` | `OfferHeroMedia` | hero (per offer family) | `screenshot` \| `illustration` \| `brand-mark` | `useCaseCatalogData.ts` → `OFFER_FAMILIES[i].media.hero` |
| `/what-we-do` | `SolutionThumbnailMedia` | thumbnail (per solution) | `screenshot` \| `illustration` \| `brand-mark` | `siteContent.ts` → `solutions[i].media.thumbnail` |
| `/what-we-do` | `DeliverableThumbnailMedia` | thumbnail (per deliverable) | `screenshot` \| `brand-mark` | `useCaseCatalogData.ts` → `deliverables[j].media.thumbnail` |
| `/solutions` | `SolutionCard` | (none currently) — **future**: inline `diagram` \| `metrics` | `diagram` \| `metrics` | `siteContent.ts` → `solutions[i].media.inline` |
| `/sectors` | Sector cards | hero/thumbnail | `illustration` \| `screenshot` | `sector-registry.ts` → `sectors[i].media` |
| `/proof` | Metric cards | inline | `metrics` (Recharts) | `siteContent.ts` → `PLATFORM_METRICS` |
| `/proof` | Case study cards | thumbnail | `screenshot` \| `illustration` | `siteContent.ts` → `proofCaseStudies[i].media.thumbnail` |
| `/insights` | `InsightArticlePage` | hero | `illustration` \| `screenshot` | `insights.ts` → `insightArticles[i].media.hero` |
| `/insights` | `InsightArticlePage` | inline (per block) | `diagram` \| `metrics` \| `illustration` | `insights.ts` → `InsightBlock` extensions |
| `/ai-company-builder` | Dashboard | hero | `screenshot` (live dashboard) | Playwright capture of `/athena/dashboard` |
| `/contact` | CTA band | brand-mark | `brand-mark` (full logo) | Static brand asset |

### 4.1 Data Model Extensions Required

Add `media: ContentMediaSet` to:
- `OfferFamily` (in `useCaseCatalogData.ts`)
- `Solution` (in `siteContent.ts`)
- `Deliverable` (in `useCaseCatalogData.ts`)
- `Sector` (in `sector-registry.ts`)
- `ProofCaseStudy` (in `siteContent.ts`)
- `InsightArticle` (in `insights.ts`)

---

## 5. Asset Pipeline — Build-Time → Runtime

### 5.1 Build-Time (Vite)

| Step | Tool | Input | Output |
|------|------|-------|--------|
| 1. Brand sync | `scripts/build/sync-brand.ps1` | `brand/**` | `public/brand/**`, `static/brand/**` |
| 2. Screenshot gen | `visual_check.cjs` (CI) | Staging URLs | `public/assets/screenshots/**` |
| 3. Illustration gen | `article-illustrations` / `k-dense-infographics` | Briefs | `public/assets/illustrations/**` |
| 4. Vite build | `vite build` | `public/**` + `src/**` | `dist/**` (hashed filenames) |

**Vite config:** `public/` copied as-is to `dist/`. No image transformation (YAGNI — sharp not in deps).

### 5.2 Runtime Loading

- **Static assets (`/brand/...`, `/assets/...`):** Served directly by Vite/Cloudflare Pages — no import needed
- **Dynamic `src` in `ContentMedia`:** String paths (e.g., `/assets/screenshots/what-we-do-1280x800.png`) — rendered as `<img src={media.src} />`
- **Inline SVG (diagrams/metrics):** Injected via component render — no network request

### 5.3 Feature Flag: `VITE_CONTENT_MEDIA_ENABLED`

```ts
// In every media component (see OfferHeroMedia.tsx, SolutionThumbnailMedia.tsx)
const isMediaEnabled = (): boolean => {
  if (typeof window === 'undefined') return false;
  return import.meta.env.VITE_CONTENT_MEDIA_ENABLED === 'true';
};
```

| Environment | Value | Behavior |
|-------------|-------|----------|
| Local dev | `false` (default) | Media components render `null` — no layout shift |
| Staging | `true` (enable after QA) | Full media render |
| Production | `true` (after staging sign-off) | Full media render |

**Set in:** Cloudflare Pages environment variables / `.env.production` / `.env.staging`

---

## 6. QA Gate — `visual_check.cjs` Rule Set

**File:** `harness/qa/visual_check.cjs` — runs in CI and local. Exit code: `0` = PASS, `2` = FAIL.

### 6.1 Checks Performed (Per Viewport)

| Check | Selector | Pass Criteria | Fail Message |
|-------|----------|---------------|--------------|
| Horizontal overflow | `document.documentElement.scrollWidth - clientWidth` | `0px` | `horizontalOverflowPx > 0` |
| Missing `alt` | `img:not([alt])` | `0` elements | `missingAltCount > 0` |
| Empty headings | `h1,h2,h3` with empty `textContent` | `0` elements | `emptyHeadingCount > 0` |

### 6.2 Viewports Tested

Default: `1280x800` (desktop). Configurable via `--viewport WxH` (multiple allowed).

**Required viewports for release:**
- `1280x800` (desktop baseline)
- `375x667` (mobile — iPhone SE)
- `768x1024` (tablet — iPad)

### 6.3 Extended QA Rules (Manual + Automated)

| Rule | Kind | Check | Tool |
|------|------|-------|------|
| Brand colors only | All | No hex outside `#070A40`, `#DC3641`, `#00BFFF`, neutrals | `ls-artifact-qa` |
| Logo clear space | `brand-mark` | 1× "L" height padding | Visual inspection |
| Logo min size | `brand-mark` | ≥120px (full), ≥32px (icon) | Visual inspection |
| WCAG AA contrast | All text on brand red | 4.52:1 (verified) | Mathematical |
| Aspect ratio honored | `screenshot`/`illustration` | Container `aspect-video` (hero) or `aspect-square` (thumb) | Visual |
| `HonestyBadge` present | All media with honesty status | Badge rendered adjacent, not in image | Component test |
| No layout shift | All | `loading="lazy"` (non-hero) / `eager` (hero) | Lighthouse |

### 6.4 CI Integration

```yaml
# .github/workflows/visual-qa.yml (to be added)
- name: Visual QA
  run: |
    npx playwright install chromium
    node harness/qa/visual_check.cjs http://localhost:3000 --viewport 1280x800 --viewport 375x667 --json visual-report.json
```

---

## 7. Component Integration — Render Patterns

Four canonical renderer components. All in `src/components/whatwedo/` and `src/components/site/`.

### 7.1 `HeroMediaRenderer` — `OfferHeroMedia.tsx`

```tsx
// Renders hero media (aspect-video) with optional HonestyBadge overlay
<MediaRenderer media={media} isLight={isLight} size="hero" />
```

**Props:**
- `media: ContentMedia` (single, from `ContentMediaSet.hero`)
- `isLight: boolean` (theme)
- `size: 'hero'` → `aspect-video`, `loading="eager"`

**Kind handling:**
- `screenshot`/`illustration`: `<img src alt className="w-full h-auto object-cover" />`
- `brand-mark`: `<img src alt="" className="w-full h-auto object-contain p-4" />`
- `diagram`/`metrics`: Placeholder `<div>` with alt text (inline render TODO)

### 7.2 `GalleryMediaRenderer` — `OfferHeroMedia.tsx` (size="gallery")

Same as hero but `aspect-square`, `loading="lazy"`. Used for gallery arrays.

### 7.3 `ThumbnailMedia` — `SolutionThumbnailMedia.tsx` / `DeliverableThumbnailMedia.tsx`

```tsx
// Renders square thumbnail (aspect-square) in card grids
<div className="relative aspect-square">{renderThumbnail()}</div>
```

**Props:**
- `media: ContentMedia | undefined` (from `ContentMediaSet.thumbnail`)
- `isLight: boolean`

**Kind handling:** Same as hero but `object-cover` for screenshot/illustration, `object-contain p-2` for brand-mark.

### 7.4 `InlineMediaBlock` — **New Component Needed**

For `diagram` and `metrics` kinds inside article/insight bodies.

```tsx
// src/components/site/InlineMediaBlock.tsx (to be created)
export const InlineMediaBlock: React.FC<{
  media: ContentMedia; // kind: 'diagram' | 'metrics'
  isLight: boolean;
}> = ({ media, isLight }) => {
  // diagram → <MermaidDiagram source={...} /> or <svg dangerouslySetInnerHTML...>
  // metrics → <MetricChart data={...} />
};
```

**Placement:** `InsightArticlePage.tsx` `renderBlock` switch (extend `InsightBlock` union).

---

## 8. Rollout Plan — Phased Feature Flag

| Phase | Flag Value | Environment | Criteria | Owner |
|-------|------------|-------------|----------|-------|
| 0 | `false` | Local dev | Default — no media renders | — |
| 1 | `true` | Staging (preview deploy) | All `visual_check.cjs` viewports PASS; brand assets synced; screenshots captured | Creative Director |
| 2 | `true` | Staging + QA | Manual review: alt quality, honesty badges, no layout shift | Creative Director + QA Lead |
| 3 | `true` | Production | Staging sign-off + CEO approval | CEO |

**Rollback:** Set `VITE_CONTENT_MEDIA_ENABLED=false` in Cloudflare Pages env → instant disable (no redeploy).

---

## 9. Honesty Integration — `HonestyBadge` Travels With Media

**Rule:** The honesty status of a media asset is a property of the *claim*, not the pixel data. Never bake badges into image files.

### 9.1 Data Model

`ContentMedia` **does not** carry honesty. Honesty lives on the parent entity:
- `OfferFamily.honestyBadge`
- `Solution.honestyBadge` / `proof`
- `Sector.status`
- `ProofCaseStudy.honestyBadge`
- `InsightArticle` (inherits from related solutions/sectors)

### 9.2 Render Pattern (from `OfferHeroMedia.tsx`)

```tsx
const badgeLabel = getBadgeLabel(media); // Derived from parent entity, not media

return (
  <div className={containerClass}>
    <div className="relative aspect-video">
      {renderMedia()}
      {badgeLabel && (
        <HonestyBadge label={badgeLabel} className="absolute top-2 right-2 z-10" />
      )}
    </div>
  </div>
);
```

### 9.3 Badge Positioning

| Media Size | Badge Position | Z-Index |
|------------|----------------|---------|
| Hero (`aspect-video`) | `absolute top-2 right-2` | `z-10` |
| Gallery (`aspect-square`) | `absolute top-2 right-2` | `z-10` |
| Thumbnail (`aspect-square`) | `absolute top-1 right-1` | `z-10` |
| Inline (diagram/metrics) | Below media, inline with text | Flow |

### 9.4 Badge Tone Mapping (from `siteContent.ts:honestyLabel`)

| HonestyBadge Value | Tone | CSS Class |
|--------------------|------|-----------|
| `Proven in-house` \| `Live proof` \| `Published` | `proven` | `border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan` |
| `In pilot` \| `In pilot (composing evidence)` \| `In pilot (proposed)` | `pilot` | `border-ls-red/40 bg-ls-red/10 text-ls-red` |
| `Fieldable in 2026` | `fieldable` | `border-ls-grey-light-text/40 bg-ls-grey-light-text/10 text-ls-grey-light-text` |
| `In active development` \| `Proposed` | `development` | `border-ls-grey-dark/40 bg-ls-grey-dark/10 text-ls-grey-dark` |

---

## 10. Implementation Checklist (Definition of Done)

### Data Layer
- [ ] Add `media?: ContentMediaSet` to `OfferFamily`, `Solution`, `Deliverable`, `Sector`, `ProofCaseStudy`, `InsightArticle`
- [ ] Populate with real assets (brand logos, screenshots, illustration slugs)
- [ ] Ensure `diagram`/`metrics` kinds have `alt` + `tone` only (no `src`)

### Components
- [ ] Verify `OfferHeroMedia`, `SolutionThumbnailMedia`, `DeliverableThumbnailMedia` match spec
- [ ] Create `InlineMediaBlock.tsx` for `diagram`/`metrics` in articles
- [ ] Add `data-ls-image-type`, `data-ls-logo-instance`, `data-ls-tone` to all `<img>` renders
- [ ] Ensure `alt` quality per §2.3

### Pipeline
- [ ] Run `pwsh scripts/build/sync-brand.ps1` — verify `public/brand/logos/**` populated
- [ ] Generate Playwright screenshots for all 7 pages at 3 viewports
- [ ] Generate/commission illustrations for hero slots
- [ ] Configure `VITE_CONTENT_MEDIA_ENABLED` in Cloudflare Pages (staging → prod)

### QA
- [ ] Run `visual_check.cjs` on staging at 3 viewports — zero failures
- [ ] Manual audit: brand colors, logo clear space, honesty badge positioning
- [ ] Lighthouse: no CLS, all images have `width`/`height` or aspect-ratio containers

### Documentation
- [ ] This spec (`docs/IMAGE_SPEC.md`) ratified and linked from `README.md`
- [ ] Component JSDoc updated with kind-handling tables

---

## 11. Appendix — Quick Reference

### 11.1 Brand Tokens (Canonical)

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| `navy` | `#070A40` | 7, 10, 64 | Primary surfaces, headlines |
| `red` | `#DC3641` | 220, 54, 65 | CTAs, accents (WCAG AA on white) |
| `cyan` | `#00BFFF` | 0, 191, 255 | Links on dark, shield base |
| `grey-light` | `#F2F2F2` | 242, 242, 242 | Light backgrounds |
| `white` | `#FFFFFF` | 255, 255, 255 | Text on navy |
| `grey-dark` | `#6B7280` | 107, 114, 128 | Secondary text |
| `grey-light-text` | `#9CA3AF` | 156, 163, 175 | Tertiary text on dark |

### 11.2 Type Scale (from `brand-tokens.json`)

| Token | Size | Use |
|-------|------|-----|
| `displayXl` | 36pt | Hero headlines |
| `titleXl` | 32pt | Page titles |
| `titleLg` | 28pt | Section titles |
| `titleMd` | 24pt | Card titles |
| `titleSm` | 18pt | Subsection |
| `subtitle` | 16pt | Leads |
| `bodyLg` | 16pt | Body large |
| `body` | 14pt | Body |
| `bodySm` | 13pt | Captions |
| `caption` | 12pt | Footnotes |

### 11.3 Spacing Scale

`4, 8, 12, 16, 24, 32, 48, 64, 96` (base unit 4px)

### 11.4 Commands

```bash
# Sync brand assets
pwsh scripts/build/sync-brand.ps1

# Visual QA (3 viewports)
node harness/qa/visual_check.cjs https://staging.lightspeedholdings.com \
  --viewport 1280x800 --viewport 375x667 --viewport 768x1024 \
  --json visual-report.json

# Build with media enabled
VITE_CONTENT_MEDIA_ENABLED=true npm run build
```

---

**End of Specification** — This document is the contract. If implementation deviates, update this spec first.
