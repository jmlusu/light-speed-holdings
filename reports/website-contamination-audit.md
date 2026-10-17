# LightSpeed External Website Contamination Audit — Final Report

| | |
|---|---|
| **Status** | FINAL — authoritative record |
| **Date** | 2026-10-07 |
| **Scope** | Root Vite/React external client-facing application (repository root, Vercel-hosted) |
| **Mode** | Read-only audit — no source, config, data, or Git history was modified |
| **Audited HEAD** | `529258f2` |

---

## §1 Verdict

**CLEAN — no Athena contamination and no CEO Dashboard contamination of the Root Vite/React public application.**

**Recommendation: A — No application remediation.**

| Audit area | Verdict | Application action |
|---|---|---|
| Athena (client system) | **CLEAN** | None |
| CEO Dashboard (internal system) | **CLEAN** | None |
| Public routes | **CLEAN** — all routes safe | None |
| Data registries | **CLEAN** — intentionally public | None |
| Application findings | Informational only (3 × LOW) | None |
| Repository hygiene | Advisory raised — separate decision | Separate human decision (§7) |

The public website is properly bounded: no internal system is reachable through the deployed site, no internal code is bundled, and no internal data is served. The single open item is a **repository-hygiene** question about two KPI files committed to the public GitHub repository (§7) — this is **not** application contamination and requires a separate human decision.

---

## §2 Athena — CLEAN

Athena is a separate client job-consultancy system. It was removed from this repository and has no presence in the public application.

### Evidence

| Check | Method | Result |
|---|---|---|
| Athena source removed | `git log` on `src/ai_company/athena/`, `src/components/athena/`, `src/pages/athena/`, `src/lib/athena/` | All removed in commit `1dadc644` |
| Zero-match verification (source) | `git grep -i athena -- src/*.ts src/*.tsx` | **0 matches** |
| Zero-match verification (static public assets) | `git grep -i athena -- public` | **0 matches** |
| Zero-match verification (production bundle) | String search across all 403 files in `dist/` | **0 matches** |
| No TypeScript/TSX imports of Athena | `git grep "from '.*athena" -- src` | **0 matches** |
| No `/athena` route | `git grep -i athena -- src/App.tsx` | **0 matches** — route absent |
| No Athena bundle content | Bundle scan for Athena strings/assets | **None** |
| `company/athena/` local data | `.gitignore:170` → `company/athena/` | **Gitignored** — never committed, never shipped |

### Classification

**CLEAN.** Athena source, components, pages, library, routes, data, and bundle content are all absent. The prior architectural remediation (archive) is intact and verified by zero-match checks at source, static-asset, and bundle level.

---

## §3 CEO Dashboard — CLEAN

The CEO Dashboard is an internal FastAPI + Alpine.js application at `src/ai_company/dashboard/`, bound to `127.0.0.1` with API-key authentication. It is not part of the public website.

### Evidence

| Check | Method | Result |
|---|---|---|
| No TypeScript/TSX imports of `ai_company/dashboard` | `git grep "from '.*ai_company" -- src/App.tsx src/pages src/components src/hooks src/lib` | **0 matches** — zero imports into the public app |
| No CEO Dashboard content in production JS bundle | String search of `dist/assets/*.js` + `dist/index.html` for `ceo-dashboard`, `J.A.R.V.I.S.`, `ai_company/dashboard` | **0 matches** |
| Only dashboard references in `dist/` | File-level scan | `dist/brand/guidelines/brand-guidelines.md` and `dist/brand/README.md` — **documentation notes only**, explicitly stating the dashboard is internal, "NOT public-facing brand", and must not be rebranded |
| `/architecture` page references | Source inspection of `src/pages/Architecture.tsx` | Descriptive architecture text only (e.g. "RBAC for dashboard API keys") — **not an import**, not dashboard code |
| Internal dashboard code not in Vite graph | `src/ai_company/dashboard/**` is never imported by `src/App.tsx`, `src/pages/`, `src/components/`, `src/hooks/`, `src/lib/` | Excluded from build |
| Dashboard runtime boundary | `DASHBOARD_HOST=127.0.0.1`, `X-API-Key` auth (`DASHBOARD_ADMIN_KEY` / `DASHBOARD_APPROVE_KEY` / `DASHBOARD_RUN_KEY`) | Local-only, authenticated |
| Dashboard data / KPI endpoints in bundle | Bundle scan for dashboard API paths | **None** — no `/api/v1/ceo-dashboard` references in the public bundle |

### Classification

**CLEAN.** Zero imports, zero bundle content, local-only runtime. The only traces of the CEO Dashboard on the public site are brand documentation notes that explicitly designate it as internal.

---

## §4 Routes — All Public Routes Safe

Route inventory from `src/App.tsx:77-106` (`createBrowserRouter`).

| # | Route | Page component | Safe? |
|---|---|---|---|
| 1 | `/` (index) | `HomePageRoute` | Yes |
| 2 | `/what-we-do` | `WhatWeDoPageRoute` | Yes |
| 3 | `/ai-company-builder` | `AiCompanyBuilderPageRoute` | Yes |
| 4 | `/solutions` | `SolutionsPageRoute` | Yes |
| 5 | `/sectors` | `SectorsPageRoute` | Yes |
| 6 | `/proof` | `ProofPageRoute` | Yes |
| 7 | `/insights` | `InsightsPageRoute` | Yes |
| 8 | `/insights/:slug` | `InsightArticlePageRoute` | Yes |
| 9 | `/about` | `AboutPageRoute` | Yes |
| 10 | `/contact` | `ContactPageRoute` | Yes |
| 11 | `/ask` | `AskLightSpeed` | Yes |
| 12 | `/legal/privacy` | `PrivacyPageRoute` | Yes |
| 13 | `/legal/terms` | `TermsPageRoute` | Yes |
| 14 | `/architecture` | `Architecture` | Yes |
| 15 | `/build` | `Build` | Yes |
| 16 | `/offer-b` | `OfferB` | Yes |
| 17 | `/offer-c` | `OfferC` | Yes |
| 18 | `/offer-e` | `OfferE` | Yes |
| — | `*` (catch-all) | `Navigate to "/"` | Yes |

**Route verdict:** 18 public page routes + catch-all redirect (19 router entries). **All public routes safe.** No `/athena` route. No CEO Dashboard route. No internal or admin routes. The catch-all redirects unknown paths to `/`.

---

## §5 Data Registries — Intentionally Public

Public content is served through a deliberate `@lightspeed/data/*` registry architecture declared as Vite aliases in `vite.config.ts`:

| Alias | Source |
|---|---|
| `@lightspeed/data/company` | `data/company/registry.ts` |
| `@lightspeed/data/metrics` | `data/metrics/registry.ts` |
| `@lightspeed/data/capabilities` | `data/capabilities/registry.ts` |
| `@lightspeed/data/solutions` | `data/solutions/registry.ts` |
| `@lightspeed/data/use-cases` | `data/use-cases/registry.ts` |
| `@lightspeed/data/sectors` | `data/sectors/registry.ts` |
| `@lightspeed/data/insights` | `data/insights/registry.ts` |
| `@lightspeed/data/faqs` | `data/faqs/registry.ts` |
| `@lightspeed/data/claims` | `data/claims/registry.ts` |
| `@lightspeed/data/governance` | `data/governance/registry.ts` |
| `@lightspeed/data/media` | `data/media/registry.ts` |
| `@lightspeed/data/ctas` | `data/ctas/registry.ts` |
| `@lightspeed/design-system` (+ `/tokens`) | `packages/design-system/src/` |

| Data source | Referenced by public app? | Bundled? | Publicly reachable? | Classification |
|---|---|---|---|---|
| Company identity, metrics, capabilities, solutions, use-cases, sectors, insights, FAQs, CTAs, media | Yes — by design | Yes — intentionally public content | Yes, on public routes | **Intentionally public** |
| Claims registry (`@lightspeed/data/claims`) | Yes | Yes — published on public routes only | Yes, public routes only | **Intentionally public** |
| Governance registry (`@lightspeed/data/governance`) | Yes | Yes — governance documentation | Yes, public routes only | **Intentionally public** |
| `src/data/companyData.ts` | **No** — only imported by `src/__tests__/companyData.test.ts` | **No** — absent from all `dist/assets/*.js` (verified by string scan) | No | **Not bundled** |
| CEO Dashboard KPI config / KPI history | No import by public app | No | Not served (see §7) | **Not application data** |
| Athena data (`company/athena/`) | No | N/A — gitignored | No | **CLEAN** |

**Registry verdict:** All public-app data flows through explicit `@lightspeed/data/*` registries containing intentionally public marketing/identity content. Internal data is not imported, bundled, or served.

---

## §6 Findings — Informational, No Application Action Required

Three **LOW** informational findings were recorded. **None require application action.** None are contamination.

| # | Severity | Finding | Why no application action |
|---|---|---|---|
| F-1 | LOW | `dist/brand/guidelines/brand-guidelines.md` and `dist/brand/README.md` mention the CEO Dashboard (internal J.A.R.V.I.S. theme, "Dashboard Exception"). | Documentation text only. It explicitly states the dashboard is **internal** and "NOT public-facing brand". Contains no dashboard code, routes, data, or credentials. |
| F-2 | LOW | `config/company/kpis.yaml` is committed to the public GitHub repository. | Not imported by the public website, not served by Vercel, not bundled. See §7. |
| F-3 | LOW | `dashboard/kpi_history/*.ndjson` are committed to the public GitHub repository. | Not imported by the public website, not served by Vercel, not bundled. See §7. |

**Findings verdict:** Informational only. F-1 is a documentation artifact of an already-correct internal/public separation. F-2 and F-3 are repository-hygiene items, not application contamination — escalated as an advisory in §7. **No application code, routes, config, or data changes are authorized or required by this audit.**

---

## §7 Repo-Hygiene Advisory

> **Scope warning:** This section is an advisory for a **separate human decision**. It is explicitly **not** part of the application verdict, and none of the actions below were taken as part of this audit.

Recorded facts:

- `dashboard/kpi_history/*.ndjson` **is committed to the PUBLIC GitHub repository.**
- `config/company/kpis.yaml` **is committed to the PUBLIC GitHub repository.**
- These files are **NOT imported** by the public website.
- These files are **NOT served** by Vercel (Vercel deploys only the `dist/` build output plus the `api/*` serverless functions; `dashboard/` and `config/` are outside the deployed output — see §8 deployment evidence).
- Therefore this is **NOT application contamination.**
- It is nevertheless a **repository-hygiene / security consideration requiring a separate human decision.**

Explicit constraints honored by this audit:

- **Do NOT automatically rewrite Git history.**
- **Do NOT delete or modify these files as part of this task.**

**Open decision for the CEO/human owner:** determine whether these KPI files should remain public (e.g., accept exposure, relocate them to a private repository, or add them to `.gitignore` going forward). Any such change is a separate, explicitly authorized task.

---

## §8 Evidence — Deployment and Environment Boundary

### Vercel deployment configuration (`vercel.json`)

| Setting | Value | Implication |
|---|---|---|
| `buildCommand` | `bun run build` | Builds the Vite/React app only |
| `outputDirectory` | `dist` | **Only `dist/` is deployed** — `dashboard/`, `config/`, `data/`, `src/ai_company/` are never published |
| `rewrites` | `/(.*) → /index.html` | SPA routing; no internal path routing |
| `functions` | `api/enquiry.ts`, `api/ping.ts`, `api/ping-nodejs.js` | Serverless surface is a small allow-list of first-party endpoints |
| `headers` | `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` | Hardened defaults |

### `VITE_*` environment-variable boundary (`vite.config.ts`)

- Only `VITE_*`-prefixed variables are exposed to the client bundle (Vite's `import.meta.env` rule).
- Client code reads only `VITE_TURNSTILE_SITE_KEY`, `VITE_WHATSAPP_NUMBER`, `VITE_CONTENT_MEDIA_ENABLED`.
- `TURNSTILE_SITE_KEY_RE = /^[0-9a-zA-Z._-]{10,120}$/` rejects any value containing `=`, whitespace, or pasted env blocks — preventing a secret such as `TURNSTILE_SECRET_KEY` (or any pasted env block) from being baked into the bundle.
- No `DASHBOARD_*` or provider API keys are referenced anywhere in client (`src/App.tsx`, `src/pages/`, `src/components/`, `src/hooks/`, `src/lib/`) code.

### Network calls from the public app

- Form submissions target first-party **`/api/enquiry`** only — three call sites: `src/components/ContactSection.tsx:88`, `src/components/ExecutiveBriefingModal.tsx:59`, `src/components/NewsletterSignup.tsx:41`.
- The only other client call is the whitelisted analytics beacon `/api/journey-events` (`src/hooks/useJourneyEvents.ts:52`), also a first-party Vercel endpoint.
- **No internal, Athena, or CEO Dashboard endpoints are called from the public app.**

### Production bundle contents (`dist/`, 403 files)

`index.html`, compiled `assets/*.js` / `assets/*.css`, `brand/` tokens and guidelines, favicons, logo SVGs, catalog/insight imagery. Verified: **no Athena strings**, **no CEO Dashboard code strings**, **no `companyData` references**, **no `.ndjson`/KPI history content**.

---

## §9 Git-History Timeline

| Date | Commit | Event |
|---|---|---|
| 2026-08-18 | `a1dce51d` | `feat: v0.5.1 Phase 1 - Dashboard features` — `dashboard/kpi_history/*.ndjson` first committed (origin of F-3) |
| 2026-08-31 | `cd753fb0` | `feat(dashboard): CEO Alert Center…` — `config/company/kpis.yaml` history begins (origin of F-2) |
| 2026-09-02 | `3746b784` | `feat(dashboard): expand executive KPI set…` |
| 2026-09-21 | `51a52a45` | `feat(athena): job consultancy application platform` — Athena introduced |
| 2026-09-22 | `ffbfb8fd` | `feat(athena): add curated remote scrapes… (#356)` — Athena extended |
| 2026-09-22 | `85b82929` | `fix(athena): serialize Decimal salary ranges in JSONL store (#358)` — Athena bugfix |
| 2026-10-07 | `1dadc644` | `feat: archive Athena, add design system, UseCasesPage, CTA, registries, docs (#415)` — **Athena removed**: all `src/**/athena/` sources and `company/athena/` JSONL data deleted; public-facing redesign added. Deliberate architectural separation. |
| 2026-10-07 | `03ebcff7` | `feat: relocate runtime state to data/orchestrator (D-6)` — most recent `config/company/kpis.yaml` change |
| 2026-10-07 | `529258f2` | `Stage 41 untracked files…` — audited HEAD |

**Timeline verdict:** Athena was introduced (2026-09-21), extended, fixed, and fully removed (2026-10-07). The CEO Dashboard has existed throughout as a separate internal application. No commit between the audited history and HEAD added Athena routes/components/data or CEO Dashboard routes/components/data to the public application. Both systems are now — and for the audited period were — properly separated from the public website.

---

## §10 Recommendation

### A — No application remediation

The public application requires **no changes**: no code, no routes, no configuration, no data, no dependency changes.

| Question | Answer |
|---|---|
| Athena contamination? | **No** |
| CEO Dashboard contamination? | **No** |
| Remediation required? | **No** |
| Open items? | One repository-hygiene decision (§7): should `config/company/kpis.yaml` and `dashboard/kpi_history/*.ndjson` remain in the public repository? |
| Actions explicitly out of scope | Application changes, restoring Athena or `/athena`, reconnecting the CEO Dashboard, removing KPI files, Git-history rewriting, repository cleanup, "fixing" the LOW findings |

---

*Audit performed read-only. No source, `public/`, `dashboard/`, `config/`, `data/`, `vite.config.ts`, `vercel.json`, routes, KPI files, or Git history were modified. Findings are based on source inspection, route analysis, bundle examination, deployment configuration review, and Git history analysis.*
