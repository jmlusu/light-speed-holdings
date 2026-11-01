# 05 — Migration Plan

**Session 5 of the LightSpeed redesign, last planning session.** Everything after this prompt changes application code, so this plan is for human approval before prompt 06 runs.

---

## 1. Strategy Recommendation per Area

| Area | Recommendation | One-Sentence Justification |
|---|---|---|
| **NavShell / Footer / CTA band** | Incremental restyle | Audit debt: these shell components are referenced across every route; replacing them all at once risks 40+ broken links. Restyling in-place preserves navigation and form integrations while applying the new navy/cyan/red palette. |
| **Core component library (Button, Badge, Chip, ArrowLink, SectionHeading, Card variants)** | Replace-with-new-component | Audit risk: existing components use hardcoded hex colors and old badge spellings (e.g. `#PILOT`, "PILOTED", "FIELDABLE"). A clean replacement eliminates technical debt and ensures canonical status-badge taxonomy from day one. |
| **Home page** | Incremental restyle | Traffic: home is the highest-traffic entry point. Restyling section-by-section (hero, pathway cards, framework, solutions, Pharos teaser, CTA band) lets us validate each section against ref-08-home.png before moving on, reducing regression surface area. |
| **What We Do** | Replace-with-new-component | Structural gap from visual gap audit: the current page has no stat band with Africa map/outline SVG, no LightServiceCards with ArrowLinks, and column layout differs at 390/768/1440. A new component-driven build is cleaner than patching the old layout. |
| **Solutions index + detail** | Replace-with-new-component | The detail template (DomainTiles, featured cards with StatusBadge/PROVEN overlay, TagChips, ArrowLink) does not exist in the current codebase. Building from the component spec ensures all badge spellings and overlay patterns are consistent. |
| **Use Cases index + detail** | Replace-with-new-component + incremental filters | Filters (FilterBar with Status/Sector/Problem Category/Solution Category + search) are a structural gap — the current grid has no working filter state. New FilterBar + UseCaseCard components with real filter logic are required; however, the underlying use-case data schema is preserved. |
| **Company Builder** | Replace-with-new-component | Enriched by ref-04 blueprint infographic; the 6-step path component and glass stat cards do not exist in the current UI. A dedicated build ensures the path Chevron layout wraps gracefully at 390px. |
| **Pharos Insights index + article** | Incremental restyle + new article template | The Knowledge Ecosystem diagram is a structural gap (no inline SVG exists). The article template (category chip, title, meta, body, share row, related articles) can be restyled incrementally per article, but the diagram requires a new SVG component. |
| **HAOMTGV framework page** | Replace-with-new-component | Structural gap: TabBar of 7 tabs (H A O M T G V) does not exist; the funnel diagram is a new inline SVG; the "E" tab letter is a known mockup defect (b → M). A clean build avoids carrying forward the typo and placeholder gibberish. |
| **About / Contact** | Incremental restyle | Form behavior, endpoints, validation and analytics events MUST survive (audit §7). Restyling the form presentation (dark surface, cyan focus ring) while preserving the submission integration is lower risk than replacing the form logic. |
| **Assets & diagrams** | Replace-with-new-component | All framework tree, knowledge ecosystem, funnel, 6-step path, and Africa outline diagrams should be inline SVG built from tokens (currentColor usage). This is a structural upgrade from placeholder rasters, and the one-time build cost pays off in scalability and section-mode recoloring. |
| **Copy & SEO** | Incremental restyle | Content gaps and terminology unifications (prompt 18) are text-only changes. No structural risk; can be done route-by-route after the UI is in place. |
| **Responsive & a11y** | Incremental restyle | Token-level fixes (contrast, focus-visible, tap targets) are applied globally via the theme. Once tokens are live, each route gets audited and fixed — no single point of failure. |
| **QA & visual verification** | Incremental verification | Build + screenshot + axe per route; no new components land in this phase. Risks are isolated to pre-existing regressions. |
| **Cleanup & handoff** | Incremental removal | Dead code deletion is localized per phase; anything uncertain gets a changelog entry instead of silent removal. |

---

## 2. Phase Plan (prompts 06–21)

| # | Phase (Prompt) | Goal | Routes / Files Touched | Components Introduced | Risks | Rollback Note | Size |
|---|---|---|---|---|---|---|---|
| 06 | **Theme & global styles** | Apply design tokens as CSS custom properties / Tailwind theme; add section primitives (.section-dark, .section-light); self-host fonts; base element styles. | All routes (additive-only, no markup changes). | None (tokens only). | Tokens conflict with existing hex values → old UI breaks. | Revert token file to previous commit; all existing classes still work because change is additive. | S |
| 07 | **Layout shell: navbar, footer, CTA band** | Replace nav/footer on ALL routes with new navy shell + CTA band; keep content areas untouched. | All routes — shell swap. | NavShell, Footer, CTABand, LogoLockup. | Missing link hrefs or broken form submission if old footer scripts are removed. | Keep old nav/footer classes available as a fallback; git stash the new shell and re-apply old one. | M |
| 08 | **Core component library + design-system preview** | Implement all spec'd components (Button 5 variants, StatusBadge, CategoryChip, TagChip, ArrowLink, SectionHeading, StatBlock, DomainTile, 5 Card variants + HeroSplit, HeroPhoto). Create /design-system preview route. | /design-system preview route only. | Button (all 5 variants), StatusBadge, CategoryChip, TagChip, ArrowLink, SectionHeading, StatBlock, DomainTile, DarkFeatureCard, LightServiceCard, ArticleCard, PackageCard, UseCaseCard, PathwayCard, HeroSplit, HeroPhoto. | Component props mismatch with existing usage → some pages break. | New components live under new CSS class names; old classes remain until a codemod renames them. | L |
| 09 | **Home** | Rebuild home page matching ref-08-home.png using library components + tokens. | / (home). | PathwayCard, ArticleCard, StatusBadge, CategoryChip, CTABand, HeroPhoto, HeroSplit, SectionHeading. | Hero image lazy-loading CLS; framework diagram SVG responsiveness. | Re-home content from old template; the old home route HTML is preserved as a fallback. | M |
| 10 | **What We Do** | Rebuild /what-we-do matching ref-06 four-pages collage top-left. | /what-we-do. | LightServiceCard, ArrowLink, StatBlock, SectionHeading, HeroPhoto, CTABand. | Stat band Africa map SVG must render correctly at 3 widths; icon SVGs must be inline/cyan. | Swap the entire /what-we-do template with the old one; old content (service descriptions) is preserved in a data attribute. | M |
| 11 | **Solutions index + detail** | Rebuild /solutions matching ref-07-solutions.png + detail template. | /solutions, /solutions/[slug]. | DomainTile, Card (featured with StatusBadge/TagChips/ArrowLink), StatusBadge, CategoryChip, ArrowLink, CTABand. | Status badge spellings must be canonical; detail template must render for every existing solution. | Detail template can be disabled by reverting routes/[slug].tsx to the old detail page. | L |
| 12 | **Use Cases index (working filters) + detail** | Rebuild /use-cases with live filters; URL round-trips. | /use-cases, /use-cases/[slug]. | FilterBar, UseCaseCard, StatusBadge, CategoryChip, ArrowLink, HeroPhoto. | Filter combinations must not produce empty/broken states; URL query params must round-trip. | FilterBar can be hidden; old grid layout is retained under the old route handler. | L |
| 13 | **AI Company Builder** | Rebuild /company-builder per ref-06 bottom-left + ref-04 blueprint. | /company-builder. | LightServiceCard (5), SectionHeading, CTABand, HeroPhoto, HeroSplit. | 6-step path Chevron wrap at 390px; stats must come from config, not hardcoded. | Path component can be statically rendered as a list if Chevron wrap proves too fragile. | M |
| 14 | **Pharos Insights index + article template** | Rebuild /pharos-insights per ref-03-pharos.png + article template. | /pharos-insights, /pharos-insights/[slug]. | DiagramBlock, ArticleCard, CategoryChip, SectionHeading, HeroPhoto. | Knowledge Ecosystem diagram SVG must be crisp at 2x and legible at 390px; no duplicated titles/chips. | Article template can fall back to the old article HTML; diagram SVG can be replaced with a static image. | L |
| 15 | **HAOMTGV framework page** | Rebuild framework page per ref-02-haomtgv-page.png; fix tab letter E→M; real copy per layer. | /framework. | TabBar (7 tabs), SectionHeading, DiagramBlock (funnel SVG), CTABand. | Tabs keyboard accessibility (arrow keys, Home/End); hash deep-links (#governance); "E" → "M" typo. | TabBar can be collapsed to a single-view panel; hash deep-links can be disabled. | M |
| 16 | **About, pathways & contact** | Complete remaining routes: /about with dark/light alternation + tagline; /contact restyled form preserving submission. | /about, /contact. | PathwayCard (if not on home), Form inputs restyled with library, SectionHeading. | Form submission MUST be unchanged; only presentation restyled. | Old contact form handler is preserved; new CSS classes are additive. | S |
| 17 | **Diagrams, imagery & brand assets** | Replace placeholder diagrams with inline SVG (framework tree, knowledge ecosystem, funnel, 6-step path, Africa outline); hero photos with duotone overlay; logo system; favicon/OG images. | All routes — asset replacement only. | Inline SVG components for diagrams; LogoLockup variants; OG image template. | SVG currentColor recoloring may not match all section modes; hero photo format conversion may change weight. | SVG files can be replaced with the original raster placeholders; OG images reverted. | M |
| 18 | **Copy, content migration & SEO** | Walk every route: replace placeholder/gibberish strings with real copy; unify terminology; per-route SEO (title, meta, canonical, OG). | All routes — content-only changes. | None (content + SEO metadata). | Accidentally changing form field labels or CTA text that affects functionality. | Old copy is preserved in git; a changelog tracks what was swapped. | M |
| 19 | **Responsive & accessibility pass** | Verify/fix 390/768/1024/1440; contrast >=4.5:1 on dark surfaces; focus-visible everywhere; skip-link; aria-current; labels on selects/inputs; alt text; aria-live on filter count; prefers-reduced-motion. | All routes. | None (token-level and component-level fixes). | Token changes (e.g. muted token contrast) may ripple to other components. | Token revisions are gated; if a token change breaks something, revert that token and keep the one-off override. | M |
| 20 | **QA & visual verification against references** | Per-route screenshots 1440/768/390; checklist every section against reference; behavioral QA (links, forms, filters, tabs, deep-links, 404, redirects); performance; console/network clean. | All routes. | None (verification-only). | Screenshot diffs may reveal pre-existing issues not caused by this redesign. | Pre-existing failures are listed in 20-qa.md with owner + severity; they do not block closure. | L |
| 21 | **Cleanup, docs & handoff** | Delete dead code (old theme files, unused components/classes/routes); gate /design-system behind env flag; update README/AGENTS.md; finalize progress.md + changelog; full build + test + screenshot smoke; tag release. | Whole repo. | None (cleanup only). | Accidental deletion of files still in use by other routes. | Each deletion is justified in the commit body; uncertain deletions go to 21-changelog.md as a ticket instead. | M |

**Size key:** S = single-file or token change (≤2 hrs), M = multi-route component build (≈4–8 hrs), L = largest phase involving structural changes, new routes, or data config (≈8–16 hrs).

---

## 3. Must-Not-Break List (from audit §7)

The following must survive the redesign unchanged in function:

- **Forms:** Contact form submission integration, validation, analytics events — /contact must submit identically.
- **Auth:** Any authentication state or protected routes — not applicable to public-facing pages but must not break existing auth flows.
- **APIs:** All existing API calls (e.g., fetch endpoints, third-party integrations) must return the same shape and not error due to class/ID changes.
- **SEO:** Per-page `<title>`, `<meta name="description">`, `<link rel="canonical">`, Open Graph tags must remain editable/preservable; no route may lose its SEO metadata.
- **Redirects:** Any existing redirects (e.g., old blog/post URLs) must continue to resolve; no route may return 404 where a redirect was previously in place.

---

## 4. Page Implementation Order Justification

The order follows **traffic volume** and **component dependency chains**:

1. **Home** — highest-traffic entry point; establishes the shell, nav, and hero pattern that other pages inherit.
2. **What We Do** — second-highest traffic; depends on LightServiceCard, ArrowLink, StatBlock (introduced in home phase via shared library).
3. **Solutions** — third; depends on DomainTile, featured Card with StatusBadge/TagChips (components from library phase).
4. **Use Cases** — fourth; depends on FilterBar + UseCaseCard (new components) but reuses existing use-case data schema.
5. **Company Builder** — fifth; enriched by ref-04 infographic; uses LightServiceCard (5 variants) and CTABand.
6. **Pharos Insights** — sixth; article template reuses components but adds the Knowledge Ecosystem diagram.
7. **HAOMTGV framework** — seventh; high-complexity page with TabBar (7 tabs) and funnel diagram; tabs depend on Shell from phase 07.
8. **About / Contact** — eighth; about reuses shell and PathwayCards; contact form must preserve submission (audit §7 constraint).
9–11. **Assets, Copy/SEO, Responsive/a11y** — applied globally after the structural pages are in place, so each route can be verified in context.
12. **QA & visual verification** — final check against all references and the must-not-break list.
13. **Cleanup & handoff** — removes scaffolding once everything is verified.

Dependencies cascade forward: the component library (phase 08) is a prerequisite for every page phase (09–16). The shell (phase 07) is a prerequisite for about/contact and home. The order minimizes circular dependencies and lets each phase validate against a running app with previous pages already rendered.

---

## 5. Verification Approach per Phase

| Phase | Build | Screenshots (3 widths: 1440/768/390) | axe Accessibility | Route Checklist |
|---|---|---|---|---|
| 06 (theme) | `uv run pytest` + `uv run ruff check`; dev server renders all routes visually unchanged (compare against before/after screenshots). | N/A (no page markup changes). | N/A. | Verify every route opens without JS errors; console is clean. |
| 07 (shell) | Build passes; every route renders new shell at 3 widths with no horizontal scroll. | Home + 3 other key routes (what-we-do, solutions, use-cases) captured at 1440/768/390; PASS/FAIL per section. | axe on nav/footer only — no critical/serious issues. | All nav and footer links resolve to real routes; active link state correct per route. |
| 08 (library) | Build passes; /design-system renders all variants at 1440 and 390; no unused-component lint errors. | /design-system page screenshots at 3 widths; every component variant labeled. | axe on /design-system page — critical/serious = 0. | Hover/focus-visible states present on every interactive item. |
| 09–16 (pages) | Build passes per route; after-state screenshot captured per route at 1440/768/390. | One screenshot per route × 3 widths; stored in docs/redesign/screenshots/after/. | axe on each route — critical/serious = 0. | Section-by-section checklist vs reference (order, background mode, components, badges, copy tone); record PASS/FIX per item. |
| 17 (assets) | Build passes; asset weight report compared against phase 05 baseline. | Hero images at 3 widths; diagram SVGs crisp at 2x. |axe minimal — only if new SVGs introduce contrast issues. | Every route has explicit image dimensions; no layout shift from images. |
| 18 (copy/SEO) | Build passes; grep for lorem/gibberish returns 0 matches. | N/A (content-only). | N/A. | Every route has unique `<title>` (≤60 chars), `<meta description>` (≤155 chars), canonical, OG title/description/image, exactly one h1. |
| 19 (a11y) | Build passes; token-level fixes written back into 03-design-tokens.md. | Screenshot set regenerated at 4 widths (add 1024). | axe critical/serious = 0 on all routes. | Keyboard-only walkthrough of home + solutions + use-cases + framework succeeds; tap targets >=44px; contrast ratios OK; skip-link present; aria-current on nav. |
| 20 (QA) | Build passes; performance: build size vs baseline; hero LCP sanity on throttled run; image weights compared. | Before/after screenshot pairs exist for all routes. | axe critical/serious = 0 (should already be 0 from phase 19). | All internal links resolve; forms submit; filters round-trip URL; tabs deep-link (#hash); 404 route is on-brand; redirects from audit still work; console and network clean on every route. |
| 21 (cleanup) | Build + tests green; no references to removed files. | Final smoke screenshot set. | N/A. | progress.md shows 21/21 done; AGENTS.md renders complete; changelog summarises per-phase changes. |

---

## 6. Open Questions for the Human Approver

| Question | Why It Matters | Potential Options |
|---|---|---|
| **Content gaps: "ASPIRE. ACT. ACHIEVE." tagline placement** | The about page tagline is a signature pattern but its exact position (hero vs. below eyebrow) may conflict with existing H1 hierarchy on /about. | (a) Place tagline below the eyebrow + H1; (b) Integrate tagline as the H1 itself; (c) Defer to existing content placement. |
| **IA conflict: navigation link "Start Free" vs. "Start Free CTA"** | The canonical IA from visual gap (prompt 02) proposes new top-level nav: Home / What We Do / Solutions / Sectors / Use Cases / Pharos Insights / About + Contact + Start Free. "Start Free" may compete with the hero CTA. | (a) Keep "Start Free" as a top-level nav item; (b) Move it to hero CTA only; (c) Remove from nav, keep as secondary hero button. |
| **Sectors page existence** | The proposed IA includes a "Sectors" route (between Solutions and Use Cases) but no mockup explicitly defines it; it may need to be a thin index or redirect to Use Cases filters. | (a) Build a Sectors index page with sector badges; (b) Route "Sectors" link to the Use Cases filter pre-set by sector; (c) Remove the link per canonical IA decision. |
| **Footer link destinations** | Current footer may link to pages (e.g., careers, partners) that have no redesign mockup; decision needed: build minimal on-brand pages or remove links. | (a) Build minimal on-brand pages; (b) Remove links and update IA; (c) Keep as placeholders with "Coming Soon" note. |
| **Contact form integration preservation** | The contact form's backend endpoint, validation, and analytics events must be unchanged. Need confirmation that the existing form handler (e.g., Formspree, Netlify Forms, custom endpoint) is documented and will not be touched. | (a) Verify endpoint URL and analytics events with the team; (b) Document the exact integration before restyling; (c) Add a fallback to old form HTML if restyling breaks it. |
| **Hero image licensing / weight budget** | Assets phase (17) must keep total initial hero image weight under the budget in 05-plan.md. Need confirmation on whether existing hero images can be converted to AVIF/WebP or if new licensed images are required. | (a) Use existing images converted to modern formats; (b) Commission new on-brand hero images; (c) Reduce hero image count per route. |
| **Diagram SVG authorship** | Inline SVG diagrams (framework tree, knowledge ecosystem, funnel, 6-step path, Africa outline) must use `currentColor` for section-mode recoloring. Need sign-off that the SVG assets are original work and not derived from third-party copyrighted diagrams. | (a) Team produces SVGs from scratch using the design token system; (b) Use existing brand diagrams with `currentColor` wrapped; (c) Defer diagram work to post-launch sprint. |
| **Badge taxonomy canonical set** | The design tokens define PROVEN (cyan) / PILOT (green) / FIELDABLE (teal) / FUTURE (crimson). Need confirmation that the current codebase uses these exact spellings or if there are legacy variants (e.g., "#PILOT", "PILOTED") that need a global replace strategy. | (a) Global find-and-replace to canonical spellings; (b) Keep legacy spellings as-is and add canonical ones alongside; (c) Freeze badge taxonomy — no new statuses after launch. |

---

**Definition of Done:** Plan covers 100% of routes and 100% of STRUCTURAL gaps from 02; every phase has a rollback note; open questions are explicit.

**Commit:** `docs(redesign): migration plan`
