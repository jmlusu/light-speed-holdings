# Release Plan

> **Last Updated**: 2026-07-16
> **Current Version**: 0.1.0

---

## Version Strategy

Follows [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

| Component | When |
|-----------|------|
| MAJOR | Breaking changes to public API |
| MINOR | New features (backward-compatible) |
| PATCH | Bug fixes (backward-compatible) |

---

## Release Schedule

### v0.1.0 — Foundation (Current)

**Status**: Released
**Date**: 2026-07-16

| Feature | Status |
|---------|--------|
| CLI (22 commands) | Complete |
| Models (17+) | Complete |
| Config (19 files) | Complete |
| Templates (7) | Complete |
| Generator | Complete |
| BootstrapEngine | Complete |
| DecisionEngine | Complete |
| WorkflowEngine | Complete |
| MemoryEngine | Complete |
| GraphEngine | Complete |
| Tests (175) | Complete |

### v0.2.0 — Autonomy

**Status**: Planned
**Target**: Next quarter

| Feature | Priority |
|---------|----------|
| Task execution loop | High |
| HITL gates | High |
| Briefing generation | Medium |
| Scheduler | Medium |
| LLM hardening | High |

### v0.3.0 — Learning

**Status**: Planned
**Target**: Q4 2026

| Feature | Priority |
|---------|----------|
| Performance analytics | High |
| Adaptive workflows | Medium |
| Knowledge accumulation | Medium |
| Dashboard completion | Low |

### v0.4.0 — Enterprise

**Status**: Planned
**Target**: Q1 2027

| Feature | Priority |
|---------|----------|
| Multi-tenant support | High |
| Compliance features | High |
| Plugin architecture | Medium |
| Marketplace | Low |

### v1.0.0 — Stable

**Status**: Planned
**Target**: Q2 2027

| Feature | Priority |
|---------|----------|
| Production-ready platform | High |
| Enterprise security | High |
| Performance SLAs | High |
| Full documentation | High |

---

## Release Checklist

For every release:

### Pre-Release

- [ ] All tests pass (`pytest`)
- [ ] Lint clean (`ruff check src/`)
- [ ] Type check clean (`mypy src/`)
- [ ] Version bumped in `pyproject.toml`
- [ ] CHANGELOG.md updated
- [ ] STATUS.md updated
- [ ] No known critical bugs

### Release

- [ ] Create release branch
- [ ] Final verification
- [ ] PR to main
- [ ] Get approval
- [ ] Merge to main
- [ ] Tag release
- [ ] Merge back to develop
- [ ] Push tags

### Post-Release

- [ ] Update PROJECT_STATUS.md
- [ ] Update ROADMAP.md
- [ ] Notify stakeholders

---

## Related Documents

- [CHANGELOG.md](CHANGELOG.md) — Version history
- [ROADMAP.md](ROADMAP.md) — Full roadmap
- [MILESTONES.md](MILESTONES.md) — Milestone tracking
- [constitution/11-GIT-STANDARDS.md](../constitution/11-GIT-STANDARDS.md) — Git workflow
