# AI Company Builder — Git Standards

> **Authority Level**: Layer 12 — derived from [10-DEFINITION-OF-DONE.md](10-DEFINITION-OF-DONE.md)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document defines the Git workflow standards for AI Company Builder. Consistent Git practices ensure a clean history, traceable changes, and safe collaboration.

---

## 2 Scope

This document covers:

- GitFlow branching model
- Branch naming conventions
- Commit message format
- Pull request process
- Versioning strategy
- Release process
- Hotfix process
- Tagging

---

## 3 GitFlow Branching Model

### 3.1 Branch Types

| Branch | Purpose | Lifetime | Merges Into |
|--------|---------|----------|------------|
| `main` | Production-ready code | Permanent | — |
| `develop` | Integration branch | Permanent | `main` (via release) |
| `feature/*` | New features | Temporary | `develop` |
| `hotfix/*` | Production fixes | Temporary | `main` + `develop` |
| `release/*` | Release preparation | Temporary | `main` + `develop` |

### 3.2 Branch Flow

```
main ─────────────────────────────────────────────────►
  │                                   ▲                ▲
  │                                   │                │
  ▼                                   │                │
develop ────────●──────●──────●───────┤                │
                │      │      │       │                │
                ▼      ▼      ▼       │                │
             feature feature release──┘                │
                                  │                    │
                                  └────────────────────┘
```

### 3.3 Rules

| Rule | Description |
|------|------------|
| `main` is always deployable | No direct commits to `main` |
| `develop` is the integration point | All features merge here first |
| Features branch from `develop` | Isolate new work |
| Releases branch from `develop` | Stabilize before release |
| Hotfixes branch from `main` | Fix production issues |
| All merges require PR | No direct pushes to shared branches |

---

## 4 Branch Naming

### 4.1 Convention

```
<type>/<ticket-id>-<short-description>
```

### 4.2 Examples

| Type | Example |
|------|---------|
| Feature | `feature/123-add-budget-engine` |
| Hotfix | `hotfix/456-fix-memory-leak` |
| Release | `release/0.2.0` |
| Docs | `docs/update-architecture` |
| Refactor | `refactor/clean-models` |
| Test | `test/add-integration-tests` |

### 4.3 Rules

| Rule | Rationale |
|------|-----------|
| Use lowercase with hyphens | Readable, diffable |
| Include ticket ID | Traceability |
| Keep description short (<50 chars) | Readability |
| Use conventional prefixes | Automation can parse |

---

## 5 Commit Messages

### 5.1 Format

```
<type>(<scope>): <short description>

<body>

<footer>
```

### 5.2 Types

| Type | Description |
|------|------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, configs |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |

### 5.3 Examples

```
feat(decision): add risk assessment engine

Implement DecisionEngine with approval matrix matching,
risk keyword detection, and decision tree navigation.

- Add DecisionEngine class
- Add risk matrix parsing
- Add 11 unit tests

Closes #123
```

```
fix(memory): fix consolidation duplicate detection

Memory consolidation was not properly detecting duplicate
entries due to case-sensitive string comparison.

- Add case-insensitive comparison
- Add regression test
- Update TECH_DEBT.md

Fixes #456
```

### 5.4 Rules

| Rule | Rationale |
|------|-----------|
| Subject line <72 characters | Git log readability |
| Use imperative mood ("add" not "added") | Consistency |
| Body explains what and why | Not how (code shows how) |
| Reference issues | Traceability |
| Separate subject from body with blank line | Git formatting |

---

## 6 Pull Requests

### 6.1 PR Template

```markdown
## Summary
[1-2 sentence summary of the change]

## Motivation
[Why this change is needed]

## Changes
- [List of specific changes]

## Testing
- [ ] Tests added/updated
- [ ] All tests pass locally
- [ ] Lint passes
- [ ] Type check passes

## Documentation
- [ ] Docstrings updated
- [ ] STATUS.md updated (if significant)
- [ ] ADR recorded (if architectural)

## Breaking Changes
[List any breaking changes, or "None"]

## Related Issues
[Closes #123]
```

### 6.2 PR Rules

| Rule | Rationale |
|------|-----------|
| PRs should be small (<400 lines) | Reviewable |
| PRs should be focused | One concern per PR |
| PRs need at least 1 approval | Quality gate |
| CI must pass | Automated quality |
| Branch must be up-to-date with develop | Prevent merge conflicts |

---

## 7 Versioning

### 7.1 Semantic Versioning

```
MAJOR.MINOR.PATCH
```

| Component | When to Increment |
|-----------|-------------------|
| MAJOR | Breaking changes to public API |
| MINOR | New features (backward-compatible) |
| PATCH | Bug fixes (backward-compatible) |

### 7.2 Current Version

**v0.1.0** — Foundation phase

### 7.3 Version Progression

| Version | Phase | Key Changes |
|---------|-------|-------------|
| 0.1.0 | Foundation | CLI, models, config, generator, tests |
| 0.2.0 | Intelligence | Decision, workflow, memory, graph engines |
| 0.3.0 | Autonomy | Task execution, HITL, briefings |
| 0.4.0 | Learning | Performance analytics, adaptive workflows |
| 0.5.0 | Enterprise | Multi-tenant, compliance, marketplace |
| 1.0.0 | Stable | Production-ready platform |

---

## 8 Release Process

### 8.1 Steps

1. **Create release branch**: `git checkout -b release/0.2.0 develop`
2. **Update version**: `pyproject.toml` version bump
3. **Update CHANGELOG.md**: Document all changes
4. **Run full verification**: `ruff check src/ && mypy src/ && pytest`
5. **Create PR**: `release/0.2.0` → `main`
6. **Get approval**: Reviewer verifies release readiness
7. **Merge to main**: Squash merge
8. **Tag release**: `git tag -a v0.2.0 -m "Release 0.2.0"`
9. **Merge back to develop**: `main` → `develop`
10. **Push tags**: `git push origin main --tags`

### 8.2 Release Checklist

- [ ] All tests pass
- [ ] Lint clean
- [ ] Type check clean
- [ ] Version bumped in `pyproject.toml`
- [ ] CHANGELOG.md updated
- [ ] STATUS.md updated
- [ ] ARCHITECTURE.md updated (if needed)
- [ ] All PRs merged
- [ ] No known critical bugs

---

## 9 Hotfix Process

### 9.1 Steps

1. **Create hotfix branch**: `git checkout -b hotfix/456-fix-bug main`
2. **Fix the bug**: Implement fix
3. **Add regression test**: Prevent recurrence
4. **Update version**: Patch bump in `pyproject.toml`
5. **Create PR**: `hotfix/456-fix-bug` → `main`
6. **Get approval**: Reviewer verifies fix
7. **Merge to main**: Squash merge
8. **Tag hotfix**: `git tag -a v0.1.1 -m "Hotfix 0.1.1"`
9. **Merge back to develop**: `main` → `develop`
10. **Push tags**: `git push origin main --tags`

---

## 10 Tagging

### 10.1 Convention

```
v<MAJOR>.<MINOR>.<PATCH>
```

### 10.2 Examples

```
v0.1.0    # Initial release
v0.1.1    # Patch release
v0.2.0    # Feature release
v1.0.0    # Stable release
```

### 10.3 Tag Format

```bash
git tag -a v0.2.0 -m "Release 0.2.0 — Intelligence Phase"
```

---

## 11 Rules Summary

| Rule | Description |
|------|------------|
| No direct commits to `main` | Always through PR |
| No direct commits to `develop` | Always through feature PR |
| All PRs need CI green | Automated quality gate |
| All PRs need approval | Human quality gate |
| Commit messages follow convention | Traceability |
| Branches follow naming convention | Automation |
| Versions follow semver | Predictability |
| Releases follow checklist | Completeness |

---

## 12 Examples

### 12.1 Feature Workflow

```bash
# Start feature
git checkout develop
git pull
git checkout -b feature/123-add-memory-engine

# Work
# ... make changes ...
git add .
git commit -m "feat(memory): add memory store with 6 types"

# Push and create PR
git push origin feature/123-add-memory-engine
# Create PR: feature/123-add-memory-engine → develop

# After approval and merge
git checkout develop
git pull
git branch -d feature/123-add-memory-engine
```

### 12.2 Hotfix Workflow

```bash
# Start hotfix
git checkout main
git pull
git checkout -b hotfix/456-fix-memory-leak

# Fix
# ... make changes ...
git add .
git commit -m "fix(memory): fix leak in consolidation"

# Push and create PR
git push origin hotfix/456-fix-memory-leak
# Create PR: hotfix/456-fix-memory-leak → main

# After merge
git checkout main
git pull
git tag -a v0.1.1 -m "Hotfix 0.1.1"
git checkout develop
git merge main
git push origin main --tags
```

---

## 13 Future Enhancements

- Automated changelog generation
- Branch protection rules in GitHub
- Commit signature verification
- Automated version bumping
- Release automation with GitHub Actions

---

## 14 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | Supreme authority |
| [10-DEFINITION-OF-DONE.md](10-DEFINITION-OF-DONE.md) | Completion criteria |
| [12-DOCUMENTATION-STANDARDS.md](12-DOCUMENTATION-STANDARDS.md) | Documentation for releases |
| [state/CHANGELOG.md](../state/CHANGELOG.md) | Changelog |
| [state/RELEASE_PLAN.md](../state/RELEASE_PLAN.md) | Release plan |
