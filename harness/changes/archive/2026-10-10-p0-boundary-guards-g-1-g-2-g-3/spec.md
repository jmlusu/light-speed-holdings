# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first (CTO ratification §7)
- Questions asked this round: 0

## Goal And Evidence

- Real problem: Marketing Site (Vite) ports 1440/1441 and CEO Dashboard (FastAPI) ports 8420/8421 had only documentation as the boundary; no static or runtime guard prevented cross-serving.
- Current behavior: `ai-company dashboard --port 1441` would happily serve the dashboard on a Vite port; `vite --port 8420` would bind a Vite server on a dashboard port.
- Source of evidence: `docs/organization/cto-ratification-marketing-site-dashboard-boundary.md` §7 (G-1, G-2, G-3, P0); AGENTS.md §12/§13.

## User Scenarios And Success

- Primary user/system scenario: An agent or operator accidentally retargets one application onto the other's ports; the system fails fast at startup instead of silently cross-serving.
- Success criteria:
  - Static test fails CI if any port assignment drifts (vite.config.ts, ecosystem.config.cjs, dashboard CLI default, compose mappings).
  - `ai-company dashboard --port 1441` exits non-zero with a message naming the Marketing Site.
  - `vite --port 8420` (or a config edit) throws a config-resolved error naming the CEO Dashboard.
- Acceptance criteria: `pytest tests/unit/test_port_assignments.py` passes; G-2 and G-3 guards are in place; `ruff`, `mypy`, `pytest` all green; `lint-ecl.ps1` PASS.

## Non-Goals

- G-4 PM2 portability, G-5 port-binding identity audit, G-6 frontend-only CI guard, G-7 prod residual-risk note (P1/P2, separate changes).
- Changing any port assignment.

## Constraints

- Build on concurrent-session edits; do not revert uncommitted work in `ecosystem.config.cjs`, `src/ai_company/dashboard/app.py`, `tests/unit/test_dashboard_security.py`, `scripts/dev/health-check.ps1`, `README.md`, `AGENTS.md`.
- Do not hand-edit `harness/changes/INDEX.json`.
- G-1…G-3 ship as one ECL change (ratification §7).

## Assumptions

- Existing pytest CI gate (`uv run pytest`) picks up the new unit test automatically.
- ADR-012 loopback guard pattern in `dashboard.py` is the correct model for G-2.

## Open Questions

- None.

## Resolved Clarifications

- G-1/G-2/G-3 are the only P0 items in scope; P1/P2 deferred.
