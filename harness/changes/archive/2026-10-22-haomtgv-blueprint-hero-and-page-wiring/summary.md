---
title: "HAOMTGV blueprint hero and page wiring"
slug: "haomtgv-blueprint-hero-and-page-wiring"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "completed"
spec_review: "completed"
plan_review: "approved"
modules: []
files: []
tags: []
validation_status: "pass"
created_at: "2026-10-16"
updated_at: "2026-10-22"
session_id: "0ae3f812-5907-4363-b033-4470d7c36b00"
owner_agent: "jmlus"
claimed_at: "2026-10-16"
---

# Summary

## Outcome
All hero interaction, contrast, tagline, and responsive layout fixes have been applied to `src/components/haomtgv/HaomtgvBlueprintHero.tsx`. Visual QA screenshots at 1440×900 and 1024×768 were captured and verified with no clipping or overlap. The CTA contrast meets WCAG AA (5.4 : 1). The hero stacks under `lg` (1024 px) and full‑viewport on `xl` (1280 px+).

## Decisions
- Hero interaction: slab `onMouseEnter`/`onMouseLeave` with shared `activeIndex`; two‑way hover ↔ row selection.
- Connector active highlighting: width/opacity/box‑shadow follow the active slab.
- Tagline: three `aria‑hidden` spans (white/cyan/red) with `aria‑label="ASPIRE. ACT. ACHIEVE."`.
- CTA contrast: text colour changed from `text‑white` to `text-[#050B1A]` (≈5.4 : 1).
- Responsive layout: centre slab width `lg:w‑[240px]` / `lg:-ml‑[120px]`; at `xl` expands to `xl:w‑[300px]` / `xl:-ml‑[150px]`. Right list and tagline now behave correctly at both 1440 × 900 and 1024 × 768.
- ECL: all required checks (lint, build, test, ECL lint, visual‑QA) passed; the change is ready for closure.

## Validation
- `npm run lint` → passes
- `npm run build` → 1703 modules transformed, no errors
- `npm test` → 41 tests pass
- ECL lint (`scripts/maintenance/lint-ecl.ps1`) → passed
- Playwright visual QA at 1440×900 and 1024×768 → verified

## Next Step
ECL change can be closed; no further action required.

## Transition Note

- Parked by deck-QA automation change to free the single active slot; resume with harness-change.ps1 resume <id>.
- Parked for the deck logo crop-cache change (issue #485) to free the single active slot; resume with harness-change.ps1 resume <id>.
- Parked for the perf-gate calibration change (issue #484) to free the single active slot; resume with harness-change.ps1 resume <id>.
- Parked for the script lint-coverage change to free the single active slot; resume with harness-change.ps1 resume <id>.
