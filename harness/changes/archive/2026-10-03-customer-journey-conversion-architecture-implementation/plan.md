---
title: "Customer Journey Conversion Architecture — Implementation Plan"
---

# Plan

## Phase 0: Foundation & Setup (Sequential)

| Task | Agent | Verification |
|------|-------|--------------|
| 0.1 Load ls-design-system; verify brand tokens | Creative Director | Brand token audit pass |
| 0.2 Initialize Wayfinder map with child tickets | ECL Harness Engineer | Map issue + all child tickets created |
| 0.3 Create sector-registry.ts from siteContent.ts sectors | Registry Owner | New registry file with 5 sectors, PROVEN/CURRENT/DEMO/FUTURE tiers |
| 0.4 Set up analytics server endpoint /api/journey-events | Lead Frontend Engineer | Endpoint accepts POST with event schema |

## Phase 1: Homepage Journey Architecture (Parallel - 3 agents)

| Task | Agent | Blocking | Verification |
|------|-------|----------|--------------|
| 1.1 Add Homepage Solutions Beat (Beat 6) | Frontend Design Lead | 0.1-0.4 | New section renders between Workforce/Sectors |
| 1.2 Progressive Disclosure Layer Audit | UX Research Lead | 0.1-0.4 | Layer map documented; Layer 4 explicit |
| 1.3 HeroSection Metrics Rewire + "100% Auditable" Qualification | Frontend Design Lead | 0.1-0.4 | Chips from metrics.ts; honesty badge on claim |
| 1.4 ChapterRail Update | Frontend Design Lead | 1.1 | Chapter labels include new Solutions beat |
| 1.5 ls-artifact-qa on HomePage | Artifact QA Gatekeeper | 1.1-1.4 | Visual/Brand/UX/Accessibility/Content PASS |

## Phase 2: Solutions & Sectors Cross-Linking (Parallel - 3 agents)

| Task | Agent | Blocking | Verification |
|------|-------|----------|--------------|
| 2.1 Rewrite SectorsPage to consume sector-registry.ts | Frontend Design Lead | 0.3 | Hard-coded SECTORS const removed; evidence tiers render |
| 2.2 SolutionsPage → Sectors cross-links | Frontend Design Lead | 0.3 | Solution cards show relevant sector badges/links |
| 2.3 SectorsPage → Solutions cross-links | Frontend Design Lead | 0.3 | Sector cards show relevant solution cards/links |
| 2.4 Problem→Solution entry points | UX Research Lead | 2.2 | "Too many manual workflows" → Business Automation path works |
| 2.5 ls-artifact-qa on SolutionsPage, SectorsPage | Artifact QA Gatekeeper | 2.1-2.4 | Visual/Brand/UX/Accessibility/Content PASS |

## Phase 3: Proof & Trust Architecture (Parallel - 3 agents)

| Task | Agent | Blocking | Verification |
|------|-------|----------|--------------|
| 3.1 ProofPage 7-section consolidation | Frontend Design Lead | 0.1-0.4 | All 7 sections render with correct anchors |
| 3.2 Contextual Proof components (ProofCard, EvidenceBadge) | Visual Storytelling Specialist | 3.1 | Reusable components on Home/Solutions/Sectors/Builder/About/Insights |
| 3.3 Evidence ladder + honesty badges | Documentation Engineer | 3.1 | Proposed/Verified/Established/Market-leading labels honest |
| 3.4 Case study re-verification | UX Research Lead | 3.1 | All workCaseStudies evidence status confirmed |
| 3.5 ls-artifact-qa on ProofPage + contextual proof pages | Artifact QA Gatekeeper | 3.1-3.4 | Visual/Brand/UX/Accessibility/Content PASS |

## Phase 4: Ask LightSpeed & Contact Journey (Parallel - 3 agents)

| Task | Agent | Blocking | Verification |
|------|-------|----------|--------------|
| 4.1 Ask LightSpeed knowledge boundary audit | UX Research Lead | 0.1-0.4 | Client-side only; no secrets; honest empty state |
| 4.2 Ask LightSpeed sector picker → canonical 5 slugs | Frontend Design Lead | 4.1 | Sector options match industries[] slugs exactly |
| 4.3 Contact 5-step flow enhancement | Frontend Design Lead | 0.1-0.4 | "Tell Us Where You Are" framing; SLA copy; Turnstile works |
| 4.4 Newsletter journey integration + /api/enquiry endpoint | Data Analytics Engineer | 4.3 | Insight→Signup→Verified→Nurture→Returning→Engagement flow |
| 4.5 ls-artifact-qa on AskLightSpeed, ContactSection | Artifact QA Gatekeeper | 4.1-4.4 | Visual/Brand/UX/Accessibility/Content PASS |

## Phase 5: Insights & Content Journey (Parallel - 3 agents)

| Task | Agent | Blocking | Verification |
|------|-------|----------|--------------|
| 5.1 InsightsPage article model + route | Frontend Design Lead | 0.1-0.4 | Article content renders; PharosSection removed; calm design |
| 5.2 InsightCategories from OFFER_FAMILIES (12 categories) | Documentation Engineer | 5.1 | 12 categories match spec; category listing works |
| 5.3 RelatedLinks cross-navigation everywhere | Documentation Engineer | 5.1 | Every content page has relevant next steps; no dead ends |
| 5.4 ls-artifact-qa on InsightsPage + article route | Artifact QA Gatekeeper | 5.1-5.3 | Visual/Brand/UX/Accessibility/Content PASS |

## Phase 6: Navigation, Analytics & Final QA (Sequential)

| Task | Agent | Blocking | Verification |
|------|-------|----------|--------------|
| 6.1 Global nav CTA: "Start a Conversation" | Frontend Design Lead | Phase 1-5 | FloatingNav primary label updated |
| 6.2 Journey instrumentation events → /api/journey-events | Data Analytics Engineer | Phase 1-5 | All event types firing with contextual metadata |
| 6.3 Accessibility + 390px responsive verification | QA Lead | Phase 1-5 | Playwright/axe pass on all 12 routes; reduced-motion audit |
| 6.4 Full ls-artifact-qa pass on ALL modified pages | Artifact QA Gatekeeper | 6.3 | Visual/Brand/UX/Accessibility/Content all PASS |
| 6.5 Route integrity tests + build validation | QA Lead | 6.4 | tsc --noEmit 0, vite build clean, vitest run all pass |
| 6.6 Close ECL change + update STATUS.md | ECL Harness Engineer | 6.5 | harness-change.ps1 close completed; INDEX.json rebuilt |

## Parallelism Strategy

- **Max 5 concurrent agents** as approved
- Phases 1-5 run in parallel after Phase 0 completes
- Phase 6 sequential (depends on all Phase 1-5)
- Each phase ends with ls-artifact-qa gate
- Wayfinder tickets updated as work completes

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Brand token drift | ls-design-system loaded first; ls-artifact-qa validates every phase |
| Metric inconsistency | All metrics from metrics.ts registry only |
| Dead-end pages | RelatedLinks cross-navigation required on every content page |
| Accessibility regressions | Automated Playwright/axe in Phase 6; manual audit each phase |
| Analytics endpoint failure | Server endpoint created in Phase 0; validated in Phase 6 |
| Scope creep | Wayfinder map boundaries enforced; out-of-scope items documented |