# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. (spec_review + plan_review completed per front matter)

## Implementation

- [x] T002 Hero interaction, contrast, tagline, and responsive fixes in `src/components/haomtgv/HaomtgvBlueprintHero.tsx`; landed as `bf9a1d17` / PR #489.

## Validation

- [x] T003 `npm run lint`, `npm run build`, `npm test`, ECL lint, Playwright visual QA at 1440x900 and 1024x768 — all passed. Page wiring + tests landed as `df83e2a7` / PR #490.

## Deferred Tasks

- None.

## Completed Tasks
- [x] T011 Visual QA: Playwright screenshots at 1440x900 and 1024x768 passed.
