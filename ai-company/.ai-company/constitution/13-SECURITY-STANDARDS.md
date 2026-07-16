# AI Company Builder — Security Standards

> **Authority Level**: Layer 4 — derived from [02-ARCHITECTURE.md](02-ARCHITECTURE.md)
> **Immutable Rule Reference**: IR-6 (No secrets in source code), IR-8 (Human approval for production)
> **Last Updated**: 2026-07-16

---

## 1 Purpose

This document defines the security standards for AI Company Builder. Security is not a feature — it is a requirement. Every component must be designed, implemented, and reviewed with security as a primary concern.

---

## 2 Scope

This document covers:

- Secrets management
- Authentication and authorization
- Role-based access control (RBAC)
- Prompt injection prevention
- Dependency scanning
- Supply chain security
- Configuration validation
- Sensitive data handling
- Secure defaults

---

## 3 Secrets Management

### 3.1 Rules

| # | Rule | Enforcement |
|---|------|------------|
| S-1 | Never commit secrets to source code | CI pre-commit hook |
| S-2 | Never commit secrets to YAML config | CI pre-commit hook |
| S-3 | Use environment variables for secrets | Code review |
| S-4 | Use `.env` files for local development (never commit) | `.gitignore` |
| S-5 | Rotate secrets regularly | Operational procedure |
| S-6 | Log secrets as `[REDACTED]` | Code review |

### 3.2 Environment Variables

| Variable | Purpose | Committed? |
|----------|---------|-----------|
| `OPENAI_API_KEY` | OpenAI API access | No |
| `OLLAMA_BASE_URL` | Ollama server URL | No (default is localhost) |
| `AI_COMPANY_CONFIG_DIR` | Config directory override | No |

### 3.3 .gitignore

The `.gitignore` must include:

```
.env
.env.*
*.key
*.pem
*.secret
config/secrets/
```

### 3.4 Examples

```python
# Good: Load from environment
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ConfigError("OPENAI_API_KEY not set")

# Bad: Hardcoded secret
api_key = "sk-1234567890abcdef"  # NEVER DO THIS

# Bad: Secret in config file
# config/company/api.yaml
# openai_key: "sk-1234567890abcdef"  # NEVER DO THIS
```

---

## 4 Authentication

### 4.1 LLM Provider Authentication

| Provider | Auth Method | Storage |
|----------|------------|---------|
| OpenAI | API key | `OPENAI_API_KEY` env var |
| Ollama | None (local) | N/A |

### 4.2 CLI Authentication

The CLI is local-only. No remote authentication is required for the current version.

### 4.3 Dashboard Authentication

The FastAPI dashboard is local-only. For future remote access:

| Level | Implementation |
|-------|---------------|
| Current | No auth (localhost only) |
| Future | API key in header |
| Enterprise | OAuth2 / SSO |

---

## 5 Authorization

### 5.1 Agent Authorization

Each agent has explicit permissions defined in YAML config:

```yaml
# config/agents/specialists.yaml
specialists:
  - id: lead_backend
    permissions:
      - "read:config"
      - "write:code"
      - "execute:tests"
    restrictions:
      - "No production deployments without approval"
      - "No access to financial data"
```

### 5.2 Permission Categories

| Category | Description | Examples |
|----------|------------|---------|
| `read:*` | Read access | `read:config`, `read:code`, `read:memory` |
| `write:*` | Write access | `write:code`, `write:config`, `write:memory` |
| `execute:*` | Execution access | `execute:tests`, `execute:deploy`, `execute:workflow` |
| `admin:*` | Administrative access | `admin:agents`, `admin:config`, `admin:security` |

### 5.3 Authorization Rules

| Rule | Description |
|------|------------|
| Default deny | Agents have no permissions unless explicitly granted |
| Least privilege | Grant only the minimum permissions needed |
| Separation of duties | No agent can both create and approve |
| Audit trail | All permission checks are logged |

---

## 6 Role-Based Access Control (RBAC)

### 6.1 Role Hierarchy

```
CEO
├── Chief of Staff
│   ├── Executives (CTO, CFO, COO, CMO, CPO, CAIO)
│   │   ├── Departments (Engineering, Product, Marketing, etc.)
│   │   │   └── Specialists (Lead Backend, Lead Frontend, etc.)
│   │   └── Specialists (domain-specific)
│   └── Board Members (advisory, voting)
└── Security Engineer (cross-cutting)
```

### 6.2 Permission Matrix

| Role | Read Config | Write Config | Execute Tests | Deploy | Admin |
|------|------------|-------------|---------------|--------|-------|
| CEO | Yes | Yes | Yes | Yes | Yes |
| Chief of Staff | Yes | Yes | Yes | Yes | Yes |
| Executive | Yes | Limited | Yes | Limited | Limited |
| Department Head | Yes | No | Yes | No | No |
| Specialist | Yes | No | Yes | No | No |
| Board Member | Yes (read-only) | No | No | No | No |

### 6.3 Implementation

RBAC is enforced through:

1. **Config-level**: Permissions defined in YAML config files
2. **Agent-level**: Each agent template includes `permission:` blocks
3. **Engine-level**: Engines check permissions before executing actions
4. **CLI-level**: CLI commands check permissions before execution

---

## 7 Prompt Injection Prevention

### 7.1 Threat Model

| Attack Vector | Description | Mitigation |
|--------------|-------------|-----------|
| Direct injection | User input embedded in prompts | Input sanitization |
| Indirect injection | External data contains malicious prompts | Data validation |
| Role confusion | Agent manipulated to act outside role | Role enforcement |
| Data exfiltration | Agent tricked into leaking data | Permission enforcement |

### 7.2 Prevention Rules

| # | Rule | Implementation |
|---|------|---------------|
| PI-1 | Sanitize all user input before embedding in prompts | Input validation in CLI |
| PI-2 | Never embed raw external data in system prompts | Data transformation layer |
| PI-3 | Enforce agent role boundaries at engine level | Permission checks |
| PI-4 | Log all prompt inputs for audit | Structured logging |
| PI-5 | Limit prompt length to prevent abuse | CLI input validation |

### 7.3 Agent Prompt Safety

Each agent prompt includes explicit boundaries:

```markdown
## Restrictions
- You may NOT access financial data
- You may NOT deploy to production
- You may NOT modify other agents
- You must escalate decisions above your authority
```

---

## 8 Dependency Scanning

### 8.1 Current State

| Tool | Status | Purpose |
|------|--------|---------|
| `pip audit` | Manual | Vulnerability scanning |
| Dependabot | Not configured | Automated updates |
| Safety | Not configured | Dependency checking |

### 8.2 Recommended Setup

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/ai-company"
    schedule:
      interval: "weekly"
```

### 8.3 Dependency Rules

| Rule | Rationale |
|------|-----------|
| Review new dependencies before adding | Supply chain security |
| Prefer well-maintained packages | Reduce vulnerability exposure |
| Pin minimum versions only | Let pip resolve compatible versions |
| Run `pip audit` periodically | Catch known vulnerabilities |
| Remove unused dependencies | Reduce attack surface |

---

## 9 Supply Chain Security

### 9.1 Risks

| Risk | Mitigation |
|------|-----------|
| Malicious package | Review package source, maintainers, downloads |
| Typosquatting | Verify package names carefully |
| Dependency confusion | Use private package index for internal packages |
| Build poisoning | Pin build tools, use verified sources |

### 9.2 Best Practices

1. **Verify package integrity**: Check package hashes
2. **Review package source**: Ensure package is from trusted source
3. **Minimize dependencies**: Fewer deps = smaller attack surface
4. **Update regularly**: Stay current with security patches
5. **Audit periodically**: Run `pip audit` monthly

---

## 10 Configuration Validation

### 10.1 Validation at Load Time

All configuration is validated when loaded:

```python
# registry/validator.py validates:
- Company name exists
- At least one executive defined
- At least one department defined
- Board members defined
- Approval matrix has entries
- Risk matrix has entries
- Budget values are positive
```

### 10.2 Validation Rules

| Rule | Rationale |
|------|-----------|
| Fail fast on invalid config | Prevent partial initialization |
| Validate types and ranges | Prevent runtime errors |
| Reject unknown fields (future) | Prevent configuration pollution |
| Log validation failures | Audit trail |

### 10.3 Configuration Integrity

```python
# Config files are loaded in fixed order
FILE_MAP = {
    "company/company.yaml": "company",
    "company/vision.yaml": "vision",
    # ... 19 files total
}

# Each file is validated against expected schema
# Missing files raise ConfigError
# Invalid files raise ConfigError with specific field errors
```

---

## 11 Sensitive Data Handling

### 11.1 Classification

| Classification | Examples | Handling |
|---------------|---------|---------|
| Public | Agent names, org chart | No restrictions |
| Internal | Config files, workflows | Version control OK, no external sharing |
| Confidential | API keys, tokens | Environment variables only |
| Restricted | User PII | Encrypt at rest, limit access |

### 11.2 Logging Rules

| Data Type | Log As | Example |
|-----------|--------|---------|
| API keys | `[REDACTED]` | `Using API key: [REDACTED]` |
| User input | Truncated to 100 chars | `User input: "Add a new..."` |
| File paths | Full path | `Loading config: config/company/company.yaml` |
| Errors | Full detail (no secrets) | `ConfigError: Invalid YAML at line 5` |

---

## 12 Secure Defaults

### 12.1 Default Security Posture

| Setting | Default | Rationale |
|---------|---------|-----------|
| Agent permissions | None | Default deny |
| API access | Disabled | Explicit enable required |
| Remote access | Disabled | Localhost only |
| Debug mode | Off | No info leakage |
| Logging level | INFO | No verbose output in production |
| Error messages | Generic | Don't leak internal details |

### 12.2 Secure by Design

```python
# Good: Secure default
class Agent:
    permissions: list[str] = Field(default_factory=list)  # No permissions by default
    restrictions: list[str] = Field(default_factory=list)  # No restrictions needed

# Bad: Insecure default
class Agent:
    permissions: list[str] = ["read:*", "write:*", "execute:*"]  # Everything!
```

---

## 13 Security Review Checklist

Before any code change, verify:

- [ ] No secrets in source code or config files
- [ ] No secrets in log output
- [ ] Input validation on all user-facing functions
- [ ] Permission checks on all sensitive operations
- [ ] Error messages don't leak internal details
- [ ] Dependencies are from trusted sources
- [ ] New dependencies reviewed for vulnerabilities
- [ ] No hardcoded URLs pointing to external services
- [ ] Configuration validated at load time
- [ ] Audit trail for security-relevant operations

---

## 14 Future Enhancements

- Dependabot configuration for automated dependency updates
- `pip audit` integration in CI
- Pre-commit hooks for secret detection (e.g., `detect-secrets`)
- RBAC enforcement in engine layer
- Prompt injection testing framework
- Security scanning in CI pipeline
- Encrypted configuration for sensitive values
- Audit logging to persistent storage

---

## 15 References

| Document | Relationship |
|----------|-------------|
| [00-CONSTITUTION.md](00-CONSTITUTION.md) | IR-6 (No secrets), IR-8 (Human approval) |
| [03-ENGINEERING-STANDARDS.md](03-ENGINEERING-STANDARDS.md) | Error handling patterns |
| [09-CODE-REVIEW.md](09-CODE-REVIEW.md) | Security review checklist |
| [07-PROMPT-STANDARDS.md](07-PROMPT-STANDARDS.md) | Prompt safety rules |
| [pyproject.toml](../../pyproject.toml) | Dependency declarations |
