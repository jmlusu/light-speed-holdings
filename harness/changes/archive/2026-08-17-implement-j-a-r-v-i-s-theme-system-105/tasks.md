# Tasks

## Format

- `- [x] T001 [P?] Action with target path and validation note`
- `[P]` means parallel-safe.

## Setup / Intake

- [x] T001 [P] Review #101 resolution (design tokens) and #104 resolution (shell prototype) as input specs.
- [x] T002 [P] Create `control-plane-theme.css` with CSS custom properties, `.jarvis-glass`, `.chrome-scanline`, status-pulse keyframes, `@font-face` declarations.
- [x] T003 [P] Download and self-host Rajdhani (500, 700) + JetBrains Mono (400) woff2 in `static/fonts/`.

## Implementation

- [x] T004 [P] Update `base.html`: link theme CSS, extend Tailwind config with `jarvis.*` tokens + `fontFamily`, restyle header/nav/footer.
- [x] T005 [P] Update `style.css`: `.kpi-card:hover` glow, focus ring (cyan), drag-over, print styles.
- [x] T006 [P] Update `charts.js`: token-derived `COLORS` palette via `getComputedStyle`, updated Chart.js defaults.
- [x] T007 Migrate `index.html` to jarvis tokens.
- [x] T008 Migrate `agents.html` to jarvis tokens.
- [x] T009 Migrate `tasks.html` to jarvis tokens.
- [x] T010 Migrate `kpis.html` to jarvis tokens.
- [x] T011 Migrate `costs.html` to jarvis tokens.
- [x] T012 Migrate `escalations.html` to jarvis tokens.
- [x] T013 Migrate `command-center.css` to use `var(--jarvis-*)` references.

## Validation

- [x] T014 Run `ruff check src/` — PASS.
- [x] T015 Run `mypy src/` — PASS (144 files).
- [x] T016 Run `pytest tests/unit/test_dashboard_smoke.py tests/unit/test_dashboard.py tests/integration/test_dashboard_api.py` — PASS (38/38).

## Deferred Tasks

- None.
