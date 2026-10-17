# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`

## Setup / Intake

- [x] T001 Discovery of SPA + brand system + ADR-020 conflict (read-only) — done 2026-09-24.
- [x] T002 Capture open decisions and park ECL entry — done 2026-09-24.
- [x] T003 Resolve palette / scope / surface with CEO — done 2026-09-24: keep navy/red/cyan; Part 1 only; home; mist CSS option A.

## Implementation

- [x] T004 Add ripple CSS + reduced-motion block to `src/index.css`; apply `.ripple-on` to FloatingNav, HomePage cards/pills, CtaBand, UseCaseCatalog tabs — done 2026-09-24.
- [x] T005 Create `src/components/effects/HeroMist.tsx`; mount in `HeroSection.tsx` — done 2026-09-24.
- [x] T006 Update `Reveal.tsx` timing to `cubic-bezier(0.25,1,0.5,1)`; add `useSmoothScroll` helper; wire `PillarNavigationCard` anchor scroll — done 2026-09-24.
- [x] T007 Palette ADR/token path — **N/A** (keep navy decision). Deferred.

## Validation

- [x] T008 `bun run lint` && `bun run test` && `bun run build` green — done 2026-09-24 (lint exit 0; 17/17 tests; build success).
- [x] T009 Playwright visual_check + `ls-artifact-qa` APPROVE — done 2026-09-24 (1280x800 + 375x667: overflow 0, missingAlt 0, emptyHeading 0; brand navy/red/cyan; mist + ripple present; sparse full-page gaps = Reveal off-screen, not layout bugs).
- [x] T010 `pwsh scripts/lint-ecl.ps1` green; record validation in summary — done 2026-09-24 (lint-ecl passed; harness validate passed).

## Deferred Tasks

- T007: No palette change (decision: keep navy/red/cyan).
- Parts 2–5 content page: intentionally out of scope for Part 1.
