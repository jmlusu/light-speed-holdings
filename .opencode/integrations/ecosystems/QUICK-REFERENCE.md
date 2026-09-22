# LightSpeed Holdings Limited — Ecosystems Quick Reference

## Team Roster

### Orchestrator
| Agent | Role | Department | Key Skills |
|-------|------|------------|------------|
| `head-of-business-development` | Outbound partnerships, ecosystem alliances, integration deals, channel strategy | Business Development | Negotiation, partnership strategy, build-vs-buy coordination |
| `corporate-development-lead` | M&A, acqui-hire, build-vs-buy decisions | Strategy | Deal modeling, strategy analysis |

### Production Agents
| Agent | Role | Department | Key Skills |
|-------|------|------------|------------|
| `integration-engineer` | WhatsApp Business API, CRM sync, payment gateways (Airtel Money, TNM Mpamba, PayChangu), NGO data (Kobo, DHIS2, Google Sheets) | Technology | API integration, idempotent sync, fallback design, HITL escalation |
| `api-architect` | API standards, versioning, rate limiting, gateway config | Technology | OpenAPI, REST design, rollout strategy |
| `solution-architect` | End-to-end cross-system solutions | Technology | System design, integration patterns, proposal architecture |
| `vendor-manager` | External AI/ML + cloud contracts, SLA compliance | Operations | Vendor evaluation, SLA negotiation, cost oversight |

### Support Agents
| Agent | Role | Department | Key Skills |
|-------|------|------------|------------|
| `security-compliance-lead` | 5-tier approval rules, dashboard CORS lockdown, auth as continuous checklist | Security | Deny-by-default, tier gating, CORS allowlists |
| `data-privacy-officer` | GDPR/CCPA, data classification, retention, DPAs, right-to-deletion | Legal | Privacy by design, data minimization, DPA management |
| `business-continuity-manager` | BC/DR, resilience testing, failover procedures | Operations | RTO commitments, DR drills, failover design |

## Integration Catalog (Memorize)

| Integration | Type | Owner | Governance Gate |
|-------------|------|-------|-----------------|
| Jev / TypeSafe AI | Decision engine | Head of Business Development | Security + Continuity |
| Open Design | Creative production | Head of Business Development | Brand (ls-design-system) |
| ComfyUI | Media generation | Media Generation Owner | Security |
| LLM providers (multi-route) | Model routing | LLM Platform Owner | Privacy (DPAs) |
| WhatsApp Business API | Client channel | Integration Engineer | Privacy + Continuity |
| CRM sync | Client data | Integration Engineer | Privacy |
| Airtel Money / TNM Mpamba / PayChangu | Client revenue | Integration Engineer | Security + Continuity |
| Kobo / DHIS2 / Google Sheets | NGO data | Integration Engineer | Privacy |

## Routing Table (Memorize)

| Request | Route To |
|---------|----------|
| New partner / alliance / co-marketing deal | `head-of-business-development` |
| Build-vs-buy / M&A evaluation | `corporate-development-lead` |
| Client system connector (WhatsApp, CRM, payments, NGO) | `integration-engineer` |
| API surface, versioning, gateway | `api-architect` |
| Cross-system architecture / proposal | `solution-architect` |
| Vendor contract / SLA / cost | `vendor-manager` |
| Approval-tier / CORS / auth | `security-compliance-lead` |
| GDPR/CCPA / DPA / retention | `data-privacy-officer` |
| Failover / DR / resilience | `business-continuity-manager` |

## Integration Laws (Memorize)

1. Every integration has a fallback.
2. Data sync is idempotent.
3. Integration failures escalate to HITL before client impact.

## Escalation Path

```
Integration failure → integration-engineer → solution-architect → HITL (human CEO)
Vendor/contract breach → vendor-manager → corporate-development-lead → cfo
Security/privacy incident → support owner → ciso/clo → HITL
```

## Invocation

```bash
opencode --agent head-of-business-development \
  "Stand up WhatsApp Business API integration for the OI pilot; route to integration-engineer"
```

## Key Files

- Catalog: `.opencode/integrations/ecosystems/config.json`
- Team: `.opencode/integrations/ecosystems/team.json`
- Agent config: `.opencode/integrations/ecosystems/agent-config.yaml`
- Guide: `.opencode/integrations/ecosystems/README.md`