# AI Company Builder — Definition of Done

> **Authority Level**: Layer 11 — derived from [00-CONSTITUTION.md](00-CONSTITUTION.md)
> **Immutable Rule Reference**: IR-3 (Tests), IR-4 (Type annotations), IR-8 (Human approval)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document defines the completion criteria for all work in AI Company Builder. Nothing is considered complete until ALL applicable criteria are satisfied. This is the quality gate that prevents partial or broken work from being merged.

---

## 2 Scope

This document covers:

- Code completion criteria
- Documentation completion criteria
- Configuration completion criteria
- Architecture completion criteria
- Review completion criteria
- Release completion criteria

---

## 3 Code Completion Criteria

Nothing is code-complete until:

### 3.1 Mandatory (Always Required)

| # | Criterion | Verification |
|---|-----------|-------------|
| C-1 | All tests pass | `pytest` — 0 failures |
| C-2 | Lint passes | `ruff check src/` — 0 errors (excluding known E402) |
| C-3 | Type check passes | `mypy src/` — 0 errors |
| C-4 | Formatting passes | `black src/` — 0 changes |
| C-5 | No secrets in source | Manual review + automated scan |
| C-6 | No bare `except:` clauses | `ruff check` |
| C-7 | All public APIs typed | `mypy` |
| C-8 | All public functions documented | Docstrings present |

### 3.2 Conditional (When Applicable)

| # | Criterion | When Required | Verification |
|---|-----------|--------------|-------------|
| C-9 | New tests for new code | Always (IR-3) | New test file or additions |
| C-10 | Regression test for bug fix | When fixing bugs | Test that reproduces the bug |
| C-11 | Config file updated | When changing config schema | `load_config()` succeeds |
| C-12 | Template updated | When changing output format | Template renders correctly |
| C-13 | CLI command works | When adding CLI commands | `ai-company <cmd> --help` |
| C-14 | Generator produces correct output | When changing generator | Regeneration succeeds |

---

## 4 Documentation Completion Criteria

Nothing is documented-complete until:

### 4.1 Mandatory

| # | Criterion | Verification |
|---|-----------|-------------|
| D-1 | Docstrings on all public functions | `mypy` + manual review |
| D-2 | Module docstrings present | Each module has module docstring |
| D-3 | README.md is current | Reflects current state |
| D-4 | ARCHITECTURE.md is current | Reflects current structure |
| D-5 | STATUS.md is current | Reflects recent work |

### 4.2 Conditional

| # | Criterion | When Required |
|---|-----------|--------------|
| D-6 | ADR recorded | Architectural decisions |
| D-7 | CHANGELOG.md updated | Version-relevant changes |
| D-8 | .ai-company/state/ docs updated | Significant changes |
| D-9 | Template examples updated | Template changes |

---

## 5 Configuration Completion Criteria

Nothing is config-complete until:

| # | Criterion | Verification |
|---|-----------|-------------|
| CF-1 | YAML files are valid | `load_config()` succeeds |
| CF-2 | All 19 files present | `load_raw_files()` succeeds |
| CF-3 | Models parse correctly | `parse_all()` succeeds |
| CF-4 | Cross-references resolve | `resolve()` succeeds |
| CF-5 | Structure validates | `validate()` succeeds |
| CF-6 | Generated agents are valid | Generation succeeds |
| CF-7 | Generated configs are valid | YAML output is parseable |

---

## 6 Architecture Completion Criteria

Nothing is architecturally complete until:

| # | Criterion | Verification |
|---|-----------|-------------|
| A-1 | Follows clean architecture layers | Code review |
| A-2 | No circular imports | `mypy` + import check |
| A-3 | Single responsibility per module | Code review |
| A-4 | Dependencies point inward | Architecture review |
| A-5 | Public API is minimal | Code review |
| A-6 | No God objects | Code review |
| A-7 | No God functions | Code review |

---

## 7 Review Completion Criteria

Nothing is review-complete until:

| # | Criterion | Verification |
|---|-----------|-------------|
| R-1 | Self-review completed | Author verified own code |
| R-2 | CI checks pass | GitHub Actions green |
| R-3 | Manual review approved | Reviewer approval |
| R-4 | Quality score >=3.0 | Review scorecard |
| R-5 | All critical issues resolved | No unresolved critical comments |
| R-6 | Security review passed | No security issues |

---

## 8 Release Completion Criteria

Nothing is release-ready until:

### 8.1 All Previous Criteria

Every item in sections 3-7 is satisfied.

### 8.2 Additional Release Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| REL-1 | Version number updated | `pyproject.toml` |
| REL-2 | CHANGELOG.md includes all changes | Manual review |
| REL-3 | All CLI commands verified | `ai-company --help` + each command |
| REL-4 | Bootstrap process verified | `ai-company company run` |
| REL-5 | Agent generation verified | 31 agents generated correctly |
| REL-6 | No regressions in existing features | Full test suite passes |

---

## 9 Verification Commands

### 9.1 Full Verification Suite

```bash
# From ai-company/ directory
ruff check src/                    # Lint
mypy src/                          # Type check
black src/                         # Format
pytest                             # Tests
ai-company --help                  # CLI
ai-company company run             # Bootstrap
```

### 9.2 Quick Verification

```bash
ruff check src/ && mypy src/ && pytest
```

### 9.3 CI Verification

```bash
# Same as CI pipeline
ruff check src/
mypy src/
pytest
pwsh scripts/lint-ecl.ps1
```

---

## 10 Exceptions

### 10.1 Known Exceptions

| Exception | Reason | Tracking |
|-----------|--------|----------|
| E402 in `llm/client.py` | Import order (pre-existing) | Not blocking |

### 10.2 Temporary Exceptions

Temporary exceptions must be:

1. Documented in `TECH_DEBT.md`
2. Have a resolution timeline
3. Approved by reviewer
4. Removed at earliest opportunity

---

## 11 Examples

### 11.1 Complete Change

```markdown
## Change: Add new decision engine feature

### Code Completion
- [x] All tests pass (175/175)
- [x] Lint passes (0 errors)
- [x] Type check passes (0 errors)
- [x] Formatting passes
- [x] No secrets
- [x] New tests added (test_decision.py: 11 tests)

### Documentation
- [x] Docstrings present
- [x] STATUS.md updated
- [x] ADR recorded for design decision

### Configuration
- [x] Config files valid
- [x] Generated agents valid

### Architecture
- [x] Follows clean architecture
- [x] No circular imports
- [x] Single responsibility

### Review
- [x] Self-review completed
- [x] CI green
- [x] Reviewer approved (score: 4.2)

### Status: COMPLETE
```

### 11.2 Incomplete Change

```markdown
## Change: Add new feature

### Code Completion
- [x] All tests pass
- [ ] Lint passes (2 errors)
- [x] Type check passes
- [x] Formatting passes
- [x] No secrets
- [ ] New tests added (tests pending)

### Status: NOT COMPLETE — must address lint errors and add tests
```

---

## 12 Best Practices

1. **Check before merging**: Run the verification commands locally.
2. **Don't skip criteria**: Every criterion exists for a reason.
3. **Track exceptions**: If you must skip a criterion, document it.
4. **Update this document**: When you find missing criteria, add them.
5. **Automate what you can**: CI catches most criteria automatically.

---

## 13 Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| "Tests pass locally but not in CI" | Environment differences | Investigate and fix |
| "Skip tests for now, add later" | Technical debt accumulates | Write tests first |
| "It's just a comment change" | Comments can have bugs | Verify everything |
| "I'll update docs later" | Docs get forgotten | Update with the change |
| "Score was 2.5 but I merged anyway" | Violates quality gate | Address issues first |

---

## 14 Future Enhancements

- Automated DoD verification in CI
- Quality score tracking over time
- Automated documentation freshness checking
- Architecture fitness functions
- Release readiness dashboard

---

## 15 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | IR-3, IR-4, IR-8 |
| [08-TESTING-STANDARDS.md](08-TESTING-STANDARDS.md) | Testing criteria |
| [09-CODE-REVIEW.md](09-CODE-REVIEW.md) | Review criteria |
| [12-DOCUMENTATION-STANDARDS.md](12-DOCUMENTATION-STANDARDS.md) | Documentation criteria |
| [AGENTS.md](../../AGENTS.md) | Verification commands |
