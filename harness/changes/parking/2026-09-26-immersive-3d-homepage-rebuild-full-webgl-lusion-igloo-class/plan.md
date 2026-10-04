# Plan

## Technical Approach

Two-layer architecture (Lusion model): **DOM is the content, WebGL is the stage.**

- Persistent fixed-position canvas behind homepage content, bootstrapped via mount gate: `tier('none'|'lite'|'full') → IntersectionObserver → requestIdleCallback → import('./three/Scene')`.
- Authored camera driven by scroll progress (custom rAF-lerped hook, no GSAP/Lenis): hero drift → builder spotlight (the one pinned-feel moment) → node constellation for the 90-agent workforce → resolve to CTA.
- Scene content: navy volumetric field + 4px grid plane (brand grid), instanced cyan particle constellation (90 nodes, 7 category colors from theme classes), red accent beacon at the proof/CTA beat. Materials read brand tokens only (no hex literals outside `materials.ts` constants sourced from `brand/tokens`).
- Theme: scene background/lighting follows `theme` prop (light: pale field on paper; dark: deep navy field).
- Fallback: tier `none`/import failure → theme-aware static poster div (CSS gradient + grid), zero canvas bytes.
- Build: `vite.config.ts` `manualChunks` → `three` split from entry; verify with `bun run build` output.

## Impacted Modules And Files

Parallel work ownership (no two agents edit the same file):

| Owner | Files |
|---|---|
| Agent A — `lead-frontend` (WebGL) | `src/three/**` (new: `tiers.ts`, `mountGate.ts`, `Scene.ts`, `CameraRig.ts`, `materials.ts`, `poster.ts`), `src/components/ImmersiveStage.tsx` (new), `src/hooks/useScrollProgress.ts` (new), `vite.config.ts` |
| Agent B — `product-designer` (DOM) | `src/pages/HomePage.tsx`, `src/components/HeroSection.tsx`, `src/components/home/**` (new section/chapter-rail components), `src/index.css` |
| Agent C — `cmo` (copy) | `src/data/homeImmersiveCopy.ts` (new, exact keys in Interface section) |
| Orchestrator | `package.json`/`bun.lock` (dep install), ADR-036, ECL docs, integration, validation |

Shared/readonly: `src/data/siteContent.ts`, `src/components/site/*`, `src/components/Reveal.tsx`, brand tokens.

## Interfaces, Data, Permissions

**Contract A → B (mount):**

```tsx
// src/components/ImmersiveStage.tsx — Agent A delivers exactly:
export interface ImmersiveStageProps { theme: 'light' | 'dark'; }
export const ImmersiveStage: React.FC<ImmersiveStageProps>;
// Renders position:fixed inset-0 z-0 (behind content), aria-hidden, pointer-events:none.
// HomePage mounts it first: <ImmersiveStage theme={theme} /> inside a relative wrapper;
// page content sections get relative z-10.
```

**Contract B → C (copy):** `src/data/homeImmersiveCopy.ts` exports `homeImmersiveCopy` with keys: `heroEyebrow: string`, `heroTitle: string`, `heroTitleAccent: string`, `heroLead: string`, `heroCta: string`, `chapters: { id: string; num: string; label: string }[]` (7 entries matching homepage sections), `scrimHint: string`. B imports and renders; C fills final copy (shapeofintelligence micro-copy discipline: every control gets an invitation).

## Spec Gaps Found From Planning

- None; `three` install is orchestrator-owned to avoid lockfile races.

## Risks And Mitigations

- Chunk still lands in entry → `manualChunks` + build-output check (verification gate).
- Canvas covers content/CTA clicks → `pointer-events: none` on stage; DOM layer owns all interaction.
- Theme mismatch (scene vs `.dark` toggle) → scene listens to `theme` prop; both themes screenshot-verified.
- Jank on low-end → tier gate (coarse pointer / deviceMemory ≤4 → `lite` or `none`), DPR cap, pause off-screen.
- Regressions to other routes → ownership map + `bun run test` + route smoke (`bun run build`).
- Scroll jank/scroll-jacking → camera lerps *content* of canvas only; native scroll untouched (no scroll-jack, per research).

## Verification Plan

1. `bun run lint` (tsc) · 2. `bun run test` · 3. `bun run build` (three in separate chunk; sizes recorded) · 4. `pwsh scripts/lint-ecl.ps1` · 5. `uv run pytest` (Python untouched, regression sweep) · 6. Playwright visual check at 1280×800 + 375×667 both themes (re-add `@playwright/test` if broken) · 7. manual: reduced-motion → poster; DevTools no-WebGL → poster; keyboard tab order; contrast over canvas.
