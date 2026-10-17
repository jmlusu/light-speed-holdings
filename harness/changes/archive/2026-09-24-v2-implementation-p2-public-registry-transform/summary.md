---
title: "v2-implementation-p2-public-registry-transform"
slug: "v2-implementation-p2-public-registry-transform"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "accepted"
spec_review: "approved"
plan_review: "approved"
modules: []
files: []
tags: ["p2", "public-registry", "governance-backfill", "transform", "spa-cutover"]
validation_status: "pass"
created_at: "2026-09-24"
updated_at: "2026-09-24"
session_id: "deee1150-1546-48a2-bd96-c89d2f891d70"
owner_agent: "jmlus"
claimed_at: "2026-09-24"
---

# Summary

## Outcome

P2 shipped end-to-end: 4 MANDATORY governance fields backfilled 90/90 on `company-registry.yaml` (+18 on consulting template), fail-fast validator, allowlist `public_transform.py` → `src/data/generated/agent-registry.public.json`, tool normalization in sync, CLI `transform-public-registry`, SPA cutover off internal JSON, and all gates green.

## Decisions

- MANDATORY = exactly 4 fields (`decision_rights`, `approval_level`, `escalation_path`, `kpis`); roadmap's 7-MANDATORY wording overridden (workflows/inputs/outputs stay optional / NEVER public).
- Public sink: `src/data/generated/agent-registry.public.json` per ADR-028.
- Session-foreign backfill script (`deee1150…`) reused under this plan-approved change.
- User pre-approved spec + plan ("Recommendations approved. Proceed with execution.").
- Denylist scan is structural-key + value-level secret patterns only (prose must not false-positive); marketing-owner responsibility reworded "brand guidelines" → "brand standards" so the literal T012 word grep is clean.
- Consulting template got the same 4-field backfill (72 fields / 18 agents) so `load_registry(TEMPLATE_CONFIG_DIR)` passes fail-fast validation.

## Validation

- `tests/unit` **1877 passed** (310s); targeted registry/models/tool-vocab/consulting-template/generator **83 passed**.
- `npx tsc --noEmit` clean; `npx vitest run` **17/17**.
- ruff + mypy clean on all P2 modules (`registry`, `cli/main.py`, `models`).
- `pwsh scripts/lint-ecl.ps1` pass; `pwsh scripts/validate-drift.ps1` 87 claims clean.
- Transform: 90 agents / 20 depts / census 19+64+7; envelope 7 keys; idempotent double-run byte-identical; structural deny 0; forbidden words 0; tools ⊆ canonical 7; zero ts/tsx imports of `company/agent-registry.json`.
- Full-repo ruff/mypy currently red only on concurrent-session untracked `src/ai_company/lsmem/` (out of scope; owned by LS-MEM track).

## Next Step

- Close this change (`harness-change.ps1 validate` + `close completed`), restore side-effect files, clean empty parking copies, then pick up P3 per `V2_IMPLEMENTATION_ROADMAP.md`.
