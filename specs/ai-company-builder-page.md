# Spec: AI Company Builder Marketing Page

## Objective

Build a standalone, strategically designed AI Company Builder page for the LightSpeed Holdings marketing site that showcases the AI Native Company as an authority in the space. The page should engage users with rich media (carousels, animations, illustrations, infographics, diagrams, responsive hero imagery) while remaining strategically focused on demonstrating capabilities rather than technical disclosure.

**Success Criteria:**
- Page loads with LCP < 2.5s on 4G connection
- All interactive elements (carousels, filters, toggles) are accessible via keyboard and screen reader
- Brand compliance: navy `#070A40`, red `#E63946`, cyan `#00BFFF` dominant with 80/10/10 ratio
- Page is fully responsive from 320px to 1440px+
- Zero references to "honest status discipline" or provenance-based access tiers
- All animations respect `prefers-reduced-motion`
- Page passes all existing lint, mypy, and pytest gates without new failures

**User Stories:**
1. As a prospective client, I want to quickly understand what the AI Company Builder platform does and its core value.
2. As a prospective agent/hire, I want to explore the agent registry and agent roles in an engaging way.
3. As a decision-maker, I want to see social proof, use cases, and KPI evidence that the platform works.
4. As a mobile user, I want the same core message and interactives to work seamlessly on my device.

## Tech Stack

- **Framework:** React 18+ with TypeScript
- **Styling:** Tailwind CSS v4 (configured via `brand-tokens.css` and `tailwind.config.ts`)
- **Animations:** IntersectionObserver-based `Reveal` component (existing pattern); CSS transitions for hover/state changes
- **Charts/Diagrams:** Recharts for KPI/trend visualizations; Mermaid for architecture diagrams rendered via `k-dense-mermaid-skill` or inline SVG
- **Carousels:** Swiper.js (existing site dependency) or simple carousel built on `Reveal` + state management
- **Data fetching:** SWR or React Query for agent registry data; static data where appropriate
- **Build:** `npm run build` (Vite); `npm run dev` (Vite dev server)
- **Type checking:** `npx tsc --noEmit`
- **Lint:** `npm run lint` (ruff-ts / eslint)
- **Test:** `npm test` (vitest) + existing 1743 unit/integration tests

**Existing dependencies (already in package.json):**
- `react`, `react-dom`, `react-router-dom`
- `tailwindcss`, `postcss`, `autoprefixer`
- `lucide-react` (icons)
- `swiper` (carousel/slideshow library — already a site dependency)
- ` Reveal` component (stagger reveal, IntersectionObserver-based)
- `brand-tokens.css` (navy/red/cyan CSS vars)

## Commands

| Action | Command |
|--------|---------|
| Build | `npm run build` |
| Dev server | `npm run dev` |
| Type check | `npx tsc --noEmit` |
| Lint | `npm run lint` |
| Test | `npm test` |
| Test watch | `npm test -- --watch` |
| Typecheck + lint + test | `npm run lint && npx tsc --noEmit && npm test` |

## Project Structure

```
src/
├── pages/
│   └── AiCompanyBuilderPage.tsx    ← New/updated standalone page
│   └── AiCompanyBuilderPage.test.tsx ← Test file
├── components/
│   ├── AiCompanyBuilder/
│   │   ├── HeroCarousel.tsx        ← Hero image + rotating key stats
│   │   ├── AgentGrid.tsx           ← Filterable 90-agent showcase grid
│   │   ├── PrincipleCards.tsx      ← 10 principle cards with hover effects
│   │   ├── KPIChart.tsx            ← Recharts-based KPI trend chart
│   │   ├── ArchitectureDiagram.tsx ← Mermaid/SVG system diagram
│   │   ├── UseCaseCarousel.tsx     ← Swiper-based use case carousel
│   │   └── HonestyBadge.tsx        ← **SILENT** — badge component excluded from this page
│   ├── shared/
│   │   ├── Reveal.tsx              ← IntersectionObserver stagger reveal (existing)
│   │   ├── CtaBand.tsx             ← Consistent CTA strip (existing)
│   │   └── PageShell.tsx           ← Page layout wrapper (existing)
│   └── ui/
│       ├── Card.tsx                ← Card component with hover/state
│       ├── Button.tsx              ← Primary/secondary button styles
│       ├── Select.tsx              ← Filter selector for agent grid
│       └── Tabs.tsx                ← Tab navigation for sections
├── data/
│   ├── aiCompanyBuilder.ts         ← Static page data (metrics, principles, use cases)
│   ├── agentRegistry.ts            ← 90-agent metadata (subset for page showcase)
│   ├── useCases.ts                 ← 8-10 use case summaries with hero illustrations
│   └── kpis.ts                     ← KPI values displayed on page
├── lib/
│   ├── useSWR.js                   ← Data fetching (or react-query)
│   └── reducedMotion.js            ← prefers-reduced-motion hook
├── types/
│   ├── aiCompanyBuilder.types.ts   ← TypeScript interfaces for page data
│   └── agent.types.ts              ← Agent card type definitions
└── styles/
    └── page utilities ( Tailwind overrides, color utilities)
```

**Key Data Files (static, no API required):**
- `src/data/aiCompanyBuilder.ts` — Metrics, principles, use case summaries, KPI values
- `src/data/agentRegistry.ts` — Subset of 90 agents with name, role, department, primary tool, illustration caption
- `src/data/useCases.ts` — Use case title, problem statement, outcome, hero illustration reference
- `src/data/kpis.ts` — Sent/delivered/opened rates, cost reduction, latency numbers

## Code Style

**One real code snippet beats three paragraphs describing it.**

### Tailwind Class Conventions (from existing codebase)

```tsx
// Card with reveal animation and hover state
<div className="group rounded-2xl overflow-hidden bg-ls-white/95 dark:bg-ls-navy/80 p-6 sm:p-8 transition-colors duration-300 hover:bg-ls-red/10 hover-shadow-xl">
  <Reveal delay={index * 0.04}>
    <h3 className="font-display font-bold text-lg tracking-tight text-ls-navy mb-3">{title}</h3>
    <p className="text-ls-grey-dark text-sm leading-relaxed">{description}</p>
  </Reveal>
</div>
```

### Naming Conventions

- **Components:** PascalCase, `*Component.tsx` (e.g., `HeroCarousel.tsx`, `AgentGrid.tsx`)
- **Types:** PascalCase interfaces, `*Types.ts` (e.g., `AgentCardTypes.ts`)
- **Data files:** camelCase, `*.ts` (e.g., `aiCompanyBuilder.ts`)
- **Hooks:** `use` prefix, camelCase (e.g., `useSWR.js`, `useReducedMotion.js`)
- **Utility functions:** camelCase, `*Util.js` (e.g., `reducedMotion.js`)

### Color Usage (80/10/10 Rule)

| Usage | CSS Class | Context |
|-------|-----------|---------|
| Navy dominant (80%) | `text-ls-navy`, `bg-ls-navy/80`, `border-ls-grey-dark` | Headings, primary backgrounds, card borders |
| Red accent (10%) | `text-ls-red`, `bg-ls-red/10`, `border-ls-red/40`, `ring-ls-red/30` | CTAs, badge backgrounds, hover states, governance highlights |
| Cyan accent (10%) | `text-ls-cyan` | Links, pillar icons, accent elements on dark surfaces |

### TypeScript Conventions

- All components receive explicit `theme: 'light' | 'dark'` prop
- Interfaces are complete — no `any` types
- Event handlers are typed: `(e: React.MouseEvent<HTMLButtonElement>) => void`
- Prop interfaces are defined per-component, not shared globally unless truly reusable

### Good Output Example

```tsx
// PrincipleCard.tsx — single principle card with reveal + hover
interface PrincipleCardProps {
  title: string;
  description: string;
  icon: React.ComponentType<{ className: string }>;
  theme: 'light' | 'dark';
}

export const PrincipleCard: React.FC<PrincipleCardProps> = ({
  title,
  description,
  icon,
  theme,
}) => (
  <div
    className={`group rounded-2xl p-5 border transition-all duration-300 ${
      theme === 'light'
        ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
        : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
    }`}
  >
    <Reveal delay={0}>
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0">{icon}</div>
        <div className="flex-1">
          <h3 className="font-display font-bold text-base tracking-tight text-ls-red mb-2">{title}</h3>
          <p className="text-ls-grey-dark text-sm leading-relaxed">{description}</p>
        </div>
      </div>
    </Reveal>
  </div>
);
```

### Bad Output Example (to avoid)

> "Cards should have rounded corners and change color when you hover over them. They should also animate in when they appear on the page. The colors should be navy and red and maybe cyan too. Types should be defined for the props."

## Testing Strategy

**Framework:** vitest with React Testing Library

**Test Levels:**

| Level | Scope | Location |
|-------|-------|----------|
| Unit | Individual components rendered with mocked data | `src/components/AiCompanyBuilder/` |
| Integration | Page-level rendering, carousel navigation, filter interactions | `src/pages/AiCompanyBuilderPage.test.tsx` |
| Visual | Snapshot comparison light/dark, responsive breakpoints | `vitest -- --update` |
| Accessibility | Keyboard navigation, screen reader labels | `jest-axe` or `vitest-axe` |

**Coverage Requirements:**
- Minimum 80% line coverage for new `AiCompanyBuilderPage.tsx` and `AiCompanyBuilder/` components
- All carousels have "keyboard navigation" tests (arrow keys, home/end, pagination behavior)
- All filter selectors have "no-results" state tested
- `prefers-reduced-motion` is tested by mocking the media query and verifying no animation classes are applied

**Test Filenames:**
- `AiCompanyBuilderPage.test.tsx` — Page-level render + SEO metadata
- `HeroCarousel.test.tsx` — Carousel autoplay, slide navigation, infinite loop
- `AgentGrid.test.tsx` — Filter by department, search, no-results state
- `PrincipleCards.test.tsx` — Hover state, reveal animation on scroll, active/focus styles
- `KPIChart.test.tsx` — Data props render correctly, responsive resize

**Verification Commands:**
- `npm test -- AiCompanyBuilderPage.test.tsx` — Page smoke test
- `npm test -- --coverage` — Full coverage report (gate: 80% min)
- `npm test -- --run` — Headless run in CI

## Boundaries — Three-Tier System

### Always Do (non-negotiable)

- Run `npm run lint && npx tsc --noEmit && npm test` before any commit
- Follow the 80/10/10 navy/red/cyan color rule — never use off-palette colors as dominants
- Honor `prefers-reduced-motion` — all animations must have a static fallback
- Use existing `Reveal` component for staggered reveals (do not create new IntersectionObserver logic)
- Keep the page silent on "honest status discipline" — no provenance, no access-tier badges, no "proven/pilot/fieldable" labels on this page
- All images must have descriptive `alt` text per brand voice guidelines (no emojis, no hype copy)
- responsive images must use `srcWidth`/`srcDom` or Tailwind `responsive` utilities (`sm:, md:, lg:`)

### Ask First (require confirmation before proceeding)

- Adding new external dependencies (e.g., a new chart library beyond Recharts)
- Changing the grid layout from 12-column to a different base — discuss with the team first
- Modifying the existing `AiCompanyBuilderSection.tsx` — confirm the change is compatible with the 9-journey + 10-principles structure
- Introducing a new animation library — prefer existing `Reveal` + CSS transition patterns first

### Never Do

- Commit secrets, API keys, or .env values to the repository
- Edit `vendor/` or `node_modules/` directories — manage deps via `package.json` and `npm/yarn`
- Remove or comment out existing tests without approval from the human engineer
- Add provenance-based access tiers ("proven/pilot/fieldable") to this page — the page must be silent on honest status discipline
- Use `console.log` in production builds — use the project's `debug` utility if needed
- Hard-code agent names or numbers — draw from `src/data/agentRegistry.ts` or the 90-agent registry

## Success Criteria (How We'll Know This Is Done)

- [ ] Page renders at `http://localhost:5173/ai-company-builder` in both light and dark theme
- [ ] Hero carousel auto-plays, has manual slide arrows, and loops infinitely with `aria-live` politive region
- [ ] Agent grid filters by department and search; "no results" state displays with CTA to full registry
- [ ] 10 principle cards have hover state, reveal animation on mount, and focus-visible outlines
- [ ] KPI chart renders with correct data; resizes on window resize without breaking layout
- [ ] Architecture diagram (Mermaid/SVG) is interactive (tooltip on hover) and accessible
- [ ] Use case carousel (Swiper) has prev/next arrows, pagination dots, and keyboard navigation (arrow keys, home/end)
- [ ] Zero console errors in light and dark theme
- [ ] `npm run lint` passes with 0 errors
- [ ] `npx tsc --noEmit` passes with 0 errors
- [ ] `npm test` passes with ≥80% line coverage on new files
- [ ] No references to "honest status discipline", "proven", "pilot", "fieldable", or access-tier labels anywhere on the page
- [ ] All animations respect `prefers-reduced-motion` media query (verified by mocking `window.matchMedia`)
- [ ] Page is fully responsive: 320px (mobile), 768px (tablet), 1440px (desktop) — layouts adapt without horizontal scrolling
- [ ] SEO metadata (title, description, og:tags) are present and unique to this page

## Open Questions (Need Human Input)

1. **Hero image:** Should the hero use an illustrated graphic, a photograph, or a data visualization? The brand has illustrated assets in `static/brand/` but no hero-specific asset yet. Recommendation needed.

2. **Carousel framework:** Swiper.js is already a site dependency — confirm it's acceptable to use, or build a simpler carousel on the existing `Reveal` component.

3. **Agent grid scope:** Should the agent grid showcase all 90 agents, or a curated subset (e.g., 12–16 "featured" agents with the rest linkable to the full registry)? The existing `PublicAgentRegistry` shows all 90; this page may want a highlight view.

4. **KPI values:** The page should display meaningful KPIs (e.g., "90 agents," "20 departments," "5-tier governance," "SHA-256 audit trails"). Confirm which specific metrics to feature and their source data.

5. **Architecture diagram style:** Mermaid SVG rendered via client-side library, or pre-rendered static SVG with hover tooltips? The existing `k-dense-mermaid-skill` can render diagrams, but client-side hydration may be a concern for SEO.

6. **Principle card icons:** Should icons be from `lucide-react`, custom illustrations from `static/brand/`, or Mermaid-derived? Brand guidelines prefer official illustrated assets.

7. **CTA strategy:** The page should end with a primary CTA — confirm whether it routes to `/contact`, `/ask`, or a new dedicated briefing flow.

---