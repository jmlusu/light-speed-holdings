# Plan

## Technical Approach

Execute 9-stage cleanup per LightSpeed Phased Approval & Rollback Protocol:

1. **Stage 0** (Complete): Read-only audit → repo-audit/ (11 files)
2. **Stage 1**: Secrets hardening — gitleaks history rewrite, .gitignore, .env.example
3. **Stage 2**: Zero-risk cache purge — delete all caches, tmp dirs, tracked logs
4. **Stage 3**: Root moves — 11 root .py → scripts/maintenance/, directives → docs/directives/
5. **Stage 4**: Script tree consolidation — scripts/{dev,build,test,deploy,maintenance,research}/
6. **Stage 5**: Duplicate consolidation — brand tokens, milestones deck, registry .bak, runtime state
7. **Stage 6**: Generated artifact policy — untrack generated, relocate runtime, fix backup.ps1
7. **Stage 7**: Large-tool decisions — scroll-craft DELETE, open-design SUBMODULE, models/ document
8. **Stage 8**: Documentation — README, refresh ARCHITECTURE/DEVELOPMENT/ECL, create DEPLOYMENT/REPOSITORY_HEALTH
9. **Stage 9**: Full validation — ruff+mypy+pytest, generator round-trip, fresh-clone smoke, lint-ecl

Each stage = separate commit(s), validation after each, checkpoint tag.

## Impacted Modules And Files

- Root directory (107 tracked files → sparse set)
- scripts/ (49 flat → 6 subdirectories)
- .opencode/skills/ (scroll-craft 692 MB → DELETE)
- brand/tokens/ (3 copies → 1 canonical + 2 build mirrors)
- company/ (agent-registry.json.bak* → DELETE/ARCHIVE)
- open-design/ (2.7 GB gitlink → .gitmodules)
- orchestrator/ & memory/ (runtime → ~/.lightspeed/runtime/, keep §9.3 evidence)
- docs/ (refresh + consolidate)

## Interfaces, Data, Permissions

- Agent registry generation: company-registry.yaml → company/agent-registry.json (sync script)
- Brand tokens sync: brand/ → public/brand/, static/brand/ (sync-brand.ps1)
- Runtime state: orchestrator/approvals.yaml tracked, escalation_events.jsonl & dead_letter.jsonl (§9.3) stay at root
- Backup output: scripts/backup.ps1 → writes outside repo

## Spec Gaps Found From Planning

- scripts/health_check.py canonical health check needs creation
- Fresh-clone smoke test must validate open-design submodule init
- gitleaks CI gate needs addition to .github/workflows/ci.yml

## Risks And Mitigations

| Risk | Mitigation |
|------|------------|
| gitleaks history rewrite breaks clones | Tag c0-baseline, document rotation procedure |
| Root moves break script refs | grep sweep before move, fix all references atomically |
| scroll-craft still in use | Confirmed retired per AGENTS.md §9.2; Q8=YES |
| open-design submodule breaks CI | Test submodule init in fresh clone before promoting |
| Runtime state relocation breaks executor | Keep §9.3 evidence at root; test executor after move |

## Verification Plan

Per stage:
- ruff check src/
- mypy src/
- pytest (unit)
- build (npm run build / ai-company generate)

Final:
- Fresh clone + submodule init + build + test
- Generator round-trip: AgentGenerator().generate_all()
- ai-company --help
- pwsh scripts/lint-ecl.ps1
- Tracked root file count reduction
- REPOSITORY_HEALTH.md BEFORE/AFTER comparison