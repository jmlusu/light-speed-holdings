# Risks

> **Last Updated**: 2026-07-16

---

## Risk Matrix

| # | Risk | Category | Probability | Impact | Score | Mitigation |
|---|------|----------|------------|--------|-------|-----------|
| R-1 | Models.py grows unwieldy | Technical | Medium | Medium | 6 | Split at 30+ types |
| R-2 | LLM integration fragile | Technical | High | High | 9 | Harden with retries, fallbacks |
| R-3 | No automated security scanning | Security | Medium | High | 8 | Add Dependabot, pip audit |
| R-4 | Generated files hand-edited | Process | Low | High | 4 | CI check, Constitution rules |
| R-5 | Test coverage drops | Quality | Medium | Medium | 6 | 100% coverage for new code |
| R-6 | Single developer bottleneck | Project | High | Medium | 6 | Document everything, automate |
| R-7 | Scope creep | Project | High | High | 9 | Strict phase adherence |
| R-8 | Memory engine I/O coupling | Technical | Low | Medium | 3 | Extract ports when needed |
| R-9 | No CI/CD for deployments | Operations | Medium | Medium | 6 | Add deployment pipeline |
| R-10 | Constitution becomes stale | Process | Medium | Medium | 6 | Update with each sprint |

---

## Technical Risks

### R-1: Models.py Growth

**Probability**: Medium
**Impact**: Medium

The `models/models.py` file is 560+ lines with 17+ types. At 30+ types, it becomes hard to navigate.

**Mitigation**: Monitor file length. Split into domain packages when threshold is reached.

**Trigger**: File exceeds 800 lines or 30 types.

### R-2: LLM Integration Fragility

**Probability**: High
**Impact**: High

LLM providers have rate limits, timeouts, and format changes. Current integration is basic.

**Mitigation**: Add retry logic, fallback providers, response validation, cost tracking.

**Trigger**: First production deployment.

### R-8: Memory Engine I/O Coupling

**Probability**: Low
**Impact**: Medium

`MemoryEngine` does file I/O directly, violating clean architecture. Acceptable for v1 but limits flexibility.

**Mitigation**: Extract port/adapter interfaces when multiple storage backends are needed.

**Trigger**: Need for Redis/PostgreSQL storage.

---

## Security Risks

### R-3: No Automated Security Scanning

**Probability**: Medium
**Impact**: High

No Dependabot, no `pip audit` in CI, no secret detection. Manual scanning is error-prone.

**Mitigation**: Add Dependabot, integrate `pip audit` in CI, add pre-commit hooks.

**Timeline**: Next sprint.

---

## Process Risks

### R-4: Generated Files Hand-Edited

**Probability**: Low
**Impact**: High

If generated `.opencode/agents/*.md` files are hand-edited, regeneration will overwrite changes.

**Mitigation**: Constitution rule (IR-2), CI check, documentation.

### R-7: Scope Creep

**Probability**: High
**Impact**: High

The platform has many possible features. Without strict phase adherence, scope can balloon.

**Mitigation**: Follow roadmap strictly. Phase 3 = Autonomy. Phase 4 = Learning. Don't jump ahead.

### R-10: Constitution Becomes Stale

**Probability**: Medium
**Impact**: Medium

Constitution documents may drift from actual codebase state.

**Mitigation**: Update state files with each sprint. Review constitution quarterly.

---

## Project Risks

### R-6: Single Developer Bottleneck

**Probability**: High
**Impact**: Medium

Single developer means knowledge is concentrated. Bus factor = 1.

**Mitigation**: Comprehensive documentation, automated testing, clear processes.

---

## Risk Review Schedule

| Frequency | Action |
|-----------|--------|
| Each sprint | Review risk matrix, update scores |
| Monthly | Review mitigation effectiveness |
| Quarterly | Full risk assessment, add/remove risks |

---

## Related Documents

- [PROJECT_STATUS.md](PROJECT_STATUS.md) — Current status
- [TECH_DEBT.md](TECH_DEBT.md) — Known issues
- [NEXT_ACTIONS.md](NEXT_ACTIONS.md) — Prioritized actions
- [constitution/13-SECURITY-STANDARDS.md](../constitution/13-SECURITY-STANDARDS.md) — Security standards
