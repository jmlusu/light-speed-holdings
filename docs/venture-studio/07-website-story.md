# Website Story: "Build the Intelligent Enterprise"

## Overview
A Vite React SPA (React 18, Vite 6, Tailwind 4, `motion`, three.js `ThreeCanvas`) that communicates LightSpeed Holdings' venture-studio mission: from homepage brand psychology through the full solution stack, ending with proof and conversation.

---

## 1. Homepage (`/`)

### Entry Point
- First impression: immediate brand signaling via navy/red/cyan palette (ADR-020 locked)
- Hero section is the moral and visual center of the entire site

### Hero Section
- **Eyebrow**: "MALAWI-ROOTED, SADC-FOCUSED, GLOBAL CAPABILITY" — establishes geographic anchoring
- **Main Headline**: "BUILD THE INTELLIGENT ENTERPRISE" with gradient text spanning red → cyan → navy (the three brand tokens)
- **Divider**: Thin red line with small red circle accent — reinforces brand color
- **Strategy/Build/Govern/Scale tags**: Four uppercase tags with alternating red/cyan borders, representing the operating model pillars
- **Regional Proposition**: "We ground our work in Malawi, where constraints are real, then export proven patterns globally"
- **HeroMist effect**: Ambient ambient mist of blurred radial gradients (CSS only, Part 1 option A)
  - Gated on `prefers-reduced-motion` and mobile/coarse pointer
  - 6 blurred gradient blobs animated via CSS `filter: blur()` and `background-size` keyframes
  - Hidden entirely on reduced-motion or narrow/coarse pointers — accessibility first
- **PillarNavigationCard**: Four connected tactile pillars (Strategy, Build, Govern, Scale)
  - Hover/active state with border-ls-red/50 and pip animation
  - "Partner Briefing" CTA at bottom triggers `onRequestBriefing`
  - Each pillar links to its respective route (strategy-advisory, agentic-ai, technology#governance, ai-company-builder)
- **StatCounter**: 152 verified agent configs, 2373 regression tests, 20 departments onboarded, 5 human approval gates

### Strategy Chasm Section
- Section heading: "THE LIGHTSPEED THESIS"
- Three-column thesis:
  1. **Prove It in Malawi** — real clients, real constraints, real infrastructure; shipped website, donor report, dashboard (not press release)
  2. **Ship, Don't Promise** — every claim labeled Proven/in-pilot/fieldable/in-development; tests published alongside claims
  3. **Governed by Design** — five-tier human approval, immutable audit trails, regional compliance as architecture, not bolt-ons
  4. **Research Informed** — Pharos turns engineering into public intellectual work; SADC AI Governance Framework and Malawi National AI Strategy consultation

### Use Case Catalog Section
- Tabbed interface with 5 tabs: Offers, Industries, Scenarios, Proof, Method
- **Offers tab**: 7 offer families (Strategy Advisory, Agentic AI Platform, Digital Transformation, Data & Intelligence, Intelligent Automation, Client Services, AI Company Builder)
- **Industries tab**: 6 industries (Government, Development & Donor, Financial Services, Healthcare, Agriculture)
- **Scenarios tab**: 8 platform scenarios (AI-Powered Customer Service, Automated Document Processing, Predictive Maintenance, Dynamic Pricing, Personalized Learning, Fraud Detection, Supply Chain Optimization, Real-Time Personalization)
- **Proof tab**: 12 proof points with honesty badges (Proven in-house / Live proof / Fieldable in 2026 / In active development)
- **Method tab**: CATALOG METHOD and POLICIES academic framing
- **Honesty badges** use brand colors: red for "Proven in-house"/"In active development", cyan for "Live proof"/"Fieldable in 2026"

### CTA Band (below the fold)
- "Book an Executive Briefing" primary CTA with ripple-on effect
- Ripple effect (`ripple-on` class, CSS-driven) on the button
- Hover scales up to 1.02, active scales to 0.98
- Links to `/contact`

---

## 2. Solutions Pages

### `/solutions/strategy-advisory`
- Strategy advisory offering page with full catalog integration

### `/solutions/agentic-ai`
- Agentic AI platform page

### `/technology#governance`
- Technology page with governance section anchor

### `/ai-company-builder`
- AI Company Builder registry integration page

---

## 3. Industries Pages

### `/industries/government`
- Government sector page

### `/industries/development`
- Development & Donor sector page

### `/industries/financial-services`
- Financial Services sector page

### `/industries/healthcare`
- Healthcare sector page

### `/industries/agriculture`
- Agriculture sector page

---

## 4. Proof & Evidence Pages

### `/work`
- Work & Proof page — anchors the "proven" philosophy

### `/evidence`
- Evidence & Method page — academic/catalog methodology

### `/insights`
- Evidence, Research & the Agentic AI Canon page
- Long-form content positioning LightSpeed as policy source, not just product

---

## 5. Conversation & Contact Pages

### `/contact`
- Start a Conversation page
- Executive Briefing modal trigger
- Contact form or briefing request

### `/ask`
- Ask LightSpeed page — user query submission

### `/legal/privacy`
- Privacy Policy

### `/legal/terms`
- Terms of Service

---

## 6. Supporting Pages

### `/about`
- About page with institutional charter motto: '"Africa does not need to wait for the future of enterprise. It can build it."'
- Thesis banner: "Aspire. Act. Achieve."

### `/why`
- Why LightSpeed page

### `/how-we-help`
- How We Help page

### `/how-we-help/engagement`
- Engagement detail page

### `/process`
- Our Process page

### `/resources`
- Resources page

### `/events`
- Events page

### `/news`
- News page

### `/careers`
- Careers page

### `/deliverables`
- Deliverables page

### `/outcomes`
- Outcomes page

### `/partnerships`
- Partnerships page

### `/trust`
- Trust page

---

## 7. ThreeCanvas (Background)
- Three.js canvas rendering in the background of certain pages
- Visualizes abstract data flows or brand-reinforcing patterns
- Appears on technology, solutions, and potentially other pages
- Uses `lucide-react` icons integrated with the canvas

---

## Navigation Flow
Primary navigation persists across all pages (Desktop: hidden lg:flex, Mobile: hidden with hamburger toggle):
- **What We Do** → routes to solutions ecosystem
- **Proof** → work/evidence pages
- **Technology** → tech page with governance anchor
- **Ask LightSpeed** → /ask page
- **Insights** → /insights page
- **About** → /about page

Mobile menu opens fullscreen overlay with same links.

---

## Effect Summary

| Effect | Location | Technical Details | Accessibility |
|--------|----------|-------------------|---------------|
| **Ripple-on** | All navigation links, CTA buttons | CSS `&:after` pseudo-element with `animation: ripple-on 2s ease-in-out infinite`; `transform-box: border-box`; `border-radius: 9999px` | Full — pure CSS, no JS |
| **HeroMist** | Hero section only | 6 blurred radial gradient `<span>` elements; `prefers-reduced-motion` + `pointer: coarse` gating; CSS-only animation via `@keyframes` | ⚠️ Gated — hidden on reduced-motion/coarse pointer |
| **Smooth scroll** | Pillar navigation `#` anchors, internal links | `cubic-bezier(0.25, 1, 0.5, 1)` bezier curve over 650ms; falls back to `scrollIntoView({behavior: 'auto'})` when reduced-motion preferred | ✅ Full fallback |
| **ThreeCanvas** | Technology/solutions pages | WebGL/three.js scene rendering abstract data flows; integrated with brand palette | ⚠️ May be motion-sensitive — respect reduced-motion media query |

---

## Brand Enforcement

- **Primary palette**: Navy `#070A40`, Red `#E63946`, Cyan `#00BFFF` (ADR-020 locked)
- **Typography**: Arial type scale throughout; font-family: `ls-navy`, `ls-red`, `ls-cyan`, `ls-white`, `ls-grey-dark`, `ls-grey-light-text`
- **Spacing**: 4px grid system (Tailwind `p-2`, `p-3`, `p-4`, etc.)
- **Logo rules**: Official LightSpeed shield logo with tagline "MALAWI & SADC AI SYSTEMS"
- **No AI-slop**: All content labeled with provenance (Proven/in-pilot/fieldable/in-development)

---
*End of story. The website communicates: prove it in Malawi, ship don't promise, governed by design, research informed — with every claim backed by visible tests and honesty badges.*
