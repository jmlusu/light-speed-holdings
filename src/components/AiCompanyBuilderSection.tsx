import React, { useState } from 'react';
import { 
  Sparkles, 
  ArrowRight, 
  CheckCircle2, 
  Cpu, 
  Users, 
  Workflow, 
  Database, 
  Brain, 
  Zap, 
  ShieldCheck, 
  TrendingUp, 
  Layers,
  ArrowDown,
  Terminal,
  Activity
} from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille, 
  ChassisPanel 
} from './TactileHardwareElements';
import { AiCompanyBuilderOsExplorer } from './AiCompanyBuilderOsExplorer';
import { HaomtgvGovernanceFramework } from './HaomtgvGovernanceFramework';
import aiSwarmInfographic from '../assets/images/ai_builder_swarm_infographic_1789274121556.jpg';

interface AiCompanyBuilderSectionProps {
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const AiCompanyBuilderSection: React.FC<AiCompanyBuilderSectionProps> = ({
  onOpenContactModal,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';
  const [activeTab, setActiveTab] = useState<'operating-model' | 'workforce' | 'architecture' | 'journey' | 'governance'>('operating-model');

  return (
    <section id="ai-company-builder" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto font-sans">
      
      {/* Category Header Chassis */}
      <div className="text-center max-w-3xl mx-auto mb-14">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider mb-4 border select-none">
          <StatusLedPip status="amber" isLight={isLight} />
          <span className={`text-[10px] font-mono tracking-widest ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
            FLAGSHIP OPERATIONAL PILLAR // SYSTEM REF::01
          </span>
        </div>
        <h1 className={`text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-display mb-4 leading-normal sm:leading-tight break-words ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          The <span className="inline-block pb-1.5 text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">AI Company Builder</span>
        </h1>
        <p className={`text-base leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
          LightSpeed Holdings Limited architects the transition from manual, human-bound processes to high-velocity, autonomous enterprises governed by verifiable agentic operating models and resilient telemetry.
        </p>
      </div>

      {/* Strategic Infographic Banner: 144-Agent Governed Swarm Architecture */}
      <div className="relative rounded-3xl overflow-hidden mb-12 border border-zinc-800 shadow-2xl group">
        <img 
          src={aiSwarmInfographic}
          alt="144-Agent Workforce Infographic"
          className="w-full h-[260px] sm:h-[380px] object-cover brightness-[0.75] contrast-[1.1] transition-transform duration-700 group-hover:scale-105"
          referrerPolicy="no-referrer"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent p-6 sm:p-8 flex flex-col justify-end">
          <div className="flex items-center gap-2 mb-1">
            <StatusLedPip status="emerald" isLight={isLight} />
            <span className="text-[10px] font-mono text-amber-400 font-bold uppercase tracking-widest">[ INFOGRAPHIC // SYSTEM ARCHITECTURE ]</span>
          </div>
          <h3 className="text-xl sm:text-2xl font-bold font-display text-white">Governed 144-Agent Swarm &amp; 20-Department Topology</h3>
          <p className="text-xs sm:text-sm text-zinc-300 font-mono mt-1">Autonomous execution swarms operating under human CEO executive oversight and 5-tier HITL gates.</p>
        </div>
      </div>

      {/* Signature Model Comparison Visualizer: Traditional vs LightSpeed AI-Native */}
      <div className={`mb-16 p-6 sm:p-10 rounded-3xl border relative overflow-hidden transition-colors ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

        <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-zinc-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <StatusLedPip status="emerald" isLight={isLight} />
              <span className="text-xs font-mono font-bold text-amber-500 uppercase tracking-wider">
                ARCHITECTURAL COMPARISON MATRIX
              </span>
            </div>
            <h2 className={`text-xl sm:text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              The Paradigm Shift: Traditional vs. AI-Native Enterprise
            </h2>
          </div>
          <AcousticVentGrille cols={5} rows={2} isLight={isLight} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
          
          {/* Traditional Company Panel */}
          <div className={`p-6 sm:p-8 rounded-2xl border flex flex-col justify-between relative overflow-hidden ${
            isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
          }`}>
            <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />
            <div>
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-zinc-800">
                <span className="text-xs font-mono text-zinc-400 uppercase tracking-widest font-bold">LEGACY MODEL [ DEPRECATED ]</span>
                <span className={`px-2.5 py-1 text-[10px] font-mono font-bold rounded ${
                  isLight ? 'bg-slate-200 text-slate-700' : 'bg-zinc-800 text-zinc-400'
                }`}>
                  HUMAN-BOUND CHOPPY FLOW
                </span>
              </div>

              <div className="space-y-3">
                <div className={`p-3.5 rounded-xl border flex items-center justify-between text-xs font-mono ${
                  isLight ? 'bg-white border-slate-300 text-slate-800' : 'bg-zinc-900/80 border-zinc-700/60 text-zinc-300'
                }`}>
                  <div className="flex items-center gap-3">
                    <Users className="w-4 h-4 text-zinc-400" />
                    <span>Human Workforce (Manual coordination)</span>
                  </div>
                </div>
                <div className="flex justify-center"><ArrowDown className="w-4 h-4 text-zinc-500" /></div>
                
                <div className={`p-3.5 rounded-xl border flex items-center justify-between text-xs font-mono ${
                  isLight ? 'bg-white border-slate-300 text-slate-800' : 'bg-zinc-900/80 border-zinc-700/60 text-zinc-300'
                }`}>
                  <div className="flex items-center gap-3">
                    <Workflow className="w-4 h-4 text-zinc-400" />
                    <span>Siloed Manual Hand-offs</span>
                  </div>
                </div>
                <div className="flex justify-center"><ArrowDown className="w-4 h-4 text-zinc-500" /></div>

                <div className={`p-3.5 rounded-xl border flex items-center justify-between text-xs font-mono ${
                  isLight ? 'bg-white border-slate-300 text-slate-800' : 'bg-zinc-900/80 border-zinc-700/60 text-zinc-300'
                }`}>
                  <div className="flex items-center gap-3">
                    <Layers className="w-4 h-4 text-zinc-400" />
                    <span>Static SaaS Silos</span>
                  </div>
                </div>
                <div className="flex justify-center"><ArrowDown className="w-4 h-4 text-zinc-500" /></div>

                <div className={`p-3.5 rounded-xl border flex items-center justify-between text-xs font-mono ${
                  isLight ? 'bg-white border-slate-300 text-slate-800' : 'bg-zinc-900/80 border-zinc-700/60 text-zinc-300'
                }`}>
                  <div className="flex items-center gap-3">
                    <Database className="w-4 h-4 text-zinc-400" />
                    <span>Fragmented Database Islands</span>
                  </div>
                </div>
              </div>
            </div>

            <p className={`mt-8 pt-4 border-t text-xs text-center font-mono ${
              isLight ? 'border-slate-200 text-slate-500' : 'border-zinc-800 text-zinc-500'
            }`}>
              Bottlenecked by human execution speed & manual coordination latency.
            </p>
          </div>

          {/* LightSpeed AI-Native Company Panel */}
          <div className={`p-6 sm:p-8 rounded-2xl border-2 border-amber-500/50 flex flex-col justify-between relative overflow-hidden shadow-xl shadow-amber-500/10 ${
            isLight ? 'bg-amber-50/60 border-amber-500/50' : 'bg-gradient-to-b from-[#18181b] to-[#0d0d10] border-amber-500/50'
          }`}>
            <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />
            <div>
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-amber-500/30">
                <div className="flex items-center gap-2">
                  <StatusLedPip status="emerald" isLight={isLight} />
                  <span className="text-xs font-mono text-amber-500 uppercase tracking-widest font-extrabold">SOVEREIGN AI OPERATING MODEL</span>
                </div>
                <span className="px-2.5 py-1 text-[10px] font-mono font-bold rounded bg-amber-500 text-slate-950">
                  AUTONOMOUS THROUGHPUT
                </span>
              </div>

              <div className="space-y-2.5">
                <div className={`p-3 rounded-xl border flex items-center justify-between text-xs font-mono font-semibold ${
                  isLight ? 'bg-white border-amber-300 text-slate-900' : 'bg-zinc-900/90 border-amber-500/30 text-amber-200'
                }`}>
                  <div className="flex items-center gap-2.5">
                    <Brain className="w-4 h-4 text-amber-500" />
                    <span>Executive Strategic Veto (5-Tier HITL Gate)</span>
                  </div>
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                </div>
                <div className="flex justify-center"><ArrowDown className="w-3.5 h-3.5 text-amber-500" /></div>

                <div className={`p-3 rounded-xl border flex items-center justify-between text-xs font-mono font-semibold ${
                  isLight ? 'bg-white border-amber-300 text-slate-900' : 'bg-zinc-900/90 border-amber-500/30 text-amber-200'
                }`}>
                  <div className="flex items-center gap-2.5">
                    <Cpu className="w-4 h-4 text-amber-500" />
                    <span>Autonomous AI Operating Core</span>
                  </div>
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                </div>
                <div className="flex justify-center"><ArrowDown className="w-3.5 h-3.5 text-amber-500" /></div>

                <div className={`p-3 rounded-xl border flex items-center justify-between text-xs font-mono font-semibold ${
                  isLight ? 'bg-white border-amber-300 text-slate-900' : 'bg-zinc-900/90 border-amber-500/30 text-amber-200'
                }`}>
                  <div className="flex items-center gap-2.5">
                    <Users className="w-4 h-4 text-amber-500" />
                    <span>Agent Workforce Swarms (OpenCode v2)</span>
                  </div>
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                </div>
                <div className="flex justify-center"><ArrowDown className="w-3.5 h-3.5 text-amber-500" /></div>

                <div className={`p-3 rounded-xl border flex items-center justify-between text-xs font-mono font-semibold ${
                  isLight ? 'bg-white border-amber-300 text-slate-900' : 'bg-zinc-900/90 border-amber-500/30 text-amber-200'
                }`}>
                  <div className="flex items-center gap-2.5">
                    <Workflow className="w-4 h-4 text-amber-500" />
                    <span>Collapsed Real-time Task Buses</span>
                  </div>
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                </div>
                <div className="flex justify-center"><ArrowDown className="w-3.5 h-3.5 text-amber-500" /></div>

                <div className={`p-3 rounded-xl border flex items-center justify-between text-xs font-mono font-semibold ${
                  isLight ? 'bg-white border-amber-300 text-slate-900' : 'bg-zinc-900/90 border-amber-500/30 text-amber-200'
                }`}>
                  <div className="flex items-center gap-2.5">
                    <Database className="w-4 h-4 text-amber-500" />
                    <span>Unified Enterprise Semantic Fabric</span>
                  </div>
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                </div>
              </div>
            </div>

            <p className={`mt-8 pt-4 border-t text-xs text-center font-mono font-bold ${
              isLight ? 'border-amber-300 text-amber-700' : 'border-amber-500/30 text-amber-400'
            }`}>
              10x–100x operational throughput with sub-second verified dispatch.
            </p>
          </div>

        </div>
      </div>

      {/* Hardware Control Console Tabs */}
      <div className="mb-14">
        <div className="flex flex-wrap justify-center gap-2.5 pb-4 border-b border-[#e5b74c]/20">
          <button
            onClick={() => setActiveTab('operating-model')}
            className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-2 ${
              activeTab === 'operating-model'
                ? 'bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 shadow-md shadow-amber-500/20'
                : isLight ? 'bg-slate-200 text-slate-700 hover:bg-slate-300' : 'bg-[#0f2231] text-slate-300 hover:bg-[#163246] border border-[#163246]'
            }`}
          >
            <StatusLedPip status={activeTab === 'operating-model' ? 'emerald' : 'off'} isLight={isLight} />
            <span>AI Operating Model</span>
          </button>

          <button
            onClick={() => setActiveTab('workforce')}
            className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-2 ${
              activeTab === 'workforce'
                ? 'bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 shadow-md shadow-amber-500/20'
                : isLight ? 'bg-slate-200 text-slate-700 hover:bg-slate-300' : 'bg-[#0f2231] text-slate-300 hover:bg-[#163246] border border-[#163246]'
            }`}
          >
            <StatusLedPip status={activeTab === 'workforce' ? 'emerald' : 'off'} isLight={isLight} />
            <span>Agent Workforce</span>
          </button>

          <button
            onClick={() => setActiveTab('architecture')}
            className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-2 ${
              activeTab === 'architecture'
                ? 'bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 shadow-md shadow-amber-500/20'
                : isLight ? 'bg-slate-200 text-slate-700 hover:bg-slate-300' : 'bg-[#0f2231] text-slate-300 hover:bg-[#163246] border border-[#163246]'
            }`}
          >
            <StatusLedPip status={activeTab === 'architecture' ? 'emerald' : 'off'} isLight={isLight} />
            <span>Product Factory</span>
          </button>

          <button
            onClick={() => setActiveTab('journey')}
            className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-2 ${
              activeTab === 'journey'
                ? 'bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 shadow-md shadow-amber-500/20'
                : isLight ? 'bg-slate-200 text-slate-700 hover:bg-slate-300' : 'bg-[#0f2231] text-slate-300 hover:bg-[#163246] border border-[#163246]'
            }`}
          >
            <StatusLedPip status={activeTab === 'journey' ? 'emerald' : 'off'} isLight={isLight} />
            <span>Transformation Journey</span>
          </button>

          <button
            onClick={() => setActiveTab('governance')}
            className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-2 ${
              activeTab === 'governance'
                ? 'bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 shadow-md shadow-amber-500/20'
                : isLight ? 'bg-slate-200 text-slate-700 hover:bg-slate-300' : 'bg-[#0f2231] text-slate-300 hover:bg-[#163246] border border-[#163246]'
            }`}
          >
            <StatusLedPip status={activeTab === 'governance' ? 'emerald' : 'off'} isLight={isLight} />
            <span>H-A-O-M-T-G-V Framework</span>
          </button>
        </div>

        {/* Tab Content Chassis */}
        <div className={`mt-6 p-6 sm:p-8 rounded-2xl border transition-colors ${
          isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
        }`}>
          {activeTab === 'governance' && (
            <div className="space-y-4">
              <HaomtgvGovernanceFramework theme={theme} onOpenContactModal={onOpenContactModal} />
            </div>
          )}
          {activeTab === 'operating-model' && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className={`p-5 rounded-xl border ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2 rounded-lg bg-amber-500/10 text-amber-500">
                    <Workflow className="w-5 h-5" />
                  </div>
                  <StatusLedPip status="emerald" isLight={isLight} />
                </div>
                <h3 className={`font-bold font-mono text-sm mb-2 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Workflow Collapse
                </h3>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Eliminates bureaucratic delays by collapsing fragmented multi-step operations into verified, self-executing agent chains governed by deterministic SLA rules.
                </p>
              </div>

              <div className={`p-5 rounded-xl border ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2 rounded-lg bg-amber-500/10 text-amber-500">
                    <ShieldCheck className="w-5 h-5" />
                  </div>
                  <StatusLedPip status="amber" isLight={isLight} />
                </div>
                <h3 className={`font-bold font-mono text-sm mb-2 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Human-in-the-Loop Governance
                </h3>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  5-tier escalation gates ensure high-risk financial, regulatory, or policy operations require human executive review before cryptographic execution.
                </p>
              </div>

              <div className={`p-5 rounded-xl border ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2 rounded-lg bg-amber-500/10 text-amber-500">
                    <Database className="w-5 h-5" />
                  </div>
                  <StatusLedPip status="emerald" isLight={isLight} />
                </div>
                <h3 className={`font-bold font-mono text-sm mb-2 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Semantic Fabric Integration
                </h3>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Connects disparate enterprise ERP systems, relational databases, and regulatory records into an indexed, context-rich knowledge graph.
                </p>
              </div>
            </div>
          )}

          {activeTab === 'workforce' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className={`p-6 rounded-xl border space-y-3 ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-amber-500 uppercase font-bold">ROSTER ARCHITECTURE</span>
                  <StatusLedPip status="emerald" isLight={isLight} />
                </div>
                <h3 className={`text-base font-bold font-mono ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Domain-Expert Agent Swarms
                </h3>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Discarding generic chatbots for custom OpenCode agent cards engineered with explicit permission scopes, canonical tool lists, and isolated execution memory.
                </p>
                <ul className={`space-y-2 text-xs font-mono pt-2 ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Regulatory & Compliance Specialists</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Mobile Settlement & FinTech Auditors</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> AgriTech Telemetry & Supply Chain Agents</li>
                </ul>
              </div>

              <div className={`p-6 rounded-xl border space-y-3 ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-amber-500 uppercase font-bold">DISPATCH PROTOCOL</span>
                  <StatusLedPip status="emerald" isLight={isLight} />
                </div>
                <h3 className={`text-base font-bold font-mono ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Sub-Second Message Bus
                </h3>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Agents communicate across structured task queues with strict runtime deadlines, tamper-evident JSON logging, and automatic deadlock recovery.
                </p>
                <ul className={`space-y-2 text-xs font-mono pt-2 ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Asynchronous execution queues</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Sub-second latency SLA guarantees</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Cryptographic audit trail logs</li>
                </ul>
              </div>
            </div>
          )}

          {activeTab === 'architecture' && (
            <div className="space-y-6">
              <h3 className={`text-lg font-bold font-mono ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                Modular AI Product Factory (Institutional Specs)
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className={`p-4 rounded-xl border text-xs ${
                  isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
                }`}>
                  <h4 className="font-bold font-mono text-amber-500 mb-1">Semantic Layer</h4>
                  <p className={isLight ? 'text-slate-600' : 'text-zinc-400'}>Context graphs linking enterprise documents and relational schemas.</p>
                </div>
                <div className={`p-4 rounded-xl border text-xs ${
                  isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
                }`}>
                  <h4 className="font-bold font-mono text-amber-500 mb-1">Agent Mesh</h4>
                  <p className={isLight ? 'text-slate-600' : 'text-zinc-400'}>Inter-agent communication channels with token budget rate-limiters.</p>
                </div>
                <div className={`p-4 rounded-xl border text-xs ${
                  isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
                }`}>
                  <h4 className="font-bold font-mono text-amber-500 mb-1">Sovereign Gateway</h4>
                  <p className={isLight ? 'text-slate-600' : 'text-zinc-400'}>Local datacenter proxies ensuring data remains within regional borders.</p>
                </div>
                <div className={`p-4 rounded-xl border text-xs ${
                  isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
                }`}>
                  <h4 className="font-bold font-mono text-amber-500 mb-1">Human Console</h4>
                  <p className={isLight ? 'text-slate-600' : 'text-zinc-400'}>Executive dashboard for live approvals and emergency kill-switches.</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'journey' && (
            <div className="space-y-6">
              <h3 className={`text-lg font-bold font-mono ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                The 4-Stage Transformation Journey
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className={`p-5 rounded-xl border ${
                  isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
                }`}>
                  <span className="text-xs font-mono font-bold text-amber-500">[ 01. DISCOVER ]</span>
                  <h4 className={`font-bold text-sm my-1 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Process Audit</h4>
                  <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Identify friction points in manual operations and map initial data schemas.</p>
                </div>
                <div className={`p-5 rounded-xl border ${
                  isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
                }`}>
                  <span className="text-xs font-mono font-bold text-amber-500">[ 02. ARCHITECT ]</span>
                  <h4 className={`font-bold text-sm my-1 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Roster Design</h4>
                  <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Deploy domain sub-agents, enforce tool permissions, and integrate HITL gates.</p>
                </div>
                <div className={`p-5 rounded-xl border ${
                  isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
                }`}>
                  <span className="text-xs font-mono font-bold text-amber-500">[ 03. PILOT ]</span>
                  <h4 className={`font-bold text-sm my-1 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Controlled Run</h4>
                  <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Execute under strict supervision to benchmark response quality and latency.</p>
                </div>
                <div className={`p-5 rounded-xl border ${
                  isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
                }`}>
                  <span className="text-xs font-mono font-bold text-amber-500">[ 04. SCALE ]</span>
                  <h4 className={`font-bold text-sm my-1 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Full Collapse</h4>
                  <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Transition routine workflows to autonomous agent swarms at scale.</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* AI Enterprise Operating System Architecture & IaC Explorer */}
      <AiCompanyBuilderOsExplorer
        theme={theme}
        onOpenContactModal={onOpenContactModal}
      />

      {/* Action CTA Chassis */}
      <div className={`p-6 sm:p-8 rounded-2xl border flex flex-col sm:flex-row items-center justify-between gap-6 transition-colors relative overflow-hidden ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />
        <div className="text-left">
          <div className="flex items-center gap-2 mb-1">
            <StatusLedPip status="emerald" isLight={isLight} />
            <span className="text-[10px] font-mono font-bold text-amber-500 uppercase tracking-wider">
              ENGAGEMENT PROTOCOL
            </span>
          </div>
          <h3 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
            Ready to deploy your AI-Native Company?
          </h3>
          <p className={`text-xs mt-1 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
            Schedule an executive architecture consultation with LightSpeed Holdings Limited engineers.
          </p>
        </div>
        <button
          onClick={() => onOpenContactModal('Discuss a Transformation')}
          className="px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono text-xs uppercase tracking-wider transition-all shadow-md shadow-amber-500/20 active:scale-95 shrink-0 flex items-center gap-2"
        >
          <span>Initiate Consultation</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

    </section>
  );
};
