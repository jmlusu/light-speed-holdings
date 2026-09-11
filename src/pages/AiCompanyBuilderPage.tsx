import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, ShieldCheck, Fingerprint, Scale, Lock } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { CardShell } from '../components/site/CardShell';
import { Reveal } from '../components/Reveal';
import { aiCompanyBuilder, scenarios } from '../data/siteContent';

interface AiCompanyBuilderPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

const GOVERNANCE_POINTS = [
  { icon: ShieldCheck, title: '5-Tier Human Approval', desc: 'Every consequential action in the workforce is classified and routed through a human approval matrix — with expiry sweeps so stale approvals never block work.' },
  { icon: Fingerprint, title: 'Immutable Audit Trail', desc: 'SHA-256 sealed records on every agent action. If it ran, there is a receipt — and it matches what was approved.' },
  { icon: Scale, title: 'Risk-Classified Tiers', desc: 'Agents are configured with role-scoped permissions against a canonical 7-tool runtime. No agent can invent a capability on its own.' },
  { icon: Lock, title: 'Security by Design', desc: 'Least-privilege defaults, PII detection, encryption at rest, and in-region data processing with a Zero-Cloud Boundary option for sensitive work.' },
];

/**
 * /ai-company-builder — the flagship offer. The governed AI workforce that runs
 * LightSpeed is licensed to run on our clients' infrastructure.
 */
export const AiCompanyBuilderPage: React.FC<AiCompanyBuilderPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="AI COMPANY BUILDER"
        title="Your Governed AI Workforce"
        lead={aiCompanyBuilder.concept}
      >
        <div className="mt-5">
          <Link
            to="/contact"
            className="inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:brightness-110"
          >
            Start a Conversation
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </Link>
        </div>
      </PageIntro>

      {/* The Ladder */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading
          theme={theme}
          eyebrow="THE LADDER"
          title="From Traditional to AI-Native Company"
          lead="Most organisations stop at 'software that helps people work'. An AI-native company replaces stationary layers of the ladder with an operating model where humans direct and agents execute — and the whole stack remains auditable."
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
          {/* Traditional column */}
          <Reveal>
            <CardShell className={`h-full ${isLight ? 'bg-white/95 border-slate-300 shadow-md' : 'bg-zinc-950/80 border-white/15 shadow-xl'}`}>
              <div className="flex items-center justify-between">
                <h3 className={`font-display font-black text-base sm:text-lg tracking-tight ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  Traditional Company
                </h3>
                <span className="font-mono text-[10px] font-bold tracking-widest text-zinc-500">TODAY</span>
              </div>
              <ul className={`mt-6 space-y-2.5 ${
                isLight ? 'text-slate-700' : 'text-zinc-300'
              }`}>
                {[...aiCompanyBuilder.ladder.traditional].reverse().map((rung) => (
                  <li key={rung} className={`flex items-center gap-3 px-4 py-3 rounded-2xl border ${
                    isLight ? 'border-slate-200 bg-slate-50' : 'border-white/10 bg-zinc-900/60'
                  }`}>
                    <span className="w-2 h-2 shrink-0 rounded-full bg-zinc-400" aria-hidden="true" />
                    <span className="text-xs sm:text-sm font-bold">{rung}</span>
                  </li>
                ))}
              </ul>
            </CardShell>
          </Reveal>

          {/* AI-Native column */}
          <Reveal delay={0.1}>
            <CardShell className={`h-full ${isLight ? 'hardware-chassis-light' : 'hardware-chassis-dark'}`}>
              <div className="flex items-center justify-between">
                <h3 className={`font-display font-black text-base sm:text-lg tracking-tight ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  AI-Native Company
                </h3>
                <span className="font-mono text-[10px] font-bold tracking-widest text-ls-cyan">THE TARGET</span>
              </div>
              <ul className={`mt-6 space-y-2.5 ${
                isLight ? 'text-slate-800' : 'text-zinc-200'
              }`}>
                {[...aiCompanyBuilder.ladder.native].reverse().map((rung) => (
                  <li key={rung} className="flex items-center gap-3 px-4 py-3 rounded-2xl border border-ls-cyan/25 bg-ls-cyan/5">
                    <span className="w-2 h-2 shrink-0 rounded-full bg-ls-cyan shadow-[0_0_6px_rgba(0,191,255,0.8)]" aria-hidden="true" />
                    <span className="text-xs sm:text-sm font-bold">{rung}</span>
                  </li>
                ))}
              </ul>
            </CardShell>
          </Reveal>
        </div>
      </section>

      {/* Licensing / Offer E */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="max-w-4xl mx-auto">
          <div className={`relative overflow-hidden rounded-3xl p-8 sm:p-10 ${
            isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-100'
          }`}>
            <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
            <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
            <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
            <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />

            <span className="font-mono text-[10px] font-bold tracking-widest text-ls-red">
              {aiCompanyBuilder.licensing.offer.toUpperCase()}
            </span>
            <h2 className="mt-3 text-2xl sm:text-4xl font-black tracking-tight font-display">
              The Same Engine That Runs LightSpeed
            </h2>
            <p className={`mt-4 text-sm sm:text-base leading-relaxed max-w-2xl ${
              isLight ? 'text-slate-700' : 'text-zinc-300'
            }`}>
              {aiCompanyBuilder.licensing.details[0]}
            </p>
            <div className="mt-6 inline-flex items-center gap-2.5 px-5 py-2.5 rounded-2xl border border-ls-cyan/25 bg-ls-cyan/5">
              <span className="font-mono text-xs sm:text-sm font-black tracking-wider text-ls-cyan">
                {aiCompanyBuilder.licensing.price}
              </span>
            </div>
            <ul className={`mt-6 grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2.5 text-xs sm:text-sm leading-relaxed ${
              isLight ? 'text-slate-700' : 'text-zinc-300'
            }`}>
              {aiCompanyBuilder.licensing.details.slice(1).map((detail) => (
                <li key={detail} className="flex items-start gap-2">
                  <span className="mt-0.5 font-black text-ls-red" aria-hidden="true">+</span>
                  {detail}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* What it includes */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading
          theme={theme}
          eyebrow="WHAT IT INCLUDES"
          title="Every Layer of the AI-Native Company"
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {aiCompanyBuilder.dimensions.map((dim, idx) => (
            <Reveal key={dim.title} delay={(idx % 3) * 0.06}>
              <div className={`rounded-3xl p-6 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <span className="font-mono text-[10px] font-black tracking-widest text-ls-red">
                  {String(idx + 1).padStart(2, '0')}
                </span>
                <h3 className="mt-2 font-display font-bold text-sm sm:text-base tracking-tight">{dim.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {dim.desc}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Governance strip */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading
          theme={theme}
          eyebrow="GOVERNANCE"
          title="Trust Is the Architecture"
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {GOVERNANCE_POINTS.map((point, idx) => {
            const Icon = point.icon;
            return (
              <Reveal key={point.title} delay={idx * 0.06}>
                <div className={`rounded-3xl p-6 border h-full ${
                  isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
                }`}>
                  <span aria-hidden="true" className="inline-flex w-9 h-9 items-center justify-center rounded-xl bg-ls-red/10 text-ls-red">
                    <Icon className="w-4 h-4" />
                  </span>
                  <h3 className="mt-4 font-display font-bold text-sm sm:text-base tracking-tight">{point.title}</h3>
                  <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                    isLight ? 'text-slate-700' : 'text-zinc-300'
                  }`}>
                    {point.desc}
                  </p>
                </div>
              </Reveal>
            );
          })}
        </div>
        <p className={`mt-8 text-center text-sm leading-relaxed ${
          isLight ? 'text-slate-600' : 'text-zinc-400'
        }`}>
          The full architecture behind these controls lives on the{' '}
          <Link to="/technology" className="font-bold text-ls-cyan hover:underline">Technology page</Link>.
        </p>
      </section>

      {/* Deployment scenarios */}
      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading
          theme={theme}
          eyebrow="DEPLOYMENT SCENARIOS"
          title="Eight Ways an AI Company Builder Ships"
          lead="From a solo founder accelerating a startup to a government agency running compliance — the same governed workforce, the same honesty about status."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {scenarios.map((scenario, idx) => (
            <Reveal key={scenario.id} delay={(idx % 2) * 0.06}>
              <div className={`rounded-3xl p-6 sm:p-7 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <div className="flex items-center justify-between gap-3">
                  <span className="font-mono text-[10px] font-black tracking-widest text-ls-red">{scenario.id}</span>
                </div>
                <h3 className="mt-2 font-display font-bold text-base sm:text-lg tracking-tight">{scenario.title}</h3>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {scenario.desc}
                </p>
                <p className={`mt-4 pt-4 border-t text-[11px] leading-relaxed font-mono font-bold tracking-wider ${
                  isLight ? 'border-slate-200 text-zinc-500' : 'border-white/10 text-zinc-500'
                }`}>
                  <span className="text-ls-cyan">STATUS // </span>
                  {scenario.status}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand
        theme={theme}
        title="Build Your Own AI-Native Company"
        text={`${aiCompanyBuilder.licensing.offer} is licensed, self-hosted, and provider-agnostic — starting at ${aiCompanyBuilder.licensing.price}. Tell us where your organisation is today.`}
      />
    </>
  );
};

export default AiCompanyBuilderPage;
