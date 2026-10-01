# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`

## Setup / Intake

- [x] T001 Discovery of SPA + brand system + ADR-020 conflict (read-only) — done 2026-09-24.
- [x] T002 Capture open decisions and park ECL entry — `harness/changes/parking/2026-09-24-ai-venture-studio-web-experience-brand-psychology/`.

## Implementation (blocked on decisions)

- [ ] T003 Resolve palette / scope / surface with CEO (see summary Decisions).
- [ ] T004 If new palette: ADR amending ADR-020 + token sync `brand/tokens` → mirrors → `src/brand/brand-tokens.css`.
- [ ] T005 Implement Part 1 effects (ripple, mist, scroll easing, reduced-motion) in SPA.
- [ ] T006 Optional: Parts 2–5 content page.

## Validation

- [ ] T007 `bun run lint` && `bun run build` green.
- [ ] T008 Playwright → `ls-artifact-qa` APPROVE.

## Deferred Tasks

- None beyond T003–T006 (intentionally parked).
