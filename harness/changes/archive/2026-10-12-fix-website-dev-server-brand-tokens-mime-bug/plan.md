# Plan

## Technical Approach

- **P1 Remove redundant imports:** delete the single line `import '../../brand/tokens/brand-tokens.css';` from 15 TSX files (8 pages: `OfferA`–`OfferE`, `Index`, `Build`, `Architecture`; 7 components: `TrustStrip`, `Playground`, `LeadershipStrip`, `KPIBand`, `FeatureGrid`, `FeatureCard`, `Hero`). Tokens keep loading globally via `src/index.css:2` ← `main.tsx`.
- **P2 Correct stale guidance:** `docs/assets/README.md` (line ~88) and `docs/assets/inventory.md` (line ~47) — stop recommending per-component token imports; state the global-load rule (components must not import brand-tokens directly; they are loaded once via `src/index.css`).
- **P3 Verify:** lint/test/build; dev server 1441 + Playwright nav/modal suite must go green (currently fails to mount); preview 1440 re-run must stay green; `sync-brand.ps1 -Verify` untouched-but-confirmed; full non-e2e pytest suite (archive gate); `lint-ecl.ps1`.

## Impacted Modules And Files

- `src/pages/OfferA.tsx`, `OfferB.tsx`, `OfferC.tsx`, `OfferD.tsx`, `OfferE.tsx`, `Index.tsx`, `Build.tsx`, `Architecture.tsx` — remove token import.
- `src/components/TrustStrip.tsx`, `Playground.tsx`, `LeadershipStrip.tsx`, `KPIBand.tsx`, `FeatureGrid.tsx`, `FeatureCard.tsx`, `Hero.tsx` — remove token import.
- `docs/assets/README.md`, `docs/assets/inventory.md` — guidance correction.
- `harness/changes/active/*` — ECL records only.

## Interfaces, Data, Permissions

- No runtime interfaces, data models, permissions, or public APIs change. CSS delivery changes only in dev (from broken module import to the already-global `index.css` load).

## Spec Gaps Found From Planning

- None. All 15 import sites and both docs sites located by grep before implementation.

## Risks And Mitigations

- Some route loads tokens only via a removed import → all routes enter through `main.tsx` → `index.css`; confirmed by reading `index.html`/`main.tsx`. Playwright visual assertions (nav/modal styling) re-verify token application on dev and preview.
- Someone re-adds the per-component import later → docs now state the global-load rule explicitly.
- Mirror/CI drift → mirrors and `sync-brand.ps1` untouched; `-Verify` re-run as a gate.
- Concurrent sessions on shared machine (known hazard) → `git status` snapshot before/after full suite.

## Verification Plan

- `npm run lint` (tsc --noEmit), `npm run test` (vitest 38), `npm run build`.
- Dev: start `npm run dev` (1441) → Playwright `verify-nav-modal.js` against 1441 (must pass 19/19; pre-fix it cannot even mount React).
- Preview: `npm run preview` (1440) → same Playwright suite must stay green.
- `pwsh scripts/build/sync-brand.ps1 -Verify` (or equivalent CI gate) green.
- Full non-e2e `uv run pytest` to completion, listed in `validation_results`.
- `pwsh scripts/maintenance/lint-ecl.ps1` green before close.
