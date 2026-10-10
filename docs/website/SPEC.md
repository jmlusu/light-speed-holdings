# Spec: LightSpeed Holdings External Website Consolidation

## 1. Objective

**What we're building:** A coherent, credible, production-ready public website for LightSpeed Holdings Limited that communicates the company's AI-native company-building operating model, H-A-O-M-T-G-V framework, open-source/open-weight AI economics, and practical capabilities.

**Who the user is:** Prospective clients, university researchers, regulators, institutional leaders, business executives, AI practitioners, and African market participants seeking to understand LightSpeed's capabilities and engagement pathways.

**What success looks like:**
- Public website deploys and displays correctly at the verified Vercel domain
- Eight-item primary navigation (Home, What We Do, AI Company Builder, Solutions, Use Cases, Sectors, Insights, About) is intact and functional across all routes
- H-A-O-M-T-G-V framework explained as "90 operating roles. 89 AI agents. One Human CEO." with no contradictory claims
- FAQ component is accessible, keyboard-navigable, and contains at least 22 evidence-controlled questions
- Brand tokens (navy #070A40, cyan #00BFFF, red #E63946, white #FFFFFF, light grey #F2F2F2, dark grey #6B7280, light text grey #9CA3AF) are centralized and consistent across all pages
- No unsupported commercial, partnership, deployment or performance claims are introduced
- Public and internal application boundaries remain intact (no exposure of secrets, private prompts, internal databases, credentials, or sensitive orchestration details)
- Production build passes type checking and automated tests
- Live deployment has been independently verified after approved deployment

## 2. Commands

| Operation | Command |
|---|---|
| Build | `npm run build` |
| Test (unit) | `npm test -- --coverage` |
| Test (e2e) | `npx playwright test` |
| Lint | `npm run lint` |
| Type check | `npx tsc --noEmit` |
| Dev (local) | `npm run dev` |
| Dev (port 8421) | `npm run dev -- --port 8421` |
| Regenerate agents | `uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| Check server health (staging) | `curl -H "X-API-Key: $DASHBOARD_ADMIN_KEY" http://localhost:8421/health` |
| Check server health (production) | `curl -H "X-API-Key: $DASHBOARD_ADMIN_KEY" https://api.example.com/health` |
| Run website route sweep (Playwright) | `npx playwright test --project=chromium` |

## 3. Project Structure

```
src/                           → Application source code (React + TypeScript + Vite)
src/components/                → React components (global, shared, page-specific)
src/components/site/           → Site-level components (Layout, Header, Footer, Logo)
src/pages/                     → Page components indexed by route (14+ public routes)
src/lib/                     → Shared utilities (brand tokens, API helpers, formatting)
src/lib/tokens.ts              → Centralized brand token definitions
src/lib/urls.ts                → Canonical URL constants
src/routes/                    → Route configuration and guards
src/hooks/                     → Custom React hooks
src/data/                      → Content registries (useCases, sectors, faqs, solutions, ctas, claims)
src/styles/                    → Global styles, Tailwind config, base styles
public/                        → Static assets
public/brand/                  → Brand assets (logo SVGs, token references)
public/logo-*.svg              → Logo variant files
public/logos/                  → Legacy/or alternate logo files
docs/website/                  → Documentation (this spec, architecture, design system, media, content governance)
tasks/website-transformation/  → Implementation plan, todo, implementation report
```

**Test locations:**
- Unit: `src/components/`, `src/pages/`, `src/lib/`, `src/data/`
- E2E: `tests/e2e/` (Playwright) — covers critical user flows

## 4. Code Style

**Naming conventions:**
- Components: PascalCase (`UseCasesPage.tsx`, `FaqAccordion.tsx`)
- Utilities: camelCase (`formatDate.ts`, `cn.ts` — className merger)
- Files: kebab-case for styles, PascalCase for components
- Folders: lowercase (`components/`, `lib/`, `pages/`)
- Hooks: `use` prefix (`useForm.ts`, `useToken.ts`)

**Formatting rules (Tailwind + CSS):**
- Inline styles only — no external stylesheets in components
- All Tailwind classes must be alphabetically sorted within each directive
- `className` merges use the `cn()` utility from `src/lib/`
- Media (images, iframes) always have `block`, `max-w-full`, `h-auto`, `object-cover`
- SVGs have `fill-current`, `w-6`, `h-6` (or appropriate size) and `block`/`inline-block` as needed
- Focus states must include `outline-none ring-2 ring-offset-2 ring-primary-500` pattern
- Reduced-motion: `@media (prefers-reduced-motion: reduce)` must disable all non-essential animations

**Example snippet (good output):**

```tsx
// src/components/cta/PrimaryCta.tsx
import { cn } from '@/lib';

interface PrimaryCtaProps {
  onClick: () => void;
  children: React.ReactNode;
}

export function PrimaryCta({ onClick, children }: PrimaryCtaProps) {
  return (
    <a
      href="#"
      onClick={onClick}
      className={cn(
        "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring-500 focus-visible:ring-offset-2",
        "bg-primary-600 text-primary-100 hover:bg-primary-500 disabled:opacity-50 disabled:pointer-events-none disabled:select-none",
        "py-3 px-6 gap-2"
      )}
    >
      {children}
    </a>
  );
}
```

## 5. Testing Strategy

**Framework:** Jest + React Testing Library for unit tests; Playwright for e2e tests.

**Test locations:**
- Unit: `src/components/`, `src/pages/`, `src/lib/`
- E2E: `tests/e2e/` — covers critical user flows (navigation, form submission, CTA clicks, responsive breakpoints, accessibility)

**Coverage expectations:**
- Minimum 80% statement coverage for unit tests in `src/components/` and `src/lib/`
- Critical user flows must have e2e coverage in Playwright
- No tests should be skipped without a tracked issue

**Test levels and concerns:**
- **Unit:** Component rendering with correct props, event handler invocation, state updates, utility function outputs
- **Integration:** Page-level interactions (navigation routing, form submit → API mock, CTA redirect), cross-component consistency
- **E2E:** Full user flows (landing → navigation → CTA → form submission → confirmation), responsive breakpoints (mobile/desktop), accessibility (keyboard navigation, screen reader announcements, contrast ratios), error boundaries

**Verification steps (run before every commit):**
1. `npm run lint`
2. `npx tsc --noEmit`
3. `npm test -- --coverage`
4. `npx playwright test --project=chromium` (smoke: critical paths only)

## 6. Boundaries

**Always do:**
- Run `npm run lint && npx tsc --noEmit && npm test -- --coverage` before commits
- Follow naming conventions and formatting rules (see Code Style section)
- Validate all user inputs (form fields, URL parameters, navigation links)
- Preserve public/internal application boundaries — never expose secrets, private prompts, internal databases, credentials, or sensitive orchestration details
- Keep the eight-item primary navigation intact
- Document any CEO's existing changes and work outside agreed scope

**Ask first:**
- Database schema changes (Prisma migrations) — verify no public data is affected
- Adding new dependencies — confirm no duplicate or conflicting packages
- Changing CI config — ensure deployment pipelines remain functional
- Modifying the brand token system — resolve discrepancies deliberately, do not introduce a second palette

**Never do:**
- Commit secrets (API keys, tokens, credentials) to any repository
- Edit vendor directories or lock files except through package manager
- Remove failing tests without approval — debug and fix instead
- Overwrite the CEO's existing changes or discard work outside agreed scope
- Introduce unsupported commercial, partnership, deployment or performance claims
- Force every page into the same layout — reuse design primitives while giving each page a layout appropriate to its purpose

## Success Criteria

1. Current repository state and all changes are documented (gap register, implementation plan)
2. Public website uses one coherent, approved LightSpeed design system
3. New logo is implemented consistently with all required variants; any missing approval is explicitly identified
4. Eight-item primary navigation remains intact (Home, What We Do, AI Company Builder, Solutions, Use Cases, Sectors, Insights, About)
5. FAQ, Academia, Universities, Research and Regulators are included in appropriate page content without adding to primary navigation
6. Proof is retired as a primary information-architecture concept; Use Cases is the public-facing replacement
7. Canonical operating model explained as 90 roles: 89 AI agents and one Human CEO role
8. H-A-O-M-T-G-V explained accurately and represented visually
9. Open-source and open-weight AI economics are central to the LightSpeed proposition
10. Pharos established as the in-house thought-leadership team under Insights
11. Sector, solution, Use Case and FAQ content use governed, consistent data sources
12. Media is distributed strategically throughout the website (not concentrated in hero/gallery only)
13. No unsupported commercial, partnership, deployment or performance claims are introduced
14. Public and internal application boundaries remain intact
15. All critical public routes, redirects, forms and 404 behavior work
16. Accessibility, responsive behavior, SEO and performance have been tested
17. Existing unrelated changes have been preserved
18. Production build and automated tests pass
19. Live deployment has been independently checked after deployment
20. Remaining limitations are documented honestly

## Open Questions (require human input)

1. **Logo artwork:** The intended final logo SVG asset is ambiguous — CEO approval needed to confirm which existing asset (`src/components/site/Logo.tsx`, `public/brand/`, `public/logo-*.svg`, `public/logos/`) corresponds to the approved geometric LightSpeed direction (sharp forward-moving geometric L, interlocking planes, cyan/blue technology core, restrained red acceleration element).

2. **Brand token discrepancies:** Several token files exist across the repo — need human to review and consolidate into one canonical source without introducing a second palette.

3. **Vite/TypeScript alias divergence:** Registry locations need identification of every consumer before any change; requires careful testing.

4. **H-A-O-M-T-G-V diagram implementation:** Whether to use responsive SVG/CSS or canvas-based approach needs design decision.

5. **Africa-first AI economics infographic:** Trade-off details (cost, performance, privacy, connectivity, maintenance) need evidence-backed wording — no fabricated savings or misleading claims.

6. **Pharos editorial formats:** Which recurring formats (Brief, Field Note, Research Note, Policy Note, System Map, Data Story, AI Economics, Africa Watch) are prioritized for initial implementation.

7. **Sector content consolidation:** Which existing sector registries are authoritative; mapping of consumers and migration path for legitimate references.

8. **Media ownership and alt text:** Several temporary assets exist — need human to assign ownership, purpose, and replacement timeline for each.

9. **Turnstile form integration:** Exact security controls and rate-limiting configuration for contact form.

10. **Staging vs production domain mapping:** Verification of actual Vercel project and domain mapping before deployment.
