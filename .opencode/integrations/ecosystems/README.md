# LightSpeed Holdings Limited — Ecosystems (Integration with Third-Parties)

## Overview

This document describes how LightSpeed Holdings Limited orchestrates and governs all
third-party integrations — strategic partnerships, platform ecosystems, client-facing
system connectors, and vendor contracts — through a dedicated agent team assembled from
the company registry.

The Ecosystems team is the umbrella owning:

- **Strategic integrations** — LLM provider partnerships, cloud platform alliances,
  operations deals (Jev / TypeSafe AI decision engine, Open Design creative stack,
  ComfyUI media pipeline).
- **Client system integrations (Offer B / Offer C)** — WhatsApp Business API, CRM sync,
  payment gateways (Airtel Money, TNM Mpamba, PayChangu), and NGO data sources
  (Kobo, DHIS2, Google Sheets).
- **Vendor and channel management** — external AI/ML providers, cloud infrastructure
  contracts, SLAs, and co-marketing deals.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   LightSpeed Ecosystem Layer                     │
├─────────────────────────────────────────────────────────────────┤
│  Business Development → Integration Engineer → QA Gate          │
│  (orchestrator)        (production)          (governance)       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Third-Party Integration Catalog                  │
├─────────────────────────────────────────────────────────────────┤
│  Jev/TypeSafe │ Open Design │ ComfyUI │ LLM Providers │ Client  │
│  (decision)    (creative)    (media)   (multi-route)   (B/C)    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Integration Standards & Governance               │
├─────────────────────────────────────────────────────────────────┤
│  API Standards │ Security │ Data Privacy │ BC/DR │ Vendor SLA   │
└─────────────────────────────────────────────────────────────────┘
```

## Team Composition

### Orchestrator
- **Head of Business Development** (`head-of-business-development`)
  - Owns outbound partnerships, ecosystem alliances, integration deals, and channel
    strategy
  - Negotiates integration and co-marketing deals with LLM providers and cloud platforms
  - Routes every third-party integration request to the right production agent
  - Applies the "multi-win or no-win" partnership bar

### Production Agents
| Agent | Department | Primary Output | Integration Use |
|-------|------------|----------------|-----------------|
| Integration Engineer | Technology | Client system connectors | WhatsApp, CRM, payment, NGO data |
| API Architect | Technology | API standards, gateway | Versioning, rate limiting, OpenAPI |
| Solution Architect | Technology | Cross-system design | End-to-end solutions, proposals |
| Vendor Manager | Operations | Provider contracts, SLAs | AI/ML + cloud vendor management |

### Support Agents
| Agent | Department | Role |
|-------|------------|------|
| Security & Compliance Lead | Security | 5-tier approval, CORS, auth as continuous checklist |
| Data Privacy Officer | Legal | GDPR/CCPA, DPA agreements, retention |
| Business Continuity Manager | Operations | BC/DR, failover, resilience testing |

## Integration Catalog

| Integration | Type | Owner | Status | Reference |
|-------------|------|-------|--------|-----------|
| Jev / TypeSafe AI | Decision engine | Head of Business Development | Active | `docs/adr/023-jev-system-one-integration.md` |
| Open Design | Creative production | Head of Business Development | Active | `.opencode/integrations/open-design/` |
| ComfyUI | Media generation | Media Generation Owner | Active | `docs/adr/018-comfyui-media-generation.md` |
| LLM providers (multi-route) | Model routing | LLM Platform Owner | Active | `docs/adr/004-llm-router.md` |
| WhatsApp Business API | Client channel | Integration Engineer | Offer B/C | registry `integration_engineer` |
| CRM sync | Client data | Integration Engineer | Offer B/C | registry `integration_engineer` |
| Payment gateways (Airtel Money, TNM Mpamba, PayChangu) | Client revenue | Integration Engineer | Offer B/C | registry `integration_engineer` |
| NGO data (Kobo, DHIS2, Google Sheets) | Client data | Integration Engineer | Offer C | registry `integration_engineer` |

## Integration Workflow

### 1. Intake
The Head of Business Development qualifies the integration request:
1. **Partner/integration type** — strategic, client-facing, or vendor
2. **Business case** — what must it enable
3. **Data surface** — what data crosses the boundary
4. **Contract/SLA** — terms, cost, liability
5. **Compliance gate** — privacy, security, continuity review needed

### 2. Routing
| Integration Says | Production Agent | Handoff To |
|------------------|------------------|------------|
| New partner / alliance / co-marketing | Head of Business Development | corporate-development-lead (build-vs-buy) |
| Client system connector | Integration Engineer | api-architect |
| API surface / gateway | API Architect | integration-engineer |
| Cross-system architecture | Solution Architect | api-architect, integration-engineer |
| Vendor contract / SLA / cost | Vendor Manager | cfo (budget), clo (legal) |

### 3. Governance Gates
Before any third-party integration ships, the support agents must sign off:

- **Security & Compliance Lead**: approval-tier gating, dashboard CORS/auth, deny-by-default
- **Data Privacy Officer**: GDPR/CCPA, DPA agreements, data minimization, retention enforced
- **Business Continuity Manager**: every critical integration has a failover plan

The Integration Engineer enforces three standing integration laws:
> Every integration has a fallback. Data sync is idempotent. Integration failures
> escalate to HITL before client impact.

### 4. Implementation
```bash
# Via OpenCode (using Head of Business Development orchestrator)
opencode --agent head-of-business-development \
  "Stand up WhatsApp Business API integration for the OI pilot; route to integration-engineer"

# Inspect the integration catalog
cat .opencode/integrations/ecosystems/config.json
```

### 5. QA & Compliance
- **Contract QA**: SLA, liability, DPA in place before data flows
- **Security QA**: tier gating, deny-by-default, auth enforced
- **Continuity QA**: failover tested, RTO committed
- **Data QA**: minimization, retention, right-to-deletion wired

## Configuration Files

| File | Purpose |
|------|---------|
| `.opencode/integrations/ecosystems/config.json` | Ecosystem integration config |
| `.opencode/integrations/ecosystems/team.json` | Team composition |
| `.opencode/integrations/ecosystems/agent-config.yaml` | Agent-level integration config |
| `.opencode/integrations/ecosystems/README.md` | This guide |
| `.opencode/integrations/ecosystems/QUICK-REFERENCE.md` | Quick reference |

## Quick Start

### 1. Invoke the Team
```bash
opencode --agent head-of-business-development \
  "The OI pilot needs a WhatsApp + Airtel Money integration. Coordinate the Ecosystems team."
```

### 2. Route Through the Catalog
Every third-party integration enters through the catalog in `config.json`. Do not start
an integration without an owner and a governance gate.

### 3. Standards First
Open `.opencode/integrations/ecosystems/QUICK-REFERENCE.md` for the routing table and
escalation paths before beginning work.

## References

- Agent Registry: `company-registry.yaml`
- Jev Integration ADR: `docs/adr/023-jev-system-one-integration.md`
- Jev Brief: `JEV_INTEGRATION_BRIEF.md`
- Open Design Package: `.opencode/integrations/open-design/`
- ComfyUI ADR: `docs/adr/018-comfyui-media-generation.md`
- Org Chart: `company/org-chart.md`