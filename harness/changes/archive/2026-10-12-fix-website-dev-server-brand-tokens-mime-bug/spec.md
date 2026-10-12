# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first (user instruction "Proceed to fix the Pre-existing bug found" 2026-10-12; "Continue if you have next steps" reaffirmed)
- Questions asked this round: 0 (mechanism fully diagnosed in-session before intake)

## Goal And Evidence

- Real problem or user request: `npm run dev` (port 1441) fails to mount React — browser console shows `Expected a JavaScript-or-Wasm module script but the server responded with a MIME type of "text/css"` for `/brand/tokens/brand-tokens.css`.
- Current behavior: 15 TSX files do `import '../../brand/tokens/brand-tokens.css'`. Vite resolves the specifier by URL; the served response comes from `public/brand/tokens/brand-tokens.css` (public-dir middleware serves raw `text/css`), so the browser rejects the module import, the JS graph fails, and no component ever renders in dev. Production build is unaffected (rollup resolves by fs path).
- Source of evidence: dev console MIME error; Vite public-dir shadowing behavior; grep showing 15 TSX imports + surviving global load at `src/index.css:2` (`@import "../brand/tokens/brand-tokens.css"`) wired through `main.tsx`; `scripts/build/sync-brand.ps1` mirrors `brand/**` into `public/brand` (CI `-Verify` requires both mirrors).

## User Scenarios And Success

- Primary user/system scenario: any developer or agent runs `npm run dev` and loads the SPA — React must mount with full brand tokens applied; `npm run preview` (1440) and production must be unchanged.
- Success criteria: (1) dev server on 1441 mounts React, zero module/MIME errors in console; (2) brand tokens still applied globally (single load via `src/index.css`); (3) `npm run lint`, `npm run test`, `npm run build` green; (4) Playwright nav/modal suite (19 checks) green on both 1441 (dev) and 1440 (preview); (5) `sync-brand.ps1 -Verify` still green (mirrors untouched); (6) stale docs no longer recommend the broken per-component import pattern.
- Acceptance criteria: same as success criteria; ECL closed with `validation_status: pass`.

## Non-Goals

- Deleting or relocating `public/brand/tokens/brand-tokens.css` (would fail `sync-brand.ps1 -Verify` and break the documented mirror invariant).
- Changing `vite.config.ts` (`publicDir`, plugins, middleware).
- Changing `scripts/build/sync-brand.ps1` or the mirror layout (`brand/` → `static/brand/` + `public/brand/`).
- Changing `/proof` route behavior (intentional redirect to `/use-cases`, Directive §10).
- Any Python/CLI, dashboard, or registry changes.

## Constraints

- Canonical token load must survive exactly once: `src/index.css` `@import "../brand/tokens/brand-tokens.css"` (loaded via `main.tsx`).
- Mirror invariant: `brand/**`, `static/brand/**`, `public/brand/**` stay in sync; pre-commit/CI `-Verify` must pass.
- Canonical tool vocabulary and repo conventions (AGENTS.md §8); no new dependencies.
- ECL one-active-max; this change owns the slot until closed.

## Assumptions

- Every rendered route enters through `main.tsx` → `src/index.css`, so the global `@import` covers all pages/components (verified: `index.html` → `main.tsx` → `index.css`).
- The 15 per-component imports are exact duplicates of the global load (same canonical file), so removal is behavior-preserving in dev and prod.

## Open Questions

- None.

## Resolved Clarifications

- Fix approach: remove the 15 redundant per-component imports rather than touching mirrors/vite config (agent-determined within user-approved fix mandate; options and rejections recorded in summary Decisions).
- Docs updated in the same change so the stale pattern cannot be re-copied by future work.
