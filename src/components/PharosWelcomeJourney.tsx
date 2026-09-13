import React, { useState } from 'react';
import { 
  Compass, 
  Sparkles, 
  ArrowRight, 
  ShieldCheck, 
  Bot, 
  Layers, 
  Cpu, 
  Globe2, 
  CheckCircle2, 
  FileText, 
  Lock, 
  Zap, 
  Activity,
  Award,
  BookOpen,
  ChevronRight,
  Flame,
  Radio,
  Eye,
  RotateCw
} from 'lucide-react';
import { 
  StatusLedPip 
} from './TactileHardwareElements';

interface PharosWelcomeJourneyProps {
  onNavigate: (route: string, param?: string) => void;
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const PharosWelcomeJourney: React.FC<PharosWelcomeJourneyProps> = ({
  onNavigate,
  onOpenContactModal,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';
  const [selectedMilestone, setSelectedMilestone] = useState<number>(0);

  const industrialRevolutionPillars = [
    {
      era: '1st Industrial Revolution',
      catalyst: 'Steam & Mechanical Weaving',
      legacy: 'Centralized physical energy factories'
    },
    {
      era: '2nd Industrial Revolution',
      catalyst: 'Electricity & Mass Assembly',
      legacy: 'Continental grid networks'
    },
    {
      era: '3rd Industrial Revolution',
      catalyst: 'Silicon & Digital Microchips',
      legacy: 'Global internet protocols & computation'
    },
    {
      era: '4th // The AI Industrial Revolution',
      catalyst: 'Sovereign Agentic Swarms & Pharos Beacon',
      legacy: 'Self-executing cognitive infrastructure on sovereign soil'
    }
  ];

  const journeySteps = [
    {
      step: '01',
      title: 'Sovereign Grounding & Fiduciary Audit',
      subtitle: 'Data Residence & Regulatory Defense',
      description: 'Map institutional data perimeters, privacy mandates, and critical workflows. We establish air-gapped sovereign foundations so your proprietary knowledge remains 100% under your institutional command.',
      icon: Lock,
      color: 'amber',
      tag: 'Zero Data Leakage • SADC Aligned',
      beaconBeam: '13.9899° S, 33.7741° E [LILONGWE COMPUTE]'
    },
    {
      step: '02',
      title: 'Autonomous Swarm Architecture',
      subtitle: 'OpenCode v2 Deterministic Models',
      description: 'Deploy specialized, multi-tiered agentic hierarchies defined by rigorous YAML schemas. Your autonomous specialists execute complex departmental operations with sub-second precision.',
      icon: Bot,
      color: 'emerald',
      tag: 'YAML Company Registry • 7 Canonical Tools',
      beaconBeam: 'MULTI-AGENT DETERMINISTIC SWARM'
    },
    {
      step: '03',
      title: 'Human-in-the-Loop (HITL) Governance',
      subtitle: 'Tier 1 to Tier 5 Cryptographic Gates',
      description: 'Lock in unshakeable accountability. Non-trivial actions, policy decrees, and capital disbursements require explicit executive signatures, ensuring zero hallucinated actions or unverified risks.',
      icon: ShieldCheck,
      color: 'cyan',
      tag: '100% Auditable • Tier-5 Executive Gate',
      beaconBeam: 'MATHEMATICAL HITL BOUNDARIES'
    },
    {
      step: '04',
      title: 'Real-Time Ecosystem Execution',
      subtitle: 'Local Settlement & Dialect NLP',
      description: 'Connect directly to African economic realities: sub-30-second mobile money settlement over Airtel/TNM, native Chichewa/English NLP processing, and institutional infrastructure built for permanence.',
      icon: Zap,
      color: 'purple',
      tag: '<30s Settlement • Regional Dialects',
      beaconBeam: 'SOVEREIGN SADC SETTLEMENT CORRIDOR'
    }
  ];

  return (
    <div className={`rounded-3xl relative overflow-hidden transition-all p-6 sm:p-10 text-left ${
      isLight ? 'neu-card-light' : 'neu-card-dark'
    }`}>
      {/* Cinematic Ambient Beacon Rays */}
      <div className="absolute -top-24 -right-24 w-96 h-96 bg-amber-500/15 rounded-full blur-3xl pointer-events-none -z-0 animate-pulse" style={{ animationDuration: '6s' }} />
      <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-amber-600/10 rounded-full blur-3xl pointer-events-none -z-0" />

      {/* Top Telemetry Header Bar */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-2xl flex items-center justify-center shrink-0 ${
            isLight ? 'neu-inset-light text-amber-600' : 'neu-inset-dark text-amber-400'
          }`}>
            <Compass className="w-5 h-5 animate-spin text-amber-500" style={{ animationDuration: '24s' }} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <StatusLedPip status="emerald" isLight={isLight} />
              <span className="text-[11px] font-mono font-bold tracking-widest text-amber-500 uppercase">
                THE PHAROS BEACON // AI INDUSTRIAL REVOLUTION DOCTRINE
              </span>
            </div>
            <span className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Navigating SADC and Global Enterprise Through the 4th Industrial Dawn
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className={`px-3.5 py-1.5 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider ${
            isLight ? 'neu-pill-light text-slate-700' : 'neu-pill-dark text-zinc-300'
          }`}>
            Alexandria 300 BC → Lilongwe 2026 AD
          </span>
        </div>
      </div>

      {/* Welcoming Message Manifesto */}
      <div className="relative z-10 max-w-4xl space-y-4 mb-10">
        <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-mono font-semibold ${
          isLight ? 'neu-pill-light text-amber-700' : 'neu-pill-dark text-amber-400'
        }`}>
          <Flame className="w-3.5 h-3.5 text-amber-500 animate-pulse" />
          <span>The Guiding Beacon on the AI Industrial Revolution</span>
        </div>

        <h2 className={`text-2xl sm:text-4xl lg:text-5xl font-extrabold font-display tracking-tight leading-tight ${
          isLight ? 'text-slate-900' : 'text-zinc-50'
        }`}>
          The AI Industrial Revolution Requires an <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">Unwavering Beacon</span>
        </h2>

        <p className={`text-sm sm:text-base md:text-lg leading-relaxed font-sans ${
          isLight ? 'text-slate-700' : 'text-zinc-300'
        }`}>
          Just as the ancient <strong className="text-amber-500 font-semibold">Pharos of Alexandria</strong> pierced the night sea to guide commerce into harbor, <strong className="text-amber-500 font-semibold">LightSpeed Holdings</strong> operates as the premier sovereign beacon guiding enterprises, central banks, and ministries across Southern Africa through the AI Industrial Revolution.
        </p>

        <p className={`text-xs sm:text-sm md:text-base leading-relaxed font-sans ${
          isLight ? 'text-slate-600' : 'text-zinc-400'
        }`}>
          The shift from simple automation to autonomous, self-orchestrating agent swarms is the defining tectonic transition of our century. We ensure your enterprise navigates past the perils of cloud extraction, data vassalage, and uncontrolled hallucinations into mathematical certainty and regional data supremacy.
        </p>
      </div>

      {/* Industrial Revolution Epochs Ribbon */}
      <div className={`relative z-10 p-5 rounded-2xl mb-10 border ${
        isLight ? 'bg-slate-100/80 border-slate-300' : 'bg-black/40 border-zinc-800'
      }`}>
        <div className="flex items-center gap-2 mb-3">
          <Layers className="w-4 h-4 text-amber-500" />
          <span className="text-xs font-mono font-bold uppercase tracking-wider text-amber-500">
            The Historical Lineage of Industrial Transformation
          </span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {industrialRevolutionPillars.map((pillar, idx) => (
            <div 
              key={pillar.era}
              className={`p-3.5 rounded-xl border text-left transition-all ${
                idx === 3 
                  ? 'border-amber-500 bg-amber-500/15 shadow-md shadow-amber-500/10' 
                  : isLight ? 'border-slate-200 bg-white/70' : 'border-zinc-800/80 bg-zinc-900/40'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className={`text-[10px] font-mono font-bold uppercase ${idx === 3 ? 'text-amber-400' : 'text-zinc-500'}`}>
                  0{idx + 1} // EPOCH
                </span>
                {idx === 3 && <StatusLedPip status="amber" isLight={isLight} />}
              </div>
              <h4 className="text-xs font-bold font-display mb-1">{pillar.era}</h4>
              <p className="text-[11px] font-mono text-amber-500 font-semibold mb-1">{pillar.catalyst}</p>
              <p className="text-[10px] text-zinc-400 leading-snug">{pillar.legacy}</p>
            </div>
          ))}
        </div>
      </div>

      {/* 4-Step Navigational Journey Grid */}
      <div className="relative z-10 grid grid-cols-1 md:grid-cols-2 gap-5 lg:gap-6 mb-10">
        {journeySteps.map((step, index) => {
          const IconComp = step.icon;
          const isSelected = selectedMilestone === index;
          return (
            <div 
              key={step.step}
              onClick={() => setSelectedMilestone(index)}
              className={`p-6 rounded-2xl transition-all duration-300 flex flex-col justify-between relative group cursor-pointer border ${
                isSelected 
                  ? 'border-amber-500 bg-amber-500/10 shadow-2xl scale-[1.01]' 
                  : isLight ? 'neu-convex-light hover:shadow-xl border-transparent' : 'neu-convex-dark hover:shadow-2xl border-transparent'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3.5">
                  <div className="flex items-center gap-3">
                    <div className={`p-3 rounded-xl flex items-center justify-center ${
                      isSelected 
                        ? 'bg-amber-500 text-slate-950 font-bold' 
                        : isLight ? 'neu-inset-light text-amber-600' : 'neu-inset-dark text-amber-400'
                    }`}>
                      <IconComp className="w-5 h-5" />
                    </div>
                    <div>
                      <span className="text-[10px] font-mono font-bold text-amber-500 tracking-wider">
                        BEACON VECTOR [ {step.step} ]
                      </span>
                      <h3 className={`text-base sm:text-lg font-bold font-display ${
                        isLight ? 'text-slate-900' : 'text-zinc-100'
                      }`}>
                        {step.title}
                      </h3>
                    </div>
                  </div>
                </div>

                <div className="text-xs font-mono font-semibold text-amber-600/95 dark:text-amber-400/95 mb-2">
                  {step.subtitle}
                </div>

                <p className={`text-xs sm:text-sm leading-relaxed mb-4 ${
                  isLight ? 'text-slate-600' : 'text-zinc-400'
                }`}>
                  {step.description}
                </p>
              </div>

              <div className={`pt-3.5 border-t flex items-center justify-between ${
                isLight ? 'border-slate-300/60' : 'border-slate-800/80'
              }`}>
                <span className={`text-[10px] font-mono px-3 py-1 rounded-full ${
                  isLight ? 'neu-pill-light text-slate-700' : 'neu-pill-dark text-zinc-300'
                }`}>
                  {step.tag}
                </span>
                <span className="text-[9px] font-mono text-amber-500/80 uppercase font-bold">
                  {step.beaconBeam}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Institutional Founder Stance & Quote (Recessed Neumorphic Well) */}
      <div className={`relative z-10 p-6 sm:p-7 rounded-2xl mb-8 flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-6 ${
        isLight ? 'neu-well-light text-slate-800' : 'neu-well-dark text-zinc-200'
      }`}>
        <div className={`p-3.5 rounded-2xl shrink-0 ${
          isLight ? 'neu-convex-light text-amber-600' : 'neu-convex-dark text-amber-400'
        }`}>
          <BookOpen className="w-6 h-6" />
        </div>
        <div className="space-y-1.5 text-left flex-1 min-w-0">
          <p className="text-xs sm:text-sm italic font-serif leading-relaxed">
            &ldquo;African enterprise must never simply consume foreign algorithms as digital tenants. Through Pharos, we construct the sovereign intelligence foundations anchored in our own soil, laws, languages, and economic institutions.&rdquo;
          </p>
          <div className="text-[11px] font-mono text-amber-500 font-bold pt-1">
            — Jack Mlusu, Founder &amp; CEO, LightSpeed Holdings Limited
          </div>
        </div>
      </div>

      {/* Guided Call-to-Action Bar (Neumorphic Buttons) */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-4 pt-5 border-t ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex flex-wrap items-center gap-3.5">
          <button
            onClick={() => onOpenContactModal('Embark on the Pharos AI Journey')}
            className="neu-btn-amber px-6 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 shrink-0 cursor-pointer"
          >
            <span>Begin Your Guided AI Journey</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => onNavigate('pharos')}
            className={`px-5 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 shrink-0 cursor-pointer ${
              isLight ? 'neu-btn-light text-slate-900' : 'neu-btn-dark text-zinc-200'
            }`}
          >
            <Compass className="w-4 h-4 text-amber-500" />
            <span>Read Pharos Treatises (I–IV)</span>
          </button>
        </div>

        <button
          onClick={() => onNavigate('ai-company-builder')}
          className={`flex items-center gap-2 text-xs font-mono font-bold text-amber-500 hover:text-amber-400 transition-colors py-2 px-3 rounded-xl cursor-pointer ${
            isLight ? 'hover:neu-pill-light' : 'hover:neu-pill-dark'
          }`}
        >
          <span>Explore AI Company Builder</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

    </div>
  );
};

