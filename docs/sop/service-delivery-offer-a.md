# Service Delivery SOP — Offer A: Digital Presence

**Document ID:** SOP-SVC-A-001
**Department:** Marketing / Technology (shared)
**Owner:** cmo
**Classification:** Internal
**Last Updated:** 2026-08-12
**Offer Code:** A — Digital Presence (websites, brand, content, automation)

---

## 1. Purpose

Defines the end-to-end delivery process for Offer A client engagements: business websites, e-commerce stores, brand identity kits, and Google Business listings. All work is delivered through the AI Company Builder platform and requires human_ceo review before client handoff.

## 2. Scope

Applies to all client engagements tagged `offer-a` in `.opencode/inbox.json`.

## 3. Roles & Agent Assignment

| Role | Agent | Responsibility |
|------|-------|----------------|
| Engagement Lead | human_ceo | Final approval gate, client sign-off |
| Brand Strategy | brand_strategist | Brand identity, color systems, fonts |
| Content | content_writer | Copywriting, SEO content, blog posts |
| Product Design | product_designer | UI/UX wireframes, visual design |
| Frontend | frontend_engineer | HTML/CSS/JS implementation, hosting setup |
| Growth | growth_hacker | Post-launch growth setup, analytics |
| QA | qa_engineer | Automated checks + manual review |

## 4. Delivery Pipeline

```
1. Client Brief → 2. Scope & Quote → 3. Intake Task → 4. Build → 5. Review → 6. QA → 7. Deliver
```

### Step-by-step

1. **Client Brief** — `client` CLI sub-app creates a client record + SOW. Gates G1–G4 checked (see client-onboarding-policy.md).
2. **Scope & Quote** — `product_designer` drafts wireframes; `content_writer` drafts copy outline; `human_ceo` approves scope and sends quotation.
3. **Intake Task** — `human_ceo` creates inbox.json task tagged `offer-a`, `client-<id>`, `requires_approval=True`.
4. **Build** — `product_designer` and `frontend_engineer` build the site; `content_writer` fills content; `brand_strategist` creates brand kit.
5. **Review** — `human_ceo` performs final review gate against the SOW checklist.
6. **QA** — `qa_engineer` runs automated checks (link validation, mobile responsiveness, form tests).
7. **Deliver** — Final files + 30-day support window opened. `support_agent` handles post-delivery questions.

## 5. Pricing & Payment

| Deliverable | Currency | Price |
|-------------|----------|-------|
| A1 — Business Website | MWK 800,000 (≈$450) || A2 — E-commerce Store | MWK 1,800,000 (≈$1,000) || A3 — Brand Identity | MWK 500,000 (≈$280) || A4 — Google Business | MWK 150,000 (≈$85) |

**Payment:** 50% upfront via Airtel Money/TNM Mpamba, 50% on delivery. Ad spend and third-party licensing (domain, hosting) are pass-through.

## 6. Quality Standards

- All websites: mobile-first, ≤10-day turnaround, contact form + WhatsApp button, hosting setup.
- All brand kits: color system + fonts + social media kit + letterhead.
- `qa_engineer` verifies: links work, mobile responsive, forms submit, analytics installed.

## 7. Post-Delivery

- 30-day support window included. `support_agent` handles questions.
- `content_creator` and `growth_hacker` provide optional retainers for ongoing content/social management.
- Postmortem recorded: `support_agent` logs client feedback to episodic memory.
