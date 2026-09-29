# Implementation Audit — LightSpeed Holdings Rebuild

## Status: Phases 1–4 Complete — Spec Conformance Audit Passed

### Phase 1: Foundation & Cleanup
- **Deleted**: `src/components/StatCounter.tsx`, `src/components/ThreeCanvas.tsx`
- **Updated**: `src/brand/brand-tokens.css` — `--color-ls-mist: #F7F8F9`, `--color-ls-slate: #121518`, light/dark mode CSS variables, motion tokens
- **Rewrote**: `src/index.css` — Calm Intelligence design language, `prefers-reduced-motion`, skip-link, ambient mist, focus-visible, selection styles
- **Updated**: `package.json` — Removed `three`, `@types/three`, `recharts`, `@playwright/test`, `framer-motion`, `motion`
- **Fixed**: `siteContent.ts` — `valueCycle` → `['Strategy', 'Build', 'Govern', 'Research & Policy']`, all `89` → `90`
- **Fixed**: `useCaseCatalogData.ts`, `WhatWeDoPage.tsx` — `89` → `90`

### Phase 2: Architecture Rewrite
- **Rewrote**: `App.tsx` — 11-route router (Home, What We Do, AI Company Builder, Solutions, Sectors, Proof, Insights, About, Contact, Legal/Privacy, Legal/Terms) + Ask at `/ask` + 404 fallback
- **Rewrote**: `FloatingNav.tsx`, `SiteFooter.tsx`, `SiteLayout.tsx`, `HeroSection.tsx`
- **Created**: `src/pages/SectorsPage.tsx` (placeholder — rebuilt in Phase 4b)

### Phase 3: Page Rebuilds per MASTER_SPEC
- **HomePage.tsx**: Full rewrite per §8 narrative sequence (Orientation → Core proposition → Operating model → AI Company Builder → 90-Agent Workforce → Solutions → Sectors → Proof → Insights → About band → CTA)
- **WhatWeDoPage.tsx**: Removed industries tab; fixed dead `/solutions/:slug` links → `/contact`, relabeled "View Domain Details" → "Discuss This Domain"
- **AiCompanyBuilderSection.tsx**: Fully rebuilt — no `@ts-nocheck`, 9-step journey, 10 principles, 90-agent operating model
- **SolutionsPage.tsx**: Fixed dead `/solutions/:slug` detail links → `/contact`; dead `/technology#governance` references → AI Company Builder
- **@ts-nocheck removed** from: `AboutSection.tsx`, `ContactSection.tsx`, `AiCompanyBuilderSection.tsx` (plus deleted files). Zero `@ts-nocheck` in `src/`

### Phase 4: Dead Code Removal
- **4b — 16 dead pages deleted**: WorkPage, WhyLightSpeedPage, TrustPage, SolutionDetailPage, ResourcesPage, ProcessPage, PartnershipsPage, OutcomesPage, NewsPage, LeadershipPage, HowWeHelpPage, GeographyPage, FAQPage, EventsPage, DeliverablesPage, CareersPage
- **4c — 4 dead components deleted**: SynergyMatrix, StrategyChasmSection, PillarNavigationCard, AgentModal
- **Phase 4 earlier — 11 dead files deleted**: IndustriesPage, IndustryDetailPage, TechnologyPage, EvidencePage, OfferingsPage, UseCaseCatalogSection, TactileHardwareElements, AiCompanyBuilderOsExplorer, HaomtgvGovernanceFramework, OfferingDetailCard, CoreOfferingsSection

### Phase 4d: Spec Conformance Audit + Route Repair (this round)
- **MASTER_SPEC §10–§14 audited** against SolutionsPage, SectorsPage, ProofPage, InsightsPage, AskLightSpeed
- **Dead routes repaired across `siteContent.ts`** (route remap, labels aligned):
  - `/how-we-help#engagement`, `/how-we-help` → `/what-we-do`
  - `/technology#governance`, `/technology` → `/ai-company-builder`
  - `/events`, `/news`, `/resources` → `/insights`
  - `/leadership` → `/about`; `/faq` → `/what-we-do`; `/trust` → `/proof`
  - `relatedLinksByRoute` rebuilt: 8 valid route keys (was 6 dead + 1 duplicate)
- **ProofPage.tsx**: metric `152` → `90` (`Canonical AI Agents`, source company-registry.yaml)
- **InsightsPage.tsx**: dead RelatedLinks (`/news`, `/resources`, `/events`) → `/proof`, `/what-we-do`, `/sectors`; **§13 added** — 12 content categories (Agentic AI … AI implementation) as topic chips
- **SectorsPage.tsx**: **rebuilt per §11** — 9 spec sectors (Government, Development/donor, Health, Financial services, Agriculture, Energy, Telecommunications, SMEs, Technology), each with honest evidence text + one of 4 evidence tiers (Proven experience / Current capability / Demonstration / Future opportunity) + tier legend section
- **AskLightSpeed.tsx**: **§14 added** — public-safe knowledge boundary notice (explicit exclusion list: secrets, credentials, private prompts, internal agent instructions, client info, financial data, infrastructure details, unpublished strategy)
- **onboarding.py**: stale comment `127 agents` → `90 agents` (confirmed `.opencode/agents/` holds exactly 90 files)

### Phase 4e: §10 Solutions Enrichment + Visitor Content Review (this round)
- **`siteContent.ts`**: Added `spec` five-question block to all 6 solutions (problem, audience, changes, builds, evidence) — answers written strictly from existing capability/use-case facts, each inheriting the solution's honesty status
- **`SolutionsPage.tsx`**: Cards rebuilt as shared `SolutionCard` rendering all five §10 questions as labeled rows; grid switched to 2-col; CTA → "DISCUSS THIS SOLUTION"
- **Visitor link audit**: every `to`/`href`/nav/footer route across pages, components, and siteContent validated against the 11 valid routes — zero dead links
- **Placeholder sweep**: zero lorem/TODO/FIXME/coming-soon in any page or component
- **Test-count correction**: site claimed 2,373 regression tests; actual CI gate (`pytest -m "not e2e"`) collects **2,557** — updated in 7 locations (HomePage, ProofPage ×3, SectorsPage, HeroSection, siteContent)
- **Prohibited-tech sweep**: zero references to three.js/GSAP/framer-motion/StatCounter in src/

### Phase 6: Browser Verification Sweep + Turnstile Secret Containment (this round)

Sweep tool: `output/playwright/site_sweep.cjs` (Playwright chromium, `reducedMotion: reduce`) — 12 routes × light/dark × desktop 1280×800 + mobile 390×844 = **48 page-loads**, checking console/page errors, horizontal overflow, `img` without `alt`, empty headings, h1 presence, theme class applied, internal link validity, HTTP status; full-page screenshots per page/theme/viewport. (Sweep ran on the remediation branch carrying this fix.)

- **Round 1 findings (2 unique issues)**:
  1. `h1 = 0` on `/ai-company-builder`, `/contact`, `/ask` — first heading on each was an `h2` (`SectionHeading` / `ContactSection`)
  2. Page error on `/insights`: Turnstile `Invalid input for parameter "sitekey"`
- **h1 fixes**: `SectionHeading` gained an optional `level: 'h1' | 'h2'` prop (default `h2`); `AiCompanyBuilderSection` (first heading) and `AskLightSpeed` now render `level="h1"`; `ContactSection` headline promoted `h2` → `h1`. Each promoted component is single-use (one page each) — no duplicate-h1 risk.
- **Turnstile secret containment (security)**: root cause was `.env` carrying **two** `VITE_TURNSTILE_SITE_KEY` lines — line 58 valid key (24 chars), line 67 malformed 156-char blob that embeds the `TURNSTILE_SECRET_KEY` value. `vite.config.ts` read raw env into `define.__TURNSTILE_SITE_KEY__` and `useTurnstile` fell back to `import.meta.env.VITE_TURNSTILE_SITE_KEY`, so the blob (secret included) was baked into `dist/assets/index-BxBezel6.js`.
  - Verified **0 git-tracked files** contain the secret or blob (`.env` untracked; full `git ls-files` scan = 0 hits) — leak existed only in local build output.
  - Fix: `vite.config.ts` now uses `loadEnv(mode, ...)` and injects **only** a value matching `/^[0-9a-zA-Z._-]{10,120}$/` (rejects `=`/whitespace/pasted env blocks); `useTurnstile` validates the same pattern and no longer falls back to `import.meta.env` (the fallback was the inlining path).
  - Rebuilt bundle re-scanned: **secret = 0, blob = 0, `TURNSTILE_SECRET_KEY` name = 0** across all `dist/` files.
- **Round 2: 48/48 page-loads, 0 findings**; visual review of home/contact/ask/insights (light+dark, desktop+mobile) clean.

### Open items (require owner action — do-not-touch files)
- **`.env` line 67**: delete the malformed duplicate `VITE_TURNSTILE_SITE_KEY` line (keep line 58). Until then the sitekey is shadowed, the Turnstile widget is intentionally disabled, and the newsletter Subscribe button stays enabled (graceful degradation, `NewsletterSignup.tsx:174`).
- **Turnstile secret**: rotate the Cloudflare secret if this machine's `dist/` was ever deployed anywhere (Vercel builds from a clean checkout do not read local `.env`, so exposure risk is local-manual-deploy only).

### Verification (latest, after Phase 6)
- ✅ `npm run lint` (`tsc --noEmit`) — 0 errors
- ✅ `npm run build` — success (422.74 KB JS / 110.77 KB CSS)
- ✅ **Browser sweep** (`site_sweep.cjs` vs preview :4173, remediation branch) — 48/48 loads, 0 findings; screenshots reviewed
- ✅ **Bundle secret scan** — Turnstile secret/blob absent from `dist/`; 0 tracked files affected
- ✅ `uv run pytest --collect-only -q` — 2,557 tests (67 e2e deselected)
- ✅ Zero `@ts-nocheck` in `src/`
- ✅ Zero dead route references (`/technology`, `/how-we-help`, `/events`, `/leadership`, `/faq`, `/trust`, `/news`, `/resources`, `/evidence`, `/industries`, `/offerings`, `/solutions/:slug`)
- ✅ Canonical agent count 90 everywhere (no 89/127/144/152 in website or stale comments)
- ✅ Agent count source of truth: 90 files in `.opencode/agents/`

### MASTER_SPEC Section → Implementation Map
| Spec | Section | Status |
|------|---------|--------|
| §5 | 90-agent operating model | ✅ 90 across site + registry |
| §8 | Homepage narrative | ✅ HomePage.tsx sequence |
| §10 | Solutions (5 questions per solution) | ✅ cards + detail data in siteContent; detail links → /contact |
| §11 | Sectors (evidence tiers) | ✅ 9 sectors, 4 tiers, legend |
| §12 | Proof (honesty labels) | ✅ 4-tier ladder + `Proposed` badges; metrics from registry/tests |
| §13 | Insights (categories) | ✅ 12 categories + PharosSection + newsletter |
| §14 | AskLightSpeed (public boundary) | ✅ boundary notice added |
| §20–22 | Calm Intelligence design | ✅ tokens/index.css, no prohibited libs |

### Key Metrics
- **Agents**: 90 | **Departments**: 20 | **Regression tests**: 2,557
- **valueCycle**: `['Strategy', 'Build', 'Govern', 'Research & Policy']`
- **Navigation**: 9 sections + Legal (Privacy, Terms) + Ask
- **Design**: #F7F8F9 light / #121518 dark; no Three.js, GSAP, video, shaders, animated counters, glassmorphism, neon, cyberpunk
