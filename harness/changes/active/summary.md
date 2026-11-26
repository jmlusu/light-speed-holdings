---
title: "Honest legacy redirects and visible IA"
slug: "honest-legacy-redirects-and-visible-ia"
status: "in_progress"
location: "active"
phase: "validate"
intake_status: "complete"
spec_review: "approved"
plan_review: "approved"
modules:
  - src/components
  - src/components/home
  - src/components/site
  - src/data
  - src/data/registries
  - src/brand/tokens
  - src/lib
  - src/__tests__
files:
  - src/App.tsx
  - src/components/home/VisitorPathsSection.tsx
  - src/components/home/WhatWeBuildGrid.tsx
  - src/components/home/InsightsSection.tsx
  - src/components/site/HonestyBadge.tsx
  - src/data/siteContent.ts
  - src/components/HeroSection.tsx
  - src/components/AboutSection.tsx
  - src/data/publicMetrics.ts
  - src/lib/enquiry.ts
  - src/lib/legacyRedirects.ts
  - src/components/site/LegacyRedirect.tsx
  - src/data/registries/faq-registry.json
  - src/brand/tokens/brand-tokens.css
  - vitest.config.ts
tags:
  - marketing-site
  - trust-and-clarity
  - accessibility
  - brand-governance
  - legacy-redirects
validation_status: "pass"
validation_results:
  - "Verification scope: LOCAL ONLY; CI not run — no push, no PR, no CI run, production deployment unverified"
  - "npm test (vitest): 210 passed across 22 files (local only; CI not run)"
  - "npm run build (tsc + vite build): PASS — one pre-existing esbuild file: CSS warning, not introduced by this change"
  - "Lighthouse GET http://localhost:1440/ (close-out, after c3754e7d): accessibility 1.00 / best practices 1.00 / SEO 1.00, zero failures"
  - "Impeccable detector: 5 warnings triaged — 3 previously accepted false positives plus 2 plan-mandated border-l-4 callouts; accepted in ledger"
  - "Per-task reviews: Tasks 0-5 APPROVED; Task 2 and Task 4 each clean after one fix round (0 open findings)"
  - "Whole-branch review: REQUEST CHANGES → one fix wave (a06504a1..da6dd7d1) → scoped re-review clean (3 addressed, 0 open)"
  - "Close-out Lighthouse gate: one label-content-name-mismatch fixed in c3754e7d; scoped re-review clean"
  - "git log main..HEAD: 10 commits present; working tree has only the pre-existing opencode.json edit and untracked plan/handoff docs"
created_at: "2026-11-25"
updated_at: "2026-11-26"
session_id: "eb616607-1d27-4ba4-a265-a9ca9f18eeed"
owner_agent: "jmlus"
claimed_at: "2026-11-25"
---

# Summary

## Outcome

All five workstreams in `docs/superpowers/plans/2026-11-25-marketing-site-trust-and-clarity.md` are implemented and reviewed on branch `fix/honest-legacy-redirects`, in ten commits (`git log --oneline main..HEAD`):

1. **Preflight isolation** — `9ef4476b` isolates the 19 pre-existing accessibility-polish `src/` files; `opencode.json` stays unstaged.
2. **Homepage decision load** — `76391fc8` keeps four primary audience paths outside a closed "More ways in" disclosure, gives six capability links unique accessible names, and collapses eight Pharos formats behind one disclosure; research and capability copy preserved.
3. **Honesty badge legibility** — `13c31427` adds AA-safe brand tokens; `8dc62f28` makes the evidence-chip test render the real `FaqCardList` (with the `@lightspeed/design-system` alias in `vitest.config.ts`). The four badge levels (`proven`, `pilot`, `fieldable`, `development`) are unchanged.
4. **Canonical brand voice** — `221d479a` renders `humanAuthorityStatement` ("AI executes. Humans decide.") from the registry on `/` and `/about` and replaces green trust/status colours with cyan; the red sweep replaced 24 `#DC3641` tokens, not the 20 estimated.
5. **Claims evidence** — `06463ab2` grounds public metric tiles in publishable claim IDs and removes unquantified/absolute promises; `1aa99c12` removes the stale response-SLA note from the FAQ registry.
6. **Redirects and IA** — `a06504a1` makes legacy redirects single-hop with a visible moved notice and preserves destination SEO, and points Ask LightSpeed at `/contact`.

Close-out fixes `da6dd7d1` (theme-aware cyan text) and `c3754e7d` (visible text in capability-link accessible names) followed the whole-branch and Lighthouse gates. The complete changeset is `git diff --name-only main..HEAD`.

## Decisions

- **Branch isolation:** Task 0 committed the pre-existing 19-file accessibility polish separately (`9ef4476b`); `opencode.json` was excluded and remains an unstaged user change. No stash, reset, clean, or restore of user files.
- **File ownership / sequencing:** Task 1 lands before Task 5 on `VisitorPathsSection.tsx` (`/ask` → `/contact`); Task 2 owns badge tokens and the shared badge map, Task 3 only verifies tokens; Task 3 lands before Task 4 so claims edits preserve brand hunks.
- **Real-component test:** accepted one extra staged file (`vitest.config.ts`) with the design-system alias so `honestyBadge.test.tsx` imports the actual `FaqCardList` instead of copying JSX. The pre-fix test was a genuine defect, found and fixed in Task 2 round 1.
- **Brand constraint is binding:** Task 3 took option A — replace every `#DC3641` occurrence across the nine reported files (24 actually replaced), rather than narrowing the test or leaving a known brand fracture. Canonical counts (90 roles = 89 agents + 1 human CEO, 20 departments, 5 governance tiers) were not changed.
- **No invented claims:** no claim was added for "100% audit trail coverage"; no published response-time SLA survives. Every public surface imports the single non-promissory `ENQUIRY_RESPONSE_COPY`.
- **Close-out scope:** the Lighthouse `label-content-name-mismatch` finding came from a different gate than the final review, so one scoped component + test fix (`c3754e7d`) and re-review were authorised — not a second final-review wave.
- **Review capacity:** the paid reviewer model had insufficient balance; all review seats used the free `opencode/hy4-flash-free` model, mitigated by task briefs, the ledger, report packages and full diffs.
- **Deferred minors:** all reviewer minors were recorded in the SDD ledger for triage (Step 3 of the handoff); none were silently dropped. Two new Impeccable `border-l-4` warnings were accepted as plan-mandated canonical-line treatment.

## Validation

**Scope: local only; CI not run.** No push, no PR, no CI checks, no production deployment. CI status is unverified and must be read from `gh` output after authorisation.

- `npm test` — **210 passed, 22 files**, after the final close-out fix (`c3754e7d`).
- `npm run build` — TypeScript check and Vite build passed; one pre-existing esbuild `file:` CSS warning, not introduced here.
- Lighthouse on `http://localhost:1440/` after `c3754e7d` — accessibility **1.00**, best practices **1.00**, SEO **1.00**, **zero failures** (plan's close-out gate).
- Impeccable detector — 5 warnings, all triaged in the ledger: 3 previously accepted false positives (`border-l-4` blockquote, `slate-950` on `cyan-500`, nav `border-l-2`) and 2 plan-mandated `border-l-4` canonical-line callouts.
- Reviews — Tasks 0–5 approved; Task 2 and Task 4 each needed one fix round; whole-branch review needed one fix wave (`da6dd7d1`); the close-out Lighthouse gate needed one aria-label fix (`c3754e7d`). All re-reviews clean.
- `git log --oneline main..HEAD` shows the expected 10 commits; `git status --short --branch` shows only the pre-existing `opencode.json` modification plus untracked plan/handoff docs.

Not verified: CI, remote branch state, production. Evidence sources: `.superpowers/sdd/2026-11-25-marketing-site-trust-and-clarity/progress.md` and `docs/superpowers/handoffs/2026-11-26-marketing-site-trust-and-clarity.md`.

## Next Step

1. **CEO authorisation, then push and open the PR** (handoff Step 1): `git push -u origin fix/honest-legacy-redirects`, then `gh pr create --base main --head fix/honest-legacy-redirects` with the full PR template including the Surface area checklist. Report CI from `gh pr checks` / `gh run view` only.
2. **Finish the harness record** (this step): `plan.md` remains a generated stub and is outside this task's edit whitelist; assign it to the governance owner before archive.
3. **Triage deferred minors** (handoff Step 3): reviewer rulings in the ledger — `qa-lead` for contrast/test items, `cmo` for copy, `cto` for component colours, `clo` for registry copy.
4. **Decide the deeper product critique** (handoff Step 4): `cpo` + `cmo` + `thought-leadership-lead`, with CEO sign-off on claims.
5. **Before archive only after green CI:** update `docs/STATUS.md`, verify archive hygiene (no side-effect files dirty), run `harness-change.ps1 close completed`, then `lint-ecl.ps1`. Archive is deliberately not performed here.
