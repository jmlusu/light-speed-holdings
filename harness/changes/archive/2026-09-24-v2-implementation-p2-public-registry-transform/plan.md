# Plan

## Technical Approach

1. **T003 Backfill** — Run `harness/changes/active/scripts/backfill_governance_fields.py` (idempotent; fills the 4 MANDATORY fields on all 90 agents in `company-registry.yaml`). Verify 90/90 + spot-check `qa_lead`, `human_ceo`, `board_chair`.
2. **T004 Models + fail-fast validator** — Add `decision_rights`, `approval_level`, `escalation_path`, `kpis` to `Agent` and `BoardMember` in `src/ai_company/models/models.py` (`Executive` already has `decision_rights`; add the other three). Extend `RegistryValidator` with a `_check_governance_fields` that errors when any field is missing/empty on any of `executives`/`specialists`/`board`. Wire through `cli/validate.py` if not already covered. Unit tests in `tests/unit/test_registry.py`.
3. **T005–T007 Public transform + tool normalization** — New `src/ai_company/registry/public_transform.py`: load YAML, validate counts 90/20/19-64-7, allowlist project per schema §3/§4, remap legacy tools (`write`→`edit`, `execute`→`bash`, `delegate`→`task`, `web_search`/`websearch`→`webfetch`), hard-fail `code_interpreter`, optional KPI label join, write `src/data/generated/agent-registry.public.json` with fixed `generated_at` (idempotent) + denylist scan. Normalize tools in `sync.py` `_agent_yaml_to_json` (same alias map). Regenerate `company/agent-registry.json` via `sync_registry`. Add CLI command (e.g. `ai-company public-registry` or wire into `generate`). Idempotency re-run.
4. **T008+ SPA cutover** — `companyData.ts` imports `./generated/agent-registry.public.json`; map `PublicAgent` → whatever local `Agent` shape pages still need (drop `guidelines`/`permission`). `types.ts`: split or narrow `Agent` so public surface has no `guidelines`/`permission`. Fix `AgentModal.tsx` L79 (`agent.permission`) and `HaomtgvGovernanceFramework.tsx` L923/L1253 (`permission`/`guidelines`). Rewrite `src/__tests__/companyData.test.ts` to assert public shape (90, no forbidden keys, canonical tools). V4 ops fixtures stay out of this change.
5. **Gates** — `uv run ruff check src/ && uv run mypy src/ && uv run pytest && npx tsc --noEmit && npx vitest run`; `pwsh scripts/lint-ecl.ps1`; `pwsh scripts/validate-drift.ps1`. Update `docs/STATUS.md`, set `phase: validate` + `validation_results`, then `harness-change.ps1 close completed`.

## Impacted Modules And Files

| Path | Change |
|------|--------|
| `company-registry.yaml` | T003: add 4 fields ×90 (script rewrite) |
| `harness/changes/active/scripts/backfill_governance_fields.py` | Already present; run as T003 |
| `src/ai_company/models/models.py` | T004: fields on `Agent`, `BoardMember`, `Executive` |
| `src/ai_company/registry/validator.py` | T004: `_check_governance_fields` |
| `src/ai_company/cli/validate.py` | T004: surface governance errors if CLI path is separate |
| `tests/unit/test_registry.py` | T004: missing-field fail-fast tests |
| `src/ai_company/registry/public_transform.py` | T005–T006: NEW transform module |
| `src/ai_company/registry/sync.py` | T006: tool alias normalization in `_agent_yaml_to_json` |
| `src/ai_company/cli/main.py` | T006: CLI wiring for transform |
| `company/agent-registry.json` | Regenerated after sync |
| `src/data/generated/agent-registry.public.json` | NEW public artifact |
| `src/data/companyData.ts` | T008: switch import to public artifact |
| `src/types.ts` | T008: public type (no guidelines/permission) |
| `src/components/AgentModal.tsx` | T008: drop `agent.permission` render |
| `src/components/HaomtgvGovernanceFramework.tsx` | T008: drop `permission`/`guidelines` renders |
| `src/__tests__/companyData.test.ts` | T009: rewrite for public shape |

Out of scope (do not touch): `.opencode/agents/*` regeneration, `vercel.json`/routes, `docs/STATUS.md` historical lines, parked copies under `harness/changes/parking/`.

## Interfaces, Data, Permissions

- **Internal SoT:** `company-registry.yaml` `company.agents[]` gains four keys per agent:
  - `decision_rights: list[str]` (≥1)
  - `approval_level: str` ∈ `self|lead|exec|ceo|board` (enum per AI_WORKFORCE §5.1; backfill uses `lead|exec|ceo|board` — no `self` in current data)
  - `escalation_path: list[str]` terminal `human_ceo`/`board`
  - `kpis: list[str]` labels only
- **Public artifact envelope:** `schema_version`, `generated_at`, `source`, `meta.agents`, `meta.departments`, `agents[]`, `departments[]` (7 required).
- **PublicAgent required 7:** `id` (kebab), `name`, `title`, `type`, `department`, `reports_to` (null only for board_chair), `mission`. Optional: `tools`, `kpi_labels`, `decision_rights`, `responsibilities`, `technical_domain`, `department_id`, `is_human`.
- **Never in public:** `guidelines`, `permission`, `model_tier`, `approval_level`, `escalation_path`, `workflows`, `inputs`, `outputs`, secrets, raw KPI values.
- **CLI:** new/extended command emits the public artifact; exit non-zero on denylist/count/tool violations.
- **No new secrets or RBAC changes.**

## Spec Gaps Found From Planning

- Roadmap P2 exit still says "7 MANDATORY … workflows/inputs/outputs" — spec Resolved Clarification overrides to 4 MANDATORY; workflows/inputs/outputs stay NEVER public and non-enforced for this change. Recorded, not blocking.
- `company/departments.yaml` at 19 (missing pharos) vs registry 20 — transform must not fail solely on departments.yaml lag; prefer registry-derived department set + SoT 20.
- Internal JSON has no `id` (slug lives in `name`) — transform must source ids from YAML (`id` → kebab `id`).

## Risks And Mitigations

| Risk | Mitigation |
|------|------------|
| Full `yaml.safe_dump` reorders/reformats registry → huge diff / breaks comments | Registry is comment-free; verify with `git diff --stat` and spot-check structure; keep `sort_keys=False`. |
| Validator too strict breaks existing generation before backfill lands | Order: T003 backfill FIRST, then T004 fail-fast. |
| Legacy tools leak into public artifact | Shared alias map + denylist scan + unit test asserting zero legacy names. |
| Concurrent session mutates `active/` | Race-check `harness-change.ps1 status` before each harness op. |
| SPA type-check breaks after type split | Fix all `guidelines`/`permission` consumers in same T008 commit; run `tsc --noEmit`. |
| Idempotent `generated_at` vs freshness | Store fixed timestamp in artifact (or derive from env/`SOURCE_DATE_EPOCH`); re-run must not churn byte-identical output except intended fields. |

## Verification Plan

| Step | Command / check |
|------|-----------------|
| T003 | `uv run python harness/changes/active/scripts/backfill_governance_fields.py` then inline `uv run python -c` count of 4 fields ×90; spot-check qa_lead / human_ceo / board_chair; re-run script → coverage still 90/90 (idempotent). |
| T004 | `uv run pytest tests/unit/test_registry.py`; deliberate missing-field fixture → non-empty errors. |
| T005–T006 | `uv run python -m ai_company.cli.main public-registry` (or equivalent) → artifact exists; `uv run python -c` asserts counts, denylist, tool set; re-run idempotent; `uv run ruff check src/ && uv run mypy src/`. |
| T008–T009 | `npx tsc --noEmit`; `npx vitest run`; grep `src/` for `company/agent-registry.json` → zero; grep public JSON for forbidden keys → zero. |
| Full | `uv run ruff check src/ && uv run mypy src/ && uv run pytest && npx tsc --noEmit && npx vitest run` |
| ECL | `pwsh scripts/lint-ecl.ps1`; `pwsh scripts/validate-drift.ps1` |
| Close | `docs/STATUS.md` update; `harness-change.ps1 validate`; `harness-change.ps1 close completed` |
