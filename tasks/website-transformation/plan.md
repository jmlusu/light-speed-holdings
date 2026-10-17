# Spec: LightSpeed Website Transformation & Repository Consolidation

## Objective
Transform the LightSpeed public website into a coherent, production-ready, premium public website that expresses the LightSpeed business model, AI Company Builder, African operating context, governance model, use cases, thought leadership, and commercial entry points. The existing repository is a transitional state containing current website implementation, legacy components, duplicate content/sever registries, proof terminology, legacy offers, AI Company Builder backend, internal dashboards, Athena, Pharos infrastructure, local/open-weight model infrastructure, multiple competing design-system definitions, multiple generations of brand assets, generated artifacts, stale agent count references, and obsolete UI concepts.

Per the Website Transformation & Repository Consolidation Directive (V1.0, CRITICAL priority, STATUS: IMPLEMENT NOW), the website must:
- Become ONE coherent LightSpeed experience (not a collection of AI landing pages, SaaS dashboard, generic AI consultancy, Pinterest screenshots, product catalog, or blog)
- Communicate CALM INTELLIGENCE: Curiosity → Clarity → Confidence → Action
- NOT feel like internal AI control plane exposed to customers
- Feel like: LIGHTSPEED HOLDINGS — AI-native company builder and operating company built from Malawi for Southern Africa and Africa

Success is defined by the 25/25 Definition of Done (all criteria met).

## Agent Team (from AGENTS.md analysis — 131+ skills curated)

### Core Orchestrators
- `ls-creative-director` — Reads creative briefs, routes skill chains, produces executable briefs (AGENTS.md:246)
- `ls-design-system` — MUST load first by any creative skill; brand tokens in `brand/tokens/`; enforces navy #070A40, cyan #00BFFF, red #E63946, Arial type scale, 4px grid (AGENTS.md:245)

### Design & Frontend
- `ls-frontend-design` — On-brand React/Spa builder; enforces design system; targets repo-root Vite React SPA (React + Tailwind 4 + framer-motion + lucide + recharts); QA via Playwright → `ls-artifact-qa` (AGENTS.md:250)
- `ls-presentation-design` — Board presentations, investor decks; branded 10x7.5in slides, navy left rail, navy/red/cyan palette, Arial scale (AGENTS.md:250)
- `ls-visual-storytelling` — Message → visual narrative → medium choice (article-illustrations for Grav, k-dense-infographics for professional, Mermaid via ls-diagramming for structures, SVG/HTML one-pagers) → `ls-artifact-qa` gate (AGENTS.md:250)
- `ls-brand-advertising` — Commercial creative; enforces on-brand (navy/red/cyan, official logo, tagline); per-platform ad dimensions automatic (AGENTS.md:250)
- `ls-diagramming` — LightSpeed diagram engine; Mermaid (architecture/process/flow), SVG/D3 (custom data visuals), Kroki fallback; brand-palette restyle always (AGENTS.md:250)

### Quality Assurance (FINAL GATE on EVERY artifact)
- `ls-artifact-qa` — Runs LAST on EVERY artifact: Visual/Brand/UX/Accessibility/Content QA → APPROVE or FIX→RENDER AGAIN. Includes Playwright probe for screenshots, overflow, alt-text, empty-heading checks. (AGENTS.md:250)
- `code-review-and-quality` — Multi-axis code review before any merge (AGENTS.md:235)
- `bug-hunter` — Systematic debugging; trace symptoms to root cause; implement fixes; prevent regression (AGENTS.md:235)
- `tdd` — Red-green-refactor cycle (AGENTS.md:235)

### Data/Model Governance
- `domain-modeling` — Pin down terminology/ubiquitous language; record architectural decisions for future engineers (AGENTS.md:236)
- `spec-driven-development` — Create specs before coding; use when starting new project/feature/significant change/unclear requirements (AGENTS.md:237)
- `incremental-implementation` — Deliver changes incrementally with checkpoints; use when task feels too big for one step (AGENTS.md:237)
- `code-structure` — Identify duplicated operational logic across domain flows; decide what belongs in actions vs shared services (AGENTS.md:237)
- `evidence-driven-testing` — Record visual proof while testing; hands-on computer use; screen recording with structured test/assertion annotations; post video + results summary instead of prose claims (AGENTS.md:237)
- `validate-data` — Validate analysis accuracy, well-supported, ready to share/use for decision; review methodology, calculations, comparisons, visuals, caveats, conclusions (AGENTS.md:237)
- `market-sizing` — Estimate TAM/SAM/SOM with transparent assumptions; model/provider agnostic; "use least expensive model that can reliably do the job" (AGENTS.md:237)
- `data-analytics` — Quantitative product/business analysis; data quality checks; metric diagnostics; KPI design/reporting; dashboards; semantic layers; evidence-backed recommendations (AGENTS.md:237)
- `building-accessible-interfaces` — WCAG-oriented a11y; keyboard nav, screen readers, focus management, ARIA, color contrast, form labels/error announcements, reduced motion, touch target size (AGENTS.md:237)

### Specialized Skills (as needed)
- `pharos-thought-leadership-lead` — Heads Pharos dept; turns engineering/research/experimentation/field observations into public intellectual work (AGENTS.md:251)
- `pharos-media-pr` — Creates recurring Pharos visual formats (PHAROS BRIEF, FIELD NOTE, RESEARCH NOTE, SYSTEM MAP, DATA STORY, AI ECONOMICS, AFRICA WATCH) (AGENTS.md:251)
- `k-dense-infographics` — 10 infographic types, 8 industry styles, colorblind-safe palettes; integrates research lookup/web search; Gemini quality review (AGENTS.md:237)
- `article-illustrations` — Hand-drawn Grav character IP illustrations (AGENTS.md:237)
- `k-dense-mermaid-skill` — Natural language → 11+ diagram types (.mmd validation); output PNG/SVG/PDF via mmdc/Kroki; vision self-checks on rendered PNGs (AGENTS.md:237)
- `ls-documentation-engineering` — Diátaxis-classified content (tutorial/how-to/explanation/reference); READMEs, API docs, developer portals, release notes, changelogs, FAQs; wraps documentation-and-adrs skill for decision records (AGENTS.md:251)
- `spec-check` — Validates Claude Code skills against agentskills specification; catches structural, semantic, naming issues before users do (AGENTS.md:237)

### Success Criteria (25/25 Definition of Done)
The work is complete only when all 25 criteria are met (see Directive §42). Each criterion maps to specific agent capabilities as defended in the scoring analysis.

## Phased Implementation Plan (per Directive §36)

### PHASE 0 — Repository Audit
Produce: `REPOSITORY_CLEANUP_PLAN.md`, `WEBSITE_ARCHITECTURE.md`, `CONTENT_ARCHITECTURE.md`, `LIGHTSPEED_DESIGN_SYSTEM.md`, `MEDIA_ARCHITECTURE.md`, `CLAIMS_GOVERNANCE.md`
- Agents: `codebase-audit-pre-push`, `incremental-implementation`, `writing-plans`
- No destructive changes initially; classify every major artifact: KEEP/REFactor/DEPRECATE/MOVE/DELETE
- Risk: Low (audit-only phase)

### PHASE 1 — Canonicalize Data
Fix: 90 roles (89 AI + 1 Human CEO), 20 departments, H-A-O-M-T-G-V, sector registry, solution registry, use-case registry, FAQ registry, CTA registry, claims registry
- Agents: `spec-driven-development`, `domain-modeling`, `brainstorming` (MUST use before any creative work per AGENTS.md:237)
- Key deliverables: canonical 90-role model explanation, 20 departments, H-A-O-M-T-G-V framework, 10-sector taxonomy
- Risk: Medium (data restructure affecting all pages)

### PHASE 2 — Canonicalize Design System
Implement new logo; remove competing visual tokens; enforce brand tokens across all pages
- Agents: `ls-design-system` (CANNOT be bypassed per AGENTS.md:245), `impeccable`, `code-structure`
- Key deliverables: `docs/LIGHTSPEED_DESIGN_SYSTEM.md`, `src/brand/tokens/brand-tokens.json`, new geometric "L" logo SVG, brand token enforcement across all pages
- Risk: Medium (visual rebrand affecting all pages)

### PHASE 3 — Refactor Global Shell
Header, Navigation, Footer, Page container, CTA system, Theme, Typography, Motion, Motion principle: "Slow to the eye. Fast to the mind." Respect prefers-reduced-motion.
- Agents: `ls-frontend-design`, `ls-creative-director`, `ls-artifact-qa` (final gate on every change)
- Key deliverables: consolidated header/nav/footer, CTA system (primary: "START A CONVERSATION", secondary: "REQUEST AI READINESS ASSESSMENT"), theme (navy/red/cyan/Arial/4px grid), motion patterns, no "Proof" navigation, no stale agent counts
- Risk: High (structural changes to base layout)

### PHASE 4 — Implement Key Pages
Home, AI Company Builder, What We Do, Solutions, Use Cases, Sectors, Insights, About, FAQ, Contact, Assessment
- Agents: `ls-frontend-design`, `ls-presentation-design`, `ls-social-media-design`, `ls-visual-storytelling`, `ls-artifact-qa`
- Key deliverables: all 14+ public routes with correct navigation, no Proof items, correct 90-role explanation, H-A-O-M-T-G-V prominent, open-weight economics communicated, Pharos as thought-leadership, academia/universities/regulators in sectors, FAQ with 27 evidence-controlled questions, media distributed per §19 Types A-K, no fabricated claims
- Risk: High (multiple page implementations)

### PHASE 5 — Media Implementation
Per §19 Media Types A-K and §20 Media Placement Strategy; extract composition/color/light/material/typography/spacing/image treatment/motion/geometry from Pinterest references into reusable LightSpeed visual language; result should feel: "LightSpeed has its own visual identity inspired by these references" NOT "LightSpeed copied these websites."
- Agents: `ls-visual-storytelling`, `ls-brand-advertising`, `k-dense-infographics`, `article-illustrations`, `k-dense-mermaid-skill`
- Key deliverables: hero imagery, H-A-O-M-T-G-V infographic, AI Company Builder org chart, model routing infographic, Africa AI economics infographic, use case cards, architecture diagrams, African maps, research visuals, human/leadership micro-illustrations
- Risk: Medium-high (creative implementation)

### PHASE 6 — SEO/Accessibility/Performance
§31 SEO (unique title, meta description, canonical URL, OG image, structured headings, accessible images, alt text, semantic HTML, internal links, structured content around: LightSpeed Holdings, AI Company Builder, Agentic AI, African AI, AI governance, AI automation, AI strategy, Open-weight AI, Sovereign AI, Malawi AI, SADC AI, AI use cases, AI policy, AI research); §32 accessibility (keyboard nav, visible focus, semantic headings, sufficient contrast, alt text, reduced motion, accessible dialogs, accessible forms, no color-only info, screen-reader status badges); §30 performance (fast initial load, optimized images, lazy-loaded media, responsive design, accessible navigation, minimal JS, progressive enhancement, graceful degradation, mobile-first; CSS/SVG/HTML for diagrams, no blocking 3D/animation)
- Agents: `building-accessible-interfaces`, `design-kpis`, `observability-and-instrumentation`, `performance-optimizer`, `ls-frontend-design`
- Key deliverables: all public pages with SEO markup, WCAG-compliant accessibility, performance under targets, CSS/SVG/HTML diagrams
- Risk: Medium (technical implementation)

### PHASE 7 — Full Route QA
Per §37 Critical Website QA: visit every public route; verify: no Proof navigation remains; no stale "Proof" terminology (except internal historical refs); no stale agent count; no unsupported client claim; no duplicate CTA; no broken images; no missing alt text; no inconsistent typography; no inconsistent buttons; no orphaned routes; no dead links; no mobile overflow; no accessibility failures; no accidental Athena exposure; no internal dashboard exposure; no stale design-system artifacts; no console errors
- Agents: `ls-artifact-qa` (final gate), `bug-hunter`, `code-review-and-quality`, `tdd`
- Key deliverables: all public routes verified, zero console errors, production-quality mobile experience, site credible enough for immediate use
- Risk: High (comprehensive QA)

## Open Questions (require human resolution before advancing)
1. **Brand token format**: `brand-tokens.json` flat key-value vs. nested semantic structure?
2. **Pharos visual formats priority**: Which of 7 recurring formats (BRIEF, FIELD NOTE, RESEARCH NOTE, SYSTEM MAP, DATA STORY, AI ECONOMICS, AFRICA WATCH) for Phase 1?
3. **CTA labeling**: Additional contextual CTAs beyond "START A CONVERSATION" / "REQUEST AI READINESS ASSESSMENT"?
4. **Athena boundary**: `/athena` vs. `apps/athena` from start?
5. **Repository cleanup risk tolerance**: DELETE vs. DEPRECATE vs. MOVE vs. KEEP?
6. **Timeline sequencing**: Which PHASES compress/parallelize given "CRITICAL BUSINESS PRIORITY"?

## Parallelization Opportunities (per spec-driven-development AGENTS.md:237)
- Safe: Template creation + keyword research; platform profile setup across 6 platforms; analytics setup + keyword list; Reddit + Quora engagement
- Must be sequential: Profile setup → Warm-up → Full cadence; Phase 0 → Phase 1 → Phase 2 → Phase 3
- Needs coordination: Content creation ↔ Template availability; CEO content ↔ Company content calendar; Collaboration outreach ↔ Content calendar

## Verification (before advancing to next phase)
- [ ] Human has reviewed and approved the spec
- [ ] Success criteria are specific and testable
- [ ] Boundaries (Always/Ask First/Never) are defined
- [ ] The plan is saved to `tasks/website-transformation/plan.md`
- [ ] The task list is saved to `tasks/website-transformation/todo.md`

---
*Plan version 1.0 — created during build mode. Ready for human review before Phase 1 execution begins.*
