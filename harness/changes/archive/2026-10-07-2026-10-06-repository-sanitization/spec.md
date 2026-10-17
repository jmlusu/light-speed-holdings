# Specification

## Scope

Full repository sanitization targeting ~4.4 GB disk reclaim and ~400+ tracked file reduction while maintaining:
- All existing functionality (tests pass)
- All agent orchestration (generator round-trip)
- All runtime state integrity (§9.3 evidence preserved)
- All CI/CD pipelines (fresh clone works)

## Acceptance Criteria

### Stage 1: Secrets Hardening
- [ ] gitleaks detect --source . --redact → clean (history rewritten if needed)
- [ ] .gitignore includes: opencode.local.json, qa-*.png, qa-report*.json, *.log, tmp/, lab/
- [ ] .env.example: personal path removed, duplicate TURNSTILE_HOSTNAMES removed
- [ ] Tag: cleanup/c1-secrets

### Stage 2: Cache Purge
- [ ] Deleted: .mypy_cache/, .ruff_cache/, .pytest_cache/, .hypothesis/, .pytest_tmp*/, dist/
- [ ] Deleted tracked: install.log, probe.log, runtask.log, vite*.log, git_ls_files.txt
- [ ] .google notebook artifacts/ deleted
- [ ] All added to .gitignore
- [ ] Tag: cleanup/c2-caches

### Stage 3: Root Moves
- [ ] 11 root .py → scripts/maintenance/ (refs fixed)
- [ ] start_vite.bat, start-dev.ps1, Clean-LSMEM.ps1 → scripts/
- [ ] 9 directives → docs/directives/
- [ ] 14 specs/audits → docs/ or reports/
- [ ] 11 analysis reports → reports/
- [ ] SECURITY.md, DEPLOYMENT.md → docs/
- [ ] All references fixed (package.json, Makefile, .pre-commit-config.yaml, AGENTS.md, CI)
- [ ] Tag: cleanup/c3-root-moves

### Stage 4: Script Tree
- [ ] Created: scripts/{dev,build,test,deploy,maintenance,research}/
- [ ] 49 scripts moved into purpose dirs
- [ ] scripts/health_check.py created
- [ ] All references updated
- [ ] Tag: cleanup/c4-scripts

### Stage 5: Consolidation
- [ ] Brand tokens: brand/ canonical, public/static documented as build mirrors
- [ ] Milestones deck: one implementation kept (ref sweep decides)
- [ ] Registry .bak: .bak-2026-09-18 DELETED, .bak-2026-09-18-hybrid ARCHIVED
- [ ] Runtime state: relocated to ~/.lightspeed/runtime/ (except §9.3 evidence)
- [ ] open-design: .gitmodules added
- [ ] Branding landing page/ → ARCHIVED
- [ ] src.bak/ → verified empty diff → DELETED
- [ ] Tag: cleanup/c5-consolidation

### Stage 6: Generated Artifacts
- [ ] 15 generated root artifacts untracked
- [ ] agent-registry.json.bak-* DELETED
- [ ] models.yaml.executor-bak DELETED
- [ ] backups/ DELETED + backup.ps1 updated
- [ ] Tag: cleanup/c6-generated

### Stage 7: Large Tools
- [ ] scroll-craft: .opencode/skills/scroll-craft/, scrollcraft/, lab/ screenshots DELETED
- [ ] open-design: .gitmodules added, submodule init verified
- [ ] models/: strategy documented, kept gitignored
- [ ] case-study artifacts: duplicate QA screenshots DELETED
- [ ] Tag: cleanup/c7-large-tools

### Stage 8: Documentation
- [ ] README.md canonical entry
- [ ] ARCHITECTURE.md, DEVELOPMENT.md, ECL.md refreshed
- [ ] DEPLOYMENT.md created (consolidated from 4 sources)
- [ ] REPOSITORY_HEALTH.md created (BEFORE/AFTER)
- [ ] AGENTS.md cross-references verified
- [ ] Tag: cleanup/c8-docs

### Stage 9: Final Validation
- [ ] ruff check src/ && mypy src/ && pytest
- [ ] ai-company --help + generator round-trip clean
- [ ] Fresh clone smoke test passes (including submodule)
- [ ] pwsh scripts/lint-ecl.ps1 passes
- [ ] Root tracked count reduced, no oversized files
- [ ] Human: "REPOSITORY SANITIZATION: APPROVED"