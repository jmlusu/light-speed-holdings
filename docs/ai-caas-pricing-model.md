# AI Consulting-as-a-Service (AI-CaaS) — Pricing Model

**Document ID:** PRICE-AIC-001
**Owner:** cfo / sales (co-owned)
**Status:** PROPOSED — validate with 2–3 real consulting-firm prospects before publishing
**Date:** 2026-09-06
**Source case study:** `docs/case-studies/wlo-ai-native-consultancy.md`
**Source offers:** `config/company/ai_caas_offers.yaml`
**Registry template:** `company/registry-templates/consulting-firm/`

---

## 1. Why This Exists

**We Lead Out** proved that a ~7-person, AI-native consulting firm can deliver
enterprise work at a fraction of traditional cost and speed (5.0 client rating,
**4-week median** time to first value, 20+ deliveries). Light Speed Holdings
productizes that operating model into three revenue streams.

The core economic claim, from the WLO case study:

| Metric | Traditional | WLO model | AI-CaaS (LSH) |
|--------|------------|-----------|----------------|
| Team size | 5–8 consultants | 2–3 + AI | 1 human + agents |
| Time to value | 12–16 weeks | 4 weeks | 2–3 weeks |
| Engagement cost | $150–300K | $60–100K | $25–50K |
| Gross margin (est.) | 25–35% | 40–50% | 60–75% |

---

## 2. Offer F — WLO-in-a-Box (Platform License) — `offer-f`

Target: **consulting firms** (and agencies) that want to become AI-native
without building the stack. LSH licenses the consulting-firm template, agent
cards, and delivery workflows; the firm runs its own agent workforce.

### License tiers

| Tier | Included | Price |
|------|----------|-------|
| **Starter** | 1 firm registry, consulting + delivery workflows, 1 onboarding session, self-serve docs | $15K/yr + $250/mo |
| **Growth** | All Starter + white-label agent cards, custom departments, quarterly enablement, priority support | $30–50K/yr + $500/mo |
| **Enterprise** | Multi-practice hierarchy, custom workflows/SOPs, dedicated support, co-marketing options | Custom |

### What the firm gets

- `company/registry-templates/consulting-firm/` (validated, passes `load_registry`)
- Discovery → proposal → delivery → support workflows (9-workflow engine, SLA)
- 6-type memory so client knowledge and delivery patterns compound
- 5-tier human-in-the-loop approval gates + audit trail
- Training: 2-hour onboarding + recorded walkthrough (mirrors Offer E SOP)

### Numbers

- Target: 50 consulting firms, blend of Starter/Growth across FY2026–27
- At a 40/60 Starter/Growth mix: ~**$1.9–2.6M ARR**
- Licensee path: firm replaces junior billable hours with the agent workforce,
  converting overhead to margin — the value WLO proved

---

## 3. Offer G — Ghost Delivery (Per-Engagement) — `offer-g`

Target: **clients who want WLO outcomes without building anything.** LSH runs
the agent back-office; a human consultant coordinates delivery to the client.

### Engagement packages

| Package | Scope | Price |
|---------|-------|-------|
| **Discovery Sprint** | Interview agent + workflow mapping + opportunity identification + roadmap (the existing `ai-company consulting` pipeline) | $8–12K, 2 weeks |
| **Build Sprint** | Solution architecture + implementation of one deliverable (automation, dashboard, integration) | $15–25K |
| **Full Engagement** | Discovery + build + 30-day support (mirrors the `foaster_engagement` workflow) | $25–50K |

### Notes

- **Pricing rules** (inherited from Malawi catalog): 50% upfront / 50% on
  delivery; scope creep = change order; express ≤50% turnaround = +40%.
- Awareness: for the first deal, sell the case study — lead with a working
  deliverable, earn strategy after (WLO lesson #6).

---

## 4. Offer H — Managed AI Consultancy (Retainer) — `offer-h`

Target: firms/organizations that want a standing AI delivery capability.

| Tier | Included | Price |
|------|----------|-------|
| **Ops Retainer** | Ongoing delivery support, enhancement cycles, knowledge-base upkeep | $2–4K/mo |
| **Full Back-Office** | Ops Retainer + quarterly opportunity review + expansion roadmap | $5–8K/mo |

Recurring revenue engine aligned with the WLO Managed Support offering.
Customer net retention target: **≥120%** (project work converting to retainers).

---

## 5. Financial Guardrails

- **Cost control:** LLM + infra spend ≤ 10% of engagement revenue
  (guardrails.yaml default: $2/day, $0.50/task caps enforced by executor).
- **Margin floor:** reject engagements with < 55% modeled margin.
- **ARR target:** AI-CaaS contributes toward the FY2028–30 $10M ARR plan,
  with Offer E (platform licensing) and AI-CaaS sharing the licensing muscle.
- **Revenue-per-employee floor:** ≥ $300K by 2028 — sustained by agent leverage,
  not headcount.

---

## 6. Governance Gates to Ratify (before first client)

Same four policies as the Malawi portfolio, mirrored in `ai_caas_offers.yaml`:

1. **Client onboarding approval** — contract, DPA, compliance risk, CISO review
2. **Data handling protocol** — PII classification, encryption, access logging
3. **Ethics review** — Tier 3+ deliverables through the AI Ethics Board
4. **Service-level liability cap** — 100% of fees

Blocks: all three offers are `proposed` until the board ratifies.

---

## 7. Sales Narrative (the 30-second pitch)

> *"A 7-person consultancy in Melbourne delivers enterprise Salesforce work in
> 4 weeks with a 5.0 client rating — because AI does the repeatable work and
> experts do the judgment. We built the platform that makes that a template.
> License it, have us run it for you, or let us deliver for you. Pick one."*

---

## 8. Open Questions

- [ ] Validate price anchors with 2–3 real consulting-firm prospects
- [ ] Decide Starter/Growth feature cut for the first licensed firm
- [ ] Confirm liability/insurance posture for Ghost Delivery (operator vs. subcontractor)
- [ ] Ratify governance gates through the board
