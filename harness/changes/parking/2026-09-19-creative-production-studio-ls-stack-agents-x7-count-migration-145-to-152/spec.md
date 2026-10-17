# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first
- Questions asked this round: 2 (working session prior to this change: clarified scope = complete `ls-*` skill stack, no new department, agents under Marketing; confirmed park-then-new ECL flow)

## Goal And Evidence

- Real problem or user request: `.agents/skills/ls-*` defines a 7-layer Creative Production Stack (design-system -> creative-director -> production x5 + support -> artifact-qa), but the registry has no 1:1 agent cards for those skills. Producing an on-brand artifact requires a human/skill to be mapped to an owned agent card.
- Current behavior: Registry has 145 agents (144 AI + 1 Human CEO). Marketing has `brand_strategist`, `social_media_manager`, `content_creator`, `media_generation_owner`; the `ls-*` stack is not represented by dedicated agents.
- Source of evidence: `company-registry.yaml` (lines 3720-3746, `media_generation_owner` is last entry); `.agents/skills/ls-*`; `brand/CANONICAL_SOURCES.md`; `AGENTS.md` "Creative Production Stack" section.

## User Scenarios And Success

- Primary user/system scenario: A user invokes `/create-website`, `/create-keynote`, `/create-whitepaper`, or `create a campaign`; the routing agent dispatches to `creative_director`, which composes a brief and hands to a production specialist (presentation/document/diagram/visual/ad), ending with `artifact_qa_reviewer` approving before delivery.
- Success criteria: 7 new Marketing specialists exist in `company-registry.yaml`; generated `.opencode/agents/*.md` cards exist with `mode: subagent` + canonical 7-tool permission blocks; `company/agent-registry.json` synced; `docs/AGENT-REGISTRY-TABLE.md` regenerated; registry count 145 -> 152.
- Acceptance criteria:
  - `load_registry()` returns 20 executives / 125 specialists / 7 board / 20 departments / 152 total.
  - `ai-company generate` and `ai-company sync-registry --verify` succeed with no drift.
  - `scripts/validate-drift.ps1` and `pytest tests/docs/test_doc_drift.py` pass with `agent_count` updated to 152 in `docs/source-of-truth.yaml`.
  - Full gates pass: `scripts/lint-ecl.ps1`, `ruff check src/`, `mypy src/`, full pytest suite.

## Non-Goals

- No new department; Creative Production Studio is not a department, agents sit under Marketing.
- No change to templates (`.j2`) or generator code.
- No change to existing 145 agent cards beyond regeneration side effects (`.bak` files, AGENT-REGISTRY-TABLE).
- No edit to the six non-production `ls-*` support skills' registry coverage (they remain skill-only).
- No changes to `docs/STATUS.md` as a drift-tracked doc (excluded from pattern checks; it is a dated log).

## Constraints

- Specialist `reports_to` must reference an existing executive or specialist (resolver valid set is executives | specialists | board | human_ceo). `creative_director` -> `cmo`; remaining six -> `creative_director`.
- Specialist `department` must match a known department; `marketing` exists in `company/departments.yaml` (id `marketing`, name `Marketing`).
- IDs must be unique snake_case; regenerated cards are kebab-case (`creative-director.md`).
- Registry `tools` use canonical names (`read`, `write`, `bash`, `execute`, `web_search`, `webfetch`, `grep`, `list`, `task`, `delegate`); generator maps them to OpenCode v2 permission keys.
- `docs/source-of-truth.yaml` is the drift manifest: only `agent_count` (docs: README.md, docs/USER-GUIDE.md, docs/ORGANIZATION.md) changes here. Other entries (departments, KPIs, providers, templates) unchanged.
- ECL: `active/` allows one change; only script-generated INDEX.json writes.

## Assumptions

- Each new agent maps 1:1 to an `ls-*` skill card; model_tier `standard` matches peers.
- Human CEO remains separate from the 151-AI count; registry total includes it (145 = 144 AI + 1 Human CEO; 152 = 151 AI + 1 Human CEO).
- Pathological `.bak` companions in `.opencode/agents/` are regenerated side effects, not tracked as intended output.
- `uv run` is available (project uses uv per AGENTS.md).

## Open Questions

- None blocking.

## Resolved Clarifications

- Scope is the 7-agent Creative Production Studio only (completed `ls-*` stack), not a broader skill->agent expansion.
- Prior `2026-09-04-doc-drift-prevention` change parked (moved to `parking/`), new active change created.
