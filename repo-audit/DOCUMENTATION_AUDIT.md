# Documentation Audit

**38 tracked `.md` files at repo root.** `docs/` holds another 565. Documentation is
the most visible form of the repository's clutter.

---

## 1. The four documents that actually matter

| Document | Role | Assessment |
|---|---|---|
| `AGENTS.md` | primary agent operating contract; 11 numbered sections, §4 context-loading, §8 tool vocabulary, §9 governance, §10 verification, §11 key rotation | **Good.** The strongest asset in the repo. Needs §9.2 corrected (see §5). |
| `README.md` | human + agent entry point | **Stale** — must become the canonical entry (§36). |
| `LICENSE` | legal | KEEP |
| `CONTRIBUTING.md` | contribution guide | KEEP |

## 2. Stale cross-references — the important defect

`AGENTS.md` §1 and §3 point to documents that **do exist in `docs/`**. The defect is
staleness and accuracy, not missing files:

| Referenced | Expected path | Exists? | State |
|---|---|---|---|
| Architecture | `docs/ARCHITECTURE.md` | **YES** | 16.1 KB, last modified 2026-09-21 — stale |
| Development | `docs/DEVELOPMENT.md` | **YES** | 8.3 KB, last modified 2026-10-01 — refresh |
| ECL | `docs/ECL.md` | **YES** | 7.6 KB, last modified 2026-09-16 — stale |
| Harness lint | `scripts/lint-ecl.ps1` | **YES** | verified present |
| Generator regen | `python -c "from ai_company.generator import ..."` | verified | canonical package is `src/ai_company/` |

`AGENTS.md` §1 presents these as the three documents to read first, and §3 tabulates
them. They resolve, but their content has drifted from verified reality (counts,
paths, cleanup state).

**Disposition: REFACTOR** `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`,
`docs/ECL.md` against verified facts. `ARCHITECTURE_MAP.md` in this audit is
source material; `docs/REPOSITORY_CLEANUP_PLAN.md` is the authority for cleanup
state.

> `docs/` contains 429 tracked Markdown files. Volume, not broken links, is the
> documentation problem here.

## 3. Root-level document sprawl (38 files)

### Directives (historical, one-shot) — ARCHIVE to `docs/directives/`
```
GEOGRAPHIC POSITIONING & MARKET ARCHITECTURE REFINEMENT DIRECTIVE.md
REBUILD_DIRECTIVE.md
WEBSITE TRANSFORMATION & REPOSITORY CONSOLIDATION DIRECTIVE.md
lightspeed-aistudio-opencode-handoff-directive.md
lightspeed-narrative-positioning.md
lightspeed-opencode-migration-directive.md
LIGHTSPEED REPOSITORY SANITIZATION & STREAMLINING DIRECTIVE.md   ← this audit
RENDER-HOSTING-PLAN.md
TARGET_ARCHITECTURE.md
```

### Specs / audits — ARCHIVE to `docs/` or `reports/`
```
MASTER_SPEC.md   SPEC.md   Plan.md   SPECIFICATION_MAP.md
IMPLEMENTATION_AUDIT.md  LEGACY_INVENTORY.md
SECURITY_AUDIT_REPORT.md  UX_VALIDATION_REPORT.md
WCAG_AA_FIX_SUMMARY.md    ISSUE_382_IMPLEMENTATION_SUMMARY.md
REGRESSION_TEST_PLAN_374.md  TESTING.md  DEPLOY_TEST.md
```

### Analysis / one-off reports — ARCHIVE to `reports/`
```
analysis_taxonomy.md  knowledge-model-analysis.md
brand-strategy-validation-report.md
seo-specialist-analysis.md  dual_environment_compatibility_standard.md
issue-381-amended-policy.md  sadc-research-scan-2026-09-17.md
JEV_INTEGRATION_BRIEF.md  CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE.md
WAYFINDER_IMAGE_MAP.md
```

### Governance — RELOCATE to `docs/`
```
SECURITY.md  security-checklist.md  CHANGELOG.md  DEPLOYMENT.md
```
`DEPLOYMENT.md` and `SECURITY.md` belong in `docs/`; `CHANGELOG.md` conventionally
stays at root.

### DEFECT — file literally named `.md`
A tracked root file named exactly `.md` exists. A hidden file with an extension and
no name. Needs inspection: it is either a botched write or a placeholder, and it is
invisible in most listings.

**Disposition: INVESTIGATE** (read contents, then DELETE or rename).

## 4. Directive-required documentation status (verified 2026-10-06)

| Required | §ref | Status |
|---|---|---|
| `README.md` documenting canonical setup/validation/deploy | §36 | exists but stale |
| `docs/ARCHITECTURE.md` | §10 / §36 | **EXISTS** — needs accuracy refresh |
| `docs/DEVELOPMENT.md` | §10 / §36 | **EXISTS** — needs accuracy refresh |
| `docs/ECL.md` | §10 / §36 | **EXISTS** — directive never names ECL; kept because `AGENTS.md` references it |
| `docs/DEPLOYMENT.md` | §10 (explicitly listed in its doc inventory) | **MISSING** — 4 competing docs exist instead |
| `docs/AGENTS.md` or canonical agent onboarding | §36 (agent instructions must be current) | satisfied by root `AGENTS.md` |
| Canonical repo-wide health check | §26 | **MISSING** — partial gates only |
| `docs/REPOSITORY_HEALTH.md` | §37 — the only §37 deliverable | genuinely absent; due after cleanup |
| Root README must not duplicate `docs/` content | §36 | not yet enforced |

## 5. Documentation quality findings

- **`AGENTS.md` §9.2 claims `scroll-craft` is deleted.** It is not — 692 MB remains
  under `.opencode/skills/scroll-craft/`. Documentation and reality disagree, and the
  documentation is the one agents trust. Either the policy or the tree must change.
- **No single entry point.** An agent or new developer must guess whether to read
  `README.md`, `AGENTS.md`, `MASTER_SPEC.md`, `TARGET_ARCHITECTURE.md`, or one of the
  directives. §36 requires the entry point to be obvious.
- **RETRACTED — no such reference exists.** An earlier draft claimed `AGENTS.md`
  names "lmstudio" and that §40 restricts competitor references. Both premises are
  false. §40 reads only "**Do not optimize for the number of files deleted.**"
  and imposes no competitor-reference rule. Direct search found no `lmstudio` or
  "LM Studio" string in `AGENTS.md`, `README.md`, or `company-registry.yaml`; the
  only occurrences in the tree are test fixtures inside
  `open-design/apps/daemon/tests/runtimes/run-failure-telemetry-smoke.test.ts`.
  No action required.
- **Docs describe a runtime the repo does not contain.** The `open-design` nested
  repo has its own `AGENTS.md`/`CLAUDE.md`/`CONTEXT.md`, which can be mistaken for
  LightSpeed documentation.

## 6. Disposition summary

| Category | Count | Action |
|---|---:|---|
| Canonical root docs | 4 | KEEP, refresh README |
| Directives | 9 | ARCHIVE → `docs/directives/` |
| Specs/audits | 14 | ARCHIVE → `docs/` or `reports/` |
| Analysis reports | 11 | ARCHIVE → `reports/` |
| Governance | 4 | RELOCATE → `docs/` |
| Anomalous (`.md`, `test_fragment.tsx`) | 2 | INVESTIGATE |
| Referenced-but-missing | 3 | CREATE or fix links |
