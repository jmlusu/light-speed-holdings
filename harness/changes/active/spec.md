# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first (audit-driven next steps from 2026-10-10 narrative-claims audit)
- Questions asked this round: 3 (gate-conflict handling, wording approval, pending evolution)

## Goal And Evidence

- Real problem or user request: The narrative-claims audit (`docs/AUDIT-NARRATIVE-CLAIMS-2026-10-10.md`) found 7 claims (CL-01..CL-07) in `docs/NARRATIVE-AND-POSITIONING.md` that are UNSUPPORTED or MISLEADING against internal artifacts, and it left three next steps: (1) correct the claims (ECL-controlled doc), (2) reconcile the Offer B/C gate conflict (briefing only, decision deferred), (3) re-verify audit line citations.
- Current behavior: `NARRATIVE-AND-POSITIONING.md` still asserts clinic/WhatsApp, NGO donor-report, and Offer E licensee outcomes as shipped/measured; policy doc + `src/ai_company/services/client_intake.py:44` block Offer B/C while `config/company/malawi_offers.yaml` shows the unblock condition ratified (`blocked_offers: []`).
- Source of evidence: audit report CL matrix; `USE-CASE-CATALOG.md:116/:229/:382/:507/:510/:518`; `NARRATIVE-AND-POSITIONING.md:27/:29/:92/:153/:203`; `malawi_offers.yaml`; `client-onboarding-policy.md:36-41`.

## User Scenarios And Success

- Primary user/system scenario: Human CEO reviews corrected narrative wording (draft-first, approval before apply); CEO/CLO later consumes the gate briefing; agents/docs consumers get an accurate narrative.
- Success criteria: all 7 claims rewritten to match verified artifact status; no claim stronger than its artifact; citations in the audit verified against live files.
- Acceptance criteria: user approves wording before any NARRATIVE edit; `lint-ecl.ps1` PASS; `pytest tests/docs/` PASS; full non-e2e suite PASS at archive; briefing saved under `reviews/`.

## Non-Goals

- No change to `src/` (`client_intake.py` stays untouched); decision on Offer B/C gate is deferred to the human CEO/CLO.
- No edits to `config/company/malawi_offers.yaml` or `docs/legal/client-onboarding-policy.md`.
- No commits (not requested); no handling of `harness/evolution/pending.md`; no touching pre-existing dirty working-tree files.

## Constraints

- `docs/NARRATIVE-AND-POSITIONING.md` may only be modified inside this ECL change (its own governance note, line 225).
- ADR-020 / `EVIDENCE_ARCHITECTURE.md`: claims require T1/T2 evidence or T3 CEO approval; honesty rule beats persuasion.
- Only one active change; wording requires explicit user approval before apply (user decision 2026-10-10).
- Do not hand-edit `harness/changes/INDEX.json`.

## Assumptions

- The audit's `USE-CASE-CATALOG` line citations that matched on spot-check (116/229/382/507/510/518) will survive the full sweep, or will be corrected in the audit doc.
- `thought-leadership-author` and `chief-of-staff` are valid `subagent_type` values (roster check); `ecl-harness-engineer` is used as a skill only.

## Open Questions

- None.

## Resolved Clarifications

- Gate conflict → briefing only, decision deferred (user, 2026-10-10).
- Claim wording → draft, user review, then apply (user, 2026-10-10).
- Pending evolution → ignore for now (user, 2026-10-10).
