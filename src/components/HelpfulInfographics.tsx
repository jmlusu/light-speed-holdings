import React, { useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';
import {
  Workflow,
  CheckCircle2,
  ArrowRight,
  Zap,
  ShieldCheck,
  Layers,
  Cpu,
  Clock,
  Sparkles,
  TrendingDown,
  TrendingUp,
  Activity
} from 'lucide-react';
import {
  StatusLedPip
} from './TactileHardwareElements';

interface HelpfulInfographicsProps {
  theme?: 'light' | 'dark';
  onNavigate: (route: string) => void;
  onOpenContactModal: (intent?: string) => void;
}

export const HelpfulInfographics: React.FC<HelpfulInfographicsProps> = ({
  theme = 'dark',
  onNavigate,
  onOpenContactModal
}) => {
  const isLight = theme === 'light';
  const [activeGraphic, setActiveGraphic] = useState<'lifecycle' | 'latency' | 'governance'>('lifecycle');
  const [activeStep, setActiveStep] = useState<number>(0);

  const lifecycleSteps = [
    {
      step: '01',
      phase: 'Sovereign Readiness & Ingress Audit',
      duration: 'Week 1–2',
      deliverable: 'Data Sovereignty Matrix & Security Baseline',
      desc: 'Comprehensive mapping of institutional data silos, regulatory boundaries, and cloud dependency vulnerabilities.',
      icon: ShieldCheck,
      color: 'amber'
    },
    {
      step: '02',
      phase: 'OpenCode Agent Hierarchy Design',
      duration: 'Week 3–4',
      deliverable: 'company-registry.yaml & Sub-Agent Cards',
      desc: 'Mathematical formalization of executive and specialist agent topologies with explicit permissions (read, edit, grep, list, bash, webfetch, task).',
      icon: Layers,
      color: 'cyan'
    },
    {
      step: '03',
      phase: 'Edge Infrastructure & Node Provisioning',
      duration: 'Week 5–6',
      deliverable: 'Lilongwe/SADC On-Soil Compute Cluster',
      desc: 'Deployment of localized high-performance compute nodes, air-cooled server clusters, and cryptographic hardware security modules.',
      icon: Cpu,
      color: 'emerald'
    },
    {
      step: '04',
      phase: 'Local Financial & Dialect NLP Binding',
      duration: 'Week 7–8',
      deliverable: 'Sub-30s Mobile Money & Chichewa NLP',
      desc: 'Direct API integration with Airtel Money, TNM Mpamba, and regional RTGS banking rails alongside indigenous NLP tokenizers.',
      icon: Zap,
      color: 'purple'
    },
    {
      step: '05',
      phase: 'Autonomous Swarm Fleet Launch',
      duration: 'Ongoing',
      deliverable: 'Live Telemetry & Tier-5 HITL Oversight',
      desc: 'Full operational activation of autonomous business swarms with 24/7 human-in-the-loop executive control and SLA monitoring.',
      icon: Activity,
      color: 'amber'
    }
  ];

  const latencyData = [
    { name: 'Offshore US API', latency: 840, settlement: 4320, color: '#ef4444' },
    { name: 'European Cloud', latency: 420, settlement: 2880, color: '#e63946' },
    { name: 'Generic SADC Proxy', latency: 180, settlement: 1440, color: '#e63946' },
    { name: 'LightSpeed Lilongwe Edge', latency: 16, settlement: 0.5, color: '#10b981' }
  ];

  const hitlTiers = [
    {
      tier: 'Tier 1',
      title: 'Autonomous Read-Only Ops',
      threshold: 'Low Stakes',
      approval: 'Autonomous Execution',
      description: 'Telemetry polling, index lookups, document summarization, log analysis.',
      color: 'emerald'
    },
    {
      tier: 'Tier 2',
      title: 'Operational Drafts & Suggestions',
      threshold: 'Internal Drafts',
      approval: 'Specialist Sign-Off',
      description: 'Report drafting, code linting, customer query triaging, scheduling.',
      color: 'cyan'
    },
    {
      tier: 'Tier 3',
      title: 'Workflow Execution & Staging',
      threshold: 'Process Mutation',
      approval: 'Manager Verification',
      description: 'Database record updates, invoice batching, test environment rollouts.',
      color: 'amber'
    },
    {
      tier: 'Tier 4',
      title: 'Capital Disbursements & Outlays',
      threshold: 'Financial & PII',
      approval: 'Dual Executive Multi-Sig',
      description: 'Mobile money mass payouts, bank wires, contractual commitments, user PII access.',
      color: 'orange'
    },
    {
      tier: 'Tier 5',
      title: 'Sovereign Policy & Core Mutex',
      threshold: 'Critical State / Board',
      approval: 'Board / Ministerial Cryptographic Key',
      description: 'System architectural rewrites, model retraining on state data, legal governance decrees.',
      color: 'rose'
    }
  ];

  return (
    <div className={`rounded-3xl relative overflow-hidden transition-all text-left p-6 sm:p-10 ${
      isLight ? 'neu-card-light' : 'neu-card-dark'
    }`}>
      {/* Top Header Bar */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-2xl flex items-center justify-center shrink-0 ${
            isLight ? 'neu-inset-light text-amber-600' : 'neu-inset-dark text-amber-400'
          }`}>
            <Workflow className="w-5 h-5 text-amber-500" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <StatusLedPip status="emerald" isLight={isLight} />
              <span className="text-[11px] font-mono font-bold tracking-widest text-amber-500 uppercase">
                HELPFUL INFOGRAPHICS &amp; STEP-BY-STEP PROCESS CHARTS
              </span>
            </div>
            <span className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Scannable Visual Architecture, Benchmarks &amp; Governance Blueprints
            </span>
          </div>
        </div>

        {/* Chart Selector Pills */}
        <div className="flex items-center gap-2">
          <div className={`flex items-center p-1 rounded-2xl ${
            isLight ? 'neu-inset-light' : 'neu-inset-dark'
          }`}>
            <button
              onClick={() => setActiveGraphic('lifecycle')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeGraphic === 'lifecycle'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              5-Phase Lifecycle
            </button>
            <button
              onClick={() => setActiveGraphic('latency')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeGraphic === 'latency'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              Latency Benchmark
            </button>
            <button
              onClick={() => setActiveGraphic('governance')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeGraphic === 'governance'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              HITL 5-Tier Spectrum
            </button>
          </div>
        </div>
      </div>

      {/* Main Narrative Headline */}
      <div className="relative z-10 max-w-4xl space-y-4 mb-10">
        <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-mono font-semibold ${
          isLight ? 'neu-pill-light text-amber-700' : 'neu-pill-dark text-amber-400'
        }`}>
          <Sparkles className="w-3.5 h-3.5 text-amber-500" />
          <span>Interactive Visual Architecture</span>
        </div>

        <h2 className={`text-2xl sm:text-4xl lg:text-5xl font-extrabold font-display tracking-tight leading-tight ${
          isLight ? 'text-slate-900' : 'text-zinc-50'
        }`}>
          Sovereign AI Decoded: <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">Clear, Measurable &amp; Scannable</span>
        </h2>

        <p className={`text-sm sm:text-base md:text-lg leading-relaxed font-sans ${
          isLight ? 'text-slate-700' : 'text-zinc-300'
        }`}>
          We convert abstract AI hype into deterministic engineering roadmaps. Explore our 5-phase transformation sequence, regional latency advantages, and cryptographic governance tiers.
        </p>
      </div>

      {/* Infographic 1: 5-Phase Lifecycle */}
      {activeGraphic === 'lifecycle' && (
        <div className="space-y-6 relative z-10 mb-10">
          {/* Horizontal Progress Flow */}
          <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
            {lifecycleSteps.map((s, idx) => {
              const isCurrent = activeStep === idx;
              const IconComp = s.icon;
              return (
                <button
                  key={s.step}
                  onClick={() => setActiveStep(idx)}
                  className={`p-4 rounded-2xl text-left transition-all cursor-pointer flex flex-col justify-between ${
                    isCurrent
                      ? (isLight ? 'neu-pressed-light border-amber-500/50' : 'neu-pressed-dark border-amber-500/50')
                      : (isLight ? 'neu-convex-light' : 'neu-convex-dark')
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-mono font-bold text-amber-500">
                        PHASE {s.step}
                      </span>
                      <IconComp className="w-4 h-4 text-amber-500" />
                    </div>
                    <div className={`text-xs font-bold font-display line-clamp-2 ${
                      isCurrent ? 'text-amber-600 dark:text-amber-400' : (isLight ? 'text-slate-900' : 'text-zinc-100')
                    }`}>
                      {s.phase}
                    </div>
                  </div>
                  <div className="text-[10px] font-mono text-zinc-400 mt-2">
                    {s.duration}
                  </div>
                </button>
              );
            })}
          </div>

          {/* Active Phase Deep Dive Card */}
          <div className={`p-6 sm:p-8 rounded-2xl ${isLight ? 'neu-well-light' : 'neu-well-dark'}`}>
            <div className="flex flex-wrap items-center justify-between gap-4 mb-4 pb-4 border-b border-zinc-500/15">
              <div className="flex items-center gap-3">
                <span className="text-2xl sm:text-3xl font-mono font-extrabold text-amber-500">
                  {lifecycleSteps[activeStep].step}
                </span>
                <div>
                  <h3 className={`text-lg sm:text-xl font-bold font-display ${
                    isLight ? 'text-slate-900' : 'text-zinc-100'
                  }`}>
                    {lifecycleSteps[activeStep].phase}
                  </h3>
                  <span className="text-xs font-mono text-amber-600 dark:text-amber-400 font-semibold">
                    Expected Timeline: {lifecycleSteps[activeStep].duration}
                  </span>
                </div>
              </div>

              <div className={`px-3.5 py-1.5 rounded-full text-xs font-mono font-bold ${
                isLight ? 'bg-amber-100 text-amber-800 border border-amber-300' : 'bg-amber-950/50 text-amber-400 border border-amber-800/40'
              }`}>
                Deliverable: {lifecycleSteps[activeStep].deliverable}
              </div>
            </div>

            <p className={`text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700' : 'text-zinc-300'
            }`}>
              {lifecycleSteps[activeStep].desc}
            </p>
          </div>
        </div>
      )}

      {/* Infographic 2: Latency & Settlement Benchmark Chart */}
      {activeGraphic === 'latency' && (
        <div className="space-y-6 relative z-10 mb-10">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            {/* Chart */}
            <div className={`lg:col-span-8 p-6 rounded-2xl ${isLight ? 'neu-well-light' : 'neu-well-dark'}`}>
              <div className="flex items-center justify-between mb-4">
                <h3 className={`text-sm font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Network Latency to Lilongwe Node (Milliseconds - Lower is Better)
                </h3>
                <span className="text-[10px] font-mono text-emerald-500 font-bold">
                  98.1% LATENCY REDUCTION
                </span>
              </div>

              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={latencyData} layout="vertical" margin={{ left: 20, right: 30, top: 10, bottom: 10 }}>
                    <XAxis type="number" unit="ms" stroke={isLight ? '#64748b' : '#94a3b8'} />
                    <YAxis dataKey="name" type="category" width={140} stroke={isLight ? '#64748b' : '#94a3b8'} tick={{ fontSize: 11 }} />
                    <Tooltip
                      formatter={(val: any) => [`${val} ms`, 'Latency']}
                      contentStyle={{
                        backgroundColor: isLight ? '#ffffff' : '#0f1422',
                        borderColor: isLight ? '#cbd5e1' : '#334155',
                        borderRadius: '0.75rem',
                        color: isLight ? '#070a40' : '#f8fafc',
                        fontFamily: 'monospace'
                      }}
                    />
                    <Bar dataKey="latency" radius={[0, 8, 8, 0]}>
                      {latencyData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Metrics Breakdown */}
            <div className="lg:col-span-4 space-y-4">
              <div className={`p-5 rounded-2xl ${isLight ? 'neu-convex-light' : 'neu-convex-dark'}`}>
                <div className="flex items-center gap-2 text-xs font-mono font-bold text-emerald-500 mb-1">
                  <Zap className="w-4 h-4" />
                  <span>&lt;18ms SADC Latency</span>
                </div>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Direct on-soil edge compute clusters eliminate 800ms+ roundtrip transit to foreign datacenters.
                </p>
              </div>

              <div className={`p-5 rounded-2xl ${isLight ? 'neu-convex-light' : 'neu-convex-dark'}`}>
                <div className="flex items-center gap-2 text-xs font-mono font-bold text-amber-500 mb-1">
                  <Clock className="w-4 h-4" />
                  <span>Sub-30s Mobile Money</span>
                </div>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Autonomous agent payment settlements execute over Airtel and TNM Mpamba without international wire delays.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Infographic 3: 5-Tier HITL Governance Spectrum */}
      {activeGraphic === 'governance' && (
        <div className="space-y-4 relative z-10 mb-10">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {hitlTiers.map((t) => (
              <div
                key={t.tier}
                className={`p-5 rounded-2xl transition-all flex flex-col justify-between ${
                  isLight ? 'neu-convex-light' : 'neu-convex-dark'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-mono font-bold text-amber-500">
                      {t.tier}
                    </span>
                    <ShieldCheck className="w-4 h-4 text-amber-500" />
                  </div>
                  <h4 className={`text-sm font-bold font-display mb-1 ${
                    isLight ? 'text-slate-900' : 'text-zinc-100'
                  }`}>
                    {t.title}
                  </h4>
                  <div className="text-[11px] font-mono text-amber-600 dark:text-amber-400 font-semibold mb-2">
                    {t.threshold}
                  </div>
                  <p className={`text-xs leading-relaxed ${
                    isLight ? 'text-slate-600' : 'text-zinc-400'
                  }`}>
                    {t.description}
                  </p>
                </div>

                <div className="pt-3 mt-3 border-t border-zinc-500/15 text-[10px] font-mono font-bold text-emerald-500">
                  Gate: {t.approval}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-4 pt-5 border-t ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => onOpenContactModal('Request Architecture Blueprint & SLAs')}
            className="neu-btn-amber px-6 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 cursor-pointer"
          >
            <span>Request Architecture Blueprint</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => onNavigate('ai-company-builder')}
            className={`px-5 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 cursor-pointer ${
              isLight ? 'neu-btn-light text-slate-900' : 'neu-btn-dark text-zinc-200'
            }`}
          >
            <Cpu className="w-4 h-4 text-amber-500" />
            <span>Launch Swarm Builder</span>
          </button>
        </div>

        <button
          onClick={() => onNavigate('technology')}
          className="text-xs font-mono font-bold text-amber-500 hover:text-amber-400 transition-colors py-2 px-3 flex items-center gap-1.5 cursor-pointer"
        >
          <span>View Hardware Specifications</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
