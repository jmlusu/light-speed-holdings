---
title: "How Our Agents Ask Permission: The 5-Tier Approval System Behind 90 Agents"
status: Draft — awaiting CEO approval
word_count: 1965 (body)
pillar: Governance
claims_ledger:
  - claim: "90 agents across 20 departments"
    source: "docs/Pharos/positioning.md:61; docs/Pharos/manifesto-draft.md:107-109; company-registry.yaml (direct count 2026-09-23)"
  - claim: "Five tiers: Auto / Notify / Single Approve / Dual Approve / CEO Only"
    source: "docs/APPROVAL-UX-SPEC.md:16-22"
  - claim: "Friction scales with risk; no silent failures; auditability by default; timeout is never final"
    source: "docs/APPROVAL-UX-SPEC.md:9-12"
  - claim: "Tier 2: any operator, 60 min escalate to Tier 3 approver; Tier 3: any 2 operators, 30 min escalate to CEO; Tier 4: CEO only, 24 hr to board notification"
    source: "docs/APPROVAL-UX-SPEC.md:20-22"
  - claim: "Timeout escalates and never auto-approves or auto-deletes"
    source: "docs/APPROVAL-UX-SPEC.md:12; docs/APPROVAL-UX-SPEC.md:366-372"
  - claim: "H-A-O-M-T-G-V Governance layer"
    source: "docs/Pharos/positioning.md:41-52"
atomization:
  - "1 LinkedIn long-form post — the five tiers told as a permission story, CTA to the Monitor"
  - "1 X thread — 7 posts: friction principle → tier table → one timeout walkthrough → escalation → two-person rule → audit trail → regulator CTA"
  - "5 Instagram carousel slides — (1) the four principles, (2) tier 0-1 invisible, (3) tier 2-3 gates, (4) tier 4 CEO lock, (5) escalation never drops"
  - "1 YouTube script (4-6 min) — live approval queue demo, one pending Tier 3 card resolving end-to-end"
---

# How Our Agents Ask Permission: The 5-Tier Approval System Behind 90 Agents

*Pillar 02 of the Pharos Governance series — a technical but human-readable
walkthrough of how we keep humans in the loop without slowing agents to a
crawl.*

---

## One sentence, three decisions

Let me start with the design principle that governs everything else:

**Friction scales with risk.**

A 90-agent company operating 20 departments cannot ask a human for permission
on every action. Nobody would work there — the humans would drown in
notifications and the agents would be useless. But a company that lets agents
act without gates is not a company; it is an ungoverned process running at
harness scale. The resolution is not zero risk or total control. It is a
five-tier system where the amount of human friction grows with the amount of
risk, and where a timeout is never, ever treated as permission.

The four principles behind the whole system, in the order I will defend them:

1. **Friction scales with risk** — Tier 0–1 are invisible; Tier 3–4 force
   deliberate human action.
2. **No silent failures** — every timeout produces a visible escalation, never
   a silent drop.
3. **Auditability by default** — every approval or rejection is logged with
   who, when, and why.
4. **Timeout is never final** — a timeout escalates upward; it never
   auto-approves and never auto-deletes.

This is not a theory document. Everything below is the operating system of a
live enterprise, and I will show you the exact mechanics.

## The five tiers

### Tier 0 — Auto (no approval needed)

Reading, listing, searching, recalling. These actions pose no material risk and
require no human attention. The agent executes immediately; the action appears
in the task execution log. This is where most agent work lives, and that is
correct. Governance that gates every read is governance theater.

### Tier 1 — Notify (log only)

Memory storage, routine task completion, status updates. The action executes,
and a notification entry is written to the approval log for audit purposes.
The operator sees it in history as a completed entry with a `[T1]` badge —
never in the approval queue, never blocking. This is the layer that makes
auditability possible without making humans the bottleneck.

### Tier 2 — Single Approve (one human)

Editing code, budget changes under $100, configuration changes. Any operator
can approve. The request carries an ID, an agent name, an action category, a
risk score, a description, and a hard deadline. If nobody resolves it within
**60 minutes**, it escalates to the Tier 3 approvers, and the original agent
remains blocked.

The key detail for skeptics: the timeout that fires is an escalation, not a
silent acceptance. The request changes status to `escalated`, and a new
request is created at Tier 3 with `escalated_from` pointing back to the
original. The agent's poll loop detects the status change and stays blocked
until the new request resolves.

### Tier 3 — Dual Approve (two humans)

Shell execution, deleting data, spending over $500, production deployment.
This is the tier where the stakes are real, so we require **two distinct human
approvers**. One signature is not enough. The request tracks `0 of 2`
approvals, and the second approver can never be the same person as the first —
the system rejects self-approval outright.

If the request is not fully resolved within **30 minutes**, it escalates to
the CEO. The agent stays blocked. Two humans, a strict count, and a hard
escalation path.

### Tier 4 — CEO Only (explicit CEO authorization)

Constitutional changes, deploying a new agent, restructuring the organization.
No other approver may substitute. The request carries a risk score in the
high 90s, a lock icon, and an unambiguous message: *this action requires
explicit CEO authorization.* If the CEO has not acted within **24 hours**, the
board is notified — and the request does not vanish. It stays in the CEO's
queue with an `[EXPIRED]` badge until the CEO explicitly acts on it.

Tier 4 never auto-resolves. It is the upper bound of the system, and the point
where organizational design meets the founders themselves.

## Why the timeout rule is the whole ballgame

Most systems treat a timeout as a fallback: if nobody answered, the request
eventually proceeds or dies. If you run a 90-agent company for even one day
with that rule, you will see the flaw instantly. A fallback deadline is a
pressure release valve for the humans — and pressure release valves, when
agents are involved, become default permission.

Our rule is the opposite. **A timeout is never final and never permissive.**
It always escalates upward:

- Tier 2 times out → Tier 3 approvers
- Tier 3 times out → CEO
- Tier 4 times out → board notification (and the request stays visible)

When a request escalates, the system creates a linked request with a new ID,
`escalated_from` pointing at the original, a tier one level higher, and the
appropriate approval count for the new tier. The agent's poll loop continues
on the new request. Nothing is dropped. Nothing is silently approved. The
human who was too busy, or the approver who ignored the queue, is not rewarded
with an automatic yes — the ask gets louder and more senior until a human
actually answers.

## The tool-to-tier mapping: where the rubber meets the rule

The abstraction is a single table, and that table is where governance becomes
architecture:

| Tool | Default Tier | Override |
|------|-------------|----------|
| `read` | T0 | — |
| `grep` | T0 | — |
| `list` | T0 | — |
| `write` (edit files) | T2 | T3 if path is in `/etc/` or production dirs |
| `execute` (shell) | T3 | T2 if command is allowlisted |
| `delete` | T3 | T4 if deleting audit logs or configs |

A few notes on why this table is the product, not the demo:

- **The default tier is the risk floor, not the ceiling.** Overrides only raise
  risk, never lower it.
- **File edits are Tier 2; shell execution is Tier 3.** This is a deliberate
  posture: executing an arbitrary command is riskier than editing a file, and
  the table says so.
- **Deleting audit logs or configs is Tier 4**, not Tier 3. Because if an
  actor — human or agent — can delete the evidence trail, the whole audit
  story collapses. That is a constitutional line, and we treat it as one.

This is the mapping regulators should ask to see. Any organization claiming to
run governed agents should be able to produce exactly this table, updated when
the risk profile changes, and audited when a mistake happens.

## What the two-person rule catches

The human failure mode that the tier system is most defensively designed
against is not rogue AI. It is single-person dominance: one operator who can
approve their own risky action, one executive who rubber-stamps, one shared
password. Tier 3's two-distinct-approvers rule is the countermeasure, and the
system enforces it mechanically:

- First approval: "Signature recorded — status 1 of 2, awaiting second
  approver."
- Same person tries again: "DENIED: already signed this request. Tier 3
  requires two DISTINCT approvers."
- Second, different approver: "APPROVED (2/2 signatures)."

The audit log records who approved, when, why, and in what order. There is no
way to retroactively manufacture a second signature. This is what
organizational governance looks like when it is enforced by the system rather
than by a policy document that nobody re-reads.

## Where this sits in the H-A-O-M-T-G-V framework

In the framework we publish for the region, Governance is the G layer — the
shared control surface that governs permissions, humans, agents, audit, and
risk as one coherent system. The five tiers are the practical embodiment of
that layer.

The reason the framework exists at all is that most regional conversations
about AI governance are still stuck at the level of principles: "be
transparent," "be fair," "be accountable." Those are necessary, but they are
not implementable. A minister cannot inspect a principle. A regulator cannot
test a value statement. What they can inspect and test is a tier table, a
timeout rule, an escalation path, and an audit log.

That is not an argument against principles. It is an argument for engineering
them in.

## What a regulator can take today

If your job is to write or enforce AI policy in an African context, here is the
honest, transferable core of what we run:

1. **Ask for the tier table.** Every deployment should be able to state what
   risk classifies to which tier and who approves what.
2. **Test the timeout rule.** Ask what happens at 59 minutes, at 90 minutes,
   and at 25 hours. If the answer is "it dropped" or "it auto-approved,"
   that is a governance weakness, not a feature.
3. **Audit the audit trail.** Who, when, why, and in what order. If the
   evidence trail can be modified by the agent being audited, the governance
   fails at the exact point where it most needs to hold.
4. **Require two-person rules for irreversible actions.** Deleting data,
   spending money, deploying to production, changing constitutional decisions
   — none of these should hang on a single person's rubber stamp.

None of this is exotic. It is the same discipline banks and hospitals learned
decades ago, translated to a world where the actor performing the action is a
software agent.

## The honest trade-off

I will not pretend the tiers are free. Tier 2 and Tier 3 requests block agents
until humans respond, and human response is the scarcest resource in the
company. There are days when the queue is the controller of the workflow, and
that is annoying.

But the alternative is worse, and I can describe it from experience: post-hoc
review. Architecture that never earns a Chief Risk Officer's or a minister's
"yes." A governance layer built after the incident, playing catch-up, while
the agent that caused the problem is still running. The cost of the queue is
the price of the permission. It is the discipline that makes a 90-agent
company deployable outside a laboratory — and it is the discipline that makes
the H-A-O-M-T-G-V framework worth publishing at all.

## Call to action

If you run an enterprise deploying AI agents, ask yourself tonight: *what does
my system do at the timeout?* If the honest answer is anything other than "it
escalates to a more senior human and never auto-approves," you have
governance-shaped risk, and you should fix it before the regulator — or the
incident — finds it.

The next pillar in this series is the region-facing argument: the four
reservations that African risk officers and ministers raise against AI, and
the engineering answers to each. It goes out through the Malawi Agentic AI
Monitor, and if you want it in your inbox, subscribe at the link below.

---

## Atomization Plan

| Channel | Form | Leader line |
|---------|------|-------------|
| LinkedIn long-form | ~1,300-word extract | "What does your approval system do when nobody answers? If the answer is not 'it escalates,' you have governance-shaped risk." |
| X thread | 7 posts | 1) friction principle → 2) tier table → 3) timeout walkthrough → 4) escalation path → 5) two-person rule → 6) audit trail → 7) regulator CTA |
| Instagram carousel | 5 slides | 1) four principles, 2) T0–1 invisible, 3) T2–3 gates, 4) T4 CEO lock, 5) "timeout escalates, never drops" |
| YouTube script | 4–6 min | Live approval-queue demo: one pending Tier 3 card resolving end-to-end with two signatures |

*Draft by the Pharos thought-leadership team on behalf of the Human CEO. All
claims trace to the ledger above; pending CEO review before any publication.*
