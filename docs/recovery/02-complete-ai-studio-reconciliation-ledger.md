# 02 — Complete AI Studio Reconciliation Ledger

**Reference (prototype):** `_staging/lsh-prototype/src/` (241 files)
**Implementation (repo):** `src/` + `packages/`
**Method:** for every file under the prototype `src/` tree, test whether the same relative path exists under repo `src/`; for every file that does not, grep the prototype tree for imports/usages to decide whether its absence is a *functional loss* or *dead code*.

All counts below were produced by this session's scans; none are copied from the earlier `.audit/reconciliation/` set (which contains inflated counts — see `01-…` §3).

---

## 1. Headline reconciliation numbers

| Metric | Count |
|---|---|
| Prototype `src/` files | 241 |
| Present in repo `src/` at the same relative path | 124 |
| Absent from repo `src/` at the same relative path | 117 |
| **Of the 117 absent, restored by this session** | **4** |
| Remaining absent after this session | 113 |

Breakdown of the 113 remaining-absent files:

| Category | Count | Disposition class |
|---|---|---|
| `assets/images/**` | 62 | Media — reconciled separately (§4) |
| `design-system/**` (prototype copy) | 26 | **Superseded** by `packages/design-system` (§3) |
| `docs/design/**` + `reports/**` (markdown) | 10 | Documentation artifacts, non-functional |
| Functional `.tsx`/`.ts` + brand token | 19 | Analysed individually in §2 |

`62 + 26 + 10 + 19 = 117` ✓ (and `117 − 4 restored = 113`).

---

## 2. Functional-component ledger (the 19 non-media, non-design-system, non-doc files)

Legend: **RESTORED** = recovered verbatim this session · **REPLACED** = equivalent exists in repo · **OMITTED** = used in the prototype, no repo equivalent · **DEAD** = zero references in the prototype · **RELOCATED** = same content at a different repo path.

### 2.1 Restored this session (4)

| Prototype file | Repo path | Class | Staging refs | Evidence |
|---|---|---|---|---|
| `components/HumanApprovalMatrix.tsx` | `src/components/HumanApprovalMatrix.tsx` | **RESTORED** | HomePage | SHA256 `3ED62FCD…F0884` identical; wired into `HomePage.tsx` |
| `components/BackToTop.tsx` | `src/components/BackToTop.tsx` | **RESTORED** | SiteLayout | SHA256 `06B234A6…2A08F3` identical; wired into `SiteLayout.tsx` |
| `components/FaqCardList.tsx` | `src/components/FaqCardList.tsx` | **RESTORED** | FaqPage | SHA256 identical; `Card` import resolves (`packages/design-system`) |
| `pages/FaqPage.tsx` | `src/pages/FaqPage.tsx` | **RESTORED** | App route `/faq` | SHA256 identical; route added |

### 2.2 Used in prototype → replaced by a repo equivalent (9)

| Prototype file | Staging refs | Repo equivalent | Class |
|---|---|---|---|
| `components/DistinctCTA.tsx` | HomePage, WhatWeDoPage | `src/components/site/CtaBand.tsx` | REPLACED |
| `components/haomtgv/HaomtgvPipelineDiagram.tsx` | HAOMTGVPage | `src/pages/HAOMTGVPage.tsx` (repo-native) | REPLACED |
| `components/haomtgv/HaomtgvUnifiedArchitecture.tsx` | HAOMTGVPage | `src/pages/HAOMTGVPage.tsx` (repo-native) | REPLACED |
| `components/home/HAOMTGVVisualization.tsx` | HAOMTGVSection | `src/components/home/HAOMTGVSection.tsx` + `/haomtgv` visuals | REPLACED |
| `components/home/IntroductionSection.tsx` | HomePage, home/index | `CtaBand` + "Our Value Framework" on `HomePage.tsx` | REPLACED |
| `components/home/LightSpeedProposition.tsx` | HomePage | `VALUES` "Our Value Framework" (`src/data/homeCopy.ts`) | REPLACED |
| `components/home/WhatWeBuildGrid.tsx` | HomePage | "Practical Business Outcomes" grid (`HomePage.tsx`) | REPLACED |
| `components/PharosReaderModal.tsx` | InsightsPage | Dedicated `/insights/:slug` article pages (`InsightArticlePage.tsx`) | REPLACED |
| `hooks/useSectionReveal.ts` | HAOMTGVPage, RevealSection | `src/components/Reveal.tsx` + `src/hooks/useInView.ts` | REPLACED |

### 2.3 Used in prototype → genuinely omitted (1)

| Prototype file | Staging refs | Class | Note |
|---|---|---|---|
| `components/home/IntentToExecutionLifecycle.tsx` | HomePage | **OMITTED** | The prototype's "Intent → Execution" lifecycle section has no repo equivalent. The repo covers the same concept textually in `HAOMTGVSection` and `/haomtgv` but not as this lifecycle component. Recorded as an outstanding gap (O-06), not restored because its visual dependencies (the prototype's home composition) are not part of the repo's IA. |

### 2.4 Dead in the prototype — zero references (5 components + 2 data + 1 relocated)

| Prototype file | Staging refs | Class |
|---|---|---|
| `components/ContentCarousel.tsx` | 0 | DEAD |
| `components/ImpactImageSection.tsx` | 0 | DEAD |
| `components/RevealSection.tsx` | 0 | DEAD |
| `components/TelemetryBar.tsx` | 0 | DEAD |
| `components/AiCompanyBuilder/VentureMaturityInfographic.tsx` | 0 | DEAD |
| `components/home/StrategicHeroVisual.tsx` | 0 | DEAD |
| `data/shipped/company.ts` | 0 | DEAD |
| `data/shipped/ctas.ts` | 0 | DEAD |
| `brand/tokens/brand-tokens.css` | — | **RELOCATED** to repo `brand/tokens/brand-tokens.css` (present) |

> A "dead" prototype component is **not** a recovery loss: the prototype itself never rendered it, so no functionality was omitted from the implementation.

---

## 3. Design-system reconciliation

| Prototype | Repo | Note |
|---|---|---|
| `src/design-system/**` — 26 files (components, tokens, hooks, utils, styles, `index.ts`) | `packages/design-system/src/**` — 34 files | The prototype's in-tree design system is **superseded** by a real package. The repo exposes it via the `@lightspeed/design-system` alias (`tsconfig.json:21`, `vite.config.ts:65–66`). `Card` is exported (`packages/design-system/src/index.ts:15`), which is why `FaqCardList` could be restored verbatim. |

No functional loss: the repo package is a superset.

---

## 4. Media-asset reconciliation

| Location | Files | Note |
|---|---|---|
| Prototype `public/assets/aistudio/` | 35 | Prototype-only public media |
| Prototype `src/assets/images/` | 62 | Prototype-only bundled media (all 62 are in the absent set) |
| Repo `public/assets/` | 288 | Across `catalog/`, `diagrams/`, `generated/`, `insights/`, `sectors/` |
| Repo `brand/` | present | Canonical brand media (`brand/digital/Homepage_Hero_High_fidelity.jpeg`, logos) |

The repo has **288** public assets — substantially more than the prototype's media, and organised into registries. The prior audit's "290+ AI Studio media assets vs 17 registry entries" figure was not reproduced; the real prototype media count is `35 + 62 = 97` files, and the repo's asset set is larger and registry-backed. Media reconciliation is therefore **not a net loss**; the repo's media registry (`src/data/media/registry.ts`) is the canonical gate.

---

## 5. Data reconciliation

| Prototype | Repo | Result |
|---|---|---|
| `src/data/faqs.ts` (6 FAQs) | `src/data/faqs.ts` (6 FAQs) | **Byte-identical** (SHA256 `1FF205B6…8745A`; 6 array objects in both — the 7th `registryId:` match is the interface declaration) |
| `src/data/homeCopy.ts` | `src/data/homeCopy.ts` | Present; repo extends with `VALUES` |
| `src/data/shipped/ctas.ts` | — | DEAD in prototype (0 refs) |
| `src/data/shipped/company.ts` | — | DEAD in prototype (0 refs) |

FAQ **content** was never lost; the prototype's dedicated `/faq` **route** was, and is restored in §2.1.

---

## 6. Route reconciliation

| Prototype route | Repo route before | Repo route now |
|---|---|---|
| `/faq` | *missing* | **`/faq` (restored)** |
| `/faqs` → redirect | *missing* | **`/faqs` → `/faq` (restored)** |
| `/` … `/insights/:slug` | present | present (verified in `04-…`) |

All other prototype routes were already present or intentionally redirected (see `04-…` route matrix).

---

## 7. Ledger summary

| Class | Count | Meaning |
|---|---|---|
| RESTORED (this session) | 4 | Functionality recovered verbatim |
| REPLACED (verified equivalent) | 9 | Functionality present via a different implementation |
| OMITTED (real gap) | 1 | `IntentToExecutionLifecycle` — no equivalent |
| DEAD (prototype never used it) | 8 | No loss |
| RELOCATED | 1 | Same content, new path |
| SUPERSEDED (design system) | 26 | Package supersedes in-tree copy |
| DOC ARTIFACTS | 10 | Markdown, non-functional |
| MEDIA | 62 | Reconciled against the larger repo media set |

**Functional omissions outstanding: 1** (`IntentToExecutionLifecycle`), plus the two user-directed exclusions recorded in `07-…`.
