import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Compass, Shield, Zap } from 'lucide-react';
import { Icon3D } from './common';

interface DistinctCTAProps {
  theme?: 'light' | 'dark';
  title?: string;
  subtitle?: string;
  primaryActionText?: string;
  primaryActionHref?: string;
  secondaryActionText?: string;
  secondaryActionHref?: string;
}

export const DistinctCTA: React.FC<DistinctCTAProps> = ({
  title = "THE FUTURE OF BUSINESS IS BUILT, NOT PREDICTED.",
  subtitle = "Partner with LightSpeed Holdings Limited™ to design, govern, and scale your autonomous enterprise operating model.",
  primaryActionText = "ENGAGE LIGHTSPEED",
  primaryActionHref = "/contact",
  secondaryActionText = "EXPLORE WHAT WE DO",
  secondaryActionHref = "/what-we-do",
}) => {
  return (
    <section id="final-cta" className="relative py-28 px-6 lg:px-12 min-h-[520px] flex items-center overflow-hidden bg-[#070A40] border-t-2 border-b-2 border-ls-cyan">
      {/* Background Earth Horizon Sunrise Space Visual */}
      <div className="absolute inset-0 pointer-events-none select-none overflow-hidden z-0">
        <img
          src="/assets/aistudio/call_to_action_blank_background_ee1fa8f8.jpg"
          alt="LightSpeed Global Earth Horizon Call to Action Background"
          className="w-full h-full object-cover object-center transition-all duration-700 opacity-70 filter saturate-110 brightness-100"
          loading="lazy"
        />
        {/* Darker Atmospheric Scrim Overlay for maximum typography legibility */}
        <div className="absolute inset-0 bg-gradient-to-b from-[#070A40]/85 via-[#070A40]/70 to-[#070A40]/90" />
      </div>

      <div className="max-w-7xl mx-auto text-center relative z-20 space-y-8 sm:space-y-10 w-full">
        {/* Sharp Tag Badge */}
        <div className="inline-flex items-center gap-2.5 px-4 py-1.5 bg-[#070A40] border-2 border-ls-red text-[11px] font-black text-ls-red uppercase tracking-[0.2em] font-sans shadow-[2px_2px_0px_#E63946]">
          <Icon3D name="lightning" size="xs" /> ASPIRE. ACT. ACHIEVE.
        </div>

        <h2 className="text-4xl lg:text-6xl font-black tracking-tight text-white leading-tight font-sans max-w-5xl mx-auto drop-shadow-[0_4px_16px_rgba(7,10,64,0.95)]">
          {title}
        </h2>

        <p className="text-slate-100 text-lg sm:text-xl max-w-2xl mx-auto leading-relaxed font-sans font-medium drop-shadow-[0_2px_8px_rgba(7,10,64,0.95)]">
          {subtitle}
        </p>

        {/* High-Contrast Action Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-5 pt-4">
          <Link
            to={primaryActionHref}
            className="inline-flex items-center gap-3 px-10 py-4 font-black text-xs tracking-widest bg-ls-red hover:bg-white hover:text-ls-navy text-white border-2 border-ls-red hover:border-white shadow-[4px_4px_0px_#070A40] transition-all cursor-pointer active:translate-x-[1px] active:translate-y-[1px] uppercase font-sans"
          >
            <span>{primaryActionText}</span>
            <ArrowRight className="w-4 h-4" />
          </Link>

          <Link
            to={secondaryActionHref}
            className="inline-flex items-center gap-3 px-10 py-4 font-black text-xs tracking-widest bg-[#0A0E2A] hover:bg-ls-cyan text-white hover:text-ls-navy border-2 border-ls-cyan shadow-[0_0_15px_rgba(0,191,255,0.4),4px_4px_0px_#00BFFF] transition-all cursor-pointer active:translate-x-[1px] active:translate-y-[1px] uppercase font-sans backdrop-blur-md"
          >
            <span className="text-white group-hover:text-ls-navy tracking-widest drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] font-black">
              {secondaryActionText}
            </span>
          </Link>
        </div>

        {/* Sharp High-Legibility Telemetry Badges */}
        <div className="pt-10 flex flex-wrap items-center justify-center gap-8 text-[11px] font-bold text-white uppercase tracking-widest border-t border-white/20 font-mono">
          <span className="flex items-center gap-2.5 px-3.5 py-2 bg-[#070A40]/90 border border-white/20 shadow-md backdrop-blur-md">
            <Icon3D name="governance" size="xs" />
            Governed Autonomous Agents
          </span>
          <span className="flex items-center gap-2.5 px-3.5 py-2 bg-[#070A40]/90 border border-white/20 shadow-md backdrop-blur-md">
            <Icon3D name="compass" size="xs" />
            SADC & Global Reach
          </span>
          <span className="flex items-center gap-2.5 px-3.5 py-2 bg-[#070A40]/90 border border-white/20 shadow-md backdrop-blur-md">
            <Icon3D name="lightning" size="xs" />
            Intelligence Architecture
          </span>
        </div>

      </div>
    </section>
  );
};

export default DistinctCTA;
