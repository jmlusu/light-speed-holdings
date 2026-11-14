import React from 'react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { Icon3D, Icon3DName } from '../common';

interface FormatCard {
  id: string;
  title: string;
  subtitle: string;
  icon3d: Icon3DName;
  to: string;
}

const PHAROS_FORMATS: FormatCard[] = [
  {
    id: 'briefs',
    title: 'Briefs',
    subtitle: 'Concise executive summaries connecting research to real-world use cases.',
    icon3d: 'documents',
    to: '/insights/open-source-cost-architecture',
  },
  {
    id: 'field-notes',
    title: 'Field Notes',
    subtitle: 'First-hand operational observations and field lessons from live deployments.',
    icon3d: 'notebook',
    to: '/insights/inside-a-90-agent-company',
  },
  {
    id: 'research-notes',
    title: 'Research Notes',
    subtitle: 'Technical deep-dives and empirical benchmarks on multi-agent execution.',
    icon3d: 'microscope',
    to: '/insights/five-tier-approval-matrix',
  },
  {
    id: 'policy-briefs',
    title: 'Policy Briefs',
    subtitle: 'Sovereign AI governance, compliance, and policy frameworks across SADC.',
    icon3d: 'policy-shield',
    to: '/insights/sadc-ai-opportunity',
  },
  {
    id: 'system-maps',
    title: 'System Maps',
    subtitle: 'Architectural blueprints and visual topology maps of agentic workflows.',
    icon3d: 'system-map',
    to: '/insights',
  },
  {
    id: 'data-stories',
    title: 'Data Stories',
    subtitle: 'Quantitative metrics on cycle-time compression and operational performance.',
    icon3d: 'chart',
    to: '/insights',
  },
  {
    id: 'ai-economics',
    title: 'AI-Economics Analyses',
    subtitle: 'OpEx reduction models, ROI frameworks, and AI pricing dynamics.',
    icon3d: 'finance',
    to: '/insights/dual-economy-ai-pricing',
  },
  {
    id: 'africa-watch',
    title: 'Africa Watch Regional Monitors',
    subtitle: 'Market intelligence and regional policy monitoring across Malawi & SADC.',
    icon3d: 'africa-map',
    to: '/insights/sadc-ai-opportunity',
  },
];

interface InsightsSectionProps {
  theme: 'light' | 'dark';
}

/** Chapter 06 - Pharos Thought-Leadership Engine & 8 Monthly Formats */
export const InsightsSection: React.FC<InsightsSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <section
      id="insights"
      aria-label="Pharos Thought-Leadership Engine"
      tabIndex={-1}
      className={`relative w-full py-[100px] px-6 lg:px-12 scroll-mt-28 overflow-hidden transition-colors duration-300 ${
        isLight ? 'bg-[#F2F2F2] text-ls-navy' : 'bg-[#1A1D21] text-white'
      }`}
    >
      {/* Background Pharos Lighthouse & Africa Network Image */}
      <div className="absolute inset-0 pointer-events-none select-none overflow-hidden z-0">
        <img
          src="/assets/aistudio/Pharos2_85555724.jpg"
          alt="Pharos Thought-Leadership Lighthouse Background"
          className="w-full h-full object-cover object-center transition-all duration-700 opacity-65 dark:opacity-75 filter saturate-110 brightness-100"
          loading="lazy"
        />
        {/* Clear Atmospheric Scrim Overlay for optimal contrast & typography clarity */}
        <div
          className={`absolute inset-0 transition-colors duration-500 ${
            isLight
              ? 'bg-gradient-to-b from-[#F2F2F2]/75 via-[#F2F2F2]/45 to-[#F2F2F2]/80'
              : 'bg-gradient-to-b from-[#1A1D21]/80 via-[#1A1D21]/55 to-[#1A1D21]/85'
          }`}
        />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto w-full">
        <SectionHeading
          theme={theme}
          eyebrow="THOUGHT-LEADERSHIP ENGINE"
          title="Pharos – LightSpeed's Thought-Leadership Engine"
          lead="Pharos transforms LightSpeed's agentic-AI research, experiments and field observations into a steady stream of high-impact, evidence-led insights. Each month we publish policy briefs, whitepapers, system maps, data stories, AI-economics analyses and Africa Watch regional monitors that clearly link our findings to real-world use cases, solutions and sectors across Malawi, the SADC region and the broader African continent."
        />

      {/* OUR EIGHT MONTHLY FORMATS SECTION */}
      <div className="mt-12">
        <div className="flex items-center justify-between border-b pb-4 mb-8 border-white/10 dark:border-white/10 border-slate-300">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-ls-cyan shadow-[0_0_8px_#00BFFF]" />
            <h3 className={`text-xs font-mono font-bold tracking-[0.25em] uppercase ${
              isLight ? 'text-ls-navy' : 'text-ls-cyan'
            }`}>
              OUR EIGHT MONTHLY FORMATS
            </h3>
          </div>
          <span className={`text-xs font-mono hidden sm:block ${isLight ? 'text-slate-500' : 'text-slate-400'}`}>
            8 PUBLICATION CHANNELS
          </span>
        </div>

        {/* 8 Formats Cards Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          {PHAROS_FORMATS.map((format, idx) => (
            <Reveal key={format.id} delay={idx * 0.05}>
              <Link
                to={format.to}
                className={`group p-5 sm:p-6 rounded-2xl border transition-all duration-300 flex flex-col justify-between h-full block backdrop-blur-xl ${
                  isLight
                    ? 'bg-white/90 border-slate-200/90 text-ls-navy shadow-sm hover:border-ls-navy/40 hover:shadow-lg'
                    : 'bg-[#070A40]/80 border-white/10 text-white shadow-xl hover:border-ls-cyan/50 hover:shadow-[0_8px_24px_rgba(0,191,255,0.15)]'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className={`text-[10px] font-mono font-bold tracking-widest uppercase px-2 py-0.5 rounded ${
                      isLight ? 'bg-ls-navy/10 text-ls-navy' : 'bg-ls-cyan/10 text-ls-cyan'
                    }`}>
                      0{idx + 1}
                    </span>
                    <Icon3D name={format.icon3d} size="md" isInteractive />
                  </div>

                  <h4 className={`text-base font-bold font-display tracking-tight mb-2 group-hover:text-ls-cyan transition-colors ${
                    isLight ? 'text-ls-navy group-hover:text-ls-red' : 'text-white'
                  }`}>
                    {format.title}
                  </h4>

                  <p className={`text-xs leading-relaxed ${
                    isLight ? 'text-slate-600' : 'text-slate-300'
                  }`}>
                    {format.subtitle}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-white/10 dark:border-white/10 border-slate-200 flex items-center justify-between text-[11px] font-mono font-bold">
                  <span className={isLight ? 'text-ls-red' : 'text-ls-cyan'}>EXPLORE</span>
                  <span className="transform group-hover:translate-x-1 transition-transform">→</span>
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
      </div>

    </div>
  </section>
  );
};

export default InsightsSection;
