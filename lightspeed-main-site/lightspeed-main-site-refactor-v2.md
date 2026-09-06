# LightSpeed Main Site — V2 Refactor Specification

**Project name:** `lightspeed-main-site`
**Previous name:** `marketing-site`
**Repository:** `jmlusu/light-speed-holdings`
**Primary domain:** `https://lightspeedholdings.com/`
**Status:** Refactor specification
**Audience:** LightSpeed implementation agent team
**Objective:** Transform the existing marketing site into the authoritative corporate, consulting, technology and thought-leadership site for LightSpeed Holdings.

---

## 1. Executive Direction

The existing site is technically strong but currently communicates LightSpeed primarily as an **AI Company Builder / developer platform**.

The V2 site must communicate a broader proposition:

> **LightSpeed Holdings is an AI-native enterprise transformation, Agentic AI advisory, implementation and thought-leadership company originating in Malawi and operating across SADC and Africa.**

The **AI Company Builder remains a core differentiator**, but it should be positioned as LightSpeed's **living laboratory and technical proof**, not as the entire corporate identity.

### Strategic shift

Current mental model:

```text
LightSpeed
    ↓
AI Company Builder
    ↓
144 agents
    ↓
CLI / architecture / technical features
```

Target mental model:

```text
LIGHTSPEED HOLDINGS
        │
        ├── AI-Native Enterprise
        │       ├── Strategy
        │       ├── Transformation
        │       ├── Agentic Operating Model
        │       └── Governance
        │
        ├── Services
        │       ├── AI Strategy
        │       ├── Agentic Automation
        │       ├── Use-Case Discovery
        │       ├── Executive Intelligence
        │       └── AI Governance
        │
        ├── AI Company Builder
        │       ├── 144-Agent Workforce
        │       ├── Orchestration
        │       ├── Memory
        │       ├── Model Routing
        │       ├── Policy
        │       └── CEO Control Plane
        │
        ├── Research & Thought Leadership
        │       ├── Agentic AI
        │       ├── AI-Native Organisations
        │       ├── African AI
        │       ├── AI Use Cases
        │       ├── AI Governance
        │       └── SADC AI
        │
        └── Proof
                ├── Case Studies
                ├── Architecture
                └── Demonstrations
```

---

# 2. Non-Negotiable Positioning

Every page should reinforce some combination of the following:

1. **AI-native enterprise transformation**
2. **Agentic AI**
3. **Enterprise use cases**
4. **Working AI systems**
5. **Governance and responsible deployment**
6. **African/SADC context**
7. **Thought leadership**
8. **Practical implementation**

Avoid positioning LightSpeed as merely:

- an AI chatbot company
- a generic AI consultancy
- an AI SaaS product
- a developer tooling company
- a collection of AI agents
- a prompt-engineering service

The technical platform is evidence of capability.

---

# 3. Rename the Site

The directory/application formerly called:

```text
marketing-site
```

must now be:

```text
lightspeed-main-site
```

Update all relevant:

- directory names
- package names
- project names
- README references
- deployment references
- CI/CD references
- build scripts
- comments
- documentation
- environment references
- navigation metadata
- internal labels
- agent instructions

Do **not** leave visible references to `marketing-site` unless they are explicitly historical migration notes.

Recommended repository structure:

```text
light-speed-holdings/
└── lightspeed-main-site/
```

---

# 4. Homepage Strategy

The homepage must become **executive-first, authority-first and outcome-first**.

It should not open with a developer-centric explanation of YAML files, CLI commands or internal architecture.

## Hero

Recommended headline:

> **Building the AI-native enterprise.**

Supporting proposition:

> LightSpeed Holdings helps organisations redesign how work gets done—combining executive strategy, agentic AI, automation, data and governance into a new operating model.

Primary CTA:

> **Start a conversation →**

Secondary CTA:

> **Explore the AI Company Builder**

Geographic signal:

> **Malawi · SADC · Africa**

Optional supporting capability line:

> Strategy · Agentic AI · Enterprise Automation · Governance

---

# 5. Homepage Narrative

Implement this sequence:

## Section 1 — Hero

Communicate:

- what LightSpeed is
- who it serves
- the strategic problem
- the geographic ambition
- immediate CTA

Do not lead with implementation statistics.

---

## Section 2 — The Thesis

Headline:

> **AI is not a chatbot strategy. It is an organisational redesign.**

Explain that AI-native transformation changes:

- how decisions are made
- how work moves
- how knowledge compounds
- how humans and machines coordinate
- how governance operates

Core conceptual model:

```text
People
   +
AI Agents
   +
Workflows
   +
Data
   +
Governance
   =
AI-Native Enterprise
```

---

## Section 3 — Methodology

Headline:

> **From AI ambition to operating reality.**

Use five stages:

### 01 — Discover

Understand strategy, workflows, decisions, data and organisational friction.

### 02 — Prioritise

Identify high-value use cases based on business/institutional value.

### 03 — Build

Design and deploy agents, workflows, tools and intelligence systems.

### 04 — Govern

Establish human oversight, policies, security, auditability and accountability.

### 05 — Compound

Use memory, measurement and learning to continuously improve the organisation.

---

# 6. AI Company Builder as Proof

Introduce the platform after establishing the strategic proposition.

Headline:

> **We built the company we believe enterprises will become.**

Subheadline:

> The LightSpeed AI Company Builder is our living laboratory for the AI-native enterprise.

Show selected proof points:

- **144 AI agents**
- **20 departments**
- **5-tier governance**
- **6 memory types**
- Model routing
- Task orchestration
- Message bus
- Policy engine
- CEO Control Plane

Do not present these as vanity metrics.

Explain what they prove:

> LightSpeed does not merely advise organisations to become AI-native. We are building and testing the operating model ourselves.

---

# 7. Services

Replace generic product-first service presentation with buyer-oriented capabilities.

Recommended services:

## AI-Native Enterprise Strategy

Help leadership define:

- AI ambition
- target operating model
- capability gaps
- transformation roadmap
- investment priorities

## Agentic Automation

Redesign high-friction workflows around:

- humans
- agents
- tools
- data
- approvals

## AI Use-Case Discovery

Identify and prioritise AI opportunities according to:

- value
- feasibility
- risk
- data readiness
- organisational readiness

## Executive Intelligence

Create systems that turn fragmented information into:

- decision intelligence
- market intelligence
- management insight
- executive reporting

## AI Governance

Design:

- human oversight
- policy
- auditability
- controls
- model governance
- agent governance
- responsible AI practices

## AI Company Builder

For organisations wanting to build an AI-native operating model from the ground up.

---

# 8. Industry / Use-Case Layer

Show concrete applications rather than abstract AI terminology.

Recommended sectors:

### Financial Services

- customer operations
- credit workflows
- risk intelligence
- collections
- decision support
- digital channels

### Enterprise Operations

- workflow automation
- reporting
- PMO
- knowledge management
- executive intelligence

### Development Sector

- programme intelligence
- monitoring
- research
- data operations
- field-to-decision workflows

### Public Sector

- service delivery
- administrative automation
- policy intelligence
- responsible AI governance

### Market Intelligence

- research automation
- intelligence systems
- competitive monitoring
- decision support

---

# 9. African / SADC Positioning

Create a clear regional authority section.

Suggested headline:

> **Africa should not only adopt the AI future. It should design it.**

Explain the opportunity:

```text
Malawi
   ↓
SADC
   ↓
Africa
```

Position LightSpeed around practical African AI adoption, enterprise transformation and governance.

Do not use exaggerated claims such as "Africa's leading..." unless independently substantiated.

Use credible language such as:

- building from Malawi
- focused on African organisations
- SADC perspective
- African AI practice
- applied AI for African institutions

---

# 10. Research & Thought Leadership

Research should become a strategic pillar rather than a generic blog.

Create topic areas:

- Agentic AI
- AI-Native Organisations
- African AI
- AI Use Cases
- AI Governance
- SADC AI
- Enterprise Transformation

Content types:

- essays
- frameworks
- field notes
- case studies
- research briefs
- executive perspectives
- diagrams
- practical playbooks

The objective is to establish LightSpeed as an **intellectual authority**, not merely an implementation vendor.

---

# 11. AI Company Builder Page

Create a technically sophisticated page for the technical audience.

Recommended architecture:

```text
Company Registry
       ↓
Agent Workforce
       ↓
Task Graph
       ↓
Runtime / Message Bus
       ↓
Tools + Models
       ↓
Memory
       ↓
Policy + Governance
       ↓
CEO Control Plane
       ↓
Measurement + Learning
```

Explain the organisational implications of each layer.

The page should contain:

- architecture diagrams
- agent organisation
- department model
- orchestration
- model routing
- memory
- tools
- policy
- governance
- control plane
- technical documentation
- GitHub link

Technical depth belongs here, not in the hero.

---

# 12. Audience Segmentation

The site must serve two major audiences without confusing them.

## Audience A — Leaders

Needs:

- strategy
- economics
- use cases
- transformation
- governance
- proof
- leadership
- regional insight

## Audience B — Builders

Needs:

- architecture
- agents
- orchestration
- APIs
- models
- memory
- tools
- deployment
- GitHub
- documentation

Architecture:

```text
                 LIGHTSPEED
                     │
          ┌──────────┴──────────┐
          │                     │
      FOR LEADERS           FOR BUILDERS
          │                     │
       Strategy              Platform
       Use Cases             Architecture
       Transformation        Agents
       Governance             GitHub
       Research              Documentation
          │                     │
          └──────────┬──────────┘
                     │
              AI COMPANY BUILDER
```

---

# 13. Navigation

Recommended primary navigation:

```text
AI-Native Enterprise
Services
AI Company Builder
Research & Insights
About
```

Primary CTA:

> **Start a conversation**

Secondary utility link:

> **GitHub ↗**

Avoid making these primary navigation items:

- Changelog
- Pricing
- Features
- Agents
- Documentation

Those are supporting resources.

Suggested secondary architecture:

```text
AI Company Builder
├── Architecture
├── Agent Workforce
├── Orchestration
├── Memory
├── Governance
├── Control Plane
├── Documentation
└── Updates
```

---

# 14. CTA Strategy

Replace the current SaaS-style default CTA:

> Book deployment

with:

> **Start a conversation →**

Other context-specific CTAs:

- Discuss your AI agenda →
- Explore the AI Company Builder →
- Read our research →
- Explore the architecture →
- Discuss an AI transformation →
- Bring us the hard problem →

"Book deployment" may remain inside an appropriate technical/product journey if genuinely required.

---

# 15. Pricing

Do not position LightSpeed primarily as a SaaS product with public pricing.

Instead create engagement models:

- Executive Advisory
- AI Strategy Sprint
- Use-Case Discovery
- Agentic Transformation
- AI Operating Model
- Enterprise AI Build
- Strategic AI Partnership

CTA:

> **Discuss your requirements →**

If pricing is retained technically, move it out of the primary corporate navigation.

---

# 16. About Page

The About page must become an authority page.

Recommended headline:

> **Building the next generation of African enterprises.**

Cover:

1. Why LightSpeed exists
2. The AI-native enterprise thesis
3. Malawi/SADC/Africa opportunity
4. Practical implementation philosophy
5. Leadership
6. Experience and credibility
7. Technology laboratory
8. Governance philosophy
9. Contact

Do not expose internal development language.

---

# 17. Proof / Case Studies

Create a dedicated proof architecture.

Recommended:

```text
Proof
├── LightSpeed Case Study
├── AI Company Builder
├── Architecture
├── Demonstrations
├── Use Cases
└── Results
```

Where actual client results are unavailable, clearly label internal platform work as:

- internal case study
- reference architecture
- demonstration
- living laboratory
- prototype

Never imply client deployment where none exists.

---

# 18. Remove Internal / Placeholder Content

Perform a repository-wide search for public-facing text containing:

```text
Foaster
placeholder
T5
slice
MVP
what ships here
re-skinned
parity
implementation note
internal
TODO
FIXME
```

Internal implementation language must not appear in production pages.

Examples of unacceptable public content include:

> "Foaster-parity placeholder — expand in T5 / slice 2."

or:

> "Content lives in src/content/*.mdx."

These are development notes and must be removed or replaced with actual public content.

---

# 19. Visual Direction

The existing design system is a useful foundation.

Do not perform an unnecessary visual rewrite.

Evolve the visual language from:

> Developer AI platform

toward:

> **Institutional intelligence + frontier technology + African context**

Keep:

- Astro
- Tailwind
- existing design tokens where useful
- responsive architecture
- accessibility features
- lightweight JS
- SEO foundations
- self-hosted/local font strategy where practical

Increase:

- editorial whitespace
- executive typography
- diagrams
- strategic frameworks
- restrained motion
- high-quality data visualisation
- architectural storytelling

Reduce:

- terminal-heavy visuals
- excessive technical cards
- feature-grid overload
- SaaS dashboard aesthetics on the homepage

---

# 20. Technical Principles

The implementation team must preserve:

### Performance

- static-first Astro architecture
- minimal client-side JavaScript
- lazy-load heavy visualisations
- avoid unnecessary libraries

### Accessibility

Maintain:

- semantic HTML
- keyboard navigation
- focus states
- skip link
- reduced-motion support
- sufficient contrast
- accessible navigation

### SEO

Every strategic page needs:

- unique `<title>`
- meta description
- canonical URL
- OpenGraph metadata
- Twitter metadata
- relevant JSON-LD
- semantic heading hierarchy

### Structured data

Use appropriate Schema.org types:

- Organization
- WebSite
- Article
- Person
- Service
- BreadcrumbList

Do not create unsupported claims through structured data.

---

# 21. Recommended Sitemap

Target information architecture:

```text
/
│
├── /ai-native-enterprise
│   ├── /operating-model
│   ├── /transformation
│   └── /governance
│
├── /services
│   ├── /ai-strategy
│   ├── /agentic-automation
│   ├── /use-case-discovery
│   ├── /executive-intelligence
│   └── /ai-governance
│
├── /ai-company-builder
│   ├── /architecture
│   ├── /agents
│   ├── /orchestration
│   ├── /memory
│   ├── /governance
│   └── /control-plane
│
├── /research
│   ├── /agentic-ai
│   ├── /ai-native-enterprise
│   ├── /african-ai
│   ├── /ai-use-cases
│   ├── /ai-policy
│   └── /sadc
│
├── /proof
│   ├── /light-speed-case-study
│   ├── /architecture
│   └── /demonstrations
│
├── /about
├── /contact
├── /docs
├── /privacy
└── /security
```

Existing routes should be redirected or mapped where possible rather than broken.

The current sitemap contains routes including `/`, `/about/`, `/agents/`, `/case-study/`, `/changelog/`, `/contact/`, `/docs/`, `/features/`, `/how-it-works/`, `/platform/`, `/pricing/`, `/research/`, `/security/`, `/solutions/`, and solution subpages. Preserve useful content and establish redirects when changing routes.

---

# 22. Content Architecture

Use reusable content models.

Recommended collections:

```text
services
research
case-studies
use-cases
platform
agents
pages
```

Research articles should support:

```text
title
slug
description
author
date
updated
category
tags
featuredImage
readingTime
body
```

Services should support:

```text
title
slug
problem
outcomes
approach
capabilities
useCases
proof
cta
```

Case studies should support:

```text
title
context
challenge
approach
architecture
outcomes
lessons
status
```

---

# 23. Messaging Rules for Agents

When writing or editing site copy:

### Prefer

- enterprise value
- organisational transformation
- practical AI
- agentic systems
- operating model
- decision intelligence
- workflow transformation
- governance
- African context
- measurable outcomes
- responsible deployment

### Avoid overusing

- revolutionary
- disruptive
- game-changing
- unprecedented
- world's first
- Africa's leading
- cutting-edge

Use evidence-based language.

### Important

Do not make unsupported claims about:

- number of customers
- revenue
- deployments
- market leadership
- performance
- ROI
- partnerships
- production usage

Internal LightSpeed platform metrics can be used when clearly described as internal platform/reference architecture metrics.

---

# 24. Implementation Phases

## Phase 0 — Repository Hygiene

- rename `marketing-site` → `lightspeed-main-site`
- update references
- remove internal placeholder copy
- inventory all routes
- identify duplicate/obsolete pages
- preserve useful technical assets

## Phase 1 — Brand / IA

- update navigation
- update footer
- establish new information architecture
- establish page hierarchy
- define CTA strategy

## Phase 2 — Homepage

Implement:

1. Hero
2. Thesis
3. Methodology
4. Services
5. Use cases
6. AI Company Builder proof
7. Africa/SADC positioning
8. Research
9. Final CTA

## Phase 3 — Strategic Pages

Build/refactor:

- AI-Native Enterprise
- Services
- About
- Contact
- Research

## Phase 4 — Technical Platform

Build/refactor:

- AI Company Builder
- Architecture
- Agents
- Orchestration
- Memory
- Governance
- Control Plane
- Docs

## Phase 5 — Proof

Build:

- case study
- demonstrations
- architecture visualisations
- technical evidence

## Phase 6 — SEO / Analytics / QA

Perform:

- SEO audit
- accessibility audit
- responsive testing
- performance testing
- link validation
- metadata validation
- schema validation
- sitemap validation
- robots validation
- analytics/conversion instrumentation

---

# 25. Agent Team Structure

Recommended implementation team:

```text
SITE REFACTOR ORCHESTRATOR
│
├── IA / Strategy Agent
│   └── navigation, sitemap, page hierarchy
│
├── Brand / Messaging Agent
│   └── positioning, copy, CTAs
│
├── UX Agent
│   └── user journeys and page layouts
│
├── Visual Design Agent
│   └── typography, spacing, diagrams, visual system
│
├── Astro Engineering Agent
│   └── components, routes, layouts
│
├── Content Agent
│   └── service/research/case-study content
│
├── SEO Agent
│   └── metadata, schema, canonical, sitemap
│
├── Accessibility Agent
│   └── WCAG-oriented QA
│
├── Performance Agent
│   └── Core Web Vitals, bundle and image optimisation
│
└── QA / Release Agent
    └── route, visual, responsive and regression testing
```

The **Orchestrator must enforce the positioning rules in this document**.

---

# 26. Definition of Done

The V2 site is not complete merely because it builds successfully.

It is complete when:

### Strategic

- [ ] LightSpeed is immediately understood as an AI-native enterprise transformation company.
- [ ] AI Company Builder is positioned as proof/laboratory.
- [ ] Malawi → SADC → Africa positioning is clear.
- [ ] Research/thought leadership has a meaningful role.
- [ ] Services are understandable to executives.

### UX

- [ ] Navigation is simple.
- [ ] Executive and technical audiences can find their journeys.
- [ ] CTAs are appropriate.
- [ ] Homepage has clear narrative progression.

### Technical

- [ ] `marketing-site` has been renamed to `lightspeed-main-site`.
- [ ] Build passes.
- [ ] No broken internal links.
- [ ] No production placeholder language.
- [ ] Responsive layouts work.
- [ ] Accessibility checks pass.
- [ ] SEO metadata is present.

### Content

- [ ] No unsupported claims.
- [ ] No internal implementation notes.
- [ ] No accidental SaaS-only positioning.
- [ ] Technical claims are accurate.
- [ ] Internal platform metrics are contextualised.

### Conversion

A first-time executive visitor should be able to understand within approximately 30 seconds:

1. **What LightSpeed is**
2. **What problem it solves**
3. **Who it helps**
4. **Why it is credible**
5. **What to do next**

---

# 27. North-Star Statement

All agents should use this as the ultimate test:

> **LightSpeed Holdings helps organisations become AI-native by redesigning how people, agents, workflows, data and governance work together—and proves the model by building and operating an AI-native company itself.**

If a proposed design, component, page, feature or piece of copy strengthens that proposition, keep it.

If it makes LightSpeed look more like a generic AI SaaS product, developer tool or chatbot company, reconsider it.

---

# 28. Final Strategic Principle

**Do not hide the technology. Reframe it.**

The 144-agent organisation, AI Company Builder, model router, memory engine, message bus, task graph, policy engine and CEO Control Plane are valuable.

They should answer:

> **“Can LightSpeed actually build the future it is describing?”**

The corporate site should answer:

> **“Why does this future matter to my organisation?”**

The combination is the differentiator.

```text
THOUGHT LEADERSHIP
        +
ENTERPRISE STRATEGY
        +
AGENTIC AI
        +
WORKING SYSTEMS
        +
GOVERNANCE
        +
AFRICAN CONTEXT
        =
LIGHTSPEED HOLDINGS
```

**This is the target state for `lightspeed-main-site` V2.**
