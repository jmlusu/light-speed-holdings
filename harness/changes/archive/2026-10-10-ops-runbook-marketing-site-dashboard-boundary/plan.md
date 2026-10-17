# Plan

## Technical Approach

Docs-only delta. Four SOP edits, each additive and cross-referencing the CSO naming directive and CTO ratification rather than duplicating port tables. No application code, scripts, or generated files touched.

1. **Incident SOP v2** (`docs/sop-incident-response-v2.md`): extend §2 scope with Marketing Site / CEO Dashboard port-boundary incidents; add SEV-3/SEV-2 examples for cross-serving in §5; in §6 Step 1 clarify health-check endpoints per app + identity probes; add a Step 3a containment sub-procedure for wrong-port serving; add references to the naming directive + ratification in §12.
2. **Operations SOP** (`docs/sop/operations-sop.md`): extend §5.3 with the two-app health-check table (`GET /` HTML vs `GET /health` JSON); insert new §5.5 "Application Launch & Port Boundary" (standard launch commands, port-conflict response runbook, cold-start probe note); add naming docs to §15 Related Documents.
3. **Engineering SOP** (`docs/sop/engineering-sop.md`): amend §5.2 step 5 to name the dashboard port/JSON contract and add cross-serving fail rule; small addition only.
4. **Marketing SOP** (`docs/sop/marketing-sop.md`): add short §4.5 or near-scope subsection "Marketing Site Runtime Ownership" (PM2 launch, ports, Vercel deploy, never bind 8420/8421); add naming doc to Related Documents.

## Impacted Modules And Files

- `docs/sop-incident-response-v2.md` — scope, severity examples, detection, containment, references
- `docs/sop/operations-sop.md` — §5.3 health checks, new §5.5 launch/port boundary, §15 related docs
- `docs/sop/engineering-sop.md` — §5.2 step 5 health verification
- `docs/sop/marketing-sop.md` — new runtime-ownership subsection + related docs
- `harness/changes/active/*` — spec/plan/tasks/summary maintained by this change

## Interfaces, Data, Permissions

- No runtime interfaces, data files, or permission changes.
- Audience: ops agents, CTO/eng on-call, CMO/content team, Chief of Staff triage.
- Authority: CSO directive (naming/ports) + CTO ratification (probe contracts); COO owns ops SOP; CTO owns incident + engineering SOPs; CMO owns marketing SOP — edits are in-line with existing owners and flagged for owner review via summary.

## Spec Gaps Found From Planning

- None. Naming directive §6 escalation (stop misconfigured app → Chief of Staff → CSO) is the basis for the port-conflict runbook; CTO ratification §5 supplies the exact identity probes.

## Risks And Mitigations

- Risk: duplicating port tables that could drift from the naming directive. Mitigation: SOPs reference the directive by path; tables only restate launch/probe commands, not full port matrices.
- Risk: confusing `/` vs `/health` in monitoring scripts. Mitigation: state the fail rules explicitly ("wrong content-type on assigned port = cross-serving, follow containment").
- Risk: cold-start false positives on health checks. Mitigation: document retry-after-`VITE ready` ≥30s rule in ops §5.5.

## Verification Plan

- `pwsh scripts/maintenance/lint-ecl.ps1`
- Grep each edited SOP for "Marketing Site", "1440", "1441", "pm2 start ecosystem.config.cjs", "GET /health" to confirm coverage.
- Manual read-through of edited sections for consistency with naming directive §2–§6 and ratification §5.
- No pytest/ruff needed (docs-only); per AGENTS.md §6 "Harness / docs" row.
