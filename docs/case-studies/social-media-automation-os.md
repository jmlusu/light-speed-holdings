# Case Study — Social Media Automation OS (Client Build Engagement)

**Document ID:** CASE-SMAOS-001
**Author:** program-manager / solution-architect synthesis
**Owner:** consulting-lead
**Classification:** Internal / Sales Enablement — client identity shared only as agreed
**Date:** 2026-09-12
**Status:** IMPLEMENTATION COMPLETE — client engagement, all five waves
delivered; final gates green on 2026-09-12 (typecheck 0, contract tests
110/110, Python analytics 12 pass / 1 opt-in skip, consistency PASS, health
OK). Pending client handover (git baseline commit + release/CI setup).

**Honesty badge:** Client engagement in progress. No deliverables shipped to a
live audience yet; "fieldable in 2026" refers to the client's operating system,
not to LightSpeed production use. No fabricated metrics, testimonies, or client
logos. Client repo and internal docs are separate workspaces; nothing in this
file discloses client-proprietary secrets.

---

## 0. Engagement Guardrails (Read First)

- **Separate identity:** We are the delivery partner. We do **not** become part
  of the client's company. No LSH agents, registry internals, dashboards, or
  internal platform details are introduced into the client repository.
- **Scope-limited sharing:** Only SMA-OS engineering content (architecture,
  code, docs, scripts) enters client deliverables. LightSpeed process details
  that touch the client's work are described as delivery practice, never as LSH
  internal tooling internals.
- **No secrets:** Client platform credentials are env-only (`client/.env`),
  never committed. Mock/dry-run adapters require none.
- **Ownership:** The client repo remains the client's property; LightSpeed
  delivers implementation + documentation services against a fixed script
  contract, and this case study records the engagement for LSH's portfolio
  only.

---

## 1. Problem / Baseline

The client holds a **scaffolded but unimplemented** self-hosted, free-tier,
event-driven **Social Media Automation Operating System** (CREATE → APPROVE →
PUBLISH → ANALYZE). At intake:

- **Implemented:** `@sma/core` package (12 modules + `ai/` — Router/Writer/QA
  agents, Ollama client, deterministic fallbacks), 9 DB migrations
  (001–009 incl. vector), 6 runtime configs (brand, frequency, image-presets,
  model-routing, platform-matrix, platform-rules), 18 prompt files across 6
  platforms + QA + learning, 7 JSON schemas, full `.env.example` contract.
- **Missing (build scope ≈ 100% of application layer):** `apps/api` (Fastify),
  `apps/worker` (event choreography), `apps/dashboard` (static UI while API is
  running), `adapters/` (mock → real platform adapters), `tests/` (unit,
  integration, e2e, chaos, python), `scripts/` (bootstrap, health-check,
  consistency, analytics, media, publishing, utils), `infrastructure/`
  (postgres, ollama, minio, n8n), `docs/`, `assets/`.
- **Baseline number:** `pnpm typecheck`/`test` on the scaffold would fail —
  entry files referenced by scripts (`apps/api/src/index.ts`,
  `apps/worker/src/index.ts`, `scripts/consistency/index.ts`,
  `scripts/health-check.mjs`, `scripts/bootstrap.ps1`) do not exist.

## 2. Agentic Approach

The OS itself runs a content pipeline of AI agents: **Router → Strategist →
Writer → Editor → QA**, each with Ollama-first execution and a deterministic
offline fallback engine (AI_MODE `auto | ai | off`), validated against JSON
schema. LightSpeed's delivery of it is organized as an agent team mapped to
workstreams:

| Workstream | LSH Agent | Charter |
|------------|-----------|---------|
| Engagement lead | `program-manager` | milestone tracking, wave gating, status to operator |
| Solution architecture | `solution-architect` | end-to-end blueprint, seams, build order |
| API | `senior-backend-engineer` | Fastify app, routes, validation, dashboard static hosting |
| Backend support | `backend-engineer` | persistence wiring, repos, error paths |
| Platform adapters | `integration-engineer` | `Adapter` contract + mock adapters → real (LinkedIn, Meta/IG/FB, Threads, YouTube, Buffer, X) |
| Data & analytics | `data-engineer` | metrics collectors, learning tables, analytics scripts |
| LLM orchestration | `llm-platform-owner` | Ollama health, model-routing bind, fallback purity |
| Prompt binding | `prompt-engineer` | bind `prompts/` YAML/MD files into agent prompts |
| Pipeline choreography | `workflow-owner` | CREATE→APPROVE→PUBLISH→ANALYZE state machine in worker |
| Dashboard | `senior-frontend-engineer` | minimal static dashboard served by the API |
| UX contract | `product-designer` | dashboard UX, approval UX |
| QA strategy | `qa-lead` | test pyramid, fallback-vs-AI parity checks |
| Test engineering | `test-engineering-lead` | unit/integration/e2e (tsx --test, Node ≥22) |
| Security | `security-architect` | secrets hygiene, basic auth, adapter credential envelopes |
| Infra/platform | `devops-lead` | bootstrap, health-check, consistency, docker-compose (postgres/ollama/minio/n8n) |
| Observability | `observability-engineer` | structured logs, `/health`, metrics endpoints |
| Documentation | `technical-documentation-lead` | client README, API reference, ops runbook |
| Boundary review | `data-privacy-officer` | confirms no client/LSH data fusion, no PII leakage |

**Skills applied (LSH org):** spec-driven-development (blueprint),
planning-and-task-breakdown + incremental-implementation (waves),
tdd (worker/API flows), api-endpoint-builder, security-and-hardening,
ci-cd-and-automation (bootstrap/consistency/health), observability-and-instrumentation,
designing-frontend-interfaces, code-review-and-quality + brooks-lint + logic-lens
(pre-delivery gate), karpathy-guidelines + ponytail (keep the free-tier build
lean), ls-documentation-engineering, using-git-worktrees (isolation),
reservations-playbook (case-study honesty framing).

## 3. Measurable Outcome (Targets)

- **`pnpm typecheck`** green under `tsconfig.base.json` (strict).
- **`pnpm test`** green: unit + integration + e2e suites; `pnpm test:python` for
  the Python analytics layer.
- **`pnpm check:consistency`** green (config/schema/prompt drift detection).
- **`pnpm health`** returns healthy status against live API + DB + Ollama (auto).
- **Offline guarantee:** full pipeline runs with `AI_MODE=off` on deterministic
  engines (repeatable tests, zero network, free tier).
- **Supported platforms:** LinkedIn, Meta (Instagram/Facebook), Threads, YouTube,
  Buffer (with X via Buffer), plus mock/dry-run adapters for every slot.

## 4. Governance and Auditability

- Delivery follows the LSH client-onboarding posture: engagement recorded,
  boundary documented, secrets-classification applied (PII-free; platform
  credentials env-only).
- Every adapter exposes a credential envelope; publish attempts without
  credentials fail in **dry-run/mock** mode, never silently.
- Client repo CI gates mirror the Qa-agent contract: JSON-schema validation on
  every AI output; falls back, never fabricates.
- No LSH internal data leaves the LSH workspace into client deliverables.

## 5. Reuse Note

- The **Adapter Contract** + **deterministic fallback engine** pattern are
  directly reusable for any social/content automation project (SME, media,
  donor comms).
- The **free-tier, offline-first posture** answers reservation #1
  (low-bandwidth/resource-constrained) and #2 (data protection — local
  inference, sovereignty by default) of the Trust-by-Engineering doctrine.
- This engagement is the first **external build** recorded in the portfolio —
  the FOW-02 (enterprise automation) and FOW-03 (consulting delivery backbone)
  scenario shape, applied to a client's repo.

---

## 6. Build Plan (Waves)

1. **Blueprint** — solution-architect writes `docs/implementation-plan.md` in
   the client repo (module inventory, adapter interface, wave order, acceptance).
2. **Wave 1 — Foundations:** apps/api skeleton (Fastify + dashboard static
   mount), apps/worker event loop (CREATE→APPROVE→PUBLISH→ANALYZE states),
   apps/dashboard shell, Adapter contract + mock adapters, bootstrap/health
   scripts, test harness scaffolding.
3. **Wave 2 — Endpoints & pipeline:** content/approval/publish/analytics routes,
   worker processing steps (router→writer→QA→human gate), persistence repos.
4. **Wave 3 — Adapters & AI:** platform adapters with credential envelopes,
   prompt binding, model-routing wiring.
5. **Wave 4 — Quality & docs:** full unit/integration/e2e + python suites,
   consistency checks, README/API/ops docs, infra compose.
6. **Gate:** typecheck + full test + health green; `code-review-and-quality`
   audit; operator sign-off before client handover.

*Milestone/gate details and acceptance criteria live in the client-repo
blueprint; this file records only the engagement.*

*End of case study. Honest, boundary-respecting, evidence-traceable.*
