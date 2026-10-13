import type { InsightArticle } from '../../src/data/insights';

export const article: InsightArticle = {
  slug: 'evidence-ladder-honest-claims',
  title: 'The Evidence Ladder: How Every Public Claim Gets a Class, and What Buyers Should Demand',
  topic: 'EVIDENCE & PROOF',
  dek: 'Architecture never earns a risk officer\'s "yes" on its own. Claims do the rest of the work, which is why every claim we publish is classified, sourced, and occasionally cut.',
  category: 'Operating models',
  readMins: 7,
  publishedAt: '2026-10-12',
  source:
    'research/site-claims-ledger.md · research/site-claims-audit.md · research/site-claims-index.yaml · src/data/registries/claims-registry.json · src/data/governance.ts · src/data/sectors.ts · src/data/insights.ts · docs/Pharos/pillars/03-agentic-ai-resource-constrained-africa.md · docs/Pharos/manifesto-draft.md',
  blocks: [
    {
      kind: 'p',
      text: 'Every AI vendor deck contains the same slide: a wall of logos, a throughput number with no unit, a customer quote nobody can call. The slide exists because claims are cheap and verification is expensive. In markets where buyers have been burned (and AI skepticism across African enterprises and ministries was, in our own research, earned by years of slide-deck AI that never changed an operating metric), that slide is not persuasion. It is a liability. This article is about the operating model we built to stop ourselves from writing it: an evidence ladder, a claims registry, and a public ledger that classifies every claim on our own website before it ships.',
    },
    { kind: 'h', text: 'The principle, stated once' },
    {
      kind: 'p',
      text: 'The thesis we publish and practice is uncomfortable for a growth-stage company: architecture never earns a Chief Risk Officer\'s or a minister\'s "yes" on its own. The architecture gets you into the room. The claims (what you say the architecture has done, is doing, and will do) decide whether anyone believes you. So the claims get the same engineering discipline as the code. We use an evidence ladder, applied strictly: Proposed, Verified, Established, Market-leading. A claim advances a rung only where evidence exists. Most of what any honest operator has lives in the first two rungs. The top rung is where almost nothing should sit without independent market data. Nothing we publish sits at a rung its evidence does not support.',
    },
    {
      kind: 'quote',
      text: 'An evidence ladder (Proposed, Verified, Established, Market-leading) used strictly: claims advance only where evidence exists, which is the only durable answer to skepticism.',
      cite: 'LightSpeed public doctrine · src/data/insights.ts',
    },
    { kind: 'h', text: 'Three machines under the ladder' },
    {
      kind: 'p',
      text: 'A ladder without machinery is a slogan. Ours runs on three artifacts that exist in the repository, not in a brand guide.',
    },
    {
      kind: 'p',
      text: 'First, a claims registry. Every public claim is classified before it can appear anywhere on the site: Verified, Proven in-house, Pilot, Demonstration, Fieldable, Future, Historical, or Unverified. That last one is labeled "do not publish," and the registry says so in its own description. "Proven in-house" means the claim is verified running inside LightSpeed\'s own operations: our 90-agent company is the reference deployment, and we say that rather than implying a client win we do not have. "Future" means a roadmap target with no evidence yet, stated honestly.',
    },
    {
      kind: 'p',
      text: 'Second, a claims ledger. Before any public surface ships, claims are read against the repository (the actual source files, the actual artifacts) and assigned a class: (a) fully evidenced, (b) qualified (labeled, hedged, or internally consistent), or (c) unqualified (no provenance, or contradicted). Class (c) does not ship. The ledger we last reconciled books 67 classified claims: 18 fully evidenced, 26 qualified, 23 previously flagged and resolved by fixing the copy, and zero remaining contradictions. Every one of the 18 legacy unqualified claims was remediated (hedged, labeled, or deleted) rather than quietly defended.',
    },
    {
      kind: 'p',
      text: 'Third, sector evidence tiers on the public site itself. Every sector we claim experience in carries one of four badges: Proven Experience, Current Capability, Demonstration, or Future Opportunity. The legend for the last one is a sentence we would want every vendor forced to print: roadmap target, no evidence yet, and we say so. A governance rule in code backs this: claims in evidence-sensitive categories cannot reach a published state without an evidence field attached, and the check surfaces violations rather than trusting the author\'s memory.',
    },
    { kind: 'h', text: 'What the ladder actually cut' },
    {
      kind: 'p',
      text: 'The test of an evidence system is not what it lets through. It is what it kills. A sample of our own cuts, all traceable in the public ledger:',
    },
    {
      kind: 'ul',
      items: [
        'An unverifiable superlative: "the world\'s smallest AI-native bar," removed from three surfaces after the audit found zero sizing artifacts behind it. The SME story survived; the boast did not.',
        'Fabricated-looking performance numbers on marketing surfaces deleted rather than defended, because no measured run backed them.',
        'A submission claim that said a governance standard had been "submitted to member-state ministers" downgraded to "authored as a policy proposal" because the repo held the proposal and not the submission.',
        'A "published" badge on a national AI strategy consultation response re-badged to "prepared for drafting for submission" when the artifact on disk still said DRAFT.',
        'An absolute quality claim: "every decision auditable," softened to "decision logs auditable on request," because the audit-trail design exists but the absolute did not.',
        'A throughput claim stated as measured reality rewritten as design intent: "designed for 10x to 100x," and a simulated product console explicitly labeled "SIMULATED OUTPUT: NOT A LIVE RUN" so the demo could not be mistaken for telemetry.',
      ],
    },
    {
      kind: 'p',
      text: 'None of these cuts required a crisis. They required a ledger, a class system, and the standing rule that copy loses arguments with evidence. That is the whole operating model. The alternative (shipping the claim and hoping no one asks) is the slide-deck economy this industry is trying to grow out of.',
    },
    { kind: 'h', text: 'What buyers should demand from any AI vendor' },
    {
      kind: 'p',
      text: 'If you are a bank, a ministry, or a cooperative evaluating AI claims this year, you do not need to adopt our registry to use its logic. Four demands separate evidence-led vendors from story-led ones:',
    },
    {
      kind: 'ul',
      items: [
        'Ask every claim for its class and its source. Verified against what? Proven where? If the answer is a case study you cannot inspect, the claim is unqualified by definition.',
        'Treat superlatives as a red flag, not a highlight. "First," "only," "fastest," "world\'s": each one is a data obligation. Vendors who cannot discharge it will soften when pressed. Vendors who refuse to soften are telling you how they will handle the next unverifiable claim.',
        'Demand rung-discipline on timelines. A pilot is not a deployment. A demonstration is not proven experience. A roadmap item is not a capability. Vendors who blur those boundaries in the pitch will blur them in the delivery report.',
        'Check whether the honesty badge survives contact with sales. The badge that says "no paid clients yet" should still be legible on the website after the first serious conversation. If it disappears under commercial pressure, you have learned something about the vendor that no reference call would have told you.',
      ],
    },
    { kind: 'h', text: 'Why this is the durable answer to skepticism' },
    {
      kind: 'p',
      text: 'The four reservations we hear from African risk officers and ministers (bandwidth, data protection, technology debt, and AI skepticism) are not answered by louder claims. They are answered by inspectable ones. A regulator cannot test a value statement; they can test a tier table, an audit log, and a claims ledger that says, in public, which numbers are measured and which are targets. Running this discipline on ourselves is not modesty. It is the only sales architecture that survives a technical due diligence, and it is why the operating evidence of a 90-agent company, classified rung by rung, is worth more to a CRO than any logo wall we could have built instead.',
    },
    { kind: 'h', text: 'Honest status' },
    {
      kind: 'p',
      text: 'LightSpeed runs this model on ourselves. The claims registry, the ledger, and the sector evidence tiers are in the repository; the last full reconciliation booked 67 claims with zero unqualified rows remaining, and the remediation trail is public in our own research files rather than performed behind a rebrand. What the ladder has not yet earned us is a client claim: no paid enterprise deployment has been delivered this stack, and every public surface says so. What it has earned is the right to be inspected, which for a buyer who has sat through one too many logo walls is the only claim that should matter.',
    },
  ],
  relatedSolutions: ['boardroom-briefing', 'digital-presence', 'ai-company-builder'],
  relatedSectors: ['financial-services', 'government', 'healthcare'],
};
