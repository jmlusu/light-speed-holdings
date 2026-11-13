import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';

interface AboutSectionProps {
  theme: 'light' | 'dark';
}

const VALUES = [
  {
    title: 'AI-Native First',
    description: 'We build AI-native companies where constraints are real, scaling from strategy to governed execution.',
  },
  {
    title: 'Evidence Over Claims',
    description: 'Every statement is classified: Proven, Fieldable, or In development. Zero fabricated client logos or metrics.',
  },
  {
    title: 'Governed by Design',
    description: 'Five-tier human approval matrices, append-only audit trails, and data compliance gates are core architecture.',
  },
  {
    title: 'African Intelligence',
    description: 'Pharos turns our engineering into public intellectual work: SADC governance frameworks and regional strategy.',
  },
];

export const AboutSection: React.FC<AboutSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <section
      id="about"
      aria-label="About LightSpeed"
      tabIndex={-1}
      className={`relative w-full py-[100px] px-6 lg:px-12 scroll-mt-28 overflow-hidden transition-colors duration-300 ${
        isLight ? 'bg-[#F7F8F9] text-ls-navy' : 'bg-[#121518] text-white'
      }`}
    >
      {/* Background Horizon & African Continent Network Visual */}
      <div className="absolute inset-0 pointer-events-none select-none overflow-hidden z-0">
        <img
          src="/assets/aistudio/who_we_are_background_df66900f.jpg"
          alt="Who We Are - LightSpeed Global & African Network Visual"
          className="w-full h-full object-cover object-center transition-all duration-700 opacity-65 dark:opacity-75 filter saturate-110 brightness-100"
          loading="lazy"
        />
        {/* Atmospheric Scrim Overlay for optimal contrast & typography clarity */}
        <div
          className={`absolute inset-0 transition-colors duration-500 ${
            isLight
              ? 'bg-gradient-to-b from-[#F7F8F9]/75 via-[#F7F8F9]/45 to-[#F7F8F9]/80'
              : 'bg-gradient-to-b from-[#121518]/80 via-[#121518]/55 to-[#121518]/85'
          }`}
        />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto w-full">
        <SectionHeading
          theme={theme}
          eyebrow="WHO WE ARE"
          title="ASPIRE. ACT. ACHIEVE."
          lead="LightSpeed Holdings Limited™ is an AI-native strategy, venture-building, and technology organization transforming human intent into governed, intelligent, and executable business operations."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
          {VALUES.map((val, idx) => (
            <Reveal key={val.title} delay={idx * 0.08}>
              <div className={`rounded-2xl p-6 h-full border text-left backdrop-blur-xl transition-all duration-300 ${
                isLight
                  ? 'bg-white/85 border-slate-200/90 shadow-md hover:border-slate-300 hover:shadow-lg'
                  : 'bg-[#070A40]/75 border-white/10 shadow-xl hover:border-white/20'
              }`}>
                <span className="font-mono text-xs font-bold tracking-widest text-ls-red uppercase block mb-2">{val.title}</span>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
                  {val.description}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
        <div className={`mt-12 pt-8 border-t ${isLight ? 'border-slate-300/60' : 'border-white/10'}`}>
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
            <div className="text-left">
              <h3 className={`font-display font-bold text-lg sm:text-xl tracking-tight ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                Discover Our Operating Principles & Governance
              </h3>
              <p className={`mt-1 text-xs sm:text-sm ${isLight ? 'text-slate-600' : 'text-slate-400'}`}>
                Explore our mission, executive leadership, public agent registry, and commitment to transparent AI governance.
              </p>
            </div>
            <Link
              to="/about"
              className="ripple-on inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white transition-all cursor-pointer hover:bg-ls-red/90 shrink-0 shadow-md"
            >
              <span>LEARN ABOUT LIGHTSPEED</span>
              <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
