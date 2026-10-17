# Part 4 — Technical Architecture for OpenCode Agents (AI-Agnostic System)

**Source:** `brand/ai_venture_studio_execution_plan.md` Part 4
**ECL:** AI Venture Studio Execution Plan Parts 2-5
**Owner:** CTO / Platform Engineering
**Date:** 2026-09-24
**Status:** Architecture strategy (docs only — no provider lock-in changes, no registry rewrites)

---

## 1. Scope vectors

| Vector | What it is | Architectural requirements | LightSpeed fit |
|--------|------------|----------------------------|----------------|
| **B2B Enterprise Workflows** | Long-horizon multi-step processes (procurement, auditing, ERP reconciliation) | Durable state machines (Temporal, LangGraph or equivalent), HITL gates, replay/audit | Workflow engine + 5-tier approval already in-house |
| **Industry-specific specialized agents** | Vertical logic (medical reporting, legal discovery, financial underwriting) | Private RAG pipelines; optional **sovereign on-prem** hosting | Portfolio C; DPA/local residency |
| **Consumer / high-volume platforms** | Sub-second UX, streaming UI, edge cost control | Edge/cost-optimized cascade, low-latency routing | Secondary; not first studio wedge |

**Studio default posture:** ship **B2B workflows first** (predictable HITL + audit), keep vertical specialists and consumer platforms as later portfolio shapes.

---

## 2. Multi-layer abstraction architecture

```
┌───────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION & AGENT LAYER                        │
│                   (B2B Workflows / Vertical Agents / B2C)                 │
└─────────────────────────────────────────────┬─────────────────────────────┘
                                              │ Unified API Standard
                                              ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                        MODEL MESH & ROUTING ENGINE                        │
│  ┌─────────────────┐   ┌──────────────────────┐   ┌────────────────────┐  │
│  │ Fallback Chains │   │ Cost/Latency Router  │   │ Guardrail Proxy    │  │
│  └─────────────────┘   └──────────────────────┘   └────────────────────┘  │
└────────┬────────────────────────────┬────────────────────────────┬────────┘
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
│ Frontier Models │          │ Open-Weights    │          │ Local/Sovereign │
│ (Claude, OpenAI)│          │ (DeepSeek, Qwen)│          │ (Ollama, On-Prem)│
└─────────────────┘          └─────────────────┘          └─────────────────┘
```

### Layer contracts

| Layer | Responsibility | In-repo anchors |
|-------|----------------|-----------------|
| **Application & Agent** | Task graphs, agent cards, department workflows | `company-registry.yaml`, `.opencode/agents/*`, MessageBus, workflow engine |
| **Unified API** | Single interface apps call — never provider SDKs directly | Multi-provider LLM client / router modules under `src/ai_company/` |
| **Model Mesh** | Fallback chains, cost/latency routing, guardrails | Router + circuit breaker + cost tracker (see AGENTS.md provider keys) |
| **Model classes** | Frontier · open-weights · local/sovereign | Env: `OPENCODE_API_KEY` primary; `GEMINI_API_KEY` fallback; optional DeepSeek/Kimi/OpenAI/Anthropic |

---

## 3. Engineering directives (implementation-ready)

### 3.1 Universal protocol proxy (unified gateway)

- Expose **one internal interface** (existing multi-provider LLM client or a LiteLLM-style gateway).
- **Decouple** application code from OpenAI / Anthropic / DeepSeek / local Ollama endpoints.
- Provider swap = config, not PR across the monorepo.

### 3.2 Model cascade & dynamic cost router

| Task class | Default routing | Escalation rule |
|------------|-----------------|-----------------|
| Extraction, classification, summarization of structured fields | Low-cost / open-weights | Escalate only if confidence < threshold |
| Multi-step reasoning, high-risk synthesis, policy/legal text | Frontier first | Fallback chain on outage; never silent wrong-model for Tier-0 decisions |
| Sovereign deployments | Local/on-prem only | No cross-border egress of client data (Part 2 Reservation 2) |

Emit **cost + model_id + latency** per call for Part 5 capital-efficiency metrics.

### 3.3 Deterministic execution & state tracking

- Keep **orchestration logic separate from model inference**.
- Durable workers (Temporal, LangGraph, or the in-repo MessageBus + workflow engine with the same guarantees).
- **State persists across API failures** — retry, dead-letter, resume; no lost approvals.
- HITL: blocked states wait on ApprovalGate; expired pending → EXPIRED (AGENTS.md §9.1).

### 3.4 Security & PII guardrails

- Intermediary proxy **redacts/hashes PII** before outbound LLM requests where policy requires it.
- **Schema validation** on model outputs before any DB/file commit.
- Canonical **7-tool sandbox** (`read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task`) — no ad-hoc tools from prompts (AGENTS.md §8).
- Skills that transmit local data require `docs/APPROVED-VENDORS.md` allow-list (§9.2).

---

## 4. Mapping to current LightSpeed architecture

| Blueprint element | Existing system | Gap / follow-up |
|-------------------|-----------------|-----------------|
| Model mesh / router | Multi-provider client, cost tracker, circuit breaker | Harden cascade thresholds + per-venture cost tags |
| Guardrail proxy | ApprovalGate, RBAC, audit chains | PII redaction layer formalized as shared middleware |
| Durable orchestration | MessageBus + workflow engine (9 workflows) | Prove multi-venture isolation / tenancy for spin-outs |
| Unified registry | `company-registry.yaml` → generated agents | Public/internal boundary (ADR-027/028); P2 registry transform ECL (parked) |
| Evidence metrics | Org Health KPIs, ADR-033 | Studio rollup + venture scorecards (Part 5) |

**Constraint:** This ECL is documentation only. Registry schema and route cutover remain under architecture v2 / P2 implementation tracks (`docs/architecture/V2_IMPLEMENTATION_ROADMAP.md`).

---

## 5. AI-agnostic decision

| Choice | Why |
|--------|-----|
| Gateway + cascade, not single-vendor SDK | Cost control, availability, sovereignty options |
| Durable state, not fire-and-forget chains | B2B workflows require audit + resume |
| HITL in the mesh, not only in the app | One governance plane for every venture |
| Open-weights / local as first-class peers | Malawi bandwidth + data-protection constraints are product features, not edge cases |

---

## 6. Deliverable checklist

- [x] Scope vectors for B2B / vertical / consumer
- [x] Multi-layer diagram with contracts
- [x] Directives: proxy, cascade, durable state, PII/schema guardrails
- [x] Map to in-repo systems and known gaps
- [x] Explicit non-goals (no code migration in this ECL)

**Non-goals:** implementing the gateway, changing provider keys, or landing P2 registry transform.
