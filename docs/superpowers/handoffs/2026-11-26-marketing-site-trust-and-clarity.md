# Handoff — Marketing Site Trust and Clarity (2026-11-26)

**For:** the next agent team
**From:** the session that executed `docs/superpowers/plans/2026-11-25-marketing-site-trust-and-clarity.md`
**Status:** implementation complete locally; **nothing pushed, no PR, no CI run**. Treat all verification below as **local only**.

---

## 1. Situation in one paragraph

The five workstreams in the plan are implemented and reviewed: homepage decision load was reduced, honesty badges made legible, unsupported public claims removed or grounded, the canonical human-authority line rendered, and legacy redirects made honest with a visible notice. Ten commits sit on branch `fix/honest-legacy-redirects`, based on `main`. A whole-branch review passed after one fix wave, and the plan's close-out gate (Lighthouse on preview 1440) is clean. The remaining work is governance, publication, and deeper product decisions — not more implementation of the agreed scope.

## 2. Exact current state

Run these first; do not assume this document is fresher than git:

```powershell
git status --short --branch
git log --oneline main..HEAD
```

Expected at handoff time:

- Branch: `fix/honest-legacy-redirects`
- `git log --oneline main..HEAD` (newest first):
  - `c3754e7d` fix(a11y): include visible text in capability link accessible names
  - `da6dd7d1` fix(a11y): make cyan text theme-aware on light and dark surfaces
  - `a06504a1` fix(site): make legacy redirects honest and surface canonical IA
  - `1aa99c12` fix(data): remove stale response-SLA source note from FAQ registry
  - `06463ab2` fix(site): ground public metrics and remove unsupported response SLA
  - `221d479a` feat(brand): render canonical human-authority line and replace green status with cyan
  - `8dc62f28` fix(test): verify real FAQ evidence-chip rendering in honesty badge test
  - `13c31427` Make honesty badges legible with AA-safe brand tokens
  - `76391fc8` fix(home): reduce homepage decision load while preserving research and capability copy
  - `9ef4476b` fix(site): make marketing site accessible and per-route SEO correct
- `opencode.json` is modified in the working tree by a previous user action (removal of the gbrain MCP entry). **Do not stage, revert, or overwrite it.**
- `docs/superpowers/plans/2026-11-25-marketing-site-trust-and-clarity.md` is untracked. Do not add it to task commits unless asked.
- SDD workspace (git-ignored) holds the ledger, briefs, reports and review packages:
  `C:\Users\jmlus\light-speed-holdings\.superpowers\sdd\2026-11-25-marketing-site-trust-and-clarity\progress.md`
  Read this ledger before deciding anything — it contains every ruling made on the CEO's behalf and the deferred-minor list.

## 3. What is verified (local only)

- `npm test` — 210 tests passed (22 files) after the final close-out fix.
- `npm run build` — TypeScript check and Vite build succeeded. One pre-existing esbuild warning about a `file:` CSS property; not introduced by this work.
- Lighthouse on `http://localhost:1440/` — accessibility **1.00**, best practices **1.00**, SEO **1.00**, **zero failures**.
- Impeccable detector — 5 warnings: three previously proven false positives (blockquote `border-l-4`, `slate-950` on `cyan-500`, nav active-state `border-l-2`) plus two `border-l-4` callouts prescribed verbatim by the plan for the canonical line. All documented in the ledger.
- Per-task reviews: Tasks 0–5 all approved; Task 2 and Task 4 each needed one fix round; the whole-branch review needed one fix wave; the close-out Lighthouse gate needed one small aria-label fix. All re-reviews clean.

**Not verified:** CI, remote branch state, production deployment. A PR exists only if `gh pr create` output shows it.

## 4. Governance and constraints (read before any git)

Read in this order:

1. `AGENTS.md`
2. `.ai-company/constitution/16-AGENT-GUARDRAILS.md`
3. `docs/ECL.md` (if creating/changing a change record)

Hard rules carried forward:

- `main` is protected (6 required checks). Work on the existing branch; merge only when checks are green.
- Never `git add .` / `git add -A`; stage by explicit path. Never `--no-verify`, empty commits, `git config` changes, stash/reset/clean/restore of files you did not create.
- Do not touch `opencode.json` or the untracked plan document.
- Marketing-site ports are 1441 (dev) and 1440 (preview). Never bind 8420/8421 (CEO Dashboard).
- Brand is fixed: navy `#070A40`, red `#E63946`, cyan `#00BFFF`, Arial-only, 4px grid, cyan is the only trust/status colour. Canonical counts 90 roles = 89 agents + 1 human CEO, 20 departments, 5 governance tiers.
- Every public claim must be registry-backed; do not invent evidence.

## 5. Next steps, in order

### Step 1 — Get CEO authorisation, then push and open a PR

Pushing and opening a PR are external side effects and were deliberately not done. Ask the CEO explicitly. Once authorised:

```powershell
git push -u origin fix/honest-legacy-redirects
gh pr create --base main --head fix/honest-legacy-redirects --title "Marketing site trust and clarity" --body-file <prepared-pr-body>
```

Fill the PR template (` .github/pull_request_template.md `) completely, including the Surface area checklist (UI and CLI are both relevant to this repo; explain any non-applicable box). Then watch with `gh pr checks <n>` / `gh run view`; do not re-run local tests and call it CI monitoring. If CI status cannot be read, say so and ask.

### Step 2 — Complete the ECL change record

Task 5 created change records via `harness-change.ps1 new`, but they remain generated stubs (`phase: intake`, all Pending) at:

- `harness/changes/active/summary.md`
- `harness/changes/active/spec.md`
- `harness/changes/active/tasks.md`
- `harness/changes/active/reviews/review.md`

Owner: `ecl-harness-engineer`. Fill phase, validation results, spec review, and plan review per `docs/ECL.md` §4–§5 before attempting archive. Do not archive with `phase: plan` or `validation_status: unknown`.

### Step 3 — Triage the deferred minors

Point the reviewer at the ledger's `minor (deferred)` lines. Suggested owners: `qa-lead` for test/contrast items, `cmo` for copy, `cto` for component colours, `clo` for registry copy.

- `src/design-system/components/Logo/Logo.tsx` still has three `#DC3641` values (outside the public site's current render path — verify before spending effort).
- Flat-surface contrast test in `honestyBadge.test.tsx` uses `#FFFFFF`/`#070A40`, not 10% tints.
- Pre-existing build warning (esbuild `file:` CSS property) and CRLF→LF diff notes.
- `OperatingModelOverview.tsx` sibling cyan pillars and inspector badge still use `text-ls-cyan` on light surfaces; the V pillar was fixed, the siblings were not.
- `InsightsSection.tsx:121` hover class now equals the light-mode base, so light hover gives no extra visual feedback.
- `faq-registry.json` faq-28 answer still publishes one-week / 2–3-week windows while its note says no basis exists. The public FAQ component renders `src/data/faqs.ts`, which no longer has those windows — confirm before changing copy.
- Duplicate canonical enquiry sentence in the CTA band (`CtaBand.tsx` text prop plus built-in footnote).
- Task 5 duplicate `role="status"` + `aria-live="polite"` annotation (brief-mandated) and jsdom `scrollTo` warnings in test output.

Rule on each; do not silently drop them. Record rulings in the ledger.

### Step 4 — Decide whether to act on the deeper product critique

The design review's unresolved findings are product decisions, not defects:

- The site still reads as a competent AI consultancy; the proprietary mechanisms (approval matrix, HAOMTGV glyphs, registry IDs) are text labels inside a generic shell.
- Enterprise visitors get no named client, testimonial, outcome case, price, or timeline.
- Regulators get governance vocabulary but no named counsel, no MACRA/SADC/UNDP evidence, and no explicit data-residency commitment on the main pages.
- Six identically named capability links were fixed with unique accessible names, but the homepage still asks visitors to make many choices; consider a second simplification pass after launch data.
- The honesty badge system is now legible, but the badge *meaning* still needs evidence upkeep.

Owner: `cpo` + `cmo` + `thought-leadership-lead`, with CEO sign-off on claims.

### Step 5 — Impeccable tooling follow-up

Impeccable was updated in this session from v4.3.1 to **v4.11.1** (engine v0.1.31) at `C:\Users\jmlus\.config\opencode\skills\impeccable`. The updater's doctor also reported:

- `DESIGN.md` is ~9 KB; `context` now carries a map. Run `impeccable design-compact` and **show the person** before using `--write`.
- `.impeccable/design.json` sidecar is stale relative to `DESIGN.md`; offer `impeccable document` to refresh it while preserving `DESIGN.md`.

Do these in a separate turn from any design task; do not rewrite DESIGN.md without approval.

## 6. Suggested team for the next phase

| Role | Agent | Responsibility |
|---|---|---|
| Release | `release-manager` + `devops-lead` | Push, PR, CI watch, merge gating |
| Governance | `ecl-harness-engineer` | Complete ECL records, archive gates |
| Quality | `qa-lead` | Deferred-minor triage and re-review |
| Product/message | `cpo`, `cmo`, `thought-leadership-lead` | Deeper critique decisions |
| Final verdict | `vp-engineering` | Whole-branch re-review after any new fixes |

## 7. How to resume the SDD workflow

If continuing with subagent-driven execution, read the ledger first, then use the skill scripts by absolute path from the repo root:

```powershell
& "C:\Program Files\Git\bin\bash.exe" -lc '"/c/Users/jmlus/.config/opencode/skills/subagent-driven-development/scripts/sdd-workspace" -C /c/Users/jmlus/light-speed-holdings /c/Users/jmlus/light-speed-holdings/docs/superpowers/plans/2026-11-25-marketing-site-trust-and-clarity.md'
```

The workspace already exists; do not create a second one. All previous task briefs, reports and review packages are in it. Once the branch is merged and the ledger's rulings have been copied into the final report, the workspace may be deleted — not before.
