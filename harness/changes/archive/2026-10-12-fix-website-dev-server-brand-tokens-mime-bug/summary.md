---
title: "fix-website-dev-server-brand-tokens-mime-bug"
slug: "fix-website-dev-server-brand-tokens-mime-bug"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "approved"
plan_review: "approved"
modules: ["website/pages", "website/components", "docs/assets"]
files: ["src/pages/OfferA.tsx", "src/pages/OfferB.tsx", "src/pages/OfferC.tsx", "src/pages/OfferD.tsx", "src/pages/OfferE.tsx", "src/pages/Index.tsx", "src/pages/Build.tsx", "src/pages/Architecture.tsx", "src/components/TrustStrip.tsx", "src/components/Playground.tsx", "src/components/LeadershipStrip.tsx", "src/components/KPIBand.tsx", "src/components/FeatureGrid.tsx", "src/components/FeatureCard.tsx", "src/components/Hero.tsx", "docs/assets/README.md", "docs/assets/inventory.md"]
tags: ["bugfix", "vite", "website", "brand-tokens"]
validation_status: "pass"
created_at: "2026-10-12"
updated_at: "2026-10-12"
session_id: "8360b709-ecf9-4a7a-970f-c2c941004947"
owner_agent: "jmlus"
claimed_at: "2026-10-12"
---

# Summary

## Outcome

Implemented and validated. Fix for the pre-existing dev-server bug found during the FloatingNav modal verification: 15 TSX files imported `../../brand/tokens/brand-tokens.css`, but in dev the response is served from `public/brand/tokens/brand-tokens.css` as raw `text/css` by Vite's public-dir middleware, so the browser rejects it as a module script (`Expected a JavaScript-or-Wasm module script ... MIME type of "text/css"`) and React never mounts on `npm run dev` (1441). Fix: removed the 15 redundant imports (tokens already load globally via `src/index.css:2` through `main.tsx`) + corrected 2 stale docs that recommended the broken pattern. Verified: dev 1441 renders (all module responses `200 [text/javascript]`, zero MIME errors, Playwright 19/19), preview 1440 19/19, lint/test/build green, full suite 2584 passed. Production build unaffected; mirrors untouched.

## Decisions

- Remove per-component imports (15 files + 2 docs) — chosen because the global load via `src/index.css` already exists and this fixes the bug class without touching any invariant.
- Rejected: deleting `public/brand/tokens/brand-tokens.css` (fails `sync-brand.ps1 -Verify`, breaks mirror invariant); vite.config `publicDir`/middleware changes (breaks other public assets or reimplements internals); path-alias tricks (still 15 file edits or fragile query bypass).
- Fix mandate approved by user: "Proceed to fix the Pre-existing bug found" + "Continue if you have next steps" (2026-10-12); technical approach selected by agent investigation within that mandate, options/rejections recorded above.
- Pending evolution (`harness/evolution/pending.md`, auto-evolve, 6+ eligible archives) noted per ECL §6/§9 — does not block this change; not handled here.

## Validation

- **validation_results**: T005 PASS (`npm run lint` clean, `npm run test` 38/38, `npm run build` 11.64s — pre-existing non-blocking esbuild CSS warning only).
- T006 PASS: dev 1441 — `mime-check.cjs` all module responses `200 [text/javascript]`, zero console MIME errors; `verify-nav-modal.js` 19/19.
- T007 PASS: preview 1440 — `verify-nav-modal.js` 19/19 (no regression).
- T008 PRE-EXISTING FAIL, out of scope: `sync-brand.ps1 -Verify` reports 113 MISSING mirror files. Evidence unrelated to this diff: git status shows zero changes under `brand/`, `static/brand/`, `public/brand/`; `-Verify` reads only those dirs; canonical `brand/logos/fulllogo/fulllogo.png` exists and is tracked (56 files under `brand/logos`) while `public/brand` tracks only 25 files — mirrors were never fully synced. This change did not touch mirrors (the actual T008 requirement). Syncing 113 binary assets deferred as separate work.
- T009 PASS: `uv run pytest -q -m "not e2e"` → **2584 passed, 2 skipped, 67 deselected, exit 0** (351s); git status unchanged after run (only script-generated `harness/changes/INDEX.json`).
- Code Review: approved; Validation Review: approved (see `reviews/review.md`).

## Next Step

- Close: `harness-change.ps1 close completed`, then report to user (commit only if explicitly requested).
