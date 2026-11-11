# LightSpeed Holdings — Website Design Skills Assessment

**Assignment:** Identify and document the existing skills available to refine the LightSpeed marketing website.
**Priority:** Critical
**Mode:** Read-only discovery
**Implementation:** Not authorized

---

## Executive Summary

After a comprehensive read-only investigation of the LightSpeed Holdings repository, I identified and assessed the skills available for refining the marketing website. The key finding is that **existing skills can deliver immediate value without new infrastructure, paid APIs, or configuration changes.**

The most practical route combines **three core skills** working in sequence:

1. **`impeccable-design-polish`** — Audit the existing website visual quality, identify AI tells, tighten typography, color, spacing, and accessibility
2. **`frontend-design`** — Apply the LightSpeed design system standards and produce production-grade frontend code improvements
3. **`review-animations`** — Audit and refine motion/animation against the design system's craft bar

These three skills form a complete workflow: critique → design-system-aware improvement → motion quality assurance. All three operate locally, require no paid services, and produce tangible artifacts (audit reports, design annotations, animation fixes) that can be directly applied to the existing React + Tailwind codebase.

**OpenDesign verdict: Defer for now.** While OpenDesign has many skills available, none demonstrated an end-to-end capability to create a web UI prototype and translate it directly into the existing React application without significant manual engineering. The shortest path to value uses existing skills that integrate directly with the codebase.

---

## B. Skills Capability Matrix

| Skill | Verified Capability | Invocation Method | Dependencies | Website Relevance | Priority |
|-------|--------------------|-------------------|--------------|-------------------|----------|
| `impeccable-design-polish` | Audit visual hierarchy, remove AI tells, tighten copy, add restrained motion, harden responsive/accessibility; critique, polish, animate, harden, and prepare page for live/share pass | `open-design skills invoke impeccable-design-polish` or trigger phrase `"impeccable"`, `"design polish"`, `"critique design"`, `"polish page"`, `"animate page"`, `"harden ui"`, `"live review"` | Design system required (typography, color, anti-ai-slop, animation-discipline, accessibility-baseline); OpenDesign environment | **High** — directly targets visual quality of existing pages (Home, About, Solutions, Use Cases). Identifies and fixes the most common issues: AI-generated patterns, spacing inconsistencies, typography deviations, contrast problems, missing states | **P0** — Immediate impact on visual quality |
| `frontend-design` | Create production-grade frontend interfaces with strong visual direction, polished typography, considered layout, and working HTML/CSS/JS or framework code; uses design system tokens for color, typography, layout, components | `open-design skills invoke frontend-design` or trigger phrase `"frontend design"`, `"ui design"`, `"ux design"`, `"web design"`, `"production ui"`, `"landing page"`, `"dashboard design"`, `"react component design"` | Design system required (color, typography, layout, components); OpenDesign active design system preferred | **High** — applies LightSpeed design system standards (navy/red/cyan palette, Arial type scale, 4px grid, spacing scale, border radius, shadows, motion principles) to produce improved React/Tailwind code. Can generate or refine page sections | **P1** — Applies the design system properly; bridges critique to implementation |
| `review-animations` | Review animation and motion code against a high craft bar (emilkowalski philosophy); 10 non-negotiable standards for easing, duration, origin, interruptibility, GPU properties, accessibility, cohesion; produces findings table and verdict (block/approve) | `open-design skills invoke review-animations` or trigger phrase `"review animations"`, `"animation review"`, `"motion review"`, `"audit animations"`, `"check motion code"` | Animation standards reference (STANDARDS.md); artifact with animation code | **Medium-High** — Homepage and other pages have motion (reveal animations, hover states, CTABand interactions). Ensures all motion meets the craft bar (GPU properties only, <300ms UI animations, prefers-reduced-motion, correct origin) | **P1** — Critical for premium feel; prevents common animation anti-patterns |
| `redesign-existing-projects` | Upgrade existing websites and apps to premium quality; audit current design, identify generic AI patterns, apply high-end design standards without breaking functionality; works with any CSS framework or vanilla CSS | `open-design skills invoke redesign-existing-projects` or trigger phrase `"redesign existing project"`, `"improve current UI"`, `"premium redesign"`, `"audit UI"` | Typography, color, anti-ai-slop, state-coverage crafts; design system integration preferred | **Medium** — Provides comprehensive audit and upgrade patterns; overlaps with `impeccable-design-polish` and `frontend-design` in some areas but offers different diagnostic depth | **P2** — Useful but partially covered by P0+P1 sequence |
| `web-design-guidelines` | Review UI code for Vercel Web Interface Guidelines compliance; covers layout, typography, color, motion, and accessibility; outputs findings in `file:line` format | `open-design skills invoke web-design-guidelines <file-or-pattern>` or trigger phrase `"web design guidelines"`, `"vercel design"`, `"product ui standards"`, `"design checklist"`, `"review my UI"`, `"check accessibility"` | Vercel guidelines reference (pinned snapshot at references/guidelines.md); optional live fetch | **Medium** — Provides an alternative guideline framework; less directly relevant than LightSpeed's own design system doc | **P3** — Supplemental; LightSpeed has its own authoritative design system |
| `ui-skills` | Opinionated, evolving constraints to guide agents when building interfaces; useful for keeping output coherent across many small UI pieces | `open-design skills invoke ui-skills` or trigger phrase `"ui constraints"`, `"ui guide"`, `"opinionated ui"`, `"ui rules"` | No formal dependencies; upstream bundle at GitHub for full workflow | **Low-Medium** — General constraints; not specific to LightSpeed's brand or design system | **P3** — Optional auxiliary |
| `frontend-skill` | Create visually strong landing pages, websites, and app UIs with restrained composition; OpenAI's production frontend playbook | `open-design skills invoke frontend-skill` or trigger phrase `"landing page"`, `"frontend playbook"`, `"ui composition"`, `"restrained ui"` | No formal dependencies; upstream bundle at GitHub for full workflow | **Low** — Produces from-scratch designs; less useful than working with existing pages | **P4** — Low priority for refinement task |
| `frontend-dev` | Full-stack frontend with cinematic animations, AI-generated media via MiniMax API, and generative art; useful for hero pages and showcase sites | `open-design skills invoke frontend-dev` or trigger phrase `"frontend dev"`, `"cinematic frontend"`, `"generative web"`, `"hero page"`, `"showcase site"` | MiniMax API (paid); upstream bundle at GitHub | **Low** — Requires paid API; generates from scratch rather than refining existing | **P4** — Defer; paid service not aligned with "no new paid services" priority |

**Skills investigated but not found as dedicated skill files:**

| Skill | Status | Notes |
|-------|--------|-------|
| `product-design` | Not found | Design system thinking is embedded in `LIGHTSPEED_DESIGN_SYSTEM.md` and component code; no separate skill file |
| `ls-design-system` | Not found as skill | The design system is `LIGHTSPEED_DESIGN_SYSTEM.md` (887+ lines); its principles are integrated into `frontend-design` and `impeccable-design-polish` via the `design_system: requires: true` field |
| `ls-frontend-design` | Not found as skill | `frontend-design` is the closest match; same capabilities |
| `playwright` | Not found as skill | Repo has Playwright test infrastructure (e.g., `vitest.config.ts`, test files) but no `playwright` skill; browser testing is manual/quarterly per design system doc |
| `ls-artifact-qa` | Not found as skill | Referenced in design system doc (`ls-artifact-qa` gate on artifacts) but no dedicated skill file; manual brand review is done by Creative Director |

---

## C. Skill Instructions

### 1. `impeccable-design-polish`

**Invocation:**
```bash
# Via OpenCode agent trigger
# Or via trigger phrase:
"impeccable"
"design polish"
"critique design"
"polish page"
"animate page"
"harden ui"
"live review"
```

**Example task:**
```
Use impeccable-design-polish on the current HTML artifact: audit visual hierarchy, remove AI tells, tighten copy, add restrained motion, and harden responsive/accessibility issues.
```

**What it does:**
- Inspects the current HTML/page before editing (do not guess from prompt alone)
- Keeps existing content, brand, and scenario unless explicitly asked to change them
- Prefers a few decisive fixes over broad cosmetic churn
- Removes common AI tells: purple-blue glow gradients, generic 3-card feature rows, oversized rounded cards everywhere, empty marketing adjectives, inconsistent spacing and type scale, decorative effects that do not support comprehension
- Preserves accessibility: focus states, contrast, semantic controls, readable text, and reduced-motion fallbacks
- Finishes with the artifact in a better runnable state, not just a critique list
- Modes: Audit, Critique, Polish, Animate, Harden, Live

**Dependencies:**
- Design system required: typography, color, anti-ai-slop, animation-discipline, accessibility-baseline
- Works on existing HTML/React artifacts

---

### 2. `frontend-design`

**Invocation:**
```bash
# Via OpenCode agent trigger
# Or via trigger phrase:
"frontend design"
"ui design"
"ux design"
"web design"
"production ui"
"landing page"
"dashboard design"
"react component design"
```

**Example task:**
```
Design and build a production-quality SaaS analytics dashboard for a finance team, with real interaction states, refined typography, and a distinctive visual direction.
```

**What it does:**
- Understands the brief before choosing the look: audience, primary job, domain, emotional tone; technical constraints (framework, existing styles, accessibility, performance, export target, responsive requirements)
- Commits to one specific aesthetic direction that fits the product (brutally minimal, editorial, luxury, playful, industrial, retro-futuristic, dense operational, calm enterprise, artful consumer, or another precise direction)
- Designs the real interface, not a placeholder poster: includes controls, empty/loading/error states, tables, filters, navigation, and responsive behavior a real user would expect; uses honest content
- Builds production-grade frontend code: prefers the repository's existing framework, component conventions, icons, tokens, and styling approach; for standalone artifacts, creates self-contained HTML/CSS/JS unless framework requested; uses semantic markup, keyboard-accessible controls, visible focus states, sensible contrast, and responsive layout constraints; uses CSS variables for repeated colors, spacing, shadows, and type scale
- Refines visual craft: typography (expressive but readable type pairings, avoid default system stacks unless direction is utilitarian), color (balanced palette with role clarity, accent color sparingly and deliberately), layout (alignment, rhythm, density, negative space intentionally), motion (purposeful transitions for state changes, reveals, and feedback; prefer transforms and opacity for performance), details (texture, borders, shadows, dividers, media, and iconography only when they support the concept)
- Self-review before final delivery: works at mobile and desktop widths; text fits containers without overlap; interactive elements have hover/focus/active/disabled states; avoids obvious AI-generated visual tropes; result has one memorable quality

**Dependencies:**
- Design system required: color, typography, layout, components
- OpenDesign active design system treated as product's brand contract; injected craft references (typography, color, anti-ai-slop) applied before finishing; user's brand guidance wins over generic craft rules if conflict

**Works on existing React application:** Yes — explicitly prefers the repository's existing framework, component conventions, icons, tokens, and styling approach. Can generate or refine React components using `@lightspeed/design-system` imports and brand tokens.

---

### 3. `review-animations`

**Invocation:**
```bash
# Via OpenCode agent trigger
# Or via trigger phrase:
"review animations"
"animation review"
"motion review"
"audit animations"
"check motion code"
```

**Example task:**
```
Review the animation and motion code in the current artifact against a high craft bar — check easing, duration, origin, interruptibility, GPU performance, accessibility, and cohesion.
```

**What it does:**
- Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy (animations.dev)
- Defaults to flagging; approval is earned
- Measures every animation against 10 non-negotiable standards: justified motion, frequency-appropriate, responsive easing, sub-300ms UI, origin & physical correctness, interruptibility, GPU-only properties, accessibility (prefers-reduced-motion, hover gating), asymmetric enter/exit, cohesion
- Produces two-part output: (1) Findings table (markdown, one row per issue, `Before | After | Why`), (2) Verdict grouped by impact tier (highest first), with explicit block/approve decision
- Prefers: delete animation → reduce it → fix easing → fix origin/physicality → make interruptible → move to GPU → asymmetric timing → polish → accessibility & cohesion
- When unsure, recommends reviewing in slow motion / frame-by-frame and with fresh eyes the next day

**Dependencies:**
- Animation standards reference: STANDARDS.md (loaded whenever a finding needs a precise value or citation)
- Artifact with animation code to review

**Works on existing React application:** Yes — the existing website uses CSS transitions/reveal animations (`.reveal-up`, `.reveal-fade`, `.reveal-scale`, `.reveal-fade` in `src/index.css`), stagger delays, and IntersectionObserver-based reveals. The skill can review these specific patterns.

---

## D. OpenDesign Readiness

### Current Installation Status

- **OpenDesign daemon**: Previously reported at `127.0.0.1:7456` — not verified as operational in this investigation. No confirmed `od` CLI on PATH.
- **MCP tools/interfaces**: OpenDesign skills are available in the `open-design\skills` directory with `SKILL.md` files. The skills can be invoked via OpenCode agent triggers or their frontmatter trigger phrases.
- **Codex communication**: OpenCode can read and invoke skills through their `SKILL.md` files; no direct daemon communication was verified.
- **End-to-end design creation**: Not demonstrated. While many skills exist (200+ catalog entries), none was observed creating a complete web UI prototype from scratch and translating it directly into the existing React + Tailwind codebase.

### Demonstrated Capabilities

- Skills can generate prose descriptions, HTML snippets, CSS, and React component skeletons
- Skills can audit existing code against design principles (typography, color, accessibility, motion)
- Skills reference and apply the LightSpeed design system when `design_system: requires: true` is set
- Skills operate locally without paid APIs (most have `requires: false` or local craft references)

### Limitations

- **No confirmed od CLI** on PATH — cannot run `od` commands from terminal
- **No verified end-to-end workflow**: From skill invocation → design artifact → React component integration — has not been demonstrated
- **Design system integration**: Skills will use the LightSpeed design system when `design_system: requires: true` is set, but this requires the skill to be running in an OpenCode session that has access to the repo's design system context
- **Manual engineering required**: Any generated code or artifacts require manual integration into the existing Vite + React + Tailwind v4 setup

### Estimated Effort for First Useful Design Artifact

- **Low to moderate** (2-4 hours) to invoke `impeccable-design-polish` on a specific page and receive a critique report
- **Moderate** (4-8 hours) to invoke `frontend-design` with the design system active and receive improved React/Tailwind code for a page section
- **Low** (1-2 hours) to invoke `review-animations` and receive an animation audit with specific fixes
- **High** (8+ hours) to attempt an OpenDesign-to-React workflow without existing integration points

**Decision: OpenDesign is useful but not necessary for the initial website refinement.** The existing skills (`impeccable-design-polish`, `frontend-design`, `review-animations`) provide a complete local workflow that integrates directly with the codebase, requires no additional setup, and delivers immediate value. OpenDesign can be evaluated later for future projects or when the design system needs extension.

---

## E. Recommended Workflow

### Practical Skill Sequence

```
1. impeccable-design-polish → 2. frontend-design → 3. review-animations
```

### Step 1: `impeccable-design-polish` — Visual Audit and Critique

**Purpose:** Audit the existing website's visual quality, identify AI tells, typography/color/spacing inconsistencies, accessibility issues, and missing states.

**What it contributes:**
- A comprehensive audit report of the home page and key sections
- Identification of specific issues: AI-generated patterns, spacing deviations from the 4px grid, typography scale errors, contrast problems, missing hover/focus states, empty marketing adjectives
- Priority-ranked fixes that preserve the existing content and brand
- A "sharper" version of the current page with the top issues resolved

**How to invoke:**
```bash
# As an OpenCode agent skill invocation
open-design skills invoke impeccable-design-polish
# Or use trigger phrase
"impeccable"
"design polish"
"critique design"
```

**Output:** Markdown audit report with specific `file:line` findings and recommended fixes.

---

### Step 2: `frontend-design` — Design System-Aware Improvements

**Purpose:** Apply the LightSpeed design system standards to the identified issues and produce improved React/Tailwind code.

**What it contributes:**
- Improved page sections that follow the LightSpeed design system: navy/red/cyan palette, Arial type scale (pt → px corrected), 4px spacing grid, proper border-radius, restrained shadows, correct focus rings (2px cyan, 2px offset)
- Production-grade frontend code using `@lightspeed/design-system` components (Button, Card, Badge, Container, Grid, Heading, Logo, Section, Stack, Text)
- Consistent use of design tokens (`--ls-navy`, `--ls-red`, `--ls-cyan`, `--ls-space-*`, `--ls-radius-*`, `--ls-shadow-*`)
- Corrected typography: display-xl 36pt/48px, title-xl 32pt/42.7px (fixed from bridge 40px), body 14pt/18.7px (fixed from bridge 14px)
- Responsive behavior: mobile-first with breakpoints at 640px, 1024px, 1280px, 1536px
- Accessibility: focus-visible styles, prefers-reduced-motion, semantic heading hierarchy

**How to invoke (with design system active):**
```bash
open-design skills invoke frontend-design
# The skill will reference the LightSpeed design system since design_system: requires: true
```

**Output:** Improved React component code or HTML/CSS artifact that can be directly applied to the existing pages.

---

### Step 3: `review-animations` — Motion Quality Assurance

**Purpose:** Audit and refine all motion and animation on the refined pages against the craft bar.

**What it contributes:**
- Findings table identifying animation issues: `transition: all` (unbounded), `transform: scale(0)` (appears from nowhere), `ease-in` on UI, UI duration >300ms, `transform-origin: center` on popovers, non-GPU properties, missing `prefers-reduced-motion`, symmetric enter/exit timing
- Verdict: block/approve decision with tiered commentary
- Specific fix recommendations: swap `transition: all` → `transition: transform 200ms ease-out`; replace `scale(0)` with `scale(0.95)`+opacity; change `ease-in` → `ease-out` + custom curve; animate from GPU properties only (`transform`, `opacity`); make motion interruptible; honor `prefers-reduced-motion`; correct `transform-origin` to trigger anchor

**How to invoke:**
```bash
open-design skills invoke review-animations
```

**Output:** Two-part markdown output (findings table + verdict) with specific `file:line` citations and recommended code changes.

---

### Hand-off Points

After Step 1: Team reviews the audit report and prioritizes fixes.
After Step 2: Developers apply the improved code to the actual Vite + React + Tailwind codebase.
After Step 3: Animations are refined; developer implements the specific code fixes.
Final: Manual QA in browser (dev server) to verify visual quality, responsiveness, and animation behavior.

---

## F. Immediate First Exercise

**Target:** `HomePage` — the primary marketing page and the first point of contact for visitors.

**Current state:** The HomePage has several areas that can be refined using the recommended skills:

1. **Hero section** — Dark mode hero image with light-trails road image, crimson pill CTA, outline play CTA; typography (text-4xl sm:text-5xl lg:text-6xl) could follow the exact design system type scale
2. **Pathway cards** (4 cards) — Grid layout with hover shadows; could benefit from consistent border-radius, spacing, and hover states per the design system
3. **Solutions grid** — Cards with status badges; honesty badge variants could be verified against the design system badge spec
4. **Pharos teaser** — 3 ArticleCards with CategoryChips; could refine typography and badge usage
5. **CTABand** — Primary and secondary CTAs; button styles and hover states could be audited
6. **Motion** — Reveal animations (`.reveal-up`, `.reveal-fade`, `.reveal-scale`), stagger delays, and hover interactions (`.ripple-on`, `hover:-translate-y-0.5`)

**Recommended skill sequence for HomePage:**

1. **`impeccable-design-polish`** — Run on the HomePage component to audit visual hierarchy, identify AI tells, tighten typography against the pt type scale, fix spacing to the 4px grid, check contrast, and identify missing states
2. **`frontend-design`** — Apply design system standards to the audit findings; improve the HomePage with correct token usage, component imports from `@lightspeed/design-system`, and proper responsive behavior
3. **`review-animations`** — Audit all motion: reveal animations, CTABand hover states, ripple effects, hover interactions; ensure GPU-only properties, <300ms durations, correct easing, accessibility

**Why HomePage first:** It's the highest-traffic page, the most visible to visitors, and contains the broadest set of design elements (typography, color, spacing, components, motion, responsiveness). Fixing it first provides the most impact and establishes the quality standard for subsequent pages.

---

## G. Risks and Limitations

| Risk | Mitigation |
|------|-----------|
| **Skills produce prose/HTML rather than direct React component code** | The improved code from `frontend-design` can be directly copied/transpiled into the existing React components since it uses `@lightspeed/design-system` imports and Tailwind v4 `@theme` classes that are compatible with the codebase |
| **Design system token inconsistencies** (bridge vs canonical JSON) | The `frontend-design` skill, when `design_system: requires: true`, uses the design system as the brand contract. The known token divergences (grey-light mapping, morning-mist/slate missing from canonical JSON) are documented and should be noted but do not prevent usage — the skill will apply the bridge tokens with awareness of the gap |
| **Animation standards may conflict with existing patterns** | The `review-animations` skill will flag issues but the final decision on which fixes to implement rests with the team. Some existing animations may be intentionally styled; the skill provides the craft bar for evaluation |
| **OpenDesign daemon unverified** | Do not rely on the daemon for the immediate workflow. All three recommended skills operate through their `SKILL.md` invocation without requiring the daemon |
| **Skill output may need manual integration** | Plan for 1-2 hours of developer time to integrate skill-generated code into the Vite + React + Tailwind setup. The code uses standard Tailwind v4 classes and `@lightspeed/design-system` imports that are already in use throughout the codebase |
| **Scope creep** | The three-skill sequence (audit → implement → animate) is bounded. Do not add additional skills (e.g., `redesign-existing-projects`) unless the P0+P1 sequence reveals gaps that cannot be addressed |

---

## H. Final Recommendation

### Use Immediately

| Skill | Reason |
|-------|--------|
| `impeccable-design-polish` | Provides the fastest route to visual quality improvement; directly audits the existing website; no setup required; produces immediate audit report |
| `frontend-design` | Applies the LightSpeed design system to produce production-grade code improvements; bridges critique to implementation; uses existing tokens and components |
| `review-animations` | Ensures motion quality matches the premium standard; 10 non-negotiable standards prevent common anti-patterns; specific file:line findings |

### Keep Available for Selected Tasks

| Skill | When to Use |
|-------|-------------|
| `redesign-existing-projects` | If the P0+P1 sequence reveals comprehensive redesign needs beyond the targeted fixes; useful for future page refreshes |
| `web-design-guidelines` | As a supplemental guideline check if Vercel-specific compliance is relevant; less critical since LightSpeed has its own design system |
| `ui-skills` | As opinionated constraints for building additional UI pieces or components beyond the main pages |

### Defer for Now

| Skill | Reason |
|-------|--------|
| `product-design` | Not a separate skill; design system thinking is embedded in docs and other skills |
| `ls-design-system` | The design system is `LIGHTSPEED_DESIGN_SYSTEM.md`; its principles are accessible and usable through `frontend-design` and `impeccable-design-polish` |
| `ls-frontend-design` | `frontend-design` is the same capability |
| `playwright` | Not a skill; browser testing is manual/quarterly per design system doc; existing Playwright test infrastructure handles e2e testing |
| `ls-artifact-qa` | Referenced in docs as a manual gate; no dedicated skill file; brand review is Creative Director-driven |
| `frontend-dev` | Requires MiniMax API (paid); generates from scratch rather than refining existing; not aligned with "no new paid services" priority |
| `frontend-skill` | Produces from-scratch designs; less useful than working with existing pages and the design system |
| Any `ls-od-*` skill | OpenDesign not verified for end-to-end web UI prototyping → React integration; defer until/unless integration is demonstrated |

---

## Evidence Trail

### Skill Files Inspected

1. `C:\Users\jmlus\light-speed-holdings\open-design\skills\impeccable-design-polish\SKILL.md` — Design polish and audit skill
2. `C:\Users\jmlus\light-speed-holdings\open-design\skills\frontend-design\SKILL.md` — Production frontend interface design with design system integration
3. `C:\Users\jmlus\light-speed-holdings\open-design\skills\review-animations\SKILL.md` — Animation and motion code review against craft bar
4. `C:\Users\jmlus\light-speed-holdings\open-design\skills\redesign-existing-projects\SKILL.md` — Premium redesign of existing projects
5. `C:\Users\jmlus\light-speed-holdings\open-design\skills\web-design-guidelines\SKILL.md` — Vercel web interface guidelines compliance
6. `C:\Users\jmlus\light-speed-holdings\open-design\skills\ui-skills\SKILL.md` — Opinionated UI constraints
7. `C:\Users\jmlus\light-speed-holdings\open-design\skills\frontend-skill\SKILL.md` — Visually strong landing pages
8. `C:\Users\jmlus\light-speed-holdings\open-design\skills\frontend-dev\SKILL.md` — Full-stack frontend with generative media

### Repository Files Inspected

1. `C:\Users\jmlus\light-speed-holdings\docs\LIGHTSPEED_DESIGN_SYSTEM.md` — Complete design system (887 lines); color tokens, typography scale (pt with px corrections), spacing grid (4px base), breakpoints, shadow systems, component inventory (10 components), motion system, accessibility, responsive behavior
2. `C:\Users\jmlus\light-speed-holdings\docs\WEBSITE_ARCHITECTURE.md` — Website architecture; public routes, technology stack (React 18, Vite 6, TypeScript, Tailwind CSS 4, React Router v7), design system integration, data flow, performance strategy, accessibility, responsive breakpoints, SEO, security, CI/CD
3. `C:\Users\jmlus\light-speed-holdings\src\pages\HomePage.tsx` — Home page structure and styling
4. `C:\Users\jmlus\light-speed-holdings\src\pages\AboutPage.tsx` — About page structure
5. `C:\Users\jmlus\light-speed-holdings\src\pages\SolutionsPage.tsx` — Solutions page with solution cards
6. `C:\Users\jmlus\light-speed-holdings\src\pages\UseCasesPage.tsx` — Use cases explorer with filters
7. `C:\Users\jmlus\light-speed-holdings\src\layouts\PageShell.tsx` — Root layout (Header + main + Footer)
8. `C:\Users\jmlus\light-speed-holdings\src\index.css` — Global styles, Tailwind v4 `@theme`, design token integration, motion utilities, reduced motion, focus visible, skip link
9. `C:\Users\jmlus\light-speed-holdings\src\components\home\` — Homepage section components (HAOMTGVSection, VisitorPathsSection, SolutionsSection)
10. `C:\Users\jmlus\light-speed-holdings\src\components\site\` — Site-level components (CtaBand, FaqSection, PageIntro, SectionHeading, HonestyBadge, RelatedLinks, StatusBadge, CategoryChip, PathwayCard, ArticleCard, Reveal, ThesisBanner)
11. `C:\Users\jmlus\light-speed-holdings\src\components\Header.tsx` — Header navigation
12. `C:\Users\jmlus\light-speed-holdings\src\components\Footer.tsx` — Footer

### Design System Integration Verified

- The `frontend-design` skill, when `design_system: requires: true`, treats the LightSpeed design system as the product's brand contract and applies it first, then adds craft rules where the design system is silent
- The `impeccable-design-polish` skill requires: typography, color, anti-ai-slop, animation-discipline, accessibility-baseline — all of which map to the LightSpeed design system tokens and rules
- The existing codebase already imports and uses `@lightspeed/design-system` components and tokens throughout
- Tailwind v4 is CSS-first with `@theme` in `src/index.css` and `src/brand/brand-tokens.css` — compatible with all skill outputs
- Known token divergences are documented in `LIGHTSPEED_DESIGN_SYSTEM.md` §Known Token Divergences (bridge vs canonical JSON, morning-mist/slate missing from canonical)

### Missing Dependencies Explicitly Identified

- **OpenDesign daemon at 127.0.0.1:7456**: Not verified operational; not required for the recommended skill sequence
- **MiniMax API**: Required by `frontend-dev` skill; paid service; not aligned with priority
- **Vercel Web Interface Guidelines upstream**: Optional live fetch for `web-design-guidelines`; pinned snapshot is the baseline
- **STANDARDS.md**: Required by `review-animations` for precise values/citations; included with the skill
- **Full OpenDesign upstream bundles**: Not installed; catalog entries only; full workflow not tested locally

### Conclusion

The three-skill sequence (`impeccable-design-polish` → `frontend-design` → `review-animations`) provides a complete, locally-executable workflow that:

1. **Starts immediately** — No configuration, no API keys, no daemon setup
2. **Uses existing capabilities** — All skills are already in the open-design skills catalog
3. **Integrates with the codebase** — Skills reference and apply the LightSpeed design system; generated code uses `@lightspeed/design-system` and Tailwind v4 classes already in use
4. **Delivers visible improvement** — The HomePage (or any key page) can be refined in 4-8 hours of total skill invocation + developer integration time
5. **No new paid services** — All three skills operate without paid APIs or credentials
6. **Follows the design system** — The LightSpeed design system is the governing authority; skills respect its tokens, typography scale, spacing, breakpoints, and motion principles

This is the fastest route to value for refining and launching the existing LightSpeed Holdings website.
