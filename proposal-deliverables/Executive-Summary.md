# Executive Summary

**For the attention of:** VillageReach — CHOICE Project Team, Malawi

**From:** Light Speed Holdings — Jack Mlusu, USSD Consultant
**Subject:** USSD Consultant — CHOICE Project. Design, Deployment & 24-Month Managed Service of an SRHR Information and Feedback Service on Short Code 54747 (Malawi)
**Re:** Technical & Financial Proposal dated 2026-09-17

---

## The Engagement

This proposal responds to VillageReach's requirement for a USSD Consultant to design, deploy and manage a USSD module on short code **54747** that delivers sexual and reproductive health and rights (SRHR) information and a structured feedback channel for low-literacy users in Malawi, under the **CHOICE Project**.

We propose a **4-week rapid setup** followed by a **24-month managed service** (total engagement value **USD 45,000**). This is a design–deploy–manage engagement: its products are a working USSD service, an integration to the VillageReach data warehouse, a validated user acceptance test, and a governed, measurable 24-month service — not a research-only consultancy.

## Why USSD, Why Now

USSD is the lowest-barrier, lowest-literacy digital channel available to Malawian users across TNM and Airtel:
- **Universal reach** — works on every feature phone ever sold; no data plan, app installation or smartphone required.
- **Real-time and free to the end-user** — the session begins immediately and costs the caller nothing.
- **Private in form** — handset sessions do not persist content in an inbox visible to family members, reducing stigma risk for sensitive SRHR topics.
- **Trackable** — every session can be logged and aggregated for measurement and continuous improvement.

## What We Will Deliver

- **Two service paths** on short code 54747 (provisioned on both TNM and Airtel via a single aggregator): an **Info** path of staged, plain-language SRHR content and a **Feedback** path of structured capture — number-driven, ≤182 characters per screen, max four levels deep, with a "99. Main menu" escape on every screen and a clear referral ("For urgent help, dial 54747", **no callback**).
- **A privacy-by-design data pipeline**: every session is logged and forwarded by a REST API to the VillageReach data warehouse, with the phone number **hashed and salted at the edge** so the warehouse receives anonymous session records, not personal content — consistent with the Malawi Data Protection Act (2024), with idempotent delivery, a dead-letter queue, and daily reconciliation.
- **Validated user acceptance**: facilitated UAT with **≥20 feature-phone users** across Lilongwe and Balaka (VillageReach organises participants; we facilitate), gated on ≥90% task completion before go-live.
- **A governed service regime**: **≥99% uptime**, **4-hour response** during Malawian working hours (08:00–17:00) with 24-hour escalation for short-code outages, **up to 4 menu updates per 12 months**, and **monthly reports by the 5th** of each month.
- **Handover-ready operations**: documentation, training and a 24-Month Completion Report so the client or a successor operator can take the service over at any point.

## The Investment

| Component | USD |
|-----------|-----|
| Phase 1 — Setup & Development (4 weeks) | $13,350 |
| Phase 2 — Maintenance & Support (24 months) | $25,633 |
| Reimbursables (travel, testing SIMs, UAT incentives) | $1,926 |
| Subtotal | $40,909 |
| Contingency (10%) | $4,091 |
| **Total engagement value** | **$45,000** |

**≈ USD 1,875 per month all-in** (USD 45,000 ÷ 24 months). Payment follows the agreed **40/20/40 schedule** aligned to VillageReach cash flow: **40% at signing, 20% at go-live, 40% in monthly installments** across the maintenance period.

## Why Light Speed Holdings

The service is led by **Jack Mlusu (USSD Consultant)** and backed by an in-house specialist team with existing aggregator relationships — so short code 54747 is provisioned once, recovers fast, and is run measurably (uptime, response times, completion rates and feedback themes are instrumented and reported monthly). We treat every SRHR session as sensitive by default and build the service to be handed over cleanly. We look forward to confirming the scope with the VillageReach CHOICE team and beginning the 4-week setup window.

---

*Prepared by Light Speed Holdings, Lilongwe. For the complete technical approach, work plan, deliverables, risk management and financial details, see the accompanying proposal.*
