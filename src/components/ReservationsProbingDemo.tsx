import React, { useState } from 'react';
import { 
  Wifi, 
  WifiOff, 
  ShieldCheck, 
  Database, 
  Lock, 
  AlertTriangle, 
  CheckCircle2, 
  FileText, 
  ArrowRight, 
  Terminal, 
  Layers, 
  RefreshCw, 
  Cpu, 
  Zap, 
  Sparkles, 
  UserCheck, 
  Building2, 
  Globe2, 
  HelpCircle,
  Clock,
  ChevronRight,
  Play
} from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille 
} from './TactileHardwareElements';

interface ReservationsProbingDemoProps {
  theme?: 'light' | 'dark';
  onOpenContactModal?: (intent?: string) => void;
}

export const ReservationsProbingDemo: React.FC<ReservationsProbingDemoProps> = ({
  theme = 'dark',
  onOpenContactModal
}) => {
  const isLight = theme === 'light';
  
  // Active beat state (0 to 5)
  const [activeBeat, setActiveBeat] = useState<number>(0);

  // Beat 1 State (Network Simulation)
  const [networkMode, setNetworkMode] = useState<'4g' | '3g' | 'offline'>('3g');
  const [syncedActions, setSyncedActions] = useState<number>(4);
  const [queuedActions, setQueuedActions] = useState<number>(0);
  const [isLocalModelFallback, setIsLocalModelFallback] = useState<boolean>(true);

  // Beat 2 State (Governance Gates)
  const [activeGate, setActiveGate] = useState<'G1' | 'G2' | 'G3' | 'G4'>('G1');

  // Beat 3 State (Legacy Stack Adapter)
  const [selectedAdapter, setSelectedAdapter] = useState<'kobo' | 'dhis2' | 'postgres' | 'excel'>('kobo');
  const [techDebtPaid, setTechDebtPaid] = useState<boolean>(true);

  // Beat 4 State (HITL Gate & Audit)
  const [hitlTriggered, setHitlTriggered] = useState<boolean>(false);
  const [promptInjectionBlocked, setPromptInjectionBlocked] = useState<boolean>(true);
  const [auditLogCount, setAuditLogCount] = useState<number>(2373);

  const handleSimulateAction = () => {
    if (networkMode === 'offline') {
      setQueuedActions(prev => prev + 1);
    } else {
      setSyncedActions(prev => prev + 1);
    }
  };

  const handleTriggerHitlAction = () => {
    setHitlTriggered(true);
    setAuditLogCount(prev => prev + 1);
  };

  return (
    <section className={`p-6 sm:p-10 rounded-3xl border relative overflow-hidden transition-all my-12 ${
      isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
    }`}>
      <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
      <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
      <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
      <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

      {/* Header & Title */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-zinc-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <StatusLedPip status="emerald" isLight={isLight} />
            <span className="text-[10px] font-mono font-bold text-amber-500 uppercase tracking-widest">
              CLIENT DEMO SUITE // RESERVATIONS-PROBING SCRIPT V1.0
            </span>
          </div>
          <h2 className={`text-xl sm:text-3xl font-extrabold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
            The Interactive Reservations-Probing Demo
          </h2>
          <p className={`text-xs sm:text-sm mt-1 max-w-2xl ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
            Test our platform live against the 4 core reservations decision-makers hold: low connectivity, data sovereignty, legacy stack integration, and trust/governance.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <AcousticVentGrille cols={6} rows={2} isLight={isLight} />
        </div>
      </div>

      {/* Beat Selector Stepper */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2 mb-8">
        {[
          { id: 0, title: 'Beat 0', label: 'Capability DNA' },
          { id: 1, title: 'Beat 1', label: '3G / Offline' },
          { id: 2, title: 'Beat 2', label: 'Data Sovereignty' },
          { id: 3, title: 'Beat 3', label: 'Legacy Stack' },
          { id: 4, title: 'Beat 4', label: 'Trust & HITL' },
          { id: 5, title: 'Beat 5', label: 'Discovery Close' }
        ].map((beat) => {
          const isActive = activeBeat === beat.id;
          return (
            <button
              key={beat.id}
              onClick={() => setActiveBeat(beat.id)}
              className={`p-3 rounded-xl border text-left transition-all cursor-pointer select-none ${
                isActive
                  ? 'bg-amber-500 text-slate-950 border-amber-400 font-extrabold shadow-lg shadow-amber-500/20 scale-[1.02]'
                  : isLight
                  ? 'bg-slate-200/70 border-slate-300 text-slate-700 hover:bg-slate-200'
                  : 'bg-zinc-900/80 border-zinc-800 text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200'
              }`}
            >
              <div className="text-[9px] font-mono uppercase tracking-wider opacity-80">{beat.title}</div>
              <div className="text-xs font-bold font-mono truncate">{beat.label}</div>
            </button>
          );
        })}
      </div>

      {/* Beat Display Viewport */}
      <div className={`p-6 sm:p-8 rounded-2xl border relative overflow-hidden transition-all ${
        isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />

        {/* ================= BEAT 0: CAPABILITY FRAME ================= */}
        {activeBeat === 0 && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
              <div>
                <span className="text-[10px] font-mono font-bold text-amber-500 uppercase tracking-widest">
                  BEAT 0 // CAPABILITY DNA & PEDIGREE
                </span>
                <h3 className={`text-lg sm:text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Institutional Engineering Discipline
                </h3>
              </div>
              <span className="px-3 py-1 rounded-full text-[10px] font-mono font-bold bg-purple-500/10 text-purple-400 border border-purple-500/30">
                Honesty Badge: Proven In-House
              </span>
            </div>

            <p className={`text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
              LightSpeed Holdings Limited is an AI-native company builder. We have architected data platforms for enterprise telecom, finance, and healthcare organizations — including regulated digital platforms — and delivered health-program data systems in low-connectivity field settings across district health offices. The same engineering discipline that shipped those estates ships inside everything we show you today.
            </p>

            {/* Talk Track Quote Box */}
            <div className={`p-4 rounded-xl border italic text-xs ${
              isLight ? 'bg-amber-50/80 border-amber-300 text-amber-950' : 'bg-amber-500/10 border-amber-500/30 text-amber-200'
            }`}>
              <span className="font-mono font-bold not-italic block text-[10px] text-amber-500 uppercase mb-1">
                EXECUTIVE TALK TRACK
              </span>
              &ldquo;We establish pedigree without personal biography. Never name an individual; never say &lsquo;the CEO&rsquo; — say &lsquo;our engineering discipline.&rsquo;&rdquo;
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="text-amber-500 font-mono text-lg font-bold mb-1">144 Agents</div>
                <div className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>143 AI Specialist Agents + 1 Human CEO operating across 20 departments.</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="text-amber-500 font-mono text-lg font-bold mb-1">2,373 Tests</div>
                <div className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Passing regression suite verifying state, security, and workflow dispatch.</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="text-amber-500 font-mono text-lg font-bold mb-1">Zero-Cloud Boundary</div>
                <div className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Sovereign in-country processing default for state, health, and financial data.</div>
              </div>
            </div>
          </div>
        )}

        {/* ================= BEAT 1: 3G / OFFLINE ================= */}
        {activeBeat === 1 && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
              <div>
                <span className="text-[10px] font-mono font-bold text-amber-500 uppercase tracking-widest">
                  BEAT 1 // RESERVATION 1: LOW-BANDWIDTH & OFFLINE-FIRST
                </span>
                <h3 className={`text-lg sm:text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  &ldquo;Show it on 3G, and show it offline.&rdquo;
                </h3>
              </div>
              <span className="px-3 py-1 rounded-full text-[10px] font-mono font-bold bg-blue-500/10 text-blue-400 border border-blue-500/30">
                Honesty Badge: Proven In-House
              </span>
            </div>

            {/* Interactive Network Switcher */}
            <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl border bg-black/40 border-zinc-800">
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono font-bold text-zinc-400 uppercase">SIMULATE CONNECTION:</span>
                <div className="inline-flex rounded-lg border border-zinc-800 p-1 bg-zinc-900">
                  <button
                    onClick={() => setNetworkMode('4g')}
                    className={`px-3 py-1 rounded-md text-xs font-mono font-bold transition-all ${
                      networkMode === '4g' ? 'bg-emerald-500 text-slate-950' : 'text-zinc-400 hover:text-zinc-200'
                    }`}
                  >
                    4G / LTE
                  </button>
                  <button
                    onClick={() => setNetworkMode('3g')}
                    className={`px-3 py-1 rounded-md text-xs font-mono font-bold transition-all ${
                      networkMode === '3g' ? 'bg-amber-500 text-slate-950' : 'text-zinc-400 hover:text-zinc-200'
                    }`}
                  >
                    3G Throttled
                  </button>
                  <button
                    onClick={() => setNetworkMode('offline')}
                    className={`px-3 py-1 rounded-md text-xs font-mono font-bold transition-all ${
                      networkMode === 'offline' ? 'bg-red-500 text-white' : 'text-zinc-400 hover:text-zinc-200'
                    }`}
                  >
                    Offline (Air-Gapped)
                  </button>
                </div>
              </div>

              <button
                onClick={handleSimulateAction}
                className="px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-mono font-bold text-xs uppercase tracking-wider transition-all flex items-center gap-2 cursor-pointer"
              >
                <Zap className="w-4 h-4" />
                <span>Simulate Field Transaction</span>
              </button>
            </div>

            {/* Network Status Simulation Panel */}
            <div className={`p-5 rounded-xl border transition-all ${
              networkMode === 'offline' 
                ? 'bg-red-500/10 border-red-500/40 text-red-200' 
                : networkMode === '3g'
                ? 'bg-amber-500/10 border-amber-500/40 text-amber-200'
                : 'bg-emerald-500/10 border-emerald-500/40 text-emerald-200'
            }`}>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  {networkMode === 'offline' ? (
                    <WifiOff className="w-5 h-5 text-red-400 animate-pulse" />
                  ) : (
                    <Wifi className="w-5 h-5 text-amber-400" />
                  )}
                  <span className="font-mono font-bold text-xs uppercase tracking-wider">
                    CURRENT STATE: {networkMode === '4g' ? 'HIGH-SPEED BROADBAND' : networkMode === '3g' ? 'THROTTLED 3G [QUOTA-FIRST ROUTING]' : 'AIR-GAPPED OFFLINE CLIENT [PWA QUEUE]'}
                  </span>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-black/40 border border-white/10">
                  {networkMode === 'offline' ? 'DISCONNECTED' : 'LATENCY: 420ms'}
                </span>
              </div>

              {networkMode === 'offline' && (
                <div className="p-3 rounded-lg bg-red-900/40 border border-red-500/50 text-xs font-mono text-red-100 mb-3 flex items-center justify-between">
                  <span>⚠️ You are offline. Changes will sync automatically when reconnected.</span>
                  <span className="px-2 py-0.5 rounded bg-red-500 text-white font-bold">{queuedActions} QUEUED</span>
                </div>
              )}

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
                <div className="p-3 rounded bg-black/30 border border-white/10">
                  <span className="text-zinc-500 block text-[10px]">SYNCED TRANSACTIONS</span>
                  <span className="font-bold text-emerald-400 text-sm">{syncedActions} Executed</span>
                </div>
                <div className="p-3 rounded bg-black/30 border border-white/10">
                  <span className="text-zinc-500 block text-[10px]">OFFLINE QUEUE (PWA)</span>
                  <span className="font-bold text-amber-400 text-sm">{queuedActions} Pending Sync</span>
                </div>
                <div className="p-3 rounded bg-black/30 border border-white/10">
                  <span className="text-zinc-500 block text-[10px]">LOCAL INFERENCE</span>
                  <span className="font-bold text-purple-400 text-sm">Ollama Llama3 (Free Local)</span>
                </div>
              </div>
            </div>

            {/* Talk Track Quote Box */}
            <div className={`p-4 rounded-xl border italic text-xs ${
              isLight ? 'bg-amber-50/80 border-amber-300 text-amber-950' : 'bg-amber-500/10 border-amber-500/30 text-amber-200'
            }`}>
              <span className="font-mono font-bold not-italic block text-[10px] text-amber-500 uppercase mb-1">
                EXECUTIVE TALK TRACK
              </span>
              &ldquo;We design for the reality. Bandwidth is a budget; latency is a constraint we engineer to. Everything you just saw runs on the architecture we run on every day.&rdquo;
            </div>
          </div>
        )}

        {/* ================= BEAT 2: DATA SOVEREIGNTY ================= */}
        {activeBeat === 2 && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
              <div>
                <span className="text-[10px] font-mono font-bold text-amber-500 uppercase tracking-widest">
                  BEAT 2 // RESERVATION 2: DATA SOVEREIGNTY & BOUNDARIES
                </span>
                <h3 className={`text-lg sm:text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  &ldquo;Where does our data live?&rdquo;
                </h3>
              </div>
              <span className="px-3 py-1 rounded-full text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30">
                In Active Development (G1–G4 Gates)
              </span>
            </div>

            <p className={`text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
              Your data stays on your infrastructure. Sovereign, in-country processing is the default. Malawi Data Protection Act 2017/2024 and GDPR compliance are built in from day one, and we never use client data to train models. Every cross-border flow is documented — there is no mystery ledger.
            </p>

            {/* Interactive Gate Stepper */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { id: 'G1', title: 'Gate G1', name: 'Contract & Scope' },
                { id: 'G2', title: 'Gate G2', name: 'DPA & Privacy' },
                { id: 'G3', title: 'Gate G3', name: 'Compliance Review' },
                { id: 'G4', title: 'Gate G4', name: 'Security & Audit' }
              ].map((gate) => {
                const isActive = activeGate === gate.id;
                return (
                  <button
                    key={gate.id}
                    onClick={() => setActiveGate(gate.id as any)}
                    className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
                      isActive
                        ? 'bg-amber-500 text-slate-950 border-amber-400 font-bold shadow-md'
                        : isLight
                        ? 'bg-slate-100 border-slate-300 text-slate-700'
                        : 'bg-zinc-900 border-zinc-800 text-zinc-400'
                    }`}
                  >
                    <div className="text-[10px] font-mono font-bold uppercase">{gate.title}</div>
                    <div className="text-xs font-bold font-mono truncate">{gate.name}</div>
                  </button>
                );
              })}
            </div>

            {/* Gate Details Panel */}
            <div className={`p-5 rounded-xl border font-mono text-xs ${
              isLight ? 'bg-slate-100 border-slate-300 text-slate-800' : 'bg-zinc-900 border-zinc-800 text-zinc-300'
            }`}>
              <div className="flex items-center justify-between border-b border-zinc-800 pb-2 mb-3">
                <span className="font-bold text-amber-500">GOVERNANCE GATE DETAILS :: [{activeGate}]</span>
                <span className="text-[10px] text-emerald-400 font-bold">VERIFIED BY APPROVALGATE</span>
              </div>

              {activeGate === 'G1' && (
                <div>
                  <h4 className="font-bold text-sm mb-1 text-slate-900 dark:text-zinc-100">G1: Contractual Scope & Liability Cap</h4>
                  <p className="text-zinc-400 text-xs mb-3">Establishes clear liability boundaries, deliverable specs, and non-disclosure covenants before workspace activation.</p>
                  <div className="p-2 rounded bg-black/40 border border-white/10 text-[11px] text-amber-300">
                    STATUS: MANDATORY FOR ALL ENGAGEMENTS // EXECUTED ON-SOIL
                  </div>
                </div>
              )}

              {activeGate === 'G2' && (
                <div>
                  <h4 className="font-bold text-sm mb-1 text-slate-900 dark:text-zinc-100">G2: Data Processing Agreement (DPA) & Cross-Border Consent</h4>
                  <p className="text-zinc-400 text-xs mb-3">Enforces explicit consent workflows for donor, state, or patient PII transfers to LLM providers. Zero-training guarantee enforced.</p>
                  <div className="p-2 rounded bg-black/40 border border-white/10 text-[11px] text-emerald-300">
                    STATUS: DPA 2017/2024 & GDPR ALIGNED // NO CLIENT DATA MODEL TRAINING
                  </div>
                </div>
              )}

              {activeGate === 'G3' && (
                <div>
                  <h4 className="font-bold text-sm mb-1 text-slate-900 dark:text-zinc-100">G3: Regulatory & Industry Compliance Review</h4>
                  <p className="text-zinc-400 text-xs mb-3">Audits workflow templates against SADC regional guidelines, MACRA telecoms regulations, and financial inclusion directives.</p>
                  <div className="p-2 rounded bg-black/40 border border-white/10 text-[11px] text-purple-300">
                    STATUS: AI ETHICS BOARD TIER 3+ REVIEW TRIGGER
                  </div>
                </div>
              )}

              {activeGate === 'G4' && (
                <div>
                  <h4 className="font-bold text-sm mb-1 text-slate-900 dark:text-zinc-100">G4: Security Assessment & Cryptographic Key Validation</h4>
                  <p className="text-zinc-400 text-xs mb-3">Verifies RBAC key rotation, memory encryption at rest, and zero-trust proxy routing to local datacenters.</p>
                  <div className="p-2 rounded bg-black/40 border border-white/10 text-[11px] text-blue-300">
                    STATUS: 2,373 INTEGRATION TESTS PASSING // AUDIT LOG READY
                  </div>
                </div>
              )}
            </div>

            {/* Talk Track Quote Box */}
            <div className={`p-4 rounded-xl border italic text-xs ${
              isLight ? 'bg-amber-50/80 border-amber-300 text-amber-950' : 'bg-amber-500/10 border-amber-500/30 text-amber-200'
            }`}>
              <span className="font-mono font-bold not-italic block text-[10px] text-amber-500 uppercase mb-1">
                EXECUTIVE TALK TRACK
              </span>
              &ldquo;Your data stays on your infrastructure. Sovereign, in-country processing is the default. Data Protection Act 2017/2024 and GDPR are built in from day one, and we never use client data to train models. Every cross-border flow is documented — there is no mystery ledger.&rdquo;
            </div>
          </div>
        )}

        {/* ================= BEAT 3: LEGACY STACK ================= */}
        {activeBeat === 3 && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
              <div>
                <span className="text-[10px] font-mono font-bold text-amber-500 uppercase tracking-widest">
                  BEAT 3 // RESERVATION 3: LEGACY STACK INTEGRATION
                </span>
                <h3 className={`text-lg sm:text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  &ldquo;What happens to our legacy stack?&rdquo;
                </h3>
              </div>
              <span className="px-3 py-1 rounded-full text-[10px] font-mono font-bold bg-blue-500/10 text-blue-400 border border-blue-500/30">
                Honesty Badge: Proven In-House
              </span>
            </div>

            <p className={`text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
              Adopting AI should not mean ripping out what works. The 90-day pilot integrates with your existing stack via non-invasive API connectors and leaves it in place. And we hold ourselves to the same rule — our own engineering debt is tracked, reviewed, and paid down.
            </p>

            {/* Legacy Adapter Selector */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { id: 'kobo', name: 'KoboToolbox M&E', type: 'REST API' },
                { id: 'dhis2', name: 'DHIS2 Health DB', type: 'GraphQL / Webhook' },
                { id: 'postgres', name: 'PostgreSQL ERP', type: 'SQL Connector' },
                { id: 'excel', name: 'Excel / CSV Sheets', type: 'File Pipeline' }
              ].map((adapter) => {
                const isActive = selectedAdapter === adapter.id;
                return (
                  <button
                    key={adapter.id}
                    onClick={() => setSelectedAdapter(adapter.id as any)}
                    className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
                      isActive
                        ? 'bg-amber-500 text-slate-950 border-amber-400 font-bold shadow-md'
                        : isLight
                        ? 'bg-slate-100 border-slate-300 text-slate-700'
                        : 'bg-zinc-900 border-zinc-800 text-zinc-400'
                    }`}
                  >
                    <div className="text-[10px] font-mono uppercase text-zinc-500">{adapter.type}</div>
                    <div className="text-xs font-bold font-mono truncate">{adapter.name}</div>
                  </button>
                );
              })}
            </div>

            {/* Adapter Pipeline Visualizer */}
            <div className={`p-5 rounded-xl border font-mono text-xs ${
              isLight ? 'bg-slate-100 border-slate-300 text-slate-800' : 'bg-zinc-900 border-zinc-800 text-zinc-300'
            }`}>
              <div className="flex items-center justify-between border-b border-zinc-800 pb-2 mb-3">
                <span className="font-bold text-amber-500">ADAPTER SEAM PIPELINE :: [{selectedAdapter.toUpperCase()}]</span>
                <span className="text-[10px] text-emerald-400 font-bold">NO RIP-AND-REPLACE</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                <div className="p-3 rounded bg-black/30 border border-white/10">
                  <div className="text-[10px] text-zinc-500">1. SOURCE SYSTEM</div>
                  <div className="font-bold text-amber-400 text-xs mt-1">{selectedAdapter.toUpperCase()} READ-ONLY SEAM</div>
                </div>
                <div className="p-3 rounded bg-black/30 border border-white/10 flex flex-col justify-center items-center">
                  <div className="text-[10px] text-zinc-500">2. AGENTIC TRANSFORM</div>
                  <div className="font-bold text-emerald-400 text-xs mt-1">144-AGENT ORCHESTRATOR</div>
                </div>
                <div className="p-3 rounded bg-black/30 border border-white/10">
                  <div className="text-[10px] text-zinc-500">3. EXECUTIVE OUTPUT</div>
                  <div className="font-bold text-purple-400 text-xs mt-1">AUTOMATED NARRATIVE REPORT</div>
                </div>
              </div>
            </div>

            {/* Talk Track Quote Box */}
            <div className={`p-4 rounded-xl border italic text-xs ${
              isLight ? 'bg-amber-50/80 border-amber-300 text-amber-950' : 'bg-amber-500/10 border-amber-500/30 text-amber-200'
            }`}>
              <span className="font-mono font-bold not-italic block text-[10px] text-amber-500 uppercase mb-1">
                EXECUTIVE TALK TRACK
              </span>
              &ldquo;Adopting AI should not mean ripping out what works. The 90-day pilot integrates with your existing stack and leaves it in place. And we hold ourselves to the same rule — our own debt is tracked, reviewed, and paid down. There is no system-of-systems we quietly stick you with.&rdquo;
            </div>
          </div>
        )}

        {/* ================= BEAT 4: TRUST & HITL ================= */}
        {activeBeat === 4 && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
              <div>
                <span className="text-[10px] font-mono font-bold text-amber-500 uppercase tracking-widest">
                  BEAT 4 // RESERVATION 4: GOVERNANCE & TRUST
                </span>
                <h3 className={`text-lg sm:text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  &ldquo;How do we trust it?&rdquo;
                </h3>
              </div>
              <span className="px-3 py-1 rounded-full text-[10px] font-mono font-bold bg-purple-500/10 text-purple-400 border border-purple-500/30">
                Honesty Badge: Proven In-House
              </span>
            </div>

            <p className={`text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
              Most AI failures here are governance failures, not technology failures. Our governance is the architecture: approvals before irreversible actions, an unchangeable audit trail after, and risk controls graded to what moves. The system earns a Chief Risk Officer&apos;s yes before a user&apos;s wow — and we never fabricate proof.
            </p>

            {/* HITL Simulation Trigger */}
            <div className="p-4 rounded-xl border bg-black/40 border-zinc-800 flex flex-wrap items-center justify-between gap-4">
              <div>
                <span className="text-xs font-mono font-bold text-amber-500 block uppercase">5-TIER APPROVAL GATE SIMULATOR</span>
                <span className="text-xs text-zinc-400">Trigger a high-risk financial procurement or policy deployment to view the HITL lock.</span>
              </div>

              <button
                onClick={handleTriggerHitlAction}
                className="px-4 py-2 rounded-lg bg-red-500 hover:bg-red-400 text-white font-mono font-bold text-xs uppercase tracking-wider transition-all flex items-center gap-2 cursor-pointer shadow-lg shadow-red-500/20"
              >
                <Lock className="w-4 h-4" />
                <span>Simulate High-Risk Action</span>
              </button>
            </div>

            {/* HITL Gate Simulation Display */}
            {hitlTriggered ? (
              <div className="p-5 rounded-xl border bg-amber-500/10 border-amber-500/40 text-amber-200 font-mono text-xs space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Lock className="w-5 h-5 text-amber-400 animate-bounce" />
                    <span className="font-bold uppercase text-sm">APPROVALGATE BLOCKED :: [HIGH_RISK_ACTION]</span>
                  </div>
                  <span className="px-2 py-0.5 rounded bg-amber-500 text-slate-950 font-bold">STATUS: PENDING HUMAN CEO SIGN-OFF</span>
                </div>
                <p className="text-zinc-300">
                  Agent requested disbursement of MWK 2,500,000 for procurement. Action rated RISK_LEVEL::CRITICAL (5x5 matrix score = 20). Executor thread paused for up to 30 minutes.
                </p>
                <div className="p-3 rounded bg-black/60 border border-white/10 text-[11px] text-zinc-400">
                  <div>[AUDIT_EVENT_ID]: evt_20260912_8a5a657a</div>
                  <div>[MUTATION]: ApprovalGate.block_executor(thread_id=&quot;task-481&quot;, timeout=1800s)</div>
                  <div>[LOG_TYPE]: Append-only JSONL event written to audit trail.</div>
                </div>
              </div>
            ) : (
              <div className="p-5 rounded-xl border bg-zinc-900 border-zinc-800 text-zinc-400 font-mono text-xs text-center">
                Click &ldquo;Simulate High-Risk Action&rdquo; above to see the 5-Tier Human-in-the-Loop Approval Gate block execution live.
              </div>
            )}

            {/* Red Team Prompt Injection Rejection */}
            <div className={`p-4 rounded-xl border font-mono text-xs flex items-center justify-between ${
              promptInjectionBlocked ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-red-500/10 border-red-500/30 text-red-300'
            }`}>
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-emerald-400" />
                <span>RED-TEAM SECURITY EVAL: Prompt-injection attempt rejected by system prompt guardrails.</span>
              </div>
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold text-[10px]">PASSING</span>
            </div>

            {/* Talk Track Quote Box */}
            <div className={`p-4 rounded-xl border italic text-xs ${
              isLight ? 'bg-amber-50/80 border-amber-300 text-amber-950' : 'bg-amber-500/10 border-amber-500/30 text-amber-200'
            }`}>
              <span className="font-mono font-bold not-italic block text-[10px] text-amber-500 uppercase mb-1">
                EXECUTIVE TALK TRACK
              </span>
              &ldquo;Most AI failures here are governance failures, not technology failures. Our governance is the architecture: approvals before irreversible actions, an unchangeable audit trail after, and risk controls graded to what moves. The system earns a Chief Risk Officer&apos;s yes before a user&apos;s wow — and we never fabricate proof. Every claim carries its honest status.&rdquo;
            </div>
          </div>
        )}

        {/* ================= BEAT 5: DISCOVERY CLOSE ================= */}
        {activeBeat === 5 && (
          <div className="space-y-6 text-center max-w-2xl mx-auto py-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30 mb-2">
              <Sparkles className="w-3.5 h-3.5" />
              <span>BEAT 5 // DISCOVERY CLOSE & CO-ARCHITECTURE</span>
            </div>

            <h3 className={`text-2xl sm:text-3xl font-extrabold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              Co-Architect Your Governed AI Workforce
            </h3>

            <p className={`text-sm leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              We don&apos;t sell hours; we sell outcomes. Book a Discovery Call with LightSpeed Holdings engineers to evaluate a 90-day pilot tailored to your organization&apos;s specific data, governance, and operating context.
            </p>

            <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
              <button
                onClick={() => onOpenContactModal && onOpenContactModal('Book a Discovery Call')}
                className="px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono text-xs uppercase tracking-wider transition-all shadow-xl shadow-amber-500/20 active:scale-95 flex items-center gap-2 cursor-pointer"
              >
                <span>Book a Discovery Call</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

      </div>
    </section>
  );
};
