# LightSpeed Holdings — Creative Engine Consolidation Implementation Summary

## Phase 1: Cleanup and Reconciliation (Complete)

### Obsolete Capabilities Removed

**1. `archify`**
- Deleted `.opencode/skills/archify/` skill directory
- Removed `archify-check` CI step from `.github/workflows/ci.yml`
- Updated `.pre-commit-config.yaml` to remove archify exclude patterns
- Updated `AUDIT_REPORT.md` to remove archify drift detection entry
- Updated `docs/ARCHIFY-USAGE.md` to document capability removal
- **Follow-up (Nov 2026): completed the Python surface removal** — deleted
  `src/ai_company/cli/archify.py`, the `src/ai_company/archify/` package
  (converter/renderer), `tests/unit/test_archify.py`, `tests/cli/test_cli_archify.py`,
  and the `archify` lazy sub-app registration in `cli/main.py`. The renderer
  depended on the already-deleted skill checkout, so `validate`/`deliver`/`compare`
  could never run; stale references cleaned in `docs/ARCHITECTURE.md`,
  `docs/assets/`, `docs/website-imagery-spec.md`, `specs/open-design-integration.md`
  and `ai_development_constitution/`.

**2. `rayden-code`**
- Removed from `docs/archive/2026-08-11-pre-restructure/SKILL_INTEGRATION_ANALYSIS.md` skills table
- Removed from `docs/SKILL_CURATION_POLICY.md` Original 28 skills inventory

**3. `k-dense-infographics`**
- Updated 20+ documentation files across `docs/`, `tasks/`, `harness/changes/`
- Replaced `k-dense-infographics` references with `ls-visual-storytelling` where functional
- Updated research feasibility doc: table row, sources list, verdict section
- Updated task files: website-transformation plan, about-tasks.md, spec-about-page.md
- Updated harness changes: linkedin-ai-native-series spec/plan/summary/INDEX.json

### Brand Token Reconciliation

Canonical red `#DC3641` now used in all active source code:
- `src/ai_company/presentation/pipeline.py` — presentation pipeline red value
- `src/ai_company/presentation/pptxgen-base.json.j2` — PPTX template red value
- `src/ai_company/presentation/phase1 brief.j2` — brief deck palette
- `src/pages/HAOMTGVPage.tsx` — HAOMTGV page brand bar
- `src/components/common/Icon3D.tsx` — 3D icon red fill
- `src/ai_company/prompts/presentation.md` — presentation prompt brand tokens

The authoritative LightSpeed red is `#DC3641` per task specification. Legacy `#E63946` retained only in superseded files and brand guidelines.

### Creative Director — Already Registered

The `creative_director` agent was **already present** in the company registry:
- `company-registry.yaml` — `id: creative_director`, type: specialist, dept: Marketing, reports to: cmo
- `.opencode/agents/creative-director.md` — full agent card with mandate: "reads creative brief, decides skill chain, produces executable brief for production specialist"
- Operating guidelines: "Every creative task starts at ls-creative-director and ends at artifact QA. Reuse existing rendering engines rather than rebuilding them. Never invent brand colors or fonts; brand tokens are the single source of truth."
- Skills: `ls-od-runtime`, `ls-od-catalogue`, `ls-od-brand`, `ls-od-project`, `ls-od-prototype`, `ls-od-live-artifact`, `ls-od-deck`, `ls-od-image`, `ls-od-video`

### Infrastructure In Place

**Model Router** (`src/ai_company/model_router.py`):
- Tier-aware routing (fast → standard → premium)
- Domain-aware detection from task prompt keywords
- Task-type detection (read, edit, debugging, architecture, planning, etc.)
- Complexity scoring and budget degradation
- Quality-based fallback when providers fail
- Per-agent override from registry

**Executor** (`src/ai_company/executor/`):
- `daemon.py` — main execution loop
- `agent_loop.py` — agent session management
- `hitl_gate.py` — human-in-the-loop approval gate
- `dead_letter.py` — failed task handling and replay
- `history_manager.py` — session history and learning
- `loop.py` — scheduling and recurring tasks
- `tool_runner.py` — tool execution with HITL guards
- `context.py` — session context and state management

## Acceptance Criteria Status

| Criterion | Status |
|---|---|
| Obsolete capabilities removed and references reconciled | ✅ |
| Canonical brand tokens consistently applied | ✅ (src/ code updated) |
| Creative Director registered and invocable | ✅ (already existed) |
| Existing model router used | ✅ |
| Existing production application unaffected | ✅ |
| Structured creative brief accepted | — (Phase 3 demo) |
| Task classification and specialist routing | — (Phase 3 demo) |
| At least one knowledge/creative production workflow | — (Phase 3 demo) |
| Brand and artifact QA executed | — (Phase 3 demo) |
| Execution manifest produced | — (Phase 3 demo) |
| Human approval before final release | — (Phase 3 demo) |
| Output saved in correct location | — (Phase 3 demo) |
| Failure handling and rerun behavior | — (Phase 3 demo) |

## Phase 2: Architecture and Integration (Complete)

The Creative Director is established as the primary orchestration entry point
in code, not just on paper. New package `src/ai_company/creative/`
(implemented, tested — `tests/unit/test_creative_pipeline.py`, 32 tests,
97% coverage; architecture detail in `docs/CREATIVE-PRODUCTION-ARCHITECTURE.md`):

- **Structured creative brief** — `CreativeBrief` model enforcing the five-question
  intake (artifact type, audience, objective, narrative, visual language) plus
  handoff fields (structure, channels, CTA, QA scope, source research).
- **Execution manifest** — `ExecutionManifest` recording run id, brief, skill chain,
  agent assignments, model route, adapter availability, outputs, QA verdict,
  human approval (kept separate from QA), warnings, errors and rerun lineage.
  Persisted at `output/creative/<run_id>/manifest.json` after every stage.
- **Model router integration** — routing calls the existing `ModelRouter.resolve()`
  for the production specialist (per-agent overrides, tier rules, domain/task-type
  detection unchanged). No second routing system was created.
- **Creative Director routing table** — deterministic brief → skill chain
  (`ls-design-system` first, one production skill, `ls-artifact-qa` last) →
  specialist agent, validated against `company/agent-registry.json`.
- **Knowledge workflow connection** — content-heavy briefs without `source_research`
  (or with broken research paths) get explicit manifest warnings; production must
  not invent facts.
- **Replaceable tool adapters** — one interface, local-only probes, no paid APIs
  or external transmission: `presentation` (wired MVP backend), `opendesign`
  (probed, delegated to ls-od-* agent skills, not an MVP dependency),
  `comfyui` (loopback probe, not an MVP dependency).
- **QA + human approval gates** — deterministic QA floor (outputs exist, legacy red
  `#E63946` absent, canonical `#DC3641` present); approval is only offered after
  QA passes and is recorded separately (`qa_passed` ≠ `approved`); runs without an
  approver park awaiting CEO approval.
- **Failure and rerun** — adapter failures and missing adapters mark the run
  `failed` with the error recorded; reruns create a new run linked via `retry_of`.

Registry untouched (`company-registry.yaml` unchanged — registry baseline gate
preserved); no dashboard, port, or deployment changes.

## Deliverables

1. **Implementation summary** — Complete (this document)
2. **Final architecture diagram** — Interim ASCII architecture in `docs/CREATIVE-PRODUCTION-ARCHITECTURE.md` §1; final visual diagram in Phase 3
3. **List of removed capabilities and reconciled references** — Complete (above)
4. **Updated agent and skill assignments** — Creative Director registered; archify/rayden-code/k-dense-infographics removed
5. **Workflow execution trace** — To be produced in Phase 3 MVP demonstration
6. **MVP demonstration outputs** — To be produced in Phase 3
7. **QA evidence** — To be produced in Phase 3
8. **Outstanding limitations and dependencies** — Phase 3 will identify these
9. **Recommended next implementation phase** — Phase 3: MVP vertical slice

**Goal**: A production system, not another architecture document. The obsolete has been removed, the reusable has been retained, and the pipeline is ready for vertical slice demonstration.
