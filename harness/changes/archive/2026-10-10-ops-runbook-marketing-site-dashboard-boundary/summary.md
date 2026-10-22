---
title: "ops-runbook-marketing-site-dashboard-boundary"
slug: "ops-runbook-marketing-site-dashboard-boundary"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "approved"
spec_review: "approved"
plan_review: "approved"
modules: ["docs"]
files:
  - "docs/sop-incident-response-v2.md"
  - "docs/sop/operations-sop.md"
  - "docs/sop/engineering-sop.md"
  - "docs/sop/marketing-sop.md"
tags: ["ops", "sop", "incident-response", "marketing-site", "port-boundary", "docs-only"]
validation_status: "pass"
created_at: "2026-10-10"
updated_at: "2026-10-10"
session_id: "79e4217a-be1f-4d94-8a56-90860af6b84f"
owner_agent: "jmlus"
claimed_at: "2026-10-10"
---

# Summary

## Outcome

Ops runbook delta applied: four SOPs now carry Marketing Site / CEO Dashboard boundary language — standard PM2/uvicorn launch commands, per-app health probes (`GET /` HTML on 1440/1441 vs `GET /health` JSON `status:"ok"` on 8420/8421), cross-serving fail rules, and a port-conflict containment runbook. Authority stays with `docs/organization/app-naming-and-port-assignments.md` and the CTO ratification; SOPs cross-reference rather than duplicate port tables.

## Decisions

- Interpretation stands: edit operational docs AND return the delta summary to the user (no code/script changes in this change).
- Port-boundary violation = SEV-3 normally, SEV-2 if CEO Dashboard is unreachable as a result (incident SOP §5).
- Cold-start probe rule propagated into ops health checks: allow ≥30s, retry once after `VITE ready in ...`.
- Engineering enforcement gaps (ratification G-1..G-6: CI gates, Docker HEALTHCHECK wiring) deferred as follow-up, not part of this docs delta.
- `scripts/dev/health-check.ps1` "Vite servers" wording and start-vite.ps1 divergence from PM2 noted as follow-up; not edited here (code/scripts out of scope).

## Validation

- `pwsh scripts/maintenance/lint-ecl.ps1` — run after edits (see T007).
- Coverage greps for Marketing Site / ports / pm2 / /health across the four edited SOPs.
- No pytest/ruff: docs-only per AGENTS.md §6 harness/docs row.

## Next Step

- Mark T007 after lint + greps; set validation_status; close change via harness script; deliver delta summary to user (COO handoff).
