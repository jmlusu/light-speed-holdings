import type { InsightArticle } from '../../src/data/insights';

export const article: InsightArticle = {
  slug: 'offline-first-ai-for-africa',
  title: 'Offline-First AI for Africa: Designing for Bandwidth, Sovereignty, and Mobile-Money Reality',
  topic: 'AI IN AFRICA',
  dek: 'Low-bandwidth is not a deployment footnote — it is the design brief. Here is how offline-first routing, a zero-cloud boundary, and local models answer the four reservations risk officers actually raise.',
  category: 'African AI',
  readMins: 8,
  publishedAt: '2026-10-12',
  source:
    'docs/RESERVATIONS-STRATEGY.md · docs/Pharos/pillars/03-agentic-ai-resource-constrained-africa.md · docs/Pharos/case-study-pipeline.md · src/ai_company/llm/providers/ · src/ai_company/model_router.py · research/site-claims-ledger.md',
  blocks: [
    {
      kind: 'p',
      text: 'The default deployment story for agentic AI assumes fibre, idle GPUs, and a data centre in another hemisphere. That story does not survive contact with a district clinic, a Lilongwe SME counter, or a ministry network that still runs legacy cores. In Malawi and across SADC, the binding constraints are bandwidth, power, device class, data-sovereignty law, and a legitimate fatigue with vendor hype. Offline-first is not a nice-to-have mode we bolt on for rural demos. It is the design principle: core functions run against local state and local models where the constraint demands it, and the system reconciles when the network returns. The workflow — not the cloud — is the unit of operation.',
    },
    { kind: 'h', text: 'The four reservations, named' },
    {
      kind: 'p',
      text: 'Decision-makers in the region do not object to AI out of technophobia. They raise four reservations, and they are right to. Our answer doctrine — honesty-badged, never claimed as delivered unless it was — starts by naming them without softening:',
    },
    {
      kind: 'ul',
      items: [
        'Bandwidth and resource constraints — inference and orchestration cannot assume always-on connectivity or new devices.',
        'Data protection — citizen and financial data cannot casually leave the jurisdiction; Malawi’s Data Protection Act (2024) already binds it, with no published interpretation yet for autonomous systems.',
        'Technology debt — institutions run systems that already cost years of budget; nothing may require a rip-and-replace programme.',
        'AI skepticism — earned by demos that never changed an operating metric, and answered only by evidence.',
      ],
    },
    {
      kind: 'p',
      text: 'Each reservation maps to architecture, not a disclaimer. The sections below are how we engineer the answers in our own stack — with badges that say what is proven in-house, what is fieldable, and what is still in development.',
    },
    { kind: 'h', text: 'Offline-first routing, not offline brochureware' },
    {
      kind: 'p',
      text: 'Offline-first means the system is allowed to work when the network is bad or absent. In practice that shows up in three places we can point at in code and architecture docs. First, model routing with quota-first and offline-aware behaviour: when connectivity or budget is the constraint, traffic prefers free or local paths rather than failing into a spinner. The router’s tier order — fast, standard, premium, with special free and override lanes — exists so cost and connectivity are routing inputs, not afterthoughts. Second, provider-agnostic execution: the LLM client is not welded to one cloud vendor. It resolves providers through the model router and can call OpenAI-compatible endpoints, Ollama, or llama.cpp — local inference is a first-class provider class, not an undocumented fallback. Third, client surfaces that queue work and sync on reconnect: PWA offline action queues and WhatsApp-native flows so the interface meets users where they already are, without forcing an app download as a prerequisite for participation.',
    },
    {
      kind: 'quote',
      text: 'Low-bandwidth does not mean no-AI. It means AI designed for the constraint — which is usually the better engineering problem.',
      cite: 'Pharos pillar 03 — resource-constrained Africa',
    },
    { kind: 'h', text: 'Zero-cloud boundary and sovereign-by-default' },
    {
      kind: 'p',
      text: 'The second reservation — where does our data go? — cannot be answered with a privacy policy alone. It is answered with a deployment boundary. Sovereign in-country processing is the default posture: processing happens where the data lives, audit trails stay local, and any cross-border flow to an external LLM is an explicit, documented governance decision rather than a silent side effect. For institutions that cannot risk external inference at all, a zero-cloud option exists in the architecture — orchestration and state on infrastructure they control. When a regulator asks who processed what, under what authority, and where it still resides, the answer should be a map and an audit log, not a promise slide. Malawi’s DPA 2024 and GDPR-shaped expectations are treated as engineering constraints from day one; we never use client data to train models. Honesty badge: proven in-house for architecture and governance posture; specific consent-workflow productisation is still in active development where noted in our catalog.',
    },
    { kind: 'h', text: 'Local models and provider-agnostic routing' },
    {
      kind: 'p',
      text: '“Local model” is not one capability. It is a routing choice. Our providers module ships OpenAI-compatible, Ollama, and llama.cpp implementations behind a common provider interface, with circuit breakers, token accounting, response caching, and prompt compression as cross-cutting concerns. The model router escalates across fast → standard → premium tiers on failure and supports free and override lanes for budget-constrained or human-directed runs. That structure is what makes “run free models when connectivity or budget demands it” an operable policy rather than a whiteboard intention: the same client code path can target a cloud endpoint when the link is healthy and a local server when it is not, without rewriting the agents. Specific model weights and sizes vary by deployment hardware; we do not claim a single universal offline stack for every device class in the region.',
    },
    { kind: 'h', text: 'Mobile-money rails from day one' },
    {
      kind: 'p',
      text: 'Agentic AI that cannot touch how value actually moves in Malawi is a science project. Airtel Money and TNM Mpamba are not exotic edge cases in our market — they are default rails for SMEs and households, with PayChangu in the checkout mix where e-commerce is in scope. Our digital-presence and automation surfaces treat local mobile-money checkout as day-one integration, not a phase-two roadmap item, because the customer’s money already moves that way. On the deeper financial-inclusion side, the case pipeline sketches agentic workflows over mobile-money rails and informal savings groups for VSLA/SACCO risk assessment — use cases regional bodies have asked for. Badge discipline still applies: mobile-money checkout for our digital products is fieldable; broader agentic finance workflows over those rails remain piloted or conceptual until a documented deployment exists.',
    },
    { kind: 'h', text: 'No rip-and-replace: seams, pilots, and debt honesty' },
    {
      kind: 'p',
      text: 'Technology debt is the reservation that kills good AI programmes in institutions that cannot afford a greenfield. The engineering answer is integration seams and a 90-day pilot pattern: thin, reversible connectors to existing systems, one workflow in scope, measured cost and benefit, and a decision gate to continue, adjust, or stop. We hold ourselves to the same rule — our own engineering debt is tracked in a ledger and reviewed, because transparency about what you are choosing not to fix is part of trust. The point is not to sell a forever platform. The point is to let an institution learn on a boundary it can defend to a board.',
    },
    { kind: 'h', text: 'The SME anchor: J&S StopOver Bar' },
    {
      kind: 'p',
      text: 'Architecture arguments are cheap until they touch a counter. J&S StopOver Bar — a real, non-tech SME already running agentic decision support for pricing through an LLM-council methodology, with a documented story arc from human business through finance, inventory, procurement, and operations agents to a CEO dashboard. It matters to the offline-first thesis for a blunt reason: if the only proof lives inside a company with an engineering department, the region’s risk officers are right to be skeptical. A small business in Lilongwe is the proof that the stack is not reserved for hyperscaler customers.',
    },
    { kind: 'h', text: 'A 90-day pilot, in one page' },
    {
      kind: 'ul',
      items: [
        'Scope one workflow that already hurts — inventory, reconciliation, citizen query, or field reporting.',
        'Deploy with sovereignty constraints explicit: where models run, where data rests, what may cross a border.',
        'Route for the real link: local or free models when bandwidth is thin; cloud tiers when it is not.',
        'Gate every consequential action; measure approvals, timeouts, and escalations as first-class metrics.',
        'At day 90: continue, adjust, or stop — with the audit trail as the board pack, not a marketing appendix.',
      ],
    },
    { kind: 'h', text: 'Honest status' },
    {
      kind: 'p',
      text: 'Offline-first routing, provider-agnostic LLM clients (including Ollama and llama.cpp), and sovereign deployment patterns are proven in-house on LightSpeed’s own platform. WhatsApp-native and mobile-money-aware product surfaces are fieldable or in pilot as tagged on the site. J&S StopOver Bar is a real SME running agentic pricing support; it is not a paid LightSpeed client delivery. No ministerial or bank production deployment of this full stack is claimed. Class-level architecture claims above describe capabilities and design decisions we run and publish; they do not assert a finished client product where none has been delivered. Nothing in this article should be read as a paid engagement reference.',
    },
  ],
  relatedSolutions: ['enterprise-deployment', 'business-automation', 'digital-presence'],
  relatedSectors: ['agriculture', 'financial-services', 'healthcare', 'government'],
};
