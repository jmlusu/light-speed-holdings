# ADR-004: Multi-provider LLM Strategy

**Status:** Accepted
**Date:** 2026-07-17
**Deciders:** CTO, CAIO, CFO
**Technical Domain:** LLM Integration

## Context

AI Company Builder needs LLM access for agent reasoning, but:
- No single provider is optimal for all tasks (cost, capability, speed tradeoffs)
- Provider outages are common — a single provider creates a single point of failure
- Different agents have different capability needs (simple drafts vs. complex reasoning)
- Cost control is critical — LLM API bills can grow quickly without optimization
- Some users may prefer local inference (Ollama) for privacy or cost reasons
- The system should gracefully degrade when a provider is unavailable

## Decision

We implement a **multi-provider LLM strategy** with:
1. A `ModelRouter` that selects providers based on cost tiers
2. Automatic fallback across providers within a tier
3. Per-agent model overrides for specialized needs
4. A `CostTracker` that enforces budget limits

## Architecture

```
ModelRouter
  ├─ agent_override? → use specified model
  ├─ context_rule? → escalation/approval → premium tier
  ├─ agent_type + priority → matched from routing rules
  └─ fallback → default tier

LLMClient
  ├─ try provider[0] → success? return
  ├─ try provider[1] → success? return
  ├─ try provider[2] → success? return
  └─ all failed → raise error
```

## Provider Configuration

```yaml
# company/models.yaml
providers:
  opencode:
    base_url: https://api.opencode.ai/v1
    models: [big-pickle]
  openai:
    base_url: https://api.openai.com/v1
    models: [gpt-4o, gpt-4o-mini]
  anthropic:
    base_url: https://api.anthropic.com/v1
    models: [claude-sonnet, claude-haiku]
  deepseek:
    base_url: https://api.deepseek.com/v1
    models: [deepseek-chat]
  ollama:
    base_url: http://localhost:11434
    models: [llama3, codellama]

tiers:
  fast:
    providers:
      - provider: deepseek
        model: deepseek-chat
      - provider: ollama
        model: llama3
  standard:
    providers:
      - provider: opencode
        model: big-pickle
      - provider: openai
        model: gpt-4o-mini
  premium:
    providers:
      - provider: opencode
        model: big-pickle
      - provider: anthropic
        model: claude-sonnet
```

## Options Considered

### 1. Multi-provider with tier-based routing (chosen)

**Pros:**
- Cost optimization — cheap models for simple tasks, powerful models for complex work
- Resilience — automatic fallback on provider failure
- Flexibility — per-agent overrides for specialized needs
- Local option — Ollama for zero-cost inference
- Budget control — tier-based cost predictability

**Cons:**
- Complexity — 5 providers to maintain
- Testing — must test across providers
- Inconsistent outputs — different models may produce different quality

### 2. Single provider (OpenAI only)

**Pros:**
- Simplest implementation
- Consistent API surface

**Cons:**
- Single point of failure
- No cost optimization
- No local inference option
- Vendor lock-in

### 3. Provider-agnostic abstraction only

**Pros:**
- Users choose their own provider
- No routing complexity

**Cons:**
- No automatic cost optimization
- No automatic fallback
- Users must configure everything manually

## Consequences

### Positive

- **Cost control**: Fast tier uses Ollama (free) or DeepSeek ($0.14/1M tokens) for simple tasks
- **Resilience**: Automatic fallback means provider outages don't halt the system
- **Flexibility**: Per-agent overrides let CTO use premium models while drafts use budget models
- **Local-first**: Ollama integration means zero marginal cost for development and testing
- **Transparency**: Model routing decisions are logged and visible in the dashboard

### Negative

- **Provider maintenance**: Each provider requires API key management and format normalization
- **Testing surface**: Must test LLM integration across 5 providers
- **Output variance**: Different models may produce different quality for the same task

### Mitigations

- Provider-specific adapters in `src/ai_company/llm/providers/` normalize API differences
- Integration tests run against mock providers; live tests against Ollama (free)
- Quality variance is managed by routing critical tasks to premium tier
- `ModelRouter` logs the selected provider for every call, enabling cost and quality analysis

## Evidence

- 5 providers configured in `company/models.yaml`
- 3 cost tiers with automatic fallback chains
- `ModelRouter` resolves provider selection in <1ms
- `CostTracker` enforces per-task and daily budgets across all providers
- Dashboard shows model routing assignments for every agent

## References

- `src/ai_company/model_router.py` — Model routing logic
- `src/ai_company/llm/client.py` — Multi-provider LLM client
- `src/ai_company/llm/providers/` — Provider-specific adapters
- `company/models.yaml` — Provider and tier configuration
- `docs/MODEL-ROUTING-POLICY.md` — Routing policy documentation
