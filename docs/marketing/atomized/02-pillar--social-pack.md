# Pillar 02 — Social Pack (Atomized)

**Source pillar:** `docs/Pharos/pillars/02-5-tier-human-in-the-loop.md`
**Pack status:** Draft — awaiting CEO approval (#189/#195/#196); post only after #194 accounts exist
**Voice:** Builder register, CEO-voice first person, no emojis, no hype. `™` on first mention of LightSpeed Holdings Limited. Tagline verbatim: `ASPIRE. ACT. ACHIEVE.` (on-image only where a tagline slot exists).
**Claims source:** pillar claims_ledger (fact checklist at bottom).
**Template system:** P1 foundational templates (ticket #311) — canonical PNGs at `static/brand/social/templates/`. Slot keys per `static/brand/templates/social-templates/GENERATED-P1.md`.

**ADD fact (flagged once per pack):** the Malawi Agentic AI Monitor subscription URL is not stated in the pillar ("subscribe at the link below"). This pack uses the established site root `https://lightspeedholdings.com` (`docs/BRAND_DEPLOYMENT_GUIDE.md:46`). `ADD: Malawi Agentic AI Monitor subscription URL — requires pillar update.`

---

## LinkedIn long-form post

**Status:** Draft — awaiting CEO approval (#189/#195/#196); post only after #194 accounts exist
**Format:** Feed long-form, text-only, evidence-led, builder register. Char count below is verified against the LinkedIn 3,000 limit; warmup convention targets ~1,800–2,500.
**Characters:** 2,184 chars (within LinkedIn 3,000 limit)

```text
What does your approval system do when nobody answers?

If the answer is anything other than "it escalates to a more senior human and never auto-approves," you have governance-shaped risk.

LightSpeed Holdings Limited™ runs 152 agents across 20 departments. A company that lets agents act without gates is not a company — it is an ungoverned process running at harness scale. The resolution is not zero risk or total control. It is a five-tier system where human friction grows with risk.

Tier 0 — Auto. Reading, listing, searching, recalling. No gate. Most agent work lives here; it appears in the task log.

Tier 1 — Notify. Log only. Memory storage, routine task completion, status updates. Humans see it in history, never in the queue.

Tier 2 — Single Approve. One human operator. Editing code, budget changes under $100, configuration changes. Sixty minutes, then it escalates to a Tier 3 approver. The agent stays blocked.

Tier 3 — Dual Approve. Two distinct humans. Shell execution, deleting data, spending over $500, production deployment. Thirty minutes, then it escalates to the CEO. The second signer can never be the first signer.

Tier 4 — CEO Only. Explicit CEO authorization. Constitutional changes, deploying a new agent, restructuring. Twenty-four hours, then the board is notified — and the request stays in the CEO's queue until the CEO acts. It never auto-resolves.

The rule that governs all of it: a timeout is never final and never permissive. When a request escalates, a linked request is created with escalated_from pointing at the original — nothing drops into a silent void. The human who ignored the queue is not rewarded with an automatic yes; the ask gets louder and more senior until a human answers.

What a regulator can take today: ask for the tier table. Test the timeout rule. Audit the audit trail. Require two-person rules for irreversible actions.

The cost of the queue is the price of the permission. It is the discipline that makes a 152-agent company deployable outside a laboratory.

Everything else goes out monthly through the Malawi Agentic AI Monitor.

https://lightspeedholdings.com

#AgenticAI #AIGovernance #HumanInTheLoop #Malawi
```

### LinkedIn carousel companion (slot map)

The LinkedIn carousel companion uses the same five-slide square set as the Instagram carousel below — all 1080×1080 P1 templates. Generate with `uv run python static/brand/templates/generate-post-templates.py --template <name> --slots '{"key": "value"}'` per slide.

| Slide | P1 template (canonical PNG) | Slot keys used |
|-------|------------------------------|----------------|
| 1 | `static/brand/social/templates/stat-card.png` | `number`, `label`, `context`, `source`, `tagline` |
| 2 | `static/brand/social/templates/linkedin-carousel-cover.png` | `title`, `subtitle`, `tagline` |
| 3 | `static/brand/social/templates/linkedin-carousel-cover.png` | `title`, `subtitle`, `tagline` |
| 4 | `static/brand/social/templates/linkedin-carousel-cover.png` | `title`, `subtitle`, `tagline` |
| 5 | `static/brand/social/templates/quote-card.png` | `quote`, `author`, `role`, `tagline` |

---

## X thread (5 posts)

**Status (all posts):** Draft — awaiting CEO approval (#189/#195/#196); post only after #194 accounts exist
**Rules:** No links in posts 1–4; only post 5 carries the site link (warmup shadowban protocol). Hashtags on post 1 (`#AgenticAI`) and post 2 (`#AIGovernance`) only. Char counts below verified against X 280 limit.
**Deviation note:** pillar atomization plan lists 7 posts; per the atomization brief this pack compresses to 5 (tier table + two-person rule beats merged) — beats from the pillar plan map: 1→friction principle (post 1), 2→tier table (post 2), 3→timeout walkthrough (post 3), 4→escalation path (post 3), 5→two-person rule (post 4), 6→audit trail (post 4), 7→regulator CTA (post 5).

### Post 1 (friction principle)
**Characters:** 254 chars (within X 280 limit)

```text
Friction scales with risk. A 152-agent company cannot ask a human for permission on every action — the humans would drown. But a company that lets agents act without gates is not a company; it is an ungoverned process running at harness scale. #AgenticAI
```

### Post 2 (tier table)
**Characters:** 228 chars (within X 280 limit)

```text
Five tiers: Auto. Notify. Single Approve — one human. Dual Approve — two distinct humans. CEO Only. The amount of human friction grows with the amount of risk. The default tier is the risk floor, never the ceiling. #AIGovernance
```

### Post 3 (timeout walkthrough + escalation)
**Characters:** 222 chars (within X 280 limit)

```text
What happens at the timeout? Ours escalates. Tier 2 times out to Tier 3 approvers, Tier 3 to the CEO, Tier 4 to the board. Never auto-approves. Never auto-deletes. The ask gets louder and more senior until a human answers.
```

### Post 4 (two-person rule + audit trail)
**Characters:** 194 chars (within X 280 limit)

```text
Tier 3 requires two distinct human approvers. The system rejects self-approval outright — "DENIED: already signed this request." The audit log records who approved, when, why, and in what order.
```

### Post 5 (regulator CTA)
**Characters:** 230 chars (within X 280 limit)

```text
Ask your system tonight: what does it do at the timeout? If the answer is not "it escalates to a more senior human and never auto-approves," fix it before the regulator — or the incident — finds it.

https://lightspeedholdings.com
```

---

## Instagram carousel (5 slides)

**Status (all slides):** Draft — awaiting CEO approval (#189/#195/#196); post only after #194 accounts exist
**Note:** Only square 1080×1080 P1 templates are used. Excluded by aspect: `reels-shorts-cover.png` (1080×1920), `thread-header.png` (1200×675), `youtube-thumbnail.png` (1280×720).

### Slide 1 — four principles
**Template:** `static/brand/social/templates/stat-card.png` — slots: `number`, `label`, `context`, `source`, `tagline`

```text
number: 4
label: Principles behind the whole system
context: Friction scales with risk. No silent failures. Auditability by default. Timeout is never final.
source: docs/APPROVAL-UX-SPEC.md:9-12
tagline: ASPIRE. ACT. ACHIEVE.
```

### Slide 2 — T0–1 invisible
**Template:** `static/brand/social/templates/linkedin-carousel-cover.png` — slots: `title`, `subtitle`, `tagline`

```text
title: Tier 0–1: invisible by design.
subtitle: Auto actions execute and appear in the task log. Notify writes an audit entry with a [T1] badge. Humans see history — never the queue, never a bottleneck.
tagline: ASPIRE. ACT. ACHIEVE.
```

### Slide 3 — T2–3 gates
**Template:** `static/brand/social/templates/linkedin-carousel-cover.png` — slots: `title`, `subtitle`, `tagline`

```text
title: Tier 2–3: the gates.
subtitle: Single Approve — one human, 60 minutes, then a Tier 3 approver. Dual Approve — two distinct humans, 30 minutes, then the CEO. The agent stays blocked either way.
tagline: ASPIRE. ACT. ACHIEVE.
```

### Slide 4 — T4 CEO lock
**Template:** `static/brand/social/templates/linkedin-carousel-cover.png` — slots: `title`, `subtitle`, `tagline`

```text
title: Tier 4: CEO only.
subtitle: Constitutional changes, deploying a new agent, restructuring. Risk score in the high 90s, a lock icon, 24 hours to board notification. It never auto-resolves.
tagline: ASPIRE. ACT. ACHIEVE.
```

### Slide 5 — escalation never drops
**Template:** `static/brand/social/templates/quote-card.png` — slots: `quote`, `author`, `role`, `tagline`

```text
quote: A timeout escalates upward. It never auto-approves and never auto-deletes.
author: Jack Mlusu
role: Human CEO, LightSpeed Holdings Limited™
tagline: ASPIRE. ACT. ACHIEVE.
```

---

## YouTube script (~90s)

**Status:** Draft — awaiting CEO approval (#189/#195/#196); post only after #194 accounts exist
**Runtime:** ~90 seconds (~150 spoken words) — compressed from the pillar's planned 4–6 min per the atomization brief.
**Format:** Live approval-queue demo — one pending Tier 3 card resolving end-to-end with two signatures.

```text
[OPEN 0:00–0:08] On screen: approval queue — one pending Tier 3 card: "Deploy to production."
VO: This is what governed agentic AI looks like at the moment of risk. One pending approval. It will not move until two distinct humans sign.

[0:08–0:20] On screen: card details — risk score, deadline, 0 of 2 approvals.
VO: The card carries an ID, an agent name, an action category, a risk score, and a hard deadline. Friction scales with risk — this one is Tier 3.

[0:20–0:38] On screen: first approver signs; status "1 of 2, awaiting second approver"; same person retries → DENIED.
VO: The first signature records. If the same person tries again, the system denies it: Tier 3 requires two distinct approvers. Single-person dominance is the failure mode we engineered against.

[0:38–0:58] On screen: second, different approver signs → "APPROVED (2/2 signatures)"; audit log scrolls who, when, why, order.
VO: The second approver signs from a different account. Approved. The audit log records exactly who approved, when, why, and in what order — and it cannot be rewritten.

[0:58–1:15] On screen: timeout path diagram.
VO: And if nobody had signed? At 30 minutes this card would escalate to the CEO — never auto-approve, never drop. The ask gets louder until a human answers.

[1:15–1:30] End card: https://lightspeedholdings.com.
VO: Ask your system tonight: what does it do at the timeout?
```

---

## Fact checklist

Every claim above is verbatim-consistent with the source pillar body and ledger:

| Claim | Source |
|-------|--------|
| 152 agents across 20 departments | `docs/Pharos/positioning.md:61`; `docs/Pharos/manifesto-draft.md:107-109`; `company-registry.yaml` (direct count 2026-09-17) |
| Five tiers: Auto / Notify / Single Approve / Dual Approve / CEO Only | `docs/APPROVAL-UX-SPEC.md:16-22` |
| Friction scales with risk; no silent failures; auditability by default; timeout is never final | `docs/APPROVAL-UX-SPEC.md:9-12` |
| Tier 2: any operator, 60 min escalate to Tier 3 approver; Tier 3: any 2 operators, 30 min escalate to CEO; Tier 4: CEO only, 24 hr to board notification | `docs/APPROVAL-UX-SPEC.md:20-22` |
| Timeout escalates and never auto-approves or auto-deletes | `docs/APPROVAL-UX-SPEC.md:12; 366-372` |
| H-A-O-M-T-G-V Governance layer | `docs/Pharos/positioning.md:41-52` |
| Website root | `docs/BRAND_DEPLOYMENT_GUIDE.md:46` |

## Deviations from pillar atomization plan

- X thread: 5 posts (brief) vs 7 posts (pillar plan) — beats merged, mapping noted above.
- LinkedIn: feed post 2,184 chars (verified ≤3,000 limit) vs ~1,300-word extract (pillar plan) — full extract via LinkedIn Articles once #194 accounts exist.
- YouTube: ~90s (brief) vs 4–6 min (pillar plan).
- Instagram: slides use square 1080×1080 P1 templates only; vertical `reels-shorts-cover.png` excluded per brief (short-video scripts are not part of this deliverable).
