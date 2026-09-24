# Case Study — LightSpeed Holdings Scroll Page (In-House Brand Build)

**Document ID:** CASE-LSP-001
**Author:** creative-director / frontend-engineer synthesis (scroll-craft skill)
**Owner:** cmo
**Classification:** Internal / Sales Enablement — LightSpeed's own brandsite flagship page
**Date:** 2026-09-22
**Status:** SHIPPED — build complete, verified, evidence archived. CEO ship report
delivered. Final gates green on 2026-09-22 (four device/motion combos, 30 frames
settled each, `failed: []`, 0 console errors; focus check PASS in normal and
reduced-motion; contrast worst 15.97:1 headline / 4.45:1 CTA).

**Honesty badge:** Proven in-house. This is LightSpeed's own brand page built on
its own creative stack — not a client deliverable, and not shipped to any live
audience. The page is a portfolio proof point (Offer A — digital presence) and a
demo artifact. Verification numbers below come from the archived lab runs in
`artifacts/lab/`, not from claims.

---

## 0. Build Guardrails (Read First)

- **Single artifact folder.** Everything for this build lives under
  `docs/case-studies/lightspeed-scroll-page/`: this record plus `artifacts/`
  (build files, `out/` render set, lab reports + contact sheets). Evidence is
  copied, never moved.
- **No bulky frame duplication.** Lab frame PNGs (~700 MB across five runs) are
  **not** copied into `artifacts/`. Each run contributes only `report.json`
  (machine evidence) and `sheet.png` (contact sheet) — the two files that prove
  the run's verdicts at a glance.
- **Source of truth stays in place.** The canonical build lives at
  `scrollcraft/builds/lightspeed/`; `artifacts/build/` is a snapshot copy for
  the record.
- **No secrets.** `scrollcraft/.env` is never read or copied.

## 1. Problem / Baseline

LightSpeed Holdings needed its own flagship page proving the scroll-craft
grammar and the brand — a page that could double as a sales demo for Offer A
(digital presence) and a proof-of-product artifact for the "proven in-house"
rung of the honesty ladder.

At intake the creative stack was in place but no **distinct** build existed:
the scroll-craft registry (`scrollcraft/FINGERPRINTS.md`) was empty, so there
was no proof the grammar could produce a page that was *not* a re-skin of
someone else's.

- **Baseline number:** `FINGERPRINTS.md` had zero registry rows and zero
  "What is taken" bullets — the gate couldn't be demonstrated.

## 2. Agentic Approach

The page was produced by the scroll-craft skill (orchestrated by
`creative-director` + production by `frontend-engineer`, QA'd by
`artifact-qa-reviewer`), working against the LightSpeed brand system
(`ls-design-system`).

| Workstream | Owner | Charter |
|------------|-------|---------|
| Creative direction | `creative-director` | brief intake, Wikipedia-0 homepage as source copy, act-sequence shape |
| Production | scroll-craft skill | Chaptered editorial grammar, folio nav, flags signature, 16:9 + 3:4 plates |
| Brand conformance | `ls-design-system` | navy/crimson/cyan tokens, Arial scale, verbatim copy rules |
| Verifiable evidence | lab scripts (`shoot.mjs`, `tab-focus.mjs`, `serve.mjs`) | deterministic Playwright probes → `report.json` + `sheet.png` |
| QA gate | `ls-artifact-qa` | visual / brand / UX / accessibility / content review |

**Standing page constraints (enforced throughout):** verbatim copy; no em
dashes in page copy; no scroll cues; single `.sc-label`; accent `#E63946` in
exactly one region; no code comments; no `data-sc-progress`; `.sc-split`
kinetic line-split; flag math inherited even in flow acts.

## 3. Measurable Outcome

- **Fingerprint gate satisfied.** One registry row appended and six "What is
  taken" bullets written — the next build must differ on ≥4 of 6 dimensions
  against this row.
- **Page shape:** 6 acts, `flow > pin > flow > scrub > flow > pin`, ~9.8 vh on
  desktop (8687 px / 900 vh) and ~9.8 vh on mobile (7922 px / 812 vh — the
  mobile page runs 9.8 viewport-heights tall).
- **Act stages** (desktop): 900 / 3962 / 7652.
- **All five lab runs green:** desktop normal (`shots`), mobile 375×812
  (`mobile`), desktop reduced-motion (`reduced`, `reduced-rerun`), mobile
  reduced-motion (`mobile-reduced`) — 30 frames each, all `settled: true`,
  `failed: []`, 0 `consoleErrors`.
- **Contrast (worst frame, y=7698, reduced-motion):** "Run it at light speed."
  worst **15.97:1**; footer line worst 16.31:1; CTA "Start a project" worst
  **4.45:1** (large display text, above the 3:1 large-text threshold). Frame 0
  headline "ASPIRE. ACT. ACHIEVE." worst 8.82:1 / mean 17.36:1.
- **Focus:** 4 tab stops (hero CTA, join CTA, foot email, folio CTA);
  `FOCUS CHECK PASS` in normal and reduced-motion; `:focus-visible` ring
  `outline 2px solid rgb(230, 57, 70)`.
- **Server:** port 4500.

## 4. Governance and Auditability

- The fingerprint gate is append-only: rows and "What is taken" bullets are
  never edited to make room for a later build; a row occupies its space forever.
- Every lab run archives `report.json` (deterministic machine evidence) plus a
  `sheet.png` contact sheet — the verdicts in this file are reproducible from
  `artifacts/lab/` without a browser.
- The page carries the brand as its honesty contract: verbatim copy, one
  accent region, no fabricated claims, no invented metrics in the running text.

## 5. Reuse Note

- The Chaptered-editorial grammar + folio-in-the-margin nav + raising-flags
  signature is one complete entry in the fingerprint registry — the *next* build
  is already banned from reusing it.
- The lab-evidence pattern (`report.json` + `sheet.png` contact sheet per run,
  deterministic probes, no frame dump in the record) is reusable for every
  future creative build with the `ls-*` stack.
- Serving as Offer A demo material: a real, shipped, verified page shows the
  digital-presence family rather than describing it.

---

## 6. Build Plan (Waves)

1. **Brief + brand load** — `creative-director` intake; `ls-design-system`
   tokens; Wikipedia-0 verbatim copy selected.
2. **Fingerprint plan** — registry consulted (empty); 6-act ~9.8 vh shape and
   flags close committed as the distinguishing identity.
3. **Build** — `scrollcraft/builds/lightspeed/` (index.html, scrollcraft.css,
   scrollcraft.js, BRIEF.md) on port 4500.
4. **Lab verification (desktop normal)** — `shots` run: 30 frames settled.
5. **Mobile + reduced-motion passes** — `mobile`, `reduced` runs; reduced-motion
   cloth/flag defect found (worst contrast 2.09:1) → fixed →
   `reduced-rerun` (15.97:1) and `mobile-reduced` (both green).
6. **Focus pass** — `tab-focus.mjs` defect fixed (expected count included
   non-tabbable nodes; now filters genuinely tabbable, dedupes by idx, breaks on
   first repeat, bound `expected * 2 + 4`); FOCUS CHECK PASS both modes.
7. **Fingerprint append** — registry row + 6 "What is taken" bullets.
8. **Gate + record** — ship report to CEO; evidence consolidated into
   `docs/case-studies/lightspeed-scroll-page/`.

## 7. Evidence Index (Verification)

| Run | Device / motion | Doc height vh | Frames settled | failed | consoleErrors | Artifact |
|-----|-----------------|---------------|----------------|--------|---------------|----------|
| shots | desktop normal | 8687 / 900 | 30 / 30 | — | 0 | `artifacts/lab/shots/` |
| mobile | mobile 375×812 normal | 7922 / 812 | 30 / 30 | — | 0 | `artifacts/lab/mobile/` |
| reduced | desktop reduced-motion | 8687 / 900 | 30 / 30 | — | 0 | `artifacts/lab/reduced/` |
| reduced-rerun | desktop reduced-motion (fixed) | 8687 / 900 | 30 / 30 | — | 0 | `artifacts/lab/reduced-rerun/` |
| mobile-reduced | mobile 375×812 reduced-motion | 7922 / 812 | 30 / 30 | — | 0 | `artifacts/lab/mobile-reduced/` |

- **Build snapshot:** `artifacts/build/` (index.html, scrollcraft.css,
  scrollcraft.js, BRIEF.md).
- **Render set:** `artifacts/out/` (4 posters, founder-desk 3:4, 3 videos,
  logo).
- **Reproduction:** run `serve.mjs` on `scrollcraft/builds/lightspeed/` (port
  4500), then `shoot.mjs` / `tab-focus.mjs` from
  `.opencode/skills/scroll-craft/scripts/`.

*End of case study. Honest, boundary-respecting, evidence-traceable.*
