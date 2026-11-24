# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation. Approved plan of record confirmed.

## Implementation

- [x] T002 [P] Tier 1: rewrite one-line, memory-line table, seven headings and bodies in `docs/pharos/h-a-o-m-t-g-v-framework.md`, `docs/pharos/articles/h-a-o-m-t-g-v-seven-layers.md`, `docs/pharos/whitepaper/h-a-o-m-t-g-v-chapter.md`.
- [x] T003 [P] Tier 2: replace sequence strings in the 11 LinkedIn drafts, companion copy, and `scripts/maintenance/enqueue_post1.py`.
- [x] T004 [P] Tier 3: rewrite prose (not labels) in `src/components/home/HAOMTGVSection.tsx` and `src/pages/HAOMTGVPage.tsx`.
- [x] T004a Repair three `faq-evidence.test.ts` anchors in `src/data/registries/faq-registry.json` broken by the Tier 3 copy change (test was red until fixed).

## Validation

- [x] T005 Grep in-scope files for old callout strings; verify zero survivors.
- [x] T006 Run `git diff --check`, frontend typecheck/tests/build, Python checks, full pytest, and ECL lint.
- [ ] T007 Commit by explicit path, push branch, open PR, read CI with `gh pr checks`.
- [ ] T008 Close ECL change and update `docs/STATUS.md`.

## Deferred Tasks

- Visual assets, alternate-name docs, historical records, root `haomtgv-committed.tsx` — out of scope by user decision.
