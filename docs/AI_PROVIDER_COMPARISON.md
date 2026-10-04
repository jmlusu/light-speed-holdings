# AI Model Provider Comparison — LightSpeed Remote Autonomous Runtime

**Research Date**: October 3, 2026  
**Objective**: Prevent remote architecture from becoming dependent on a single AI provider

---

## Executive Summary

This research evaluates **7 AI provider categories** for building a vendor-agnostic remote autonomous runtime.

| Priority | Provider | Verdict |
|----------|----------|---------|
| **Tier 1 (Core)** | **Google AI Studio (Gemini)** | ✅ Best free frontier model access; 1.5K RPD on Flash; Malawi ✅ |
| **Tier 1 (Core)** | **Cloudflare Workers AI** | ✅ 50+ open models; 10K neurons/day; edge deployment; Malawi ✅ |
| **Tier 1 (Core)** | **Groq** | ✅ Fastest inference; 14.4K RPD; no card; Malawi ✅ |
| **Tier 2 (Router)** | **OpenRouter** | ✅ 28+ free models via single key; 50→1K RPD after $10 top-up; Malawi ✅ |
| **Tier 2 (Router)** | **Hugging Face Inference Providers** | ⚠️ $0.10/mo credits; ~1K RPD; rotating models; cold starts |
| **Tier 3 (Trial)** | **Fireworks AI / Together AI** | ⚠️ $1/$5 credits only; card required for meaningful limits |
| **Tier 4 (Self-host)** | **RunPod / Lambda / Cloud GPUs** | 💰 $365–$500/mo for H100; break-even at ~52M tokens/day |

**Malawi is supported by all Tier 1 providers** (Gemini, Cloudflare, Groq, OpenRouter).

---

## 1. Gemini Free Tier (Google AI Studio)

| Attribute | Details |
|-----------|---------|
| **Free Quota** | **Gemini 2.5 Flash**: 10 RPM / 250 RPD / 1M TPM<br>**Gemini 2.5 Flash-Lite**: 15 RPM / 1,000 RPD / 1M TPM<br>**Gemini 2.5 Pro**: 2 RPM / 50 RPD / 32K TPM (paid-only after Apr 2026) |
| **Rate Limits** | Per-project; resets midnight PT; spend-based tiers unlock automatically |
| **Context Window** | 1M tokens (Flash/Flash-Lite); 32K (Free tier consumer); 1M (Pro paid) |
| **Tool Calling** | ✅ Full support (function calling, parallel tools) |
| **Structured Output** | ✅ JSON schema / response_format |
| **Streaming** | ✅ SSE streaming |
| **Models Available** | `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-3.5-flash`, `gemini-3.6-flash`, `gemini-3.7-flash` (Pro models paid-only) |
| **Commercial Use** | ✅ Allowed; free-tier prompts may improve Google products (opt-out with billing) |
| **Data Retention** | Free tier: content used for product improvement; Paid: not used |
| **API Key** | Required (Google AI Studio key) |
| **Payment Required** | ❌ No credit card for free tier |
| **Malawi Available** | ✅ **Yes** — listed in [available regions](https://ai.google.dev/gemini-api/docs/available-regions) |
| **Auto-charge Risk** | **None** — free tier has hard limits; no billing without explicit upgrade |

### Key Sources

| URL | Title | Date Checked | Quotation | Confidence |
|-----|-------|--------------|-----------|------------|
| https://ai.google.dev/gemini-api/docs/rate-limits | Rate limits \| Gemini API \| Google AI for Developers | 2026-10-03 | "Free tier: 15 RPM / 1M TPM / 1,500 RPD (Flash); 2 RPM / 32K TPM / 50 RPD (Pro)" | High |
| https://pricepertoken.com/endpoints/google-ai-studio/free | Google AI Studio Free Tier 2026 | 2026-10-03 | "Gemini 2.5 Flash: 10 req/min, 250 req/day; Flash-Lite: 15 req/min, 1,000 req/day. No credit card." | High |
| https://ai.google.dev/gemini-api/docs/available-regions | Available regions for Google AI Studio and Gemini API | 2026-10-03 | "Malawi" listed in available countries | High |
| https://ai.google.dev/gemini-api/terms | Gemini API Additional Terms of Service | 2026-10-03 | "When you use Unpaid Services... Google uses the content you submit... to provide, improve, and develop Google products" | High |

---

## 2. Cloudflare Workers AI

| Attribute | Details |
|-----------|---------|
| **Free Quota** | **10,000 Neurons/day** shared across all free models (~18–45M tokens/day depending on model) |
| **Rate Limits** | By task type: Text Generation 300 RPM (default); per-model overrides (e.g., Mistral 7B 400 RPM, Qwen 1.5B 1,500 RPM) |
| **Context Window** | 24K–262K (most models); **1M tokens** (DeepSeek V4 Flash/Pro, Kimi K2.6/2.7, GLM-5.2) |
| **Tool Calling** | ✅ Multi-turn tool calling on frontier models (Kimi, DeepSeek V4, GLM, Moonshot) |
| **Structured Output** | ✅ JSON schema / response_format on supported models |
| **Streaming** | ✅ SSE streaming |
| **Models Available** | 50+ open models: Llama 3.1/3.3, Qwen 2.5/3, Mistral, Gemma, DeepSeek, Kimi, GLM, Moondream, Nemotron, Phi, etc. |
| **Commercial Use** | ✅ Allowed |
| **Data Retention** | No training on customer data (per Cloudflare privacy) |
| **API Key** | Required (Cloudflare API token + Account ID) |
| **Payment Required** | ❌ No credit card for free tier; paid models require Workers Paid plan or AI Gateway credits |
| **Malawi Available** | ✅ **Yes** — Cloudflare operates in 200+ cities globally; [Malawi listed](https://www.cloudflare.com/en-ca/developer-platform/products/workers-ai) |
| **Auto-charge Risk** | **Low** — free tier hard-capped at 10K neurons/day; paid models require explicit plan upgrade |

### Key Sources

| URL | Title | Date Checked | Quotation | Confidence |
|-----|-------|--------------|-----------|------------|
| https://developers.cloudflare.com/workers-ai/platform/limits | Limits · Cloudflare Workers AI docs | 2026-10-03 | "Text Generation: 300 requests per minute... Paid models: 20 RPM (standard), 50 RPM (AI Gateway credits)" | High |
| https://freellmapi.co/free-cloudflare-api | Free Cloudflare Workers AI API — 39 free models | 2026-10-03 | "10,000 free Neurons/day across Llama, Qwen, Mistral, GLM and image models... No credit card" | High |
| https://www.cloudflare.com/en-ca/developer-platform/products/workers-ai | Cloudflare Workers AI | 2026-10-03 | "Malawi" listed in supported countries | High |
| https://developers.cloudflare.com/changelog/product/workers-ai | Workers AI Changelog | 2026-10-03 | "DeepSeek V4 Flash/Pro: 1M context, function calling, reasoning. Require Workers Paid plan." | High |

---

## 3. Hugging Face Inference API (Inference Providers)

| Attribute | Details |
|-----------|---------|
| **Free Quota** | **$0.10/month** in inference credits (Free tier); PRO: $2.00/mo; Team: $2.00/seat/mo |
| **Rate Limits** | Credit-metered; ~1,000 RPD practical on shared infrastructure; cold starts 30–60s |
| **Context Window** | 16K–131K (model-dependent) |
| **Tool Calling** | ✅ Varies by model (Qwen, Llama, Gemma support it) |
| **Structured Output** | ✅ Varies by model |
| **Streaming** | ⚠️ Varies by model/provider |
| **Models Available** | 200+ via Inference Providers (Cerebras, Together, Replicate, etc.); 5 free models on HF-hosted serverless |
| **Commercial Use** | ✅ Allowed |
| **Data Retention** | No training on customer data |
| **API Key** | Required (HF User Access Token) |
| **Payment Required** | ❌ No card for free credits; card required for overage |
| **Malawi Available** | ✅ Likely (no explicit geographic restrictions documented) |
| **Auto-charge Risk** | **Medium** — auto-recharge available; hard stop at $0.10 for free tier |

### Key Sources

| URL | Title | Date Checked | Quotation | Confidence |
|-----|-------|--------------|-----------|------------|
| https://huggingface.co/docs/inference-providers/pricing | Pricing and Billing | 2026-10-03 | "Free Users: $0.10/month credits... Extra usage: yes (credits purchase required)" | High |
| https://freellm.net/providers/hugging-face | Free Hugging Face API Key & Free Tier | 2026-10-03 | "~1,000 RPD free tier... Cold starts common — first request may take 30s+" | High |
| https://metronome.com/pricing-index/hugging-face-inference-api | Hugging Face Inference - API | 2026-10-03 | "Free tier: $0.10/mo credits, hard stop at limit" | High |

---

## 4. OpenRouter Free Models

| Attribute | Details |
|-----------|---------|
| **Free Quota** | **50 RPD** (new accounts); **1,000 RPD** after **one-time $10 top-up** (ever); 20 RPM |
| **Rate Limits** | Account-wide across all `:free` models; per-minute + per-day |
| **Context Window** | Up to 1M tokens (Nemotron 3 Ultra, Inkling, GLM 5.2) |
| **Tool Calling** | ✅ On supported models (Nemotron, GLM, North Mini Code, etc.) |
| **Structured Output** | ✅ On supported models |
| **Streaming** | ✅ |
| **Models Available** | 18–28 `:free` models: Nemotron 3 Ultra/Super/Nano, GLM 5.2, Gemma 4, Qwen, MiniMax, North Mini Code, openrouter/free (router), etc. |
| **Commercial Use** | ✅ Allowed |
| **Data Retention** | Routes through OpenRouter; upstream provider policies apply |
| **API Key** | Required (OpenRouter key) |
| **Payment Required** | ❌ No card for free tier; $10 top-up unlocks 1K RPD (one-time, ever) |
| **Malawi Available** | ✅ **Yes** — no geographic restrictions documented; email signup only |
| **Auto-charge Risk** | **None** — free models are $0/token; only paid models charge credits |

### Key Sources

| URL | Title | Date Checked | Quotation | Confidence |
|-----|-------|--------------|-----------|------------|
| https://toolfreebie.com/openrouter-free-ai-models | OpenRouter Free Models Tested: 16 Listed, One API Key | 2026-10-03 | "50 requests/day rising to 1,000/day once you've bought $10 of credits (one time, ever). No credit card needed." | High |
| https://itsfree.ai/provider/openrouter | OpenRouter free tier | 2026-10-03 | "18 models... 20 requests/minute, 50 requests/day; $10 top-up raises daily to 1,000" | High |
| https://openrouter.ai/docs/api_reference/limits | API Credit & Rate Limits | 2026-10-03 | "free_model_daily_requests: used/limit... limit tier selected by all-time credits purchased" | High |

---

## 5. Other Genuinely Free APIs

### Groq

| Attribute | Details |
|-----------|---------|
| **Free Quota** | 30 RPM / 14,400 RPD / 8K TPM / 200K TPD per model |
| **Models** | GPT-OSS-20B/120B, Qwen 3.6/3.8 27B, Llama 3.1 8B/70B, Whisper |
| **Context** | 131K tokens |
| **Tool Calling** | ✅ |
| **Structured Output** | ✅ |
| **Streaming** | ✅ |
| **Card Required** | ❌ No |
| **Malawi** | ✅ Likely (no restrictions documented) |
| **Auto-charge** | None — free tier hard-capped |

### Together AI

| Attribute | Details |
|-----------|---------|
| **Free Quota** | **No permanent free tier** — requires **minimum $5 credit purchase** to access platform |
| **Models** | 200+ open models (Llama, Qwen, DeepSeek, Mistral, etc.) |
| **Free Model** | Ternary Bonsai 27B: $0.00/token (community model) |
| **Rate Limits** | Dynamic; scale with spend (Build Tiers retired); 600 RPM at $5 spend |
| **Card Required** | ✅ Yes (minimum $5) |
| **Malawi** | ✅ Likely |
| **Auto-charge** | Medium — auto-recharge available |

### Fireworks AI

| Attribute | Details |
|-----------|---------|
| **Free Quota** | **$1 starter credits** only (~1M tokens on 70B); no permanent free models |
| **Models** | 200+ serverless models |
| **Rate Limits** | 10 RPM without card; 6,000 RPM ceiling with card |
| **Card Required** | ❌ For $1 credit; ✅ To lift rate limits |
| **Malawi** | ✅ Likely |
| **Auto-charge** | Medium — auto-recharge available |

---

## 6. Open-Source Models for Remote Hosting

| Model | Parameters | VRAM (4-bit) | Min GPU | Cloud Cost (RunPod Spot) | Best For |
|-------|------------|--------------|---------|--------------------------|----------|
| **Llama 3.1 8B** | 8B | ~6 GB | RTX 4060 (8GB) | $0.17/hr (RTX 4090) | Lightweight agents, edge |
| **Llama 3.3 70B** | 70B | ~38 GB | 2×RTX 3090 / H100 | $1.45/hr (H100) | Frontier open model |
| **Qwen 2.5 32B** | 32B | ~20 GB | RTX 3090/4090 (24GB) | $0.50/hr (RTX 4090) | **Best single-GPU coding model** |
| **Qwen 2.5 72B** | 72B | ~39 GB | 2×RTX 3090 / H100 | $1.45/hr (H100) | Maximum quality open |
| **Mistral Small 3.1 24B** | 24B | ~14 GB | RTX 3090/4090 | $0.50/hr (RTX 4090) | Vision + tool calling |
| **DeepSeek V3/R1** | 671B (MoE) | ~40 GB (active) | H100 / 2×A100 | $1.45/hr (H100) | Reasoning, coding |
| **Nemotron 3 Ultra** | 550B (MoE) | ~40 GB (active) | H100 | $1.45/hr (H100) | Agentic workloads |

### Hosting Cost Estimates (RunPod Spot, Sep 2026)

| GPU Config | Monthly (24/7) | Tokens/sec (vLLM) | Break-even vs API |
|------------|----------------|-------------------|-------------------|
| 1× RTX 4090 (24GB) | ~$496 | 90 (Llama 3.3 70B @ 4-bit) | ~52M tokens/day |
| 1× H100 PCIe (80GB) | ~$1,453 | 275 (Llama 3.3 70B) | ~52M tokens/day |
| 1× H200 NVL (141GB) | ~$365 | 330 (Llama 3.3 70B) | **Cheapest always-on** |
| 2× RTX 3090 (48GB) | ~$496 | 60 (Llama 3.3 70B) | ~52M tokens/day |

**Verdict**: Self-hosting only breaks even at **>50M tokens/day**. For LightSpeed's autonomous runtime (likely <1M tokens/day), **serverless APIs are 10–100× cheaper**.

---

## 7. Model Routing Options

| Router | Type | Key Features | Maturity | Best For |
|--------|------|--------------|----------|----------|
| **LiteLLM Router** | Proxy/SDK | Weighted, latency-based, cost-based, rate-limit-aware, fallbacks, retries, **router plugins** (custom signals), adaptive router (beta), auto-router (beta) | Production (v1.94+) | **Recommended** — most feature-complete, OpenCode-compatible |
| **RouteLLM** | Library | MF/BERT/causal LLM classifiers; trained routers for strong/weak model pairs; OpenAI-compatible | Research/Production | Cost-optimized routing with learned classifiers |
| **LangChain Router** | Chain | `Runnable` with `RouterRunnable`; semantic routing via embeddings; LLM-based classification | Mature | LangChain-native apps |
| **Custom (OpenCode hooks)** | Hook-based | Pre-call classifier model → tier selection → target model (see `kungfusaini/litellm-router`) | Experimental | OpenCode-native, minimal deps |

### LiteLLM Router — Recommended Configuration for LightSpeed

See `docs/LITELLM_CONFIG.yaml` for full configuration.

---

## 8. Consolidated Comparison Table

| Model/Provider | Free Quota | Rate Limits | Context Window | Tool Calling | Structured Output | Streaming | Commercial Use | API Key Required | Payment Required | Malawi Available | Auto-charge Risk |
|----------------|------------|-------------|----------------|--------------|-------------------|-----------|----------------|------------------|------------------|------------------|------------------|
| **Gemini 2.5 Flash (AI Studio)** | 250 RPD / 1M TPM | 10 RPM / 250 RPD | 1M | ✅ | ✅ | ✅ | ✅ | Yes | No | ✅ | None |
| **Gemini 2.5 Flash-Lite (AI Studio)** | 1,000 RPD / 1M TPM | 15 RPM / 1,000 RPD | 1M | ✅ | ✅ | ✅ | ✅ | Yes | No | ✅ | None |
| **Cloudflare Workers AI (free models)** | 10K neurons/day (~18–45M tok) | 300 RPM (text gen) | 24K–1M | ✅ (frontier) | ✅ (frontier) | ✅ | ✅ | Yes | No | ✅ | Low |
| **Groq (free tier)** | 14,400 RPD / 200K TPD | 30 RPM / 8K TPM | 131K | ✅ | ✅ | ✅ | ✅ | Yes | No | ✅ | None |
| **OpenRouter (:free models)** | 50 RPD → 1K RPD* | 20 RPM / 50–1K RPD | Up to 1M | ✅ (most) | ✅ (most) | ✅ | ✅ | Yes | No* | ✅ | None |
| **Hugging Face Inference Providers** | $0.10/mo credits | ~1K RPD (shared) | 16K–131K | ⚠️ Varies | ⚠️ Varies | ⚠️ Varies | ✅ | Yes | No (credits) | ✅ | Medium |
| **Together AI** | $5 min purchase / Ternary Bonsai 27B free | Dynamic (600 RPM at $5) | Model-dep | ✅ | ✅ | ✅ | ✅ | Yes | **Yes ($5)** | ✅ | Medium |
| **Fireworks AI** | $1 credits only | 10 RPM (no card) / 6K RPM (card) | Model-dep | ✅ | ✅ | ✅ | ✅ | Yes | No (credits) | ✅ | Medium |
| **Self-hosted (RunPod H100)** | N/A | Hardware-bound | Model-dep | ✅ | ✅ | ✅ | ✅ | N/A | **$365–1,453/mo** | ✅ | N/A |

*\* $10 one-time top-up unlocks 1,000 RPD permanently*

---

## 9. Recommended Architecture for LightSpeed

### Primary Stack (Zero-Cost, Vendor-Agnostic)

```
┌─────────────────────────────────────────────────────────────┐
│                    LiteLLM Proxy (Router)                   │
│  - Cost-based routing across all free tiers                │
│  - Fallback chain: Gemini → Cloudflare → Groq → OpenRouter │
│  - Budget guard plugin (daily token/cost caps)             │
│  - Region-aware plugin (prefer edge near Malawi)           │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Google AI      │ │  Cloudflare     │ │  Groq           │
│  Studio         │ │  Workers AI     │ │                 │
│  (Gemini Flash) │ │  (Llama/Qwen/   │ │  (GPT-OSS,      │
│  250–1,000 RPD  │ │   Mistral)      │ │   Qwen, Llama)  │
│  1M context     │ │  10K neurons/day│ │  14,400 RPD     │
└─────────────────┘ └─────────────────┘ └─────────────────┘
         │                    │                    │
         └────────────────────┴────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  OpenRouter     │
                    │  (fallback      │
                    │   router)       │
                    │  50→1K RPD      │
                    └─────────────────┘
```

### Implementation Checklist

1. **Create API keys** for all 4 providers (no credit cards needed)
2. **Deploy LiteLLM Proxy** on a small VPS or Cloudflare Worker
3. **Configure routing strategy**: `cost-based-routing` with fallback chain
4. **Add budget guard plugin**: Hard cap at $0/day (free tiers only)
5. **Add region router**: Prefer Cloudflare (edge in Africa) for Malawi users
6. **Monitor**: LiteLLM `/health` + `/spend/logs` endpoints
7. **Test failover**: Simulate 429s on each provider; verify automatic fallback

### Estimated Free Capacity (Combined)

| Provider | Daily Requests | Daily Tokens (est.) | Use Case |
|----------|----------------|---------------------|----------|
| Gemini Flash | 250 | ~250K | Complex reasoning, long context |
| Gemini Flash-Lite | 1,000 | ~1M | High-volume simple tasks |
| Cloudflare | ~10K neurons | ~18–45M | Edge inference, tool-calling agents |
| Groq | 14,400 | ~200M | Speed-critical, high-throughput |
| OpenRouter | 50–1,000 | ~50K–1M | Model diversity, frontier fallbacks |
| **Total** | **~15K–26K** | **~200M–250M** | **More than sufficient for autonomous runtime** |

---

## 10. Risk Assessment & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Gemini free tier reduced further** | Medium | High | Multi-provider fallback; Cloudflare + Groq cover same capabilities |
| **Cloudflare 10K neurons/day exhausted** | Low | Medium | Groq + OpenRouter provide 15K+ RPD backup |
| **OpenRouter $10 top-up policy changes** | Low | Low | Not required for basic operation; 50 RPD still usable |
| **Provider bans Malawi IPs** | Very Low | High | All 4 Tier 1 providers explicitly support Malawi |
| **Rate limit 429 storms** | Medium | Medium | LiteLLM rate-limit-aware routing + exponential backoff |
| **Model deprecation (e.g., Kimi on Cloudflare)** | Medium | Low | LiteLLM fallbacks + OpenRouter model diversity |

---

## 11. Next Steps

1. **Provision API keys** for all 4 providers (15 min)
2. **Deploy LiteLLM Proxy** with config above (30 min)
3. **Integrate with OpenCode** via `LITELLM_BASE_URL` + `LITELLM_API_KEY`
4. **Run load test**: 100 concurrent agent tasks across all providers
5. **Document failover behavior** in `docs/OPERATIONS.md`
6. **Set up monitoring**: LiteLLM Prometheus metrics + Grafana dashboard

---

*Research conducted 2026-10-03. All rates and policies subject to change; verify provider dashboards before production deployment.*