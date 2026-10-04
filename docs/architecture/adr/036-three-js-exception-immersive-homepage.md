# ADR-036: Three.js Exception for the Immersive Homepage

**Status:** Superseded by ADR-037 (2026-09-27, user override: Three.js strip)
**Date:** 2026-09-26
**ECL:** Immersive 3D homepage rebuild - full WebGL (lusion/igloo class)
**Cross-refs:** MASTER_SPEC §25, LEGACY_INVENTORY.md, ADR-020 (migrate in place), ADR-034 (dep weight = risk register), compliance ledger #303, `docs/research/immersive-3d-website-research.md`

## Context

MASTER_SPEC §25 states: "Do not add Three.js, GSAP, video, shaders, or other heavy technologies simply because they are available." LEGACY_INVENTORY marked the old `ThreeCanvas.tsx` DELETE, and compliance ticket #303 confines "ThreeCanvas/WebGL + tactile motif … to internal diagnostics only" (OPEN, P2). Commit `30d268d` removed `three` from the dependency set.

The CEO has directed a **full-WebGL immersive homepage rebuild** (lusion/igloo class) using igloo.inc, videinfra.com, lusion.co, and shapeofintelligence.com as inspiration. This is a deliberate, budgeted exception to §25 — authorized because it is the *product* of this change, not an incidental dependency. Research (`docs/research/immersive-3d-website-research.md`) supplies the budget and fallback discipline that §25's intent (no gold-plating) requires.

## Decision

1. **`three` is authorized** as a homepage-only dependency, loaded exclusively through a lazy dynamic import behind a device/ability tier gate (`src/three/tiers.ts` → `mountGate.ts`). It must never appear in the initial JS chunk of any route (`manualChunks` split; verified via build output).
2. **No GSAP, no Lenis, no R3F, no drei.** Scroll-driven camera uses a small custom rAF-lerped progress hook. React stays 18 (raw `three`, no R3F v9 which requires React 19). The exception covers exactly one package: `three`.
3. **#303 supersession is partial:** WebGL is permitted on the public homepage `/` behind `ImmersiveStage` only. All other routes remain WebGL-free; the tactile/motif confinement is otherwise unchanged. The compliance ledger is updated by its owner, not edited by this change.
4. **Hard budgets (from research §5.4):** three chunk ≤ 250 KB gz; homepage never blocks LCP on the canvas (DOM paints first); DPR ≤ 2; render loop pauses off-screen, on `visibilitychange`, and under `prefers-reduced-motion` (tier `none` → static poster fallback); canvas is `aria-hidden` with all content/CTAs in the DOM.
5. **Rollback:** removing the `<ImmersiveStage />` mount from `HomePage.tsx` returns the site to its pre-change behavior; the dep can be dropped from `package.json` in the same revert.

## Consequences

- Bundle analyzer and CI budget gates must be checked at close of the ECL change.
- `bun.lock` gains `three`; Playwright visual QA (`scripts/visual_check.js`) must be re-runnable (re-add `@playwright/test` dev dep) — known gap from `30d268d`.
- §25 text remains as-is; this ADR is the record of exception, not a spec edit.
