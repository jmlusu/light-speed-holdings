import React from 'react';
import { FaqSection } from '../components/FaqSection';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { CardShell } from '../components/site/CardShell';
import { Reveal } from '../components/Reveal';
import { mission, vision, values, commitments, company } from '../data/siteContent';

interface AboutPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

/**
 * /about — the firm, told honestly. Leads with the official Mission & Vision,
 * then Our Story, How We Think (the eight values), commitments, leadership,
 * and the reasons to choose LightSpeed. Every claim stays traceable.
 */
export const AboutPage: React.FC<AboutPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="ABOUT THE FIRM"
        title="An Agentic AI Company That Ships"
        lead="LightSpeed Holdings Limited™ builds and governs agentic AI systems for organizations. One human CEO directs a workforce of 140+ AI agents. We prove the model in Malawi first — websites, automation, reporting, and marketing, shipped for the organizations that need them most."
      />

      {/* Mission & Vision */}
      <section
        aria-labelledby="mission-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="MISSION AND VISION"
          title="Why We Do This"
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Reveal>
            <CardShell className={`h-full ${isLight ? 'bg-white/95 border-slate-300 shadow-md text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-xl text-zinc-100'}`}>
              <span className="text-xs font-mono font-bold tracking-widest text-ls-red">MISSION</span>
              <p className={`mt-3 text-sm sm:text-base leading-relaxed font-semibold ${
                isLight ? 'text-slate-800' : 'text-zinc-100'
              }`}>
                {mission.statement}
              </p>
              <p className={`mt-4 text-justify text-xs sm:text-sm leading-relaxed ${
                isLight ? 'text-slate-600' : 'text-zinc-400'
              }`}>
                {mission.why}
              </p>
            </CardShell>
          </Reveal>

          <Reveal delay={0.1}>
            <CardShell className={`h-full ${isLight ? 'bg-white/95 border-slate-300 shadow-md text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-xl text-zinc-100'}`}>
              <span className="text-xs font-mono font-bold tracking-widest text-ls-cyan">VISION</span>
              <p className={`mt-3 text-sm sm:text-base leading-relaxed font-semibold ${
                isLight ? 'text-slate-800' : 'text-zinc-100'
              }`}>
                {vision.statement}
              </p>
              <p className={`mt-4 text-justify text-xs sm:text-sm leading-relaxed ${
                isLight ? 'text-slate-600' : 'text-zinc-400'
              }`}>
                {vision.why}
              </p>
            </CardShell>
          </Reveal>
        </div>

        <p className={`mt-10 text-center text-sm sm:text-base font-mono font-bold tracking-widest ${
          isLight ? 'text-slate-600' : 'text-zinc-400'
        }`}>
          <span className="text-ls-red">NORTH STAR // </span>
          {company.northStar.toUpperCase()}
        </p>
      </section>

      {/* Our Story */}
      <section
        aria-labelledby="story-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="OUR STORY"
          title="Proof, Then Scale"
          lead="The company is its own first customer. Everything we sell is run in production here first."
        />
        <div className={`max-w-3xl mx-auto space-y-4 text-justify text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700' : 'text-zinc-300'
        }`}>
          <p>
            Malawi's SMEs, NGOs, schools, clinics, and cooperatives are underserved by an industry that prices enterprise-grade work out of reach. LightSpeed was founded to close that gap — not with a promise, but with a working system.
          </p>
          <p>
            Today that system runs 144 agent configurations across 20 departments, governed by a five-tier human approval matrix and an immutable audit trail. Our first live proof in the real, non-tech economy: J&S StopOver Bar — a genuine Malawi SME running agentic decision support for inventory, sales, shortage detection, cash reconciliation, and procurement.
          </p>
          <p>
            We do not claim to have all the answers. We publish the tests that gate our work, label every claim{' '}
            <span className="font-bold text-ls-cyan">Proven in-house</span> or{' '}
            <span className="font-bold text-ls-red">In pilot</span> — and we treat Malawi first as the discipline that makes us credible everywhere else.
          </p>
        </div>
      </section>

      {/* How We Think */}
      <section
        aria-labelledby="values-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="HOW WE THINK"
          title="Eight Values, Turned Into Behavior"
          lead="Values without 'how this shows up' are decoration. Ours map to concrete operating rules."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {values.map((value, idx) => (
            <Reveal key={value.num} delay={(idx % 4) * 0.05}>
              <div className={`rounded-3xl p-6 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <span className="font-mono text-[10px] font-black tracking-widest text-ls-red">
                  VALUES // {String(value.num).padStart(2, '0')}
                </span>
                <h3 className="mt-2 font-display font-bold text-sm sm:text-base tracking-tight">{value.title}</h3>
                <p className={`mt-2 text-xs leading-relaxed ${
                  isLight ? 'text-slate-600' : 'text-zinc-400'
                }`}>
                  {value.sentence}
                </p>
                <p className={`mt-3 pt-3 border-t text-[11px] leading-relaxed ${
                  isLight ? 'border-slate-200 text-ls-cyan font-semibold' : 'border-white/10 text-ls-cyan font-semibold'
                }`}>
                  {value.showsUp}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Commitments */}
      <section
        aria-labelledby="commitments-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="COMMITMENTS"
          title="What We Promise Whom"
          lead="Accountability is not a value statement — it is a list of who owes what to whom."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {commitments.map((group, idx) => (
            <Reveal key={group.audience} delay={(idx % 2) * 0.06}>
              <div className={`rounded-3xl p-6 sm:p-7 border h-full ${
                isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md' : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl'
              }`}>
                <h3 className="font-display font-bold text-base sm:text-lg tracking-tight">{group.audience}</h3>
                <ul className={`mt-4 space-y-3 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {group.items.map((item) => (
                    <li key={item} className="flex items-start gap-2.5">
                      <span className="mt-0.5 shrink-0 w-4 h-4 rounded-full bg-ls-red/10 text-ls-red flex items-center justify-center text-[10px] font-black" aria-hidden="true">✓</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Leadership */}
      <section
        aria-labelledby="leadership-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="LEADERSHIP"
          title="One Human CEO. A Governed Workforce."
          lead="The operating model we sell is the operating model we run."
        />
        <div className={`max-w-3xl mx-auto rounded-3xl p-6 sm:p-8 border ${
          isLight ? 'bg-white/95 border-slate-300 shadow-md' : 'bg-zinc-950/80 border-white/15 shadow-xl'
        }`}>
          <ul className={`space-y-3 text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700' : 'text-zinc-300'
          }`}>
            <li className="flex items-start gap-3">
              <span className="font-mono font-black text-ls-red" aria-hidden="true">01</span>
              <span>One human CEO sets vision, strategy, and culture, and makes final decisions on high-stakes matters.</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="font-mono font-black text-ls-red" aria-hidden="true">02</span>
              <span>140+ AI agents execute across 20 departments — engineering, legal, governance, policy, creative, and more.</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="font-mono font-black text-ls-red" aria-hidden="true">03</span>
              <span>A standing governance body reviews high-stakes decisions and sets ethics precedent before they are executed.</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="font-mono font-black text-ls-red" aria-hidden="true">04</span>
              <span>Every consequential action passes a five-tier human approval matrix and lands on an immutable audit trail.</span>
            </li>
          </ul>
        </div>
      </section>

      <FaqSection theme={theme} />

      <CtaBand
        theme={theme}
        title="Talk to the Human in the Loop"
        text="Every conversation starts with a human. Tell us where your organisation is today — we will be honest about whether we can help, and what it takes."
        ctaLabel="Start a Conversation"
      />
    </>
  );
};

export default AboutPage;
