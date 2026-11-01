# LightSpeed Web Redesign — opencode Prompt Playbook

A sequenced pack of **21 copy-paste prompts** for implementing the LightSpeed Holdings redesign in [opencode](https://opencode.ai), derived from the 8 reference mockups in `design/reference/`.

**How it works in one paragraph:** each prompt is one opencode session with exactly one verifiable outcome. Sessions don't share memory, so the prompts chain together through **artifact documents** written into `docs/redesign/` (audit → gap analysis → tokens → component spec → plan → progress tracker). Every later prompt starts by reading those artifacts, so context never gets lost and no session can wander off-scope. The sequence starts with two **read-only audits** (codebase, then visual gap), because you cannot plan a migration before you know what exists and how far it is from the target.

---

## 0. Before you start (human, ~10 minutes, once)

1. Put the repo in a clean git state on a `redesign` branch.
2. Create `design/reference/` and copy the mockups in with these slug names (prompts refer to these names):

   | Slug | Original file | Defines |
   |---|---|---|
   | `ref-01-venture-studio.png` | LightSpeed_Solutions_Page_1.png | Early home / AI Venture Studio hero + "Our Studio Model" cards |
   | `ref-02-haomtgv-page.png` | LightSpeed_HAOMTGV_Page_1.png | H-A-O-M-T-G-V page (hero funnel + tab interface) |
   | `ref-03-pharos.png` | LightSpeed_Pharos_Page_1.png | Pharos Insights index (knowledge ecosystem + article cards) |
   | `ref-04-blueprint-infographic.png` | Lightspeed AI Company Builder Blueprint.png | Company-builder infographic (stack tower, approval matrix, 6-step path) |
   | `ref-05-haomtgv-infographic.png` | Lightspeed H.A.O.M.T.G.V. Operating System.png | HAOMTGV 7-layer tower infographic |
   | `ref-06-four-pages-collage.png` | LightSpeed Holdings AI Website Collage.png | What We Do, Solutions (old), Company Builder, Use Cases pages |
   | `ref-07-solutions.png` | LightSpeed Solutions_ Proven, Practical, Ready.png | Solutions index (canonical) |
   | `ref-08-home.png` | LightSpeed AI Operating Model Landing Page.png | Home / landing (canonical) |

3. Decide who approves the **human gates** (after Prompt 05, and at the end of each phase).
4. Run prompts **in order, one per session**. Paste the prompt verbatim; if your opencode model supports vision, also attach the reference files the prompt names. Commit happens inside each prompt's last step.

---

## 1. How every prompt is structured (the anatomy)

Every prompt below has the same six blocks. This is the part worth teaching your team — any future prompt they write themselves should use the same skeleton:

| Block | Purpose |
|---|---|
| **CONTEXT** | One paragraph: which session number this is, what already exists, what this session must NOT do. Sets role and scope fence. |
| **INPUTS** | Exact files/artifacts to read first (`docs/redesign/*.md`, reference images, routes). Forces read-before-write and carries memory across sessions. |
| **TASK** | Numbered, concrete steps. One outcome per prompt — never "redesign the site". |
| **RULES** | Hard constraints: don't touch X, no hardcoded hex, keep Y working, read-only, etc. This is where scope creep dies. |
| **DEFINITION OF DONE** | Checkable acceptance criteria (build passes, route renders at 3 widths, table exists, axe clean…). The agent self-checks before ending. |
| **ARTIFACTS & COMMIT** | What to write/update on disk (including `docs/redesign/progress.md`) and the exact commit message. One prompt = one commit. |

**Golden rules for the team**

1. One prompt = one session = one commit. Never bundle two prompts.
2. Artifacts are the memory. If a decision is made in a session, it gets written into `docs/redesign/`, not just chat.
3. Reference citations are mandatory in gap/QA work: every claim names a file + region (`ref-07-solutions.png, featured cards row`).
4. No orphan values: after Prompt 06, hardcoded hex/px in components is a defect.
5. Mockups are the visual source of truth but **contain errors** — Appendix B lists them; prompts fix, never replicate, them.
6. Stop and ask a human at the gates (after Prompt 05, end of each phase), not mid-prompt.

**Blank template** (for prompts the team adds later):

```text
CONTEXT: Session N of the LightSpeed redesign. <what exists already>. This session only <outcome>.
INPUTS: Read docs/redesign/progress.md, <artifacts>, <reference files>. Run the app if needed.
TASK:
1. ...
RULES: Do not modify <fenced areas>. <constraints>.
DEFINITION OF DONE: <checkable criteria>.
ARTIFACTS & COMMIT: Update docs/redesign/progress.md (row N = done, commit SHA). Commit: "<type>(redesign): <what>".
```

---

## 2. The prompts, one by one

### Phase 1 — Understand (read-only)

---

#### PROMPT 01 — Codebase & content audit

```text
CONTEXT: Session 1 of the LightSpeed Holdings web redesign. You are auditing this
application before any visual work begins. The target design lives in design/reference/
but is NOT relevant yet. This session is READ-ONLY for application code: your output is
a factual audit report that every later redesign session will rely on. Accuracy matters
more than speed; verify by running the app wherever static reading is inconclusive.

INPUTS: The whole repository. docs/redesign/ may not exist yet - create it.

TASK:
1. Stack & tooling: framework + versions, language, build tool, package manager, CSS
   approach (Tailwind / CSS Modules / styled-components / plain CSS), routing solution,
   state management, CMS or content source, test setup, deploy target.
2. Route inventory: table of EVERY route/URL - purpose, file/template rendering it,
   data source, one-line note on current visual state.
3. Component inventory: table of every reusable component - path, props, usage count
   (grep), how it is styled.
4. Styling audit: where colors/fonts/spacing are defined; list every distinct hex value
   and font-family in use with file locations; count duplicates and conflicts; note any
   theming mechanism (or its absence).
5. Content inventory per page: headings, body blocks, CTAs, badges, forms, stats;
   flag which copy is hardcoded vs driven by data/CMS.
6. Asset inventory: images, icons, logos, fonts - path, format, weight in KB, used where.
7. Behaviour & integrations that MUST survive the redesign: forms, auth, API calls,
   analytics, third-party scripts, redirects, SEO metadata.
8. Baseline: run build and dev server; record build time, bundle size, console errors,
   and any failing tests.
9. Debt & risk: dead code, unused routes/components, legacy patterns, and anything that
   could break when styles are replaced.

RULES: Do not modify application code or config. Only create files under docs/redesign/.
Prefer tables over prose. No opinions about the new design yet - facts only.

DEFINITION OF DONE: docs/redesign/01-audit.md exists with sections 1-9 as tables; the
build still passes; git status shows only new files under docs/redesign/.

ARTIFACTS & COMMIT: Also create docs/redesign/progress.md containing a tracker table
with rows for prompts 01-21 (columns: #, title, status, commit SHA, notes) and mark row
01 done. Commit: "docs(redesign): codebase and content audit".
```

---

#### PROMPT 02 — Visual gap audit vs the reference mockups

```text
CONTEXT: Session 2 of the LightSpeed redesign, second and last read-only session. You now
compare the RUNNING application against the target mockups in design/reference/ and
produce the per-page gap list that the migration plan (session 5) will be built from.

INPUTS: docs/redesign/01-audit.md, docs/redesign/progress.md, design/reference/*,
the running dev server.

TASK:
1. Write docs/redesign/reference-map.md: map each reference image to the route(s) it
   defines. Start from: ref-08-home.png -> home; ref-06-four-pages-collage.png top-left
   -> /what-we-do; ref-07-solutions.png -> /solutions; ref-06 bottom-right -> /use-cases;
   ref-06 bottom-left -> /company-builder; ref-03-pharos.png -> /pharos-insights;
   ref-02-haomtgv-page.png -> /framework (HAOMTGV); ref-01-venture-studio.png ->
   historical home variant (context only). Adjust to the routes that actually exist.
2. Screenshot every route at 1440px and 390px wide (Playwright or Puppeteer; if none is
   installed, add it as a devDependency; if impossible, state so and describe manually).
3. Per route, compare current vs mapped reference across: layout & section order; color
   & contrast; typography (family, scale, weights, letter-spacing); components (nav,
   buttons, cards, badges, footer); imagery & diagram treatment; content differences.
4. Classify every gap: TOKEN (fixable by theme values), COMPONENT (new/changed
   component), STRUCTURAL (new section or page), CONTENT (copy/data).
5. List conflicts BETWEEN reference mockups (different navbars, footers, badge
   spellings, duplicate titles) and propose ONE canonical decision per conflict.

RULES: Read-only for application code. Every gap entry must cite reference file + region,
e.g. "ref-07-solutions.png, featured solutions cards row". Do not propose implementation
order yet.

DEFINITION OF DONE: docs/redesign/02-visual-gap.md exists with one table per route
(columns: area, current, target, gap class, reference citation) plus a "canonical
decisions" section; screenshots saved under docs/redesign/screenshots/before/.

ARTIFACTS & COMMIT: Update progress.md row 02. Commit: "docs(redesign): visual gap analysis".
```

---

### Phase 2 — Define (documents only, no app code)

---

#### PROMPT 03 — Extract the design token set

```text
CONTEXT: Session 3 of the LightSpeed redesign. The audits are done. You now extract the
complete visual language of the target design into a token document. Sample the reference
images (measure/pick pixels); do not invent values from memory. No application code yet.

INPUTS: docs/redesign/01-audit.md (section 4, current styling), 02-visual-gap.md,
design/reference/* (especially ref-08-home.png, ref-07-solutions.png, ref-06-four-pages-collage.png).

TASK: Produce docs/redesign/03-design-tokens.md containing:
1. Color primitives + semantic aliases: dark backgrounds (page, hero gradient stops,
   card surface), light section background and light card surface, accent cyan (button
   fill, link, icon, border-at-low-alpha), accent crimson/pink, text-on-dark (heading,
   body, muted), text-on-light (heading, body), borders, footer surface.
2. Status & category badge palettes: PROVEN / PILOT / FIELDABLE / FUTURE; IN DEVELOPMENT /
   PROTOTYPE / IN-HOUSE / EXPLORATION; WHITEPAPER / RESEARCH / PERSPECTIVE - each with
   background, text, and dot colors.
3. Typography: family recommendation matching the mockups (geometric/neo-grotesque sans,
   e.g. Poppins/Manrope/Plus Jakarta Sans - pick one and justify), scale from 12 to 56px,
   weights, line-heights, and the uppercase eyebrow style (size, tracking, color).
4. Spacing scale, container widths, grid gaps; radii (cards vs pill buttons = 999px);
   border styles (1px, cyan at low alpha on dark; hairline gray on light).
5. Elevation & glow: soft shadows on light cards, cyan glow treatment on hero diagrams.
6. Motion defaults: durations 150-250ms, easing, hover/press behavior, reduced-motion rule.
7. Breakpoints: 390 / 768 / 1024 / 1440.
8. Do / Don't list (e.g. don't place crimson text on crimson fill; don't mix badge palettes).

RULES: Every value must cite the reference file + region it was sampled from. Include BOTH
dark-section and light-section tokens - the design uses both. No code changes.

DEFINITION OF DONE: A developer could rebuild any mockup screen using only this document;
no value is unsourced; token names are semantic (surface-card-dark), not literal (blue3).

ARTIFACTS & COMMIT: Update progress.md row 03. Commit: "docs(redesign): design tokens".
```

---

#### PROMPT 04 — Component & page specification

```text
CONTEXT: Session 4 of the LightSpeed redesign. Tokens exist; now specify the target
component library and per-page section blueprints so implementation sessions never
improvise structure. Documents only - no application code.

INPUTS: docs/redesign/02-visual-gap.md, 03-design-tokens.md, design/reference/*,
docs/redesign/reference-map.md.

TASK: Write docs/redesign/04-component-spec.md with:
1. Component sheets (purpose, variants, props, states, spacing rules, which reference
   shows it) for at least: NavShell, Footer, CTABand, LogoLockup, Button (cyan pill,
   crimson pill, outline-on-dark, outline-on-light, ghost-with-play-icon), StatusBadge,
   CategoryChip, TagChip, ArrowLink, SectionHeading (eyebrow + short rule + title),
   Card variants: DarkFeatureCard, LightServiceCard, ArticleCard, PackageCard,
   UseCaseCard, PathwayCard, DomainTile, StatBlock, HeroSplit (copy left / art right),
   HeroPhoto (photo + dark overlay + handwritten annotation), TabBar (7 letters),
   FilterBar (selects + search), DiagramBlock (framework tree / knowledge ecosystem /
   layer tower / 6-step path).
2. States for interactive items: hover, focus-visible, active, disabled, current-page.
3. Per-route section blueprint: ordered list of sections per route with the components
   each section uses and its background mode (dark/light), derived from the reference map.
4. Responsive behavior per component (stacking order, nav collapse, diagram fallbacks).

RULES: Components must be expressible using only tokens from 03-design-tokens.md; if a
token is missing, add it to the token doc in the same session and say so. No code.

DEFINITION OF DONE: Every visible element in every reference image is covered by exactly
one component sheet; every route in reference-map.md has a section blueprint.

ARTIFACTS & COMMIT: Update progress.md row 04. Commit: "docs(redesign): component and page spec".
```

---

#### PROMPT 05 — Phased migration plan  [HUMAN GATE]

```text
CONTEXT: Session 5 of the LightSpeed redesign, last planning session. Everything after
this prompt changes application code, so you produce the plan a human approves first.

INPUTS: docs/redesign/01-audit.md, 02-visual-gap.md, 03-design-tokens.md,
04-component-spec.md, reference-map.md.

TASK: Write docs/redesign/05-plan.md containing:
1. Strategy recommendation per area: incremental restyle vs replace-with-new-component,
   with one-sentence justification (use audit debt/risk data).
2. Phase plan mirroring playbook prompts 06-21 (foundation shell, component library,
   pages in order home -> what-we-do -> solutions -> use-cases -> company-builder ->
   pharos -> framework -> about/contact, assets, content, a11y, QA, cleanup), each with:
   goal, routes/files touched, components introduced, risks, rollback note, size S/M/L.
3. Must-not-break list from audit section 7 (forms, auth, APIs, SEO, redirects).
4. Page implementation order justification (traffic, dependencies on components).
5. Verification approach per phase (build, screenshots at 3 widths, axe, route checklist).
6. Open questions for the human approver (content gaps, IA conflicts from gap analysis).

RULES: Do not modify application code. Do not start implementation. End the session
immediately after committing - a human must approve before prompt 06 runs.

DEFINITION OF DONE: Plan covers 100% of routes and 100% of STRUCTURAL gaps from 02;
every phase has a rollback note; open questions are explicit.

ARTIFACTS & COMMIT: Update progress.md row 05 (status: awaiting approval).
Commit: "docs(redesign): migration plan".
```

---

### Phase 3 — Build the foundation

---

#### PROMPT 06 — Theme & global styles

```text
CONTEXT: Session 6, first code session of the LightSpeed redesign. The plan in
docs/redesign/05-plan.md is approved. You implement the token layer only - no markup
changes, no component work.

INPUTS: docs/redesign/03-design-tokens.md, 05-plan.md, 01-audit.md section 4 (current
styling mechanism), the repo.

TASK:
1. Implement every token from 03 in the stack's native mechanism (CSS custom properties,
   Tailwind theme, or theme file) with the semantic names from the doc.
2. Self-host the chosen font family(s) with font-display: swap and preload for the
   heading weight; remove unused old font imports only if nothing references them.
3. Base element styles: body background/text per section mode, heading scale, link
   styles, ::selection, global focus-visible ring (cyan, 2px, offset 2).
4. Section primitives: .section-dark and .section-light (background, text colors,
   vertical rhythm) and the shared container widths from the token doc.
5. Keep every existing class/style working: the old UI must render exactly as before
   (additive change only) so pages can migrate one at a time.

RULES: No hardcoded hex outside the token file. No page/component markup edits. If the
stack has no theming mechanism, introduce the smallest one and document it in
docs/redesign/06-theme-notes.md.

DEFINITION OF DONE: Build passes; dev server renders all existing routes visually
unchanged (compare against docs/redesign/screenshots/before/); tokens are importable
from one file; git diff touches only theme/base files.

ARTIFACTS & COMMIT: Update progress.md row 06. Commit: "feat(theme): design tokens and section primitives".
```

---

#### PROMPT 07 — Layout shell: navbar, footer, CTA band

```text
CONTEXT: Session 7 of the LightSpeed redesign. Tokens are live. You replace the
application shell (nav + footer) on ALL routes and add the shared CTA band, matching
ref-08-home.png and ref-07-solutions.png.

INPUTS: docs/redesign/04-component-spec.md (NavShell, Footer, CTABand, LogoLockup),
03-design-tokens.md, design/reference/ref-08-home.png (header + footer), ref-07-solutions.png
(header + CTA band), the repo.

TASK:
1. LogoLockup as inline SVG (mark + "LightSpeed / Holdings Limited" wordmark) per refs.
2. NavShell: dark navy bar; links per the canonical IA decision in 02-visual-gap.md;
   active link = cyan text + 2px cyan underline; right side search icon (if it exists
   today), outline "Contact" pill and cyan "Start Free" pill; sticky with subtle
   background blur; mobile = hamburger opening a full-height drawer with the same links.
3. Footer: dark navy, logo lockup, link columns, legal row with current year, social
   icons as inline SVG (LinkedIn, X, YouTube) per ref-08-home.png footer.
4. CTABand: blue gradient band with logo, heading with cyan final word, sub line, and
   crimson pill button with arrow - reusable component, not page markup.
5. Apply the shell to every route, replacing old nav/footer; keep old content areas untouched.

RULES: Components consume tokens only. Keyboard: tab order logical, drawer closes on
Escape and on route change. No route/content changes beyond shell swap.

DEFINITION OF DONE: Every route renders the new shell at 1440/768/390 with no horizontal
scroll; active states correct per route; build passes; axe reports no critical issues
on nav/footer.

ARTIFACTS & COMMIT: Update progress.md row 07. Commit: "feat(shell): navbar, footer, CTA band".
```

---

#### PROMPT 08 — Core component library + design-system preview

```text
CONTEXT: Session 8 of the LightSpeed redesign. Shell is live. You build the shared
component library from the spec and a private preview route to validate it.

INPUTS: docs/redesign/04-component-spec.md, 03-design-tokens.md, the repo.

TASK: Implement, exactly per spec: Button (all 5 variants + states), StatusBadge,
CategoryChip, TagChip, ArrowLink, SectionHeading, StatBlock, DomainTile, and Card
variants DarkFeatureCard, LightServiceCard, ArticleCard, PackageCard, UseCaseCard,
PathwayCard; plus HeroSplit and HeroPhoto layout primitives.
Then create route /design-system rendering every component and variant on both dark and
light section backgrounds, labelled, for visual review.

RULES: Tokens only - zero hardcoded colors/spacing in components. Components take
children/slots where the spec says so; no page-specific logic inside them. Existing
pages must not change appearance.

DEFINITION OF DONE: /design-system renders all variants at 1440 and 390; every component
has hover/focus-visible states; build passes; no unused-component lint errors.

ARTIFACTS & COMMIT: Update progress.md row 08. Commit: "feat(ui): core component library".
```

---

### Phase 4 — Pages (one prompt per route)

---

#### PROMPT 09 — Home

```text
CONTEXT: Session 9 of the LightSpeed redesign. Library exists; rebuild the home page to
match ref-08-home.png using only library components and tokens.

INPUTS: docs/redesign/04-component-spec.md (home blueprint), reference-map.md,
design/reference/ref-08-home.png, current home route code, existing content (audit 5).

TASK: Sections in order: (1) dark hero - eyebrow "AI-NATIVE OPERATING MODEL", three-line
headline white / cyan / white ("Human Direction. / Intelligent Execution. / Measurable
Value."), body copy, crimson pill CTA + outline play CTA, right side logo lockup over
light-trails road image with dark overlay; (2) "How would you like to engage" - 4
PathwayCards (Business Leaders, Partners, Researchers, Policy Makers) + view-all link;
(3) framework section - H-A-O-M-T-G-V node diagram (H top, A O M T row, G, V) as inline
SVG/HTML with the side note; (4) solutions grid - 6 cards with status chips (IN
DEVELOPMENT / PILOT / PROTOTYPE / IN-HOUSE / EXPLORATION); (5) Pharos teaser - 3
ArticleCards with CategoryChips; (6) CTABand.

RULES: Reuse existing real copy from the current site where the mockup shows placeholders;
links must route to real routes (no dead hrefs). Diagram must be responsive (stack or
scale at 390px). Tokens + library components only.

DEFINITION OF DONE: Section order and background modes match the reference at 1440/768/390;
no console errors; Lighthouse-style sanity: hero image lazy-safe, CLS ~0; build passes.

ARTIFACTS & COMMIT: Screenshot after-state to docs/redesign/screenshots/after/home-*.png.
Update progress.md row 09. Commit: "feat(pages): home redesign".
```

---

#### PROMPT 10 — What We Do

```text
CONTEXT: Session 10 of the LightSpeed redesign. Rebuild /what-we-do to match the
top-left quadrant of ref-06-four-pages-collage.png.

INPUTS: 04-component-spec.md, design/reference/ref-06-four-pages-collage.png (top-left
quadrant), current route content.

TASK: Sections: (1) HeroPhoto - landscape photo with dark-blue overlay, eyebrow "WHAT WE
DO", headline "AI Solutions for Real-World Impact." (second line cyan), body, two CTAs,
handwritten-style annotation top-right ("Local problems. Real solutions."); (2) five
LightServiceCards (Agentic Automation, AI Integrations, Governance & Compliance, Data &
Analytics, AI Company Builder) with line icons and ArrowLinks; (3) dark stat band -
outlined Africa map SVG + "Built for Africa. Designed for Scale." + StatBlocks
(5 Sectors / 20 Departments / 90 AI Agents).

RULES: Icons as inline SVG line style (cyan). Real copy from current site; mockup copy is
fallback only. Tokens/components only.

DEFINITION OF DONE: Matches reference layout at 1440/768/390 (cards 5->2->1 columns);
stat band numbers render as data, not images; build passes.

ARTIFACTS & COMMIT: Screenshots after/what-we-do-*.png; progress.md row 10.
Commit: "feat(pages): what-we-do redesign".
```

---

#### PROMPT 11 — Solutions index + detail template

```text
CONTEXT: Session 12-of-run session 11 of the LightSpeed redesign. Rebuild /solutions to
match ref-07-solutions.png and create the solution detail template.

INPUTS: 04-component-spec.md, design/reference/ref-07-solutions.png, current solutions
routes + data.

TASK: Index sections: (1) HeroPhoto with eyebrow "SOLUTIONS", headline "Turn Real Problems
into Working Solutions." (last two words cyan), body, cyan pill + ghost play CTA,
handwritten annotation ("Local context. Real solutions. Lasting impact."), right-side
glass panel with 3 icon rows (Governed by design / AI agents with human oversight /
Built for Africa and beyond); (2) light section "Explore Our Capabilities" - 7 DomainTiles
with the first in active state (cyan underline); (3) dark section "Proven. Practical.
Ready." - 5 featured cards (image top, StatusBadge overlay, icon+title, body, TagChips,
ArrowLink) with badges PROVEN/PROVEN/PILOT/FIELDABLE/FUTURE; (4) CTABand "Ready to Build
Your Solution?". Detail template: hero with badge + title + summary, body sections,
related solutions grid.

RULES: Status badge spellings canonical only (Appendix B). Cards link to real detail
routes. Tokens/components only.

DEFINITION OF DONE: Index matches reference at 3 widths; detail template renders for every
existing solution entry; no dead links; build passes.

ARTIFACTS & COMMIT: Screenshots after/solutions-*.png; progress.md row 11.
Commit: "feat(pages): solutions index and detail".
```

---

#### PROMPT 12 — Use Cases index (working filters) + detail template

```text
CONTEXT: Session 12 of the LightSpeed redesign. Rebuild /use-cases per the bottom-right
quadrant of ref-06-four-pages-collage.png. Filters must actually work, not decorate.

INPUTS: 04-component-spec.md (FilterBar, UseCaseCard), design/reference/ref-06-four-pages-collage.png
(bottom-right), current use-case data/routes.

TASK: (1) HeroPhoto - headline "What Can LightSpeed Actually Do?" (second line cyan),
body, two CTAs, right-side vertical status legend pills (PROVEN / PILOT / FIELDABLE /
FUTURE with colored dots); (2) light FilterBar - selects Status / Sector / Problem
Category / Solution Category + search input; filtering updates the grid AND the URL query
string so views are shareable; (3) "Featured Use Cases" card grid - image, StatusBadge,
title, body, TagChips, ArrowLink; (4) detail template with evidence section ("no
fabricated client evidence" rule: only statuses/claims present in data).

RULES: No fake results - empty filter combinations render a proper empty state. Keep
existing use-case data schema; extend only if the plan allows.

DEFINITION OF DONE: Each filter demonstrably narrows the grid; URL round-trips (paste a
filtered URL, same view renders); 390px stacks filters vertically; build passes.

ARTIFACTS & COMMIT: Screenshots after/use-cases-*.png; progress.md row 12.
Commit: "feat(pages): use cases with live filters".
```

---

#### PROMPT 13 — AI Company Builder

```text
CONTEXT: Session 13 of the LightSpeed redesign. Rebuild /company-builder per the
bottom-left quadrant of ref-06-four-pages-collage.png, enriched by the infographic
language of ref-04-blueprint-infographic.png.

INPUTS: 04-component-spec.md, design/reference/ref-06-four-pages-collage.png (bottom-left),
ref-04-blueprint-infographic.png (6-step path), current route content.

TASK: (1) Dark hero - eyebrow "AI COMPANY BUILDER", headline "Your AI-Native Organization.
Built." (last word cyan), body, cyan pill + outline CTA, right side three glass stat
cards (90 Agents / 20 Departments / 5 Tier Governance) over a control-room image;
(2) light "What's Included" - 5 LightServiceCards (Agent Registry, Orchestration,
Governance, Tools & Integrations, Training & Support); (3) dark band "The 6-Step Path" -
chevron steps Opportunity / Design / Build / Deploy / Govern / Measure with icons and
one-line descriptions per ref-04; (4) dark CTA band "Ready to Build?" with rocket icon
and cyan pill.

RULES: Stats must come from data/config, not hardcoded in markup, so they stay editable.
Tokens/components only.

DEFINITION OF DONE: Matches reference at 3 widths; 6-step path wraps gracefully at 390px
(2 columns or horizontal scroll with snap); build passes.

ARTIFACTS & COMMIT: Screenshots after/company-builder-*.png; progress.md row 13.
Commit: "feat(pages): company builder redesign".
```

---

#### PROMPT 14 — Pharos Insights index + article template

```text
CONTEXT: Session 14 of the LightSpeed redesign. Rebuild /pharos-insights per
ref-03-pharos.png and create the article template.

INPUTS: 04-component-spec.md (DiagramBlock, ArticleCard), design/reference/ref-03-pharos.png,
current insights content.

TASK: (1) Dark hero - headline "Pharos Insights: Navigating the AI Frontier.", body, cyan
pill CTA, right side Knowledge Ecosystem diagram rebuilt as inline SVG: central crystal
node with orbit rings and 6 UNIQUE labels (Agentic Governance, Policy & Regulation,
Workflow Collapsing, Market Dynamics, Sovereign AI, Venture Metrics) - the mockup repeats
"Venture Metrics"; fix it; (2) light article grid - ArticleCards with CategoryChip
(WHITEPAPER / RESEARCH / PERSPECTIVE), UNIQUE titles (mockup repeats one title three
times - use real titles from current content), excerpt, "Read Article" ArrowLink;
(3) article template: category chip, title, meta, body prose styles, share row, related
articles.

RULES: Prose styles for article body must be added to base styles as tokens-driven
typography (measure ~68ch). No duplicated titles/chips.

DEFINITION OF DONE: Diagram is crisp at 2x and legible at 390px (labels reflow or list
fallback); article template renders for every existing article; build passes.

ARTIFACTS & COMMIT: Screenshots after/pharos-*.png; progress.md row 14.
Commit: "feat(pages): pharos insights and article template".
```

---

#### PROMPT 15 — H-A-O-M-T-G-V framework page

```text
CONTEXT: Session 15 of the LightSpeed redesign. Rebuild the framework page per
ref-02-haomtgv-page.png. The mockup contains a typo and placeholder gibberish - fix both.

INPUTS: 04-component-spec.md (TabBar, HeroSplit), design/reference/ref-02-haomtgv-page.png,
ref-05-haomtgv-infographic.png (layer definitions), docs/redesign/02-visual-gap.md
canonical decisions.

TASK: (1) Dark hero - headline "H-A-O-M-T-G-V: The Agentic Governance Constitution.",
body, cyan pill CTA labelled with the agent-personas stat, right side funnel diagram
(inline SVG) with 4 numbered stage labels (Opportunity ID, Venture Concept, AI
Architecture, Scale & Govern) and caption "The Venture Build Process"; (2) light section
with TabBar of SEVEN tabs reading H A O M T G V (the mockup's "E" is wrong); below it a
dark elaboration panel showing, per tab: letter title (e.g. "H - Human Purpose &
Authority"), the governing question, and 2-4 sentences of REAL copy per layer using
ref-05 definitions (Human, Agents, Orchestration, Memory, Tools, Governance, Value);
(3) centered cyan pill CTA "Download the H-A-O-M-T-G-V Whitepaper" linking to the real
asset or the Pharos article if none exists.

RULES: Tabs keyboard accessible (arrow keys, Home/End), URL hash per tab (#governance),
panel content server-rendered for the default tab (no empty first paint). NEVER copy the
mockup's placeholder text.

DEFINITION OF DONE: All 7 tabs render unique real copy; keyboard flow verified; hash
deep-links work; 390px tabs scroll horizontally with snap; build passes.

ARTIFACTS & COMMIT: Screenshots after/framework-*.png; progress.md row 15.
Commit: "feat(pages): HAOMTGV framework page".
```

---

#### PROMPT 16 — About, pathways & contact

```text
CONTEXT: Session 16 of the LightSpeed redesign. Complete the remaining routes so the
canonical navigation from prompt 07 has no stubs.

INPUTS: 02-visual-gap.md canonical IA, 04-component-spec.md, ref-08-home.png (pathways
section), current about/contact code and form integrations (audit section 7).

TASK: (1) /about - story sections using dark/light alternation, "ASPIRE. ACT. ACHIEVE."
tagline treatment, leadership/principles blocks from existing content, PathwayCards
section if not already on home; (2) /contact - restyle existing form with library inputs
(dark surface, cyan focus ring), preserve the current submission integration EXACTLY,
add office/email blocks; (3) any remaining nav targets (careers, sectors) - either build
a minimal on-brand page or remove the link per the canonical IA decision; document the
choice in progress.md notes.

RULES: Form behavior, endpoints, validation and analytics events must be unchanged; only
presentation changes. No new third-party dependencies.

DEFINITION OF DONE: Every nav and footer link resolves to a real route; contact form
submits successfully in dev; 3 widths verified; build passes.

ARTIFACTS & COMMIT: Screenshots after/about-*.png, after/contact-*.png; progress.md row 16.
Commit: "feat(pages): about and contact redesign".
```

---

### Phase 5 — Assets & content

---

#### PROMPT 17 — Diagrams, imagery & brand assets

```text
CONTEXT: Session 17 of the LightSpeed redesign. Pages are rebuilt; now make every visual
asset production-grade and on-brand.

INPUTS: 03-design-tokens.md, all design/reference/*, current asset inventory (audit 6),
the routes.

TASK:
1. Replace any raster/placeholder diagrams with inline SVG built from tokens: framework
   tree, knowledge ecosystem, funnel, 6-step path, Africa outline; ensure currentColor
   usage so section mode recolors them.
2. Photography treatment: consistent dark-blue duotone/gradient overlay component for
   all hero photos; crop/focal rules documented; convert hero images to responsive
   formats (avif/webp + fallback, srcset, width/height attributes).
3. Logo system: inline SVG lockups (horizontal, stacked, mark-only), favicon set, and OG
   image template per route type.
4. Audit bundle impact: report before/after asset weight in progress.md notes.

RULES: No AI-regenerated approximations of the logo - trace the existing mark. Keep total
initial hero weight under the budget in 05-plan.md. Do not touch page structure.

DEFINITION OF DONE: Zero layout shift from images (explicit dimensions); all diagrams
crisp at 2x; every route has OG image + correct alt text; build passes.

ARTIFACTS & COMMIT: Update progress.md row 17. Commit: "feat(assets): diagrams, imagery, brand set".
```

---

#### PROMPT 18 — Copy, content migration & SEO

```text
CONTEXT: Session 18 of the LightSpeed redesign. Final content pass across all routes.
The mockups contain typos and gibberish (Appendix B of the playbook / list below); the
live site's real copy wins wherever the mockup is placeholder.

INPUTS: All routes, docs/redesign/01-audit.md section 5 (content inventory),
design/reference/* for tone, the list: tab letter "E"->"M"; "Governonce"->"Governance";
"© 29"-> current year; duplicate Pharos card titles -> unique; "FIELDABLE/PILOT" badge
spelling canonical set; gibberish strings in ref-01/ref-02 cards and labels -> rewritten.

TASK:
1. Walk every route; replace placeholder/lorem/gibberish strings with real, edited copy
   in the brand voice (confident, plain, governance-forward; short sentences).
2. Unify terminology: "AI agents", "human oversight", "5-tier approval", "append-only
   audit trail", statuses PROVEN/PILOT/FIELDABLE/FUTURE everywhere.
3. Per-route SEO: unique title (<=60 chars), meta description (<=155 chars), canonical,
   OG title/description/image, heading hierarchy exactly one h1 per route.
4. Buttons/links: consistent CTA vocabulary (Explore / Talk to an Expert / Start Free /
   Read Article / Learn More) and sentence-case labels.

RULES: Do not invent clients, metrics, or case-study outcomes ("no fabricated client
evidence"). Stats limited to the known set (90 agents, 20 departments, 5 sectors, 5-tier).

DEFINITION OF DONE: grep finds no lorem/gibberish strings; every route has unique meta;
h1 audit clean; a human-readable copy changelog appended to progress.md notes.

ARTIFACTS & COMMIT: Update progress.md row 18. Commit: "content(redesign): copy migration and SEO".
```

---

### Phase 6 — Harden & hand off

---

#### PROMPT 19 — Responsive & accessibility pass

```text
CONTEXT: Session 19 of the LightSpeed redesign. Full-site a11y and responsive hardening;
fix, don't redesign.

INPUTS: All routes, 03-design-tokens.md (breakpoints, focus styles), audit section 8.

TASK:
1. Verify and fix 390 / 768 / 1024 / 1440: no horizontal scroll, no clipped badges,
   diagrams have mobile fallbacks, tables/grids reflow, tap targets >=44px.
2. Accessibility: contrast ratios (body text on dark surfaces >=4.5:1 - adjust muted
   tokens if needed), focus-visible everywhere including tabs/filters/drawer, skip-link,
   aria-current on nav, roles+arrow-key support on TabBar, labels on all selects/inputs,
   alt text audit, aria-live on use-case filter result count, prefers-reduced-motion
   disables glow/animation.
3. Run automated axe (or equivalent) on every route; fix all critical/serious issues.

RULES: Token-level fixes preferred over one-off overrides; any token change must be
written back into 03-design-tokens.md in the same session.

DEFINITION OF DONE: axe critical/serious = 0 on all routes; keyboard-only walkthrough of
home + solutions + use-cases + framework succeeds; 4-width screenshot set regenerated.

ARTIFACTS & COMMIT: docs/redesign/19-a11y-report.md; progress.md row 19.
Commit: "fix(a11y): responsive and accessibility hardening".
```

---

#### PROMPT 20 — QA & visual verification against references

```text
CONTEXT: Session 20 of the LightSpeed redesign. Systematic verification of the finished
build against the mockups and the audit's must-not-break list.

INPUTS: docs/redesign/02-visual-gap.md, 05-plan.md must-not-break list, reference-map.md,
screenshots/before and after, the running app.

TASK:
1. Per route: screenshot 1440/768/390; checklist every section against its reference
   (order, background mode, components, badges, copy tone); record PASS/FIX per item.
2. Behavioural QA: all internal links resolve; forms submit; filters round-trip; tabs
   deep-link; 404 route is on-brand; redirects from audit still work; console and
   network clean on every route.
3. Performance: build size vs baseline; hero LCP sanity on throttled run; image weights;
   fix regressions you caused, list pre-existing ones.
4. Fix all FAIL items you can within this session; anything requiring a product decision
   goes to docs/redesign/20-qa.md with owner + severity.

RULES: Fixes must stay token/component-based; no one-off hacks. Do not close the session
with a failing build.

DEFINITION OF DONE: 20-qa.md shows every route checklist complete; zero open critical
items; before/after screenshot pairs exist for all routes.

ARTIFACTS & COMMIT: progress.md row 20. Commit: "test(redesign): QA and visual verification".
```

---

#### PROMPT 21 — Cleanup, docs & handoff

```text
CONTEXT: Session 21, final session of the LightSpeed redesign. Remove the scaffolding of
the old design and leave the repo better documented than you found it.

INPUTS: Whole repo, docs/redesign/*, audit sections 4 and 9.

TASK:
1. Delete dead code: old theme files, unused components/classes/routes from the pre-
   redesign UI (verify with grep + build before deleting).
2. Gate /design-system behind an env flag (or delete it per team preference); document
   the choice.
3. Update README and AGENTS.md (or create AGENTS.md): how to run, where tokens live,
   the rule "components consume tokens only", how to add a new component (spec first),
   badge/status taxonomy, content voice rules from prompt 18.
4. Finalize docs/redesign/progress.md (all rows done with SHAs) and write
   docs/redesign/21-changelog.md summarizing what changed per phase.
5. Full build + test + screenshot smoke run; tag the release if the repo uses tags.

RULES: Deletions must be justified in the commit body; anything uncertain gets a comment
ticket in 21-changelog.md instead of silent removal.

DEFINITION OF DONE: Build and tests green; no references to removed files; AGENTS.md
renders complete; progress.md shows 21/21 done.

ARTIFACTS & COMMIT: Commit: "chore(redesign): cleanup, docs and handoff".
```

---

## Appendix A — Design language cheat-sheet (seed for Prompt 03; verify by sampling)

**Surfaces & color (approximate hex — Prompt 03 must sample and finalize)**

| Token | Approx | Used for |
|---|---|---|
| `bg-page-dark` | `#060D1A` → `#0A1626` gradient | hero & dark sections |
| `surface-card-dark` | `#0E1B2E` | dark cards, panels, nav |
| `bg-section-light` | `#F4F7FA` | light sections |
| `surface-card-light` | `#FFFFFF`, border `#DCE6F0` | light cards |
| `accent-cyan` | `#2BD3E9` (deep `#0FA8C4`) | primary pills, links, icons, active states |
| `accent-crimson` | `#E62B54` (bright `#F43F6B`) | secondary CTA, governance layer, emphasis |
| `text-on-dark` | heading `#EAF3FC`, body `#B9CBDD`, muted `#8FA6BB` | dark sections |
| `text-on-light` | heading `#0B2540`, body `#33475C` | light sections |
| `border-on-dark` | cyan @ 20-35% alpha, 1px | dark card borders, glass panels |

**Type:** geometric/neo-grotesque sans (Poppins / Manrope / Plus Jakarta Sans family). H1 44-56px semibold, tight leading; section titles 28-36px; eyebrow 11-12px uppercase, tracking ~0.12em, cyan or crimson, often with a 24px rule after it; body 15-16px/1.6.

**Signature patterns:** split hero (copy left, art/photo right); dark↔light section alternation; pill buttons only (no sharp buttons); uppercase status badges with dot; card grids of 3-5; glass panel over photo (1px cyan border + blur); handwritten script annotation on photos; letter-spaced tagline "ASPIRE. ACT. ACHIEVE."; cyan glow on isometric/3D diagram art; chevron step rows.

**Badge taxonomy (canonical):** delivery status `PROVEN` (cyan) / `PILOT` (green) / `FIELDABLE` (teal) / `FUTURE` (crimson); maturity `IN DEVELOPMENT` / `PROTOTYPE` / `IN-HOUSE` / `EXPLORATION`; content type `WHITEPAPER` / `RESEARCH` / `PERSPECTIVE`.

## Appendix B — Known mockup defects (fix, never replicate)

1. `ref-02-haomtgv-page.png`: tab bar reads **H A O E T G V** — must be **H A O M T G V**.
2. Same file: elaboration panel is placeholder gibberish ("[Elaboration text]… f.taot eialliboration…") — write real per-layer copy.
3. `ref-01/02/03` footers: "© 29 LightSpeed" — use the current year.
4. `ref-01-venture-studio.png`: card body copy is gibberish ("corprorfooft ats analyster analligent", "a mond ootitle") — rewrite.
5. `ref-01` diagram labels: "Governonce Governance Rules", "Celorlops Emngnt & Ess…" — rewrite to Governance Rules / Enterprise Data Layer etc.
6. `ref-03-pharos.png`: three article cards share one title (one mangled: "Aliwing") — unique real titles; "Venture Metrics" label duplicated in the ecosystem diagram.
7. Nav/IA differs between mockup generations (old: AI Venture Studio / Solutions / Pharos Insights / About / Log In; new: Home / What We Do / Solutions / Sectors / Use Cases / Pharos Insights / About + Contact + Start Free) — Prompt 02 proposes, Prompt 05 decides the canonical IA.
8. Badge spellings vary ("#PILOT", "PILOTED", "FIELDABLE") — use the canonical set in Appendix A.
9. Old-mockup gray footer (`#3A4148`) is superseded by the navy footer in `ref-08-home.png`.

## Appendix C — Progress tracker (created by Prompt 01, updated by every prompt)

| # | Title | Status | Commit SHA | Notes |
|---|---|---|---|---|
| 01 | Codebase & content audit | done | | |
| 02 | Visual gap audit | | | |
| 03 | Design tokens | | | |
| 04 | Component & page spec | | | |
| 05 | Migration plan (gate) | | | |
| 06 | Theme & global styles | | | |
| 07 | Layout shell | | | |
| 08 | Component library | | | |
| 09 | Home | | | |
| 10 | What We Do | | | |
| 11 | Solutions | | | |
| 12 | Use Cases | | | |
| 13 | Company Builder | | | |
| 14 | Pharos Insights | | | |
| 15 | HAOMTGV framework | | | |
| 16 | About / contact | | | |
| 17 | Assets & diagrams | | | |
| 18 | Copy & SEO | | | |
| 19 | Responsive & a11y | | | |
| 20 | QA & visual verify | | | |
| 21 | Cleanup & handoff | | | |
