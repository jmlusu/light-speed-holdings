# Git Workflow & Branch Conventions

## Branch Model

```
main (protected trunk)
│
├── production (protected, release tags only)
│
├── development (continuous staging deploy)
│
├── reconciliation-aistudio-opencode (short-lived, auto-delete on merge)
│
├── feature/* (new functionality, PR → main)
│
├── hotfix/* (urgent production fixes, PR → production → backport to main)
│
├── fix/* (bug fixes, PR → main)
│
├── build/* (infrastructure/tooling, PR → main)
│
├── chore/* (maintenance, PR → main)
│
├── research/* (spikes/experiments, PR → main or discard)
│
├── governance/* (policy/docs, PR → main)
│
└── resolve/* (wayfinder ticket resolution, PR → main)
```

## Branch Protection Summary

| Branch | PR Required | Status Checks | Force Push | Linear History | Auto-delete on Merge |
|--------|-------------|---------------|------------|----------------|---------------------|
| `main` | ✅ | 10 checks | ❌ | ✅ | ❌ |
| `production` | ✅ | 10 checks | ❌ | ✅ | ❌ |
| `development` | ✅ | 10 checks | ✅ | ❌ | ❌ |
| `feature/*` | ✅ | 10 checks | ✅ | ❌ | ✅ |
| `hotfix/*` | ✅ | 10 checks | ✅ | ❌ | ✅ |
| `reconciliation-*` | ❌ | 10 checks | ✅ | ❌ | ✅ |

**Required status checks (all branches):**
- Lint (ruff)
- Type check (mypy)
- Test (ubuntu-latest)
- Test (windows-latest)
- ECL Harness Lint
- Security (bandit)
- Dependency Audit (uv-audit)
- Generated Files Drift Check
- Archify Diagram Check
- Version Sync Check

## Workflow Rules

### Feature Work
1. `git checkout -b feature/descriptive-name main`
2. Implement + test locally (`ruff && mypy && pytest`)
3. Push, open PR → `main`
4. CI gate must pass + approval → squash merge
5. Branch auto-deleted

### Hotfix Work (Production Incident)
1. `git checkout -b hotfix/description production`
2. Fix + verify locally
3. Push, open PR → `production`
4. CI gate passes + approval → squash merge to `production`
5. **Backport:** `git checkout main && git cherry-pick -x <hotfix-merge-commit>`
6. Push `main` (CI re-runs automatically)

### Reconciliation Work
1. `git checkout -b reconciliation/ticket-name main`
2. Resolve technical debt / cross-cutting concern
3. Push, open PR → `main`
4. Auto-deletes on merge

### Development Branch
- Auto-deploys to staging on push
- Integration testing target
- PRs from feature branches can target `development` for staging validation before `main`

### Release Process
1. Ensure `production` is green
2. `git checkout production && git pull`
3. `scripts/release.ps1` (or manual tag `vX.Y.Z`)
4. Release workflow: version sync → Trivy → build → PyPI + GHCR → GitHub Release → canary deploy

## Naming Conventions

| Prefix | Purpose | Target | Lifetime |
|--------|---------|--------|----------|
| `feature/` | New functionality | `main` | Days-weeks |
| `hotfix/` | Production emergency fix | `production` | Hours-days |
| `fix/` | Bug fix (non-urgent) | `main` | Days |
| `build/` | CI/infra/tooling | `main` | Days |
| `chore/` | Maintenance/deps | `main` | Days |
| `research/` | Spikes, PoCs | `main` or discard | Days-weeks |
| `governance/` | Policy, docs, ADRs | `main` | Days |
| `resolve/` | Wayfinder ticket resolution | `main` | Days |

## Commit Message Format

Follow conventional commits (enforced by CI version-sync check):
```
<type>(<scope>): <subject>

<body>

<footer>
```
Types: `feat`, `fix`, `build`, `chore`, `docs`, `refactor`, `perf`, `test`, `security`, `ci`

## Current Active Branches (as of 2026-09-18)

| Branch | Type | Worktree | Purpose |
|--------|------|----------|---------|
| `main` | trunk | ✅ | Protected trunk |
| `production` | protected | — | Release tags only |
| `development` | protected | — | Staging auto-deploy |
| `reconciliation-aistudio-opencode` | reconciliation | — | AI Studio / OpenCode reconciliation |
| `feature/b1-smtp-send` | feature | ✅ | SMTP migration (ADR-021) |
| `fix/function-region` | fix | ✅ | Vercel iad1 region pin |