---
title: "P0 boundary guards G-1 G-2 G-3"
slug: "p0-boundary-guards-g-1-g-2-g-3"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "accepted"
spec_review: "approved"
plan_review: "approved"
modules: ["cli.dashboard", "vite.config", "tests.unit"]
files: ["src/ai_company/cli/dashboard.py", "vite.config.ts", "tests/unit/test_port_assignments.py"]
tags: ["p0", "boundary-guards", "ports", "cto-ratification"]
validation_status: "pass"
validation_results: ["pytest test_port_assignments.py: 7/7", "ruff: clean", "mypy src/: clean", "vite port guard runtime: refused 8420/8421, 1441 starts", "lint-ecl.ps1: PASS"]
created_at: "2026-10-10"
updated_at: "2026-10-10"
session_id: "fe82c5d4-1c98-4813-9a23-d51fa7ad9523"
owner_agent: "jmlus"
claimed_at: "2026-10-10"
---

# Summary

## Outcome

CTO ratification §7 P0 boundary guards G-1/G-2/G-3 implemented:

- **G-1** `tests/unit/test_port_assignments.py` — static CI gate asserting vite 1441/1440, PM2 vite-dev/preview ports, dashboard CLI default 8420, compose 8420:8420 / staging 8421, and `dashboard_ports ∩ vite_ports == ∅`.
- **G-2** `src/ai_company/cli/dashboard.py` — refuses `--port 1440`/`1441` with Marketing Site message, `typer.Exit(1)` (adjacent to ADR-012 loopback guard).
- **G-3** `vite.config.ts` — `dashboardPortGuard()` plugin throws on resolved server/preview port ∈ {8420, 8421}, naming CEO Dashboard; catches `vite --port` CLI overrides via `configResolved`.

## Decisions

- G-1…G-3 ship as one change (ratification §7); G-4…G-7 deferred as P1/P2.
- Runtime guards fail fast at startup; no port reassignment.
- Pre-existing 5 `test_ecl_change_lifecycle.py` failures are historical INDEX archive-quality issues (missing slug/phase, validation_status=unknown on old entries); out of scope here.

## Validation

- `pytest tests/unit/test_port_assignments.py` — 7/7 pass.
- `ruff check src/ tests/unit/test_port_assignments.py` — clean.
- `mypy src/` — clean (229 files).
- Runtime: `vite dev --port 8420` and `vite preview --port 8421` both refuse with CEO Dashboard message; `vite dev --port 1441` starts normally.
- `pwsh scripts/maintenance/lint-ecl.ps1` — PASS (4 historical slug WARNs).

## Next Step

Archive this change and commit G-1/G-2/G-3 files on `mypy-fix-asset-pipeline`.
