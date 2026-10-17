# Plan

## Technical Approach

- **P1 Census (done 2026-10-07, read-only):** programmatic counts — registry 90 agents (89 AI + `human_ceo`; types 19 executive / 64 specialist / 7 board) across 20 departments (per-dept table in `summary.md`); `company/departments.yaml` 20 entries incl. `pharos`; `company/agent-registry.json` 90; `.opencode/agents/*.md` 90. Data layer needs no fix; work is comment/prose reconciliation.
- **P2 Scoped edits (6 files):**
  1. `docs/source-of-truth.yaml` — replace line-23 "has 19 (missing pharos)" comment with reconciled note (20 incl. `pharos`, #421).
  2. `docs/NARRATIVE-AND-POSITIONING.md` — §§5e/5f/§7-bullet/§9(j): "has 19 — must be reconciled" → "reconciled at 20 incl. `pharos` per #421"; §7 line-142 "say 152" → "say 90".
  3. `docs/EXECUTIVE-STRATEGY-EXPANSION.md:8` — "145 specialized agents" → "90 specialized agents (89 AI + 1 human CEO)".
  4. `docs/marketing/warmup-content-pack/linkedin-post.md:60` — parenthetical "(152 agent entries …)" → "(90 agent entries …, reconciled #421)"; claim text already 90.
  5. `docs/Pharos/linkedin-intro-post.md:94-99` — "152 agent entries" → "90 agent entries" + pre-trim qualifier; dated ground-truth row otherwise untouched.
  6. Triaged no-change: `docs/MASTER_SPEC.md:105-115` (intentional do-not-use guard), `docs/Pharos/linkedin-series/post-11/video-script.md:13,22` (intentional 152→90 story beats per ADR-025), all STATUS/CHANGELOG/archive history.
- **P3 Verify:** ruff + mypy + generator (90/0 errors) + `sync-registry --verify` + `validate-drift.ps1` + `validate-architecture.ps1` stale-claims + doc drift/count tests + full non-e2e `pytest`; record in `validation_results`; close `completed`.

## Impacted Modules And Files

- `docs/source-of-truth.yaml` — comment-only (no `current_value` change: still 20/90).
- `docs/NARRATIVE-AND-POSITIONING.md` — prose reconciliation only.
- `docs/EXECUTIVE-STRATEGY-EXPANSION.md` — one live count fix.
- `docs/marketing/warmup-content-pack/linkedin-post.md`, `docs/Pharos/linkedin-intro-post.md` — fact-check row fixes.
- `harness/changes/active/*` — ECL records only.
- No `src/` changes; no schema/config/behavior changes.

## Interfaces, Data, Permissions

- No interfaces, data shapes, or permissions change. Drift-manifest `current_value` fields (20/90) unchanged; only a stale code comment is corrected.

## Spec Gaps Found From Planning

- Issue body says "Fix company/departments.yaml 19->20 (missing Pharos)" but the file already holds 20 entries incl. `pharos` (verified programmatically). Gap resolved as comment/prose reconciliation, recorded in spec assumptions — no data fix required.

## Risks And Mitigations

- NARRATIVE doc-control footer ("Do not hand-edit") → mitigated: edits ride this ECL change through validate/close.
- Concurrent sessions editing shared files (known hazard) → `git status` snapshot before/after full suite; isolated `--basetemp`.
- Drift-gate false positives from blanket `\d+ agents` patterns → mitigated: edited rows keep the canonical 90/20 figures; history untouched per allowlists.

## Verification Plan

- `uv run ruff check src/` clean; `uv run mypy src/` clean.
- `AgentGenerator().generate_all()` → 90 agents / 0 errors; `ai-company sync-registry --verify` pass.
- `pytest tests/docs/test_doc_drift.py tests/docs/test_doc_agent_counts.py` green; `pwsh scripts/maintenance/validate-drift.ps1` green; `pwsh scripts/maintenance/validate-architecture.ps1` stale-claims check green; `pwsh scripts/maintenance/lint-ecl.ps1` green.
- Full non-e2e `pytest` to completion; results in `summary.md validation_results`; `validation_status: pass`, `phase: validate` before close.
- Grep gates: `145 agent|152 agent|140+ agent` in edited files → zero live claims; `has 19|missing.*pharos` → only archive/harness history.
