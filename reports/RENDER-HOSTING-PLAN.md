# RENDER-HOSTING-PLAN

## Team Composition (Agents/Sub-Agents)

Based on `company-registry.yaml` and project architecture, the following agents/sub-agents are relevant:

### Rendering Team (from registry)

| Agent ID | Type | Role | Tools |
|----------|------|------|-------|
| `chief_of_staff` | executive | Orchestrates generation pipeline, coordinates agent communication | read, write, execute, delegate |
| `cto` | executive | Oversees rendering infrastructure, platform reliability | read, write, execute |
| `devops_lead` | specialist | CI/CD pipelines, deployment automation, infrastructure-as-code | read, write, execute, grep, list |
| `platform_reliability_engineer` | specialist | Concurrency safety, DLQ hardening, circuit breaker robustness | read, write, execute, grep, list |
| `dashboard_owner` | specialist | Dashboard REST API, KPI collectors, analytics layer | read, write, execute, grep, list |
| `llm_platform_owner` | specialist | Multi-provider LLM client, cost tracker, provider routing | read, write, execute, grep, list |
| `orchestration_owner` | specialist | MessageBus task queue, executor loop lifecycle | read, write, execute, grep, list |
| `security_compliance_lead` | specialist | 5-tier approval rules, CORS lockdown, dashboard auth | read, write, grep, list |

### Hosting/Deployment Team

| Agent ID | Type | Role | Tools |
|----------|------|------|-------|
| `vp_engineering` | executive | Overall engineering velocity, technical domain decisions | read, write, execute |
| `coo` | executive | Operations, resource allocation, workflow optimization | read, write, execute |
| `ci-cd-and-automation` | skill | CI/CD pipeline setup, quality gates, test runner configuration | (skill-based) |
| `ls-creative-director` | skill | Creative brief orchestrator, routes to production skills | (skill-based) |
| `ls-artifact-qa` | skill | QA gatekeeper, visual/brand/UX/accessibility/content validation | (skill-based) |

## Rendering Pipeline Architecture

```
company-registry.yaml  →  AgentGenerator →  Jinja2 Templates  →  .opencode/agents/*.md
                                          ↓
                                    docs/AGENT-REGISTRY-TABLE.md
```

### Step 1: Registry Load
- `AgentGenerator.load_registry()` reads `company-registry.yaml` via `load_yaml_cached()`
- Parses 19 YAML configs into CompanyRegistry model (executives, specialists, departments, board)

### Step 2: Template Selection (`_TEMPLATE_MAP`)
| Agent Type | Template |
|------------|----------|
| executive | `executive.md.j2` |
| department | `department.md.j2` |
| specialist | `specialist.md.j2` |
| board | `board.md.j2` |
| workflow | `workflow.md.j2` |
| config | `config.md.j2` |
| agent | `agents/agent.md.j2` (OpenCode v2) |
| default | `base.md.j2` |

### Step 3: Tool Normalization (`_normalize_tools`)
Registry tool names → OpenCode v2 permission keys:
- `write` → `edit`, `execute` → `bash`, `delegate` → `task`, `web_search` → `webfetch`

### Step 4: Permission Block Generation (`_build_permission`)
```python
keys = sorted({_TOOL_MAP.get(tool, tool) for tool in tools})
return {key: "allow" for key in keys}
```

### Step 5: Template Rendering
Each agent gets rendered with:
- `company` context (from registry: "Light Speed Holdings")
- Agent-specific fields (id, name, title, description, department, tools, permission, etc.)
- PowerShell anti-pattern validation (`_check_anti_patterns`)

### Step 6: Output
- `.md` files written to `.opencode/agents/{id}.md` (underscores → hyphens)
- Shared standards: `operating-standards.md` copied to parent directory
- Registry table: `docs/AGENT-REGISTRY-TABLE.md` regenerated

## Hosting/Deployment Configuration

### Staging Environment (port 8421)
```bash
docker compose -f docker-compose.staging.yml up --build
# Port mapping: host 8421 → container 8420
```

### Production Environment (port 8420)
```bash
docker compose up --build
# Port mapping: host 8420 → container 8420
```

### Dashboard RBAC Keys (priority order)
1. `DASHBOARD_ADMIN_KEY` — full access (also accepts `DASHBOARD_API_KEY`)
2. `DASHBOARD_APPROVE_KEY` — approve/reject tasks
3. `DASHBOARD_RUN_KEY` — execute tasks, read KPIs
4. `DASHBOARD_API_KEY` — legacy single-key mode

### Key Rotation Procedure (every 90 days)
1. Generate new keys for each provider/service
2. Update local `.env` (NEVER commit to git — it's gitignored)
3. Update deployed environments (GitHub Actions secrets, Docker secrets, cloud secret stores: AWS Secrets Manager, GCP Secret Manager, Azure Key Vault)
4. Verify health endpoints respond with new keys:
   - `curl http://<host>:8420/health` (production)
   - `curl http://<host>:8421/health` (staging)
5. Revoke old keys after confirming new ones work across all environments
6. Update `.env.example` placeholders if key format/naming changed
7. Document rotation in CHANGELOG.md

### Verification Commands
```bash
# Local verification
uv run python -c "from dotenv import load_dotenv; load_dotenv(); from ai_company.security.rbac import verify_keys; verify_keys()"

# Staging verification
curl -H "X-API-Key: $DASHBOARD_ADMIN_KEY" http://localhost:8421/health

# Production verification (adjust host/port)
curl -H "X-API-Key: $DASHBOARD_ADMIN_KEY" https://api.example.com/health
```

## Parallel Execution Strategy

Agents can work in parallel with no friction:

| Parallel Group | Agents | Reason |
|----------------|--------|--------|
| **Rendering** | All agent generators | Independent template rendering, no shared state during generation |
| **Tool normalization** | All tool name mappings | Concurrent `_TOOL_MAP` lookups, stateless |
| **Permission blocks** | All agent permission builds | Independent, no cross-agent dependencies |
| **Hosting config** | Staging + production compose | Separate environments, no conflicts |
| **Key rotation** | All key updates | Independent per-provider, no ordering dependency |

## Verification Checklist

- [ ] `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` — generates all agents
- [ ] `ai-company --help` + `ai-company <command> --help` — CLI commands responsive
- [ ] `pytest` — models/orchestrator tests pass
- [ ] `ruff check src/ && mypy src/ && pytest` — full source verification
- [ ] `pwsh scripts/lint-ecl.ps1` — harness/docs linting
- [ ] Generated agent files have valid YAML frontmatter, mode ∈ {primary, subagent}, permission dict valid
- [ ] No PowerShell anti-patterns in generated content
- [ ] Filenames use hyphens, not underscores
- [ ] `docs/AGENT-REGISTRY-TABLE.md` in sync with generated agents

---
*This file was generated as part of the RENDER-HOSTING-PLAN implementation. Plan mode is now complete; execution mode is active.*