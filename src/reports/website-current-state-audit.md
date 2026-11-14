# Website Current State Audit: LightSpeed Holdings

**Audit Date**: November 3, 2026
**Auditor**: Lead Product Designer & Senior Frontend Architect
**Scope**: Public Marketing Website (`/app/applet`)

---

## 1. Executive Summary & Application Boundary

The public marketing website for **LightSpeed Holdings Limited™** (`/app/applet`) is built on React 18, TypeScript, Vite 6, Tailwind CSS v4, and `react-router-dom` v7. The marketing application boundary is cleanly isolated from internal administrative planes (such as the J.A.R.V.I.S. CEO control plane and internal runtime databases).

The marketing experience is structured into four primary destinations:
1. **Home (`/`)**: 12-stage progressive narrative covering identity, HAOMTGV architecture, Calm Intelligence, visitor pathways, practice area carousel, 5-tier governance matrix, searchable 90-agent workforce registry, applications, research highlights, company overview, FAQ, and engagement CTAs.
2. **What We Do (`/what-we-do`)**: Detailed capability breakdown across 6 core practice areas and commercial offer families A–E, with honesty status badges (*Fieldable in 2026*, *In Active Development*), dual-currency MWK/USD pricing notes, and G1–G4 governance gates.
3. **Pharos (`/insights` & `/insights/:slug`)**: Executive research and thought-leadership hub presenting foundational whitepapers, policy briefs, and canonical essays with full modal readers and article pages.
4. **Who We Are (`/about`)**: Company identity, approved mission and vision, founder bio (Founder & CEO Jack Mlusu), and operating principles.

---

## 2. Router & Entry Point Audit

### Entry Point
- **HTML Entry**: `/index.html` (Title: `LIGHTSPEED HOLDINGS LIMITED™ — ASPIRE. ACT. ACHIEVE.`)
- **Mount Point**: `/src/main.tsx`
- **Root Component**: `/src/App.tsx`
- **Layout Wrapper**: `/src/components/SiteLayout.tsx`

### Active Primary Routes (`src/App.tsx`)
| Path | Component | Status | Purpose |
| :--- | :--- | :--- | :--- |
| `/` | `HomePage.tsx` | Production | Primary marketing narrative |
| `/what-we-do` | `WhatWeDoPage.tsx` | Production | Practice areas & offer families A–E |
| `/insights` | `InsightsPage.tsx` | Production | Pharos research hub & whitepapers |
| `/insights/:slug` | `InsightArticlePage.tsx` | Production | Pharos essay reader |
| `/about` | `AboutPage.tsx` | Production | Mission, vision & leadership |
| `/contact` | `ContactPage.tsx` | Production | Contact & engagement pathway |
| `/haomtgv` | `HAOMTGVPage.tsx` | Production | HAOMTGV 7-layer framework deep dive |
| `/ai-assessment` | `AiAssessmentPage.tsx` | Production | AI readiness assessment wizard |
| `/legal/privacy` | `PrivacyPage.tsx` | Production | Privacy Policy |
| `/legal/terms` | `TermsPage.tsx` | Production | Terms of Service |

---

## 3. Navigation & CTA Contract Audit

- **Header / Floating Navigation**: `FloatingNav.tsx`
  - Links: `Home` (`/`), `What We Do` (`/what-we-do`), `Pharos` (`/insights`), `Who We Are` (`/about`).
  - Persistent CTA: `ENGAGE LIGHTSPEED` (`/contact`).
  - Theme Switcher: Sun/Moon button toggling `.dark` class on `document.documentElement` and persisting in `localStorage`.
  - Mobile Menu: Accessible modal drawer with escape key listener and focus trap.

- **Footer**: `SiteFooter.tsx`
  - Group 1: PLATFORM (Home, What We Do, HAOMTGV Framework)
  - Group 2: KNOWLEDGE (Pharos Research, Who We Are, FAQ)
  - Group 3: ENGAGEMENT (Contact Us, Ask LightSpeed, ENGAGE LIGHTSPEED)
  - Group 4: LEGAL (Privacy Policy, Terms of Service)

---

## 4. Observed Technical Debt & Recommendations

1. **Observed Fact**: All legacy routing redirects (such as `/solutions`, `/use-cases`, `/sectors`) resolve cleanly to `/what-we-do`.
2. **Observed Fact**: `compile_applet` and `lint_applet` pass with 0 errors.
3. **Recommendation**: Continue maintaining the strict 4-destination top bar contract without adding secondary pill tags or clutter to the header wordmark.
