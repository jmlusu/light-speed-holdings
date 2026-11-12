# Deliverable 1: Executive Reconciliation Summary

## Overall Level of Prototype Parity

The current OpenCode website (repo `src/`, Vite/React, Tailwind CSS 4, React 18) represents a **substantive implementation** of the AI Studio prototype's architecture, but with significant gaps in animations, interactive functionality, and visual fidelity. Approximately 60-65% of the original AI Studio experience is faithfully reproduced; the remaining 35-40% is partially implemented, disconnected, or intentionally redesigned per Lightspeed's "Calm Intelligence" brand direction.

## Most Significant Discrepancies

### 1. **Animations and Motion (P0 — Critical)**
- **Zero animation library implementations** despite modern marketing site expectations. The AI Studio prototype had rich motion behaviors (theme transitions, staggered reveals, scroll progress, FAB entrance, 3D icon hover, executive briefing modals, mobile drawer transitions, accordion chevron transitions, workflow simulator animations). The current OpenCode site has **only CSS-based transitions** and the `Reveal` scroll-reveal component, which requires the user to scroll past an element to trigger — no on-mount animations exist.
- **No page transition animations** between SPA routes — React Router DOM 7 navigates with instant content swap.
- The `Reveal` component uses `useInView` hook with `opacity`/`translate-y` transitions, but effects never trigger on initial render; they require scroll past the element.

### 2. **Interactive Functionality — Missing or Disconnected (P0-P1)**
- **Contact/enquiry API**: The journey events system posts to `/api/journey-events` but no backend inbox/json queue exists at `.opencode/inbox.json`. The contact form behavior is unverified.
- **Cloudflare Turnstile integration**: Present in the code but returns error `400020` on `/insights` under `vite preview` localhost — the site key hostname allowlist rejects `localhost:1440`. Production behavior is unverified.
- **Five-tier Human Approval Matrix**: The model and description exist in data (`siteContent.ts`, `metrics.ts`), but the interactive matrix component is not present on the site.
- **Five-domain AI Readiness Assessment**: Referenced in prototype but no implementation found.
- **Four-stage Contact Wizard**: No wizard component or navigation exists.
- **Pharos article reader and sharing**: The Insights page renders article cards but sharing functionality and the full reader experience are not implemented.
- **Journey telemetry**: The `useJourneyEvents` hook tracks events but posts to a non-existent backend endpoint `/api/journey-events`.
- **Before/After Workflow Simulator**: No component or interaction exists.

### 3. **Hero Imagery and Assets (P1)**
- **Hero image**: The homepage hero uses `<img src="/brand/digital/Homepage_Hero_High_fidelity.jpeg" alt="" />` with **empty alt attribute** — violates WCAG 1.1.1. The media registry declares hero imagery in webp/avif formats (`/assets/hero/home-hero.webp`, `/assets/hero/home-hero.avif`) but **these files do not exist** in `public/assets/hero/`.
- **Focus ring color**: Uses `focus-visible:ring-ls-red` instead of the design system `var(--ls-cyan)`. This is a keyboard accessibility deviation.
- **Link color on light mode**: Uses `text-ls-red` for links instead of the design system-specified `text-ls-navy` on light mode.

### 4. **Architecture Diagrams and SVG Assets (P2-P3)**
- **15+ SVG assets referenced in media registry** but have no corresponding component rendering them (D04–D09 from the previous audit). Architecture diagrams (`aicb-system`, `orchestration`, `memory`, `governance`, `data-sovereignty`) are in the registry with placement routes but no components render them.
- **Micro-illustration glyphs** (7 SVGs) exist in `public/assets/diagrams/micro-illustrations/` but **usage in components is unmapped**. The glyphs are referenced in registry placement arrays for all routes.
- **HAOMTGV progressive reveal SVG** (`haomtgv-progressive.svg`) exists but has **no scroll-triggered animation logic** — the progressive reveal behavior is unimplemented.

### 5. **Route and Page Structure (P1-P2)**
- **21 routes registered** in `App.tsx`, but several have workarounds: `architecture` → `/ai-company-builder`, `build` → `/what-we-do`, `offer-a` through `offer-e` → `/solutions`, `proof` → `/use-cases`, `ask` → `/contact`. These are acknowledged workarounds for missing pages.
- **Use case detail pages**: P1 defect confirmed — all 16 `/use-cases/<slug>` detail pages render "Use case not found" due to dual registry issue (Vite alias `@lightspeed/data/use-cases` resolves to root `data/use-cases/registry.ts` instead of `src/data/registries/use-case-registry.json`).

### 6. **Design System and Visual Fidelity (P2-P3)**
- **Tailwind CSS 4 JIT changes**: May affect class output vs. expected CSS approach.
- **Font rendering**: Arial declared as `--ls-font-*` tokens; rendering depends on system fonts.
- **Focus ring color**: Deviates from design system (see above).
- **Link color on light mode**: Uses red instead of navy per §155 of design system.

## Critical Deployment Risks

1. **P0 — Use case detail pages broken**: All 16 detail routes render "Use case not found" — this is a functional blocker for the `/use-cases` section.
2. **P0 — Hero image missing alt text**: WCAG 1.1.1 violation; will fail accessibility compliance checks.
3. **P1 — Turnstile integration unverified**: 400020 errors on localhost; production behavior unknown.
4. **P1 — Dual registry issue**: Use cases and sectors have two file trees (`root/data/` vs `src/data/`) with mismatched IDs.
5. **P2 — Focus ring accessibility**: Keyboard users see red ring instead of cyan — moderate accessibility regression.

## Primary Problem Category

The problem is **primarily missing/interconnected functionality and assets**, not architectural divergence. The core routing, page structure, layout systems, and design system integration are largely intact. The gaps are:

- **Animations**: Entirely missing animation libraries and on-mount behaviors
- **Interactive features**: Contact flow, Turnstile, journey events backend, interactive matrices/wizards
- **Assets**: Missing hero images (webp/avif), disconnected SVG diagrams, unmapped micro-illustrations
- **Visual fidelity**: Focus ring, link colors, hero alt text

## Recommended Immediate Actions

1. **Fix P0 use-case detail data source** — retarget `UseCaseDetailPage` imports to the relative `src/data/use-cases` path (same as `UseCasesPage`).
2. **Add descriptive alt text to hero image** — critical WCAG compliance.
3. **Fix focus ring color** — change `focus-visible:ring-ls-red` to `focus-visible:ring-ls-cyan`.
4. **Fix link color on light mode** — change `text-ls-red` to `text-ls-navy` for links.
5. **Verify and harmonize all SVG assets referenced in media registry** — confirm existence at `public/assets/` paths.
6. **Add missing animation library** (Framer Motion or GSAP) if animations are required per prototype standards.
7. **Verify Turnstile production behavior** on the production hostname.

*This audit was strictly read-only; no source code modifications were made.*
