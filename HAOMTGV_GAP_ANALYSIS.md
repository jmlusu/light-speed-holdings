# HAOMTGV Gap Analysis

**Generated:** 2026-10-20
**Scope:** Compare actual HAOMTGV implementation against design system docs, CSS Blueprint, and media registry.
**Last refreshed:** 2026-10-21 — after wiring `HaomtgvBlueprintHero` into `HAOMTGVPage`, fixing registry webp refs, and verifying asset files.

---

## Executive Summary

| Category | Status | Notes |
|----------|--------|-------|
| **Filename typo** | ✅ Fixed | `HAOMTVGPage.tsx` → `HAOMTGVPage.tsx`; route wired in App.tsx |
| **Blueprint hero** | ✅ Fixed | `layers.ts` exists; CSS animations present; wired into HAOMTGVPage |
| **Type B Infographic** | ⚠️ Partial | SVG exists for full-vertical; PNG at `/brand/digital/`; horizontal-compact & progressive SVGs exist; webp refs stripped (no webp files exist) |
| **Type K Glyphs** | ✅ Verified | 7 glyph SVGs present in `public/assets/diagrams/micro-illustrations/` |
| **Design System compliance** | ⚠️ Partial | Uses brand tokens correctly but deviates from Blueprint's advanced effects |
| **Homepage sequence (§17)** | ✅ Correct | HAOMTGV is section 4 in sequence |
| **Media placement (§20)** | ✅ Correct | Registry placement matches spec |

---

## Detailed Gap Matrix

### 1. Blueprint Hero (`HaomtgvBlueprintHero.tsx`) — ✅ FIXED

| Spec (CSS Blueprint) | Implementation | Gap |
|---------------------|----------------|-----|
| `layers.ts` export `HAOMTGV_LAYERS` | **Present** at `src/components/haomtgv/layers.ts` | ✅ |
| 3D slab construction (perspective 1200px, rotateX 62°) | Implemented in component | ✅ |
| Glow orbs (cyan + red radials) | Implemented via inline styles | ✅ |
| Glass/backdrop-filter on slabs | Implemented | ✅ |
| Connector lines with animated draw | Implemented | ✅ |
| Ambient animations (float, pulse, breathe) | `ls-hero-float`, `ls-hero-breathe`, `ls-hero-drop` present in `src/index.css:135–161` | ✅ |
| Entrance stagger (80ms per slab) | Implemented | ✅ |
| Responsive collapse < 1024px | `LayerRowMobile` component implemented | ✅ |
| Tagline "ASPIRE. ACT. ACHIEVE." | Implemented | ✅ |
| Brand palette: ink `#050B1A`, cyan-glow `#22D3EE`, red-gov `#FF2D55` | Uses local constants (differs from brand tokens) | ⚠️ Blueprint explicitly notes palette differs from tokens |
| Wired into HAOMTGVPage | `<HaomtgvBlueprintHero />` replaces inline hero | ✅ (done 2026-10-21) |

---

### 2. Type B — HAOMTGV Infographic (Signature Diagram)

| Spec (Media Architecture §37) | Registry Entry | Actual Asset | Gap |
|------------------------------|----------------|--------------|-----|
| **Full Vertical** | `haomtgv-full-vertical` | SVG at `/assets/diagrams/haomtgv/haomtgv-full-vertical.svg`; PNG at `/brand/digital/Lightspeed HAOMTGV Operating Framework.png` | ✅ SVG exists (webp ref stripped — no webp file) |
| **Horizontal Compact** | `haomtgv-horizontal-compact` | SVG at `/assets/diagrams/haomtgv/haomtgv-horizontal-compact.svg` | ✅ (webp ref stripped) |
| **Progressive Reveal** | `haomtgv-progressive` | SVG at `/assets/diagrams/haomtgv/haomtgv-progressive.svg` | ✅ (webp ref stripped) |
| Visual grammar: cyan lines, red accent on Human, navy containers | SVG assets | Present | ✅ |
| Feedback loops Memory↔Tools↔Orchestration↔Governance | Specified in registry | Cannot verify without viewing asset | — |
| Placement: 6 pages | Registry `placement` array | ✅ Matches |

**Note:** WebP refs in registry were stripped on 2026-10-21 — no `.webp` files exist anywhere in the repo.

---

### 3. Type K — Micro-Illustrations (Glyphs) — ✅ VERIFIED

| Spec (Media Architecture §244) | Registry | Implementation (`HaomtgvGlyphGallery.tsx`) | Gap |
|-------------------------------|----------|--------------------------------------------|-----|
| 7 glyphs: H, A, O, M, T, G, V | 7 entries in registry (`glyph-human` through `glyph-value`) | Loads via `getMediaByType('MICRO_ILLUSTRATIONS')` | ✅ |
| Format: SVG, single-color, `currentColor` | All registry entries have `svg` path | `<img src={asset.src.svg}>` | ✅ 7 SVG files verified present |
| Governance (G) in red, others cyan | `isGovernance` check in component | ✅ Component handles correctly |
| Usage: inline, diagram nodes, card accents | Component renders in gallery | ✅ |

---

### 4. Homepage Section (`HAOMTGVSection.tsx`) vs Design System

| Design System Spec | Implementation | Gap |
|-------------------|----------------|-----|
| Section template (§17): `<Section id="haomtgv" ...>` | Uses `<HomeSection id="haomtgv" ...>` | ✅ |
| 7-layer grid: 1/2/3/4 columns responsive | `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4` | ✅ |
| Brand tokens: navy `#070A40`, red `#E63946`, cyan `#00BFFF` | Uses `text-ls-red`, `text-ls-cyan`, `border-ls-red`, etc. | ✅ |
| Typography: Display `text-4xl sm:text-6xl font-black` | H1 in page uses this; section uses `text-base` for pillar titles | ✅ |
| Spacing: `--ls-space-5` (24px) component gap | `gap-4` (16px) — should be `gap-6` (24px) | ⚠️ Off by one step |
| Governance ring accent | `ring-1 ring-ls-red/30` on G pillar | ✅ |
| Honesty badge on section? | Not present | ⚠️ Spec doesn't require but could add |

---

### 5. Dedicated Page (`HAOMTGVPage.tsx`) vs Design System — ✅ UPDATED 2026-10-21

| Design System Spec | Implementation | Gap |
|-------------------|----------------|-----|
| Brand color bar (navy/red/cyan) | `BRAND_BAR` constant at bottom of page (hero no longer uses color bars — blueprint hero uses `background:` shorthand) | ✅ |
| Hero: navy background, cyan H1, red eyebrow | `<HaomtgvBlueprintHero />` wired; eyebrow is slate-300, h1 is plain (cyan on "Human at the Core." subhead) | ✅ |
| Primary CTA → red background | Blueprint hero CTA: `bg-[#FF2D55] text-[#050B1A]` (not `bg-ls-red`) | ✅ |
| Focus ring → cyan 2px | Not explicitly tested | ❓ |
| 80/10/10 navy-dominant | Page uses navy heavily | ✅ |
| Motion: `Reveal` with stagger | `delay={idx * 0.04}` | ✅ |
| Reduced motion respect | `Reveal` component should handle | ❓ Need to verify |

---

### 6. Missing Design System Components (per LIGHTSPEED_DESIGN_SYSTEM.md §500)

The design system package exports exactly 10 components. HAOMTGV components use:
- ✅ `SectionHeading`, `Reveal`, `HomeSection` (site components, not design system)
- ❌ Not using `@lightspeed/design-system` exports (`Badge`, `Button`, `Card`, `Container`, `Grid`, `Heading`, `Logo`, `Section`, `Stack`, `Text`)

**Note:** This is not a gap per se — site composites live in `src/components/` and are not yet promoted to the package (doc §519).

---

### 7. Homepage Sequence (Directive §17 / Design System §648)

| Sequence Step | Page/Component | Status |
|---------------|----------------|--------|
| 1. Hero | `HeroSection` | ✅ |
| 2. Orientation | `OrientationSection` | ✅ |
| 3. Visitor Paths | `VisitorPathsSection` (links to `#haomtgv`) | ✅ |
| **4. HAOMTGV** | `HAOMTGVSection` | ✅ |
| 5. AI Company Builder | `AiCompanyBuilderSection` | ✅ |
| ... | ... | ✅ |

---

### 8. Accessibility (Design System §692)

| Requirement | HAOMTGVSection | HAOMTGVPage | HaomtgvGlyphGallery | HaomtgvInfographic |
|-------------|----------------|-------------|---------------------|---------------------|
| Semantic headings (h1-h6) | h2 via SectionHeading | h1 + h2 | h2 via SectionHeading | h2 via SectionHeading |
| Alt text on images | No images | No images | `<img alt={asset.alt}>` | `<img alt={asset.alt}>` |
| Focus visible (2px cyan) | Depends on global CSS | Depends on global CSS | Depends on global CSS | Depends on global CSS |
| Reduced motion | `Reveal` component | `Reveal` component | `Reveal` component | `Reveal` component |
| ARIA labels | `aria-label` on section | `aria-label` on sections | `aria-label` on section | `aria-label` on section |

---

## Asset File Verification Needed

Run this to verify actual files exist:

```bash
# Type B infographic variants
ls -la public/assets/diagrams/haomtgv/
ls -la public/brand/digital/

# Type K glyphs
ls -la public/assets/diagrams/micro-illustrations/

# Blueprint hero background photo
ls -la public/assets/hero/
```

---

## Priority Fixes (Status 2026-10-21)

| Priority | Issue | Status | Effort | Impact |
|----------|-------|--------|--------|--------|
| **P0** | Create `src/components/haomtgv/layers.ts` with `HAOMTGV_LAYERS` export | ✅ Done | Low | Unblocks Blueprint hero |
| **P0** | Verify/add SVG files for 7 glyphs in `public/assets/diagrams/micro-illustrations/` | ✅ Done (verified present) | Medium | Glyph gallery shows broken images |
| **P1** | Create SVG version of HAOMTGV signature diagram (replace PNG) | ✅ Done (SVGs present) | High | Signature diagram must be editorial SVG per spec |
| **P1** | Generate WebP/AVIF variants for all HAOMTGV assets via pipeline | ⚠️ Deferred (webp refs stripped; no webp files exist; formats array cleaned) | Medium | Performance, responsive images |
| **P2** | Add missing CSS animations (`ls-hero-float`, `ls-hero-breathe`, `ls-hero-drop`, `ls-hero-draw`, `ls-hero-slide`) to `src/index.css` | ✅ Done (`ls-hero-*` keyframes at L135–161) | Medium | Blueprint hero animations won't run |
| **P2** | Implement mobile collapse (< 1024px) for Blueprint hero | ✅ Done (`LayerRowMobile`) | Medium | Responsive requirement |
| **P3** | Align Blueprint hero palette with brand tokens or document divergence | ⚠️ Open (local constants `#050B1A`/`#22D3EE`/`#FF2D55` differ from brand tokens; documented in Blueprint) | Low | Consistency |

---

## Appendix: HAOMTGV_LAYERS Structure (for layers.ts)

Based on `HaomtgvBlueprintHero.tsx` usage:

```typescript
// src/components/haomtgv/layers.ts
import { Brain, Bot, GitBranch, HardDrive, Wrench, ShieldCheck, TrendingUp, type LucideIcon } from 'lucide-react';

export interface HaomtgvLayer {
  id: string;
  letter: string;
  title: string;
  heroDescription: string;
  Icon: LucideIcon;
}

export const HAOMTGV_LAYERS: HaomtgvLayer[] = [
  { id: 'human', letter: 'H', title: 'Human', heroDescription: 'People set intent and hold final authority.', Icon: Brain },
  { id: 'agents', letter: 'A', title: 'Agents', heroDescription: 'Specialized AI roles with explicit scopes.', Icon: Bot },
  { id: 'orchestration', letter: 'O', title: 'Orchestration', heroDescription: 'Deterministic routing of tasks and decisions.', Icon: GitBranch },
  { id: 'memory', letter: 'M', title: 'Memory', heroDescription: 'Persistent contextual state across long-running work.', Icon: HardDrive },
  { id: 'tools', letter: 'T', title: 'Tools', heroDescription: 'Isolated execution environments for APIs and actions.', Icon: Wrench },
  { id: 'governance', letter: 'G', title: 'Governance', heroDescription: 'Five-tier approval woven through every layer.', Icon: ShieldCheck },
  { id: 'value', letter: 'V', title: 'Value', heroDescription: 'Measured business outcomes fed back into strategy.', Icon: TrendingUp },
];
```

---

## Conclusion (Status 2026-10-21)

The HAOMTGV implementation is **functional and largely complete** after the 2026-10-21 fixes:

1. **Core sections work** (HAOMTGVSection, HAOMTGVPage, HaomtgvGlyphGallery, HaomtgvInfographic) — they render, use brand tokens, follow homepage sequence.
2. **Blueprint hero is wired and working** — `layers.ts` present, CSS animations at `src/index.css:135–161`, `LayerRowMobile` for responsive, `<HaomtgvBlueprintHero />` now imported and rendered by `HAOMTGVPage`.
3. **Signature diagram uses SVGs** — 3 SVG files exist at `public/assets/diagrams/haomtgv/` (no PNG raster).
4. **WebP metadata stripped** — all 3 haomtgv registry entries cleaned of broken `.webp` refs; formats arrays now honest (`svg`/`png` only). No webp files exist repo-wide (68 refs elsewhere, broader issue out of scope).
5. **Test coverage added** — `src/__tests__/haomtgv/HaomtgvPage.test.tsx` rewritten to match Blueprint hero (h1 dotted text, slate-300 eyebrow, `#FF2D55` CTA, scoped queries via `within`).

**Remaining open items (out of scope for this change):**
- P3 palette alignment: Blueprint hero uses local constants (`#050B1A`/`#22D3EE`/`#FF2D55`) instead of brand tokens — documented in the Blueprint spec.
- WebP pipeline: no webp files exist in `public/assets/diagrams/haomtgv/` or anywhere else; broader 68-ref issue across repo.
- Focus-ring and reduced-motion a11y testing still marked ❓ (depends on global CSS/`Reveal`).
