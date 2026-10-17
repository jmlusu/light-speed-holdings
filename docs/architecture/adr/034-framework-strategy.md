# ADR-034: Framework Strategy — No Premature SPA/Framework Rewrite

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** [ROUTE_MIGRATION_V2.md](../../ROUTE_MIGRATION_V2.md) §stack, [V2_IMPLEMENTATION_ROADMAP.md](../../V2_IMPLEMENTATION_ROADMAP.md), ADR-031, ADR-020 (migrate in place)

## Context

v2 work is route consolidation, IA, evidence, builder UX, and a public registry transform — not a platform migration. ADR-020 already ratified **migrate in place** on the repo-root Vite React SPA (no Astro revival, no new rebuild). Rewriting the router or framework mid-consolidation would multiply regression surface (redirects, a11y, tabs, modals) without a measured product reason. Heavy deps (e.g. Three.js, possibly unused `recharts`) create performance *risk* signals but are not automatic rewrite triggers.

## Decision

1. **Keep-list (v2 default stack):**
   - **Vite 6** + **React 18** + **TypeScript 5.7**
   - **Tailwind 4**
   - **react-router-dom 7** (`createBrowserRouter`)
   - Repo-root `src/` SPA; deploy via Vercel (`vercel.json` SPA rewrite + edge redirects) — canonical host per ADR-035
   - `bun` package manager as currently used in the frontend workspace

2. **No framework or SPA rewrite** in the v2 architecture program or its immediate implementation ECL. Route work is **table-driven**: `vercel.json` + `App.tsx` redirects + link repoints (ADR-031).

3. **No router migration** (e.g. to Next.js, Remix, Astro, or RR6↔RR7 hops) unless a future ADR records: concrete problem, measured constraint (perf, SEO, hosting), migration plan, and rollback — brief §23 “redesign only with reason.”

4. **Dependency weight is a risk register item, not a rewrite trigger:**
   - Audit unused/heavy deps during P3 (e.g. remove `recharts` if dead; evaluate Three.js only if builder UX actually needs WebGL — UX spec currently says **not required** for v2).
   - Performance budgets and bundle analysis may motivate dep removal or code-splitting; they do **not** authorize framework swap.

5. **Python AI OS stack unchanged** by this ADR (Typer CLI, uv, generators, orchestrator, FastAPI dashboard remain as-is per existing ADRs 001–005, 012–019, 022–024).

## Alternatives

| Option | Why not |
|--------|---------|
| Next.js / SSR migration | New hosting model, routing rewrite, contradicts ADR-020 migrate-in-place; SEO need not proven beyond static SPA + edge redirects |
| Astro marketing + React islands | Explicitly rejected in ADR-020 (no marketing-site revival) |
| Stay on React Router 6 | Already on 7; migration cost zero benefit for v2 goals |
| Rewrite because Three.js is heavy | 3D not required for v2 builder UX; optimize or drop dep first |
| Micro-frontend split | Operational complexity far exceeds current product surface |

## Rationale

- ADR-020 is binding: in-place migration on the existing SPA is the ratified target.
- Route/IA/evidence/builder work is independent of framework choice; coupling them risks never shipping consolidation.
- Rewrites during dual-front-door cleanup (ADR-035) would double deployment uncertainty.
- YAGNI: no measured constraint requires SSR, RSC, or a new meta-framework today.

## Consequences

- Roadmap P3–P4 implement against RR7 + Vite only; “framework evaluation” is not a phase.
- Bundle/dep audit is a QA/perf task inside P3/P7, with dep removal preferred over architecture change.
- If future requirements (true SSR SEO, per-route edge logic beyond redirects) appear, open a **new ADR** with evidence — do not treat Three.js weight or route count as sufficient cause.
- Stack keep-list appears in the primary v2 architecture doc so implementers do not re-litigate tools per ticket.
