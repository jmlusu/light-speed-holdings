# Tasks: About Page — LightSpeed Holdings Limited

Tasks are ordered by dependency, each completable in a single focused session. No task should require changing more than ~5 files.

---

## Task 1: Validate brand tokens & extend AboutSection scaffolding

**Description**: Verify `brand-tokens.json` covers all needed colors/typography for the About Page; extend `AboutSection.tsx` with new section scaffolding (hero, thesis, grids placeholders).

**Acceptance**:
- `brand-tokens.json` has all required tokens (navy, red, cyan, grey variants, type sizes)
- `AboutSection.tsx` compiles without errors
- New section placeholders added without breaking existing functionality

**Verify**:
- `uv run ruff check src/`
- `uv run mypy src/`
- `npm test -- --run`

**Files to touch** (max 5):
- `src/components/AboutSection.tsx` — add section dividers/comments for new sections
- `brand/tokens/brand-tokens.json` — verify/extend token coverage
- `src/data/leadership.ts` — verify Jack Mlusu entry is complete

---

## Task 2: Create HeroBanner component — "Institutional Charter // Sovereign Mission"

**Description**: Build `src/components/HeroBanner.tsx` featuring the "Institutional Charter // Sovereign Mission" header with the emerald dot, LightSpeed branding, and the Africa quotation. Uses brand tokens for theming.

**Acceptance**:
- Hero banner renders with correct header text and quotation
- Light and dark theme variants both work
- Brand colors applied via token classes (`text-ls-navy`, `bg-ls-red`, etc.)
- No layout shift CLS issues

**Verify**:
- `npm test -- --run --grep HeroBanner`
- Visual inspection: header text, quotation, branding elements
- `uv run ruff check src/`

**Files to touch** (max 5):
- `src/components/HeroBanner.tsx` — new file
- `src/components/AboutSection.tsx` — import and integrate HeroBanner
- `brand/tokens/brand-tokens.json` — ensure token classes reference correctly

---

## Task 3: Create ThesisBanner component — "ASPIRE. ACT. ACHIEVE."

**Description**: Build `src/components/ThesisBanner.tsx` featuring the "ASPIRE. ACT. ACHIEVE." thesis statement with red gradient styling. Below it, the ambition/execution paragraph.

**Acceptance**:
- Thesis banner renders with "ASPIRE. ACT. ACHIEVE." in red gradient
- Body paragraph: "Ambition without execution is theatre..."
- Light and dark theme variants both work
- Red gradient uses `from-ls-red via-ls-red/40 to-ls-red/85` per existing pattern

**Verify**:
- `npm test -- --run --grep ThesisBanner`
- Check red gradient rendering in both themes
- `uv run ruff check src/`

**Files to touch** (max 5):
- `src/components/ThesisBanner.tsx` — new file
- `src/components/AboutSection.tsx` — import and integrate ThesisBanner

---

## Task 4: Create OperatingModelGrid component — Strategy → Build → Govern → Research

**Description**: Build `src/components/OperatingModelGrid.tsx` featuring the 4-step operating model grid (Strategy, Build, Govern, Research) in a responsive 12-column grid with brand-styled wells.

**Acceptance**:
- 4 grid items render: Strategy, Build, Govern, Research
- Correct body text for each step
- Responsive: 1 column on mobile, 2 on sm, 4 on lg
- Brand-styled wells (`flight-deck-well-light` / `flight-deck-well-dark`)
- Light and dark themes both work

**Verify**:
- `npm test -- --run --grep OperatingModelGrid`
- Check responsive grid behavior (browser resize or CSS)
- `uv run ruff check src/`

**Files to touch** (max 5):
- `src/components/OperatingModelGrid.tsx` — new file
- `src/components/AboutSection.tsx` — import and integrate OperatingModelGrid

---

## Task 5: Create MissionVisionValuesGrid component — Mission, Vision, Core Values

**Description**: Build `src/components/MissionVisionValuesGrid.tsx` featuring 3 sections in prescribed order: Institutional Mission, Strategic Vision, Why LightSpeed (Core Values). Each has icon (Target, Compass, ShieldCheck), title, and body text. Uses brand grid (12-column, gap-6, md:grid-cols-3).

**Acceptance**:
- 3 sections render in prescribed order: Mission → Vision → Core Values
- Each has correct icon, title, and body text
- Mission: "To enable enterprises... sovereign AI operating models..."
- Vision: "To establish LightSpeed Holdings Limited as the premier AI-Native Operator..."
- Core Values: "We are not a generic software outsourcer..."
- Responsive grid: 1 column on mobile, 3 on md+
- Brand-styled chassis-milled wells
- Light and dark themes both work

**Verify**:
- `npm test -- --run --grep MissionVisionValuesGrid`
- Verify order: mission before vision before values
- `uv run ruff check src/`

**Files to touch** (max 5):
- `src/components/MissionVisionValuesGrid.tsx` — new file
- `src/components/AboutSection.tsx` — import and integrate MissionVisionValuesGrid

---

## Task 6: Create BrandCarousel component with media artifacts

**Description**: Build `src/components/BrandCarousel.tsx` featuring a carousel with 3+ slides auto-cycling with manual controls. Each slide integrates:
- 1 illustration from `article-illustrations` skill (Grav character IP)
- 1 Mermaid diagram from `ls-diagramming` skill (LightSpeed brand)
- 1 infographic from `k-dense-infographics` or `ls-visual-storytelling` skill

Carousel uses framer-motion for entrance transitions and CSS for auto-cycle.

**Acceptance**:
- Carousel auto-cycles every 6 seconds
- Manual prev/next controls work
- 3 slides render with different media combinations
- Brand colors respected across all slides
- Accessibility: aria-labels, keyboard navigation, pause on hover
- No CLS issues

**Verify**:
- `npm test -- --run --grep BrandCarousel`
- Playwright: verify carousel auto-plays and manual controls work
- `uv run ruff check src/`

**Files to touch** (max 5):
- `src/components/BrandCarousel.tsx` — new file
- `src/components/AboutSection.tsx` — import and integrate BrandCarousel

---

## Task 7: Integrate article-illustrations skill output (Grav illustrations)

**Description**: Use the `article-illustrations` skill to generate Grav character illustrations for the About Page carousel/slides. The skill generates hand-drawn article illustrations featuring the Grav character IP.

**Acceptance**:
- At least 1 Grav illustration generated and rendered on the About Page
- Illustration style consistent with LightSpeed brand (navy/red/cyan palette)
- Image has appropriate alt text (descriptive, not generic)
- File size optimized for web (LCP impact considered)

**Verify**:
- Inspect generated illustration file(s) in `src/components/BrandCarousel.tsx`
- Check alt text is descriptive and relevant
- `npm test -- --run`
- `uv run ruff check src/`

**Files to touch** (max 5):
- `src/components/BrandCarousel.tsx` — import illustration
- No direct file edits — skill output is consumed via the skill tool

---

## Task 8: Integrate ls-diagramming skill output (Mermaid diagrams)

**Description**: Use the `ls-diagramming` skill to generate a Mermaid diagram in LightSpeed brand (navy/red/cyan) for the About Page. Diagram type could be: system architecture, value chain, or agent hierarchy diagram.

**Acceptance**:
- 1 Mermaid diagram generated and rendered on the About Page
- Diagram uses LightSpeed brand colors (navy rail, red accents, cyan highlights)
- Diagram has a descriptive caption
- Rendered as standalone HTML with inline SVG, dark/light themes
- Diagram fits within the About Page layout constraints

**Verify**:
- Run `ls-diagramming` skill to generate the diagram
- Inspect the generated HTML/SVG output
- Check color compliance with brand tokens
- `npm test -- --run`
- `uv run ruff check src/`

**Files to touch** (max 5):
- `src/components/BrandCarousel.tsx` — embed diagram HTML/SVG
- No direct file edits — skill output consumed via skill tool

---

## Task 9: Integrate k-dense-infographics or ls-visual-storytelling skill output

**Description**: Use either the `k-dense-infographics` or `ls-visual-storytelling` skill to generate a branded infographic for the About Page. Infographic should reinforce key brand messaging (leapfrogging opportunity, agentic AI operating systems, African markets).

**Acceptance**:
- 1 branded infographic generated and rendered on the About Page
- Uses LightSpeed brand palette (navy #070A40, red #E63946, cyan #00BFFF)
- Supports key messaging about sovereign AI operating models
- Renders as professional infographic with proper data visualization
- Light and dark theme variants available

**Verify**:
- Run the chosen skill (k-dense-infographics or ls-visual-storytelling)
- Inspect generated output for brand compliance
- Check color usage against brand-tokens.json
- `npm test -- --run`
- `uv run ruff check src/`

**Files to touch** (max 5):
- `src/components/BrandCarousel.tsx` — embed infographic
- No direct file edits — skill output consumed via skill tool

---

## Task 10: Expand leadership data — Jack Mlusu + executive team

**Description**: Verify/expand `src/data/leadership.ts` with Jack Mlusu founder bio and potentially additional executive team members for the Leadership Chassis section. The Master Spec §15 has 1 human CEO; additional members may be added if the design requires a team showcase.

**Acceptance**:
- Jack Mlusu entry is complete with id, name, initials, title, bio
- Leadership data compiles without errors
- If additional executives are added, they follow the Leader interface
- Light and dark theme styling works with leadership cards

**Verify**:
- `uv run mypy src/data/leadership.ts`
- `npm test -- --run`
- `uv run ruff check src/`

**Files to touch** (max 5):
- `src/data/leadership.ts` — verify/extend Jack Mlusu entry and/or add executives

---

## Task 11: Compose full AboutPage.tsx with all sections + dark mode

**Description**: Update `src/pages/AboutPage.tsx` to compose the full page with all sections: HeroBanner, ThesisBanner, OperatingModelGrid, MissionVisionValuesGrid, BrandCarousel, LeadershipChassis, CTA. Add dark mode variants (theme prop = 'light' | 'dark').

**Acceptance**:
- Full AboutPage renders at `/about` route
- All sections in correct order: hero → thesis → operating model → mission/vision/values → carousel → leadership → cta
- Dark mode (`theme='light'`) works across all sections
- Light mode (`theme='dark'`) works across all sections
- CTA button "Partner with LightSpeed Holdings Limited" functions and routes to `/contact`
- SEO metadata present (title, description, open graph tags)

**Verify**:
- `npm run build` — successful build
- `npm test -- --run` — all tests pass
- `uv run ruff check src/ && uv run mypy src/`
- Playwright: `npx playwright test e2e/about-page.spec.ts` if E2E exists

**Files to touch** (max 5):
- `src/pages/AboutPage.tsx` — compose full page with all sections, dark mode
- `src/components/AboutSection.tsx` — may need minor updates to integrate new components

---

## Task 12: Final QA — tests, lint, typecheck, accessibility, performance

**Description**: Run comprehensive verification to confirm all success criteria are met. Includes unit tests, lint, typecheck, Playwright E2E, accessibility audit, and performance metrics.

**Acceptance**:
- All unit tests pass (80%+ coverage for new code)
- Ruff + MyPy pass with no new errors
- Playwright E2E: AboutPage loads, all sections display in correct order, CTA works, dark mode switches
- Accessibility: WCAG AA — contrast ≥ 4.5:1, alt text on all images, keyboard-navigable carousel
- Performance: LCP < 2.5s, CLS < 0.1 (audit with Lighthouse/PageSpeed)
- No mention of Honest status discipline anywhere on the page

**Verify**:
- `uv run ruff check src/ && uv run mypy src/ && pytest` — or `npm test -- --run --coverage`
- `npm test:e2e` — Playwright suite
- `npx playwright test --reporter=terminal` — detailed output
- Lighthouse CI or manual PageSpeed audit
- Manual review: scroll page, verify no Honest status discipline content, verify brand order

**Files to touch** (max 5):
- No new file changes expected — verification only
- May fix any issues revealed by testing

---
*All tasks derived from `tasks/plan.md` and `tasks/spec-about-page.md`. Tasks should be worked in order; later tasks depend on earlier task outputs. No task should require changing more than ~5 files.*
