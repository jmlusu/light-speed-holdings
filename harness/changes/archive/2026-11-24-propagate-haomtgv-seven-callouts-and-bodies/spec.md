# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: plan-first
- Questions asked this round: 2
- Intake status: complete

## Goal And Evidence

- Real problem or user request: The user rewrote the H-A-O-M-T-G-V framework into seven short callouts plus expanded bodies, then asked to propagate those values to all relevant documents.
- Current behavior: Canonical docs, LinkedIn drafts, and website prose carry mixed older wording ("Memory runs sovereign", "Models run sovereign", "Gates approve", "Verification records it all") and longer pillar headings.
- Source of evidence: `docs/pharos/h-a-o-m-t-g-v-framework.md`, `docs/pharos/articles/h-a-o-m-t-g-v-seven-layers.md`, `docs/pharos/whitepaper/h-a-o-m-t-g-v-chapter.md`, `docs/pharos/linkedin-series/*`, `src/components/home/HAOMTGVSection.tsx`, `src/pages/HAOMTGVPage.tsx`.

## User Scenarios And Success

- Primary user/system scenario: A reader encounters the framework in the canonical doc, an article, a LinkedIn post, or the website and sees the same approved callouts and body copy.
- Success criteria: Every in-scope surface uses the seven approved callouts; the seven-clause line is consistent; no excluded surface was modified.
- Acceptance criteria: (1) Canonical one-line and memory-line table updated; (2) seven pillar headings and bodies updated in Tier 1; (3) LinkedIn sequence strings updated in Tier 2; (4) website prose updated in Tier 3; (5) tests/build/validation run; (6) no changes to excluded files.

## Non-Goals

- No visual assets (three SVGs, raster PNGs, visual generator template).
- No normalization of alternate pillar names in `docs/Pharos/positioning.md`, `docs/MASTER_SPEC.md`, `content/drafts/faq.md`, `USE-CASE-CATALOG.md`, `monitor-01.md`, `validate_evidence.py`.
- No short UI label renames in website components.
- No rewrites of historical/audit records.
- No root `haomtgv-committed.tsx` changes (stale artifact).

## Constraints

- Project root is `C:\Users\jmlus\light-speed-holdings`, not the session worktree.
- `main` is protected; work on branch `docs/haomtgv-callout-propagation`.
- Never `git add .`; stage by explicit path.
- PowerShell 5.1 shell rules from `AGENTS.md` apply.
- No `--no-verify`, no empty commits, no `git config` changes.

## Assumptions

- The plan presented in conversation and accepted by the user is the approved plan of record.
- The approved copy is the exact text recorded in `plan.md`.

## Open Questions

None.

## Resolved Clarifications

- Naming scope: canonical + sequence only (user decision 2026-11-24).
- Visual assets: docs and code only (user decision 2026-11-24).
- V pillar name: keep Value (user decision 2026-11-24).
- Callout length: two or three words (user instruction 2026-11-24).
