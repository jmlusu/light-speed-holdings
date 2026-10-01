from ai_company.publishing.queue import PublishQueue

queue = PublishQueue()

# Post 1 body - the LinkedIn article body from draft-v1.md
body_post1 = """Most organizations adopt AI the way they adopted email: they buy tools, hand them to people, and hope for a transformation. Nothing about that approach makes the organization AI-native. It makes the organization a traditional organization with a new expense line.

An AI-native organization is different in kind, not degree. It is an organization deliberately engineered so that AI agents perform meaningful, coordinated work -- and so that humans remain accountable for what those agents do. The agents are not a feature layered on top of an old operating model. They are part of the structure, with owners, budgets, metrics, and governance as real as any department you would find on an org chart.

We know this because we did not write a deck about it. LightSpeed Holdings runs one.

### An AI-native organization is engineered, not equipped

The distinction matters because "we use AI" hides three very different realities:

1. **Tool users.** People paste prompts into chat windows. Output quality depends on who is having a good day. Nothing is measured, nothing is audited, and nothing compounds.

2. **Process automation.** Scripts and copilots speed up known tasks. Useful, but the work still routes exclusively through humans, so throughput is still bounded by headcount.

3. **AI-native.** Agents are first-class participants in the operating model. They own defined tasks, they coordinate through a shared queue, they are measured like staff, and they act inside permission boundaries that humans set and can revoke.

The third state is engineered. It requires an agent registry rather than a folder of prompts. It requires a task queue rather than a chat history. It requires approval gates rather than "the model seemed confident." None of these are exotic -- but none of them appear by default when you buy a licence.

### What we actually run: 90 agents, 20 departments

At LightSpeed Holdings, the operating model looks like this:

- **90 AI agents** defined in a single company registry, each with a named role, a domain scope, and an explicit permission boundary. The registry is the source of truth; if an agent is not in it, it does not exist. (Confirmed at 90 agents across ADR-032.)
- **20 departments**, from engineering and security to sales, finance, and Pharos -- our thought-leadership function. Agents are assigned to departments, and department health rolls up to an executive scorecard rather than being inferred.
- **One message bus.** Every task enters a crash-safe, idempotent queue; the executor loop picks work up, records audit logs, and re-enqueues through a dead-letter path when something fails. No task is executed by vibes.
- **Measured like staff.** Agent Utilization (KPI-003) tracks engagement per department against a target window; Build Success Rate (KPI-004) measures delivery health. If a department's agents are idle or its pipeline is red, someone sees it -- the same way a human manager would see an idle team.

That is what "AI-native" means in practice: agents are on the payroll metaphorically, in the registry literally, and in the metrics unambiguously.

One clarification worth making, because it is where the definition usually gets watered down. An AI-native organization is not a company where every employee has a chat assistant. Assisted humans are still the whole workflow; the organization's throughput, quality, and error rate still move with headcount and mood. In an AI-native structure, removing an agent from the registry removes owned work from the system -- and the queue, the metrics, and the department scorecard all reflect it within a reporting window. The test is not "do people use AI." The test is "does the organization's operating structure change when the agents change?"

### Human Purpose: the layer that makes all of it governable

This is where most AI adoption stories stop, and where the H layer of our H-A-O-M-T-G-V framework begins.

H -- Human Purpose and Authority -- is the constitutional layer. Strategy, ethics, leadership, relationships, and final accountability stay with named humans. Agents are delegates, never principals. The delegation is reversible, and the human is the one who answers for the outcome.

In our architecture, that principle is not a value statement. It is a mechanism: a five-tier human-in-the-loop approval matrix (ADR-017) that moves every agentic decision through autonomous → HITL-approved → reviewed → snoozed → cleared. Low-risk work proceeds without ceremony. High-impact actions -- treasury movements, policy changes, external commitments -- sit behind explicit human sign-off. An approval sweep retires stale requests so a forgotten pending item can neither block the system nor slip through it silently.

The failure mode this prevents is easy to name. Hand authority to agents without a sign-off path and the system moves faster while nothing is accountable. Speed without accountability is not a capability; it is an incident waiting for a date.

The regulator's version of the check is simple: who, by name, authorized this action? Is the authorization logged? Can the principal delegate less tomorrow? In our case the answer to all three is documented, mechanical, and auditable.

### What this means for Malawi and SADC

For institutions in Malawi and across SADC, the AI-native question is not whether to match a Silicon Valley headcount. It is how to build accountability into the architecture before scale makes it painful -- under constraints that generic AI advice ignores:

- **Sovereign data by default.** Data Protection Act 2017/2024 compliance and GDPR-grade handling are defaults, not afterthoughts. Regulated sectors -- banking, health, telco -- cannot treat data residency as a roadmap item.
- **Low-bandwidth operation.** Offline-first design, local and fallback model runtimes, and messaging-native interfaces (including WhatsApp-style queues) mean the system works where connectivity does not always cooperate.
- **Visible variable cost.** No rip-and-replace, no multi-year lock-in. A 90-day pilot with per-agent cost visible from week one means an institution can decide with a invoice in hand rather than a forecast.
- **Revenue-funded experimentation.** Our agent economy is underwritten by recurring products rather than a blank cheque -- a pattern any SME or parastatal can mirror at 8–12 agents instead of 90.

There is also a procurement argument. Institutions in our region will be asked to approve AI spending they cannot fully inspect. An architecture where agents are registry entries, actions are approval-gated, and utilization is a dashboard number converts that conversation from trust-me to check-this. Buyers, regulators, and boards can audit the structure without understanding the models -- which is exactly the point of putting governance in the architecture rather than in the prompt.

The framework does not require believing our numbers. It requires checking our receipts -- and we publish them.

### The rest of the framework -- and what follows

H is the first of seven layers: Humans authorize, Agents act, Orchestration orders the work, Models run sovereign, Tools stay sandboxed, Gates approve every high-impact move, and Verification records it all -- so value can be proven, not promised.

Over the next two posts we take the layers in order. Next: what running 90 agents actually means -- the registry, the roles, the cost curve, and why the number matters less than the boundaries around it. Then: the orchestration layer that keeps twenty departments moving as one system.

Follow along if you are building, governing, or procuring AI in Malawi and the SADC region -- and want the engineering receipts, not the marketing."""

# Enqueue Post 1
record = queue.enqueue(
    platform='linkedin',
    title='What is an AI-Native Organization?',
    body=body_post1,
    notes='Post 1 of AI-Native Organizations series, approved by CEO'
)

print(f"Enqueued Post 1: {record.id}")
print(f"Platform: {record.platform}")
print(f"Title: {record.title}")
print(f"Status: {record.status}")
print(f"Char count: {len(record.body)}")
print(f"Created at: {record.created_at}")