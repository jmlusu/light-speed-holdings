# Pharos publishing plan: thought-leadership slate

**Date:** 2026-10-12 · **Owner:** CMO · **Status:** Ready for review, ship via one PR to `main` once gates clear
**Target surface:** `https://lightspeedholdings.vercel.app` (Vite/React SPA, repo-root `src/`)

This plan sequences the six site articles, three branded HTML visuals, and one whitepaper into a two-week publishing window. Content is final as written in `src/data/insights.ts`, `docs/Pharos/whitepaper/resource-constrained-deployment-playbook.md`, and the three static HTML files under `public/`. This document covers order, placement, gating, SEO, linking, the calendar, and blockers. **No git operations were performed.**

---

## 0. Canonical-facts guardrail (applies to every surface)

Every item below ships under these constraints (AGENTS.md §15; `research/site-claims-ledger.md`):

| Fact | Canonical form |
|------|----------------|
| Company size | 90 agents (89 AI + 1 human CEO), 20 departments |
| Governance | 5-tier HITL approval matrix; timeout escalates, never auto-approves |
| Audit | SHA-256-chained append-only audit, a design/implementation claim, hedged ("decision logs auditable on request"), never "externally audited" |
| J&S StopOver Bar | Real, non-tech SME in Malawi running agentic decision support, **not** a paid client |
| Client deliveries | **None yet.** "Proven in-house first" badges stay on every surface |
| SADC framework | Policy **proposal** authored by the CEO, not adopted, not verified as submitted |
| Banned phrase | The sizing superlative listed in `research/site-claims-ledger.md` (PC-01) is prohibited on all public surfaces. It survives once, inside article 06 (`evidence-ladder-honest-claims`), as a documented meta-example of the removal policy. Do not repeat it in meta titles, descriptions, social copy, image alt text, whitepaper, or this plan's distribution notes |

No invented numbers. No unproven superlatives. Every load-bearing claim keeps its in-article hedge or provenance line.

---

## 1. Recommended publish order (6 articles, ~2 weeks)

Order is a narrative arc: **anchor (cost) → proof (the company) → governance (the gate) → deployment (the constraint) → commercial (the price) → trust (the discipline)**. It leads with the broadest-audience argument, earns the right to state prices only after the operating proof and governance are on the record, and closes on the piece that explains why every other claim on the slate is inspectable.

| # | Slug | Publish date | Why this position |
|---|------|--------------|-------------------|
| 1 | `open-source-cost-architecture` | **Tue 2026-10-13** | **Anchor.** Cost is the universal entry question; the piece leads with external evidence (ITU connectivity cost, open-weight price floors) and first-party architecture, and it names its own honest limits up front. Widest top-of-funnel; sets the slate's evidence voice on day one. |
| 2 | `inside-a-90-agent-company` | **Thu 2026-10-15** | **Proof.** After "how we think about cost," answer "what is this company." The registry/queue/gate explainer is the flagship operating-evidence piece; it gives every later article a concrete referent for "90 agents." Pairs with the flagship infographic. |
| 3 | `five-tier-approval-matrix` | **Mon 2026-10-17** | **Governance.** Deep-dive on the control plane introduced in #2. Targets risk officers, CROs, regulators, the audience that must be warmed before pricing lands. Pairs with the graduated-autonomy-ladder visual. |
| 4 | `offline-first-ai-for-africa` | **Wed 2026-10-20** | **Deployment constraint.** The four reservations and the engineering answers; naturally sets up the whitepaper (same thesis, deeper). Keeps the public argument honest about bandwidth, sovereignty, and debt before any price appears. |
| 5 | `dual-economy-ai-pricing` | **Fri 2026-10-22** | **Commercial.** Publishing the MWK ladder and USD retainer rails *after* operating proof and governance are established is deliberate: the price reads as a consequence of the evidence, not a pitch detached from it. The piece already labels the ladder as offer language pending prospect validation, and that hedge stays. |
| 6 | `evidence-ladder-honest-claims` | **Mon 2026-10-24** | **Trust closer.** The meta-piece: how claims get classed, what the ledger cut, what buyers should demand. It ties the slate together, retroactively vouches for the five articles above it, and is the only public home of the banned-superlative removal example. Close the arc here, not mid-stream. |

**Whitepaper:** Tue 2026-10-26 (see §3). It lands once the slate has established the thesis it deepens.

**Listing behavior note (implementation):** `InsightsPage` renders `insightArticles` in array order, not by date. Before merge, reorder the array so position 0 = article #1 (anchor), position 5 = article #6 (trust closer). The three pre-existing articles (`sadc-ai-opportunity`, `agentic-ai-african-governments`, `digital-to-ai-native-transformation`) follow beneath the six.

**Date note:** all six entries currently carry `publishedAt: '2026-10-12'`. Update each to its calendar date at publish time (or in the single PR, with the later articles simply not promoted until their date). Displayed dates on cards and article headers derive from this field via `formatInsightDate`.

---

## 2. HTML visual placement

All three visuals are standalone static files under `public/` and will be reachable at fixed URLs the moment `main` deploys, so zero code is required for the link-out path:

| Visual | File | Public URL | Pairs with | Placement |
|--------|------|------------|------------|-----------|
| Inside the 90-Agent Company | `public/infographics/inside-the-90-agent-company.html` | `/infographics/inside-the-90-agent-company.html` | `inside-a-90-agent-company` (article #2) | Primary: linked from the article ("Explore the interactive org visual"). Also the standalone share asset for the LinkedIn amplification of #2, since it reads correctly with no article context. |
| The Open-Source Stack Behind a 90-Agent Company | `public/infographics/open-source-stack.html` | `/infographics/open-source-stack.html` | `open-source-cost-architecture` (article #1) | Primary: linked from article #1's "What the stack is actually built on" section. Secondary: link from `offline-first-ai-for-africa` (provider-agnostic routing section) as a "see the actual stack" hop. |
| The Graduated Autonomy Ladder | `public/visuals/graduated-autonomy-ladder.html` | `/visuals/graduated-autonomy-ladder.html` | `five-tier-approval-matrix` (article #3) | Primary: linked from article #3's tier-table section. Secondary: cross-linked from the existing `sadc-ai-opportunity` article, with its standing hedge that the SADC framework is a proposal. The visual must not be captioned anywhere as an adopted standard. |

**Embed mechanism.** `InsightBlock` supports only `h | p | ul | quote`, and there is no embed block kind today. For this ship the baseline is link-out: a text link or a small "INTERACTIVE VISUAL →" affordance added in the article body or as a related-links row. It works with no component changes and preserves the visuals' full-viewport standalone experience. The stretch, post-slate, is an `embed` block kind on `InsightArticlePage` for in-page iframes with lazy-loading. That is not a blocker for this window. Do not block the slate on embed chrome.

---

## 3. Whitepaper gating recommendation

**File:** `docs/Pharos/whitepaper/resource-constrained-deployment-playbook.md` (~3,219 words; frontmatter carries a per-claim ledger).

**Recommendation.** Publish open (ungated) for this cycle. Gated lead-gen is a v2 option, not a ship blocker.

Rationale:

1. **The thesis is inspectability.** The slate's closer (#6) argues that the durable answer to buyer skepticism is claims you can test. Gating the flagship paper behind a form puts friction between the claim and the evidence, which is the exact pattern article #6 criticizes ("the slide exists because claims are cheap and verification is expensive"). For a first public flagship from a vendor whose entire positioning is "inspect us," open beats capture.
2. **No lead-capture backend exists on the SPA.** The site ships `NewsletterSignup` and `/contact` + `/ask` routes; there is no form-to-delivery pipeline for a gated PDF. Building gating would be new engineering inside a content window, the wrong place to invent infrastructure, and any invented endpoint would itself be an unverified claim.
3. **Conversion paths already exist.** The open paper ends in CTAs that route to `/contact`, `/ask`, and the boardroom-briefing solution card (`/solutions#boardroom-briefing`). Newsletter signup sits at the foot of every article. Warm readers already have a path; we just don't extort an email for the PDF.
4. **Gating later is cheap; ungating later is embarrassing.** If lead volume justifies it, v2 adds a soft gate (email-for-PDF) once a real backend exists. Reversing a gate after publishing the "inspect everything" paper would be a self-inflicted trust wound.

**Ship mechanics (engineering prerequisite, flagged in §7).**

- The whitepaper is markdown in `docs/`, not a public page. It needs a rendered route (e.g. `/whitepapers/resource-constrained-deployment-playbook`) or a static PDF/HTML render under `public/whitepapers/`, with the frontmatter ledger preserved as an appendix or source line.
- Frontmatter currently reads `status: Draft — awaiting CEO approval`. **It does not ship until that status changes** (§7, blocker B2).
- Keep title, hedges, and the claims ledger intact; do not compress the honesty notes for "readability."

---

## 4. On-page SEO notes (per article)

All six slugs are descriptive, hyphenated, and stable, and are publish-ready as URLs. Categories were checked against `insightCategories` in `src/data/siteContent.ts`: **all six values are valid list members** ("African AI", "Market intelligence", "AI governance", "AI Company Building", "African AI", "Operating models"). Two systemic gaps, then per-article flags.

**Gap S1.** `InsightArticlePage` sets no `document.title` and no per-article `<meta name="description">`; `usePageMeta` is not wired to this route. Until fixed, every article serves the SPA's default head. Wiring title + description per slug is a pre-publish engineering task. Derived `<title>` and meta-description strings below are ready for that task. Keep `<title>` ≤ ~65 chars and meta descriptions ≤ ~155 chars; H1s and on-page deks stay as written.

**Gap S2.** Several deks, displayed as the article lead and the natural description source, run 250–350 chars, too long for SERP snippets. Use the trimmed variants below as meta descriptions; do not edit the on-page deks.

| # | Slug | Verdict | Derived `<title>` (≤65ch) | Meta description (≤155ch) | Flags |
|---|------|---------|---------------------------|----------------------------|-------|
| 1 | `open-source-cost-architecture` | **Publish-ready** (head metadata per S1) | `Cutting AI Costs With Open Source \| LightSpeed` | `Token prices are not the binding constraint in Malawi, connectivity is. Why open-source AI cost is an architecture argument, with honest limits.` | Strong anchor. ITU/secondary-source and third-party price-tracker provenance is already in-body. Keep it. |
| 2 | `inside-a-90-agent-company` | **Publish-ready** (head metadata per S1) | `Inside a 90-Agent Company \| Registry, Queue, Gate` | `90 agents (89 AI + 1 human CEO) across 20 departments. What the registry, message bus, and five-tier approval gate actually do.` | Canonical 90/89+1/20 figures used correctly. "Not a lab toy, not a client deployment" hedge intact. Keep it. |
| 3 | `five-tier-approval-matrix` | **Publish-ready** (head metadata per S1) | `The Five-Tier Approval Matrix for Agent Governance` | `A permission system that gates everything drowns humans. One that gates nothing is not a company. The tier table lives in code; a timeout never means yes.` | "90-agent company" framing matches canonical count. Pillar essay CEO-review status noted in Honest status is accurate. Leave it. |
| 4 | `offline-first-ai-for-africa` | **Publish-ready** (head metadata per S1) | `Offline-First AI for Africa \| Bandwidth and Sovereignty` | `Low-bandwidth is the design brief, not a footnote. How offline-first routing, a zero-cloud boundary, and local models answer the four reservations.` | Zero-cloud correctly framed as product option, not guarantee. J&S correctly framed as SME, not client. |
| 5 | `dual-economy-ai-pricing` | **Publish-ready with one flag** (head metadata per S1) | `Pricing Agentic AI in a Dual Economy \| MWK and USD` | `A dollar list price divided by the exchange rate died with the 44% kwacha devaluation. Kwacha ladders, dollar retainers, mobile-money rails.` | **Flag:** the MWK ladder is explicitly offer language pending prospect validation. Meta copy must not imply transacted revenue. The derived description above states only the devaluation fact and the mechanism, which is safe. |
| 6 | `evidence-ladder-honest-claims` | **Publish-ready** (head metadata per S1) | `The Evidence Ladder \| How Every Claim Gets a Class` | `Every public claim gets a class and a source, and occasionally gets cut. What the ledger killed, and what buyers should demand of any AI vendor.` | The banned phrase appears once, in-body, as the documented removal example, allowed here and nowhere else. Do not quote it in meta, social, or alt text. |

**Cross-checks performed:** titles/deks/sources/categories read directly from `src/data/insights.ts`; no title or dek required rewriting; no unproven superlative found in any derived meta string above.

---

## 5. Internal linking plan

Two layers ship automatically; one needs a small addition.

**Layer A is auto, already wired.** `InsightArticlePage` renders each article's `relatedSolutions` as cards to `/solutions#{slug}` and `relatedSectors` to `/sectors#{id}`. The existing mappings are correct and ship as-is:

| Article | `/solutions#` cards | `/sectors#` cards |
|---------|--------------------|--------------------|
| `open-source-cost-architecture` | `ai-company-builder`, `enterprise-deployment`, `business-automation` | agriculture, financial-services, government |
| `inside-a-90-agent-company` | `ai-company-builder`, `enterprise-deployment`, `boardroom-briefing` | financial-services, government, education |
| `five-tier-approval-matrix` | `ai-company-builder`, `enterprise-deployment`, `boardroom-briefing` | financial-services, government |
| `offline-first-ai-for-africa` | `enterprise-deployment`, `business-automation`, `digital-presence` | agriculture, financial-services, healthcare, government |
| `dual-economy-ai-pricing` | `business-automation`, `digital-presence`, `boardroom-briefing` | financial-services, agriculture, government |
| `evidence-ladder-honest-claims` | `boardroom-briefing`, `digital-presence`, `ai-company-builder` | financial-services, government, healthcare |

**Layer B.** Article-to-article links need wiring. There is no related-articles mechanism on `InsightArticlePage` today. Recommended minimal implementation: extend `InsightArticle` with an optional `relatedInsights: string[]` field and render a "Related thinking" row using the same card pattern as solutions. If that slips, fall back to one prose cross-reference per article (edit-in-body) rather than nothing. Target graph:

```
#1 cost-architecture ──► #2 90-agent · #4 offline-first · #6 evidence-ladder
#2 90-agent ───────────► #3 five-tier · #1 cost-architecture · #6 evidence-ladder
#3 five-tier ──────────► #2 90-agent · #6 evidence-ladder · [grad-autonomy visual]
#4 offline-first ──────► #1 cost-architecture · [whitepaper] · #5 pricing
#5 pricing ────────────► #4 offline-first · #2 90-agent
#6 evidence-ladder ────► #1 · #2 · #3 · #4 · #5  (the slate's index page in miniature)
```

Older slate articles already on the site (`sadc-ai-opportunity`, `agentic-ai-african-governments`, `digital-to-ai-native-transformation`) gain inbound links where natural: #4 → `sadc-ai-opportunity` (policy environment section), #3 → `agentic-ai-african-governments` (governance section). Do not rewrite those older articles beyond the one cross-link each.

**Layer C, `/what-we-do`.** The hub route `/what-we-do` and the `/solutions` index both exist; solution cards already deep-link `/solutions#{slug}`. Add nothing new. The one gap: the whitepaper's closing CTA should link `/what-we-do` (company overview) plus `/solutions#boardroom-briefing` (the natural next step for the institutional reader).

**Visuals in the graph.** Article #1 → `open-source-stack.html`; article #2 → `inside-the-90-agent-company.html`; article #3 → `graduated-autonomy-ladder.html`; article #4 → `open-source-stack.html` (secondary); `sadc-ai-opportunity` → `graduated-autonomy-ladder.html` (secondary, proposal hedge intact).

---

## 6. Editorial calendar (one page)

| Date | Item | Slug / path | Type | Visual embed (link-out) | Owner |
|------|------|-------------|------|-------------------------|-------|
| Tue 2026-10-13 | Cutting AI Costs With Open Source: Why the Architecture Matters More Than the Arithmetic | `/insights/open-source-cost-architecture` | Article #1, anchor | `/infographics/open-source-stack.html` | CMO |
| Thu 2026-10-15 | Inside a 90-Agent Company: What the Registry, the Queue, and the Approval Gate Actually Do | `/insights/inside-a-90-agent-company` | Article #2, proof | `/infographics/inside-the-90-agent-company.html` | CMO |
| Mon 2026-10-17 | The Five-Tier Approval Matrix: How Friction Scales With Risk in a 90-Agent Company | `/insights/five-tier-approval-matrix` | Article #3, governance | `/visuals/graduated-autonomy-ladder.html` | CMO |
| Wed 2026-10-20 | Offline-First AI for Africa: Designing for Bandwidth, Sovereignty, and Mobile-Money Reality | `/insights/offline-first-ai-for-africa` | Article #4, deployment | (secondary: open-source-stack) | CMO |
| Fri 2026-10-22 | Pricing Agentic AI in a Dual Economy: Kwacha Ladders, Dollar Retainers, and Paying for What You Run | `/insights/dual-economy-ai-pricing` | Article #5, commercial |  | CMO |
| Mon 2026-10-24 | The Evidence Ladder: How Every Public Claim Gets a Class — and What Buyers Should Demand | `/insights/evidence-ladder-honest-claims` | Article #6, trust closer |  | CMO |
| Tue 2026-10-26 | Agentic AI in Resource-Constrained Environments: A Deployment Playbook for African Institutions | `/whitepapers/resource-constrained-deployment-playbook` (route TBC, §7 B4) | Whitepaper, **open**, post-CEO-approval |  | CMO + **CEO (approval)** |

**Every ship date is contingent on gates B1–B4 in §7.** If a gate slips, the sequence holds. Shift dates rather than reordering; the order is the argument.

---

## 7. Risks and blockers

| ID | Item | Severity | Detail | Resolution before |
|----|------|----------|--------|-------------------|
| **B1** | **No QA verdicts exist for the three HTML visuals** | **Hard gate** | `docs/Pharos/qa/` is empty; no `ls-artifact-qa` PASS is on record for `inside-the-90-agent-company.html`, `open-source-stack.html`, or `graduated-autonomy-ladder.html`. | Any article that links a visual (dates 10-13, 10-15, 10-17). Run `ls-artifact-qa` (Visual / Brand / UX / Accessibility / Content) on each; ship link-outs only on APPROVE. On FIX → re-render → re-approve per the skill's loop. |
| **B2** | **Whitepaper is `Draft — awaiting CEO approval`** (frontmatter, line 3) | **Hard gate** | The paper speaks in the Human CEO voice with a claims ledger; it must not publish on an agent's authority. | 2026-10-26 date. CEO review + status flip to approved. If unapproved by 10-24, slide the whitepaper date; do not gate the six articles on it. |
| **B3** | **Per-article `<title>` / meta description not wired** (`InsightArticlePage` sets no head metadata) | **Hard gate for SEO claim** | Articles will serve the SPA default head. Derived strings are ready in §4. | First publish (2026-10-13). Small, well-scoped task; can land in the same PR as the content. |
| **B4** | **Whitepaper has no public rendering path** | Hard gate for 10-26 only | Markdown in `docs/Pharos/whitepaper/` is not served by the SPA. Needs a route or a static render under `public/`. | 2026-10-26. Decide route vs. PDF render; preserve the claims ledger as appendix. |
| **B5** | **Insights array order drives the `/insights` listing** | Medium | `InsightsPage` does not sort by date; the array order is the display order. All six currently share `publishedAt: '2026-10-12'`. | The PR: reorder array to match §1 sequence; set per-article `publishedAt` to calendar dates. |
| **B6** | **No article-to-article related mechanism** | Medium | Only solutions/sectors cards exist (§5 Layer B). | Before first publish, or accept prose-only cross-links for cycle 1. |
| **B7** | **Pricing amplification risk** | Medium | Article #5 publishes real MWK figures labeled as offer language. Social/email amplification must repeat that label. | Any promotion of #5. Canonical copy: "published offer ladder pending prospect validation, not a revenue record." |
| **B8** | **Banned-phrase discipline in distribution** | Medium | The banned phrase listed in `research/site-claims-ledger.md` appears once, in article #6, as the removal-policy example. Every other channel (LinkedIn series, email, ad copy, alt text, whitepaper) is phrase-free. | Every distribution artifact. |
| **B9** | **Nothing is committed** | Process | All content + this plan are uncommitted working-tree state. Ship = one PR to `main` (branch required; `main` is protected, 6 checks). | Merge. **No git operations performed in this task**, sequencing only. |
| **B10** | **Canonical-fact drift in social copy** | Low | Amplification (LinkedIn/email) must not upgrade claims: 90 agents = 89 AI + 1 human CEO; J&S is not a client; SADC framework is a proposal; SHA-256 audit stays hedged. | Each amplification send; check against §0 table. |

**Explicit non-blockers.** The six articles' bodies, deks, and source lines are final and were verified against the canonical-facts table, so no content rewrite is required. Categories validate against `insightCategories`. Related-solution mappings are already correct in data.

---

## 8. Ship checklist (single PR)

1. B1 QA verdicts recorded for all three visuals (APPROVE or re-render loop complete).
2. Array reorder + per-article `publishedAt` set to calendar dates (B5).
3. Per-article head metadata wired using §4 strings (B3); `relatedInsights` row or prose cross-links per §5 (B6).
4. Visual link-outs added to articles #1–#3 (+ secondary links from #4 and `sadc-ai-opportunity`).
5. Whitepaper: CEO approval (B2) + rendering path (B4); closing CTAs → `/what-we-do`, `/solutions#boardroom-briefing`, `/contact`.
6. §0 canonical-facts pass over the diff (90/89+1/20, 5-tier, SHA-256 hedge, J&S-not-client, no-deliveries, SADC-is-proposal, banned phrase count = 1 and only in article #6).
7. Normal PR → protected `main` (6 required checks green). No direct pushes.

---

*Prepared by the CMO, LightSpeed Holdings · 2026-10-12 · Sources: `src/data/insights.ts`, `docs/Pharos/whitepaper/resource-constrained-deployment-playbook.md`, `public/infographics/*.html`, `public/visuals/graduated-autonomy-ladder.html`, `src/pages/InsightArticlePage.tsx`, `src/pages/InsightsPage.tsx`, `src/data/siteContent.ts`, `research/site-claims-ledger.md`, AGENTS.md §15.*
