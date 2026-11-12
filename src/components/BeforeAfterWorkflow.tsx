import React, { useState, useEffect } from 'react';
import {
  Unlink,
  Clock,
  Database,
  RefreshCw,
  FolderArchive,
  ShieldCheck,
  Brain,
  GitBranch,
  HardDrive,
  UserCheck,
  Zap,
  Sparkles,
  Layers,
  ChevronRight,
  AlertTriangle,
  CheckCircle2,
  Lock,
  Puzzle,
  Settings,
  BarChart2,
  Trophy,
  Play,
  RotateCcw,
  Info,
  X,
  ArrowRight,
  Activity,
  Sliders,
  Cpu,
  Eye
} from 'lucide-react';

interface BeforeAfterWorkflowProps {
  theme?: 'light' | 'dark';
}

interface WorkflowPair {
  id: number;
  category: 'execution' | 'intelligence' | 'governance';
  categoryLabel: string;
  traditional: {
    title: string;
    desc: string;
    icon: React.ComponentType<{ className?: string }>;
    metric: string;
    riskLevel: 'Critical' | 'High' | 'Severe';
  };
  lightspeed: {
    title: string;
    desc: string;
    icon: React.ComponentType<{ className?: string }>;
    metric: string;
    haomtgvPillar: string;
    governanceTier: string;
  };
  deepDive: {
    problemAnalysis: string;
    solutionMechanism: string;
    quantifiedImpact: string;
  };
}

const WORKFLOW_PAIRS: WorkflowPair[] = [
  {
    id: 1,
    category: 'execution',
    categoryLabel: 'Execution & Tools',
    traditional: {
      title: 'Disconnected Tools',
      desc: 'Fragmented toolchain requiring manual setup, API glue, and handoffs.',
      icon: Layers,
      metric: '14+ SaaS Silos',
      riskLevel: 'Severe',
    },
    lightspeed: {
      title: 'Governed Execution',
      desc: 'Deterministic workflows with enterprise-grade controls.',
      icon: GitBranch,
      metric: 'Single Execution Graph',
      haomtgvPillar: 'Tools & Orchestration',
      governanceTier: 'Level 5 Deterministic',
    },
    deepDive: {
      problemAnalysis: 'Data must be copied across incompatible web apps, spreadsheet exports, and manual email threads, creating extreme surface area for compliance breaches.',
      solutionMechanism: 'LightSpeed replaces fragmented APIs with a unified HAOMTGV tool router that validates permissions prior to any system mutation.',
      quantifiedImpact: '94% reduction in manual setup time; 100% encrypted trace logging.',
    },
  },
  {
    id: 2,
    category: 'execution',
    categoryLabel: 'Execution & Tools',
    traditional: {
      title: 'Manual Handoffs',
      desc: 'Tasks move between teams, increasing delay, friction, and human error.',
      icon: Clock,
      metric: '4.8 Days Avg Delay',
      riskLevel: 'Critical',
    },
    lightspeed: {
      title: 'Contextual Intelligence',
      desc: 'AI-driven decisions with full institutional context.',
      icon: Brain,
      metric: '< 250ms Response',
      haomtgvPillar: 'Agents & Memory',
      governanceTier: 'Level 4 Context Aware',
    },
    deepDive: {
      problemAnalysis: 'Cross-departmental approvals stall in queues for days while context is repeatedly re-explained to new reviewers.',
      solutionMechanism: 'Autonomous AI agents equipped with vector-indexed organizational memory process inputs instantaneously and flag only true anomalies for human oversight.',
      quantifiedImpact: 'Eliminates 98% of approval latency while maintaining strict human-in-the-loop decision checkpoints.',
    },
  },
  {
    id: 3,
    category: 'intelligence',
    categoryLabel: 'Intelligence & Context',
    traditional: {
      title: 'Fragmented Information',
      desc: 'Critical context scattered across disparate systems and unindexed files.',
      icon: Puzzle,
      metric: '35% Information Loss',
      riskLevel: 'High',
    },
    lightspeed: {
      title: 'Orchestrated Workflows',
      desc: 'Multi-step tasks executed seamlessly across multi-agent networks.',
      icon: Lock,
      metric: '100% Context Synthesis',
      haomtgvPillar: 'Orchestration',
      governanceTier: 'Level 5 Zero-Trust',
    },
    deepDive: {
      problemAnalysis: 'Employees spend up to 20% of workweeks searching for files, historical decisions, or system status across Slack, Drive, and Jira.',
      solutionMechanism: 'LightSpeed orchestrates persistent memory graphs that continuously synthesize real-time data into actionable, audit-ready operational state.',
      quantifiedImpact: 'Zero lost context across shift handoffs and cross-functional task executions.',
    },
  },
  {
    id: 4,
    category: 'governance',
    categoryLabel: 'Governance & Oversight',
    traditional: {
      title: 'Reactive Coordination',
      desc: 'Operational failures addressed after damage occurs due to blind spots.',
      icon: Settings,
      metric: 'Post-Mortem Only',
      riskLevel: 'Severe',
    },
    lightspeed: {
      title: 'Tiered Approval Memory',
      desc: 'Human oversight at every critical threshold with tamper-proof logging.',
      icon: HardDrive,
      metric: 'Pre-Execution Audit',
      haomtgvPillar: 'Governance',
      governanceTier: 'Level 5 Audit Verified',
    },
    deepDive: {
      problemAnalysis: 'Legacy operations rely on periodic compliance audits that catch violations weeks or months after execution.',
      solutionMechanism: 'Deterministic policy gates intercept high-risk actions before execution, enforcing tiered approval requirements based on transaction value and sensitivity.',
      quantifiedImpact: '100% pre-execution policy enforcement; zero compliance surprises.',
    },
  },
  {
    id: 5,
    category: 'governance',
    categoryLabel: 'Governance & Oversight',
    traditional: {
      title: 'Limited Organizational Memory',
      desc: 'Institutional knowledge lost when personnel churn or change roles.',
      icon: BarChart2,
      metric: 'High Attrition Risk',
      riskLevel: 'High',
    },
    lightspeed: {
      title: 'Human-Directed Execution',
      desc: 'Trusted outcomes under direct executive control and strategy.',
      icon: Trophy,
      metric: 'Immutable Knowledge',
      haomtgvPillar: 'Human Authority & Value',
      governanceTier: 'Level 5 Executive Directed',
    },
    deepDive: {
      problemAnalysis: 'Critical domain knowledge lives in individual minds, leaving the enterprise vulnerable when key team members leave.',
      solutionMechanism: 'LightSpeed captures operational patterns into reusable, version-controlled execution recipes that continuously improve while preserving human oversight.',
      quantifiedImpact: 'Permanent preservation of operational capital and strategy execution.',
    },
  },
];

export const BeforeAfterWorkflow: React.FC<BeforeAfterWorkflowProps> = ({ theme = 'dark' }) => {
  const isLight = theme === 'light';

  // Interactive States
  const [activePairId, setActivePairId] = useState<number | null>(null);
  const [activeFilter, setActiveFilter] = useState<'all' | 'execution' | 'intelligence' | 'governance'>('all');
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [simStep, setSimStep] = useState<number>(0);
  const [inspectorPair, setInspectorPair] = useState<WorkflowPair | null>(null);

  // Filtered Items
  const visiblePairs = WORKFLOW_PAIRS.filter(
    (p) => activeFilter === 'all' || p.category === activeFilter
  );

  // Live Simulation Controller
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isSimulating) {
      if (simStep < WORKFLOW_PAIRS.length) {
        timer = setTimeout(() => {
          setActivePairId(WORKFLOW_PAIRS[simStep].id);
          setSimStep((prev) => prev + 1);
        }, 800);
      } else {
        timer = setTimeout(() => {
          setIsSimulating(false);
          setSimStep(0);
        }, 1200);
      }
    }
    return () => clearTimeout(timer);
  }, [isSimulating, simStep]);

  const handleStartSimulation = () => {
    setIsSimulating(true);
    setSimStep(0);
    setActivePairId(WORKFLOW_PAIRS[0].id);
  };

  const handleReset = () => {
    setIsSimulating(false);
    setSimStep(0);
    setActivePairId(null);
  };

  return (
    <section
      id="workflow-collapsing"
      className={`py-24 px-4 sm:px-6 lg:px-12 relative overflow-hidden transition-colors duration-300 ${
        isLight
          ? 'bg-[#F2F2F2] text-[#070A40]'
          : 'bg-[#070A40] text-white selection:bg-[#00BFFF] selection:text-[#070A40]'
      }`}
    >
      {/* Background Architectural Atmosphere & Sector Background */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <img
          src="/brand/digital/Homepage_Hero_High_fidelity.jpeg"
          alt=""
          aria-hidden="true"
          className="w-full h-full object-cover object-center opacity-40 dark:opacity-55 transition-opacity duration-500 filter brightness-95"
          loading="lazy"
          referrerPolicy="no-referrer"
        />

        {/* Scrim Overlay for Optimal Contrast (Lightened for enhanced clarity) */}
        <div
          className={`absolute inset-0 transition-colors duration-500 ${
            isLight
              ? 'bg-gradient-to-b from-[#F2F2F2]/65 via-[#F2F2F2]/40 to-[#F2F2F2]/70'
              : 'bg-gradient-to-b from-[#070A40]/70 via-[#070A40]/45 to-[#070A40]/75'
          }`}
        />

        {/* Ambient Glow Accents (Red & Cyan) */}
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-[#E63946]/15 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute top-1/3 -right-32 w-96 h-96 bg-[#00BFFF]/15 rounded-full blur-[120px] pointer-events-none" />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">

        {/* =========================================================================
            SECTION HEADER
            ========================================================================= */}
        <div className="text-center max-w-4xl mx-auto mb-12 space-y-5">

          {/* Category Badge */}
          <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full border text-xs font-mono font-bold tracking-widest uppercase shadow-lg ${
            isLight ? 'bg-white border-slate-300 text-[#070A40]' : 'bg-[#070A40]/90 border-slate-700/80 text-slate-200'
          }`}>
            <span className="w-2 h-2 rounded-sm bg-[#E63946] rotate-45 animate-pulse" />
            <span>WORKFLOW COLLAPSING ARCHITECTURE</span>
          </div>

          {/* Main Title with Cyan Accent */}
          <h2 className={`text-3xl sm:text-5xl lg:text-6xl font-black font-display tracking-tight leading-tight ${
            isLight ? 'text-[#070A40]' : 'text-white'
          }`}>
            The Shift to{' '}
            <span className="bg-gradient-to-r from-[#00BFFF] via-[#38BDF8] to-[#00BFFF] bg-clip-text text-transparent drop-shadow-[0_2px_12px_rgba(0,191,255,0.4)]">
              Governed AI-Native
            </span>{' '}
            Operations
          </h2>

          {/* Supporting Copy */}
          <p className={`text-base sm:text-lg leading-relaxed max-w-3xl mx-auto font-sans font-medium ${
            isLight ? 'text-[#6B7280]' : 'text-[#9CA3AF]'
          }`}>
            LightSpeed collapses multi-step operational friction, fragmented SaaS silos, and manual handoffs into deterministic, governed execution graphs.
          </p>

          {/* Corporate Tagline & Cyan Dividers */}
          <div className="pt-1 flex items-center justify-center gap-4 text-xs font-mono tracking-widest text-[#00BFFF] font-bold">
            <div className="h-px w-16 sm:w-28 bg-gradient-to-r from-transparent via-[#00BFFF]/60 to-[#00BFFF]" />
            <span className="text-[#00BFFF] drop-shadow-[0_0_8px_rgba(0,191,255,0.4)]">
              ASPIRE. ACT. ACHIEVE.
            </span>
            <div className="h-px w-16 sm:w-28 bg-gradient-to-l from-transparent via-[#00BFFF]/60 to-[#00BFFF]" />
          </div>
        </div>

        {/* =========================================================================
            INTERACTIVE CONTROLS BAR (Filters & Simulation Trigger)
            ========================================================================= */}
        <div className="mb-10 flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl border backdrop-blur-xl transition-all duration-300 shadow-lg ${
          isLight ? 'bg-white/80 border-slate-200' : 'bg-[#070A40]/80 border-white/10'
        }">
          {/* Filter Tabs */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono font-bold text-[#9CA3AF] uppercase mr-2 flex items-center gap-1">
              <Sliders className="w-3.5 h-3.5 text-[#00BFFF]" />
              Filter:
            </span>
            {[
              { id: 'all', label: 'All Operations' },
              { id: 'execution', label: 'Execution & Tools' },
              { id: 'intelligence', label: 'Intelligence & Context' },
              { id: 'governance', label: 'Governance & Oversight' },
            ].map((tab) => {
              const isActive = activeFilter === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveFilter(tab.id as any)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all duration-200 cursor-pointer ${
                    isActive
                      ? 'bg-[#00BFFF] text-[#070A40] shadow-md shadow-[#00BFFF]/30 scale-105'
                      : isLight
                      ? 'bg-slate-100 text-[#070A40] hover:bg-slate-200'
                      : 'bg-white/5 text-slate-300 hover:bg-white/10'
                  }`}
                >
                  {tab.label}
                </button>
              );
            })}
          </div>

          {/* Interactive Simulation Button */}
          <div className="flex items-center gap-3">
            {isSimulating ? (
              <button
                onClick={handleReset}
                className="px-4 py-2 rounded-xl bg-red-950/80 border border-[#E63946] text-[#E63946] text-xs font-mono font-bold flex items-center gap-2 shadow-lg cursor-pointer hover:bg-red-900/80 transition-all"
              >
                <RotateCcw className="w-4 h-4 animate-spin text-[#E63946]" />
                <span>Simulating... ({simStep}/5) - Stop</span>
              </button>
            ) : (
              <button
                onClick={handleStartSimulation}
                className="px-5 py-2 rounded-xl bg-gradient-to-r from-[#00BFFF] to-blue-600 text-[#070A40] text-xs font-mono font-extrabold flex items-center gap-2 shadow-lg shadow-[#00BFFF]/30 cursor-pointer hover:scale-105 transition-all duration-200"
              >
                <Play className="w-4 h-4 fill-current text-[#070A40]" />
                <span>Simulate Workflow Collapse</span>
              </button>
            )}

            {activePairId !== null && (
              <button
                onClick={() => setActivePairId(null)}
                className="px-3 py-2 rounded-xl text-xs font-mono text-slate-400 hover:text-white transition-colors cursor-pointer"
                title="Clear Selection"
              >
                Clear Focus
              </button>
            )}
          </div>
        </div>

        {/* =========================================================================
            COMPARISON CONTAINER (3-COLUMN DESKTOP SPLIT)
            ========================================================================= */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 items-center relative">

          {/* ─────────────────────────────────────────────────────────────
              LEFT PANEL: TRADITIONAL OPERATIONS (Red #E63946 Theme)
              ───────────────────────────────────────────────────────────── */}
          <div className={`lg:col-span-5 rounded-3xl p-6 sm:p-8 relative overflow-hidden transition-all duration-300 backdrop-blur-2xl border shadow-2xl ${
            isLight
              ? 'bg-white/95 border-[#E63946]/30 shadow-red-500/10'
              : 'bg-[#070A40]/90 border-[#E63946]/40 shadow-[0_0_50px_rgba(230,57,70,0.2)]'
          }`}>
            {/* Corner Ambient Glow Accent */}
            <div className="absolute top-0 left-0 w-32 h-32 bg-[#E63946]/20 rounded-br-full blur-2xl pointer-events-none" />

            {/* Header Lockup */}
            <div className="flex items-center justify-between pb-5 border-b border-[#E63946]/20">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-[#E63946] to-red-950 p-0.5 shadow-lg shadow-[#E63946]/30 flex items-center justify-center shrink-0">
                  <div className={`w-full h-full rounded-[14px] flex items-center justify-center ${
                    isLight ? 'bg-red-50 text-[#E63946]' : 'bg-[#120407] text-[#E63946]'
                  }`}>
                    <Layers className="w-6 h-6 text-[#E63946]" />
                  </div>
                </div>

                <div>
                  <h3 className={`text-xl sm:text-2xl font-black font-display ${
                    isLight ? 'text-[#070A40]' : 'text-white'
                  }`}>
                    Traditional Operations
                  </h3>
                  <p className="text-[11px] font-mono font-bold text-[#E63946] tracking-widest uppercase mt-0.5">
                    FRAGMENTED · SLOW · SILOED
                  </p>
                </div>
              </div>
            </div>

            {/* Kicker Subhead */}
            <p className={`text-xs font-mono mt-4 mb-5 ${
              isLight ? 'text-[#6B7280]' : 'text-[#9CA3AF]'
            }`}>
              Click or hover any operational challenge to inspect governance solution:
            </p>

            {/* Traditional Challenge Cards */}
            <div className="space-y-3">
              {visiblePairs.map((pair) => {
                const item = pair.traditional;
                const IconComp = item.icon;
                const isFocused = activePairId === pair.id;

                return (
                  <div
                    key={pair.id}
                    onClick={() => {
                      setActivePairId(pair.id);
                      setInspectorPair(pair);
                    }}
                    onMouseEnter={() => !isSimulating && setActivePairId(pair.id)}
                    className={`p-3.5 rounded-2xl border transition-all duration-300 flex items-center justify-between gap-3 group cursor-pointer ${
                      isFocused
                        ? isLight
                          ? 'bg-red-50 border-[#E63946] shadow-lg translate-x-1.5 ring-2 ring-[#E63946]/50'
                          : 'bg-red-950/70 border-[#E63946] shadow-xl shadow-red-950/70 translate-x-1.5 ring-2 ring-[#E63946]/50'
                        : isLight
                        ? 'bg-[#F2F2F2]/80 border-slate-200 text-[#070A40] hover:bg-red-50/50'
                        : 'bg-white/[0.03] border-white/10 text-white hover:bg-white/[0.06]'
                    }`}
                  >
                    <div className="flex items-center gap-3.5 min-w-0">
                      {/* 3D Red Badge */}
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 border transition-transform duration-300 ${
                        isFocused
                          ? 'scale-110 bg-[#E63946] border-[#E63946] text-white shadow-md'
                          : isLight
                          ? 'bg-red-100 border-[#E63946]/30 text-[#E63946]'
                          : 'bg-red-950/40 border-[#E63946]/30 text-[#E63946]'
                      }`}>
                        <IconComp className="w-5 h-5" />
                      </div>

                      <div className="text-left min-w-0">
                        <div className="flex items-center gap-2">
                          <h4 className={`text-sm font-bold font-display ${
                            isLight ? 'text-[#070A40]' : 'text-white'
                          }`}>
                            {item.title}
                          </h4>
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-red-950/40 text-[#E63946] border border-[#E63946]/30 font-semibold shrink-0">
                            {item.metric}
                          </span>
                        </div>
                        <p className={`text-xs leading-snug line-clamp-2 mt-0.5 ${
                          isLight ? 'text-[#6B7280]' : 'text-[#9CA3AF]'
                        }`}>
                          {item.desc}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-1.5 shrink-0">
                      <Eye className={`w-4 h-4 transition-all duration-200 ${
                        isFocused ? 'text-[#E63946] scale-110' : 'text-slate-500 opacity-0 group-hover:opacity-100'
                      }`} />
                      <ChevronRight className={`w-4 h-4 transition-transform duration-300 ${
                        isFocused ? 'text-[#E63946] translate-x-1' : 'text-slate-400'
                      }`} />
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Bottom Warning Banner */}
            <div className="mt-6 pt-4 border-t border-[#E63946]/20">
              <div className={`py-2.5 px-4 rounded-xl border flex items-center justify-between gap-2 text-xs font-mono font-bold text-[#E63946] ${
                isLight ? 'bg-red-50 border-[#E63946]/30' : 'bg-red-950/40 border-[#E63946]/30'
              }`}>
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 shrink-0 animate-pulse text-[#E63946]" />
                  <span>Higher Risk. Greater Friction.</span>
                </div>
                <span className="text-[10px] opacity-75">Siloed Bottlenecks</span>
              </div>
            </div>
          </div>

          {/* ─────────────────────────────────────────────────────────────
              CENTRAL ARCHITECTURE HUB (Visual Centerpiece & Interactive Switch)
              ───────────────────────────────────────────────────────────── */}
          <div className="lg:col-span-2 flex flex-col items-center justify-center my-6 lg:my-0 relative select-none z-20">

            {/* SVG Connecting Circuit Traces */}
            <div className="hidden lg:block absolute inset-0 -mx-12 pointer-events-none">
              <svg viewBox="0 0 200 500" className="w-full h-full">
                <defs>
                  <filter id="hub-glow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="4" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                  </filter>
                </defs>

                {/* Dynamic Circuit Paths for 5 Pairs */}
                {[
                  { yStart: 70, yMid: 220, id: 1 },
                  { yStart: 150, yMid: 235, id: 2 },
                  { yStart: 250, yMid: 250, id: 3 },
                  { yStart: 350, yMid: 265, id: 4 },
                  { yStart: 430, yMid: 280, id: 5 },
                ].map((trace) => {
                  const isHighlighted = activePairId === trace.id;
                  return (
                    <g key={trace.id}>
                      {/* Red Incoming Trace */}
                      <path
                        d={`M 0,${trace.yStart} L 60,${trace.yStart} L 100,${trace.yMid}`}
                        fill="none"
                        stroke={isHighlighted ? '#E63946' : '#E63946'}
                        strokeWidth={isHighlighted ? '3.5' : '2'}
                        strokeOpacity={isHighlighted ? '1' : '0.4'}
                        className={isHighlighted ? 'animate-pulse' : ''}
                      />
                      {/* Cyan Outgoing Trace */}
                      <path
                        d={`M 200,${trace.yStart} L 140,${trace.yStart} L 100,${trace.yMid}`}
                        fill="none"
                        stroke={isHighlighted ? '#00BFFF' : '#00BFFF'}
                        strokeWidth={isHighlighted ? '3.5' : '2'}
                        strokeOpacity={isHighlighted ? '1' : '0.4'}
                        filter="url(#hub-glow)"
                        className={isHighlighted ? 'animate-pulse' : ''}
                      />
                    </g>
                  );
                })}
              </svg>
            </div>

            {/* Vertical Radiant Light Pillar Effect */}
            <div className={`absolute -inset-y-12 w-20 transition-opacity duration-300 blur-xl pointer-events-none ${
              activePairId !== null ? 'bg-gradient-to-b from-[#00BFFF]/40 via-[#00BFFF]/60 to-[#070A40]/0 opacity-100' : 'bg-gradient-to-b from-[#00BFFF]/0 via-[#00BFFF]/20 to-[#070A40]/0 opacity-50'
            }`} />

            {/* 3D Tiered Pedestal Hub (Interactive Trigger) */}
            <button
              onClick={handleStartSimulation}
              className="relative group flex flex-col items-center cursor-pointer focus:outline-none"
              title="Click to simulate workflow collapse transformation"
            >
              {/* Outer Cyan Ring Pedestal */}
              <div className={`w-36 h-36 sm:w-44 sm:h-44 rounded-full p-1 bg-gradient-to-tr from-[#00BFFF] via-[#38BDF8] to-white transition-all duration-300 ${
                isSimulating
                  ? 'shadow-[0_0_60px_rgba(0,191,255,0.9)] scale-110 ring-4 ring-[#00BFFF]'
                  : activePairId !== null
                  ? 'shadow-[0_0_50px_rgba(0,191,255,0.7)] scale-105'
                  : 'shadow-[0_0_40px_rgba(0,191,255,0.5)] group-hover:scale-105'
              } flex items-center justify-center relative`}>

                {/* Inner Glowing Cyan/Navy Glass Circle */}
                <div className={`w-full h-full rounded-full border-2 border-[#00BFFF]/60 flex flex-col items-center justify-center p-3 text-center shadow-inner relative overflow-hidden ${
                  isLight
                    ? 'bg-gradient-to-b from-[#F2F2F2] via-white to-cyan-50'
                    : 'bg-gradient-to-b from-[#0B1A48] via-[#070A40] to-[#04102B]'
                }`}>

                  {/* Subtle Shimmer & Inner Glow */}
                  <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,_var(--tw-gradient-stops))] from-[#00BFFF]/25 via-transparent to-transparent pointer-events-none" />

                  {/* LightSpeed 3D Emblem Mark */}
                  <div className="w-10 h-10 sm:w-12 sm:h-12 mb-1 relative flex items-center justify-center">
                    <img
                      src="/logo-icon-v2.svg"
                      alt="LightSpeed"
                      className={`w-full h-full object-contain filter drop-shadow-[0_0_10px_rgba(0,191,255,0.8)] ${
                        isSimulating ? 'animate-bounce' : 'animate-pulse'
                      }`}
                    />
                  </div>

                  {/* Brand Wordmark */}
                  <span className={`font-extrabold font-display text-xs sm:text-sm tracking-wider ${
                    isLight ? 'text-[#070A40]' : 'text-white'
                  }`}>
                    LightSpeed
                  </span>

                  {/* Architecture Identifier */}
                  <span className="text-[9px] font-mono font-bold text-[#00BFFF] tracking-widest uppercase mt-0.5">
                    {isSimulating ? `STEP ${simStep}/5` : 'HAOMTGV'}
                  </span>
                </div>
              </div>

              {/* Multi-Tiered Metallic Cyan/Navy Base Plates */}
              <div className="w-28 sm:w-36 h-3 bg-gradient-to-r from-[#070A40] via-[#00BFFF] to-[#070A40] rounded-b-xl border-t border-[#00BFFF]/50 shadow-lg -mt-1" />
              <div className="w-36 sm:w-44 h-2.5 bg-gradient-to-r from-[#04102B] via-[#00BFFF]/70 to-[#04102B] rounded-b-xl border-t border-[#00BFFF]/30 shadow-md -mt-0.5" />
            </button>
          </div>

          {/* ─────────────────────────────────────────────────────────────
              RIGHT PANEL: LIGHTSPEED AI-NATIVE FLOW (Cyan #00BFFF Theme)
              ───────────────────────────────────────────────────────────── */}
          <div className={`lg:col-span-5 rounded-3xl p-6 sm:p-8 relative overflow-hidden transition-all duration-300 backdrop-blur-2xl border shadow-2xl ${
            isLight
              ? 'bg-white/95 border-[#00BFFF]/30 shadow-cyan-500/10'
              : 'bg-[#070A40]/90 border-[#00BFFF]/40 shadow-[0_0_50px_rgba(0,191,255,0.25)]'
          }`}>
            {/* Corner Ambient Cyan Glow Accent */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-[#00BFFF]/20 rounded-bl-full blur-2xl pointer-events-none" />

            {/* Header Lockup */}
            <div className="flex items-center justify-between pb-5 border-b border-[#00BFFF]/20">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-[#00BFFF] to-blue-900 p-0.5 shadow-lg shadow-[#00BFFF]/30 flex items-center justify-center shrink-0">
                  <div className={`w-full h-full rounded-[14px] flex items-center justify-center ${
                    isLight ? 'bg-cyan-50 text-[#00BFFF]' : 'bg-[#030d1a] text-[#00BFFF]'
                  }`}>
                    <ShieldCheck className="w-6 h-6 text-[#00BFFF]" />
                  </div>
                </div>

                <div>
                  <h3 className={`text-xl sm:text-2xl font-black font-display ${
                    isLight ? 'text-[#070A40]' : 'text-white'
                  }`}>
                    LightSpeed AI-Native Flow
                  </h3>
                  <p className="text-[11px] font-mono font-bold text-[#00BFFF] tracking-widest uppercase mt-0.5">
                    CONNECTED · INTELLIGENT · GOVERNED
                  </p>
                </div>
              </div>
            </div>

            {/* Kicker Subhead */}
            <p className={`text-xs font-mono mt-4 mb-5 ${
              isLight ? 'text-[#6B7280]' : 'text-[#9CA3AF]'
            }`}>
              Unified, governed, and observable execution.
            </p>

            {/* LightSpeed Capability Cards */}
            <div className="space-y-3">
              {visiblePairs.map((pair) => {
                const item = pair.lightspeed;
                const IconComp = item.icon;
                const isFocused = activePairId === pair.id;

                return (
                  <div
                    key={pair.id}
                    onClick={() => {
                      setActivePairId(pair.id);
                      setInspectorPair(pair);
                    }}
                    onMouseEnter={() => !isSimulating && setActivePairId(pair.id)}
                    className={`p-3.5 rounded-2xl border transition-all duration-300 flex items-center justify-between gap-3 group cursor-pointer ${
                      isFocused
                        ? isLight
                          ? 'bg-cyan-50 border-[#00BFFF] shadow-lg -translate-x-1.5 ring-2 ring-[#00BFFF]/50'
                          : 'bg-cyan-950/70 border-[#00BFFF] shadow-xl shadow-cyan-950/70 -translate-x-1.5 ring-2 ring-[#00BFFF]/50'
                        : isLight
                        ? 'bg-[#F2F2F2]/80 border-slate-200 text-[#070A40] hover:bg-cyan-50/50'
                        : 'bg-white/[0.03] border-white/10 text-white hover:bg-white/[0.06]'
                    }`}
                  >
                    <div className="flex items-center gap-3.5 min-w-0">
                      {/* 3D Cyan Badge */}
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 border transition-transform duration-300 ${
                        isFocused
                          ? 'scale-110 bg-[#00BFFF] border-[#00BFFF] text-[#070A40] shadow-md'
                          : isLight
                          ? 'bg-cyan-100 border-[#00BFFF]/30 text-[#00BFFF]'
                          : 'bg-cyan-950/40 border-[#00BFFF]/30 text-[#00BFFF]'
                      }`}>
                        <IconComp className="w-5 h-5" />
                      </div>

                      <div className="text-left min-w-0">
                        <div className="flex items-center gap-2">
                          <h4 className={`text-sm font-bold font-display ${
                            isLight ? 'text-[#070A40]' : 'text-white'
                          }`}>
                            {item.title}
                          </h4>
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950/40 text-[#00BFFF] border border-[#00BFFF]/30 font-semibold shrink-0">
                            {item.metric}
                          </span>
                        </div>
                        <p className={`text-xs leading-snug line-clamp-2 mt-0.5 ${
                          isLight ? 'text-[#6B7280]' : 'text-[#9CA3AF]'
                        }`}>
                          {item.desc}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-1.5 shrink-0">
                      <Eye className={`w-4 h-4 transition-all duration-200 ${
                        isFocused ? 'text-[#00BFFF] scale-110' : 'text-slate-500 opacity-0 group-hover:opacity-100'
                      }`} />
                      <ChevronRight className={`w-4 h-4 transition-transform duration-300 ${
                        isFocused ? 'text-[#00BFFF] translate-x-1' : 'text-slate-400'
                      }`} />
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Bottom Statement Banner */}
            <div className="mt-6 pt-4 border-t border-[#00BFFF]/20">
              <div className={`py-2.5 px-4 rounded-xl border flex items-center justify-between gap-2 text-xs font-mono font-bold text-[#00BFFF] ${
                isLight ? 'bg-cyan-50 border-[#00BFFF]/30' : 'bg-cyan-950/40 border-[#00BFFF]/30'
              }`}>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 shrink-0 text-[#00BFFF]" />
                  <span>Greater Control. Higher Productivity.</span>
                </div>
                <span className="text-[10px] opacity-75">100% Governed</span>
              </div>
            </div>
          </div>

        </div>

        {/* =========================================================================
            BOTTOM ENTERPRISE FOOTER TAGLINE
            ========================================================================= */}
        <div className="mt-16 text-center space-y-2">
          <div className="flex items-center justify-center gap-4 text-xs font-mono tracking-widest text-[#00BFFF] font-bold">
            <div className="h-px w-20 sm:w-36 bg-gradient-to-r from-transparent via-[#00BFFF]/60 to-[#00BFFF]" />
            <span className="text-[#00BFFF] uppercase tracking-widest text-xs font-extrabold drop-shadow-[0_0_8px_rgba(0,191,255,0.4)]">
              A GOVERNED AI-NATIVE ENTERPRISE
            </span>
            <div className="h-px w-20 sm:w-36 bg-gradient-to-l from-transparent via-[#00BFFF]/60 to-[#00BFFF]" />
          </div>

          <p className={`text-xs font-mono font-bold tracking-[0.25em] uppercase ${
            isLight ? 'text-[#6B7280]' : 'text-[#9CA3AF]'
          }`}>
            BUILT FOR WHAT'S NEXT
          </p>
        </div>

      </div>

      {/* =========================================================================
          INTERACTIVE INSPECTOR MODAL DRAWER
          ========================================================================= */}
      {inspectorPair && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
          <div className={`max-w-2xl w-full rounded-3xl p-6 sm:p-8 border shadow-2xl relative overflow-hidden ${
            isLight ? 'bg-white text-[#070A40] border-slate-300' : 'bg-[#070A40] text-white border-[#00BFFF]/40'
          }`}>
            {/* Top Accent Bar */}
            <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-[#E63946] via-[#00BFFF] to-[#E63946]" />

            {/* Modal Header */}
            <div className="flex items-center justify-between pb-4 border-b border-white/10 mb-6">
              <div className="flex items-center gap-3">
                <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-[#00BFFF]/20 text-[#00BFFF] border border-[#00BFFF]/40">
                  {inspectorPair.lightspeed.haomtgvPillar}
                </span>
                <span className="text-xs font-mono text-slate-400">
                  HAOMTGV Inspection
                </span>
              </div>
              <button
                onClick={() => setInspectorPair(null)}
                className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors cursor-pointer"
              >
                <X className="w-4 h-4 text-white" />
              </button>
            </div>

            {/* Side-by-Side Comparison Breakdown */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
              {/* Traditional Challenge */}
              <div className="p-4 rounded-2xl bg-red-950/30 border border-[#E63946]/30 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-bold text-[#E63946] uppercase">
                    Traditional Bottleneck
                  </span>
                  <span className="text-[10px] font-mono text-red-400">
                    Risk: {inspectorPair.traditional.riskLevel}
                  </span>
                </div>
                <h4 className="text-base font-bold text-white font-display">
                  {inspectorPair.traditional.title}
                </h4>
                <p className="text-xs text-slate-300">
                  {inspectorPair.traditional.desc}
                </p>
                <div className="pt-2 text-xs font-mono text-red-400 font-bold">
                  Impact: {inspectorPair.traditional.metric}
                </div>
              </div>

              {/* LightSpeed Governed Solution */}
              <div className="p-4 rounded-2xl bg-cyan-950/30 border border-[#00BFFF]/40 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-bold text-[#00BFFF] uppercase">
                    LightSpeed Collapsed Graph
                  </span>
                  <span className="text-[10px] font-mono text-cyan-300">
                    {inspectorPair.lightspeed.governanceTier}
                  </span>
                </div>
                <h4 className="text-base font-bold text-white font-display">
                  {inspectorPair.lightspeed.title}
                </h4>
                <p className="text-xs text-slate-300">
                  {inspectorPair.lightspeed.desc}
                </p>
                <div className="pt-2 text-xs font-mono text-[#00BFFF] font-bold">
                  Result: {inspectorPair.lightspeed.metric}
                </div>
              </div>
            </div>

            {/* Deep Dive Details */}
            <div className="space-y-3 p-4 rounded-2xl bg-white/[0.03] border border-white/10 text-xs">
              <div>
                <span className="font-bold text-[#E63946] font-mono">Structural Problem:</span>
                <p className="text-slate-300 mt-0.5">{inspectorPair.deepDive.problemAnalysis}</p>
              </div>
              <div className="pt-2 border-t border-white/10">
                <span className="font-bold text-[#00BFFF] font-mono">LightSpeed Mechanism:</span>
                <p className="text-slate-300 mt-0.5">{inspectorPair.deepDive.solutionMechanism}</p>
              </div>
              <div className="pt-2 border-t border-white/10">
                <span className="font-bold text-emerald-400 font-mono">Quantified Enterprise Impact:</span>
                <p className="text-emerald-300 font-semibold mt-0.5">{inspectorPair.deepDive.quantifiedImpact}</p>
              </div>
            </div>

            {/* Modal Actions */}
            <div className="mt-6 flex items-center justify-end gap-3 pt-4 border-t border-white/10">
              <button
                onClick={() => {
                  setInspectorPair(null);
                  handleStartSimulation();
                }}
                className="px-4 py-2 rounded-xl bg-[#00BFFF] text-[#070A40] text-xs font-mono font-bold flex items-center gap-2 hover:scale-105 transition-all cursor-pointer"
              >
                <Play className="w-3.5 h-3.5 fill-current text-[#070A40]" />
                <span>Simulate Transformation</span>
              </button>
              <button
                onClick={() => setInspectorPair(null)}
                className="px-4 py-2 rounded-xl bg-white/10 text-slate-200 text-xs font-mono font-bold hover:bg-white/20 transition-all cursor-pointer"
              >
                Close Inspector
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default BeforeAfterWorkflow;
