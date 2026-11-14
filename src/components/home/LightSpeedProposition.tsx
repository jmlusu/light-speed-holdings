import React from 'react';
import { SectionHeading } from '../site/SectionHeading';
import { Icon3D, Icon3DName } from '../common';

interface LightSpeedPropositionProps {
  theme?: 'light' | 'dark';
}

export const LightSpeedProposition: React.FC<LightSpeedPropositionProps> = ({ theme = 'dark' }) => {
  const isLight = theme === 'light';

  const dimensions: Array<{
    id: string;
    num: string;
    title: string;
    icon3d: Icon3DName;
    color: string;
    borderColor: string;
    bgColor: string;
    lead: string;
    details: string;
  }> = [
    {
      id: 'intelligence',
      num: '01',
      title: 'Connected Intelligence',
      icon3d: 'intelligence',
      color: 'text-ls-cyan',
      borderColor: 'border-ls-cyan/30',
      bgColor: isLight ? 'bg-ls-cyan/5' : 'bg-ls-cyan/10',
      lead: 'Context-aware models grounded in enterprise domain knowledge.',
      details: 'Rather than isolated chatbot widgets, LightSpeed connects intelligent models directly to structured knowledge bases, vector memory, and internal data streams.',
    },
    {
      id: 'orchestration',
      num: '02',
      title: 'Deterministic Orchestration',
      icon3d: 'orchestration',
      color: 'text-ls-red',
      borderColor: 'border-ls-red/30',
      bgColor: isLight ? 'bg-ls-red/5' : 'bg-ls-red/10',
      lead: 'Task decomposition and deterministic routing across specialized agents.',
      details: 'Complex business operations are broken down into discrete sub-tasks, routed to specialized agent roles, and monitored continuously to prevent hallucination or drift.',
    },
    {
      id: 'governance',
      num: '03',
      title: 'Bounded Governance',
      icon3d: 'governance',
      color: 'text-ls-navy',
      borderColor: isLight ? 'border-ls-navy/30' : 'border-white/20',
      bgColor: isLight ? 'bg-ls-navy/5' : 'bg-white/5',
      lead: 'Five-tier human approval matrices and immutable audit receipts.',
      details: 'No action touches production or external systems without passing bounded approval gates, contract checks, and append-only cryptographic logging.',
    },
  ];

  const bgImage = isLight
    ? '/assets/aistudio/ValuePropositionBackground_beecaad0.jpg'
    : '/assets/images/val_prop_bg_night_1793997847272.avif';

  return (
    <section id="proposition" className={`py-24 px-6 lg:px-12 relative overflow-hidden transition-colors duration-300 ${
      isLight ? 'bg-white text-ls-navy' : 'bg-[#070A40] text-white'
    }`}>
      {/* Background Cinematic Panoramic Visual */}
      <div className="absolute inset-0 pointer-events-none select-none overflow-hidden z-0">
        <img
          src={bgImage}
          alt="LightSpeed Value Proposition Architecture Horizon"
          className="w-full h-full object-cover object-center transition-all duration-700 opacity-65 dark:opacity-70 filter brightness-100"
          loading="lazy"
        />
        {/* Transparent film scrim overlay so the background is clearer while maintaining text legibility */}
        <div
          className={`absolute inset-0 transition-colors duration-500 ${
            isLight
              ? 'bg-gradient-to-b from-white/70 via-white/40 to-white/70'
              : 'bg-gradient-to-b from-[#070A40]/70 via-[#070A40]/45 to-[#070A40]/75'
          }`}
        />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <SectionHeading
          theme={theme}
          eyebrow="THE LIGHTSPEED PROPOSITION"
          title="Building Governed Operating Capability, Not Isolated Tools"
          lead="LightSpeed does not sell point-solution chatbots or experimental AI widgets. We design and scale integrated operating capabilities where intelligence, orchestration, and governance reinforce one another."
        />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          {dimensions.map((dim) => {
            return (
              <div
                key={dim.id}
                className={`p-8 rounded-2xl border transition-all duration-300 flex flex-col justify-between backdrop-blur-xl ${
                  isLight
                    ? 'bg-white/85 border-slate-200/90 shadow-lg hover:border-ls-navy/40 hover:shadow-xl'
                    : 'bg-[#070A40]/80 border-white/10 shadow-2xl hover:border-ls-cyan/50 hover:shadow-[0_8px_32px_rgba(0,191,255,0.15)]'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <span className={`text-xs font-mono font-bold tracking-widest ${dim.color}`}>
                      DIMENSION {dim.num}
                    </span>
                    <div className="flex items-center shrink-0">
                      <Icon3D name={dim.icon3d} size="md" isInteractive />
                    </div>
                  </div>

                  <h3 className={`text-xl font-black mb-3 font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                    {dim.title}
                  </h3>

                  <p className={`text-sm font-semibold mb-4 leading-snug ${isLight ? 'text-slate-800' : 'text-slate-200'}`}>
                    {dim.lead}
                  </p>

                  <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-slate-400'}`}>
                    {dim.details}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default LightSpeedProposition;
