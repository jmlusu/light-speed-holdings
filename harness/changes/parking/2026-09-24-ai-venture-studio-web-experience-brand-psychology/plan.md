# Plan

## Approach

1. Resolve three open decisions (palette, scope, surface) with CEO.
2. If new palette: draft ADR amending ADR-020 → update `brand/tokens/*` → `scripts/sync-brand.ps1` → update `src/brand/brand-tokens.css` + theme branches in `App.tsx` / `index.css` / components / `ThreeCanvas`.
3. Implement Part 1 effects regardless of palette choice: ripple component, mist/particle hero treatment, scroll easing, reduced-motion.
4. Optional: content page for Parts 2–5 using existing section patterns.
5. Verify: `bun run lint`, `bun run build`, Playwright → `ls-artifact-qa`.

## Key Files

| Path | Role |
|------|------|
| `brand/ai_venture_studio_execution_plan.md` | Source brief |
| `docs/adr/020-client-facing-site-guiding-principles.md` | Palette authority (amend if adopting Mist/Slate) |
| `brand/tokens/brand-tokens.{json,css}` | Canonical tokens |
| `src/brand/brand-tokens.css` | SPA Tailwind `@theme` |
| `src/App.tsx`, `src/index.css` | Theme toggle + mode backgrounds |
| `src/components/ThreeCanvas.tsx` | Existing particles |
| `src/pages/HomePage.tsx` + hero components | Primary surface if restyling home |

## Plan Review

- Status: pending (parked before approval)
