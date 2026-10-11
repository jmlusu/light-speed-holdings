# Website Architecture

**Version:** 1.0
**Status:** ACTIVE
**Created:** 2026-10-04
**Owner:** VP Engineering / Lead Frontend

---

## Purpose

This document defines the canonical technical architecture for the LightSpeed Holdings public website. It serves as the single source of truth for all frontend engineering decisions, ensuring consistency across the implementation of the Website Transformation & Repository Consolidation Directive.

---

## Target Architecture (Directive §29)

```
apps/
  web/                    # Public LightSpeed website (this application)
    src/
      components/         # Page-specific components
      pages/              # Route-level page components
      layouts/            # Layout components (Header, Footer, PageShell)
      hooks/              # Web-app specific hooks
      lib/                # Web-app specific utilities
      styles/             # Global styles, CSS variables
      routes/             # Route configuration
    public/               # Static assets
    package.json
    vite.config.ts
    tsconfig.json

  control-plane/          # AI Company Builder / J.A.R.V.I.S. (internal)
    # Separate application - not part of public web

  athena/                 # Athena application (internal)
    # Separate application - not part of public web

packages/
  design-system/          # Canonical design system (React components, tokens, hooks)
    src/
      components/         # Reusable UI components (Button, Card, Badge, etc.)
      tokens/             # Design tokens (colors, spacing, typography, motion)
      hooks/              # Shared hooks (useTheme, useMediaQuery, etc.)
      utils/              # Shared utilities (cn, formatters, etc.)
      styles/             # Global CSS, Tailwind config
    package.json

  content-model/          # Content types & validation schemas
    src/
      schemas/            # Zod/JSON schemas for all content types
      types/              # TypeScript types derived from schemas
      validators/         # Content validation functions
    package.json

  shared-types/           # Shared TypeScript types across apps
    src/
      agent.ts
      company.ts
      governance.ts
      ...
    package.json

  agent-schema/           # Agent registry schemas & transforms
    src/
      registry.ts
      public-transform.ts
      validator.ts
    package.json

services/
  orchestrator/           # MessageBus, executor, task queue
  governance/             # Approval gates, audit, compliance
  memory/                 # 6-type memory store
  audit/                  # Audit logging, evidence collection

data/
  agents/                 # Canonical agent registry (public subset)
  solutions/              # Solutions registry
  use-cases/              # Use cases registry
  sectors/                # Sectors registry
  insights/               # Insights/Pharos registry
  claims/                 # Claims & evidence registry
  metrics/                # Platform metrics
  faqs/                   # FAQ registry
  ctas/                   # CTA registry
  governance/             # Governance registry
  media/                  # Media asset registry
  company/                # Company identity registry

docs/
  LIGHTSPEED_DESIGN_SYSTEM.md
  WEBSITE_ARCHITECTURE.md (this file)
  CONTENT_ARCHITECTURE.md
  USE_CASE_ARCHITECTURE.md
  MEDIA_ARCHITECTURE.md
  CLAIMS_GOVERNANCE.md
  REPOSITORY_CLEANUP_PLAN.md
```

---

## Current State → Target State Migration

### Current Structure (Monolithic)

```
src/
  components/           # Mixed: page-specific + site-wide + athena + effects
  pages/                # Mixed: public pages + athena pages + legacy pages
  data/                 # Mixed: canonical + legacy + generated + dashboard data
  hooks/                # Mixed: web + athena + shared
  lib/                  # Mixed: web + athena
  types/                # Mixed: all types
  brand/                # Duplicate design tokens
```

### Migration Strategy

1. **Extract Design System** → `packages/design-system/`
2. **Extract Content Model** → `packages/content-model/`
3. **Extract Shared Types** → `packages/shared-types/`
4. **Extract Agent Schema** → `packages/agent-schema/`
5. **Move Athena** → `apps/athena/`
6. **Move Control Plane** → `apps/control-plane/`
7. **Reorganize Public Web** → `apps/web/` with clean structure
8. **Create Canonical Data Registries** → `data/`

---

## Public Website Routes (Directive §9)

| Route | Page Component | Status | Notes |
|-------|----------------|--------|-------|
| `/` | `HomePage` | **REBUILD** | Per directive §17 sequence |
| `/what-we-do` | `WhatWeDoPage` | **REBUILD** | Per directive §15 |
| `/ai-company-builder` | `AiCompanyBuilderPage` | **REBUILD** | Per directive §14 |
| `/solutions` | `SolutionsPage` | **REBUILD** | Per directive §16 |
| `/use-cases` | `UseCasesPage` | **NEW** | Replaces `/proof` (directive §10) |
| `/use-cases/:slug` | `UseCaseDetailPage` | **NEW** | Detail pages per directive §11 |
| `/sectors` | `SectorsPage` | **REBUILD** | Expand to 10 sectors (directive §12) |
| `/sectors/:slug` | `SectorDetailPage` | **NEW** | Sector detail pages |
| `/insights` | `InsightsPage` | **REBUILD** | Pharos branding (directive §13) |
| `/insights/:slug` | `InsightArticlePage` | **REBUILD** | Pharos visual language |
| `/about` | `AboutPage` | **REBUILD** | New structure |
| `/contact` | `ContactPage` | **REBUILD** | With AI Assessment CTA |
| `/ai-assessment` | `AIAssessmentPage` | **NEW** | Primary CTA destination |
| `/legal/privacy` | `PrivacyPage` | **KEEP** | Update design |
| `/legal/terms` | `TermsPage` | **KEEP** | Update design |

### Removed Routes

| Route | Reason |
|-------|--------|
| `/proof` | Replaced by `/use-cases` (directive §10) |
| `/architecture` | Merged into `/ai-company-builder` |
| `/build` | Merged into `/what-we-do` |
| `/offer-b`, `/offer-c`, `/offer-e` | Merged into `/solutions` |
| `/docs`, `/cli` | Internal - not public website |

---

## Technology Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Framework | React | 18.3.1 | Current; stable |
| Build Tool | Vite | 6.1.0 | Fast HMR, optimized builds |
| Language | TypeScript | 5.7.3 | Type safety |
| Styling | Tailwind CSS | 4.0.0 | Utility-first, design token integration |
| Routing | React Router | 7.18.3 | Nested routes, data loading |
| Charts | Recharts | 3.10.1 | Data visualization |
| Icons | Lucide React | 0.475.0 | Consistent icon system |
| Testing | Vitest + React Testing Library | 5.0.0 | Fast, modern testing |
| Linting | TypeScript (tsc --noEmit) | 5.7.3 | Type-checking as lint |
| Deployment | Vercel | — | Edge network, preview deployments |

---

## Design System Integration

The public website **must** consume the canonical design system from `packages/design-system/`:

```typescript
// ✅ Correct - consume from design system
import { Button, Card, Badge, useTheme } from '@lightspeed/design-system';
import { tokens } from '@lightspeed/design-system/tokens';

// ❌ Incorrect - local duplicates
import { Button } from '@/components/ui/Button';
import { colors } from '@/styles/colors';
```

### Design Token Contract

Tokens are defined in `brand/tokens/brand-tokens.json` and `brand/tokens/brand-tokens.css` as the **single source of truth**. The design system package reads these at build time and exports them as:

- CSS custom properties (for global styles)
- JavaScript/TypeScript objects (for programmatic access)
- Tailwind CSS config (for utility classes)

---

## Component Architecture

### Page Components (`apps/web/src/pages/`)

Each page is a self-contained component that:
- Composes layout components (Header, Footer, PageShell)
- Consumes data from canonical registries (`@lightspeed/data/*`)
- Uses design system components (`@lightspeed/design-system/*`)
- Implements page-specific logic only

```tsx
// Example page structure
import { PageShell } from '@/layouts/PageShell';
import { HeroSection } from '@/components/HeroSection';
import { UseCasesSection } from '@/components/UseCasesSection';
import { solutionsRegistry } from '@lightspeed/data/solutions';

export const SolutionsPage = () => (
  <PageShell>
    <HeroSection variant="solutions" />
    <UseCasesSection solutions={solutionsRegistry} />
    {/* ... */}
  </PageShell>
);
```

### Layout Components (`apps/web/src/layouts/`)

| Component | Purpose |
|-----------|---------|
| `PageShell` | Root layout: Header + main + Footer |
| `Header` | Global navigation, logo, primary CTAs |
| `Footer` | Global footer, links, legal, social |
| `PageContainer` | Max-width wrapper, padding, background |

### Page-Specific Components (`apps/web/src/components/`)

Organized by page/feature:
```
components/
  home/           # Homepage sections
  ai-company-builder/  # AI Company Builder sections
  what-we-do/     # What We Do sections
  solutions/      # Solutions sections
  use-cases/      # Use Cases sections (explorer, cards, detail)
  sectors/        # Sectors sections
  insights/       # Insights/Pharos sections
  about/          # About sections
  contact/        # Contact/Assessment sections
  shared/         # Truly shared components (used across 3+ pages)
```

---

## Data Flow

```
Canonical Source (YAML/JSON in data/)
       ↓
   Build-time / Dev-time
       ↓
TypeScript Registry Modules (data/*.ts)
       ↓
   Imported by Page Components
       ↓
Design System Components (render)
       ↓
   Browser
```

### Registry Pattern

Each registry follows this pattern:

```typescript
// data/use-cases/index.ts
import { useCases } from './registry.json';
import type { UseCase } from '@lightspeed/content-model/schemas';

export const useCasesRegistry: UseCase[] = useCases as UseCase[];

export function getUseCaseBySlug(slug: string): UseCase | undefined {
  return useCasesRegistry.find(uc => uc.slug === slug);
}

export function getUseCasesBySector(sectorId: string): UseCase[] {
  return useCasesRegistry.filter(uc => uc.sectors.includes(sectorId));
}

export function getUseCasesByStatus(status: UseCaseStatus): UseCase[] {
  return useCasesRegistry.filter(uc => uc.status === status);
}
```

---

## State Management

| Scope | Solution |
|-------|----------|
| Global UI state (theme, nav open) | React Context (`SiteContext`) |
| Server state (if any) | React Query / SWR (future) |
| Form state | React Hook Form + Zod |
| URL state | React Router search params |

**No Redux, Zustand, or complex state libraries.** The public website is primarily static content with minimal interactivity.

---

## Performance Strategy (Directive §30)

| Technique | Implementation |
|-----------|----------------|
| Fast initial load | Vite code splitting, preload critical CSS |
| Optimized images | WebP/AVIF, responsive images, lazy loading |
| Lazy-loaded media | IntersectionObserver for below-fold images/video |
| Minimal JS | No heavy frameworks; CSS/SVG for diagrams |
| Progressive enhancement | Core content works without JS |
| Mobile-first | Mobile styles first; desktop enhancements via media queries |
| Caching | Vercel edge caching, immutable asset hashes |

### Bundle Budget

| Metric | Target |
|--------|--------|
| Initial JS (gzipped) | < 100 KB |
| Initial CSS (gzipped) | < 30 KB |
| LCP (4G) | < 2.5s |
| CLS | < 0.1 |
| TBT | < 200ms |

---

## Accessibility (Directive §32)

| Requirement | Implementation |
|-------------|----------------|
| Keyboard navigation | All interactive elements focusable, logical tab order |
| Visible focus | Design system focus ring (cyan on dark, navy on light) |
| Semantic headings | h1-h6 hierarchy enforced in components |
| Sufficient contrast | Design system tokens meet WCAG AA |
| Alt text | Required prop on all image components |
| Reduced motion | `prefers-reduced-motion` respected in motion system |
| Accessible dialogs | Focus trap, ARIA roles, escape to close |
| Accessible forms | Labels, error announcements, validation |
| No color-only information | Icons + text for status badges |
| Screen-reader status | Live regions for dynamic content |

---

## Responsive Breakpoints (Directive §33)

| Breakpoint | Width | Use Case |
|------------|-------|----------|
| `mobile` | < 640px | Phone portrait |
| `tablet` | 640px - 1023px | Phone landscape, tablet portrait |
| `laptop` | 1024px - 1279px | Tablet landscape, small laptop |
| `desktop` | 1280px - 1535px | Standard desktop |
| `large-desktop` | ≥ 1536px | Large monitors |

**Mobile-first methodology:** Base styles target mobile; enhancements added at each breakpoint.

---

## SEO Implementation (Directive §31)

Every public page must include:

```tsx
// In page component or layout
<Helmet>
  <title>{pageTitle} | LightSpeed Holdings</title>
  <meta name="description" content={pageDescription} />
  <link rel="canonical" href={canonicalUrl} />
  <meta property="og:title" content={ogTitle} />
  <meta property="og:description" content={ogDescription} />
  <meta property="og:image" content={ogImageUrl} />
  <meta property="og:type" content="website" />
  <meta name="twitter:card" content="summary_large_image" />
  {/* Structured data (JSON-LD) per page type */}
</Helmet>
```

### Structured Data Types

| Page | Schema.org Type |
|------|-----------------|
| Home | `WebSite`, `Organization` |
| Solutions | `Service`, `Product` |
| Use Cases | `CaseStudy`, `CreativeWork` |
| Sectors | `IndustryClassification` |
| Insights | `Article`, `BlogPosting` |
| About | `Organization`, `AboutPage` |
| Contact | `ContactPage` |

---

## Security Considerations (Directive §28)

**Never expose in public website:**

- Secrets / API keys
- Internal credentials
- Internal memory / audit data
- Private client data
- Internal prompts
- Private operational logs
- Internal agent configurations (full registry)

**Public-safe data only:**

- Canonical agent count (90 roles: 89 AI + 1 Human CEO)
- Department names (20 departments)
- Public agent registry (subset: name, title, department, mission)
- Solutions, use cases, sectors, insights (published content)
- Governance framework (public description)
- Company identity, leadership (public)

---

## Build & Deployment

### Development

```bash
# From repository root
cd apps/web
npm run dev          # Start dev server
npm run build        # Type-check + production build
npm run preview      # Preview production build
npm run test         # Run tests
npm run lint         # Type-check only
```

### CI/CD Pipeline

```yaml
# .github/workflows/web-ci.yml
jobs:
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: cd apps/web && pnpm install --frozen-lockfile
      - run: cd apps/web && pnpm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: cd apps/web && pnpm install --frozen-lockfile
      - run: cd apps/web && pnpm run test

  build:
    needs: [typecheck, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: cd apps/web && pnpm install --frozen-lockfile
      - run: cd apps/web && pnpm run build
      - uses: actions/upload-artifact@v4
        with:
          name: web-dist
          path: apps/web/dist

  deploy-preview:
    needs: build
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: web-dist
          path: apps/web/dist
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: apps/web
```

### Production Deployment

- **Platform:** Vercel (connected to `main` branch)
- **Domain:** `lightspeedholdings.vercel.app`
- **Environment variables:** Managed in Vercel dashboard (never in repo)
- **Preview deployments:** Automatic for every PR

---

## Monitoring & Observability

| Metric | Tool | Implementation |
|--------|------|----------------|
| Core Web Vitals | Vercel Analytics + Web Vitals library | Automatic |
| Error tracking | Sentry (future) | DSN in env |
| Uptime | Vercel / Pingdom | Automatic |
| Build health | GitHub Actions | Workflow status |

---

## Migration Checklist

- [ ] Create `packages/design-system/` with canonical components
- [ ] Create `packages/content-model/` with schemas
- [ ] Create `packages/shared-types/` with shared types
- [ ] Create `packages/agent-schema/` with registry transforms
- [ ] Move Athena to `apps/athena/`
- [ ] Move Control Plane to `apps/control-plane/`
- [ ] Restructure `apps/web/` per target architecture
- [ ] Create canonical data registries in `data/`
- [ ] Update all imports to use package aliases
- [ ] Configure Vite/Tailwind for monorepo
- [ ] Update CI/CD for new structure
- [ ] Verify all routes work
- [ ] Run full QA per directive §37

---

*This document is living. Update as architecture evolves during implementation.*
