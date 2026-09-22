# Plan

## Overview

This change produces the **LightSpeed Narrative & Positioning Document** — a single canonical artifact covering all 13 mandated sections (What LightSpeed is/is not; Who it serves; Problems it solves; Core capabilities; Differentiators; Strategic thesis; AI-native philosophy; Strategy → Build → Govern → Research model; Malawi → SADC → Africa ambition; Approved terminology; Claims that can/cannot be made; Brand/system integration points; Roster validation). The document becomes the source-of-truth for all 152 agents (151 AI + 1 human CEO) across 20 departments, replacing fragmented positioning across Pharos, USE-CASE-CATALOG, MISSION_AND_VISION, and the brand system.

## Technical Approach

1. **Finish recon** (already complete): Last reads confirmed — `COMPANY-CONSTITUTION.md`, `ORGANIZATION.md`, `brand-guidelines.md`, `company-registry.yaml` reviewed. Key assets catalogued: Pharos positioning (3 territories + H→A→O→M→T→G→V), brand palette (navy/red/cyan, Arial, 4px grid), mission/vision/values (Malawi first / Prove it / Then the world), USE-CASE-CATALOG positioning ("The AI-native company builder for Southern Africa" / "ASPIRE. ACT. ACHIEVE."), source-of-truth.yaml (20 departments / 152 agents), company-registry.yaml (151 AI + 1 human CEO). Graphify graph (`graphify-out/graph.json`) already indexed.

2. **Open ECL change** — already done: `harness-change.ps1 new "Narrative and Positioning Track..."` created active change in `intake` phase. `summary.md`, `spec.md`, `plan.md` now populated.

3. **Dispatch agent team** from validated roster: select 8–10 agents from candidate list (thought-leadership-lead, thought-leadership-author, brand-strategist, product-marketing-manager, knowledge-manager, cso, cmo, chief-of-staff; optionally community-ecosystem-builder, ai-ethics-officer, ai-safety-lead). Each agent receives a per-agent brief (strategy/thesis, CEO-voice narrative, brand/positioning, marketing/messaging, knowledge/terminology, Malawi→SADC→Africa, governance/claims). Drafts collected.

4. **Integrate drafts with existing assets** into one canonical LightSpeed Narrative & Positioning Document:
   - Section 1–6 (What, Who, Problems, Capabilities, Differentiators, Strategic thesis): authored from drafts + existing positioning (Pharos 3 territories + H→A→O→M→T→G→V framework; USE-CASE-CATALOG tagline; MISSION_AND_VISION mission/vision/values).
   - Section 7 (AI-native philosophy): drafted from brand system (navy/red/cyan, Arial, 4px grid, ASPIRE. ACT. ACHIEVE. tagline, ™ usage) + source-of-truth.yaml claims.
   - Section 8 (Strategy → Build → Govern → Research model): newly authored (no prior artifact).
   - Section 9 (Malawi → SADC → Africa ambition): drafted from Pharos throughline "building → evidence → policy" + Malawi HQ context.
   - Section 10 (Approved terminology): assembled from brand-guidelines.md (navy/red/cyan, Arial, 4px, ™, no emojis, no generic AI commentary), Pharos positioning NOT to position as AI Expert/Consultant/Engineer, USE-CASE-CATALOG honesty_classification.
   - Section 11 (Claims that can/cannot be made): reconciled from mission/vision ("140+ AI agents" vs canonical 152), source-of-truth.yaml counts (20 departments / 152 agents), company-registry.yaml (151 AI + 1 human CEO). Note discrepancy and document resolution.
   - Section 12 (Brand/system integration points): cross-reference brand tokens, Pharos skills (`ls-design-system` mandatory before any creative), `docs/Pharos/` asset map, `brand-guidelines.md` compliance checklist (logo from official assets, clear space, palette only, vector for print, ™ on first mention, type sizes from scale, tagline "ASPIRE. ACT. ACHIEVE.").
   - Section 13 (Roster validation): validate chosen agent names against system-prompt roster (skill names ≠ subagent_type); record which names were accepted/rejected; note any gaps.

5. **Validate and close change**: Run `scripts/validate-drift.ps1`, `tests/docs/test_doc_drift.py`, and `pwsh scripts/lint-ecl.ps1`; record `validation_results` in `summary.md` front matter `phase: validate`; then close the change via `harness-change.ps1 close`.

## Impacted Modules And Files

- `harness/changes/active/summary.md` — change metadata (already created)
- `harness/changes/active/spec.md` — filled above
- `harness/changes/active/plan.md` — filled above
- `docs/NARRATIVE-AND-POSITIONING.md` — final canonical document (to be written after draft collection)
- `docs/source-of-truth.yaml` — may need updating if new canonical claims added (currently: 20 departments / 152 agents)
- `company/departments.yaml` — has 19 (missing pharos); reconcile or note as pending
- `docs/Pharos/positioning.md` — integrated (3 territories + H→A→O→M→T→G→V framework)
- `docs/client-facing/USE-CASE-CATALOG.md` — integrated (positioning node + tagline)
- `docs/MISSION_AND_VISION.md` — integrated (mission/vision/values, 140+ vs 152 note)
- `brand/tokens/brand-tokens.json`, `brand/guidelines/brand-guidelines.md` — integrated (palette, type scale, ™ rules)
- `scripts/validate-drift.ps1`, `tests/docs/test_doc_drift.py` — run at validate phase
- `pwsh scripts/lint-ecl.ps1` — run at close phase

## Interfaces, Data, Permissions

- Agent dispatch uses `task` subagent_type (validated against system-prompt roster, NOT skill names).
- `summary.md` front matter `phase` transitions: intake → plan → implement → validate → close.
- `validation_results` front matter block required when entering `validate` phase; format per ECL.md §3.2.
- No new API keys, domains, or Resend resources required.

## Risks And Mitigations

| Risk | Mitigation |
|------|-----------|
| R1: Roster name validation fails (skill name ≠ subagent_type) | Validate chosen names against the system-prompt agent roster *before* dispatch; if a name isn't a known subagent_type, pick a valid roster entry or do the work directly. |
| R2: "Strategy → Build → Govern → Research" model feels forced or inauthentic | Model is newly authored; iterate with CEO (jmlus) brief until voice feels authentic. Document rationale in section 8. |
| R3: 140+ vs 152 agent count discrepancy triggers claims-gate scrutiny | Acknowledge discrepancy in section 11; document that mission/vision text says "140+ AI agents" while canonical registry/source-of-truth say 152; resolution: update mission/vision text or add clarifying note. |
| R4: Phapos 3-territory framework conflicts with new strategic thesis | Integrate: thesis sits under "Strategic thesis" section; three territories documented as existing positioning, not overwritten. |
| R5: ECL change blocks if another agent starts a change first | ECL rule: only one active change at a time. If conflict arises, park/close current change before starting new. Already handled. |

## Verification Plan

1. After draft collection, run `uv run ruff check src/ && uv run mypy src/ && uv run pytest` to confirm no regressions in source code.
2. Run `pwsh scripts/lint-ecl.ps1` to verify ECL change compliance (change context, phase transitions, INDEX.json not hand-edited).
3. Run `scripts/validate-drift.ps1` and `tests/docs/test_doc_drift.py` to validate doc drift against `source-of-truth.yaml` and `company-registry.yaml`; confirm counts: 20 departments, 152 agents.
4. If `summary.md` `validation_results` block is populated with all green, close change via `harness-change.ps1 close`.
5. If any step fails, re-open the change, address the finding, and re-run verification.

## Next Step

- Dispatch the agent team (selected from validated roster) with per-agent briefs.
- Collect drafts.
- Integrate into canonical `docs/NARRATIVE-AND-POSITIONING.md`.
- Run verification scripts.
- Close the ECL change.
