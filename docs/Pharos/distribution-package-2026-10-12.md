# Pharos thought-leadership slate: distribution package (2026-10-12)

**Channel:** LinkedIn-first, with X/Twitter and newsletter adaptations.
**Owner:** Social Media Manager, LightSpeed Holdings.
**Source of truth:** titles and deks in `src/data/insights.ts` (newest six articles); flagship whitepaper exec summary in `docs/Pharos/whitepaper/resource-constrained-deployment-playbook.md`; three HTML visuals in `public/` (paths below).
**Canonical facts allowed in copy (nothing else invented):** 90 agents (89 AI + 1 human CEO) · 20 departments · 5-tier HITL approval · SHA-256-chained audit (hedged language only) · J&S StopOver Bar is a real Malawi SME, not a paid client · no paid client deliveries yet · SADC framework is a proposal, not adopted.
**Banned:** the sizing superlative struck by the claims-ledger audit (see `research/site-claims-ledger.md`), and it appears nowhere in this package, including the checklist (referenced by pointer only). No other superlatives. No invented numbers. Every external claim keeps the hedge it carries in the article.

---

## 1. Sequencing plan (~2 weeks, LinkedIn)

Arc: **cost architecture → governance → operations.** Cost first (the binding constraint in our market), governance second (how the fleet stays governable), operations last (the capstone: the company itself). Each visual posts adjacent to its paired article so the feed reads as a designed sequence, not a dump.

| Day | Asset | Role in the arc | Visual pairing |
|-----|-------|-----------------|----------------|
| Tue 2026-10-13 | **open-source-cost-architecture** | Opens on the constraint: connectivity, not token prices. Sets the honesty tone for the whole slate. | **open-source-stack** visual post (same day or +1) |
| Thu 2026-10-15 | **dual-economy-ai-pricing** | Cost arc, commercial half: once the architecture is cheap-by-design, how do you price and collect in a dual-currency market. |  |
| Mon 2026-10-17 | **offline-first-ai-for-africa** | Closes the constraint arc: bandwidth, sovereignty, mobile-money. Points to the flagship playbook as the deep read. |  |
| Tue 2026-10-20 | **five-tier-approval-matrix** | Opens the governance arc: friction scales with risk; timeouts never approve. | **graduated-autonomy-ladder** visual post (Thu 10-22), framed as the *policy* proposal, explicitly not conflated with the internal HITL tiers |
| Thu 2026-10-22 | **evidence-ladder-honest-claims** | Governance of claims: how every public claim gets a class, and what gets cut. Reinforces why the slate's hedges exist. |  |
| Mon 2026-10-24 | **inside-a-90-agent-company** | Capstone: registry, queue, approval gate. The whole operating model, ending the slate on inspectable evidence. | **inside-the-90-agent-company** visual post (same day or +1) |

**Rationale:** a reader who arrives for cost stays for governance; a risk officer who arrives for governance stays for the capstone. The whitepaper (*Agentic AI in Resource-Constrained Environments: A Deployment Playbook for African Institutions*) is referenced as the deep read in the offline-first post and the newsletter, not given its own slot, since it compounds rather than competes.

---

## 2. LinkedIn post drafts (6 articles)

Each post: hook in line 1, 120–180 words, ends with the link placeholder. An alternate hook follows each draft for A/B or retweet framing.

### 2.1 open-source-cost-architecture
*"Cutting AI Costs With Open Source: Why the Architecture Matters More Than the Arithmetic"*

> The cost of AI in Malawi is not a token price. It's a bandwidth bill.
>
> Most cost essays start in the wrong place: a hyperscaler price list divided by the exchange rate. Our new article argues from the constraint instead. Connectivity costs a documented share of GNI per capita (ITU data, sourced and caveated in the piece). The device class is a phone on an intermittent link, not a workstation on fibre.
>
> The open-source cost argument is architectural, not arithmetic:
> → Route to local models (Ollama, llama.cpp) where the marginal token is free by ledger convention, a design choice, not a measured saving, and we say so.
> → Rent open-weight APIs where host competition has already capped the price.
> → Spend the difference on what actually binds: connectivity, devices, power, and the human approvals that keep agents governable.
>
> We publish mechanisms and inventories, not invented savings. No before/after numbers, because we haven't measured them.
>
> Honest status, as everywhere: the stack is proven in-house. J&S StopOver Bar is a real Malawi SME in our case pipeline, not a paid client delivery.
>
> [LINK: /insights/open-source-cost-architecture]

**Alternate hook:** Everyone divides the US list price by the exchange rate and calls it an AI strategy. In Malawi, that's not analysis. It's a spreadsheet with hope.

### 2.2 dual-economy-ai-pricing
*"Pricing Agentic AI in a Dual Economy: Kwacha Ladders, Dollar Retainers, and Paying for What You Run"*

> Take a US list price. Divide by the exchange rate. Hope. That method died the night the kwacha devalued 44%.
>
> Malawi's market pays in kwacha. Its NGO and regional work is budgeted in dollars. So we don't price on one rail.
>
> Our new piece lays out the dual-economy approach: a published MWK ladder for local clients, USD-denominated retainers where the budget is in dollars, and mobile-money collection (Airtel Money, TNM Mpamba) treated as day-one plumbing, not a phase-two roadmap item.
>
> It also gives an honest account of what has actually been sold. That matters, because AI skepticism in the region was earned by vendors who priced on hope and delivered on hype.
>
> What we can say: the rails exist, the reasoning is published, and the SME anchor, J&S StopOver Bar, is a real business running agentic decision support, not a paid client delivery. No paid client work is claimed. That badge stays on.
>
> [LINK: /insights/dual-economy-ai-pricing]

**Alternate hook:** One market pays kwacha. Another budgets in dollars. A pricing model that ignores either isn't a model. It's a bet on the exchange rate.

### 2.3 offline-first-ai-for-africa
*"Offline-First AI for Africa: Designing for Bandwidth, Sovereignty, and Mobile-Money Reality"*

> Low-bandwidth isn't a deployment footnote. It's the design brief.
>
> The default deployment story for agentic AI assumes fibre, idle GPUs, and a data centre in another hemisphere. That story doesn't survive contact with a district clinic, an SME counter in Lilongwe, or a ministry network still running legacy cores.
>
> Our new article maps the four reservations risk officers actually raise to engineering answers: bandwidth, data protection, technology debt, and AI skepticism. The answers are offline-first routing with a sovereign-by-default posture and a zero-cloud boundary as an architecture option, local models as a first-class provider class, thin integration seams instead of rip-and-replace, and mobile-money rails treated as default.
>
> Each answer carries an honesty badge: what's proven in-house, what's fieldable or in pilot, what's still conceptual. The badges are part of the architecture, not marketing garnish.
>
> Deep-read companion: our deployment playbook for African institutions, linked from the article.
>
> [LINK: /insights/offline-first-ai-for-africa]

**Alternate hook:** The best AI engineering problem in Africa isn't a bigger model. It's a smaller pipe.

### 2.4 five-tier-approval-matrix
*"The Five-Tier Approval Matrix: How Friction Scales With Risk in a 90-Agent Company"*

> Ask a team how they govern their AI agents and you'll hear a policy. Ask what happens when nobody answers an approval request, and you'll learn whether the policy is real.
>
> LightSpeed Holdings runs 90 agents, 89 AI personas and one human CEO, across 20 departments. The only thing between that fleet and ungoverned action is a five-tier approval matrix enforced in code, not prose: Tier 0 auto-approve for read-only work, up to Tier 4 CEO-only for secrets, legal, and financial exposure.
>
> The doctrine in one line: friction scales with risk. Low-risk work moves without asking. High-risk work cannot move without deliberate human action. And a timeout never means yes. An unanswered request expires loudly and must be re-submitted. No path in the system converts silence into permission.
>
> The tier table lives in our platform code, exercised by our own regression suite, not drafted for a deck. We'd show it to a regulator today. No paid enterprise delivery is claimed; the operating evidence is our own company.
>
> [LINK: /insights/five-tier-approval-matrix]

**Alternate hook:** An ignored approval queue is governance theater. A timeout that auto-approves is governance's opposite.

### 2.5 inside-a-90-agent-company
*"Inside a 90-Agent Company: What the Registry, the Queue, and the Approval Gate Actually Do"*

> Building ninety agent personas takes an afternoon. Making them safe to run takes a control plane.
>
> Most conversations about "AI companies" start with the model. Ours starts with the paperwork. LightSpeed Holdings runs 90 agents, 89 AI plus one human CEO, across 20 departments, and that count isn't a marketing abstraction. It's a direct tally of the registry file: every agent's identity, tools, approval level, and escalation path in one source of truth. When someone asks who can spend money here, the answer is a grep, not a meeting.
>
> Our new piece walks through the three pieces that turn personas into a company: the registry (the org as data), the queue (work that persists between handoffs), and the approval gate (friction that scales with risk).
>
> If you can't point to where work lives between handoffs, you don't have an operating model. You have a pile of sessions.
>
> [LINK: /insights/inside-a-90-agent-company]

**Alternate hook:** When someone asks "who can spend money here?" the answer should be a grep, not a meeting.

### 2.6 evidence-ladder-honest-claims
*"The Evidence Ladder: How Every Public Claim Gets a Class — and What Buyers Should Demand"*

> Architecture never earns a Chief Risk Officer's "yes" on its own. Claims do the rest of the work.
>
> Every AI vendor deck has the same slide: logos, a throughput number with no unit, a customer quote nobody can call. AI skepticism across African enterprises and ministries was earned by years of slide-deck AI that never changed an operating metric. In markets where buyers have been burned that way, the slide isn't persuasion. It's a liability.
>
> Our answer is an evidence ladder: Proposed → Verified → Established → Market-leading. Claims advance a rung only where evidence exists. Most of what any honest operator has lives in the first two rungs. A claims registry classifies every public claim before it can ship anywhere on our site, and unqualified claims don't ship.
>
> What the ladder actually cut is the test: unverifiable superlatives, unsourced performance numbers, submission claims downgraded to authored proposals. Copy loses arguments with evidence. That's the whole operating model, and it's why we publish the honest status at the end of every piece, including this slate.
>
> [LINK: /insights/evidence-ladder-honest-claims]

**Alternate hook:** The test of an evidence system isn't what it lets through. It's what it kills.

---

## 3. Visual posts (3), with image attach notes

### 3.1 `public/infographics/open-source-stack.html`
*"The Open-Source Stack Behind a 90-Agent Company"*

> New visual: the open-source stack behind our 90-agent company. A verified inventory of the permissive-licensed toolchain we build on, the cost architecture it enables, and an explicit statement of what has not been measured. Sources shown per claim, caveats included.
>
> Open-source-first is how AI cost becomes an architectural choice instead of a vendor invoice: local models where the marginal token is free by design, open-weight APIs where host competition has capped the price, and the difference spent on the constraints that actually bind.
>
> Pairs with the article: [LINK: /insights/open-source-cost-architecture]

**Image attach:** render the page full-length, or export the thesis + context-fact panels as PNG (feed-friendly crop). Never edit out the per-claim source lines.

### 3.2 `public/visuals/graduated-autonomy-ladder.html`
*"The Graduated Autonomy Ladder"*

> New visual: the Graduated Autonomy Ladder. A policy proposal, not an adopted standard. Four tiers, four risk classes: advisory drafting is not power-grid switching, and policy should not treat them the same. The control a domain demands scales with the damage an agent could do there.
>
> It sits at the "Proposed" rung of our own evidence ladder. The honest-status chip is on the page itself: not adopted by SADC or any government; no paid client deployments.
>
> Note for readers (and our own team): this is the *policy* taxonomy. Our internal five-tier HITL is the *operational* taxonomy, and it gates individual actions in our stack. The page explains why they must not be conflated.

**Image attach:** export the ladder panel (the four-rung SVG) as PNG; keep the autonomy-ceiling bar and tier labels legible. Do not crop off the honest-status chip.

### 3.3 `public/infographics/inside-the-90-agent-company.html`
*"Inside the 90-Agent Company"*

> New visual: Inside the 90-Agent Company. The org at a glance, extracted from the operating repository. One human CEO, 89 AI agents, 20 departments, five human approval tiers. Every stat carries its source path.
>
> This is what an AI-native company looks like when the org chart is a file you can read and the approval ladder is code you can run.
>
> Pairs with the article: [LINK: /insights/inside-a-90-agent-company]

**Image attach:** tall infographic. Crop the headline stat strip for the feed image and link the full page; never detach a stat from its source path in the crop.

---

## 4. X/Twitter thread (6 posts), one narrative and an honest tone

*Adaptation note: each LinkedIn post in §2 can also stand alone on X by cutting to its alternate hook + link; this thread is the slate-level X asset.*

> **1/6** We run a company in Lilongwe, Malawi, where 90 agents, 89 AI and 1 human CEO, hold defined work across 20 departments. This is the honest version: what that actually looks like, what it costs, and what we have not proven. Thread. [LINK: /insights/inside-a-90-agent-company]

> **2/6** Start with the constraint. In Malawi the binding cost of AI isn't the token price. It's connectivity, and a device class that is a phone on an intermittent link. So the cost architecture is open-source-first: local models via Ollama/lllama.cpp where the marginal token is free by design; open-weight APIs where host competition has capped the price. We claim mechanisms, not measured savings, because we haven't measured them.

> **3/6** Pricing follows the market, not a vendor calculator. Local clients pay kwacha; NGO and regional work is quoted in dollars; mobile-money rails are day-one plumbing. The kwacha devalued 44% in a single night in 2023. A dollar list price divided by hope is not a pricing model. [LINK: /insights/dual-economy-ai-pricing]

> **4/6** Governance is code. Five approval tiers: read-only work runs free; code changes need one human; production paths need two distinct humans; secrets and financial exposure are CEO-only. Friction scales with risk. And a timeout never means yes. An unanswered request expires and gets re-asked. That rule is the difference between governance and a deadline that auto-approves. [LINK: /insights/five-tier-approval-matrix]

> **5/6** Offline-first is the design brief, not a demo mode: sovereign-by-default processing, local models as a first-class provider class, thin seams into existing systems instead of rip-and-replace. The four reservations African risk officers raise are engineering problems: bandwidth, data protection, tech debt, skepticism. Every answer carries a badge: proven in-house, fieldable, or still in pilot. [LINK: /insights/offline-first-ai-for-africa]

> **6/6** What we can honestly say at the end of this slate: the stack is proven in-house. J&S StopOver Bar is a real Malawi SME running agentic decision support, not a paid client. We have no paid client deliveries yet. Our SADC governance framework is a proposal, not adopted. If any of that makes you want to inspect the work instead of the pitch: six articles and a deployment playbook are live. [LINK: /insights/evidence-ladder-honest-claims]

---

## 5. Newsletter blurb (~100 words)

**Subject:** Six new pieces from inside a 90-agent company

> We've published a new slate from Pharos, LightSpeed Holdings' thought-leadership program, written from operating evidence, not a pitch deck.
>
> It covers cost architecture for AI in Malawi (open source and dual-currency pricing), offline-first design for bandwidth and sovereignty realities, the five-tier approval matrix that governs our 90-agent company (89 AI + one human CEO), and the evidence ladder that classifies every claim we publish, including the ones we cut.
>
> Every article ends with an honest status: what's proven in-house, what's a real SME anchor (J&S StopOver Bar, not a paid client), and what's still a proposal. Start anywhere: [LINK: /insights]

---

## 6. Compliance checklist, mandatory before any post ships

Run every item on every post, image caption, thread reply, and newsletter blurb. Any FAIL stops the send; fix and re-run from item 1.

1. **Banned phrase, hard fail.** The sizing superlative struck by the claims-ledger audit must appear in **zero** posts in any casing or hyphenation. The canonical banned string lives in `research/site-claims-ledger.md`, and the audit record notes it was an unverifiable boast about the SME, removed from three surfaces. Grep each draft against that ledger before publishing. This package contains no instance of it.
2. **No invented numbers.** Permitted hard facts: 90 agents (89 AI + 1 human CEO), 20 departments, 5-tier HITL. Any other statistic must be copied from the linked article *with its hedge* (e.g., the 44% devaluation as published in the dual-economy dek; the 8.45%-of-GNI connectivity figure only with its ITU-secondary-mirror caveat, or omit the number entirely). No new metrics, percentages, savings figures, or client counts, ever.
3. **SME not-client framing.** J&S StopOver Bar is "a real Malawi SME" / "in our case pipeline" / "running agentic decision support." Never: client, customer, paid engagement, delivered-to, case study (unqualified). If the post mentions J&S, this framing is mandatory.
4. **No paid client deliveries.** Any post that could imply commercial proof must carry the badge explicitly ("no paid client deliveries yet" or equivalent hedge). Never imply enterprise, ministerial, or bank production deployments.
5. **SADC = proposal, not adopted.** The framework is authored as a policy proposal. Never: SADC-approved, SADC-compliant, adopted by SADC, working with SADC (unless separately fact-sourced; the default is do not claim it).
6. **No superlatives.** Per the evidence-ladder piece, "first," "only," "fastest," "leading," "best," and any sizing superlative of that class are each a data obligation we cannot discharge. Default: delete the word, keep the fact.
7. **SHA-256 audit language stays hedged.** Allowed: "append-only, SHA-256-chained audit design/trails," "decision logs auditable on request." Banned: tamper-proof, certified, externally audited, unalterable, guarantees.
8. **Two ladders, never conflated.** The graduated autonomy ladder is the *policy* taxonomy (Proposed). The five-tier HITL (T0–T4) is our *operational* taxonomy. If a post or caption mentions one, it must not describe it using the other's numbering or framing.
9. **Links resolve.** Every `[LINK: /insights/<slug>]` placeholder is replaced with the correct live path before send; click-test once. Visual posts link their paired article.
10. **Posts summarize; they don't extend.** No claim in a post may go beyond what the linked article states. If a sentence can't be traced to the article body or dek, cut it.
11. **Visual integrity.** Image exports keep per-claim source lines and honest-status chips in frame; no cropping that detaches a stat from its source or removes the proposal disclaimers.
12. **Second-pair-of-eyes rule.** Any post mentioning J&S StopOver Bar, SADC, or audit trails gets a human second reviewer before send, mirroring the tier discipline we publish.

---

*Package prepared for the 2026-10-12 slate. Canonical sources: `src/data/insights.ts`, `docs/Pharos/whitepaper/resource-constrained-deployment-playbook.md` (exec summary), `public/infographics/inside-the-90-agent-company.html`, `public/infographics/open-source-stack.html`, `public/visuals/graduated-autonomy-ladder.html`.*
