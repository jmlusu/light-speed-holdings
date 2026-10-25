import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowDown, ArrowRight, Sparkles } from 'lucide-react';
import { homeImmersiveCopy } from '../data/homeImmersiveCopy';
import { liveTestCount } from '../data/metrics';
import { CTAS } from '../data/ctas';
import { capabilityTitles } from '../data/capabilities';
import { ScrimPanel } from './home/ScrimPanel';

interface HeroSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

const HERO_CHIPS = [...capabilityTitles];

const HERO_CARDS = [
  {
    title: 'Local Fluency',
    body: 'We know Malawi\'s institutions, business realities, infrastructure, and talent pool from the inside.',
  },
  {
    title: 'Regional Africa',
    body: 'Our systems account for African corridor dynamics, trade patterns, and national regulatory differences.',
  },
  {
    title: 'Global Standards',
    body: 'Our engineering, security, and design quality stand alongside top international firms.',
  },
];

/**
 * Hero as the stage's DOM layer: immersive copy on the left over the WebGL
 * scene, a blurred claims panel on the right for the dense preserved prose.
 */
export const HeroSection: React.FC<HeroSectionProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const copy = homeImmersiveCopy;

  return (
    <section id="hero" className="relative min-h-[92vh] flex flex-col justify-center pt-32 sm:pt-36 pb-20 sm:pb-24 px-4 sm:px-8 lg:px-10 max-w-7xl mx-auto w-full">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-center relative z-10 w-full">

        {/* Left - immersive layer over the stage */}
        <div className="lg:col-span-7 space-y-7 sm:space-y-8 text-left">
          <span className={`block font-body text-[11px] font-bold tracking-widest ${isLight ? 'text-ls-grey-dark' : 'text-ls-cyan/90 font-semibold'}`}>
            {copy.heroEyebrow}
          </span>

          <div className={`inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full border text-[11px] font-body tracking-widest transition-all shadow-xs ${isLight
              ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy shadow-ls-red/5'
              : 'bg-ls-navy/90 border-ls-white/15 text-ls-white/90 shadow-sm shadow-ls-navy/50'
            }`}>
            <span className="w-2 h-2 rounded-full bg-ls-red shadow-xs shadow-ls-red/80 animate-pulse" />
            <span>MALAWI-BASED, AFRICA-FOCUSED, GLOBAL CAPABILITY</span>
          </div>

          <h1 className={`text-4xl sm:text-6xl md:text-7xl lg:text-[4.75rem] font-black tracking-tight font-display leading-[1.02] ${isLight ? 'text-ls-navy' : 'text-ls-white'
            }`}>
            {copy.heroTitle}{' '}
            <span className={isLight
              ? 'text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-[#d82a38] to-ls-cyan font-black'
              : 'text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-[#ff4a58] to-ls-cyan font-black drop-shadow-[0_2px_14px_rgba(230,57,70,0.35)]'
            }>
              {copy.heroTitleAccent}
            </span>
          </h1>

          {/* Preserved headline, restyled as a strapline under the red rule */}
          <div className="flex items-center gap-3 pt-1">
            <div className={`w-16 h-[2px] shrink-0 ${isLight ? 'bg-ls-red/80' : 'bg-ls-red shadow-xs shadow-ls-red/50'}`} />
            <div className="w-1.5 h-1.5 shrink-0 rounded-xs bg-ls-red shadow-sm shadow-ls-red" aria-hidden="true" />
            <p className={`font-body text-[11px] font-bold tracking-widest uppercase ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
              THE AI-NATIVE COMPANY BUILDER.
            </p>
          </div>

          <p className={`text-left max-w-2xl text-base sm:text-lg md:text-xl font-semibold leading-relaxed tracking-normal ${isLight ? 'text-ls-navy/90' : 'text-ls-white/95'
            }`}>
            {copy.heroLead}
          </p>

          <div className="flex flex-wrap items-center gap-3.5 pt-3">
            <button
              type="button"
              onClick={() => onRequestBriefing(copy.heroCta)}
              className="ripple-on group inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest bg-ls-red hover:bg-[#d62837] text-ls-white shadow-lg shadow-ls-red/30 hover:shadow-ls-red/50 transition-all cursor-pointer active:scale-[0.98]"
            >
              <div className="w-5 h-5 rounded-full bg-ls-white/20 flex items-center justify-center transition-transform group-hover:translate-x-0.5">
                <ArrowRight className="w-3 h-3" aria-hidden="true" />
              </div>
              <span>{copy.heroCta}</span>
            </button>

            <Link
              to={CTAS.assessment.to}
              className={`group inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest border transition-all cursor-pointer active:scale-[0.98] ${isLight
                  ? 'border-ls-red text-ls-red bg-transparent hover:bg-ls-red/10 shadow-xs'
                  : 'border-ls-cyan text-ls-cyan bg-transparent hover:bg-ls-cyan/10 hover:border-ls-cyan shadow-sm shadow-ls-cyan/20'
                }`}
            >
              <span>{CTAS.assessment.label}</span>
              <ArrowRight className="w-3 h-3 transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
            </Link>

            <Link
              to="/ai-company-builder"
              className={`px-6 py-3.5 rounded-full font-bold text-xs tracking-widest border transition-all shadow-xs flex items-center gap-2 cursor-pointer active:scale-[0.98] ${isLight
                  ? 'bg-ls-navy hover:bg-ls-navy/90 text-ls-white border-ls-navy'
                  : 'bg-ls-navy/90 hover:bg-ls-navy text-ls-white border-ls-white/25 hover:border-ls-cyan/50'
                }`}
            >
              <span>Explore AI Company Builder</span>
            </Link>

            <Link
              to="/what-we-do"
              className={`px-5 py-3.5 rounded-full font-bold text-xs tracking-widest border backdrop-blur-xl transition-all shadow-xs flex items-center gap-2 cursor-pointer active:scale-[0.98] ${isLight
                  ? 'bg-ls-white hover:bg-ls-grey-light text-ls-navy border-ls-grey-dark/40 hover:border-ls-red'
                  : 'bg-ls-navy/60 hover:bg-ls-navy text-ls-grey-light-text hover:text-ls-white border-ls-white/15 hover:border-ls-white/30'
                }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-ls-red" aria-hidden="true" />
              <span>How It Works</span>
            </Link>
          </div>

          <div className={`pt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 border-t max-w-2xl ${isLight ? 'border-ls-grey-dark' : 'border-ls-white/15'
            }`}>
            <div>
              <span className={`text-[11px] font-body font-bold block ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Agent Fleet</span>
              <span className="text-sm font-bold font-body text-ls-red">90 Configurations</span>
            </div>
            <div>
              <span className={`text-[11px] font-body font-bold block ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Regression Tests</span>
              <span className={`text-sm font-bold font-body ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}>{liveTestCount.toLocaleString('en-US')} tests collected</span>
            </div>
            <div>
              <span className={`text-[11px] font-body font-bold block ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Operating Departments</span>
              <span className={`text-sm font-bold font-body ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>20 Live</span>
            </div>
            <div>
              <span className={`text-[11px] font-body font-bold block ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Audit Coverage</span>
              <span className={`text-sm font-bold font-body ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>100% Auditable</span>
            </div>
          </div>

          <div className="pt-4">
            <a
              href="#haomtgv"
              className={`group inline-flex items-center gap-2 font-body text-[11px] font-bold tracking-widest transition-colors hover:text-ls-red ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}
            >
              <span className="sr-only">Scroll to chapter 01. </span>
              <span>{copy.scrimHint}</span>
              <ArrowDown className="w-3.5 h-3.5 transition-transform group-hover:translate-y-0.5" aria-hidden="true" />
            </a>
          </div>
        </div>

        {/* Right - preserved claims panel over the stage */}
        <div className="lg:col-span-5">
          <ScrimPanel theme={theme} blur className="space-y-5">
            <div className="space-y-3">
              <p className={`text-justify text-base sm:text-lg font-bold leading-relaxed ${isLight ? 'text-ls-navy' : 'text-ls-white'
                }`}>
                <span className="text-ls-red font-extrabold">LightSpeed Holdings</span> builds AI-native companies: 90 operating roles (89 AI agents + 1 Human CEO), 20 departments, five-tier human approval, every decision auditable.
              </p>
              <p className={`text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-navy font-medium' : 'text-ls-grey-light-text'
                }`}>
                Strategy. Build. Govern. Research & Policy. We build AI-native companies with shipped work: websites, automation, reporting, and marketing for the organizations that need them most.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-2 font-body text-[11px] font-bold tracking-widest uppercase">
              {HERO_CHIPS.map((step, i) => (
                <React.Fragment key={step}>
                  {i > 0 && <span className="text-ls-red" aria-hidden="true">→</span>}
                  <span className={`px-2.5 py-1 rounded-full border ${i % 2 === 0
                      ? 'border-ls-red/40 bg-ls-red/10 text-ls-red'
                      : `border-ls-cyan/40 bg-ls-cyan/10 ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`
                    }`}>
                    {step}
                  </span>
                </React.Fragment>
              ))}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-1 gap-3">
              {HERO_CARDS.map((card) => (
                <div key={card.title} className={`p-3.5 rounded-2xl border transition-all ${isLight ? 'bg-ls-white border-ls-grey-dark shadow-xs' : 'bg-ls-navy/80 border-ls-white'
                  }`}>
                  <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-ls-red mb-1 font-body">
                    <span className="w-1.5 h-1.5 rounded-full bg-ls-red" aria-hidden="true" />
                    {card.title}
                  </div>
                  <p className={`text-justify text-[11px] leading-snug ${isLight ? 'text-ls-navy font-medium' : 'text-ls-grey-light-text'}`}>
                    {card.body}
                  </p>
                </div>
              ))}
            </div>
          </ScrimPanel>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
