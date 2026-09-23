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
          '[BOOTSTRAP] Validating Pydantic schemas for 20 Departments & 90 Agents...',
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
          'Nodes: 90 Agents + 20 Departments + 1 Board',
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
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-ls-grey-dark">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <StatusLedPip status="emerald" isLight={isLight} />
            <span className="text-[10px] font-body font-bold text-ls-red uppercase tracking-widest">
              AI COMPANY BUILDER V2 // SUPREME SYSTEM OPERATING SYSTEM
            </span>
          </div>
          <h2 className={`text-xl sm:text-3xl font-extrabold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
            Enterprise Infrastructure-as-Code OS
          </h2>
          <p className={`text-xs sm:text-sm mt-1 max-w-2xl ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
            Explore the configuration-driven platform that generates entire governed AI companies from a single declarative manifest.
          </p>
        </div>
        <AcousticVentGrille cols={6} rows={2} isLight={isLight} />
      </div>

      {/* Navigation Tabs */}
      <div className="flex flex-wrap items-center gap-2 mb-8 border-b border-ls-grey-dark pb-3">
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
              className={`px-4 py-2 rounded-xl text-xs font-body font-bold transition-all flex items-center gap-2 cursor-pointer select-none ${
                isActive
                  ? 'bg-ls-red text-ls-navy font-extrabold shadow-md shadow-ls-red/20'
                  : isLight
                  ? 'bg-ls-grey-light/80 text-ls-grey-dark hover:bg-ls-grey-light'
                  : 'bg-ls-navy text-ls-grey-light-text hover:text-ls-white hover:bg-ls-navy'
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
            <div className="p-6 rounded-2xl border bg-gradient-to-r from-ls-red/10 via-ls-red/5 to-transparent border-ls-red/30">
              <span className="text-[10px] font-body font-bold text-ls-red uppercase tracking-widest block mb-1">
                PLATFORM MISSION STATEMENT
              </span>
              <h3 className={`text-xl sm:text-2xl font-bold font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                &ldquo;Build AI-first businesses that can operate with high levels of autonomy while remaining governed by human leadership.&rdquo;
              </h3>
              <p className={`text-xs sm:text-sm mt-3 ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                Our goal is to create scalable companies powered by specialized AI executives, reusable workflows, and shared organizational knowledge — defined purely in declarative YAML and generated into production-ready software.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 font-body text-xs">
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy border-ls-grey-dark'}`}>
                <div className="text-ls-red font-bold mb-1">1. Everything from YAML</div>
                <div className="text-ls-grey-light-text text-[11px]">Single source of truth. No hardcoded prompts, workflows, or reports.</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy border-ls-grey-dark'}`}>
                <div className="text-ls-red font-bold mb-1">2. Pydantic Validation</div>
                <div className="text-ls-grey-light-text text-[11px]">Strict schema validation, type safety, serialization to YAML & JSON.</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy border-ls-grey-dark'}`}>
                <div className="text-ls-red font-bold mb-1">3. Idempotent Generation</div>
                <div className="text-ls-grey-light-text text-[11px]">Jinja2 templates compile custom code without overwriting user files.</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'iac-tree' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-ls-grey-dark pb-3">
              <span className="text-xs font-body font-bold text-ls-red uppercase">DECLARATIVE IAC DIRECTORY TREE</span>
              <span className="text-[10px] font-body text-ls-grey-light-text">SINGLE SOURCE OF TRUTH</span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 font-body text-xs">
              {/* Folder Tree Navigation */}
              <div className={`p-4 rounded-xl border space-y-1.5 ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy border-ls-grey-dark'}`}>
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
                          ? 'bg-ls-red text-ls-navy font-bold'
                          : isLight ? 'text-ls-grey-dark hover:bg-ls-grey-light' : 'text-ls-grey-light-text hover:text-ls-white hover:bg-ls-navy'
                      }`}
                    >
                      <FileText className="w-3.5 h-3.5 shrink-0" />
                      <span className="truncate">{item.name}</span>
                    </button>
                  );
                })}
              </div>

              {/* Code Previewer */}
              <div className={`lg:col-span-2 p-4 rounded-xl border font-body text-[11px] overflow-x-auto ${
                isLight ? 'bg-ls-navy text-ls-red/30 border-ls-white' : 'bg-ls-navy text-ls-red/40 border-ls-grey-dark'
              }`}>
                <div className="text-ls-grey-light-text text-[10px] pb-2 border-b border-ls-grey-dark mb-2 flex justify-between">
                  <span>FILE :: {selectedFolder}</span>
                  <span>YAML / PYDANTIC / JINJA2</span>
                </div>
                <pre className="leading-relaxed">
{selectedFolder.includes('company.yaml') && `company:
  name: LightSpeed Holdings Limited
  location: Lilongwe, Malawi
  governance: 5-Tier Human-in-the-Loop (HITL)
  departments_count: 20
  agents_count: 90
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
            <div className="flex items-center justify-between border-b border-ls-grey-dark pb-3">
              <span className="text-xs font-body font-bold text-ls-red uppercase">PYDANTIC DOMAIN MODELS & REGISTRIES</span>
              <span className="text-[10px] font-body text-ls-grey-light-text">TYPE SAFETY & VALIDATION</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-body text-xs">
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy border-ls-grey-dark'}`}>
                <div className="font-bold text-ls-red mb-1">CompanyModel</div>
                <div className="text-ls-grey-light-text text-[11px]">Validates name, board, strategy, vision, culture, and policies.</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy border-ls-grey-dark'}`}>
                <div className="font-bold text-ls-red mb-1">ExecutiveModel</div>
                <div className="text-ls-grey-light-text text-[11px]">CEO, CoS, COO, CTO, CFO, CISO, CDO, CLO, CSO directives & decision rights.</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy border-ls-grey-dark'}`}>
                <div className="font-bold text-ls-red mb-1">DepartmentModel</div>
                <div className="text-ls-grey-light-text text-[11px]">20 departments: Engineering, Finance, Ops, Legal, IT, Security, Data...</div>
              </div>
              <div className={`p-4 rounded-xl border ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy border-ls-grey-dark'}`}>
                <div className="font-bold text-ls-red mb-1">AgentModel</div>
                <div className="text-ls-grey-light-text text-[11px]">90 specialist agents with canonical tool vocabulary & memory isolation.</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'decision-engine' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-ls-grey-dark pb-3">
              <span className="text-xs font-body font-bold text-ls-red uppercase">5x5 RISK MATRIX & APPROVAL ENGINE</span>
              <span className="text-[10px] font-body text-ls-grey-light-text">25 RISK-GATED ACTIONS</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-body text-xs">
              <div className={`p-4 rounded-xl border space-y-3 ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy border-ls-grey-dark'}`}>
                <div className="font-bold text-ls-red text-sm">4 Risk Levels</div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between p-2 rounded bg-ls-navy/30 border border-ls-white/10">
                    <span className="text-ls-cyan/80 font-bold">LOW (Score 1-4)</span>
                    <span className="text-ls-grey-light-text text-[10px]">Auto-executed with JSONL audit event</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded bg-ls-navy/30 border border-ls-white/10">
                    <span className="text-ls-cyan/80 font-bold">MEDIUM (Score 5-9)</span>
                    <span className="text-ls-grey-light-text text-[10px]">Supervisor Agent review</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded bg-ls-navy/30 border border-ls-white/10">
                    <span className="text-ls-red/40 font-bold">HIGH (Score 10-15)</span>
                    <span className="text-ls-grey-light-text text-[10px]">Department Head sign-off</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded bg-ls-navy/30 border border-ls-white/10">
                    <span className="text-ls-red/40 font-bold">CRITICAL (Score 16-25)</span>
                    <span className="text-ls-grey-light-text text-[10px]">Human CEO approval required</span>
                  </div>
                </div>
              </div>

              <div className={`p-4 rounded-xl border space-y-3 ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy border-ls-grey-dark'}`}>
                <div className="font-bold text-ls-red text-sm">Governance Gate (G1–G4) Enforcement</div>
                <ul className="space-y-2 text-ls-grey-light-text text-[11px]">
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-ls-cyan/80" /> G1: Contract & Scope signed</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-ls-cyan/80" /> G2: DPA & Cross-Border Consent verified</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-ls-cyan/80" /> G3: Regulatory & SADC Compliance review</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-ls-cyan/80" /> G4: Security Assessment & Cryptographic key check</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'cli' && (
          <div className="space-y-4 font-body text-xs">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-ls-grey-light-text text-[11px]">PRESET COMMANDS:</span>
              <button
                onClick={() => handleRunCliCommand('ai-company bootstrap company.yaml')}
                className="px-2.5 py-1 rounded bg-ls-red/10 hover:bg-ls-red/20 text-ls-red/40 border border-ls-red/30 text-[11px] cursor-pointer"
              >
                ai-company bootstrap
              </button>
              <button
                onClick={() => handleRunCliCommand('ai-company doctor')}
                className="px-2.5 py-1 rounded bg-ls-cyan/10 hover:bg-ls-cyan/20 text-ls-cyan/80 border border-ls-cyan/30 text-[11px] cursor-pointer"
              >
                ai-company doctor
              </button>
              <button
                onClick={() => handleRunCliCommand('ai-company graph')}
                className="px-2.5 py-1 rounded bg-ls-red/10 hover:bg-ls-red/20 text-ls-red/40 border border-ls-red/30 text-[11px] cursor-pointer"
              >
                ai-company graph
              </button>
              <button
                onClick={() => handleRunCliCommand('ai-company memory')}
                className="px-2.5 py-1 rounded bg-ls-cyan/10 hover:bg-ls-cyan/20 text-ls-cyan/80 border border-ls-cyan/30 text-[11px] cursor-pointer"
              >
                ai-company memory
              </button>
            </div>

            {/* Interactive Terminal Output Window */}
            <div className={`p-4 rounded-xl border bg-ls-navy border-ls-grey-dark text-ls-red/40 min-h-[180px] font-body text-[11px] space-y-1.5 ${
              cliRunning ? 'opacity-80' : ''
            }`}>
              <div className="text-ls-grey-dark text-[10px] pb-2 border-b border-ls-grey-dark flex justify-between">
                <span>AI COMPANY BUILDER CLI // V2.0</span>
                <span>TYPER APP ENGINE</span>
              </div>
              {cliOutput.map((line, idx) => (
                <div key={idx} className={line.startsWith('$') ? 'text-ls-white font-bold' : line.includes('SUCCESS') ? 'text-ls-cyan/80 font-bold' : 'text-ls-red/90'}>
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
