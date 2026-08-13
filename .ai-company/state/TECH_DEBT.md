# Technical Debt

> **Last Updated**: 2026-07-16

---

## Known Issues

### Critical (Security/Data Risk)

| # | Issue | Location | Mitigation | Resolution |
|---|-------|----------|-----------|-----------|
| — | None identified | — | — | — |

### High (Blocks Development)

| # | Issue | Location | Mitigation | Resolution |
|---|-------|----------|-----------|-----------|
| TD-1 | E402 import order warnings | `src/ai_company/llm/client.py` | Not blocking | Refactor imports |

### Medium (Inconvenience)

| # | Issue | Location | Mitigation | Resolution |
|---|-------|----------|-----------|-----------|
| TD-2 | Legacy files in root `src/ai_company/` | Root package | Ignore root, work in `ai-company/` | Remove legacy |
| TD-3 | Two `.venv` directories | Root + `ai-company/` | Use `ai-company/.venv/` | Consolidate |
| TD-4 | Models.py single file (560+ lines) | `models/models.py` | Manageable at 17+ types | Split at 30+ |
| TD-5 | Memory engine does file I/O directly | `memory/engine.py` | Acceptable for v1 | Extract ports/adapters |

### Low (Cosmetic/Theoretical)

| # | Issue | Location | Mitigation | Resolution |
|---|-------|----------|-----------|-----------|
| TD-6 | No Dependabot configured | `.github/` | Manual scanning | Configure Dependabot |
| TD-7 | No pre-commit hooks | Project root | Manual verification | Add pre-commit |
| TD-8 | No coverage reporting in CI | CI pipeline | Manual coverage checks | Add coverage job |
| TD-9 | No hash checking for generated files | Generator | Manual verification | Implement manifests |
| TD-10 | Dashboard is skeleton | `dashboard/api.py` | Not critical | Complete implementation |

---

## Future Improvements

### Short-Term (Next Sprint)

1. Fix E402 import order in `llm/client.py`
2. Remove legacy root `src/ai_company/` files
3. Add Dependabot configuration
4. Add pre-commit hooks for ruff, black, mypy

### Medium-Term (Next Quarter)

1. Extract domain models into separate packages
2. Add port/adapter interfaces for storage
3. Implement task execution loop
4. Complete dashboard implementation
5. Add coverage reporting to CI

### Long-Term (Next Year)

1. Plugin architecture for third-party extensions
2. Event-driven engine communication
3. Distributed memory (Redis/PostgreSQL)
4. Persistent graph (Neo4j)
5. Multi-tenant support

---

## Debt Classification

| Class | Criteria | Action Timeline |
|-------|----------|----------------|
| Critical | Security risk or data loss | Fix immediately |
| High | Blocks other development | Fix within sprint |
| Medium | Workaround exists | Fix within quarter |
| Low | Theoretical improvement | Backlog |

---

## Related Documents

- [PROJECT_STATUS.md](PROJECT_STATUS.md) — Current status
- [RISKS.md](RISKS.md) — Risk assessment
- [constitution/03-ENGINEERING-STANDARDS.md](../constitution/03-ENGINEERING-STANDARDS.md) — Engineering standards
