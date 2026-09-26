import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { SectionHeading } from './site/SectionHeading';
import { HonestyBadge } from './site/HonestyBadge';
import { Reveal } from './Reveal';
import { CtaBand } from './site/CtaBand';
import { company } from '../data/siteContent';

interface AiCompanyBuilderSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

const JOURNEY_STEPS = [
  { num: '01', title: 'Opportunity', desc: 'Identify where AI creates leverage — diagnose the gap between current state and AI-native potential.' },
  { num: '02', title: 'Strategy', desc: 'Define the operating model, governance framework, and measurable outcomes for transformation.' },
  { num: '03', title: 'Architecture', desc: 'Design the modular agent topology, data pipelines, and integration points for your stack.' },
  { num: '04', title: 'Agents', desc: 'Configure role-scoped agents from the 90-agent registry — each with explicit permissions and approval thresholds.' },
  { num: '05', title: 'Workflows', desc: 'Orchestrate agent coordination with human-in-the-loop gates — automated where safe, gated where consequential.' },
  { num: '06', title: 'Deployment', desc: 'Ship working systems with immutable audit trails, circuit breakers, and 30 days of included support.' },
  { num: '07', title: 'Governance', desc: 'Establish the five-tier approval matrix, risk classification, and expiry sweeps that make autonomy safe.' },
  { num: '08', title: 'Measurement', desc: 'Track outcomes, cost, and quality — every metric traces to a canonical source, never invented.' },
  { num: '09', title: 'Continuous Improvement', desc: 'Scale what works, retire what does not — the system learns, adapts, and improves under human oversight.' },
];

const PRINCIPLES = [
  { title: 'Human-led', desc: 'Every decision has a clear owner. AI augments judgment; it does not replace it.' },
  { title: 'AI-native', desc: 'Systems designed as agentic operating layers from day one — not AI bolted onto legacy software.' },
  { title: 'Agentic', desc: '90 specialized agents coordinate across 20 departments, each with explicit role definitions.' },
  { title: 'Governed', desc: 'Five-tier human approval, immutable audit trails, and regional compliance are the architecture.' },
  { title: 'Data-informed', desc: 'Every claim carries its honesty status. We never blur proven vs. planned.' },
  { title: 'Modular', desc: 'Role-scoped agents configured in a registry — each component can be replaced independently.' },
  { title: 'Measurable', desc: 'Time saved, processes automated, decision cycles reduced. We report on what changed.' },
  { title: 'Progressive', desc: 'Start with a pilot, scale to production — with honest-status gates at every phase.' },
  { title: 'Secure', desc: 'Least-privilege permissions, Bandit + pre-commit gates, SHA-256 audit trails.' },
  { title: 'Practical adoption', desc: 'Designed for real constraints — mobile-first, local payment rails, intermittent connectivity.' },
];

export const AiCompanyBuilderSection: React.FC<AiCompanyBuilderSectionProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <div>
      <SectionHeading
        theme={theme}
        eyebrow="AI COMPANY BUILDER"
        title="Build Governed AI Companies"
        lead="LightSpeed helps organisations move from Opportunity to Continuous Improvement — a coordinated journey across strategy, architecture, agents, workflows, deployment, and governance. Every step carries its honesty status."
      />

      {/* The Journey */}
      <section aria-labelledby="journey-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80'}`}>
        <SectionHeading
          theme={theme}
          eyebrow="THE JOURNEY"
          title="Opportunity to Continuous Improvement"
          lead="From initial diagnosis to scaled deployment and beyond — nine connected phases ensure every step is governed, measured, and progressive."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {JOURNEY_STEPS.map((step, idx) => (
            <Reveal key={step.title} delay={(idx % 3) * 0.06}>
              <div className={`rounded-3xl p-6 border h-full ${
                isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
              }`}>
                <span className="font-body text-2xl font-black text-ls-red">{step.num}</span>
                <h3 className="mt-2 font-display font-bold text-base tracking-tight">{step.title}</h3>
                <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {step.desc}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Core Principles */}
      <section aria-labelledby="principles-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80'}`}>
        <SectionHeading
          theme={theme}
          eyebrow="PRINCIPLES"
          title="How We Build"
          lead="Ten principles guide every decision — from agent configuration to governance design."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {PRINCIPLES.map((principle, idx) => (
            <Reveal key={principle.title} delay={(idx % 5) * 0.05}>
              <div className={`rounded-2xl p-5 border ${
                isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
              }`}>
                <h4 className="font-display font-bold text-sm tracking-tight">{principle.title}</h4>
                <p className={`mt-2 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {principle.desc}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* The Operating Model */}
      <section aria-labelledby="model-heading" className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 ${isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80'}`}>
        <SectionHeading
          theme={theme}
          eyebrow="OPERATING MODEL"
          title="90 Agents, 1 Human CEO"
          lead="The canonical LightSpeed operating model uses 90 AI agents across 20 departments. Each agent has explicit role definitions, approval thresholds, and five-tier human oversight. High-impact decisions require human sign-off."
        />
        <div className={`rounded-3xl p-8 sm:p-10 border shadow-xl ${
          isLight ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy' : 'bg-ls-navy border-ls-white/15 text-ls-white'
        }`}>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="space-y-4">
              <h4 className="font-display font-bold text-lg">Human Direction</h4>
              <p className={`text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                One human CEO provides strategic direction. Every consequential decision passes through five tiers of human approval — machines execute, humans approve.
              </p>
            </div>
            <div className="space-y-4">
              <h4 className="font-display font-bold text-lg">Agent Workforce</h4>
              <p className={`text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                90 specialized agents across strategy, research, product, operations, governance, content, and finance — each configured with explicit permissions and audit trails.
              </p>
            </div>
            <div className="space-y-4">
              <h4 className="font-display font-bold text-lg">Governed Execution</h4>
              <p className={`text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                Immutable SHA-256 audit trails, risk-classified agent tiers, expiry sweeps on stale approvals, and circuit breakers on errors — governance is the architecture.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <div className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-8">
        <div className={`rounded-3xl p-8 sm:p-10 flex flex-col lg:flex-row lg:items-center gap-6 border ${
          isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
        }`}>
          <div className="flex-1 space-y-3">
            <span className="font-body text-[10px] font-bold tracking-widest text-ls-red">NEXT STEP</span>
            <h3 className="text-xl sm:text-2xl font-black tracking-tight font-display">Start Your AI Company Builder Journey</h3>
            <p className={`text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Begin with a governed discovery conversation — not a product demo. We will evaluate your readiness honestly and define exactly which phase fits your goals.
            </p>
          </div>
          <Link
            to="/contact"
            className="ripple-on inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90"
          >
            Book an Executive Briefing
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </Link>
        </div>
      </div>
    </div>
  );
};

export default AiCompanyBuilderSection;
