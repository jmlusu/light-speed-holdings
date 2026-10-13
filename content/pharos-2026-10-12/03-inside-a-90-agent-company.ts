import type { InsightArticle } from '../../src/data/insights';

export const article: InsightArticle = {
  slug: 'inside-a-90-agent-company',
  title: 'Inside a 90-Agent Company: What the Registry, the Queue, and the Approval Gate Actually Do',
  topic: 'AI COMPANY BUILDING',
  dek: 'Building ninety personas takes an afternoon. Making them safe to run takes a control plane: a registry, a message bus, and an approval gate that scales friction with risk.',
  category: 'AI Company Building',
  readMins: 8,
  publishedAt: '2026-10-12',
  source:
    'company-registry.yaml · src/ai_company/orchestrator/tier_rules.py · src/ai_company/orchestrator/approval.py · src/ai_company/orchestrator/message_bus.py · docs/Pharos/pillars/01-built-a-90-agent-company.md · docs/APPROVAL-UX-SPEC.md',
  blocks: [
    {
      kind: 'p',
      text: 'Most conversations about "AI companies" start with the model. Ours starts with the paperwork. LightSpeed Holdings runs 90 agents (89 AI personas plus one human CEO) across 20 departments. That count is not a marketing abstraction; it is a direct tally of company-registry.yaml, the single source of truth that defines every agent\'s identity, tools, approval level, and escalation path. The agents themselves are the easy part. A schema, a generator, and an afternoon will mint ninety personas. What took the discipline was everything that sits above them: how work is assigned, how actions are gated, and what happens when a human does not answer.',
    },
    { kind: 'h', text: 'The org is a registry, not a slide' },
    {
      kind: 'p',
      text: 'An AI-native company is not a chat window with a budget. It is an operating structure in which software owns defined work under human accountability. LightSpeed\'s structure is described by a seven-layer frame: Human, Agents, Orchestration, Memory, Tools, Governance, Value (H-A-O-M-T-G-V). Each layer is a design question, not a slogan. Humans keep strategy, ethics, leadership, and final answerability. Agents take research, monitoring, reporting, and other discrete knowledge work. Orchestration wires them together. Governance decides who must approve what.',
    },
    {
      kind: 'p',
      text: 'In practice, that structure is concrete files. company-registry.yaml lists every agent: id, department, reports_to, direct_reports, tools, approval_level, escalation_path, KPIs, and decision rights. The Chief of Staff reports to human_ceo and coordinates executives from CPO to CISO; a backend lead reports to the CTO; permissions are not folklore. They are fields. When someone asks "who can spend money?" the answer is a grep, not a meeting.',
    },
    { kind: 'h', text: 'The queue is the operating system' },
    {
      kind: 'p',
      text: 'Agents do not collaborate by osmosis. They collaborate through a task queue. The orchestrator\'s message bus persists work to a JSON inbox under a file lock, so concurrent agents, the dashboard, and the human operators cannot corrupt each other\'s updates. Every task carries identity and context; the briefing path turns a backlog of inbox items into something an agent can actually execute. This is unglamorous infrastructure, and it is the difference between ninety demos and a company. If you cannot point to where work lives between handoffs, you do not have an operating model; you have a pile of sessions.',
    },
    { kind: 'h', text: 'The control plane: five tiers, friction that scales with risk' },
    {
      kind: 'p',
      text: 'The layer that earned its keep is governance. Early on we did what most teams do: let agents act, then review afterwards. That approach died with one incident: a state-changing action no human had consciously authorized. Post-hoc review is archaeology. By the time you are reading the log, the action has already happened. The rebuild around a five-tier approval matrix, enforced in code rather than policy prose, is now the constitution of the company.',
    },
    {
      kind: 'ul',
      items: [
        'Tier 0: Auto-Approve. Read-only work: listing, searching, recalling. No gate; the action executes and lands in the log.',
        'Tier 1: Notify. Low-risk writes that humans should see in history but never in a queue: memory storage, routine status updates.',
        'Tier 2: Single Approver. Code edits, tests, sub-threshold changes. One human must approve; a timeout escalates rather than expires into silence.',
        'Tier 3: Two-Person Rule. Shell execution, production paths, destructive or high-spend actions. Two distinct humans (the second can never be the first), and a timeout climbs to the CEO.',
        'Tier 4: CEO Only. Constitutional moves: deploying a new agent, financial/legal/security exposure, changes to the rules of the company itself.',
      ],
    },
    {
      kind: 'p',
      text: 'Classification is not vibes. tier_rules.py maps tools and path fragments to tiers: secrets, legal, and compliance paths escalate to CEO-only; production and deploy paths hit the two-person rule; source and test paths require a single approver. Sensitive paths are tuples in code. When the executor evaluates a tool call, seniority caps and tool defaults combine into a tier, and the approval gate either lets it through or parks it for a human. The gate itself is a working store with versioned records, retention, and an append-only audit ledger of record: every request and every decision, including expiry sweeps that move stale pending items to EXPIRED instead of blocking a queue forever.',
    },
    {
      kind: 'quote',
      text: 'Friction scales with risk. Auditability is the default. Timeout is never final. It escalates; it does not silently pass.',
      cite: 'LightSpeed approval doctrine · docs/APPROVAL-UX-SPEC.md',
    },
    { kind: 'h', text: 'What broke, and what that taught us' },
    {
      kind: 'p',
      text: 'Three failures shaped the control plane more than any architecture slide. First, the post-hoc review failure above: governance that only inspects after the fact is not governance. Second, the silent-timeout trap. Early queues treated an unanswered approval as a soft failure; agents would stall or, worse, find a path that skipped the gate. The fix is boring and non-negotiable: every timeout produces a visible escalation, linked back to the original request via escalated_from, and nothing auto-approves on the way up. Third, metacharacter and shell-risk handling, flagged at request time so a pending tool call that will always be rejected is not silently retried into a loop.',
    },
    {
      kind: 'p',
      text: 'The pattern across all three is the same: make the dangerous path the explicit path. If an agent needs a human, the queue says so. If the human is late, the system says so again, upward. If the action is inherently unsafe as proposed, the request carries that fact forward instead of hiding it.',
    },
    { kind: 'h', text: 'Proof before promise' },
    {
      kind: 'p',
      text: 'Two proofs sit under this architecture. The first is the company itself: a running registry, a locked message bus, a five-tier gate, and append-only SHA-256 sealed audit trails exercised daily, not a lab toy and not a client deployment claimed where none exists. The second is deliberately small. J&S StopOver Bar is a real, non-tech SME in Malawi already using agentic decision support for pricing through an LLM-council methodology, with a documented arc from finance and inventory agents through procurement and operations to a human owner\'s dashboard. If the stack only works inside an engineering department, it is not a company model; it is a specialist tool. The SME is the test that it is neither.',
    },
    { kind: 'h', text: 'Starting from the registry' },
    {
      kind: 'p',
      text: 'For a bank, a ministry, or a cooperative asking how to begin: start with the registry, not the model. Define what work agents will own, which tools they may touch, who approves what, and where escalation lands, before wiring a single LLM call. Pick one workflow, put it behind a real gate, measure it against the old way, then widen. Retrofitting governance onto an ungoverned fleet is an order of magnitude harder than designing the tiers in from day one. That is the whole lesson of ninety agents in one sentence.',
    },
    { kind: 'h', text: 'Honest status' },
    {
      kind: 'p',
      text: 'LightSpeed runs this model in-house. The agent count is 90 (89 AI plus one human CEO) across 20 departments per company-registry.yaml, verified by direct count. The five-tier matrix, message-bus queue, and audit-ledger patterns ship in our own platform code: Tier 0 through Tier 4 classification, approval-gate persistence, and expiry sweeps are implemented, not proposed. J&S StopOver Bar is a real SME running agentic decision support; it is not a LightSpeed client engagement. No paid enterprise client has been delivered this stack yet. Client-facing badges on the site say the same thing: proven in-house first, fieldable and piloted where true, never claimed delivered when it is not.',
    },
  ],
  relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'boardroom-briefing'],
  relatedSectors: ['financial-services', 'government', 'education'],
};
