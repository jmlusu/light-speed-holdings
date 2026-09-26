# Legacy Inventory — LightSpeed Holdings Website

**Date:** 2026-09-25
**Purpose:** Document the existing application architecture before structural rebuild per REBUILD_DIRECTIVE.md
**Companion:** MASTER_SPEC.md, REBUILD_DIRECTIVE.md

---

## 1. APPLICATION OVERVIEW

### Technology Stack
| Layer | Technology | Version | Status |
|-------|-----------|---------|--------|
| Framework | React | 18.3.1 | Keep |
| Build Tool | Vite | 6.1.0 | Keep |
| Language | TypeScript | 5.7.3 | Keep |
| Styling | Tailwind CSS | 4.0.0 | Modify |
| CSS | Custom CSS (~745 lines) | — | Rebuild |
| Routing | React Router DOM | 7.18.3 | Modify |
| 3D Rendering | Three.js | 0.173.0 | **DELETE** |
| Animation | framer-motion, custom CSS | — | Rebuild |
| State | React Context | — | Modify |
| Icons | lucide-react | 0.475.0 | Keep |
| Charts | recharts | 3.10.1 | **DELETE** |
| Forms | Custom + turnstile | — | Keep |

### Project Structure
```
src/
├── App.tsx                    — Main router (30+ routes)
├── main.tsx                   — Entry point
├── index.css                  — Custom CSS (745 lines, heavy legacy aesthetic)
├── types.ts                   — Type definitions (Agent, Department, KPI, etc.)
├── site-context.tsx           — React Context for theme/briefing
├── data/
│   ├── siteContent.ts         — Main content model (~1000+ lines)
│   ├── companyData.ts         — Agent/KPI/task/audit data (~360 lines)
│   └── generated/
│       └── agent-registry.public.json — 90 agents, 20 departments
├── components/
│   ├── SiteLayout.tsx         — Shared shell (canvas + nav + footer + modal)
│   ├── SiteFooter.tsx         — Footer with 7 columns, 50+ links
│   ├── FloatingNav.tsx        — Fixed nav with 6 links
│   ├── HeroSection.tsx        — Hero with StatCounter, PillarNavigationCard
│   ├── ThreeCanvas.tsx        — Three.js particle canvas (CONFLICTS WITH SPEC)
│   ├── StatCounter.tsx        — Animated counters (CONFLICTS WITH SPEC)
│   ├── AskLightSpeed.tsx      — Chat-like discovery interface
│   ├── AiCompanyBuilderSection.tsx — AI Company Builder page content
│   ├── AiCompanyBuilderOsExplorer.tsx — OS explorer component
│   ├── HaomtgvGovernanceFramework.tsx — Governance framework
│   ├── TactileHardwareElements.tsx — Industrial/mechanical UI elements
│   ├── HeroMist.tsx           — Hero ambient mist effect
│   ├── ExecutiveBriefingModal.tsx — Briefing modal
│   ├── PillarNavigationCard.tsx — Hero right-panel card
│   ├── CoreOfferingsSection.tsx — Offerings grid
│   ├── OfferingDetailCard.tsx — Offering card
│   ├── UseCaseCatalogSection.tsx — Use case catalog
│   ├── StrategyChasmSection.tsx — Strategy section
│   ├── SynergyMatrix.tsx      — Matrix visualization
│   ├── CtaBand.tsx            — CTA band
│   ├── NewsletterSignup.tsx   — Newsletter form
│   ├── Reveal.tsx             — Scroll reveal wrapper
│   ├── HonestyBadge.tsx       — Honesty status badge
│   ├── SectionHeading.tsx     — Section heading
│   ├── PageIntro.tsx          — Page intro
│   ├── RelatedLinks.tsx       — Related links
│   ├── ContactSection.tsx     — Contact form section
│   └── agent/                 — Agent modal and registry
├── pages/                     — 30+ page components
├── brand/
│   └── brand-tokens.css       — Brand design tokens (87 lines)
└── lib/                       — Validation, enquiry utilities
```

---

## 2. CLASSIFICATION OF EACH MAJOR ITEM

### KEEP (Directly compatible with MASTER_SPEC)

| Item | Rationale |
|------|-----------|
| `src/types.ts` — Agent/Department/KPI types | Type model aligns with registry-driven content model |
| `src/data/generated/agent-registry.public.json` | Canonical 90-agent registry, source of truth |
| `src/data/siteContent.ts` — Content model | Rich content data aligned with MASTER_SPEC sections |
| `src/data/companyData.ts` — KPI/task data | Useful for dashboard/admin, not public-facing |
| `src/brand/brand-tokens.css` | Brand tokens (navy/red/cyan) are valid |
| `src/site-context.tsx` | Theme context pattern is sound |
| `src/components/HonestyBadge.tsx` | Honest-status system aligns with MASTER_SPEC proof requirements |
| `src/components/Reveal.tsx` | Scroll reveal pattern is useful |
| `src/components/SectionHeading.tsx` | Reusable heading component |
| `src/components/PageIntro.tsx` | Reusable page intro component |
| `src/components/CtaBand.tsx` | CTA pattern is useful |
| `src/components/ContactSection.tsx` | Contact form component |
| `src/hooks/useInView.ts` | Intersection observer hook |
| `src/hooks/useSmoothScroll.ts` | Scroll utility |
| `src/lib/enquiry.ts` | Enquiry logic |
| `src/lib/validation.ts` | Validation utilities |
| `package.json` dependencies (React, Vite, TS, Tailwind, lucide) | Core stack is sound |
| `vite.config.ts` | Vite config is sound |
| `tsconfig.json` | TypeScript config |

### MODIFY (Useful functionality needing adaptation)

| Item | Issue | Action |
|------|-------|--------|
| `src/index.css` | 745 lines of tactile hardware/industrial/pharos CSS (machine screws, rotary dials, LED pips, chassis panels, pharos beam animation, stone masonry). Conflicts with "Calm Intelligence" design. | **Rewrite** — Remove all tactile/industrial/pharos CSS. Replace with Calm Intelligence tokens. |
| `src/components/FloatingNav.tsx` | 6 nav links don't match MASTER_SPEC's 9-section architecture. Brand text "MALAWI & SADC AI SYSTEMS" not aligned. | **Modify** — Align nav to MASTER_SPEC sections (Home, What We Do, AI Company Builder, Solutions, Sectors, Proof, Insights, About, Contact) |
| `src/components/SiteFooter.tsx` | 7 columns with 50+ links, many pointing to obsolete routes (/industries/government, /solutions/agentic-ai, /evidence, etc.). Contains "Proof & Evidence" linking to /proof but spec says "Proof" is a top-level section. | **Modify** — Align footer columns to MASTER_SPEC architecture. Remove obsolete links. |
| `src/App.tsx` — Router | 30+ routes, many obsolete (/geography, /leadership, /faq, /resources, /events, /news, /careers, /deliverables, /outcomes, /partnerships, /trust, /why, /how-we-help, /process, /offerings, /work, /evidence). `solutions`, `industries`, `offerings`, `work`, `evidence` redirect to /what-we-do. | **Rebuild** — Replace with MASTER_SPEC architecture routes. |
| `src/components/ThreeCanvas.tsx` | Three.js 3D particle canvas. MASTER_SPEC §25 says "Do not add Three.js, GSAP, video, shaders, or other heavy technologies simply because they are available." | **DELETE** — Replace with CSS-based ambient effects (HeroMist pattern is acceptable) |
| `src/components/StatCounter.tsx` | Animated counters that animate from 0 to target. MASTER_SPEC §16 says "Never use animated counters to make unsupported claims look authoritative." | **DELETE** — Replace with static values from canonical data source |
| `src/data/siteContent.ts` — valueCycle | `valueCycle: ['Strategy', 'Build', 'Govern', 'Scale']` but MASTER_SPEC §3 says `Strategy → Build → Govern → Research & Policy` | **Modify** — Correct to match MASTER_SPEC |
| `src/data/siteContent.ts` — agent count | Solutions page says "89 agents" but registry says 90. HeroSection says "90 agents". | **Modify** — Centralize to canonical 90 from agent registry |
| `src/data/siteContent.ts` — solutions data | Solutions data has hard-coded "89 agents" in one-ler and capabilities | **Modify** — Reference canonical agent count |
| `src/components/HeroSection.tsx` | Uses StatCounter (animated), has hard-coded numbers, uses "BUILD THE INTELLIGENT ENTERPRISE" headline which conflicts with MASTER_SPEC branding | **Rebuild** — Align to MASTER_SPEC homepage narrative |
| `src/data/siteContent.ts` — `company.northStar` | `northStar: 'Malawi first. Prove it. Then the world.'` — not in MASTER_SPEC as brand line | Keep as supplementary |
| `src/data/siteContent.ts` — `company.tagline` | `tagline: 'ASPIRE. ACT. ACHIEVE.'` — matches MASTER_SPEC §2 | Keep |
| `src/data/siteContent.ts` — `company.heroHeadline` | `heroHeadline: 'Build the intelligent enterprise.'` — needs alignment | Modify to match MASTER_SPEC |

### REBUILD (Structure must be recreated)

| Item | Rationale |
|------|-----------|
| `src/App.tsx` — Full router | 30+ legacy routes must be replaced with MASTER_SPEC architecture (9 sections + legal) |
| `src/components/SiteLayout.tsx` | Contains ThreeCanvas reference, ROUTE_TITLES map with 30+ entries, legacy structure |
| `src/components/SiteFooter.tsx` | Must be rebuilt with MASTER_SPEC-aligned columns |
| `src/components/FloatingNav.tsx` | Must be rebuilt with MASTER_SPEC-aligned navigation |
| `src/components/HeroSection.tsx` | Must follow MASTER_SPEC §8 homepage narrative sequence |
| `src/index.css` | Must be rewritten for Calm Intelligence design language |
| `src/brand/brand-tokens.css` | Must add #F7F8F9 (Morning Mist) and #121518 (Slate/Deep Mineral) colors per MASTER_SPEC §20 |
| All 30+ page components | Most are obsolete (CareersPage, EventsPage, ResourcesPage, DeliverablesPage, OutcomesPage, PartnershipsPage, TrustPage, GeographyPage, LeadershipPage, FAQPage, HowWeHelpPage, ProcessPage, OfferingsPage, WorkPage, EvidencePage, TrustPage). Must be removed or rebuilt. |
| `src/components/TactileHardwareElements.tsx` | Industrial/mechanical UI components (machine screws, rotary dials, LED pips) — entirely conflicts with Calm Intelligence |
| `src/components/StrategyChasmSection.tsx` | Legacy strategy visualization |
| `src/components/SynergyMatrix.tsx` | Legacy matrix visualization |
| `src/components/UseCaseCatalogSection.tsx` | Legacy catalog pattern |
| `src/components/CoreOfferingsSection.tsx` | Legacy offerings pattern |
| `src/components/PillarNavigationCard.tsx` | Legacy pillar card with hardware aesthetic |
| `src/components/HaomtgvGovernanceFramework.tsx` | Legacy governance component |
| `src/components/AiCompanyBuilderOsExplorer.tsx` | Legacy OS explorer |
| `src/components/AiCompanyBuilderSection.tsx` | 535-line legacy section |
| `src/components/AskLightSpeed.tsx` | Chat interface — MASTER_SPEC §14 says to provide AI-assisted interface but must operate against public-safe knowledge boundary |
| `src/components/ExecutiveBriefingModal.tsx` | Legacy briefing modal |
| `src/components/NewsletterSignup.tsx` | Legacy newsletter component |
| `src/components/ThreeCanvas.tsx` | Three.js canvas — DELETE |
| `src/components/StatCounter.tsx` | Animated counters — DELETE |
| `src/components/HeroMist.tsx` | Hero mist effect — Keep the concept but simplify |
| `src/data/siteContent.ts` | Content model needs restructuring to match MASTER_SPEC sections |

### DELETE (Obsolete code, pages, components, routes, styles, assets)

| Item | Rationale |
|------|-----------|
| `src/components/ThreeCanvas.tsx` | Three.js is prohibited by MASTER_SPEC §25 |
| `src/components/StatCounter.tsx` | Animated counters prohibited by MASTER_SPEC §16 |
| `src/components/TactileHardwareElements.tsx` | Industrial/mechanical aesthetic violates Calm Intelligence |
| `src/components/StrategyChasmSection.tsx` | Legacy, not in MASTER_SPEC |
| `src/components/SynergyMatrix.tsx` | Legacy, not in MASTER_SPEC |
| `src/components/UseCaseCatalogSection.tsx` | Legacy pattern |
| `src/components/CoreOfferingsSection.tsx` | Legacy pattern |
| `src/components/PillarNavigationCard.tsx` | Legacy hardware aesthetic |
| `src/components/HaomtgvGovernanceFramework.tsx` | Legacy pattern |
| `src/components/AiCompanyBuilderOsExplorer.tsx` | Legacy pattern |
| `src/components/AiCompanyBuilderSection.tsx` | Legacy 535-line section |
| `src/components/ExecutiveBriefingModal.tsx` | Legacy pattern |
| `src/components/HeroMist.tsx` | Replace with simpler CSS ambient effect |
| `src/components/NewsletterSignup.tsx` | Legacy pattern |
| `src/components/AboutSection.tsx` | Legacy pattern |
| All obsolete page routes | `/geography`, `/leadership`, `/faq`, `/resources`, `/events`, `/news`, `/careers`, `/deliverables`, `/outcomes`, `/partnerships`, `/trust`, `/why`, `/how-we-help`, `/process`, `/offerings`, `/work`, `/evidence` — All obsolete per MASTER_SPEC §7 |
| All obsolete footer links | Links to deleted routes |
| `src/components/PharosSection.tsx` (if exists) | Pharos theming conflicts with Calm Intelligence |
| `src/index.css` — All tactile hardware CSS classes | `.chassis-milled-dark`, `.flight-deck-well-dark`, `.machine-screw`, `.status-pip-container`, `.pip-led-amber`, `.pip-led-emerald`, `.pip-led-crimson`, `.pip-led-dim`, `.telemetry-tag-dark`, `.telemetry-tag-light`, `.hardware-chassis-dark`, `.hardware-well-dark`, `.tactile-concave-btn-dark`, `.tactile-concave-btn-light`, `.master-rotary-housing-dark`, `.tactile-chassis-dark`, `.tactile-btn-inactive-dark`, `.tactile-btn-active-dark`, `.analog-rotary-dial-dark`, `.pharos-beacon-beam`, `.pharos-stone-masonry`, `.ripple-on`, `.hero-mist`, `.hero-mist-blob-1` through `_6` — ~500+ lines of legacy CSS |
| `src/index.css` — Pharos keyframe animation | `@keyframes pharosSweep` |
| `src/index.css` — All tactile keyframe animation | `@keyframes telemetryPulse` |
| `src/index.css` — Mist keyframe animation | `@keyframes mistDrift` (keep simplified version) |
| `src/index.css` — All ripple-on CSS | `::after` ripple effects |
| `src/data/siteContent.ts` — `engagementModels` | Legacy engagement model data structure |
| `src/data/siteContent.ts` — `whyLightSpeed` | Legacy structure, replace with MASTER_SPEC-aligned content |
| `src/data/siteContent.ts` — `capabilityDomains` | Legacy structure with 5 domains, MASTER_SPEC specifies 4 |
| `src/data/siteContent.ts` — `clientProblems` | Legacy structure |
| `src/data/siteContent.ts` — `engagementProcess` | Legacy structure |
| `src/data/siteContent.ts` — `deliverables` | Legacy structure |
| `src/data/siteContent.ts` — `outcomeCategories` | Legacy structure |
| `src/data/siteContent.ts` — `geography` | Legacy structure |
| `src/data/siteContent.ts` — `leadership` | Legacy structure |
| `src/data/siteContent.ts` — `partnerships` | Legacy structure |
| `src/data/siteContent.ts` — `techPhilosophy` | Legacy structure |
| `src/data/siteContent.ts` — `responsibleAi` | Legacy structure |
| `src/data/siteContent.ts` — `securityTopics` | Legacy structure |
| `src/data/siteContent.ts` — `faqs` | Legacy structure |
| `src/data/siteContent.ts` — `resources` | Legacy structure |
| `src/data/siteContent.ts` — `events` | Legacy structure |
| `src/data/siteContent.ts` — `newsItems` | Legacy structure |
| `src/data/siteContent.ts` — `careers` | Legacy structure |
| `src/data/siteContent.ts` — `insightTeasers`, `insightCategories` | Legacy structure |
| `src/data/siteContent.ts` — `solutions` | Legacy structure — rebuild per MASTER_SPEC §10 |
| `node_modules/three` | Three.js dependency |
| `node_modules/recharts` | Recharts dependency (unused in public site?) |
| `node_modules/framer-motion` | If used only for legacy animations |
| `node_modules/motion` | If used only for legacy animations |
| `package.json` — `three`, `@types/three`, `recharts`, `@playwright/test` | Remove if unused for public site |

---

## 3. LEGACY DESIGN LANGUAGE ANALYSIS

### Current Design Language (CONFLICTS with MASTER_SPEC)

The current site uses a **Tactile Industrial / Pharos Lighthouse** aesthetic:

- **Chassis panels** with gradient backgrounds simulating precision-milled metal
- **Machine screws** (circular buttons with slot patterns)
- **Status LEDs** (amber, emerald, crimson, dim) with glow effects
- **Rotary dials** (conic gradient circles)
- **Flight deck wells** (recessed panel effects)
- **Telemetry tags** (monospace uppercase labels)
- **Pharos beacon beam** (rotating conic gradient sweep)
- **Stone masonry** pattern backgrounds
- **Ripple effects** on hover
- **Animated telemetry pulse** LEDs
- **Hardware chassis shadows** with multi-layer inset/outset effects

### MASTER_SPEC Required Design Language (Calm Intelligence)

- **Morning Mist / Alabaster** (#F7F8F9) for light mode
- **Slate / Deep Mineral** (#121518) for dark mode
- **Calm → Curiosity → Clarity → Confidence → Action** emotional sequence
- **Natural and architectural visual metaphors**: morning mist, slate, deep mineral, calm water, stone, light, space, reflections, subtle depth
- **Restrained motion**: slow, fluid, spatial, intentional
- **No excessive glassmorphism, neon, gradients, or animation**
- **Typography**: Arial, clean, readable
- **Color accents**: navy (#070A40), red (#E63946), cyan (#00BFFF) used deliberately

### Key Conflicts

| Legacy Pattern | Spec Requirement | Resolution |
|---------------|-----------------|------------|
| Machine screw buttons | Calm, rounded, minimal buttons | Delete all tactile hardware CSS |
| Rotary dials | No decorative gauges | Delete |
| Status LEDs | No status indicators on public site | Delete |
| Pharos sweep animation | `prefers-reduced-motion` compliant, restrained | Delete pharos animation |
| Telemetry tags | Editorial, calm typography | Delete |
| Hardware chassis shadows | Minimal, clean surfaces | Rewrite CSS |
| `#070a40` dark bg | `#121518` dark bg | Update |
| `#edf3f8` / `#f2f2f2` light bg | `#F7F8F9` light bg | Update |
| Three.js particles | CSS ambient effects only | Replace |
| Animated stat counters | Static values from canonical source | Replace |
| Glassmorphism (backdrop-blur-xl) | Restrained, calm surfaces | Reduce |

---

## 4. LEGACY ROUTE INVENTORY

### Current Routes (30+)

| Route | Page Component | MASTER_SPEC Status |
|-------|---------------|-------------------|
| `/` | HomePage | **KEEP** — Home |
| `/what-we-do` | WhatWeDoPage | **KEEP** — What We Do |
| `/proof` | ProofPage | **KEEP** — Proof |
| `/solutions` | Navigate → /what-we-do | **DELETE** — Redirect removed |
| `/solutions/:slug` | SolutionDetailPage | **REBUILD** — Under Solutions |
| `/industries` | Navigate → /what-we-do | **DELETE** — Redirect removed |
| `/industries/:slug` | IndustryDetailPage | **REBUILD** — Under Sectors |
| `/offerings` | Navigate → /what-we-do | **DELETE** |
| `/work` | Navigate → /proof | **DELETE** |
| `/evidence` | Navigate → /proof | **DELETE** |
| `/technology` | TechnologyPage | **REBUILD** — Under AI Company Builder |
| `/insights` | InsightsPage | **KEEP** — Insights |
| `/about` | AboutPage | **KEEP** — About |
| `/ai-company-builder` | AiCompanyBuilderPage | **KEEP** — AI Company Builder |
| `/ask` | AskLightSpeed | **KEEP** — Ask LightSpeed |
| `/contact` | ContactPage | **KEEP** — Contact |
| `/legal/privacy` | PrivacyPage | **KEEP** — Legal |
| `/legal/terms` | TermsPage | **KEEP** — Legal |
| `/why` | WhyLightSpeedPage | **DELETE** |
| `/how-we-help` | HowWeHelpPage | **DELETE** |
| `/how-we-help/engagement` | HowWeHelpPage | **DELETE** |
| `/process` | ProcessPage | **DELETE** |
| `/geography` | GeographyPage | **DELETE** |
| `/leadership` | LeadershipPage | **DELETE** |
| `/faq` | FAQPage | **DELETE** |
| `/resources` | ResourcesPage | **DELETE** |
| `/events` | EventsPage | **DELETE** |
| `/news` | NewsPage | **DELETE** |
| `/careers` | CareersPage | **DELETE** |
| `/deliverables` | DeliverablesPage | **DELETE** |
| `/outcomes` | OutcomesPage | **DELETE** |
| `/partnerships` | PartnershipsPage | **DELETE** |
| `/trust` | TrustPage | **DELETE** |
| `*` | Navigate → / | **KEEP** — 404 fallback |

### Routes to DELETE (20+)

`/why`, `/how-we-help`, `/how-we-help/engagement`, `/process`, `/geography`, `/leadership`, `/faq`, `/resources`, `/events`, `/news`, `/careers`, `/deliverables`, `/outcomes`, `/partnerships`, `/trust`, `/offerings`, `/work`, `/evidence`, `/solutions` (redirect), `/industries` (redirect)

### Routes to REBUILD

`/solutions/:slug`, `/industries/:slug`, `/technology`

### Routes to KEEP (9 core + legal)

`/`, `/what-we-do`, `/ai-company-builder`, `/solutions`, `/sectors`, `/proof`, `/insights`, `/about`, `/contact` + legal pages

---

## 5. LEGACY CONTENT DATA ANALYSIS

### Content Model (`siteContent.ts`)

The current `siteContent.ts` contains ~1000+ lines of content organized in these structures:

| Structure | MASTER_SPEC Alignment | Status |
|-----------|----------------------|--------|
| `company` | §2 Brand Position | **KEEP** — identity data is valid |
| `mission`, `vision` | §3 Core Operating Model | **KEEP** |
| `whyLightSpeed` | §10 Solutions | **REBUILD** — restructure per spec |
| `capabilityDomains` | §4 AI Company Builder | **REBUILD** — 5 domains → 4 capabilities |
| `clientProblems` | §10 Solutions | **REBUILD** |
| `engagementModels` | §10 Solutions | **REBUILD** |
| `engagementProcess` | §8 Homepage | **REBUILD** |
| `deliverables` | §10 Solutions | **REBUILD** |
| `outcomeCategories` | §10 Solutions | **REBUILD** |
| `geography` | §11 Sectors | **REBUILD** — align to MASTER_SPEC sectors |
| `leadership` | §29 Executive Control | **KEEP** |
| `partnerships` | §12 Proof | **REBUILD** |
| `techPhilosophy` | §26 Architecture | **REBUILD** |
| `responsibleAi` | §6 Human + AI | **REBUILD** |
| `securityTopics` | §27 Public/Internal | **REBUILD** |
| `faqs` | §14 Ask LightSpeed | **KEEP** |
| `resources` | §13 Insights | **KEEP** |
| `events` | §13 Insights | **REBUILD** |
| `newsItems` | §13 Insights | **REBUILD** |
| `careers` | Not in MASTER_SPEC | **DELETE** |
| `insightTeasers`, `insightCategories` | §13 Insights | **REBUILD** |
| `solutions` | §10 Solutions | **REBUILD** — has "89 agents" bug |
| `TONE_STYLES` | Honesty system | **KEEP** |
| `HonestyLabel` types | Honesty system | **KEEP** |

### Agent Count Inconsistency

- `agent-registry.public.json` meta: `agents: 90` — **CANONICAL**
- `HeroSection.tsx`: "90 agents, 20 departments" — **CORRECT**
- `siteContent.ts` solutions: "89 agents and 1 human CEO" — **BUG**
- `siteContent.ts` mission: "90 agents across 20 departments" — **CORRECT**
- `siteContent.ts` newsItems: "90-Agent Operation Live" — **CORRECT**
- `siteContent.ts` faqs: "Our own 90-agent operation" — **CORRECT**

### Content Governance

- Honesty status system (`proven`, `pilot`, `fieldable`, `development`) exists and aligns with MASTER_SPEC §12
- No content state management (Draft, Review, Approved, Published, Archived) — MASTER_SPEC §17 requires this
- No canonical data source for metrics — MASTER_SPEC §16 requires centralized metrics

---

## 6. LEGACY COMPONENT INVENTORY

### Public-Facing Components

| Component | Lines | Status | Action |
|-----------|-------|--------|--------|
| `SiteLayout.tsx` | 108 | Contains ThreeCanvas, ROUTE_TITLES | Rebuild |
| `SiteFooter.tsx` | 170 | 7 columns, 50+ links | Rebuild |
| `FloatingNav.tsx` | 174 | 6 nav links | Modify |
| `HeroSection.tsx` | 210 | Uses StatCounter, hard-coded numbers | Rebuild |
| `HeroMist.tsx` | ~50 | CSS ambient mist | Keep concept, simplify |
| `ThreeCanvas.tsx` | 173 | Three.js | **DELETE** |
| `StatCounter.tsx` | 86 | Animated counters | **DELETE** |
| `AskLightSpeed.tsx` | 353 | Chat interface | Modify per §14 |
| `AiCompanyBuilderSection.tsx` | 535 | AI Builder content | Rebuild |
| `AiCompanyBuilderOsExplorer.tsx` | ~200 | OS explorer | Rebuild |
| `HaomtgvGovernanceFramework.tsx` | ~150 | Governance | Rebuild |
| `TactileHardwareElements.tsx` | ~200 | Industrial UI | **DELETE** |
| `PillarNavigationCard.tsx` | ~150 | Hero card | Rebuild |
| `ExecutiveBriefingModal.tsx` | ~100 | Briefing modal | Keep concept |
| `CtaBand.tsx` | ~50 | CTA band | Keep |
| `NewsletterSignup.tsx` | ~50 | Newsletter | Keep |
| `HonestyBadge.tsx` | ~40 | Honesty badge | Keep |
| `Reveal.tsx` | ~30 | Scroll reveal | Keep |
| `SectionHeading.tsx` | ~40 | Section heading | Keep |
| `PageIntro.tsx` | ~30 | Page intro | Keep |
| `ContactSection.tsx` | ~50 | Contact form | Keep |
| `RelatedLinks.tsx` | ~30 | Related links | Keep |

### Legacy/Hidden Components

| Component | Status |
|-----------|--------|
| `StrategyChasmSection.tsx` | Legacy, delete |
| `SynergyMatrix.tsx` | Legacy, delete |
| `UseCaseCatalogSection.tsx` | Legacy, delete |
| `CoreOfferingsSection.tsx` | Legacy, delete |
| `OfferingDetailCard.tsx` | Legacy, delete |
| `PharosSection.tsx` | Pharos-themed, delete |
| `AboutSection.tsx` | Legacy, delete |
| `AgentModal.tsx` | Legacy, delete |
| `FloatingNav.tsx` | Modify |

---

## 7. OBSOLETE TERMINOLOGY

| Legacy Term | MASTER_SPEC Term | Location |
|-------------|-----------------|----------|
| "ValueCycle: Scale" | "Research & Policy" | siteContent.ts valueCycle |
| "89 agents" | "90 agents" | siteContent.ts solutions |
| "How We Help" | Not in MASTER_SPEC nav | App.tsx, FloatingNav, SiteFooter |
| "Why LightSpeed" | Not in MASTER_SPEC nav | App.tsx |
| "Geography" | Not in MASTER_SPEC nav | App.tsx |
| "Leadership" | Not in MASTER_SPEC nav | App.tsx |
| "FAQ" | Not in MASTER_SPEC nav | App.tsx |
| "Resources" | Not in MASTER_SPEC nav | App.tsx |
| "Events" | Not in MASTER_SPEC nav | App.tsx |
| "News" | Not in MASTER_SPEC nav | App.tsx |
| "Careers" | Not in MASTER_SPEC nav | App.tsx |
| "Deliverables" | Not in MASTER_SPEC nav | App.tsx |
| "Outcomes" | Not in MASTER_SPEC nav | App.tsx |
| "Partnerships" | Not in MASTER_SPEC nav | App.tsx |
| "Trust" | Not in MASTER_SPEC nav | App.tsx |
| "Process" | Not in MASTER_SPEC nav | App.tsx |
| "Offerings" | Not in MASTER_SPEC nav | App.tsx |
| "Work" | Not in MASTER_SPEC nav | App.tsx |
| "Evidence" | Not in MASTER_SPEC nav | App.tsx |
| "Proof & Evidence" | "Proof" | SiteFooter |
| "All Capabilities & Catalog" | "What We Do" | SiteFooter |
| "Client Service Catalog" | Not aligned | SiteLayout ROUTE_TITLES |
| "MALAWI & SADC AI SYSTEMS" | Not in spec | FloatingNav |
| "Tactile" UI language | "Calm Intelligence" | index.css |
| "Pharos" theming | Not in spec | index.css |
| "Telemetry" language | Not in spec | index.css |

---

## 8. SUMMARY COUNTS

| Category | Count |
|----------|-------|
| Total legacy routes | 30+ |
| Routes to DELETE | 20+ |
| Routes to KEEP | 12 |
| Routes to REBUILD | 3 |
| Total page components | 30+ |
| Page components to DELETE | 20+ |
| Page components to KEEP/REBUILD | 10 |
| Total components | ~40 |
| Components to DELETE | ~15 |
| Components to MODIFY | ~5 |
| Components to KEEP | ~20 |
| CSS lines to DELETE | ~500+ |
| Legacy design patterns | 12+ |
| Obsolete terminology entries | 20+ |
| Agent count inconsistencies | 1 bug |
| Content data structures to rebuild | ~15 |
