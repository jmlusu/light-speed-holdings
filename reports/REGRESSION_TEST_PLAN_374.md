# Regression Test Plan for Issue #374 — Phase 6: Full Regression + Artifact-QA Gates + 40 DoD

**Date**: 2026-10-03  
**Branch**: `feature/382-content-media-fields` (staging for #382)  
**Target**: Main branch after #381 ratification  
**ECL Change**: Customer Journey Conversion Architecture (active, Phase 6)

---

## Overview

This document outlines the complete regression test plan for Phase 6 (Wayfinder #374) of the Customer Journey Conversion Architecture implementation. All 40 Definition of Done (DoD) criteria from the specification must be verified, all `ls-artifact-qa` gates must pass on all 9 primary routes, and the build must be clean.

---

## 1. Primary Routes to Test (9 routes)

| Route | Component | Phase | QA Gate Status |
|-------|-----------|-------|----------------|
| `/` | HomePage | Phase 1 | ✅ PASS (Phase 1) |
| `/solutions` | SolutionsPage | Phase 2 | ✅ PASS (Phase 2) |
| `/sectors` | SectorsPage | Phase 2 | ✅ PASS (Phase 2) |
| `/proof` | ProofPage | Phase 3 | ✅ PASS (Phase 3) |
| `/insights` | InsightsPage | Phase 5 | ✅ PASS (Phase 5) |
| `/insights/:slug` | InsightArticlePage | Phase 5 | ✅ PASS (Phase 5) |
| `/ask` | AskLightSpeed | Phase 4 | ✅ PASS (Phase 4) |
| `/contact` | ContactPage | Phase 4 | ✅ PASS (Phase 4) |
| `/what-we-do` | WhatWeDoPage | Phase 5 | ✅ PASS (Phase 5) |
| `/about` | AboutPage | Phase 1 | ✅ PASS (Phase 1) |

---

## 2. 40 Definition of Done Criteria (from Spec §40)

### Architecture (4 criteria)
| # | Criterion | Verification Method | Expected Result |
|---|-----------|---------------------|-----------------|
| 1 | All major journey routes exist | Navigate to each route | 9 routes accessible |
| 2 | Routes logically connected | Check cross-links, RelatedLinks | No orphaned routes |
| 3 | Direct-entry routes understandable | Manual review of page intros | Clear purpose per route |
| 4 | No major page is a dead end | Crawl all links | Every page has ≥1 CTA/next step |

### Visitor Intent (3 criteria)
| # | Criterion | Verification Method | Expected Result |
|---|-----------|---------------------|-----------------|
| 5 | Each major page has clear visitor purpose | Review PageIntro lead text | Purpose stated in lead |
| 6 | Primary CTAs reflect page intent | Check primary button labels | CTA matches page goal |
| 7 | Secondary paths provide contextual exploration | Verify RelatedLinks, cross-links | ≥2 secondary paths/page |

### Solutions (3 criteria)
| # | Criterion | Verification Method | Expected Result |
|---|-----------|---------------------|-----------------|
| 8 | Solutions connect to sectors | Check sector badges/links on SolutionsPage | All 5 solutions link to sectors |
| 9 | Solutions connect to proof | Check ProofCard/EvidenceBadge usage | Proof components on SolutionsPage |
| 10 | Solutions provide clear engagement pathways | Verify CTA buttons, contact links | "Discuss This Solution" → Contact |

### Sectors (3 criteria)
| # | Criterion | Verification Method | Expected Result |
|---|-----------|---------------------|-----------------|
| 11 | Sectors connect to relevant solutions | Check solution links on SectorsPage | All 5 sectors link to solutions |
| 12 | Sector evidence represented honestly | Verify HonestyBadge on each sector | Badge matches evidence tier |
| 13 | Sector pages provide clear next actions | Check CTAs on SectorsPage | "Explore Solutions for This Sector" |

### Proof (4 criteria)
| # | Criterion | Verification Method | Expected Result |
|---|-----------|---------------------|-----------------|
| 14 | Evidence ladder implemented consistently | Check all 7 ProofPage sections | Proposed→Verified→Established→Market-leading |
| 15 | Unsupported claims not introduced | Audit all claims against registries | Zero invented metrics |
| 16 | Proof connected contextually to claims | Verify ProofCard on Home/Solutions/Sectors/Builder/About/Insights | Proof components on 7 pages |
| 17 | Canonical 90-agent count preserved | Check metrics.ts, company-registry.yaml | 90 agents everywhere |

### Insights (3 criteria)
| # | Criterion | Verification Method | Expected Result |
|---|-----------|---------------------|-----------------|
| 18 | Insights connect to relevant solutions/sectors | Check relatedSolutions/relatedSectors on articles | All 3 articles have cross-links |
| 19 | Newsletter journey works | Test signup flow | Capture → Confirm → Verified → Nurture |
| 20 | Ask LightSpeed pathway available | Check "Ask LightSpeed" links on Insights pages | Link present on all content pages |

### Ask LightSpeed (3 criteria)
| # | Criterion | Verification Method | Expected Result |
|---|-----------|---------------------|-----------------|
| 21 | Knowledge boundary respected | Test out-of-scope queries | Honest "No published match" panel |
| 22 | Unknown/out-of-bound questions handled | Test boundary step | Escalation to Contact works |
| 23 | Relevant site content discoverable | Test sector picker, solution matching | Canonical 5 slugs used |

### Contact (4 criteria)
| # | Criterion | Verification Method | Expected Result |
|---|-----------|---------------------|-----------------|
| 24 | Contact journey clear | Walk 5-step flow | Discover→Diagnose→Design→Build→Govern |
| 25 | Form has appropriate qualification info | Check form fields | Who, org, problem, interest, next step |
| 26 | Turnstile verification works | Submit form | Challenge rendered, passes on valid |
| 27 | Submission confirmation exists | Complete submission | Success message + next steps shown |

### Conversion (4 criteria)
| # | Criterion | Verification Method | Expected Result |
|---|-----------|---------------------|-----------------|
| 28 | Engagement pathways measurable | Check journey events firing | All 12 event types POST to /api/journey-events |
| 29 | CTA interactions instrumented | Click CTAs, check network | cta_clicked events with metadata |
| 30 | Contact and newsletter events tracked | Submit forms | contact_started/completed, newsletter_started/completed |
| 31 | Post-contact transition clearly defined | Check thank you / confirmation | Clear next steps, SLA stated |

### UX (5 criteria)
| # | Criterion | Verification Method | Expected Result |
|---|-----------|---------------------|-----------------|
| 32 | Desktop journey works | Test all routes at 1280×800 | No layout breaks, all content visible |
| 33 | Mobile journey works (390px verified) | Test all routes at 390×844 (Playwright) | No horizontal overflow, touch targets ≥44px |
| 34 | Accessibility preserved (WCAG AA) | axe-core + manual audit | 0 violations AA, focus visible, contrast ≥4.5:1 |
| 35 | Progressive disclosure intact | Viewport testing | One dominant element per viewport |
| 36 | Visual design consistent with LightSpeed design system | Brand token audit | Navy #070A40, Red #E63946, Cyan #00BFFF, Arial, 4px grid |

---

## 3. ls-artifact-qa Gates (5 checks per route)

Each route must pass all 5 gates:

| Gate | Check | Tool |
|------|-------|------|
| Visual | No overflow, proper spacing, hierarchy, balance, contrast, whitespace, alignment | Playwright screenshots + visual diff |
| Brand | Colors, type, logo, tagline match design system | Token audit + visual check |
| UX | CTA clarity, no overflow, navigation works, responsive, mobile | Playwright interaction tests |
| Accessibility | Contrast, alt text, focus, headings, ARIA | axe-core + manual |
| Content | Claims have citations, consistency, grammar, numbers accurate | Manual review + registry cross-check |

---

## 4. Technical Validation

| Check | Command | Expected Exit Code |
|-------|---------|-------------------|
| TypeScript compile | `bun run lint` (tsc --noEmit) | 0 (except pre-existing App.tsx errors) |
| Vite build | `bun run build` | 0 |
| Test suite | `bun run test` (vitest run) | 0 (38 tests pass) |
| Route smoke test | Playwright navigation to all 9 routes | All 200 OK |
| WCAG AA + 390px | Playwright + axe on all routes | 0 violations |

---

## 5. Journey Event Verification

All 12 event types must POST to `/api/journey-events` with 201:

| Event Type | Trigger Pages | Metadata Required |
|------------|---------------|-------------------|
| page_view | All routes | route, journey_stage |
| solution_view | /solutions, /what-we-do | solution, journey_stage |
| sector_view | /sectors | sector, journey_stage |
| proof_view | /proof | journey_stage |
| insight_view | /insights, /insights/:slug | slug, contentType |
| ask_started | /ask | journey_stage |
| ask_completed | /ask | journey_stage |
| newsletter_started | /insights, /insights/:slug, /contact | journey_stage |
| newsletter_completed | /contact (after verification) | journey_stage |
| contact_started | /contact (step 1) | journey_stage |
| contact_completed | /contact (submit) | journey_stage |
| cta_clicked | All CTA buttons | route, cta_label |

---

## 6. #382 Media Fields — Implementation Status (Staging Branch)

The following ContentMedia fields have been added behind feature flag `VITE_CONTENT_MEDIA_ENABLED`:

### Type Definitions (`src/types.ts`)
- ✅ `ContentMedia` union type (image/video/diagram/screenshot/chart)
- ✅ `ContentMediaSet` (hero, gallery, thumbnail)
- ✅ `MediaFeatureFlag` type
- ✅ Added to all catalog interfaces

### Data Models
| File | Entities Updated | Media Fields Added |
|------|-----------------|-------------------|
| `src/data/insights.ts` | InsightArticle | hero, gallery, thumbnail + inline `media` block kind |
| `src/data/siteContent.ts` | Solution (5), GOVERNANCE_SOLUTION | hero, gallery, thumbnail |
| `src/data/sector-registry.ts` | Sector (5) | hero, gallery, thumbnail |
| `src/data/useCaseCatalogData.ts` | OFFER_FAMILIES (5), deliverables (20), ENTERPRISE_CAPABILITIES (7), CATALOG_INDUSTRIES (5), PLATFORM_SCENARIOS (8), CATALOG_PROOF_POINTS (5), CATALOG_POLICIES (3) | hero, gallery, thumbnail |

### Components Updated
| Component | Media Rendering Added |
|-----------|----------------------|
| `InsightArticlePage` | HeroMediaRenderer, GalleryMediaRenderer, InlineMediaBlock |
| `SectorsPage` | SectorHeroMedia |
| `SectorsSection` (Home) | SectorThumbnailMedia |
| `SolutionsPage` | SolutionHeroMedia |
| `SolutionsSection` (Home) | SolutionThumbnailMedia |
| `WhatWeDoPage` | OfferHeroMedia, DeliverableThumbnailMedia, SolutionThumbnailMedia |
| `ProofPage` | CaseStudyHeroMedia, TrustThumbnailMedia |

### Feature Flag
All media rendering is gated behind `VITE_CONTENT_MEDIA_ENABLED` environment variable. Default: `false` (disabled). Enable in `.env` for staging/production after #381 ratification.

---

## 7. Test Execution Checklist

### Pre-Test Setup
- [ ] Checkout `main` branch (for baseline)
- [ ] Run `bun run lint && bun run test && bun run build` — verify clean baseline
- [ ] Checkout `feature/382-content-media-fields`
- [ ] Verify all 38 tests pass
- [ ] Verify TypeScript errors only in pre-existing App.tsx (Athena components)

### Route Testing (All 9 routes, Desktop + Mobile)
- [ ] `/` — HomePage: Hero, 10 beats, ChapterRail, all sections
- [ ] `/solutions` — SolutionsPage: 5 solution cards + Governance, cross-links
- [ ] `/sectors` — SectorsPage: 5 sector cards, evidence tiers, cross-links
- [ ] `/proof` — ProofPage: 7 sections, metrics, cases, outcomes, trust, policy
- [ ] `/insights` — InsightsPage: 12 categories, 3 teasers, calm design
- [ ] `/insights/sadc-ai-opportunity` — Article: blocks, media, related, CTAs
- [ ] `/insights/agentic-ai-african-governments` — Article: blocks, media, related, CTAs
- [ ] `/insights/digital-to-ai-native-transformation` — Article: blocks, media, related, CTAs
- [ ] `/ask` — AskLightSpeed: sector picker, boundary, results, CTAs
- [ ] `/contact` — ContactPage: 5-step flow, Turnstile, SLA copy
- [ ] `/what-we-do` — WhatWeDoPage: Packages tab (A-E), Solutions tab, deliverables
- [ ] `/about` — AboutPage: 90 agents, departments, governance

### ls-artifact-qa Execution
- [ ] Run `ls-artifact-qa` on each route (Visual/Brand/UX/Accessibility/Content)
- [ ] Verify 0 overflow, 0 missing alt, 0 empty headings
- [ ] Verify brand tokens on all pages
- [ ] Verify honesty badges on all claims
- [ ] Verify accessibility: contrast, focus, ARIA, reduced-motion

### Journey Events Verification
- [ ] Open DevTools Network tab
- [ ] Navigate each route, verify `page_view` POST 201
- [ ] Click solution/sector cards, verify `solution_view`/`sector_view`
- [ ] Submit Contact form, verify `contact_started`/`contact_completed`
- [ ] Click CTAs, verify `cta_clicked`

### Build Validation
- [ ] `bun run lint` — only pre-existing App.tsx errors
- [ ] `bun run build` — clean Vite build
- [ ] `bun run test` — 38/38 tests pass

---

## 8. Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Lead Frontend Engineer | | | |
| QA Lead | | | |
| Artifact QA Gatekeeper | | | |
| ECL Harness Engineer | | | |

---

## 9. Post-Regression Actions

1. If all criteria PASS: Close ECL change via `scripts/harness-change.ps1 close`
2. Update `STATUS.md` with completion status
3. Merge `feature/382-content-media-fields` after #381 ratification
4. Enable `VITE_CONTENT_MEDIA_ENABLED=true` in staging/production
5. Re-run ls-artifact-qa with media enabled

---

*Generated as part of Phase 6 preparation for Issue #374. All 40 DoD criteria must be verified before ECL change closure.*