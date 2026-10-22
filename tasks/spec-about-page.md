# Spec: About Page — LightSpeed Holdings Limited

## Objective

Build a standalone About Page on the LightSpeed Holdings marketing site (https://lightspeedholdings.vercel.app) that strategically showcases the company's identity in a prescribed order:

1. **LightSpeed Holdings Limited** — corporate entity
2. **Mission** — enabling sovereign AI operating models for African enterprises
3. **Vision** — premier AI-Native Operator and Partner globally
4. **Core Values** — the principles that guide the company
5. **Jack Mlusu** — Founder & CEO, the human authority

The page must be strategically designed to engage users with strategic media artifacts (carousels, animations, illustrations, infographics) while remaining silent on Honest status discipline for the time being.

Success is measured by: user engagement, clear communication of brand identity, and alignment with the LightSpeed Holdings brand system (navy #070A40, red #E63946, cyan #00BFFF, Arial type scale, 4px grid).

## Tech Stack

- **Framework**: React 18 + TypeScript (Vite)
- **Styling**: Tailwind CSS 4 with brand token classes
- **Components**: Existing `AboutSection.tsx`, `AboutPage.tsx` in `src/pages/`, `leadership` data in `src/data/`
- **Brand tokens**: `brand/tokens/brand-tokens.json` (navy, red, cyan, type scale, grid, spacing)
- **Illustrations**: `article-illustrations` skill (Grav character IP)
- **Diagrams**: `ls-diagramming` skill (Mermaid diagrams)
- **Infographics**: `k-dense-infographics` skill or `ls-visual-storytelling` skill
- **Carousel**: Custom React carousel or `ls-frontend-design` pattern
- **Animation**: Framer Motion for entrance/transition effects
- **Testing**: Vitest + React Testing Library
- **Lint/Type**: `uv run ruff check src/` + `uv run mypy src/`

## Commands

| Action | Command |
|--------|---------|
| Build | `npm run build` |
| Test | `npm test -- --coverage` |
| Lint | `uv run ruff check src/` |
| Type Check | `uv run mypy src/` |
| Dev | `npm run dev` |
| Regenerate Agents | `uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |

## Project Structure

```
src/
  pages/              → Page components (AboutPage.tsx already exists)
  components/         → AboutSection.tsx (existing), hero, carousel, infographic components
  data/               → leadership.ts (Jack Mlusu), ctas.ts, brand tokens
  lib/                → Shared utilities (carousel, animation helpers)
  layouts/            → PageShell.tsx, PageContainer.tsx
  styles/             → Global styles, theme overrides
  hooks/              → useFontLoad, useIntersectionObserver
  constants/          → Brand constants, CTA labels
public/
  brand/              → Logo assets, icons, images
  brand/templates/    → Pre-built templates
docs/
  about/              → Spec documents, design rationale
tasks/
  spec-about-page.md  → This specification
```

## Code Style

**Naming conventions:**
- Components: PascalCase (`AboutSection`, `HeroCarousel`, `MissionGrid`)
- Variables: camelCase (`brandNavy`, `missionStatement`)
- Constants: UPPER_SNAKE_CASE (`CTAS_PRIMARY`, `MAX_WIDTH`)
- Files: kebab-case for templates, PascalCase for components

**Formatting rules (Tailwind + CSS):**
- Use brand token classes: `text-ls-navy`, `bg-ls-red`, `text-ls-cyan`
- Color palette: navy `#070A40` (dominant), red `#E63946` (accent), cyan `#00BFFF` (accent), grey-light `#F2F2F2`, white `#FFFFFF`
- Typography: Arial, weight 700 for display/headings, weight 400 for body (per brand-tokens.json)
- Grid: 12-column, 24px gutter, 48px margin, max-width 1200px (per brand-tokens.json)
- Spacing: base unit 4px, scale 4/8/12/16/24/32/48/64/96
- Rounded corners: small 4px, medium 8px, large 16px
- No flexbox/grid shorthand — use `padding-top` not `padding` (per Resend HTML guidelines, applied analogously)
- Inline styles only where Tailwind isn't appropriate

**Code snippet example (good):**

```tsx
<div className="p-6 sm:p-8 rounded-3xl border bg-ls-grey-light text-ls-navy">
  <h2 className="text-2xl font-bold font-display text-ls-navy mb-4">Mission</h2>
  <p className="text-base leading-relaxed">To enable enterprises across Malawi and African markets to design, build, and govern sovereign AI operating models...</p>
</div>
```

**Anti-pattern (avoid):**

```tsx
<div style={{ padding: '1rem', color: '#0070f3' }}>
  <h2>Mission</h2>
</div>
```

## Testing Strategy

- **Framework**: Vitest + React Testing Library
- **Test locations**: `src/tests/about-page/`, `src/__tests__/ AboutPage.test.tsx`
- **Coverage requirements**: 80% minimum for new code
- **Test levels**:
  - **Unit**: Individual component rendering, brand token class application
  - **Integration**: AboutPage with AboutSection, carousel navigation, CTA flow
  - **E2E**: Playwright tests at `e2e/about-page.spec.ts` — verify page loads, mission/vision/values display, carousel auto-plays, CTA button works
- **Verification commands**:
  - `npm test -- --run --coverage`
  - `npm test:e2e` (Playwright)
  - `uv run graphify query "about page"` — surf prior bug fixes

**Acceptance criteria for tests:**
- AboutPage renders without errors in light and dark themes
- Mission statement displays correctly with proper brand styling
- Vision statement displays after mission, in prescribed order
- Core Values grid shows 3-5 values with correct iconography
- Jack Mlusu section renders with founder bio
- Carousel components auto-cycle and respond to manual controls
- All brand colors comply with brand-tokens.json
- No CLS (layout shift) CLS < 0.1
- LCP < 2.5s on 4G connection

## Boundaries

### Always do:
- Run `npm test -- --run` before committing
- Follow brand token classes (`text-ls-navy`, `bg-ls-red`, etc.)
- Use Arial type scale from `brand-tokens.json`
- Maintain 12-column grid with 24px gutter
- Include `™` on first mention of "LightSpeed Holdings Limited"
- Keep page silent on Honest status discipline

### Ask first:
- Database schema changes (not applicable — static page)
- Adding new dependencies (verify no conflict with existing packages)
- Changing CI config (verify 6 required checks still pass)
- New animation libraries (verify against existing framer-motion usage)

### Never do:
- Commit secrets or `.env` files
- Edit `vendor` or `node_modules` directories
- Remove failing tests without approval
- Invent brand colors or typography outside `brand-tokens.json`
- Add content about Honest status discipline

## Success Criteria

The About Page is complete when all of the following are true:

1. **Page structure**: AboutPage renders at `/about` route with correct SEO metadata (title, description, open graph tags)
2. **Entity showcase order**: LightSpeed Holdings Limited → Mission → Vision → Core Values → Jack Mlusu (in that exact order)
3. **Brand compliance**: All colors from `brand-tokens.json`; no off-palette colors; `™` on first mention; Arial type scale; 4px spacing grid
4. **Media artifacts**:
   - Carousel with 3+ slides auto-cycling with manual controls
   - At least 1 illustration (Grav character via `article-illustrations` skill pathway)
   - At least 1 Mermaid diagram via `ls-diagramming` skill
   - At least 1 infographic via `k-dense-infographics` or `ls-visual-storytelling` skill
5. **Accessibility**: WCAG AA compliant — contrast ratio ≥ 4.5:1, alt text on all images, keyboard-navigable carousel, focus management
6. **Performance**: LCP < 2.5s, CLS < 0.1, FCP < 1.5s on local dev setup
7. **CTA**: "Partner with LightSpeed Holdings Limited" button functions, routes to `/contact`
8. **Silent on Honest status**: No mention, reference, or implication of Honest status discipline anywhere on the page

## Open Questions

1. **Carousel content**: Should the carousel feature illustrations, brand statements, or customer stories? — *Needs human input from CMO/CMO team*
2. **Core Values selection**: Which core values to showcase? The brand guidelines don't explicitly list core values — should we infer from mission/vision or use established company values? — *Needs human input*
3. **Illustration style**: Grav character illustrations or abstract brand-focused illustrations? — *Per `article-illustrations` skill, Grav IP is used; confirm with Creative Director*
4. **Diagram type**: What kind of architecture/diagram best represents the About content? (system architecture, value chain, agent hierarchy) — *Per `ls-diagramming` skill, confirm topic*
5. **Animation complexity**: Subtle entrance animations vs. elaborate continuous animations — *Balance engagement against performance metrics*
6. **Dark mode variants**: All brand tokens have light/dark support; confirm design accounts for both themes — *Verify with design system owner*

> **Note**: All open questions should be resolved before advancing to Phase 2 (Plan). The spec is a living document — update as decisions are made.

## Agent Team Roster

For the About Page design, the following agents/sub-agents should be invoked during implementation:

| Agent | Role | Trigger |
|-------|------|---------|
| `ls-creative-director` | Orchestrates the creative brief; decides skill chain (design-system → production → artifact-qa) | Kickoff meeting about page concept |
| `ls-frontend-design` | Builds distinctive, on-brand LightSpeed websites/landing pages; enforces design system (navy/red/cyan, Arial scale, 4px grid) | Component design and implementation |
| `ls-visual-storytelling` | Turns information into visual communication (infographics, one-pagers, visual abstracts) always on-brand | Infographic and illustration design |
| `ls-diagramming` | Produces technical/diagrams (architecture, process, flow) in LightSpeed brand | System/architecture diagrams |
| `ls-brand-advertising` | Specializes in commercial creative (ads, banners, campaign graphics); enforces brand palette and dimensions | Brand compliance and CTA design |
| `ls-artifact-qa` | Last gate on every artifact: visual/brand/UX/accessibility/content QA → APPROVE or FIX→re-render | Final quality gate |
| `ls-design-system` | MUST be loaded first by any creative skill; enforces brand tokens, logo rules, template usage | Brand system enforcement (pre-requisite) |

> **Invocation protocol**: Each agent is invoked via the `skill` tool with the agent's `SKILL.md` file. The agent's instructions and workflow guidance are injected into the current conversation. No code is built until all agents have signed off on the spec and open questions are resolved.

---
*This spec was generated following spec-driven development methodology. It is a living document — update when decisions change, scope changes, or open questions are resolved. Commit this spec alongside the code it describes.*
