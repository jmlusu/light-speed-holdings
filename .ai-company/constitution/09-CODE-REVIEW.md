# AI Company Builder — Code Review

> **Authority Level**: Layer 10 — derived from [04-CODING-STANDARDS.md](04-CODING-STANDARDS.md)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document defines the code review standards for AI Company Builder. Code review is the primary quality gate before changes are merged. Every change must be reviewed against these checklists.

---

## 2 Scope

This document covers:

- Review checklist (general)
- Architecture review
- Security review
- Performance review
- Maintainability review
- Readability review
- Technical debt review
- Quality scoring system
- Release readiness checklist

---

## 3 General Review Checklist

Every code review must verify:

### 3.1 Functionality

- [ ] Does the code do what it claims to do?
- [ ] Are edge cases handled?
- [ ] Are error conditions handled gracefully?
- [ ] Is the behavior consistent with the Constitution?

### 3.2 Code Quality

- [ ] Does the code follow 04-CODING-STANDARDS.md?
- [ ] Are type annotations complete?
- [ ] Are there unnecessary comments?
- [ ] Is the code DRY?
- [ ] Is the code KISS?

### 3.3 Testing

- [ ] Are there tests for the change?
- [ ] Do tests cover success and failure paths?
- [ ] Do tests cover edge cases?
- [ ] Are tests independent?

### 3.4 Documentation

- [ ] Are docstrings present and accurate?
- [ ] Is README.md updated if needed?
- [ ] Are architectural decisions recorded (ADR)?

### 3.5 Security

- [ ] No secrets in source code
- [ ] Input validation present
- [ ] Permission checks enforced
- [ ] No new security risks introduced

---

## 4 Architecture Review

Verify changes adhere to the architecture defined in [02-ARCHITECTURE.md](02-ARCHITECTURE.md):

### 4.1 Layer Compliance

| Check | Rule |
|-------|------|
| CLI layer | Does not contain business logic |
| Engine layer | Does not depend on CLI or I/O (except memory/graph) |
| Domain models | Pure Pydantic, no external dependencies |
| Configuration | YAML files are source of truth |

### 4.2 Module Boundaries

| Check | Rule |
|-------|------|
| Single responsibility | Module has one clear purpose |
| Dependency direction | Dependencies point inward |
| No circular imports | Import graph is a DAG |
| Public API | Only intended interface is exposed |

### 4.3 Component Design

| Check | Rule |
|-------|------|
| Engines are focused | Each engine handles one domain concept |
| Models are clean | Pure data structures with validation |
| Templates are simple | No business logic in templates |

---

## 5 Security Review

### 5.1 Checklist

| # | Check | Reference |
|---|-------|-----------|
| SEC-1 | No secrets in source code | [13-SECURITY-STANDARDS.md](13-SECURITY-STANDARDS.md) S-1 |
| SEC-2 | No secrets in config files | S-2 |
| SEC-3 | No secrets in log output | S-6 |
| SEC-4 | Input validation on user-facing functions | PI-1 |
| SEC-5 | Permission checks on sensitive operations | RBAC |
| SEC-6 | Error messages don't leak internals | Secure defaults |
| SEC-7 | Dependencies are from trusted sources | Supply chain |
| SEC-8 | No hardcoded URLs to external services | Configuration |

### 5.2 High-Risk Changes

Changes that require additional security review:

- Authentication/authorization changes
- File I/O operations
- Network requests
- Configuration file modifications
- Template rendering with user input
- Memory storage operations

---

## 6 Performance Review

### 6.1 Checklist

| # | Check | Guideline |
|---|-------|-----------|
| PERF-1 | No N+1 queries | Database access patterns |
| PERF-2 | No unnecessary computations | Caching where appropriate |
| PERF-3 | Memory usage is reasonable | No unbounded growth |
| PERF-4 | File I/O is efficient | Use streaming for large files |
| PERF-5 | No blocking operations in async code | Async/sync consistency |

### 6.2 Current Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Config load time | <1s | `time python -c "from ai_company.config import load_config; load_config()"` |
| Agent generation | <5s | Time to generate all 31 agents |
| Test suite | <60s | `time pytest` |
| CLI response | <2s | Manual timing |

---

## 7 Maintainability Review

### 7.1 Checklist

| # | Check | Guideline |
|---|-------|-----------|
| MAINT-1 | Module length <500 lines | Readability |
| MAINT-2 | Function length <50 lines | Readability |
| MAINT-3 | Class length <200 lines | Readability |
| MAINT-4 | No code duplication | DRY principle |
| MAINT-5 | Clear naming conventions | [04-CODING-STANDARDS.md](04-CODING-STANDARDS.md) |
| MAINT-6 | Dependencies are minimal | Reduce coupling |
| MAINT-7 | Public API is documented | API documentation |

---

## 8 Readability Review

### 8.1 Checklist

| # | Check | Guideline |
|---|-------|-----------|
| READ-1 | Code reads like prose | Variable names are descriptive |
| READ-2 | Comments explain why, not what | Inline comments |
| READ-3 | No magic numbers | Named constants |
| READ-4 | Consistent formatting | ruff + black |
| READ-5 | Logical flow is clear | Function organization |

---

## 9 Technical Debt Review

### 9.1 Checklist

| # | Check | Guideline |
|---|-------|-----------|
| DEBT-1 | No workarounds without TODO | Document debt |
| DEBT-2 | No known issues without tracking | Add to TECH_DEBT.md |
| DEBT-3 | No deprecated APIs without migration plan | Track deprecation |
| DEBT-4 | No skipped tests without justification | Document why |

### 9.2 Tech Debt Classification

| Class | Description | Action |
|-------|------------|--------|
| Critical | Security risk or data loss potential | Fix immediately |
| High | Significant impact on development velocity | Fix within sprint |
| Medium | Minor inconvenience, workaround exists | Fix within quarter |
| Low | Cosmetic or theoretical improvement | Backlog |

---

## 10 Quality Scoring System

### 10.1 Scorecard

Each review assigns a score:

| Score | Meaning |
|-------|---------|
| 5 | Excellent — exceeds standards |
| 4 | Good — meets all standards |
| 3 | Acceptable — meets minimum standards |
| 2 | Needs work — must address before merge |
| 1 | Unacceptable — significant issues |

### 10.2 Scoring Criteria

| Category | Weight | Criteria |
|----------|--------|----------|
| Functionality | 30% | Correctness, edge cases, error handling |
| Code Quality | 25% | Standards compliance, typing, DRY |
| Testing | 25% | Coverage, quality, independence |
| Documentation | 10% | Docstrings, README, ADRs |
| Security | 10% | No vulnerabilities, proper validation |

### 10.3 Merge Criteria

| Score | Decision |
|-------|----------|
| >=4.0 | Approve |
| 3.0-3.9 | Approve with minor comments |
| 2.0-2.9 | Request changes |
| <2.0 | Reject |

---

## 11 Release Readiness Checklist

Before any release:

### 11.1 Code Quality

- [ ] All tests pass (`pytest`)
- [ ] Lint passes (`ruff check src/`)
- [ ] Type check passes (`mypy src/`)
- [ ] No known critical bugs

### 11.2 Documentation

- [ ] README.md is current
- [ ] ARCHITECTURE.md reflects changes
- [ ] STATUS.md is updated
- [ ] CHANGELOG.md includes new version
- [ ] ADRs recorded for architectural decisions

### 11.3 Configuration

- [ ] All config files are valid
- [ ] Config changes are documented
- [ ] Breaking changes are flagged

### 11.4 Security

- [ ] No secrets in source
- [ ] Dependencies scanned
- [ ] Security review completed

### 11.5 Operations

- [ ] CLI commands verified
- [ ] Agent generation verified
- [ ] Bootstrap process verified

---

## 12 Review Process

### 12.1 Steps

1. **Self-review**: Reviewer reads own code before submitting
2. **Automated checks**: CI runs lint, type check, tests
3. **Manual review**: Reviewer checks against checklists
4. **Discussion**: Reviewer and author discuss issues
5. **Resolution**: Issues addressed or documented
6. **Approval**: Reviewer approves with score
7. **Merge**: Change merged to main

### 12.2 Review Turnaround

| Priority | Target Turnaround |
|----------|------------------|
| Critical (security, data loss) | <4 hours |
| High (blocks other work) | <24 hours |
| Medium (normal PR) | <48 hours |
| Low (improvement, refactor) | <1 week |

---

## 13 Examples

### 13.1 Good Review Comment

```markdown
## Functionality (5/5)
The decision evaluation logic correctly handles all risk levels.

## Code Quality (4/5)
- Type annotations are complete
- Docstrings are clear

**Suggestion**: Consider extracting `_assess_risk_keywords` into a
separate method for testability.

## Testing (4/5)
Good coverage of the main paths. Consider adding a test for the
edge case where the risk matrix is empty.

## Score: 4.2/5 — Approve with minor comments
```

### 13.2 Bad Review Comment

```markdown
Looks good to me! +1
```

(Not actionable, doesn't verify standards compliance)

---

## 14 Best Practices

1. **Review against standards**: Use the checklists, don't eyeball it.
2. **Be constructive**: Suggest solutions, not just problems.
3. **Review in small batches**: Smaller PRs are easier to review.
4. **Automate what you can**: Lint, type check, tests are automated.
5. **Ask questions**: If something is unclear, ask.
6. **Prioritize issues**: Critical issues first, nits last.

---

## 15 Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| Rubber-stamp approvals | Defeats purpose of review | Review against checklists |
| Reviewing too much at once | Fatigue reduces quality | Keep PRs small |
| Not running tests locally | CI catches issues too late | Run tests before submitting |
| Blocking on nits | Slows down development | Distinguish critical vs. cosmetic |
| Not reviewing generated code | Generated code has bugs too | Review generator logic |

---

## 16 Future Enhancements

- Automated code review scoring
- Review assignment automation
- Review metrics tracking
- Security scanning in CI
- Performance regression detection
- Architecture fitness functions

---

## 17 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | Supreme authority |
| [04-CODING-STANDARDS.md](04-CODING-STANDARDS.md) | Standards being reviewed |
| [08-TESTING-STANDARDS.md](08-TESTING-STANDARDS.md) | Testing standards for review |
| [13-SECURITY-STANDARDS.md](13-SECURITY-STANDARDS.md) | Security review criteria |
| [10-DEFINITION-OF-DONE.md](10-DEFINITION-OF-DONE.md) | Completion criteria |
