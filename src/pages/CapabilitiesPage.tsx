import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Boxes, Radar } from 'lucide-react';
import { OperatingModelSection } from '../components/OperatingModelSection';

interface CapabilitiesPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

interface SpokeCard {
  num: string;
  title: string;
  icon: React.ComponentType<{ className?: string }>;
  desc: string;
  to: string;
  cta: string;
}

const SPOKES: SpokeCard[] = [
  {
    num: '01',
    title: 'Core Offerings',
    icon: Boxes,
    desc: 'The four connected services — strategy, private intelligence, autonomous systems, and audited execution — with input/output contracts, lineage, and deliverables for each.',
    to: '/capabilities/offerings',
    cta: 'Explore the Offering Suite',
  },
  {
    num: '02',
    title: 'AI Diagnostic',
    icon: Radar,
    desc: 'An interactive, sector-aware assessment that scores your operating model across four pillars and produces honest, tiered recommendations before any engagement begins.',
    to: '/capabilities/diagnostic',
    cta: 'Run the Diagnostic',
  },
];

interface PlatformScenario {
  id: string;
  title: string;
  desc: string;
  status: string;
}

const SCENARIOS: PlatformScenario[] = [
  {
    id: 'FOW-01',
    title: 'Startup Acceleration (Solo Founder + AI)',
    desc: 'A solo founder operates with the functional coverage of a multi-person team: agents handle CTO, CFO, CMO, and CLO roles, with a CEO dashboard for real-time visibility. The founder sets vision; agents execute operations, legal, finance, marketing, and sales.',
    status: 'Proven in-house — LightSpeed itself operates as a 1-human, 144-agent organisation.',
  },
  {
    id: 'FOW-02',
    title: 'Enterprise Automation (Augment Existing Teams)',
    desc: 'Existing teams gain specialist AI agents for compliance scanning, data pipelines, and contract review — without the 6-month hiring cycle. The system adapts to an organization\'s structure via YAML configuration.',
    status: 'In active development — enterprise deployment model designed for SADC regulatory environments.',
  },
  {
    id: 'FOW-03',
    title: 'Consulting Firm Scale (Delivery Backbone)',
    desc: 'Consulting firms sell expertise but are constrained by headcount. Agents handle research, analysis, and report generation; humans focus on client relationships.',
    status: 'In active development — framework validated in LightSpeed\'s own consulting operations.',
  },
  {
    id: 'FOW-04',
    title: 'Non-Profit Operations (Full Capability, Minimal Staff)',
    desc: 'A small non-profit gets coverage across finance, HR, compliance, M&E, and donor communications. The audit trail provides the documentation grantmakers require.',
    status: 'In active development — supports free local models (Ollama) for budget-constrained deployments.',
  },
  {
    id: 'FOW-05',
    title: 'Government Compliance (Authorisation-Aligned)',
    desc: 'AI agents handle compliance monitoring, contract review, and regulatory reporting. The 5-tier approval matrix aligns with government authorisation levels.',
    status: 'In active development — governance framework mapped to Malawi DPA and SADC standards.',
  },
  {
    id: 'FOW-06',
    title: 'E-Commerce (24/7 Customer Success)',
    desc: 'Customer success, sales pipeline, and marketing analytics without shift-based human teams. AI agents maintain customer context across interactions and escalate high-value issues.',
    status: 'In active development — WhatsApp-native interface designed for SADC mobile-first markets.',
  },
  {
    id: 'FOW-07',
    title: 'Healthcare Administration',
    desc: 'Billing compliance, patient scheduling, credentialing, and regulatory reporting — agents handle the administrative burden so clinical staff can focus on patients. Memory encryption and PII detection for sensitive data environments.',
    status: 'In active development — designed for Malawi DPA and GDPR compliance.',
  },
  {
    id: 'FOW-08',
    title: 'Financial Services (Risk & Compliance)',
    desc: 'Continuous compliance monitoring, risk analysis, and audit preparation. The 5-tier approval matrix maps directly to financial services authorisation levels.',
    status: 'In active development — audit trail meets financial regulatory documentation requirements.',
  },
];

/**
 * Capabilities overview. Leads with the interactive operating model, then
 * spokes out to the two deep-dive sub-pages (offerings + diagnostic), and
 * closes with the eight company deployment scenarios that show the platform
 * in practice across organisation types.
 */
export const CapabilitiesPage: React.FC<CapabilitiesPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      {/* Page Intro */}
      <header className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-24 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
          <span>CAPABILITY SYSTEM</span>
        </div>
        <h1 className={`mt-4 text-3xl sm:text-5xl font-black tracking-tight font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
          The Lightspeed Delivery Model
        </h1>
        <p className={`mt-4 max-w-2xl text-sm sm:text-base leading-relaxed ${isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'}`}>
          Four connected offerings — strategy, private intelligence, autonomous agent fleets, and audited core execution — compiled into one closed-loop operating system for regulated enterprises across SADC.
        </p>
      </header>

      {/* Interactive Operating Model */}
      <OperatingModelSection theme={theme} onRequestBriefing={onRequestBriefing} />

      {/* Hub-and-Spoke Navigation to the two deep-dive pages */}
      <section
        aria-labelledby="capability-spokes-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
            OVERVIEW
          </span>
          <h2
            id="capability-spokes-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}
          >
            Two Deep-Dive Modules
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'}`}>
            This page is the overview of the Lightspeed Delivery Model. The two deep-dive modules below carry the detailed offerings and the interactive diagnostic on their own documented pages — readable, shareable, and inspectable.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {SPOKES.map((spoke) => {
            const Icon = spoke.icon;
            return (
              <article
                key={spoke.num}
                className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 transition-transform hover:-translate-y-1 ${
                  isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
                }`}
              >
                {/* Hardware corner screws */}
                <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
                <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
                <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
                <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

                <div className="flex items-center justify-between">
                  <span className={`font-mono text-[10px] font-bold tracking-widest text-ls-red`}>
                    MODULE {spoke.num}
                  </span>
                  <Icon className="w-5 h-5 text-ls-cyan" aria-hidden="true" />
                </div>

                <h3 className={`mt-4 text-xl font-bold tracking-tight font-display ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  {spoke.title}
                </h3>
                <p className="mt-3 text-xs sm:text-sm leading-relaxed">{spoke.desc}</p>

                <Link
                  to={spoke.to}
                  className="mt-5 inline-flex items-center gap-2 font-mono text-[11px] font-bold text-ls-red hover:text-ls-red cursor-pointer group"
                >
                  <span>{spoke.cta}</span>
                  <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
                </Link>
              </article>
            );
          })}
        </div>
      </section>

      {/* Company Scenarios — Platform Use Cases */}
      <section
        aria-labelledby="company-scenarios-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
            EIGHT DEPLOYMENT SCENARIOS
          </span>
          <h2
            id="company-scenarios-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}
          >
            Company Scenarios
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'}`}>
            Company Scenarios — Platform Use Cases. Eight ways the Lightspeed platform deploys across organisation types, from a solo founder running a full company to regulated financial services.
          </p>
          <span className="block text-[10px] font-mono font-bold tracking-[0.25em] text-ls-cyan">
            PLATFORM USE CASES — NOT CLIENT DELIVERABLES
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {SCENARIOS.map((scenario) => (
            <article
              key={scenario.id}
              className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 ${
                isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
              }`}
            >
              {/* Hardware corner screws */}
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              <em className="font-mono text-[10px] font-bold tracking-widest text-ls-red not-italic">
                {scenario.id}
              </em>
              <h3 className={`mt-4 text-lg font-bold tracking-tight font-display ${
                isLight ? 'text-slate-900' : 'text-zinc-100'
              }`}>
                {scenario.title}
              </h3>
              <p className="mt-3 text-xs sm:text-sm leading-relaxed">{scenario.desc}</p>
              <p className={`mt-4 font-mono text-[10px] font-bold tracking-wider text-ls-cyan`}>
                {scenario.status}
              </p>
            </article>
          ))}
        </div>
      </section>
    </>
  );
};

export default CapabilitiesPage;
