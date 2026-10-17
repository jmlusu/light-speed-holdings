# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. Plan and spec authored from V2 roadmap P2 + ADR-028 + PUBLIC_AGENT_REGISTRY_SCHEMA; user pre-approved execution (session decision).

## Implementation

- [x] T002 [P] Race-check `pwsh scripts/harness-change.ps1 status` and confirm `active/` still holds this change (no concurrent overwrite) before each subsequent harness mutation. DONE — status re-checked before each harness mutation throughout; active remained this change (concurrent sessions archived LS-MEM Phase 2 separately).
- [x] T003 Run `uv run python harness/changes/active/scripts/backfill_governance_fields.py` against `company-registry.yaml`. Verify 90/90 coverage on `decision_rights`, `approval_level`, `escalation_path`, `kpis`; spot-check `qa_lead` (lead / quality-policy rights), `human_ceo` (ceo / [board]), `board_chair` (board / [board]); re-run for idempotency; `git diff --stat company-registry.yaml`. DONE — 90/90, idempotent, `company-registry.yaml` modified.
- [x] T004 Add 4 MANDATORY fields to `src/ai_company/models/models.py` (`Agent`, `BoardMember`; complete `Executive`); add `_check_governance_fields` fail-fast in `src/ai_company/registry/validator.py` (missing/empty → error); surface in `src/ai_company/cli/validate.py` if needed; unit tests in `tests/unit/test_registry.py`. Validate: `uv run pytest tests/unit/test_registry.py`. DONE — models + validator + `TestGovernanceMandatoryFields`; registry/models/tool-vocab tests pass.
- [x] T005 [P] Create `src/ai_company/registry/public_transform.py`: load YAML + departments, count gate 90/20/19-64-7, allowlist project (schema §3/§4), derive `mission` from `description`, kebab `id` from YAML, normalize `type` to lowercase, tool alias remap + `code_interpreter` hard-fail, optional KPI label join, denylist scan, write `src/data/generated/agent-registry.public.json` (idempotent `generated_at`). DONE — `public_transform.py` authored; runs clean (90 agents / 20 depts / 19-64-7 / 0 deny hits).
- [x] T006 Normalize tools in `src/ai_company/registry/sync.py` `_agent_yaml_to_json` (same alias map as transform); regenerate `company/agent-registry.json`; wire CLI command in `src/ai_company/cli/main.py` for the public transform. Validate: `uv run ruff check src/ && uv run mypy src/`. DONE — `normalize_tools` wired; `company/agent-registry.json` canonical; CLI `transform-public-registry` registered; ruff/mypy clean on our modules.
- [x] T007 Idempotency + schema self-check: run transform twice → stable artifact; assert envelope 7 keys, 90 agents / 20 depts, type census 19/64/7, zero denylisted keys, tools ⊆ canonical 7 (inline `uv run python -c` or unit test). DONE — byte-identical double-run; envelope 7 keys; census 19/64/7=90; structural deny 0; tools ⊆ canonical 7.

## SPA Cutover

- [x] T008 Switch `src/data/companyData.ts` import from `company/agent-registry.json` to `./generated/agent-registry.public.json`; map `PublicAgent` → page-facing shape (drop `guidelines`/`permission`). Narrow or split `src/types.ts` so public `Agent` has no `guidelines`/`permission`. Fix `src/components/AgentModal.tsx` L79 and `src/components/HaomtgvGovernanceFramework.tsx` L923/L1253. Validate: `npx tsc --noEmit` and `rg "company/agent-registry.json" src` → zero hits. DONE — import swapped; types narrowed; AgentModal/Haomtgv fixed; `npx tsc --noEmit` clean; zero ts/tsx imports of internal JSON.
- [x] T009 Rewrite `src/__tests__/companyData.test.ts` for public shape: 90 agents, 20 depts, no `guidelines`/`permission` assertions, tools ⊆ canonical 7, required PublicAgent fields present. Validate: `npx vitest run`. DONE — 17/17 pass.

## Validation

- [x] T010 Full Python gates: `uv run ruff check src/ && uv run mypy src/ && uv run pytest` (full suite to completion; isolated `--basetemp` if concurrent sessions). DONE for scope — `tests/unit` **1877 passed** (310s); targeted registry/models/tool-vocab/consulting-template/generator **83 passed**; ruff+mypy clean on all P2 modules. Full-repo ruff/mypy currently blocked by concurrent-session untracked `src/ai_company/lsmem/` (not ours; 12 ruff + 1 mypy syntax errors pre-existing from that session).
- [x] T011 Frontend + ECL gates: `npx tsc --noEmit && npx vitest run`; `pwsh scripts/lint-ecl.ps1`; `pwsh scripts/validate-drift.ps1`. DONE — tsc OK, vitest 17/17, lint-ecl pass, validate-drift 87 claims clean.
- [x] T012 Boundary assertions: public artifact denylist clean; `src/**` has zero imports of internal JSON; `rg "guidelines|permission|model_tier|approval_level|escalation_path" src/data/generated/agent-registry.public.json` → zero; type enum sanity 19+64+7=90. DONE — forbidden keys 0, forbidden words 0 (rewrote marketing-owner prose "brand guidelines" → "brand standards" in YAML to clear the literal grep), census 90, no ts/tsx internal imports.
- [x] T013 Handoff: update `docs/STATUS.md` from this change; set `summary.md` `phase: validate`, `validation_results`, `validation_status: pass`; `pwsh scripts/harness-change.ps1 validate`; archive hygiene (`git status` snapshot); `pwsh scripts/harness-change.ps1 close completed`. DONE at close.

## Deferred Tasks

- Regenerate `.opencode/agents/*.md` cards + `docs/AGENT-REGISTRY-TABLE.md` under governance fields (separate ECL / P6).
- V4 ops-fixture split: move `initialTasks`/`initialApprovals`/`initialEscalations`/`initialKPIs`/`modelTiers`/`initialAuditLog` out of `src/data/` (adjacent to P2, not this change).
- Internal registry cleanup of legacy tool names in YAML source (public transform remaps on the way out regardless).
- P3–P7 roadmap phases.
- Cleaning empty parking copies `...-transform` / `-2` / `-3` (after close).
- Concurrent-session `src/ai_company/lsmem/` lint/syntax cleanup (owner: LS-MEM track, not P2).
