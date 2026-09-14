import React, { useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  XCircle,
  ShieldCheck,
  Layers,
  Lock,
  Zap,
  Cpu,
  Database,
  Scale,
  ArrowRight,
  Sparkles,
  RefreshCw,
  Server
} from 'lucide-react';
import {
  StatusLedPip
} from './TactileHardwareElements';

interface CentralProblemSolutionProps {
  theme?: 'light' | 'dark';
  onOpenContactModal: (intent?: string) => void;
  onNavigate: (route: string) => void;
}

export const CentralProblemSolution: React.FC<CentralProblemSolutionProps> = ({
  theme = 'dark',
  onOpenContactModal,
  onNavigate
}) => {
  const isLight = theme === 'light';
  const [activeTab, setActiveTab] = useState<'matrix' | 'architecture' | 'roi'>('matrix');

  const comparisonPoints = [
    {
      dimension: 'Data Sovereignty & Residency',
      extractiveProblem: 'Sensitive institutional data exfiltrated to offshore hyperscalers subject to foreign surveillance and jurisdictional seizure.',
      lightspeedSolution: '100% on-soil data residency within Malawian & SADC sovereign datacenters under local jurisdiction and legal protection.',
      icon: Lock,
      impact: 'Zero Foreign Jurisdiction Risk'
    },
    {
      dimension: 'Fiduciary Accountability & Governance',
      extractiveProblem: 'Black-box chatbots with hallucinated outputs, unverified API calls, and zero cryptographic audit trails for board sign-off.',
      lightspeedSolution: 'Tier-1 to Tier-5 Human-in-the-Loop (HITL) approval gates requiring cryptographic signatures for high-stakes capital actions.',
      icon: ShieldCheck,
      impact: '100% Auditable Fiduciary Rigor'
    },
    {
      dimension: 'Local Economic & Payment Integration',
      extractiveProblem: 'Restricted to foreign USD credit cards with multi-day international wire friction and zero mobile money connectivity.',
      lightspeedSolution: 'Direct sub-30-second mobile money settlement over Airtel Money, TNM Mpamba, and regional RTGS banking networks.',
      icon: Zap,
      impact: '<30s Settlement Velocity'
    },
    {
      dimension: 'Cultural & Dialect NLP Precision',
      extractiveProblem: 'Generic Western models failing on Chichewa, Tumbuka, and local African commercial dialect nuances.',
      lightspeedSolution: 'Custom-tuned sovereign tokenizers and multi-lingual agents fluent in indigenous African linguistic and legal frameworks.',
      icon: Cpu,
      impact: 'Native Regional Dialect NLP'
    },
    {
      dimension: 'Autonomous Swarm Orchestration',
      extractiveProblem: 'Single-thread prompt boxes that require manual human babysitting for every repetitive operational workflow.',
      lightspeedSolution: 'OpenCode-native autonomous agent hierarchies (Executives + Specialists) with stateful task bus and self-healing execution.',
      icon: Layers,
      impact: '74% Operational Velocity Boost'
    }
  ];

  return (
    <div className={`rounded-3xl relative overflow-hidden transition-all text-left p-6 sm:p-10 ${
      isLight ? 'neu-card-light' : 'neu-card-dark'
    }`}>
      {/* Top Telemetry Header */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-2xl flex items-center justify-center shrink-0 ${
            isLight ? 'neu-inset-light text-amber-600' : 'neu-inset-dark text-amber-400'
          }`}>
            <Scale className="w-5 h-5 text-amber-500" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <StatusLedPip status="emerald" isLight={isLight} />
              <span className="text-[11px] font-mono font-bold tracking-widest text-amber-500 uppercase">
                THE CENTRAL PROBLEM &amp; SOVEREIGN RESOLUTION
              </span>
            </div>
            <span className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Comparative Analysis: Extractive SaaS Traps vs. Sovereign Infrastructure
            </span>
          </div>
        </div>

        {/* View Switcher Pills */}
        <div className="flex items-center gap-2">
          <div className={`flex items-center p-1 rounded-2xl ${
            isLight ? 'neu-inset-light' : 'neu-inset-dark'
          }`}>
            <button
              onClick={() => setActiveTab('matrix')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeTab === 'matrix'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              Comparison Matrix
            </button>
            <button
              onClick={() => setActiveTab('architecture')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeTab === 'architecture'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              Sovereign Pillars
            </button>
            <button
              onClick={() => setActiveTab('roi')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeTab === 'roi'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              Institutional ROI
            </button>
          </div>
        </div>
      </div>

      {/* Main Punchy Narrative Headlines */}
      <div className="relative z-10 max-w-4xl space-y-4 mb-10">
        <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-mono font-semibold ${
          isLight ? 'neu-pill-light text-amber-700' : 'neu-pill-dark text-amber-400'
        }`}>
          <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
          <span>The Institutional Reality Check</span>
        </div>

        <h2 className={`text-2xl sm:text-4xl lg:text-5xl font-extrabold font-display tracking-tight leading-tight ${
          isLight ? 'text-slate-900' : 'text-zinc-50'
        }`}>
          Why Rent Ephemeral Chat Wrappers When You Can <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">Own Sovereign AI Infrastructure?</span>
        </h2>

        <p className={`text-sm sm:text-base md:text-lg leading-relaxed font-sans ${
          isLight ? 'text-slate-700' : 'text-zinc-300'
        }`}>
          Enterprises and governments across Africa face a critical fork in the road: either become perpetual data colonies paying exorbitant foreign subscription fees for generic, un-audited chatbots—or partner with <strong className="text-amber-500 font-semibold">LightSpeed Holdings</strong> to build resilient, on-soil sovereign intelligence.
        </p>
      </div>

      {/* Content View: Matrix */}
      {activeTab === 'matrix' && (
        <div className="space-y-4 relative z-10 mb-10">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pb-2">
            <div className={`p-4 rounded-2xl flex items-center gap-2.5 font-mono text-xs font-bold uppercase tracking-wider ${
              isLight ? 'bg-rose-50 border border-rose-200 text-rose-800' : 'bg-rose-950/30 border border-rose-900/50 text-rose-400'
            }`}>
              <XCircle className="w-4 h-4 text-rose-500 shrink-0" />
              <span>Extractive AI SaaS &amp; Generic Cloud Wrappers</span>
            </div>

            <div className={`p-4 rounded-2xl flex items-center gap-2.5 font-mono text-xs font-bold uppercase tracking-wider ${
              isLight ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'bg-emerald-950/30 border border-emerald-900/50 text-emerald-400'
            }`}>
              <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
              <span>LightSpeed Holdings Sovereign Architecture</span>
            </div>
          </div>

          <div className="space-y-4">
            {comparisonPoints.map((item, idx) => {
              const IconComp = item.icon;
              return (
                <div
                  key={idx}
                  className={`p-5 sm:p-6 rounded-2xl transition-all ${
                    isLight ? 'neu-convex-light' : 'neu-convex-dark'
                  }`}
                >
                  <div className="flex items-center justify-between gap-3 mb-4 pb-3 border-b border-zinc-500/15">
                    <div className="flex items-center gap-2.5">
                      <div className={`p-2 rounded-xl ${
                        isLight ? 'neu-inset-light text-amber-600' : 'neu-inset-dark text-amber-400'
                      }`}>
                        <IconComp className="w-4 h-4" />
                      </div>
                      <h3 className={`text-sm sm:text-base font-bold font-display ${
                        isLight ? 'text-slate-900' : 'text-zinc-100'
                      }`}>
                        {item.dimension}
                      </h3>
                    </div>

                    <span className={`text-[10px] font-mono px-3 py-1 rounded-full font-bold uppercase ${
                      isLight ? 'neu-pill-light text-emerald-700' : 'neu-pill-dark text-emerald-400'
                    }`}>
                      {item.impact}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Problem Side */}
                    <div className={`p-3.5 rounded-xl text-xs leading-relaxed flex items-start gap-2.5 ${
                      isLight ? 'bg-rose-50/50 text-slate-700' : 'bg-rose-950/20 text-zinc-300'
                    }`}>
                      <XCircle className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
                      <span>{item.extractiveProblem}</span>
                    </div>

                    {/* Solution Side */}
                    <div className={`p-3.5 rounded-xl text-xs leading-relaxed flex items-start gap-2.5 ${
                      isLight ? 'bg-emerald-50/50 text-slate-800 font-medium' : 'bg-emerald-950/20 text-zinc-200'
                    }`}>
                      <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                      <span>{item.lightspeedSolution}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Content View: Architecture Pillars */}
      {activeTab === 'architecture' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-10 mb-10">
          <div className={`p-6 rounded-2xl ${isLight ? 'neu-convex-light' : 'neu-convex-dark'}`}>
            <div className={`p-3 rounded-xl w-fit mb-4 ${isLight ? 'neu-inset-light text-amber-600' : 'neu-inset-dark text-amber-400'}`}>
              <Server className="w-6 h-6" />
            </div>
            <h3 className={`text-base font-bold font-display mb-2 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              1. Sovereign Compute Backbone
            </h3>
            <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Air-cooled, high-density GPU edge clusters situated directly inside Malawian and SADC data zones, guaranteeing ultra-low latency and zero international transit dependency.
            </p>
          </div>

          <div className={`p-6 rounded-2xl ${isLight ? 'neu-convex-light' : 'neu-convex-dark'}`}>
            <div className={`p-3 rounded-xl w-fit mb-4 ${isLight ? 'neu-inset-light text-cyan-600' : 'neu-inset-dark text-cyan-400'}`}>
              <ShieldCheck className="w-6 h-6 text-cyan-500" />
            </div>
            <h3 className={`text-base font-bold font-display mb-2 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              2. Fiduciary Cryptographic Gates
            </h3>
            <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Multi-signature authorization routines for financial outlays, regulatory compliance filings, and state data transformations with immutable hash logging.
            </p>
          </div>

          <div className={`p-6 rounded-2xl ${isLight ? 'neu-convex-light' : 'neu-convex-dark'}`}>
            <div className={`p-3 rounded-xl w-fit mb-4 ${isLight ? 'neu-inset-light text-purple-600' : 'neu-inset-dark text-purple-400'}`}>
              <Zap className="w-6 h-6 text-purple-500" />
            </div>
            <h3 className={`text-base font-bold font-display mb-2 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              3. Indigenous Dialect Swarms
            </h3>
            <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Autonomous sub-agents calibrated on authentic regional vernacular, agricultural supply chain dynamics, and SADC cross-border trade regulations.
            </p>
          </div>
        </div>
      )}

      {/* Content View: Institutional ROI */}
      {activeTab === 'roi' && (
        <div className={`p-6 sm:p-8 rounded-2xl relative z-10 mb-10 ${isLight ? 'neu-well-light' : 'neu-well-dark'}`}>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-3xl sm:text-4xl font-extrabold font-mono text-amber-500 mb-1">
                74%
              </div>
              <div className={`text-xs font-mono font-semibold uppercase ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                Process Latency Reduction
              </div>
              <p className={`text-[11px] mt-1 ${isLight ? 'text-slate-500' : 'text-zinc-500'}`}>
                Workflow cycle times slashed from days to seconds
              </p>
            </div>

            <div>
              <div className="text-3xl sm:text-4xl font-extrabold font-mono text-emerald-500 mb-1">
                &lt;30s
              </div>
              <div className={`text-xs font-mono font-semibold uppercase ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                Mobile Settlement
              </div>
              <p className={`text-[11px] mt-1 ${isLight ? 'text-slate-500' : 'text-zinc-500'}`}>
                Native Airtel &amp; TNM payment execution
              </p>
            </div>

            <div>
              <div className="text-3xl sm:text-4xl font-extrabold font-mono text-cyan-500 mb-1">
                100%
              </div>
              <div className={`text-xs font-mono font-semibold uppercase ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                Auditable Logs
              </div>
              <p className={`text-[11px] mt-1 ${isLight ? 'text-slate-500' : 'text-zinc-500'}`}>
                Cryptographic hash per agent task output
              </p>
            </div>

            <div>
              <div className="text-3xl sm:text-4xl font-extrabold font-mono text-purple-500 mb-1">
                0%
              </div>
              <div className={`text-xs font-mono font-semibold uppercase ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                Foreign Exfiltration
              </div>
              <p className={`text-[11px] mt-1 ${isLight ? 'text-slate-500' : 'text-zinc-500'}`}>
                All data remains within sovereign border control
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Clear Action CTAs */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-4 pt-5 border-t ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => onOpenContactModal('Request Sovereign AI Diagnostic & Audit')}
            className="neu-btn-amber px-6 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 cursor-pointer"
          >
            <span>Request Sovereign Audit</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => onNavigate('solutions')}
            className={`px-5 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 cursor-pointer ${
              isLight ? 'neu-btn-light text-slate-900' : 'neu-btn-dark text-zinc-200'
            }`}
          >
            <ShieldCheck className="w-4 h-4 text-amber-500" />
            <span>Explore Sovereign Solutions</span>
          </button>
        </div>

        <button
          onClick={() => onNavigate('technology')}
          className="text-xs font-mono font-bold text-amber-500 hover:text-amber-400 transition-colors py-2 px-3 flex items-center gap-1.5 cursor-pointer"
        >
          <span>Deep-Dive Engineering Specs</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
