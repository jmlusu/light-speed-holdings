# Specification-to-Code Map — LightSpeed Holdings

**Date:** 2026-09-25
**Purpose:** Map MASTER_SPEC.md requirements to target implementation, identifying existing code and actions needed
**Companion:** LEGACY_INVENTORY.md, MASTER_SPEC.md, REBUILD_DIRECTIVE.md

---

## 1. CORE SPECIFICATION REQUIREMENTS

### 1.1 MASTER_SPEC §2 — Brand Position

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Company name: LightSpeed Holdings Limited | Brand tokens, header, footer | `company.legalName` in siteContent.ts | **KEEP** |
| Brand line: ASPIRE. ACT. ACHIEVE. | Brand tokens, footer | `company.tagline` in siteContent.ts | **KEEP** |
| Geographic ambition: Malawi → SADC → Africa | Section architecture, footer | `geography` in siteContent.ts | **REBUILD** |
| AI-native company builder positioning | Hero, sections, navigation | `heroHeadline: 'Build the intelligent enterprise.'` | **REBUILD** |

### 1.2 MASTER_SPEC §3 — Core Operating Model

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Four capabilities: Strategy, Build, Govern, Research & Policy | Homepage section, navigation | `valueCycle: ['Strategy', 'Build', 'Govern', 'Scale']` | **REBUILD** — Change "Scale" to "Research & Policy" |
| Connected system, not four unrelated categories | Section design | `capabilityDomains` (5 domains) | **REBUILD** — 4 capabilities |

### 1.3 MASTER_SPEC §4 — AI Company Builder

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Transformation journey: Opportunity → Strategy → Architecture → Agents → Workflows → Deployment → Governance → Measurement → Continuous Improvement | AI Company Builder page | `AiCompanyBuilderSection.tsx` (legacy) | **REBUILD** |
| Principles: Human-led, AI-native, Agentic, Governed, Data-informed, Modular, Measurable, Progressive, Secure, Designed for practical adoption | Page content | Not explicitly represented | **CREATE** |

### 1.4 MASTER_SPEC §5 — 90-Agent Operating Model

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| 90 AI agents (not 127, 144, 152) | Agent registry, homepage, AI Builder | `agent-registry.public.json` (90), `HeroSection.tsx` (90), `solutions` (89 bug) | **FIX BUG** — Centralize to 90 |
| Public representation: coordinated digital workforce | Homepage section, AI Builder | `agentsList` from registry | **KEEP** |
| Do not expose private prompts, credentials, orchestration logic | Public registry filter | Registry contains full agent details | **MODIFY** — Filter public registry |
| Centralize canonical agent count | Data source | `registry.meta.agents` | **CREATE** — Single source of truth |

### 1.5 MASTER_SPEC §7 — Public Information Architecture

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Top-level nav: Home, What We Do, AI Company Builder, Solutions, Sectors, Proof, Insights, About, Contact / Start a Conversation | Navigation component | FloatingNav has 6 links, SiteFooter has 7 columns | **REBUILD** — All nav components |
| Route structure matching 9 sections | Router configuration | 30+ routes | **REBUILD** — Replace App.tsx router |
| Exact labels may be refined if IA intact | Navigation | — | **MODIFY** |

### 1.6 MASTER_SPEC §8 — Homepage Experience

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| 1. Orientation: who, what, who served, why AI-native matters | Hero section | `HeroSection.tsx` (partially aligned) | **REBUILD** |
| 2. Core proposition: AI-native company builder | Hero section | `heroHeadline` | **REBUILD** |
| 3. Operating model: Strategy → Build → Govern → Research & Policy | Hero or dedicated section | Hero has "STRATEGY BUILD GOVERN SCALE" | **REBUILD** |
| 4. AI Company Builder journey | Hero or dedicated section | Not in hero | **CREATE** |
| 5. 90-agent workforce | Hero metric strip | StatCounter (90) | **REBUILD** — Remove animated counter |
| 6. Solutions | Solutions section | Not on homepage currently | **CREATE** |
| 7. Sectors | Sectors section | Not on homepage currently | **CREATE** |
| 8. Proof | Proof section | ProofPage exists | **MODIFY** |
| 9. Insights | Insights section | InsightsPage exists | **MODIFY** |
| 10. CTA | Hero CTA | "Start a Conversation" button | **KEEP** concept |

### 1.7 MASTER_SPEC §9 — Progressive Disclosure

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Layer 1: Executive — What is LightSpeed? | Hero | Hero section | **KEEP** concept |
| Layer 2: Business — What can LightSpeed do? | What We Do / Solutions | WhatWeDoPage | **REBUILD** |
| Layer 3: Operating model — How does AI Company Builder work? | AI Company Builder | AiCompanyBuilderPage | **REBUILD** |
| Layer 4: Architecture — How are agents, data, workflows connected? | Technology page | TechnologyPage | **REBUILD** |
| Layer 5: Evidence — What has been built? | Proof | ProofPage | **MODIFY** |
| Layer 6: Technical detail — How does system work? | Technology | TechnologyPage | **REBUILD** |
| Stop at any layer | Navigation | — | **DESIGN** — Clear section boundaries |

### 1.8 MASTER_SPEC §10 — Solutions

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Express in terms of organizational problems and outcomes | Solutions page | `solutions` array in siteContent.ts | **REBUILD** — Per spec §10 structure |
| Every solution answers: What problem? Who? What changes? What builds? What evidence? | Solution detail pages | `SolutionDetailPage` | **REBUILD** |
| Avoid generic consulting language | Content | `capabilityDomains` has consulting language | **REBUILD** |

### 1.9 MASTER_SPEC §11 — Sectors

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Government, Development, Health, Financial Services, Agriculture, Energy, Telecom, SMEs, Technology | Sectors page | `geography` in siteContent.ts (Malawi, SADC, Africa, Global) | **REBUILD** |
| Distinguish proven, current capability, demonstration, future opportunity | Sector pages | HonestyBadge exists | **MODIFY** |
| Only claim sector experience where evidence exists | Content | Honest-status system exists | **KEEP** |

### 1.10 MASTER_SPEC §12 — Proof

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Do not manufacture testimonials, logos, metrics, case studies | Proof section | `resources` array, `newsItems` | **MODIFY** |
| Evidence types: case studies, demonstrations, prototypes, research | Proof section | `resources`, `newsItems` | **KEEP** concept |
| Label as Concept/Prototype/Demonstration/Internal capability/Proposed | HonestyBadge | `HonestyBadge` component | **KEEP** |

### 1.11 MASTER_SPEC §13 — Insights

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Support short posts and deeper articles/reports | Insights page | `insightTeasers`, `insightCategories` | **REBUILD** |
| Content categories: Agentic AI, AI Company Building, AI governance, etc. | Insights categories | `insightCategories` | **REBUILD** |

### 1.12 MASTER_SPEC §14 — Ask LightSpeed

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| AI-assisted interface exploring public knowledge | AskLightSpeed component | `AskLightSpeed.tsx` (353 lines) | **MODIFY** — Enforce public-safe boundary |
| Operate against explicitly defined public-safe knowledge boundary | Content source | Chat uses `solutions` data | **MODIFY** |
| Do not expose secrets, credentials, prompts, memory | Data source | Chat reads from siteContent.ts | **KEEP** — Already safe |
| Distinguish Public knowledge → Internal knowledge | UI design | Not implemented | **CREATE** |

### 1.13 MASTER_SPEC §15 — Data and Content Architecture

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Structured registries: services, solutions, sectors, case studies, insights, metrics, capabilities, agents, leadership, FAQs, CTAs | Data files | `siteContent.ts`, `companyData.ts`, `agent-registry.public.json` | **REBUILD** — Registry-driven |
| Business facts have canonical source | Data architecture | `siteContent.ts` is single source | **KEEP** concept, restructure |
| Avoid hard-coding same number in multiple components | Metrics | Agent count hard-coded in HeroSection, solutions | **FIX** — Single source |

### 1.14 MASTER_SPEC §16 — Dynamic Metrics

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Metrics as governed data | Data source | `companyData.ts` initialKPIs | **MODIFY** — For public use |
| Do not duplicate numbers | Single source | Agent count in HeroSection and solutions | **FIX** |
| Never use animated counters | Static display | `StatCounter.tsx` | **DELETE** — Replace with static |

### 1.15 MASTER_SPEC §17 — Content Governance

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Every claim has source or owner | Content model | HonestyBadge exists | **EXTEND** |
| Content states: Draft, Review, Approved, Published, Archived | Content model | HonestyTone only has 4 states | **EXTEND** |
| Claims require evidence | Honesty system | Honest-status system | **KEEP** |

### 1.16 MASTER_SPEC §18–23 — Design Language, Visual, Color, Light/Dark, Motion, Responsive, Accessibility

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Calm, Intelligent, Premium, Modern, Human, Trustworthy | CSS/tailwind | Tactile industrial CSS | **REBUILD** — All CSS |
| Morning Mist #F7F8F9 / Slate #121518 | Brand tokens | `#070a40` dark, `#edf3f8` light | **REBUILD** — Update tokens |
| Both light/dark modes first-class | Theme system | `SiteContext` with theme toggle | **MODIFY** — Fix colors |
| Restrained motion, `prefers-reduced-motion` | CSS | Has `prefers-reduced-motion` gate | **KEEP** gate, reduce animations |
| Responsive: desktop, laptop, tablet, mobile | Tailwind responsive | Tailwind responsive classes | **KEEP** |
| Accessibility: semantic HTML, keyboard, focus, contrast | HTML/CSS | Skip link exists | **KEEP** concept, enhance |

### 1.17 MASTER_SPEC §24 — Performance

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Prioritize content clarity, Core Web Vitals | Code quality | Three.js, framer-motion, recharts | **DELETE** heavy dependencies |
| Do not add Three.js, GSAP, video, shaders | Dependency removal | `three` in package.json, `ThreeCanvas.tsx` | **DELETE** |
| Lazy loading, image optimization | Implementation | Not explicitly implemented | **ADD** |
| Minimal unnecessary JavaScript | Code audit | 40+ components | **CLEANUP** |

### 1.18 MASTER_SPEC §25 — Technical Architecture

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Modular components | Component architecture | Has components but many legacy | **REBUILD** |
| Clear data boundaries | Data architecture | Mixed data in siteContent.ts | **RESTRUCTURE** |
| Centralized design tokens | CSS tokens | `brand-tokens.css` | **EXTEND** — Add MASTER_SPEC colors |
| Predictable routing | Router | 30+ routes | **REBUILD** |
| Testable logic | Code structure | Has `__tests__` | **KEEP** |

### 1.19 MASTER_SPEC §26–29 — Public/Internal Boundary, Agent Registry, Executive Control

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Public vs Internal boundary | Data filtering | Agent registry has full details | **MODIFY** — Filter public registry |
| Public agent records: name, role, category, description, capability, status | Agent display | `PublicAgent` types exist | **KEEP** concept |
| Human leadership + governed AI | Content | `leadership` in siteContent.ts | **KEEP** |
| AI shown as operating capability, not replacement | Content | `human-ceo` leadership | **KEEP** |

### 1.20 MASTER_SPEC §30–33 — Architecture Documentation, Migration, Acceptance, Source of Truth

| Requirement | Target Implementation | Existing Implementation | Action |
|-------------|----------------------|------------------------|--------|
| Architecture documentation | ADRs | `docs/adr/` exists | **KEEP** |
| Migration prioritization | Build order | — | **PLAN** |
| Acceptance criteria | Verification | — | **CREATE** |
| MASTER_SPEC takes precedence | All decisions | — | **GOVERN** |

---

## 2. TARGET ROUTE ARCHITECTURE

| Route | Page | MASTER_SPEC Section | Action |
|-------|------|---------------------|--------|
| `/` | HomePage | §8 Homepage | **KEEP** (rebuild content) |
| `/what-we-do` | WhatWeDoPage | §7 Navigation | **KEEP** (rebuild content) |
| `/ai-company-builder` | AiCompanyBuilderPage | §4 AI Company Builder | **KEEP** (rebuild content) |
| `/solutions` | SolutionsPage | §10 Solutions | **KEEP** (rebuild) |
| `/sectors` | SectorsPage | §11 Sectors | **CREATE** |
| `/proof` | ProofPage | §12 Proof | **KEEP** (modify) |
| `/insights` | InsightsPage | §13 Insights | **KEEP** (modify) |
| `/about` | AboutPage | §7 Navigation | **KEEP** (modify) |
| `/contact` | ContactPage | §7 Navigation | **KEEP** (modify) |
| `/ask` | AskLightSpeedPage | §14 Ask LightSpeed | **KEEP** (modify) |
| `/legal/privacy` | PrivacyPage | Legal | **KEEP** |
| `/legal/terms` | TermsPage | Legal | **KEEP** |
| `*` | NotFound | Fallback | **KEEP** |

### Routes to DELETE

`/why`, `/how-we-help`, `/process`, `/geography`, `/leadership`, `/faq`, `/resources`, `/events`, `/news`, `/careers`, `/deliverables`, `/outcomes`, `/partnerships`, `/trust`, `/offerings`, `/work`, `/evidence`, `/solutions/:slug` (rebuild under `/solutions`), `/industries/:slug` (rebuild under `/sectors`)

---

## 3. TARGET COMPONENT ARCHITECTURE

### Core Components to KEEP
| Component | Reason |
|-----------|--------|
| `SiteContext` + `withSite` | Theme/context pattern is sound |
| `HonestyBadge` | Public safety system aligns with spec |
| `Reveal` | Scroll reveal |
| `SectionHeading` | Reusable |
| `PageIntro` | Reusable |
| `CtaBand` | CTA pattern |
| `ContactSection` | Contact form |
| `HeroMist` | Ambient effect concept |
| `useInView`, `useSmoothScroll` | Utility hooks |
| `site-context.tsx` | Context provider |
| `enquiry.ts`, `validation.ts` | Form logic |

### Components to REBUILD
| Component | MASTER_SPEC Section |
|-----------|---------------------|
| `SiteLayout` | All sections |
| `SiteFooter` | §7 Navigation |
| `FloatingNav` | §7 Navigation |
| `HeroSection` | §8 Homepage |
| `HomePage` | §8 Homepage |
| `WhatWeDoPage` | §7 Navigation |
| `AiCompanyBuilderPage` | §4 AI Company Builder |
| `SolutionsPage` | §10 Solutions |
| `SectorsPage` | §11 Sectors |
| `ProofPage` | §12 Proof |
| `InsightsPage` | §13 Insights |
| `AboutPage` | §7 Navigation |
| `ContactPage` | §7 Navigation |
| `AskLightSpeed` | §14 Ask LightSpeed |
| `TechnologyPage` | §4, §5, §6 |

### Components to CREATE
| Component | MASTER_SPEC Section |
|-----------|---------------------|
| `AgentRegistry` | §5, §28 |
| `MetricDisplay` | §16 |
| `PublicSafeKnowledgeBoundary` | §14 |
| `ThemeToggle` | §21 |
| `ArchitectureDiagram` | §4, §25 |

### Components to DELETE
| Component | Reason |
|-----------|--------|
| `ThreeCanvas` | Three.js prohibited |
| `StatCounter` | Animated counters prohibited |
| `TactileHardwareElements` | Industrial aesthetic violates spec |
| `AiCompanyBuilderSection` | Legacy |
| `AiCompanyBuilderOsExplorer` | Legacy |
| `HaomtgvGovernanceFramework` | Legacy |
| `PillarNavigationCard` | Legacy hardware aesthetic |
| `HeroSection` (current) | Will be replaced |
| `StrategyChasmSection` | Legacy |
| `SynergyMatrix` | Legacy |
| `UseCaseCatalogSection` | Legacy |
| `CoreOfferingsSection` | Legacy |
| `OfferingDetailCard` | Legacy |
| `PharosSection` | Pharos theming violates spec |
| `AboutSection` | Legacy |
| `AgentModal` | Legacy |
| `ExecutiveBriefingModal` | Legacy |
| `NewsletterSignup` | Legacy |
| `FloatingNav` (current) | Will be replaced |
| `SiteFooter` (current) | Will be replaced |
| `SiteLayout` (current) | Will be replaced |

### Design Tokens to UPDATE
| Token | Current | Target |
|-------|---------|--------|
| Dark background | `#070a40` | `#121518` |
| Light background | `#edf3f8` / `#f2f2f2` | `#F7F8F9` |
| Navy | `#070A40` | Keep as accent |
| Red | `#E63946` | Keep as accent |
| Cyan | `#00BFFF` | Keep as accent |
| Spacing | 4px grid | Keep |
| Typography | Arial | Keep |

---

## 4. DESIGN TOKEN SPECIFICATION

### Color System (MASTER_SPEC §20)

```css
:root {
  /* Light mode (Morning Mist / Alabaster) */
  --ls-bg-light: #F7F8F9;
  --ls-surface-light: #FFFFFF;
  --ls-text-light: #121518;
  --ls-text-secondary-light: #6B7280;

  /* Dark mode (Slate / Deep Mineral) */
  --ls-bg-dark: #121518;
  --ls-surface-dark: #1A1D21;
  --ls-text-dark: #F7F8F9;
  --ls-text-secondary-dark: #9CA3AF;

  /* Brand accents */
  --ls-navy: #070A40;
  --ls-red: #E63946;
  --ls-cyan: #00BFFF;
}
```

### Motion System (MASTER_SPEC §22)

```css
/* Slow to the eye. Fast to the mind. */
--transition-slow: 500ms ease;
--transition-medium: 300ms ease;
--transition-fast: 150ms ease;
--ease-spatial: cubic-bezier(0.4, 0, 0.2, 1);
```

---

## 5. DATA ARCHITECTURE SPECIFICATION

### Canonical Data Sources

| Data Type | Source File | Canonical Field |
|-----------|-------------|-----------------|
| Agent count | `agent-registry.public.json` | `meta.agents` |
| Department count | `agent-registry.public.json` | `meta.departments` |
| Agent list | `agent-registry.public.json` | `agents[]` |
| Company identity | `siteContent.ts` | `company` |
| Mission/Vision | `siteContent.ts` | `mission`, `vision` |
| Solutions | `siteContent.ts` | `solutions[]` |
| Sectors | `siteContent.ts` | `sectors[]` (to create) |
| Proof | `siteContent.ts` | `proof[]` (to create) |
| Insights | `siteContent.ts` | `insights[]` (to create) |
| FAQs | `siteContent.ts` | `faqs[]` |
| Resources | `siteContent.ts` | `resources[]` |
| News | `siteContent.ts` | `newsItems[]` |
| Leadership | `siteContent.ts` | `leadership[]` |

### Centralized Metrics

| Metric | Source | Used By |
|--------|--------|---------|
| Agent count | `registry.meta.agents` | HomePage, AiCompanyBuilderPage |
| Department count | `registry.meta.departments` | HomePage |
| All KPIs | `companyData.ts` initialKPIs | Dashboard (internal) |
| Project count | To be defined | HomePage |

---

## 6. MIGRATION SEQUENCE

### Phase 1: Foundation (Week 1)
1. Update `brand-tokens.css` with MASTER_SPEC colors
2. Rewrite `index.css` for Calm Intelligence
3. Update `vite.config.ts` to remove Three.js
4. Update `package.json` to remove `three`, `@types/three`, `recharts`
5. Create filtered public agent registry

### Phase 2: Architecture (Week 2)
6. Rewrite `App.tsx` router with MASTER_SPEC routes
7. Rewrite `SiteLayout.tsx` without ThreeCanvas
8. Rewrite `FloatingNav.tsx` with 9-section navigation
9. Rewrite `SiteFooter.tsx` with aligned columns
10. Update `index.html` title and meta

### Phase 3: Pages (Week 3)
11. Rebuild `HomePage.tsx` per §8 narrative
12. Rebuild `WhatWeDoPage.tsx` per §7
13. Rebuild `AiCompanyBuilderPage.tsx` per §4
14. Create `SectorsPage.tsx` per §11
15. Modify `ProofPage.tsx` per §12
16. Modify `InsightsPage.tsx` per §13
17. Modify `AboutPage.tsx`, `ContactPage.tsx`, `AskLightSpeed.tsx`

### Phase 4: Cleanup (Week 4)
18. Delete all obsolete pages and components
19. Remove legacy CSS
20. Remove Three.js dependency
21. Fix agent count inconsistency
22. Remove animated counters
23. Remove obsolete content data structures
24. Run lint, typecheck, tests, build
25. Create IMPLEMENTATION_AUDIT.md

### Phase 5: Validation (Week 5)
26. Specification audit against MASTER_SPEC §32
27. Accessibility checks
28. Responsive checks
29. Light/dark mode verification
30. Broken-link checks
31. Final legacy search (REBUILD_DIRECTIVE §22)

---

## 7. SPECIFICATION COVERAGE MAP

| MASTER_SPEC § | Requirement | Implementation Target | Status |
|---------------|-------------|----------------------|--------|
| §2 | Brand Position | `brand-tokens.css`, `siteContent.ts` | Partial |
| §3 | Core Operating Model | `siteContent.ts` valueCycle | Needs fix |
| §4 | AI Company Builder | `AiCompanyBuilderPage.tsx` | Needs rebuild |
| §5 | 90-Agent Model | `agent-registry.public.json` | Has bug (89 vs 90) |
| §6 | Human + AI | `leadership`, content | Keep |
| §7 | Public IA | Navigation, routes | Needs rebuild |
| §8 | Homepage | `HomePage.tsx` | Needs rebuild |
| §9 | Progressive Disclosure | Section design | Design needed |
| §10 | Solutions | `SolutionsPage.tsx` | Needs rebuild |
| §11 | Sectors | `SectorsPage.tsx` | Needs create |
| §12 | Proof | `ProofPage.tsx` | Modify |
| §13 | Insights | `InsightsPage.tsx` | Modify |
| §14 | Ask LightSpeed | `AskLightSpeed.tsx` | Modify |
| §15 | Data Architecture | Registry files | Restructure |
| §16 | Dynamic Metrics | Centralized | Fix |
| §17 | Content Governance | Honesty system | Extend |
| §18-23 | Design/Responsive/A11y | CSS, components | Rebuild |
| §24-29 | Architecture/Boundary | Codebase | Rebuild |
| §30-33 | Documentation/Validation | ADRs, audit | Create |
