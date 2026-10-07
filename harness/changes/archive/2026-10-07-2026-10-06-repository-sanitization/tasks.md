# Tasks

## Stage 0: Baseline & Audit (COMPLETE)
- [x] T001 Baseline capture: git tag cleanup/c0-baseline
- [x] T002 Read-only audit: repo-audit/ (11 files)
- [x] T003 Human approval: Q1–Q8 answered
- [x] T004 ECL change created: 2026-10-06-repository-sanitization

## Stage 1: Secrets Hardening (IN PROGRESS)
- [x] T005 Install gitleaks
- [x] T006 Run gitleaks detect --source . --redact
- [x] T007 If findings: rotate credentials, rewrite history
- [x] T008 Update .gitignore: opencode.local.json, qa-*.png, qa-report*.json, *.log, tmp/, lab/
- [x] T009 Fix .env.example: remove personal path, remove duplicate TURNSTILE_HOSTNAMES
- [x] T010 Commit: chore(repo): secrets hardening
- [x] T011 Tag: cleanup/c1-secrets
- [x] T012 Validate: ruff + mypy + pytest

## Stage 2: Cache Purge
- [x] T013 Delete: .mypy_cache/, .ruff_cache/, .pytest_cache/, .hypothesis/
- [x] T014 Delete: .pytest_tmp/, .pytest_tmp_ci/, .pytest_tmp_ci2/, .pytest_tmp_commit/, .pytest_tmp_linkedin/
- [x] T015 Delete: dist/
- [x] T016 Delete tracked: install.log, probe.log, runtask.log, vite.log, vite_start.log, vite-dev.log, git_ls_files.txt
- [x] T017 Delete: .google notebook artifacts/
- [x] T018 Add all to .gitignore
- [x] T019 Commit: chore(repo): purge caches and generated artifacts
- [x] T020 Tag: cleanup/c2-caches
- [x] T021 Validate: ruff + mypy + pytest

## Stage 3: Root Moves
- [x] T022 grep refs for 11 root .py scripts
- [x] T023 Move 11 root .py → scripts/maintenance/
- [x] T024 Move start_vite.bat, start-dev.ps1, Clean-LSMEM.ps1 → scripts/
- [x] T025 Move 9 directives → docs/directives/
- [x] T026 Move 14 specs/audits → docs/ or reports/
- [x] T027 Move 11 analysis reports → reports/
- [x] T028 Move SECURITY.md, DEPLOYMENT.md → docs/
- [x] T029 Fix all references (package.json, Makefile, .pre-commit-config.yaml, AGENTS.md, CI)
- [x] T030 Commit per logical group
- [x] T031 Tag: cleanup/c3-root-moves
- [x] T032 Validate after each: ruff + mypy + pytest + build

## Stage 4: Script Tree Consolidation
- [x] T033 Create scripts/{dev,build,test,deploy,maintenance,research}/
- [x] T034 Move 49 scripts into purpose directories
- [x] T035 Create scripts/health_check.py
- [x] T036 Update all references
- [x] T037 Commit: refactor(scripts): consolidate into subdirectories
- [x] T038 Tag: cleanup/c4-scripts
- [x] T039 Validate: ruff + mypy + pytest + all script refs

## Stage 5: Duplicate Consolidation
- [x] T040 Brand tokens: document public/ + static/ as build mirrors (Q1=YES)
- [ ] T041 Milestones deck: ref sweep → pick one → delete other (DEFERRED — Q3 unanswered; see Deferred Tasks)
- [x] T042 Registry .bak: delete .bak-2026-09-18, archive .bak-2026-09-18-hybrid
- [ ] T043 Runtime state: create ~/.lightspeed/runtime/, move orchestrator/ + memory/ (except §9.3) (DEFERRED — needs code changes; see Deferred Tasks)
- [x] T044 open-design: add .gitmodules entry
- [x] T045 Branding landing page/ → archive
- [x] T046 src.bak/ → verified absent, nothing to do
- [x] T047 Commit per consolidation
- [x] T048 Tag: cleanup/c5-consolidation
- [x] T049 Validate: ruff + mypy + pytest + generator round-trip

## Stage 6: Generated Artifact Policy
- [x] T050 Untrack 15 generated root artifacts (QA/logs in Stage 1, git_ls_files in Stage 2)
- [x] T051 Delete agent-registry.json.bak-* and models.yaml.executor-bak
- [ ] T052 Relocate runtime state out of root (except §9.3 evidence) (DEFERRED — see Deferred Tasks)
- [x] T053 Delete backups/ + update backup.ps1 → write outside repo
- [x] T054 Commit: chore(repo): generated artifact policy
- [x] T055 Tag: cleanup/c6-generated
- [x] T056 Validate: ruff + mypy + pytest

## Stage 7: Large-Tool Decisions
- [x] T057 scroll-craft: DELETE .opencode/skills/scroll-craft/, scrollcraft/, lab/ screenshots
- [x] T058 open-design: .gitmodules declared, origin reachable (full fresh-clone test DEFERRED — see Deferred Tasks)
- [x] T059 models/: verified gitignored + regenerable (strategy recorded in REPOSITORY_HEALTH.md + DEPLOYMENT.md)
- [x] T060 case-study artifacts: DELETE duplicate QA screenshots
- [x] T061 Commit per item
- [x] T062 Tag: cleanup/c7-large-tools
- [x] T063 Validate: ruff + mypy + pytest (fresh clone test deferred)

## Stage 8: Documentation
- [x] T064 README.md → canonical entry point (milestone-deck paths fixed)
- [x] T065 Refresh ARCHITECTURE.md (no stale refs found — no change needed)
- [x] T066 Refresh DEVELOPMENT.md (scripts layout, harness paths, backup docs)
- [x] T067 Refresh ECL.md (no stale refs found — no change needed)
- [x] T068 Create DEPLOYMENT.md (canonical entry point + source index)
- [x] T069 Create REPOSITORY_HEALTH.md (BEFORE/AFTER metrics)
- [x] T070 Verify AGENTS.md cross-references (swept clean)
- [x] T071 Commit: docs(repo): post-cleanup documentation
- [x] T072 Tag: cleanup/c8-docs
- [x] T073 Validate: ruff + mypy + pytest

## Stage 9: Final Validation
- [x] T074 ruff check src/ && mypy src/ && pytest (pass; 4 documented exclusions)
- [x] T075 ai-company --help + generator round-trip (pass, no drift)
- [ ] T076 Fresh clone smoke test (DEFERRED — network clone of 2.7 GB submodule; see Deferred Tasks)
- [x] T077 pwsh scripts/maintenance/lint-ecl.ps1 (pass)
- [x] T078 Root tracked file count check (107 → 32)
- [x] T079 REPOSITORY_HEALTH.md final comparison (done)
- [ ] T080 Human final approval (DEFERRED — awaiting owner; see Deferred Tasks)
- [x] T081 Close ECL change (merge to main left to owner)

## Deferred Tasks

- T041 (Q3): pick the surviving milestones deck (`.py` runs on installed
  toolchain; `.js` needs uninstalled `pptxgenjs`; neither is referenced).
  Owner decision required before any deletion.
- T043/T052 (D-6): relocate root `orchestrator/` + `memory/` runtime state.
  Needs code + config changes on live paths; executor/dashboard/CLI read
  them today. Requires a mini-proposal with rollback plan + human approval.
- Q4 follow-up: `src/ai_company/memory/` vs `lsmem/` — evidence shows the
  legacy store is still load-bearing (executor, dashboard, MCP, doctor,
  services, CLI). Needs a human architecture decision; delete neither.
- `tmp/` tracked scratch triage (~40 files, looks like another session's
  scaffolding). Owner to classify or remove.
- T058/T063/T076: full fresh-clone verification of the open-design
  submodule pin (metadata verified: `.gitmodules` parses, origin
  reachable, gitlink commit recorded).
- T080: owner final approval + promotion (merge) decision.