import React, { useState } from 'react';
import { 
  ArrowRight, 
  CheckCircle2, 
  Cpu, 
  Layers, 
  ShieldCheck, 
  Workflow, 
  Zap, 
  TrendingUp, 
  Building2, 
  Landmark, 
  Globe2, 
  Sparkles, 
  ChevronRight,
  FileText,
  Clock,
  Send,
  ExternalLink,
  Coins,
  Shield,
  FileCheck,
  Compass,
  Brain,
  Download,
  Check,
  Network,
  GitMerge,
  Lock,
  RefreshCw,
  Activity,
  ArrowDownRight,
  ArrowUpRight,
  Database
} from 'lucide-react';
import { Agent } from '../types';
import { InteractiveOperatingModel } from './InteractiveOperatingModel';
import { TransformationDiagnostic } from './TransformationDiagnostic';
import { TemplatesArtifacts } from './TemplatesArtifacts';
import { TactileRockerSwitch, TactileRotaryKnob, AcousticVentGrille } from './TactileHardwareElements';

interface CorporateLandingProps {
  onRequestBriefing: (summary?: string) => void;
  onSelectAgentForModal: (agent: Agent) => void;
  agentsList: Agent[];
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

export const CorporateLanding: React.FC<CorporateLandingProps> = ({
  onRequestBriefing,
  onSelectAgentForModal,
  agentsList,
  theme = 'dark',
  onToggleTheme
}) => {
  const isLight = theme === 'light';
  const [activePillar, setActivePillar] = useState<number>(0);
  const [selectedSynergy, setSelectedSynergy] = useState<string>('strategy-intelligence');
  const [selectedIndustry, setSelectedIndustry] = useState<string>('finance');
  const [contactSubmitted, setContactSubmitted] = useState<boolean>(false);
  const [contactFormData, setContactFormData] = useState({
    name: '',
    title: '',
    organization: '',
    email: '',
    scope: 'Advisory Architecture Sprint (2 Weeks)',
    objective: '',
    timeline: 'Within 30 days'
  });

  const handleContactSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setContactSubmitted(true);
  };

  // The 4 Connected Core Offerings
  const coreCapabilities = [
    {
      id: 'strategy',
      title: 'Strategy Formulation & Operating Models',
      shortTitle: 'Strategy Formulation',
      eyebrow: 'CORE OFFERING 01 // ENTERPRISE TOPOLOGY',
      tagline: 'Computable Policy-as-Code & Capital Allocation Models',
      desc: 'We partner with Chairpersons, CEOs, and Executive Committees across SADC to redesign organizational topologies from first principles. We replace static 6-month consulting decks with executable business policies, sovereign data boundaries, and deterministic human-in-the-loop governance.',
      metrics: '40–60% Compression of Administrative Latency',
      inputContract: 'Board Mandates, Statutory Frameworks, Capital Budgets & Operating Topology',
      outputContract: 'Computable Policy-as-Code, Token Budgets, Fiduciary Approval Gate Schemas',
      upstreamSource: 'Real-time settlement telemetry and model drift feedback from Offering 04 (Execution)',
      downstreamTarget: 'Feeds policy constraints and data access rules directly to Offering 02 (Intelligence) & 03 (Autonomous Systems)',
      governance: 'Basel IV / King IV / SADC Regulatory Compliant',
      deliverables: [
        'Organizational Cognitive Topology & Latency Audit',
        'Fiduciary Gatekeeper Specification & Risk Matrix',
        'AI Capital Allocation & Deterministic ROI Roadmap',
        'Sovereign Data Residency & Compliance Blueprint'
      ]
    },
    {
      id: 'intelligence',
      title: 'Private Intelligence & Sovereign Knowledge Graphs',
      shortTitle: 'Private Intelligence',
      eyebrow: 'CORE OFFERING 02 // KNOWLEDGE FABRICS',
      tagline: 'Sovereign Knowledge Synthesis & Semantic Enclaves',
      desc: 'Transforming siloed enterprise data, regulatory filings, cross-border SADC shipping manifests, and legacy ERP databases into private, real-time semantic knowledge graphs with continuous verification and zero public SaaS cloud leakage.',
      metrics: '< 200ms Ingestion & Lineage Verification',
      inputContract: 'Unstructured Manifests, ERP Databases, Core Mainframes & Regulatory Filings',
      outputContract: 'Private Enterprise Vector Fabric, Semantic Entity Graphs & Cryptographic AST Lineage',
      upstreamSource: 'Governed by data boundary policies defined in Offering 01 (Strategy)',
      downstreamTarget: 'Supplies verified, air-gapped contextual embeddings to Offering 03 (Autonomous Systems)',
      governance: '100% Data Sovereignty / Air-Gapped On-Premise',
      deliverables: [
        'Private Vector & Semantic Data Fabrics',
        'Multimodal Document Ingestion & Classification Engines',
        'Cryptographic AST Provenance & Lineage Verification',
        'Air-Gapped Sovereign Model Enclaves & Local Inference'
      ]
    },
    {
      id: 'systems',
      title: 'Autonomous Systems & Multi-Agent Fleets',
      shortTitle: 'Autonomous Systems',
      eyebrow: 'CORE OFFERING 03 // AUTONOMOUS ARCHITECTURE',
      tagline: 'Deterministic Multi-Agent Fleet Engineering',
      desc: 'Building structured hierarchies of specialized AI agents constrained to canonical tool wrappers, task budgets, and cryptographic audit rails. No black-box hallucinations—every action is bounded, validated, and executable via Directed Acyclic Graphs (DAGs).',
      metrics: '144 Verified Agent Personas & Production DAGs',
      inputContract: 'Policy bounds from Offering 01 and contextual knowledge from Offering 02',
      outputContract: 'Structured Transaction Payloads, Reconciled Ledgers & Exception Alerts',
      upstreamSource: 'Driven by Strategy policies (01) and grounded in Sovereign Intelligence graphs (02)',
      downstreamTarget: 'Dispatches validated payloads to Offering 04 (Fiduciary Execution & Core Settlement)',
      governance: 'OpenCode Canonical 7-Tool Permission Gates',
      deliverables: [
        'OpenCode Multi-Agent Hierarchies & Task DAGs',
        'Deterministic Tool Budgets & Rate Limiters',
        'Consensus Arbiters & Safety Guardrails',
        'Continuous Model Drift & Evaluation Telemetry'
      ]
    },
    {
      id: 'execution',
      title: 'Fiduciary Assurance, Governance & Core Execution',
      shortTitle: 'Fiduciary & Execution',
      eyebrow: 'CORE OFFERING 04 // PRODUCTION INTEGRATION',
      tagline: 'Legacy Core Modernization & High-Throughput Settlement',
      desc: 'Bridging monolithic banking cores, government customs clearing systems, and enterprise supply chain software into reactive API event streams with Human-in-the-Loop (HITL) approval gates and immutable cryptographic audit logging.',
      metrics: 'Sub-second API Execution & Real-time Settlement',
      inputContract: 'Validated agent payloads from Offering 03 and Human Executive Approval tokens',
      outputContract: 'Live Core Settlement, Customs EDI Filings, Immutable SHA-256 Audit Trails',
      upstreamSource: 'Receives transaction payloads from Offering 03; enforces HITL approvals',
      downstreamTarget: 'Streams performance KPIs, recovered duties, and drift telemetry back to Offering 01 (Strategy)',
      governance: 'Immutable SHA-256 / WCO SAFE / SADC EDI Standard',
      deliverables: [
        'Legacy Core API Modernization Wrappers',
        'SADC Regional Payment & Customs EDI Connectors',
        'Automated Fiduciary Settlement & HITL Approval Gates',
        'Zero-Trust Immutable Audit Logging & Telemetry Rails'
      ]
    }
  ];

  // Interconnected Synergy Matrix Pairs
  const synergyPairs: Record<string, {
    title: string;
    from: string;
    to: string;
    headline: string;
    mechanism: string;
    compoundImpact: string;
  }> = {
    'strategy-intelligence': {
      title: 'Strategy ↔ Intelligence',
      from: '01. Strategy',
      to: '02. Private Intelligence',
      headline: 'Policy-Governed Knowledge Synthesis',
      mechanism: 'Statutory compliance policies and corporate mandates are encoded as machine-readable schema filters, ensuring the semantic knowledge graph strictly enclaves confidential data and enforces SADC regulatory jurisdiction rules before indexing.',
      compoundImpact: '100% elimination of unauthorized data leakage across cross-border business units.'
    },
    'intelligence-systems': {
      title: 'Intelligence ↔ Autonomous Systems',
      from: '02. Private Intelligence',
      to: '03. Autonomous Systems',
      headline: 'Deterministic RAG Grounding',
      mechanism: 'Air-gapped knowledge graphs supply real-time entity linking and verified document citations to agent fleets, preventing LLM hallucinations and grounding every operational recommendation in immutable source records.',
      compoundImpact: 'Zero hallucination risk with sub-200ms factual retrieval across millions of legacy records.'
    },
    'systems-execution': {
      title: 'Autonomous Systems ↔ Execution',
      from: '03. Autonomous Systems',
      to: '04. Fiduciary & Execution',
      headline: 'Verified Autonomous Settlement',
      mechanism: 'Specialist agent hierarchies decompose complex transactions into atomic API payloads and route high-value operations through cryptographic Human-in-the-Loop (HITL) approval gates before writing to core banking or customs EDI mainframes.',
      compoundImpact: 'Reconciliation times compressed from 72 hours to 14 minutes with zero unverified writes.'
    },
    'execution-strategy': {
      title: 'Execution ↔ Strategy (Feedback Loop)',
      from: '04. Fiduciary & Execution',
      to: '01. Strategy',
      headline: 'Closed-Loop Telemetry & Adaptive Policy',
      mechanism: 'Live transaction latency, recovered revenue yield, exception rates, and agent drift telemetry are piped directly into executive dashboards, allowing board committees to adjust business policies and capital allocation dynamically.',
      compoundImpact: 'Quarterly strategy cycles converted into real-time computable operational optimization.'
    }
  };

  const industriesData: Record<string, {
    title: string;
    subtitle: string;
    description: string;
    citation: string;
    impact: string[];
  }> = {
    finance: {
      title: 'Commercial Banking & Financial Services',
      subtitle: 'Autonomous trade finance, liquidity reconciliation, and cross-border settlement.',
      description: 'Tier-1 commercial lenders and central banks leverage LightSpeed architectures to automate real-time letter of credit verification, cross-border treasury balancing across SADC corridors, and continuous AML anomaly detection.',
      citation: 'SADC Regional Banking Architecture Standard',
      impact: [
        'Letter of credit reconciliation compressed from 72 hours to 14 minutes.',
        'Real-time AML/Sanction anomaly detection with 100% audit precision.',
        'Automated multi-currency treasury balancing across Southern African corridors.'
      ]
    },
    government: {
      title: 'Revenue Authorities & Customs Services',
      subtitle: 'Sovereign border intelligence, manifest classification, and tariff enforcement.',
      description: 'National ministries and customs authorities deploy our private edge intelligence to audit cross-border cargo manifests, detect fraudulent tariff classifications, and eliminate physical inspection bottlenecks.',
      citation: 'National Sovereign Customs Framework',
      impact: [
        '$14.2M in previously undetected import duties recovered in 90 days.',
        'Cargo clearance throughput increased by 400% across key border posts.',
        'Sovereign data residency guaranteed through on-premise local inference clusters.'
      ]
    },
    logistics: {
      title: 'Supply Chain, Mining & Commodity Logistics',
      subtitle: 'Predictive corridor dispatch, demurrage mitigation, and port coordination.',
      description: 'Commodity extractors, port operators, and freight logistics networks deploy LightSpeed multi-agent pipelines to coordinate 400+ unit transport fleets, anticipate border delays, and minimize demurrage costs.',
      citation: 'Pan-African Mineral Logistics Corridor',
      impact: [
        'Demurrage wait times along Dar es Salaam and Beira corridors reduced by 64%.',
        '4.8M liters of transport fuel saved through predictive routing.',
        'Automated bills-of-lading ingestion and instant customs pre-clearance.'
      ]
    },
    multilateral: {
      title: 'Development Finance & Multilaterals',
      subtitle: 'Program monitoring, grant evaluation, and fiduciary disbursement integrity.',
      description: 'International development banks, sovereign trust funds, and bilateral agencies utilize our cognitive verification pipelines to audit field milestones and enforce anti-diversion covenants on capital deployments.',
      citation: 'Multilateral Fiduciary Oversight Protocol',
      impact: [
        'Continuous remote satellite and telemetry verification of infrastructure milestones.',
        'Fiduciary grant disbursement checks reducing fund diversion risk to near-zero.',
        'Automated donor-grade impact reports generated dynamically from ground data.'
      ]
    }
  };

  const caseStudies = [
    {
      sector: 'COMMERCIAL BANKING',
      client: 'Regional Tier-1 Bank (Southern & Eastern Africa)',
      problem: 'Manual trade finance reconciliation took 72 hours per letter of credit, creating massive merchant bottlenecks and foreign currency exposure.',
      intervention: 'Engineered a 4-agent sovereign pipeline (Ingest, Verification, Sanction Sweep, Swift Dispatch) with verified Human-in-the-Loop approval gates.',
      outcome: 'Reduced letter of credit issuance time from 72 hours to 14 minutes with 100% compliance audit match.'
    },
    {
      sector: 'NATIONAL REVENUE AUTHORITY',
      client: 'Sovereign Taxation & Customs Service',
      problem: 'Cross-border cargo manifest discrepancies resulted in millions in uncollected tariffs and multi-day border queues.',
      intervention: 'Deployed a multimodal computer vision and manifest cross-examination system running local edge models at border control points.',
      outcome: 'Recovered $14.2M in previously missed duty within 90 days; border clearance throughput increased by 400%.'
    },
    {
      sector: 'COMMODITY LOGISTICS',
      client: 'Export Mineral Logistics Fleet (Central & Southern Africa)',
      problem: 'Fragmented warehouse receipts, volatile corridor delays, and disjointed transport fleets caused massive demurrage penalties at regional ports.',
      intervention: 'Constructed an autonomous logistics orchestration pipeline with predictive border wait times and automated clearing manifests.',
      outcome: 'Corridor transit times reduced by 3.8 days; fleet fuel consumption decreased by 18% across 400+ transport units.'
    }
  ];

  const whitepapers = [
    {
      tome: 'TOME I',
      greekNumeral: 'Α // 01',
      tag: 'EXECUTIVE DISPATCH',
      title: 'The AI-Native Enterprise: Collapsing Strategy into Real-Time Execution',
      epigraph: 'Guiding enterprise navigation past the shoals of static consulting slide decks into dynamic computable topologies.',
      desc: 'Why conventional management consulting slide decks fail to deliver, and how closed-loop cognitive topologies bridge boardroom intent with real-time operational delivery.',
      author: 'LightSpeed Advisory Practice',
      readTime: '12 min read',
      downloads: '1,420 Executive Downloads',
      focus: 'Fiduciary Strategy & Topology'
    },
    {
      tome: 'TOME II',
      greekNumeral: 'Β // 02',
      tag: 'SOVEREIGN INTELLIGENCE',
      title: 'Sovereign Data Fabrics & Regional Compliance in the SADC Corridor',
      epigraph: 'Illuminating on-soil air-gapped compute architectures that withstand regulatory and data residency storms.',
      desc: 'Architecting air-gapped, on-soil inference clusters that comply strictly with national banking acts and SADC regional data residency mandates without sacrificing LLM reasoning capabilities.',
      author: 'Systems & Infrastructure Group',
      readTime: '15 min read',
      downloads: '980 Executive Downloads',
      focus: 'On-Premises Sovereignty'
    },
    {
      tome: 'TOME III',
      greekNumeral: 'Γ // 03',
      tag: 'SYSTEMS ENGINEERING',
      title: 'Deterministic Fiduciary Controls in Multi-Agent Swarms',
      epigraph: 'Mathematical bounds and cryptographic human-in-the-loop gates preventing agentic drift and hallucination.',
      desc: 'A mathematical and architectural specification for bounding autonomous AI agents to canonical tools, rate limits, and cryptographic human-in-the-loop approval gates.',
      author: 'AI Engineering Division',
      readTime: '18 min read',
      downloads: '2,150 Technical Downloads',
      focus: 'Agentic DAG Verification'
    },
    {
      tome: 'TOME IV',
      greekNumeral: 'Δ // 04',
      tag: 'REGULATORY TREATISE',
      title: 'The Alexandria Protocol: Air-Gapped High-Assurance Compute for Central Banks',
      epigraph: 'Deterministic settlement rails and anti-money laundering verification under sovereign jurisdictional bounds.',
      desc: 'Formulating provable cryptographic audit trails for automated foreign currency issuance, letters of credit, and cross-border customs declarations.',
      author: 'Sovereign Regulatory Institute',
      readTime: '20 min read',
      downloads: '1,840 Central Bank Downloads',
      focus: 'Monetary & Fiduciary Proofs'
    }
  ];

  return (
    <div className={`relative z-10 w-full transition-colors duration-300 ${
      isLight ? 'text-slate-700 selection:bg-orange-100 selection:text-slate-900' : 'text-zinc-300 selection:bg-white/20 selection:text-white'
    }`}>

      {/* SECTION 01: HERO — STRATEGY TO INTELLIGENT EXECUTION */}
      <section id="hero" className="relative min-h-[92vh] flex flex-col justify-center pt-28 pb-16 px-4 sm:px-8 max-w-7xl mx-auto w-full">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center relative z-10 w-full">
          
          {/* Left Column: Core Positioning Statement & Vision */}
          <div className="lg:col-span-7 xl:col-span-7 space-y-6 text-left">
            
            {/* Eyebrow Badge */}
            <div className={`inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border text-[11px] font-mono tracking-widest transition-all shadow-xs ${
              isLight 
                ? 'bg-white border-slate-300 text-slate-900 shadow-orange-500/5' 
                : 'bg-zinc-900/90 border-orange-500/40 text-zinc-300 shadow-black/40'
            }`}>
              <span className="w-2 h-2 rounded-full bg-orange-500 shadow-sm shadow-orange-500/80 animate-pulse" />
              <span>MALAWI-ROOTED • SADC-FOCUSED • GLOBAL CAPABILITY</span>
            </div>

            {/* Main Headline: Positioning Statement */}
            <h1 className={`text-4xl sm:text-6xl md:text-7xl font-black tracking-tight font-display leading-[1.04] ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              FROM STRATEGY <br />
              <span className={isLight 
                ? 'text-transparent bg-clip-text bg-gradient-to-r from-orange-600 via-amber-600 to-slate-900'
                : 'text-transparent bg-clip-text bg-gradient-to-r from-orange-400 via-amber-400 to-amber-200'
              }>
                TO INTELLIGENT
              </span> <br />
              EXECUTION.
            </h1>

            {/* Divider Accent Line */}
            <div className="flex items-center gap-2">
              <div className={`w-16 h-[2px] ${isLight ? 'bg-orange-500/80' : 'bg-orange-500'}`} />
              <div className="w-1.5 h-1.5 rounded-xs bg-orange-400 shadow-sm shadow-orange-400" />
            </div>

            {/* Explicit Regional Proposition Statement */}
            <div className="space-y-3">
              <p className={`text-justify text-justify max-w-2xl text-base sm:text-lg font-bold leading-relaxed ${
                isLight ? 'text-slate-900' : 'text-zinc-100'
              }`}>
                From Malawi, <span className="text-orange-500 font-extrabold">LightSpeed</span> helps organizations across SADC turn strategy, data, AI, and technology into practical execution.
              </p>
              <p className={`text-justify text-justify max-w-2xl text-xs sm:text-sm leading-relaxed ${
                isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'
              }`}>
                We position Southern Africa as a high-potential market for practical innovation, institutional transformation, locally grounded AI systems, and new operating models—combining management consulting, data engineering, AI fleets, and fiduciary governance.
              </p>
            </div>

            {/* 30-60 Second Visually Understandable Regional Advantage Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 max-w-2xl">
              <div className={`p-3.5 rounded-2xl border transition-all ${
                isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/80 border-slate-800'
              }`}>
                <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-orange-500 mb-1 font-mono">
                  <span className="w-1.5 h-1.5 rounded-full bg-orange-500" />
                  Local Fluency
                </div>
                <p className={`text-justify text-justify text-[11px] leading-snug ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                  Deep operational mastery of Malawi’s institutions, business realities, infrastructure, and talent environment.
                </p>
              </div>

              <div className={`p-3.5 rounded-2xl border transition-all ${
                isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/80 border-slate-800'
              }`}>
                <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-orange-500 mb-1 font-mono">
                  <span className="w-1.5 h-1.5 rounded-full bg-orange-500" />
                  Regional SADC
                </div>
                <p className={`text-justify text-justify text-[11px] leading-snug ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                  Solutions architected for SADC corridor dynamics, trade integration, and national regulatory nuances.
                </p>
              </div>

              <div className={`p-3.5 rounded-2xl border transition-all ${
                isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/80 border-slate-800'
              }`}>
                <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-orange-500 mb-1 font-mono">
                  <span className="w-1.5 h-1.5 rounded-full bg-orange-500" />
                  Global Standards
                </div>
                <p className={`text-justify text-justify text-[11px] leading-snug ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                  Engineering, security, air-gapped governance, and design quality standing alongside top international firms.
                </p>
              </div>
            </div>

            {/* Primary Action Buttons */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <a
                href="#operating-model"
                className="group inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-lg shadow-orange-500/30 transition-all cursor-pointer"
              >
                <div className="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center transition-transform group-hover:translate-x-0.5">
                  <ArrowRight className="w-3 h-3" />
                </div>
                <span>Explore Operating Model</span>
              </a>

              <button
                onClick={() => onRequestBriefing('SADC Regional Transformation Briefing')}
                className={`px-6 py-3.5 rounded-full font-bold text-xs tracking-widest border transition-all shadow-xs flex items-center gap-2 cursor-pointer ${
                  isLight 
                    ? 'bg-slate-900 hover:bg-slate-800 text-white border-slate-900' 
                    : 'bg-orange-500 hover:bg-orange-600 text-white border-orange-500'
                }`}
              >
                <span>Request Briefing</span>
              </button>

              <a
                href="#diagnostic"
                className={`px-5 py-3.5 rounded-full font-bold text-xs tracking-widest border backdrop-blur-xl transition-all shadow-xs flex items-center gap-2 cursor-pointer ${
                  isLight 
                    ? 'bg-white hover:bg-slate-50 text-slate-900 border-slate-300 hover:border-orange-500' 
                    : 'bg-zinc-900/80 hover:bg-zinc-800 text-zinc-300 hover:text-white border-white/15'
                }`}
              >
                <Sparkles className="w-3.5 h-3.5 text-orange-500" />
                <span>AI Diagnostic</span>
              </a>
            </div>

            {/* 30-Second Clarity Metric Strip */}
            <div className={`pt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 border-t max-w-2xl ${
              isLight ? 'border-slate-200' : 'border-white/15'
            }`}>
              <div>
                <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-[#2D3748]' : 'text-[#2D3748]'}`}>Formulation Cycle</span>
                <span className="text-sm font-bold font-mono text-orange-500">9 Months → Real-Time</span>
              </div>
              <div>
                <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-[#2D3748]' : 'text-[#2D3748]'}`}>Settlement Speed</span>
                <span className="text-sm font-bold font-mono text-emerald-500">14 Min Trade Rails</span>
              </div>
              <div>
                <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-[#2D3748]' : 'text-[#2D3748]'}`}>Recovered Duties</span>
                <span className={`text-sm font-bold font-mono ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>$14.2M in Q1</span>
              </div>
              <div>
                <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-[#2D3748]' : 'text-[#2D3748]'}`}>Governance</span>
                <span className={`text-sm font-bold font-mono ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>100% Auditable</span>
              </div>
            </div>

          </div>

          {/* Right Column: Audio/Hardware-Grade 4-Pillars Architectural Chassis Card */}
          <div className="lg:col-span-5 xl:col-span-5 flex justify-end">
            <div className={`p-6 sm:p-7 rounded-3xl max-w-md w-full transition-all duration-300 relative overflow-hidden ${
              isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
            }`}>
              {/* Hardware Hex Corner Fasteners */}
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              {/* Chassis Header Strip with Micro Acoustic Vent */}
              <div className={`flex items-center justify-between pb-3.5 border-b ${isLight ? 'border-black/10' : 'border-white/10'}`}>
                <div className="flex items-center gap-2 pl-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.9)]" />
                  <span className={`font-mono text-xs font-bold tracking-wider ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                    OPERATING TOPOLOGY
                  </span>
                </div>
                <div className="flex items-center gap-2.5 pr-2">
                  <AcousticVentGrille variant="strip" isLight={isLight} />
                  <span className="text-[10px] font-mono text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20 font-bold">
                    LIVE CORE
                  </span>
                </div>
              </div>

              {/* The 4 Connected Pillars (Tactile Hardware Stepped Array) */}
              <div className="space-y-2 pt-4">
                {[
                  { num: '01', title: 'Strategy', desc: 'Operating model redesign & capital allocation', tag: 'Executive', idx: 0 },
                  { num: '02', title: 'Intelligence', desc: 'Private data fabrics & semantic synthesis', tag: 'Sovereign', idx: 1 },
                  { num: '03', title: 'AI-Native Systems', desc: 'Multi-agent orchestration & deterministic DAGs', tag: 'Autonomous', idx: 2 },
                  { num: '04', title: 'Execution', desc: 'Legacy core integration & instant settlement', tag: 'Production', idx: 3 }
                ].map((p) => (
                  <button 
                    key={p.num}
                    onClick={() => {
                      setActivePillar(p.idx);
                      const el = document.getElementById('capabilities');
                      if (el) el.scrollIntoView({ behavior: 'smooth' });
                    }}
                    className={`w-full text-left p-3 rounded-2xl transition-all cursor-pointer group ${
                      activePillar === p.idx
                        ? isLight ? 'tactile-btn-active-light border-orange-500/50' : 'tactile-btn-active-dark border-orange-500/50'
                        : isLight 
                          ? 'tactile-concave-btn-light' 
                          : 'tactile-concave-btn-dark'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs mb-1">
                      <div className="flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full transition-all ${
                          activePillar === p.idx ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                        }`} />
                        <span className="font-mono font-bold text-orange-500">{p.num}</span>
                        <span className={`font-bold font-display group-hover:text-orange-500 transition-colors ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{p.title}</span>
                      </div>
                      <span className={`text-[10px] font-mono font-semibold ${activePillar === p.idx ? 'text-orange-500' : 'text-[#2D3748]'}`}>{p.tag}</span>
                    </div>
                    <p className="text-justify text-justify text-xs leading-snug pl-6 text-[#2D3748] font-medium">
                      {p.desc}
                    </p>
                  </button>
                ))}
              </div>

              {/* Card Footer */}
              <div className={`pt-4 mt-3 border-t flex items-center justify-between text-xs px-2 ${isLight ? 'border-black/10' : 'border-white/10'}`}>
                <span className="font-mono text-[10px] font-semibold text-[#2D3748]">SADC & International</span>
                <button
                  onClick={() => onRequestBriefing()}
                  className="font-mono text-[11px] font-bold text-orange-500 hover:text-orange-400 flex items-center gap-1 cursor-pointer"
                >
                  <span>Partner Briefing</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>

            </div>
          </div>

        </div>
      </section>

      {/* SECTION 02: THE LIGHTSPEED THESIS — 3D INTERACTIVE OPERATING MODEL (Objective 2 & 3) */}
      <section id="operating-model" className="py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full relative z-10">
        <InteractiveOperatingModel 
          theme={theme}
          onRequestBriefing={onRequestBriefing}
        />
      </section>

      {/* SECTION 03: THE 4 CONNECTED CORE OFFERINGS */}
      <section id="capabilities" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="max-w-3xl mb-12 space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-500 font-mono text-[11px] tracking-widest">
            <Network className="w-3.5 h-3.5" />
            <span>INTEGRATED SOVEREIGN ARCHITECTURE</span>
          </div>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Four Connected Core Offerings
          </h2>
          <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Lightspeed does not deliver isolated point-tools or transient chatbots. We engineer a closed-loop institutional stack where high-level strategy directly compiles into private knowledge graphs, deterministic agent fleets, and audited core execution.
          </p>
        </div>

        {/* 4 Core Offerings Tab Switcher (Hardware Transport Stepped Array) */}
        <div className={`p-2 rounded-3xl mb-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 ${
          isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'
        }`}>
          {coreCapabilities.map((cap, idx) => (
            <button
              key={cap.id}
              onClick={() => setActivePillar(idx)}
              className={`p-4 rounded-2xl text-left transition-all duration-200 cursor-pointer relative overflow-hidden group ${
                activePillar === idx
                  ? isLight 
                    ? 'tactile-btn-active-light text-slate-900 border-orange-500/50 shadow-md' 
                    : 'tactile-btn-active-dark text-white border-orange-500/50 shadow-lg'
                  : isLight 
                    ? 'tactile-btn-inactive-light text-slate-700' 
                    : 'tactile-btn-inactive-dark text-zinc-300'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    activePillar === idx ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                  }`} />
                  <span className={`text-[10px] font-mono tracking-widest font-bold px-2 py-0.5 rounded-md ${
                    activePillar === idx 
                      ? 'bg-orange-500/20 text-orange-500' 
                      : 'bg-black/5 text-[#2D3748]'
                  }`}>
                    OFFERING 0{idx + 1}
                  </span>
                </div>
                <span className={`text-[10px] font-mono font-medium ${
                  activePillar === idx ? 'text-orange-500 font-bold' : 'text-[#2D3748]'
                }`}>
                  {idx === 0 ? 'GOVERN' : idx === 1 ? 'SYNTHESIZE' : idx === 2 ? 'ORCHESTRATE' : 'SETTLE'}
                </span>
              </div>
              <span className="text-sm font-bold tracking-wide block font-display leading-tight">{cap.shortTitle}</span>
              <p className={`text-justify text-justify text-[11px] mt-1.5 line-clamp-2 ${
                activePillar === idx 
                  ? isLight ? 'text-slate-800 font-medium' : 'text-zinc-200' 
                  : 'text-[#2D3748]'
              }`}>
                {cap.tagline}
              </p>
            </button>
          ))}
        </div>

        {/* Active Core Offering Deep-Dive View */}
        {(() => {
          const active = coreCapabilities[activePillar];
          return (
            <div className={`p-6 sm:p-10 rounded-3xl transition-all duration-300 relative overflow-hidden shadow-2xl ${
              isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
            }`}>
              {/* Hardware Hex Corner Screws */}
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              {/* Corner Badge */}
              <div className="absolute top-0 right-0 py-1.5 px-4 rounded-bl-2xl bg-orange-500 text-white text-[10px] font-mono font-bold tracking-wider shadow-md">
                {active.governance}
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                
                {/* Left Column: Core Description & Contracts */}
                <div className="lg:col-span-7 space-y-6">
                  <div>
                    <span className="text-xs font-mono font-bold tracking-wider text-orange-500 block mb-1">
                      {active.eyebrow}
                    </span>
                    <h3 className={`text-2xl sm:text-3xl font-black tracking-tight font-display ${
                      isLight ? 'text-slate-900' : 'text-white'
                    }`}>
                      {active.title}
                    </h3>
                    <div className={`text-sm font-semibold mt-1 ${isLight ? 'text-slate-800' : 'text-orange-400'}`}>
                      {active.tagline}
                    </div>
                  </div>

                  <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
                    isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
                  }`}>
                    {active.desc}
                  </p>

                  {/* Inter-Offering Data Contracts Box (Recessed Hardware Well) */}
                  <div className={`p-4 rounded-2xl space-y-3 ${
                    isLight ? 'hardware-well-light' : 'hardware-well-dark'
                  }`}>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <GitMerge className="w-4 h-4 text-orange-500" />
                        <span className={`text-xs font-mono font-bold ${isLight ? 'text-slate-900' : 'text-zinc-200'}`}>
                          Structured Inter-Offering Contracts
                        </span>
                      </div>
                      <AcousticVentGrille variant="cluster" isLight={isLight} />
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                      <div className={`p-3 rounded-xl border ${isLight ? 'bg-white/90 border-slate-300' : 'bg-zinc-950/80 border-white/10'}`}>
                        <span className={`text-[10px] font-mono font-bold block mb-1 ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                          Input Contract (Feeds In)
                        </span>
                        <p className={`text-justify text-justify font-medium leading-tight ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                          {active.inputContract}
                        </p>
                      </div>

                      <div className={`p-3 rounded-xl border ${isLight ? 'bg-white/90 border-slate-300' : 'bg-zinc-950/80 border-white/10'}`}>
                        <span className={`text-[10px] font-mono font-bold block mb-1 text-emerald-500`}>
                          Output Contract (Generates)
                        </span>
                        <p className={`text-justify text-justify font-medium leading-tight ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                          {active.outputContract}
                        </p>
                      </div>
                    </div>

                    {/* Upstream & Downstream Flow Lineage Grid */}
                    <div className={`pt-3 border-t grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs ${
                      isLight ? 'border-slate-200' : 'border-white/10'
                    }`}>
                      {/* Upstream Source Card */}
                      <div className={`p-3 rounded-xl border flex flex-col justify-between space-y-1.5 ${
                        isLight ? 'bg-orange-50/70 border-orange-200/80' : 'bg-orange-950/30 border-orange-500/20'
                      }`}>
                        <div className="flex items-center gap-1.5">
                          <span className="p-1 rounded-md bg-orange-500/15 text-orange-500">
                            <ArrowUpRight className="w-3.5 h-3.5" />
                          </span>
                          <span className="font-bold font-mono text-[10px] tracking-wider text-orange-500">
                            Upstream Source
                          </span>
                        </div>
                        <p className={`text-justify text-justify text-[11px] sm:text-xs leading-relaxed font-medium break-words ${
                          isLight ? 'text-slate-800' : 'text-zinc-300'
                        }`}>
                          {active.upstreamSource}
                        </p>
                      </div>

                      {/* Downstream Target Card */}
                      <div className={`p-3 rounded-xl border flex flex-col justify-between space-y-1.5 ${
                        isLight ? 'bg-emerald-50/70 border-emerald-200/80' : 'bg-emerald-950/30 border-emerald-500/20'
                      }`}>
                        <div className="flex items-center gap-1.5">
                          <span className="p-1 rounded-md bg-emerald-500/15 text-emerald-500">
                            <ArrowDownRight className="w-3.5 h-3.5" />
                          </span>
                          <span className="font-bold font-mono text-[10px] tracking-wider text-emerald-500">
                            Downstream Target
                          </span>
                        </div>
                        <p className={`text-justify text-justify text-[11px] sm:text-xs leading-relaxed font-medium break-words ${
                          isLight ? 'text-slate-800' : 'text-zinc-300'
                        }`}>
                          {active.downstreamTarget}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Deliverables List */}
                  <div>
                    <div className={`text-xs font-mono font-bold mb-3 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                      Production Deliverables & Specifications:
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                      {active.deliverables.map((item, dIdx) => (
                        <div 
                          key={dIdx} 
                          className={`flex items-center gap-2.5 p-3 rounded-xl border text-xs font-medium transition-colors ${
                            isLight ? 'bg-slate-50 border-slate-300 text-slate-800 hover:bg-slate-100' : 'border-white/15 bg-white/[0.04] text-zinc-300 hover:bg-white/[0.08]'
                          }`}
                        >
                          <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                          <span className="leading-snug">{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Right Column: Institutional Benchmarks & Engagement Model */}
                <div className="lg:col-span-5 space-y-5">
                  <div className={`p-6 rounded-2xl ${
                    isLight ? 'hardware-well-light' : 'hardware-well-dark'
                  }`}>
                    <span className={`text-xs font-mono block mb-1 font-bold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                      Verified Institutional Benchmark
                    </span>
                    <div className="text-xl sm:text-2xl font-black font-mono text-emerald-500">
                      {active.metrics}
                    </div>
                    <div className={`text-xs font-medium mt-2 leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                      Backed by audited telemetry in live production deployments across SADC commercial banking, national revenue authorities, and transport corridors.
                    </div>
                  </div>

                  {/* Interconnected Ecosystem Nav (Tactile Stepped Array) */}
                  <div className={`p-5 rounded-2xl space-y-3 ${
                    isLight ? 'hardware-well-light' : 'hardware-well-dark'
                  }`}>
                    <div className="flex items-center justify-between text-xs font-mono font-bold">
                      <span className={isLight ? 'text-slate-900' : 'text-zinc-200'}>Integrated Suite Position</span>
                      <span className="text-orange-500">Step {activePillar + 1} of 4</span>
                    </div>

                    <div className="grid grid-cols-4 gap-1.5">
                      {coreCapabilities.map((c, cIdx) => (
                        <button
                          key={c.id}
                          onClick={() => setActivePillar(cIdx)}
                          className={`h-2.5 rounded-full transition-all ${
                            activePillar === cIdx 
                              ? 'bg-orange-500 shadow-[0_0_6px_rgba(249,115,22,0.8)]' 
                              : isLight ? 'bg-slate-300 hover:bg-slate-400' : 'bg-zinc-800 hover:bg-zinc-700'
                          }`}
                          title={`Switch to Offering 0${cIdx + 1}: ${c.shortTitle}`}
                        />
                      ))}
                    </div>

                    <div className="flex items-center justify-between pt-2">
                      <button
                        onClick={() => setActivePillar((activePillar + 3) % 4)}
                        className={`text-xs font-mono font-semibold hover:text-orange-500 cursor-pointer ${
                          isLight ? 'text-slate-600' : 'text-zinc-400'
                        }`}
                      >
                        ← Prev Offering
                      </button>
                      <button
                        onClick={() => setActivePillar((activePillar + 1) % 4)}
                        className="text-xs font-mono font-bold text-orange-500 hover:text-orange-400 cursor-pointer flex items-center gap-1"
                      >
                        <span>Next Offering</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </div>
                  </div>

                  <div className="p-6 rounded-2xl bg-orange-500/10 border border-orange-500/30 space-y-3 relative overflow-hidden">
                    <div className="text-xs font-mono tracking-wider text-orange-500 font-bold flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5" />
                      <span>Commercial Engagement Protocol</span>
                    </div>
                    <div className={`text-sm font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                      2-Week Advisory Sprint → 90-Day Co-Engineered Pilot
                    </div>
                    <p className={`text-justify text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                      We embed directly with executive committees to audit institutional latency, specify private cognitive topologies, and deliver verified production code with zero data leakage.
                    </p>
                    <button
                      onClick={() => onRequestBriefing(`Inquiry regarding ${active.title}: ${active.tagline}`)}
                      className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs tracking-wider flex items-center justify-center gap-2 cursor-pointer transition-all shadow-md shadow-orange-500/20 active:scale-98"
                    >
                      <span>Engage {active.shortTitle} Practice</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

              </div>
            </div>
          );
        })()}

        {/* INTERACTIVE CONTINUOUS CLOSED-LOOP & SYNERGY MATRIX */}
        <div className={`mt-12 p-8 sm:p-10 rounded-3xl border ${
          isLight ? 'bg-slate-50/80 border-slate-300' : 'bg-zinc-950/70 border-white/15'
        }`}>
          <div className="max-w-3xl mb-8 space-y-2">
            <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-500 font-mono text-[10px] tracking-widest">
              <RefreshCw className="w-3 h-3" />
              <span>THE CLOSED-LOOP MULTIPLIER EFFECT</span>
            </div>
            <h3 className={`text-2xl sm:text-3xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              How the Four Offerings Interconnect
            </h3>
            <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Deploying any single offering creates value, but connecting all four creates an insurmountable sovereign compounding advantage. Click any interface pair below to inspect the joint protocol:
            </p>
          </div>

          {/* Synergy Pair Selector Buttons */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
            {Object.entries(synergyPairs).map(([key, pair]) => (
              <button
                key={key}
                onClick={() => setSelectedSynergy(key)}
                className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer ${
                  selectedSynergy === key
                    ? 'bg-orange-500 text-white border-orange-400 shadow-md shadow-orange-500/20'
                    : isLight 
                      ? 'bg-white hover:bg-slate-100 text-slate-800 border-slate-300' 
                      : 'bg-zinc-900/80 hover:bg-zinc-900 text-zinc-300 border-white/15'
                }`}
              >
                <div className={`text-[10px] font-mono font-bold mb-1 ${
                  selectedSynergy === key ? 'text-orange-100' : 'text-orange-500'
                }`}>
                  {pair.title}
                </div>
                <div className="text-xs font-bold truncate">{pair.headline}</div>
              </button>
            ))}
          </div>

          {/* Active Synergy Detail Card */}
          {(() => {
            const pair = synergyPairs[selectedSynergy];
            if (!pair) return null;
            return (
              <div className={`p-6 rounded-2xl border transition-all ${
                isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-zinc-900/90 border-white/20'
              }`}>
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-orange-500/20 mb-4">
                  <div className="flex items-center gap-3">
                    <span className="px-3 py-1 rounded-lg bg-orange-500 text-white font-mono text-xs font-bold">
                      {pair.title}
                    </span>
                    <h4 className={`text-base font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {pair.headline}
                    </h4>
                  </div>
                  <div className="flex items-center gap-2 text-xs font-mono font-semibold text-emerald-500">
                    <Activity className="w-3.5 h-3.5" />
                    <span>Real-time Integration Protocol</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
                  <div className="md:col-span-7 space-y-2">
                    <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                      Integration Mechanism & Technical Contract
                    </span>
                    <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                      {pair.mechanism}
                    </p>
                  </div>

                  <div className={`md:col-span-5 p-4 rounded-xl border ${
                    isLight ? 'bg-emerald-50/70 border-emerald-200 text-emerald-950' : 'bg-emerald-950/20 border-emerald-500/30 text-emerald-200'
                  }`}>
                    <span className="text-[10px] font-mono font-bold text-emerald-600 dark:text-emerald-400 block mb-1">
                      Compound Institutional Impact
                    </span>
                    <p className="text-justify text-justify text-xs font-bold leading-relaxed">
                      {pair.compoundImpact}
                    </p>
                  </div>
                </div>
              </div>
            );
          })()}

          {/* Comparative Table: Point Solutions vs. Lightspeed Connected Suite */}
          <div className="mt-8 pt-8 border-t border-slate-200 dark:border-white/10">
            <div className="flex items-center justify-between mb-4">
              <span className={`text-xs font-mono font-bold tracking-wider ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                Architectural Contrast: Disconnected Point-Tools vs. Connected Sovereign Suite
              </span>
              <span className="text-[10px] font-mono text-orange-500 font-bold">
                Zero Cloud SaaS Leakage
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className={`border-b ${isLight ? 'border-slate-300 bg-slate-100/80 text-slate-800' : 'border-white/10 bg-zinc-900/50 text-zinc-300'}`}>
                    <th className="p-3 font-mono font-bold">Offering Layer</th>
                    <th className="p-3 font-mono font-bold text-rose-500">Fragmented Point Solution</th>
                    <th className="p-3 font-mono font-bold text-emerald-500">Lightspeed Connected Architecture</th>
                  </tr>
                </thead>
                <tbody className={`divide-y ${isLight ? 'divide-slate-200 text-slate-700' : 'divide-white/10 text-zinc-300'}`}>
                  <tr>
                    <td className="p-3 font-bold font-mono text-orange-500">01. Strategy</td>
                    <td className="p-3">Static PowerPoint slide decks, 9-month review cycles, zero computable rules.</td>
                    <td className="p-3 font-medium text-emerald-600 dark:text-emerald-400">Executable Policy-as-Code, dynamic token budgets, computable board models.</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-bold font-mono text-orange-500">02. Intelligence</td>
                    <td className="p-3">Siloed data lakes, public LLM SaaS APIs risking trade secrets and residency.</td>
                    <td className="p-3 font-medium text-emerald-600 dark:text-emerald-400">100% sovereign air-gapped knowledge graphs with cryptographic AST lineage.</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-bold font-mono text-orange-500">03. Autonomous Systems</td>
                    <td className="p-3">Unbounded probabilistic chatbots prone to hallucinations and tool abuse.</td>
                    <td className="p-3 font-medium text-emerald-600 dark:text-emerald-400">Deterministic OpenCode agent fleets bound to 7 canonical tools and strict DAGs.</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-bold font-mono text-orange-500">04. Execution & Governance</td>
                    <td className="p-3">Manual data re-entry, 72-hour paper settlement, post-facto audit trails.</td>
                    <td className="p-3 font-medium text-emerald-600 dark:text-emerald-400">Direct core API event rails, Human-in-the-Loop gates, immutable SHA-256 ledgers.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

      </section>

      {/* SECTION 04: THE SYSTEMIC PROBLEM — THE STRATEGY-EXECUTION CHASM */}
      <section id="problem" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-orange-500">
            THE STRATEGY-EXECUTION CHASM
          </span>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Why Enterprise Transformations Fail
          </h2>
          <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Institutions do not fail for lack of strategy. They fail because strategy is stranded in slide decks, data is trapped in silos, and execution requires months of bureaucratic handoffs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Failure Trap 01 */}
          <div className={`p-8 rounded-3xl border transition-all flex flex-col justify-between ${
            isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-lg' : 'bg-zinc-950/80 border-white/15 text-zinc-300 shadow-xl'
          }`}>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-mono font-black text-orange-500">01</span>
                <span className="text-[10px] font-mono tracking-widest px-2.5 py-0.5 rounded-full border border-red-500/30 text-red-500 bg-red-500/10 font-bold">
                  THE SLIDE TRAP
                </span>
              </div>
              <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Static Strategy Decks</h3>
              <p className="text-justify text-justify text-xs sm:text-sm leading-relaxed text-[#2D3748]">
                Conventional consultancies spend 6 months formulating 200-page slide decks. By the time the presentation is delivered, market conditions have shifted, and the strategy is already obsolete.
              </p>
            </div>
            <div className={`pt-6 border-t text-xs font-mono flex justify-between font-semibold ${isLight ? 'border-slate-200' : 'border-white/10'} text-[#2D3748]`}>
              <span>LATENCY: 6–9 MONTHS</span>
              <span className="text-red-500 font-bold">CODE SHIPPED: 0%</span>
            </div>
          </div>

          {/* Failure Trap 02 */}
          <div className={`p-8 rounded-3xl border transition-all flex flex-col justify-between ${
            isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-lg' : 'bg-zinc-950/80 border-white/15 text-zinc-300 shadow-xl'
          }`}>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-mono font-black text-orange-500">02</span>
                <span className="text-[10px] font-mono tracking-widest px-2.5 py-0.5 rounded-full border border-amber-500/30 text-amber-500 bg-amber-500/10 font-bold">
                  THE SILO TAX
                </span>
              </div>
              <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Fragmented Knowledge Pools</h3>
              <p className="text-justify text-justify text-xs sm:text-sm leading-relaxed text-[#2D3748]">
                Critical business truth is locked within legacy mainframe ERPs, paper bills-of-lading, and siloed spreadsheets. Executives make multimillion-dollar decisions on information that is two weeks stale.
              </p>
            </div>
            <div className={`pt-6 border-t text-xs font-mono flex justify-between font-semibold ${isLight ? 'border-slate-200' : 'border-white/10'} text-[#2D3748]`}>
              <span>TRUTH CONVERGENCE: POOR</span>
              <span className="text-amber-500 font-bold">FIDUCIARY RISK: HIGH</span>
            </div>
          </div>

          {/* Failure Trap 03 */}
          <div className={`p-8 rounded-3xl border transition-all flex flex-col justify-between ${
            isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-lg' : 'bg-zinc-950/80 border-white/15 text-zinc-300 shadow-xl'
          }`}>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-mono font-black text-orange-500">03</span>
                <span className="text-[10px] font-mono tracking-widest px-2.5 py-0.5 rounded-full border border-amber-500/30 text-amber-500 bg-amber-500/10 font-bold">
                  THE TOY PLAYGROUND
                </span>
              </div>
              <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Ungoverned Ad-Hoc AI</h3>
              <p className="text-justify text-justify text-xs sm:text-sm leading-relaxed text-[#2D3748]">
                Organizations subscribe to disjointed SaaS chatbots that generate text but have zero access to production ledgers, cannot invoke audited tools, and cannot assume fiduciary accountability.
              </p>
            </div>
            <div className={`pt-6 border-t text-xs font-mono flex justify-between font-semibold ${isLight ? 'border-slate-200' : 'border-white/10'} text-[#2D3748]`}>
              <span>BUSINESS IMPACT: 0%</span>
              <span className="text-orange-500 font-bold">COMPLIANCE: UNVERIFIED</span>
            </div>
          </div>

        </div>
      </section>

      {/* SECTION 05: SECTOR EXPERTISE & REGIONAL AUTHORITY (Objective 1) */}
      <section id="authority" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div className="space-y-2 max-w-2xl">
            <span className="text-xs font-mono font-bold tracking-widest text-orange-500">
              REGIONAL RELEVANCE & PROVEN AUTHORITY
            </span>
            <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              Engineered for Regulated Scale
            </h2>
            <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Tested and deployed in demanding African and international environments—where connectivity, data sovereignty, and regulatory scrutiny cannot be compromised.
            </p>
          </div>

          <div className={`flex flex-wrap p-1.5 rounded-2xl gap-2 ${
            isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'
          }`}>
            {Object.keys(industriesData).map((key) => {
              const isSelected = selectedIndustry === key;
              return (
                <button
                  key={key}
                  onClick={() => setSelectedIndustry(key)}
                  className={`px-4 py-2 rounded-xl text-xs font-mono font-bold tracking-wider transition-all duration-200 cursor-pointer flex items-center gap-2 ${
                    isSelected
                      ? isLight ? 'tactile-btn-active-light text-slate-900 border-orange-500/50' : 'tactile-btn-active-dark text-white border-orange-500/50'
                      : isLight 
                        ? 'tactile-btn-inactive-light text-slate-700' 
                        : 'tactile-btn-inactive-dark text-zinc-300'
                  }`}
                >
                  <span className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    isSelected ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                  }`} />
                  <span>{key}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Selected Sector Deep-Dive Card */}
        {(() => {
          const ind = industriesData[selectedIndustry];
          return (
            <div className={`p-8 sm:p-10 rounded-3xl border mb-12 ${
              isLight ? 'bg-white/95 border-slate-300 shadow-xl text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-2xl text-zinc-300'
            }`}>
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                <div className="lg:col-span-7 space-y-4">
                  <span className="text-xs font-mono text-orange-500 font-bold">
                    {ind.citation}
                  </span>
                  <h3 className={`text-2xl sm:text-3xl font-black tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{ind.title}</h3>
                  <p className={`text-justify text-justify text-sm font-semibold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>{ind.subtitle}</p>
                  <p className={`text-justify text-justify text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>{ind.description}</p>
                </div>

                <div className="lg:col-span-5 space-y-3">
                  <span className={`text-xs font-mono font-bold block ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                    Verified Production Impact:
                  </span>
                  {ind.impact.map((imp, iIdx) => (
                    <div 
                      key={iIdx} 
                      className={`p-3.5 rounded-2xl border text-xs flex items-start gap-2.5 font-medium ${
                        isLight ? 'bg-slate-50 border-slate-300 text-slate-800' : 'border-white/15 bg-white/[0.05] text-zinc-300'
                      }`}
                    >
                      <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                      <span>{imp}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          );
        })()}

        {/* Case Studies Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {caseStudies.map((cs, cIdx) => (
            <div 
              key={cIdx} 
              className={`p-6 rounded-3xl border flex flex-col justify-between space-y-4 ${
                isLight ? 'bg-slate-50 border-slate-300' : 'bg-zinc-900/70 border-white/15'
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between text-[11px] font-mono">
                  <span className="text-orange-500 font-bold">{cs.sector}</span>
                  <span className={`font-semibold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>PRODUCTION</span>
                </div>
                <div className={`text-sm font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{cs.client}</div>
                <p className={`text-justify text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                  <strong className={`font-semibold ${isLight ? 'text-slate-900' : 'text-zinc-200'}`}>Challenge:</strong> {cs.problem}
                </p>
                <p className={`text-justify text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                  <strong className={`font-semibold ${isLight ? 'text-slate-900' : 'text-zinc-200'}`}>LIGHTSPEED Solution:</strong> {cs.intervention}
                </p>
              </div>

              <div className="pt-3 border-t border-white/10 text-xs font-mono text-emerald-500 font-bold">
                Outcome: {cs.outcome}
              </div>
            </div>
          ))}
        </div>

      </section>

      {/* SECTION 06: INTERACTIVE AI TRANSFORMATION DIAGNOSTIC (Objective 4) */}
      <section id="diagnostic" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <TransformationDiagnostic 
          theme={theme}
          onRequestBriefing={onRequestBriefing}
        />
      </section>

      {/* SECTION 07: STANDARDIZED ARTIFACTS & DELIVERABLE TEMPLATES (With Hardware Interface Ports) */}
      <TemplatesArtifacts
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />

      {/* SECTION 08: PHAROS // THOUGHT LEADERSHIP (The Ancient Lighthouse of Alexandria on the Island of Pharos) */}
      <section id="publications" className={`py-28 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t relative overflow-hidden ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        {/* Subtle stone masonry background pattern */}
        <div className="absolute inset-0 pharos-stone-masonry pointer-events-none opacity-40" />

        {/* Pharos Header & Lighthouse Lore */}
        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-end mb-14">
          <div className="lg:col-span-8 space-y-4">
            <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-amber-500/40 bg-gradient-to-r from-amber-500/15 via-orange-500/10 to-transparent text-amber-500 font-mono text-[11px] tracking-widest shadow-sm">
              <span className="w-2 h-2 rounded-full bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,1)] animate-pulse" />
              <span>PHAROS // THE LIGHTHOUSE OF ALEXANDRIA</span>
            </div>

            <h2 className={`text-4xl sm:text-6xl font-black tracking-tight font-display leading-[1.05] ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              PHAROS <br />
              <span className={isLight 
                ? 'text-transparent bg-clip-text bg-gradient-to-r from-amber-600 via-orange-600 to-slate-900' 
                : 'text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-orange-400 to-amber-100'
              }>
                THOUGHT LEADERSHIP
              </span>
            </h2>

            <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed max-w-3xl ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Erected on the limestone bedrock of the island of Pharos in Alexandria, Egypt, the ancient Lighthouse stood as humanity's supreme beacon of guidance—projecting radiant light across treacherous maritime shoals. 
              In today's turbulent storm of AI hype, SaaS data leakages, and consulting slide paralysis, LIGHTSPEED's <strong className="text-orange-500 font-bold">PHAROS</strong> casts unyielding illumination: providing boards, central banks, and sovereign ministries with definitive mathematical, architectural, and fiduciary clarity.
            </p>
          </div>

          {/* Pharos Beacon Optical Station Telemetry Card */}
          <div className="lg:col-span-4">
            <div className={`p-5 rounded-3xl relative overflow-hidden backdrop-blur-xl ${
              isLight ? 'hardware-chassis-light text-slate-800' : 'hardware-chassis-dark text-zinc-300'
            }`}>
              {/* Sweeping Golden Beacon Light Ray Beam */}
              <div className="pharos-beacon-beam" />

              <div className="relative z-10 space-y-3">
                <div className="flex items-center justify-between border-b border-amber-500/20 pb-2.5">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,1)] animate-ping" />
                    <span className="font-mono text-xs font-bold tracking-wider text-amber-500">
                      PHAROS OPTICAL BEACON
                    </span>
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold">
                    RADIANT
                  </span>
                </div>

                <div className="space-y-1.5 text-[11px] font-mono">
                  <div className="flex justify-between">
                    <span className="text-[#2D3748]">Isle Coordinates:</span>
                    <span className="font-bold text-amber-400">31.2140° N, 29.8850° E</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#2D3748]">Optical Reach:</span>
                    <span className="font-bold text-emerald-400">300 Stadia (~55 km)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#2D3748]">Emission Spectrum:</span>
                    <span className="font-bold text-orange-400">589nm Solar Amber</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#2D3748]">Guiding Purpose:</span>
                    <span className={`font-bold ${isLight ? 'text-slate-800' : 'text-white'}`}>Sovereign Clarity</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 4 Pharos Treatises / Tomes Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 relative z-10">
          {whitepapers.map((wp, wIdx) => (
            <div 
              key={wIdx} 
              className={`p-6 sm:p-7 rounded-3xl flex flex-col justify-between space-y-6 transition-all group relative overflow-hidden ${
                isLight 
                  ? 'hardware-chassis-light hover:border-amber-500 text-slate-900' 
                  : 'hardware-chassis-dark hover:border-amber-500/60 text-zinc-300'
              }`}
            >
              {/* Corner Hardware Fasteners */}
              <div className="absolute top-2.5 left-2.5 w-1.5 h-1.5 rounded-full hardware-screw" />
              <div className="absolute top-2.5 right-2.5 w-1.5 h-1.5 rounded-full hardware-screw" />

              {/* Decorative classical top gold accent rule */}
              <div className="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-transparent via-amber-500/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

              <div className="space-y-3.5 pt-1">
                {/* Tome Header & Greek Numeral */}
                <div className="flex items-center justify-between text-[11px] font-mono border-b border-black/10 dark:border-white/10 pb-2.5">
                  <span className="px-2.5 py-0.5 rounded-full bg-amber-500/15 text-amber-500 border border-amber-500/30 font-bold">
                    {wp.tome}
                  </span>
                  <span className="font-semibold text-[#2D3748]">{wp.readTime}</span>
                </div>

                {/* Subtitle & Tag */}
                <div className="flex items-center justify-between text-[10px] font-mono">
                  <span className="text-orange-500 font-bold">{wp.tag}</span>
                  <span className="text-[#2D3748]">{wp.greekNumeral}</span>
                </div>

                {/* Title */}
                <h3 className={`text-base sm:text-lg font-bold tracking-tight leading-snug group-hover:text-amber-500 transition-colors ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  {wp.title}
                </h3>

                {/* Epigraph / Quote */}
                <blockquote className="text-xs italic border-l-2 pl-3 py-0.5 border-amber-400 text-[#2D3748]">
                  "{wp.epigraph}"
                </blockquote>

                {/* Detailed Description */}
                <p className="text-justify text-justify text-xs leading-relaxed text-[#2D3748]">
                  {wp.desc}
                </p>
              </div>

              {/* Treatise Footer */}
              <div className={`pt-4 border-t flex items-center justify-between text-xs ${
                isLight ? 'border-black/10' : 'border-white/10'
              }`}>
                <span className="text-[10px] font-mono font-medium text-[#2D3748]">
                  {wp.downloads}
                </span>
                <button
                  onClick={() => onRequestBriefing(`Request Pharos Treatise: ${wp.tome} - ${wp.title}`)}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-mono font-bold text-amber-500 hover:text-amber-400 cursor-pointer transition-all ${
                    isLight ? 'tactile-concave-btn-light' : 'tactile-concave-btn-dark'
                  }`}
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download Tome</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* SECTION 09: COMMERCIAL CONVERSION & ENGAGEMENT MODELS (Objective 4) */}
      <section id="engagement" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-orange-500">
            HOW WE ENGAGE
          </span>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Engagement Structures
          </h2>
          <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Structured engagement frameworks designed for institutional leadership, board accountability, and rapid time-to-value.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Model 01 */}
          <div className={`p-8 rounded-3xl border flex flex-col justify-between space-y-6 ${
            isLight ? 'bg-white/95 border-slate-300 shadow-md text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-xl text-zinc-300'
          }`}>
            <div className="space-y-4">
              <span className={`text-xs font-mono font-bold block ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                PHASE 01 // 2 WEEKS
              </span>
              <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Advisory Architecture Sprint</h3>
              <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                A rapid forensic audit of your organizational topology, regulatory constraints, and sovereign data availability. Deliverable is an executive blueprint with computable business rules and an ROI model.
              </p>
              <ul className={`space-y-2 text-xs font-medium pt-2 ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>Cognitive Friction & Latency Audit</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>Sovereign Data Residency Blueprint</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>Board-Level Investment Case</span>
                </li>
              </ul>
            </div>

            <button
              onClick={() => onRequestBriefing('Advisory Architecture Sprint (2 Weeks)')}
              className="w-full py-3 rounded-full border border-orange-500/50 text-orange-500 hover:bg-orange-500 hover:text-white font-bold text-xs tracking-wider transition-colors cursor-pointer"
            >
              Initiate Architecture Sprint
            </button>
          </div>

          {/* Model 02: Featured Co-Engineered Pilot */}
          <div className="p-8 rounded-3xl border-2 border-orange-500 bg-gradient-to-b from-orange-500/10 via-zinc-950 to-zinc-950 flex flex-col justify-between space-y-6 relative shadow-2xl shadow-orange-500/10">
            <div className="absolute -top-3 left-8 px-3 py-1 rounded-full bg-orange-500 text-white font-mono text-[10px] font-bold tracking-widest">
              MOST COMMON COMMENCEMENT
            </div>

            <div className="space-y-4">
              <span className="text-xs font-mono text-orange-400 font-bold block">
                PHASE 02 // 90 DAYS
              </span>
              <h3 className="text-xl font-bold tracking-tight text-white">Co-Engineered Pilot</h3>
              <p className="text-justify text-justify text-xs sm:text-sm text-zinc-300 leading-relaxed font-normal">
                Co-deploying a live sovereign multi-agent pipeline alongside your internal engineers. Proving measurable business outcomes against real transaction volume before broad institutional rollout.
              </p>
              <ul className="space-y-2 text-xs text-zinc-200 font-medium pt-2">
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                  <span>Production Core API Integration</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                  <span>Human-in-the-Loop Sign-off Gates</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                  <span>Verified ROI Ledgers & SLA Guarantee</span>
                </li>
              </ul>
            </div>

            <button
              onClick={() => onRequestBriefing('Co-Engineered Pilot (90 Days)')}
              className="w-full py-3.5 rounded-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs tracking-widest transition-all cursor-pointer shadow-md shadow-orange-500/25"
            >
              Request Pilot Consultation
            </button>
          </div>

          {/* Model 03 */}
          <div className={`p-8 rounded-3xl border flex flex-col justify-between space-y-6 ${
            isLight ? 'bg-white/95 border-slate-300 shadow-md text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-xl text-zinc-300'
          }`}>
            <div className="space-y-4">
              <span className={`text-xs font-mono font-bold block ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                PHASE 03 // ENTERPRISE SCALE
              </span>
              <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Sovereign Enterprise Deployment</h3>
              <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                Full-scale institutional transition to an AI-native operating model. Continuous agent fleets, on-premise air-gapped inference clusters, and embedded transformation partners.
              </p>
              <ul className={`space-y-2 text-xs font-medium pt-2 ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>Autonomous Multi-Agent Fleet</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>Enterprise Sovereign Air-Gap Infra</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>24/7 Model Drift & Security Oversight</span>
                </li>
              </ul>
            </div>

            <button
              onClick={() => onRequestBriefing('Sovereign Enterprise Deployment')}
              className="w-full py-3 rounded-full border border-orange-500/50 text-orange-500 hover:bg-orange-500 hover:text-white font-bold text-xs tracking-wider transition-colors cursor-pointer"
            >
              Consult On Enterprise Scope
            </button>
          </div>

        </div>
      </section>

      {/* SECTION 10: FREQUENTLY ASKED QUESTIONS */}
      <section id="faq" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-orange-500">
            CLARITY & ASSURANCE
          </span>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Frequently Asked Questions
          </h2>
          <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Addressing the critical security, structural, and fiduciary considerations of enterprise AI integration and standardized deliverable templates.
          </p>
        </div>

        <div className="max-w-4xl mx-auto space-y-6">
          {[
            {
              q: "What is the purpose of the Templates & Deliverables section?",
              a: "The Templates section showcases production-grade, standardized architectural deliverables engineered by LightSpeed for institutional clients across SADC. These include formal OpenCode-compatible agent YAML schemas, deterministic DAG task flows, sovereign data residency matrices, SADC trade finance compliance frameworks, and Human-in-the-Loop (HITL) cryptographic approval gates. Clients utilize these templates as actionable blueprints to eliminate the 6–9 month strategy gap and deploy verified AI-native operating models directly into production."
            },
            {
              q: "Are these templates static documents or executable engineering artifacts?",
              a: "Every template is an executable, deterministic artifact. Unlike standard consulting slide decks, our templates define canonical tool boundaries, task token budgets, audit logging mechanisms, and live API wrapper patterns that can be directly provisioned, compiled, and run within your enterprise VPC and sovereign compute clusters."
            },
            {
              q: "What is LightSpeed's core proposition?",
              a: "From Malawi, LightSpeed helps organizations across SADC turn strategy, data, AI, and technology into practical execution. We bridge the gap between abstract strategy formulation and concrete technological execution by combining local operating fluency, regional SADC relevance, and global standards in strategy, engineering, governance, and design quality."
            },
            {
              q: "What is deterministic multi-agent fleet engineering?",
              a: "Unlike unstructured consumer chatbots that can hallucinate or invoke unauthorized operations, our multi-agent fleets are strictly bound by mathematically constrained tool parameters, rate limiters, and Human-in-the-Loop (HITL) approval gates. Every action executed by an agent is logged to an immutable cryptographic audit ledger."
            },
            {
              q: "How does LightSpeed ensure data sovereignty and privacy?",
              a: "We deploy air-gapped, on-soil inference clusters. Your data never leaves your secure VPC or private cloud. We build semantic knowledge graphs natively inside your organization's perimeter, ensuring strict adherence to regional compliance and national banking acts."
            },
            {
              q: "How fast can you integrate with legacy systems (e.g. monolithic banking cores)?",
              a: "During our 90-Day Co-Engineered Pilot, we build legacy core API modernization wrappers that translate mainframe and legacy protocols into reactive event streams. This typically reduces systemic transaction latencies from hours or days to sub-second settlements."
            },
            {
              q: "Why do conventional transformations fail?",
              a: "Conventional consultancies spend 6–9 months producing static slide decks with 0% shipped code (The Slide Trap), while organizations suffer from the 'Silo Tax' where critical institutional knowledge is locked in fragmented legacy databases. LightSpeed collapses this gap by delivering executable strategy backed by live sovereign systems."
            },
            {
              q: "How does an organization transition from these templates to full deployment?",
              a: "We offer a structured 3-phase progression: Phase 1 begins with a 2-Week Advisory Architecture Sprint to audit cognitive friction and map templates to your topology. Phase 2 transitions into a 90-Day Co-Engineered Pilot deploying live pipelines with internal teams. Phase 3 scales into a permanent Sovereign Enterprise Deployment with 24/7 telemetry and model drift oversight."
            }
          ].map((faq, idx) => (
            <div key={idx} className={`p-6 sm:p-8 rounded-3xl border transition-all ${
              isLight ? 'bg-white/95 border-slate-300 shadow-sm' : 'bg-zinc-950/80 border-white/15'
            }`}>
              <h3 className={`text-lg sm:text-xl font-bold tracking-tight mb-3 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                {faq.q}
              </h3>
              <p className={`text-justify text-justify text-sm leading-relaxed ${isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'}`}>
                {faq.a}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* SECTION 11: CONTACT / EXECUTIVE BRIEFING INTAKE (Objective 4) */}
      <section id="contact" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
          
          <div className="lg:col-span-5 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-500 font-mono text-[11px] tracking-widest font-bold">
              <span>COMMENCE TRANSFORMATION</span>
            </div>
            <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              Request an Executive Briefing
            </h2>
            <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Schedule a confidential 45-minute advisory diagnostic with our Managing Partners. We will assess your current operating latency and evaluate the feasibility of deploying sovereign AI architectures.
            </p>

            <div className={`space-y-4 pt-4 border-t ${isLight ? 'border-slate-200' : 'border-white/15'}`}>
              <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <ShieldCheck className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Strict fiduciary non-disclosure agreement standard</span>
              </div>
              <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <Clock className="w-4 h-4 text-orange-500 shrink-0" />
                <span>Executive response within 12 business hours</span>
              </div>
              <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <Globe2 className="w-4 h-4 text-amber-500 shrink-0" />
                <span>Offices in Southern Africa & International Advisory Network</span>
              </div>
            </div>
          </div>

          <div className="lg:col-span-7">
            <div className={`p-8 sm:p-10 rounded-3xl relative overflow-hidden shadow-2xl ${
              isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
            }`}>
              {/* Hardware Screws */}
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              {/* Console Header Bar */}
              <div className="flex items-center justify-between pb-3.5 mb-6 border-b border-black/10 dark:border-white/10 px-1">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.9)]" />
                  <span className="font-mono text-xs font-bold tracking-wider">
                    BRIEFING TRANSMISSION CONSOLE
                  </span>
                </div>
                <AcousticVentGrille variant="strip" isLight={isLight} />
              </div>

              {contactSubmitted ? (
                <div className="py-12 text-center space-y-4">
                  <div className="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-500 border border-emerald-500/40 flex items-center justify-center mx-auto shadow-[0_0_15px_rgba(16,185,129,0.3)]">
                    <CheckCircle2 className="w-8 h-8" />
                  </div>
                  <h3 className={`text-2xl font-black tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                    Briefing Request Received
                  </h3>
                  <p className={`text-justify text-justify text-sm max-w-md mx-auto leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                    Thank you. A Senior Partner will review your institutional profile and contact you directly within 12 business hours.
                  </p>
                  <button
                    onClick={() => setContactSubmitted(false)}
                    className="px-6 py-2.5 rounded-xl bg-orange-500 text-white font-bold text-xs tracking-wider cursor-pointer shadow-md hover:bg-orange-600 transition-all"
                  >
                    Submit Another Inquiry
                  </button>
                </div>
              ) : (
                <form onSubmit={handleContactSubmit} className="space-y-4">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                        Executive Name *
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Dr. K. Mlangeni"
                        value={contactFormData.name}
                        onChange={(e) => setContactFormData({ ...contactFormData, name: e.target.value })}
                        className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                          isLight 
                            ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner' 
                            : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner'
                        }`}
                      />
                    </div>
                    <div>
                      <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                        Executive Title *
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Chief Executive Officer"
                        value={contactFormData.title}
                        onChange={(e) => setContactFormData({ ...contactFormData, title: e.target.value })}
                        className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                          isLight 
                            ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner' 
                            : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner'
                        }`}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                        Institution / Entity *
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Reserve Bank / Standard Bank"
                        value={contactFormData.organization}
                        onChange={(e) => setContactFormData({ ...contactFormData, organization: e.target.value })}
                        className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                          isLight 
                            ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner' 
                            : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner'
                        }`}
                      />
                    </div>
                    <div>
                      <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                        Official Email *
                      </label>
                      <input
                        type="email"
                        required
                        placeholder="executive@institution.com"
                        value={contactFormData.email}
                        onChange={(e) => setContactFormData({ ...contactFormData, email: e.target.value })}
                        className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                          isLight 
                            ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner' 
                            : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner'
                        }`}
                      />
                    </div>
                  </div>

                  <div>
                    <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                      Target Engagement Model
                    </label>
                    <select
                      value={contactFormData.scope}
                      onChange={(e) => setContactFormData({ ...contactFormData, scope: e.target.value })}
                      className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                        isLight 
                          ? 'bg-slate-100/90 border-slate-300 text-slate-900 shadow-inner' 
                          : 'bg-zinc-900 border-white/20 text-white shadow-inner'
                      }`}
                    >
                      <option value="Advisory Architecture Sprint (2 Weeks)">Advisory Architecture Sprint (2 Weeks)</option>
                      <option value="Co-Engineered Pilot (90 Days)">Co-Engineered Pilot (90 Days)</option>
                      <option value="Sovereign Enterprise Deployment">Sovereign Enterprise Deployment</option>
                      <option value="Executive Boardroom Briefing">Executive Boardroom Briefing</option>
                    </select>
                  </div>

                  <div>
                    <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                      Strategic Objectives & Context
                    </label>
                    <textarea
                      rows={3}
                      placeholder="Describe your current strategic bottlenecks, regulatory constraints, or legacy IT dependencies..."
                      value={contactFormData.objective}
                      onChange={(e) => setContactFormData({ ...contactFormData, objective: e.target.value })}
                      className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors resize-none font-medium ${
                        isLight 
                          ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner' 
                          : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner'
                      }`}
                    />
                  </div>

                  <div className="pt-2">
                    <button
                      type="submit"
                      className="w-full py-3.5 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs tracking-widest transition-all flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-orange-500/25 active:scale-98"
                    >
                      <span>Submit Confidential Executive Request</span>
                      <Send className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </form>
              )}
            </div>
          </div>

        </div>
      </section>

      {/* FOOTER: Minimalist Editorial Signoff */}
      <footer className={`py-12 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono ${
        isLight ? 'border-slate-200 text-slate-700' : 'border-white/15 text-zinc-300'
      }`}>
        <div>
          © {new Date().getFullYear()} LIGHTSPEED HOLDINGS LIMITED. All rights reserved. Sovereign AI Transformation.
        </div>
        <div className={`flex items-center gap-4 ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
          <a href="#operating-model" className="hover:text-orange-500 font-medium">Model</a>
          <a href="#capabilities" className="hover:text-orange-500 font-medium">Capabilities</a>
          <a href="#diagnostic" className="hover:text-orange-500 font-medium">Diagnostic</a>
          <a href="#templates" className="hover:text-orange-500 font-medium">Templates</a>
          <a href="#publications" className="hover:text-orange-500 font-medium">Publications</a>
          <a href="#faq" className="hover:text-orange-500 font-medium">FAQ</a>
          <a href="#contact" className="hover:text-orange-500 font-medium">Contact</a>
        </div>
      </footer>

    </div>
  );
};
