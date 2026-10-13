import type { InsightArticle } from '../../src/data/insights';

export const article: InsightArticle = {
  slug: 'five-tier-approval-matrix',
  title: 'The Five-Tier Approval Matrix: How Friction Scales With Risk in a 90-Agent Company',
  topic: 'AI GOVERNANCE',
  dek: 'A permission system that gates every action drowns its humans. One that gates nothing is not a company. The middle is a tier table in code and a timeout that never means yes.',
  category: 'AI governance',
  readMins: 7,
  publishedAt: '2026-10-12',
  source:
    'src/ai_company/orchestrator/tier_rules.py · src/ai_company/executor/hitl_gate.py · src/ai_company/orchestrator/approval.py · docs/Pharos/pillars/02-5-tier-human-in-the-loop.md · docs/APPROVAL-UX-SPEC.md',
  blocks: [
    {
      kind: 'p',
      text: 'Ask a team how they govern their AI agents and you will hear a policy. Ask them what happens when nobody answers an approval request and you will learn whether the policy is real. That second question is the one this article is about, because LightSpeed Holdings runs 90 agents (89 AI personas plus one human CEO) across 20 departments, and the only thing standing between that fleet and ungoverned action is a five-tier approval matrix enforced in code, not prose.',
    },
    { kind: 'h', text: 'The failure mode nobody designs for' },
    {
      kind: 'p',
      text: 'There are two ways to get permission wrong. Gate nothing, and an agent with shell access is an incident report waiting for a timestamp. Gate everything, and the humans drown: every read, every search, every status update lands in an approval queue until the queue is ignored, and an ignored queue is governance theater. The design principle that resolves this is short enough to remember under pressure: friction scales with risk. Low-risk work moves without asking. High-risk work cannot move without deliberate human action. The tier table is where that principle stops being a slogan.',
    },
    { kind: 'h', text: 'The five tiers, as the code defines them' },
    {
      kind: 'p',
      text: 'The implementation lives in tier_rules.py: an ApprovalTier enum with five values, each with a label, a default timeout, and a class of work it is responsible for. This is the table risk officers should ask to see from any vendor claiming governed agents. It is also the table we can produce, because it is ours:',
    },
    {
      kind: 'ul',
      items: [
        'Tier 0: Auto-Approve. Read-only work: listing, searching, recalling. No gate; the action executes and lands in the execution log. Most agent work lives here, which is correct.',
        'Tier 1: Notify. Low-risk writes humans should see in history but never in a queue: memory storage, routine status updates. Logged for audit, never blocking.',
        'Tier 2: Single Approver. Code edits, test execution, sub-threshold changes. One human must approve before the action proceeds.',
        'Tier 3: Two-Person Rule. Production paths, shell execution that reaches production, destructive or high-spend actions. Two distinct humans; the gate rejects a second signature from the first approver.',
        'Tier 4: CEO Only. Secrets, legal and compliance paths, financial and security exposure, constitutional moves like deploying a new agent. No substitute approver exists.',
      ],
    },
    {
      kind: 'p',
      text: 'Classification is not vibes. tier_rules.py maps tool defaults to tiers (read-only tools at Tier 0, edits at Tier 2) and then applies path and command rules on top. A fragment list for sensitive paths (secrets, .env files, audit directories, legal and compliance trees) escalates the action to CEO-only unconditionally. Production and deploy fragments escalate to the two-person rule. Dangerous commands, the ones that delete broadly or reach production systems, escalate the same way. The default tier is a floor; overrides only ever raise risk, never lower it.',
    },
    {
      kind: 'quote',
      text: 'Friction scales with risk. No silent failures. Auditability by default. Timeout is never final.',
      cite: 'LightSpeed approval doctrine · docs/APPROVAL-UX-SPEC.md',
    },
    { kind: 'h', text: 'What the gate does while a human is deciding' },
    {
      kind: 'p',
      text: 'A tier table is only half of governance. The other half is behavior at the boundary: what the system does while an approval is pending, and what it does when nobody answers. Three mechanics matter, and all three are implemented rather than proposed.',
    },
    {
      kind: 'p',
      text: 'First, requests persist. The executor-side HITL gate writes pending requests to disk, so a restart does not lose the ask and does not reset the clock into silence. An agent blocks on the gate; it does not route around it.',
    },
    {
      kind: 'p',
      text: 'Second, timeouts never approve. Per-tier deadlines sit in configuration (four hours at Tier 2, two at Tier 3, one at Tier 4) with a shorter default on the executor-side wait. When a deadline passes, the governance sweep moves the request from pending to expired: a visible, terminal state that must be re-submitted, written to the audit ledger on the way. No path in the system converts an unanswered request into a yes. That is the whole ballgame. A fallback deadline under agent pressure becomes default permission; ours becomes a louder ask.',
    },
    {
      kind: 'p',
      text: 'Third, unsafe requests are flagged at creation, not discovered at review. A tool call carrying shell metacharacters or a blocked pattern is marked at request time, so a pending item that will always be rejected is not silently retried into a loop. The audit trail records why it was flagged, not merely that it died.',
    },
    { kind: 'h', text: 'What a risk officer should demand from any agent deployment' },
    {
      kind: 'p',
      text: 'None of this is exotic. It is the same discipline banks and hospitals learned decades ago, translated to a world where the actor is software. If you are evaluating agent governance (as a CRO, a regulator, a procurement lead), the transferable test is four questions:',
    },
    {
      kind: 'ul',
      items: [
        'Ask for the tier table. What classifies to which tier, and who approves what? If the answer is a policy slide rather than a mapping in code, keep asking.',
        'Test the timeout rule. Ask what happens at one minute past the deadline. If the answer is "it dropped" or "it approved," that is governance-shaped risk.',
        'Audit the audit trail. Who, when, why, in what order, and can the agent under review modify the evidence? If yes, the governance fails exactly where it must hold.',
        'Require two distinct approvers for irreversible actions. One signature on deletion, spend, or production deployment is one person away from an incident.',
      ],
    },
    { kind: 'h', text: 'The honest trade-off' },
    {
      kind: 'p',
      text: 'The tiers are not free. Tier 2 and Tier 3 requests block agents until humans respond, and human attention is the scarcest resource in the company. There are days when the queue is the controller of the workflow. The alternative is worse, and we have lived it: post-hoc review, where the governance layer arrives after the incident, playing catch-up while the agent that caused the problem is still running. The cost of the queue is the price of the permission. It is the discipline that makes a 90-agent company deployable outside a laboratory.',
    },
    { kind: 'h', text: 'Honest status' },
    {
      kind: 'p',
      text: 'LightSpeed runs this model in-house. The five-tier matrix is implemented in our platform code: the ApprovalTier enum, path and command escalation, per-tier timeouts, request persistence, the expired-state sweep, and metacharacter flagging are all in the repository, exercised by our own regression suite, not drafted for a deck. The pillar essay that narrates this system is a draft awaiting CEO review; the code it describes is not. What this governance has not yet earned is a client claim: no paid enterprise deployment has been delivered this stack. The operating evidence is our own company (90 agents, one human CEO, every gated action attributable), and the tier table above is what we would show a regulator today.',
    },
  ],
  relatedSolutions: ['ai-company-builder', 'enterprise-deployment', 'boardroom-briefing'],
  relatedSectors: ['financial-services', 'government'],
};
