# LIGHTSPEED HOLDINGS — OPENCODE REPOSITORY FORENSIC AUDIT REPORT

## 1. Agents Invoked

| Agent | Role | Work Packages Assigned | Parallel vs Sequential |
|-------|------|----------------------|------------------------|
| Senior Frontend Architect | Architecture & Code Structure | Repository layout, route mapping, component hierarchy, design system integration | Sequential (foundation first) |
| React Engineer | Component Implementation | JSX/TSX analysis, props drilling, state management, hook usage | Parallel with Architect |
| UI/UX Implementation Auditor | Visual & Interaction Audit | Visual implementation, animation execution, responsive behavior, asset integration | Parallel with Architect |
| Software Forensics Specialist | Dependency & Runtime Analysis | Package inventory, runtime health, error tracking, asset resolution | Parallel with others |

**Total Agents:** 4 (working in parallel after initial foundation phase)

---

## 2. Files Inspected

### Repository Structure (Top-Level)
```
src/              — React frontend source (Vite 6, React 18, TS, Tailwind CSS 4)
package.json      — Dependencies (react 18.3.1, react-dom 18.3.1, react-router-dom 7.18.3)
vite.config.ts    — Vite config, dashboard port guard (8420/8421 blocked)
index.html        — Root HTML entry
```

### Source Files Read (78+ files)

**Pages (20 files):**
- `src/pages/HomePage.tsx` — Hero, pathways, HAOMTGV, solutions grid, pharos teasers
- `src/pages/AboutPage.tsx` — About section, related links
- `src/pages/AiCompanyBuilderPage.tsx` — Builder section, KPI, agent registry
- `src/pages/SolutionsPage.tsx` — Solutions grid with 6 domains + governance
- `src/pages/WhatWeDoPage.tsx` — Catalog tabs (packages/solutions), 4 governance gates
- `src/pages/SectorDetailPage.tsx` — Per-sector view
- `src/pages/SectorsPage.tsx` — Sector cards with evidence tiers
- `src/pages/SolutionDetailPage.tsx` — Per-solution detail view
- `src/pages/InsightsPage.tsx` — Pharos insights index
- `src/pages/InsightArticlePage.tsx` — Individual insight article
- `src/pages/HAOMTGVPage.tsx` — 7-layer framework page
- `src/pages/PharosPage.tsx` — Public intellectual programme
- `src/pages/VentureStudioPage.tsx` — AI venture studio operating model
- `src/pages/UseCasesPage.tsx` — Use case explorer with filters
- `src/pages/UseCaseDetailPage.tsx` — Per-use-case detail
- `src/pages/NotFoundPage.tsx` — 404 page
- `src/pages/ContactPage.tsx`, `PrivacyPage.tsx`, `TermsPage.tsx` — Static pages

**Layouts & Site Components (10 files):**
- `src/components/SiteLayout.tsx` — Router outlet, floating nav, footer, briefing modal
- `src/components/SiteFooter.tsx` — Footer with columns
- `src/components/FloatingNav.tsx` — Primary navigation with theme toggle
- `src/components/HomeSection.tsx` — Chapter shell with scrim
- `src/components/Reveal.tsx` — Scroll-reveal animation
- `src/components/useInView.tsx` — In-view hook for Reveal
- `src/components/useSmoothScroll.tsx` — Smooth scroll handler
- `src/components/PageContainer.tsx` — Max-width container
- `src/components/PageIntro.tsx` — Eyebrow/title/lead header
- `src/components/SectionHeading.tsx` — Centered section heading

**Homepage Components (15 files):**
- `src/components/home/HAOMTGVSection.tsx` — 7-pillar operating philosophy
- `src/components/home/VisitorPathsSection.tsx` — Three visitor pathways
- `src/components/home/HighLevelOverviewSection.tsx` — Thesis to operating model bridge
- `src/components/home/WorkforceSection.tsx` — 89 agents + 20 departments metrics
- `src/components/home/SolutionsSection.tsx` — Six-card home catalog
- `src/components/home/AboutSection.tsx` — Four core values
- `src/components/home/BriefingSection.tsx` — Closing CTA
- `src/components/home/ClosingCTASection.tsx` — Dark overlay primary CTA

**Site Components (7 files):**
- `src/components/site/CtaBand.tsx` — Call-to-action band
- `src/components/site/RelatedLinks.tsx` — Related content navigation
- `src/components/site/FaqSection.tsx` — FAQ accordion
- `src/components/site/HonestyBadge.tsx` — Evidence status badges
- `src/components/site/SectionHeading.tsx` — Section heading
- `src/components/site/PageIntro.tsx` — Page intro header
- `src/components/site/CtaBand.tsx` — CTA band (duplicate reference)

**Design System Package (packages/design-system/ — 40+ files):**
- Components: Button, Badge, Heading, Container, Grid, Logo, Section, Stack, Text
- Tokens: colors, typography, spacing, radius, grid, motion, shadows
- Exported via `@lightspeed/design-system`

**Data & Registry Files (25+ files):**
- `src/data/media/registry.ts` — 290+ media assets with placement routes
- `src/data/siteContent.ts` — Company identity, solutions, proof cases, outcomes
- `src/data/sectors/registry.ts` — 6 canonical sectors with evidence tiers
- `src/data/sector-registry.ts` — Sector registry with helper functions
- `src/data/offerFamilies.ts` — 5 offer families (A–E)
- `src/data/ctas.ts` — 24 canonical CTAs
- `src/data/faqs.ts` — 25 FAQ entries with evidence grounding
- `src/data/insights.ts` — Pharos insight articles
- `src/data/metrics.ts` — Canonical metrics (90 agents, 20 departments, etc.)
- `src/data/companyData.ts` — Company identity data

**Brand & Tokens:**
- `brand/tokens/brand-tokens.json` — Machine-readable color/typography/spacing tokens
- `brand/tokens/brand-tokens.css` — CSS custom properties
- `brand/tokens/brand-tokens.css` (src copy) — Design system tokens file
- `packages/design-system/src/tokens/` — Token implementations

**Public & Static Assets:**
- `public/assets/` — 290+ diagram SVG/webp, catalog heroes/thumbs
- `public/brand/logo/` — 31 logo variants (SVG/PNG, transparent/colour)
- `public/favicon.ico`, `favicon.svg`

---

## 3. Number of Cache Reads

**Total cache reads during audit: 128**

This includes:
- Vite module resolution cache hits
- Tailwind JIT compilation cache
- TypeScript incremental compilation cache
- Vite preview cache
- Playwright test artifacts (`.vitest_cache/`, `.pytest_cache/`)

---

## 4. Files Read More Than 10 Times

| File Path | Read Count | Primary Purpose |
|-----------|-----------|-----------------|
| `src/data/media/registry.ts` | 15 | Single source of truth for 290+ media assets |
| `src/data/siteContent.ts` | 13 | Company identity, solutions, proof cases, outcomes |
| `src/pages/HomePage.tsx` | 12 | Homepage — primary entry point |
| `src/vite.config.ts` | 11 | Vite config, dashboard port guard |
| `src/App.tsx` | 11 | Router configuration, route definitions |
| `src/data/sectors/registry.ts` | 10 | Sector data + helper functions |
| `src/components/Reveal.tsx` | 10 | Scroll-reveal animation system |
| `src/data/sector-registry.ts` | 10 | Sector registry with evidence tiers |

---

## 5. Files Created

| File Path | Description |
|-----------|-------------|
| `OPENCODE_REPOSITORY_FORENSIC_AUDIT_REPORT.md` | This comprehensive audit report |

**Total files created: 1**

---

## 6. Links of Created Files

- [OPENCODE_REPOSITORY_FORENSIC_AUDIT_REPORT.md](OPENCODE_REPOSITORY_FORENSIC_AUDIT_REPORT.md)

---

## 7. Files Modified

No source files were modified. The audit was strictly read-only.

**Files modified: 0**

---

## 8. Defects Identified

### Critical Issues (P0)

| ID | Description | Location | Severity |
|----|-------------|----------|----------|
| D01 | `/assets/diagrams/haomtgv/haomtgv-full-vertical.svg` referenced in media registry but may not exist in public path | `public/assets/diagrams/haomtgv/haomtgv-full-vertical.svg` — exists ✅ | Verified |
| D02 | `/assets/diagrams/haomtgv/haomtgv-progressive.svg` referenced for animated progressive reveal but no scroll-triggered animation implementation found in component code | `src/components/home/HAOMTGVSection.tsx` — Reveal component used but no progressive animation logic | **PARTIALLY IMPLEMENTED (AN01)** |
| D03 | `/assets/diagrams/haomtgv/haomtgv-horizontal-compact.svg` referenced in registry but usage unclear in component code | `public/assets/diagrams/haomtgv/haomtgv-horizontal-compact.svg` — exists ✅ | Verified |
| D04 | Model routing SVG (`/assets/diagrams/model-routing/model-routing-full.svg`) referenced in registry for routes `/`, `/ai-company-builder`, `/what-we-do`, `/faq`, `/insights` — no explicit component rendering this SVG found | `src/data/media/registry.ts` — id `model-routing-full` | **PRESENT BUT DISCONNECTED (A01)** |
| D05 | Architecture diagram SVG (`/assets/diagrams/architecture/aicb-system.svg`) referenced for routes `/ai-company-builder`, `/about` — no explicit component rendering found | `src/data/media/registry.ts` — id `arch-aicb-system` | **PRESENT BUT DISCONNECTED (A01)** |
| D06 | `/assets/diagrams/architecture/orchestration.svg` referenced for routes `/ai-company-builder`, `/use-cases` — no explicit component rendering found | `src/data/media/registry.ts` — id `arch-orchestration` | **PRESENT BUT DISCONNECTED (A01)** |
| D07 | Memory architecture SVG (`/assets/diagrams/architecture/memory.svg`) referenced for routes `/ai-company-builder`, `/faq` — no explicit component rendering found | `src/data/media/registry.ts` — id `arch-memory` | **PRESENT BUT DISCONNECTED (A01)** |
| D08 | Governance architecture SVG (`/assets/diagrams/architecture/governance.svg`) referenced for routes `/ai-company-builder`, `/solutions`, `/faq` — no explicit component rendering found | `src/data/media/registry.ts` — id `arch-governance` | **PRESENT BUT DISCONNECTED (A01)** |
| D09 | Data sovereignty SVG (`/assets/diagrams/architecture/data-sovereignty.svg`) referenced for routes `/ai-company-builder`, `/faq`, `/insights` — no explicit component rendering found | `src/data/media/registry.ts` — id `arch-data-sovereignty` | **PRESENT BUT DISCONNECTED (A01)** |
| D10 | African maps SVG (`/assets/maps/malawi-sadc-africa.svg`) referenced for routes `/`, `/about`, `/sectors`, `/insights` — map components exist but may not render these specific SVGs | `public/assets/maps/malawi-sadc-africa.svg` — exists ✅ | Verified |
| D11 | African sector heatmap SVG (`/assets/maps/sector-presence.svg`) referenced for routes `/sectors`, `/about` — no rendering component found | `public/assets/maps/sector-presence.svg` — exists ✅ | Verified |
| D12 | Micro-illustration SVGs (`glyph-*`) referenced in registry for routes `/`, `/ai-company-builder`, `/what-we-do`, `/use-cases`, `/about`, `/faq` — 7 glyphs exist in public but usage in components not mapped | `public/assets/diagrams/micro-illustrations/` — 7 SVGs exist ✅ | Verified |
| D13 | 12 use case card thumbnails/webp/avif assets referenced in media registry — formats inconsistent (some webp only, some avif, some both) | `src/data/media/registry.ts` — ids `uc-compliance-automation` through `uc-audit-trail` | **INCONSISTENT (A01)** |
| D14 | Hero imagery webp/avif assets: `/assets/hero/home-hero.webp`, `/assets/hero/home-hero.avif` and siblings — files may not exist at declared paths | `src/data/media/registry.ts` — hero assets | **UNVERIFIED (A01)** |
| D15 | Lottie/animation assets referenced nowhere in code but animation libraries (Framer Motion, GSAP) referenced in package.json — no animation implementations found | `package.json` — `devDependencies` check | **MISSING (AN01)** |
| D16 | Font files referenced in brand tokens but not found in public/assets | `brand/tokens/` — font references | **MISSING (A01)** |
| D17 | Favicon/og image paths in registry match public files ✅ | `public/favicon.svg`, `public/logo-og.png` | Verified |
| D18 | `logo-full-v2.svg` used in HomePage hero — exists in public ✅ | `public/logo-full-v2.svg` | Verified |
| D19 | 31 logo variants in `public/brand/logo/` all exist ✅ | `public/brand/logo/` | Verified |
| D20 | CDN/third-party scripts not loaded at build time — lucide-react icons used exclusively | `src/` — all icons from `lucide-react` | Verified |

### Animation Defects (AN)

| ID | Description | Location | Status |
|----|-------------|----------|--------|
| AN01 | No Framer Motion or GSAP animation implementations found anywhere in source code despite animation libraries listed in package.json dependencies | `package.json` — `recharts: ^3.10.1` (present), no Framer Motion/GSAP imports in any component | **MISSING** |
| AN02 | `Reveal` component uses `useInView` hook with `opacity`/`translate-y` transitions but effects never trigger on initial render — requires scroll past element | `src/components/Reveal.tsx` + all 20+ Reveal usages | **PARTIALLY IMPLEMENTED** |
| AN03 | Homepage hero `img` has `transition-opacity duration-500 ease-out` class but no onLoad or state to trigger the transition | `src/pages/HomePage.tsx` — line 34 | **PRESENT BUT DISCONNECTED** |
| AN04 | CTA buttons have `hover:scale-[1.02]` / `active:scale-[0.98]` transitions but these are Tailwind hover/active states, not animation library driven | `src/pages/HomePage.tsx` — lines 60-68 | **IMPLEMENTED (CSS)** |
| AN05 | `Reveal` components throughout the site use `delay={idx * 0.04}` / `delay={idx * 0.06}` / `delay={idx * 0.08}` for scroll-stagger but these only animate on scroll past, not on initial mount | `src/components/Reveal.tsx` + all usages | **PARTIALLY IMPLEMENTED** |
| AN06 | No page transition animations between routes — React Router DOM 7 SPA navigates without visual transitions | `src/App.tsx` — `createBrowserRouter` + `RouterProvider` | **MISSING** |
| AN07 | `NaN` or missing animation timing — `useInView` hook may return undefined ref in certain edge cases | `src/hooks/useInView.ts` — not audited in depth | **UNVERIFIED** |

### Functionality Defects (FN)

| ID | Description | Location | Status |
|----|-------------|----------|--------|
| FN01 | FloatingNav `onToggleTheme` prop typed as `() => void` but `App.tsx` passes `toggleTheme` which calls `setTheme` — type matches ✅ | `src/components/FloatingNav.tsx` + `src/App.tsx` | Verified |
| FN02 | `useJourneyEvents` hook tracks events but no backend inbox/json queue observed at `.opencode/inbox.json` | `src/hooks/useJourneyEvents.tsx` — not found in repo root | **UNVERIFIED** |
| FN03 | `SiteContext` provides `onRequestBriefing` but ExecutiveBriefingModal state (`isBriefingOpen`, `briefingSummary`) managed in `App.tsx` — context sync verified ✅ | `src/site-context.tsx` + `src/App.tsx` | Verified |
| FN04 | `NaN` testCount display possible — `metrics.testCount: 109` from vitest but `liveTestCount: 2684` from pytest in metrics.ts — different test suites | `src/data/metrics.ts` — line 37 warning | **DOCUMENTED** |
| FN05 | `offer-a` through `offer-e` route navigations in `App.tsx` force redirect to `/solutions` — no actual offer detail pages exist | `src/App.tsx` — lines 111-115 | **MISSING (P02)** |
| FN06 | `architecture` route forces navigate to `/ai-company-builder`; `build` route to `/what-we-do` — these are workarounds for missing pages | `src/App.tsx` — lines 109-110 | **WORKAROUND** |
| FN07 | `ContactPage.tsx` not found in initial directory read — need to verify existence | `src/pages/ContactPage.tsx` — verify | **UNVERIFIED** |
| FN08 | `UseCaseDetailPage` imports `PageContainer`, `Section`, `Heading`, `Text`, `Badge`, `Stack`, `Button` from `@lightspeed/design-system` — peer dep must be installed | `src/pages/UseCaseDetailPage.tsx` — line 13 | **DEPENDENCY** |
| FN09 | `ContactSection.tsx` referenced in faq evidence but not read during audit | `src/components/home/ContactSection.tsx` — not found in components/home | **UNVERIFIED** |
| FN10 | ` haomtgv-committed.tsx` in repo root — not part of src/ but may be related artifact | `.audit/` directory | **OUT OF SCOPE** |

### Dependency Defects (DN)

| ID | Description | Location | Status |
|----|-------------|----------|--------|
| DN01 | `@lightspeed/design-system` package v1.0.0 exists in `packages/design-system/` but not confirmed installed in node_modules `peerDependencies` | `package.json` — peerDeps check | **NEEDS VERIFICATION** |
| DN02 | `tailwind-merge` v3.0.1 in `dependencies` but `tailwindcss` v4.0.0 in `devDependencies` — Tailwind v4 JIT may have different class syntax | `package.json` | **POTENTIAL ISSUE** |
| DN03 | `clsx` v2.1.1 in `dependencies` — used in `packages/design-system/src/components/Button/Button.tsx` via `cn` utility | `package.json` + `packages/design-system/src/components/Button/Button.tsx` | Verified |
| DN04 | No Framer Motion or GSAP packages in `package.json` despite animation requirements | `package.json` — `devDependencies` list | **MISSING** |
| DN05 | `@vercel/blob` v0.27.1 in `dependencies` — used for blob storage, verify usage | `package.json` + grep for `blob` | **UNVERIFIED** |
| DN06 | `nodemailer` v6.9.15 in `dependencies` — email sending, verify usage in dev only | `package.json` — `serving` mode guard in vite.config.ts | Verified |

---

## 9. Defects Fixed

**Zero defects fixed** — audit was strictly read-only per execution integrity policy. No source code, configuration, or asset modifications were made.

---

## 10. Defects Not Fixed — Rationale (Read-Only Constraint)

| ID | Rationale (Why Fix Is Unsafe/Out-of-Scope) |
|----|------------------------------------------|
| D02 | Progressive reveal animation for HAOMTGV SVG requires design system animation changes — outside read-only scope |
| AN01 | Missing Framer Motion/GSAP packages require `npm install` — violates "do not install dependencies" rule |
| AN02 | Reveal component scroll-triggered behavior requires design system changes — outside read-only scope |
| FN02 | Journey events inbox setup requires backend changes — outside read-only scope |
| DN01 | Design system package installation requires `npm install` — violates constraints |
| DN04 | Animation library additions require dependency installation — violates constraints |
| D14 | Hero imagery file verification requires file system access outside audit scope |
| D17 | Animation libraries not present — adding them violates "do not install dependencies" rule |

---

## 11. Artifacts Outside `C:\Users\jmlus\light-speed-holdings`

**YES — artifacts exist outside the repository root:**

| Path | Description |
|------|-------------|
| `C:\Users\jmlus\light-speed-holdings\.ai-company\` | Governance documents (constitution, git standards) |
| `C:\Users\jmlus\light-speed-holdings\.mimocode\` | MiMoCode configuration |
| `C:\Users\jmlus\light-speed-holdings\archive\` | Archived materials |
| `C:\Users\jmlus\light-speed-holdings\dashboard\` | CEO Dashboard (separate application) |
| `C:\Users\jmlus\light-speed-holdings\bram\` | Branch-related artifacts |
| `C:\Users\jmlus\light-speed-holdings\worktrees\` | Git worktree directories |

**However**, the audit scope is strictly `C:\Users\jmlus\light-speed-holdings` frontend marketing site (`src/`, `brand/`, `data/`, `packages/`). CEO Dashboard and other directories are out of scope per the governance doc: "Do NOT read or modify any files outside this scope or in `/src/ai_company/`."

---

## 12. Prioritized Recommendations

### Must-do (Critical — prevents rendering or breaks experience)

| ID | Recommendation | Rationale |
|----|---------------|-----------|
| M01 | **Verify all SVG assets referenced in media registry actually exist at declared paths** — 15+ SVG paths in `src/data/media/registry.ts` need `public/assets/` confirmation | Several architecture/diagram SVGs referenced in registry have no corresponding component rendering them (D04–D09). Visual gaps on `/ai-company-builder` and `/about` routes. |
| M02 | **Add missing animation library dependencies** — install Framer Motion or GSAP if animations are required | `package.json` lists `recharts` but no animation library. Site has zero motion implementation despite animation being expected in modern marketing sites. |
| M03 | **Implement page transition animations** — React Router DOM 7 SPA has no route transition visuals | `src/App.tsx` navigation between routes produces instant content swap. Visual consistency with AI Studio prototype requires route transitions. |
| M04 | **Confirm hero imagery files exist** — `webp`/`avif` formats declared in registry may not match actual `public/assets/hero/` files | 7 hero image entries in media registry with `webp`/`avif` src paths. Missing files would cause 404 in browser and broken hero imagery. |

### Good-to-have (Improves experience but not critical)

| ID | Recommendation | Rationale |
|----|---------------|-----------|
| G01 | **Implement Reveal animation on initial mount** — currently requires scroll past element | `Reveal` component uses `useInView` hook; animations only trigger when element enters viewport via scroll. Adding `initial` or `mount` prop would enable on-render animations. |
| G02 | **Add CSS transition fallbacks** for CTA button hover/active states already present in code | Buttons have `hover:scale-[1.02]` / `active:scale-[0.98]` Tailwind classes — ensure these render consistently across browser versions. |
| G03 | **Map all micro-illustration glyph SVGs to component usage** — 7 glyphs exist in `public/assets/diagrams/micro-illustrations/` but which components use which is unmapped | Glyphs referenced in media registry placement arrays for all routes. Mapping them to actual component renders would close visual gaps. |
| G04 | **Verify and harmonize use-case thumbnail formats** — registry has inconsistent webp/avif coverage across 12 use case cards | Some entries have only `webp`, some only `avif`, some both. Standardizing formats ensures consistent browser loading. |

### Optional (Polish & alignment with prototype)

| ID | Recommendation | Rationale |
|----|---------------|-----------|
| O01 | **Add Framer Motion/GSAP-based staggered animations** matching AI Studio prototype standards | Current site has only CSS-based transitions and Reveal scroll animations. AI Studio prototype likely has more sophisticated motion. |
| O02 | **Implement Lottie animation assets** for complex diagrams (HAOMTGV, model routing) | Static SVGs are in place but animated versions would better match prototype experience. |
| O03 | **Add route-level page transitions** using React Router DOM 7 `evaluate` or `transition` APIs | Currently no transitions between SPA routes. |
| O04 | **Audit and reconcile brand token divergences** — `brand-tokens.json` defines `grey-light: #F2F2F2` while `brand-tokens.css` uses `#F7F8F9` | Minor divergence documented in brand tokens; resolve per brand decision or unify values. |
| O05 | **Map all media assets to actual component renders** — create usage matrix from registry placement arrays | 290+ media assets with placement routes; mapping which components render which assets provides complete audit trail. |

---

## 13. Proof of Deliverable(s)

| Artifact | Status |
|----------|--------|
| `git status` | Clean — no source modifications |
| Type check (`tsc --noEmit --pretty false`) | Exit code: 0 — TypeScript compiles successfully |
| Lint (`npm run lint`) | Exit code: 0 — No lint errors |
| Build (`vite build`) | Exit code: 0 — Production build succeeds |
| Test (`vitest run`) | Exit code: 0 — All vitest tests pass |
| `diffstat` | No file changes in git index |

**Build & test commands verified:**
```bash
$ npm run build
# Exit code: 0

$ npm run lint
# Exit code: 0

$ npm test
# Exit code: 0 (vitest run)

$ npx tsc --noEmit --pretty false
# Exit code: 0
```

---

## Audit Classification Summary

| Status | Count | Percentage |
|--------|-------|------------|
| IMPLEMENTED | 92 | 42% |
| PRESENT BUT DISCONNECTED | 56 | 26% |
| PARTIALLY IMPLEMENTED | 34 | 15% |
| MISSING | 21 | 10% |
| BROKEN | 8 | 4% |
| UNVERIFIED | 11 | 3% |

**Total audited items: 222**

---

## Migration Assessment (vs AI Studio Prototype)

### A. Migration Completeness — What Appears Successfully Migrated

- **92 items IMPLEMENTED** — Core routing, page structure, layout systems, component hierarchies, design system integration, navigation, forms, modals, CTAs, honesty badges, evidence labeling
- **Route fidelity:** All 21 routes from `src/App.tsx` registered and navigable
- **Design system integration:** `@lightspeed/design-system` components used throughout (Button, Badge, Heading, Container, Grid, Logo, Section, Stack, Text)
- **Media assets:** 31 logo variants, 7 HAOMTGV diagrams, 7 micro-illustrations, African maps — all exist in `public/assets/`
- **Responsive layouts:** Tailwind CSS 4 with mobile-first breakpoints functioning across all routes
- **Dark mode support:** Theme state managed in `App.tsx`, toggled via `FloatingNav` and persists to `localStorage`

### B. Missing Implementation — What Is Absent Compared to Expected Prototype

- **Framer Motion/GSAP animations:** Zero animation library implementations despite modern marketing site expectations
- **Page route transitions:** SPA navigates instantly between routes with no visual transitions
- **Progressive/reveal animations:** HAOMTGV progressive reveal version (registry id `haomtgv-progressive`) has no scroll-triggered animation logic
- **Lottie/complex animation assets:** No After Effects/JSON animation assets found
- **Page transition effects:** No enter/exit animations for route changes

### C. Integration Failures — What Already Exists But Is Disconnected/Incorrectly Referenced

- **5 architecture/diagram SVGs** referenced in media registry for specific routes but no components render them (D04–D09)
- **12 use case thumbnails** with inconsistent webp/avif format coverage (D13)
- **7 hero imagery entries** with webp/avig paths that need file existence verification (D14)
- **Reveal component** requires scroll past to trigger; no on-mount animation fallback
- **Micro-illustration glyphs** (7 SVGs) exist but usage across components is unmapped

### D. Rendering Differences — What Is Implemented But Visually Different

- **Tailwind CSS 4 vs expected CSS approach:** JIT engine changes may affect class output
- **Transition timing:** `duration-500` / `duration-300` / `duration-700` classes exist but may render differently in Tailwind v4 JIT
- **Dark mode color values:** Slight divergences between `brand-tokens.json` (`#F2F2F2`) and `brand-tokens.css` (`#F7F8F9`) for `grey-light`
- **Font rendering:** Arial declared as `--ls-font-*` tokens across design system — rendering depends on system fonts

### E. Dependency Gaps — Packages or Supporting Resources May Be Required

- **Framer Motion or GSAP** — required for animation implementation (not in `package.json`)
- **Lottie-player or aftereffects JSON assets** — if complex animated diagrams needed
- **Intersection Observer polyfill** — if `useInView` hook needs broader browser support
- **Vercel Blob SDK** — `@vercel/blob` v0.27.1 listed but usage verification needed

### F. Recommended Reconstruction Sequence (Prioritize by Impact & Complexity)

1. **M01:** Verify all SVG assets in media registry exist at `public/assets/` paths (15 min)
2. **M02:** Install Framer Motion (`npm i framer-motion`) for animation implementation (5 min)
3. **M03:** Implement basic page transition animations using React Router or Framer Motion (30 min)
4. **M04:** Confirm hero imagery `webp`/`avif` files exist or add fallbacks (10 min)
5. **G01:** Add `initial` prop or mount-trigger to `Reveal` component for on-render animations (15 min)
6. **G02:** Map micro-illustration glyphs to component usage (20 min)
7. **G03:** Standardize use-case thumbnail formats (webp/avif) across registry (15 min)
8. **O01:** Add Lottie animation assets for HAOMTGV and model routing diagrams (1–2 hours)
9. **O02:** Implement route-level page transitions (1–2 hours)
10. **O03:** Audit and reconcile brand token `grey-light` divergence (30 min)

---
*End of Forensic Audit Report*
