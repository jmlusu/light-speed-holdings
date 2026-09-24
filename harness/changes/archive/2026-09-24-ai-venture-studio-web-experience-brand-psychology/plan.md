# Plan

## Approach

1. ~~Resolve three open decisions~~ **Done (2026-09-24):** keep navy/red/cyan; Part 1 only; restyle existing home; hero mist = CSS gradients (option A).
2. **No palette/ADR/token changes** — ADR-020 remains authority.
3. Implement Part 1 effects on home chrome:
   - Ripple CSS (`.ripple-on`) on nav, home cards/pills, CtaBand (scale-safe), UseCaseCatalog tabs.
   - `HeroMist` CSS layer in `HeroSection` (low-alpha cyan/navy; reduced-motion + mobile gates).
   - `Reveal` ease → `cubic-bezier(0.25, 1, 0.5, 1)`; small rAF scroll helper for in-page anchors.
   - `@media (prefers-reduced-motion: reduce)` in `index.css`.
4. Leave `ThreeCanvas` unchanged (site-wide constellation ≠ mist).
5. Verify: `bun run lint`, `bun run test`, `bun run build`, Playwright → `ls-artifact-qa`, `lint-ecl.ps1`.

## Key Files

| Path | Role |
|------|------|
| `brand/ai_venture_studio_execution_plan.md` | Source brief (Part 1 only) |
| `docs/adr/020-client-facing-site-guiding-principles.md` | Palette authority — **not amended** |
| `src/index.css` | Ripple, mist, reduced-motion |
| `src/components/effects/HeroMist.tsx` | New hero mist layer |
| `src/components/HeroSection.tsx` | Mount mist |
| `src/components/FloatingNav.tsx` | Ripple on links |
| `src/components/site/CtaBand.tsx` | Ripple on CTAs |
| `src/components/UseCaseCatalogSection.tsx` | Ripple on tabs |
| `src/pages/HomePage.tsx` | Ripple on cards/pills |
| `src/components/Reveal.tsx` | Cascade easing |
| `src/hooks/useSmoothScroll.ts` | In-page anchor bezier scroll |
| `src/components/PillarNavigationCard.tsx` | Use smooth-scroll helper |
| `src/components/ThreeCanvas.tsx` | **Untouched** |

## Plan Review

- Status: approved
- Approved by: CEO (user) 2026-09-24 — keep navy + Part 1 + home + mist option A.
