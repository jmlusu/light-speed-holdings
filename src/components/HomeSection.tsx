import React, { useState } from 'react';
import { 
  Sparkles, 
  ArrowRight, 
  ShieldCheck, 
  Bot, 
  Database, 
  Workflow, 
  Building2, 
  Globe2, 
  Cpu, 
  CheckCircle2, 
  TrendingUp, 
  Compass, 
  ChevronRight, 
  Layers, 
  Terminal, 
  Activity, 
  Zap, 
  Radio, 
  PlayCircle,
  FileText,
  Lock,
  Landmark
} from 'lucide-react';
import { PharosWelcomeJourney } from './PharosWelcomeJourney';
import { HeroVideoFilm } from './HeroVideoFilm';
import { CentralProblemSolution } from './CentralProblemSolution';
import { HelpfulInfographics } from './HelpfulInfographics';
import { InteractiveTimelineMap } from './InteractiveTimelineMap';
import { OurStoryOrigin } from './OurStoryOrigin';
import { StakeholderEngagementHub } from './StakeholderEngagementHub';
import { 
  StatusLedPip 
} from './TactileHardwareElements';

interface HomeSectionProps {
  onNavigate: (route: string, param?: string) => void;
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const HomeSection: React.FC<HomeSectionProps> = ({
  onNavigate,
  onOpenContactModal,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';
  const [activeStoryChapter, setActiveStoryChapter] = useState<string>('all');

  const storyChapters = [
    { id: 'film', label: 'I. Hero Film', anchor: 'chapter-film' },
    { id: 'pharos', label: 'II. Pharos Journey', anchor: 'chapter-pharos' },
    { id: 'problem', label: 'III. Problem & Solution', anchor: 'chapter-problem' },
    { id: 'infographics', label: 'IV. Infographics', anchor: 'chapter-infographics' },
    { id: 'map', label: 'V. SADC Node Map', anchor: 'chapter-map' },
    { id: 'origin', label: 'VI. Our Story & Team', anchor: 'chapter-origin' },
    { id: 'builder', label: 'VII. Swarm Builder', anchor: 'chapter-builder' }
  ];

  const scrollToChapter = (anchorId: string) => {
    const el = document.getElementById(anchorId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <div className="space-y-24 font-sans max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      
      {/* =========================================================================
          STORYTELLING QUICK-NAVIGATION CHAPTER RIBBON
          ========================================================================= */}
      <div className={`p-2 rounded-2xl flex items-center justify-between overflow-x-auto gap-2 border transition-all sticky top-2 z-30 backdrop-blur-md ${
        isLight ? 'bg-slate-100/95 border-slate-300 shadow-sm' : 'bg-[#0d121f]/95 border-slate-800 shadow-lg'
      }`}>
        <div className="flex items-center gap-2 shrink-0 pl-2">
          <StatusLedPip status="emerald" isLight={isLight} />
          <span className="text-[10px] font-mono font-bold tracking-wider text-amber-500 uppercase hidden sm:inline">
            STORY CHAPTERS:
          </span>
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5">
          {storyChapters.map((ch) => (
            <button
              key={ch.id}
              onClick={() => scrollToChapter(ch.anchor)}
              className={`px-2.5 py-1 rounded-lg text-[11px] font-mono font-semibold whitespace-nowrap transition-all cursor-pointer ${
                isLight 
                  ? 'hover:bg-slate-200 text-slate-700 hover:text-slate-900' 
                  : 'hover:bg-zinc-800 text-zinc-300 hover:text-white'
              }`}
            >
              {ch.label}
            </button>
          ))}
        </div>

        <button
          onClick={() => onOpenContactModal('Executive Briefing Consultation')}
          className="neu-btn-amber px-3 py-1.5 rounded-xl text-[10px] font-mono font-bold uppercase tracking-wider shrink-0 cursor-pointer hidden md:flex items-center gap-1.5"
        >
          <span>Book Call</span>
          <ArrowRight className="w-3 h-3" />
        </button>
      </div>

      {/* =========================================================================
          HERO SECTION: TACTICAL FLIGHT-DECK HEADLINE
          ========================================================================= */}
      <section className="relative text-center overflow-hidden pt-2 pb-6">
        
        {/* Subtle Ambient Vignette / Hardware Backing */}
        <div className={`absolute top-0 left-1/2 -translate-x-1/2 w-[800px] max-w-full h-[360px] rounded-full filter blur-[140px] pointer-events-none -z-10 ${
          isLight ? 'bg-amber-400/10' : 'bg-amber-500/5'
        }`} />

        {/* Tactical Classification Badge */}
        <div className={`inline-flex items-center gap-2 sm:gap-3 px-4 py-2 rounded-full text-xs font-mono font-bold uppercase tracking-wider mb-6 transition-all select-none ${
          isLight ? 'neu-pill-light' : 'neu-pill-dark'
        }`}>
          <StatusLedPip status="emerald" isLight={isLight} />
          <span className={`text-[11px] font-mono tracking-widest ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
            AI-NATIVE OPERATOR &amp; PARTNER // LILONGWE COMMAND
          </span>
          <span className="hidden sm:inline text-zinc-500">•</span>
          <span className="hidden sm:inline text-[10px] text-amber-500 font-mono">
            SYS::VERIFIED 2026.4
          </span>
        </div>

        {/* Main Headline */}
        <h1 className={`text-2xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight font-display mb-6 leading-normal sm:leading-tight break-words ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          The <span className="inline-block pb-1.5 text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">AI-Native Operator &amp; Partner</span>
        </h1>

        <p className={`max-w-3xl mx-auto text-base sm:text-lg font-sans leading-relaxed mb-8 ${
          isLight ? 'text-slate-600' : 'text-zinc-400'
        }`}>
          Engineered for institutional rigor and fiduciary command. We architect sovereign AI operating models, autonomous sub-agent swarms, and high-velocity computational infrastructure for enterprises, governments, and financial networks across Malawi, SADC, and Africa.
        </p>

        {/* Action CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-4 mb-10">
          <button
            onClick={() => onNavigate('ai-company-builder')}
            className="neu-btn-amber px-8 py-4 rounded-2xl font-extrabold font-mono text-xs uppercase tracking-wider flex items-center gap-2.5 group cursor-pointer"
          >
            <span>Deploy AI Company Builder</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
          </button>

          <button
            onClick={() => onOpenContactModal('Request Executive Consultation')}
            className={`px-8 py-4 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider transition-all flex items-center gap-2 cursor-pointer ${
              isLight ? 'neu-btn-light text-slate-900' : 'neu-btn-dark text-zinc-200'
            }`}
          >
            <Compass className="w-3.5 h-3.5 text-amber-500" />
            <span>Book Consultation</span>
          </button>
        </div>
      </section>

      {/* =========================================================================
          CHAPTER I: HERO HOOK VIDEO & WELCOMING FILM
          ========================================================================= */}
      <section id="chapter-film" className="scroll-mt-6">
        <HeroVideoFilm
          theme={theme}
          onNavigate={onNavigate}
          onOpenContactModal={onOpenContactModal}
        />
      </section>

      {/* =========================================================================
          CHAPTER II: THE PHAROS WELCOMING JOURNEY
          ========================================================================= */}
      <section id="chapter-pharos" className="scroll-mt-6">
        <PharosWelcomeJourney
          theme={theme}
          onNavigate={onNavigate}
          onOpenContactModal={onOpenContactModal}
        />
      </section>

      {/* =========================================================================
          CHAPTER III: THE CENTRAL PROBLEM & SOVEREIGN SOLUTION
          ========================================================================= */}
      <section id="chapter-problem" className="scroll-mt-6">
        <CentralProblemSolution
          theme={theme}
          onNavigate={onNavigate}
          onOpenContactModal={onOpenContactModal}
        />
      </section>

      {/* =========================================================================
          CHAPTER IV: HELPFUL INFOGRAPHICS & PROCESS VISUALIZERS
          ========================================================================= */}
      <section id="chapter-infographics" className="scroll-mt-6">
        <HelpfulInfographics
          theme={theme}
          onNavigate={onNavigate}
          onOpenContactModal={onOpenContactModal}
        />
      </section>

      {/* =========================================================================
          CHAPTER V: INTERACTIVE TIMELINE & SADC GEO-SOVEREIGNTY MAP
          ========================================================================= */}
      <section id="chapter-map" className="scroll-mt-6">
        <InteractiveTimelineMap
          theme={theme}
          onNavigate={onNavigate}
          onOpenContactModal={onOpenContactModal}
        />
      </section>

      {/* =========================================================================
          CHAPTER VI: OUR STORY, ORIGIN & LEADERSHIP TEAM
          ========================================================================= */}
      <section id="chapter-origin" className="scroll-mt-6">
        <OurStoryOrigin
          theme={theme}
          onNavigate={onNavigate}
          onOpenContactModal={onOpenContactModal}
        />
      </section>

      {/* =========================================================================
          CHAPTER VII: FLAGSHIP PILLAR CHASSIS — AI COMPANY BUILDER
          ========================================================================= */}
      <section id="chapter-builder" className="scroll-mt-6">
        <div className={`p-8 sm:p-12 rounded-3xl relative overflow-hidden flex flex-col lg:flex-row items-center justify-between gap-8 transition-all ${
          isLight ? 'neu-card-light' : 'neu-card-dark'
        }`}>
          <div className="max-w-2xl space-y-4 text-left relative z-10">
            <div className={`inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider ${
              isLight ? 'neu-pill-light text-amber-700' : 'neu-pill-dark text-amber-400'
            }`}>
              <StatusLedPip status="amber" isLight={isLight} />
              <span className="font-mono text-[10px]">FLAGSHIP OPERATING ENGINE</span>
            </div>

            <h2 className={`text-2xl sm:text-4xl font-extrabold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              The <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">AI Company Builder</span>
            </h2>

            <p className={`text-sm sm:text-base leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
              Do not simply add a chat widget to legacy software. Re-engineer your enterprise architecture around an autonomous AI Operating Model, specialized agent workforces, and intelligent workflows.
            </p>

            <div className="flex flex-wrap gap-4 pt-2">
              <div className={`flex items-center gap-2 text-xs font-mono ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                <span>Workflow Collapse Engine</span>
              </div>
              <div className={`flex items-center gap-2 text-xs font-mono ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                <span>Multi-Agent Swarm Orchestration</span>
              </div>
              <div className={`flex items-center gap-2 text-xs font-mono ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                <span>Sovereign Data Containment</span>
              </div>
            </div>
          </div>

          <div className="relative z-10 flex flex-col sm:flex-row lg:flex-col gap-3 shrink-0">
            <button
              onClick={() => onNavigate('ai-company-builder')}
              className="neu-btn-amber px-8 py-4 rounded-2xl font-extrabold font-mono text-xs uppercase tracking-wider transition-all active:scale-95 shrink-0 flex items-center justify-center gap-2 cursor-pointer"
            >
              <span>Launch Company Builder</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => onOpenContactModal('Schedule AI Company Builder Demo')}
              className={`px-6 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-2 cursor-pointer ${
                isLight ? 'neu-btn-light text-slate-900' : 'neu-btn-dark text-zinc-200'
              }`}
            >
              <span>Schedule Live Demo</span>
              <PlayCircle className="w-4 h-4 text-amber-500" />
            </button>
          </div>
        </div>
      </section>

      {/* STAKEHOLDER CONSULTATION & ENGAGEMENT HUB */}
      <StakeholderEngagementHub
        theme={theme}
        onOpenContactModal={(intent) => onOpenContactModal(intent)}
      />

      {/* =========================================================================
          FINAL RESOLUTION: INSTITUTIONAL CALL-TO-ACTION BANNER
          ========================================================================= */}
      <section className="text-center pb-8">
        <div className={`p-8 sm:p-12 rounded-3xl max-w-4xl mx-auto space-y-6 relative overflow-hidden transition-all ${
          isLight ? 'neu-card-light' : 'neu-card-dark'
        }`}>
          <div className="flex items-center justify-center gap-2">
            <StatusLedPip status="emerald" isLight={isLight} />
            <span className="text-[10px] font-mono text-amber-500 font-bold uppercase tracking-wider">
              ENGAGE THE SOVEREIGN OPERATOR
            </span>
          </div>

          <h2 className={`text-2xl sm:text-4xl font-extrabold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
            Ready to Embark on Your Sovereign AI Transformation?
          </h2>

          <p className={`text-sm sm:text-base font-sans max-w-2xl mx-auto leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
            Consult directly with Jack Mlusu and the LightSpeed senior engineering team in Lilongwe to architect your custom agent hierarchy and sovereign infrastructure.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <button
              onClick={() => onOpenContactModal('Book Executive Consultation with Founder')}
              className="neu-btn-amber px-8 py-4 rounded-2xl font-extrabold font-mono text-xs uppercase tracking-wider flex items-center gap-2.5 cursor-pointer shadow-lg"
            >
              <span>Book Executive Consultation</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => onNavigate('resources')}
              className={`px-8 py-4 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider transition-all flex items-center gap-2 cursor-pointer ${
                isLight ? 'neu-btn-light text-slate-900' : 'neu-btn-dark text-zinc-200'
              }`}
            >
              <FileText className="w-4 h-4 text-amber-500" />
              <span>Execute Diagnostic Audit</span>
            </button>
          </div>
        </div>
      </section>

    </div>
  );
};
