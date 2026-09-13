import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  ShieldCheck, 
  Cpu, 
  Workflow, 
  Database, 
  Terminal, 
  Lock, 
  CheckCircle2, 
  Users, 
  Building2, 
  ArrowRight, 
  Activity, 
  AlertTriangle, 
  Clock, 
  FileCode, 
  Key, 
  Zap, 
  Layers, 
  Compass, 
  ExternalLink,
  ChevronRight,
  ShieldAlert,
  Server,
  Network,
  RotateCcw,
  Search,
  Filter,
  Check,
  Code2,
  HardDrive,
  Eye,
  X,
  Play
} from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille 
} from './TactileHardwareElements';
import { agentsList, departmentsList } from '../data/companyData';
import { Agent, Department } from '../types';

interface HaomtgvGovernanceFrameworkProps {
  theme?: 'light' | 'dark';
  onOpenContactModal?: (intent?: string) => void;
}

type FrameworkTab = 'pillars' | 'roster' | 'topology' | 'simulator';

export const HaomtgvGovernanceFramework: React.FC<HaomtgvGovernanceFrameworkProps> = ({
  theme = 'dark',
  onOpenContactModal
}) => {
  const isLight = theme === 'light';
  
  // Navigation State
  const [activeTab, setActiveTab] = useState<FrameworkTab>('pillars');
  const [activePillar, setActivePillar] = useState<'H' | 'A' | 'O' | 'M' | 'T' | 'G' | 'V'>('H');
  
  // 144 Agent Hierarchy State
  const [selectedDeptId, setSelectedDeptId] = useState<string>('executive');
  const [agentSearchQuery, setAgentSearchQuery] = useState<string>('');
  const [selectedToolFilter, setSelectedToolFilter] = useState<string>('all');
  const [inspectingAgent, setInspectingAgent] = useState<Agent | null>(null);

  // Tool Sandbox State
  const [selectedTool, setSelectedTool] = useState<string>('task');
  const [simulatedToolOutput, setSimulatedToolOutput] = useState<string>('');

  // 5-Tier Gate Simulator State
  const [simulatedTaskState, setSimulatedTaskState] = useState<'idle' | 'routing' | 'evaluating' | 'approved' | 'rejected' | 'expired'>('idle');
  const [activeSimTaskIndex, setActiveSimTaskIndex] = useState<number>(0);
  const [hitlExpirySeconds, setHitlExpirySeconds] = useState<number>(1440);
  const [customTaskTitle, setCustomTaskTitle] = useState<string>('');
  const [customTaskTier, setCustomTaskTier] = useState<number>(3);
  const [generatedBlockHash, setGeneratedBlockHash] = useState<string>('');
  const [sweepNotice, setSweepNotice] = useState<string | null>(null);

  // The 7 Pillars of H-A-O-M-T-G-V
  const pillars = [
    {
      id: 'H',
      letter: 'H',
      name: 'Human Purpose',
      headline: 'Human Apex Authority & Non-Delegable Sovereignty',
      coreQuestion: 'What must humans retain absolute, non-delegable sovereignty over?',
      summary: 'The Human CEO (Jack Mlusu), Executive Committee, and Board retain constitutional authority. No high-impact decision, treasury disbursement, or sovereign policy dispatch is executed without human cryptographic signature.',
      principles: [
        'Non-Delegable Apex: AI agents recommend, analyze, and draft; humans hold legal and moral accountability.',
        'Cryptographic HITL: Tier 4 and Tier 5 actions require authenticated ed25519 human signature before state execution.',
        'HITL Expiry Sweep (Rule 9.1): Autonomous daemon sweeps stale PENDING requests to EXPIRED, preventing inbox deadlock.',
        'Trust-by-Engineering: Eliminating human displacement anxiety through structured operator-in-the-loop pairing.'
      ],
      metrics: '100% Statutory Compliance // Zero Ungoverned State Changes',
      codeSnippet: `// Human Sovereignty & Tier 5 Approval Gate Schema
interface HumanExecutiveGate {
  signatory: "Jack Mlusu, Human CEO" | "Board Executive Committee";
  cryptographicKey: "ed25519-pharos-root-sig-902";
  mandatoryTiers: ["Tier 4 Legal & Fiduciary", "Tier 5 Treasury & Public Commit"];
  expirySweepMinutes: 1440; // Auto-transition to EXPIRED after 24h
  bypassAllowed: false; // Hardware-locked prohibition of bypass
  auditProof: "SHA-256 tamper-evident chaining";
}`
    },
    {
      id: 'A',
      letter: 'A',
      name: 'Agentic Workforce',
      headline: '144 Specialized Sub-Agents Across 20 Governed Departments',
      coreQuestion: 'What organizational labor can specialized AI agents autonomously perform?',
      summary: '144 discrete, role-bounded agent personas defined strictly in company-registry.yaml. Every agent has an explicit domain scope, tool permission boundary, and deterministic escalation pathway.',
      principles: [
        'Single Source of Truth: company-registry.yaml defines every agent ID, name, tools, and permissions.',
        'Jinja2 Templating: Generated into OpenCode v2 markdown cards (.opencode/agents/*.md) with mode: subagent.',
        'Strict Role Bounding: Subagents cannot mutate their own prompt or access tools outside their whitelist.',
        'Hierarchical Escalation: Specialists report to Department Leads; Leads report to Executive Swarm.'
      ],
      metrics: '144 Active Specialists // 20 Governed Departments',
      codeSnippet: `name: thought-leadership-author
version: 2.4.0
mode: subagent
department: Pharos
permission: Tier 3 (Department Lead Sign-Off)
tools: [read, edit, grep, list, task]
reports_to: thought-leadership-lead
system_prompt: |
  Draft flagship white papers and the H-A-O-M-T-G-V public narrative.
  Enforce brand-voice distinct from technical code documentation.
  Never dispatch external communications without Tier 4 Legal approval.`
    },
    {
      id: 'O',
      letter: 'O',
      name: 'Orchestration',
      headline: 'Deterministic Workflow DAGs & Asynchronous Inbox',
      coreQuestion: 'How do 144 agents coordinate without race conditions, collisions, or chaos?',
      summary: 'Task coordination operates via a deterministic JSON queue at .opencode/inbox.json. Directed Acyclic Graphs (DAGs) break complex strategic briefs into sub-tasks with sub-second message routing.',
      principles: [
        'Message Bus Integrity: File-based asynchronous task queue preventing network state loss.',
        'Subagent Delegation via task: Agents launch subagents exclusively through the canonical task tool runner.',
        'Deterministic State Machine: Every task moves strictly: PENDING → ASSIGNED → IN_PROGRESS → REVIEW → COMPLETED.',
        'Sub-Second Routing: Local IPC and socket queues eliminate SaaS API network latency overhead (<180ms).'
      ],
      metrics: '< 180ms Dispatch Latency // Zero Race Conditions',
      codeSnippet: `// Message Bus Task Specification (.opencode/inbox.json)
{
  "taskId": "task-2026-sadc-policy-tome-4",
  "assignedAgent": "thought-leadership-lead",
  "delegatedSubagents": ["thought-leadership-author", "policy-analyst"],
  "dagStage": "STAGE_3_PEER_REVIEW",
  "permissionTierRequired": "Tier_4_Legal",
  "timeoutSeconds": 3600,
  "auditChainPrevHash": "0x7a3f89b...e21c",
  "state": "IN_PROGRESS"
}`
    },
    {
      id: 'M',
      letter: 'M',
      name: 'Enterprise Memory',
      headline: 'Air-Gapped Sovereign Memory & Knowledge Graph',
      coreQuestion: 'How does the enterprise learn and retain context without cloud data leakage?',
      summary: 'A dual memory architecture separating ephemeral conversational scratchpads from persistent institutional knowledge graphs (graphify-out/), completely air-gapped on national soil.',
      principles: [
        'Local AST Knowledge Graph: graphify maintains AST relationships without sending tokens to public clouds.',
        'Zero Cloud Telemetry: Operational data stays within Malawi and SADC national borders.',
        'Partitioned Vector Fabrics: Department memory isolated by cryptographic tenant namespaces.',
        'Continuous Institutional Learning: Post-task reflections indexed into persistent institutional memory.'
      ],
      metrics: '100% SADC Data Residency // Zero Public Cloud Egress',
      codeSnippet: `// Sovereign Enterprise Memory Architecture
class SovereignEnterpriseMemory:
    def __init__(self, tenant_id: str = "lightspeed-holdings"):
        self.graph = GraphifyStore(path="graphify-out/graph.json")
        self.local_vector_db = ChromaOnSoil(path="/var/lib/sovereign-vault")
        self.cloud_egress_guard = StrictAirGapBarrier(block_external=True)
    
    def recall_context(self, query: str) -> MemoryContext:
        # Zero external API tokens transmitted
        return self.graph.query_ast_subgraph(query)`
    },
    {
      id: 'T',
      letter: 'T',
      name: 'Tools & Actions',
      headline: 'The Canonical 7-Tool Sandboxing Whitelist',
      coreQuestion: 'How do agents execute tangible actions safely in real environments?',
      summary: 'Strict rejection of arbitrary shell or unconstrained code execution. All 144 agents operate exclusively through 7 canonical sandboxed runtime wrappers validated against permission blocks.',
      principles: [
        'The Canonical 7: read, edit, grep, list, bash, webfetch, and task.',
        'Legacy Alias Normalization: Backward-compatible normalization (write → edit, execute → bash, delegate → task).',
        'Forbidden Runtimes: code_interpreter is permanently removed to prevent uncontained execution.',
        'Sandboxed Shell: bash is restricted by timeout, output truncation, and forbidden command filters.'
      ],
      metrics: '7 Canonical Tools // Zero Arbitrary Code Execution',
      codeSnippet: `// Canonical Runtime Tool Vocabulary (OpenCode v2)
CANONICAL_TOOLS = {
    "read": "Read file contents within workspace root",
    "edit": "Exact string replacement; prevents whole-file overwrite",
    "grep": "AST-safe regex file searching (skips binary/deps)",
    "list": "Directory enumeration with path-traversal guard",
    "bash": "Timeout-bounded, non-interactive shell command runner",
    "webfetch": "HTTP/HTTPS fetcher with domain whitelist",
    "task": "Subagent DAG spawn runner"
}`
    },
    {
      id: 'G',
      letter: 'G',
      name: 'Governance & Policy',
      headline: '5-Tier Cryptographic Human-in-the-Loop Approval Gates',
      coreQuestion: 'How do we control agent risk boundaries before write events occur?',
      summary: 'Every agent operation is evaluated against 5 risk tiers. Low-risk actions execute autonomously; high-risk actions halt execution until cryptographic human sign-off is verified.',
      principles: [
        'Tier 1 (Autonomous): Read-only, AST queries, internal parsing, background indexing.',
        'Tier 2 (Peer Review): Code review, draft critique, schema cross-check between agents.',
        'Tier 3 (Department Lead): Task completion, internal pull requests, draft approvals.',
        'Tier 4 (Legal / Fiduciary Gate): Client dispatches, regulatory submissions, external web calls.',
        'Tier 5 (Human CEO Signature): Treasury disbursements, commercial agreements, public commitments.'
      ],
      metrics: '5 Discrete Risk Tiers // 0% Hallucinated Commits',
      codeSnippet: `// 5-Tier Approval Gate Rule Matrix
enum PermissionTier {
  TIER_1_AUTONOMOUS = 1,       // read, grep, list (local sandbox)
  TIER_2_PEER_REVIEW = 2,      // automated subagent cross-validation
  TIER_3_DEPT_LEAD = 3,        // department lead agent sign-off
  TIER_4_LEGAL_FIDUCIARY = 4,  // legal & data protection verification
  TIER_5_HUMAN_CEO = 5         // Jack Mlusu cryptographic key signature
}`
    },
    {
      id: 'V',
      letter: 'V',
      name: 'Value & Verification',
      headline: 'Immutable SHA-256 Audit Chains & Quantified Impact',
      coreQuestion: 'What verifiable outcomes are delivered, and how are statutory audits satisfied?',
      summary: 'Every prompt, tool invocation, human decision, and output is linked in a cryptographic SHA-256 tamper-evident hash chain. Mathematical verification is paired with proven field delivery.',
      principles: [
        'Tamper-Evident Hash Chain: Every step references the previous SHA-256 block hash.',
        'Pydantic Domain Safety: Strict type validation before any database state transition.',
        'Proven In-House: Tested across 144 agents running daily operations at LightSpeed Holdings.',
        'Field-Validated Impact: 48hr → 14.2s mobile money settlement audit; 25k+ smallholders served.'
      ],
      metrics: 'SHA-256 Hash Chaining // 48h → 14.2s Latency Collapse',
      codeSnippet: `// SHA-256 Tamper-Evident Ledger Entry
{
  "blockIndex": 48291,
  "timestamp": "2026-09-13T04:15:00Z",
  "agentId": "fintech-settlement-guard",
  "action": "RECONCILE_BATCH_MWK",
  "inputsHash": "0x4e9c12a...77b1",
  "outputsHash": "0x892fa10...f82a",
  "humanApprovalSig": "0x992b_jack_mlusu_ceo_verified",
  "prevBlockHash": "0x33b1e90...112a",
  "currentBlockHash": "0x77fa21e...889c"
}`
    }
  ];

  // Tool Sandbox Definitions
  const canonicalTools = [
    { 
      name: 'read', 
      desc: 'Read file contents within workspace root. Symlink traversal denied.',
      sampleCmd: 'read("company-registry.yaml")',
      output: '20 departments loaded, 144 agents validated against pydantic schema.'
    },
    { 
      name: 'edit', 
      desc: 'Exact string replacement. Prevents accidental whole-file wipes.',
      sampleCmd: 'edit(target="src/models.py", old="v1.0", new="v2.0")',
      output: 'Exact match verified. Replaced 1 occurrence without modifying surrounding syntax.'
    },
    { 
      name: 'grep', 
      desc: 'AST-safe regex search. Skips binary assets, node_modules, and virtualenvs.',
      sampleCmd: 'grep(pattern="ApprovalGate", path="src/")',
      output: 'Found 14 occurrences in src/ai_company/security/rbac.py and orchestrator.'
    },
    { 
      name: 'list', 
      desc: 'Directory enumeration with path-traversal sandboxing.',
      sampleCmd: 'list(".opencode/agents/")',
      output: '144 markdown agent cards indexed in local directory.'
    },
    { 
      name: 'bash', 
      desc: 'Timeout-bounded, non-interactive shell command runner. Dangerous commands blocked.',
      sampleCmd: 'bash("pytest tests/test_governance.py")',
      output: '38 passed in 1.42s. All 5-tier gate evaluations green.'
    },
    { 
      name: 'webfetch', 
      desc: 'HTTP/HTTPS fetcher with domain whitelist. Zero token egress.',
      sampleCmd: 'webfetch("https://rbm.mw/rates")',
      output: 'Fetched RBM official MK/USD fixing rate into memory cache.'
    },
    { 
      name: 'task', 
      desc: 'Subagent DAG spawn runner with bounded recursion depth.',
      sampleCmd: 'task(subagent="thought-leadership-author", prompt="Draft tome section")',
      output: 'Subagent process spawned under task-8921; status updated in .opencode/inbox.json.'
    }
  ];

  // Pre-configured Simulator Tasks
  const simTasks = [
    {
      title: 'Disburse MWK 4,500,000 for Lilongwe Server SSD Spares',
      department: 'Finance',
      initiator: 'datacenter-operations-agent',
      tier: 5,
      tierLabel: 'Tier 5 (Human CEO Cryptographic Key)',
      details: 'Critical purchase of enterprise NVMe SSD spares for sovereign server racks in Lilongwe datacenter.',
      risk: 'High Financial Commitment',
      requiresCeo: true
    },
    {
      title: 'Submit SADC Cross-Border AI Data Transfer Consultation Draft',
      department: 'Pharos',
      initiator: 'policy-analyst',
      tier: 4,
      tierLabel: 'Tier 4 (Legal & Fiduciary Sign-Off)',
      details: 'Formal submission to Malawi Ministry of Information & Communications Technology on Chichewa model laws.',
      risk: 'High Regulatory Exposure',
      requiresCeo: false
    },
    {
      title: 'Deploy Hotfix to Mobile Money Reconciliation Pipeline',
      department: 'Technology',
      initiator: 'lead-backend',
      tier: 3,
      tierLabel: 'Tier 3 (Department Lead Sign-Off)',
      details: 'Merge audited bugfix for Airtel Money webhook timeout handler into main branch.',
      risk: 'Production Service Logic',
      requiresCeo: false
    },
    {
      title: 'Cross-Validate Chichewa Agronomy Vector Embeddings',
      department: 'AI Research',
      initiator: 'prompt-evaluator',
      tier: 2,
      tierLabel: 'Tier 2 (Subagent Peer Review)',
      details: 'Automated cosine similarity check on 5,000 localized farming tips generated by advisory subagent.',
      risk: 'Content Quality Gate',
      requiresCeo: false
    },
    {
      title: 'Nightly AST Knowledge Graph Update (graphify update .)',
      department: 'Technology',
      initiator: 'graphify-updater',
      tier: 1,
      tierLabel: 'Tier 1 (Autonomous Execution)',
      details: 'AST-only code structure graph sync without internet egress or API token cost.',
      risk: 'Zero External Risk',
      requiresCeo: false
    }
  ];

  // Filtering Agents
  const currentDepartment = departmentsList.find(d => d.id === selectedDeptId) || departmentsList[0];
  
  const filteredAgents = useMemo(() => {
    return agentsList.filter(agent => {
      // Dept match
      const deptMatch = agent.department.toLowerCase().replace(/\s+/g, '_') === currentDepartment.id ||
                        agent.department.toLowerCase() === currentDepartment.name.toLowerCase();
      
      // Search query
      const queryMatch = !agentSearchQuery || 
        agent.name.toLowerCase().includes(agentSearchQuery.toLowerCase()) ||
        agent.role.toLowerCase().includes(agentSearchQuery.toLowerCase()) ||
        agent.description.toLowerCase().includes(agentSearchQuery.toLowerCase());
      
      // Tool filter
      const toolMatch = selectedToolFilter === 'all' || 
        agent.tools.includes(selectedToolFilter);

      return deptMatch && queryMatch && toolMatch;
    });
  }, [currentDepartment, agentSearchQuery, selectedToolFilter]);

  // Total agents count per department
  const departmentCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    departmentsList.forEach(d => {
      counts[d.id] = agentsList.filter(a => 
        a.department.toLowerCase().replace(/\s+/g, '_') === d.id ||
        a.department.toLowerCase() === d.name.toLowerCase()
      ).length;
    });
    return counts;
  }, []);

  const totalAgents = agentsList.length;

  const currentPillar = pillars.find(p => p.id === activePillar) || pillars[0];
  const activeSimTask = simTasks[activeSimTaskIndex];

  // Simulation runner
  const runTaskSimulation = () => {
    setSweepNotice(null);
    setSimulatedTaskState('routing');
    setTimeout(() => {
      setSimulatedTaskState('evaluating');
      setTimeout(() => {
        setSimulatedTaskState('approved');
        const randomHash = '0x' + Array.from({length: 16}, () => Math.floor(Math.random()*16).toString(16)).join('') + '...' + Array.from({length: 4}, () => Math.floor(Math.random()*16).toString(16)).join('');
        setGeneratedBlockHash(randomHash);
      }, 1200);
    }, 800);
  };

  // Rule 9.1 HITL Expiry Sweep Simulation
  const triggerExpirySweep = () => {
    setSimulatedTaskState('routing');
    setTimeout(() => {
      setSimulatedTaskState('expired');
      setSweepNotice('RULE 9.1 HITL SWEEP TRIGGERED: Task was PENDING beyond TTL window. Transitioned safely to EXPIRED to prevent inbox deadlock.');
    }, 600);
  };

  return (
    <div id="haomtgv-framework" className={`p-5 sm:p-8 lg:p-10 rounded-3xl border relative overflow-hidden transition-all shadow-2xl ${
      isLight 
        ? 'bg-[#edf3f8] border-[#e5b74c]/30 shadow-[0_12px_40px_rgba(6,13,22,0.08)]' 
        : 'bg-gradient-to-b from-[#091624] via-[#060d16] to-[#040810] border-[#e5b74c]/25 shadow-[0_20px_60px_rgba(0,0,0,0.85)]'
    }`}>
      {/* Structural Corner Fasteners */}
      <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
      <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
      <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
      <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

      {/* Top Telemetry & Spec Ribbon */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 mb-6 border-b border-[#e5b74c]/20">
        <div className="flex items-center gap-2.5 flex-wrap">
          <StatusLedPip status="emerald" isLight={isLight} />
          <span className="text-xs font-mono font-extrabold uppercase tracking-wider text-[#e5b74c]">
            SOVEREIGN GOVERNANCE FRAMEWORK
          </span>
          <span className="text-zinc-500 hidden sm:inline">•</span>
          <span className={`text-[11px] font-mono px-2 py-0.5 rounded ${
            isLight ? 'bg-amber-100 text-amber-900 border border-amber-300' : 'bg-[#0f2231] text-[#f7d77c] border border-[#e5b74c]/30'
          }`}>
            SPEC::H-A-O-M-T-G-V
          </span>
          <span className="text-zinc-500 hidden sm:inline">•</span>
          <span className="text-[11px] font-mono text-zinc-400">
            144 AGENTS // 20 DEPARTMENTS // ZERO AIR-GAP COMPROMISE
          </span>
        </div>

        <div className="flex items-center gap-2">
          <AcousticVentGrille cols={6} rows={2} isLight={isLight} />
          <span className={`text-[11px] font-mono px-2 py-1 rounded font-bold ${
            isLight ? 'bg-slate-200 text-slate-800' : 'bg-[#163246] text-emerald-400 border border-emerald-500/30'
          }`}>
            PROVEN IN PRODUCTION
          </span>
        </div>
      </div>

      {/* Headline & Abstract */}
      <div className="mb-8 space-y-3">
        <h2 className={`text-2xl sm:text-3xl lg:text-4xl font-extrabold font-display tracking-tight ${
          isLight ? 'text-slate-900' : 'text-slate-100'
        }`}>
          The <span className="bg-gradient-to-r from-[#e5b74c] via-[#f7d77c] to-[#c49332] bg-clip-text text-transparent">H-A-O-M-T-G-V</span> Agentic Governance Framework
        </h2>
        <p className={`text-sm sm:text-base max-w-4xl leading-relaxed ${
          isLight ? 'text-slate-700' : 'text-slate-300'
        }`}>
          How LightSpeed orchestrates <strong>144 specialist agents</strong> inside a governed, air-gapped corporate hierarchy. 
          Built on deterministic Directed Acyclic Graphs (DAGs), cryptographic human approval gates, national soil data residency, 
          and an immutable SHA-256 audit ledger.
        </p>
      </div>

      {/* Master View Mode Switcher */}
      <div className="flex flex-wrap gap-2 mb-8 p-1.5 rounded-2xl border border-[#e5b74c]/25 bg-black/30 backdrop-blur-md">
        <button
          onClick={() => setActiveTab('pillars')}
          className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-mono font-bold uppercase transition-all flex items-center gap-2 ${
            activeTab === 'pillars'
              ? 'bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 shadow-lg shadow-amber-500/20'
              : isLight ? 'text-slate-700 hover:bg-slate-200' : 'text-slate-300 hover:bg-[#0f2231]'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>I. The 7 Pillars Deep Dive</span>
        </button>

        <button
          onClick={() => setActiveTab('roster')}
          className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-mono font-bold uppercase transition-all flex items-center gap-2 ${
            activeTab === 'roster'
              ? 'bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 shadow-lg shadow-amber-500/20'
              : isLight ? 'text-slate-700 hover:bg-slate-200' : 'text-slate-300 hover:bg-[#0f2231]'
          }`}
        >
          <Users className="w-4 h-4" />
          <span>II. 144-Agent Hierarchy Explorer ({totalAgents})</span>
        </button>

        <button
          onClick={() => setActiveTab('topology')}
          className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-mono font-bold uppercase transition-all flex items-center gap-2 ${
            activeTab === 'topology'
              ? 'bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 shadow-lg shadow-amber-500/20'
              : isLight ? 'text-slate-700 hover:bg-slate-200' : 'text-slate-300 hover:bg-[#0f2231]'
          }`}
        >
          <Network className="w-4 h-4" />
          <span>III. Air-Gapped Sovereign Topology</span>
        </button>

        <button
          onClick={() => setActiveTab('simulator')}
          className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-mono font-bold uppercase transition-all flex items-center gap-2 ${
            activeTab === 'simulator'
              ? 'bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 shadow-lg shadow-amber-500/20'
              : isLight ? 'text-slate-700 hover:bg-slate-200' : 'text-slate-300 hover:bg-[#0f2231]'
          }`}
        >
          <ShieldCheck className="w-4 h-4" />
          <span>IV. 5-Tier Gate Simulator & Rule 9.1</span>
        </button>
      </div>

      {/* TAB 1: THE 7 PILLARS DEEP DIVE */}
      {activeTab === 'pillars' && (
        <div className="space-y-8 animate-in fade-in duration-300">
          {/* Pillar Selector Tabs */}
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2.5">
            {pillars.map(p => {
              const isSelected = activePillar === p.id;
              return (
                <button
                  key={p.id}
                  onClick={() => setActivePillar(p.id as any)}
                  className={`p-3 rounded-2xl border text-left transition-all relative overflow-hidden group ${
                    isSelected
                      ? 'bg-gradient-to-br from-[#163246] to-[#0f2231] border-[#e5b74c] shadow-lg shadow-amber-500/20'
                      : isLight
                        ? 'bg-white border-slate-300 hover:border-amber-400'
                        : 'bg-[#091624]/80 border-[#163246] hover:border-[#e5b74c]/50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-base sm:text-lg font-black font-mono ${
                      isSelected ? 'text-[#f7d77c]' : 'text-[#e5b74c]'
                    }`}>
                      {p.letter}
                    </span>
                    <StatusLedPip 
                      status={isSelected ? 'amber' : 'emerald'} 
                      isLight={isLight} 
                    />
                  </div>
                  <div className={`text-xs font-bold truncate ${
                    isSelected ? (isLight ? 'text-slate-900' : 'text-white') : (isLight ? 'text-slate-700' : 'text-slate-300')
                  }`}>
                    {p.name}
                  </div>
                  <div className="text-[10px] font-mono text-zinc-400 truncate mt-0.5">
                    {p.id === 'H' && 'Apex Sovereign'}
                    {p.id === 'A' && '144 Agents'}
                    {p.id === 'O' && 'DAG Message Bus'}
                    {p.id === 'M' && 'AST Memory'}
                    {p.id === 'T' && '7 Canonical Tools'}
                    {p.id === 'G' && '5-Tier Gates'}
                    {p.id === 'V' && 'SHA-256 Ledger'}
                  </div>
                </button>
              );
            })}
          </div>

          {/* Active Pillar Full Profile */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Left Narrative Column */}
            <div className="lg:col-span-7 space-y-6">
              <div className={`p-6 sm:p-8 rounded-2xl border ${
                isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-[#0f2231]/90 border-[#163246] shadow-xl'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-[#e5b74c]/20 text-[#e5b74c] border border-[#e5b74c]/30">
                    PILLAR {currentPillar.letter} // {currentPillar.name.toUpperCase()}
                  </span>
                  <span className="text-xs font-mono text-zinc-400">•</span>
                  <span className="text-xs font-mono text-emerald-400 font-semibold">{currentPillar.metrics}</span>
                </div>

                <h3 className={`text-xl sm:text-2xl font-bold font-display mb-3 ${
                  isLight ? 'text-slate-900' : 'text-white'
                }`}>
                  {currentPillar.headline}
                </h3>

                <p className={`text-xs font-mono mb-4 p-3 rounded-xl border ${
                  isLight ? 'bg-amber-50/70 border-amber-200 text-amber-900' : 'bg-[#060d16] border-[#e5b74c]/20 text-[#f7d77c]'
                }`}>
                  <span className="font-bold text-[#e5b74c]">CORE DIRECTIVE:</span> {currentPillar.coreQuestion}
                </p>

                <p className={`text-sm leading-relaxed mb-6 ${
                  isLight ? 'text-slate-700' : 'text-slate-200'
                }`}>
                  {currentPillar.summary}
                </p>

                <div className="space-y-3 border-t border-[#e5b74c]/20 pt-4">
                  <h4 className="text-xs font-mono font-bold text-[#e5b74c] uppercase tracking-wider">
                    OPERATIONAL PRINCIPLES
                  </h4>
                  {currentPillar.principles.map((pr, idx) => (
                    <div key={idx} className="flex items-start gap-3 text-xs">
                      <CheckCircle2 className="w-4 h-4 text-[#e5b74c] shrink-0 mt-0.5" />
                      <span className={isLight ? 'text-slate-800' : 'text-slate-200'}>{pr}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Dynamic Feature Sandbox based on Pillar */}
              {activePillar === 'T' && (
                <div className={`p-6 rounded-2xl border ${
                  isLight ? 'bg-white border-slate-300' : 'bg-[#0f2231] border-[#163246]'
                }`}>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-mono font-bold text-[#e5b74c] uppercase">
                      INTERACTIVE CANONICAL 7-TOOL RUNNER
                    </span>
                    <span className="text-[10px] font-mono text-emerald-400">Zero Arbitrary Execution</span>
                  </div>

                  <div className="flex flex-wrap gap-2 mb-4">
                    {canonicalTools.map(ct => (
                      <button
                        key={ct.name}
                        onClick={() => {
                          setSelectedTool(ct.name);
                          setSimulatedToolOutput('');
                        }}
                        className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition-all border ${
                          selectedTool === ct.name
                            ? 'bg-[#e5b74c] text-slate-950 border-[#f7d77c]'
                            : isLight ? 'bg-slate-100 text-slate-800 border-slate-300' : 'bg-[#091624] text-slate-300 border-[#163246]'
                        }`}
                      >
                        tool::{ct.name}
                      </button>
                    ))}
                  </div>

                  {(() => {
                    const activeCt = canonicalTools.find(c => c.name === selectedTool) || canonicalTools[0];
                    return (
                      <div className="space-y-3 text-xs font-mono p-4 rounded-xl bg-black/40 border border-[#163246]">
                        <div><span className="text-[#e5b74c] font-bold">Runtime Spec:</span> <span className="text-slate-200">{activeCt.desc}</span></div>
                        <div><span className="text-zinc-400">Execution Call:</span> <code className="text-[#f7d77c]">{activeCt.sampleCmd}</code></div>
                        <div className="pt-2 flex items-center justify-between">
                          <button
                            onClick={() => setSimulatedToolOutput(activeCt.output)}
                            className="px-3 py-1 rounded bg-[#e5b74c] text-slate-950 font-bold uppercase tracking-wider text-[11px] hover:bg-[#f7d77c] transition-colors"
                          >
                            Execute Sandboxed Probe
                          </button>
                          {simulatedToolOutput && (
                            <span className="text-[10px] text-emerald-400">OK 200 // SANDBOX VERIFIED</span>
                          )}
                        </div>
                        {simulatedToolOutput && (
                          <div className="p-2.5 rounded bg-[#060d16] border border-emerald-500/40 text-emerald-300 text-[11px]">
                            {simulatedToolOutput}
                          </div>
                        )}
                      </div>
                    );
                  })()}
                </div>
              )}

              {activePillar === 'H' && (
                <div className={`p-6 rounded-2xl border ${
                  isLight ? 'bg-white border-slate-300' : 'bg-[#0f2231] border-[#163246]'
                }`}>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-mono font-bold text-[#e5b74c] uppercase">
                      RULE 9.1 HITL EXPIRY SWEEP SIMULATOR
                    </span>
                    <span className="text-[10px] font-mono text-zinc-400">Anti-Deadlock Daemon</span>
                  </div>
                  <p className={`text-xs mb-4 ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
                    In a 144-agent enterprise, a pending human review could indefinitely lock dependent DAG subtasks. 
                    Rule 9.1 executes a scheduled governance sweep: any PENDING approval exceeding its TTL transitions to <strong>EXPIRED</strong>, 
                    notifying the human executive while releasing locked worker threads.
                  </p>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={triggerExpirySweep}
                      className="px-4 py-2 rounded-xl bg-[#e5b74c] text-slate-950 font-mono text-xs font-bold uppercase tracking-wider hover:bg-[#f7d77c] transition-colors flex items-center gap-2"
                    >
                      <RotateCcw className="w-3.5 h-3.5" />
                      Trigger Rule 9.1 Expiry Sweep
                    </button>
                    {simulatedTaskState === 'expired' && (
                      <span className="text-xs font-mono text-rose-400 font-bold">
                        TERMINAL: EXPIRED (Inbox Freed)
                      </span>
                    )}
                  </div>
                  {sweepNotice && (
                    <div className="mt-3 p-3 rounded-xl bg-rose-950/40 border border-rose-500/40 text-xs font-mono text-rose-300">
                      {sweepNotice}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Right Column: Air-Gapped Code Spec & Boundary Schema */}
            <div className="lg:col-span-5 space-y-6">
              <div className={`p-5 rounded-2xl border font-mono text-xs ${
                isLight ? 'bg-slate-900 text-slate-100 border-slate-800' : 'bg-[#060d16] text-slate-200 border-[#163246] shadow-xl'
              }`}>
                <div className="flex items-center justify-between pb-3 mb-3 border-b border-[#163246]">
                  <div className="flex items-center gap-2">
                    <FileCode className="w-4 h-4 text-[#e5b74c]" />
                    <span className="text-[#e5b74c] font-bold uppercase tracking-wider">
                      {currentPillar.name.replace(/\s+/g, '_').toLowerCase()}.spec.yaml
                    </span>
                  </div>
                  <span className="text-[10px] text-zinc-500">AIR-GAPPED COMPLIANT</span>
                </div>
                <pre className="text-emerald-400/90 overflow-x-auto text-[11px] leading-relaxed p-2 font-mono scrollbar-thin">
                  {currentPillar.codeSnippet}
                </pre>
              </div>

              {/* Sovereign Boundary Matrix */}
              <div className={`p-6 rounded-2xl border ${
                isLight ? 'bg-white border-slate-300' : 'bg-[#0f2231] border-[#163246]'
              }`}>
                <div className="flex items-center gap-2 mb-4 text-xs font-mono text-[#e5b74c] font-bold uppercase">
                  <ShieldCheck className="w-4 h-4 text-[#e5b74c]" />
                  <span>SOVEREIGN BOUNDARY MATRIX</span>
                </div>

                <div className="space-y-2.5 text-xs font-mono">
                  <div className="p-3 rounded-xl border border-[#163246] bg-black/40 flex items-center justify-between">
                    <span className="text-zinc-300">Apex Authority</span>
                    <span className="text-[#f7d77c] font-bold">Human CEO // Jack Mlusu</span>
                  </div>
                  <div className="p-3 rounded-xl border border-[#163246] bg-black/40 flex items-center justify-between">
                    <span className="text-zinc-300">Total Workforce</span>
                    <span className="text-[#f7d77c] font-bold">144 Specialist Agents</span>
                  </div>
                  <div className="p-3 rounded-xl border border-[#163246] bg-black/40 flex items-center justify-between">
                    <span className="text-zinc-300">Datacenter Soil</span>
                    <span className="text-emerald-400 font-bold">Lilongwe Server Node</span>
                  </div>
                  <div className="p-3 rounded-xl border border-[#163246] bg-black/40 flex items-center justify-between">
                    <span className="text-zinc-300">Public Cloud Egress</span>
                    <span className="text-rose-400 font-bold">0.00% (Strict Air-Gap)</span>
                  </div>
                  <div className="p-3 rounded-xl border border-[#163246] bg-black/40 flex items-center justify-between">
                    <span className="text-zinc-300">Audit Ledger</span>
                    <span className="text-emerald-400 font-bold">SHA-256 Tamper-Evident</span>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-[#163246]">
                  <button
                    onClick={() => onOpenContactModal?.('H-A-O-M-T-G-V Sovereign Architecture Briefing')}
                    className="w-full py-2.5 rounded-xl bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 font-mono text-xs font-bold uppercase tracking-wider hover:opacity-95 transition-opacity"
                  >
                    Request Institutional Briefing
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: 144-AGENT HIERARCHY EXPLORER */}
      {activeTab === 'roster' && (
        <div className="space-y-6 animate-in fade-in duration-300">
          {/* Department Navigator Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-2xl border border-[#e5b74c]/20 bg-black/30">
            <div>
              <h3 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                20 Governed Departments ({totalAgents} Active Specialist Agents)
              </h3>
              <p className="text-xs text-zinc-400 font-mono">
                Select a department to explore its specialist agent workforce and OpenCode v2 cards.
              </p>
            </div>

            {/* Filter & Search Bar */}
            <div className="flex items-center gap-2 flex-wrap">
              <div className="relative">
                <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" />
                <input
                  type="text"
                  placeholder="Search 144 agents..."
                  value={agentSearchQuery}
                  onChange={(e) => setAgentSearchQuery(e.target.value)}
                  className="pl-8 pr-3 py-1.5 rounded-lg text-xs font-mono bg-[#060d16] border border-[#163246] text-white placeholder-zinc-500 focus:outline-none focus:border-[#e5b74c]"
                />
              </div>

              <select
                value={selectedToolFilter}
                onChange={(e) => setSelectedToolFilter(e.target.value)}
                className="px-3 py-1.5 rounded-lg text-xs font-mono bg-[#060d16] border border-[#163246] text-white focus:outline-none focus:border-[#e5b74c]"
              >
                <option value="all">All Tools</option>
                <option value="read">Tool: read</option>
                <option value="edit">Tool: edit</option>
                <option value="grep">Tool: grep</option>
                <option value="list">Tool: list</option>
                <option value="bash">Tool: bash</option>
                <option value="webfetch">Tool: webfetch</option>
                <option value="task">Tool: task</option>
              </select>
            </div>
          </div>

          {/* Department Buttons Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-2 max-h-60 overflow-y-auto pr-1 scrollbar-thin">
            {departmentsList.map(dept => {
              const count = departmentCounts[dept.id] || 0;
              const isSelected = selectedDeptId === dept.id;
              return (
                <button
                  key={dept.id}
                  onClick={() => setSelectedDeptId(dept.id)}
                  className={`p-2.5 rounded-xl text-left border transition-all text-xs font-mono ${
                    isSelected
                      ? 'bg-gradient-to-br from-[#163246] to-[#0f2231] border-[#e5b74c] text-white font-bold'
                      : isLight
                        ? 'bg-white border-slate-300 text-slate-700 hover:border-amber-400'
                        : 'bg-[#091624]/70 border-[#163246] text-slate-300 hover:border-[#e5b74c]/50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="truncate">{dept.name}</span>
                    <span className={`text-[10px] px-1.5 py-0.2 rounded ${
                      isSelected ? 'bg-[#e5b74c] text-slate-950 font-bold' : 'bg-black/40 text-[#f7d77c]'
                    }`}>
                      {count}
                    </span>
                  </div>
                  <div className="text-[10px] opacity-70 truncate mt-0.5">
                    Lead: @{dept.executive}
                  </div>
                </button>
              );
            })}
          </div>

          {/* Department Lead & Mission Banner */}
          <div className={`p-4 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
            isLight ? 'bg-amber-50 border-amber-300 text-slate-800' : 'bg-[#0f2231] border-[#e5b74c]/30 text-slate-200'
          }`}>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-bold text-[#e5b74c] uppercase">
                  DEPARTMENT: {currentDepartment.name.toUpperCase()}
                </span>
                <span className="text-xs text-zinc-400">•</span>
                <span className="text-xs font-mono text-emerald-400">Headcount Target: {currentDepartment.headcount_target}</span>
              </div>
              <p className="text-xs mt-1 leading-snug">{currentDepartment.mission}</p>
            </div>
            <div className="shrink-0 text-xs font-mono">
              <span className="text-zinc-400">Lead Executive:</span> <code className="text-[#f7d77c] font-bold">@{currentDepartment.executive}</code>
            </div>
          </div>

          {/* Agents Roster Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {filteredAgents.map(agent => (
              <div
                key={agent.name}
                className={`p-4 rounded-2xl border transition-all text-xs font-mono flex flex-col justify-between ${
                  isLight 
                    ? 'bg-white border-slate-300 shadow-sm' 
                    : 'bg-[#091624] border-[#163246] hover:border-[#e5b74c]/50'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-bold text-[#f7d77c] truncate text-sm">
                      @{agent.name}
                    </span>
                    <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${
                      agent.type === 'Executive' 
                        ? 'bg-purple-950 text-purple-300 border border-purple-500/40'
                        : 'bg-emerald-950 text-emerald-300 border border-emerald-500/40'
                    }`}>
                      {agent.type}
                    </span>
                  </div>

                  <div className={`font-semibold mb-1 ${isLight ? 'text-slate-800' : 'text-slate-200'}`}>
                    {agent.role}
                  </div>

                  <p className={`text-[11px] line-clamp-2 mb-3 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                    {agent.description || 'Specialized role inside governed corporate hierarchy.'}
                  </p>
                </div>

                <div className="space-y-2 pt-2 border-t border-[#163246]/60">
                  <div className="flex items-center justify-between text-[10px] text-zinc-400">
                    <span>Reports to: <code className="text-amber-400">@{agent.reportsTo}</code></span>
                    <span>Perm: <span className="text-emerald-400 font-bold">{agent.permission}</span></span>
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <div className="flex flex-wrap gap-1">
                      {agent.tools.slice(0, 3).map(t => (
                        <span key={t} className="text-[9px] px-1.5 py-0.5 rounded bg-black/40 border border-[#163246] text-zinc-300">
                          {t}
                        </span>
                      ))}
                      {agent.tools.length > 3 && (
                        <span className="text-[9px] px-1 py-0.5 text-zinc-500">+{agent.tools.length - 3}</span>
                      )}
                    </div>

                    <button
                      onClick={() => setInspectingAgent(agent)}
                      className="text-[11px] font-bold text-[#e5b74c] hover:text-[#f7d77c] flex items-center gap-1 transition-colors"
                    >
                      <Eye className="w-3 h-3" /> Inspect Card
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredAgents.length === 0 && (
            <div className="p-8 text-center rounded-2xl border border-dashed border-[#163246] text-zinc-400 text-xs font-mono">
              No agents found matching your query in this department.
            </div>
          )}
        </div>
      )}

      {/* TAB 3: AIR-GAPPED SOVEREIGN BOUNDARY TOPOLOGY */}
      {activeTab === 'topology' && (
        <div className="space-y-8 animate-in fade-in duration-300">
          <div className={`p-6 sm:p-8 rounded-3xl border ${
            isLight ? 'bg-white border-slate-300' : 'bg-[#0f2231] border-[#163246]'
          }`}>
            <div className="max-w-3xl mb-6">
              <span className="text-xs font-mono font-bold text-[#e5b74c] uppercase tracking-wider block mb-1">
                HARDWARE-ENFORCED SOVEREIGN ISOLATION
              </span>
              <h3 className={`text-xl sm:text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                The Sovereign Air-Gap Architecture
              </h3>
              <p className={`text-xs sm:text-sm mt-2 ${isLight ? 'text-slate-700' : 'text-slate-300'}`}>
                All 144 specialist agents execute exclusively within a localized, sovereign compute enclave hosted on 
                Lilongwe soil. Zero inference tokens, organizational schematics, or banking payloads leave Malawi borders.
              </p>
            </div>

            {/* Visual Topology Diagram */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
              {/* Box 1: Ingestion & Apex Gate */}
              <div className="p-5 rounded-2xl bg-black/40 border border-[#163246] space-y-3">
                <div className="flex items-center gap-2 text-[#e5b74c] font-bold uppercase text-xs">
                  <Key className="w-4 h-4" />
                  <span>Layer 1: Human Apex Gate</span>
                </div>
                <p className="text-[11px] text-zinc-300">
                  Constitutional commands originating from Human CEO (Jack Mlusu) and Board. 
                  Encrypted via ed25519 asymmetric key pairs before ingestion into task queue.
                </p>
                <div className="p-2.5 rounded-lg bg-[#060d16] border border-[#163246] text-[10px] text-[#f7d77c]">
                  HITL Gate: Active (Rule 9.1 Sweep Enabled)
                </div>
              </div>

              {/* Box 2: IPC Message Bus & 144 Agents */}
              <div className="p-5 rounded-2xl bg-[#163246]/40 border border-[#e5b74c]/40 space-y-3 relative overflow-hidden">
                <div className="flex items-center gap-2 text-[#f7d77c] font-bold uppercase text-xs">
                  <Cpu className="w-4 h-4" />
                  <span>Layer 2: 144 Swarm Runtime</span>
                </div>
                <p className="text-[11px] text-slate-200">
                  Directed Acyclic Graph (DAG) state machine running at .opencode/inbox.json. 
                  Sub-second inter-process communication (&lt;180ms) without public internet calls.
                </p>
                <div className="p-2.5 rounded-lg bg-[#060d16] border border-[#163246] text-[10px] text-emerald-400">
                  Air-Gap Barrier: 100% BLOCKED EGRESS
                </div>
              </div>

              {/* Box 3: Sovereign Memory & Ledger */}
              <div className="p-5 rounded-2xl bg-black/40 border border-[#163246] space-y-3">
                <div className="flex items-center gap-2 text-emerald-400 font-bold uppercase text-xs">
                  <Database className="w-4 h-4" />
                  <span>Layer 3: AST Memory & Ledger</span>
                </div>
                <p className="text-[11px] text-zinc-300">
                  graphify AST knowledge graph and SHA-256 tamper-evident hash ledger. 
                  All states recorded immutably on encrypted disk arrays on Malawi soil.
                </p>
                <div className="p-2.5 rounded-lg bg-[#060d16] border border-[#163246] text-[10px] text-zinc-400">
                  Ledger: SHA-256 Tamper-Proof Chain
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: 5-TIER GATE SIMULATOR & RULE 9.1 */}
      {activeTab === 'simulator' && (
        <div className="space-y-8 animate-in fade-in duration-300">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Left Controls */}
            <div className="lg:col-span-6 space-y-6">
              <div className={`p-6 sm:p-8 rounded-3xl border ${
                isLight ? 'bg-white border-slate-300' : 'bg-[#0f2231] border-[#163246]'
              }`}>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-mono font-bold text-[#e5b74c] uppercase">
                    5-TIER APPROVAL GATE SIMULATOR
                  </span>
                  <span className="text-[10px] font-mono text-zinc-400">Interactive Probe</span>
                </div>

                <p className={`text-xs mb-4 leading-relaxed ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
                  Select a real-world enterprise scenario to observe how the H-A-O-M-T-G-V governance framework evaluates 
                  risk tiers, checks cryptographic signatures, and prevents unauthorized execution.
                </p>

                {/* Preconfigured Scenarios */}
                <div className="space-y-2 mb-6">
                  {simTasks.map((task, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        setActiveSimTaskIndex(idx);
                        setSimulatedTaskState('idle');
                        setSweepNotice(null);
                        setGeneratedBlockHash('');
                      }}
                      className={`w-full text-left p-3 rounded-xl border text-xs font-mono transition-all ${
                        activeSimTaskIndex === idx
                          ? 'bg-[#163246] border-[#e5b74c] text-white font-bold'
                          : isLight ? 'bg-slate-50 border-slate-300 text-slate-700' : 'bg-[#091624] border-[#163246] text-slate-300'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="truncate">{task.title}</span>
                        <span className="text-[10px] px-2 py-0.5 rounded bg-black/40 text-[#f7d77c] font-bold">
                          Tier {task.tier}
                        </span>
                      </div>
                      <div className="text-[10px] text-zinc-400 truncate">
                        {task.department} // {task.risk}
                      </div>
                    </button>
                  ))}
                </div>

                {/* Simulation Control Buttons */}
                <div className="flex items-center gap-3 pt-4 border-t border-[#163246]">
                  <button
                    onClick={runTaskSimulation}
                    disabled={simulatedTaskState === 'routing' || simulatedTaskState === 'evaluating'}
                    className="flex-1 py-2.5 rounded-xl bg-gradient-to-r from-[#e5b74c] to-[#c49332] text-slate-950 font-mono text-xs font-bold uppercase tracking-wider hover:opacity-95 transition-opacity disabled:opacity-50"
                  >
                    {simulatedTaskState === 'approved' ? 'Re-Run Verification Gate' : 'Simulate 5-Tier Gate Check'}
                  </button>

                  <button
                    onClick={triggerExpirySweep}
                    className="px-3 py-2.5 rounded-xl bg-[#060d16] border border-rose-500/40 text-rose-300 font-mono text-xs font-bold uppercase hover:bg-rose-950/40 transition-colors"
                  >
                    Test Rule 9.1 Sweep
                  </button>
                </div>
              </div>
            </div>

            {/* Right Gate Output Display */}
            <div className="lg:col-span-6 space-y-4">
              <div className={`p-6 rounded-3xl border font-mono text-xs ${
                isLight ? 'bg-white border-slate-300' : 'bg-[#060d16] border-[#163246]'
              }`}>
                <div className="flex items-center justify-between pb-3 mb-4 border-b border-[#163246]">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-[#e5b74c]" />
                    <span className="text-[#e5b74c] font-bold uppercase">Gate Status Telemetry</span>
                  </div>
                  <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                    simulatedTaskState === 'approved' ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/40' :
                    simulatedTaskState === 'expired' ? 'bg-rose-950 text-rose-400 border border-rose-500/40' :
                    simulatedTaskState === 'routing' || simulatedTaskState === 'evaluating' ? 'bg-amber-950 text-amber-400 border border-amber-500/40' :
                    'bg-zinc-800 text-zinc-400'
                  }`}>
                    {simulatedTaskState}
                  </span>
                </div>

                <div className="space-y-3">
                  <div>
                    <span className="text-zinc-500">TASK:</span>{' '}
                    <span className="text-white font-semibold">{activeSimTask.title}</span>
                  </div>
                  <div>
                    <span className="text-zinc-500">REQUIRED TIER:</span>{' '}
                    <span className="text-[#f7d77c] font-bold">{activeSimTask.tierLabel}</span>
                  </div>
                  <div>
                    <span className="text-zinc-500">DETAILS:</span>{' '}
                    <span className="text-zinc-300">{activeSimTask.details}</span>
                  </div>
                  <div>
                    <span className="text-zinc-500">INITIATING AGENT:</span>{' '}
                    <code className="text-amber-400">@{activeSimTask.initiator}</code>
                  </div>

                  {/* Verification Pipeline Steps */}
                  <div className="pt-4 border-t border-[#163246] space-y-2">
                    <div className="flex items-center justify-between text-[11px]">
                      <span>1. Schema & Pydantic Validation</span>
                      <span className={simulatedTaskState !== 'idle' ? 'text-emerald-400' : 'text-zinc-600'}>
                        {simulatedTaskState !== 'idle' ? 'PASSED' : 'STANDBY'}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-[11px]">
                      <span>2. Canonical 7-Tool Whitelist Check</span>
                      <span className={simulatedTaskState !== 'idle' ? 'text-emerald-400' : 'text-zinc-600'}>
                        {simulatedTaskState !== 'idle' ? 'ENFORCED' : 'STANDBY'}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-[11px]">
                      <span>3. Air-Gap Egress Sandbox Barrier</span>
                      <span className={simulatedTaskState !== 'idle' ? 'text-emerald-400' : 'text-zinc-600'}>
                        {simulatedTaskState !== 'idle' ? '0.00% EGRESS' : 'STANDBY'}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-[11px]">
                      <span>4. Human Signature Gate (Tier {activeSimTask.tier})</span>
                      <span className={
                        simulatedTaskState === 'approved' ? 'text-emerald-400 font-bold' :
                        simulatedTaskState === 'expired' ? 'text-rose-400 font-bold' :
                        simulatedTaskState === 'evaluating' ? 'text-amber-400 animate-pulse' :
                        'text-zinc-600'
                      }>
                        {simulatedTaskState === 'approved' ? (activeSimTask.requiresCeo ? 'SIGNED (Jack Mlusu ed25519)' : 'VERIFIED') :
                         simulatedTaskState === 'expired' ? 'TTL EXPIRED' :
                         simulatedTaskState === 'evaluating' ? 'EVALUATING...' : 'PENDING'}
                      </span>
                    </div>
                  </div>

                  {/* Generated Hash Block */}
                  {generatedBlockHash && (
                    <div className="mt-4 p-3 rounded-xl bg-emerald-950/30 border border-emerald-500/40 text-emerald-300 text-[11px] space-y-1">
                      <div className="font-bold flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                        AUDIT BLOCK COMMITTED TO CHAIN
                      </div>
                      <div className="text-[10px] text-emerald-400/80">
                        BlockHash: <code className="text-white">{generatedBlockHash}</code>
                      </div>
                    </div>
                  )}

                  {sweepNotice && (
                    <div className="mt-4 p-3 rounded-xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-[11px]">
                      {sweepNotice}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Agent Card Inspector */}
      <AnimatePresence>
        {inspectingAgent && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className={`w-full max-w-2xl rounded-3xl border p-6 sm:p-8 font-mono text-xs relative max-h-[90vh] overflow-y-auto ${
                isLight ? 'bg-white text-slate-800 border-slate-300' : 'bg-[#091624] text-slate-200 border-[#e5b74c]/40 shadow-2xl'
              }`}
            >
              <button
                onClick={() => setInspectingAgent(null)}
                className="absolute top-4 right-4 p-2 rounded-full hover:bg-white/10 text-zinc-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>

              <div className="flex items-center gap-2 mb-3">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-[#e5b74c] text-slate-950">
                  OPENCODE V2 AGENT SPEC
                </span>
                <span className="text-zinc-500">•</span>
                <span className="text-zinc-400">{inspectingAgent.department}</span>
              </div>

              <h3 className="text-lg font-bold text-[#f7d77c] mb-1">
                @{inspectingAgent.name}
              </h3>
              <p className="text-sm font-semibold mb-4 text-white">
                {inspectingAgent.role}
              </p>

              <div className="space-y-4">
                <div className="p-3 rounded-xl bg-black/40 border border-[#163246] space-y-1.5">
                  <div><span className="text-zinc-400">Mode:</span> <span className="text-emerald-400">subagent</span></div>
                  <div><span className="text-zinc-400">Permission Tier:</span> <span className="text-[#f7d77c] font-bold">{inspectingAgent.permission}</span></div>
                  <div><span className="text-zinc-400">Reports To:</span> <code className="text-amber-300">@{inspectingAgent.reportsTo}</code></div>
                  <div>
                    <span className="text-zinc-400">Canonical Tools:</span>{' '}
                    <span className="text-white">[{inspectingAgent.tools.join(', ')}]</span>
                  </div>
                </div>

                <div>
                  <h4 className="font-bold text-[#e5b74c] mb-2 uppercase text-[11px]">Primary Responsibilities:</h4>
                  <ul className="list-disc list-inside space-y-1 text-zinc-300">
                    {inspectingAgent.responsibilities.length > 0 ? (
                      inspectingAgent.responsibilities.map((r, i) => <li key={i}>{r}</li>)
                    ) : (
                      <li>Execute specialized departmental tasks within air-gapped sandbox constraints.</li>
                    )}
                  </ul>
                </div>

                {inspectingAgent.guidelines && (
                  <div>
                    <h4 className="font-bold text-[#e5b74c] mb-2 uppercase text-[11px]">Operating Guidelines:</h4>
                    <p className="p-3 rounded-xl bg-black/30 border border-[#163246] text-zinc-300 leading-relaxed">
                      {inspectingAgent.guidelines}
                    </p>
                  </div>
                )}
              </div>

              <div className="mt-6 pt-4 border-t border-[#163246] flex justify-end">
                <button
                  onClick={() => setInspectingAgent(null)}
                  className="px-4 py-2 rounded-xl bg-[#e5b74c] text-slate-950 font-bold uppercase tracking-wider text-xs"
                >
                  Close Specification
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* Summary Footer */}
      <div className={`mt-8 pt-5 border-t flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono ${
        isLight ? 'border-slate-300 text-slate-600' : 'border-[#163246] text-zinc-400'
      }`}>
        <div className="flex items-center gap-2">
          <StatusLedPip status="emerald" isLight={isLight} />
          <span>PROVEN IN-HOUSE: Operating daily across LightSpeed Holdings Limited, Malawi.</span>
        </div>
        <div className="text-[#e5b74c] font-bold">
          Human Purpose → Agents → Orchestration → Memory → Tools → Governance → Value
        </div>
      </div>
    </div>
  );
};
