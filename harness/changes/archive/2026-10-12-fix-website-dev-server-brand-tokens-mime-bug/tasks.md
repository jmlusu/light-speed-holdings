# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

- [x] T002 [P] Remove `import '../../brand/tokens/brand-tokens.css';` from 8 page files under `src/pages/` (OfferA–OfferE, Index, Build, Architecture); grep confirms zero remaining TSX imports of the specifier outside `src/index.css`.
- [x] T003 [P] Remove the same import from 7 component files under `src/components/` (TrustStrip, Playground, LeadershipStrip, KPIBand, FeatureGrid, FeatureCard, Hero).
- [x] T004 [P] Update `docs/assets/README.md` + `docs/assets/inventory.md` guidance: tokens load globally once via `src/index.css`; do not import brand-tokens from components/pages.

## Validation

- [x] T005 `npm run lint`, `npm run test`, `npm run build` all green. — PASS: lint clean, 38/38 tests, build 11.64s (pre-existing non-blocking esbuild CSS warning only).
- [x] T006 Dev server 1441: start, run Playwright `verify-nav-modal.js` → 19/19 pass (React mounts, zero MIME errors). — PASS: 19/19; `mime-check.cjs` shows all module responses `200 [text/javascript]`, zero console MIME errors.
- [x] T007 Preview 1440: run same Playwright suite → 19/19 pass (no regression). — PASS: 19/19.
- [x] T008 `pwsh scripts/build/sync-brand.ps1 -Verify` green (mirrors untouched). — PRE-EXISTING FAIL (113 MISSING files), unrelated to this diff: git status shows zero changes under `brand/`, `static/brand/`, `public/brand/`; `-Verify` reads only those dirs; `brand/logos/fulllogo/fulllogo.png` tracked canonically (56 files) but only 25 files tracked under `public/brand` — mirrors were never fully synced. Mirrors untouched by this change as required; syncing 113 binary assets is out of scope.
- [x] T009 Full non-e2e `uv run pytest` to completion; record in `summary.md` `validation_results`. — PASS: 2584 passed, 2 skipped, 67 deselected (e2e), 3 warnings, exit 0, 351s; git status unchanged after run (only generated `harness/changes/INDEX.json`).
- [x] T010 Update `summary.md` (outcome/decisions/validation/phase=validate), `docs/STATUS.md`, run `lint-ecl.ps1`, then `harness-change.ps1 close completed`. — summary.md finalized (phase=validate, validation_status=pass, results recorded), reviews approved, STATUS.md updated (2026-10-12), lint-ecl EXIT=0.

## Deferred Tasks

- None.
