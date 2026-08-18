# Model Routing Policy — Light Speed Holdings

> Last updated: 2026-08-17

## Overview

The ModelRouter (`src/ai_company/model_router.py`) selects which LLM provider and model to use for each agent task. Routing is cost-aware and cloud-first: Opencode free models are the default tier, with token-limit rotation and budget degradation for cost control.

## Provider Catalog

| Provider | Backend | Default Model | API Base | Env Var |
|----------|---------|---------------|----------|---------|
| opencode | openai_compatible | big-pickle | https://opencode.ai/zen/v1 | OPENCODE_API_KEY |
| deepseek | openai_compatible | deepseek-chat | https://api.deepseek.com/v1 | DEEPSEEK_API_KEY |
| gemini | openai_compatible | gemini-3.5-flash | https://generativelanguage.googleapis.com/v1beta/openai | GEMINI_API_KEY |
| ollama | ollama | llama3.1:8b | http://localhost:11434 | (none) |
| openai | openai_compatible | gpt-4o-mini | https://api.openai.com/v1 | OPENAI_API_KEY |
| anthropic | openai_compatible | claude-sonnet-4-20250514 | https://api.anthropic.com | ANTHROPIC_API_KEY |

## Tiers

| Tier | Description | Providers (fallback order) |
|------|-------------|---------------------------|
| free | Zero-cost tier using dynamic Opencode free models + Ollama fallback | Dynamic catalog (see below) |
| fast | Low-latency, low-cost. Read-only and simple tasks. | llamacpp/mistral-7b-32k -> ollama/mistral-7b-32k -> gemini/3.5-flash |
| standard | Balanced capability and cost. Default for most agents. | llamacpp/llama3.1-8b-32k -> opencode/big-pickle -> ollama/llama3.1:8b -> gemini/3.5-flash |
| premium | Maximum reasoning. Critical decisions and approvals. | llamacpp/deepseek-r1-64k -> llamacpp/gemma2-9b-q5 -> opencode/big-pickle -> ollama/llama3.1:8b |

## Free Tier (Dynamic Catalog)

The free tier fetches models from the Opencode Zen API (`https://opencode.ai/zen/v1/models`), filtering for truly free models (cost = $0). Models are sorted by context window size (largest first) and cached for 1 hour.

Known free models include: Big Pickle (200K), GPT-5 Nano (128K), Kimi K2.5 Free (262K), Qwen 3.6 Plus Free (262K), Nemotron 3 Ultra Free (200K), DeepSeek V4 Flash Free (200K), and 10+ others.

If the API is unavailable, the system falls back to a static list of known free models, then to Ollama.

## Routing Rules

Routing is resolved in this priority order:

1. **Per-agent override** — agent-registry.json `"model"` field (e.g., `"anthropic/claude-opus-4-20250514"`)
2. **Context rules** — `escalation` and `approval` contexts always resolve to `premium`
3. **Domain-aware detection** — task prompt keywords detect domain (security, finance, etc.)
4. **Agent type + priority rules** — see table below
5. **Fallback** — defaults to `standard` tier

### Agent Type Routing

| Agent Type | Priority: low | Priority: medium | Priority: high | Priority: critical |
|------------|---------------|------------------|----------------|-------------------|
| Board | fast | fast | fast | fast |
| Executive | standard | standard | premium | premium |
| Specialist | standard | standard | premium | premium |

### Context Overrides

| Context | Tier |
|---------|------|
| escalation | premium |
| approval | premium |
| domain_code_review | premium |
| domain_security | premium |
| domain_legal | premium |
| domain_data_science | premium |
| domain_deployment | standard |
| domain_finance | standard |

### Task-Type Routing

Task types are detected from the task prompt and mapped to optimal tiers. Simple tasks route to `free`, complex tasks to `standard` or `premium`.

| Task Type | Tier | Detection Heuristic |
|-----------|------|---------------------|
| read_only | free | "read", "show", "display", "list", "cat" |
| single_file_edit | free | "edit", "modify", "update", "change" |
| simple_command | free | "run", "execute", "build", "test" |
| boilerplate | free | "scaffold", "template", "generate" |
| code_review | standard | "review", "audit", "check", "lint" |
| debugging | standard | "fix", "bug", "error", "debug" |
| refactor | standard | "refactor", "reorganize", "clean up" |
| integration | standard | "integrate", "connect", "wire" |
| architecture | premium | "architecture", "design", "system design" |
| planning | premium | "plan", "strategy", "roadmap" |
| security | premium | "security", "vulnerability", "auth" |
| performance | premium | "optimize", "performance", "speed up" |

## Token-Limit Rotation

When a provider returns a token/context limit error, the system automatically rotates through free models by context window size (largest first), then escalates through tiers (standard → premium).

**Error patterns detected:**
- "context length", "max_tokens", "token limit", "too many tokens"
- "exceeds maximum", "context window", "input too long", "prompt too long"

**Rotation strategy:**
1. Find current model in the free catalog
2. Rotate to next free model with larger context window
3. If no larger free model exists, rotate to next tier (standard → premium)
4. Maximum 3 rotations before giving up

## Budget Degradation

When daily budget pressure exceeds configured thresholds, the system forces cheaper tiers for non-critical tasks.

| Pressure | Action | Notes |
|----------|--------|-------|
| 0%–80% | No change | Normal operation |
| 80%–90% | Warning | Prefer cheaper tier (don't force) |
| 90%–95% | Force fast tier | Non-critical tasks only |
| 95%–100% | Force free tier | Non-critical tasks only |
| 100%+ | Hard stop | Executor auto-suspends |

**Critical tasks bypass all degradation thresholds.**

Configuration in `company/models.yaml`:
```yaml
budget_degradation:
  enabled: true
  warning_threshold: 0.80
  pressure_threshold: 0.90
  critical_threshold: 0.95
  hard_stop_threshold: 1.00
```

## Cost Control

- **Free tier is the default** for new agents (not standard)
- Board advisors always use `fast` tier (cheapest model)
- Simple tasks (read, edit, grep) route to `free` tier automatically
- Routine executive/specialist work uses `standard` tier
- Only high/critical priority tasks and escalation/approval contexts trigger `premium`
- Per-agent overrides in the registry take highest priority (e.g., CTO locked to anthropic/claude-opus)
- Token-limit errors trigger automatic rotation (no manual intervention)
- Budget pressure triggers automatic degradation (preserves critical task capability)

## Fallback Behavior

When the primary provider in a tier is unavailable:
1. ModelRouter returns the tier's first provider
2. LLMClient iterates through the tier's provider chain on failure
3. If all providers in the tier fail, the task is marked `failed` in the inbox
4. LLMClient retries bad-JSON responses up to 5 times before giving up
5. Token-limit errors trigger rotation to a larger-context model or next tier

## Configuration

- **models.yaml**: `company/models.yaml` — defines providers, tiers, routing rules, task-type routing, free tier, token-limit rotation, budget degradation
- **agent-registry.json**: `company/agent-registry.json` — per-agent model overrides
- **opencode.json**: `.opencode/opencode.json` — registers providers for the OpenCode runtime
