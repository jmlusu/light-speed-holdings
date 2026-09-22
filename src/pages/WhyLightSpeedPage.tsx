import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { whyLightSpeed, TONE_STYLES } from '../data/siteContent';

interface WhyLightSpeedPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /why-lightspeed — the "why us" page that replaces generic marketing claims
 * with honest, evidence-backed differentiators. Each item carries its
 * honesty status badge so visitors can see exactly what is proven vs.
 * in development.
 */
export const WhyLightSpeedPage: React.FC<WhyLightSpeedPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      {/* 1. EXECUTIVE OUTCOME */}
      <PageIntro
        theme={theme}
        eyebrow="WHY LIGHTSPEED"
        title="Why Organizations Engage LightSpeed"
        lead={`We don't use generic claims like "innovative" or "world-class" — those words mean nothing without proof. Instead, we show how LightSpeed works differently: strategy and technology in one conversation, an AI-native operating model that runs on our own platform, and every engagement measured against outcomes, not activities.`}
      />

      {/* 2. THE WHY LIGHTSPEED CARDS */}
      <section
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="HOW WE WORK DIFFERENTLY"
          title="Eight Reasons Organizations Choose LightSpeed"
          lead="Every differentiator below carries its honesty status. We never blur what is proven from what is in development."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
          {whyLightSpeed.map((item, idx) => (
            <Reveal key={item.num} delay={idx * 0.06}>
              <div
                className={`rounded-3xl p-6 border flex flex-col h-full ${
                  isLight
                    ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <span
                    className="inline-flex items-center justify-center w-10 h-10 rounded-full font-black font-display text-sm"
                    style={{
                      backgroundColor: isLight ? 'rgba(230, 57, 70, 0.1)' : 'rgba(230, 57, 70, 0.15)',
                      color: isLight ? '#E63946' : '#E63946',
                    }}
                  >
                    {item.num}
                  </span>
                  <HonestyBadge label={item.proof} />
                </div>
                <h3 className="mt-4 text-base font-bold font-display tracking-tight leading-snug">
                  {item.title}
                </h3>
                <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {item.body}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* 3. HOW LIGHTSPEED WORKS DIFFERENTLY — CALLOUT */}
      <section
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
        <SectionHeading
          theme={theme}
          eyebrow="THE DIFFERENCE"
          title="How LightSpeed Works Differently"
          lead="We are not an IT consultancy that added AI. Our own operating model — 152 agents across 20 departments — is the proof that agentic systems work in production, under real constraints."
        />
        <div className="mt-8">
          <Reveal>
            <div
              className={`rounded-3xl p-8 sm:p-10 border shadow-lg ${
                isLight
                  ? 'bg-ls-white border-ls-cyan/30 shadow-md'
                  : 'bg-ls-navy/60 border-ls-cyan/20 shadow-xl'
              }`}
            >
              <div className="flex flex-col lg:flex-row lg:items-center gap-6">
                <div className="flex-1">
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full border border-ls-cyan/30 bg-ls-cyan/10 text-ls-cyan font-body text-[11px] tracking-widest font-bold">
                    PROVEN IN-HOUSE
                  </span>
                  <h3 className="mt-4 text-xl sm:text-2xl font-black tracking-tight font-display">
                    Our Platform Is Our Reference Architecture
                  </h3>
                  <p className={`mt-3 text-sm leading-relaxed ${
                    isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
                  }`}>
                    We ship working systems — websites, dashboards, agentic workflows, data pipelines — not just documents. LightSpeed Holdings runs its own 152-agent operation daily. The platform we deploy to clients is the same system that runs our business, with five-tier human approval gates, immutable SHA-256 audit trails, and cost tracking held to ≤10% of revenue.
                  </p>
                </div>
                <div className="lg:w-auto flex-shrink-0">
                  <Link
                    to="/technology"
                    className="inline-flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-cyan text-ls-navy shadow-lg shadow-ls-cyan/20 transition-all cursor-pointer hover:opacity-90 hover:scale-[1.02] active:scale-[0.98]"
                  >
                    Explore Our Technology
                    <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
                  </Link>
                </div>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* 4. WE AVOID GENERIC CLAIMS */}
      <section
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-12 border-t ${
          isLight ? 'border-ls-grey-dark/30' : 'border-ls-white/10'
        }`}
      >
        <div className="max-w-3xl mx-auto">
          <Reveal>
            <div className="text-center space-y-6">
              <span className="text-xs font-body font-bold tracking-widest text-ls-red uppercase">
                OUR COMMITMENT
              </span>
              <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
                isLight ? 'text-ls-navy' : 'text-ls-white'
              }`}>
                We Avoid Generic Claims
              </h2>
              <p className={`text-sm sm:text-base leading-relaxed ${
                isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
              }`}>
                The AI industry is flooded with vaporware and hype. Competitors cite dramatic ROI percentages from unverified tests, present cherry-picked demos as repeatable solutions, and blur future roadmap fantasies with currently fieldable software.
              </p>
              <p className={`text-sm sm:text-base leading-relaxed ${
                isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
              }`}>
                LightSpeed takes the opposite approach. Every claim on this site is classified by honesty tier — <span className="text-ls-cyan font-bold">Proven</span>, <span className="text-ls-red font-bold">Pilot</span>, <span className="text-ls-grey-light-text font-bold">Fieldable</span>, or <span className="text-ls-grey-dark font-bold">Development</span>. Our own platform is the reference architecture we deploy to clients. The tests that gate our work are published. Benchmarks are dated and regenerated on every release.
              </p>
              <p className={`text-sm sm:text-base leading-relaxed ${
                isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
              }`}>
                We show how LightSpeed works differently — not with adjectives, but with evidence.
              </p>
            </div>
          </Reveal>
        </div>
      </section>

      {/* 5. CLEAR CTA */}
      <CtaBand
        theme={theme}
        title="See Proof Before You Commit"
        text="We will show you live architecture, the tests that gate our work, and the engagement records behind our claims — no slide deck required."
        ctaLabel="Start a Conversation"
        ctaTo="/contact"
      />
    </>
  );
};

export default WhyLightSpeedPage;
