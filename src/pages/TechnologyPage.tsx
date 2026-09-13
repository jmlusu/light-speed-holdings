import React from 'react';
import { ShieldCheck, Fingerprint, Lock, GitBranch, Database, Cpu } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import {
  technologyPillars,
  technologyMetrics,
  technologyMethods,
  honestyPolicy,
  GOVERNANCE_SOLUTION,
} from '../data/siteContent';

interface TechnologyPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

const GOVERNANCE_FACTS: { icon: React.ComponentType<{ className?: string }>; title: string; body: string }[] = [
  { icon: ShieldCheck, title: '5-Tier Human Approval Matrix', body: 'Consequential actions are risk-classified and routed through a human approval gate. Pending approvals expire on a periodic sweep, so the inbox never blocks forever on a stale request.' },
  { icon: Fingerprint, title: 'Immutable Audit Trails', body: 'Every agent action is recorded on a SHA-256 sealed, append-only trail. If it ran, there is a receipt — and it matches what was approved.' },
  { icon: Lock, title: 'RBAC + Least Privilege', body: 'X-API-Key role-based access on the control plane (admin / approve / run) and role-scoped agent permissions bound to the canonical 7-tool runtime.' },
  { icon: Database, title: 'Data Protection by Default', body: 'Malawi Data Protection Act 2017 as the default posture, GDPR-level handling for donor and UN data flows, and in-region data processing with a Zero-Cloud Boundary option for state, health, and financial data.' },
  { icon: GitBranch, title: 'Four-Gate Engineering', body: 'ruff → mypy → bandit → 2,373 regression tests must pass before any change to the platform lands. The tests that gate our work are published.' },
  { icon: Cpu, title: 'Provider-Agnostic & Sovereign', body: 'Self-hosted orchestration with optional free local models (Ollama). Your workforce runs on your infra, against your provider — no lock-in.' },
];

/**
 * /technology — how the platform behind every offer is engineered, with the
 * technical proof that gates our own work, and the governance layer that makes
 * deployment safe. Anchor #governance is the landing spot for the AI Governance
 * & Policy solution card and the nav dropdown.
 */
export const TechnologyPage: React.FC<TechnologyPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="TECHNOLOGY"
        title="Engineered to Be Trusted"
        lead="Every offer on this site runs on the same governed platform: an agentic operating layer with role-scoped agents, in-region data processing, four-gate engineering, and human approval on every consequential action."
      />

      {/* Architecture */}
      <section
        id="architecture"
        aria-labelledby="architecture-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="ARCHITECTURE"
          title="Ten Pillars of the Platform"
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {technologyPillars.map((pillar, idx) => (
            <Reveal key={pillar.title} delay={(idx % 3) * 0.06}>
              <div className={`rounded-3xl p-6 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <span className="font-mono text-[10px] font-black tracking-widest text-ls-red">
                  {String(idx + 1).padStart(2, '0')}
                </span>
                <h3 className="mt-2 font-display font-bold text-sm sm:text-base tracking-tight">{pillar.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {pillar.desc}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Technical Proof */}
      <section
        id="proof"
        aria-labelledby="proof-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="TECHNICAL PROOF"
          title="Measured, Not Claimed"
        />

        {/* Metrics */}
        <div className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 ${
          isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
        }`}>
          <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-6">
            {technologyMetrics.map((metric, idx) => (
              <div key={metric.label} className="min-w-0">
                <span className={`block text-xl sm:text-2xl font-black font-mono tracking-tight ${
                  idx % 2 === 0 ? 'text-ls-red' : 'text-ls-cyan'
                }`}>
                  {metric.value}
                </span>
                <span className={`block mt-1 text-[10px] font-mono font-bold tracking-widest uppercase ${
                  isLight ? 'text-slate-500' : 'text-zinc-500'
                }`}>
                  {metric.label}
                </span>
                <span className="block text-[10px] font-mono tracking-wider text-zinc-500">
                  {metric.source}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Methods */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          {technologyMethods.map((method, idx) => (
            <Reveal key={method.step} delay={idx * 0.06}>
              <div className={`rounded-2xl p-5 sm:p-6 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <span className="font-mono text-lg font-black text-ls-red">{method.step}</span>
                <h3 className="mt-2 font-display font-bold text-sm tracking-tight">{method.title}</h3>
                <p className={`mt-2 text-xs leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {method.detail}
                </p>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Honesty policy */}
        <Reveal>
          <div className={`mt-6 rounded-3xl p-6 sm:p-8 border ${
            isLight ? 'bg-white/95 border-slate-300 shadow-md' : 'bg-zinc-950/80 border-white/15 shadow-xl'
          }`}>
            <span className="font-mono text-[10px] font-bold tracking-widest text-ls-red">HONESTY POLICY</span>
            <ul className={`mt-4 grid grid-cols-1 sm:grid-cols-3 gap-x-8 gap-y-3 text-sm leading-relaxed ${
              isLight ? 'text-slate-700' : 'text-zinc-300'
            }`}>
              {honestyPolicy.map((point) => (
                <li key={point} className="flex items-start gap-2">
                  <span className="mt-0.5 shrink-0 w-4 h-4 rounded-full bg-ls-cyan/15 text-ls-cyan flex items-center justify-center text-[10px] font-black" aria-hidden="true">✓</span>
                  {point}
                </li>
              ))}
            </ul>
          </div>
        </Reveal>
      </section>

      {/* Security & Governance */}
      <section
        id="governance"
        aria-labelledby="governance-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="SECURITY & GOVERNANCE"
          title="The Layer That Makes Deployment Safe"
          lead={GOVERNANCE_SOLUTION.lead}
        />
        <div className="mb-10 text-center">
          <HonestyBadge label={GOVERNANCE_SOLUTION.proof} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {GOVERNANCE_FACTS.map((fact, idx) => {
            const Icon = fact.icon;
            return (
              <Reveal key={fact.title} delay={(idx % 2) * 0.06}>
                <div className={`rounded-3xl p-6 sm:p-7 border h-full ${
                  isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
                }`}>
                  <div className="flex items-center gap-3">
                    <span aria-hidden="true" className="inline-flex w-9 h-9 shrink-0 items-center justify-center rounded-xl bg-ls-red/10 text-ls-red">
                      <Icon className="w-4 h-4" />
                    </span>
                    <h3 className="font-display font-bold text-sm sm:text-base tracking-tight">{fact.title}</h3>
                  </div>
                  <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${
                    isLight ? 'text-slate-700' : 'text-zinc-300'
                  }`}>
                    {fact.body}
                  </p>
                </div>
              </Reveal>
            );
          })}
        </div>

        <p className={`mt-8 text-center text-sm leading-relaxed ${
          isLight ? 'text-slate-600' : 'text-zinc-400'
        }`}>
          This governance pattern is also the subject of our regional policy work —{' '}
          <a href="/work#policy" className="font-bold text-ls-cyan hover:underline">the SADC Agentic AI Governance Framework</a> — so believe it when you see it on the policy track.
        </p>
      </section>

      <CtaBand
        theme={theme}
        title="Want the Technical Deep-Dive?"
        text="We publish the architecture that runs our own operation — and we will show you exactly where your organisation's data, and your risk, sits in any deployment we propose."
      />
    </>
  );
};

export default TechnologyPage;
