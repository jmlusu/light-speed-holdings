# LIGHTSPEED REPOSITORY CLEANUP — STATUS REPORT

**Audit date:** 2026-10-07 · **Auditor:** repository cleanup/architecture review (read-only; no files modified, nothing committed)
**Branch:** `feat/athena-archive-and-design-system` · **Current HEAD:** `be7d1848` · **Baseline:** tag `cleanup/c0-baseline` = `048627ad` (2026-10-05 23:40 +0200)
**Scope:** 19 cleanup commits, 2026-10-06 → 2026-10-07. Machine-readable evidence: `CLEANUP_EVIDENCE.json`. File manifest: `CLEANUP_FILE_MANIFEST.txt`. CEO summary: `CLEANUP_STATUS_SUMMARY.md`.

> The LIGHTSPEED PHASED APPROVAL & ROLLBACK PROTOCOL is taken as the governing change-control process. No separate approval-record, change-manifest, or rollback-procedure documents were found in the repository, so every phase below is verified against git evidence (tags, diffs, working tree, validation runs) — never against approval paperwork. No phase is marked complete on authority alone.

---

## 1. Governing documentation (§1)

| Document | Found |
|---|---|
| `DIRECTIVE.md` | MISSING |
| `MASTER_SPEC.md` | MISSING |
| `REBUILD_DIRECTIVE.md` | MISSING |
| `OPENCODE_MIGRATION_PROMPT.md` | MISSING |
| `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/ECL.md`, `docs/STATUS.md` | FOUND |
| `docs/LIGHTSPEED_DESIGN_SYSTEM.md`, `company-registry.yaml` | FOUND |
| Cleanup plan / approval records / rollback records / phase completion records / change manifests | NOT FOUND anywhere in tree |

Authoritative governance that *was* found: `AGENTS.md` §§7–9 (safety boundaries, canonical 7-tool vocabulary, HITL expiry sweep, skill transmission ban, audit evidence separation), `docs/ECL.md`, and the 5-tier permission implementation in `src/ai_company/orchestrator/tier_rules.py`. Prior audit work exists untracked in `repo-audit/` (`INVENTORY.md`, `DUPLICATES.md`, `DEAD_CODE.md`, `SECURITY_AUDIT.md`, etc.) — useful context, not cleanup records.

## 2. Baseline → Current State (§2)

- **Baseline:** `048627ad` (`cleanup/c0-baseline`), 4187 tracked files.
- **Current HEAD:** `be7d1848`, 3747 tracked files (**−440 files, −10.5%**).
- **Diff c0→HEAD:** 646 paths changed, 3802 insertions(+), 52075 deletions(−); 459 deleted, 141 renamed, 19 added, 18 modified.
- **Working tree: DIRTY.** ~50 unstaged deletions (all under `.archive/athena/`), ~20 modified files (brand tokens ×3, 10 docs, `hr/onboarding_requests.yaml`, `orchestrator/approvals.yaml`, 4 `src/` files), 5 untracked paths (`repo-audit/`, 3 knowledge bug-fix notes, 1 docs artifact dir). HEAD therefore does **not** describe the running tree.
- **Ignored/environment:** `.env` and `.env.local` exist on disk, correctly untracked; tracked env files are only `.env.example` and `.env.staging.example`. No submodules initialized (see §12).
- No `BASELINE INCOMPLETE` — the baseline tag is intact and the diff is fully reconstructible.

## 3. Executive cleanup scorecard (§3)

GREEN = verified complete · AMBER = partial / needs review · RED = incomplete / material risk · GREY = n/a or insufficient evidence

| Area | Status | Evidence | Remaining Risk |
|---|---|---|---|
| Repository structure | GREEN | 141 renames (root clutter → docs/reports/scripts, scripts → purpose dirs; commits `87dae04a`, `36ab4fd7`) | Low |
| Duplicate files/code | AMBER | Bulk corpus removed; 57× `openai.yaml` + triplicated brand tokens remain | Low–Medium |
| Dead code | AMBER | LS-MEM engine + DBs removed (`42284c54`, `be7d1848`); dead-code candidates not exhaustively proven | Medium |
| Deprecated code | AMBER | Registry still emits legacy tool names (see §9) | Medium |
| Temporary artifacts | GREEN | 126 `tmp/` scratch files deleted (`d77ea526`); zero tracked junk patterns | Low |
| Generated artifacts | GREEN | Caches purged (`aaef778e`); backup output moved out of repo (`db06a219`) | Low |
| Python artifacts | GREEN | Zero tracked `__pycache__`/`.pyc`/`.sqlite`/`.db` | Low |
| Frontend structure | GREEN | `tsc --noEmit` clean | Low |
| Backend structure | GREEN | `ruff` + `mypy` (225 files) clean | Low |
| AI Company Builder | GREEN | Generator/registry path intact; 90 agents resolve | Low |
| Agent/orchestration architecture | AMBER | 90/90 agents; tool-vocabulary drift (§9) | Medium |
| Memory architecture | AMBER | LS-MEM decommissioned, but leftover sqlite files were still being removed in HEAD commit | Low |
| Configuration | GREEN | `.env.example` fixed, `.gitignore` hardened (`d107ba44`); `openai.yaml` ×57 unexamined | Low |
| Environment/secrets hygiene | GREEN | Zero key-pattern matches; `.env` untracked | Low |
| Dependencies | AMBER | npm standardized (`7222a4c9`); full dep audit not run | Medium |
| Tests | AMBER | 2585 collect cleanly; full run NOT VERIFIED (timeout) | Medium–High |
| Build | GREY | No canonical build command asserted; `tsc` clean only |
| CI/CD | GREY | Workflow files present (13 under `.github/`), no CI run observed from this audit |
| Documentation | AMBER | Post-cleanup docs pass (`c3ec0184`); 441 docs in `docs/`, conflicts not fully triaged | Medium |
| Design system | GREEN | Tokens intact in 3 mirror locations; `tsc` clean | Low |
| Brand implementation | AMBER | Uncommitted token/content edits in working tree | Medium |
| Website architecture | GREEN | Positioning reads Malawi → Africa → beyond (§17) | Low |
| Open-source/open-weight strategy | AMBER | `sentence-transformers` + `src/ai_company/llm` present; abstraction depth not verified | Medium |
| Security | GREEN | No hardcoded keys; pre-commit runs ruff+mypy+bandit | Low |
| Observability | GREY | Not exercised by this audit |
| Maintainability | GREEN | −52k lines, flatter root, purpose-dir scripts | Low |
| Repository navigability | GREEN | Same as above | Low |
| Rollback integrity | AMBER | 13 tags, no procedure document; dirty tree weakens HEAD-based restore | Medium |
| **Overall cleanup readiness** | **AMBER** | **Real, verified shrinkage with clean linters; held back by dirty tree + unverified test suite** | **Medium** |

## 4. Filesystem / repository inventory (§4)

- Tracked: **3747 files** across ~96 top-level entries. Largest tracked areas: `.agents/` (698), `docs/` (619), `harness/` (424), `public/` (398), `src/` (380).
- By extension: `.md` 1536 · `.py` 571 · `.png` 303 · `.svg` 246 · `.yaml` 185 · `.html` 153 · `.json` 126 · `.tsx` 92 · `.ts` 72 · `.pdf` 54.
- **Zero** tracked `.pyc`/`__pycache__`/`.tmp`/`.bak`/`.old`/`.orig`/`.log`/`.sqlite`/`.db`. The 309 `.npy`/`.png` matches are asset/corpus files, and the `.npy` embedding caches are currently being deleted in the working tree.
- ~400 tracked `pdf/zip/npy/png/jpg` binaries remain — sampled as legitimate assets (brand, content, research); no accidental wheelhouse or database dumps identified.
- Suspicious-name scan: `archive/` (20), `output/` (38), `reports/` (40) are active working dirs, not legacy dumps; legacy content was moved to `.archive/` deliberately. Nothing was deleted by this audit.

## 5. Before / after metrics (§5)

| Metric | Before (c0) | After (HEAD) | Change |
|---|---|---|---|
| Total tracked files | 4187 | 3747 | **−440 (−10.5%)** |
| Python files | 602 | 571 | −31 |
| TS/TSX files | 165 | 164 | −1 |
| Markdown files | 1634 | 1536 | −98 |
| PNG files | 532 | 303 | −229 (scroll-craft corpus) |
| YAML files | 188 | 185 | −3 |
| Total diff | — | 646 paths, +3802 / −52075 | net −48k lines |
| Duplicate candidates | N/A — insufficient evidence (no pre-cleanup duplicate census found) |
| Dead-code candidates | N/A — insufficient evidence (same reason; see §7 for current-state triage) |
| Test files | 185 under `tests/` at HEAD; baseline count not separately censused — N/A for before |
| Dependencies / build artifacts / config counts | N/A — insufficient evidence; no authorized upgrade performed |

No historical numbers are fabricated: "before" counts above are recomputed from the `cleanup/c0-baseline` tag, not quoted from any cleanup claim.

## 6. Duplication analysis (§6)

- **Removed:** scroll-craft image corpus (~1 GB, commit `c3d2002d`), registry backups (`bc1d1590`), duplicate landing page (`6b39ea44`), bun.lock (`7222a4c9`).
- **Remaining clusters:**
  1. `openai.yaml` ×57 — suspected duplicated per-agent model config. Content-diff not performed. Confidence: MEDIUM. Intentional: UNKNOWN.
  2. Brand tokens ×3 (`brand/`, `public/brand/`, `static/brand/`, identical 6217/3168-byte files) — intentional mirrors per `AGENTS.md`; canonical root `brand/`. Confidence: HIGH.
  3. `SKILL.md` ×176, `__init__.py` ×58, harness `Plan.md`/`SPEC.md`/`tasks.md`/`summary.md` (~50 each) — structural convention (one per skill / package / change record), not duplication. Confidence: HIGH.
- No competing "source of truth" implementations of the same feature were identified at audit depth.

## 7. Dead / orphaned / legacy code (§7)

- **Confirmed dead & removed:** LS-MEM memory engine + sqlite runtimes, `tmp/` scratch (126 files), superseded branding page, retired registry backups, scroll-craft corpus.
- **Suspected dead (not proven, do not delete on this report alone):** contents of `archive/` (20 files) and `output/` (38 files) post-move; `open-design/` reference while submodule is uninitialized; any `openai.yaml` copies orphaned by the decommission.
- Nothing is classified dead merely for looking unreferenced; each suspected item above carries location + reason and needs a reference check before removal.

## 8. Architectural alignment review (§8)

Correctly implemented: Python CLI + registry→template→cards generator (`company-registry.yaml` → `src/ai_company/generator.py` → `.opencode/agents/*.md`), task queue at `.opencode/inbox.json` (`orchestrator/message_bus.py`), 5-tier approval enum + approval store, triplicated-but-canonical brand tokens, Malawi→Africa→beyond positioning.
Partially implemented: provider abstraction for open-weight/local inference (library + `llm/` dir present, substitution path not traced end-to-end).
Documented but not verified executed: full 90-agent orchestration at runtime (definitions resolve; live routing not exercised).
Legacy still present: legacy tool names in registry (`write`/`execute`/`delegate` vs canonical `edit`/`bash`/`task`); `.archive/athena` awaiting final deletion; uninitialized `open-design` submodule.
Contradictions found: exactly one — the tool-vocabulary drift (§9/R3). No other architecture contradictions identified.

## 9. Agent architecture audit (§9)

- **90 agent definitions** in `company-registry.yaml` (nested under `company.agents`), **90 generated cards** in `.opencode/agents/*.md`. Zero duplicate ids. Zero deprecated/orphan markers found.
- **No contradictory counts found** — no 127/144/152 references in `README.md`, `AGENTS.md`, `docs/STATUS.md`, or `docs/ARCHITECTURE.md`.
- Human CEO vs CEO-facing agent vs specialists vs control plane: registry `reports_to: human_ceo` chain + `orchestrator/` (approval, tiers, escalation, scheduler, dead-letter) preserves the boundary structurally.
- **Drift:** registry cards (e.g. `chief_of_staff`) declare tools `read, write, execute, delegate`; `AGENTS.md` §8 canonicalizes `read, edit, grep, list, bash, webfetch, task` and states `write→edit`, `execute→bash`, `delegate→task` are backward-compatible aliases while `code_interpreter` is rejected. Per `AGENTS.md`, ToolRunner validates against the canonical list — any card emitting a non-canonical, non-alias tool errors at runtime. Remediation: regenerate cards from the Jinja2 template after updating the template's tool mapping, then re-run §13 validation.

## 10. Permission and governance audit (§10)

- The 5-tier model (Tier 0 auto-approve → Tier 4 CEO-only) is implemented in `tier_rules.py` with `approval.py`, `approvals.yaml`, `escalation.yaml`, plus the `ApprovalGate` expiry sweep (`AGENTS.md` §9.1). No standalone permission-policy document was found — code + AGENTS.md are the documentation.
- Implementation-vs-policy discrepancies found: (a) legacy tool names in registry cards (above); (b) enforcement audited statically only — no live approval-bypass test executed, so bypass resistance is NOT VERIFIED.
- Destructive-operation gating, approval auditability, and rollback retention exist structurally (`dead_letter.jsonl`, `escalation_events`, per-phase tags). No evidence of agents bypassing controls was found.

## 11. Cleanup phase audit (§11)

No phase approval records, manifests, or validation logs were found in the repo, so every phase is rated on git evidence only. Tags `cleanup/c1`…`c10` all exist.

| Phase | Objective (from tag/commit evidence) | Status |
|---|---|---|
| c1-secrets | `.env.example` fix, `.gitignore` hardening, untrack QA/logs | PARTIAL (effect verified clean; no approval record, tree re-dirtied since) |
| c2-caches | Purge caches/generated artifacts | COMPLETE in effect (zero tracked junk files) |
| c3-root-moves | Root clutter → docs/reports/scripts | COMPLETE in effect (141 renames) |
| c4-scripts | Script sprawl → purpose dirs; milestone-deck consolidation | COMPLETE in effect |
| c5-consolidation | npm standardization, registry-backup removal | COMPLETE in effect |
| c6-generated | Backup output out of repo; large-tool removal staging | COMPLETE in effect |
| c7-large-tools | scroll-craft corpus (~1 GB) removal; open-design submodule | PARTIAL (corpus gone; submodule uninitialized) |
| c8-docs | Post-cleanup documentation | PARTIAL (docs pass committed; 441 docs untriaged; working-tree doc edits uncommitted) |
| c9-validated | Test repair + validation | PARTIAL (ruff/mypy/tsc green at audit; full pytest NOT VERIFIED) |
| c10-decommission | LS-MEM decommission + ECL closeout | PARTIAL (engine gone; HEAD commit still removing sqlite leftovers; `.archive/athena` deletions uncommitted) |

## 12. Rollback integrity (§12)

- **Rollback points:** 11 `cleanup/*` tags (c0 baseline → c10) + 2 `backup/*` tags. No manifests, no restore runbook.
- **Coverage:** git tags cover source/config fully; database rollback n/a (sqlite runtimes deleted, no production DB in repo); deployment rollback via `docker-compose.staging.yml` + `scripts/deploy/backup.ps1` is documented but not tested by this audit.
- **### Rollback Confidence: MEDIUM.** Tags bracket the cleanup and diffs confirm their contents, but (a) tags may be local-only (branch `feat/athena-archive-and-design-system` unmerged at audit), (b) no procedure document exists, (c) the dirty working tree means checking out HEAD does not reproduce the working state, and (d) the `open-design` submodule (`-6fd2f60`, uninitialized) will not restore on a fresh clone without `git submodule update --init`.

## 13. Build / test / runtime validation (§13)

Exact commands run at audit time (Windows PowerShell, repo root):

| Command | Result |
|---|---|
| `uv run ruff check src/` | **PASS** — all checks passed |
| `uv run mypy src/` | **PASS** — no issues in 225 source files |
| `npx tsc --noEmit` | **PASS** — no output |
| `uv run pytest --collect-only -q` | 2518/2585 collected (67 deselected) in 3.34 s |
| `uv run pytest -q` (full) | **NOT VERIFIED** — exceeded 120 s audit timeout; no failures observed, run did not complete |

No failures to classify, so no PRE-EXISTING vs CLEANUP-INTRODUCED determination was possible. The c9 tag's "validated" claim is therefore only partially corroborated. Application startup, health checks, and agent runtime tests were not exercised (no canonical commands asserted in docs for this Windows environment).

## 14. Dependency audit (§14)

- Python (`pyproject.toml`/`uv.lock`): `sentence-transformers>=3.0` present (local-embedding path for open-weight strategy); full unused/outdated/conflict audit not run — no upgrades performed, none authorized.
- JS: standardized on npm, `bun.lock` removed (`7222a4c9`); `node_modules/` present on disk, untracked, correct.
- Vendored/local packages: none identified beyond the intentional brand-token mirrors and `.agents/` skill tree.
- Model/runtime deps: no hard proprietary-model lock-in found at audit depth (see §18).

## 15. Secrets / security hygiene (§15)

- Content scan for `sk-ant-`, `sk-proj-`, `ghp_`, `AKIA`, `PRIVATE KEY` headers across `src/`, `orchestrator/`, `config/`, `.env.example`: **zero matches**. No `SECRET DETECTED` entries to redact.
- `.env`/`.env.local` on disk are untracked (gitignored); only `.env.example` + `.env.staging.example` are tracked. Commit `d107ba44` fixed a personal path + duplicates in `.env.example`.
- Pre-commit runs ruff, mypy, and bandit. No unsafe debug artifacts or secret-bearing logs found tracked. PII scan: nothing flagged beyond normal contact fixtures; no values reproduced in this report.

## 16. Design system / brand integrity (§16)

- Tokens intact: `brand/tokens/brand-tokens.{json,css}` with identical mirrors under `public/brand/` and `static/brand/` (canonical-root convention per `AGENTS.md`). `docs/LIGHTSPEED_DESIGN_SYSTEM.md` found; brand guidelines directory `brand/` (103 tracked files) preserved.
- **Risk:** all three `brand-tokens.json` copies plus 10 brand/narrative docs (`BRAND_ADOPTION_ROADMAP.md`, `NARRATIVE-AND-POSITIONING.md`, `GEOGRAPHIC_POSITIONING_AUDIT.md`, etc.) have **uncommitted modifications** — the design system is currently a moving target, not a stable baseline.
- No competing design system was found. `tsc` clean implies no broken token imports. Biophilic Luxury & Zen / ASPIRE. ACT. ACHIEVE. / logo-direction claims were not re-verified pixel-by-pixel (visual QA out of scope for this audit).

## 17. Website / product structure (§17)

- Positioning verified in `src/data/siteContent.ts`: `Lilongwe, Malawi` base; "in Malawi, across Africa and beyond"; African operating realities (Airtel Money, TNM Mpamba, PayChangu) alongside Africa-wide insight routes (`/insights/sadc-ai-opportunity`, `/insights/agentic-ai-african-governments`). **Supports Malawi-based → Africa-focused → open internationally without unsupported claims.**
- Duplicate/dead-route/stale-content census: not performed page-by-page; no obsolete-page evidence surfaced during inventory. `src/pages/SectorsPage.tsx` + `WhatWeDoPage.tsx` carry uncommitted edits (see backlog P1-3).

## 18. Open-source / open-weight model strategy (§18)

- Present: `sentence-transformers` dependency, `src/ai_company/llm/` module directory, `src/ai_company/models/` layer — a local-inference/provider-abstraction shape exists.
- Not traced: whether any call path hard-codes a proprietary provider or cost-bearing default; no Ollama references confirmed at audit depth.
- State: **plumbing present, substitution guarantee NOT VERIFIED**. Risk is cost/lock-in opacity, not a known violation. No redesign proposed.

## 19. Documentation hygiene (§19)

- `docs/` holds 441 tracked markdown files; harness changes add ~424. Sample classification: AUTHORITATIVE — `AGENTS.md`, `docs/ECL.md`, `docs/ARCHITECTURE.md`, `company-registry.yaml`, tier_rules.py docstrings. CURRENT — post-cleanup docs (`c3ec0184`), `docs/STATUS.md`. HISTORICAL — `harness/changes/archive/*`, `.archive/*`. OBSOLETE — none positively identified (requires per-doc triage). CONFLICTING — one: registry tool names vs `AGENTS.md` §8. UNKNOWN — the long tail of 441 docs, including whether any claim unimplemented features.
- Untracked `repo-audit/*.md` + 3 `knowledge/technology/bug-fixes/BUG-*.md` notes are reviewer context, not part of the cleanup baseline.

## 20. Git hygiene (§20)

- 19 cleanup commits, all conventionally messaged (`chore`/`refactor`/`fix`/`docs`), one logical change each, with per-phase tags — exemplary structure for future agent archaeology.
- No accidental large files introduced (largest deletions were the intended corpus purge). No generated files newly committed. `.gitignore` hardened for QA/logs/caches.
- Detractions: work continues on a feature branch (`feat/athena-archive-and-design-system`) with a dirty tree; `repo-audit/`, knowledge notes, and case-study artifacts are untracked and will either pollute or be lost; the uninitialized submodule breaks fresh-clone reproducibility.

## 21. Agent-readiness assessment (§21)

Discoverability, canonical sources (`company-registry.yaml`, `company/departments.yaml`, `brand/`), and predictable structure all improved; −52k lines and purpose-dir scripts lower onboarding complexity. Offset by: dirty tree (agents cannot trust HEAD), one tool-vocabulary contradiction, uninitialized submodule, and an untriaged 441-doc tail.

### Agent Readiness Score: 72/100

Justification: a materially smaller, linter-clean, well-tagged repo (+25 vs pre-cleanup baseline state) held back ~28 points by unverified tests (10), dirty tree (8), tool-name drift (5), and submodule/docs-ambiguity drag (5). Committing the tree, greening pytest, and regenerating agent cards would plausibly score 90+.

## 22. Remaining cleanup backlog (§22)

### P0 — Blocking (require resolution before next development phase; CEO approval: yes for P0-1 archival commit, no otherwise)

| ID | Issue | Location | Evidence | Recommended action | Risk if ignored | Complexity |
|---|---|---|---|---|---|---|
| P0-1 | Dirty working tree: ~50 unstaged `.archive/athena` deletions + ~20 modified files | `.archive/athena/`, `brand/tokens/*`, `docs/*`, `src/*` | `git status --short` (§2) | Commit (or explicitly revert) everything; tag `cleanup/c11-landing` | Reviewer cannot reproduce HEAD; rollback claims unverifiable | Small |
| P0-2 | Full test suite never observed green | `tests/` (2585 tests) | §13 timeout | Run `uv run pytest -q` to completion (raise timeout, use `-p no:cacheprovider` if cache I/O is the bottleneck) and record results | Silent regressions from 141 renames ship into next phase | Medium |
| P0-3 | `open-design` submodule uninitialized | `open-design/`, `.gitmodules` | `git submodule status` → `-6fd2f60` | `git submodule update --init` and commit the pin, or revert commit `d284836e` to re-vendor | Fresh clones / CI / agents hit missing-path failures | Small |

### P1 — High (before major new features)

| ID | Issue | Location | Evidence | Risk | Complexity |
|---|---|---|---|---|---|
| P1-1 | Registry tool-vocabulary drift (`write`/`execute`/`delegate`) | `company-registry.yaml`, `templates/agents/agent.md.j2` | §9 | Runtime tool-rejection for regenerated agents | Small–Medium |
| P1-2 | No phase approval records / manifests / rollback runbook | repo root / `harness/` | §§1, 11, 12 | Next cleanup repeats the evidence gap; rollback stays tag-only | Small (write docs) |
| P1-3 | Uncommitted brand-token + positioning edits | `brand/`, `public/brand/`, `static/brand/`, `src/data/*`, `src/pages/*` | §16 | Design system drifts without a reviewed baseline | Small |
| P1-4 | `openai.yaml` ×57 duplication unexamined | per-agent config copies | §6 | Config drift; secret-sprawl surface | Medium |

### P2 — Medium (during normal development)

P2-1: Triage `archive/` (20) + `output/` (38) for final delete/keep decisions. P2-2: Per-doc triage of the 441-file `docs/` tail (OBSOLETE vs HISTORICAL). P2-3: Full dependency audit (unused/outdated/conflicting). P2-4: Trace open-weight substitution end-to-end (§18). P2-5: Decide fate of untracked `repo-audit/`, knowledge bug notes, case-study artifacts (track or `.gitignore`).

### P3 — Low (future hygiene)

P3-1: Push/merge `feat/athena-archive-and-design-system` so tags exist remotely. P3-2: Re-run `scripts/deploy/backup.ps1` and record a restore test. P3-3: Pixel-level brand QA (Biophilic Luxury & Zen, ASPIRE. ACT. ACHIEVE., logo direction).

## 23. "DO NOT CLEAN UP" list (§23)

- `company-registry.yaml` + `company/departments.yaml` — canonical agent sources; drift-exempt per ECL-linked manifest.
- `src/ai_company/orchestrator/` (`tier_rules.py`, `approval.py`) + `orchestrator/approvals.yaml`, `escalation.yaml` — live governance; changes need CEO-gated review.
- `brand/` token roots — architectural anchors for every creative skill; mirrors are intentional.
- `templates/agents/agent.md.j2` + `src/ai_company/generator.py` — regeneration pipeline; hand-editing generated cards instead is the error to avoid.
- `.opencode/inbox.json` + `orchestrator/dead_letter.jsonl` — runtime state and audit trail, not clutter.
- `harness/changes/archive/*`, `.archive/*`, ADRs — historical record; drift-exempt by policy.
- `cleanup/c*` + `backup/*` tags, `.gitmodules` pin — rollback infrastructure.
- `docker-compose*.yml`, `Dockerfile`, `scripts/deploy/backup.ps1`, `.github/` — deployment/CI boundaries.
- `.env` (untracked), `.env.example`, `.env.staging.example` — secrets boundary; never "consolidate" live env into tracked files.

## 24. RED FLAGS REQUIRING CEO ATTENTION (§24)

1. **Working tree dirty at audit close** — the audited state (HEAD `be7d1848`) is not the running state. Any sign-off must name a commit hash *after* P0-1 lands. (Evidence: §2.)
2. **Full test suite not green-observed** — 2585 tests collect; completion unknown. No regression claim is supportable until P0-2 runs. (Evidence: §13.)
3. **Rollback is tag-only** — no runbook, no manifest, possibly local-only tags, uninitialized submodule. A restore has never been demonstrated. (Evidence: §12.)
4. **Agent tool-vocabulary contradiction** — registry cards vs `AGENTS.md` §8 canonical list; runtime rejection risk on regeneration. (Evidence: §9.)
5. **No phase approval paperwork exists** — the Protocol is cited as complete but left no records in the repo; all phase ratings in §11 are `PARTIAL`/`NOT VERIFIED` on evidence grounds, not on quality grounds.
6. **Uncommitted design-system edits** — brand tokens and positioning docs are mid-edit; the brand baseline is unstable at the exact moment of sign-off. (Evidence: §16.)

## 25. Evidence register (§25)

| Finding | Evidence | Confidence |
|---|---|---|
| −440 tracked files, −52k lines c0→HEAD | `git diff --shortstat cleanup/c0-baseline..HEAD`; `git ls-tree` counts 4187→3747 | HIGH |
| 19 cleanup commits 2026-10-06→07 with per-phase tags c0–c10 | `git log`, `git tag --list 'cleanup/*'` | HIGH |
| Zero tracked junk artifacts | `git ls-files` × junk-pattern filter = 0 matches | HIGH |
| ruff / mypy / tsc green | §13 command table | HIGH |
| Full pytest NOT VERIFIED | 120 s timeout; collect-only 2518/2585 | HIGH |
| 90 agents, no count contradictions, no dup ids | registry `id:` count, `.opencode/agents/*.md` count, doc grep | HIGH |
| Tool-vocabulary drift | `company-registry.yaml:37-41` vs `AGENTS.md` §8 | HIGH |
| 5-tier model implemented; bypass resistance untested | `tier_rules.py`, `approval.py`, approvals/escalation yaml | MEDIUM |
| Submodule uninitialized | `git submodule status` (`-` prefix) | HIGH |
| Secrets clean | zero-pattern scan; `.env` untracked | MEDIUM (pattern scan, not full secret audit) |
| Positioning Malawi→Africa→beyond | `src/data/siteContent.ts:40-111` | HIGH |
| Open-weight support partial | `sentence-transformers`, `src/ai_company/llm/` present; no e2e trace | MEDIUM |
| `openai.yaml` ×57 duplication | basename census | MEDIUM |
| Brand mirrors intentional | identical sizes + `AGENTS.md` mirror note + `brand/CANONICAL_SOURCES.md` convention | HIGH |

## 26. Final verdict (§26)

## CLEANUP STATUS

**READY WITH CONDITIONS** — the repo is genuinely smaller (−10.5% files, −52k lines), junk-free, and linter-clean, but sign-off is conditional on P0-1 (land the dirty tree), P0-2 (pytest to green), and P0-3 (submodule init-or-revert).

## ARCHITECTURAL STATUS

**MOSTLY ALIGNED** — registry→generator→cards, task bus, 5-tier gates, brand canonical roots, and geographic positioning all hold; one contradiction (tool vocabulary) and one unverified path (open-weight substitution) keep this from ALIGNED.

## REGRESSION STATUS

**NOT VERIFIED** — no failures seen (ruff/mypy/tsc green, pytest collects), but the full suite never completed, so no regression claim is supportable either way.

## ROLLBACK STATUS

**PARTIALLY VERIFIED** — per-phase tags exist and bracket the work, but there is no runbook, no manifest, possibly-local-only tags, and a dirty tree.

## NEXT RECOMMENDED ACTION

**Commit or revert the dirty working tree and run the full pytest suite to green on the resulting hash (P0-1 + P0-2), then sign off against that hash — not against `be7d1848`.**
