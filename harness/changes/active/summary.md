---
title: "HAOMTGV blueprint hero and page wiring"
slug: "haomtgv-blueprint-hero-and-page-wiring"
status: "in_progress"
location: "active"
phase: "implemented"
intake_status: "complete"
spec_review: "complete"
plan_review: "complete"
modules:
  - "src/components/haomtgv"
  - "src/pages"
  - "src"
files:
  - "src/components/haomtgv/layers.ts"
  - "src/components/haomtgv/HaomtgvBlueprintHero.tsx"
  - "src/pages/HAOMTVGPage.tsx"
  - "src/App.tsx"
  - "src/index.css"
tags:
  - "frontend"
  - "hero"
  - "haomtgv"
validation_status: "passed"
created_at: "2026-10-16"
updated_at: "2026-10-20"
session_id: "0ae3f812-5907-4363-b033-4470d7c36b00"
owner_agent: "jmlus"
claimed_at: "2026-10-16"
---

# Summary

## Outcome

The approved HAOMTGV hero from `brand/H.A.O.M.T.G.V. CSS Blueprint.md` is implemented as a dedicated component and mounted at the top of `/haomtgv`. Seven layers now come from one shared module that both the hero and the page grid consume, and the previously dangling `/haomtgv` nav link resolves to a real route.

## Decisions

- Coexist with existing: new component at `src/components/haomtgv/HaomtgvBlueprintHero.tsx`; root `haomtgv-committed.tsx` and `src/components/home/HAOMTGVSection.tsx` are untouched.
- Hero background: CSS gradient stand-in (night-sky base with baked sunset glow). No photograph was fabricated; `backgroundImage` is an optional prop.
- Canvas: full-viewport on desktop, stacked 16:9-style composition below 1024px.
- Blueprint palette implemented verbatim as local constants (`#050B1A`, `#22D3EE`, `#2563EB`, `#FF2D55`) rather than remapping brand tokens.
- Icon set kept as the page's existing Lucide set (Brain, Bot, GitBranch, HardDrive, Wrench, ShieldCheck, TrendingUp) instead of the blueprint's User/Share2/Workflow/Database/Wrench/Shield/Gauge.
- Framing preserved: the model is not a linear pipeline — human authority runs through every layer and governance is integral, not a checkpoint.
- Animation is CSS keyframes only; no `framer-motion` dependency.

## Validation

- `npm run lint` (`tsc --noEmit --pretty false`): clean, no diagnostics.
- `npm run build`: passed. 1706 modules transformed in 11.75s; `dist/assets/index-yub0vCfh.js` 410.88 kB (gzip 109.17 kB), `dist/assets/index-BLUwSNus.css` 152.17 kB (gzip 23.23 kB), `vendor-react` 236.09 kB, `vendor-ui` 14.25 kB.
- Pre-existing build warnings unchanged: unresolved `/hero-background.jpg` and a `"file" is not a known CSS property` diagnostic from an existing arbitrary-value class.
- Not verified: rendered appearance. Playwright is not installed locally (`uv run python -c "import playwright"` → `ModuleNotFoundError`), so no screenshots were captured. Visual QA (T011) remains open.

## Known Deviations From Blueprint

- Palette: blueprint hex values used instead of `--ls-navy`/`--ls-cyan`/`--ls-red`.
- Typography: `font-display` is Arial per `brand-tokens.css`, not Inter/Sora.
- Mobile slab scale: `0.26 / 0.4 / 0.42` instead of `0.7`, because the blueprint value crops the stack.
- CTA button moved into the hero's left column; the blueprint implies it below the fold.
- Header logo and photo credit omitted — `SiteLayout` already renders the global `Header`.
- Connector lines re-anchored to the grid (fixed 40px width) instead of percentage math, which produced negative widths at `lg`.

## Next Step

- Optional: install Playwright and capture 1440×900 / 1024×768 screenshots to close T011.
- Then branch + PR for the hero (6 required checks), and decide the `job_board` baseline question before wiring Task 4's CI gate.
