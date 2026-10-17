# Malawi Agentic AI Monitor — Monthly Plan

**Owner:** Pharos Thought Leadership (via Content Writer)
**First issue:** #1 — The State of Agentic AI in Malawi (September 2026)
**Slots on record:** `docs/Pharos/content-calendar.md` — 7 planned monthly issues through 2027.

---

## 1. Cadence

| Item | Value |
|------|-------|
| Frequency | Monthly, one edition per calendar month |
| Issue #1 | September 2026 (this month) |
| Planned issue sequence | per `docs/Pharos/content-calendar.md`: (1) State of Agentic AI in Malawi, (2) 10 High-Value Agentic AI Use Cases, (3) How Malawi Banks Should Prepare for AI Agents, (4) AI Agents in Government, (5) Governance of Autonomous AI Systems, (6) The Economics of AI Employees, (7) The Four Reservations — Trust-by-Engineering |
| Publication target | First full week of the month (warm-up protocol permits manual sends only until 2026-10-03 — see `docs/marketing/warmup-log.md`) |
| Format | `monitor-NN.md` (editorial + claim ledger) + `layout.html` (brand email template, reusable) |
| Archive | `docs/marketing/newsletter/monitor-NN.md`, previous issue's layout kept for reference |

**Production pipeline (per issue):**
1. Pull candidate content from this month's repo artifacts (see section 2).
2. Draft `monitor-NN.md` with editorial metadata, subject/preview options, CEO note, 5 sections, and a claim ledger.
3. Assemble/verify HTML from `layout.html` (replace placeholders, keep tokens).
4. Verification pass: every ledger claim re-checked against repo file or live source URL; publish-queue dry-run receipt reviewed.
5. QA render via `ls-artifact-qa` (visual, brand, UX, accessibility, content checks).
6. Send via publishing rails when unblocked (section 5), then log metrics (section 4).

---

## 2. Content Pipeline (repo artifacts → sections)

The Monitor reuses artifacts LightSpeed already produces — no net-new research for core sections.

| Monitor section | Feeds / source artifacts | Owner | Cadence of feed |
|-----------------|--------------------------|-------|------------------|
| CEO Note | `docs/Pharos/positioning.md` (voice, North Star); monthly theme | Human CEO / Content Writer | Monthly |
| This Month at LightSpeed (company milestone) | `company-registry.yaml` (agent/department counts), `docs/STATUS.md`, `docs/marketing/warmup-log.md`, `docs/marketing/content-calendar-90day.md`, `results/` run logs | Content Writer + build-log agents | Weekly (Build Log) → monthly digest |
| Policy & Governance (regional item) | `templates/pharos/routines/friday-policy-governance-africa.md` (Friday policy brief), `docs/Pharos/policy-drafts/*` (SADC framework, national strategy comments), plus live source URLs (verified each issue — see section 5) | Agentic Policy Analyst | Weekly (Friday brief) → monthly digest |
| From the Build Log (technical note) | `docs/STATUS.md` shipped builds; `src/ai_company/**` modules; `results/` evidence | Content Writer + engineering agents | Weekly (Wednesday Build Log) → monthly digest |
| How We Think (framework insight) | `docs/Pharos/positioning.md` (H→A→O→M→T→G→V, Four Reservations), `docs/Pharos/policy-drafts/sadc-agentic-ai-governance-framework.md` (HITL tiers) | Thought Leadership Lead | Rotating framework per issue |
| CTA | Subscribe URL, LinkedIn profile, contact email (placeholders in `layout.html` until confirmed) | Marketing | Per issue |

**Pillar rule (from `docs/Pharos/content-calendar.md`):** every section maps 1:1 to the three pillars — Company Builder / Use Cases / Policy. Never drift into generic "AI news commentary."

---

## 3. Audience & Segments

Primary segments (aligned to `docs/Pharos/positioning.md`, `docs/Pharos/README.md`, and Friday policy-brief audiences):

| Audience | Why | Content emphasis |
|----------|-----|------------------|
| Malawi ministries & regulators (incl. MACRA, CRASA, NCST) | Rule-writers; AI Bill before Dec 2026; DPA 2024 enforcement | Policy & Governance, governance framework drafts |
| SADC secretariat & member-state institutions | Regional AI Strategy / Regulatory Framework under development | Regional coordination items, SADC framework draft |
| Development partners (UNDP, UNESCO-ROSA, World Bank) | Fund readiness assessments, data governance programs | Readiness data, RAM, governance standards |
| Banks, SACCOs, VSLA & financial institutions | DPA 2024 + financial safety; AI agents for finance | Use-case issues, HITL/financial autonomy tiers |
| Enterprise C-suites & decision-makers | Deploying agentic AI; "how do we start" | Company milestone, build log, Use Case Map |
| Development community / supporters | Build-in-public audience, warm-up engagement | Build log, How We Think |

Segmentation mechanics: one audience-wide list initially; split into "policy/government" vs "enterprise/practice" segments once the contact list grows (2,000+ subscriber target per `docs/Pharos/README.md`). Platform blocks for send are #192/#194 (section 5).

---

## 4. Success Metrics

| Metric | Target (initial) | Source/measure |
|--------|------------------|----------------|
| List growth | 2,000+ subscribers (12-month Pharos target) | `docs/Pharos/README.md`; warm-up Week 4 signup forms (`docs/marketing/warmup-log.md`) |
| Open rate | Benchmark first 3 issues; establish baseline | ESP open tracking (send flow TBD, section 5) |
| Click rate | Benchmark first 3 issues; establish baseline | ESP click tracking |
| CTA conversion | Subscribe clicks among non-subscribers; contact/inquiry pings for institutions | Click log + inbox |
| Engagement | Reply/forward signal, LinkedIn cross-posts | `docs/Pharos/content-calendar.md` channel mix; `docs/marketing/analytics-setup.md` |
| Quarterly review | Drop what does not move deployments, policy influence, or recognized expertise | `docs/Pharos/README.md` operating principle 6 |

---

## 5. Send Flow — BLOCKED (open items)

**Status: content + layout ready for Issue #1; sending is blocked pending two tickets:**

- **#192 — Email platform decision.** No sender platform chosen/configured yet, so there is no ESP for domain verification, list hosting, template hosting, or open/click tracking. The `layout.html` template is ESP-agnostic (table-based, inline styles, placeholders) and ready to import once decided.
- **#194 — Accounts.** Required accounts/domains (sending domain on a proper domain, LinkedIn company profile, subscribe landing, mailing address) are not confirmed. Warm-up protocol (`docs/marketing/warmup-log.md`, until 2026-10-03) intentionally gates signup-form and account work to Week 4.

**Until unblocked:**
- Ship issues as internal deliverables (`monitor-NN.md` + `layout.html`) and via the Pharos publish-queue **dry-run receipt** path (`src/ai_company/publishing/queue.py`; `docs/STATUS.md` 2026-09-14) — nothing goes out without operator approval.
- Keep the claim-verification pass per issue so each edition is send-ready the moment #192/#194 close.

**When unblocked (future state):**
1. Verify sending domain in chosen ESP; ensure DKIM/SPF/DMARC records (see `docs/DASHBOARD_KEY_ROTATION.md` pattern — never commit secrets).
2. Import `layout.html` as template; set subject + preview text (options per issue editorial).
3. Replace placeholders `[LOGO_URL] [SUBSCRIBE_URL] [LINKEDIN_URL] [CONTACT_EMAIL] [UNSUBSCRIBE_URL] [MAILING_ADDRESS]`.
4. Final claim verification (live URL check) + `ls-artifact-qa` render check.
5. Send to segment; record metrics; close the issue in the ticker with the send evidence.

---

## 6. Verification & QA Checklist (every issue)

- [ ] Every claim in the claim ledger maps to a repo file (path) or a live public URL with publication/access date.
- [ ] No invented numbers; registry counts re-verified against `company-registry.yaml` on the issue date.
- [ ] Brand tokens from `brand/tokens/brand-tokens.json`: navy `#070A40`, red `#E63946`, cyan `#00BFFF` only for accents/CTA; Arial stack; wordmark "LightSpeed Holdings Limited™" on first mention; tagline "ASPIRE. ACT. ACHIEVE."
- [ ] Layout passes strict email-HTML rules (table-based, inline styles, bgcolor attrs, no JS, absolute image URLs, alt text, explicit font sizes/colors/line-heights).
- [ ] `ls-artifact-qa` review: visual, brand, UX, accessibility, content.
- [ ] Dry-run receipt from publish-queue reviewed before any operator-approved send.
