import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { homeImmersiveCopy } from '../data/homeImmersiveCopy';

interface HeroSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

/**
 * Hero as the stage's DOM layer: immersive copy on the left over the WebGL
 * scene, a blurred claims panel on the right for the dense preserved prose.
 */
export const HeroSection: React.FC<HeroSectionProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const copy = homeImmersiveCopy;

  const bgImage = isLight
    ? '/src/assets/images/hero_cinematic_landscape_day.jpg'
    : '/src/assets/images/hero_cinematic_landscape_night_1793514971805.jpg';

  const logoSrc = isLight
    ? '/brand/logo/logo-light-bg.svg'
    : '/brand/logo/logo-dark-bg.svg';

  return (
    <section
      id="hero"
      className={`relative min-h-screen flex flex-col justify-center pt-32 sm:pt-36 pb-20 sm:pb-24 px-6 lg:px-12 w-full overflow-hidden group transition-colors duration-500 ${
        isLight ? 'bg-[#F2F4F8]' : 'bg-[#070A40]'
      }`}
    >
      {/* Cinematic Background Atmosphere */}
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none select-none">
        <img
          src={bgImage}
          alt="LightSpeed Cinematic Architecture Background"
          className="w-full h-full object-cover object-center opacity-75 dark:opacity-70 transition-all duration-[10000ms] ease-out group-hover:scale-105 border-none"
        />

        {/* Dynamic Atmospheric Overlays (Lightened for enhanced clarity) */}
        <div
          className={`absolute inset-0 z-10 transition-colors duration-500 ${
            isLight
              ? 'bg-gradient-to-r from-[#F2F4F8]/75 via-[#F2F4F8]/50 sm:via-[#F2F4F8]/35 to-[#F2F4F8]/10'
              : 'bg-gradient-to-r from-[#070A40]/75 via-[#070A40]/55 sm:via-[#070A40]/35 to-[#070A40]/15'
          }`}
        />
        <div
          className={`absolute inset-0 z-20 mix-blend-overlay ${
            isLight ? 'bg-white/5' : 'bg-black/10'
          }`}
        />

        {/* Animated Light Trails / Glowing Accents */}
        <div
          className={`absolute top-1/2 left-0 w-full h-px blur-md animate-[pulse_8s_infinite] ${
            isLight
              ? 'bg-gradient-to-r from-transparent via-[#0090D6]/40 to-transparent'
              : 'bg-gradient-to-r from-transparent via-ls-cyan/30 to-transparent'
          }`}
        />
        <div className="absolute bottom-1/4 right-0 w-2/3 h-px bg-gradient-to-r from-transparent via-ls-red/25 to-transparent blur-lg animate-[pulse_12s_infinite_delay-2000]" />
      </div>

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-start relative z-30 w-full">
        {/* Left Column — Text from attached image */}
        <div className="lg:col-span-7 space-y-6 sm:space-y-8 text-left">
          {/* Eyebrow */}
          <div className="inline-flex items-center gap-2.5">
            <span className="w-2 h-2 rounded-full bg-ls-red shadow-xs shadow-ls-red animate-pulse" />
            <span className="font-body font-bold text-xs sm:text-sm tracking-[0.22em] uppercase text-ls-red">
              AI-NATIVE OPERATING MODEL
            </span>
          </div>

          {/* Headline */}
          <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-[4.2rem] xl:text-[4.65rem] font-black tracking-tight font-display leading-[1.08] animate-fade-in-up delay-100">
            <span
              className={`block transition-colors duration-300 ${
                isLight ? 'text-ls-navy' : 'text-white'
              }`}
            >
              The AI-native
            </span>
            <span
              className={`block ${
                isLight
                  ? 'text-[#0088CC] drop-shadow-[0_2px_18px_rgba(0,136,204,0.3)]'
                  : 'text-ls-cyan drop-shadow-[0_2px_24px_rgba(0,191,255,0.4)]'
              }`}
            >
              company builder
            </span>
            <span
              className={`block transition-colors duration-300 ${
                isLight ? 'text-ls-navy' : 'text-white'
              }`}
            >
              that ships.
            </span>
          </h1>

          {/* Subtitle Paragraph */}
          <p
            className={`text-left max-w-2xl text-base sm:text-lg md:text-xl font-normal leading-relaxed transition-colors duration-300 animate-fade-in-up delay-200 ${
              isLight ? 'text-slate-700 font-medium' : 'text-slate-200'
            }`}
          >
            Strategy. AI. Execution. Built for Africa and beyond.
            <br />
            LightSpeed Holdings builds and scales AI-native companies that turn bold ideas into real-world impact — starting in Malawi and expanding across the SADC region and Africa.
          </p>

          <div className="flex flex-wrap items-center gap-3.5 pt-2 animate-fade-in-up delay-500">
            <Link
              to="/contact"
              className="ripple-on group inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest bg-ls-red hover:bg-[#d62837] text-ls-white shadow-lg shadow-ls-red/30 hover:shadow-ls-red/50 transition-all cursor-pointer active:scale-[0.98]"
            >
              <div className="w-5 h-5 rounded-full bg-ls-white/20 flex items-center justify-center transition-transform group-hover:translate-x-0.5">
                <ArrowRight className="w-3 h-3" aria-hidden="true" />
              </div>
              <span>ENGAGE LIGHTSPEED</span>
            </Link>

            <Link
              to="/what-we-do"
              className={`px-6 py-3.5 rounded-full font-bold text-xs tracking-widest transition-all shadow-xs flex items-center gap-2 cursor-pointer active:scale-[0.98] ${
                isLight
                  ? 'bg-ls-navy hover:bg-[#0c125e] text-ls-white shadow-md'
                  : 'bg-ls-navy/90 hover:bg-ls-navy text-ls-white border border-white/10'
              }`}
            >
              <span className="text-[#00BFFF]">EXPLORE WHAT WE DO</span>
              <ArrowRight className="w-3 h-3 text-[#00BFFF]" aria-hidden="true" />
            </Link>
          </div>
        </div>

        {/* Right Column — Raised Logo aligned with "Intelligent Execution" */}
        <div className="lg:col-span-5 flex items-start justify-center lg:justify-end animate-fade-in-up delay-300 lg:pt-1 xl:pt-2">
          <div className="relative p-0 flex items-center justify-center">
            {/* Atmospheric ambient glow behind the logo */}
            <div
              className={`absolute w-72 h-72 sm:w-96 sm:h-96 rounded-full blur-3xl -z-10 pointer-events-none transition-colors duration-500 ${
                isLight ? 'bg-ls-cyan/20' : 'bg-ls-cyan/15'
              }`}
            />
            <img
              src={logoSrc}
              alt="LightSpeed Holdings Limited™ — ASPIRE. ACT. ACHIEVE."
              className={`w-64 sm:w-72 md:w-80 lg:w-[360px] xl:w-[410px] max-w-full h-auto object-contain transition-all duration-700 hover:scale-105 ${
                isLight
                  ? 'drop-shadow-[0_15px_30px_rgba(7,10,64,0.15)]'
                  : 'drop-shadow-[0_15px_40px_rgba(0,191,255,0.25)]'
              }`}
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
