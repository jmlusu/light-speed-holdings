import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Cpu, ArrowRight, CheckCircle2, ShieldCheck } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { OFFER_FAMILIES } from '../data/useCaseCatalogData';
import { solutions, industries, GOVERNANCE_SOLUTION } from '../data/siteContent';

interface WhatWeDoPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

type CatalogTab = 'packages' | 'solutions' | 'industries';

export const WhatWeDoPage: React.FC<WhatWeDoPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const [activeTab, setActiveTab] = useState<CatalogTab>('packages');

  return (
    <>
      {/* 1. EXECUTIVE OUTCOME (Above the fold: what/who/why/next in 5s) */}
      <PageIntro
        theme={theme}
        eyebrow="WHAT WE DO"
        title="Enterprise AI Systems Built for Real Constraints"
        lead="LightSpeed Holdings delivers modular AI services and custom agent architectures for organizations in Malawi, across SADC, and beyond. One human CEO directs 151 specialized AI agents to deliver world-class software, automation, and reporting at accessible regional pricing."
      >
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={() => onRequestBriefing?.('Request an AI Readiness Assessment')}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90"
          >
            Request an AI Readiness Assessment
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </button>
          <a
            href="#catalog"
            className={`inline-flex items-center gap-2 px-5 py-3 rounded-full font-bold text-xs tracking-widest uppercase border transition-all ${
              isLight
                ? 'border-ls-grey-dark/40 text-ls-navy hover:bg-ls-navy/5'
                : 'border-ls-white/20 text-ls-white hover:bg-ls-white/5'
            }`}
          >
            View Service Catalog
          </a>
        </div>
      </PageIntro>

      {/* 2. THE INSTITUTIONAL PROBLEM */}
      <section
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="THE INSTITUTIONAL PROBLEM"
          title="Why Traditional Software & AI Consultancies Fail the Region"
          lead="African enterprises, clinics, NGOs, and public institutions are priced out of high-end software development while being underserved by overseas platforms."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <Reveal delay={0}>
            <div
              className={`rounded-3xl p-6 sm:p-8 border h-full flex flex-col justify-between ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy shadow-md' : 'bg-ls-navy border-ls-white/15 text-ls-white shadow-xl'
              }`}
            >
              <div>
                <span className="font-body text-xs font-black tracking-widest text-ls-red uppercase">01 // COST & CURRENCY</span>
                <h3 className="mt-3 text-lg font-bold font-display tracking-tight">The Offshore Price Barrier</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  International consultancies bill in foreign currency at rates that assume Western enterprise balance sheets, pricing out local SMEs, schools, and health institutions.
                </p>
              </div>
            </div>
          </Reveal>
          <Reveal delay={0.08}>
            <div
              className={`rounded-3xl p-6 sm:p-8 border h-full flex flex-col justify-between ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy shadow-md' : 'bg-ls-navy border-ls-white/15 text-ls-white shadow-xl'
              }`}
            >
              <div>
                <span className="font-body text-xs font-black tracking-widest text-ls-red uppercase">02 // INTEGRATION GAPS</span>
                <h3 className="mt-3 text-lg font-bold font-display tracking-tight">Disconnected from Local Rails</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  Generic software assumes credit cards and gigabit fiber. Regional workflows depend on Airtel Money, TNM Mpamba, PayChangu, and offline-tolerant network resilience.
                </p>
              </div>
            </div>
          </Reveal>
          <Reveal delay={0.16}>
            <div
              className={`rounded-3xl p-6 sm:p-8 border h-full flex flex-col justify-between ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy shadow-md' : 'bg-ls-navy border-ls-white/15 text-ls-white shadow-xl'
              }`}
            >
              <div>
                <span className="font-body text-xs font-black tracking-widest text-ls-red uppercase">03 // THE PILOT TRAP</span>
                <h3 className="mt-3 text-lg font-bold font-display tracking-tight">AI Demos Without Governance</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  Most AI projects stall in slide decks or fragile chatbot prototypes. Without human-in-the-loop oversight and strict data residency, institutions cannot risk production deployment.
                </p>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* 3. LIGHTSPEED'S APPROACH */}
      <section
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="LIGHTSPEED'S APPROACH"
          title="The Governed Agentic Workforce"
          lead="We combine radical unit economics with executive accountability. Work is executed across 20 specialized AI agent departments, governed by strict human approval gates."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div
            className={`p-6 rounded-3xl border ${
              isLight ? 'bg-ls-white border-ls-grey-dark/20 text-ls-navy' : 'bg-ls-navy/60 border-ls-white/10 text-ls-white'
            }`}
          >
            <ShieldCheck className="w-6 h-6 text-ls-red mb-3" />
            <h4 className="font-bold text-base font-display">Human-in-the-Loop Sign-Off</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Agents execute in parallel, but the human CEO signs off on all client-facing deliverables before anything is handed over.
            </p>
          </div>
          <div
            className={`p-6 rounded-3xl border ${
              isLight ? 'bg-ls-white border-ls-grey-dark/20 text-ls-navy' : 'bg-ls-navy/60 border-ls-white/10 text-ls-white'
            }`}
          >
            <Cpu className="w-6 h-6 text-ls-cyan mb-3" />
            <h4 className="font-bold text-base font-display">Local Payment &amp; Data Rails</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Native integrations with Airtel Money, TNM Mpamba, and PayChangu, compliant with the Malawi Data Protection Act and GDPR.
            </p>
          </div>
          <div
            className={`p-6 rounded-3xl border ${
              isLight ? 'bg-ls-white border-ls-grey-dark/20 text-ls-navy' : 'bg-ls-navy/60 border-ls-white/10 text-ls-white'
            }`}
          >
            <CheckCircle2 className="w-6 h-6 text-ls-red mb-3" />
            <h4 className="font-bold text-base font-display">Transparent Fixed Pricing</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Published unit economics in both MWK and USD with clear turnaround SLAs and zero hidden consultancies markups.
            </p>
          </div>
        </div>
      </section>

      {/* 4. PROOF & EVIDENCE: INTERACTIVE CATALOG (PACKAGES / SOLUTIONS / INDUSTRIES) */}
      <section
        id="catalog"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-16 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
          <div>
            <span className="text-xs font-body font-bold tracking-widest text-ls-red uppercase">
              PROOF &amp; EVIDENCE // COMMERCIAL CATALOG
            </span>
            <h2 className="text-2xl sm:text-4xl font-black tracking-tight font-display mt-2">
              Explore Our Capabilities
            </h2>
            <p className={`mt-2 text-sm max-w-xl ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Every service tier carries an explicit honesty status badge. We do not invent capabilities or hide behind vague promises.
            </p>
          </div>

          {/* Interactive Tab Switcher */}
          <div
            className={`inline-flex p-1.5 rounded-full border ${
              isLight ? 'bg-ls-white border-ls-grey-dark/30' : 'bg-ls-navy border-ls-white/15'
            }`}
            role="tablist"
          >
            <button
              type="button"
              role="tab"
              aria-selected={activeTab === 'packages'}
              onClick={() => setActiveTab('packages')}
              className={`px-4 sm:px-5 py-2 rounded-full text-xs font-bold tracking-wider transition-all cursor-pointer ${
                activeTab === 'packages'
                  ? 'bg-ls-red text-ls-white shadow-md'
                  : isLight ? 'text-ls-navy hover:text-ls-red' : 'text-ls-white hover:text-ls-red'
              }`}
            >
              Service Packages (A–E)
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={activeTab === 'solutions'}
              onClick={() => setActiveTab('solutions')}
              className={`px-4 sm:px-5 py-2 rounded-full text-xs font-bold tracking-wider transition-all cursor-pointer ${
                activeTab === 'solutions'
                  ? 'bg-ls-red text-ls-white shadow-md'
                  : isLight ? 'text-ls-navy hover:text-ls-red' : 'text-ls-white hover:text-ls-red'
              }`}
            >
              Solutions (6 Domains)
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={activeTab === 'industries'}
              onClick={() => setActiveTab('industries')}
              className={`px-4 sm:px-5 py-2 rounded-full text-xs font-bold tracking-wider transition-all cursor-pointer ${
                activeTab === 'industries'
                  ? 'bg-ls-red text-ls-white shadow-md'
                  : isLight ? 'text-ls-navy hover:text-ls-red' : 'text-ls-white hover:text-ls-red'
              }`}
            >
              Industry Verticals
            </button>
          </div>
        </div>

        {/* Tab 1: Service Packages A–E */}
        {activeTab === 'packages' && (
          <div className="space-y-8 animate-in fade-in duration-300">
            {OFFER_FAMILIES.map((family) => (
              <div
                key={family.id}
                className={`rounded-3xl p-6 sm:p-8 border ${
                  isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-inherit">
                  <div>
                    <div className="flex items-center gap-3">
                      <span className="px-2.5 py-1 rounded-md bg-ls-red/10 text-ls-red text-xs font-black font-body">
                        OFFER {family.letter}
                      </span>
                      <HonestyBadge label={{ label: family.honestyBadge, tone: 'fieldable' }} />
                    </div>
                    <h3 className="text-xl sm:text-2xl font-bold font-display mt-2">{family.title}</h3>
                    <p className={`text-xs sm:text-sm mt-1 max-w-2xl ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                      {family.description}
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => onRequestBriefing?.(`Enquiry for Offer ${family.letter}: ${family.title}`)}
                    className="self-start sm:self-center px-4 py-2 rounded-full text-xs font-bold tracking-wider uppercase bg-ls-red text-ls-white hover:bg-ls-red/90 transition-colors shadow-sm whitespace-nowrap cursor-pointer"
                  >
                    Select Offer {family.letter}
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
                  {family.deliverables.map((item) => (
                    <div
                      key={item.id}
                      className={`p-4 rounded-2xl border flex flex-col justify-between ${
                        isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy/70 border-ls-white/10'
                      }`}
                    >
                      <div>
                        <div className="flex items-baseline justify-between gap-2">
                          <h4 className="font-bold text-sm font-display">{item.name}</h4>
                          <span className="text-[11px] font-black text-ls-red whitespace-nowrap">{item.priceMwk}</span>
                        </div>
                        <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                          {item.description}
                        </p>
                      </div>
                      <div className="mt-4 pt-3 border-t border-inherit flex items-center justify-between text-[11px]">
                        <span className="font-medium opacity-80">{item.priceUsd}</span>
                        <span className="font-bold text-ls-cyan">{item.turnaround}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tab 2: Solution Domains */}
        {activeTab === 'solutions' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-in fade-in duration-300">
            {solutions.map((sol) => (
              <div
                key={sol.slug}
                className={`rounded-3xl p-6 sm:p-7 border flex flex-col justify-between ${
                  isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
                }`}
              >
                <div>
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-body text-[10px] font-bold tracking-widest text-ls-red uppercase">
                      {sol.eyebrow}
                    </span>
                    <HonestyBadge label={sol.proof} />
                  </div>
                  <h3 className="mt-3 text-xl font-bold font-display">{sol.title}</h3>
                  <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                    {sol.oneLiner}
                  </p>
                </div>
                <div className="pt-5 mt-5 border-t border-inherit flex items-center justify-between">
                  <Link
                    to={`/solutions/${sol.slug}`}
                    className="text-xs font-bold tracking-wider text-ls-red flex items-center gap-1 hover:underline"
                  >
                    View Domain Details <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}

            {/* Governance Domain */}
            <div
              className={`rounded-3xl p-6 sm:p-7 border flex flex-col justify-between ${
                isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
              }`}
            >
              <div>
                <div className="flex items-start justify-between gap-3">
                  <span className="font-body text-[10px] font-bold tracking-widest text-ls-red uppercase">
                    {GOVERNANCE_SOLUTION.eyebrow}
                  </span>
                  <HonestyBadge label={GOVERNANCE_SOLUTION.proof} />
                </div>
                <h3 className="mt-3 text-xl font-bold font-display">{GOVERNANCE_SOLUTION.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {GOVERNANCE_SOLUTION.oneLiner}
                </p>
              </div>
              <div className="pt-5 mt-5 border-t border-inherit flex items-center justify-between">
                <Link
                  to={GOVERNANCE_SOLUTION.to}
                  className="text-xs font-bold tracking-wider text-ls-red flex items-center gap-1 hover:underline"
                >
                  View Policy Specs <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Industry Verticals */}
        {activeTab === 'industries' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-in fade-in duration-300">
            {industries.map((ind) => (
              <div
                key={ind.slug}
                className={`rounded-3xl p-6 sm:p-7 border flex flex-col justify-between ${
                  isLight ? 'bg-ls-white border-ls-grey-dark/30 shadow-md' : 'bg-ls-navy border-ls-white/15 shadow-xl'
                }`}
              >
                <div>
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-body text-[10px] font-bold tracking-widest text-ls-red uppercase">
                      VERTICAL
                    </span>
                    <HonestyBadge label={ind.proof} />
                  </div>
                  <h3 className="mt-3 text-xl font-bold font-display">{ind.title}</h3>
                  <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                    {ind.problem}
                  </p>
                </div>
                <div className="pt-5 mt-5 border-t border-inherit flex items-center justify-between">
                  <Link
                    to={`/industries/${ind.slug}`}
                    className="text-xs font-bold tracking-wider text-ls-red flex items-center gap-1 hover:underline"
                  >
                    Explore Vertical <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* 5. ENGAGEMENT PATH: G1–G4 GATES */}
      <section
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-16 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="ENGAGEMENT PATH"
          title="Four Governance Gates Before Any Work Ships"
          lead="Every client relationship moves through an orderly four-gate lifecycle. No unexpected charges, no runaway scopes, and full intellectual property transfer upon delivery."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
          <div
            className={`p-6 rounded-3xl border ${
              isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'
            }`}
          >
            <span className="text-2xl font-black font-body text-ls-red">G1</span>
            <h4 className="mt-2 text-base font-bold font-display">Discovery &amp; Contract</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Governed executive alignment on goals, deliverables, and unit pricing. Zero ambiguity before signing.
            </p>
          </div>
          <div
            className={`p-6 rounded-3xl border ${
              isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'
            }`}
          >
            <span className="text-2xl font-black font-body text-ls-red">G2</span>
            <h4 className="mt-2 text-base font-bold font-display">Architecture &amp; DPA</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Data processing agreement, system security classification, and local compliance sign-off.
            </p>
          </div>
          <div
            className={`p-6 rounded-3xl border ${
              isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'
            }`}
          >
            <span className="text-2xl font-black font-body text-ls-red">G3</span>
            <h4 className="mt-2 text-base font-bold font-display">Build &amp; Pilot Sprint</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Rapid execution through agentic workforce, gated by regression tests and human approval checkpoints.
            </p>
          </div>
          <div
            className={`p-6 rounded-3xl border ${
              isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy border-ls-white/15'
            }`}
          >
            <span className="text-2xl font-black font-body text-ls-red">G4</span>
            <h4 className="mt-2 text-base font-bold font-display">Handover &amp; Support</h4>
            <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Complete code and asset transfer, deployment verification, and 30 days of included executive support.
            </p>
          </div>
        </div>
      </section>

      {/* 6. CLEAR CTA */}
      <CtaBand
        theme={theme}
        title="Request an AI Readiness Assessment"
        text="Speak with our executive team. We will evaluate your data and workflow readiness honestly — and determine exactly which service tier fits your goals."
        ctaLabel="Request an AI Readiness Assessment"
        ctaTo="/contact"
      />
    </>
  );
};

export default WhatWeDoPage;
