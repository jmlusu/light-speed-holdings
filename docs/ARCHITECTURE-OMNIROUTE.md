# OpenCode + OmniRoute Architecture

## Integration Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER'S MACHINE                              │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                      OpenCode CLI/Desktop                    │   │
│  │                                                              │   │
│  │  opencode.json                                               │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  "model": "auto"                                        │  │   │
│  │  │  "plugin": ["@omniroute/opencode-plugin"]               │  │   │
│  │  │  "provider": {                                          │  │   │
│  │  │    "omniroute": {                                       │  │   │
│  │  │      "baseURL": "http://localhost:20128/v1"             │  │   │
│  │  │    }                                                    │  │   │
│  │  │  }                                                      │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  │                                                              │   │
│  │  ┌─────────────────────────┐                                 │   │
│  │  │  @omniroute/            │                                 │   │
│  │  │  opencode-plugin        │──── GET /v1/models ────┐       │   │
│  │  │  (startup: fetches      │     (model catalog)    │       │   │
│  │  │   live model list)      │                        │       │   │
│  │  └─────────────────────────┘                        │       │   │
│  │                                                     │       │   │
│  │  ┌─────────────────────────┐                        │       │   │
│  │  │  @ai-sdk/               │                        │       │   │
│  │  │  openai-compatible      │── POST /v1/chat/ ─────┤       │   │
│  │  │  (HTTP transport)       │    completions         │       │   │
│  │  └─────────────────────────┘                        │       │   │
│  └─────────────────────────────────────────────────────┼───────┘   │
│                                                        │           │
│  ┌─────────────────────────────────────────────────────▼───────┐   │
│  │                   OmniRoute Server                          │   │
│  │                  localhost:20128                             │   │
│  │                                                             │   │
│  │  ┌───────────────────────────────────────────────────────┐  │   │
│  │  │              Request Handler                          │  │   │
│  │  │  1. Detect model prefix (auto, auto/coding, etc.)    │  │   │
│  │  │  2. Route to Auto-Combo Engine or specific provider   │  │   │
│  │  └───────────────────────┬───────────────────────────────┘  │   │
│  │                          │                                  │   │
│  │  ┌───────────────────────▼───────────────────────────────┐  │   │
│  │  │          AUTO-COMBO ENGINE (13-Factor Scoring)        │  │   │
│  │  │                                                       │  │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │  │   │
│  │  │  │ Health  │ │ Quota   │ │ Cost    │ │ Latency │   │  │   │
│  │  │  │  20%    │ │  15%    │ │  15%    │ │  12%    │   │  │   │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │  │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │  │   │
│  │  │  │Task Fit │ │Stability│ │Tier Pri │ │Tier Aff │   │  │   │
│  │  │  │   8%    │ │   5%    │ │   5%    │ │   5%    │   │  │   │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │  │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐               │  │   │
│  │  │  │Specific.│ │Context  │ │Connect. │  + 3 more     │  │   │
│  │  │  │  Match  │ │Affinity │ │ Density │   factors     │  │   │
│  │  │  │   5%    │ │   5%    │ │   5%    │               │  │   │
│  │  │  └─────────┘ └─────────┘ └─────────┘               │  │   │
│  │  │                                                       │  │   │
│  │  │  Strategy: scorePool() → pick highest-scoring model   │  │   │
│  │  └───────────────────────┬───────────────────────────────┘  │   │
│  │                          │                                  │   │
│  │  ┌───────────────────────▼───────────────────────────────┐  │   │
│  │  │              Circuit Breaker                          │  │   │
│  │  │  CLOSED → healthy    HALF_OPEN → retry    OPEN → skip│  │   │
│  │  └───────────────────────┬───────────────────────────────┘  │   │
│  │                          │                                  │   │
│  └──────────────────────────┼──────────────────────────────────┘   │
│                             │                                      │
└─────────────────────────────┼──────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    UPSTREAM AI PROVIDERS                            │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │Pollinat. │ │OpenCode  │ │Kiro AI   │ │OpenAI    │ │Anthropic │ │
│  │(free)    │ │Free      │ │(free)    │ │(paid)    │ │(paid)    │ │
│  │          │ │(free)    │ │          │ │          │ │          │ │
│  │GPT-5     │ │GPT-4o    │ │Claude    │ │GPT-5.x   │ │Claude    │ │
│  │Claude    │ │Claude    │ │Sonnet    │ │o3        │ │Opus      │ │
│  │Gemini    │ │Gemini    │ │Haiku     │ │          │ │Sonnet    │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │DeepSeek  │ │Groq      │ │Cerebras  │ │Cloudflare│              │
│  │(paid)    │ │(paid)    │ │(free)    │ │(free)    │              │
│  │          │ │          │ │          │ │          │              │
│  │DeepSeek  │ │Llama     │ │GLM 4.7   │ │50+ models│              │
│  │V3/R1     │ │GPT-OSS   │ │GPT-OSS   │ │          │              │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │
│                                                                     │
│  + 340+ more providers (290+ with free tiers)                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Model Selection Flow

```
User sends: model: "auto"
                │
                ▼
┌───────────────────────────────────┐
│  1. PARSE MODEL PREFIX            │
│                                   │
│  "auto"        → default weights  │
│  "auto/coding" → quality-first    │
│  "auto/fast"   → latency-first    │
│  "auto/cheap"  → cost-first       │
│  "auto/offline"→ quota-first      │
│  "auto/smart"  → quality+explor.  │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│  2. BUILD CANDIDATE POOL          │
│                                   │
│  ┌─────────────────────────────┐  │
│  │ getProviderConnections()    │  │
│  │ → all enabled providers     │  │
│  └─────────────┬───────────────┘  │
│                │                  │
│  ┌─────────────▼───────────────┐  │
│  │ Filter: valid credentials   │  │
│  │ (API key or OAuth token)    │  │
│  └─────────────┬───────────────┘  │
│                │                  │
│  ┌─────────────▼───────────────┐  │
│  │ Cross-ref provider registry │  │
│  │ for model availability +    │  │
│  │ pricing data                │  │
│  └─────────────┬───────────────┘  │
│                │                  │
│  ┌─────────────▼───────────────┐  │
│  │ Build VirtualAutoCombo      │  │
│  │ Candidates (per-request,    │  │
│  │ never persisted to DB)      │  │
│  └─────────────┬───────────────┘  │
│                │                  │
└────────────────┼──────────────────┘
                 │
                 ▼
┌───────────────────────────────────┐
│  3. SCORE EACH CANDIDATE          │
│                                   │
│  For each (provider, model):      │
│                                   │
│  score = Σ(factor × weight)       │
│                                   │
│  health       × 0.20              │
│  + quota      × 0.15              │
│  + costInv    × 0.15              │
│  + latencyInv × 0.12              │
│  + taskFit    × 0.08              │
│  + stability  × 0.05              │
│  + tierPri    × 0.05              │
│  + tierAff    × 0.05              │
│  + specMatch  × 0.05              │
│  + ctxAff     × 0.05              │
│  + connDens   × 0.05              │
│  + cacheAff   × 0.00              │
│  + resetWin   × 0.00              │
│  ─────────────────────            │
│  = total score [0..1]             │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│  4. APPLY CIRCUIT BREAKER         │
│                                   │
│  OPEN (broken) → score = 0        │
│  HALF_OPEN     → score × 0.5     │
│  CLOSED        → score × 1.0     │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│  5. PICK WINNER                   │
│                                   │
│  highest_score → route to that    │
│                  provider/model   │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│  6. FORWARD REQUEST               │
│                                   │
│  OpenCode → OmniRoute → Provider  │
│  ←─────────────────────────────   │
│           Response flows back     │
└───────────────────────────────────┘
```

## Auto Variant Weight Profiles

```
┌──────────────┬────────┬───────┬──────┬─────────┬──────────┬───────────┐
│ Variant      │ Health │ Quota │ Cost │ Latency │ Task Fit │ Stability │
├──────────────┼────────┼───────┼──────┼─────────┼──────────┼───────────┤
│ auto         │  0.20  │ 0.15  │ 0.15 │  0.12   │   0.08   │   0.05    │
│ auto/coding  │  0.10  │ 0.05  │ 0.05 │  0.05   │   0.40   │   0.30    │
│ auto/fast    │  0.10  │ 0.05  │ 0.05 │  0.40   │   0.10   │   0.10    │
│ auto/cheap   │  0.10  │ 0.20  │ 0.50 │  0.05   │   0.05   │   0.05    │
│ auto/offline │  0.05  │ 0.50  │ 0.05 │  0.05   │   0.05   │   0.30    │
│ auto/smart   │  0.10  │ 0.05  │ 0.05 │  0.05   │   0.40   │   0.30    │
└──────────────┴────────┴───────┴──────┴─────────┴──────────┴───────────┘
                                              (+ 10% exploration rate)
```

## Data Flow Summary

```
STARTUP:
  OpenCode starts
    → plugin calls GET http://localhost:20128/v1/models
    → returns 632 model IDs from all connected providers
    → populates OpenCode's model picker

REQUEST:
  User types message
    → OpenCode sends POST http://localhost:20128/v1/chat/completions
      with model: "auto"
    → OmniRoute Auto-Combo Engine scores all candidates
    → Picks highest-scoring provider/model
    → Forwards request to upstream provider
    → Returns response to OpenCode
    → User sees response

FALLBACK (if provider fails):
  Circuit breaker opens (OPEN state)
    → Next request skips that provider
    → Scores remaining candidates
    → Routes to next best option
    → Half-open probe after cooldown
```

## Key Files

| Component | File | Purpose |
|-----------|------|---------|
| Plugin config | `opencode.json` | Plugin + provider registration |
| Plugin runtime | `@omniroute/opencode-plugin` | Fetches live model catalog |
| AI SDK transport | `@ai-sdk/openai-compatible` | HTTP layer for OpenAI-compatible APIs |
| Auto-Combo scorer | `open-sse/services/autoCombo/scoring.ts` | 13-factor scoring function |
| Virtual factory | `open-sse/services/autoCombo/virtualFactory.ts` | Builds candidate pool per-request |
| Circuit breaker | `open-sse/services/combo/circuitBreaker.ts` | Health tracking + failover |
| Config schema | `src/shared/services/opencodeConfig.ts` | Provider config generation |
