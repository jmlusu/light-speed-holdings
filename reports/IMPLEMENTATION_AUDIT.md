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
- **onboarding.py**: stale comment `127 agents` → `90 agents` claimed — **retracted**: the fix never landed in git (see Phase 5 deviation D1); `.opencode/agents/` holds exactly 90 files

### Phase 4e: §10 Solutions Enrichment + Visitor Content Review (this round)
- **`siteContent.ts`**: Added `spec` five-question block to all 6 solutions (problem, audience, changes, builds, evidence) — answers written strictly from existing capability/use-case facts, each inheriting the solution's honesty status
- **`SolutionsPage.tsx`**: Cards rebuilt as shared `SolutionCard` rendering all five §10 questions as labeled rows; grid switched to 2-col; CTA → "DISCUSS THIS SOLUTION"
- **Visitor link audit**: every `to`/`href`/nav/footer route across pages, components, and siteContent validated against the 11 valid routes — zero dead links
- **Placeholder sweep**: zero lorem/TODO/FIXME/coming-soon in any page or component
- **Test-count correction**: site claimed 2,373 regression tests; actual CI gate (`pytest -m "not e2e"`) collects **2,557** — updated in 7 locations (HomePage, ProofPage ×3, SectorsPage, HeroSection, siteContent)
- **Prohibited-tech sweep**: zero references to three.js/GSAP/framer-motion/StatCounter in src/

### Phase 5: Content Model Consolidation (§15/§17) + Honesty Tone (this round)

Commits `852b956b`, `c3a4b9cc`, `5f7f8942` — all CI green (runs 36407824642, 36413397382, 36419637777, 36424594277, 36427263763, 36429175350).

- **§17 governance registries** (`852b956b`): `src/data/governance.ts` (CONTENT_CLAIMS, single source per business fact), `leadership.ts`, `capabilities.ts`, `ctas.ts`, `faqs.ts` — each with source/owner/evidence per §17; +14 governance tests
- **Removed website leftovers** (from commit `09b0322c`, were never deleted): `AboutBand.tsx`, `BuilderSection.tsx`, `ThesisSection.tsx` — dead `HomePage` imports
- **CTA normalization**: "Start a Conversation" wired everywhere via `ctas.ts` (page heroes + contact form link); About page consumes `leadership` registry
- **§11 sectors** (`c3a4b9cc`): `src/data/sectors.ts` → canonical 9-sector registry in spec order with `SECTOR_TIERS` + `sectorTierLegend` (4 tiers); `SectorsPage` rewritten to consume it (local duplicate `SECTORS` deleted); `SectorsSection` lead updated to four-tier wording; conflict resolutions documented in-file (Central Bank → Financial Services; UNIMA + National AI Strategy → Government; Agriculture/Energy split; Telecom = demonstration; Health = future; SMEs = current; Technology = proven)
- **§13 insights** (`c3a4b9cc`): `insightCategories` (12 categories) added to `siteContent`; `InsightsPage` consumes it; `governance.ts` insights claim source updated
- **SolutionsPage** (`c3a4b9cc`): dark-mode divider `border-ls-white/10` fix
- **Honesty badge tone mapper** (`5f7f8942`): `siteContent.honestyLabel()` maps every `types.ts` HonestyBadge string to its tone; `WhatWeDoPage` Offer B/C were rendering "In active development" with a `fieldable` tone (hard-coded) — fixed; `AskLightSpeed` case-sensitive heuristic (missed `Proven in-house`, mis-toned `Published`) — replaced; Solutions tab count derived from `solutions.length` instead of hard-coded 6; +2 mapper tests
- **§22 final legacy search (website scope)**: zero hits for retired CTAs ("Book a Briefing"/"Executive Briefing" — only test guard + `ctas.ts` doc comment), old nav labels, dead routes, old agent counts (89/127/144/152), duplicate metric literals (test counts only in canonical `metrics.ts`)

### Phase 6: Browser Verification Sweep + Turnstile Secret Containment (this round)

Sweep tool: `output/playwright/site_sweep.cjs` (Playwright chromium, `reducedMotion: reduce`) — 12 routes × light/dark × desktop 1280×800 + mobile 390×844 = **48 page-loads**, checking console/page errors, horizontal overflow, `img` without `alt`, empty headings, h1 presence, theme class applied, internal link validity, HTTP status; full-page screenshots per page/theme/viewport.

- **Round 1 findings (2 unique issues)**:
  1. `h1 = 0` on `/ai-company-builder`, `/contact`, `/ask` — first heading on each was an `h2` (`SectionHeading` / `ContactSection`)
  2. Page error on `/insights`: Turnstile `Invalid input for parameter "sitekey"`
- **h1 fixes**: `SectionHeading` gained an optional `level: 'h1' | 'h2'` prop (default `h2`); `AiCompanyBuilderSection` (first heading) and `AskLightSpeed` now render `level="h1"`; `ContactSection` headline promoted `h2` → `h1`. Each promoted component is single-use (one page each) — no duplicate-h1 risk.
- **Turnstile secret containment (security)**: root cause was `.env` carrying **two** `VITE_TURNSTILE_SITE_KEY` lines — line 58 valid key (24 chars), line 67 malformed 156-char blob that embeds the `TURNSTILE_SECRET_KEY` value. `vite.config.ts` read raw env into `define.__TURNSTILE_SITE_KEY__` and `useTurnstile` fell back to `import.meta.env.VITE_TURNSTILE_SITE_KEY`, so the blob (secret included) was baked into `dist/assets/index-BxBezel6.js`.
  - Verified **0 git-tracked files** contain the secret or blob (`.env` untracked; full `git ls-files` scan = 0 hits) — leak existed only in local build output.
  - Fix: `vite.config.ts` now uses `loadEnv(mode, ...)` and injects **only** a value matching `/^[0-9a-zA-Z._-]{10,120}$/` (rejects `=`/whitespace/pasted env blocks); `useTurnstile` validates the same pattern and no longer falls back to `import.meta.env` (the fallback was the inlining path).
  - Rebuilt bundle re-scanned: **secret = 0, blob = 0, `TURNSTILE_SECRET_KEY` name = 0** across all 103 `dist/` files.
- **Round 2: 48/48 page-loads, 0 findings**; visual review of home/contact/ask/insights (light+dark, desktop+mobile) clean.

### Phase 6 addendum: Turnstile widget verification (after owner fixed `.env`)

Diagnostics (`output/playwright/turnstile_probe.cjs`, `turnstile_diag.cjs`) against preview `:4173`:

- **Bundle after rebuild**: valid 24-char sitekey present in exactly 1 file; `TURNSTILE_SECRET_KEY` name, secret value, and malformed blob all absent from all 103 `dist/` files.
- **Secret validated server-side**: `siteverify` (Cloudflare's own endpoint) with `.env` `TURNSTILE_SECRET_KEY` (line 59) returns `missing-input-response` = **secret accepted**; an invalid secret would return `invalid-input-secret`. Rotation confirmed.
- **Widget pipeline works**: Cloudflare `api.js` loads, `window.turnstile.render()` executes, official always-pass test sitekey (`1x00000000000000000000AA`) tokenizes instantly (headless and headed) → local network/browser are not the problem.
- **Real sitekey does NOT tokenize** on `localhost` (no token, no error-callback, both mounts, 15s+) → Cloudflare-side widget config, not site code. Owner checks needed: (a) sitekey on `.env` line 58 still the CURRENT widget key after rotation (a newly created widget has a new sitekey), (b) widget Hostnames allowlist must include `localhost` for local dev.
- **Newsletter widget un-hidden** (`NewsletterSignup.tsx:164`): was mounted in `className="hidden"` (`display:none`) — a managed Turnstile widget cannot execute there, so `Subscribe` (gated on `siteKey && !token`) would stay disabled forever once the key config is fixed. Now rendered visibly (`scale-90 origin-left`), consistent with `ContactSection` and `ExecutiveBriefingModal`. Pre-existing since file creation (PR #360).
- **`.env` state at handoff**: lines 57–60 correct (comment, single valid `VITE_TURNSTILE_SITE_KEY`, valid `TURNSTILE_SECRET_KEY`, `TURNSTILE_HOSTNAMES`); a second, messy duplicate `TURNSTILE_SECRET_KEY` line further down (~L67, value has whitespace + trailing junk) still exists — dotenv last-wins means it shadows line 59 for anything reading the file. Owner must delete it; `.env` is do-not-edit for agents.
- Verified again after the fix: `npm run lint` 0 errors, vitest 38/38, `npm run build` success.

### Open items (require owner action — do-not-touch files)
- **`.env` duplicate TURNSTILE_SECRET_KEY** (~L67): a second `TURNSTILE_SECRET_KEY` line with whitespace + trailing junk (~109 chars) now exists below line 59. dotenv last-wins means it shadows the valid secret on line 59 for anything reading the file (edge functions, etc.). Delete this line — keep only lines 57–60 as the canonical Turnstile config. This overwrites the earlier instruction to delete “VITE_TURNSTILE_SITE_KEY” line 67 (that duplicate was already removed; the current duplicate is a secret line).
- **Newsletter widget**: the Turnstile container at `NewsletterSignup.tsx:164` is now rendered visibly (`className="scale-90 origin-left"` per the fix in this session), consistent with `ContactSection` and `ExecutiveBriefingModal`. The prior `className="hidden"` prevented the widget from executing.
- **Turnstile secret**: rotate the Cloudflare secret if this machine's `dist/` was ever deployed anywhere (Vercel builds from a clean checkout do not read local `.env`, so exposure risk is local-manual-deploy only).

### Verification (latest, after Phase 6)
- ✅ `npm run lint` (`tsc --noEmit`) — 0 errors
- ✅ `npm test` (vitest) — 38/38 (17 companyData + 21 governance)
- ✅ `npm run build` — success (510.84 KB JS / 141.45 KB CSS; known >500 kB Rollup warning from `public-agent-registry.json`, code-splitting candidate)
- ✅ **Browser sweep** (`site_sweep.cjs` vs preview :4173) — 48/48 loads, 0 findings; screenshots reviewed
- ✅ **Bundle secret scan** — Turnstile secret/blob absent from all `dist/` files; 0 tracked files affected
- ✅ `uv run pytest --collect-only -q` — 2,557 tests (67 e2e deselected)
- ✅ Zero `@ts-nocheck` in `src/`
- ✅ Zero dead route references (`/technology`, `/how-we-help`, `/events`, `/leadership`, `/faq`, `/trust`, `/news`, `/resources`, `/evidence`, `/industries`, `/offerings`, `/solutions/:slug`)
- ✅ Canonical agent count 90 everywhere in website `src/` (no 89/127/144/152)
- ✅ Agent count source of truth: 90 files in `.opencode/agents/`
- ✅ CI `ls-mem-phase3`: all 6 runs this session green

### Deviations (Phase 5)
- **D1** — `src/ai_company/hr/onboarding.py:6` docstring still says `<5s for 127 agents`; Phase 4d claim that this was fixed is retracted (never committed). Not edited: `hr/` is on the do-not-touch list for this session. Recommended: one-word fix `127` → `90` when `hr/` owner approves.
- **D2** — `src/ai_company/dashboard/**` uses "Executive Briefing" for an internal command-center widget; unrelated to the retired website CTA, intentionally retained (internal product terminology, never rendered publicly).
- **D3** — `metrics.ts` `metrics.testCount = 17` now stale (suite is 38) and `sectorStats` unused; zero-import file, left as-is (out of scope, documented).

### MASTER_SPEC Section → Implementation Map
| Spec | Section | Status |
|------|---------|--------|
| §5 | 90-agent operating model | ✅ 90 across site + registry |
| §8 | Homepage narrative | ✅ HomePage.tsx sequence |
| §10 | Solutions (5 questions per solution) | ✅ cards + detail data in siteContent; detail links → /contact |
| §11 | Sectors (evidence tiers) | ✅ canonical `src/data/sectors.ts` (9 sectors, 4 tiers, legend); SectorsPage + SectorsSection consume it |
| §12 | Proof (honesty labels) | ✅ 4-tier ladder + `Proposed` badges; metrics from registry/tests |
| §13 | Insights (categories) | ✅ canonical `siteContent.insightCategories` (12 categories) + PharosSection + newsletter |
| §14 | AskLightSpeed (public boundary) | ✅ boundary notice added; badges via `honestyLabel()` |
| §15/§17 | Content model / claims registry | ✅ governance.ts CONTENT_CLAIMS + leadership/capabilities/ctas/faqs/sectors/insights registries |
| §20–22 | Calm Intelligence design | ✅ tokens/index.css, no prohibited libs |

### Key Metrics
- **Agents**: 90 | **Departments**: 20 | **Regression tests**: 2,557 pytest / 38 vitest
- **valueCycle**: `['Strategy', 'Build', 'Govern', 'Research & Policy']`
- **Navigation**: 9 sections + Legal (Privacy, Terms) + Ask
- **Design**: #F7F8F9 light / #121518 dark; no Three.js, GSAP, video, shaders, animated counters, glassmorphism, neon, cyberpunk
