import React, { useState } from 'react';
import { 
  Folder, 
  FileText, 
  Terminal, 
  Database, 
  Layers, 
  ShieldCheck, 
  Cpu, 
  Brain, 
  Workflow, 
  CheckCircle2, 
  AlertTriangle, 
  Play, 
  ChevronRight, 
  ChevronDown, 
  Code2, 
  Sparkles, 
  Building2, 
  UserCheck, 
  Search,
  Lock,
  ListFilter
} from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille 
} from './TactileHardwareElements';

interface AiCompanyBuilderOsExplorerProps {
  theme?: 'light' | 'dark';
  onOpenContactModal?: (intent?: string) => void;
}

export const AiCompanyBuilderOsExplorer: React.FC<AiCompanyBuilderOsExplorerProps> = ({
  theme = 'dark',
  onOpenContactModal
}) => {
  const isLight = theme === 'light';
  const [activeTab, setActiveTab] = useState<'mission' | 'iac-tree' | 'models' | 'decision-engine' | 'cli'>('mission');

  // IaC Folder Tree selection
  const [selectedFolder, setSelectedFolder] = useState<string>('config/company/company.yaml');

  // CLI Shell State
  const [cliCommand, setCliCommand] = useState<string>('ai-company bootstrap company.yaml');
  const [cliOutput, setCliOutput] = useState<string[]>([]);
  const [cliRunning, setCliRunning] = useState<boolean>(false);

  const handleRunCliCommand = (cmd: string) => {
    setCliCommand(cmd);
    setCliRunning(true);
    setCliOutput(['$ ' + cmd, 'Initializing AI Company Builder Engine v2.0...']);

    setTimeout(() => {
      if (cmd.includes('bootstrap')) {
        setCliOutput([
          '$ ' + cmd,
          '[BOOTSTRAP] Loading company.yaml configuration...',
          '[BOOTSTRAP] Validating Pydantic schemas for 20 Departments & 144 Agents...',
          '[BOOTSTRAP] Generating directory structure: config/, board/, executives/, departments/...',
          '[BOOTSTRAP] Rendering Jinja2 templates for CEO, CoS, COO, CTO, CFO, CISO...',
          '[BOOTSTRAP] Compiling 5-tier Human-in-the-Loop Approval Matrix & 5x5 Risk Matrix...',
          '[BOOTSTRAP] Generating OpenCode agent cards & sub-second message bus queues...',
          '[BOOTSTRAP] Initializing memory engine & NetworkX organization graph...',
          '----------------------------------------------------------------',
          'SUCCESS: Entire AI Company generated successfully in 1.42s!',
          '2,373 unit & integration tests collected and passing.'
        ]);
      } else if (cmd.includes('doctor')) {
        setCliOutput([
          '$ ' + cmd,
          '[DOCTOR] Running diagnostic checks...',
          '  [✓] YAML Configuration Syntax: VALID',
          '  [✓] Pydantic Model Validation: 100% PASS',
          '  [✓] OpenCode Agent Permissions: 7 CANONICAL TOOLS',
          '  [✓] DPA 2017/2024 & GDPR Compliance Rules: ACTIVE',
          '  [✓] 5-Tier HITL Approval Gates: WIRED',
          '  [✓] Test Suite: 2,373 TESTS PASSING',
          'System Status: HEALTHY // READY FOR DEPLOYMENT'
        ]);
      } else if (cmd.includes('graph')) {
        setCliOutput([
          '$ ' + cmd,
          '[GRAPH] Building NetworkX Organization & Workflow Graph...',
          'Nodes: 144 Agents + 20 Departments + 1 Board',
          'Edges: 342 Workflow Dispatch & Escalation Channels',
          'Graph density: 0.082 (Modular Cluster Topology)',
          'Exported to graphify-out/graph.json (AST-synchronized)'
        ]);
      } else if (cmd.includes('memory')) {
        setCliOutput([
          '$ ' + cmd,
          '[MEMORY] Searching 6 memory types (Episodic, Semantic, Procedural, Relational, Temporal, Aggregate)...',
          'Found 1,280 indexed memory vectors.',
          'Memory encryption status: AES-256-GCM AT REST'
        ]);
      } else {
        setCliOutput([
          '$ ' + cmd,
          '[SUCCESS] Action completed successfully.'
        ]);
      }
      setCliRunning(false);
    }, 600);
  };

  return (
    <section className={`p-6 sm:p-10 rounded-3xl border relative overflow-hidden transition-all my-12 ${
      isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
    }`}>
      <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
      <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
      <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
      <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

      {/* Title Chassis */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-zinc-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <StatusLedPip status="emerald" isLight={isLight} />
            <span className="text-[10px] font-mono font-bold text-amber-500 uppercase tracking-widest">
              AI COMPANY BUILDER V2 // SUPREME SYSTEM OPERATING SYSTEM
            </span>
          </div>
          <h2 className={`text-xl sm:text-3xl font-extrabold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
            Enterprise Infrastructure-as-Code OS
          </h2>
          <p className={`text-xs sm:text-sm mt-1 max-w-2xl ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
            Explore the configuration-driven platform that generates entire governed AI companies from a single declarative manifest.
          </p>
        </div>
        <AcousticVentGrille cols={6} rows={2} isLight={isLight} />
      </div>

      {/* Navigation Tabs */}
      <div className="flex flex-wrap items-center gap-2 mb-8 border-b border-zinc-800 pb-3">
        {[
          { id: 'mission', label: '01. Mission & Principles', icon: Sparkles },
          { id: 'iac-tree', label: '02. IaC File Tree', icon: Folder },
          { id: 'models', label: '03. Pydantic Schemas', icon: Database },
          { id: 'decision-engine', label: '04. Decision Engine', icon: ShieldCheck },
          { id: 'cli', label: '05. CLI Terminal', icon: Terminal }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2 rounded-xl text-xs font-mono font-bold transition-all flex items-center gap-2 cursor-pointer select-none ${
                isActive
                  ? 'bg-amber-500 text-slate-950 font-extrabold shadow-md shadow-amber-500/20'
                  : isLight
                  ? 'bg-slate-200/80 text-slate-700 hover:bg-slate-200'
                  : 'bg-zinc-900 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Main Viewport Content */}
      <div className={`p-6 sm:p-8 rounded-2xl border relative overflow-hidden transition-all ${
        isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />

        {/* ================= TABS ================= */}
        {activeTab === 'mission' && (
          <div className="space-y-6">
            <div className="p-6 rounded-2xl border bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-transparent border-amber-500/30">
              <span className="text-[10px] font-mono font-bold text-amber-500 uppercase tracking-widest block mb-1">
                PLATFORM MISSION STATEMENT
              </span>
              <h3 className={`text-xl sm:text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                &ldquo;Build AI-first businesses that can operate with high levels of autonomy while remaining governed by human leadership.&rdquo;
              </h3>
              <p className={`text-xs sm:text-sm mt-3 ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                Our goal is to create scalable companies powered by specialized AI executives, reusable workflows, and shared organizational knowledge — defined purely in declarative YAML and generated into production-ready software.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 font-mono text-xs">
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="text-amber-500 font-bold mb-1">1. Everything from YAML</div>
                <div className="text-zinc-400 text-[11px]">Single source of truth. No hardcoded prompts, workflows, or reports.</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="text-amber-500 font-bold mb-1">2. Pydantic Validation</div>
                <div className="text-zinc-400 text-[11px]">Strict schema validation, type safety, serialization to YAML & JSON.</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="text-amber-500 font-bold mb-1">3. Idempotent Generation</div>
                <div className="text-zinc-400 text-[11px]">Jinja2 templates compile custom code without overwriting user files.</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'iac-tree' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
              <span className="text-xs font-mono font-bold text-amber-500 uppercase">DECLARATIVE IAC DIRECTORY TREE</span>
              <span className="text-[10px] font-mono text-zinc-500">SINGLE SOURCE OF TRUTH</span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 font-mono text-xs">
              {/* Folder Tree Navigation */}
              <div className={`p-4 rounded-xl border space-y-1.5 ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                {[
                  { path: 'config/company/company.yaml', name: 'company.yaml [Root Manifest]' },
                  { path: 'config/board/board.yaml', name: 'board.yaml [Board Governance]' },
                  { path: 'executives/ceo.yaml', name: 'ceo.yaml [Executive Persona]' },
                  { path: 'departments/engineering.yaml', name: 'engineering.yaml [Dept Spec]' },
                  { path: 'agents/software_engineer.yaml', name: 'software_engineer.yaml [Agent]' },
                  { path: 'config/decision/approval_matrix.yaml', name: 'approval_matrix.yaml [HITL]' },
                  { path: 'src/ai_company/bootstrap.py', name: 'bootstrap.py [Generator]' }
                ].map((item) => {
                  const isSelected = selectedFolder === item.path;
                  return (
                    <button
                      key={item.path}
                      onClick={() => setSelectedFolder(item.path)}
                      className={`w-full text-left p-2 rounded flex items-center gap-2 cursor-pointer transition-all ${
                        isSelected 
                          ? 'bg-amber-500 text-slate-950 font-bold' 
                          : isLight ? 'text-slate-700 hover:bg-slate-200' : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800'
                      }`}
                    >
                      <FileText className="w-3.5 h-3.5 shrink-0" />
                      <span className="truncate">{item.name}</span>
                    </button>
                  );
                })}
              </div>

              {/* Code Previewer */}
              <div className={`lg:col-span-2 p-4 rounded-xl border font-mono text-[11px] overflow-x-auto ${
                isLight ? 'bg-slate-900 text-amber-300 border-slate-700' : 'bg-black text-amber-400 border-zinc-800'
              }`}>
                <div className="text-zinc-500 text-[10px] pb-2 border-b border-zinc-800 mb-2 flex justify-between">
                  <span>FILE :: {selectedFolder}</span>
                  <span>YAML / PYDANTIC / JINJA2</span>
                </div>
                <pre className="leading-relaxed">
{selectedFolder.includes('company.yaml') && `company:
  name: LightSpeed Holdings Limited
  location: Lilongwe, Malawi
  governance: 5-Tier Human-in-the-Loop (HITL)
  departments_count: 20
  agents_count: 144
  llm_providers: [gemini, opencode, deepseek, ollama, openai]
  compliance: [Malawi_DPA_2017_2024, GDPR]`}

{selectedFolder.includes('board.yaml') && `board:
  committees: [Audit, Risk, AI_Ethics, Strategy]
  governance_cadence:
    weekly: Standup
    monthly: Management Board Review
    quarterly: Strategy & Capital Allocation`}

{selectedFolder.includes('approval_matrix.yaml') && `approval_matrix:
  risk_levels:
    low: Auto-execute with audit log
    medium: Supervisor Agent review
    high: Department Head sign-off
    critical: Human CEO approval required (timeout=1800s)`}

{selectedFolder.includes('bootstrap.py') && `def bootstrap(manifest_path: str) -> bool:
    registry = RegistryLoader.load(manifest_path)
    Validator.validate_all(registry)
    BootstrapEngine.generate_directories()
    BootstrapEngine.render_templates(registry)
    return True`}
                </pre>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'models' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
              <span className="text-xs font-mono font-bold text-amber-500 uppercase">PYDANTIC DOMAIN MODELS & REGISTRIES</span>
              <span className="text-[10px] font-mono text-zinc-500">TYPE SAFETY & VALIDATION</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono text-xs">
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="font-bold text-amber-500 mb-1">CompanyModel</div>
                <div className="text-zinc-400 text-[11px]">Validates name, board, strategy, vision, culture, and policies.</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="font-bold text-amber-500 mb-1">ExecutiveModel</div>
                <div className="text-zinc-400 text-[11px]">CEO, CoS, COO, CTO, CFO, CISO, CDO, CLO, CSO directives & decision rights.</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="font-bold text-amber-500 mb-1">DepartmentModel</div>
                <div className="text-zinc-400 text-[11px]">20 departments: Engineering, Finance, Ops, Legal, IT, Security, Data...</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="font-bold text-amber-500 mb-1">AgentModel</div>
                <div className="text-zinc-400 text-[11px]">144 specialist agents with canonical tool vocabulary & memory isolation.</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'decision-engine' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
              <span className="text-xs font-mono font-bold text-amber-500 uppercase">5x5 RISK MATRIX & APPROVAL ENGINE</span>
              <span className="text-[10px] font-mono text-zinc-500">25 RISK-GATED ACTIONS</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono text-xs">
              <div className={`p-4 rounded-xl border space-y-3 ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="font-bold text-amber-500 text-sm">4 Risk Levels</div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between p-2 rounded bg-black/30 border border-white/10">
                    <span className="text-emerald-400 font-bold">LOW (Score 1-4)</span>
                    <span className="text-zinc-400 text-[10px]">Auto-executed with JSONL audit event</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded bg-black/30 border border-white/10">
                    <span className="text-blue-400 font-bold">MEDIUM (Score 5-9)</span>
                    <span className="text-zinc-400 text-[10px]">Supervisor Agent review</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded bg-black/30 border border-white/10">
                    <span className="text-amber-400 font-bold">HIGH (Score 10-15)</span>
                    <span className="text-zinc-400 text-[10px]">Department Head sign-off</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded bg-black/30 border border-white/10">
                    <span className="text-red-400 font-bold">CRITICAL (Score 16-25)</span>
                    <span className="text-zinc-400 text-[10px]">Human CEO approval required</span>
                  </div>
                </div>
              </div>

              <div className={`p-4 rounded-xl border space-y-3 ${isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900 border-zinc-800'}`}>
                <div className="font-bold text-amber-500 text-sm">Governance Gate (G1–G4) Enforcement</div>
                <ul className="space-y-2 text-zinc-300 text-[11px]">
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> G1: Contract & Scope signed</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> G2: DPA & Cross-Border Consent verified</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> G3: Regulatory & SADC Compliance review</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> G4: Security Assessment & Cryptographic key check</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'cli' && (
          <div className="space-y-4 font-mono text-xs">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-zinc-400 text-[11px]">PRESET COMMANDS:</span>
              <button
                onClick={() => handleRunCliCommand('ai-company bootstrap company.yaml')}
                className="px-2.5 py-1 rounded bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/30 text-[11px] cursor-pointer"
              >
                ai-company bootstrap
              </button>
              <button
                onClick={() => handleRunCliCommand('ai-company doctor')}
                className="px-2.5 py-1 rounded bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 border border-blue-500/30 text-[11px] cursor-pointer"
              >
                ai-company doctor
              </button>
              <button
                onClick={() => handleRunCliCommand('ai-company graph')}
                className="px-2.5 py-1 rounded bg-purple-500/10 hover:bg-purple-500/20 text-purple-400 border border-purple-500/30 text-[11px] cursor-pointer"
              >
                ai-company graph
              </button>
              <button
                onClick={() => handleRunCliCommand('ai-company memory')}
                className="px-2.5 py-1 rounded bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[11px] cursor-pointer"
              >
                ai-company memory
              </button>
            </div>

            {/* Interactive Terminal Output Window */}
            <div className={`p-4 rounded-xl border bg-black border-zinc-800 text-amber-400 min-h-[180px] font-mono text-[11px] space-y-1.5 ${
              cliRunning ? 'opacity-80' : ''
            }`}>
              <div className="text-zinc-600 text-[10px] pb-2 border-b border-zinc-900 flex justify-between">
                <span>AI COMPANY BUILDER CLI // V2.0</span>
                <span>TYPER APP ENGINE</span>
              </div>
              {cliOutput.map((line, idx) => (
                <div key={idx} className={line.startsWith('$') ? 'text-white font-bold' : line.includes('SUCCESS') ? 'text-emerald-400 font-bold' : 'text-amber-300/90'}>
                  {line}
                </div>
              ))}
            </div>
          </div>
        )}

      </div>
    </section>
  );
};
