# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.
- [x] T002 Resolve three CEO decisions: gradient stand-in background, hybrid canvas, wire-and-reconcile roster gate.

## Implementation

- [x] T003 [US1] Create `src/components/haomtgv/layers.ts` with `HaomtgvLayer` and the seven `HAOMTGV_LAYERS` entries.
- [x] T004 [US1] Build `src/components/haomtgv/HaomtgvBlueprintHero.tsx` (backdrop, headline, slab stack, layer badges, connectors, CTA).
- [x] T005 [US1] Add hero keyframes and reduced-motion guard to `src/index.css`.
- [x] T006 [US1] Replace the inline hero in `src/pages/HAOMTVGPage.tsx` with `<HaomtgvBlueprintHero />` and drive the grid from `HAOMTGV_LAYERS`.
- [x] T007 [US1] Register the `haomtgv` route in `src/App.tsx` via `withSite(HaomtgvPage)`.
- [x] T008 [US1] Remove the duplicate connector overlay and retune headline breakpoints in `HaomtgvBlueprintHero.tsx`.

## Validation

- [x] T009 Run `npm run lint` — clean, no diagnostics.
- [x] T010 Run `npm run build` — passes; 1706 modules, JS 410.88 kB (gzip 109.17), CSS 152.17 kB (gzip 23.23).
- [ ] T011 Optional visual QA: Playwright screenshots at 1440×900 and 1024×768. Blocked — Playwright is not installed locally.
- [x] T012 Document deviations (palette, icon set, type stack, mobile scale, CTA placement, header logo, connector geometry) in `summary.md`.

## Deferred Tasks

- T013 Wire `scripts/ci/check_agent_baseline.py` into `.github/workflows/ci.yml` via branch + PR.
- T014 Reconcile `company-registry.yaml` (91 ids) with `company/agent-baseline.json` (90 ids) — pending decision on `job_board`.
- T015 Swap in a real hero photograph via `HaomtgvBlueprintHeroProps.backgroundImage` once one exists.
