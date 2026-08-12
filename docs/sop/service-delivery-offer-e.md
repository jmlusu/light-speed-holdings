# Service Delivery SOP — Offer E: Platform Licensing

**Document ID:** SOP-SVC-E-001
**Department:** Product / Marketing (shared)
**Owner:** cpo
**Classification:** Internal
**Last Updated:** 2026-08-12
**Offer Code:** E — Platform Licensing (AI Company Builder)

---

## 1. Purpose

Defines the delivery process for Offer E: licensing the AI Company Builder platform
to other founders and agencies. This is the high-margin, scalable product path.
The platform software already exists — the work is packaging, onboarding, and support.

## 2. Scope

Applies to all client engagements tagged `offer-e` in `.opencode/inbox.json`.

## 3. Roles & Agent Assignment

| Role | Agent | Responsibility |
|------|-------|----------------|
| Engagement Lead | human_ceo | Final approval, contract signing |
| Product Ownership | cpo | Platform roadmap, feature priorities |
| Licensing Sales | growth_product_manager | License sales, pricing |
| Developer Relations | head_of_developer_relations | Partner onboarding, community |
| Documentation | technical_documentation_lead | User guides, API reference |
| Developer Experience | developer_experience_engineer | Onboarding flow, CLI ergonomics |
| Legal | legal_owner | License agreement, ToS amendment |
| Marketing | product_marketing_manager | Go-to-market, positioning |
| Support | customer_success_owner | Licensee support, knowledge base |

## 4. Delivery Pipeline

```
1. Lead → 2. Demo & Proposal → 3. Contract → 4. Onboarding Task →
   5. Platform Delivery → 6. Training → 7. Ongoing Support
```

### Step-by-step

1. **Lead** — `head_of_developer_relations` captures lead; `product_marketing_manager`
   qualifies.
2. **Demo & Proposal** — `growth_product_manager` demonstrates the platform; sends
   license proposal (E1: one-time fee + monthly support).
3. **Contract** — `legal_owner` drafts license agreement; `human_ceo` approves; client signs.
4. **Onboarding Task** — `human_ceo` creates inbox.json task tagged `offer-e`,
   `client-<id>`, `requires_approval=True`.
5. **Platform Delivery** — `developer_experience_engineer` packages a deployable
   registry subset (branded for the licensee); `technical_documentation_lead`
   customizes docs.
6. **Training** — `head_of_developer_relations` delivers 2-hour onboarding session
   (live + recording). `developer_experience_engineer` provides CLI walkthrough.
7. **Ongoing Support** — `customer_success_owner` handles ticket escalation;
   `developer_experience_engineer` monitors feedback for platform improvements.

## 5. Pricing & Payment

| Deliverable | Currency | Price |
|-------------|----------|-------|
| E1 — AI Company Builder license | USD $2,000 one-off + $200/mo | |
| E2 — White-label agency setup | Custom quote | |

**Payment:** Full license fee upfront via bank transfer. Monthly support billed in advance.

## 6. Platform Packaging Workflow

The license deliverables are generated FROM the platform's own service work:
1. The `data_engineer`/`business_intelligence_engineer` dashboard configs built for
   Offer C clients become template registries in the license package.
2. The `frontend_engineer`/`product_designer` website configs become starter templates.
3. The `legal_owner` MSA/SOW templates become licensee-facing agreements.

This creates the reinforcement loop: client service revenue proves the platform,
and the proven configs become license SKUs.

## 7. Quality Standards

- Licensee registry subset must validate cleanly (`ai-company validate`).
- Onboarding must achieve first-agent invocation within 30 minutes.
- `developer_experience_engineer` tracks time-to-first-success metric.

## 8. Post-Delivery

- 30-day intensive support window, then standard monthly support.
- `head_of_developer_relations` checks in at 7, 30, and 90 days.
- `growth_product_manager` tracks licensee expansion (additional agents, modules).
- `ai_ethics_board_chair` reviews platform improvements for safety implications.
