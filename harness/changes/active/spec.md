# Spec

## Intake Review

- Intake type: Structured Change (plan-first; five sequenced workstreams, ten commits)
- Input shape: plan-first — `docs/superpowers/plans/2026-11-25-marketing-site-trust-and-clarity.md`, cross-checked against `PRODUCT.md`, `DESIGN.md`, the SDD ledger and git history
- Questions asked this round: 0 at intake. Ambiguities that surfaced during execution (Task 3 red-token scan scope, close-out Lighthouse failure, review model) were resolved by ledger rulings, not new intake questions.

## Goal And Evidence

- Real problem or user request: the public marketing site asked visitors to make too many homepage choices; honesty badges were rendered at 10px with non-AA ink and green/amber trust signals; public copy carried an unmeasured "100% audit trail coverage" claim and a two-business-day response promise; legacy URLs redirected without explaining the move; and the canonical human-authority line was not rendered from the registry.
- Current behavior (before this change): four audience paths plus five secondary links and eight Pharos formats all visible at once; six capability links shared one accessible name; FAQ evidence chips used green/amber; About tiles published unbadged absolute percentages; enquiry surfaces promised a response window; legacy paths redirected silently; green status tokens and an off-brand `#DC3641` red survived in marketing sources.
- Source of evidence: `docs/superpowers/plans/2026-11-25-marketing-site-trust-and-clarity.md` (goal, review focus, global constraints, task tests), `PRODUCT.md` and `DESIGN.md` (reachable specs), `.superpowers/sdd/2026-11-25-marketing-site-trust-and-clarity/progress.md` (rulings, fix rounds, deferred minors), `docs/superpowers/handoffs/2026-11-26-marketing-site-trust-and-clarity.md`, and `git log --oneline main..HEAD` (10 commits: 9ef4476b, 76391fc8, 13c31427, 8dc62f28, 221d479a, 06463ab2, 1aa99c12, a06504a1, da6dd7d1, c3754e7d).

## User Scenarios And Success

- Primary user/system scenario: a visitor arrives at `/`, sees one primary decision per section (four audience paths; one research link; six uniquely named capability links), can open a closed disclosure for deeper material, reads evidence-labelled claims with legible badges, follows an existing legacy URL through a single hop to the canonical page with a visible "moved" notice, and encounters one canonical brand voice ("AI executes. Humans decide.") on `/` and `/about`.
- Success criteria: (1) homepage tests preserve every audience, secondary destination and all eight Pharos format labels while exposing only four primary paths and one research link outside disclosures; (2) four honesty tones keep AA contrast in light and dark with no new badge level and no green/amber trust signal; (3) every public metric tile carries a publishable `claimId` and a badge, with no `100%` absolute and no response-time promise; (4) legacy redirects resolve in one hop, show a visible notice, and keep destination SEO metadata; (5) the canonical line is imported from the registry, not hardcoded, in both root `HeroSection` and `AboutSection`.
- Acceptance criteria: `npm test` green (210 passed across 22 files after the close-out fix), `npm run build` green (only the pre-existing esbuild `file:` CSS warning), Lighthouse on preview `http://localhost:1440/` at 1.00/1.00/1.00 with zero failures, and per-task plus whole-branch reviews approved with all findings closed. All verification is local only; CI is not part of this record.

## Non-Goals

- No changes to the CEO Dashboard (`src/ai_company/`, `company-registry.yaml`, dashboard ports 8420/8421) — the marketing Vite app and dashboard are separate applications.
- No change to canonical counts, honesty badge levels, evidence vocabulary (`verified`/`unknown`), or badge label mapping.
- No new public claim without a registry source; no reintroduction of absolute percentages or response-time SLAs.
- No push, PR, CI run, merge, or production deployment in this change record.
- No enterprise proof narrative (named clients, testimonials, prices, timelines), regulator evidence pages, or second homepage simplification pass — those are post-launch product decisions in handoff Step 4.
- No paid reviewer model, no Impeccable/DESIGN.md rewrite, and no restaging of `opencode.json` or the untracked plan/handoff documents.

## Constraints

- Brand is fixed: navy `#070A40`, red `#E63946`, cyan `#00BFFF`, Arial-only typography, 4px spacing grid; cyan is the sole trust/status signal. Green, amber and the duplicate `#DC3641` red are removed from audited marketing sources.
- Canonical counts are test-enforced: 90 roles = 89 agents + 1 human CEO, 20 departments, 5 governance tiers.
- Every public claim must be registry-backed; `AGENTS.md` §7 forbids invented evidence, metrics, source anchors, or explanations.
- Marketing ports are dev 1441 and preview 1440 only; never bind dashboard ports 8420/8421.
- Windows/PowerShell 5.1 shell: no `head`, `tail`, `sed`, `$?`, `2>/dev/null`, `&&`/`||` chaining.
- Git guardrails: `main` protected (6 checks); work on the existing branch; never `git add .`/`-A` (stage by explicit path), `--no-verify`, empty commits, `git config` changes, or destructive restore/clean/reset of files not created in-session. "Done" is CI-verified; otherwise label local only.
- File-ownership contract: one task owns a file at a time (Task 1 before Task 5 on `VisitorPathsSection.tsx`; Task 2 before Task 3 on tokens; Task 3 before Task 4 on `AboutSection.tsx`).
- `opencode.json` is a pre-existing unstaged user edit; the plan and handoff documents are untracked. Neither is staged or modified by this change.

## Assumptions

- `src/data/shipped/company.ts` and the registries under `src/data/registries/` are the authoritative sources for counts, claims and the canonical line; no new source of truth was introduced.
- "AI executes. Humans decide." is the canonical `humanAuthorityStatement`; both public render sites import it rather than hardcoding it.
- Local `npm test`, `npm run build` and Lighthouse runs recorded in the ledger are valid evidence of local correctness but not of CI; CI remains unverified until `gh` reports it.
- The ten commits listed above are the whole branch delta from `main`; the working tree contains no additional implementation changes beyond the ECL record completion.
- Deferred minors listed in the ledger are accepted for post-merge triage and do not block the agreed scope.

## Open Questions

- None open. Every high-impact ambiguity raised during the work was resolved by a recorded ledger ruling (see Resolved Clarifications).

## Resolved Clarifications

- **Task 3 red-token scan scope:** the brief's `#DC3641` test scanned all `.ts/.tsx` under `src/components`, `src/site`, `src/pages` while Step 6 named only two files. Ruling: option A — replace all occurrences across the nine reported files; the implementer replaced 24 tokens, not the 20 estimated at ruling time.
- **Honesty badge test contract:** the pre-fix test copied JSX instead of rendering the real `FaqCardList`. Ruling: allow `vitest.config.ts` to gain the design-system alias as one extra staged file in Task 2 fix round 1; no production behaviour change.
- **Task 4 registry contradiction:** the FAQ note said no basis existed for a response-time promise while the answer still published windows. Ruling: remove the stale source note in `1aa99c12`; keep the single `ENQUIRY_RESPONSE_COPY` line and no SLA.
- **Close-out Lighthouse failure:** `label-content-name-mismatch` on six `aria-label="Explore …"` links with visible `EXPLORE CAPABILITY`. Ruling: evidence from a different gate, not a second final-review wave — one scoped component + test fix authorised (`c3754e7d`) followed by clean re-review.
- **Impeccable warnings:** 3 previously accepted false positives stand; 2 new `border-l-4` callouts were accepted because the plan prescribed that treatment verbatim.
- **Review model:** paid `claude-sonnet-5-5` failed with insufficient balance; free `hy4-flash-free` used for all review seats, mitigated by briefs, full diff packages and the whole-branch review.
