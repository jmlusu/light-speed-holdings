import type { InsightArticle } from '../../src/data/insights';

export const article: InsightArticle = {
  slug: 'dual-economy-ai-pricing',
  title: 'Pricing Agentic AI in a Dual Economy: Kwacha Ladders, Dollar Retainers, and Paying for What You Run',
  topic: 'AI PRICING',
  dek: 'Take a US list price, divide by the exchange rate, hope. That method died on the night the kwacha devalued 44%. Malawi\'s market pays in kwacha; its NGO and regional work is quoted in dollars. So we run two rails: a published MWK ladder, USD-denominated retainers, and mobile-money collection built in from day one. Here is the ladder, the reasoning, and an honest account of what has actually been sold.',
  category: 'Market intelligence',
  readMins: 7,
  publishedAt: '2026-10-12',
  source:
    'docs/Pharos/research-briefs/2026-10-12-ai-economics-sadc.md · docs/client-facing/USE-CASE-CATALOG.md · docs/marketing/competitive-landscape.md · content/drafts/faq.md · results/pestel-lightspeed-2026.md · src/data/insights.ts · docs/venture-studio/12-T3-call-scripts.md · docs/Pharos/articles/h-a-o-m-t-g-v-seven-layers.md · docs/Pharos/roadmap.md · docs/Pharos/case-study-pipeline.md',
  blocks: [
    {
      kind: 'p',
      text: 'The standard way to price software in an emerging market is arithmetic: take the vendor\'s dollar list price, divide by the exchange rate, and hope the rate holds until the invoice clears. In Malawi that hope has already failed once. The kwacha devalued 44% in a single night in November 2023 and has been managed at roughly 1,716 to 1,751 per US dollar since (our PESTEL 2026 baseline, an internal scan, labelled as such). A dollar price that looked competitive in 2023 can now be wrong for a Blantyre SME by more than a month\'s margin. So we do not price on one rail. Our catalog states it directly: pricing is "anchored in dual currency (MWK for local clients, ~USD for international)", kwacha for Malawian institutions and dollars for the international organisations that budget in them. This article lays out the ladder, the reasoning under it, and what has actually been sold so far.',
    },
    { kind: 'h', text: 'Two rails, one catalog' },
    {
      kind: 'p',
      text: 'One clarification before the numbers: this is offer language, not transacted revenue. The MWK figures are stated in kwacha with ~USD estimates that are explicitly labelled estimates in the source and pending prospect validation before public reliance. The USD-quoted side (international NGO and regional work) is documented in our FAQ and catalog, but no public rate card exists, and none will be invented here. With that boundary set, the published ladder:',
    },
    {
      kind: 'ul',
      items: [
        'Licensing: MWK 3,500,000 (~$2,000 estimate), paired with a USD-denominated support retainer at $200/month.',
        'Minimum viable deployment: MWK 150,000 (~$85), the entry rung for a first automation.',
        'Business website (A1): MWK 800,000 (~$450).',
        'E-commerce store (A2): MWK 1,800,000 (~$1,000).',
        'WhatsApp chatbot (B1): MWK 1,500,000 (~$850) plus MWK 100,000/month hosting.',
        'One-off payment terms: 50% upfront, 50% on delivery.',
      ],
    },
    { kind: 'h', text: 'Why two currencies, not one' },
    {
      kind: 'p',
      text: 'The two rails exist because the two buyers carry different risks. A Malawian institution earns kwacha, borrows in kwacha, and was taught by the 2023 devaluation that a dollar-denominated invoice is a currency bet it did not ask to make. An international NGO or regional programme budgets in dollars twelve months ahead and cannot plan against a kwacha figure that moves. Quoting each in the currency it carries is not a discount tactic. It is risk sitting with the party that can actually hold it. Every ~USD figure above stays the catalog\'s own estimate; we do not convert kwacha prices at rates of our own invention.',
    },
    {
      kind: 'p',
      text: 'The collection side matters as much as the quote. Seventy-five percent of Malawian adults already transact on mobile money (MWK 8.6 trillion in volume in 2025) on Airtel Money and TNM Mpamba, rails our catalog says are "built in from day one, not bolted on". A price in kwacha is only as real as the phone it can be paid from, and in this market the phone already is the bank.',
    },
    {
      kind: 'quote',
      text: 'Dual-economy pricing so institutions pay for what they run, not for idle hyperscaler capacity.',
      cite: 'src/data/insights.ts:69 · docs/client-facing/USE-CASE-CATALOG.md:76',
    },
    { kind: 'h', text: 'The market underneath the price' },
    {
      kind: 'p',
      text: 'A ladder is only defensible against the market it climbs. Our PESTEL 2026 baseline (an internal scan, cited as such) describes it plainly:',
    },
    {
      kind: 'ul',
      items: [
        'Demographics: ~22.2m people, ~62% under 25, median age 19.2, ~18 to 20% urban.',
        'Informal-first demand: ~1.6m MSMEs, 90%+ informal, the addressable market is informal-first.',
        'Slow growth, projected: GDP 1.9% (2025) rising to 2.3% (2026 projected).',
        'Easing but high inflation: 28.4% average in 2025, ~22% average projected for 2026.',
        'Connectivity is the constraint, not demand: 27.7% internet penetration against a SADC average of 59.8%.',
      ],
    },
    {
      kind: 'p',
      text: 'Every figure in that list carries the same caveat: it is our own scan, not an official statistic we commissioned. What it explains is the shape of the ladder. An economy that is young, overwhelmingly informal and phone-first cannot start at seat licences and annual commits. It starts at MWK 150,000 for a first deployment and MWK 800,000 for a website, with the dollar retainer reserved for the buyers who already budget in dollars.',
    },
    { kind: 'h', text: 'The competitor is the spreadsheet' },
    {
      kind: 'p',
      text: 'The buyer\'s real alternative is not another AI vendor. It is the stack they already have: Kobo and Google Forms feeding spreadsheets, plus global consultancies priced out of reach for most of the market. Our sales doctrine meets that directly: no rip-and-replace; we sit beside the current M&E sheets for one cycle, and the 90-day pilot is a documented offer, classified internally as an offer rather than a result. When a risk officer says no, they are usually raising one of four legitimate objections (bandwidth and devices, data location, forever-maintenance, prior AI failures). The honest answer to all four is a bounded pilot, not a bigger claim.',
    },
    {
      kind: 'p',
      text: 'On the local competitive set, an internal read (labelled as such): nearly every Malawi player above sells custom software, and none sells a governed agentic organisation. The category is empty locally. Those named players do not disclose pricing, and the global consultancies sell governance-shaped messaging at enterprise rates with no SADC-specific price points we can cite. So we cite none. The competitor that matters is the spreadsheet, and the price has to beat the cost of staying where they are.',
    },
    { kind: 'h', text: 'What has actually been sold' },
    {
      kind: 'p',
      text: 'Here is the constraint that governs everything above: nothing has been delivered to paying clients yet. What exists is operating evidence. J&S StopOver Bar, a real non-tech SME, is the single LIVE commercial proof point: inventory, procurement and pricing agents running on a small business\'s actual numbers. The 90-agent company itself (89 AI agents and one human CEO) is proven in-house, verified by a direct count of the company registry on 23 September 2026. The agricultural coop, health monitoring and VSLA/SACCO work are pilots, honest about being pilots, with no signed partnership or engagement to name. The WhatsApp automation offer is blocked pending security review. No revenue figures, win rates or pipeline values appear here because none exist to appear.',
    },
    { kind: 'h', text: 'A category being defined, not settled' },
    {
      kind: 'p',
      text: 'Pricing lands in a policy environment that is still moving. Malawi validated its UNESCO AI Readiness Assessment in July 2026 and is drafting its first National AI Strategy; the Data Protection Act (2024) is in force but is not AI-specific; an AI Bill was announced in August 2026 with its status moving; the AU\'s Continental AI Strategy (2024) is a non-binding reference. One naming point of honesty: the SADC "Agentic AI Governance Framework" is our own policy proposal, not an adopted standard, and our engagement on it is advisory and pilot work, not deployed client systems. A category being defined is precisely why governance architecture has to ship before throughput. It is also why a published price, stated plainly in the currencies the market actually uses, is worth more than a discount introduced at signature.',
    },
    { kind: 'h', text: 'Honest status' },
    {
      kind: 'p',
      text: 'What this article does not contain is as deliberate as what it does: no TAM, SAM or SOM figure for Malawi or SADC agentic AI; no adoption percentage for African enterprises; no competitor prices, because they are undisclosed; no FX conversions beyond the catalog\'s own ~USD estimates; no signed-revenue, win-rate or pipeline numbers, because no paying client delivery exists yet. The ladder is offer language pending prospect validation, not a revenue record. The policy citations are current as of October 2026 and should be re-verified if this is read more than 30 days out. The pricing is defensible because it is published, collectable on rails that already exist, and denominated in the currency the buyer carries. That is the whole claim, and it is enough to start a conversation on.',
    },
  ],
  relatedSolutions: ['business-automation', 'digital-presence', 'boardroom-briefing'],
  relatedSectors: ['financial-services', 'agriculture', 'government'],
};
