# Spec: Website Artifact Roadmap — Option A

## Objective
Implement the CEO-approved set of website enhancements that expand the existing LightSpeed public SPA (lightspeedholdings.vercel.app) without adding new routes or violating the canonical Information Architecture from Directive §9–§11. Deliver in‑route artifact improvements that are already ticketed and aligned with open site‑compliance wayfinder issues. Success means the site remains a single‑page application with the exact route set defined in `src/App.tsx:79–107`; no new top‑level paths, no `/work`, no `/evidence`, no standalone Proof page.

**User:** Public visitors to lightspeedholdings.vercel.app.
**Success:** All key routes (Home, What We Do, Solutions, Use Cases, Sectors, Insights, About, Contact, legal) remain fully functional with enhanced images, analytics, journey UI, and merged content drafts. No layout breaks, no new navigation, no fabricated‑proof claims.

## Success Criteria (testable, specific)
- **Images:** Per‑page OG/social bundle landed for Home (13 sections), What We Do, Solutions, Proof (Use Cases), Insights list+article, About. Visual QA `ls‑artifact‑qa` APPROVE on each route.
- **Analytics:** Client‑side event schema (issue #307) deployed; Plausible/Umami dashboard shows event volume within ±10% of expected after 48h.
- **Journey UI:** 5‑step contact form + newsletter double‑opt‑in visible and functional on `/contact`; client‑side instrumentation (`api/journey-events.ts`) posts stage events without errors.
- **Content:** `content/drafts/` copy merged into data modules (`src/data/siteContent.ts`, `src/data/companyData.ts`) without regressions; `bun run build` exits 0.
- **Build/lint:** `bun run build` exit 0, `bun run lint` exit 0, `bun run test` exit 0.
- **No route drift:** `src/App.tsx` route list unchanged from directive §9 canonical set.

## Tech Stack
- **Framework:** Vite 5 + React 18 + TypeScript (per `docs/WEBSITE_ARCHITECTURE.md`).
- **Router:** `createBrowserRouter` in `src/App.tsx` (React Router DOM v6).
- **Styling:** Tailwind 4 + framer‑motion + lucide icons + recharts (per repo conventions).
- **Data modules:** `src/data/siteContent.ts`, `src/data/companyData.ts`, `src/data/sector-registry.ts`, `src/data/insights.ts`.
- **Resend/Email:** Existing Resend configuration for transactional/ newsletter emails (issues #277–#279).
- **Testing:** `bun` test runner with Playwright for visual QA; `vitest` unit tests where applicable.
- **Build:** `bun run build` → static output in `dist/`, deployed via Vercel edge.

## Commands (full, executable)
| Purpose | Command |
|---|---|
| Install deps (first time) | `bun install` |
| Dev server (hot‑reload) | `bun run dev` |
| Build static bundle | `bun run build` |
| Lint (ruff‑style) | `bun run lint` |
| Unit/tests | `bun test` |
| Visual QA (Playwright) | `bun run qa` |
| Type check | `bun run typecheck` |

## Project Structure (relevant sections)
```
src/
  app/               → React Router routes (App.tsx)
  components/        → Reusable UI (Header, Footer, CTA, etc.)
  data/              → SiteContent, companyData, sector-registry, insights
  pages/             → Page components (HomePage, WhatWeDoPage, etc.)
  lib/               → Shared utilities (date formatting, etc.)
  styles/            → Tailwind config, global CSS
dist/                → Production build output (generated)
tests/
  unit/              → Vitest unit tests
  e2e/               → Playwright e2e tests (visual QA, journey flows)
docs/
  SPEC_WEBSITE_ARTIFACT_ROADMAP.md → This spec
  WEBSITE_ARCHITECTURE.md → Canonical IA reference
  REPOSITORY_CLEANUP_PLAN.md → Cleanup decisions
content/drafts/      → Pending content copy (homepage, what-we-do, solutions, faq, ai-company-builder)
```

## Code Style (key conventions)
- **Naming:** camelCase for functions/variables, PascalCase for components, UPPER_SNAKE for constants/env.
- **Formatting:** `bun run lint` enforces; no `var`, use `const`/`let`; 2‑space indentation.
- **Components:** Functional components with hooks; no class components. PropTypes not used (TypeScript).
- **API calls:** `fetch` with AbortController; no `axios` unless added via `planning-and-task-breakdown` review.
- **Accessibility:** WCAG AA per §40; `onRed: #FFFFFF` for red text; contrast ratio ≥ 4.5:1 normal, ≥ 3:1 large text.
- **Images:** WebP/AV1-first; `srcset` for responsive; `loading="lazy"` below the fold; alt text required on every `<img>`.

**Example snippet (good):**
```tsx
// src/components/FeatureCard.tsx
import { Image } from 'lucide-react';

interface FeatureCardProps {
  title: string;
  description: string;
  icon: typeof Image;
  href: string;
}

export function FeatureCard({ title, description, icon, href }: FeatureCardProps) {
  return (
    <article className="p-6 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors">
      <h3 className="text-xl font-medium mb-2">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
      <a href={href} className="inline-flex items-center mt-4 text-primary">
        {/** CTA */}
        <span>Learn more</span>
        <ArrowRight className="ml-2 h-4 w-4" />
      </a>
    </article>
  );
}
```

## Testing Strategy
| Level | Framework | Location | Coverage Expectation |
|---|---|---|---|
| **Unit** | `vitest` | `tests/unit/` | < 30% overall; focus on utils, formatters, type guards |
| **Integration** | `vitest + react-testing-library` | `tests/integration/` | Key components (Header, FeatureCard, CTA) rendered with correct props |
| **Visual QA** | Playwright | `tests/e2e/visual_check.cjs` | Full‑page screenshots on each canonical route; `ls‑artifact‑qa` APPROVE gate |
| **End‑to‑End** | Playwright | `tests/e2e/journey.cjs` | Contact form submit, newsletter opt‑in, navigation between all §9 routes |
| **Performance** | Playwright Lighthouse | `tests/e2e/lighthouse.cjs` | LCP < 2.5s on 4G, CLS < 0.1, TTI < 5s |

**Test locations:**
- `tests/e2e/visual_check.cjs` — runs Playwright against `/`, `/what-we-do`, `/solutions`, `/use-cases`, `/sectors`, `/insights`, `/about`, `/contact`, `/legal/privacy`, `/legal/terms`.
- `tests/e2e/journey.cjs` — fills contact form, subscribes to newsletter, verifies stage events land in Resend inbox.
- `tests/unit/data.test.ts` — validates data module shapes (`siteContent.ts`, `companyData.ts`).

## Boundaries
| Always (no approval needed) | Ask first (HITL) | Never |
|---|---|---|
| Run `bun run lint` and `bun run build` before every commit | Database schema changes (Prisma migrations) | Commit secrets (API keys, passwords) |
| Follow naming conventions (camelCase, PascalCase) | Adding new npm dependencies (review in PR) | Edit vendor directories (`node_modules/`) |
| Write tests before marking a task complete (red‑green‑refactor) | Change CI config (`.github/workflows/`) | Remove failing tests without approval |
| Keep `src/App.tsx` route list exactly matching directive §9 | Rename or move `content/drafts/` files | Delete or comment‑out entire page components |

## Open Questions (need human input)
1. **Analytics provider:** Plausible vs Umami — which script tag and domain suffix is approved? (Cost / GDPR scope)
2. **Resend inbox setup:** Should a dedicated inbox be created for newsletter sign‑opt‑in confirmations? (Requires Resend inboxes beta enablement)
3. **Image CDN:** Use existing `public/images/` or configure Vercel image optimization? (Bandwidth cost vs simplicity)
4. **Contact form backend:** Keep existing Netlify Forms, or migrate to Resend transactional email + inbox? (Compliance impact)

## Success Criteria (final)
All of the following must pass before this spec is closed:
- [`bun run build`] exits 0 and `dist/` contains exactly the routes in §9.
- [`bun run lint`] exits 0 with zero warnings.
- Playwright visual QA `ls‑artifact‑qa` gate APPROVE on every canonical route.
- Contact form + newsletter opt‑in submits without JS error and lands a Resend inbox thread.
- No new top‑level routes added to `src/App.tsx`; deprecated routes (`/proof`, `/ask`, `/architecture`, `/build`, `/offer-*`) remain as redirects only.
- All image assets have valid alt text, WebP format, and `srcset` for responsive breakpoints.

## History
- **2026‑10‑09:** Spec written following CEO choice Option A (website artifact roadmap — in‑route artifacts only).
- **2026‑10‑09:** Research phase completed; all repo sources inspected (directive §9, venture‑studio sitemap, GitHub open issues #302–#387, content drafts, reports).
- **2026‑10‑09:** CEO confirmed Option A; research output and decision record archived.
