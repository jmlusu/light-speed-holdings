---
title: "Implement J.A.R.V.I.S. theme system (#105)"
slug: "implement-j-a-r-v-i-s-theme-system-105"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules:
  - "ai_company.dashboard"
files:
  - "src/ai_company/dashboard/static/css/control-plane-theme.css"
  - "src/ai_company/dashboard/static/css/style.css"
  - "src/ai_company/dashboard/static/css/command-center.css"
  - "src/ai_company/dashboard/static/js/charts.js"
  - "src/ai_company/dashboard/static/fonts/Rajdhani-Medium.woff2"
  - "src/ai_company/dashboard/static/fonts/Rajdhani-Bold.woff2"
  - "src/ai_company/dashboard/static/fonts/JetBrainsMono-Regular.woff2"
  - "src/ai_company/dashboard/templates/base.html"
  - "src/ai_company/dashboard/templates/index.html"
  - "src/ai_company/dashboard/templates/agents.html"
  - "src/ai_company/dashboard/templates/tasks.html"
  - "src/ai_company/dashboard/templates/kpis.html"
  - "src/ai_company/dashboard/templates/costs.html"
  - "src/ai_company/dashboard/templates/escalations.html"
  - "src/ai_company/dashboard/templates/command-center.html"
tags:
  - "frontend"
  - "theme"
  - "jarvis"
  - "dashboard"
  - "design-tokens"
validation_status: "pass"
validation_results:
  - gate: "ruff check src/"
    result: "PASS"
    details: "All checks passed"
  - gate: "mypy src/"
    result: "PASS"
    details: "Success: no issues found in 144 source files"
  - gate: "pytest tests/unit/test_dashboard_smoke.py tests/unit/test_dashboard.py tests/integration/test_dashboard_api.py"
    result: "PASS"
    details: "38 passed, 13 warnings"
created_at: "2026-08-17"
updated_at: "2026-08-17"
---

# Summary

## Outcome

Implemented the J.A.R.V.I.S. Control Plane theme system across the entire CEO dashboard. The theme introduces CSS custom property design tokens, self-hosted typography, glass-panel surfaces, scan-line textures, and status-pulse animations — all CSP-compatible with no new CDN dependencies.

## Decisions

- **Palette**: near-black base (`#070b14`), electric cyan primary (`#22d3ee`), cool-gray text (`#e2e8f0`/`#94a3b8`), amber warning, red critical, cyan-green success.
- **Typography**: Rajdhani (display) + JetBrains Mono (telemetry), self-hosted woff2 — no CSP change required.
- **Glass treatment**: `.jarvis-glass` utility class (rgba 0.72 opacity + 12px blur + luminous border + glow shadow), applied to all panels/cards.
- **Scan-line texture**: `.chrome-scanline` pseudo-element restricted to header/nav chrome, respects `prefers-reduced-motion`.
- **Token migration**: `surface-*`/`brand-*` Tailwind classes replaced with `jarvis-*` equivalents; backward-compat `brand-*`/`surface-*` retained in Tailwind config for incremental migration.
- **Chart palette**: `charts.js` COLORS object now reads from `getComputedStyle` at init — charts re-palette automatically when tokens change.
- **Dark-mode only**: `<html class=dark>` kept hardcoded; tokens do not change under light-mode class.

## Validation

| Gate | Result | Details |
|------|--------|---------|
| `ruff check src/` | PASS | All checks passed |
| `mypy src/` | PASS | 144 source files, no issues |
| Dashboard tests (smoke+unit+integration) | PASS | 38/38 passed |

## Blocked By

- #101 (Decide the J.A.R.V.I.S. visual language and design tokens) — CLOSED
- #104 (Prototype the Control Plane shell) — CLOSED

## Scope Delivered

1. **`control-plane-theme.css`** — CSS custom properties (palette, glass, typography), `.jarvis-glass`, `.chrome-scanline`, status-pulse keyframes, `@font-face` declarations, reduced-motion block.
2. **Self-hosted fonts** — Rajdhani 500/700 + JetBrains Mono 400 woff2 files in `static/fonts/`.
3. **`base.html`** — Theme CSS link, extended Tailwind config with `jarvis.*` tokens + `fontFamily`, restyled header/nav/footer with jarvis tokens.
4. **`style.css`** — Updated `.kpi-card:hover` glow, focus ring (cyan), drag-over, print styles.
5. **`charts.js`** — Token-derived `COLORS` palette via `getComputedStyle`, updated Chart.js defaults.
6. **Template migration** — All 7 content templates (`index`, `agents`, `tasks`, `kpis`, `costs`, `escalations`, `command-center`) migrated from `surface-*`/`brand-*` to `jarvis-*` tokens.
7. **`command-center.css`** — Replaced all hardcoded rgba values with `var(--jarvis-*)` references.

## What Remains (out of scope)

- Agent-flow particles, event pulse, full particle layer (deferred to #108)
- Command bar vocabulary / command execution (map #33 ticket #50)
- Light-mode support (dark-only per #101 decision)
- Full unit test suite regression run (dashboard suite verified; full suite was in progress at timeout)
