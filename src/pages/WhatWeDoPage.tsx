import React from 'react';
import {
  AfricaStatBand,
  ArrowLink,
  ArrowRightIcon,
  AutomationIcon,
  BuilderIcon,
  DataIcon,
  GovernanceIcon,
  HeroPhoto,
  IntegrationIcon,
  LightServiceCard,
} from '../components/ui';
import { Reveal } from '../components/Reveal';
import { CtaBand } from '../components/site/CtaBand';
import { metrics } from '../data/metrics';
import { CTAS } from '../data/ctas';

interface WhatWeDoPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * Service pillars. Titles follow the page design; body copy is condensed from
 * the canonical solution registry (src/data/registries/solution-registry.json)
 * and the service descriptions already published on /what-we-do.
 */
const SERVICES = [
  {
    id: 'agentic-automation',
    title: 'Agentic Automation',
    body: 'Turn complex processes into governed agent workflows that execute in parallel across departments, with a human approving every gate before work ships.',
    to: '/solutions#ai-agentic-systems',
    icon: <AutomationIcon className="h-7 w-7" />,
  },
  {
    id: 'ai-integrations',
    title: 'AI Integrations',
    body: 'Connect AI to the tools you already run on: WhatsApp, Airtel Money, TNM Mpamba, PayChangu, Kobo and DHIS2 — and keep working when the network drops.',
    to: '/solutions#intelligent-automation',
    icon: <IntegrationIcon className="h-7 w-7" />,
  },
  {
    id: 'governance-compliance',
    title: 'Governance & Compliance',
    body: 'Human-in-the-loop sign-off, append-only audit trails and Malawi DPA / GDPR-aligned data handling, mapped to a five-tier approval matrix.',
    to: '/solutions#ai-governance-policy',
    icon: <GovernanceIcon className="h-7 w-7" />,
  },
  {
    id: 'data-analytics',
    title: 'Data & Analytics',
    body: 'Turn programme data into donor-ready reports and KPI dashboards in hours, built to be read on a phone and defendable in an audit.',
    to: '/solutions#data-decision-intelligence',
    icon: <DataIcon className="h-7 w-7" />,
  },
  {
    id: 'ai-company-builder',
    title: 'AI Company Builder',
    body: 'Licence and run the same governed agent platform that operates LightSpeed Holdings — self-hosted, provider-agnostic, on your own infrastructure.',
    to: '/ai-company-builder',
    icon: <BuilderIcon className="h-7 w-7" />,
  },
];

const HERO_IMAGE = '/brand/digital/LightSpeed%20brand%20and%20hero%20visual.jpeg';

const STATS = [
  { value: Object.keys(metrics.sectorStats).length, label: 'Sectors' },
  { value: metrics.departments, label: 'Departments' },
  { value: metrics.agentCount, label: 'Operating roles' },
];

export const WhatWeDoPage: React.FC<WhatWeDoPageProps> = ({ theme, onRequestBriefing }) => (
  <div className="bg-ls-white">
    {/*
     * AGENT TEAM NARRATIVE - WhatWeDoPage
     * Content fidelity governed by:
     *   - registry-owner           | sector/solution evidence mapping
     *   - decision-engine-owner    | G1-G4 gate logic, 5-tier approval matrix
     *   - security-compliance-lead | tier_rules.py compliance, risk assessment
     * Last audited: 2026-11-01
     */}

    {/* 1. HERO — photo, navy overlay, service proposition */}
    <HeroPhoto
      imageSrc={HERO_IMAGE}
      imageAlt="Deep blue light planes and data points forming the LightSpeed visual identity"
      eyebrow="WHAT WE DO"
      title={
        <>
          AI Solutions for
          <br />
          <span className="text-ls-cyan">Real-World Impact.</span>
        </>
      }
      body="LightSpeed Holdings delivers modular AI services and custom agent architectures for organizations in Malawi, across Africa and beyond. One Human CEO directs 89 specialized AI agents to deliver software, automation, and reporting at accessible regional pricing."
      annotation={
        <>
          Local problems.
          <br />
          Real solutions.
        </>
      }
    >
      <button
        type="button"
        onClick={() => onRequestBriefing?.(CTAS.assessment.label)}
        className="inline-flex cursor-pointer items-center gap-2 rounded-full bg-ls-cyan px-6 py-3 text-xs font-bold uppercase tracking-widest text-ls-navy transition-colors hover:bg-ls-cyan/85 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ls-cyan focus-visible:ring-offset-2 focus-visible:ring-offset-ls-navy"
      >
        {CTAS.assessment.label}
        <ArrowRightIcon className="h-4 w-4" />
      </button>
      <a
        href="#catalog"
        className="inline-flex items-center gap-2 rounded-full border border-ls-white/35 px-6 py-3 text-xs font-bold uppercase tracking-widest text-ls-white transition-colors hover:border-ls-white/70 hover:bg-ls-white/5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ls-cyan focus-visible:ring-offset-2 focus-visible:ring-offset-ls-navy"
      >
        {CTAS.catalog.label}
      </a>
    </HeroPhoto>

    {/* 2. SERVICE PILLARS — five cards, 5 → 2 → 1 columns */}
    <section
      id="catalog"
      aria-labelledby="service-pillars-heading"
      className="bg-ls-white px-4 py-14 sm:px-8 sm:py-16 lg:px-10"
    >
      <div className="mx-auto w-full max-w-7xl">
        <h2 id="service-pillars-heading" className="sr-only">
          Service pillars
        </h2>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-5 lg:gap-5">
          {SERVICES.map((service, index) => (
            <Reveal key={service.id} delay={index * 0.05} className="h-full">
              <LightServiceCard
                icon={service.icon}
                title={service.title}
                body={service.body}
                to={service.to}
              />
            </Reveal>
          ))}
        </div>

        <div className="mt-10 flex flex-wrap items-center justify-between gap-4">
          <p className="max-w-xl text-[13px] leading-relaxed text-ls-grey-dark">
            Every engagement passes four governance gates before build: discovery, architecture,
            build and handover.
          </p>
          <ArrowLink to="/solutions" tone="navy">
            Explore the solutions index
          </ArrowLink>
        </div>
      </div>
    </section>

    {/* 3. STAT BAND — Africa outline plus operating-model figures */}
    <AfricaStatBand
      heading="Built for Africa. Designed for Scale."
      body="From local SMEs to international donors, we deliver solutions that work in real-world conditions, with local context, local data and local teams."
      stats={STATS}
    />

    <CtaBand
      theme={theme}
      title={CTAS.assessment.label}
      text="Speak with our executive team. We will evaluate your data and workflow readiness honestly, and determine exactly which service tier fits your goals."
      ctaLabel={CTAS.assessment.label}
      ctaTo={CTAS.assessment.to}
    />
  </div>
);

export default WhatWeDoPage;
