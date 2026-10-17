# ADR-020: Pharos Content Intelligence — Build Internal Loop + Consume Eden MCP Probe + Expose Own MCP

**Status:** Proposed
**Date:** 2026-09-13
**Deciders:** Human CEO, CTO, CMO, CSO, Thought Leadership Lead
**Technical Domain:** Marketing / Technology (Thought Leadership + Content Operations)

## Context

Eden.so (`eden.so`) is the *content brain for creators*: outlier-scored post
research across 7 platforms, a Meta/TikTok ad library, creator/brand study,
swipe-file boards, an AI research chat, scheduled Routines, an MCP server
(`https://mcp.eden.so/mcp`) that gives any MCP-capable agent "eyes on social",
cross-platform scheduling, and analytics.

LightSpeed's Pharos engine (`docs/Pharos/`) must produce 50 thought-leadership
articles/yr, a weekly 3-post cadence (Mon Agentic Enterprise Brief / Wed Build
Log / Fri AI Policy & Governance Africa), a monthly Malawi Agentic AI Monitor,
and 2,000+ newsletter subscribers — for an **institutional SADC audience**
(ministries, SADC secretariat, UNDP/UNESCO-ROSA, banks, ICTAM), who are moved by
evidence, citation, and policy input, not viral hooks.

A four-specialist review (competitive intel, market research, content-engine
alignment, CTO) concluded: Eden optimizes the US creator economy and its corpus
has near-zero SADC/policy coverage — **do not buy it as a research tool** — but
its *architecture* is the strongest current proof that exposing an organizational
capability over **MCP** is the right distribution wedge for an agentic-AI
company, and its Routines/save-then-chat/outlier patterns map 1:1 onto LightSpeed
infrastructure the company already owns (daemon scheduler, message-bus, memory
engine, knowledge graph).

We need a governed content-intelligence loop (research → draft in the CEO's
voice → publish → measure) that (1) runs on existing LightSpeed infra as thin
extensions, (2) borrows Eden patterns without inheriting its data moat or its
consumer persuasion mechanics, and (3) doubles as a "Use Cases" proof and a
Lighthouse pilot product ("agentic content operations for institutions").

## Decision

### 1. Build "Pharos Content Intelligence" as the internal content loop (3 phases)

- **P0 — Foundation:** a `routine:` cycle type in `config/company/scheduler.yaml`
  fired by the existing daemon scheduler loop (`src/ai_company/executor/daemon.py`,
  same cadence code as `kpi_snapshot`); each fire enqueues a **fresh** Task via
  `src/ai_company/orchestrator/message_bus.py` with a `routine_run_id` for
  idempotency; `AgentLoop` runs the Pharos agent, stores episodic memory +
  knowledge-graph upsert, writes a report to `results/`, emails the result.
  Research sources are webfetch-only at P0 (no new vendor). Extend
  `src/ai_company/dashboard/kpis/marketing.py` with content-performance
  collectors (post counts, engagement, subscriber growth vs the 2,000-target).
- **P1 — Core loop:** Deep-research routines; CEO voice profile (semantic +
  relational memory) for voice-preserving drafting; reverse-engineer + Boost
  batch fan-out over the message-bus; publishing rails for LinkedIn/Substack
  (buy-side — no platform API churn in-house); content-performance dashboards;
  Whisper transcription (local-first).
- **P2 — Scale:** Expose the **Pharos Content Intelligence MCP** (read-only →
  gated write); regional Malawi/SADC corpus collectors feeding the monthly
  Monitor; pared-down board/tracker workspace for per-pillar evidence libraries;
  package the capability as a Lighthouse pilot offer.

Adopt five Eden **patterns**: (1) Routines on the daemon, (2) MCP-as-distribution,
(3) save-then-chat with citation-grounded synthesis, (4) outlier scoring against
each voice's own baseline, (5) reverse-engineer + Boost. **Never adopt** Eden's
Auto-DM/Instagram automation, TikTok-first rails, ad library as a content
engine, or creator commerce — they corrode the trust-by-engineering positioning
with institutional audiences.

### 2. Consume Eden MCP only as a global-creator trend probe (optional, flagged)

Register `https://mcp.eden.so/mcp` as a research tool inside AgentLoop behind a
feature flag. Purpose: pattern inspiration / global hook-format signals for
Pharos writers. Rule: **never cite Eden corpus as SADC evidence**; anything
cited must pass a regional verification pass (`k-dense-research-lookup` +
webfetch). Keep a webfetch fallback so the loop degrades gracefully — Eden is an
accelerator, never the backbone.

### 3. Expose a Pharos Content Intelligence MCP (`src/ai_company/mcp/server.py`)

Mirror Eden's design but source from LightSpeed stores:

- Tools: `knowledge_graph_query` (GraphEngine), `memory_recall` (MemoryStore
  semantic recall), `research_lookup` (regional corpus), `pharos_reference`
  (indexed `docs/Pharos/*`), `publish_queue` (write, gated).
- Security: authenticate via existing RBAC (`src/ai_company/security/rbac.py`)
  X-API-Key roles — `run` = read-only research tools; `approve` = queue/publish.
  **Read-only exposure first** — an MCP surface is a data-exfiltration vector;
  write tools behind `approval.py` gates. Outputs pass content filter + PII
  guard; every call audit-logged (`audit/writer.py`).

### 4. Execution governance

Track as an ECL change (`harness/changes/active/`) with a plan-review gate
before implementation; record validation per phase (ruff/mypy/pytest). The team
uses valid roster `subagent_type`s per `docs/agents/pharos-agent-mapping.md`
(e.g., `thought-leadership-lead`/`thought-leadership-author` via `content-writer`,
`agentic-research-lead` via `general`) plus `cto`, `head-of-competitive-intelligence`,
`market-analyst`, `cmo`, `community-ecosystem-builder`.

## Consequences

- **Positive:** Pharos cadence moves from manual/blank-page to evidence-backed
  automated research briefs; the MCP surface is both internal enablement and a
  demo of the company-builder thesis; building the loop is itself a flagship
  "Use Cases" case study; ~$950/yr saved vs Eden Pro licensing with a
  misaligned data moat.
- **Negative / risk:** Regional data freshness is the chief credibility risk
  (localized evidence is scarce and pricey) — mitigated by the regional
  verification pass and never citing Eden as SADC evidence; routine API costs
  compound — mitigated by per-routine `budget_tokens`, `standard` model tier
  default, `cost_tracker.py` budgets; single-daemon scheduler reliability —
  mitigated by idempotent `routine_run_id`, DLQ reuse, UTC+2 (Malawi) handling.
- **Neutral:** No schema change to `CompanyRegistry`; no new top-level CLI; a
  publish queue is bought, not built.

## Alternatives Considered

- **Buy Eden Pro ($79/mo) as the Pharos research tool:** Rejected — corpus is
  US creator-economy with negligible SADC/policy coverage; the outperformance
  signal is irrelevant to citation/institutional influence; consumer persuasion
  mechanics would blur the lighthouse positioning.
- **Build a 3M-post-scale competitor corpus:** Rejected — that is Eden's
  proprietary data moat and the least relevant part; LightSpeed needs a *curated*
  regional corpus (dozens of accounts + policy feeds), not millions of posts.
- **Full Eden-style UI (canvas boards, Readwise sync, DM automation) in-house:**
  Rejected — UI-heavy build with no institutional payoff; only table/tracker
  workspaces survive.

## Links

- `docs/eden-review-plan.md` — full review (feature taxonomies, alignment
  matrix, skills, team, risks) this ADR implements.
- `docs/Pharos/README.md`, `content-calendar.md`, `roadmap.md` — cadence and
  targets the loop serves.
- `docs/agents/pharos-agent-mapping.md` — valid delegation aliases.
- `config/company/scheduler.yaml` — routine cycle host (P0).
- `src/ai_company/executor/daemon.py` — scheduler loop.
- `src/ai_company/orchestrator/message_bus.py` — fresh-task-per-run.
- `src/ai_company/security/rbac.py` — MCP authz; `audit/writer.py` — audit.
- ADR-012 (RBAC), ADR-017 (suspend store), ADR-019 (memory/knowledge
  governance — pattern for MCP read surface).
- Evidence: ECL change `pharos-content-intelligence-p0` (P0: routine engine +
  content KPIs + daily research loop).
