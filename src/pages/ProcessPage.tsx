import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { engagementProcess, company } from '../data/siteContent';

interface ProcessPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /process — the six-step engagement process:
 * DISCOVER → DIAGNOSE → DESIGN → BUILD → GOVERN → SCALE.
 *
 * Each step carries its own output artifact. The page also surfaces the
 * four-pillar framing from company.valueCycle (Strategy → Build → Govern → Scale).
 */
export const ProcessPage: React.FC<ProcessPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="HOW WE WORK"
        title="What an Engagement Looks Like"
        lead="This is the process we use to move from understanding to scale — Strategy, Build, Govern, and Scale."
      />

      {/* ── Six-Step Process Timeline ────────────────────── */}
      <section
        id="process"
        aria-labelledby="process-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="ENGAGEMENT PROCESS"
          title="Six Steps From Understanding to Scale"
          lead="Every engagement follows the same disciplined arc — from discovery through to expansion. No shortcuts, no skipped gates."
        />

        <div className="relative">
          {/* Vertical connector line (desktop) */}
          <div
            className="hidden md:block absolute left-[27px] top-0 bottom-0 w-px bg-gradient-to-b from-ls-red/40 via-ls-cyan/30 to-ls-red/40"
            aria-hidden="true"
          />

          <div className="space-y-0 divide-y divide-ls-grey-dark/20">
            {engagementProcess.map((step, idx) => {
              const isLast = idx === engagementProcess.length - 1;
              return (
                <Reveal key={step.name} delay={idx * 0.08}>
                  <div
                    className={`relative flex items-start gap-6 py-8 sm:py-10 ${
                      idx === 0 ? 'pt-0' : ''
                    } ${isLast ? 'pb-0' : ''}`}
                  >
                    {/* Step number badge */}
                    <div className="shrink-0 w-14 h-14 sm:w-16 sm:h-16 flex items-center justify-center rounded-full border-2 font-body font-black text-xl sm:text-2xl tracking-wider z-10 bg-ls-navy text-ls-white shadow-lg shadow-ls-red/20">
                      {step.num}
                    </div>

                    {/* Step content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-wrap items-center gap-2 mb-1">
                        <span className="font-body text-[10px] font-black tracking-widest text-ls-red">
                          {step.name}
                        </span>
                        <span
                          className={`inline-flex items-center rounded-full border px-2.5 py-0.5 font-body text-[9px] font-bold tracking-widest ${
                            isLight
                              ? 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan'
                              : 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan'
                          }`}
                        >
                          {step.output}
                        </span>
                      </div>
                      <h3
                        className={`font-display font-bold text-lg sm:text-xl tracking-tight ${
                          isLight ? 'text-ls-navy' : 'text-ls-white'
                        }`}
                      >
                        {step.title}
                      </h3>
                      <p
                        className={`mt-2 text-sm sm:text-base leading-relaxed ${
                          isLight
                            ? 'text-ls-grey-dark font-medium'
                            : 'text-ls-grey-light-text'
                        }`}
                      >
                        {step.description}
                      </p>
                    </div>
                  </div>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── Strategy → Build → Govern → Scale Callout ────── */}
      <section
        id="process-summary"
        aria-labelledby="process-summary-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
          isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="THE FOUR PILLARS"
          title="Strategy → Build → Govern → Scale"
          lead="The full arc of an engagement. Every phase feeds the next, and governance is never an afterthought — it is the architecture."
        />

        <div className="relative overflow-hidden rounded-3xl p-6 sm:p-8 md:p-12 border shadow-xl">
          {/* Corner screws */}
          <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />

          <div className={`border ${isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'}`} />

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8 relative z-10">
            {company.valueCycle.map((pillar, idx) => {
              const Icon = ArrowRight;
              return (
                <React.Fragment key={pillar}>
                  <div className="flex flex-col items-center text-center">
                    <div
                      className={`w-16 h-16 sm:w-18 sm:h-18 rounded-2xl flex items-center justify-center font-body font-black text-sm sm:text-base tracking-wider border-2 shadow-lg ${
                        idx === 0
                          ? isLight
                            ? 'bg-ls-navy border-ls-red text-ls-white shadow-ls-red/30'
                            : 'bg-ls-navy border-ls-red text-ls-white shadow-ls-red/30'
                          : isLight
                          ? 'bg-ls-white border-ls-cyan text-ls-navy shadow-ls-cyan/20'
                          : 'bg-ls-navy/60 border-ls-cyan text-ls-white shadow-ls-cyan/20'
                      }`}
                    >
                      {idx + 1}
                    </div>
                    <span
                      className={`mt-4 font-body text-[10px] font-bold tracking-widest uppercase ${
                        isLight ? 'text-ls-red' : 'text-ls-cyan'
                      }`}
                    >
                      {pillar}
                    </span>
                  </div>
                  {idx < company.valueCycle.length - 1 && (
                    <div className="hidden lg:flex items-center justify-center pt-10">
                      <ArrowRight className="w-5 h-5 text-ls-cyan" aria-hidden="true" />
                    </div>
                  )}
                </React.Fragment>
              );
            })}
          </div>

          {/* Mobile horizontal scroll */}
          <div className="lg:hidden flex items-center justify-center gap-4 mt-6 overflow-x-auto pb-2">
            {company.valueCycle.map((pillar, idx) => (
              <React.Fragment key={pillar}>
                <div className="flex flex-col items-center">
                  <div
                    className={`w-12 h-12 rounded-xl flex items-center justify-center font-body font-black text-xs tracking-wider border-2 ${
                      idx === 0
                        ? 'bg-ls-navy border-ls-red text-ls-white'
                        : 'bg-ls-white border-ls-cyan text-ls-navy'
                    }`}
                  >
                    {idx + 1}
                  </div>
                  <span
                    className={`mt-2 font-body text-[9px] font-bold tracking-widest uppercase ${
                      isLight ? 'text-ls-red' : 'text-ls-cyan'
                    }`}
                  >
                    {pillar}
                  </span>
                </div>
                {idx < company.valueCycle.length - 1 && (
                  <ArrowRight className="w-4 h-4 text-ls-cyan shrink-0" aria-hidden="true" />
                )}
              </React.Fragment>
            ))}
          </div>

          <div className="mt-8 text-center">
            <p
              className={`text-sm leading-relaxed max-w-2xl mx-auto ${
                isLight
                  ? 'text-ls-grey-dark font-medium'
                  : 'text-ls-grey-light-text'
              }`}
            >
              Governance is not a bolt-on — it is the architecture. Every engagement runs through all four pillars
              with five-tier human approval, immutable audit trails, and honest-status gates at every phase.
            </p>
          </div>
        </div>
      </section>

      <CtaBand
        theme={theme}
        title="Start With a Discovery Conversation"
        text="Every engagement begins with a governed, 5-tier-approved conversation — not a product demo. Tell us where your organisation is today and we will map the path forward."
        ctaLabel="Book a Discovery Call"
        ctaTo="/contact"
      />
    </>
  );
};

export default ProcessPage;
