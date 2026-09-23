# ADR-023: Jev System One Model Integration for Decision Primitives

**Status:** Proposed
**Date:** 2026-09-18
**Deciders:** CTO, CAIO, CFO, Head of Pharos
**Technical Domain:** Decision Engine / LLM Architecture

## Context

LightSpeed's agentic stack currently uses LLMs (via multi-provider routing, ADR-004) for all reasoning tasks including:
- Agent routing & intent classification (3–30s, $0.02–$0.08/task)
- Tool call verification (sampled, post-hoc)
- Trace observability & anomaly detection (batch LLM passes)
- Policy compliance checks (deterministic + sampled LLM)

**Problems:**
1. **Latency ceiling**: LLM routing adds 3–30s per task, blocking real-time UX
2. **Cost at scale**: 10k tasks/day × $0.03 = $300/day on routing alone
3. **Hallucination risk**: Tool arg hallucinations detected only post-hoc
4. **No calibration**: LLM confidence scores are uncalibrated — can't set reliable thresholds
5. **Overkill for decisions**: Structured decisions (choice/score/verify) don't need generative capability

**Jev (TypeSafe AI)** introduces a new model category — **System One Models** — trained via **RLCD (Reinforcement Learning for Calibrated Decisions)** that output **typed probabilistic decisions** instead of text.

| Metric | Jev (System One) | Frontier LLM (RLHF/RLVR) |
|--------|------------------|--------------------------|
| Training Objective | Calibrated decisions (epistemically honest probabilities) | Human preference / verifiable rewards |
| Output | Typed values (Choice, Score, Noul) + calibrated probabilities | Free-form text strings |
| Sampling | Parallel (all outputs in single query) | Sequential (autoregressive) |
| Input Cost | **$0.042 / M tokens** | $0.20 – $10 / M tokens |
| Output Cost | **FREE** | ~5× input cost |
| Latency (p50) | **70–500 ms** | 3 – 329 seconds |
| Type Safety | Structural guarantee (bounded by declared schema) | Runtime validation required |
| Hallucination | Impossible by construction | Inherent risk |

**Published workflow benchmarks** (4 production-shaped tasks):
- Jev: **67.8% agreement** with GPT-6 Astra + Claude Fable 5.1 reference at **$0.0004/case, 0.4s**
- GPT-5.6 Terra: 67.9% at **$0.0304/case, 10.1s** (76× cost, 25× latency)
- GPT-5.6 Sol: 74.1% at **$0.0836/case, 23.3s** (209× cost, 58× latency)

## Decision

We will integrate Jev as a **decision primitive layer** sitting between deterministic code and LLM calls, enabling per-turn supervision, routing, verification, and guardrails at negligible cost/latency.

**Integration approach:**
1. **New `DecisionProvider` abstraction** in `src/ai_company/llm/` — unified interface for Jev + LLM fallback
2. **Replace LLM router** with `JevRouter` for intent classification, complexity scoring, risk assessment
3. **Add `DecisionAgent` type** to `company-registry.yaml` schema with native Jev question schemas
4. **Instrument executor loop** with Jev pre/post tool-call guardrails
5. **Build map-reduce observability** over agent traces using Jev batch scoring

**Phased rollout:**
- **Phase 1 (Days 1–30)**: Validation on 5 LightSpeed workflows using `daf-jev` toolkit
- **Phase 2 (Days 31–60)**: Prototype `DecisionProvider`, `JevRouter`, `DecisionAgent` type
- **Phase 3 (Days 61–90)**: Production hardening, calibration monitoring, enterprise terms negotiation

**Commercial model:** Start with **API Consumption + Strategic Partnership** (TypeSafe is early-stage, $40M seed from DCVC, Sep 2026 launch). Evaluate Enterprise License at scale.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DECISION PROVIDER LAYER                           │
├─────────────────────────────────────────────────────────────────────────┤
│  DecisionProvider (interface)                                           │
│    ├─ JevProvider (TypeSafe SDK) ──▶ Jev API (primary)                 │
│    └─ LLMProvider (existing) ──────▶ ModelRouter (fallback)            │
│                                                                          │
│  Questions batched per request:                                         │
│    {intent: Choice, complexity: Score, risk: Choice, human: Noul}      │
│    → single forward pass, parallel evaluation, calibrated probabilities │
└─────────────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  JevRouter    │    │ JevGuardrail  │    │ DecisionAgent │
│  (routing)    │    │ (executor)    │    │ (registry)    │
└───────────────┘    └───────────────┘    └───────────────┘
```

**Registry extension (`company-registry.yaml`):**
```yaml
agents:
  - id: triage-specialist
    type: decision_agent
    model: jev-1.13.0
    primitives:
      - choice: {criteria: {billing: "...", technical: "...", security: "...", other: "..."}}
      - score: {criteria: ["routine", "urgent", "critical", "catastrophic"]}
      - noul: {instructions: "Is this a known attack pattern?"}
    thresholds:
      confidence: 0.85
      human_escalation: 0.6
    fallback: {type: llm_agent, id: senior-analyst}
```

## Options Considered

### 1. Jev as decision primitive layer (chosen)

**Pros:**
- 76–209× cost reduction on decision tasks
- 25–58× latency improvement enabling real-time UX
- Calibrated probabilities enable reliable threshold gating
- Structural type safety eliminates hallucination class
- Complementary to LLMs — not a replacement
- TypeSafe early partnership window (seed stage, DCVC-backed)

**Cons:**
- Single-source vendor dependency (mitigated by LLM fallback abstraction)
- Early-access instability (rate limits, API changes)
- English-primary training (benchmark non-English workloads)
- RLCD generalizability unproven beyond 4 published workflows
- No native rationale generation (audit trail via versioned inputs + distributions)

### 2. Continue with LLM-only routing

**Pros:**
- No new vendor, no integration work
- Familiar technology, mature ecosystem
- Consistent generative capability for all tasks

**Cons:**
- Latency ceiling blocks real-time applications
- Cost grows linearly with task volume
- No calibration — can't build reliable confidence gates
- Hallucination risk persists on tool calls
- Over-provisioning generative models for structured decisions

### 3. Build custom decision model in-house

**Pros:**
- Full control, no vendor risk
- Tailored to LightSpeed workflows
- IP ownership

**Cons:**
- RLCD methodology is novel research (InstructGPT co-author led)
- 12–24 months to parity, $5M+ investment
- TypeSafe has 2+ year head start, DCVC backing
- Distracts from core agentic platform roadmap

### 4. Use structured-output LLMs (JSON mode, Instructor, etc.)

**Pros:**
- Available today on existing providers
- No new vendor

**Cons:**
- Still autoregressive (1–30s latency)
- No calibration — confidence scores unreliable
- Post-hoc constraint ≠ structural guarantee
- 10–100× cost of Jev for equivalent decisions
- Hallucination reduced but not eliminated

## Consequences

### Positive

- **Cost reduction**: Routing + guardrails + observability → ~$400K–$1.2M annual savings at current scale
- **Latency breakthrough**: 100ms decision loops enable real-time chat, adaptive UI, content moderation
- **Reliability**: Calibrated confidence gates catch 90%+ tool hallucinations pre-execution
- **Observability at scale**: Full-trace analysis for $4/day vs $400–$4,000 with LLMs
- **LLM capacity freed**: ~40% of LLM calls shift to Jev → 66% throughput increase on reasoning tasks
- **Compliance advantage**: Jev's audit trail (versioned inputs, distributions, thresholds) exceeds opaque LLM baselines

### Negative

- **Vendor dependency**: TypeSafe API is single-source (mitigated by `DecisionProvider` abstraction + LLM fallback)
- **Integration complexity**: New provider adapters, registry schema, generator templates, middleware
- **Calibration monitoring required**: Must track ECE, Brier score continuously; version pin `jev-1.13.0`
- **English-centric risk**: Validate multilingual workloads; maintain LLM fallback for low-confidence non-English
- **Early-access volatility**: Rate limits, API changes, potential pivot (contractual escrow, parity fallback)

### Mitigations

- `DecisionProvider` interface abstracts Jev behind same contract as LLM providers
- Shadow-mode evaluation on 100% traffic before production rollout
- Automated calibration dashboard (Grafana + TypeSafe SDK metrics)
- Contractual source-code escrow; monitor DCVC portfolio signals
- Run LightSpeed-specific evals on 5+ internal workflows before production gate (≥90% LLM agreement on ≥4/5)

## Evidence

- TypeSafe AI official docs, blog, SDK: https://typesafe.ai/, https://docs.typesafe.ai/
- Workflow evals (interactive): https://evals.typesafe.ai/
- Michał Chromiak technical analysis (Sep 17, 2026): https://mchromiak.github.io/articles/2026/Sep/17/Jev-Typed-Decisions-for-Enterprise-AI/
- `daf-jev` toolkit (Zenodo:22816188): https://zenodo.org/records/22816188
- TypeSafe SDKs: github.com/typesafe-ai/typesafe-sdk-python, github.com/typesafe-ai/typesafe-sdk-js
- Founder: Diogo Almeida (InstructGPT co-author, OpenAI 2018–2022)
- Research brief: `JEV_INTEGRATION_BRIEF.md` (this repo)

## References

- `docs/adr/004-multi-provider-llm.md` — Existing LLM routing architecture
- `src/ai_company/model_router.py` — Model routing logic (to extend)
- `src/ai_company/llm/client.py` — Multi-provider LLM client (to extend)
- `src/ai_company/orchestrator/router.py` — Current LLM router (to replace)
- `src/ai_company/orchestrator/executor.py` — Executor loop (to instrument)
- `src/ai_company/models/models.py` — Domain models (add `DecisionAgent`)
- `src/ai_company/generator.py` — Agent generator (add decision_agent template)
- `templates/agents/agent.md.j2` — Agent card template (extend for Jev)
- `company-registry.yaml` — Agent registry (add decision_agent type)

## Next Steps

1. **Week 1**: Join TypeSafe waitlist; request early access for LightSpeed team
2. **Week 2**: Run `daf-jev` benchmarks on 5 LightSpeed workflows
3. **Week 3**: Compare Jev vs. LLM vs. deterministic on agreement, calibration, latency, cost
4. **Week 4**: Decision gate — proceed if Jev ≥90% LLM agreement on ≥4/5 workflows
5. **Days 31–60**: Implement `DecisionProvider`, `JevRouter`, `DecisionAgent` type
6. **Days 61–90**: Production hardening, calibration monitoring, enterprise terms

---

**Decision Gate (Day 30):** Proceed to Phase 2 only if validation criteria met. Otherwise, revert to LLM-only with structured-output optimization.