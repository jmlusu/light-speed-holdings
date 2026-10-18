# fix(registry): restore 90-agent baseline and add HITL CI gate

**ID:** BUG-c2452e5af
**Date:** 2026-10-18
**Resolved:** resolved
**Commit:** c2452e5afd4742d16daae4a93b8e03a77089b5d3
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

PR #474 squash-merged an unapproved 91st agent (`job_board`) into
`company-registry.yaml` (commit `72e450b8`, LSAI Remediation Bot). The
`ci.registry_gate` gap identified in `reports/repo-audit-2026-10-18.md`
meant no CI check validated the agent roster, so the addition merged
silently. The first (earlier) incident cannot be determined from
available evidence — the registry file only exists from `fa5a233c`
(2026-10-17).

## Fix (filled by the resolving engineer)

1. Removed the `job_board` entry from `company-registry.yaml` (no
   backing functionality: no JobSource, no athena package).
2. Restored all count pins, docs, frontend copy, and wayfinder
   gap-analysis from 91/65-specialist to 90/64-specialist.
3. Added HITL CI gate: `company/agent-baseline.json` records the 90
   CEO-approved agent IDs; `scripts/ci/check_agent_baseline.py` fails
   any unapproved add/remove/swap; wired as `registry-baseline` job
   in `.github/workflows/ci.yml` gate.
4. Documented the rule in `AGENTS.md` section 9.4 (cites ADR-026).

## Files Changed

- `company-registry.yaml` — job_board entry removed
- `company/agent-baseline.json` — new baseline (90 approved IDs)
- `scripts/ci/check_agent_baseline.py` — new HITL check
- `.github/workflows/ci.yml` — registry-baseline job + gate.needs
- `AGENTS.md` — section 9.4
- `src/ai_company/registry/public_transform.py` — census 91→90
- Count pins, docs, frontend copy, wayfinder (see commit stat)

## Diagnostic Commands

- `git log -S job_board -- company-registry.yaml`
- `git log -S scrape -- docs/wayfinder/`
- `uv run python scripts/ci/check_agent_baseline.py` (exit 0 at 90)

## Verification

- Targeted pytest: 46 passed
- Full pytest: 2652 passed, 2 skipped
- `bun run site:check`: tsc clean, vite build OK, 41 vitest tests passed
- Baseline check: positive OK (exit 0); negative smoke test exits 1
  with `::error::` for unapproved ID + missing approved ID

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
