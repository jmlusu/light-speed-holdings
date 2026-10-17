# Cleanup Plan

**Nothing in this plan has been executed.** Every stage is gated on explicit user
authorization. Stages are ordered so that each one is independently revertable and
independently reviewable.

---

## Ground rules

1. **No destructive action without authorization.** `DELETE` = `rm`. `ARCHIVE` = move
   to `docs/archive/` or outside the repo (recoverable). `KEEP` = untouched.
2. **Preserve the 83 pre-existing unstaged changes.** Do not `git add -A`. Stage by
   category (§31, Git hygiene).
3. **AGENTS.md §9.3 is absolute.** `orchestrator/escalation_events.jsonl` and
   `orchestrator/dead_letter.jsonl` are declared audit evidence — never write, move,
   rename, or delete them, or anything sharing their directory, without sign-off.
4. **Prefer reversible first.** For every `DELETE`, name the recovery path. If there is
   no recovery path, it is an `ARCHIVE`, not a `DELETE`.
5. Verify after each stage; do not batch stages into one commit.

---

## Stage 0 — Documentation (no authorization needed)

Already complete: this audit set.

| File | Purpose |
|---|---|
| `repo-audit/INVENTORY.md` | directory census + dispositions |
| `repo-audit/ARCHITECTURE_MAP.md` | current-state architecture |
| `repo-audit/DEPENDENCY_MAP.md` | dependencies + package-manager conflict |
| `repo-audit/DUPLICATES.md` | duplicate implementations |
| `repo-audit/DEAD_CODE.md` | dead-code candidates (§27 deletion gate noted) |
| `repo-audit/CONFIGURATION_AUDIT.md` | config sprawl + conflicts |
| `repo-audit/DOCUMENTATION_AUDIT.md` | docs + broken cross-references |
| `repo-audit/GENERATED_FILES.md` | generated/reproducible classification |
| `repo-audit/SECURITY_AUDIT.md` | findings + hardening |
| `repo-audit/NAMING_AUDIT.md` | naming defects + adopt convention |
| `repo-audit/CLEANUP_PLAN.md` | this file |
| `repo-audit/OPEN_QUESTIONS.md` | blocking decisions |
| `repo-audit/inventory.csv` | per-file table — deferred until decisions settle |

---

## Stage 1 — Secrets hardening — **ASK FIRST**

Highest severity, lowest risk of data loss, and it should land first.

- [ ] `git check-ignore` confirm; add `opencode.local.json` to `.gitignore` (S-1)
- [ ] Untrack + ignore 9 `qa-*.png`, 4 `qa-report*.json`, 6 `*.log` (S-2)
- [ ] Ignore `tmp/`, `lab/` (S-3)
- [ ] Add a secret-scan hook + CI gate (S-4)
- [ ] **Run `gitleaks detect --source . --redact` over full history** — if it fires,
      rotate the credential first, then rewrite history
- [ ] Replace the personal path in `.env.example` (S-6)
- [ ] Remove the duplicate `TURNSTILE_HOSTNAMES` key (S-7)

Recovery: untracking is `git rm --cached`; history rewrite is the only irreversible
step, hence the separate gate.

---

## Stage 2 — Zero-risk cache & artifact purge — **SAFE, no data loss**

Untracked or trivially regenerable. ~**350 MB**, no Git impact for most of it.

- [ ] `.mypy_cache/` (126 MB), `.ruff_cache/`, `.pytest_cache/`, `.hypothesis/`
- [ ] `.pytest_tmp/`, `.pytest_tmp_ci/`, `.pytest_tmp_ci2/`, `.pytest_tmp_commit/`,
      `.pytest_tmp_linkedin/` (~162 MB)
- [ ] `dist/` (6.9 MB)
- [ ] `tmp/`, `.playwright-cli/`, `.google notebook artifacts/`
- [ ] **Tracked but worthless:** `git_ls_files.txt`, `install.log`, `probe.log`,
      `runtask.log`, `vite.log`, `vite_start.log`, `vite-dev.log`
- [ ] Add all of the above to `.gitignore` so they cannot return

Recovery: every one regenerates on the next run.

---

## Stage 3 — Root moves — **ASK FIRST (mostly reversible)**

Reduces 107 tracked root files toward a sparse root (§18).

- [ ] 11 root `.py` scripts → `scripts/maintenance/` (reference sweep first)
- [ ] `start_vite.bat`, `start-dev.ps1`, `Clean-LSMEM.ps1` → `scripts/`
- [ ] 9 directives → `docs/directives/`
- [ ] 14 specs/audits → `docs/` or `reports/`
- [ ] 11 analysis reports → `reports/`
- [ ] `SECURITY.md`, `security-checklist.md`, `DEPLOYMENT.md` → `docs/`
- [ ] `test_fragment.tsx` → `src/` or delete
- [ ] Fix every path reference: `package.json`, `Makefile`,
      `.pre-commit-config.yaml`, `AGENTS.md`, CI

Recovery: `git mv` is history-preserving and trivially revertable.

---

## Stage 4 — Consolidated script tree — **ASK FIRST**

- [ ] Create `scripts/{dev,build,test,deploy,maintenance,research}/`
- [ ] Move the 49 flat scripts into purpose directories
- [ ] Add `scripts/health_check.py` (canonical health check, §26)
- [ ] Update all references

**Blocker:** the §27 `Before deleting` checks have not been completed —
`CHECK REFERENCES`, `CHECK DYNAMIC IMPORTS`, `CHECK BUILD`, `CHECK TESTS`,
`CHECK DOCUMENTATION`. Until all five pass, nothing in `scripts/` may be
*deleted* here — only moved.

---

## Stage 5 — Duplicate consolidation — **ASK FIRST**

| Target | Action | Gate |
|---|---|---|
| 3× brand token copies | Keep `brand/` as canonical; keep `public/brand/tokens/` + `static/brand/tokens/` as runtime mirrors **only if** a fetch path exists | verify runtime fetch first (Q1) |
| `scripts/generate-milestones-deck.{js,py}` | Pick one; delete the other | Q3 |
| `src/ai_company/memory/` vs `lsmem/` vs root `memory/` | Pick one implementation | Q4 |
| `company-registry.yaml` vs `agent-registry.json` vs `.opencode/agents/` | Pick one source; derive the rest | Q5 |
| `.github/` vs `.github.bak/` vs `.github.old/` vs `.github-security/` | Consolidate to `.github/` | verify what `.bak` holds |
| `.crush/`, `.mimocode/` | Merge into `.opencode/` or remove | Q6 |
| root `CLAUDE.md` vs `AGENTS.md` | **NO ACTION** - no competitor: root `CLAUDE.md` is absent (verified); `AGENTS.md` is the single root contract. `open-design/CLAUDE.md` is nested-project scope (D-5) | none - resolved |
| `src/` vs `src.bak/` (410 files) | `src.bak` is almost certainly delete | verify no unique content |

---

## Stage 6 — Generated-artifact policy — **ASK FIRST**

- [ ] Untrack 15 generated root artifacts (done in Stage 1)
- [ ] Delete the 2 `agent-registry.json.bak-*` files (D-4)
- [ ] Delete `company/models.yaml.executor-bak`
- [ ] Decide output locations: `results/`, `logs/`, `data/`, `reports/`
- [ ] Relocate runtime state out of root — **except** the two §9.3 evidence files
- [ ] Delete `backups/` (85 MB) + relocate backup output outside the repo; update
      `scripts/backup.ps1` and `AGENTS.md` §5

---

## Stage 7 — Large-tool handling — **ASK FIRST**

| Item | Size | Recommendation |
|---|---:|---|
| `models/` | 24.1 GB | **KEEP** — already gitignored, regenerable via `scripts/download_models.py`. Move out of the repo tree if disk pressure demands. |
| `open-design/` | 2.7 GB | Resolve the gitlink (§ Q2). Add `.gitmodules`, or untrack and fetch on demand into a gitignored path. |
| `.opencode/skills/scroll-craft/` | 692 MB | **DELETE** — `AGENTS.md` §9.2 says it was retired 2026-09-23. Requires confirmation that no one is still using it. |
| `scrollcraft/` | 32 MB | **DELETE** — duplicate feature copy |
| `docs/case-studies/…/artifacts/` | 79 MB | **DELETE** — 78.9 MB of duplicate QA screenshots |
| `lab/` | 216 MB | **ARCHIVE/DELETE** — generated visual-test artifacts (also needs gitignore, S-3) |

---

## Stage 8 — Documentation production — **NO GATE**

Documentation maintenance: refresh and consolidate. Safe — new/edited files only, no
deletions. Note that `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, and `docs/ECL.md`
**already exist**; the work is accuracy refresh, not creation.

- [ ] `README.md` → canonical entry: what the repo is, setup, canonical commands,
      validation, deployment (§36). Must **not** duplicate `docs/` content.
- [ ] `docs/ARCHITECTURE.md` → **refresh**, using `repo-audit/ARCHITECTURE_MAP.md` (§10/§36)
- [ ] `docs/DEVELOPMENT.md` → **refresh** (exists, 8.3 KB, 2026-10-01)
- [ ] `docs/ECL.md` → **refresh** (exists, 7.6 KB, 2026-09-16)
- [ ] `docs/DEPLOYMENT.md` → **create by consolidation**: neither `docs/DEPLOYMENT.md`
      nor root `DEPLOYMENT.md` exists. Merge `docs/DEPLOYMENT-GUIDE.md`,
      `docs/BRAND_DEPLOYMENT_GUIDE.md`, `docs/OCI-FREE-TIER-DEPLOYMENT.md`, and
      `RUNBOOK-LightspeedAI-Deployment-2026-10-03.md`
- [ ] `docs/SECURITY.md` — relocate + expand (§20, security sanitization)
- [ ] Verify `AGENTS.md` cross-references resolve and describe current reality
- [ ] `docs/REPOSITORY_HEALTH.md` — genuinely absent; create after Stages 1–7 report
      real numbers
- [ ] Name the canonical repo-wide health check (§26) — today only partial gates exist:
      `scripts/dev.ps1`, `scripts/validate-drift.ps1`, `scripts/validate-architecture.ps1`,
      `scripts/health_check_models.py` (models only), `tests/docs/test_doc_drift.py`

---

## Stage 9 — Post-cleanup validation

- [ ] `ruff check src/ && mypy src/ && pytest`
- [ ] `ai-company --help`
- [ ] generator round-trip (`AgentGenerator().generate_all()`) — verify no drift in
      `.opencode/agents/` or `company/*.yaml`
- [ ] fresh-clone smoke test — **should have caught the `open-design` gitlink**
- [ ] `pwsh scripts/lint-ecl.ps1`
- [ ] verify root tracked-file count dropped toward a sparse set
- [ ] confirm no tracked file exceeds a sane size limit

---

## Estimated impact

| Bucket | Size | Requires authorization |
|---|---:|---|
| Caches + tmp | ~290 MB | no |
| Generated root artifacts (tracked) | small | yes (untrack) |
| `scroll-craft` + `scrollcraft` | 724 MB | yes |
| `lab/` | 216 MB | yes |
| case-study artifacts | 79 MB | yes |
| `backups/` | 85 MB | yes |
| root runtime state | 329 MB | yes (excluding AGENTS.md §9.3 pair) |
| `open-design` | 2.7 GB | yes |
| **Total** | **≈ 4.4 GB** | |

## Sequencing rationale

Secrets first (protect), then caches (free, no risk), then moves (reversible), then
consolidation (needs decisions), then large tools (needs decisions), then
documentation last so it describes the *final* state rather than the old one.
