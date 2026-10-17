# ADR-027: Public vs Internal Boundary

**Status:** Accepted
**Date:** 2026-09-24
**ECL:** LightSpeed AI Company Builder + Web Experience Architecture v2.0
**Cross-refs:** [PUBLIC_INTERNAL_BOUNDARY.md](../../PUBLIC_INTERNAL_BOUNDARY.md), [PUBLIC_AGENT_REGISTRY_SCHEMA.md](../../PUBLIC_AGENT_REGISTRY_SCHEMA.md), ADR-012, ADR-013, ADR-019

## Context

Discovery (2026-09-24) found the public SPA importing the full internal agent registry: `guidelines` (private operating instructions), `permission: "Execute"`, legacy tool names, and internal ops fixtures (tasks, approvals, escalations, raw KPI series, cost internals) all entered the client bundle via `src/data/companyData.ts`. No build-time public transform existed (violations V1–V5). The internal AI operating system (registry, inbox, approvals, memory, dashboard, CI) must never share a trust boundary with the untrusted internet.

## Decision

1. **Layer model (deny by default):**

   - **Public experience** — Vercel SPA, untrusted.
   - **Public-safe data** — allowlisted, build-time artifact only.
   - **Client platform** — `src/` Vite bundle; imports only public-safe modules.
   - **Internal AI OS** — registry YAML/JSON full fields, orchestrator, dashboard (RBAC), memory, security, CI.

   Arrows never cross INTERNAL → PUBLIC except through the **public transform**.

2. **NEVER-EXPOSE list (non-exhaustive, deny-by-default):** secrets/credentials; `guidelines` / system prompts / card bodies; permission levels and tool grant flags; unrestricted approval bypasses; task/inbox/approval/escalation payloads; raw KPI current/target/history; live cost/model-tier internals; raw memory; audit log entries; sensitive infra topology; dashboard RBAC keys and session tokens.

3. **EXPOSE-OK allowlist only** (fields enumerated in `PUBLIC_AGENT_REGISTRY_SCHEMA.md` §3): `id`, `name`, `title`, `type`, `department`, `reports_to` display, `mission`, curated `responsibilities`, tool **names** (canonical 7 only), KPI **labels** only, derived counts (90/20). Anything not listed is DENY.

4. **Public transform is mandatory** before any public surface renders agent data (roadmap: P2 before P3/P4 agent-data surfaces). Build-time, not runtime API filter.

5. **Governance tiers** for the 90-agent org remain internal: Tier 0–1 autonomous; Tier 2 human gate; Tier 3 two-person; Tier 4 CEO only. Public site holds zero dashboard keys.

## Alternatives

| Option | Why not |
|--------|---------|
| Do nothing (full registry public) | Ships private instructions + permission model to any visitor |
| Hand-curated public JSON | Drifts immediately from 90/20 SoT |
| Runtime API filter | Adds network surface, latency, mutable post-deploy artifact; still needs schema gate |
| Filter only in React components | Bundle still contains forbidden strings; type system keeps `guidelines`/`permission` on `Agent` |
| **Build-time allowlist transform** | **Chosen** — deterministic, CI-gateable, immutable per deploy, deny-by-default |

## Rationale

- Matches existing pipeline shape (YAML → JSON → cards); transform is one more deterministic stage.
- `additionalProperties: false` + denylist greps make regressions loud in CI.
- Aligns with ADR-012/013 (keys and tokens stay server-side/network-bound) and ADR-019 (raw memory internal).
- PII/content filter can run as final egress check on the serialized public artifact.

## Consequences

- Follow-on ECL must: implement transform; swap `companyData.ts` to public artifact only; CI-fail any `src/**` import of `company/agent-registry.json`; split ops fixtures out of `src/data/`.
- Schema tests assert 90 agents / 20 departments and zero forbidden keys (`guidelines`, `permission`, `model_tier`, `initialTasks`, `approval_level`, `escalation_path`, `DASHBOARD_`, `API_KEY`, `llm_cost`, legacy tools).
- Until implementation lands, V1–V5 remain **open violations** tracked in the boundary doc — docs-only change does not close them.
