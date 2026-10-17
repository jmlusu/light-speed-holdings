# Spec

## Intake Review

- Intake type: Structured Change (requirement-first)
- Input shape: requirement-first — CTO ratification §7 action table (G-4..G-7)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: The 2026-10-10 CTO ratification of the Marketing Site / CEO Dashboard port boundary lists four unfilled engineering actions (G-4, G-5, G-6, G-7). Owner directive: implement these four items only.
- Current behavior:
  - G-4: `ecosystem.config.cjs` hardcodes `C:\Users\jmlus\light-speed-holdings\node_modules\.bin\vite.exe` (finding F2) — breaks any other checkout, CI, Linux host, container.
  - G-5: no port-binding *identity* audit exists (ratification §6 "Missing" bullet 4); `scripts/dev/health-check.ps1:4` declares an unused `$ProjectRoot` hardcoded path (same portability smell).
  - G-6: `.github/workflows/site-principles-gate.yml` builds/tests the site but never asserts the four port assignments — a frontend-only PR can retarget ports without Python tests running (ratification §6 "Missing" bullet 3).
  - G-7: `docs/organization/app-naming-and-port-assignments.md` §5 checklist carries no production residual-risk note (Vercel 443 → cross-serving structurally impossible in prod; exposure is local/dev/staging only).
- Source of evidence: `docs/organization/cto-ratification-marketing-site-dashboard-boundary.md` §6 (lines 115-121), §7 table (G-4..G-7 rows), §4 finding F2, §5 health contracts (lines 97-101); `tests/unit/test_port_assignments.py` (G-1 precedent).

## User Scenarios And Success

- Primary user/system scenario: any developer/CI runner on a different machine, plus the deployment operator verifying at runtime that each of 1440/1441/8420/8421 is owned by the correct process.
- Success criteria:
  - `pm2 start ecosystem.config.cjs` resolves vite from `node_modules/vite/bin/vite.js` relative to the repo root on any checkout.
  - `scripts/dev/verify-port-bindings.ps1` reports which process owns each of the four ports and fails on cross-serving (HTML on 8420/8421, JSON status on 1440/1441) per §5 contracts.
  - `site-principles-gate.yml` fails a PR that changes port values in `vite.config.ts` without matching assignments.
  - The org communication doc states the prod residual-risk posture.
- Acceptance criteria:
  - `uv run pytest tests/unit/test_port_assignments.py` green (G-1 parity preserved: `vite-dev`→1441, `vite-preview`→1440).
  - `pwsh scripts/maintenance/lint-ecl.ps1` PASS.
  - `pwsh scripts/dev/verify-port-bindings.ps1` runs to completion (exit 0 when ports unbound/idle or correctly bound; non-zero on identity mismatch).

## Non-Goals

- G-1/G-2/G-3 (already shipped, archived as `2026-10-10-p0-boundary-guards-g-1-g-2-g-3`).
- Any new dashboard runtime refusal logic (G-2/G-3 territory), PM2 readiness integration (F3), Vercel-side changes, other org files, A1–A7 evolution items (separate track).

## Constraints

- Single ECL change; do not hand-edit `harness/changes/INDEX.json` (regenerate via `reindex`).
- Do not touch concurrent-session dirty files (`src/ai_company/generator.py`, `tests/unit/test_kpi_collectors.py`, untracked `knowledge/technology/bug-fixes/BUG-b0d879ac1.md`).
- Keep PM2 `port:` metadata fields (G-1 test asserts them); only `script:`/`cwd:` change.

## Assumptions

- Node is invoked via the repo-local `node_modules/vite/bin/vite.js` (cross-platform, PM2 runs it with node).
- Port-binding identity audit is a local PowerShell check (Windows dev host per AGENTS §12), not a CI gate.

## Open Questions

(none)

## Resolved Clarifications

- A4–A7 / evolution items are out of this change's scope — handled as a separate harness-evolution track per task directive.
