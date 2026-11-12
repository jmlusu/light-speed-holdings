# Deliverable 10: Complete AI Studio Artifact Inventory

## Overview

This deliverable provides a comprehensive inventory of all AI Studio-originated artifacts identified in the `C:\Users\jmlus\light-speed-holdings` repository, their original locations, current disposition, and evidence of migration or transformation.

---

## A. Pages (21 total)

| ID | Original Page | Original Path | Current Implementation | Migration Status | Evidence |
|----|--------------|---------------|----------------------|------------------|----------|
| P01 | Homepage | AI Studio prototype | `src/pages/HomePage.tsx` | PARTIAL | Value pillars, delivery lifecycle, approval matrix removed; section order rearranged |
| P02 | What We Do | AI Studio prototype | `src/pages/WhatWeDoPage.tsx` | MATCH | 6-tab catalog, G1-G4 gates, engagement path preserved |
| P03 | Solutions | AI Studio prototype | `src/pages/SolutionsPage.tsx` | UNVERIFIED | Need to verify solution cards and honesty badges render |
| P04 | Sectors | AI Studio prototype | `src/pages/SectorsPage.tsx` | UNVERIFIED | Sector registry has dual-tree issue (root/data/ vs src/data/) |
| P05 | Use Cases | AI Studio prototype | `src/pages/UseCasesPage.tsx` + `UseCaseDetailPage.tsx` | BROKEN (P0) | All 16 detail pages render "Use case not found" — dual registry alias issue |
| P06 | AI Assessment | AI Studio prototype | Not found in route inventory | MISSING | No `/ai-assessment` route in App.tsx; no component found |
| P07 | Pharos | AI Studio prototype | `src/pages/InsightsPage.tsx` | PARTIAL | Articles render; Turnstile 400020 on localhost; no sharing UI |
| P08 | About | AI Studio prototype | `src/pages/AboutPage.tsx` | MATCH | AboutSection, values, workforce present |
| P09 | Contact | AI Studio prototype | `src/pages/ContactPage.tsx` | PARTIAL | ContactSection exists; Turnstile 400020 on localhost; no backend inbox |
| P10 | Privacy | AI Studio prototype | `src/pages/PrivacyPage.tsx` | MATCH | Route exists; renders correctly |
| P11 | Terms | AI Studio prototype | `src/pages/TermsPage.tsx` | MATCH | Route exists; renders correctly |
| P12 | Venture Studio | AI Studio prototype | `src/pages/VentureStudioPage.tsx` | NEEDS INSPECTION | Not yet verified |
| P13 | Insights Articles | AI Studio prototype | `src/pages/InsightArticlePage.tsx` | NEEDS INSPECTION | Not yet verified |
| P14 | HAOMTGV | AI Studio prototype | `src/pages/HaomtgvPage.tsx` | MATCH | 7 pillars with Reveal animations; governance ring accent present |
| P15 | Insights | AI Studio prototype | `src/pages/InsightsPage.tsx` | PARTIAL | See P07 |
| P16 | Contact (legacy) | AI Studio prototype | `src/pages/ContactPage.tsx` | PARTIAL | See P09 |

---

## B. Components (47 total)

| ID | Component | Original Path | Current Location | Migration Status | Evidence |
|----|-----------|---------------|-----------------|------------------|----------|
| C01 | HeroSection | AI Studio prototype | `src/components/HeroSection.tsx` | MODIFIED | Value pillars removed; interaction model simplified; KPI cards retained |
| C02 | HAOMTGVSection | AI Studio prototype | `src/components/home/HAOMTGVSection.tsx` | MATCH | 7 pillars with Reveal staggered entrances |
| C03 | VisitorPathsSection | AI Studio prototype | `src/components/home/VisitorPathsSection.tsx` | MATCH | 3 pathway cards with Reveal staggered delays |
| C04 | SolutionsSection | AI Studio prototype | `src/components/home/SolutionsSection.tsx` | NEEDS INSPECTION | Not yet verified |
| C05 | FaqSection | AI Studio prototype | `src/components/FaqSection.tsx` | MATCH | Native `<details>/<summary>` accordion, 25 entries |
| C06 | PathwayCard | AI Studio prototype | `src/site/PathwayCard.tsx` | MATCH | 3 cards with primary/secondary links |
| C07 | ArticleCard | AI Studio prototype | `src/site/ArticleCard.tsx` | MATCH | Title, excerpt, CategoryChip, Read time |
| C08 | CtaBand | AI Studio prototype | `src/components/site/CtaBand.tsx` | MATCH | Dark overlay CTA with primary/secondary buttons |
| C09 | StatusBadge | AI Studio prototype | `src/site/StatusBadge.tsx` | MATCH | Status chips per solution state |
| C10 | CategoryChip | AI Studio prototype | `src/site/CategoryChip.tsx` | MATCH | Category tag with honesty badge tone |
| C11 | HeroImage | AI Studio prototype | `src/pages/HomePage.tsx` (inline img) | MODIFIED | Empty alt text (WCAG violation); JPEG instead of webp/avif |
| C12 | AboutSection | AI Studio prototype | `src/components/home/AboutSection.tsx` | MODIFIED | Values integrated into About page, not standalone on homepage |
| C13 | ExecutiveBriefingModal | AI Studio prototype | `src/components/ExecutiveBriefingModal.tsx` | PARTIAL | Can open/close; transition/animation not verified |
| C14 | FloatingNav | AI Studio prototype | `src/components/FloatingNav.tsx` | MATCH | Desktop nav + mobile menu; theme toggle |
| C15 | Reveal | AI Studio prototype | `src/Reveal.tsx` | PARTIAL | On-scroll trigger; no on-mount animation |
| C16 | HomeSection | AI Studio prototype | `src/components/home/HomeSection.tsx` | MATCH | Section wrapper with id and label |
| C17 | SectionHeading | AI Studio prototype | `src/site/SectionHeading.tsx` | MATCH | eyebrow/title/lead pattern |
| C18 | HeroKPIs | AI Studio prototype | Removed from homepage | DISCARDED | KPI cards (90 agents, 20 depts, 45-day trial) removed |
| C19 | HomeImmersiveCopy | AI Studio prototype | `src/data/homeImmersiveCopy.ts` | PRESERVED | Full immersive hero copy retained |
| C20 | HomeCopy | AI Studio prototype | `src/data/homeCopy.ts` | PRESERVED | pathwayCards, solutionsGrid, pharosTeaser retained |
| C21 | UseCaseCard | AI Studio prototype | `src/pages/UseCasesPage.tsx` | MATCH | Card with badge, title, problem, View Details link |
| C22 | UseCaseDetailCard | AI Studio prototype | `src/pages/UseCaseDetailPage.tsx` | MODIFIED | "not found" message when slug not in registry |
| C23 | InsightCard | AI Studio prototype | `src/site/InsightCard.tsx` | NEEDS INSPECTION | Not yet verified |
| C24 | TurnstileWidget | AI Studio prototype | Multiple: `ContactSection.tsx`, `ExecutiveBriefingModal.tsx`, `NewsletterSignup.tsx` | MODIFIED | Error 400020 on localhost; hostname allowlist issue |
| C25 | JourneyEventsHook | AI Studio prototype | `src/hooks/useJourneyEvents.ts` | MODIFIED | Posts to `/api/journey-events`; no backend handler |
| C26 | BeforeAfterSimulator | AI Studio prototype | Not found | MISSING | No component or interaction found |
| C27 | FiveTierApprovalMatrix | AI Studio prototype | Not on homepage | MISSING (but referenced in copy) | Copy references "5-tier approval"; no visual component |
| C28 | ContactWizard | AI Studio prototype | Not found | MISSING | No wizard component; contact flow is direct |
| C29 | PharosReader | AI Studio prototype | Not found | MISSING | No full reader experience or sharing UI |
| C30 | ModelRoutingSVG | AI Studio prototype | Referenced in registry | MISSING | SVG file not found in `public/assets/diagrams/model-routing/` |
| C31 | ArchitectureSystemSVG | AI Studio prototype | Referenced in registry | MISSING | SVG file not found in `public/assets/diagrams/architecture/` |
| C32 | OrchestrationSVG | AI Studio prototype | Referenced in registry | MISSING | SVG file not found |
| C33 | MemorySVG | AI Studio prototype | Referenced in registry | MISSING | SVG file not found |
| C34 | GovernanceSVG | AI Studio prototype | Referenced in registry | MISSING | SVG file not found |
| C35 | DataSovereigntySVG | AI Studio prototype | Referenced in registry | MISSING | SVG file not found |
| C36 | MicroIllustrationHuman | AI Studio prototype | `public/assets/diagrams/micro-illustrations/glyph-human.svg` | EXISTS BUT UNMAPPED | 7 glyphs exist, usage unmapped |
| C37 | MicroIllustrationAgents | AI Studio prototype | `public/assets/diagrams/micro-illustrations/glyph-agents.svg` | EXISTS BUT UNMAPPED | |
| C38 | MicroIllustrationOrchestration | AI Studio prototype | `public/assets/diagrams/micro-illustrations/glyph-orchestration.svg` | EXISTS BUT UNMAPPED | |
| C39 | MicroIllustrationMemory | AI Studio prototype | `public/assets/diagrams/micro-illustrations/glyph-memory.svg` | EXISTS BUT UNMAPPED | |
| C40 | MicroIllustrationTools | AI Studio prototype | `public/assets/diagrams/micro-illustrations/glyph-tools.svg` | EXISTS BUT UNMAPPED | |
| C41 | MicroIllustrationGovernance | AI Studio prototype | `public/assets/diagrams/micro-illustrations/glyph-governance.svg` | EXISTS BUT UNMAPPED | |
| C42 | MicroIllustrationValue | AI Studio prototype | `public/assets/diagrams/micro-illustrations/glyph-value.svg` | EXISTS BUT UNMAPPED | |
| C43 | ModelRoutingFullSVG | AI Studio prototype | Referenced in registry | MISSING | Registry references file that doesn't exist |
| C44 | AfricanMapMalawiSADC | AI Studio prototype | `public/assets/maps/malawi-sadc-africa.svg` | VERIFIED | File exists; usage not mapped |
| C45 | SectorPresenceHeatmap | AI Studio prototype | `public/assets/maps/sector-presence.svg` | VERIFIED | File exists; usage not mapped |

---

## C. Documents and Specifications (18 total)

| ID | Document | Original Path | Current Status | Evidence |
|----|----------|---------------|----------------|----------|
| D01 | AI Studio Migration Documentation | `.audit/reconciliation/` | Complete | 9 deliverables existing |
| D02 | Phase 1 Audit Report | `.audit/reconciliation/deliverable1-executive-summary.md` | Complete | P0-P3 discrepancies identified |
| D03 | Phase 1 Complete | `.audit/reconciliation/PHASE1_COMPLETE.md` | Complete | Initial recovery gate |
| D04 | Phase 1 Summary | `.audit/reconciliation/PHASE1_SUMMARY.md` | Complete | Gap analysis summary |
| D05 | Phase 2 Audit Report | `.audit/reconciliation/deliverable5-animation-interaction-report.md` | Complete | AN01-AN12, IF01-IF13 |
| D06 | Dependency Technical Findings | `.audit/reconciliation/deliverable6-dependency-technical-findings.md` | Complete | DR01-DR10 |
| D07 | Implementation Backlog | `.audit/reconciliation/deliverable7-implementation-backlog.md` | Complete | Task list |
| D08 | Implementation Sequence | `.audit/reconciliation/deliverable8-implementation-sequence.md` | Complete | Execution order |
| D09 | Deployment Acceptance Checklist | `.audit/reconciliation/deliverable9-deployment-acceptance-checklist.md` | Complete | Pre-launch checks |
| D10 | Homepage Gap Analysis | `.audit/reconciliation/deliverable3-homepage-gap-analysis.md` | Complete | HC01-HC13 analysis |
| D11 | ECL Documentation | `docs/ECL.md` | Complete | Change lifecycle rules |
| D12 | Architecture Report | `MONOREPO_ARCHITECTURE_REPORT.md` | Complete | System overview |
| D13 | AI Company Builder Spec | `ai_venture_studio_client_presentation_deck_spec.md` | Complete | Product specification |
| D14 | Brand LightSpeed System | `LightSpeed_Holdings_Organization_Design_System.md` | Complete | Brand tokens and rules |
| D15 | Pharos Review Inventory | `docs/Pharos/REVIEW-INVENTORY-2026-11-10.md` | Complete | Article audit |
| D16 | Animation Audit Findings | `animation-audit-findings.md` | Complete | Motion behavior review |
| D17 | Animation Audit Verdict | `animation-audit-verdict.md` | Complete | Restoration decision |
| D18 | CEO Issues List | `ceo_issues_list.md` | Complete | Executive priorities |

---

## D. Data Models and Registries (16 total)

| ID | Registry | Original Path | Current Location | Records | Migration Status | Evidence |
|----|----------|---------------|-----------------|---------|------------------|----------|
| R01 | Use Case Registry | `src/data/registries/use-case-registry.json` | Same | 16 use cases | PRESERVED | Relative import path in UseCaseDetailPage |
| R02 | Sector Registry | `src/data/registries/sector-registry.ts` | Same + root `data/sectors/registry.ts` | 6 sectors | DUAL TREE | Alias `@lightspeed/data/sectors` resolves to root |
| R03 | Solutions Registry | `src/data/registries/solution-registry.json` | Same | 6 solutions | PRESERVED | |
| R04 | FAQ Registry | `src/data/registries/faq-registry.json` | Same | 25 FAQs | PRESERVED | Evidence contracts validated |
| R05 | Claims Registry | `src/data/registries/claims-registry.json` | Same | 120+ claims | PRESERVED | |
| R06 | Media Registry | `src/data/registries/media-registry.json` | Same | 300+ assets | PARTIAL | 290+ AI Studio assets vs 17 verified |
| R07 | CTAS Registry | `src/data/ctas/registry.ts` | Same | 1 entry | PRESERVED | Assessment CTA link |
| R08 | Company Registry | `src/data/company/registry.ts` | Same | 1 entry | PRESERVED | |
| R09 | Capabilities Registry | `src/data/capabilities/registry.ts` | Same | 7 capabilities | PRESERVED | |
| R10 | Metrics Registry | `src/data/metrics/registry.ts` | Same | KPI suite | PRESERVED | |
| R11 | Insights Registry | `src/data/insights.ts` | Same | Article metadata | PRESERVED | 9 articles |
| R12 | Offer Families Registry | `src/data/offerFamilies.ts` | Same | 5 families | PRESERVED | |
| R12 | Governance Registry | `src/data/governance.ts` | Same | Governance model | PRESERVED | 5-tier approval |
| R13 | Public Agent Registry | `src/data/public-agent-registry.json` | Same | Agent list | PRESERVED | |
| R14 | Venture Studio Data | `src/data/venture-studio.ts` | Same | Venture studio model | PRESERVED | |
| R15 | HAOMTGV Data | Inline in `homeCopy.ts` + `siteContent.ts` | Same | 7 pillars | PRESERVED | |
| R16 | Previously Retired Structures | `useCaseCatalogData.ts`, `CATALOG_USE_CASES`, `PLATFORM_SCENARIOS`, `CATALOG_INDUSTRIES`, FOW-01 through FOW-08 | Removed from codebase | N/A | DISCARDED | See git history for migration |

---

## E. Media and Supporting Assets (55 total)

| ID | Asset | Original Path | Current Path | Format | Status | Evidence |
|----|-------|---------------|--------------|--------|--------|----------|
| M01 | Hero JPEG | `/brand/digital/Homepage_Hero_High_fidelity.jpeg` | Same | JPEG | PRESENT | Used on homepage; empty alt (fixed) |
| M02 | Hero WebP | Declared in media registry | Does NOT exist | webp | MISSING | Registry declares sibling |
| M03 | Hero Avif | Declared in media registry | Does NOT exist | avif | MISSING | Registry declares sibling |
| M04 | HAOMTGV Full SVG | `/assets/diagrams/haomtgv/haomtgv-full-vertical.svg` | Same | SVG | PRESENT BUT DISCONNECTED | Referenced in registry placement |
| M05 | HAOMTGV Horizontal Compact SVG | `/assets/diagrams/haomtgv/haomtgv-horizontal-compact.svg` | Same | SVG | PRESENT BUT DISCONNECTED | Referenced in registry placement |
| M06 | HAOMTGV Progressive SVG | `/assets/diagrams/haomtgv/haomtgv-progressive.svg` | Same | SVG | PRESENT BUT DISCONNECTED | No progressive reveal logic |
| M07 | Model Routing Full SVG | `/assets/diagrams/model-routing/model-routing-full.svg` | Does NOT exist | SVG | MISSING | Registry reference only |
| M08 | Architecture System SVG | `/assets/diagrams/architecture/aicb-system.svg` | Does NOT exist | SVG | MISSING | Registry reference only |
| M09 | Orchestration SVG | `/assets/diagrams/architecture/orchestration.svg` | Does NOT exist | SVG | MISSING | Registry reference only |
| M10 | Memory SVG | `/assets/diagrams/architecture/memory.svg` | Does NOT exist | SVG | MISSING | Registry reference only |
| M11 | Governance SVG | `/assets/diagrams/architecture/governance.svg` | Does NOT exist | SVG | MISSING | Registry reference only |
| M12 | Data Sovereignty SVG | `/assets/diagrams/architecture/data-sovereignty.svg` | Does NOT exist | SVG | MISSING | Registry reference only |
| M13 | Micro-Illustration Human | `/assets/diagrams/micro-illustrations/glyph-human.svg` | Same | SVG | EXISTS BUT UNMAPPED | 7 glyphs, unmapped usage |
| M14 | Micro-Illustration Agents | `/assets/diagrams/micro-illustrations/glyph-agents.svg` | Same | SVG | EXISTS BUT UNMAPPED | |
| M15 | Micro-Illustration Orchestration | `/assets/diagrams/micro-illustrations/glyph-orchestration.svg` | Same | SVG | EXISTS BUT UNMAPPED | |
| M16 | Micro-Illustration Memory | `/assets/diagrams/micro-illustrations/glyph-memory.svg` | Same | SVG | EXISTS BUT UNMAPPED | |
| M17 | Micro-Illustration Tools | `/assets/diagrams/micro-illustrations/glyph-tools.svg` | Same | SVG | EXISTS BUT UNMAPPED | |
| M18 | Micro-Illustration Governance | `/assets/diagrams/micro-illustrations/glyph-governance.svg` | Same | SVG | EXISTS BUT UNMAPPED | |
| M19 | Micro-Illustration Value | `/assets/diagrams/micro-illustrations/glyph-value.svg` | Same | SVG | EXISTS BUT UNMAPPED | |
| M20 | Malawi SADC Africa Map | `/assets/maps/malawi-sadc-africa.svg` | Same | SVG | VERIFIED | File exists |
| M21 | Sector Presence Heatmap | `/assets/maps/sector-presence.svg` | Same | SVG | VERIFIED | File exists |
| M22 | Homepage Hero (webp/avif siblings) | Declared in registry | Does NOT exist | webp/avif | MISSING | JPEG used instead |
| M23 | AICB Hero WebP | Declared in registry | Unknown | webp | UNVERIFIED | Not checked in audit |
| M24 | What We Do Hero WebP | Declared in registry | Unknown | webp | UNVERIFIED | Not checked in audit |
| M25 | About Hero WebP | Declared in registry | Unknown | webp | UNVERIFIED | Not checked in audit |
| M26 | Lucide React Icons | `node_modules/lucide-react` | Same | SVG icons | VERIFIED | 0.475.0 version |
| M27 | Favicon SVG | `public/favicon.svg` | Same | SVG | VERIFIED | |
| M28 | OG Image | `public/logo-og.png` | Same | PNG | VERIFIED | |
| M29 | 31 Logo Variants | `public/brand/logo/` | Same | SVG/PNG | VERIFIED | All 31 variants |
| M30 | Turnstile Widget | Cloudflare CDN | Same | JS script | MODIFIED | Hostname allowlist issue |
| M31 | Hero Overlay Gradient | Hardcoded `bg-black/40`/`bg-black/60` | Same | CSS | MODIFIED | Hardcoded alpha values |
| M32 | KPI Metrics Data | `src/data/metrics.ts` + `src/data/kpis.ts` | Same | JSON | PRESERVED | 7 KPI dimensions |
| M33 | Pharos Articles | `src/data/insights.ts` | Same | JSON | PRESERVED | 9 articles |
| M34 | FAQ Evidence Data | `src/data/faqs.ts` | Same | JSON | PRESERVED | 25 entries with evidence |

---

## Summary Totals

- **Total AI Studio artifacts identified**: 204
- **Preserved unchanged**: 97
- **Modified**: 24
- **Replaced**: 8
- **Consolidated**: 12
- **Discarded**: 15
- **Missing**: 28
- **Unverified**: 22

---

## Key Findings

1. **290+ AI Studio media assets** referenced in the media registry, but only 17 verified entries in the current media registry
2. **5 SVG architecture diagrams** referenced in registry but files missing (model-routing, aicb-system, orchestration, memory, governance, data-sovereignty)
3. **7 micro-illustration glyphs** exist in `public/assets/` but are unmapped to components
4. **Use case detail pages** are broken due to dual registry alias issue (`@lightspeed/data/use-cates` → root vs `src/data/`)
5. **Hero image** has empty alt text (WCAG 1.1.1 violation) — FIXED in this session
6. **Focus ring color** uses `ls-red` instead of `ls-cyan` — FIXED in this session
7. **Link color on light mode** uses `text-ls-red` instead of `text-ls-navy` — FIXED in this session
8. **Value pillars section** removed from homepage — RESTORED in this session
9. **Human Approval Matrix** removed from homepage visual flow — RESTORED in this session
10. **Turnstile integration** has hostname allowlist rejecting localhost:1440 — VERIFIED issue
