# Service Delivery SOP — Offer D: Digital Marketing

**Document ID:** SOP-SVC-D-001
**Department:** Marketing
**Owner:** cmo
**Classification:** Internal
**Last Updated:** 2026-08-12
**Offer Code:** D — Digital Marketing (social media, content, ads)

---

## 1. Purpose

Defines the delivery process for Offer D client engagements: social media management,
content packs, and Google/Facebook ads setup. This is a commoditized but reliable revenue
stream for local SMEs.

## 2. Scope

Applies to all client engagements tagged `offer-d` in `.opencode/inbox.json`.

## 3. Roles & Agent Assignment

| Role | Agent | Responsibility |
|------|-------|----------------|
| Engagement Lead | human_ceo | Final approval |
| Marketing Strategy | cmo | Campaign strategy, positioning |
| Content | content_writer, content_creator | Copy, visuals, captions |
| Growth | growth_hacker | Funnel optimization, conversion |
| Analytics | market_analyst | Campaign performance, insights |
| UX Research | ux_research_lead | Audience research, feedback |
| QA | qa_engineer | Link checks, content review |
| Support | support_agent | Client communication |

## 4. Delivery Pipeline

```
1. Client Brief → 2. Scope & Quote → 3. Intake Task → 4. Build → 5. Review → 6. Deliver
```

### Step-by-step

1. **Client Brief** — `client` CLI sub-app creates client record + SOW.
2. **Scope & Quote** — `cmo` drafts campaign brief; `content_writer` outlines content plan.
3. **Intake Task** — `human_ceo` creates inbox.json task tagged `offer-d`, `client-<id>`,
   `requires_approval=True`.
4. **Build** — `content_writer` creates 12 posts/month + captions; `content_creator` designs
   visual assets; `growth_hacker` sets up campaign tracking.
5. **Review** — `human_ceo` reviews content for brand fit + accuracy.
6. **QA** — `qa_engineer` verifies links, image alt text, caption grammar.
7. **Deliver** — Client receives content calendar + assets + ad account access.
   `growth_hacker` monitors performance and provides monthly reports.

## 5. Pricing & Payment

| Deliverable | Currency | Price |
|-------------|----------|-------|
| D1 — Social Media Mgmt | MWK 350,000/mo | |
| D2 — Content Pack | MWK 600,000 | |
| D3 — Ads Setup | MWK 700,000 + ad spend | |

**Payment:** Monthly retainers billed in advance via Airtel Money/TNM Mpamba.
Ad spend is pass-through (client pays provider directly or reimburses).

## 6. Quality Standards

- Content adapted for local audiences.
- `ux_research_lead` validates audience targeting before campaign launch.
- `market_analyst` provides weekly performance report.

## 7. Post-Delivery

- Ongoing retainer model for D1 (social media management).
- `growth_hacker` optimizes campaigns based on weekly performance data.
- `content_writer` maintains content calendar continuity.
