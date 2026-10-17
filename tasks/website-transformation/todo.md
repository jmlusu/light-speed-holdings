# Tasks: LightSpeed Website Transformation (Nav/Route Consolidation)

Source of truth: `plan.md` (v2.0) · Governing: `docs/directives/WEBSITE TRANSFORMATION & REPOSITORY CONSOLIDATION DIRECTIVE.md` §9/§10/§34/§36/§41/§42

Status legend: `[ ]` pending · `[~]` in progress · `[x]` done · `[!]` blocked

## Phase 1 — Planning artifacts
- [x] Update `plan.md` with route dispositions + resolved decisions
- [x] Create this task list

## Phase 2 — Global shell (nav)
- [x] `src/components/FloatingNav.tsx`: 9 links → directive 8 items + AI ASSESSMENT
  - [x] Remove `Proof /proof`
  - [x] Add `Use Cases /use-cases` (order per §9: Home, What We Do, AI Company Builder, Solutions, Use Cases, Sectors, Insights, About)
  - [x] Primary CTA action = `AI ASSESSMENT` → opens ExecutiveBriefingModal (reuse)
  - [x] Preserve mobile menu, keyboard nav, a11y, theme

## Phase 3 — Route registration (`src/App.tsx`)
- [x] Add `/use-cases` → UseCasesPage
- [x] Add `/use-cases/:slug` → new UseCaseDetailPage
- [x] Add `/sectors/:slug` → new SectorDetailPage
- [x] Add `/ai-assessment` → assessment entry (reuse ExecutiveBriefingModal)
- [x] `/proof` → redirect `/use-cases`
- [x] `/ask` → redirect `/contact`
- [x] Deprecate `/architecture`, `/build`, `/offer-b`, `/offer-c`, `/offer-e` (redirect home)
- [x] `*` → NotFoundPage (replace `<Navigate to="/" />`)
- [x] `tsc --noEmit` pass (exit 0)

## Phase 4 — Footer, meta, links, email, modal rename
- [x] `SiteFooter.tsx`: remove Proof column entry + Ask LightSpeed link; add Use Cases + AI Assessment
- [x] `SiteFooter.tsx`: mailto → `info.lightspeedholdings@gmail.com` (if present)
- [x] `src/config/site.ts`: SUPPORT_EMAIL → `info.lightspeedholdings@gmail.com`
- [x] `usePageMeta.ts`: add `/ai-assessment`; fix `/proof` + `/ask` entries
- [x] `useJourneyEvents.ts`: update `/proof` + `/ask` stage map
- [x] `public/sitemap.xml`: remove `/proof`, `/ask`; add `/use-cases`, `/sectors/:slug` pattern, `/ai-assessment`
- [x] `public/robots.txt`: verify allow rules
- [x] Internal `/proof` refs → `/use-cases` (grep whole src/)
- [x] Internal `/ask` refs → `/contact` (grep whole src/)
- [x] `ExecutiveBriefingModal.tsx`: rename off retired §34 phrasing → canonical CTA language (user-facing strings → Assessment; wire format `form:'briefing'` kept for backend)
- [x] CTA registry: add/use `EXPLORE USE CASES` contextual CTA (`exploreUseCases`)
- [x] tsc exit 0 + governance 21/21 pass

## Phase 5 — ProofPage content → Use Cases
- [x] Inventory `src/pages/ProofPage.tsx` evidence content (ws-01..03, oc-01..03, te-01..06, wp-01..04, platform metrics)
- [x] Confirm case studies migrated into `src/data/registries/use-case-registry.json` (16 entries incl. ws-01/02/03 + fow-01..08; statuses LIVE/PROVEN_IN_HOUSE/PILOT/DEMONSTRATION per §10)
- [x] Confirm trust/policy evidence covered by live surfaces: WhatWeDoPage (4 gates, payment rails, sovereignty), PrivacyPage (DPA), AiCompanyBuilderSection (SHA-256, 5-tier), ProofSection home chapter (canonical metrics)
- [x] `/proof` → `/use-cases` redirect is lossless for top evidence items (ws-01/02/03 appear as filterable Use Case cards)
- [x] Keep `ProofPage.tsx` on disk but unrouted (file retained; exports still cited by claims-registry + governance.ts as evidence lineage — do NOT delete siteContent arrays)
- [x] Updated `governance.ts` registry.case-studies source to cite use-case-registry.json
- [x] tsc exit 0

## Phase 6 — Verification
- [x] `npx tsc --noEmit` — exit 0
- [x] `npm run build` (tsc + vite build) — exit 0, ~5s incremental / ~48s cold
- [x] `npx vitest run` — 38/38 pass (governance 21, companyData 17)
- [x] Browser route sweep (Playwright, http://localhost:1440): 14 primary routes 200 + correct SPA titles; `/proof`→`/use-cases`, `/ask`→`/contact`, `/architecture|/build|/offer-b|/offer-c|/offer-e`→`/`; `*` → NotFoundPage
- [x] Nav verification: FloatingNav 8-item primary + AI ASSESSMENT CTA (`href=/ai-assessment`); footer has no Proof link, has AI Assessment
- [x] Home chapter rail relabeled: 05 Proof → Use Cases, 07 Briefing → Assessment (DOM ids kept for scroll-spy)
- [x] ProofSection eyebrow: "PROOF // …" → "OPERATING METRICS // AUDITABLE EVIDENCE"; button → "Explore Use Cases"; subtext → §10 status vocabulary
- [x] ExecutiveBriefingModal on /ai-assessment: new heading present, "Executive Briefing" absent, "Boardroom Strategy Keynote" option present
- [x] Production verification: `dist/` built clean; production check deferred to Vercel deploy (no live deploy from this session)

## Phase 7 — Final report (9 sections)
- [x] Report written to `tasks/website-transformation/final-report.md`

---
*Tracking file — do not hand-edit INDEX; this is a standalone task list.*
