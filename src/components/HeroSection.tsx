import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles } from 'lucide-react';
import { PillarNavigationCard } from './PillarNavigationCard';
import { StatCounter } from './StatCounter';

interface HeroSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
  activePillar: number;
  onSelectPillar: (idx: number) => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  theme,
  onRequestBriefing,
  activePillar,
  onSelectPillar
}) => {
  const isLight = theme === 'light';
  return (
    <section id="hero" className="relative min-h-[92vh] flex flex-col justify-center pt-28 pb-16 px-4 sm:px-8 max-w-7xl mx-auto w-full">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center relative z-10 w-full">

        {/* Left Column: Core Positioning Statement & Vision */}
        <div className="lg:col-span-7 xl:col-span-7 space-y-6 text-left">

          {/* Eyebrow Badge */}
          <div className={`inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border text-[11px] font-mono tracking-widest transition-all shadow-xs ${
            isLight
              ? 'bg-white border-slate-300 text-slate-900 shadow-ls-red/5'
              : 'bg-ls-navy border-ls-red/40 text-zinc-300 shadow-black/40'
          }`}>
            <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80 animate-pulse" />
            <span>MALAWI-ROOTED, SADC-FOCUSED, GLOBAL CAPABILITY</span>
          </div>

          {/* Main Headline */}
          <h1 className={`text-4xl sm:text-6xl md:text-7xl font-black tracking-tight font-display leading-[1.04] ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            BUILD THE
            <br />
            <span className={isLight
              ? 'text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-ls-cyan to-slate-900'
              : 'text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-ls-cyan to-ls-cyan'
            }>
              INTELLIGENT ENTERPRISE.
            </span>
          </h1>

          {/* Divider Accent Line */}
          <div className="flex items-center gap-2">
            <div className={`w-16 h-[2px] ${isLight ? 'bg-ls-red/80' : 'bg-ls-red'}`} />
            <div className="w-1.5 h-1.5 rounded-xs bg-ls-red shadow-sm shadow-ls-red" />
          </div>

          {/* Strategy → Build → Govern → Scale */}
          <div className="flex flex-wrap items-center gap-2 font-mono text-[11px] font-bold tracking-widest">
            {['STRATEGY', 'BUILD', 'GOVERN', 'SCALE'].map((step, i) => (
              <React.Fragment key={step}>
                {i > 0 && <span className={`text-ls-red ${isLight ? '' : ''}`} aria-hidden="true">→</span>}
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

          {/* Explicit Regional Proposition Statement */}
          <div className="space-y-3">
            <p className={`text-justify max-w-2xl text-base sm:text-lg font-bold leading-relaxed ${
              isLight ? 'text-slate-900' : 'text-zinc-100'
            }`}>
              <span className="text-ls-red font-extrabold">LightSpeed Holdings</span> builds and operates agentic AI systems from Malawi for organizations across SADC — 144 agents, 20 departments, five-tier human approval, every decision auditable.
            </p>
            <p className={`text-justify max-w-2xl text-xs sm:text-sm leading-relaxed ${
              isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'
            }`}>
              Strategy — Build — Govern — Scale. We prove the model in Malawi first with shipped work — websites, automation, reporting, and marketing — for the organizations that need them most.
            </p>
          </div>

          {/* 3 Advantage Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 max-w-2xl">
            <div className={`p-3.5 rounded-2xl border transition-all ${
              isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/80 border-slate-800'
            }`}>
              <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-ls-red mb-1 font-mono">
                <span className="w-1.5 h-1.5 rounded-full bg-ls-red" />
                Local Fluency
              </div>
              <p className={`text-justify text-[11px] leading-snug ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                We know Malawi's institutions, business realities, infrastructure, and talent pool from the inside.
              </p>
            </div>

            <div className={`p-3.5 rounded-2xl border transition-all ${
              isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/80 border-slate-800'
            }`}>
              <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-ls-red mb-1 font-mono">
                <span className="w-1.5 h-1.5 rounded-full bg-ls-red" />
                Regional SADC
              </div>
              <p className={`text-justify text-[11px] leading-snug ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                Our systems account for SADC corridor dynamics, trade patterns, and national regulatory differences.
              </p>
            </div>

            <div className={`p-3.5 rounded-2xl border transition-all ${
              isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/80 border-slate-800'
            }`}>
              <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-ls-red mb-1 font-mono">
                <span className="w-1.5 h-1.5 rounded-full bg-ls-red" />
                Global Standards
              </div>
              <p className={`text-justify text-[11px] leading-snug ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                Our engineering, security, and design quality stand alongside top international firms.
              </p>
            </div>
          </div>

          {/* Primary Action Buttons */}
          <div className="flex flex-wrap items-center gap-3 pt-2">
            <Link
              to="/contact"
              className="group inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest bg-ls-red text-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer"
            >
              <div className="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center transition-transform group-hover:translate-x-0.5">
                <ArrowRight className="w-3 h-3" />
              </div>
              <span>Start a Conversation</span>
            </Link>

            <Link
              to="/ai-company-builder"
              className={`px-6 py-3.5 rounded-full font-bold text-xs tracking-widest border transition-all shadow-xs flex items-center gap-2 cursor-pointer ${
                isLight
                  ? 'bg-slate-900 hover:bg-slate-800 text-white border-slate-900'
                  : 'bg-ls-red hover:bg-ls-red text-white border-ls-red'
              }`}
            >
              <span>Explore AI Company Builder</span>
            </Link>

            <Link
              to="/technology"
              className={`px-5 py-3.5 rounded-full font-bold text-xs tracking-widest border backdrop-blur-xl transition-all shadow-xs flex items-center gap-2 cursor-pointer ${
                isLight
                  ? 'bg-white hover:bg-slate-50 text-slate-900 border-slate-300 hover:border-ls-red'
                  : 'bg-zinc-900/80 hover:bg-zinc-800 text-zinc-300 hover:text-white border-white/15'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-ls-red" />
              <span>How It Works</span>
            </Link>
          </div>

          {/* Metric Strip */}
          <div className={`pt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 border-t max-w-2xl ${
            isLight ? 'border-slate-200' : 'border-white/15'
          }`}>
            <div>
              <span className={`text-[11px] font-mono font-bold block ${'text-zinc-500'}`}>Agent Fleet</span>
              <span className="text-sm font-bold font-mono text-ls-red">
                <StatCounter to={144} format="comma" /> Configurations
              </span>
            </div>
            <div>
              <span className={`text-[11px] font-mono font-bold block ${'text-zinc-500'}`}>Regression Tests</span>
              <span className="text-sm font-bold font-mono text-ls-cyan">
                <StatCounter to={2373} format="comma" /> Passing
              </span>
            </div>
            <div>
              <span className={`text-[11px] font-mono font-bold block ${'text-zinc-500'}`}>Operating Departments</span>
              <span className={`text-sm font-bold font-mono ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                <StatCounter to={20} /> Live
              </span>
            </div>
            <div>
              <span className={`text-[11px] font-mono font-bold block ${'text-zinc-500'}`}>Audit Coverage</span>
              <span className={`text-sm font-bold font-mono ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                <StatCounter to={100} suffix="%" /> Auditable
              </span>
            </div>
          </div>

        </div>

        {/* Right Column: Audio/Hardware-Grade 4-Pillars Architectural Chassis Card */}
        <div className="lg:col-span-5 xl:col-span-5 flex justify-end">
          <PillarNavigationCard
            theme={theme}
            onRequestBriefing={onRequestBriefing}
            activePillar={activePillar}
            onSelectPillar={onSelectPillar}
          />
        </div>

      </div>
    </section>
  );
};
