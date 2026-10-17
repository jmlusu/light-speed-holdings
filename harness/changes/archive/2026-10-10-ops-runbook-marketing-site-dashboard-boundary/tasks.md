# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

- [x] T002 Update `docs/sop-incident-response-v2.md`: scope (§2), severity examples (§5), detection identity probes (§6 Step 1), port-conflict containment (§6 Step 3), references (§12). Validation: file contains "Marketing Site", identity-probe table, containment steps.
- [x] T003 [P] Update `docs/sop/operations-sop.md`: extend §5.3 with two-app health-check table; insert §5.5 Application Launch & Port Boundary (PM2 launch commands, port-conflict runbook, cold-start note); add naming docs to §15. Validation: contains "pm2 start ecosystem.config.cjs", `/health` JSON vs `/` HTML split, port-conflict steps.
- [x] T004 [P] Update `docs/sop/engineering-sop.md` §5.2 step 5: name dashboard 8420/8421 JSON contract; add Marketing Site `/` HTML note + cross-serving fail rule. Validation: step 5 mentions ports and both endpoints.
- [x] T005 [P] Update `docs/sop/marketing-sop.md`: add Marketing Site Runtime Ownership subsection (PM2, ports, Vercel, never 8420/8421); add naming directive to Related Documents. Validation: subsection present; Related Documents lists naming directive path.
- [x] T006 Update `harness/changes/active/summary.md` front matter (phase, files, tags) and Outcome/Decisions sections to reflect completed edits.

## Validation

- [x] T007 Run `pwsh scripts/maintenance/lint-ecl.ps1`; expect pass. Then grep edited SOPs for key terms (Marketing Site, 1440, 1441, pm2, /health) and confirm coverage; record result in summary.md validation_status.

## Deferred Tasks

- Follow-up (not this change): wire ratification G-1..G-6 enforcement (CI gates, Docker HEALTHCHECK); consider updating `scripts/dev/health-check.ps1` wording "Vite servers" → "Marketing Site".
