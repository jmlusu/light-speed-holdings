# HAOMTGV Gap Analysis

**Generated:** 2026-10-20
**Scope:** Compare actual HAOMTGV implementation against design system docs, CSS Blueprint, and media registry.

---

## Executive Summary

| Category | Status | Notes |
|----------|--------|-------|
| **Filename typo** | ✅ Fixed | `HAOMTVGPage.tsx` → `HAOMTGVPage.tsx`; route wired in App.tsx |
| **Blueprint hero** | ❌ Broken | `HaomtgvBlueprintHero` imports missing `layers.ts` |
| **Type B Infographic** | ⚠️ Partial | PNG-only (no SVG/WebP/AVIF variants); `haomtgv-horizontal-compact` and `haomtgv-progressive` assets missing |
| **Type K Glyphs** | ⚠️ Partial | Registry has 7 glyphs but SVG files likely missing from `public/assets/diagrams/micro-illustrations/` |
| **Design System compliance** | ⚠️ Partial | Uses brand tokens correctly but deviates from Blueprint's advanced effects |
| **Homepage sequence (§17)** | ✅ Correct | HAOMTGV is section 4 in sequence |
| **Media placement (§20)** | ✅ Correct | Registry placement matches spec |

---

## Detailed Gap Matrix

### 1. Blueprint Hero (`HaomtgvBlueprintHero.tsx`) — **BROKEN**

| Spec (CSS Blueprint) | Implementation | Gap |
|---------------------|----------------|-----|
| `layers.ts` export `HAOMTGV_LAYERS` | **Missing file** | Component cannot compile/run |
| 3D slab construction (perspective 1200px, rotateX 62°) | Implemented in component | ✅ Code exists but unused due to missing import |
| Glow orbs (cyan + red radials) | Implemented via inline styles | ✅ |
| Glass/backdrop-filter on slabs | Implemented | ✅ |
| Connector lines with animated draw | Implemented | ✅ |
| Ambient animations (float, pulse, breathe) | Implemented via CSS animations | ❓ Animations (`ls-hero-float`, `ls-hero-breathe`, `ls-hero-drop`) not found in global CSS |
| Entrance stagger (80ms per slab) | Implemented | ✅ |
| Responsive collapse < 1024px | Not implemented | Missing mobile layout |
| Tagline "ASPIRE. ACT. ACHIEVE." | Implemented | ✅ |
| Brand palette: ink `#050B1A`, cyan-glow `#22D3EE`, red-gov `#FF2D55` | Uses local constants (differs from brand tokens) | ⚠️ Blueprint explicitly notes palette differs from tokens |

**Blocking Issue:** `import { HAOMTGV_LAYERS } from './layers'` → **file does not exist**

---

### 2. Type B — HAOMTGV Infographic (Signature Diagram)

| Spec (Media Architecture §37) | Registry Entry | Actual Asset | Gap |
|------------------------------|----------------|--------------|-----|
| **Full Vertical** | `haomtgv-full-vertical` | PNG only at `/brand/digital/Lightspeed HAOMTGV Operating Framework.png` | ❌ No SVG, WebP, AVIF variants; PNG is raster (not editorial SVG) |
| **Horizontal Compact** | `haomtgv-horizontal-compact` | SVG + WebP paths registered | ❌ Files likely missing from `public/assets/diagrams/haomtgv/` |
| **Progressive Reveal** | `haomtgv-progressive` | SVG + WebP paths registered | ❌ Files likely missing |
| Visual grammar: cyan lines, red accent on Human, navy containers | PNG asset | Cannot verify without viewing asset |
| Feedback loops Memory↔Tools↔Orchestration↔Governance | Specified in registry | Cannot verify |
| Placement: 6 pages | Registry `placement` array | ✅ Matches |

**Key Issue:** Signature diagram should be **SVG (editorial diagram)** per Media Architecture: "Editorial diagrams are preferred over photographs for explaining mechanism" and "SVG/HTML/CSS (not raster) for crispness, accessibility". Current asset is a PNG.

---

### 3. Type K — Micro-Illustrations (Glyphs)

| Spec (Media Architecture §244) | Registry | Implementation (`HaomtgvGlyphGallery.tsx`) | Gap |
|-------------------------------|----------|--------------------------------------------|-----|
| 7 glyphs: H, A, O, M, T, G, V | 7 entries in registry (`glyph-human` through `glyph-value`) | Loads via `getMediaByType('MICRO_ILLUSTRATIONS')` | ✅ Registry complete |
| Format: SVG, single-color, `currentColor` | All registry entries have `svg` path | `<img src={asset.src.svg}>` | ❌ SVG files likely missing from `public/assets/diagrams/micro-illustrations/` |
| Governance (G) in red, others cyan | `isGovernance` check in component | ✅ Component handles correctly |
| Usage: inline, diagram nodes, card accents | Component renders in gallery | ✅ |

**Verification Needed:** Check if `/assets/diagrams/micro-illustrations/glyph-*.svg` files exist.

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

### 5. Dedicated Page (`HAOMTGVPage.tsx`) vs Design System

| Design System Spec | Implementation | Gap |
|-------------------|----------------|-----|
| Brand color bar (navy/red/cyan) | `BRAND_BAR` constant with correct hex values | ✅ |
| Hero: navy background, cyan H1, red eyebrow | Implemented | ✅ |
| Primary CTA → red background | `bg-ls-red text-ls-white` | ✅ |
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

## Priority Fixes

| Priority | Issue | Effort | Impact |
|----------|-------|--------|--------|
| **P0** | Create `src/components/haomtgv/layers.ts` with `HAOMTGV_LAYERS` export | Low | Unblocks Blueprint hero |
| **P0** | Verify/add SVG files for 7 glyphs in `public/assets/diagrams/micro-illustrations/` | Medium | Glyph gallery shows broken images |
| **P1** | Create SVG version of HAOMTGV signature diagram (replace PNG) | High | Signature diagram must be editorial SVG per spec |
| **P1** | Generate WebP/AVIF variants for all HAOMTGV assets via pipeline | Medium | Performance, responsive images |
| **P2** | Add missing CSS animations (`ls-hero-float`, `ls-hero-breathe`, `ls-hero-drop`, `ls-hero-draw`, `ls-hero-slide`) to `src/index.css` | Medium | Blueprint hero animations won't run |
| **P2** | Implement mobile collapse (< 1024px) for Blueprint hero | Medium | Responsive requirement |
| **P3** | Align Blueprint hero palette with brand tokens or document divergence | Low | Consistency |

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

## Conclusion

The HAOMTGV implementation is **functional but incomplete**:

1. **Core sections work** (HAOMTGVSection, HAOMTGVPage, HaomtgvGlyphGallery, HaomtgvInfographic) — they render, use brand tokens, follow homepage sequence.
2. **Blueprint hero is broken** — missing `layers.ts` and CSS animations.
3. **Signature diagram is raster (PNG)** — should be editorial SVG per Media Architecture.
4. **Asset pipeline incomplete** — missing WebP/AVIF variants, glyph SVGs likely missing.
5. **No test coverage** — zero tests in `tests/` for any HAOMTGV component.

**Recommendation:** Fix P0 items first (layers.ts, verify glyph SVGs), then address asset pipeline, then consider whether Blueprint hero should replace or supplement current HAOMTGVPage hero.
