# H-A-O-M-T-G-V: What Running a 152-Agent Company Taught Us About Governance

**By Jack Mlusu, Founder & CEO, LightSpeed Holdings**

**Status:** Draft for Human CEO review before publication (Substack / LinkedIn long-form).
**Target:** 1,800-2,400 words.

---

Software is leaving the chat window.

For two years, most organizations treated AI as a content engine. It drafted
emails, summarized documents, generated images. That is generative AI, and just
as most companies got comfortable with it, the terrain moved. The next wave is
agentic AI: software that plans a multi-step task, decides which tools to call,
executes transactions, coordinates with other agents, and only pauses to ask a
human when the stakes are high enough to require one.

This is not a sharper chatbot. It is a digital workforce. And it forces a
question most organizations are avoiding: if software can perform meaningful
organizational work, how do you design a company around it?

At LightSpeed Holdings we did not answer that question on a whiteboard. We
answer it every day, because we run the experiment. The company is staffed by
152 agents across 20 departments, each with a documented role, a permission
boundary, and a reporting chain, overseen by human executives and a board that
exercises real oversight. Every high-impact action is gated behind a five-tier
human-in-the-loop approval system. Every decision path is written to an
immutable audit trail.

The rules that make that system safe and explainable fit into seven layers. We
call the framework H-A-O-M-T-G-V, after the seven pillars. This is what each
pillar does, and what we learned building it.

A line to retain the seven: *Humans authorize, agents act, orchestration
orders, models run sovereign, tools stay tamed, gates govern, and verification
vouches.*

## H — Humans stay accountable

Most AI projects start with the model. The right place to start is the human.

In an agentic company, humans keep the work they are most accountable for:
strategy, ethics, leadership, relationships, and the final answer. Agents are
delegates, not principals. They take on the work; they do not take on the
responsibility.

The consequence is structural, not cultural. High-impact actions, spending, and
policy changes sit behind a five-tier approval matrix. No money moves and no
irreversible action executes without cryptographic human sign-off. And the
system is built so a delegation can always be pulled back. The human is the
last line of code in the organization.

The failure mode is obvious in hindsight: hand authority to an agent without a
sign-off path and the system gets fast, then ungovernable.

## A — Agents are a workforce, not a chatbot

A single "AI" that can do everything is an empty promise and an audit
nightmare. So we stopped talking about "the AI" and started talking about a
roster.

Each of our 152 agents is a discrete persona with an explicit domain scope, a
declared set of tools, and a deterministic escalation path. The roster is
defined once in `company-registry.yaml`, compiled mechanically into agent cards,
and treated like an org chart: readable, countable, auditable.

When a task exceeds an agent's scope, it escalates. It does not improvise.

## O — Orchestration orders the work

Agents do not improvise in parallel. Work flows through a message bus as tasks,
each with an owner, a lifecycle, and a dead-letter path when something fails.
Nothing important happens that is not on the bus.

The same discipline applies to the organization itself. Departments, budgets,
and data-classification rules are encoded as schemas, not policy PDFs. "Is this
allowed?" becomes a query, not a meeting.

## M — Models run sovereign

Two things share this pillar, and both matter.

First, inference runs in-country. Our models run on sovereign infrastructure,
with local fallbacks and a circuit breaker, so the organization is not exporting
its operations or its telemetry to a public cloud it does not control. Sovereignty
is a deployment property. If it is not in the architecture, it is not real.

Second, the organization learns. Decisions, context, and lessons are captured
in a structured memory, so the company does not rediscover what it already
knows on every new task.

## T — Tools stay sandboxed

An agent's world is a closed set of tools. Ours compile to seven primitives:
reading, editing, searching, listing, running controlled commands, fetching web
content, and launching sub-agents. No arbitrary code execution. No hidden
gateways. The runtime rejects anything outside that list.

This is what gives "what can this agent do?" a finite answer. Governance
requires that question always be answerable.

## G — Gates govern before execution

Control happens before the action, not after the incident. Every agent proposal
is checked against thresholds, budgets, and regulatory covenants before an
external write event fires. State transitions are deterministic: pending,
approved, rejected, expired. A sweep regularly clears stale approvals so a
forgotten request never blocks the queue or slips through.

We treat post-hoc review as archaeology, not governance. By the time you are
reading logs, the damage is already on the bus.

## V — Verification vouches

Every prompt, tool call, human decision, and API response is written to a
cryptographic hash chain. Auditing is a byproduct of running the company, not a
separate exercise that happens in the last quarter before an inspection.

Above the trail, outcomes are measured: cost, productivity, service delivery,
and impact, tracked against KPIs with honest status. In a system where a human
must eventually answer for results, the results have to be verifiable. And the
measurement is the point of the whole structure. Seven layers of control exist
so that the value the company produces is real, attributable, and provable to
the people it serves.

## Why this matters in Malawi and SADC

The region's institutions are not afraid of the technology. They are afraid of
ungoverned deployment. When a risk officer or a minister says no to AI, they
are rarely rejecting the idea. They are raising four legitimate reservations:

- It will not work on our bandwidth and our devices.
- Where does our data go?
- Will this become a second system we maintain forever?
- We tried AI before and it failed. Why would this be different?

H-A-O-M-T-G-V answers each one from the architecture, not from a slide deck.

Bandwidth is a budget we engineer to, not an obstacle. Work queues locally and
syncs when connectivity returns; the same batch of agents runs on a district
connection that would starve a cloud dependency. Data sovereignty is the M
pillar: inference runs in-country on our own infrastructure, cross-border flows
are documented if they exist at all, and the audit trail proves where each
action happened. The tech-debt objection meets the opposite answer: the system
integrates with the existing stack in a ninety-day pilot instead of ripping it
out, and because every agent is a bounded role with a finite toolset, there is
no sprawling undocumented surface left to inherit. And the "we tried AI before"
skepticism meets the one answer a story cannot give it: a working company, with
an immutable trail, running the framework in production today.

## How we built it

The order of construction matters, because the pillars are load-bearing.

**One: the registry.** Every agent starts as a row in a YAML registry: id,
role, manager, tools, permissions, escalation path. No agent exists in the
runtime that is not in the registry. That single file is what makes the roster
countable and auditable instead of ad hoc.

**Two: the generator.** Agent cards are compiled from the registry by a
template generator. The system never hand-writes agent definitions, so the
runtime can never drift from the registry without failing visible.

**Three: the sandbox.** Before any agent ran, the tool boundary was closed.
Seven canonical primitives, nothing else. If the runtime is asked for an
eighth, it refuses. This is the layer that makes "governance" a property of
execution rather than a policy document.

**Four: the gates and the queue.** Work enters through a message bus. Each task
has an owner and a lifecycle; high-impact tasks wait at a five-tier approval
gate until a named human signs off. Nothing important bypasses the queue and
nothing high-impact bypasses the gate.

**Five: the trail.** From the first day, every prompt, tool call, approval, and
response has been written to a hash-chained audit log. The company's history is
a cryptographic record, which is the only honest foundation for the claim that
the framework works.

None of these five steps was a pilot. They are the operating conditions of the
company.

## The proof is the point

We did not build a demo. We built a company, and the framework is how we keep
it safe enough to run every day. The numbers are the credibility: 152 agents,
20 departments, five-tier approvals, seven sandboxed tools, immutable audit
trails.

Theories earn attention. Numbers earn trust. The region is not short of
commentary on AI. It is short of documented, governed, quantified deployments.
Our job is to build more of them, publish them, and give the policy makers of
Malawi and SADC a working reference they can point to.

## What happens next

The framework is not finished. None of the seven pillars is a static
configuration: the roster grows, the policy engine learns new covenants as the
Data Protection Act and regional guidelines settle, and the audit trail keeps
growing by the day. What matters is that the layer below each change holds.
Whatever moves, the human stays accountable, the scope stays bounded, and the
record stays verifiable. That is the property this framework exists to protect,
and it is the one thing we will not trade for speed.

If you are a policymaker, a regulator, a CIO, or an enterprise leader in
Malawi or Southern Africa working through what agentic AI means for your
institution, the door is open. Come see the system, read the framework, and
help us build the measurement and the governance together.

---

## Publication notes

- **Tone:** builder-advocate. Proof before principle, no hype, no emojis.
- **Primary home:** Substack long-form; LinkedIn republish with the summary in
  the post body.
- **Hashtags:** `#AgenticAI` `#AIGovernance` `#AINativeCompany` `#Malawi` `#SADC`
- **Fact checklist:** 152 agents / 20 departments (`docs/Pharos/positioning.md:61`),
  5-tier approvals (`docs/Pharos/manifesto-draft.md:64-80`), 7 canonical tools
  (AGENTS.md §8), SHA-256 audit chains (`h-a-o-m-t-g-v-framework.md` §3-V).
- **Review gate:** Human CEO approval before any publication; then route through
  reservations-playbook demo beat per objection before lock-in.
