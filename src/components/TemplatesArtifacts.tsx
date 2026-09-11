import React, { useState, useEffect } from 'react';
import { 
  FileCheck, 
  Download, 
  Eye, 
  Layers, 
  ShieldCheck, 
  Cpu, 
  Database, 
  Sparkles, 
  Lock, 
  ArrowRight, 
  Terminal, 
  CheckCircle2, 
  Sliders, 
  RotateCcw,
  Maximize2,
  X,
  Copy,
  Check
} from 'lucide-react';

interface TemplatesArtifactsProps {
  onRequestBriefing: (summary?: string) => void;
  theme?: 'light' | 'dark';
}

export interface ArtifactTemplate {
  id: string;
  title: string;
  category: 'strategy' | 'architecture' | 'agents' | 'deployment';
  categoryLabel: string;
  format: 'YAML' | 'JSON' | 'REGO' | 'TERRAFORM' | 'PDF';
  stageTimeline: string;
  portType: 'RJ45_MESH' | 'USBC_CRYPTO' | 'RS232_POLICY' | 'SFP_OPTICAL' | 'DB25_MAINFRAME';
  portLabel: string;
  purpose: string;
  problemSolved: string;
  highlights: string[];
  sampleSnippet: string;
  sha256: string;
}

export const ARTIFACTS_CATALOG: ArtifactTemplate[] = [
  // 01. Strategy & Board
  {
    id: 'art-strat-01',
    title: '2-Week Executive Advisory & Capital Allocation Matrix',
    category: 'strategy',
    categoryLabel: 'Board & Strategy',
    format: 'PDF',
    stageTimeline: 'Week 01 - 02 (Advisory Sprint)',
    portType: 'USBC_CRYPTO',
    portLabel: 'USB-C / HSM Key Port',
    purpose: 'Aligns C-suite stakeholders with computable ROI metrics and Capex/Opex models before capital is committed.',
    problemSolved: 'Eliminates 6-month consulting deck paralysis and quantifies real unit economics against traditional SaaS lock-in.',
    highlights: [
      'Multi-year Net Sovereign Value (NSV) financial model',
      'Air-gap compute infrastructure TCO vs Cloud API pricing',
      'Board-ready fiduciary liability and governance charter'
    ],
    sampleSnippet: `# EXECUTIVE CAPITAL ALLOCATION SPECIFICATION
sovereign_transformation:
  engagement_model: "2-Week Executive Advisory Sprint"
  capex_allocation:
    on_prem_inference_cluster: "$1,250,000"
    internal_mesh_fabric: "$340,000"
  opex_displacement:
    legacy_saas_reduction_annual: "$2,850,000"
    projected_payback_period_months: 8.4
  fiduciary_signoff:
    risk_committee_status: "APPROVED_WITH_HITL_GATE"
    regulatory_framework: "SADC_BANKING_ACT_SEC_48"`,
    sha256: '9f8e7d6c5b4a39201f8e7d6c5b4a39201f8e7d6c5b4a39201f8e7d6c5b4a3920'
  },
  {
    id: 'art-strat-02',
    title: 'Fiduciary Board AI Governance Charter & Audit Matrix',
    category: 'strategy',
    categoryLabel: 'Board & Strategy',
    format: 'REGO',
    stageTimeline: 'Week 02 (Advisory Sprint)',
    portType: 'RS232_POLICY',
    portLabel: 'RS-232 / Policy Diagnostic Header',
    purpose: 'Establishes clear legal, operational, and ethical accountability structures for autonomous decision engines.',
    problemSolved: 'Provides immutable auditability to satisfy bank regulators, central bank directives, and risk committees.',
    highlights: [
      'Executive signing authority rules by financial threshold',
      'Automated kill-switch and fail-safe triggers',
      'Statutory compliance mapping for sovereign jurisdictions'
    ],
    sampleSnippet: `package lightspeed.fiduciary.governance

default allow = false

# Gate 1: Financial Settlement Threshold
allow {
    input.action.type == "SETTLEMENT_TRANSACTION"
    input.action.amount_usd <= 250000
    input.agent.clearance_level == "LEVEL_3_FINANCIAL"
    input.cryptographic_signature_valid == true
}

# Gate 2: High-Value Requires Multi-Party HITL Confirmation
allow {
    input.action.type == "SETTLEMENT_TRANSACTION"
    input.action.amount_usd > 250000
    input.human_in_the_loop_approvals[_].role == "CHIEF_RISK_OFFICER"
    input.audit_log_hash_committed == true
}`,
    sha256: 'a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0'
  },

  // 02. Sovereign Architecture
  {
    id: 'art-arch-01',
    title: 'Air-Gapped On-Soil Inference Topology Blueprint',
    category: 'architecture',
    categoryLabel: 'Sovereign Architecture',
    format: 'TERRAFORM',
    stageTimeline: 'Month 01 (Pilot Phase)',
    portType: 'RJ45_MESH',
    portLabel: 'RJ-45 / Air-Gap Mesh Bus',
    purpose: 'Complete bare-metal and private-VPC infrastructure definitions for local model inference with zero external cloud egress.',
    problemSolved: 'Prevents intellectual property and banking ledger leaks through unauthorized third-party LLM endpoints.',
    highlights: [
      'Zero-Trust physical network isolation rules',
      'Dual-redundant inference cluster configuration',
      'Hardware security module (HSM) key store integration'
    ],
    sampleSnippet: `module "sovereign_inference_cluster" {
  source = "./modules/airgap_hpc"
  
  cluster_name         = "ls-sovereign-node-01"
  data_residency_zone  = "SOIL_ZONE_PRIMARY"
  egress_policy        = "STRICT_BLOCK_ALL_PUBLIC_INTERNET"
  
  accelerator_nodes = {
    count            = 8
    chipset          = "NVIDIA_H100_SXM5_80GB"
    interconnect     = "INFINIBAND_NDR_400GB"
  }
  
  hsm_vault_endpoint = "hsm://internal-mesh.sovereign.local"
  audit_telemetry_port = 8420
}`,
    sha256: 'c3d4e5f6a1b27890c3d4e5f6a1b27890c3d4e5f6a1b27890c3d4e5f6a1b27890'
  },
  {
    id: 'art-arch-02',
    title: 'Enterprise Knowledge Graph & Semantic Fabric Schema',
    category: 'architecture',
    categoryLabel: 'Sovereign Architecture',
    format: 'JSON',
    stageTimeline: 'Month 01 (Pilot Phase)',
    portType: 'SFP_OPTICAL',
    portLabel: 'SFP+ / High-Speed Optical Bus',
    purpose: 'Transforms fragmented enterprise databases, PDF archives, and transactional logs into a unified computable ontology.',
    problemSolved: 'Eliminates the "Silo Tax" where critical operational truth is locked across legacy departments.',
    highlights: [
      'Temporal entity relationship schema with bidirectional tracking',
      'Real-time vector indexing with cryptographic access controls',
      'Mainframe relational-to-graph translation mappings'
    ],
    sampleSnippet: `{
  "$schema": "https://lightspeed.holdings/schemas/v2/semantic-fabric.json",
  "ontology": "SOVEREIGN_ENTERPRISE_CORE",
  "entities": {
    "TransactionSettlement": {
      "properties": {
        "settlementId": { "type": "string", "index": "primary" },
        "originatingAccount": { "type": "string", "securityClassification": "CONFIDENTIAL" },
        "destinationCorridor": { "type": "string", "enum": ["SADC_01", "EU_03", "APAC_02"] },
        "deterministicRiskScore": { "type": "number", "minimum": 0, "maximum": 1.0 }
      },
      "immutableAuditBinding": true
    }
  }
}`,
    sha256: 'e5f6a1b2c3d47890e5f6a1b2c3d47890e5f6a1b2c3d47890e5f6a1b2c3d47890'
  },

  // 03. Multi-Agent Fleets
  {
    id: 'art-agent-01',
    title: 'Deterministic Multi-Agent Fleet Specification & Tool Contract',
    category: 'agents',
    categoryLabel: 'Multi-Agent Fleets',
    format: 'YAML',
    stageTimeline: 'Month 02 (Pilot Phase)',
    portType: 'DB25_MAINFRAME',
    portLabel: 'DB-25 / Legacy Interconnect',
    purpose: 'Defines autonomous agent hierarchies, constrained tool permissions, and deterministic execution boundaries.',
    problemSolved: 'Eliminates model hallucination and unauthorized system mutations by enforcing strict mathematical parameters.',
    highlights: [
      'Granular read/edit/bash/execute tool contracts',
      'Subagent delegation topology and message bus queues',
      'Timeout, circuit breaker, and retry exponential backoffs'
    ],
    sampleSnippet: `agent:
  id: "settlement-recon-specialist"
  name: "Settlement Reconciliation Agent"
  role: "Reconcile high-volume cross-border batches against core ledger"
  mode: "subagent"
  permissions:
    allowed_tools:
      - "read_core_ledger_stream"
      - "compute_discrepancy_delta"
      - "stage_journal_entry"
    forbidden_tools:
      - "direct_ledger_write_without_gate"
      - "external_network_egress"
  circuit_breakers:
    max_batch_anomaly_pct: 0.05
    on_breach: "TRIGGER_HITL_PAUSE_AND_NOTIFY_COMPLIANCE"`,
    sha256: '7890123456789abcdef0123456789abcdef0123456789abcdef0123456789abcd'
  },
  {
    id: 'art-agent-02',
    title: 'Cryptographic Event Lineage & Audit Trail Protocol',
    category: 'agents',
    categoryLabel: 'Multi-Agent Fleets',
    format: 'JSON',
    stageTimeline: 'Month 02 (Pilot Phase)',
    portType: 'USBC_CRYPTO',
    portLabel: 'USB-C / HSM Key Port',
    purpose: 'Embeds tamper-proof cryptographic proofs into every autonomous decision and action taken across the agent fleet.',
    problemSolved: 'Guarantees 100% legal admissibility and non-repudiation during statutory regulatory inspections.',
    highlights: [
      'Merkle-tree anchored action hashing',
      'Timestamped hardware HSM key signatures',
      'Instant verification CLI tooling for compliance officers'
    ],
    sampleSnippet: `{
  "actionId": "ACT-8421-9920",
  "timestamp": "2026-09-09T20:14:22.842Z",
  "agentId": "settlement-recon-specialist",
  "toolInvoked": "stage_journal_entry",
  "parametersHash": "sha256:d41d8cd98f00b204e9800998ecf8427e",
  "merkleRootAnchor": "0x8f2a4c6e8b1d3f5a7c9e0b2d4f6a8c1e3b5d7f9a",
  "hsmSignature": "MEYCIQD1u2g3h4...verified",
  "fiduciaryStatus": "COMPLIANT_L3"
}`,
    sha256: '123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef01'
  },

  // 04. 90-Day Deployment
  {
    id: 'art-dep-01',
    title: 'Legacy Core Modernization Wrapper & API Event Gateway',
    category: 'deployment',
    categoryLabel: '90-Day Deployment',
    format: 'YAML',
    stageTimeline: 'Month 03 (Production Go-Live)',
    portType: 'DB25_MAINFRAME',
    portLabel: 'DB-25 / Legacy Interconnect',
    purpose: 'Bridges monolithic COBOL/mainframe banking engines with real-time autonomous event streams without risky rip-and-replace.',
    problemSolved: 'Reduces batch reconciliation latency from 24 hours to 450 milliseconds while safeguarding legacy integrity.',
    highlights: [
      'Bidirectional protocol translation (EBCDIC/SNA to JSON/Kafka)',
      'Sub-second deterministic state reconciliation',
      'Automated shadow-run verification testing mode'
    ],
    sampleSnippet: `legacy_gateway:
  upstream_mainframe:
    protocol: "IBM_SNA_LU6.2"
    target_host: "mframe-core.prod.bank.internal"
    character_encoding: "EBCDIC_CP037"
  downstream_mesh:
    event_bus: "SOVEREIGN_KAFKA_CLUSTER"
    topic: "settlements.reconciled.v1"
    target_latency_p99_ms: 350
  safety_harness:
    shadow_mode_enabled: true
    tolerance_threshold_bps: 0.001`,
    sha256: 'fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210'
  },
  {
    id: 'art-dep-02',
    title: 'Production SLA, High-Availability & Disaster Recovery Spec',
    category: 'deployment',
    categoryLabel: '90-Day Deployment',
    format: 'PDF',
    stageTimeline: 'Month 03 (Production Go-Live)',
    portType: 'RJ45_MESH',
    portLabel: 'RJ-45 / Air-Gap Mesh Bus',
    purpose: 'Legally binding operational guarantees for 99.999% uptime, deterministic latency, and local failover execution.',
    problemSolved: 'Ensures zero operational downtime during high-volume systemic volatility or external grid disruptions.',
    highlights: [
      'Sub-500ms regional settlement SLA guarantees',
      'Dual active-active regional data center synchronization',
      '24/7 dedicated engineering response escalation paths'
    ],
    sampleSnippet: `# PRODUCTION LEVEL SERVICE AGREEMENT & FAILOVER MATRIX
operational_parameters:
  availability_target: "99.999%"
  maximum_allowable_failover_rto_seconds: 12
  maximum_allowable_rpo_transactions: 0
infrastructure_redundancy:
  primary_site: "JOHANNESBURG_SOVEREIGN_TIER4"
  secondary_site: "CAPE_TOWN_AIRGAP_TIER4"
  replication_protocol: "SYNCHRONOUS_FIBER_MESH"`,
    sha256: '456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123'
  }
];

export const TemplatesArtifacts: React.FC<TemplatesArtifactsProps> = ({
  onRequestBriefing,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [selectedArtifact, setSelectedArtifact] = useState<ArtifactTemplate | null>(null);
  const [copiedCode, setCopiedCode] = useState(false);
  const [rotaryAngle, setRotaryAngle] = useState(0);

  useEffect(() => {
    if (selectedArtifact) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [selectedArtifact]);

  const categories = [
    { id: 'all', label: 'All Artifacts', angle: 0 },
    { id: 'strategy', label: 'Board & Strategy', angle: 45 },
    { id: 'architecture', label: 'Sovereign Arch', angle: 90 },
    { id: 'agents', label: 'Agent Fleets', angle: 135 },
    { id: 'deployment', label: '90-Day Deploy', angle: 180 },
  ];

  const handleCategorySelect = (catId: string, angle: number) => {
    setActiveCategory(catId);
    setRotaryAngle(angle);
  };

  const filteredArtifacts = activeCategory === 'all' 
    ? ARTIFACTS_CATALOG 
    : ARTIFACTS_CATALOG.filter(a => a.category === activeCategory);

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  return (
    <section id="templates" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t transition-colors duration-300 ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      {/* SECTION HEADER & EXPLICIT STATEMENT OF PURPOSE */}
      <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono font-bold tracking-widest bg-orange-500/10 text-orange-400 border border-orange-500/20">
          <Layers className="w-3.5 h-3.5" />
          <span>STANDARDIZED ARTIFACT LIBRARY</span>
        </div>
        
        <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          Sovereign Engagement Artifacts
        </h2>

        {/* Explicit Purpose Statement */}
        <div className={`p-6 rounded-2xl border text-left space-y-3 ${
          isLight ? 'bg-white/95 border-slate-300 shadow-sm' : 'bg-zinc-950/80 border-white/15 shadow-xl'
        }`}>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full tactile-pip-active" />
            <span className={`text-xs font-mono font-bold tracking-wider ${isLight ? 'text-slate-900' : 'text-orange-400'}`}>
              The Purpose of LightSpeed Templates & Specifications
            </span>
          </div>
          <p className={`text-justify text-justify text-sm leading-relaxed ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
            In enterprise AI transformation, theoretical slides produce 0% ROI. The <strong>LightSpeed Sovereign Artifact Library</strong> is our verified repository of computable blueprints, deterministic policy schemas, air-gapped hardware topologies, and governance protocols. Every template is an actionable, production-ready deliverable engineered to de-risk executive decision-making and ensure verifiable compliance across your organization’s infrastructure.
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 border-t border-white/10 text-[11px] font-mono">
            <div className="flex flex-col">
              <span className="text-orange-400 font-bold">4 CATEGORIES</span>
              <span className={isLight ? 'text-slate-700 font-semibold' : 'text-zinc-300'}>Advisory to Go-Live</span>
            </div>
            <div className="flex flex-col">
              <span className="text-orange-400 font-bold">100% CODE-BACKED</span>
              <span className={isLight ? 'text-slate-700 font-semibold' : 'text-zinc-300'}>YAML, JSON, Rego, TF</span>
            </div>
            <div className="flex flex-col">
              <span className="text-orange-400 font-bold">ZERO SAAS LEAK</span>
              <span className={isLight ? 'text-slate-700 font-semibold' : 'text-zinc-300'}>Air-Gapped Sovereignty</span>
            </div>
            <div className="flex flex-col">
              <span className="text-orange-400 font-bold">AUDIT-PROVEN</span>
              <span className={isLight ? 'text-slate-700 font-semibold' : 'text-zinc-300'}>Cryptographic Lineage</span>
            </div>
          </div>
        </div>
      </div>

      {/* ANALOG HARDWARE FILTER CONSOLE (Rotary Selector & Tactile Push Matrix) */}
      <div className={`mb-12 p-6 rounded-3xl border ${
        isLight ? 'analog-port-plate-light border-slate-300' : 'analog-port-plate-dark border-white/15'
      }`}>
        <div className="flex flex-col lg:flex-row items-center justify-between gap-6">
          
          {/* Left: Analog Rotary Selector Simulation */}
          <div className="flex items-center gap-5">
            <div className="relative flex items-center justify-center">
              {/* Rotary Dial Outer Bezel */}
              <div className={`w-16 h-16 rounded-full flex items-center justify-center p-1.5 ${
                isLight ? 'analog-rotary-dial-light' : 'analog-rotary-dial-dark'
              }`}>
                {/* Pointer Notch */}
                <div 
                  className="w-full h-full rounded-full relative flex items-start justify-center transition-transform duration-300 ease-out"
                  style={{ transform: `rotate(${rotaryAngle}deg)` }}
                >
                  <div className="w-1 h-3.5 bg-orange-500 rounded-full shadow-sm" />
                </div>
              </div>
              {/* Dial Tick Marks */}
              <div className="absolute inset-0 -m-2 pointer-events-none flex items-center justify-center">
                <div className="w-20 h-20 rounded-full border border-dashed border-orange-500/30" />
              </div>
            </div>

            <div className="flex flex-col">
              <span className="text-xs font-mono font-bold tracking-wider text-orange-400 flex items-center gap-1.5">
                <span>DOMAIN SELECTOR</span>
                <span className="w-1.5 h-1.5 rounded-full tactile-pip-active" />
              </span>
              <span className={`text-[11px] font-mono ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                Active Filter: <strong className={isLight ? 'text-slate-900' : 'text-zinc-100'}>{categories.find(c => c.id === activeCategory)?.label}</strong>
              </span>
            </div>
          </div>

          {/* Right: Tactile Push-Key Buttons */}
          <div className={`flex flex-wrap p-1.5 rounded-2xl gap-2 ${
            isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'
          }`}>
            {categories.map((cat) => {
              const isSelected = activeCategory === cat.id;
              return (
                <button
                  key={cat.id}
                  onClick={() => handleCategorySelect(cat.id, cat.angle)}
                  className={`px-4 py-2 rounded-xl text-xs font-mono font-bold tracking-wider transition-all duration-200 cursor-pointer flex items-center gap-2 ${
                    isSelected
                      ? isLight ? 'tactile-btn-active-light text-slate-900 border-orange-500/50' : 'tactile-btn-active-dark text-white border-orange-500/50'
                      : isLight ? 'tactile-btn-inactive-light text-slate-800' : 'tactile-btn-inactive-dark text-zinc-300'
                  }`}
                >
                  <span className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    isSelected ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                  }`} />
                  <span>{cat.label}</span>
                </button>
              );
            })}
          </div>

        </div>
      </div>

      {/* ARTIFACTS GRID (Featuring Analog Hardware Interface Ports) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredArtifacts.map((artifact) => {
          return (
            <div
              key={artifact.id}
              className={`p-6 sm:p-7 rounded-3xl border transition-all duration-300 flex flex-col justify-between relative group ${
                isLight ? 'bg-white/95 border-slate-300 hover:border-orange-500/50 shadow-md' : 'bg-zinc-950/80 border-white/15 hover:border-orange-500/50 shadow-xl'
              }`}
            >
              {/* Top Meta: Format Pill + Timeline */}
              <div className="flex items-center justify-between gap-2 mb-4">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-1 rounded-md text-[10px] font-mono font-black tracking-wider bg-orange-500/10 text-orange-400 border border-orange-500/30">
                    {artifact.format}
                  </span>
                  <span className="text-[11px] font-mono font-medium text-[#2D3748]">
                    {artifact.stageTimeline}
                  </span>
                </div>

                {/* Screw Head Accents */}
                <div className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full analog-screw" />
                  <span className="w-2.5 h-2.5 rounded-full analog-screw" />
                </div>
              </div>

              {/* Title & Purpose */}
              <div className="space-y-2.5 mb-6">
                <h3 className={`text-lg sm:text-xl font-bold tracking-tight leading-snug ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  {artifact.title}
                </h3>
                <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                  {artifact.purpose}
                </p>
              </div>

              {/* Problem Solved Badge */}
              <div className={`p-3 rounded-xl mb-6 text-xs font-mono border ${
                isLight ? 'bg-slate-100 border-slate-300 text-slate-800' : 'bg-zinc-900/60 border-white/10 text-zinc-300'
              }`}>
                <span className="text-orange-400 font-bold block mb-1 text-[10px]">Challenge Overcome:</span>
                <span>{artifact.problemSolved}</span>
              </div>

              {/* Highlights Checklist */}
              <div className="space-y-2 mb-6 text-xs">
                {artifact.highlights.map((hl, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-orange-400 shrink-0 mt-0.5" />
                    <span className={isLight ? 'text-slate-800 font-medium' : 'text-zinc-300 font-medium'}>{hl}</span>
                  </div>
                ))}
              </div>

              {/* Bottom Actions (Tactile Audio Transport Style Buttons) */}
              <div className="flex items-center gap-3 pt-4 border-t border-white/10">
                <button
                  onClick={() => setSelectedArtifact(artifact)}
                  className={`flex-1 py-2.5 px-3 rounded-xl text-xs font-mono font-bold tracking-wider transition-all duration-200 cursor-pointer flex items-center justify-center gap-2 ${
                    isLight ? 'tactile-btn-inactive-light text-slate-800' : 'tactile-btn-inactive-dark text-zinc-100'
                  }`}
                >
                  <Eye className="w-3.5 h-3.5 text-orange-400" />
                  <span>Inspect Spec</span>
                </button>

                <button
                  onClick={() => onRequestBriefing(`Requesting technical specification & deployment preview for: ${artifact.title}`)}
                  className="flex-1 py-2.5 px-3 rounded-xl text-xs font-mono font-bold tracking-wider bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-md shadow-orange-500/25 transition-all cursor-pointer flex items-center justify-center gap-2"
                >
                  <span>Request Spec</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

            </div>
          );
        })}
      </div>

      {/* DETAILED SPEC INSPECTION MODAL (Realistic Hardware Terminal Inspector) */}
      {selectedArtifact && (
        <div className="fixed inset-0 z-[1000] flex items-center justify-center p-4 pt-16 sm:pt-20 bg-black/80 backdrop-blur-md animate-in fade-in duration-200 overflow-y-auto">
          <div className={`w-full max-w-3xl rounded-3xl border p-6 sm:p-8 max-h-[90vh] overflow-y-auto flex flex-col justify-between space-y-6 relative ${
            isLight ? 'bg-white border-slate-300 text-slate-800 shadow-2xl' : 'bg-zinc-950 border-white/20 text-zinc-100 shadow-2xl'
          }`}>
            
            {/* Modal Header */}
            <div className="flex items-start justify-between gap-4 pb-4 border-b border-white/10 relative z-10">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full tactile-pip-active" />
                  <span className="text-xs font-mono font-bold tracking-widest text-orange-400">
                    SPECIFICATION INSPECTOR // {selectedArtifact.format}
                  </span>
                </div>
                <h3 className={`text-xl sm:text-2xl font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  {selectedArtifact.title}
                </h3>
                <span className="text-xs font-mono text-[#2D3748]">
                  SHA-256 Digest: {selectedArtifact.sha256.substring(0, 32)}...
                </span>
              </div>

              <button
                onClick={() => setSelectedArtifact(null)}
                type="button"
                aria-label="Close modal"
                title="Close modal"
                className={`relative z-50 p-2 rounded-full border transition-all cursor-pointer shrink-0 ${
                  isLight ? 'tactile-btn-inactive-light text-slate-800 hover:bg-slate-200' : 'tactile-btn-inactive-dark text-zinc-300 hover:bg-zinc-800'
                }`}
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Code / Schema View */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs font-mono text-[#2D3748]">
                <span className="flex items-center gap-1.5">
                  <Terminal className="w-3.5 h-3.5 text-orange-400" />
                  <span>EXECUTABLE SPECIFICATION PREVIEW</span>
                </span>
                <button
                  onClick={() => handleCopy(selectedArtifact.sampleSnippet)}
                  className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] font-mono transition-all cursor-pointer ${
                    isLight ? 'bg-slate-100 hover:bg-slate-200 text-slate-700' : 'bg-zinc-900 hover:bg-zinc-800 text-zinc-300'
                  }`}
                >
                  {copiedCode ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedCode ? 'Copied' : 'Copy Code'}</span>
                </button>
              </div>

              <pre className="p-4 rounded-2xl bg-zinc-900 text-zinc-200 font-mono text-xs overflow-x-auto border border-white/10 leading-relaxed shadow-inner max-h-72">
                <code>{selectedArtifact.sampleSnippet}</code>
              </pre>
            </div>

            {/* Summary Highlights */}
            <div className={`p-4 rounded-2xl border space-y-2 ${
              isLight ? 'bg-slate-50 border-slate-200' : 'bg-zinc-900/50 border-white/10'
            }`}>
              <span className="text-xs font-mono font-bold text-orange-400 block">
                Deliverable Guarantees & Verification:
              </span>
              <ul className="space-y-1.5 text-xs">
                {selectedArtifact.highlights.map((hl, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                    <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>{hl}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Modal Bottom CTA */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-4 border-t border-white/10">
              <span className={`text-xs font-mono ${isLight ? 'text-slate-500' : 'text-zinc-500'}`}>
                Full artifact bundle includes test suite, deployment terraform & compliance signoff.
              </span>
              <button
                onClick={() => {
                  setSelectedArtifact(null);
                  onRequestBriefing(`Requesting full artifact access and co-engineering briefing for: ${selectedArtifact.title}`);
                }}
                className="w-full sm:w-auto py-2.5 px-6 rounded-xl font-mono font-bold text-xs tracking-wider bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-md shadow-orange-500/25 transition-all cursor-pointer flex items-center justify-center gap-2"
              >
                <span>Request Full Bundle</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>

          </div>
        </div>
      )}

    </section>
  );
};
