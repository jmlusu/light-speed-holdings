import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  ShieldCheck, 
  Scale, 
  Landmark, 
  FileText, 
  Lock, 
  CheckCircle2, 
  AlertTriangle, 
  Download, 
  ArrowRight, 
  BookOpen, 
  Globe2, 
  Cpu, 
  Layers, 
  Workflow, 
  Zap, 
  ChevronRight, 
  Building2, 
  Key, 
  Network, 
  Activity, 
  FileCheck, 
  Sparkles,
  ExternalLink,
  Coins,
  Shield,
  Clock,
  Compass,
  Check
} from 'lucide-react';
import { StatusBadge } from './ui/StatusBadge';
import { AcousticVentGrille } from './TactileHardwareElements';

interface SadcGovernanceFrameworkProps {
  theme?: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const SadcGovernanceFramework: React.FC<SadcGovernanceFrameworkProps> = ({
  theme = 'dark',
  onRequestBriefing
}) => {
  const isLight = theme === 'light';
  
  const [activeTab, setActiveTab] = useState<'principles' | 'hitl-matrix' | 'standards' | 'blueprints' | 'roadmap' | 'dossier'>('principles');
  const [activeTier, setActiveTier] = useState<number>(3);
  const [downloadedState, setDownloadedState] = useState<boolean>(false);
  const [activeSector, setActiveSector] = useState<'finance' | 'public-sector' | 'logistics'>('finance');

  const hitlTiers = [
    {
      tier: 1,
      risk: 'Low — Advisory',
      name: 'Advisory & Drafting',
      example: 'Market aggregation, policy drafting, summarization, research synthesis',
      control: 'No automated execution without explicit human output confirmation.',
      badgeColor: 'border-blue-500/30 text-blue-400 bg-blue-500/10',
      status: 'Advisory Only',
      sandboxRequired: false,
      technicalRequirement: 'Standard LLM prompt scoping with read-only sandbox context.'
    },
    {
      tier: 2,
      risk: 'Medium — Automated Workflow',
      name: 'Internal Workflows & DBs',
      example: 'Internal logistics routing, routine database catalog updates, inventory threshold alerts',
      control: 'Automated execution permitted with deterministic real-time append-only telemetry logging.',
      badgeColor: 'border-emerald-500/30 text-emerald-400 bg-emerald-500/10',
      status: 'Supervised Auto',
      sandboxRequired: false,
      technicalRequirement: 'Deterministic rate limiters, token budgets, and OpenCode canonical tool wrappers.'
    },
    {
      tier: 3,
      risk: 'High — Direct Execution',
      name: 'Fiduciary & Sovereign Actions',
      example: 'Financial disbursements, health records modification, customs/border processing, statutory filings',
      control: 'Mandatory Human-in-the-Loop (HITL) cryptographic authorization checkpoints prior to execution payload release.',
      badgeColor: 'border-orange-500/30 text-orange-400 bg-orange-500/10',
      status: 'Mandatory HITL Gate',
      sandboxRequired: true,
      technicalRequirement: 'Dual-key cryptographic signatures (PKI), SHA-256 state hashing, and automated expiry sweep.'
    },
    {
      tier: 4,
      risk: 'Critical — National Infrastructure',
      name: 'National Critical Systems',
      example: 'National power grid management, telecom core switching, water distribution, air traffic control',
      control: 'Autonomous execution strictly prohibited; decision-support and scenario modeling only.',
      badgeColor: 'border-red-500/30 text-red-400 bg-red-500/10',
      status: 'Autonomous Prohibited',
      sandboxRequired: true,
      technicalRequirement: 'Strict physical air-gapping of operational technology (OT) from internet-connected planning agents.'
    }
  ];

  const standardsData = [
    {
      domain: 'System Identity',
      standard: 'Machine-readable agent credentials (Agent ID, deployment hash, registered owning entity)',
      verification: 'Automated API-gateway audits & machine-identity verification by national regulators (MACRA / CRASA)',
      icon: Key
    },
    {
      domain: 'Audit Trails',
      standard: 'Deterministic execution logs capturing prompts, tool invocations, memory retrievals, and outputs',
      verification: 'Immutable append-only cryptographic ledger for High (Tier 3) and Critical (Tier 4) deployments',
      icon: FileCheck
    },
    {
      domain: 'Model Alignment',
      standard: 'Prompts, system cards, and tool boundaries formally aligned to SADC law, ethics, and data protection',
      verification: 'Mandatory independent third-party algorithmic audit prior to live commercial deployment',
      icon: ShieldCheck
    },
    {
      domain: 'Credential Management',
      standard: 'Scoped, least-privilege API keys; strictly no master admin credentials stored in agent context memory',
      verification: 'Continuous zero-trust architecture checks and automated programmatic kill switches',
      icon: Lock
    }
  ];

  const sectoralBlueprints = [
    {
      id: 'finance',
      title: 'Financial Services & Mobile Money Rails',
      scope: 'Commercial Banking (RTGS/SWIFT) • Airtel Money • TNM Mpamba • PayChangu • SACCOs',
      specs: [
        'Automated transaction volume and single-ticket caps calibrated by institutional tier.',
        'Multi-agent fraud anomaly monitoring with real-time account isolation and multi-sig recovery.',
        'Formal SADC regulatory sandbox provisions for agentic micro-lending and automated parametric crop insurance payouts.',
        'Direct integration with central bank RTGS settlement while preserving local mobile money liquidity buffers.'
      ],
      compliance: 'Basel IV / SADC Central Bank Model Law / Malawi Financial Services Act'
    },
    {
      id: 'public-sector',
      title: 'Public Sector, Healthcare & NGO M&E',
      scope: 'Ministry of Health • Agricultural Extension • DHIS2 • KoboToolbox • Multilateral Donors',
      specs: [
        'Autonomous monitoring and evaluation (M&E) over public health clinic registries and crop yield telemetry.',
        'Privacy-enhancing computation (differential privacy and federated orchestration) across citizen datasets.',
        'Fiduciary anti-diversion protocols with satellite-verified physical milestone verification for donor tranches.',
        'Bilingual vernacular Chichewa/Swahili/Portuguese interfaces for rural frontline community workers.'
      ],
      compliance: 'Malawi DPA 2017/2024 / WHO Digital Health Standards / UNDP Guidelines'
    },
    {
      id: 'logistics',
      title: 'Critical Infrastructure & Cross-Border Logistics',
      scope: 'Nacala / Beira Corridors • Mwanza Border Post • ESCOM Power Grid • SADC FTA Customs',
      specs: [
        'Corridor freight dispatch and port container queue optimization across Mozambique, Malawi, and Zambia.',
        'Standardized cryptographic EDI document signing (PKI) for automated customs clearance under AfCFTA.',
        'Strict architectural air-gapping of operational technology (OT) control loops from cloud-facing planning agents.',
        'Programmatic cross-border liability arbitration for agent operations affecting multinational assets.'
      ],
      compliance: 'WCO SAFE Framework / SADC Protocol on Transport & Trade / AfCFTA Annex 4'
    }
  ];

  const roadmapPhases = [
    {
      phase: 'Phase 1 // Standardization',
      timeline: 'Months 01–06',
      title: 'Model Framework & Sandbox Network',
      deliverables: [
        'Draft SADC Model Agentic AI Framework & technical guidelines for digital/ICT ministries.',
        'Establish the SADC Multi-Agent Regulatory Sandbox network anchored across regional fintech & university labs.',
        'Publish SADC Machine-Identity Guidelines for verifying automated software requests.'
      ],
      status: 'Current Strategic Focus'
    },
    {
      phase: 'Phase 2 // National Enactment',
      timeline: 'Months 07–12',
      title: 'Regulatory Policy Alignment & Certification',
      deliverables: [
        'Align national telecom and data authorities (MACRA, CRASA, BOCRA) with graduated autonomy tiers.',
        'Launch SADC Executive & AI Developer Certification programs for enterprise and public service engineering.',
        'Establish national cryptographic agent identity issuance registries.'
      ],
      status: '2026-2027 Pipeline'
    },
    {
      phase: 'Phase 3 // Operational Harmonization',
      timeline: 'Months 13–24',
      title: 'Cross-Border Harmonization & SADC AI Summit',
      deliverables: [
        'Deploy cross-border agent identity interoperability across SADC central banks and revenue authorities.',
        'Convene the SADC Annual Agentic AI Governance Summit in Lilongwe for Member State delegations.',
        'Formalize multilateral liability arbitration mechanisms for autonomous cross-border transactions.'
      ],
      status: 'Institutional Scale'
    }
  ];

  const handleDownloadDossier = () => {
    setDownloadedState(true);
    setTimeout(() => setDownloadedState(false), 3500);
  };

  return (
    <section 
      id="sadc-governance-framework"
      aria-label="SADC Agentic AI Governance Framework"
      className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full relative z-10 border-t ${
        isLight ? 'border-slate-300 bg-slate-50/50' : 'border-white/10 bg-black/40'
      }`}
    >
      {/* Policy Briefing Metadata Strip */}
      <div className={`p-4 rounded-2xl border mb-10 flex flex-col lg:flex-row lg:items-center justify-between gap-4 ${
        isLight 
          ? 'bg-white border-slate-300 shadow-sm' 
          : 'bg-zinc-900/90 border-orange-500/30 shadow-xl'
      }`}>
        <div className="flex flex-wrap items-center gap-3">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-orange-500/10 border border-orange-500/30 text-orange-500 font-mono text-[10px] font-bold tracking-wider">
            <span className="w-1.5 h-1.5 rounded-full bg-orange-500 animate-pulse" />
            <span>PHAROS POLICY TRACK // EXECUTIVE SUBMISSION</span>
          </div>
          <span className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
            Author: <strong className={isLight ? 'text-slate-900' : 'text-white'}>Jack Mlusu</strong>, Founder & CEO, LightSpeed Holdings
          </span>
          <span className="text-zinc-500 hidden sm:inline">•</span>
          <span className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
            Target: SADC ICT Ministers, MACRA, CRASA, Central Banks & C-Suites
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleDownloadDossier}
            className={`px-3.5 py-1.5 rounded-xl border text-xs font-mono font-bold flex items-center gap-2 transition-all cursor-pointer ${
              downloadedState
                ? 'bg-emerald-500 text-white border-emerald-500'
                : isLight
                  ? 'bg-slate-100 hover:bg-slate-200 text-slate-900 border-slate-300'
                  : 'bg-zinc-800 hover:bg-zinc-700 text-white border-white/20'
            }`}
          >
            {downloadedState ? <Check className="w-3.5 h-3.5" /> : <Download className="w-3.5 h-3.5 text-orange-500" />}
            <span>{downloadedState ? 'Policy Dossier Retrieved' : 'Download Executive Submission'}</span>
          </button>

          <button
            onClick={() => onRequestBriefing?.('Policy Briefing: SADC Agentic AI Governance Framework Submission')}
            className="px-3.5 py-1.5 rounded-xl bg-orange-500 hover:bg-orange-600 text-white text-xs font-mono font-bold flex items-center gap-1.5 transition-all cursor-pointer shadow-sm shadow-orange-500/30"
          >
            <span>Request Policy Briefing</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Hero Section of Policy Framework */}
      <div className="max-w-4xl space-y-4 mb-12">
        <div className="flex items-center gap-2 font-mono text-[11px] tracking-widest text-orange-500 font-bold">
          <Scale className="w-4 h-4" />
          <span>SADC REGIONAL REGULATORY STANDARD // OPERATIONAL BLUEPRINT</span>
        </div>
        
        <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display leading-[1.08] ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}>
          SADC Agentic AI <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 via-amber-500 to-amber-300">
            Governance Framework
          </span>
        </h2>

        <p className={`text-justify text-base sm:text-lg leading-relaxed ${
          isLight ? 'text-slate-800 font-medium' : 'text-zinc-200'
        }`}>
          A unified, forward-looking operational and regulatory standard for deploying autonomous agentic AI across SADC Member States — purpose-built for low-bandwidth edge environments, dual mobile money economies, and sovereign on-soil data boundaries.
        </p>
      </div>

      {/* The SADC Context Callout: Why SADC Needs Its Own Frame */}
      <div className={`p-6 sm:p-8 rounded-3xl border mb-12 relative overflow-hidden ${
        isLight ? 'bg-white border-slate-300 shadow-md' : 'bg-zinc-950/90 border-white/15 shadow-2xl'
      }`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2 font-mono text-xs font-bold text-orange-500 uppercase tracking-wider">
            <Globe2 className="w-4 h-4" />
            <span>Why SADC Needs Its Own Governance Architecture</span>
          </div>
          <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
            isLight ? 'bg-slate-100 border-slate-300 text-slate-700' : 'bg-zinc-900 border-white/10 text-zinc-400'
          }`}>
            Anti-SaaS Dependency Directive
          </span>
        </div>

        <p className={`text-justify text-sm sm:text-base leading-relaxed mb-6 ${
          isLight ? 'text-slate-700' : 'text-zinc-300'
        }`}>
          Static, cloud-centric governance models built for Western or East Asian contexts fail against Southern African structural realities. SADC cannot afford to regulate reactively after failures; defining technical parameters today attracts sovereign investment, protects critical infrastructure, and fosters domestic enterprise.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <div className={`p-4 rounded-2xl border ${
            isLight ? 'bg-slate-50 border-slate-200' : 'bg-zinc-900/60 border-white/5'
          }`}>
            <div className="flex items-center gap-2 font-mono text-xs font-bold text-orange-500 mb-1.5">
              <Zap className="w-3.5 h-3.5" />
              <span>Low-Bandwidth Edge Runtimes</span>
            </div>
            <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Intermittent connectivity demands open-weight, locally hosted models capable of air-gapped inference to survive undersea-cable outages.
            </p>
          </div>

          <div className={`p-4 rounded-2xl border ${
            isLight ? 'bg-slate-50 border-slate-200' : 'bg-zinc-900/60 border-white/5'
          }`}>
            <div className="flex items-center gap-2 font-mono text-xs font-bold text-amber-500 mb-1.5">
              <Coins className="w-3.5 h-3.5" />
              <span>Dual Economy Interoperability</span>
            </div>
            <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Agents must natively bridge formal banking cores (RTGS / SWIFT) and mobile money rails (Airtel Money, TNM Mpamba, PayChangu).
            </p>
          </div>

          <div className={`p-4 rounded-2xl border ${
            isLight ? 'bg-slate-50 border-slate-200' : 'bg-zinc-900/60 border-white/5'
          }`}>
            <div className="flex items-center gap-2 font-mono text-xs font-bold text-emerald-500 mb-1.5">
              <Activity className="w-3.5 h-3.5" />
              <span>Cross-Border SADC & AfCFTA Trade</span>
            </div>
            <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Automated customs, shipping manifests, and currency settlements cross borders in real time, requiring harmonized regional liability standards.
            </p>
          </div>
        </div>
      </div>

      {/* Navigation Sub-Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-2 mb-8">
        {[
          { id: 'principles', label: '1. Core Principles (4 Pillars)', icon: ShieldCheck },
          { id: 'hitl-matrix', label: '2. Graduated Autonomy Matrix (HITL)', icon: Layers },
          { id: 'standards', label: '3. Technical & Operational Standards', icon: Lock },
          { id: 'blueprints', label: '4. Sectoral Blueprints', icon: Building2 },
          { id: 'roadmap', label: '5. SADC Enactment Roadmap', icon: Clock },
          { id: 'dossier', label: '6. Full Executive Dossier', icon: BookOpen }
        ].map(tab => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`shrink-0 px-4 py-2.5 rounded-2xl text-xs font-mono font-bold flex items-center gap-2 border transition-all cursor-pointer ${
                isActive
                  ? 'bg-orange-500 text-white border-orange-500 shadow-md shadow-orange-500/20'
                  : isLight
                    ? 'bg-white text-slate-700 hover:text-slate-900 border-slate-300'
                    : 'bg-zinc-900/80 text-zinc-300 hover:text-white border-white/10'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* TAB 1: CORE PRINCIPLES (4 PILLARS) */}
      {activeTab === 'principles' && (
        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            
            {/* Principle 1: Agency Control */}
            <div className={`p-6 rounded-3xl border flex flex-col justify-between ${
              isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-zinc-900/80 border-white/10 shadow-xl'
            }`}>
              <div className="space-y-3">
                <div className="w-10 h-10 rounded-2xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-500">
                  <Workflow className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-orange-500 font-bold block">
                  PRINCIPLE 01
                </span>
                <h3 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                  Agency Control & Graduated Autonomy
                </h3>
                <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Autonomous systems must be bounded by mathematical risk tiers. Non-critical tasks execute autonomously, while high-risk financial and statutory actions enforce mandatory Human-in-the-Loop (HITL) authorization gates.
                </p>
              </div>
              <div className="pt-4 mt-4 border-t border-black/10 dark:border-white/10">
                <button
                  onClick={() => setActiveTab('hitl-matrix')}
                  className="text-[11px] font-mono font-bold text-orange-500 hover:text-orange-400 flex items-center gap-1 cursor-pointer"
                >
                  <span>Inspect 4-Tier Matrix</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            </div>

            {/* Principle 2: Cryptographic Identity */}
            <div className={`p-6 rounded-3xl border flex flex-col justify-between ${
              isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-zinc-900/80 border-white/10 shadow-xl'
            }`}>
              <div className="space-y-3">
                <div className="w-10 h-10 rounded-2xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-400">
                  <Key className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-blue-400 font-bold block">
                  PRINCIPLE 02
                </span>
                <h3 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                  Cryptographic Identity & Immutable Audit
                </h3>
                <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Every agent carries a machine-readable credential bound to a registered legal entity and deployment hash. High/Critical tiers mandate append-only SHA-256 action ledgers for tamper-evident regulatory audits.
                </p>
              </div>
              <div className="pt-4 mt-4 border-t border-black/10 dark:border-white/10">
                <span className="text-[10px] font-mono text-zinc-500">
                  PKI Header Authentication
                </span>
              </div>
            </div>

            {/* Principle 3: Data Sovereignty */}
            <div className={`p-6 rounded-3xl border flex flex-col justify-between ${
              isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-zinc-900/80 border-white/10 shadow-xl'
            }`}>
              <div className="space-y-3">
                <div className="w-10 h-10 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-emerald-400 font-bold block">
                  PRINCIPLE 03
                </span>
                <h3 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                  Data Sovereignty & Edge Compute
                </h3>
                <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Sovereign in-country compute for state, health, and primary financial records. Encourages open-weight local inference ensuring continuity even during sub-sea cable disruptions.
                </p>
              </div>
              <div className="pt-4 mt-4 border-t border-black/10 dark:border-white/10">
                <span className="text-[10px] font-mono text-zinc-500">
                  Malawi DPA 2017/2024 Bound
                </span>
              </div>
            </div>

            {/* Principle 4: Liability & Accountability */}
            <div className={`p-6 rounded-3xl border flex flex-col justify-between ${
              isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-zinc-900/80 border-white/10 shadow-xl'
            }`}>
              <div className="space-y-3">
                <div className="w-10 h-10 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
                  <Scale className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-amber-400 font-bold block">
                  PRINCIPLE 04
                </span>
                <h3 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                  Liability & Agency-as-Instrument
                </h3>
                <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Agents possess zero legal personality; full vicarious corporate liability rests on the deploying entity. Mandates programmatic kill switches, rate limiters, and cross-border PKI arbitration.
                </p>
              </div>
              <div className="pt-4 mt-4 border-t border-black/10 dark:border-white/10">
                <span className="text-[10px] font-mono text-zinc-500">
                  Vicarious Corporate Liability
                </span>
              </div>
            </div>

          </div>

          {/* Core Principles Architecture Diagram */}
          <div className={`p-6 rounded-3xl border ${
            isLight ? 'bg-white border-slate-300' : 'bg-zinc-900/50 border-white/10'
          }`}>
            <div className="font-mono text-xs font-bold text-orange-500 mb-4 uppercase tracking-widest flex items-center gap-2">
              <Network className="w-4 h-4" />
              <span>SADC Agentic AI Principles Topology</span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-center">
              <div className={`p-4 rounded-2xl border ${isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/40 border-white/10'}`}>
                <div className="font-mono text-xs font-bold text-orange-500">Agency Control</div>
                <div className={`text-[11px] mt-1 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Graduated 4-Tier HITL</div>
              </div>
              <div className={`p-4 rounded-2xl border ${isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/40 border-white/10'}`}>
                <div className="font-mono text-xs font-bold text-blue-400">Sovereignty</div>
                <div className={`text-[11px] mt-1 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>On-Soil Edge Runtimes</div>
              </div>
              <div className={`p-4 rounded-2xl border ${isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/40 border-white/10'}`}>
                <div className="font-mono text-xs font-bold text-emerald-400">Financial Safety</div>
                <div className={`text-[11px] mt-1 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>RTGS / Mobile Money Caps</div>
              </div>
              <div className={`p-4 rounded-2xl border ${isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/40 border-white/10'}`}>
                <div className="font-mono text-xs font-bold text-amber-400">Traceability</div>
                <div className={`text-[11px] mt-1 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>Cryptographic Audit Rails</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: GRADUATED AUTONOMY & HITL MATRIX */}
      {activeTab === 'hitl-matrix' && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                Graduated Autonomy & Human-in-the-Loop (HITL) Matrix
              </h3>
              <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                A deterministic 4-tier risk classification binding agent capability to statutory human verification.
              </p>
            </div>
            <span className="text-[10px] font-mono px-2.5 py-1 rounded-full bg-orange-500/10 border border-orange-500/30 text-orange-500 font-bold self-start sm:self-auto">
              Mandatory Regulatory Standard
            </span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
            {hitlTiers.map(t => {
              const isSelected = activeTier === t.tier;
              return (
                <div
                  key={t.tier}
                  onClick={() => setActiveTier(t.tier)}
                  className={`p-5 rounded-3xl border transition-all cursor-pointer relative overflow-hidden flex flex-col justify-between ${
                    isSelected
                      ? isLight
                        ? 'bg-white border-orange-500 shadow-lg ring-1 ring-orange-500/50'
                        : 'bg-zinc-900 border-orange-500 shadow-2xl ring-1 ring-orange-500/50'
                      : isLight
                        ? 'bg-slate-50 hover:bg-white border-slate-300'
                        : 'bg-zinc-950/70 hover:bg-zinc-900/90 border-white/10'
                  }`}
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-xs font-bold text-orange-500">
                        TIER 0{t.tier}
                      </span>
                      <span className={`text-[9px] font-mono px-2 py-0.5 rounded-full border font-bold uppercase ${t.badgeColor}`}>
                        {t.status}
                      </span>
                    </div>

                    <h4 className={`text-base font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {t.risk}
                    </h4>

                    <div className={`p-2.5 rounded-xl text-xs font-medium leading-snug ${
                      isLight ? 'bg-slate-100 text-slate-800' : 'bg-white/5 text-zinc-300'
                    }`}>
                      <strong className="block text-[10px] uppercase font-mono text-zinc-500 mb-1">Examples:</strong>
                      {t.example}
                    </div>

                    <div className="text-xs leading-relaxed">
                      <strong className="block text-[10px] uppercase font-mono text-orange-500 mb-1">Statutory Control:</strong>
                      <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>{t.control}</span>
                    </div>
                  </div>

                  <div className="pt-3 mt-3 border-t border-black/10 dark:border-white/10 text-[10px] font-mono text-zinc-500">
                    Technical Spec: {t.technicalRequirement}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Deep-Dive Inspection for Selected Tier */}
          {(() => {
            const current = hitlTiers.find(t => t.tier === activeTier) || hitlTiers[2];
            return (
              <div className={`p-6 rounded-3xl border ${
                isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-zinc-900/90 border-orange-500/30 shadow-xl'
              }`}>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-orange-500 animate-pulse" />
                    <span className="font-mono text-xs font-bold text-orange-500 uppercase">
                      Tier 0{current.tier} Deep-Dive Operational Specification
                    </span>
                  </div>
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${current.badgeColor}`}>
                    {current.risk}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                  <div>
                    <strong className="block text-[10px] font-mono text-zinc-500 uppercase mb-1">Deployment Scope:</strong>
                    <p className={isLight ? 'text-slate-700' : 'text-zinc-300'}>{current.example}</p>
                  </div>
                  <div>
                    <strong className="block text-[10px] font-mono text-zinc-500 uppercase mb-1">Enforced Policy Gate:</strong>
                    <p className={isLight ? 'text-slate-700' : 'text-zinc-300'}>{current.control}</p>
                  </div>
                  <div>
                    <strong className="block text-[10px] font-mono text-zinc-500 uppercase mb-1">Audit & Cryptography:</strong>
                    <p className={isLight ? 'text-slate-700' : 'text-zinc-300'}>{current.technicalRequirement}</p>
                  </div>
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* TAB 3: TECHNICAL & OPERATIONAL STANDARDS */}
      {activeTab === 'standards' && (
        <div className="space-y-6">
          <div>
            <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
              Technical & Operational Verification Standards
            </h3>
            <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Formal verification protocols required for enterprise multi-agent deployments across SADC.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {standardsData.map((std, idx) => {
              const Icon = std.icon;
              return (
                <div
                  key={idx}
                  className={`p-6 rounded-3xl border flex flex-col justify-between ${
                    isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-zinc-900/80 border-white/10 shadow-xl'
                  }`}
                >
                  <div className="space-y-3">
                    <div className="flex items-center gap-2.5">
                      <div className="w-8 h-8 rounded-xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-500">
                        <Icon className="w-4 h-4" />
                      </div>
                      <h4 className={`text-base font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                        {std.domain}
                      </h4>
                    </div>

                    <div className={`p-3 rounded-2xl border text-xs leading-relaxed ${
                      isLight ? 'bg-slate-50 border-slate-200 text-slate-800' : 'bg-black/40 border-white/5 text-zinc-200'
                    }`}>
                      <strong className="block text-[10px] font-mono text-orange-500 uppercase mb-1">Standard Specification:</strong>
                      {std.standard}
                    </div>

                    <div className={`p-3 rounded-2xl border text-xs leading-relaxed ${
                      isLight ? 'bg-emerald-50/50 border-emerald-200 text-emerald-900' : 'bg-emerald-950/20 border-emerald-500/20 text-emerald-300'
                    }`}>
                      <strong className="block text-[10px] font-mono text-emerald-500 uppercase mb-1">Regulatory Verification Protocol:</strong>
                      {std.verification}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Cross-Border Execution Liability Box */}
          <div className={`p-6 rounded-3xl border ${
            isLight ? 'bg-amber-50/60 border-amber-300 text-amber-950' : 'bg-amber-950/20 border-amber-500/30 text-amber-200'
          }`}>
            <div className="flex items-center gap-2 font-mono text-xs font-bold text-amber-500 mb-2 uppercase tracking-wider">
              <Scale className="w-4 h-4" />
              <span>Cross-Border Execution Liability Protocol (SADC FTA & AfCFTA)</span>
            </div>
            <p className="text-xs leading-relaxed">
              Harmonizes liability when an agent hosted in Country A executes an automated action impacting financial or physical assets in Country B. Requires standardized cryptographic PKI signing of all agent external communications, automated customs documentation reconciliation, and mutual recognition of digital agent identities across SADC central banks.
            </p>
          </div>
        </div>
      )}

      {/* TAB 4: SECTORAL BLUEPRINTS */}
      {activeTab === 'blueprints' && (
        <div className="space-y-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                Sectoral Governance Blueprints
              </h3>
              <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                Tailored regulatory architectures for high-impact Southern African industries.
              </p>
            </div>

            {/* Sector Selector */}
            <div className={`flex items-center p-1 rounded-2xl border ${
              isLight ? 'bg-white border-slate-300' : 'bg-zinc-900 border-white/10'
            }`}>
              {[
                { key: 'finance', label: 'Financial & Mobile Money' },
                { key: 'public-sector', label: 'Public Sector & Health' },
                { key: 'logistics', label: 'Critical Logistics & Power' }
              ].map(sec => (
                <button
                  key={sec.key}
                  onClick={() => setActiveSector(sec.key as any)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                    activeSector === sec.key
                      ? 'bg-orange-500 text-white shadow-xs'
                      : isLight
                        ? 'text-slate-600 hover:text-slate-900'
                        : 'text-zinc-400 hover:text-white'
                  }`}
                >
                  {sec.label}
                </button>
              ))}
            </div>
          </div>

          {(() => {
            const blueprint = sectoralBlueprints.find(b => b.id === activeSector) || sectoralBlueprints[0];
            return (
              <div className={`p-6 sm:p-8 rounded-3xl border space-y-6 ${
                isLight ? 'bg-white border-slate-300 shadow-md' : 'bg-zinc-900/90 border-white/10 shadow-2xl'
              }`}>
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-black/10 dark:border-white/10">
                  <div>
                    <span className="text-[10px] font-mono text-orange-500 font-bold uppercase tracking-wider block mb-1">
                      SECTORAL REGULATORY SPECIFICATION
                    </span>
                    <h4 className={`text-xl sm:text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {blueprint.title}
                    </h4>
                  </div>
                  <span className={`text-[10px] font-mono px-3 py-1 rounded-full border font-bold self-start sm:self-auto ${
                    isLight ? 'bg-slate-100 border-slate-300 text-slate-700' : 'bg-zinc-800 border-white/10 text-zinc-300'
                  }`}>
                    {blueprint.compliance}
                  </span>
                </div>

                <div>
                  <strong className="block text-[11px] font-mono text-zinc-500 uppercase mb-1">Applicable Infrastructure Scope:</strong>
                  <p className={`text-xs font-mono font-semibold ${isLight ? 'text-slate-800' : 'text-zinc-200'}`}>
                    {blueprint.scope}
                  </p>
                </div>

                <div className="space-y-3">
                  <strong className="block text-[11px] font-mono text-orange-500 uppercase">
                    Mandated Governance Requirements:
                  </strong>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {blueprint.specs.map((spec, sIdx) => (
                      <div 
                        key={sIdx}
                        className={`p-3.5 rounded-2xl border flex items-start gap-2.5 ${
                          isLight ? 'bg-slate-50 border-slate-200 text-slate-800' : 'bg-black/40 border-white/5 text-zinc-300'
                        }`}
                      >
                        <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                        <span className="text-xs leading-relaxed">{spec}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="pt-4 border-t border-black/10 dark:border-white/10 flex flex-wrap items-center justify-between gap-3">
                  <span className="text-xs font-mono text-zinc-500">
                    Complies with SADC Model Laws & Basel IV Guidelines
                  </span>

                  <button
                    onClick={() => onRequestBriefing?.(`Inquiry on ${blueprint.title} Governance Blueprint Implementation`)}
                    className="px-4 py-2 rounded-xl bg-orange-500 hover:bg-orange-600 text-white text-xs font-mono font-bold flex items-center gap-1.5 transition-all cursor-pointer"
                  >
                    <span>Engage Sectoral Sandbox</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* TAB 5: ROADMAP */}
      {activeTab === 'roadmap' && (
        <div className="space-y-6">
          <div>
            <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
              SADC Regional Enactment Roadmap (24-Month Phased Horizon)
            </h3>
            <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              A phased operational path from technical model guidelines to full regional cross-border harmonization.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {roadmapPhases.map((phase, pIdx) => (
              <div
                key={pIdx}
                className={`p-6 rounded-3xl border flex flex-col justify-between ${
                  pIdx === 0
                    ? isLight 
                      ? 'bg-white border-orange-500 shadow-md ring-1 ring-orange-500/30' 
                      : 'bg-zinc-900 border-orange-500 shadow-xl ring-1 ring-orange-500/30'
                    : isLight
                      ? 'bg-white border-slate-300'
                      : 'bg-zinc-900/60 border-white/10'
                }`}
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono text-orange-500 font-bold uppercase tracking-wider">
                      {phase.phase}
                    </span>
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
                      pIdx === 0 
                        ? 'bg-orange-500/10 border-orange-500/30 text-orange-500 font-bold' 
                        : 'bg-black/10 dark:bg-white/5 border-transparent text-zinc-500'
                    }`}>
                      {phase.timeline}
                    </span>
                  </div>

                  <h4 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                    {phase.title}
                  </h4>

                  <ul className="space-y-2.5">
                    {phase.deliverables.map((item, dIdx) => (
                      <li key={dIdx} className="flex items-start gap-2 text-xs leading-relaxed">
                        <span className="w-1.5 h-1.5 rounded-full bg-orange-500 mt-1.5 shrink-0" />
                        <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="pt-4 mt-4 border-t border-black/10 dark:border-white/10">
                  <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider block">
                    Milestone Status: <strong className="text-orange-500">{phase.status}</strong>
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* Immediate Recommendations Box */}
          <div className={`p-6 rounded-3xl border ${
            isLight ? 'bg-slate-100 border-slate-300' : 'bg-black/60 border-white/10'
          }`}>
            <h4 className={`text-sm font-bold font-mono text-orange-500 uppercase mb-3 flex items-center gap-2`}>
              <Sparkles className="w-4 h-4" />
              <span>Three Immediate Recommendations for SADC ICT Ministers & Regulators</span>
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div className="space-y-1">
                <strong className={`block ${isLight ? 'text-slate-900' : 'text-white'}`}>1. Establish a SADC Multi-Agent Sandbox</strong>
                <p className={isLight ? 'text-slate-600' : 'text-zinc-400'}>
                  Provide safe operational zones where commercial banks, telcos, and AI builders test agentic workflows under direct regulatory observation.
                </p>
              </div>
              <div className="space-y-1">
                <strong className={`block ${isLight ? 'text-slate-900' : 'text-white'}`}>2. Draft SADC Machine-Identity Guidelines</strong>
                <p className={isLight ? 'text-slate-600' : 'text-zinc-400'}>
                  Standardize how automated software requests identify themselves cryptographically across national API gateways.
                </p>
              </div>
              <div className="space-y-1">
                <strong className={`block ${isLight ? 'text-slate-900' : 'text-white'}`}>3. Fund Localized Capability Infrastructure</strong>
                <p className={isLight ? 'text-slate-600' : 'text-zinc-400'}>
                  Invest in domestic multi-agent orchestration, security auditing pipelines, and vernacular alignment across Chichewa, Swahili, and Portuguese.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 6: FULL EXECUTIVE DOSSIER READOUT */}
      {activeTab === 'dossier' && (
        <div className={`p-8 rounded-3xl border space-y-6 ${
          isLight ? 'bg-white border-slate-300 shadow-md' : 'bg-zinc-950 border-white/15 shadow-2xl'
        }`}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-black/10 dark:border-white/10">
            <div>
              <span className="text-xs font-mono text-orange-500 font-bold uppercase tracking-wider block mb-1">
                POLICY BRIEFING & EXECUTIVE SUBMISSION // COMPLETE TEXT
              </span>
              <h3 className={`text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                SADC Agentic AI Governance Framework
              </h3>
              <p className={`text-xs mt-1 font-mono ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                Author: Jack Mlusu, Founder & CEO, LightSpeed Holdings (Pharos policy track)
              </p>
            </div>

            <button
              onClick={handleDownloadDossier}
              className="px-4 py-2 rounded-xl bg-orange-500 hover:bg-orange-600 text-white text-xs font-mono font-bold flex items-center gap-2 transition-all cursor-pointer self-start sm:self-auto"
            >
              <Download className="w-4 h-4" />
              <span>Export Dossier (Markdown / PDF)</span>
            </button>
          </div>

          <div className={`prose max-w-none text-xs leading-relaxed space-y-4 font-mono ${
            isLight ? 'text-slate-800' : 'text-zinc-300'
          }`}>
            <p>
              <strong>Objective:</strong> A unified, forward-looking operational and regulatory standard for deploying autonomous agentic AI across SADC Member States.
            </p>

            <p>
              <strong>Target Audience:</strong> SADC Member State digital/ICT ministers, telecom & data regulators (e.g. MACRA, CRASA), central banks, enterprise C-suites, and regional development banks.
            </p>

            <div className="p-4 rounded-xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10">
              <p className="font-bold text-orange-500 mb-2">EXECUTIVE SUMMARY</p>
              <p>
                Static, cloud-centric governance built for Western or East Asian contexts fails against SADC's constraints: low-bandwidth edge environments, dual mobile-money economies, and fast-moving cross-border trade under AfCFTA. SADC cannot regulate reactively after failures. Clear technical parameters now attract investment, ensure data sovereignty, and foster domestic enterprise.
              </p>
            </div>

            <p className="font-bold text-orange-500 pt-2">CORE PRINCIPLES:</p>
            <ul className="list-disc pl-5 space-y-1.5">
              <li><strong>Graduated Autonomy & Human-in-the-Loop (HITL):</strong> 4-tier risk classification from Low (Advisory) to Critical (Infrastructure). Mandatory HITL gates on Tier 3 High-Risk actions.</li>
              <li><strong>Cryptographic Identity & Immutable Audit Trails:</strong> Machine-readable agent credentials bound to a registered legal entity; tamper-evident append-only action logs.</li>
              <li><strong>Data Sovereignty & Edge-Compute Standards:</strong> Sovereign in-country processing for state and financial data; open-weight air-gapped inference to survive sub-sea cable disruptions.</li>
              <li><strong>Liability & Accountability:</strong> Agency-as-Instrument doctrine. Vicarious corporate liability for delegated credentials; programmatic kill switches and cross-border PKI arbitration.</li>
            </ul>

            <p className="font-bold text-orange-500 pt-2">CONCLUSION:</p>
            <p>
              By enacting clear, practical governance standards tailored to regional realities, SADC can protect critical systems while positioning Southern Africa as a global leader in sovereign, autonomous enterprise architecture.
            </p>
          </div>

          <div className="pt-4 border-t border-black/10 dark:border-white/10 flex flex-wrap items-center justify-between gap-4">
            <span className="text-xs font-mono text-zinc-500">
              Official Submission Dossier • Pharos Policy Track • LightSpeed Holdings
            </span>

            <button
              onClick={() => onRequestBriefing?.('Ministerial Briefing Request: SADC Agentic AI Governance Framework')}
              className="px-5 py-2.5 rounded-full bg-gradient-to-r from-orange-500 to-amber-500 text-white text-xs font-mono font-bold flex items-center gap-2 cursor-pointer shadow-md hover:from-orange-600 hover:to-amber-600"
            >
              <span>Schedule Ministerial Briefing</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

    </section>
  );
};
