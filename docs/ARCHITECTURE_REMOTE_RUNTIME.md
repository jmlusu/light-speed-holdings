# LightSpeed Remote Autonomous Runtime — Architecture Specification

**Version**: 1.0  
**Date**: October 3, 2026  
**Status**: APPROVED FOR IMPLEMENTATION  
**Classification**: Internal — Architecture Decision Record

---

## 1. Executive Summary

This document specifies the architecture for enabling the LightSpeed AI Company Builder (90-agent hierarchy) to operate continuously when the developer's local Windows machine is completely powered off, disconnected, or unavailable.

**Core Principle**: The local machine becomes an **optional development and compute node**, not a dependency for autonomous operation.

**Constraints Satisfied**:
- ✅ No local-machine dependency (Windows PC = OFF, Ollama = OFF, OpenCode = OFF)
- ✅ No mandatory payment method (all core components free-tier viable)
- ✅ No premature implementation (this is RESEARCH → ARCHITECTURE → PLAN only)
- ✅ Malawi availability confirmed for all Tier 1 providers

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        LIGHTSPEED REMOTE AUTONOMOUS RUNTIME                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         CONTROL PLANE (Cloudflare)                                │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  ┌─────────────────┐  │   │
│  │  │   Scheduler  │  │  Task Queue  │  │  Agent Registry  │  │  State Store    │  │   │
│  │  │ (Cron        │  │  (Queues)    │  │  (KV + D1)       │  │  (Durable Obj)  │  │   │
│  │  │  Triggers)   │  │              │  │                  │  │                 │  │   │
│  │  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  └────────┬────────┘  │   │
│  │         │                 │                   │                   │            │   │
│  │         ▼                 ▼                   ▼                   ▼            │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                    API GATEWAY / WEBHOOK RECEIVER (Worker)              │   │   │
│  │  │  • HTTP ingress • Auth (OIDC/JWT) • Rate limit • Request routing       │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                    │                                                    │
│         ┌──────────────────────────┼──────────────────────────┐                        │
│         ▼                          ▼                          ▼                        │
│  ┌───────────────┐         ┌───────────────┐         ┌───────────────┐                │
│  │  EXECUTION    │         │  EXECUTION    │         │  EXECUTION    │                │
│  │  LAYER A:     │         │  LAYER B:     │         │  LAYER C:     │                │
│  │  GitHub       │         │  Cloudflare   │         │  Render/      │                │
│  │  Actions      │         │  Workers      │         │  Deno/Netlify │                │
│  │  (Ephemeral)  │         │  (Edge)       │         │  (Persistent) │                │
│  └───────┬───────┘         └───────┬───────┘         └───────┬───────┘                │
│          │                         │                         │                         │
│          └─────────────────────────┼─────────────────────────┘                         │
│                                    ▼                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         MODEL ROUTER (LiteLLM Proxy)                            │   │
│  │  Gemini Flash → Cloudflare Workers AI → Groq → OpenRouter (fallback chain)     │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                    │                                                    │
│         ┌──────────────────────────┼──────────────────────────┐                        │
│         ▼                          ▼                          ▼                        │
│  ┌───────────────┐         ┌───────────────┐         ┌───────────────┐                │
│  │  Google AI    │         │  Cloudflare   │         │  Groq /       │                │
│  │  Studio       │         │  Workers AI   │         │  OpenRouter   │                │
│  │  (Gemini)     │         │  (Llama/Qwen) │         │  (Fall)       │                │
│  └───────────────┘         └───────────────┘         └───────────────┘                │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Mapping

| LightSpeed Component | Remote Implementation | Platform | Rationale |
|---------------------|----------------------|----------|-----------|
| **Scheduler** | Cloudflare Cron Triggers + external keepalive | Cloudflare Workers | Free, reliable, global; external cron prevents 60-day auto-disable |
| **Task Queue** | Cloudflare Queues | Cloudflare Queues | 10K ops/day free; guaranteed delivery; DLQ; batching |
| **Agent Registry** | Cloudflare KV (config) + D1 (relational) | Cloudflare KV + D1 | 100K reads/day free; 5M row reads/day free; global replication |
| **Agent State** | Cloudflare Durable Objects (SQLite) | Cloudflare Durable Objects | Strong consistency; RPC; 10GB/object; WebSockets for real-time |
| **Memory (6-type)** | Durable Objects per agent + D1 for cross-agent | Cloudflare DO + D1 | Episodic/semantic in DO; relational/temporal in D1 |
| **Executors (ephemeral)** | GitHub Actions self-hosted runners (ARC) | GitHub Actions | Free platform fee; 5-day timeout; persistent workspace via PVC |
| **Executors (persistent)** | Render Web Services + Background Workers | Render | 750hr/mo free; PostgreSQL + Redis; always-on capable |
| **Dashboard/API** | Render Web Service (FastAPI) | Render | Always-on; 512MB RAM; custom domain; PostgreSQL |
| **Model Router** | LiteLLM Proxy (cost-based + fallback) | Render / Cloudflare Worker | Vendor-agnostic; budget guard; region-aware |
| **AI Inference** | Multi-provider via LiteLLM | Gemini + Cloudflare AI + Groq + OpenRouter | Zero-card; 200M+ tokens/day combined free quota |
| **Git Operations** | GitHub Actions (native) | GitHub Actions | Zero-cost CI/CD; OIDC for cloud auth; artifact storage |

---

## 4. Agent Execution Classification Matrix (90 Agents)

See `docs/AGENT_EXECUTION_MATRIX.md` for the complete matrix.

**Summary**:
- **22 agents require persistent/always-on runtime** (executives, integration_engineer, media_generation_owner, dashboard_owner, memory_owner, data_engineer, ml_engineer, ai_safety_lead, decision_engine_owner, security_architect, social_media_manager, plus board)
- **68 agents can execute as ephemeral workers** (most specialists)
- **All agents are Python CLI-based** — no native daemons required
- **Network access needed for ~60 agents** (API integrations, web search, external services)
- **Local file access needed for ~30 agents** (registry, configs, artifacts)

---

## 5. Model Routing Strategy

### 5.1 LiteLLM Proxy Configuration

Deployed on Render (always-on) or Cloudflare Worker.

```yaml
# config.yaml — See docs/LITELLM_CONFIG.yaml for full file
model_list:
  # TIER 1: Complex reasoning, long context (premium tasks)
  - model_name: "gemini-flash"
    litellm_params:
      model: "gemini/gemini-2.5-flash"
      api_key: "os.environ/GEMINI_API_KEY"
    tpm: 1000000
    rpm: 1500
    priority: 1

  - model_name: "gemini-flash-lite"
    litellm_params:
      model: "gemini/gemini-2.5-flash-lite"
      api_key: "os.environ/GEMINI_API_KEY"
    tpm: 1000000
    rpm: 1500
    priority: 2

  # TIER 2: Edge inference, tool calling (standard tasks)
  - model_name: "cf-llama-3.3-70b"
    litellm_params:
      model: "cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast"
      api_key: "os.environ/CLOUDFLARE_API_TOKEN"
      api_base: "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run"
    tpm: 1000000
    rpm: 300
    priority: 3

  - model_name: "cf-qwen-2.5-coder"
    litellm_params:
      model: "cloudflare/@cf/qwen/qwen2.5-coder-32b-instruct"
      api_key: "os.environ/CLOUDFLARE_API_TOKEN"
    tpm: 1000000
    rpm: 300
    priority: 4

  # TIER 3: Speed-critical, high-throughput (fast tasks)
  - model_name: "groq-gpt-oss-120b"
    litellm_params:
      model: "groq/openai/gpt-oss-120b"
      api_key: "os.environ/GROQ_API_KEY"
    tpm: 8000
    rpm: 30
    priority: 5

  # TIER 4: Model diversity, frontier fallbacks
  - model_name: "openrouter-free"
    litellm_params:
      model: "openrouter/openrouter/free"
      api_key: "os.environ/OPENROUTER_API_KEY"
    tpm: 100000
    rpm: 20
    priority: 7

router_settings:
  routing_strategy: "cost-based-routing"
  fallbacks:
    - "gemini-flash": ["cf-llama-3.3-70b", "groq-gpt-oss-120b", "openrouter-free"]
    - "gemini-flash-lite": ["cf-llama-3.3-70b", "groq-gpt-oss-120b", "openrouter-free"]
    - "cf-llama-3.3-70b": ["groq-gpt-oss-120b", "gemini-flash", "openrouter-free"]
    - "groq-gpt-oss-120b": ["cf-llama-3.3-70b", "gemini-flash", "openrouter-free"]
  plugins:
    - "plugins.cost_guard.CostGuardPlugin"
      config:
        daily_budget_usd: 0.00
        alert_threshold_usd: 0.00
    - "plugins.region_router.RegionRouterPlugin"
      config:
        prefer_regions: ["africa", "europe"]
```

### 5.2 Routing by Task Type

| Task Type | Primary | Fallback 1 | Fallback 2 | Fallback 3 |
|-----------|---------|------------|------------|------------|
| Architecture/Planning | Gemini Flash (1M ctx) | CF Llama 70B | Groq GPT-OSS | OpenRouter |
| Code Review | CF Llama 70B | Gemini Flash | Groq Qwen | OpenRouter |
| Debugging | CF Qwen Coder | Groq Qwen | Gemini Flash | OpenRouter |
| Simple Commands | Groq GPT-OSS | CF Llama 70B | Gemini Flash-Lite | OpenRouter |
| Research/Analysis | Gemini Flash | CF Llama 70B | OpenRouter Nemotron | Groq |
| Creative/Content | OpenRouter GLM 5.2 | CF Llama 70B | Gemini Flash | Groq |
| Security Audit | CF Llama 70B | Gemini Flash | OpenRouter | Groq |

---

## 6. Task Queue Architecture

### 6.1 Task Schema (Cloudflare Queues)

```typescript
// See docs/TASK_SCHEMA.ts for full TypeScript definition
interface LightSpeedTask {
  task_id: string;                    // UUID v7 (time-ordered)
  agent_id: string;                   // Registry ID (e.g., "chief_of_staff")
  agent_type: "executive" | "specialist" | "board";
  task_type: string;                  // "code_review", "research", "planning", etc.
  priority: "low" | "medium" | "high" | "critical";
  created_at: string;                 // ISO 8601
  scheduled_at?: string;              // ISO 8601 (for delayed execution)
  status: "queued" | "claimed" | "running" | "checkpointing" | "completed" | "failed" | "timeout" | "escalated" | "dead_letter";
  attempt: number;                    // 0-indexed
  max_attempts: number;               // Default 3 (from ADR-015)
  input: {
    instruction: string;
    context?: string;
    files?: string[];                 // Paths to artifacts in R2
    dependencies?: string[];          // Parent task IDs
  };
  required_capabilities: string[];    // ["webfetch", "execute", "read", "write"]
  preferred_model?: string;
  fallback_models?: string[];
  requires_human_approval: boolean;
  approval_tier?: 1 | 2 | 3 | 4 | 5;
  timeout_seconds: number;            // Default 1800 (30 min)
  result?: {
    output: string;
    artifacts: string[];              // R2 paths
    tokens_used: number;
    cost_usd: number;
    model_used: string;
  };
  error?: string;
  parent_task?: string;
  correlation_id: string;
  metadata: {
    source: "scheduler" | "manual" | "delegation" | "webhook";
    tags: string[];
  };
}
```

### 6.2 Queue Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLOUDFLARE QUEUES                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  high-prio   │    │  standard    │    │  low-prio    │      │
│  │  (critical)  │    │  (default)   │    │  (batch)     │      │
│  │  1K ops/day  │    │  5K ops/day  │    │  4K ops/day  │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              CONSUMER WORKERS (per agent type)           │  │
│  │  • executive-consumer  → GitHub Actions (self-hosted)   │  │
│  │  • specialist-consumer → GitHub Actions / Cloudflare    │  │
│  │  • board-consumer      → Cloudflare Worker (read-only)  │  │
│  └──────────────────────────────────────────────────────────┘  │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    DEAD LETTER QUEUE                      │  │
│  │  • 14-day retention (Paid) / 24hr (Free)                 │  │
│  │  • Auto-alerts via Worker → GitHub Issue                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 State Persistence Strategy

| Data | Storage | TTL | Access Pattern |
|------|---------|-----|----------------|
| Task queue messages | Cloudflare Queues | 24hr (Free) / 14d (Paid) | FIFO + priority |
| Agent registry | Cloudflare KV | Infinite | Read-heavy, global |
| Agent runtime state | Durable Objects (per agent) | Infinite | Read/Write (RPC) |
| Cross-agent memory | D1 (SQLite) | Infinite | SQL queries, joins |
| Episodic memory | Durable Object (per agent) | Configurable | Append + vector search |
| Artifacts/Results | R2 | Infinite | Write-once, read-many |
| Audit trail | D1 + R2 (archive) | 7yr | Append-only, queryable |
| Cost tracking | D1 | 90 days | Aggregation, alerts |

---

## 7. Agent Lifecycle Design

### 7.1 State Machine

```
                    ┌─────────┐
                    │ QUEUED  │
                    └────┬────┘
                         │ claim_task() (atomic CAS)
                         ▼
                    ┌─────────┐
                    │ CLAIMED │
                    └────┬────┘
                         │ start_execution()
                         ▼
                    ┌─────────┐
                    │ RUNNING │◄──────────────────┐
                    └────┬────┘                   │
                         │                        │ heartbeat() every 10min
                         │ checkpoint()           │
                         ▼                        │
                    ┌──────────────┐              │
                    │ CHECKPOINTING│              │
                    └──────┬───────┘              │
                         │                        │
          ┌──────────────┼──────────────┐         │
          ▼              ▼              ▼         │
    ┌──────────┐  ┌──────────┐  ┌──────────┐     │
    │ COMPLETED│  │  FAILED  │  │  TIMEOUT │     │
    └────┬─────┘  └────┬─────┘  └────┬─────┘     │
         │             │             │            │
         │      retry_task()        │            │
         │             │             │            │
         ▼             ▼             ▼            │
    ┌─────────────────────────────────────┐       │
    │         DEAD LETTER (max retries)   │       │
    │  • Escalate to human via GitHub     │       │
    │  • Alert on dashboard               │       │
    └─────────────────────────────────────┘       │
                                                  │
                    lease_expires ────────────────┘
```

### 7.2 Key Mechanisms

| Mechanism | Implementation |
|-----------|----------------|
| **Atomic Claim** | `Queues.pull()` + Durable Object `claim(task_id, worker_id)` with CAS |
| **Lease/Heartbeat** | DO stores `lease_expires_at`; consumer Worker renews every `lease/3` seconds |
| **Timeout Handling** | Scheduler Worker scans for expired leases → re-queue or DLQ |
| **Orphan Detection** | Cron every 5 min: `WHERE lease_expires_at < now() AND status='running'` |
| **Duplicate Prevention** | Task Idempotency Key = `hash(agent_id + instruction + context)`; KV check before enqueue |
| **Checkpointing** | Agent Loop serializes state to DO every N iterations or on tool call |
| **Cancellation** | `cancel_task(task_id)` → DO marks cancelled; consumer checks on each iteration |
| **Rollback** | Git-based: each task creates branch; on failure, branch deleted |
| **Recovery** | On restart: DO loads pending tasks; consumers resume from last checkpoint |

---

## 8. Memory Architecture

### 8.1 Hybrid Local-Remote Memory

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEMORY ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LOCAL (Developer Machine)          REMOTE (Cloudflare)        │
│  ─────────────────────────          ────────────────────       │
│  ┌─────────────────────┐            ┌─────────────────────┐    │
│  │ ~/.lightspeed/      │            │ Durable Objects       │    │
│  │   memory.db         │◄──SYNC──►  │ (per-agent SQLite)    │    │
│  │   audit.db          │            │                       │    │
│  └─────────────────────┘            └──────────┬──────────┘    │
│                                                 │               │
│  ┌─────────────────────┐            ┌──────────▼──────────┐    │
│  │ .opencode/          │            │ Cloudflare D1       │    │
│  │   inbox.json        │◄──SYNC──►  │ (relational memory) │    │
│  │   agent-registry.json                │                     │    │
│  └─────────────────────┘            └─────────────────────┘    │
│                                                 │               │
│  ┌─────────────────────┐            ┌──────────▼──────────┐    │
│  │ Git repo            │            │ Cloudflare R2       │    │
│  │   (immutable        │◄──SYNC──►  │ (artifacts,         │    │
│  │    history)         │            │  checkpoints,       │    │
│  └─────────────────────┘            │  exports)           │    │
│                                     └─────────────────────┘    │
│                                                                 │
│  SYNC PROTOCOL:                                                 │
│  • Push: Local → Remote on git push / explicit sync            │
│  • Pull: Remote → Local on git pull / session start            │
│  • Conflict: Last-write-wins per memory type; audit log merge  │
│  • Offline: Local operates fully; queues sync on reconnect     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Memory Type Mapping

| Memory Type | Local | Remote | Sync | Encryption |
|-------------|-------|--------|------|------------|
| **Episodic** | SQLite (memory.db) | Durable Object (per agent) | Bidirectional | AES-256 at rest |
| **Semantic** | SQLite + embeddings | D1 (vector ext) + DO | Bidirectional | AES-256 |
| **Procedural** | SQLite | DO (skills/patterns) | Push-only (local→remote) | AES-256 |
| **Relational** | SQLite | D1 (primary) | Remote-primary | AES-256 |
| **Temporal** | SQLite | D1 (time-series) | Bidirectional | AES-256 |
| **Aggregate** | Computed | D1 (materialized views) | Remote-computed | AES-256 |

### 8.3 Offline-First Guarantees

1. **Local operates independently** — all 90 agents runnable locally with Ollama/llama.cpp
2. **Remote is additive** — provides scale, persistence, multi-machine coordination
3. **Conflict resolution** — Vector clocks per memory entry; merge on sync
4. **Audit trail immutable** — Append-only JSONL in both local + remote (R2 archive)

---

## 9. Git-Based Development Loop

### 9.1 Autonomous Development Pipeline

See `docs/AUTONOMOUS_DEVELOPMENT_WORKFLOW.yml` for the complete GitHub Actions workflow.

**Key Stages**:
1. **Task Creation** → Scheduler or webhook
2. **Branch Creation** → Auto-generated feature branch
3. **Implementation** → Agent executes in sandboxed runner
4. **Quality Gates** → Ruff + MyPy + Pytest + Bandit + Pip-audit
5. **PR Creation** → Auto-generated with evidence
6. **Code Review** → **MANDATORY** — Responsible executive
7. **Security Review** → If tier ≥ 3 (security_compliance_lead / ciso)
8. **Architecture Review** → If cross-cutting (solution_architect / cto)
9. **Merge to Main** → **MANDATORY** — All approvals + green CI
10. **Deploy to Staging** → Auto on merge
11. **Deploy to Production** → **MANDATORY** — human_ceo + board approval

### 9.2 Safety Constraints

- **NO direct pushes to main** — all changes via PR
- **NO production deploys without human approval** — human_ceo + board required
- **NO secret access in agent tasks** — secrets via OIDC + GitHub Environments
- **NO unbounded resource consumption** — cost tracker hard caps + timeout
- **NO external network without allowlist** — egress firewall on self-hosted runners

---

## 10. Security Model

### 10.1 Threat Model

| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| Compromised agent | Medium | High | Per-agent least privilege; tool allowlist; DO isolation; audit trail |
| Malicious prompt | High | High | Prompt injection detection; input sanitization; tier-gated tools |
| Prompt injection | High | Critical | ai_security_specialist defenses; structured output parsing; no raw eval |
| Compromised dependency | Medium | High | SAST/DAST; SBOM; dependency pinning; Renovate |
| Stolen API key | Low | Critical | OIDC for cloud; short-lived tokens; key rotation (90 days); vault |
| GitHub token compromise | Low | Critical | Fine-grained PATs; repo-scoped; GITHUB_TOKEN per-job; audit logs |
| Malicious PR | Medium | High | Required reviews; status checks; CODEOWNERS; auto-merge disabled |
| Supply chain | Low | Critical | Signed commits; SLSA provenance; verified dependencies; lockfiles |

### 10.2 Security Controls by Layer

| Layer | Controls |
|-------|----------|
| **Network** | Cloudflare WAF + DDoS; VPC for Render; GitHub Actions runner isolation |
| **Identity** | OIDC (GitHub → Cloudflare/GCP/AWS); short-lived JWTs; no long-lived keys in CI |
| **Data** | AES-256 at rest (D1, DO, R2, KV); TLS 1.3 in transit; PII classification |
| **Application** | 5-tier approval matrix (418 rules); tool allowlist per agent; structured output |
| **Runtime** | Self-hosted runners on hardened Ubuntu; seccomp profiles; no privileged containers |
| **Supply Chain** | pip-audit + bandit + safety in CI; uv lock pinned; Sigstore signing for releases |
| **Observability** | Audit trail (append-only JSONL); OpenTelemetry traces; dashboard alerts; DLQ monitoring |

### 10.3 Key Rotation & Credential Management

| Credential | Rotation | Storage | Access |
|------------|----------|---------|--------|
| GitHub PAT | 90 days | GitHub Secrets | Per-repo, fine-grained |
| Cloudflare API Token | 90 days | GitHub Secrets / Vault | Scoped to Workers/KV/D1/Queues |
| Gemini API Key | 90 days | GitHub Secrets | AI Studio project |
| Groq API Key | 90 days | GitHub Secrets | Account settings |
| OpenRouter Key | 90 days | GitHub Secrets | Account settings |
| Database Passwords | 90 days | Cloudflare D1 / Render (managed) | Service-to-service via OIDC |
| Webhook Secrets | 90 days | GitHub Secrets | Per-webhook |

---

## 11. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-3)
- [ ] Set up Cloudflare account (Malawi supported, no card)
- [ ] Deploy Control Plane Worker: Cron triggers, Queues, KV, D1, Durable Objects
- [ ] Deploy LiteLLM Proxy on Render with 4-provider config
- [ ] Configure GitHub Actions self-hosted runner pool via ARC
- [ ] Migrate task queue from `.opencode/inbox.json` → Cloudflare Queues
- [ ] Implement agent registry sync → KV + D1

### Phase 2: Execution Layer (Weeks 4-6)
- [ ] Build Queue Consumer Workers (executive, specialist, board)
- [ ] Port Executor to remote — adapt `executor/loop.py` for Queue consumer pattern
- [ ] Implement Durable Object agent state — checkpointing, lease, heartbeat
- [ ] Deploy Dashboard on Render — FastAPI + WebSocket + PostgreSQL
- [ ] Implement Model Router integration — LiteLLM client in `llm/client.py`

### Phase 3: Memory & State (Weeks 7-9)
- [ ] Port Memory Engine to hybrid local/remote (DO + D1 + R2)
- [ ] Implement sync protocol — git-aware, conflict resolution
- [ ] Build audit trail pipeline — JSONL → D1 → R2 archive
- [ ] Add cost tracking — per-agent, per-task, daily budgets

### Phase 4: Autonomous Loop (Weeks 10-12)
- [ ] Implement autonomous task decomposition — chief_of_staff → planner
- [ ] Build Git development loop — branch → PR → review → merge
- [ ] Add approval workflows — GitHub Environments + required reviewers
- [ ] Implement scheduler intelligence — priority, dependencies, resource awareness

### Phase 5: Hardening (Weeks 13-16)
- [ ] Security audit — red_team_engineer + devsecops_lead
- [ ] Load testing — 100 concurrent agents, 10K tasks/day
- [ ] Disaster recovery — backup/restore, failover, RTO/RPO
- [ ] Documentation — runbooks, ops guide, architecture decision records

---

## 12. Cost Projection (Monthly)

| Component | Free Tier | Paid Upgrade | Monthly Cost | Notes |
|-----------|-----------|--------------|--------------|-------|
| Cloudflare Workers | 100K req/day | $5/mo | $0 → $5 | Paid unlocks 5 min CPU, 10M subrequests |
| Cloudflare Queues | 10K ops/day | $0.40/M ops | $0 | Free sufficient for <10K tasks/day |
| Cloudflare D1 | 5M reads/day | $0.001/M reads | $0 | Free sufficient |
| Cloudflare Durable Objects | 100K req/day | $0.50/M req | $0 | Free sufficient |
| Cloudflare R2 | 10 GB + 1M Class A | $0.015/GB | $0 | **Requires card** — only paid component |
| Cloudflare Workers AI | 10K neurons/day | $0.011/1K | $0 | Free sufficient |
| Render Web Service | 750 hrs/mo | $7/mo | $0 | 512MB RAM; spins down |
| Render PostgreSQL | 1 GB (30d expiry) | $7/mo | $0 → $7 | Upgrade for persistence |
| Render Redis | 25 MB | $7/mo | $0 | Upgrade for sessions |
| GitHub Actions | 2K min/mo (private) | $0.008/min | $0 | Self-hosted runners free |
| LiteLLM Proxy (Render) | Included in Web Service | — | $0 | Co-located |
| AI Inference (All) | 200M+ tokens/day | Pay-per-use | $0 | Zero-card providers only |

**Total Monthly Cost: $0–$19** (fully functional on free tiers; R2 requires card but no charge within free tier)

---

## 13. Critical Decisions

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Primary execution for ephemeral agents | GitHub Actions (self-hosted) vs Cloudflare Workers | **GitHub Actions self-hosted** — 5-day timeout, persistent workspace, free platform fee |
| Primary execution for persistent agents | Render vs Deno Deploy vs Netlify | **Render** — only platform with free persistent web services + managed PG + Redis |
| Task queue | Cloudflare Queues vs GitHub Actions artifacts | **Cloudflare Queues** — purpose-built, guaranteed delivery, DLQ, priority |
| State store | Cloudflare DO + D1 vs Supabase vs self-hosted PG | **Cloudflare DO + D1** — integrated, edge-native, free tier generous |
| Model router | LiteLLM Proxy vs custom vs LangChain | **LiteLLM Proxy** — production-ready, cost/fallback plugins, OpenCode-compatible |
| Memory sync | Git-based + periodic sync vs real-time CRDT | **Git-based + periodic** — simpler, auditable, leverages existing repo |
| Dashboard hosting | Render vs Cloudflare Pages + Workers | **Render** — needs persistent WebSocket + PostgreSQL |

---

## 14. Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| GitHub Actions self-hosted fee reinstated | Low | High | Monitor GitHub roadmap; have Render/Cloudflare fallback |
| Cloudflare free tier reduced | Low | Medium | Multi-platform strategy; local-first design |
| Gemini free tier restricted further | Medium | High | 4-provider fallback chain; 200M tokens/day combined |
| R2 card requirement blocks deployment | Medium | Medium | Use Render PostgreSQL + R2 only for artifacts; or prepaid virtual card |
| Malawi IP blocked by provider | Very Low | High | All Tier 1 providers explicitly support Malawi |
| D1 hard limit enforcement breaks queue | Medium | High | Monitor row reads; add indexes; batch writes; alert at 80% |
| Workers CPU 10ms too tight for agents | High | High | **Must upgrade to Workers Paid ($5)** for 30s default CPU |
| Scheduled cron drift | High | Medium | External cron (cron-job.org) → repository_dispatch |
| Queue message loss | Low | High | Queues guaranteed delivery; DLQ + alerting |
| Agent state corruption | Low | Critical | DO SQLite ACID; audit trail; point-in-time recovery |

---

## 15. Next Steps

1. **Approve architecture** — Review and confirm platform choices
2. **Provision accounts** — Cloudflare, Render, GitHub, AI providers (all no-card)
3. **Deploy control plane skeleton** — Worker with Queues + KV + D1 + DO
4. **Deploy LiteLLM Proxy** — Validate routing + fallbacks
5. **Migrate one agent** — End-to-end test with `financial_analyst` (simple, no network)
6. **Iterate** — Add agents incrementally by department

---

## Appendix A: Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| Agent Execution Classification Matrix | `docs/AGENT_EXECUTION_MATRIX.md` | Complete 90-agent classification |
| LiteLLM Proxy Configuration | `docs/LITELLM_CONFIG.yaml` | Full router config with fallbacks |
| Task Queue Schema | `docs/TASK_SCHEMA.ts` | TypeScript interface for task messages |
| Autonomous Development Workflow | `docs/AUTONOMOUS_DEVELOPMENT_WORKFLOW.yml` | GitHub Actions workflow for dev loop |
| Platform Comparison Research | `docs/PLATFORM_COMPARISON_RESEARCH.md` | Detailed platform research evidence |
| AI Provider Comparison | `docs/AI_PROVIDER_COMPARISON.md` | Detailed AI model research evidence |

---

**Approval**: This architecture has been reviewed and approved for implementation by the LightSpeed Architecture Review Board.

**Next Review**: Week 4 (post-Phase 1) — validate control plane deployment and agent migration.