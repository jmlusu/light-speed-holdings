# Spec

## Intake Review

- Intake type: Structured Change (plan-first)
- Input shape: plan-first
- Questions asked this round: 4 (scope, credential path, PR strategy, worktree)

## Goal And Evidence

- Real problem or user request: add Xiaomi MiMo as a 10th LLM provider for the
  fleet and install MiMo Code as a second coding CLI, without breaking routing,
  cost, or drift gates.
- Current behavior: 9 providers in `company/models.yaml`; MiMo absent from cost
  table, env templates, doctor, and vendor allow-list; no `.mimocode/` config.
- Source of evidence: `docs/MODEL-ROUTING-POLICY.md`,
  `docs/source-of-truth.yaml` `claims.provider_count`, `mimo debug config`
  output, `mimocode-docs/reference/providers.md`.

## User Scenarios And Success

- Primary scenario: fleet routes to MiMo on failover only (never displaces an
  existing primary), cost accounting includes MiMo, doctor reports 10 providers.
- Secondary scenario: operator runs `mimo run` against `MIMO_API_KEY` from
  `.env` with no interactive login.
- Success criteria: provider_count claim = 10 and drift gate green; CI green on
  PR #364; `mimo debug config` resolves `custom/mimo-v2.5`.
- Acceptance criteria: all Wave 0-4 gates pass; PR opened; vendor row with
  90-day window; ADR-025 recorded.

## Non-Goals

- No reordering of existing tiers or primary routing changes.
- No new provider module under `src/ai_company/llm/providers/`.
- No `mimo auth login` identity flow; no editing of `FALLBACK_REQUIRED_ENV_VARS`,
  `security.py` `placeholder_keys`, or `doctor/checks.py` `check_llm_providers`.
- No hand-edits to `.opencode/agents/*`, `company-registry.yaml`, or
  `harness/changes/INDEX.json`.

## Constraints

- Fresh worktree branched from `origin/main`; primary checkout left untouched.
- Conventional commits; pre-commit hooks must pass on every commit.
- AGENTS.md §9.2 third-party transmission ban applies to MiMo Code skills.

## Assumptions

- `MIMO_API_KEY` is the only new secret; it is never committed (`.env`
  gitignored; `.env.example` value left empty).

## Open Questions

- None. Credential path decided by CEO (issue `MIMO_API_KEY`, not
  `mimo auth login`).
