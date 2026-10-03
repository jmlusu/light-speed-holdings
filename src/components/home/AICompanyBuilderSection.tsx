import React from 'react';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';

interface AICompanyBuilderSectionProps {
  theme: 'light' | 'dark';
}

const JOURNEY_STEPS = [
  {
    id: 'opportunity',
    num: '01',
    title: 'Opportunity',
    description: 'Identify high-value AI opportunities aligned with organizational strategy and readiness.',
  },
  {
    id: 'design',
    num: '02',
    title: 'Design',
    description: 'Architect the agentic system — agents, workflows, data flows, governance gates, and human decision points.',
  },
  {
    id: 'build',
    num: '03',
    title: 'Build',
    description: 'Develop and test the AI workforce in a governed sandbox with automated regression and approval gates.',
  },
  {
    id: 'deploy',
    num: '04',
    title: 'Deploy',
    description: 'Release to production with phased rollout, monitoring, and human-in-the-loop override capability.',
  },
  {
    id: 'govern',
    num: '05',
    title: 'Govern',
    description: 'Operate under five-tier human approval, immutable audit trails, and continuous compliance monitoring.',
  },
  {
    id: 'measure',
    num: '06',
    title: 'Measure',
    description: 'Track cost, quality, adoption, and impact — feed insights back into the strategy layer for continuous improvement.',
  },
];

const PRINCIPLES = [
  'Human-led',
  'AI-native',
  'Agentic',
  'Governed',
  'Data-informed',
  'Modular',
  'Measurable',
  'Progressive',
  'Secure',
  'Designed for practical adoption',
];

export const AICompanyBuilderSection: React.FC<AICompanyBuilderSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="ai-company-builder" label="AI Company Builder" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="AI COMPANY BUILDER"
        title="From Opportunity to Governed AI Workforce"
        lead="LightSpeed helps organizations move from strategy to a shipped, auditable AI operating model — not a prototype, not a pilot, but a governed system that runs on your infrastructure."
      />
      <div className="space-y-12">
        {/* Journey Steps */}
        <div>
          <h3 className={`font-body text-[10px] font-bold tracking-widest text-ls-red mb-6 ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
            THE TRANSFORMATION JOURNEY
          </h3>
          <div className="relative">
            <div className={`hidden lg:block absolute left-1/2 top-0 bottom-0 w-[2px] -translate-x-1/2 ${isLight ? 'bg-ls-grey-dark/30' : 'bg-ls-white/10'}`} aria-hidden="true" />
            <div className="space-y-10">
              {JOURNEY_STEPS.map((step, idx) => (
                <Reveal key={step.id} delay={idx * 0.06}>
                  <div className="relative lg:w-1/2 lg:pl-16 lg:pr-4">
                    <div className={`flex flex-col lg:flex-row items-start lg:items-center gap-4 ${idx % 2 === 1 ? 'lg:ml-auto lg:flex-row-reverse lg:pl-4 lg:pr-16' : ''}`}>
                      <div className={`flex-shrink-0 w-14 h-14 rounded-full border flex items-center justify-center text-xl font-black text-ls-red ${isLight ? 'bg-ls-white border-ls-grey-dark' : 'bg-ls-navy border-ls-white/15'}`} aria-hidden="true">
                        {step.num}
                      </div>
                      <div className={`flex-1 p-5 rounded-2xl border transition-all group ${
                        isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md group-hover:shadow-xl' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl group-hover:shadow-2xl'
                      }`}>
                        <h4 className="font-display font-bold text-base sm:text-lg tracking-tight mb-1">{step.title}</h4>
                        <p className={`text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>{step.description}</p>
                      </div>
                    </div>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </div>

        {/* Principles */}
        <div className="pt-4">
          <h3 className={`font-body text-[10px] font-bold tracking-widest text-ls-red mb-6 ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
            GOVERNING PRINCIPLES
          </h3>
          <div className="flex flex-wrap gap-2">
            {PRINCIPLES.map((principle) => (
              <span key={principle} className={`px-3 py-1.5 rounded-full border text-[10px] font-body font-bold tracking-wider ${isLight ? 'bg-ls-white border-ls-grey-dark text-ls-navy' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white'}`}>
                {principle}
              </span>
            ))}
          </div>
        </div>
      </div>
    </HomeSection>
  );
};

export default AICompanyBuilderSection;