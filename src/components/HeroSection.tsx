import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles } from 'lucide-react';
import { HeroMist } from './effects/HeroMist';

interface HeroSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  theme,
  onRequestBriefing,
}) => {
  const isLight = theme === 'light';
  return (
    <section id="hero" className="relative min-h-[92vh] flex flex-col justify-center pt-28 pb-16 px-4 sm:px-8 max-w-7xl mx-auto w-full">
      <HeroMist theme={theme} />
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center relative z-10 w-full">

        <div className="lg:col-span-7 xl:col-span-7 space-y-6 text-left">
          <div className={`inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border text-[11px] font-body tracking-widest transition-all shadow-xs ${
            isLight
              ? 'bg-ls-white border-ls-grey-dark text-ls-navy shadow-ls-red/5'
              : 'bg-ls-navy border-ls-red/40 text-ls-grey-light-text shadow-ls-navy/40'
          }`}>
            <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80" />
            <span>MALAWI-ROOTED, SADC-FOCUSED, GLOBAL CAPABILITY</span>
          </div>

          <h1 className={`text-4xl sm:text-6xl md:text-7xl font-black tracking-tight font-display leading-[1.04] ${
            isLight ? 'text-ls-navy' : 'text-ls-white'
          }`}>
            THE
            <br />
            <span className={isLight
              ? 'text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-ls-cyan to-ls-navy'
              : 'text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-ls-cyan to-ls-cyan'
            }>
              AI-NATIVE COMPANY BUILDER.
            </span>
          </h1>

          <div className="flex items-center gap-2">
            <div className={`w-16 h-[2px] ${isLight ? 'bg-ls-red/80' : 'bg-ls-red'}`} />
            <div className="w-1.5 h-1.5 rounded-xs bg-ls-red shadow-sm shadow-ls-red" />
          </div>

          <div className="flex flex-wrap items-center gap-2 font-body text-[11px] font-bold tracking-widest">
            {['STRATEGY', 'BUILD', 'GOVERN', 'RESEARCH & POLICY'].map((step, i) => (
              <React.Fragment key={step}>
                {i > 0 && <span className="text-ls-red" aria-hidden="true">→</span>}
                <span className={`px-2.5 py-1 rounded-full border ${
                  i % 2 === 0
                    ? 'border-ls-red/40 bg-ls-red/10 text-ls-red'
                    : 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan'
                }`}>
                  {step}
                </span>
              </React.Fragment>
            ))}
          </div>

          <div className="space-y-3">
            <p className={`text-justify max-w-2xl text-base sm:text-lg font-bold leading-relaxed ${
              isLight ? 'text-ls-navy' : 'text-ls-white'
            }`}>
              <span className="text-ls-red font-extrabold">LightSpeed Holdings</span> builds and operates agentic AI systems from Malawi for organizations across SADC — 90 agents, 20 departments, five-tier human approval, every decision auditable.
            </p>
            <p className={`text-justify max-w-2xl text-xs sm:text-sm leading-relaxed ${
              isLight ? 'text-ls-navy font-medium' : 'text-ls-grey-light-text'
            }`}>
              Strategy — Build — Govern — Research & Policy. We prove the model in Malawi first with shipped work — websites, automation, reporting, and marketing — for the organizations that need them most.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 max-w-2xl">
            <div className={`p-3.5 rounded-2xl border transition-all ${
              isLight ? 'bg-ls-white border-ls-grey-dark shadow-xs' : 'bg-ls-navy/80 border-ls-white'
            }`}>
              <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-ls-red mb-1 font-body">
                <span className="w-1.5 h-1.5 rounded-full bg-ls-red" />
                Local Fluency
              </div>
              <p className={`text-justify text-[11px] leading-snug ${isLight ? 'text-ls-navy font-medium' : 'text-ls-grey-light-text'}`}>
                We know Malawi's institutions, business realities, infrastructure, and talent pool from the inside.
              </p>
            </div>

            <div className={`p-3.5 rounded-2xl border transition-all ${
              isLight ? 'bg-ls-white border-ls-grey-dark shadow-xs' : 'bg-ls-navy/80 border-ls-white'
            }`}>
              <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-ls-red mb-1 font-body">
                <span className="w-1.5 h-1.5 rounded-full bg-ls-red" />
                Regional SADC
              </div>
              <p className={`text-justify text-[11px] leading-snug ${isLight ? 'text-ls-navy font-medium' : 'text-ls-grey-light-text'}`}>
                Our systems account for SADC corridor dynamics, trade patterns, and national regulatory differences.
              </p>
            </div>

            <div className={`p-3.5 rounded-2xl border transition-all ${
              isLight ? 'bg-ls-white border-ls-grey-dark shadow-xs' : 'bg-ls-navy/80 border-ls-white'
            }`}>
              <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-ls-red mb-1 font-body">
                <span className="w-1.5 h-1.5 rounded-full bg-ls-red" />
                Global Standards
              </div>
              <p className={`text-justify text-[11px] leading-snug ${isLight ? 'text-ls-navy font-medium' : 'text-ls-grey-light-text'}`}>
                Our engineering, security, and design quality stand alongside top international firms.
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <Link
              to="/contact"
              className="group inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer"
            >
              <div className="w-5 h-5 rounded-full bg-ls-white/20 flex items-center justify-center transition-transform group-hover:translate-x-0.5">
                <ArrowRight className="w-3 h-3" />
              </div>
              <span>Start a Conversation</span>
            </Link>

            <Link
              to="/ai-company-builder"
              className={`px-6 py-3.5 rounded-full font-bold text-xs tracking-widest border transition-all shadow-xs flex items-center gap-2 cursor-pointer ${
                isLight
                  ? 'bg-ls-navy hover:bg-ls-navy text-ls-white border-ls-white'
                  : 'bg-ls-red hover:bg-ls-red text-ls-white border-ls-red'
              }`}
            >
              <span>Explore AI Company Builder</span>
            </Link>

            <Link
              to="/what-we-do"
              className={`px-5 py-3.5 rounded-full font-bold text-xs tracking-widest border backdrop-blur-xl transition-all shadow-xs flex items-center gap-2 cursor-pointer ${
                isLight
                  ? 'bg-ls-white hover:bg-ls-grey-light text-ls-navy border-ls-grey-dark hover:border-ls-red'
                  : 'bg-ls-navy/80 hover:bg-ls-navy text-ls-grey-light-text hover:text-ls-white border-ls-white/15'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-ls-red" />
              <span>How It Works</span>
            </Link>
          </div>

          <div className={`pt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 border-t max-w-2xl ${
            isLight ? 'border-ls-grey-dark' : 'border-ls-white/15'
          }`}>
            <div>
              <span className={`text-[11px] font-body font-bold block ${'text-ls-grey-light-text'}`}>Agent Fleet</span>
              <span className="text-sm font-bold font-body text-ls-red">90 Configurations</span>
            </div>
            <div>
              <span className={`text-[11px] font-body font-bold block ${'text-ls-grey-light-text'}`}>Regression Tests</span>
              <span className="text-sm font-bold font-body text-ls-cyan">2,557 Passing</span>
            </div>
            <div>
              <span className={`text-[11px] font-body font-bold block ${'text-ls-grey-light-text'}`}>Operating Departments</span>
              <span className={`text-sm font-bold font-body ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>20 Live</span>
            </div>
            <div>
              <span className={`text-[11px] font-body font-bold block ${'text-ls-grey-light-text'}`}>Audit Coverage</span>
              <span className={`text-sm font-bold font-body ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>100% Auditable</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
