---
title: "Customer Journey Conversion Architecture — Specification"
---

# Specification

## Source Document
`CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE.md` — Implementation Authority

## Scope
Full implementation of the customer journey architecture across the LightSpeed Holdings React 18 + Vite SPA.

## Requirements by Journey Stage

### Stage 1: Awareness — Homepage (`/`)
- **Beat 1**: Orientation — Who/what/why AI-native (HeroSection)
- **Beat 2**: Core proposition (ThesisSection)
- **Beat 3**: Operating model cycle (ThesisSection valueCycle)
- **Beat 4**: Builder journey (BuilderSection)
- **Beat 5**: 90-agent workforce (WorkforceSection — registry-driven)
- **Beat 6**: **Solutions** — NEW distinct chapter between 5 and 7
- **Beat 7**: Sectors (SectorsSection)
- **Beat 8**: Proof (ProofSection)
- **Beat 9**: Insights (InsightsSection)
- **Beat 10**: CTA (BriefingSection)

**Requirements:**
- Progressive disclosure: exactly one dominant element per viewport
- All metrics from `metrics.ts` registry (agentCount: 90, testCount: 17, departments: 20)
- "100% Auditable" qualified with honesty badge
- ChapterRail includes new Solutions beat

### Stage 2: Exploration & Consideration

#### Solutions (`/solutions`)
- 5 solution categories with consistent framework
- Each solution answers: Problem → Solution → How it works → Relevant sectors → Evidence → Engagement
- Primary CTA: "Discuss This Solution"
- Secondary: Relevant sectors, Proof, Ask LightSpeed
- Bidirectional cross-links with Sectors

#### Sectors (`/sectors`)
- 5 sectors with evidence tiers: PROVEN / CURRENT / DEMO / FUTURE
- Sector journey: Sector → Challenges → Opportunities → Relevant Solutions → Evidence → Engagement
- Primary CTA: "Explore Solutions for This Sector"
- Governed by new `sector-registry.ts` (not hard-coded const)
- Bidirectional cross-links with Solutions

#### Proof (`/proof`) — 7 Sections
1. `#metrics` — Platform metrics (single-sourced from `metrics.ts`)
2. `#honesty` — Honesty ladder (Proposed → Verified → Established → Market-leading)
3. `#cases` — Case studies (from `workCaseStudies`, renamed `proofCaseStudies`)
4. `#outcomes` — Outcomes (from `outcomeCategories`)
5. `#trust` — Trust band (from `trustEvidence`)
6. `#policy` — Policy track (from `workPolicy`, renamed `proofPolicy`)
7. `#verify` — How to verify (code review, governance walkthrough, governed pilot)

**Critical**: Proof must exist throughout site (Home, Solutions, Sectors, Builder, Workforce, About, Insights) — not confined to `/proof`

#### Insights (`/insights`)
- 12 content categories (from `OFFER_FAMILIES` / `insightCategories`)
- Article content + route (build now)
- Strip PharosSection/stone texture; calm design only
- Journey: Topic → Insight → Related concept → Relevant solution/sector → Ask LightSpeed → Subscribe/Engage
- Primary CTA: "Explore Related Thinking"
- Newsletter journey: Insight → Interest → Signup → Verified Email → Nurture → Returning Visitor → Potential Engagement

#### About (`/about`)
- Humanize organization; explain operating model
- Journey: Who is LightSpeed? → Leadership → Operating model → Departments → AI workforce → Governance → Proof → Engagement
- Consume `agent-registry.public.json` for 90-agent copy

#### Ask LightSpeed (`/ask`)
- Public-safe knowledge boundary; no secrets/prompts/internal info
- Client-side only; no LLM/backend calls
- Sector picker uses canonical 5 slugs exactly
- Results only show solutions from canonical 5 slugs
- Empty match → honest empty state + briefing CTA
- Full keyboard path; `aria-live` on assistant turns

#### Contact (`/contact`)
- 5-step flow: Discover → Diagnose → Design → Build → Govern
- Framing: "Tell Us Where You Are"
- SLA: "within two business days"
- Turnstile verification required
- Form captures: who, organization, problem, interest area, desired next step
- POST `/api/enquiry` endpoint (server needed)

### Navigation Architecture
- Global nav: Solutions, Sectors, Proof, Insights, About, Ask LightSpeed, Contact
- Primary CTA: "Start a Conversation"
- Secondary: "Book a Briefing" (backward compat)
- Contextual navigation on every content page (no dead ends)

### Analytics / Journey Instrumentation
Server endpoint for events:
- `page_view`, `solution_view`, `sector_view`, `proof_view`, `insight_view`
- `ask_started`, `ask_completed`
- `newsletter_started`, `newsletter_completed`
- `contact_started`, `contact_completed`
- `cta_clicked`

Contextual metadata: route, content type, solution, sector, CTA, journey stage

### Accessibility & Responsive
- WCAG AA on all new/modified components
- 390px responsive verification (Playwright/axe)
- `prefers-reduced-motion` respected
- Semantic heading order (h1→h2→h3)
- Focus indicators visible
- Color not only signal

### Brand Compliance
- Navy `#070A40`, Red `#E63946`, Cyan `#00BFFF`, Arial scale, 4px grid
- Official logo assets only (`brand/logos/`)
- Honesty badges on all claims
- No invented metrics — all from registries
- Canonical 90-agent count from `agent-registry.public.json`

## Acceptance Criteria (Per §40)

### Architecture
- [ ] All major journey routes exist
- [ ] Routes logically connected
- [ ] Direct-entry routes understandable
- [ ] No major page is a dead end

### Visitor Intent
- [ ] Each major page has clear visitor purpose
- [ ] Primary CTAs reflect page intent
- [ ] Secondary paths provide contextual exploration

### Solutions
- [ ] Solutions connect to sectors
- [ ] Solutions connect to proof
- [ ] Solutions provide clear engagement pathways

### Sectors
- [ ] Sectors connect to relevant solutions
- [ ] Sector evidence represented honestly
- [ ] Sector pages provide clear next actions

### Proof
- [ ] Evidence ladder implemented consistently
- [ ] Unsupported claims not introduced
- [ ] Proof connected contextually to claims
- [ ] Canonical 90-agent count preserved

### Insights
- [ ] Insights connect to relevant solutions/sectors
- [ ] Newsletter journey works
- [ ] Ask LightSpeed pathway available

### Ask LightSpeed
- [ ] Knowledge boundary respected
- [ ] Unknown/out-of-bound questions handled appropriately
- [ ] Relevant site content discoverable

### Contact
- [ ] Contact journey clear
- [ ] Form has appropriate qualification information
- [ ] Turnstile verification works
- [ ] Submission confirmation exists

### Conversion
- [ ] Engagement pathways measurable
- [ ] CTA interactions instrumented
- [ ] Contact and newsletter events tracked
- [ ] Post-contact transition clearly defined

### UX
- [ ] Desktop journey works
- [ ] Mobile journey works (390px verified)
- [ ] Accessibility preserved (WCAG AA)
- [ ] Progressive disclosure intact
- [ ] Visual design consistent with LightSpeed design system