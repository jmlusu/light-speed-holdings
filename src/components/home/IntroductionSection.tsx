import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { Icon3D, Icon3DName } from '../common';

interface IntroductionSectionProps {
  theme?: 'light' | 'dark';
}

export const IntroductionSection: React.FC<IntroductionSectionProps> = ({ theme = 'dark' }) => {
  const isLight = theme === 'light';

  const cards: Array<{
    id: string;
    title: string;
    description: string;
    icon3d: Icon3DName;
  }> = [
    {
      id: 'ai-native',
      title: 'AI-Native First',
      description: 'We design, build and operate with AI at the core, not as an add-on.',
      icon3d: 'intelligence',
    },
    {
      id: 'evidence',
      title: 'Evidence Over Claims',
      description: 'We share real results, transparent metrics and verifiable outcomes.',
      icon3d: 'compliance',
    },
    {
      id: 'governed',
      title: 'Governed by Design',
      description: 'Security, ethics and accountability are built in from day one.',
      icon3d: 'governance',
    },
    {
      id: 'african-intelligence',
      title: 'African Intelligence',
      description: 'We apply local insight and African contexts to create solutions that work here and beyond.',
      icon3d: 'location',
    },
  ];

  return (
    <section
      id="introduction"
      className={`py-16 md:py-24 px-6 lg:px-12 relative overflow-hidden transition-colors duration-300 ${
        isLight ? 'bg-[#F4F6F8] text-ls-navy' : 'bg-[#070A40] text-white'
      }`}
    >
      {/* Background Layer with Dynamic Gradient Overlay Film Layer */}
      <div className="absolute inset-0 z-0 pointer-events-none select-none overflow-hidden" aria-hidden="true">
        <img
          src="/assets/aistudio/lightspeed_malawi_map_rightside_292682fa.jpg"
          alt=""
          className={`w-full h-full object-cover object-center transition-all duration-700 ${
            isLight
              ? 'opacity-85 mix-blend-multiply filter contrast-[1.05]'
              : 'opacity-50 filter contrast-[1.25] brightness-[0.85] mix-blend-screen'
          }`}
        />
        {/* Dynamic Gradient Overlay Film Layer (Lightened for enhanced clarity) */}
        <div
          className={`absolute inset-0 transition-all duration-700 ${
            isLight
              ? 'bg-gradient-to-r from-[#F4F6F8]/65 via-[#F4F6F8]/40 to-[#F4F6F8]/50'
              : 'bg-gradient-to-r from-[#070A40]/70 via-[#070A40]/50 to-[#070A40]/65'
          }`}
        />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 items-center">

          {/* Left Column: Heading, Eyebrow, Subtext, Link */}
          <div className="lg:col-span-5 flex flex-col justify-center">

            {/* Eyebrow with red indicator line */}
            <div className="flex items-center gap-2 mb-4">
              <span className="w-5 h-[2.5px] bg-ls-red rounded-full inline-block shrink-0" aria-hidden="true" />
              <span className={`text-xs font-mono font-bold tracking-widest uppercase ${
                isLight ? 'text-slate-600' : 'text-slate-300'
              }`}>
                INTRODUCTION
              </span>
            </div>

            {/* Main Title */}
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold leading-[1.12] tracking-tight font-display mb-6">
              <span className={isLight ? 'text-[#070A40]' : 'text-white'}>
                Human Direction.
              </span>
              <br />
              <span className={isLight ? 'text-[#070A40]' : 'text-white'}>
                Intelligent Execution.
              </span>
              <br />
              <span className="text-ls-cyan">
                Measurable Value.
              </span>
            </h2>

            {/* Subtext Paragraph */}
            <p className={`text-base sm:text-lg leading-relaxed mb-8 max-w-xl ${
              isLight ? 'text-slate-700' : 'text-slate-200'
            }`}>
              LightSpeed Holdings Limited builds AI-native companies and solutions that solve real problems, create lasting value and help Africa compete and prosper in the digital economy.
            </p>

            {/* Mission CTA Link */}
            <div>
              <Link
                to="/about"
                className={`inline-flex items-center gap-2 sm:gap-3 text-sm sm:text-base font-bold transition-all duration-200 group ${
                  isLight
                    ? 'text-[#070A40] hover:text-ls-red'
                    : 'text-white hover:text-ls-cyan'
                }`}
              >
                <span>Read the Mission...</span>
                <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
                <span className={`text-xs font-mono font-medium px-2 py-0.5 rounded border ${
                  isLight
                    ? 'bg-slate-200/90 text-slate-700 border-slate-300'
                    : 'bg-white/10 text-slate-300 border-white/15'
                }`}>
                  /about
                </span>
              </Link>
            </div>

          </div>

          {/* Right Column: 2x2 Feature Cards Grid */}
          <div className="lg:col-span-7">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-5">
              {cards.map((card) => {
                return (
                  <div
                    key={card.id}
                    className={`p-6 sm:p-7 rounded-2xl border transition-all duration-300 flex flex-col justify-between ${
                      isLight
                        ? 'bg-white/95 backdrop-blur-md border-slate-200/80 shadow-[0_4px_20px_rgba(7,10,64,0.06)] hover:shadow-[0_10px_35px_rgba(7,10,64,0.12)] hover:border-slate-300'
                        : 'bg-[#0D1220]/90 backdrop-blur-md border-white/10 shadow-lg hover:border-white/20 hover:bg-[#111728]/95'
                    }`}
                  >
                    <div>
                      {/* 3D Glass & Gold Icon Container */}
                      <div className="mb-5 flex items-center shrink-0">
                        <Icon3D name={card.icon3d} size="md" isInteractive />
                      </div>

                      {/* Card Title */}
                      <h3 className={`text-lg sm:text-xl font-bold font-display mb-2 tracking-tight ${
                        isLight ? 'text-[#070A40]' : 'text-white'
                      }`}>
                        {card.title}
                      </h3>

                      {/* Card Description */}
                      <p className={`text-xs sm:text-sm leading-relaxed ${
                        isLight ? 'text-slate-600' : 'text-slate-300'
                      }`}>
                        {card.description}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};

export default IntroductionSection;
