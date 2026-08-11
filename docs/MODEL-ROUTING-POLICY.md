# Model Routing Policy — Light Speed Holdings

> Last updated: 2026-07-17

## Overview

The ModelRouter (`src/ai_company/model_router.py`) selects which LLM provider and model to use for each agent task. Routing is cost-aware: simple tasks use cheap models, critical decisions use the best available.

## Provider Catalog

| Provider | Backend | Default Model | API Base | Env Var |
|----------|---------|---------------|----------|---------|
| opencode | openai_compatible | big-pickle | https://opencode.ai/api/v1 | OPENCODE_API_KEY |
| deepseek | openai_compatible | deepseek-chat | https://api.deepseek.com/v1 | DEEPSEEK_API_KEY |
| ollama | ollama | llama3.1:8b | http://localhost:11434 | (none) |
| openai | openai_compatible | gpt-4o-mini | https://api.openai.com/v1 | OPENAI_API_KEY |
| anthropic | openai_compatible | claude-sonnet-4-20250514 | https://api.anthropic.com | ANTHROPIC_API_KEY |

## Tiers

| Tier | Description | Providers (fallback order) |
|------|-------------|---------------------------|
| fast | Low-latency, low-cost. Read-only and simple tasks. | opencode/big-pickle -> ollama/llama3.1:8b |
| standard | Balanced capability and cost. Default for most agents. | deepseek/deepseek-chat -> opencode/big-pickle |
| premium | Maximum reasoning. Critical decisions and approvals. | deepseek/deepseek-coder -> opencode/big-pickle |

## Routing Rules

Routing is resolved in this priority order:

1. **Per-agent override** — agent-registry.json `"model"` field (e.g., `"anthropic/claude-opus-4-20250514"`)
2. **Context rules** — `escalation` and `approval` contexts always resolve to `premium`
3. **Agent type + priority rules** — see table below
4. **Fallback** — defaults to `standard` tier

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

## Cost Control

- Board advisors always use `fast` tier (cheapest model)
- Routine executive/specialist work uses `standard` tier
- Only high/critical priority tasks and escalation/approval contexts trigger `premium`
- Per-agent overrides in the registry take highest priority (e.g., CTO locked to anthropic/claude-opus)
- Monthly budget reviewed by CFO; alerts at 80% and 95% of ceiling

## Fallback Behavior

When the primary provider in a tier is unavailable:
1. ModelRouter returns the tier's first provider
2. LLMClient iterates through the tier's provider chain on failure
3. If all providers in the tier fail, the task is marked `failed` in the inbox
4. LLMClient retries bad-JSON responses up to 5 times before giving up

## Configuration

- **models.yaml**: `company/models.yaml` — defines providers, tiers, and routing rules
- **agent-registry.json**: `company/agent-registry.json` — per-agent model overrides
- **opencode.json**: `.opencode/opencode.json` — registers providers for the OpenCode runtime
