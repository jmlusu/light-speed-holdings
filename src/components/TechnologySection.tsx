import React, { useState } from 'react';
import { 
  Cpu, 
  Database, 
  Terminal, 
  Code2, 
  Activity, 
  ShieldCheck, 
  CheckCircle2, 
  ArrowRight, 
  Server, 
  Network, 
  Lock, 
  Copy, 
  Check, 
  ExternalLink,
  Layers,
  Radio
} from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille, 
  ChassisPanel 
} from './TactileHardwareElements';
import technologySovereignArch from '../assets/images/technology_sovereign_architecture_1789274135850.jpg';

interface TechnologySectionProps {
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const TechnologySection: React.FC<TechnologySectionProps> = ({
  onOpenContactModal,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';
  const [activeTechTab, setActiveTechTab] = useState<'architecture' | 'agent-cards' | 'benchmarks' | 'semantic'>('architecture');
  const [copiedCode, setCopiedCode] = useState<string | null>(null);

  const sampleYamlCard = `name: Pharos_Policy_Specialist
version: 2.4.0
mode: subagent
permission: Tier 3 (Dual Sign-off Required)
tools:
  - read
  - edit
  - grep
  - list
  - bash
  - webfetch
  - task
system_prompt: |
  You are the Pharos Policy & Governance Agent for LightSpeed Holdings Limited.
  Validate sovereign policy submissions against SADC model laws and Malawi
  Department of E-Government standards. Enforce 100% human-in-the-loop
  auditability for Chichewa/English bilingual language models.
environment:
  SADC_POLICY_DB_URI: "postgres://sadc_legal_proxy:5432/sovereign_policy"
  AUDIT_LOG_STREAM: "kafka://audit-bus.lightspeed.mw:9092/policy-events"`;

  const handleCopyCode = (code: string, id: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  return (
    <section id="technology" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto font-sans">
      
      {/* Title & Classification */}
      <div className="text-center max-w-3xl mx-auto mb-14">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider mb-4 border select-none">
          <StatusLedPip status="emerald" isLight={isLight} />
          <span className={`text-[10px] font-mono tracking-widest ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
            SOVEREIGN HARDWARE & KERNEL ARCHITECTURE // VERIFIED
          </span>
        </div>
        <h2 className={`text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-display mb-4 leading-normal sm:leading-tight break-words ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          <span className="inline-block pb-1.5 text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">Technology Stack</span>
        </h2>
        <p className={`text-base leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
          Open, verifiable, and benchmarked computational engineering for enterprise AI operating models, semantic data fabrics, and sovereign African deployments.
        </p>
      </div>

      {/* Strategic Infographic Banner: Sovereign Technology Architecture */}
      <div className="relative rounded-3xl overflow-hidden mb-12 border border-zinc-800 shadow-2xl group">
        <img 
          src={technologySovereignArch}
          alt="Sovereign Architecture Diagram Infographic"
          className="w-full h-[260px] sm:h-[360px] object-cover brightness-[0.75] contrast-[1.1] transition-transform duration-700 group-hover:scale-105"
          referrerPolicy="no-referrer"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent p-6 sm:p-8 flex flex-col justify-end">
          <div className="flex items-center gap-2 mb-1">
            <StatusLedPip status="emerald" isLight={isLight} />
            <span className="text-[10px] font-mono text-amber-400 font-bold uppercase tracking-widest">[ TECHNICAL DIAGRAM // INFOGRAPHIC ]</span>
          </div>
          <h3 className="text-xl sm:text-2xl font-bold font-display text-white">Sovereign Datacenter &amp; Offline-First PWA Synchronization</h3>
          <p className="text-xs sm:text-sm text-zinc-300 font-mono mt-1">Air-gapped local model proxies, Pydantic type validation, and zero-cloud data containment.</p>
        </div>
      </div>

      {/* Tech Tabs Navigation Console */}
      <div className="flex flex-wrap justify-center gap-2.5 pb-4 mb-8 border-b border-zinc-800">
        <button
          onClick={() => setActiveTechTab('architecture')}
          className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-2 ${
            activeTechTab === 'architecture'
              ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20'
              : isLight ? 'bg-slate-200 text-slate-700 hover:bg-slate-300' : 'bg-zinc-900 text-zinc-300 hover:bg-zinc-800'
          }`}
        >
          <StatusLedPip status={activeTechTab === 'architecture' ? 'emerald' : 'off'} isLight={isLight} />
          <span>4-Layer Architecture</span>
        </button>

        <button
          onClick={() => setActiveTechTab('agent-cards')}
          className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-2 ${
            activeTechTab === 'agent-cards'
              ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20'
              : isLight ? 'bg-slate-200 text-slate-700 hover:bg-slate-300' : 'bg-zinc-900 text-zinc-300 hover:bg-zinc-800'
          }`}
        >
          <StatusLedPip status={activeTechTab === 'agent-cards' ? 'emerald' : 'off'} isLight={isLight} />
          <span>OpenCode Agent Specs</span>
        </button>

        <button
          onClick={() => setActiveTechTab('benchmarks')}
          className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-2 ${
            activeTechTab === 'benchmarks'
              ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20'
              : isLight ? 'bg-slate-200 text-slate-700 hover:bg-slate-300' : 'bg-zinc-900 text-zinc-300 hover:bg-zinc-800'
          }`}
        >
          <StatusLedPip status={activeTechTab === 'benchmarks' ? 'emerald' : 'off'} isLight={isLight} />
          <span>Telemetry Benchmarks</span>
        </button>

        <button
          onClick={() => setActiveTechTab('semantic')}
          className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-2 ${
            activeTechTab === 'semantic'
              ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20'
              : isLight ? 'bg-slate-200 text-slate-700 hover:bg-slate-300' : 'bg-zinc-900 text-zinc-300 hover:bg-zinc-800'
          }`}
        >
          <StatusLedPip status={activeTechTab === 'semantic' ? 'emerald' : 'off'} isLight={isLight} />
          <span>Semantic Fabric & RBAC</span>
        </button>
      </div>

      {/* Main Tech Chassis Console */}
      <div className={`p-6 sm:p-10 rounded-3xl border relative overflow-hidden transition-colors ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />
        
        {/* Architecture Overview */}
        {activeTechTab === 'architecture' && (
          <div className="space-y-8">
            <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-zinc-800">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <StatusLedPip status="emerald" isLight={isLight} />
                  <span className="text-xs font-mono font-bold text-amber-500 uppercase tracking-wider">
                    LAYERED SOVEREIGN STACK
                  </span>
                </div>
                <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  4-Layer Sovereign Enterprise Architecture
                </h3>
              </div>
              <AcousticVentGrille cols={5} rows={2} isLight={isLight} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className={`p-5 rounded-xl border ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono text-amber-500 font-extrabold uppercase">[ LAYER 01 ]</span>
                  <StatusLedPip status="emerald" isLight={isLight} />
                </div>
                <h4 className={`font-bold font-mono text-sm my-1 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Human Console</h4>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Executive dashboard, 5-tier HITL approval gates, veto controls, and real-time SLA monitors.</p>
              </div>

              <div className={`p-5 rounded-xl border ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono text-amber-500 font-extrabold uppercase">[ LAYER 02 ]</span>
                  <StatusLedPip status="emerald" isLight={isLight} />
                </div>
                <h4 className={`font-bold font-mono text-sm my-1 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Orchestration Bus</h4>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Asynchronous JSON task queue, message bus, token budget guard, and sub-350ms task dispatcher.</p>
              </div>

              <div className={`p-5 rounded-xl border ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono text-amber-500 font-extrabold uppercase">[ LAYER 03 ]</span>
                  <StatusLedPip status="amber" isLight={isLight} />
                </div>
                <h4 className={`font-bold font-mono text-sm my-1 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Semantic Graph</h4>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Vector indexing, ERP connectors, SADC policy models, and Chichewa/English bilingual embeddings.</p>
              </div>

              <div className={`p-5 rounded-xl border ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono text-amber-500 font-extrabold uppercase">[ LAYER 04 ]</span>
                  <StatusLedPip status="emerald" isLight={isLight} />
                </div>
                <h4 className={`font-bold font-mono text-sm my-1 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Sovereign Infrastructure</h4>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Local cloud datacenters, on-premise model proxies, hardware isolation, and zero external data egress.</p>
              </div>
            </div>
          </div>
        )}

        {/* OpenCode Agent Specs */}
        {activeTechTab === 'agent-cards' && (
          <div className="space-y-6">
            <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-zinc-800">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <StatusLedPip status="emerald" isLight={isLight} />
                  <span className="text-xs font-mono font-bold text-amber-500 uppercase tracking-wider">
                    SPECIFICATION DEFINITION // CANONICAL 7 TOOLS
                  </span>
                </div>
                <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  OpenCode-Native Agent Cards
                </h3>
              </div>
              <button
                onClick={() => handleCopyCode(sampleYamlCard, 'agent-yaml')}
                className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-200 border border-zinc-700 transition-colors"
              >
                {copiedCode === 'agent-yaml' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedCode === 'agent-yaml' ? 'COPIED TO CLIPBOARD' : 'COPY YAML SPEC'}</span>
              </button>
            </div>

            <div className={`p-4 rounded-xl border font-mono text-xs overflow-x-auto relative ${
              isLight ? 'bg-slate-900 text-amber-400 border-slate-800' : 'bg-black/90 text-amber-400 border-zinc-800'
            }`}>
              <pre className="leading-relaxed">{sampleYamlCard}</pre>
            </div>
          </div>
        )}

        {/* Live Benchmarks */}
        {activeTechTab === 'benchmarks' && (
          <div className="space-y-6">
            <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-zinc-800">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <StatusLedPip status="emerald" isLight={isLight} />
                  <span className="text-xs font-mono font-bold text-amber-500 uppercase tracking-wider">
                    HARDWARE TELEMETRY // REAL-TIME METRICS
                  </span>
                </div>
                <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Verified Technical Benchmarks
                </h3>
              </div>
              <AcousticVentGrille cols={4} rows={2} isLight={isLight} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className={`p-6 rounded-xl border text-center relative overflow-hidden ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />
                <span className="text-xs font-mono text-amber-500 uppercase font-bold">AIRTEL / TNM SETTLEMENT</span>
                <div className="text-4xl font-extrabold text-amber-500 my-3 font-mono">14.2s</div>
                <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Average dual-network reconciliation SLA across SADC cross-border payment gateways.
                </p>
              </div>

              <div className={`p-6 rounded-xl border text-center relative overflow-hidden ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />
                <span className="text-xs font-mono text-amber-500 uppercase font-bold">CHICHEWA NLP ACCURACY</span>
                <div className="text-4xl font-extrabold text-emerald-500 my-3 font-mono">98.4%</div>
                <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Evaluated on legal statutes, regulatory policies, and agricultural agronomy datasets.
                </p>
              </div>

              <div className={`p-6 rounded-xl border text-center relative overflow-hidden ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />
                <span className="text-xs font-mono text-amber-500 uppercase font-bold">AGENT DISPATCH LATENCY</span>
                <div className="text-4xl font-extrabold text-cyan-400 my-3 font-mono">&lt; 350ms</div>
                <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Sub-agent task dispatch SLA over high-throughput JSON bus.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Semantic Fabric */}
        {activeTechTab === 'semantic' && (
          <div className="space-y-6">
            <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-zinc-800">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <StatusLedPip status="emerald" isLight={isLight} />
                  <span className="text-xs font-mono font-bold text-amber-500 uppercase tracking-wider">
                    SECURITY & ENCRYPTION // ZERO-TRUST
                  </span>
                </div>
                <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Enterprise Data Isolation & RBAC
                </h3>
              </div>
              <AcousticVentGrille cols={4} rows={2} isLight={isLight} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className={`p-6 rounded-xl border space-y-3 ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center gap-2 text-amber-500 font-bold text-sm font-mono">
                  <Database className="w-4 h-4" /> <span>CONTEXT-AWARE SEMANTIC FABRIC</span>
                </div>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Extracts metadata and vector indices from PostgreSQL, NoSQL data warehouses, and official government PDFs, feeding live sub-agents without leaking sensitive customer records.
                </p>
              </div>

              <div className={`p-6 rounded-xl border space-y-3 ${
                isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
              }`}>
                <div className="flex items-center gap-2 text-emerald-500 font-bold text-sm font-mono">
                  <Lock className="w-4 h-4" /> <span>ZERO-TRUST 90-DAY KEY ROTATION</span>
                </div>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Automated RBAC key rotation protocol, scoped API access keys (Admin, Approve, Run), and comprehensive cryptographic tamper-evident event streaming.
                </p>
              </div>
            </div>
          </div>
        )}

      </div>

      {/* CTA Chassis */}
      <div className="mt-8 text-center">
        <button
          onClick={() => onOpenContactModal('Technical Architecture Deep-Dive')}
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 active:scale-95"
        >
          <span>Request Architecture Briefing</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

    </section>
  );
};
