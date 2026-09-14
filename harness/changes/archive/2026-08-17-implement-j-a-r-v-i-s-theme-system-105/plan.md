# Plan

## Technical Approach

1. Create `control-plane-theme.css` with CSS custom properties (palettes, glass, typography), `.jarvis-glass` utility, `.chrome-scanline` pseudo-element, status-pulse keyframes, and `@font-face` declarations.
2. Download and self-host Rajdhani (500, 700) and JetBrains Mono (400) woff2 files in `static/fonts/`.
3. Update `base.html`: link theme CSS, extend Tailwind config with `jarvis.*` tokens + `fontFamily`, restyle header/nav/footer with jarvis tokens.
4. Update `style.css`: update `.kpi-card:hover` glow, focus ring, drag-over, print styles.
5. Update `charts.js`: replace hardcoded `COLORS` with `getComputedStyle`-derived palette.
6. Migrate all 7 content templates from `surface-*`/`brand-*` to `jarvis-*` tokens.
7. Update `command-center.css`: replace hardcoded rgba values with `var(--jarvis-*)` references.

## Impacted Modules And Files

### Created
- `src/ai_company/dashboard/static/css/control-plane-theme.css`
- `src/ai_company/dashboard/static/fonts/Rajdhani-Medium.woff2`
- `src/ai_company/dashboard/static/fonts/Rajdhani-Bold.woff2`
- `src/ai_company/dashboard/static/fonts/JetBrainsMono-Regular.woff2`

### Modified
- `src/ai_company/dashboard/templates/base.html`
- `src/ai_company/dashboard/templates/index.html`
- `src/ai_company/dashboard/templates/agents.html`
- `src/ai_company/dashboard/templates/tasks.html`
- `src/ai_company/dashboard/templates/kpis.html`
- `src/ai_company/dashboard/templates/costs.html`
- `src/ai_company/dashboard/templates/escalations.html`
- `src/ai_company/dashboard/templates/command-center.html` (indirectly via CSS)
- `src/ai_company/dashboard/static/css/style.css`
- `src/ai_company/dashboard/static/css/command-center.css`
- `src/ai_company/dashboard/static/js/charts.js`

### Not modified
- `src/ai_company/dashboard/app.py` — CSP unchanged, no new CDN deps.

## Interfaces, Data, Permissions

- No API changes. No data model changes. No permission changes.
- Frontend-only: CSS custom properties, Tailwind class names, JS palette initialization.

## Spec Gaps Found From Planning

- None. Both prerequisites (#101, #104) provided complete specs.

## Risks And Mitigations

| Risk | Mitigation |
|------|------------|
| Font file 404 (versioned URLs) | Fetched live CSS from `fonts.googleapis.com` to get correct URLs |
| Template migration surface (7 templates + base) | Mechanical class replacement; verified with grep for orphaned tokens |
| Chart palette breakage | Token-derived via `getComputedStyle`; falls back to original colors if tokens unavailable |

## Verification Plan

| Gate | Command | Result |
|------|---------|--------|
| Lint | `ruff check src/` | PASS |
| Type check | `mypy src/` | PASS (144 files) |
| Dashboard tests | `pytest tests/unit/test_dashboard_smoke.py tests/unit/test_dashboard.py tests/integration/test_dashboard_api.py` | PASS (38/38) |
