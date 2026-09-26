# Sitemap: lightspeedholdings.com

## Root (Level 0)
- `/` — Homepage: "Build the Intelligent Enterprise"
  - Hero section with HeroMist ripple effects
  - Strategy Chasm thesis (4 columns)
  - Use Case Catalog (5 tabs: Offers, Industries, Scenarios, Proof, Method)
  - CTA: "Book an Executive Briefing"

## Solutions Ecosystem (Level 1)
- `/solutions/strategy-advisory` — Strategy Advisory offering page
- `/solutions/agentic-ai` — Agentic AI Platform page
- `/solutions/digital-transformation` — Digital Transformation page
- `/solutions/data-intelligence` — Data & Intelligence page
- `/solutions/automation` — Intelligent Automation page

## Industries (Level 1)
- `/industries/government` — Government sector
- `/industries/development` — Development & Donor sector
- `/industries/financial-services` — Financial Services sector
- `/industries/healthcare` — Healthcare sector
- `/industries/agriculture` — Agriculture sector

## Proof & Evidence (Level 1)
- `/work` — Work & Proof page (anchors "proven" philosophy)
- `/evidence` — Evidence & Method page (academic/catalog methodology)
- `/insights` — Insights: Evidence, Research & the Agentic AI Canon

## Conversation (Level 1)
- `/contact` — Start a Conversation / Executive Briefing
- `/ask` — Ask LightSpeed page

## Legal (Level 1)
- `/legal/privacy` — Privacy Policy
- `/legal/terms` — Terms of Service

## Supporting (Level 1)
- `/about` — About: Institutional Charter + Thesis Banner
- `/why` — Why LightSpeed
- `/how-we-help` — How We Help
- `/how-we-help/engagement` — Engagement detail
- `/process` — Our Process
- `/resources` — Resources
- `/events` — Events
- `/news` — News
- `/careers` — Careers
- `/deliverables` — Deliverables
- `/outcomes` — Outcomes
- `/partnerships` — Partnerships
- `/trust` — Trust

## Deep Links (Level 2+ under Solutions)
- `/solutions/strategy-advisory` — Deep link from PillarNavigationCard pillar 0
- `/solutions/agentic-ai` — Deep link from PillarNavigationCard pillar 1
- `/technology#governance` — Deep link from PillarNavigationCard pillar 2 (governance anchor)
- `/ai-company-builder` — Deep link from PillarNavigationCard pillar 3

## Deep Links (Level 2+ under Industries)
- `/industries/government` — Deep link from industry navigation
- `/industries/development` — Deep link from industry navigation
- `/industries/financial-services` — Deep link from industry navigation
- `/industries/healthcare` — Deep link from industry navigation
- `/industries/agriculture` — Deep link from industry navigation

## Navigation Structure

### Desktop (lg:)
- Home (/) — active state
- What We Do → solutions ecosystem dropdown
- Proof → /work, /evidence, /insights
- Technology → /technology (with #governance deep link)
- Ask LightSpeed → /ask
- Insights → /insights
- About → /about

### Mobile (max:lg)
- Hamburger menu with same link structure
- Fullscreen overlay when open

### Footer Links (consistent across all pages)
- Privacy Policy → /legal/privacy
- Terms of Service → /legal/terms
- About → /about
- Careers → /careers
- Resources → /resources

### Breadcrumbs
- Home > Current page on interior routes
- Example: Home > Solutions > Strategy Advisory > [sub-page]

---

## Route-to-Page Mapping Summary

| Route | Page Component | Key Features |
|-------|---------------|--------------|
| `/` | HomePage | HeroMist, HeroSection, StrategyChasmSection, UseCaseCatalogSection, CtaBand, StatCounter, FloatingNav, ThreeCanvas |
| `/about` | AboutSection | Institutional charter, thesis banner, MachineScrewHead hardware accents, StatusLedPip |
| `/technology` | Technology page | ThreeCanvas, FloatingNav, full nav |
| `/solutions/strategy-advisory` | Strategy page | Catalog integration, PillarNavigationCard with active=0 |
| `/solutions/agentic-ai` | Agentic AI page | Catalog integration, PillarNavigationCard with active=1 |
| `/solutions/digital-transformation` | Digital transformation page | Catalog integration |
| `/solutions/data-intelligence` | Data & intelligence page | Catalog integration |
| `/solutions/automation` | Intelligent automation page | Catalog integration |
| `/industries/government` | Government industry page | Industry-specific content |
| `/industries/development` | Development & donor page | Industry-specific content |
| `/industries/financial-services` | Financial services page | Industry-specific content |
| `/industries/healthcare` | Healthcare page | Industry-specific content |
| `/industries/agriculture` | Agriculture page | Industry-specific content |
| `/work` | Work section | Proof philosophy, honesty badges |
| `/evidence` | Evidence & Method | Academic catalog methodology |
| `/insights` | Insights canon | Long-form research positioning |
| `/contact` | Contact page | Briefing request form |
| `/ask` | Ask LightSpeed | User query submission |
| `/legal/privacy` | Privacy policy | Standard legal content |
| `/legal/terms` | Terms of service | Standard legal content |
| `/why` | Why LightSpeed | Value proposition |
| `/how-we-help` | How we help | Service overview |
| `/how-we-help/engagement` | Engagement detail | Specific engagement path |
| `/resources` | Resources | Downloads, docs |
| `/events` | Events | Upcoming/previous events |
| `/news` | News | Blog/posts |
| `/careers` | Careers | Job openings |
| `/deliverables` | Deliverables | Service deliverables listing |
| `/outcomes` | Outcomes | KPIs and results |
| `/partnerships` | Partnerships | Partner ecosystem |
| `/trust` | Trust | Security, compliance, governance |

---
*Auto-generated from codebase route definitions in src/components/SiteLayout.tsx and navigation structure.*
