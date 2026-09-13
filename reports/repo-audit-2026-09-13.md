# LightSpeed Holdings — Full Repository Audit

**Date:** 2026-09-13
**Mode:** READ-ONLY audit. No files were modified, regenerated, or deleted. All fixes pending human approval.
**Scope:** Entire monorepo including vendored/generated trees (inspected; runtime state distinguished from source).
**Method:** 10 subagent audit team (inventory ×3, alignment ×3, code ×3, docs/skills ×2) + `graphify update` (25,635 nodes / 38,933 edges) + CI/pytest/pre-commit read-only checks.

---

## 1. Executive Summary

The repo is **internally consistent where it matters most**: 144/144 agents trace 1:1 between `company-registry.yaml` and `.opencode/agents/*.md`, all 144 cards use only the canonical 7 tools, pytest collects green (0 errors), `tsc --noEmit` and ruff are clean, and no secrets are git-tracked.

However, there are **5 critical/blocker-grade issues** (2 registry runtime bugs, 1 broken live JS file, 1 dead CI workflow pointing at a phantom directory, 1 fresh-clone config break), ~**70 major findings**, and large volumes of orphan/stale/redundant material.

### Headline counts

| Category | Estimate |
|---|---|
| Registry/config runtime bugs (misalignment) | 2 critical parsers + 2 config trees duplicated |
| Broken live files | 1 JS (dashboard), 1 CI workflow (phantom dir) |
| Orphan/stale files & folders | ~40 (incl. 144 `.bak` cards, 63 orphan docs, 25 dead frontend files) |
| Redundant/overlapping skills | ~20 (8 pharos wrappers, 6 ponytail, docs blob, duplicates) |
| Root-level junk files | ~19 tracked + ignored debris |
| Git hygiene gaps | 2 untracked-not-ignored dirs (5.8 MB) |

### Top 10 highest-value actions (proposed — awaiting approval)

1. **Fix registry parser bugs** — `kpis` schema mismatch (registry.kpis always empty) and dropped `guardrails` (src/ai_company/registry/parser.py:77-99,136-139).
2. **Track required orchestrator configs** — `orchestrator/{escalation,scheduler}.yaml` are gitignored but `ai-company validate config` fails without them (fresh clone breaks).
3. **Fix broken dashboard JS** — `src/ai_company/dashboard/static/js/command-bar.js` missing closing `});` (syntax error, breaks command bar).
4. **Fix or delete `site.yml`** — references non-existent `lightspeed-main-site/`; frontend CI never runs and root JS lockfiles are never installed/tested.
5. **Add registry validation to CI** — `load_registry()`/`ai-company validate agents` is never invoked in `.github/workflows/ci.yml`.
6. **Archive `Branding landing page/` + `scientific-agent-skills/` + kill `.bak` litter** (~150 .bak files, 2 MB `.opencode/audit`, snapshots).
7. **Create `docs/README.md`** — fixes ~63 orphan docs at once; repoint SOP links to v2 (currently active SOPs are unreachable).
8. **Consolidate skills** — delete 8 pharos-* wrappers (mirror roster cards), merge ponytail family (6→2), delete duplicate `no-ai-slop`, move `.agents/skills/docs/` blob.
9. **Remove dead frontend cluster** (~25 unreachable pages/components) and reconcile `website/` + brand copy chain.
10. **Untrack live runtime data** — `orchestrator/approvals.yaml`, `dashboard/kpi_history/*.ndjson`; track `data/catalog/`.

---

## 2. A. MISALIGNMENT (registry ↔ code ↔ CI ↔ docs)

### 2.1 Runtime/registry bugs (CRITICAL)

| Severity | Finding | Evidence | Action |
|---|---|---|---|
| CRITICAL | `_parse_kpis` expects flat list but `config/company/kpis.yaml` uses `{company, executive}`; `registry.kpis` is always `[]` | `src/ai_company/registry/parser.py:136-139` | fix parser |
| CRITICAL | `guardrails` loaded by loader but never consumed by model; registry always defaults | `parser.py:77-99`, `loader.py:61`, `models.py:718` | wire through |
| CRITICAL | `orchestrator/escalation.yaml` + `scheduler.yaml` gitignored (`.gitignore:78`) but required by `cli/validate.py:265-266`; fresh clone fails `ai-company validate config` | `.gitignore:78`, `cli/validate.py:265-266`, `dashboard/repository.py:42-43` | `git add -f` upfront + fix ignore |

### 2.2 Config tree duplication/conflicts (MAJOR)

| Finding | Evidence | Action |
|---|---|---|
| `config/departments/departments.yaml` (19 depts, `_` ids) vs `company/departments.yaml` (20 depts incl. Board+Pharos, `-` ids) — divergent truth | `resolver.py:57` special-cases `human_ceo`; `generator.py:279-281`, `api.py:1699/1851` use hyphenated | reconcile to one canonical, mirror the other |
| `company/config/*.yaml` overlaps `config/company/*.yaml` (kpis read from different paths by dashboard vs tests) | `cli/dashboard.py:255` vs tests | merge `company/config/` → `config/company/` |
| `config/company/scheduler.yaml` (59 lines) is dead — live twin is `orchestrator/scheduler.yaml` (10 bytes) | consumers all use `orchestrator/` (api.py:627,1813,2055; validate.py:266…) | archive dead copy |
| `config/routing.yaml` only referenced by existence check; `company/config/webhooks.yaml` only docs-ref | `cli/validate.py:287`; ADR-017 | wire-in or drop |
| `company/models.yaml.executor-bak` stale backup in canonical dir | no refs | archive |
| `config/board/board.yaml` referenced in constitution/CHANGELOG but doesn't exist (restructured to `config/board/{committees,meetings,voting}.yaml`); `cli/board.py:13` reads root `board/board.yaml` instead | `.ai-company/constitution/14-DESIGN-PRINCIPLES.md:170`, `cli/board.py:13` | fix refs + wire CLI path |

### 2.3 CI/validation gaps (MAJOR)

| Finding | Evidence | Action |
|---|---|---|
| Generator CI runs `use_full_registry=False` (raw YAML render) — never exercises loader→parser→resolver→validator | `generator.py:220-226`, `.github/workflows/ci.yml` | add `load_registry()` / `ai-company validate agents` step |
| `site.yml` builds phantom `lightspeed-main-site/` (does not exist); frontend job & deploy-pages never run; both `package-lock.json` + `bun.lock` tracked but no job installs them | `site.yml:32,39`, `git ls-files lightspeed-main-site` empty | repoint or delete; wire frontend job |
| `e2e` job non-blocking; `tests/performance/*` never run in CI | `ci.yml:131-177,302` | wire-in or document |
| vitest configured + `src/__tests__` present but `package.json` has no `test` script and no CI runs it | `vitest.config.ts`, `package.json` | add script+job or delete |
| `scripts/validate-drift.ps1:37,44-47` uses bare `python` (fails without venv on PATH) | `scripts/validate-drift.ps1` | use `uv run python` |

### 2.4 Documentation drift on template counts (MAJOR)

Reality: **9** `.j2` templates (`templates/{base,board,config,department,executive,postmortem,specialist,workflow}.md.j2` + `agents/agent.md.j2`). Sources still claiming **12**:
`docs/ARCHITECTURE.md:177,238`, `docs/STATUS.md:49` (also names ghost templates `specialist_v2/board_v2/sop/raci.md.j2`), `docs/diagrams.md:116`, `docs/SPRINT-1-TRACKER.md:114`, `docs/PROJECT-STATUS-ASSESSMENT.md:46`, `docs/AGENT-REGISTRY-TABLE.md:222`, and the registry's own `generator-owner` entry (`company-registry.yaml:840-848`) → propagates into the generated card + table. Also 5 docs claim cards render via a single `templates/agents/agent.md.j2` (docs/PROMPT-ENGINEERING-GUIDE.md:11, docs/sop-deployment.md:141, docs/PHASE-1-COMPLETE.md:40, docs/Pharos/h-a-o-m-t-g-v-framework.md:244, README.md:286) — actually per-type `_TEMPLATE_MAP` (generator.py:45-52). The drift validator already canonizes 9 (`docs/source-of-truth.yaml:80`).

Other stale claims: `docs/source-of-truth.yaml:22-23` ("departments has 19") → now 20; `docs/STATUS.md:7` "Last Updated 2026-08-31"; `STATUS.md:125` → missing `docs/REMAINING-WORK-INVENTORY.md`; `STATUS.md:106` → retired `adr/011`; `STATUS.md:45-48` agent counts (127/135) vs 144.

### 2.5 Agent cards / tool vocabulary

- 144 registry ids ↔ 144 cards: **1:1, 0 orphans, 0 missing, 0 field mismatches**. All cards `mode: subagent`, canonical 7 tools only, zero `tools:` fields, zero legacy aliases (write/execute/delegate/web_search/code_interpreter). Cards are aligned — **do not regenerate**.
- Registry source file still uses legacy tool names (~250 instances) — intentional, normalized by `generator._TOOL_MAP` (generator.py:31-42,104-106). `company/registry-templates/consulting-firm/company-registry.yaml:18-20` mislabels `write/execute` as "canonical" in a comment — fix comment.
- `templates/agents/agent.md.j2` is dormant (no registry agent of `type: agent`) — keep, note.

---

## 3. B. ORPHAN FOLDERS / FILES

### 3.1 Root folder verdicts (top-level)

| Dir | Verdict | Evidence / action |
|---|---|---|
| `scientific-agent-skills/` | **CRITICAL orphan** — embedded empty git clone (origin k-dense), 0 files, not a submodule | delete (or re-init submodule) |
| `Branding landing page/` | **major** — 52 tracked client-brand assets, byte-identical copies of `brand/` + `static/brand/`, single ✅-checkbox ref | archive to `brand/` source-of-record |
| `prompts/` | major orphan — 1 file, 0 refs; builder seeds `prompts/{system,task,few-shot}` that don't exist (`builder/__init__.py:37-39`) | archive or align |
| `memory/memory-index.yaml` | minor orphan — empty skeleton, engine never reads it | delete |
| `knowledge/company/MISSION.md` | minor orphan — mission duplicated in `.ai-company/constitution/01-MISSION.md` + `docs/MISSION_AND_VISION.md` | archive |
| `workflows/new-strategic-request.md` | minor orphan | archive |
| `research/` (root) | minor orphan — 4 files unlinked; live docs live in `docs/research/` | merge into `docs/research/` |
| `board/` per-role docs | minor — 62 legacy scaffolds, 0 code readers; `board/board.yaml` IS read | archive docs, keep board.yaml |
| `orchestrator/` | keep — live state dir, but `approvals.yaml` (~21k lines) is committed; scheduler/escalation untracked | untrack data; track required configs |
| `dashboard/` | keep — live KPIHistoryStore NDJSON, though SQLite migration in flight (`data/database.py:116`) | untrack NDJSON |
| `dashboard` | keep | — |
| `company/`, `config/`, `hr/`, `memory/`, `knowledge/`, `static/`, `public/`, `tasks/`, `workflows/`, `results/`, `archive/` | keep (wired) | — |
| `dist/`, `node_modules/`, `models/`, `bin/`, `backups/`, `logs/`, `.crush/`, `.hypothesis/`, `.benchmarks/` | keep (gitignored runtime/vendored) | retention: backup.ps1 keep-14 policy not met (backups stale since 8/29) |

### 3.2 Root loose files

Tracked orphans (0 refs, git-tracked → delete/archive): `temp_issue_207.md`, `temp_issue_208.md`, `test_agent_perf.py`, `test_etl_pipelines.py`, `test_transformer.py` (all 3 excluded from pytest via `testpaths=["tests"]` at pyproject.toml:113 and run side-effects on import), `performance-testing-matrix.md`, `security-checklist.md`, `accessibility-checklist.md`, `SECURITY_AUDIT_REPORT.md` (duplicates `docs/SECURITY_AUDIT_REPORT.md` with different content), `BRAND_AUDIT_REPORT.md`, `brand-strategy-validation-report.md`, `QA_ANALYSIS.md`, `UX_VALIDATION_REPORT.md`, `TESTING.md` (referenced only as non-existent `docs/TESTING.md`).

Ignored debris (delete): `run.json`, `pytest_output.txt`, `test_errors.txt`, `test_output.txt`, `tsconfig.tsbuildinfo`, `.env.local` (0 B), `.opencode/package-lock.json` (invalid JSON).

`metadata.json`, `index.html`, `Makefile`, `Dockerfile`, `package.json`, config files → keep (wired).

### 3.3 Runtime/state (.opencode and logs)

| Path | Finding | Action |
|---|---|---|
| `.opencode/agents/*.md.bak` (144) | redundant — one-generation-old snapshots (8/31–9/3 vs cards 9/13), gitignored; reproducible via `AgentGenerator().generate_all()` | delete for hygiene (write-path still backs up going forward) |
| `.opencode/suspended_states/` | 19 orphan `.bak` with no live counterpart | delete orphans |
| `.opencode/audit` (2 MB, JSONL) | live audit trail, no rotation policy | keep; add rotation |
| `dead_letter.json.bak`, `inbox.json.bak`, `pending_approvals.json.bak` | atomic-write snapshots by design (file_store.py:54) | keep |
| `.opencode/inbox.json` (64 tasks) | live but stalled — daemon dead since 9/11; task `6f17c70c…` missing timestamps | restart daemon/drain; backfill |
| `logs/executor-daemon.pid` (dead pid) / `logs/executor-daemon.log` (5.3 MB, silent since 9/11) | stale | delete pid; rotate log |
| `backs-ups` stale (>30 days, exceeds keep-14 policy) | stale | archive; resume scheduled backup |
| `.opencode/opencode.json` (109 B, wires graphify plugin) | untracked while plugin IS tracked → fresh clone loses wiring | track or document recreation |
| `.playwright-cli/` + `screenshots/` | **git-hygiene gap** — untracked, NOT ignored (5.8 MB PNGs + snapshots) | add to .gitignore + delete |
| `.opencode/node_modules/` (52 MB) | ignored, regenerable | optional delete |

### 3.4 Frontend dead cluster (src/, ~25 files)

Unreachable from live routes → archive/delete: `src/pages/{CapabilitiesPage,DiagnosticPage,EngagementPage,EvidencePage,CaseStudyDetailPage,OfferingsPage}.tsx`; `src/components/{CorporateLanding,TemplatesArtifacts,ProofShowcase,NationalAiStrategySubmission,SovereignConstellation,InteractiveOperatingModel,EcosystemCarousel,MethodFramework,SynergyMatrix,OfferingDetailCard,SadcGovernanceFramework}.tsx`; `src/components/{OperatingModelSection,DiagnosticSection,EngagementSection,CoreOfferingsSection}.tsx`; legacy dashboard components `{MissionControl,CommandCenter,OrgChart,TaskKanban,FinanceCosts,KPIAnalytics,AgentRoster,TaskModal,ApprovalsEscalations,Header,Navigation,ScrollToTop}.tsx`. Purchased by orphaned images: `src/assets/images/{basalt_hex_relief…, celestial_arch_portal…, modular_architectural_relief…}` + 5 sadc/pharos images referenced only by dead `CorporateLanding.tsx`/`ProofShowcase.tsx`. `src/components/SPLIT_PLAN.md` → move to docs.

`src/components/SadcGovernanceFramework.tsx`: graphify syntax flag is a **false positive** (tsc passes; `&` in JSX text) — keep.

---

## 4. C. STALE CODE

### 4.1 Dead Python modules (`src/ai_company`)

| Module | Status | Action |
|---|---|---|
| `cli/init.py` | dead CLI module — NOT in `_LAZY_SUB_APPS` (main.py:31-93), 0 importers | register or archive |
| `data/etl/` (whole subpackage) | stale — 0 external importers; pyproject coverage comment calls it a "v0.5.1 stub module" (pyproject.toml:177-179) | archive or wire-in |
| `data/etl/orchestration/scheduler.py` (+ `pipelines/governance.py` sole consumer) | orphan | delete |
| `data/etl/quality/alerts.py`, `quality/profiler.py`, `extractors/file_extractor.py` | orphan | delete |
| `dashboard/kpis/company_kpis.py` | orphan (0 imports, not in ALL_COLLECTORS) | delete |
| `dashboard/kpis/operations.py` | test-only production dead (`test_kpi_collectors.py:659`) | wire-in or delete |
| `dashboard/kpis/base.py` / `company_kpis.py:27` | duplicate `_load_json`/`_load_yaml` reinventing `FileStore.read_json/yaml` | consolidate |
| ruff F401/F841 | **0 violations** in src/ | n/a |
| pytest collection | **0 errors** (2368/2435, 67 deselected) | n/a |
| llm providers | all 9 models.yaml providers have routing code, 0 orphans | keep |

### 4.2 Stale tests / duplicated test files

| Finding | Evidence | Action |
|---|---|---|
| `tests/cli/test_cli_commands.py` vs `tests/unit/test_cli_commands.py` | duplicate (both collected) | delete one |
| `tests/e2e/test_dashboard_scroll.py` vs `tests/unit/test_dashboard_scroll.py` | duplicate name, divergent behavior (e2e deselected) | delete one |
| `tests/integration|orchestrator|unit/test_approval_escalation.py` | same test ×3 | keep one |
| `Makefile:19,22` → `tests/benchmarks/` | path doesn't exist (canonical `tests/performance/`) | fix |
| `Makefile:16` coverage path | `--cov=ai_company` vs CI `--cov=src/ai_company --cov-fail-under=72` | reconcile |
| 9 `__pycache__` dirs inside tracked `tests/` tree | clutter (~4.9 MB), ignored | clean locally |
| `.env.example` missing `GEMINI_API_KEY`; `.env.staging.example:1` mojibake encoding | — | fix |

### 4.3 Stale frontend/build

| Finding | Action |
|---|---|
| `bun.lock` + `package-lock.json` dual lockfiles (npm used by Vercel) | delete `bun.lock` |
| `website/` static vanilla site — no build, ship-nowhere, only benchmark docs reference it | archive or wire a workflow/job |
| `ls-frontend-design` claims "Next.js 16 (website/)" and "Astro (lightspeed-main-site/)" — both wrong | fix SKILL.md |
| `src/brand/brand-tokens.css` unwired duplicate of `brand/tokens/brand-tokens.css` (different content) | merge + wire or delete |
| brand copy-chain (5 trees): `Branding landing page/` → `brand/` → `static/brand/` → `public/brand/` → `src/brand/` | promote `brand/` as source; symlink/copy static/brand; keep public favicon |

---

## 5. D. REDUNDANT DOCS & SKILLS

### 5.1 Docs

- **CRITICAL index bug:** `docs/sop-deployment-v2.md` + `docs/sop-incident-response-v2.md` are `status: active` but **zero inbound refs** — every live link (STATUS.md:126-127, README.md:422-423) points at superseded v1. Active SOPs unreachable.
- **Redundant duo:** `docs/CEO_DASHBOARD_USER_GUIDE.md` (212 KB monolith, 0 inbound, 3 dangling links) vs `docs/ceo-dashboard-user-guide/` (8 chapters). Keep chapters, archive monolith.
- **Docs infra gap:** no `docs/README.md`; 17 of 19 docs subdirs unindexed → ~63 orphan docs (listed in full by technical-documentation-lead subagent; clusters: historical milestones PHASE-1/2/3, SPRINT-*, PROJECT-STATUS-ASSESSMENT; dashboard-design cluster CEO_DASHBOARD_DATA_MAPPING, DASHBOARD_DATA_DICTIONARY, DESIGN-DASHBOARD-FEATURES; ADRs 001-005,013-015; research/ notes; wayfinder tickets; Pharos draft articles).
- `docs/AGENT-REGISTRY-TABLE.md.bak` — byte-identical dup → delete.
- `docs/diagrams.md` + `docs/diagrams-4-5-6.md` — split series, both unlinked → merge.
- Root audit/QA cluster (BRAND_AUDIT_REPORT, QA_ANALYSIS, UX_VALIDATION_REPORT, etc.) → archive to docs/archive/.
- `ai_development_constitution/ai_development_supreme_propmt.md` — filename typo ("propmt"), 0 refs to typo'd path → rename.
- Loose `docs/*.txt` (2) → relocate.

### 5.2 Skills (.agents/skills + .opencode/skills, 99 dirs)

| Finding | Verdict |
|---|---|
| **pharos-* (8)** mirror roster cards nearly verbatim, lack name/description frontmatter, and are the documented invalid-`task()` failure mode | delete (cards own missions) or fully rework |
| **ponytail family (6)** — audit≈review, help 0-ref, debt/gain subcommands | consolidate to 2 (`ponytail`, merged review) |
| **bug-hunter vs diagnosing-bugs** — near-duplicate symptom→root-cause loops | merge into bug-hunter |
| **ask-matt vs using-agent-skills** — both routers; ask-matt 0 refs, DI-model-invocation disabled | delete ask-matt |
| **no-ai-slop** — byte-identical SKILL.md in `.agents/skills` + `.opencode/skills` | keep `.opencode` copy only |
| **.agents/skills/docs/** (97 files) — inert vendored skills-catalog docs blob, not a skill (manifest-managed) | move out of skills tree |
| **broken-ref batch (9 skills)** — dangling `references/*.md`, `scripts/lint-*.mjs`, shared `definition-of-done.md` (ref'd by 4 skills, exists nowhere); root `security-checklist.md`/`accessibility-checklist.md` exist but at wrong path | create shared `references/` or retarget |
| `skill-check` skill — no validator binary exists (`uv run skill-check` not runnable) | keep as manual checklist, fix description |
| k-dense family (22) — clean, manifest-managed | vendor-properly (version pins) |
| ls-* stack — chain verified except `ls-documentation-engineering` (no design-system/QA refs) and `ls-frontend-design` (framework drift) | fix 2 |
| `ls-social-media-design` cites pharos-* skill outputs | retarget to roster card names |
| manifest hygiene — `.antigravity-install-manifest.json` name-only, 58 entries; 41 repo-native skills unrecorded; no lockfile | add version metadata |
| archify — skill+package interdependency (`resolve_bin`), absent from manifest | keep; add guard test |

---

## 6. Git hygiene & security

- **No secrets tracked.** `.env` (24 live keys incl. OPENCODE/GEMINI/DASHBOARD keys) is untracked+ignored; `.env.example` + `.env.staging.example` are placeholders only. Rotation still recommended on the 90-day cadence.
- `.playwright-cli/` and `screenshots/` — untracked & **not ignored** (highest accidental-commit risk).
- Root loose files not covered by ignore: generic `*.log`, `*.txt`, `deploy/` (untracked but referenced by docs/OCI-FREE-TIER-DEPLOYMENT.md — decide: commit `deploy/oci/` or gitignore), `"Branding landing page"`.
- `DASHBOARD_API_KEY` legacy alias still supported and exercised (rbac.py:70, tests) — documented depreciation optional.
- `data/` fully gitignored but `data/catalog/schemas/*.json` + `quality_rules.yaml` are READ at runtime (`data/etl/quality/validator.py:47,67`) → fresh clone missing → untrack catalog whitelist.

---

## 7. Consolidated severity register (top findings)

C = critical, M = major, m = minor, i = info.

| Sev | Category | Path | Action |
|---|---|---|---|
| C | misalignment | registry/parser.py `_parse_kpis` schema mismatch | fix |
| C | misalignment | registry parser drops `guardrails` | fix |
| C | git-fresh-clone | orchestrator/{escalation,scheduler}.yaml ignored but required | git add -f |
| C | broken-file | src/ai_company/dashboard/static/js/command-bar.js (unclosed `});`) | fix |
| C | ci-dead | .github/workflows/site.yml → phantom lightspeed-main-site/ | fix/repoint/delete |
| M | ci-gap | agent-registry validation never runs in CI | wire `validate agents` |
| M | ci-gap | root JS lockfiles never installed by CI | wire frontend job |
| M | duplicate | `config/departments` vs `company/departments` (19/20, id styles) | reconcile |
| M | duplicate | `company/config/*` vs `config/company/*` | merge |
| M | dead-config | `config/company/scheduler.yaml` (dead twin) | archive |
| M | duplicate | `bun.lock` + `package-lock.json` | delete bun.lock |
| M | duplicate | tests/cli+unit CLI tests, e2e+unit scroll, ×3 approval_escalation | dedupe |
| M | duplicate | `docs/CEO_DASHBOARD_USER_GUIDE.md` vs chapters | archive monolith |
| M | index-bug | SOP v2 active but all links → v1 | repoint links |
| M | orphan | 63 docs unreferenced (no docs index) | add docs/README + archive |
| M | orphan | `scientific-agent-skills/` embedded empty clone | delete |
| M | orphan | root Branding landing page/ (52 dup assets) | archive |
| M | orphan | 25 dead frontend pages/components + orphan images | delete/archive |
| M | orphan | `prompts/`, `memory-index.yaml`, root `research/` | archive |
| M | redundant | 144 `.bak` agent cards + 19 suspended_states `.bak` | delete |
| M | stale | `data/etl/` subsystem (0 external importers) | archive |
| M | dead-module | cli/init.py unregistered; kpis/company_kpis.py; operations.py | wire or delete |
| M | drift | "12 Jinja2 templates"/ghost template claims (8 docs + registry entry) | fix + regen card |
| M | redundant | pharos-* skills ×8 mirror cards | delete |
| M | redundant | ponytail 6→2; ask-matt delete; no-ai-slop dual | consolidate |
| M | vendored | `.agents/skills/docs/` blob, not a skill | relocate |
| M | broken-ref | 9 skills dangling references/*.md + scripts | restore refs |
| M | drift | ls-frontend-design / ls-documentation-engineering / ls-social-media-design | fix SKILL.md |
| M | git-hygiene | `.playwright-cli/` + `screenshots/` not ignored | ignore + delete |
| M | runtime-data | orchestrator/approvals.yaml + dashboard NDJSON committed; data/catalog ignored | untrack/track |
| m | many | root junk files; docs/STATUS stale; dead configs routing.yaml/webhooks.yaml; logs/pid; backups stale; agent table .bak; constitution typo; env.example gap; Makefile paths; board config docs | per register |
| i | keep-verified | 144 card↔registry alignment, canonical 7 tools, pytest green, tsc green, ruff green, no tracked secrets, providers routed | no action |

---

## 8. HITL approval gate

This report is **read-only**. Recommended next step: a remediation session (separate from this audit) executing the Top-10 actions, each behind an explicit approval:

1. Approve blocker code fixes (registry parser ×2, command-bar.js, CI registry gate, fresh-clone configs).
2. Approve deletions (`.bak` litter, root temp/test files, dead frontend cluster, scientific-agent-skills, ask-matt + pharos-* skills).
3. Approve archives (Branding landing page, orphan docs + SOP v1s, CEO guide monolith, `data/etl/`, website/).
4. Approve consolidations (test dedupe, config trees, brand copy chain, skills merges).
5. Git hygiene (ignore + untrack runtime data; commit deploy/ or ignore; restore skills references).

Nothing in this report changed the repository. Deletions should be executed via `archive/` or git rm only after explicit sign-off per item.
