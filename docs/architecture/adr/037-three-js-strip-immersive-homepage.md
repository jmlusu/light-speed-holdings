# ADR-037: Three.js Strip for the Immersive Homepage

**Status:** Accepted (User override, 2026-09-27)
**Date:** 2026-09-27
**ECL:** Three.js strip — homepage static fallback
**Cross-refs:** MASTER_SPEC §25, §31, §33; SPECIFICATION_MAP §25, §31; TARGET_ARCHITECTURE §10; IMPLEMENTATION_AUDIT.md (post-rewrite); docs/research/immersive-3d-website-research.md (superseded); LEGACY_INVENTORY.md (audit trail); compliance ledger #303, #304

## Context

MASTER_SPEC §25 states: "Do not add Three.js, GSAP, video, shaders, or other heavy technologies simply because they are available." LEGACY_INVENTORY recorded that Three.js was an authorized exception under ADR-036 (2026-09-26), granted because the CEO directed a full-WebGL immersive homepage rebuild.

On 2026-09-27 the user exercised override authority: Three.js has been stripped entirely from the codebase. All nine `src/three/` files, `ImmersiveStage.tsx`, `useScrollProgress.ts` (+test), and `HeroMist.tsx` are removed. The homepage now renders a static §19 mist/slate fallback (`.dark:bg-[#121518]` with class-based dark-mode via `@custom-variant`). The `three` and `@types/three` entries are purged from `package.json` and `bun.lock`; `node_modules/three` is absent. Vite's `manualChunks` three rule is removed. Build output is a single 427.69 kB JS bundle (no three chunk). Test suite reduced from 42 → 17 passing (2 files).

This ADR records the strip as an intentional product decision, not a regression.

## Decision

1. **Three.js removed entirely** — no `three` dependency, no lazy import, no `ImmersiveStage`, no WebGL on any route. The `three`/`@types/three` keys are removed from `package.json` and `bun.lock`; 7 transitive deps pruned.
2. **§19 static fallback active** — `HomePage.tsx` renders a fixed-position mist/slate canvas with `dark:bg-[#121518]` (class-based, not OS-preference-dependent). `index.css` includes `@custom-variant dark (&:where(.dark, .dark *))` so all `dark:` utilities follow the `.dark` class toggled by `App.tsx`.
3. **Test suite adjusted** — 5 test files deleted with `src/three/`. Remaining suite: 17 vitest cases across 2 files. No ContentBoundary tests exist; these would be added in a future Phase 2 initiative (not part of this rebuild).
4. **Rollback** — reverting the strip restores `src/three/`, `ImmersiveStage`, and associated test files; the `three` dep can be re-added to `package.json`; ADR-036 status would revert to Accepted pending re-authorization.

## Consequences

- Bundle: single 427.69 kB output; no three chunk; `dist` CSS has zero `@media (prefers-color-scheme:dark)` blocks; `.dark:` selectors are class-scoped via `:where(.dark,.dark *)`.
- Metrics: site claims "2,557" (stale; verified value ~2,566). Fix deferred to Phase 2 metrics registry (§24).
- Audit trail: 4 read-only auditors (CoS, CTO, Memory Owner, QA Lead) all attested `tsc --noEmit` exit 0 and zero lingering three refs.
- ADR-036: **Status changed to Superseded by ADR-037 (2026-09-27)**; cross-reference chain updated in `SPECIFICATION_MAP.md`.
- Rollback risk: one `git checkout` could resurrect the entire three.js stack — tracked as top open risk in QA's report.

## Superseded

ADR-036: Three.js Exception for the Immersive Homepage (2026-09-26, Accepted) — status changed to **Superseded**.

## References

- MASTER_SPEC §25, §31, §33
- SPECIFICATION_MAP §25, §31
- TARGET_ARCHITECTURE §10 roadmap
- IMPLEMENTATION_AUDIT.md (post-rewrite)
- LEGACY_INVENTORY.md audit trail
- Compliance ledger #303, #304
- docs/research/immersive-3d-website-research.md (superseded by this decision)