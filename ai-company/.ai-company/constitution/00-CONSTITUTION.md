# AI Company Builder — Constitution

> **Authority Level**: Supreme. This document overrides all other governance documents.
> **Supersedes**: `docs/COMPANY-CONSTITUTION.md`
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This Constitution is the highest-authority governance document for the AI Company Builder repository. Every agent, every engine, every template, every test, and every human contributor operates under its authority. No code, no configuration, no documentation may contradict this Constitution.

---

## 2 Scope

This Constitution governs:

- All source code in `src/ai_company/`
- All configuration in `config/`
- All templates in `templates/`
- All tests in `tests/`
- All generated output in `.opencode/`
- All documentation in `docs/` and `.ai-company/`
- All CI/CD pipelines in `.github/workflows/`
- All harness lifecycle operations in `harness/`
- All AI agent behavior when operating within this repository

---

## 3 Mission

Build the definitive Infrastructure-as-Code platform for creating, orchestrating, and governing AI-native organizations. Every company the platform creates should be as well-governed, auditable, and autonomous as a human-run enterprise — but faster, more consistent, and fully transparent.

---

## 4 Core Principles

### 4.1 Configuration Is the Source of Truth

All company structure, agent definitions, workflows, governance rules, and policies live in YAML configuration files. The `config/` directory is the single source of truth. Generated code, generated agents, and generated documentation are derived artifacts — never the source.

```
YAML Config (source)  →  Generator (engine)  →  Markdown/YAML (derived)
```

**Implication**: Editing a generated `.md` agent file is always wrong. Edit the YAML config, then regenerate.

### 4.2 Generated Code Is disposable

All generated artifacts (`.opencode/agents/*.md`, `company/*.yaml`, memory structures, workflow files) may be deleted and regenerated from the source configuration at any time. No generated artifact carries state that cannot be reconstructed from config.

**Implication**: Never hand-edit generated files. Never store irreplaceable state in generated output.

### 4.3 Infrastructure as Code

The entire company — its hierarchy, policies, workflows, decision rights, and knowledge — is defined as code. This means:

- Version-controlled (git)
- Testable (pytest)
- Auditable (change history)
- Reproducible (deterministic generation)
- Reviewable (PR-based workflow)

**Implication**: Every change to company structure goes through the same engineering discipline as application code.

### 4.4 AI Agents Are Employees

AI agents created by this platform are treated as organizational employees with:

- Defined roles and responsibilities
- Explicit decision rights and restrictions
- Clear reporting hierarchies
- Measurable performance metrics
- Escalation procedures
- Accountability for outputs

**Implication**: Agents must never operate outside their defined scope. Ambiguity in agent capability is a bug.

### 4.5 Human Authority Is Supreme

The human CEO retains final authority over all decisions. AI agents escalate to humans when:

- A decision exceeds their defined authority
- A risk exceeds acceptable thresholds
- A novel situation not covered by policy arises
- The stakeholder explicitly requests human review

**Implication**: No autonomous action may permanently alter the organization without human approval.

### 4.6 Simplicity Before Complexity

Every design choice defaults to the simpler solution. Complexity is introduced only when:

- The simpler solution demonstrably fails
- The complexity is justified by measurable benefit
- The complexity is documented and testable

**Implication**: Reject clever code. Prefer readable code. Complexity is a cost, not a feature.

### 4.7 Transparency Over Opacity

All system behavior must be observable, debuggable, and explainable. This means:

- Structured logging over print statements
- Explicit error messages over silent failures
- Audit trails over undocumented actions
- Configuration over convention when behavior differs

**Implication**: If you cannot explain why the system did something, the system is broken.

### 4.8 Quality Before Speed

Working software that is buggy, untested, or undocumented is not working software. The Definition of Done (see [10-DEFINITION-OF-DONE.md](10-DEFINITION-OF-DONE.md)) must be satisfied before any change is considered complete.

**Implication**: Skipping tests to ship faster is never acceptable.

---

## 5 Immutable Rules

These rules cannot be changed by any process, any engine, or any agent. They require explicit human approval to modify.

| # | Rule | Rationale |
|---|------|-----------|
| IR-1 | All company definitions must originate from YAML configuration | Configuration is source of truth |
| IR-2 | Generated files must never be hand-edited | Regeneration would overwrite edits |
| IR-3 | All new code must have corresponding tests | Quality before speed |
| IR-4 | All public APIs must have type annotations | Type safety prevents runtime errors |
| IR-5 | All configuration files must be validated on load | Fail fast, fail loud |
| IR-6 | No secrets may appear in source code or config | Security by design |
| IR-7 | All agent actions must be scoped to defined responsibilities | Accountability requires boundaries |
| IR-8 | Human approval is required for production deployments | Human authority is supreme |
| IR-9 | All architectural decisions must be recorded as ADRs | Decisions must be traceable |
| IR-10 | The Constitution cannot be modified by AI agents alone | Highest authority requires human consent |

---

## 6 Repository Philosophy

### 6.1 The Repository Is the Organization

The repository contains the complete definition of the AI company. It is not merely a codebase — it is the organization's DNA. Every folder, every config file, every template encodes organizational knowledge.

### 6.2 Version History Is Organizational Memory

Git history captures not just code changes but organizational decisions, pivots, and evolution. Commit messages should be written with this understanding — they are the permanent record of why things changed.

### 6.3 Everything Is Auditable

Every change to the repository is tracked. Every generated artifact can be traced back to its source configuration. Every decision can be linked to the ADR that justified it.

---

## 7 Governance Hierarchy

```
This Constitution (00-CONSTITUTION.md)
    │
    ├── Mission (01-MISSION.md)
    ├── Design Principles (14-DESIGN-PRINCIPLES.md)
    ├── AI Company Vision (15-AI-COMPANY-VISION.md)
    │
    ├── Architecture (02-ARCHITECTURE.md)
    │   ├── Engineering Standards (03-ENGINEERING-STANDARDS.md)
    │   ├── Coding Standards (04-CODING-STANDARDS.md)
    │   ├── Project Structure (05-PROJECT-STRUCTURE.md)
    │   └── Security Standards (13-SECURITY-STANDARDS.md)
    │
    ├── Generator Standards (06-GENERATOR-STANDARDS.md)
    ├── Prompt Standards (07-PROMPT-STANDARDS.md)
    ├── Testing Standards (08-TESTING-STANDARDS.md)
    ├── Code Review (09-CODE-REVIEW.md)
    ├── Definition of Done (10-DEFINITION-OF-DONE.md)
    ├── Git Standards (11-GIT-STANDARDS.md)
    └── Documentation Standards (12-DOCUMENTATION-STANDARDS.md)
```

When documents conflict, the higher-level document wins. This Constitution wins over everything.

---

## 8 What Is Prohibited

| # | Prohibition | Reason |
|---|-------------|--------|
| P-1 | Editing generated `.md` agent files by hand | Configuration is source of truth |
| P-2 | Storing secrets in source code or YAML config | Security |
| P-3 | Committing without running linter and tests | Quality |
| P-4 | Deploying without human approval | Human authority |
| P-5 | Adding dependencies without security review | Supply chain security |
| P-6 | Bypassing the ECL change lifecycle for significant work | Audit trail |
| P-7 | Creating agents without defined responsibilities | Accountability |
| P-8 | Making architectural decisions without recording an ADR | Traceability |
| P-9 | Suppressing lint or type errors to pass CI | Quality |
| P-10 | Modifying this Constitution without human approval | Supreme authority |

---

## 9 Examples

### 9.1 Correct Workflow

```
1. Developer identifies need for new agent type
2. Adds agent definition to config/agents/specialists.yaml
3. Updates templates/specialist_v2.md.j2 if template changes needed
4. Runs generator: python -c "from ai_company.generator import AgentGenerator; ..."
5. Verifies generated .opencode/agents/*.md looks correct
6. Runs tests: pytest
7. Runs lint: ruff check src/ && mypy src/
8. Creates PR with ADR if architectural change
9. Human reviews and merges
```

### 9.2 Incorrect Workflow (Violates Constitution)

```
1. Developer manually edits .opencode/agents/lead-backend.md  [VIOLATES IR-2, P-1]
2. Adds hardcoded API key to config/company/company.yaml  [VIOLATES IR-6, P-2]
3. Commits without running tests  [VIOLATES IR-3, P-3]
4. Deploys to production without review  [VIOLATES IR-8, P-4]
```

---

## 10 Engineering Ethics

All contributors — human and AI — adhere to these ethical principles:

1. **Do No Harm**: Never introduce changes that could cause data loss, security breaches, or system outages.
2. **Be Honest**: Report failures, limitations, and risks truthfully. Never mask problems.
3. **Respect Boundaries**: Operate only within defined scope. Escalate when uncertain.
4. **Protect Privacy**: Never expose personal data, secrets, or confidential information.
5. **Seek Review**: When in doubt, ask. When the change is significant, require review.
6. **Document Decisions**: Future contributors deserve to understand why choices were made.
7. **Continuously Improve**: Every incident, every review, every failure is an opportunity to improve.

---

## 11 Decision Hierarchy

When multiple authorities conflict:

```
1. Human CEO directive          (overrides everything)
2. This Constitution            (supreme governance)
3. ADRs (Architectural Decisions) (recorded decisions)
4. ECL Change Constraints       (active work scope)
5. AGENTS.md                   (session guidance)
6. docs/STATUS.md              (current state)
7. Inline code comments        (immediate context)
```

---

## 12 Definition of Repository Ownership

| Area | Owner | Deputies |
|------|-------|----------|
| Constitution | Human CEO | Chief of Staff (AI) |
| Architecture | Human CEO | CTO (AI), Software Architect (AI) |
| Source Code | Human CEO | Lead Backend (AI), Lead Frontend (AI) |
| Configuration | Human CEO | COO (AI), Chief of Staff (AI) |
| Tests | Human CEO | QA Engineer (AI) |
| Documentation | Human CEO | CPO (AI) |
| Security | Human CEO | Security Engineer (AI) |
| CI/CD | Human CEO | DevOps Lead (AI) |
| Agent Design | Human CEO | CTO (AI), CAIO (AI) |

---

## 13 Future Enhancements

- Formal governance approval workflow for Constitution amendments
- Automated Constitution compliance checking in CI
- Versioned Constitution with semantic versioning
- Constitution diff tooling for change review
- Integration with ECL change lifecycle for amendment tracking

---

## 14 References

| Document | Relationship |
|----------|-------------|
| [01-MISSION.md](01-MISSION.md) | Strategic objectives derived from this Constitution |
| [02-ARCHITECTURE.md](02-ARCHITECTURE.md) | Technical implementation of these principles |
| [10-DEFINITION-OF-DONE.md](10-DEFINITION-OF-DONE.md) | Completion criteria enforced by this Constitution |
| [14-DESIGN-PRINCIPLES.md](14-DESIGN-PRINCIPLES.md) | Design philosophy implementing these principles |
| [15-AI-COMPANY-VISION.md](15-AI-COMPANY-VISION.md) | Long-term vision enabled by this Constitution |
| [bootstrap.md](bootstrap.md) | Session startup procedure derived from this Constitution |
| [docs/ECL.md](../../docs/ECL.md) | Change lifecycle governed by this Constitution |
| [AGENTS.md](../../AGENTS.md) | Agent operating procedures under this Constitution |
