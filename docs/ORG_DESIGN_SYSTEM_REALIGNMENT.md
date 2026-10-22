# Organization Design System Realignment Report

**Status:** Final — bidirreferential scope (design system doc ↔ canonical brand files + org mapping)
**Delivered:** 2026-10-14
**Scope:** Full reconcile of `LightSpeed_Holdings_Organization_Design_System.md` v1.0 against existing canonical brand files and organization registry, with realignment recommendations across agents, skills, and processes.

---

## 1. Executive Summary

The `LightSpeed_Holdings_Organization_Design_System.md` (v1.0, merged 2026-10-14, PR #467) is a **proposed baseline** for CEO/design-owner approval. It defines organization-wide visual, tonal, and behavioral standards across public websites, presentations, dashboards, Pharos insights, AI-venture-studio outputs, and agent-generated artifacts.

**Key finding:** The doc itself §25 instructs: *"Before adopting this document as fully canonical, reconcile it with the actual approved logo files, current production tokens, and existing repository documentation. Where this file provides a proposed default, validate it against the approved implementation rather than assuming the default is already deployed."*

**Six conflict categories** were identified between the new doc and existing canonical assets (per `brand/CANONICAL_SOURCES.md` updated 2026-10-13, the single source of truth for `brand/**`):

| # | Conflict | Doc Section | Canonical Evidence | Severity |
|---|---|---|---|---|
| 1 | **Typography default** — doc §6.1 names **Inter** as preferred; canonical `brand/tokens/brand-tokens.css` ships **Arial** (`--ls-font-*: Arial`). The doc's own example CSS (line 1046) uses Inter, but the existing CSS file does not. | §6.1, §21.3 example CSS | `brand/tokens/brand-tokens.css` line 1 (`--ls-font-display: Arial, sans-serif`); `brand/tokens/brand-tokens.css` throughout; doc §6.1 p265 | P1 |
| 2 | **Spacing scale mismatch** — doc §7.3 defines `space.1`–`space.24` (4px–96px, 24 values); canonical `brand/tokens/brand-tokens.css` defines `space.1`–`space.8` (4px–64px, 8 values). Key mismatches: doc `space.5=20px` vs canonical `space-5=24px`; doc `space.6=24px` vs canonical `space-6=32px`; doc `space.8=32px` vs canonical `space-8=64px`. | §7.3 | `brand/tokens/brand-tokens.css` lines 1–8 (spacing variables); doc §7.3 table lines 350–362 | P1 |
| 3 | **Stale path references** in doc §21.2 — suggested token structure references `src/brand/design-decisions.md` (exists) and `static/brand/BRAND_GUIDELINES.md` (mirror; canonical is `brand/guidelines/brand-guidelines.md` per `brand/CANONICAL_SOURCES.md` updated 2026-10-13, one day **before** the design doc merged 2026-10-14). | §21.2 | `brand/CANONICAL_SOURCES.md` line 35–36: canonical guidelines = `brand/guidelines/brand-guidelines.md`; doc §21.2 references `static/brand/BRAND_GUIDELINES.md`; `brand/guidelines/brand-guidelines.md` §21.2 references (no exact line) | P2 |
| 4 | **Ownership role gap** — doc §22 defines roles (Executive sponsor/brand owner, Design-system steward, Content owner, Engineering owner, Research owner, AI agents) that do not map 1:1 to the 93 agent ids in `company-registry.yaml`. No agent is designated "Design-system steward" in the registry. | §22.1 | `company-registry.yaml` — 93 agent ids; none with id `design_system_steward` or equivalent; roles like `product_designer`, `creative_director`, `cto`, `cdo` present but undocumented mappings | P2 |
| 5 | **AI-agent operating instructions vs AGENTS.md §15** — doc §24.1–24.14 echoes AGENTS.md §15 evidence policy and §8 tool vocabulary, but doc §24 line 1190 ("Read existing repository guidance and canonical brand files before changing design assets") aligns with `brand/CANONICAL_SOURCES.md`; however doc §24 line 1201 ("Avoid creating duplicate token files or competing sources of truth") conflicts with the existence of both `brand/tokens/brand-tokens.css` (canonical) and `static/brand/brand-tokens.css` (mirror, may be stale). | §24 | `brand/CANONICAL_SOURCES.md` §2, §19–30 (mirror vs canonical); AGENTS.md §8 (canonical 7 tools); AGENTS.md §15 (honesty evidence policy) | P1 |
| 6 | **Public/internal boundary exception** — doc §20.7 and §2.4 acknowledge that internal tools (CEO dashboard, agent workspaces) may differ from public brand, but the ls-design-system skill explicitly states: *"The CEO Dashboard (`src/ai_company/dashboard/`) uses the J.A.R.V.I.S. theme with the 'LS' placeholder. It is **internal** and **NOT public-facing brand** — do NOT rebrand it."* This exception is not repeated in the new design system doc. | §2.4, §20.7 | `ls-design-system` skill §Dashboard Exception; `src/ai_company/dashboard/app.py` J.A.R.V.I.S. theme; AGENTS.md §13 (app boundary — dashboard vs Vite are independent apps) | P1 |

---

## 2. Ownership Mapping (doc §22 ↔ registry)

The doc §22.1 defines six governance roles. Mapping to the existing registry:

| Doc Role | Registry Equivalent(s) | Gap | Recommendation |
|---|---|---|---|
| Executive sponsor / brand owner | `human_ceo` (user proxy), `ceo_advisor` | Role exists but is the human user; no automated agent maps here. | Document `human_ceo` as the ultimate approval gate; `ceo_advisor` supports memo drafting. |
| Design-system steward | **None** in registry | Critical gap — no agent owns token maintenance, review workflow, or QA gate. | Assign to `caio` (AI research lead) or create a new agent card; add to `company-registry.yaml`. |
| Content owner | `content_creator`, `market_analyst`, `product_marketing_manager` | Content review exists but not formally linked to doc claims-provenance workflow (§22.3). | Map `content_creator` as the content owner; add claims registry workflow. |
| Engineering owner | `lead_backend`, `lead_frontend`, `vp_engineering`, `cto` | Engineering oversight exists organization-wide but not scoped to design-tokens QA. | Assign `lead_frontend` + `lead_backend` as co-owners; add token-QA gate to release checklist. |
| Research owner | `agentic_research_lead`, `thought_leadership_lead`, `data_privacy_officer` | Research validation exists (Pharos department) but not formalized against doc §12.5/§22.3. | Map `thought_leadership_lead` as research owner; integrate with doc QA checklist. |
| AI agents / automated tools | All agent cards (`.opencode/agents/*.md`) | Doc §24.11 ("Escalate conflicting brand instructions instead of silently choosing one") needs a concrete escalation path in the harness. | Add escalation workflow to `harness/changes/` INDEX.json; reference in ECL. |

---

## 3. Prioritized Realignment Recommendations

### P0 — Must resolve before doc adoption

| # | Recommendation | Target | Concrete Change | Owner |
|---|---|---|---|---|
| P0.1 | **Fix typography default** — align doc's example CSS with canonical implementation, or update canonical CSS. | `brand/tokens/brand-tokens.css` line 1 + doc §6.1 / example CSS line 1046 | Change `--ls-font-display: Arial, sans-serif` to `--ls-font-sans: Inter, ui-sans-serif, system-ui, sans-serif` in `brand/tokens/brand-tokens.css` **OR** change doc §6.1 default to Arial and update the example CSS. Per doc §25 order: canonical tokens (3) outrank agent assumptions (6). If canonical is kept as Arial, doc must explicitly state Arial is the deployed default and the Inter reference is a proposed fallback. | `cdo` / `registry_owner` |
| P0.2 | **Publish design-system steward** — assign ownership of token maintenance and review workflow. | `company-registry.yaml` + agent card `.opencode/agents/design-system-steward.md` (new) | Add agent id `design_system_steward` to registry; create agent card; assign responsibilities per doc §22.1 (maintain tokens, patterns, documentation, review workflow). | `caio` / `chief-of-staff` |
| P0.3 | **Map ownership roles to registry ids** — complete the §22.1→registry mapping table. | `company-registry.yaml` + this report | For each doc role, add a `mapping` annotation or inline comment in the registry YAML; publish the mapping table as `docs/DESIGN_SYSTEM_ROLE_MAPPING.md`. | `chief-of-staff` |

### P1 — Should resolve for coherence

| # | Recommendation | Target | Concrete Change | Owner |
|---|---|---|---|---|
| P1.1 | **Resolve spacing scale** — harmonize doc and canonical tokens; document which takes precedence per doc §25. | `brand/tokens/brand-tokens.css` spacing variables + doc §7.3 table | Option A: Expand canonical CSS to match doc's full `space.1`-`space.24` scale (add `space.5=20px`, `space.6=24px`, `space.8=32px` adjustments). Option B: Condense doc table to match canonical 8-token scale and reference "custom values permitted with justification." Per doc §25 order: canonical repo tokens (3) outrank doc proposed defaults (2) before adoption. | `cdo` / `registry_owner` |
| P1.2 | **Clarify guideline path** — doc §21.2 should reference canonical guidelines path, not mirror. | Doc §21.2 suggested token structure | Change `static/brand/BRAND_GUIDELINES.md` to `brand/guidelines/brand-guidelines.md` in the directory listing. Add a note: "If `static/brand/BRAND_GUIDELINES.md` exists, reconcile via `pwsh scripts/build/sync-brand.ps1` per `brand/CANONICAL_SOURCES.md`." | `content_creator` |
| P1.3 | **Make internal dashboard exception explicit** — add a sidebar or §2.4/§20.7 callout referencing the J.A.R.V.I.S. theme exception. | Doc §2.4, §20.7, and `ls-design-system` skill | Add boxed callout: *"Internal tools (CEO dashboard, agent workspaces) may use modified themes (e.g. J.A.R.V.I.S.) that differ from public brand tokens. Do not rebrand internal surfaces. See AGENTS.md §13 for app boundary."* | `cto` / `security-compliance-lead` |
| P1.4 | **Align AI-agent operating instructions with AGENTS.md** — harmonize §24 with AGENTS.md §8 (canonical 7 tools) and §15 (evidence policy). | Doc §24 + AGENTS.md §8, §15 | Ensure doc §24.2–24.13 language does not introduce tool names beyond the canonical 7 (read, edit, grep, list, bash, webfetch, task). Update doc to reference AGENTS.md §8 instead of duplicating. | `security-compliance-lead` |

### P2 — Nice-to-have for completeness

| # | Recommendation | Target | Concrete Change | Owner |
|---|---|---|---|---|
| P2.1 | **Prune doc §21.3 to canonical file list** — only `brand-tokens.json` and `brand-tokens.css` exist canonically; doc §21.3 listing of four additional JSON families is stale. | `doc §21.3` + `brand/CANONICAL_SOURCES.md` | Update doc §21.3 suggested token structure (line 998–1017) to list only `brand-tokens.json` and `brand-tokens.css`. Remove the four stale JSON family entries (`color-tokens.json`, `typography-tokens.json`, `spacing-tokens.json`, `motion-tokens.json`). Per doc §1019: "If a repository already has canonical files such as ... reconcile and consolidate before introducing duplicates." | `cdo` |
| P2.2 | **Annotate registry with doc-role mappings** — add inline `mapping` comments to `company-registry.yaml` for each doc §22.1 role, and publish the mapping table in this report. | `company-registry.yaml` + this report | For each doc role (Executive sponsor/brand owner, Design-system steward, Content owner, Engineering owner, Research owner, AI agents), add a `mapping` annotation comment beside the nearest matching agent id in `company-registry.yaml`. Publish the completed mapping as a sidebar in `docs/ORG_DESIGN_SYSTEM_REALIGNMENT.md`. Do not create a separate doc; the mapping lives in the registry and is referenced from the report. | `chief-of-staff` / `registry_owner` |
| P2.3 | **Design-decisions.md is superseded** — doc §21.2 references `src/brand/design-decisions.md`; this file records retired hardware-console decisions (archived per §5 Website Transformation & Repository Consolidation Directive). All current design decisions live in the canonical design system doc and `brand/tokens/brand-tokens.css`. No content update needed; the archived file is documented for historical reference only. | `src/brand/design-decisions.md` (archived, read-only) | No action required; file is retired per §5 directive. The canonical token structure and design decisions are maintained in `LightSpeed_Holdings_Organization_Design_System.md` §6–§7 and `brand/tokens/brand-tokens.css`. | `product-designer` (no-action; file is read-only archived) |

---

## 4. Adoption Roadmap (per doc §26)

| Phase | Actions | Timing | Deliverable |
|---|---|---|---|
| **Phase 1: Establish consistency** (immediate) | - P0.1: Fix typography default (P0) <br> - P0.2: Publish design-system steward <br> - P0.3: Map ownership roles <br> - Reconcile doc with canonical tokens per §25 order | Sprint 1–2 (before public MVP launch) | `docs/ORG_DESIGN_SYSTEM_REALIGNMENT.md` + registry updates + canonical CSS/spacing fixes |
| **Phase 2: Build reusable foundations** (Sprint 3–4) | - P1.1: Harmonize spacing scale <br> - P1.2: Clarify guideline path <br> - P1.3: Make internal dashboard exception explicit <br> - P1.4: Align AI-agent instructions with AGENTS.md | After Phase 1 sign-off | Updated doc (published), updated agent cards, escalation workflow |
| **Phase 3: Expand carefully** (Sprint 5+) | - P2.1: Add missing token families (or prune doc) <br> - P2.2: Populate ownership matrix <br> - P2.3: Verify `design-decisions.md` <br> - Extend patterns to internal tools, venture-building artifacts | After Phase 2 sign-off | Full maturity per doc §26 roadmap; new templates, checks, and governance artifacts |

**MVP rule (doc §26.3):** *"Apply the smallest coherent subset required to launch credibly, then expand in controlled increments."* — The P0 items are the minimum for a credible launch. P1/P2 follow in controlled increments.

---

## 5. Evidence Appendix

### 5.1 Conflict 1: Typography default

- **Doc §6.1** (line 265): *"Use a modern sans-serif family with excellent screen legibility. **Inter** is the preferred implementation default where licensing, loading, and environment permit."*
- **Doc example CSS** (line 1046): `--ls-font-sans: Inter, ui-sans-serif, system-ui, sans-serif;`
- **Canonical `brand/tokens/brand-tokens.css`** (line 1): `--ls-font-display: Arial, sans-serif;` and throughout the file all `--ls-font-*` declarations use Arial.
- **Doc §21.3 example CSS** (lines 1023–1065) uses Inter but the existing canonical file uses Arial.
- **Severity P1:** Per doc §25 conflict resolution order, canonical repo tokens (position 3) outrank agent assumptions (position 6), but the doc itself acknowledges (line 1237): *"Before adopting this document as fully canonical, reconcile it with the actual approved logo files, current production tokens, and existing repository documentation."*

### 5.2 Conflict 2: Spacing scale mismatch

- **Doc §7.3 table** (lines 350–362): `space.1=4px` through `space.24=96px` (24 entries).
- **Canonical `brand/tokens/brand-tokens.css`** (lines ~1–8): `--ls-space-1: 4px; --ls-space-2: 8px; --ls-space-3: 12px; --ls-space-4: 16px; --ls-space-5: 24px; --ls-space-6: 32px; --ls-space-7: 48px; --ls-space-8: 64px;` (8 entries).
- **Specific mismatches:**
  - Doc `space.5=20px` vs canonical `space-5=24px` (line 355 vs canonical)
  - Doc `space.6=24px` vs canonical `space-6=32px` (line 356 vs canonical)
  - Doc `space.8=32px` vs canonical `space-8=64px` (line 357 vs canonical)
- **Doc §7.3 final sentence** (line 364): *"Use fewer, consistent spacing values rather than one-off measurements."* — contradicts the doc's own 24-value table density.
- **Severity P1:** Mismatch documented; resolution per §25 order requires reconciling canonical tokens (3) before doc defaults (2).

### 5.3 Conflict 3: Stale path references

- **Doc §21.2** (lines 998–1017): suggested token structure lists directories `brand/`, `brand/tokens/`, `brand/assets/`, `brand/examples/`, `brand/` with sub-paths including `static/brand/BRAND_GUIDELINES.md`.
- **`brand/CANONICAL_SOURCES.md`** (lines 35–36, updated 2026-10-13): *"`static/brand/BRAND_GUIDELINES.md` (quick reference; canonical is `brand/guidelines/brand-guidelines.md`)."
- **Temporal gap:** `brand/CANONICAL_SOURCES.md` was updated 2026-10-13; the design doc (PR #467, commit 854c5924) was merged 2026-10-14 — the canonical cleanup preceded the doc merge by one day, meaning the doc's path references are stale relative to the updated canonical registry.
- **Severity P2:** Path reconciliation is advisory per doc §25; not blocking adoption but should be corrected.

### 5.4 Conflict 4: Ownership role gap

- **Doc §22.1** (lines 1098–1107): defines six roles — Executive sponsor/brand owner, Design-system steward, Content owner, Engineering owner, Research owner, AI agents.
- **`company-registry.yaml`** (full list of 93 ids, confirmed read): contains none of the exact role titles. Closest matches: `human_ceo` (executive sponsor), `cto`/`lead_backend`/`lead_frontend` (engineering owner), `thought_leadership_lead`/`content_creator` (content owner), but no "Design-system steward."
- **Severity P2:** Governance gap — the doc defines roles but the org has no designated steward. Recommendation (P0.2) assigns this to a new or existing agent.

### 5.5 Conflict 5: AI-agent operating instructions

- **Doc §24.1** (line 1186): *"Any AI agent producing LightSpeed artifacts must treat this document as a binding design constraint unless a higher-authority, explicitly approved directive supersedes it."*
- **Doc §24.2–24.14** (lines 1188–1203): 13 implementation rules, including §24.11 ("Escalate conflicting brand instructions instead of silently choosing one") and §24.12 ("Avoid creating duplicate token files or competing sources of truth").
- **AGENTS.md §8** (canonical 7 tools): `read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task` — no tool names beyond these.
- **AGENTS.md §15** (honesty evidence policy): 12 rules mirroring doc §24's substance (no fabricating evidence, distinguish proposed from implemented, test themes, report changes, etc.).
- **Severity P1:** The doc's §24 rules are coherent with AGENTS.md but introduce duplication; harmonization recommended.

### 5.6 Conflict 6: Public/internal boundary

- **Doc §2.4** (lines 92–99): defines public website vs internal dashboards/agent workspaces/operational reports/confidential CEO materials.
- **Doc §20.7** (lines 972–983): *"Internal tools may be denser and more utilitarian than public pages, but should retain the same tokens, typography, interaction states, and information clarity."* Also: *"AI-generated artifacts must follow this system and must not ... silently alter canonical brand tokens."*
- **`ls-design-system` skill** (Dashboard Exception section): *"The CEO Dashboard (`src/ai_company/dashboard/`) uses the J.A.R.V.I.S. theme with the 'LS' placeholder. It is **internal** and **NOT public-facing brand** — do NOT rebrand it."*
- **AGENTS.md §13** (app boundary, last updated 2026-10-07): *"The CEO Dashboard (internal) and the Vite/React app (external) are two independent applications..."*
- **Severity P1:** The new doc does not repeat the internal-exception language; risk that agents may attempt to rebrand internal surfaces. Recommendation (P1.3) adds explicit callout.

---

## 6. Conclusion

The `LightSpeed_Holdings_Organization_Design_System.md` v1.0 is a well-structured proposed baseline that aligns substantially with LightSpeed's existing canonical brand system (`brand/**` per `brand/CANONICAL_SOURCES.md`). Six conflict categories were identified, ranging from P0 (typography default, design-system steward ownership) through P1 (spacing scale, AI-agent instructions, internal/dashboard exception) to P2 (path references, missing token families, ownership matrix).

**The doc's own §25 conflict resolution order and §26 roadmap provide a coherent framework for incremental adoption.** The P0 items are the minimum viable set for a credible public MVP launch; P1 and P2 follow in controlled phases.

**Immediate next steps (Phase 1, Sprint 1–2):**
1. Resolve P0.1: Fix typography default (doc §6.1 vs canonical CSS) — decide Arial vs Inter, update canonical or doc.
2. P0.2: Assign design-system steward in `company-registry.yaml` and create agent card.
3. P0.3: Map doc §22.1 roles to registry agent ids; publish mapping.
4. Reconcile doc with canonical tokens per §25 order (canonical repo tokens position 3 before doc proposed defaults position 2).
5. Run `pwsh scripts/build/sync-brand.ps1 -Verify` to confirm mirror–canonical alignment after any canonical asset changes.

**Approval path:** Per doc §25 line 1: *"Explicit, current approval from the brand owner / CEO"* is the highest authority. This report should be reviewed by the human CEO (user proxy) and the design-system steward before the doc is adopted as fully canonical.

---
*Report generated via multi-agent review plan (plan mode → build mode). Conflicts verified against `brand/CANONICAL_SOURCES.md` (updated 2026-10-13), `brand/tokens/brand-tokens.json` and `brand/tokens/brand-tokens.css` (canonical), `brand/guidelines/brand-guidelines.md` (human-readable guidelines), `company-registry.yaml` (93 agent ids), `AGENTS.md` (dispatch/evidence/tool vocabulary), `ls-design-system` skill (brand baseline and dashboard exception), and the full design system doc (1285 lines, merged 2026-10-14, PR #467).*
