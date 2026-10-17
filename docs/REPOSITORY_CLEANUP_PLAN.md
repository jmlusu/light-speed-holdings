# Repository Cleanup Plan

**Version:** 1.0
**Status:** ACTIVE
**Created:** 2026-10-04
**Owner:** LightSpeed Holdings Engineering

---

## Purpose

This document classifies every major artifact in the LightSpeed repository and defines its fate: **KEEP**, **REFACTOR**, **DEPRECATE**, **MOVE**, or **DELETE**. This is the single source of truth for repository hygiene during the Website Transformation & Repository Consolidation initiative.

---

## Classification Criteria

| Classification | Criteria | Action |
|----------------|----------|--------|
| **KEEP** | Production-critical, actively maintained, no duplication | Preserve as-is |
| **REFACTOR** | Working but needs architectural alignment, duplication removal, or modernization | Update in place |
| **DEPRECATE** | Superseded by newer implementation, retained for reference/migration | Mark deprecated, add migration path |
| **MOVE** | Belongs in different location per target architecture (apps/, packages/, services/, data/) | Relocate with updated imports |
| **DELETE** | Dead code, stale artifacts, security risks, or explicitly superseded | Remove after verification |

---

## Audit Results

### 1. Root-Level Artifacts

| Path | Purpose | Classification | Replacement | Migration Action | Risk | Owner |
|------|---------|----------------|-------------|------------------|------|-------|
| `company-registry.yaml` | Canonical agent registry (90 roles) | **KEEP** | — | — | Low | Registry Owner |
| `package.json` | Web app dependencies & scripts | **KEEP** | — | — | Low | Platform Engineer |
| `tsconfig.json` | TypeScript config | **KEEP** | — | — | Low | Platform Engineer |
| `vite.config.ts` | Vite build config | **KEEP** | — | — | Low | Platform Engineer |
| `tailwind.config.ts` | Tailwind config (if exists) | **REFACTOR** | Unified design system tokens | Migrate to `packages/design-system` | Medium | Design System Owner |
| `.env*` | Environment files | **KEEP** (gitignored) | — | — | Low | DevOps Lead |
| `CHANGELOG.md` | Release history | **KEEP** | — | — | Low | Release Manager |
| `AGENTS.md` | Agent orchestration guide | **KEEP** | — | — | Low | Chief of Staff |
| `WEBSITE TRANSFORMATION & REPOSITORY CONSOLIDATION DIRECTIVE.md` | This initiative's directive | **KEEP** | — | — | Low | CEO |
| `_temp_brief.txt`, `_linkedin-article-body.txt`, `_carousel-concepts.txt` | Temporary content drafts | **DELETE** | — | Remove after content migration | Low | Content Creator |
| `debug_analysis.py`, `check_correlation.py`, `check_audit_db.py` | Debug scripts | **DELETE** | — | Remove; use `scripts/` instead | Low | DevOps Lead |
| `Clean-LSMEM.ps1` | Cleanup script | **MOVE** → `scripts/` | — | Relocate | Low | DevOps Lead |
| `Branding landing page/` | Legacy branding assets | **DEPRECATE** | `brand/`, `public/brand/` | Archive to `archive/branding-landing-page/` | Low | Creative Director |

---

### 2. Source Code (`src/`)

#### 2.1 AI Company Builder Backend (`src/ai_company/`)

| Path | Purpose | Classification | Replacement | Migration Action | Risk | Owner |
|------|---------|----------------|-------------|------------------|------|-------|
| `src/ai_company/` (entire) | Core backend: registry, orchestrator, memory, LLM, security, workflows | **KEEP** | — | Preserve; establish clean boundary from public web | Medium | CTO / VP Engineering |
| `src/ai_company/cli/` | CLI entry point (Typer) | **KEEP** | — | — | Low | VP Engineering |
| `src/ai_company/generator.py` | Agent markdown generator | **KEEP** | — | — | Low | Registry Owner |
| `src/ai_company/models/` | Pydantic models (Executive, Specialist, Department, Company) | **KEEP** | — | — | Low | VP Engineering |
| `src/ai_company/orchestrator/` | MessageBus, approval, escalation, scheduler | **KEEP** | — | — | Low | Orchestration Owner |
| `src/ai_company/registry/` | Registry loader, parser, resolver, validator | **KEEP** | — | — | Low | Registry Owner |
| `src/ai_company/memory/` | 6-type memory store | **KEEP** | — | — | Low | Memory Owner |
| `src/ai_company/llm/` | Multi-provider LLM client, cost tracker, circuit breaker | **KEEP** | — | — | Low | LLM Platform Owner |
| `src/ai_company/security/` | RBAC, encryption, PII detection | **KEEP** | — | — | Low | CISO |
| `src/ai_company/workflow/` | Workflow engine (9 definitions) | **KEEP** | — | — | Low | Workflow Owner |
| `src/ai_company/services/` | Client intake, onboarding, sales | **KEEP** | — | — | Low | Sales Owner / Customer Success Owner |
| `src/ai_company/publishing/` | Formats, publishers, queue | **KEEP** | — | — | Low | Publishing Owner |
| `src/ai_company/store/` | File store, file lock, report store | **KEEP** | — | — | Low | Platform Reliability Engineer |
| `src/ai_company/telemetry/` | Tracing, exporter, bridge | **KEEP** | — | — | Low | Observability Owner |
| `src/ai_company/reliability/` | Circuit breaker, timeout, config | **KEEP** | — | — | Low | Platform Reliability Engineer |
| `src/ai_company/mcp/` | MCP server | **KEEP** | — | — | Low | Integration Engineer |
| `src/ai_company/media/` | ComfyUI client, transcription | **KEEP** | — | — | Low | Media Generation Owner |

#### 2.2 Public Website (`src/components/`, `src/pages/`, `src/data/`, `src/hooks/`, `src/lib/`)

| Path | Purpose | Classification | Replacement | Migration Action | Risk | Owner |
|------|---------|----------------|-------------|------------------|------|-------|
| `src/components/home/` | Homepage sections (Hero, OperatingModel, AICompanyBuilder, Workforce, Solutions, Sectors, **Proof**, Insights, About, Briefing, VisitorPaths) | **REFACTOR** | New canonical components per directive | Replace `ProofSection` → `UseCasesSection`; update all sections to new IA | High | Lead Frontend |
| `src/components/site/` | Site-wide components (CtaBand, FaqSection, HonestyBadge, Logo, PageIntro, RelatedLinks, SectionHeading) | **REFACTOR** | Unified design system components | Migrate to `packages/design-system/src/components/` | Medium | Design System Owner |
| `src/components/athena/` | Athena-specific components | **MOVE** | `apps/athena/src/components/` | Relocate with Athena app | Low | Athena Owner |
| `src/components/effects/` | Visual effects (HeroMist) | **REFACTOR** | New motion system | Update to new motion principles | Medium | Creative Director |
| `src/components/WhatWeDoPage.tsx` | **DELETE** (duplicate) | — | `src/pages/WhatWeDoPage.tsx` | Remove duplicate | Low | Lead Frontend |
| `src/components/AiCompanyBuilderSection.tsx` | **DELETE** (duplicate) | — | `src/components/home/AICompanyBuilderSection.tsx` | Remove duplicate | Low | Lead Frontend |
| `src/components/AboutSection.tsx` | **DELETE** (duplicate) | — | `src/components/home/AboutSection.tsx` | Remove duplicate | Low | Lead Frontend |
| `src/components/AskLightSpeed.tsx` | Ask LightSpeed component | **REFACTOR** | New CTA system | Integrate with new CTA registry | Medium | Lead Frontend |
| `src/components/ContactSection.tsx` | **DELETE** (duplicate) | — | `src/pages/ContactPage.tsx` | Remove duplicate | Low | Lead Frontend |
| `src/components/ExecutiveBriefingModal.tsx` | **REFACTOR** | New briefing modal | Update to new CTA/briefing flow | Medium | Lead Frontend |
| `src/components/FeatureCard.tsx`, `FeatureGrid.tsx` | Generic feature components | **REFACTOR** | Design system components | Move to design system | Medium | Design System Owner |
| `src/components/FloatingNav.tsx` | Floating navigation | **REFACTOR** | New global shell | Replace with new header/nav | Medium | Lead Frontend |
| `src/components/Hero.tsx` | **DELETE** (legacy) | — | `src/components/HeroSection.tsx` | Remove legacy Hero | Low | Lead Frontend |
| `src/components/HeroSection.tsx` | Current hero section | **REFACTOR** | New hero per directive | Update to new homepage sequence | High | Creative Director |
| `src/components/KPIBand.tsx` | KPI display band | **REFACTOR** | New metrics display | Update to canonical metrics | Medium | Lead Frontend |
| `src/components/LeadershipStrip.tsx` | Leadership display | **REFACTOR** | New About page | Update to new leadership imagery | Medium | Creative Director |
| `src/components/NewsletterSignup.tsx` | Newsletter signup | **DEPRECATE** | New CTA system | Replace with contextual CTAs | Low | Marketing Owner |
| `src/components/Playground.tsx` | Interactive playground | **DEPRECATE** | Remove or move to Athena | Archive | Low | Creative Director |
| `src/components/PublicAgentRegistry.tsx` | Public agent registry display | **REFACTOR** | New AI Company Builder page | Integrate into new page | Medium | Lead Frontend |
| `src/components/Reveal.tsx` | Scroll reveal animation | **REFACTOR** | New motion system | Update to `prefers-reduced-motion` respect | Medium | Creative Director |
| `src/components/SiteFooter.tsx` | Site footer | **REFACTOR** | New global footer | Update to new footer design | Medium | Lead Frontend |
| `src/components/SiteLayout.tsx` | Page layout wrapper | **REFACTOR** | New global shell | Update to new layout | High | Lead Frontend |
| `src/components/TrustStrip.tsx` | Trust indicators | **REFACTOR** | New trust band | Update to new trust evidence | Medium | Lead Frontend |
| `src/pages/Index.tsx` | **DELETE** (legacy entry) | — | `src/main.tsx` + `src/App.tsx` | Remove legacy index | Low | Lead Frontend |
| `src/pages/HomePage.tsx` | Current homepage | **REFACTOR** | New homepage per directive §17 | Complete rebuild per sequence | High | Creative Director |
| `src/pages/WhatWeDoPage.tsx` | What We Do page | **REFACTOR** | New page per directive §15 | Rebuild per engagement model | High | Lead Frontend |
| `src/pages/AiCompanyBuilderPage.tsx` | AI Company Builder page | **REFACTOR** | New page per directive §14 | Rebuild per product tour structure | High | Lead Frontend |
| `src/pages/SolutionsPage.tsx` | Solutions page | **REFACTOR** | New page per directive §16 | Rebuild per solution families | High | Lead Frontend |
| `src/pages/SectorsPage.tsx` | Sectors page | **REFACTOR** | New page per directive §12 | Expand to 10 sectors | High | Lead Frontend |
| `src/pages/ProofPage.tsx` | **DELETE** (Proof → Use Cases) | `src/pages/UseCasesPage.tsx` | Create new Use Cases page; remove ProofPage | High | Lead Frontend |
| `src/pages/InsightsPage.tsx` | Insights listing | **REFACTOR** | New page per directive §13 | Update to Pharos branding | Medium | Thought Leadership Lead |
| `src/pages/InsightArticlePage.tsx` | Individual insight article | **REFACTOR** | New article template | Update to Pharos visual language | Medium | Thought Leadership Lead |
| `src/pages/AboutPage.tsx` | About page | **REFACTOR** | New page per directive | Update to new About structure | Medium | Lead Frontend |
| `src/pages/ContactPage.tsx` | Contact page | **REFACTOR** | New page with AI Assessment CTA | Update form and CTAs | Medium | Lead Frontend |
| `src/pages/Architecture.tsx` | **DELETE** (legacy) | — | `src/pages/AiCompanyBuilderPage.tsx` | Remove; content moves to AI Company Builder | Low | Lead Frontend |
| `src/pages/Build.tsx` | **DELETE** (legacy) | — | `src/pages/WhatWeDoPage.tsx` | Remove; content moves to What We Do | Low | Lead Frontend |
| `src/pages/OfferB.tsx`, `OfferC.tsx`, `OfferE.tsx` | **DEPRECATE** | `src/pages/SolutionsPage.tsx` | Migrate content to Solutions; remove legacy offer pages | Medium | Lead Frontend |
| `src/pages/PrivacyPage.tsx`, `TermsPage.tsx` | Legal pages | **KEEP** | — | Update to new design system | Low | Legal Owner |
| `src/pages/athena/` | Athena app pages | **MOVE** | `apps/athena/src/pages/` | Relocate with Athena app | Low | Athena Owner |
| `src/data/siteContent.ts` | Canonical site content (solutions, proof, governance, case studies) | **REFACTOR** | New content architecture | Split into canonical registries per directive §22 | High | Content Architect |
| `src/data/useCaseCatalogData.ts` | Legacy catalog (offers, industries, scenarios, proof points) | **DEPRECATE** | New use-case & sector registries | Migrate to `data/use-cases/`, `data/sectors/`, `data/solutions/` | High | Content Architect |
| `src/data/sector-registry.ts` | Current sector registry (5 sectors) | **REFACTOR** | Expanded 10-sector registry | Expand per directive §12 | High | Content Architect |
| `src/data/sectors.ts` | Legacy sector data | **DEPRECATE** | `src/data/sector-registry.ts` | Consolidate | Medium | Content Architect |
| `src/data/capabilities.ts` | Capability titles | **REFACTOR** | New capabilities registry | Move to `data/capabilities/` | Medium | Content Architect |
| `src/data/companyData.ts` | Dashboard company data (agents, tasks, approvals) | **KEEP** | — | Internal dashboard only; not public | Low | Dashboard Owner |
| `src/data/metrics.ts` | Live metrics (test count, agent count) | **REFACTOR** | Canonical metrics registry | Move to `data/metrics/` | Medium | Dashboard Owner |
| `src/data/faqs.ts` | FAQ data | **REFACTOR** | Canonical FAQ registry | Expand per directive §18 | Medium | Content Architect |
| `src/data/ctas.ts` | CTA definitions | **REFACTOR** | Canonical CTA registry | Canonicalize per directive §34 | Medium | Content Architect |
| `src/data/governance.ts` | Governance data | **REFACTOR** | Canonical governance registry | Move to `data/governance/` | Medium | Content Architect |
| `src/data/insights.ts` | Insights data | **REFACTOR** | Canonical insights registry | Move to `data/insights/` | Medium | Thought Leadership Lead |
| `src/data/leadership.ts` | Leadership data | **REFACTOR** | Canonical leadership registry | Move to `data/leadership/` | Medium | Content Architect |
| `src/data/publicAgentRegistry.ts` | Public agent registry | **REFACTOR** | Canonical agent registry | Move to `data/agents/` | Medium | Registry Owner |
| `src/data/generated/agent-registry.public.json` | Generated public agent registry | **KEEP** | — | Generated artifact; update generator | Low | Registry Owner |
| `src/hooks/` | Custom React hooks | **REFACTOR** | Design system hooks | Move to `packages/design-system/src/hooks/` | Medium | Design System Owner |
| `src/lib/enquiry.ts` | Enquiry form logic | **REFACTOR** | New contact/assessment flow | Update to new CTA system | Medium | Lead Frontend |
| `src/lib/validation.ts` | Form validation | **REFACTOR** | Design system validation | Move to `packages/design-system/src/lib/` | Medium | Design System Owner |
| `src/lib/athena/` | Athena library code | **MOVE** | `apps/athena/src/lib/` | Relocate with Athena app | Low | Athena Owner |
| `src/site-context.tsx` | Site context provider | **REFACTOR** | New theme/context system | Update to design system tokens | Medium | Design System Owner |
| `src/types/` | TypeScript types | **REFACTOR** | Shared types package | Move to `packages/shared-types/` | Medium | VP Engineering |

---

### 3. Public Assets (`public/`)

| Path | Purpose | Classification | Replacement | Migration Action | Risk | Owner |
|------|---------|----------------|-------------|------------------|------|-------|
| `public/brand/` | Brand guidelines, logos, tokens | **REFACTOR** | Unified brand system | Consolidate with `brand/`; single source of truth | Medium | Creative Director |
| `public/logos/` | Partner logos, Malawi gov, SADC | **KEEP** | — | — | Low | Creative Director |
| `public/assets/` | Catalog, diagrams, illustrations, insights, metrics, sectors, screenshots | **REFACTOR** | New media architecture | Reorganize per `MEDIA_ARCHITECTURE.md` | High | Creative Director |
| `public/favicon.svg`, `logo-full.svg`, `logo-icon.svg` | Legacy logo files | **DEPRECATE** | New logo system | Replace with new canonical logo | Medium | Creative Director |

---

### 4. Brand Assets (`brand/`)

| Path | Purpose | Classification | Replacement | Migration Action | Risk | Owner |
|------|---------|----------------|-------------|------------------|------|-------|
| `brand/tokens/` | Brand tokens (JSON, CSS) | **KEEP** | — | Canonical token source; sync to `src/brand/` | Low | Design System Owner |
| `brand/README.md` | Brand documentation | **REFACTOR** | `docs/LIGHTSPEED_DESIGN_SYSTEM.md` | Consolidate into design system doc | Low | Creative Director |
| `brand/print/` | Letterhead, business cards | **KEEP** | — | — | Low | Creative Director |
| `brand/guidelines/` | Brand guidelines | **REFACTOR** | `docs/LIGHTSPEED_DESIGN_SYSTEM.md` | Consolidate | Low | Creative Director |

---

### 5. Configuration & Infrastructure

| Path | Purpose | Classification | Replacement | Migration Action | Risk | Owner |
|------|---------|----------------|-------------|------------------|------|-------|
| `.github/workflows/` | CI/CD workflows | **REFACTOR** | Updated for new architecture | Add build gates for new structure | Medium | DevOps Lead |
| `docker-compose.staging.yml` | Staging environment | **KEEP** | — | Update for new app structure | Low | DevOps Lead |
| `scripts/` | Utility scripts | **REFACTOR** | Organized script library | Add Phase 0-7 automation scripts | Medium | DevOps Lead |
| `docs/` | Documentation | **REFACTOR** | New canonical docs | Add 6 new canonical docs (Phase 0) | Medium | Technical Documentation Lead |
| `templates/agents/` | Agent markdown templates | **KEEP** | — | — | Low | Registry Owner |
| `harness/` | ECL harness infrastructure | **KEEP** | — | — | Low | ECL Harness Engineer |
| `data/` | Data catalog, schemas, SQLite DB | **KEEP** | — | — | Low | Data Engineer |
| `orchestrator/` | Orchestrator runtime | **KEEP** | — | — | Low | Orchestration Owner |
| `dashboard/` | Dashboard application | **MOVE** | `apps/control-plane/` | Relocate per target architecture | Medium | Dashboard Owner |
| `api/` | API layer | **MOVE** | `services/` or `apps/control-plane/` | Relocate per target architecture | Medium | VP Engineering |
| `config/` | Configuration files | **REFACTOR** | Centralized config | Consolidate | Low | Platform Engineer |
| `models/` | Model files | **KEEP** | — | — | Low | ML Engineer |
| `evals/` | Evaluation scripts | **KEEP** | — | — | Low | Test Engineering Lead |
| `tests/` | Test suite | **REFACTOR** | Updated for new structure | Add website-specific tests | Medium | Test Engineering Lead |
| `workflows/` | Workflow definitions/instances | **KEEP** | — | — | Low | Workflow Owner |
| `archive/` | Archived content | **KEEP** | — | Add deprecated items here | Low | Content Creator |
| `backups/` | Backup scripts/output | **KEEP** | — | — | Low | DevOps Lead |
| `reports/` | Audit reports | **KEEP** | — | — | Low | Audit Owner |
| `results/` | Test/run results | **KEEP** | — | — | Low | Test Engineering Lead |
| `output/` | Generated output | **KEEP** | — | — | Low | DevOps Lead |
| `tmp/`, `.pytest_tmp*/` | Temporary files | **DELETE** | — | Clean up; add to `.gitignore` | Low | DevOps Lead |
| `node_modules/`, `.venv/`, `dist/`, `build/` | Build artifacts | **DELETE** (gitignored) | — | Ensure in `.gitignore` | Low | DevOps Lead |

---

### 6. Duplicate/Conflicting Design Systems

| Path | Purpose | Classification | Replacement | Migration Action | Risk | Owner |
|------|---------|----------------|-------------|------------------|------|-------|
| `src/brand/design-decisions.md` | Design decisions | **DEPRECATED (done 2026-10-05)** | `docs/LIGHTSPEED_DESIGN_SYSTEM.md` | Archived to `.archive/design-system/hardware-console-legacy-palette.md`; superseded stub left in place | Low | Design System Owner |
| `src/brand/brand-tokens.css` | Duplicate tokens | **DEPRECATE** | `brand/tokens/brand-tokens.css` | Remove duplicate | Low | Design System Owner |
| `public/brand/tokens/` | Duplicate tokens | **DEPRECATE** | `brand/tokens/` | Remove duplicate | Low | Design System Owner |
| `static/brand/` | Mirror of brand assets | **DEPRECATE** | `brand/` | Remove mirror | Low | Creative Director |

---

### 7. Legacy Website Artifacts (Directive §26)

| Artifact | Current Location | Classification | Migration Action |
|----------|------------------|----------------|------------------|
| ProofPage | `src/pages/ProofPage.tsx` | **DELETE** | Replace with UseCasesPage |
| ProofSection | `src/components/home/ProofSection.tsx` | **DELETE** | Replace with UseCasesSection |
| Architecture page | `src/pages/Architecture.tsx` | **DELETE** | Merge into AI Company Builder |
| Build page | `src/pages/Build.tsx` | **DELETE** | Merge into What We Do |
| OfferB, OfferC, OfferE pages | `src/pages/Offer*.tsx` | **DEPRECATE** | Migrate to Solutions page |
| Duplicate Home components | `src/components/` root | **DELETE** | Remove duplicates |
| Duplicate Hero components | `src/components/Hero.tsx` | **DELETE** | Remove legacy Hero |
| Duplicate design tokens | Multiple locations | **DEPRECATE** | Single source: `brand/tokens/` |
| Legacy catalogs | `src/data/useCaseCatalogData.ts` | **DEPRECATE** | Migrate to new registries |
| Obsolete marketing copy | Scattered in components | **DELETE** | Replace with canonical content |
| "Proof" terminology | Throughout codebase | **REFACTOR** | Replace with "Use Cases" / "Evidence" |
| Stale agent counts (127, 143, 144, 152) | Multiple files | **REFACTOR** | Canonicalize to 90 (89 AI + 1 Human CEO) |
| Obsolete UI concepts | Various components | **DELETE** | Remove unused components |

---

### 8. Athena Application (Directive §27)

| Path | Purpose | Classification | Replacement | Migration Action | Risk | Owner |
|------|---------|----------------|-------------|------------------|------|-------|
| `src/components/athena/` | Athena UI components | **MOVE** | `apps/athena/src/components/` | Full relocation | Low | Athena Owner |
| `src/pages/athena/` | Athena pages | **MOVE** | `apps/athena/src/pages/` | Full relocation | Low | Athena Owner |
| `src/lib/athena/` | Athena library | **MOVE** | `apps/athena/src/lib/` | Full relocation | Low | Athena Owner |
| `src/routes/athena/` (if exists) | Athena routing | **MOVE** | `apps/athena/src/routes/` | Full relocation | Low | Athena Owner |

---

### 9. Internal Dashboards & Control Plane (Directive §28)

| Path | Purpose | Classification | Replacement | Migration Action | Risk | Owner |
|------|---------|----------------|-------------|------------------|------|-------|
| `dashboard/` | Internal dashboard app | **MOVE** | `apps/control-plane/` | Full relocation | Medium | Dashboard Owner |
| `api/` | Internal API | **MOVE** | `services/` or `apps/control-plane/` | Relocate | Medium | VP Engineering |
| `orchestrator/` | Orchestrator runtime | **KEEP** | — | Preserve as service | Low | Orchestration Owner |

---

## Migration Priority Order

1. **Phase 0 Docs** — Create 6 canonical documentation files (this plan + 5 others)
2. **Design System** — Establish `packages/design-system/` as single source
3. **Content Architecture** — Create canonical registries in `data/`
4. **Global Shell** — Header, nav, footer, theme, CTA system
5. **Page Implementation** — Home, AI Company Builder, What We Do, Solutions, Use Cases, Sectors, Insights, About, FAQ, Contact, Assessment
6. **Athena Separation** — Move to `apps/athena/`
7. **Control Plane Separation** — Move dashboard to `apps/control-plane/`
8. **Cleanup** — Remove deprecated/deleted items
9. **QA** — Full route verification per directive §37

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking existing backend functionality | Backend (`src/ai_company/`) is **KEEP**; only public website refactored |
| Losing canonical data during migration | All canonical data sources preserved; only presentation layer changes |
| Duplicate content during transition | Single-source registries created first; pages consume from registries |
| Design system inconsistency | `LIGHTSPEED_DESIGN_SYSTEM.md` + `brand/tokens/` established before page work |
| SEO regression | Canonical URLs maintained; structured data added per §31 |
| Accessibility regression | WCAG requirements in design system; automated testing in CI |

---

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| CEO | Jack Mlusu | | |
| CTO | | | |
| VP Engineering | | | |
| Creative Director | | | |
| Lead Frontend | | | |
| Content Architect | | | |
| Design System Owner | | | |
| DevOps Lead | | | |

---

*This document is living. Update as classifications change during implementation.*
