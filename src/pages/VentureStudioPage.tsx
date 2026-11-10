import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Building2, Gauge, Layers, ShieldCheck } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { Reveal } from '../components/Reveal';
import { CTAS } from '../data/ctas';
import {
  portfolioArchetypes,
  stageGates,
  studioMetrics,
  studioModels,
  studioPillars,
} from '../data/venture-studio';

interface VentureStudioPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * AI Venture Studio page.
 *
 * Source of truth: docs/venture-studio/03-operating-model.md and
 * docs/venture-studio/05-kpi-scorecard.md. The scorecard figures are blueprint
 * TARGETS from the strategy deliverable, not measured results, and the page
 * labels them as such.
 */
export const VentureStudioPage: React.FC<VentureStudioPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const cardBase = isLight
    ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy shadow-md'
    : 'bg-ls-navy border-ls-white/15 text-ls-white shadow-xl';
  const muted = isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text';
  const sectionBase = `px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t ${
    isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
  }`;

  return (
    <>
      {/* 1. THE MODEL */}
      <PageIntro
        theme={theme}
        eyebrow="AI VENTURE STUDIO"
        title="A Repeatable Engine for AI-Native Companies"
        lead="LightSpeed Holdings is built as an AI-native organisation first, then operated as a venture studio: one shared agent stack, one governance model, and one go-to-market that every new venture inherits instead of rebuilding."
      >
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={() => onRequestBriefing?.(CTAS.primary.label)}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90"
          >
            {CTAS.primary.label}
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </button>
          <a
            href="#scorecard"
            className={`inline-flex items-center gap-2 px-5 py-3 rounded-full font-bold text-xs tracking-widest uppercase border transition-all ${
              isLight
                ? 'border-ls-grey-dark/40 text-ls-navy hover:bg-ls-navy/5'
                : 'border-ls-white/20 text-ls-white hover:bg-ls-white/5'
            }`}
          >
            View the Scorecard
          </a>
        </div>
      </PageIntro>

      {/* 2. TWO DEFINITIONS */}
      <section className={sectionBase}>
        <SectionHeading
          theme={theme}
          eyebrow="DEFINITIONS"
          title="AI-Native Organisation Is the Prerequisite"
          lead="A venture studio is only as repeatable as the organisation running it. These are the two definitions the operating model is built on, each with the failure mode it exists to prevent."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {studioModels.map((model, idx) => (
            <Reveal key={model.id} delay={idx * 0.08}>
              <article className={`h-full rounded-3xl p-6 sm:p-8 border flex flex-col ${cardBase}`}>
                <span className="font-body text-[10px] font-black tracking-widest text-ls-red uppercase">
                  MODEL {String(idx + 1).padStart(2, '0')}
                </span>
                <h3 className="mt-3 text-xl font-bold font-display tracking-tight">{model.title}</h3>
                <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${muted}`}>{model.definition}</p>
                <div className={`mt-5 pt-4 border-t ${isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'}`}>
                  <span className="font-body text-[9px] font-bold tracking-widest text-ls-red uppercase">
                    FAILURE MODE WITHOUT IT
                  </span>
                  <p className={`mt-1.5 text-xs leading-relaxed ${muted}`}>{model.failureMode}</p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      {/* 3. THE THREE STUDIO FUNCTIONS */}
      <section className={sectionBase}>
        <SectionHeading
          theme={theme}
          eyebrow="OPERATING MODEL"
          title="Three Functions, Shared Across Every Venture"
          lead="The studio is not a fund and not an agency. It runs three functions, each of which owns a slice of the stack and hands the shared asset to every spin-out."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {studioPillars.map((pillar, idx) => (
            <Reveal key={pillar.id} delay={idx * 0.08}>
              <article className={`h-full rounded-3xl p-6 sm:p-8 border flex flex-col ${cardBase}`}>
                <Layers className="w-6 h-6 text-ls-cyan mb-3" aria-hidden="true" />
                <span className="font-body text-[10px] font-black tracking-widest text-ls-red uppercase">
                  FUNCTION {String(idx + 1).padStart(2, '0')}
                </span>
                <h3 className="mt-2 text-lg font-bold font-display tracking-tight">{pillar.title}</h3>
                <p className={`mt-3 text-xs leading-relaxed ${muted}`}>{pillar.owns}</p>
                <div className={`mt-5 pt-4 border-t ${isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'}`}>
                  <span className="font-body text-[9px] font-bold tracking-widest text-ls-cyan uppercase">
                    SHARED ASSET
                  </span>
                  <p className={`mt-1.5 text-xs leading-relaxed ${muted}`}>{pillar.sharedAssets}</p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      {/* 4. PORTFOLIO ARCHETYPES */}
      <section className={sectionBase}>
        <SectionHeading
          theme={theme}
          eyebrow="PORTFOLIO"
          title="Three Archetypes the Studio Builds"
          lead="Every venture is one of three shapes. The shape decides how much of the shared stack it pulls and how sovereign its deployment has to be."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {portfolioArchetypes.map((archetype, idx) => (
            <Reveal key={archetype.id} delay={idx * 0.08}>
              <article className={`h-full rounded-3xl p-6 sm:p-8 border flex flex-col ${cardBase}`}>
                <div className="flex items-center gap-3">
                  <span
                    aria-hidden="true"
                    className="flex w-9 h-9 items-center justify-center rounded-full border border-ls-red/40 bg-ls-red/10 font-display font-black text-ls-red"
                  >
                    {archetype.id}
                  </span>
                  <h3 className="text-lg font-bold font-display tracking-tight">{archetype.title}</h3>
                </div>
                <p className={`mt-4 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                  {archetype.valueProp}
                </p>
                <div className={`mt-5 pt-4 border-t ${isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'}`}>
                  <span className="font-body text-[9px] font-bold tracking-widest text-ls-red uppercase">
                    STACK PULL
                  </span>
                  <p className={`mt-1.5 text-xs leading-relaxed ${muted}`}>{archetype.stackPull}</p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      {/* 5. SCORECARD TARGETS */}
      <section id="scorecard" className={sectionBase}>
        <SectionHeading
          theme={theme}
          eyebrow="SCORECARD"
          title="What the Studio Measures"
          lead="Four metrics decide whether a venture continues. The targets below are blueprint targets from the studio strategy, not measured results - no venture has reported against them yet."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {studioMetrics.map((metric, idx) => (
            <Reveal key={metric.id} delay={idx * 0.06}>
              <article className={`h-full rounded-3xl p-6 border flex flex-col justify-between ${cardBase}`}>
                <div>
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="text-base font-bold font-display tracking-tight">{metric.metric}</h3>
                    <Gauge className="w-4 h-4 text-ls-cyan shrink-0 mt-1" aria-hidden="true" />
                  </div>
                  <p className={`mt-2 text-xs leading-relaxed ${muted}`}>{metric.definition}</p>
                </div>
                <div className={`mt-4 pt-3 border-t ${isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'}`}>
                  <span className="font-body text-[9px] font-bold tracking-widest text-ls-red uppercase">
                    BLUEPRINT TARGET
                  </span>
                  <p className="mt-1 font-display font-black text-lg tracking-tight text-ls-red">
                    {metric.target}
                  </p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      {/* 6. STAGE GATES */}
      <section className={sectionBase}>
        <SectionHeading
          theme={theme}
          eyebrow="STAGE GATES"
          title="Four Gates Before a Spin-Out"
          lead="A venture advances only when the previous gate's exit evidence exists. The gate is the kill decision, and it is written down before the work starts."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {stageGates.map((gate, idx) => (
            <Reveal key={gate.phase} delay={idx * 0.06}>
              <article className={`h-full rounded-3xl p-6 border flex flex-col ${cardBase}`}>
                <span className="font-body text-[10px] font-black tracking-widest text-ls-red uppercase">
                  {gate.phase}
                </span>
                <span className={`mt-1 font-body text-[10px] font-bold ${muted}`}>{gate.window}</span>
                <p className={`mt-3 text-xs leading-relaxed ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                  {gate.goal}
                </p>
                <div className={`mt-4 pt-3 border-t ${isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'}`}>
                  <span className="font-body text-[9px] font-bold tracking-widest text-ls-cyan uppercase">
                    EXIT GATE
                  </span>
                  <p className={`mt-1.5 text-xs leading-relaxed ${muted}`}>{gate.exitGate}</p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      {/* 7. WHAT MAKES IT DEFENSIBLE */}
      <section className={sectionBase}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className={`p-6 rounded-3xl border ${isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy/60 border-ls-white/10'}`}>
            <ShieldCheck className="w-6 h-6 text-ls-red mb-3" aria-hidden="true" />
            <h3 className="font-bold text-base font-display">Governance Travels With the Stack</h3>
            <p className={`mt-2 text-xs leading-relaxed ${muted}`}>
              Five-tier human approval, audit trails and the claim rules are inherited by every
              venture. A spin-out cannot launch without them.
            </p>
          </div>
          <div className={`p-6 rounded-3xl border ${isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy/60 border-ls-white/10'}`}>
            <Building2 className="w-6 h-6 text-ls-cyan mb-3" aria-hidden="true" />
            <h3 className="font-bold text-base font-display">Local Rails From Day One</h3>
            <p className={`mt-2 text-xs leading-relaxed ${muted}`}>
              Mobile money, offline-tolerant operation and data residency are platform defaults, so
              each venture does not re-solve the regional constraint.
            </p>
          </div>
          <div className={`p-6 rounded-3xl border ${isLight ? 'bg-ls-white border-ls-grey-dark/20' : 'bg-ls-navy/60 border-ls-white/10'}`}>
            <Gauge className="w-6 h-6 text-ls-red mb-3" aria-hidden="true" />
            <h3 className="font-bold text-base font-display">Evidence, Not Narrative</h3>
            <p className={`mt-2 text-xs leading-relaxed ${muted}`}>
              A venture advances on recorded ATC, velocity and correction data. Where no measurement
              exists, the gate does not pass.
            </p>
          </div>
        </div>
      </section>

      {/* 8. HONEST STATUS */}
      <section className={sectionBase}>
        <Reveal>
          <div className={`rounded-3xl p-6 sm:p-8 border max-w-4xl mx-auto ${
            isLight ? 'bg-ls-white border-ls-grey-dark/30' : 'bg-ls-navy border-ls-white/15'
          }`}>
            <span className="font-body text-[10px] font-black tracking-widest text-ls-red uppercase">
              HONEST STATUS
            </span>
            <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${muted}`}>
              The operating model and scorecard on this page are the studio blueprint. The
              AI-native organisation they describe runs in-house at LightSpeed Holdings; the studio
              itself has not yet spun out a venture, and no figure above is a reported result. Where
              a target is stated, it is a target.
            </p>
          </div>
        </Reveal>
      </section>

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/ai-company-builder', label: 'AI Company Builder' },
          { to: '/pharos', label: 'Pharos' },
          { to: '/use-cases', label: 'Use Cases' },
        ]}
      />

      <CtaBand
        theme={theme}
        title={CTAS.primary.label}
        text="If you are building an AI-native business in Malawi or the SADC region and want the shared stack rather than a bespoke rebuild, start with a conversation about the thesis and the first gate."
        ctaLabel={CTAS.primary.label}
        ctaTo={CTAS.primary.to}
        onRequestBriefing={onRequestBriefing}
      />
    </>
  );
};

export default VentureStudioPage;
