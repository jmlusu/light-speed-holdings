import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Cpu, 
  ShieldCheck, 
  Workflow, 
  Terminal, 
  Lock, 
  Layers, 
  Activity, 
  CheckCircle2, 
  Sparkles, 
  ArrowRight,
  GitBranch,
  Shield,
  FileCode,
  Users,
  Building,
  Radio,
  Clock,
  Key
} from 'lucide-react';
import { StatusBadge } from './ui/StatusBadge';
import { AcousticVentGrille } from './TactileHardwareElements';

interface MethodFrameworkProps {
  theme?: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const MethodFramework: React.FC<MethodFrameworkProps> = ({
  theme = 'dark',
  onRequestBriefing
}) => {
  const isLight = theme === 'light';
  const [selectedHaomtgvIndex, setSelectedHaomtgvIndex] = useState<number>(0);
  const [selectedTool, setSelectedTool] = useState<string>('task');

  // The H-A-O-M-T-G-V Framework
  const haomtgvPillars = [
    {
      letter: 'H',
      name: 'HUMAN',
      title: 'Human Authority & Executive Oversight',
      desc: 'The executive committee, board, and appointed domain authorities retain absolute constitutional sovereignty. No high-impact action, treasury disbursement, or policy change is executed without cryptographic human sign-off.',
      proof: '5-tier approval gates & periodic HITL expiry sweeps preventing blocked state',
      tag: 'Executive Authority'
    },
    {
      letter: 'A',
      name: 'AGENT',
      title: 'Specialized 144-Agent Roster',
      desc: '144 discrete, role-bounded agent personas defined in `company-registry.yaml`. Every agent has an explicit domain scope, tool permission boundary, and deterministic escalation pathway.',
      proof: 'Jinja2 generated OpenCode markdown cards with strict subagent sandboxing',
      tag: 'Role Topology'
    },
    {
      letter: 'O',
      name: 'ORGANIZATION',
      title: 'Domain Policies & Token Budgets',
      desc: 'Organizational boundaries, department budgets, and data classification matrices are encoded as computable schemas, eliminating inter-departmental security breaches and unauthorized data leakage.',
      proof: 'Policy-as-code enforcement aligning with Malawi DPA 2017/2024 and King IV',
      tag: 'Topology Schemas'
    },
    {
      letter: 'M',
      name: 'MODEL',
      title: 'Sovereign & Air-Gapped Model Runtimes',
      desc: 'Local, on-soil model inference (Big Pickle / Gemini / DeepSeek fallbacks) running in sovereign enclaves with zero telemetry leakage to third-party public clouds.',
      proof: 'Air-gapped on-premises or national cloud deployment compatibility',
      tag: 'Inference Sovereignty'
    },
    {
      letter: 'T',
      name: 'TOOL',
      title: 'Canonical 7-Tool Sandboxing',
      desc: 'Strict rejection of arbitrary code execution. Agents operate exclusively through 7 canonical sandboxed wrappers: `read`, `edit`, `grep`, `list`, `bash`, `webfetch`, and `task`.',
      proof: 'Runtime ToolRunner validation rejecting unapproved external calls',
      tag: 'Execution Sandbox'
    },
    {
      letter: 'G',
      name: 'GATE',
      title: '5-Tier Cryptographic Approval Gates',
      desc: 'Pre-execution gatekeepers evaluating every agent proposal against threshold limits, spending budgets, and regulatory covenants before triggering external write events.',
      proof: 'Deterministic state transitions (PENDING → APPROVED / REJECTED / EXPIRED)',
      tag: 'Fiduciary Gates'
    },
    {
      letter: 'V',
      name: 'VERIFICATION',
      title: 'Immutable SHA-256 Audit Trails & Drift Telemetry',
      desc: 'Every prompt, tool invocation, human decision, and API response is immutably logged to cryptographic hash chains, creating full mathematical transparency for statutory audits.',
      proof: 'Automated continuous evaluation and model drift telemetry',
      tag: 'Cryptographic Audit'
    }
  ];

  // Canonical 7-Tool Vocabulary
  const canonicalTools = [
    { name: 'read', purpose: 'Read file contents securely within workspace bounds', safety: 'Read-only sandbox' },
    { name: 'edit', purpose: 'Exact string replacement and surgical file updates', safety: 'Target-match verification' },
    { name: 'grep', purpose: 'Search file contents with optimized regex', safety: 'Fast AST indexing' },
    { name: 'list', purpose: 'Inspect directory hierarchies and child assets', safety: 'Path-traversal shielded' },
    { name: 'bash', purpose: 'Execute controlled, bounded shell operations', safety: 'Timeout & stdout capped' },
    { name: 'webfetch', purpose: 'Retrieve external HTTP/HTTPS data & APIs', safety: 'Whitelisted domain egress' },
    { name: 'task', purpose: 'Launch specialized sub-agents for complex DAGs', safety: 'Hierarchy depth bounded' }
  ];

  return (
    <section id="method" className="py-20 px-4 sm:px-8 max-w-7xl mx-auto w-full relative z-10">
      
      {/* Section Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <StatusBadge tier="proven-in-house" size="md" />
            <span className="text-xs font-mono font-bold tracking-widest text-[#2D3748]">
              // THOUGHT LEADERSHIP CENTERPIECE
            </span>
          </div>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            The 144-Agent Method: <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 via-amber-500 to-amber-300">
              The H-A-O-M-T-G-V Governance Framework
            </span>
          </h2>
          <p className={`text-justify text-justify text-xs sm:text-sm max-w-3xl leading-relaxed ${
            isLight ? 'text-slate-700' : 'text-zinc-300'
          }`}>
            Unlike ungrounded chatbot widgets, LightSpeed constructs self-contained, multi-agent AI enterprises. Governed by computable policies, canonical tool sandboxes, and cryptographic human-in-the-loop gates—proven on our own daily operations.
          </p>
        </div>

        <button
          onClick={() => onRequestBriefing?.('Inquiry regarding 144-Agent Framework & H-A-O-M-T-G-V Governance Architecture')}
          className="self-start md:self-auto px-5 py-3 rounded-full text-xs font-bold font-mono tracking-wider bg-orange-500 hover:bg-orange-600 text-white shadow-lg shadow-orange-500/25 transition-all cursor-pointer flex items-center gap-2"
        >
          <span>Book Method Architecture Briefing</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Main Grid: H-A-O-M-T-G-V Stepper on Left, Canonical Tools & Architecture on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left: The 7 Pillars of H-A-O-M-T-G-V (7 Cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className={`p-6 sm:p-8 rounded-3xl border relative overflow-hidden ${
            isLight ? 'bg-white border-slate-300 shadow-xl' : 'bg-black/60 border-white/15 shadow-2xl'
          }`}>
            {/* Top Vent Strip */}
            <div className="flex items-center justify-between pb-4 border-b border-black/10 dark:border-white/10 mb-6">
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-orange-500" />
                <span className={`font-mono text-xs font-bold tracking-wider ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  SEVEN PILLARS OF SOVEREIGN GOVERNANCE
                </span>
              </div>
              <AcousticVentGrille variant="cluster" isLight={isLight} />
            </div>

            {/* Pillar Letters Selector */}
            <div className="grid grid-cols-7 gap-1.5 sm:gap-2 mb-6">
              {haomtgvPillars.map((p, idx) => {
                const isSelected = selectedHaomtgvIndex === idx;
                return (
                  <button
                    key={p.letter}
                    onClick={() => setSelectedHaomtgvIndex(idx)}
                    className={`py-3 rounded-2xl flex flex-col items-center justify-center transition-all cursor-pointer border ${
                      isSelected
                        ? 'bg-gradient-to-b from-orange-500 to-amber-600 text-white border-white/30 shadow-md scale-105'
                        : isLight
                          ? 'bg-slate-100 hover:bg-slate-200 border-slate-200 text-slate-800'
                          : 'bg-white/5 hover:bg-white/10 border-white/10 text-zinc-300'
                    }`}
                  >
                    <span className="text-base sm:text-xl font-black font-display">{p.letter}</span>
                    <span className="text-[8px] font-mono font-bold tracking-tighter mt-0.5 opacity-80 hidden sm:inline">
                      {p.name}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* Active Pillar Detailed Card */}
            {(() => {
              const activeP = haomtgvPillars[selectedHaomtgvIndex];
              return (
                <AnimatePresence mode="wait">
                  <motion.div
                    key={activeP.letter}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.3 }}
                    className={`p-5 sm:p-6 rounded-2xl border space-y-3 ${
                      isLight ? 'bg-slate-50 border-slate-200' : 'bg-white/[0.04] border-white/10'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="w-7 h-7 rounded-full bg-orange-500 text-white flex items-center justify-center font-bold text-xs font-mono">
                          {activeP.letter}
                        </span>
                        <h4 className={`text-base sm:text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                          {activeP.title}
                        </h4>
                      </div>
                      <span className="text-[10px] font-mono text-orange-400 bg-orange-500/10 px-2.5 py-0.5 rounded-full border border-orange-500/20 font-bold">
                        {activeP.tag}
                      </span>
                    </div>

                    <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                      {activeP.desc}
                    </p>

                    <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-start gap-2 text-emerald-400 text-xs">
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0 mt-0.5 text-emerald-400" />
                      <span className="text-[11px] font-mono">
                        <strong>Governed Proof:</strong> {activeP.proof}
                      </span>
                    </div>
                  </motion.div>
                </AnimatePresence>
              );
            })()}

          </div>
        </div>

        {/* Right: Canonical 7-Tool Sandboxing & 144-Agent Hierarchy (5 Cols) */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Canonical 7-Tool Permission Block */}
          <div className={`p-6 rounded-3xl border relative overflow-hidden ${
            isLight ? 'bg-white border-slate-300 shadow-xl' : 'bg-black/60 border-white/15 shadow-2xl'
          }`}>
            <div className="flex items-center justify-between pb-3 border-b border-black/10 dark:border-white/10 mb-4">
              <div className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-emerald-400" />
                <span className={`font-mono text-xs font-bold tracking-wider ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  CANONICAL 7-TOOL VOCABULARY
                </span>
              </div>
              <span className="text-[9px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">
                OPENCODE COMPATIBLE
              </span>
            </div>

            <p className={`text-justify text-justify text-xs leading-relaxed mb-4 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Agents are strictly prevented from executing unmonitored commands. All operations compile to these 7 verified primitives:
            </p>

            <div className="space-y-2">
              {canonicalTools.map((t) => {
                const isCurrent = selectedTool === t.name;
                return (
                  <button
                    key={t.name}
                    onClick={() => setSelectedTool(t.name)}
                    className={`w-full p-2.5 rounded-xl border text-left flex items-center justify-between transition-all cursor-pointer ${
                      isCurrent
                        ? 'bg-orange-500/15 border-orange-500 text-orange-400'
                        : isLight
                          ? 'bg-slate-50 border-slate-200 text-slate-800 hover:bg-slate-100'
                          : 'bg-white/5 border-white/10 text-zinc-300 hover:bg-white/10'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-black/40 text-emerald-400 border border-white/10">
                        {t.name}
                      </span>
                      <span className="text-[11px] truncate max-w-[200px]">{t.purpose}</span>
                    </div>
                    <span className="text-[9px] font-mono text-zinc-400 font-semibold">{t.safety}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* 144-Agent In-House Generation Pipeline */}
          <div className={`p-5 rounded-2xl border ${
            isLight ? 'bg-slate-100 border-slate-200 text-slate-800' : 'bg-zinc-950/80 border-white/10 text-zinc-300'
          }`}>
            <div className="flex items-center gap-2 mb-2">
              <FileCode className="w-4 h-4 text-orange-500" />
              <span className="text-xs font-mono font-bold tracking-wider text-orange-400">
                PROVEN IN-HOUSE CODE PIPELINE
              </span>
            </div>
            <p className="text-[11px] font-mono text-zinc-400 leading-snug">
              Single Source of Truth: <code className="text-amber-300">company-registry.yaml</code> → Jinja2 compiler → <code className="text-emerald-400">.opencode/agents/*.md</code>. 144 agents operate with deterministic task queues at <code className="text-blue-300">.opencode/inbox.json</code>.
            </p>
          </div>

        </div>

      </div>

    </section>
  );
};
