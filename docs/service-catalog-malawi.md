# Light Speed Holdings — Malawi Service Catalog

**Version:** 1.0 (draft for validation)
**Date:** 2026-08-12
**Owner:** human-ceo
**Status:** PROPOSED — pricing anchors to be validated with 2–3 real prospects before publishing

---

## 1. Positioning

Light Speed Holdings operates as an **AI-first services studio** in Malawi. One human
CEO directs a workforce of **127 AI agents** (executives, engineers, designers, writers,
analysts, sales, support) to deliver client work through a defined delivery pipeline:

```
client brief → inbox task → assigned agent(s) → human CEO review → client deliverable
```

This lets us deliver enterprise-grade output at a fraction of traditional agency cost
and speed. We win on **speed, cost, and 24/7 capacity**, not on claiming to be human-heavy.

> **Currency reality:** Malawi runs a dual-currency market. Price in **USD for
> NGO/international clients** (they pay in USD) and **MWK for local SMEs/businesses**
> (paid via Airtel Money / TNM Mpamba). Anchor rates must be validated against the
> current interbank + parallel market before quoting.

---

## 2. Offer Portfolio

### Offer A — Digital Presence (website + branding)

| Deliverable | What you get | Starting price | Turnaround |
|-------------|--------------|----------------|------------|
| **A1 — Business Website** | Up to 5 pages, mobile-first, contact form, WhatsApp button, hosting setup, 30 days support | MWK 800,000 (≈ $450) | 5–10 days |
| **A2 — E-commerce / Online store** | Product catalog, Airtel Money / Mpamba checkout integration, order notifications, 20 products | MWK 1,800,000 (≈ $1,000) | 10–15 days |
| **A3 — Brand identity** | Logo, color system, fonts, social media kit, letterhead | MWK 500,000 (≈ $280) | 3–5 days |
| **A4 — Google Business + listings** | Map listing, business info management, review setup | MWK 150,000 (≈ $85) | 2–3 days |

**Target clients:** local SMEs, schools, clinics, hotels/lodges, agri-businesses,
churches, real estate.

### Offer B — Business Process Automation (BPA)

| Deliverable | What you get | Starting price | Turnaround |
|-------------|--------------|----------------|------------|
| **B1 — WhatsApp/customer chatbot** | FAQ + order/service automation on WhatsApp Business, handoff to human, analytics dashboard | MWK 1,500,000 (≈ $850) + MWK 100,000/mo hosting | 7–14 days |
| **B2 — AI document/report generator** | Template-driven report generation (donor reports, payroll letters, certificates) | MWK 1,200,000 (≈ $680) | 7–14 days |
| **B3 — Form + survey automation** | Kobo/Google-Forms-to-spreadsheet pipeline, auto-alerts, summary dashboards | MWK 900,000 (≈ $500) | 5–10 days |
| **B4 — Internal tool / dashboard** | Custom web dashboard for tracking stock, sales, students, patients, or members | MWK 2,500,000 (≈ $1,400) | 10–20 days |

**Target clients:** SMEs, clinics, schools, cooperatives, transport companies.

### Offer C — Data, Analytics & Donor Reporting (the differentiator)

| Deliverable | What you get | Starting price | Turnaround |
|-------------|--------------|----------------|------------|
| **C1 — Data cleaning & analysis** | Clean dataset + insights report (Excel/PDF) | MWK 700,000 (≈ $400) | 3–7 days |
| **C2 — Donor/project reports** | Narrative + data-visualized quarterly/annual reports compliant with donor templates | MWK 1,000,000 (≈ $550) | 5–10 days |
| **C3 — Interactive dashboard** | Live web dashboard for program KPIs (mobile-friendly, NGO-grade) | MWK 2,000,000 (≈ $1,100) | 10–15 days |
| **C4 — Survey design + analysis** | Questionnaire design, data collection setup, analysis, recommendations | MWK 1,300,000 (≈ $720) | 7–14 days |

**Target clients:** NGOs, development programs, UN agencies, cooperatives, research orgs.
**Pricing note:** international NGOs expect USD quotes and pay in USD — quote these at
the USD figure directly with terms (50% upfront, 50% on delivery).

### Offer D — Digital Marketing

| Deliverable | What you get | Starting price | Turnaround |
|-------------|--------------|----------------|------------|
| **D1 — Social media management** | Content calendar, 12 posts/month (Chichewa + English), community management | MWK 350,000/mo (≈ $200/mo) | Ongoing |
| **D2 — Content pack** | 10 blog articles + 20 social captions | MWK 600,000 (≈ $340) | 5–10 days |
| **D3 — Google/Facebook ads setup** | Campaign setup, pixel, tracking, 2-week optimization | MWK 700,000 (≈ $400) + ad spend | 3–5 days |

### Offer E — Platform (product path)

| Deliverable | What you get | Price | Turnaround |
|-------------|--------------|-------|------------|
| **E1 — AI Company Builder license** | One-on-one onboarding, your own 127-agent company running on your laptop/VPS | MWK 3,500,000 (≈ $2,000) one-off + MWK 350,000/mo (≈ $200/mo) support | Setup 1–2 weeks |
| **E2 — Agent setup for agencies** | White-label: we stand up agent teams for your agency's clients | Contact for quote | — |

**Target clients:** tech-savvy founders, local agencies, diaspora entrepreneurs.

---

## 3. Pricing Rules

1. **50% upfront / 50% on delivery** for all one-off projects. Retainers billed monthly in advance.
2. **USD quotes** for NGO/international clients. **MWK quotes** for local clients.
3. All prices exclude **ad spend** and **third-party licensing** (hosting, domain, LLM usage, payment gateway fees).
4. Valid for 30 days. Scope creep = change order at MWK 60,000 (≈ $35)/hour.
5. **Express delivery** (≤50% of standard turnaround) = +40%.

---

## 4. Payment Rails (Malawi)

| Method | Notes |
|--------|-------|
| **Airtel Money** | Preferred for local SMEs; instant; merchant number required. |
| **TNM Mpamba** | Preferred for local SMEs; instant; merchant number required. |
| **PayChangu** | Card + mobile money gateway for online checkout (integrates with websites/stores). |
| **Bank transfer** | Required for NGO/international contracts (USD or MWK). |
| **Invoice flow** | Send PDF invoice via email before payment; receipt after payment. NGO clients often need an official quotation + proforma. |

> **Operationalize:** create one standard invoice template + one quotation template,
> and a simple payment tracker (who owes what). This is the first thing the
> `sales-owner` + `cfo` agents should be given to run.

---

## 5. Delivery Model (how the 127 agents actually work)

| Step | What happens | Who/What |
|------|--------------|----------|
| 1. Brief | Client request captured as a task in `.opencode/inbox.json` | human-ceo |
| 2. Scope & quote | Proposal drafted, sent for client approval | solutions-engineer / sales |
| 3. Kickoff | Task assigned to the right agent(s) via dashboard or CLI | human-ceo / chief-of-staff |
| 4. Build | Agents produce the deliverable in the repo (site, report, dashboard, content) | content-writer, frontend-engineer, data-engineer, etc. |
| 5. Review | human-ceo reviews against the brief; revisions loop | human-ceo |
| 6. QA | Automated checks + manual review before handoff | qa-engineer |
| 7. Deliver | Client package (files/links + invoice) sent | human-ceo |
| 8. Support | 30 days included support; postmortem + case study recorded | support-agent, cto |

**Rule:** no client-facing deliverable goes out without human-ceo review. Agents
draft and execute; the human owns the outcome.

---

## 6. Legal & Compliance Checklist (Malawi)

- [ ] Register company with **Registrar General** (Business Registration Act).
- [ ] Obtain **MRA Taxpayer Identification Number (TIN)**; register for VAT if turnover threshold met.
- [ ] Open business bank account (MWK + USD).
- [ ] Set up **Airtel Money merchant** and **TNM Mpamba merchant** accounts.
- [ ] Confirm **PayChangu** (or alternative) onboarding for card payments.
- [ ] Publish client **terms of service + privacy policy** (own site).
- [ ] Comply with **Data Protection Act 2017**: appoint data controller responsibilities, get consent for personal data, restrict cross-border transfers without safeguards.
- [ ] Draft a standard **service agreement / MSA** template (legal agent to produce v1).
- [ ] Insurance: professional indemnity (optional at first, revisit at scale).

---

## 7. First 90 Days

| Phase | Focus | Milestone |
|-------|-------|-----------|
| **Weeks 1–2** | Prove the machine: real API keys, daemon running, dashboard live, 1 portfolio demo built by agents (e.g., a fictional clinic website) | Demo ready to show prospects |
| **Weeks 3–6** | Land 2 lighthouse clients: 1 local SME (Website or chatbot) + 1 NGO (reporting/analytics). Deliver with agents, under-promise/over-deliver. | 2 paid deliveries + 2 case studies |
| **Weeks 7–12** | Systematize: standard quote/invoice templates, payment tracker, delivery SOP; package Offer C as the flagship; publish content (English + Chichewa). | Repeatable pipeline + 5 testimonials |
| **Quarter 2** | Productize: package the reporting/dashboard offer as a product for NGOs; explore platform licensing (Offer E). | First recurring revenue contract |

---

## 8. Success Metrics

- **Revenue:** first MWK 5,000,000 (≈ $2,800) gross by day 90.
- **Delivery:** ≤ 10-day turnaround on all one-off offers; ≥ 4.5/5 client satisfaction.
- **Repeat:** ≥ 30% of month-2 revenue from returning clients.
- **Cost control:** total LLM + infra spend ≤ 10% of revenue.

---

*This catalog is the business definition the agent workforce runs against. It must be
reviewed with real market feedback and updated as pricing is validated.*
