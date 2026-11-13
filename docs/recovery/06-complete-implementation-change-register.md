# 06 — Complete Implementation Change Register

**Date:** 2026-11-13
**Baseline:** `86d10e709c50424eb7109283ff7e7019a1a51bc2` (`main`)
**Status:** **all changes below are uncommitted.** No commit, merge, push, PR, or history change was made this session.

Every restored file is a **verbatim copy** of its AI Studio prototype counterpart, proven byte-identical by SHA256 (repo vs `_staging/lsh-prototype/src/…`).

---

## 1. Created — restored functional components (verbatim)

| # | Repo path | Source (prototype) | Lines | SHA256 (repo = staging) |
|---|---|---|---|---|
| 1 | `src/components/HumanApprovalMatrix.tsx` | `components/HumanApprovalMatrix.tsx` | 214 | `3ED62FCDCFFB03AE540AA0617A6BC90679708FE02C3A389483ECD603274F0884` |
| 2 | `src/components/BackToTop.tsx` | `components/BackToTop.tsx` | 122 | `06B234A66BCDD838BAF069DEBF16FD8C0B67C4CC9A1FA8A6FEC7950E672A08F3` |
| 3 | `src/components/FaqCardList.tsx` | `components/FaqCardList.tsx` | 134 | `2ADC13CE135A71762BE63D3636CBA1FC0CC53678BB92BDB5DC17351EB87DD4A7` |
| 4 | `src/pages/FaqPage.tsx` | `pages/FaqPage.tsx` | 45 | `F99EEF6B1E2408479A8546C571439608F69EBAFBCCB45EEF35228013FB76A873` |

**Why:** these were present and referenced in the prototype but absent from the repo. Each is a real functional loss, not dead code (see `02-…` §2.1). Copying them verbatim — rather than re-implementing — preserves prototype behaviour exactly, per the "preserve, do not redesign" constraint.

---

## 2. Modified — wiring

### 2.1 `src/App.tsx` (+4 lines)

```diff
+import { FaqPage } from './pages/FaqPage';
+const FaqPageRoute = withSite(FaqPage);
+          { path: 'faq', element: <FaqPageRoute /> },
+          { path: 'faqs', element: <Navigate to="/faq" replace /> },
```

**Why:** the prototype exposed a dedicated `/faq` page; the repo did not. The route is added and the legacy `/faqs` path redirects to it (mirrors the prototype's redirect).

### 2.2 `src/components/SiteLayout.tsx` (+3 lines)

```diff
+import { BackToTop } from './BackToTop';
+      <BackToTop theme={theme} />
```

**Why:** mount the restored back-to-top control in the shared site shell so it appears on every page, as in the prototype.

### 2.3 `src/pages/HomePage.tsx` (net −40 / +3)

The inline static "Five-tier Human Approval Matrix" section (42 lines of hard-coded markup) was **replaced** by the real interactive component:

```diff
-      {/* 1c. Five-tier Human Approval Matrix — preserved from AI Studio prototype */}
-      <section …>…5 static <div> cards…</section>
+      {/* 1c. Five-tier Human Approval Matrix — interactive component restored from AI Studio prototype */}
+      <HumanApprovalMatrix theme={theme} />
```

**Why:** the repo carried a simplified, non-interactive approximation of the prototype's interactive matrix. Replacing it with the real component restores the tier-selection inspector behaviour (verified in `04-…` §3.1). This is a **behaviour restoration**, not a redesign.

---

## 3. Created — verification harness (non-shipping)

| # | Path | Lines | Purpose |
|---|---|---|---|
| 5 | `scripts/recovery-verify.mjs` | 146 | Playwright: 27-route matrix + interactions → JSON + screenshots |
| 6 | `scripts/recovery-verify-focused.mjs` | 52 | Playwright: `/insights`, BackToTop, matrix detail |

These are **mission tooling**, not application code; they are not imported by the app or bundled.

---

## 4. Created — recovery deliverables (documentation only)

| # | Path |
|---|---|
| 7 | `docs/recovery/00-current-state-and-preservation-audit.md` |
| 8 | `docs/recovery/01-previous-recovery-verification.md` |
| 9 | `docs/recovery/02-complete-ai-studio-reconciliation-ledger.md` |
| 10 | `docs/recovery/03-security-and-repository-hygiene.md` |
| 11 | `docs/recovery/04-independent-verification-report.md` |
| 12 | `docs/recovery/05-execution-and-token-accounting.md` |
| 13 | `docs/recovery/06-complete-implementation-change-register.md` *(this file)* |
| 14 | `docs/recovery/07-outstanding-items-and-exclusions-register.md` |
| 15 | `docs/recovery/08-final-mission-completion-report.md` |
| 16 | `docs/recovery/screenshots/*.png` (33) |
| 17 | `docs/recovery/verification-run.json` |
| 18 | `docs/recovery/verification-focused.json` |
| 19 | `docs/recovery/_staging-absent-src.txt` |

---

## 5. Working-tree delta (authoritative)

```
 M src/App.tsx                   |  4 ++++
 M src/components/SiteLayout.tsx |  3 +++
 M src/pages/HomePage.tsx        | 43 +++----------------------------------------
?? src/components/HumanApprovalMatrix.tsx
?? src/components/BackToTop.tsx
?? src/components/FaqCardList.tsx
?? src/pages/FaqPage.tsx
?? scripts/recovery-verify.mjs
?? scripts/recovery-verify-focused.mjs
?? docs/recovery/
```

Totals: **3 modified files, 4 restored components, 2 harness scripts, 1 deliverable tree.** No deletions.

---

## 6. Explicit non-changes

| Not changed | Reason |
|---|---|
| Sector taxonomy | User exclusion |
| Workflow-simulator card keyboard navigation | User exclusion |
| `.github/workflows/verify-vite.yml` | Pre-existing defect; fixing CI is a separate authorized change (O-01) |
| `.gitignore` (`_staging/` rule) | Changing it is an unauthorized scope change (O-10) |
| Theme/palette divergences from the prototype | Brand/design, not functional defects |
| Any other route, component, or data file | Not required by the reconciliation |

---

## 7. Change-integrity statement

- All 4 restored components: **byte-identical** to the prototype (SHA256 verified, §1).
- All wiring edits are **additive** except the deliberate HomePage replacement, which swaps a static approximation for the real component.
- Gates after the changes: `tsc` 0, `vitest` 16/145, `vite build` 0 (`04-…` §1).
- **Nothing committed**; the delta is fully reversible with `git restore` / file removal.
