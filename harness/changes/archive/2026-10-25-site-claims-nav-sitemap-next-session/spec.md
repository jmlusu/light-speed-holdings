# Spec

## Intake Review
- Intake type: Structured Change
- Input shape: plan-first (plan exists in `summary.md` and `plan.md`)
- Questions asked this round: 3 (D1, D2, D3 — recorded in `summary.md` Decisions table)

## Goal And Evidence
- **Real problem or user request:** The marketing site at `lightspeedholdings.vercel.app` is live and stable but not SPEC-complete. Four concrete gaps block "production-ready": (1) a factual error claiming "90 AI agents" instead of the canonical "89 AI agents + 1 Human CEO = 90 roles"; (2) the primary nav has 6 items vs SPEC's 8; (3) 23 pages render but are orphaned and absent from sitemap; (4) public test counts are stale (2,586 vs 2,684 collected; 17 vs 87 vitest).
- **Current behavior:** Site returns HTTP 200; `tsc` clean; 87/87 vitest tests pass; use-case detail pages fixed; Turnstile widget works. But copy contradicts registry, nav is incomplete, pages unreachable by crawlers, numbers outdated.
- **Source of evidence:** 2026-10-13 handover report (`docs/website/HANDOVER-REPORT-2026-10-13.md`); SPEC (`docs/website/SPEC.md`); live site checks (2026-10-25); local verification (`tsc`, `vitest`, `pytest --collect-only`); git history; open issues (#302, #305, #492).

## User Scenarios And Success
- **Primary user/system scenario:** A prospective client, regulator, or researcher lands on the site, reads the operating model claim, navigates via the primary menu, discovers sector/use-case evidence, and sees current verified numbers — all without hitting dead ends or contradictory statements.
- **Success criteria:**
  1. Zero occurrences of "90 AI agents", "90 agents and 1 human", "91-agent" in rendered copy (P0-1).
  2. Primary nav shows 8 items in SPEC order at desktop ≥1024 px; mobile accessible (aria-expanded, Esc, focus trap) (P0-2).
  3. `/haomtgv`, all 6 `/sectors/:slug`, all 16 `/use-cases/:slug` linked from parent pages and present in `sitemap.xml` (P0-3).
  4. Hero shows "2,684 tests collected"; `testCount` shows 87; registry `lastUpdated` = 2026-10-25 (P0-4).
  5. Guard tests prevent regression on claims, sitemap, metrics (P0-1, P0-3, P0-4).
- **Acceptance criteria:** All pre-merge checks pass (`tsc`, `vitest`, `build`); post-deploy checks pass (200, 44 sitemap URLs, browser 3-width); `lint-ecl.ps1` PASS.

## Non-Goals
- Route-specific SEO metadata (deferred to follow-up)
- Token/motif confinement (#303)
- Analytics instrumentation (#307)
- Homepage outcome-led restructure (#308)
- CTA contrast fix (#376)
- Imagery generation (#378, #387)
- Dead code removal (`PageShell.tsx`, `Header.tsx`)
- Sector source consolidation
- #305 route consolidation, §8 CTA matrix, AI-readiness route (superseded by SPEC 8-item nav decision)

## Constraints
- Branch from `origin/main` (protected, 6 required checks), NOT from `feat/deck-gate` HEAD.
- Do not silently rewrite published insight article (`insights.ts`); add correction note only.
- Nav CTA must link to `/contact` (matches `ctas.ts`), not open modal.
- CSP must start report-only; promote only after Turnstile verified on staging.
- Guard tests must be co-located with the feature they protect (`__tests__/` mirroring `src/`).

## Assumptions
- D1 = SPEC 8-item nav, D2 = nav CTA → `/contact`, D3 = "2,684 tests collected" (recorded in `summary.md`; override = edit there).
- `agent-registry.public.json` remains at 90 entries with exactly one `human-ceo` (validated by new guard test).
- `public/sitemap.xml` is the canonical sitemap (not generated at build time); manual regeneration accepted for this change.
- `vercel.json` headers are additive; no existing header removal.

## Open Questions
- None — D1/D2/D3 recorded as assumptions; override = update `summary.md` Decisions table.

## Resolved Clarifications
- **Nav target:** SPEC 8-item chosen over #305 5-item and current 6-item (routes exist, smallest diff, highest spec compliance).
- **Nav CTA behaviour:** Link to `/contact` (real URL, works without JS, matches `ctas.ts`); modal retained for hero/in-page briefing CTAs.
- **Test-count claim:** "2,684 tests collected" (verified today); switch to passing count only when CI produces green-run artifact.
- **Insight article correction:** Dated note at top, no body rewrite.
- **#305 disposition:** Superseded; add decision comment or close as "wontfix — superseded by SPEC 8-item nav".