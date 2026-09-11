import React, { useState } from 'react';
import { 
  Building2, 
  Coins, 
  Globe2, 
  Zap, 
  ShieldCheck, 
  ArrowRight, 
  Sparkles, 
  CheckCircle2, 
  AlertCircle, 
  FileText,
  Clock,
  Layers,
  BarChart3,
  Cpu,
  Lock,
  Activity
} from 'lucide-react';

interface DiagnosticProps {
  theme?: 'light' | 'dark';
  onRequestBriefing: (diagnosticSummary?: string) => void;
}

interface SectorProfile {
  id: string;
  name: string;
  icon: React.ElementType;
  defaultFocus: string;
  pillar1Label: string;
  pillar1Range: [string, string];
  pillar2Label: string;
  pillar2Range: [string, string];
  pillar3Label: string;
  pillar3Range: [string, string];
  pillar4Label: string;
  pillar4Range: [string, string];
  complianceFramework: string;
  keyLatency: string;
  multiplier: string;
  bottlenecks: (scores: { strategy: number; data: number; auto: number; gov: number }) => {
    iconType: 'alert' | 'check' | 'warning';
    text: string;
    highlight: string;
  }[];
  customRecommendations: {
    tierLow: { title: string; desc: string };
    tierMid: { title: string; desc: string };
    tierHigh: { title: string; desc: string };
  };
}

const SECTOR_PROFILES: SectorProfile[] = [
  {
    id: 'banking',
    name: 'Banking & Financial Services',
    icon: Coins,
    defaultFocus: 'Trade Finance, AML/KYC & Basel IV Compliance',
    pillar1Label: 'Algorithmic Risk & Policy Formulation',
    pillar1Range: ['Manual Credit Committees', 'Deterministic Policy-as-Code Engines'],
    pillar2Label: 'Private Core Ledger & Graph Fabric',
    pillar2Range: ['Fragmented Mainframe Extracts', 'Real-Time Graph & Vector Ledger'],
    pillar3Label: 'Autonomous Transaction & Agent Execution',
    pillar3Range: ['Manual SWIFT/KYC Validation', 'Deterministic Multi-Agent Settlement Swarms'],
    pillar4Label: 'Fiduciary Assurance & Regulatory Lineage',
    pillar4Range: ['Post-Facto Quarterly Audits', 'Continuous Cryptographic Audit Trails'],
    complianceFramework: 'Basel IV, SOC2 Type II, PCI-DSS, FATF Travel Rule',
    keyLatency: '7–11 months core release latency',
    multiplier: '18x transaction audit velocity',
    bottlenecks: (s) => [
      {
        iconType: s.strategy < 3 ? 'alert' : 'check',
        text: s.strategy < 3 
          ? 'Credit underwriting and trade finance exception handling suffer from manual reviews, creating '
          : 'Algorithmic risk policies are formalized with strong computable rules, achieving ',
        highlight: s.strategy < 3 ? '12-day turnaround friction' : 'sub-minute risk adjudication'
      },
      {
        iconType: s.auto < 3 ? 'alert' : 'check',
        text: s.auto < 3
          ? 'Cross-border AML/KYC document verification is bottlenecked in manual tiers, exposing '
          : 'Deterministic agent swarms triage 92% of SWIFT/ISO-20022 exceptions, delivering ',
        highlight: s.auto < 3 ? 'fiduciary risk & false positive overload' : 'zero-leakage continuous settlement'
      },
      {
        iconType: 'check',
        text: 'Immediate deployment of air-gapped sovereign intelligence yields ',
        highlight: '18x verification speedup with zero cloud data exfiltration'
      }
    ],
    customRecommendations: {
      tierLow: {
        title: '90-Day Sovereign Banking Sandboxing',
        desc: 'Architecture audit, on-prem knowledge ingestion, and air-gapped AML/KYC agent pilot.'
      },
      tierMid: {
        title: 'Core Ledger Multi-Agent Co-Engineering',
        desc: 'Integration of sovereign agent swarms for trade finance, SWIFT reconciliation, and automated regulatory reporting.'
      },
      tierHigh: {
        title: 'Full Autonomous Sovereign Financial Core',
        desc: 'Enterprise-wide deployment of self-healing multi-agent financial infrastructure with sub-second audit logging.'
      }
    }
  },
  {
    id: 'public',
    name: 'Public Sector & Revenue',
    icon: Building2,
    defaultFocus: 'Customs Valuation, Tax Graph & Sovereign Borders',
    pillar1Label: 'Legislative Mandate & Policy Formulation',
    pillar1Range: ['Static Statutory Gazettes', 'Dynamic Executable Statutory Rules'],
    pillar2Label: 'Sovereign Citizen & Customs Knowledge Graph',
    pillar2Range: ['Isolated Agency Silos', 'Unified National Semantic Data Fabric'],
    pillar3Label: 'Autonomous Customs & Audit Orchestration',
    pillar3Range: ['Manual Border Manifest Review', 'Real-Time Anomaly Detection Swarms'],
    pillar4Label: 'Sovereign Integrity & Anti-Corruption Controls',
    pillar4Range: ['Periodic Manual Inspection', 'Immutable Public Trust Provenance'],
    complianceFramework: 'WCO SAFE Framework, Sovereign Cloud Acts, ISO 27701',
    keyLatency: '14–18 months regulatory adaptation lag',
    multiplier: '24x tariff classification throughput',
    bottlenecks: (s) => [
      {
        iconType: s.data < 3 ? 'alert' : 'check',
        text: s.data < 3
          ? 'Cross-agency data fragmentation between Customs, Inland Revenue, and Central Registries creates '
          : 'Unified sovereign knowledge graph bridges inter-ministerial databases, delivering ',
        highlight: s.data < 3 ? '$120M+ uncollected revenue leakages' : 'real-time holistic trade oversight'
      },
      {
        iconType: s.auto < 3 ? 'alert' : 'check',
        text: s.auto < 3
          ? 'Border cargo declarations and import manifests undergo physical manual checks, causing '
          : 'Autonomous classification agents pre-screen shipping manifests, enabling ',
        highlight: s.auto < 3 ? '48-hour port congestion delays' : 'instant green-lane clearance'
      },
      {
        iconType: 'check',
        text: 'Implementation of Sovereign Open-Source Agent Frameworks delivers ',
        highlight: '100% data residency guarantee inside national boundaries'
      }
    ],
    customRecommendations: {
      tierLow: {
        title: 'National Sovereign AI Architecture Blueprint',
        desc: 'Cross-ministerial data governance assessment and air-gapped customs document analysis pilot.'
      },
      tierMid: {
        title: 'Autonomous Revenue & Customs Modernization',
        desc: 'Deploying tariff classification swarms and graph-based tax anomaly detection pipelines.'
      },
      tierHigh: {
        title: 'Full Sovereign National Intelligence Grid',
        desc: 'Multi-departmental sovereign agent mesh orchestrating fiscal enforcement and citizen services.'
      }
    }
  },
  {
    id: 'logistics',
    name: 'Supply Chain & Commodities',
    icon: Globe2,
    defaultFocus: 'Cross-Border Corridors & Port Terminal Automation',
    pillar1Label: 'Logistics Network Strategy & Dynamic Routing',
    pillar1Range: ['Fixed Quarterly Schedules', 'Continuous Autonomous Fleet Adaptation'],
    pillar2Label: 'Global Telemetry & Bill-of-Lading Knowledge Graph',
    pillar2Range: ['Scattered Paper Waybills', 'Live Multimodal Digital Twin'],
    pillar3Label: 'Autonomous Dispatch & Exception Swarms',
    pillar3Range: ['Phone & Email Expediting', 'Deterministic Multi-Carrier Agent Swarms'],
    pillar4Label: 'Chain-of-Custody & Trade Integrity Verification',
    pillar4Range: ['Paper Seals & Visual Check', 'Cryptographic IoT Sensor Provenance'],
    complianceFramework: 'IMO Maritime Cyber Risk, C-TPAT, ISO 28000',
    keyLatency: '5–8 days corridor paperwork dwell time',
    multiplier: '14x manifest reconciliation velocity',
    bottlenecks: (s) => [
      {
        iconType: s.auto < 3 ? 'alert' : 'check',
        text: s.auto < 3
          ? 'Disparate multi-modal freight forwarders and customs brokers communicate via unstructured PDF emails, driving '
          : 'Autonomous Bill-of-Lading parsing and reconciliation swarms achieve ',
        highlight: s.auto < 3 ? '8–14% margin decay in detention fees' : 'zero-touch clearance automation'
      },
      {
        iconType: s.strategy < 3 ? 'alert' : 'check',
        text: s.strategy < 3
          ? 'Route optimization and cold-chain compliance are reactive, triggering '
          : 'Continuous telemetry agents dynamically re-route cargo, securing ',
        highlight: s.auto < 3 ? 'spoilage risk and demurrage penalties' : '99.8% on-time corridor reliability'
      },
      {
        iconType: 'check',
        text: 'Edge-deployed multi-agent node architecture ensures ',
        highlight: 'offline operational continuity across remote transit hubs'
      }
    ],
    customRecommendations: {
      tierLow: {
        title: 'Corridor Logistics Intelligence Diagnostic',
        desc: 'End-to-end waybill workflow audit and automated multimodal document extraction pilot.'
      },
      tierMid: {
        title: 'Autonomous Freight & Port Dispatch Co-Engineering',
        desc: 'Deployment of exception-handling agent swarms integrated with existing TOS and ERP systems.'
      },
      tierHigh: {
        title: 'Global Sovereign Supply Chain Fabric',
        desc: 'Real-time digital twin and autonomous fleet orchestration across all land, sea, and rail corridors.'
      }
    }
  },
  {
    id: 'energy',
    name: 'Energy, Mining & Utilities',
    icon: Zap,
    defaultFocus: 'Autonomous Grid Balancing, SCADA & Extraction Telemetry',
    pillar1Label: 'Asset Strategy & Peak Load Balancing',
    pillar1Range: ['Manual Dispatch Runbooks', 'Real-Time Computable Grid Models'],
    pillar2Label: 'SCADA, IoT Sensor & Spatial Knowledge Graph',
    pillar2Range: ['Isolated Historian Databases', 'Deterministic OT/IT Semantic Layer'],
    pillar3Label: 'Autonomous Control Loop & Field Fleet Swarms',
    pillar3Range: ['100% Control-Room Manual Triage', 'Agentic Closed-Loop Telemetry Swarms'],
    pillar4Label: 'Industrial Safety & Environmental Lineage',
    pillar4Range: ['Periodic Incident Logs', 'Cryptographic Carbon & Safety Provenance'],
    complianceFramework: 'NERC CIP, IEC 62443, ISO 55001, ESG Scope 1-3 Audits',
    keyLatency: '3–6 weeks predictive maintenance dispatch lag',
    multiplier: '21x incident response and grid recovery rate',
    bottlenecks: (s) => [
      {
        iconType: s.gov < 3 ? 'alert' : 'check',
        text: s.gov < 3
          ? 'Critical SCADA telemetry is isolated in OT air-gaps without secure computable intelligence, leading to '
          : 'Air-gapped sovereign inference bridges OT/IT boundaries with zero exposure, achieving ',
        highlight: s.gov < 3 ? 'unplanned turbine and substation outages' : 'predictive fault isolation in <500ms'
      },
      {
        iconType: s.data < 3 ? 'alert' : 'check',
        text: s.data < 3
          ? 'Sensor historian logs and seismic geological surveys remain locked in proprietary formats, causing '
          : 'Unified spatial and time-series knowledge graph provides ',
        highlight: s.data < 3 ? 'blind spots in resource yield extraction' : 'real-time autonomous reservoir telemetry'
      },
      {
        iconType: 'check',
        text: 'Certified on-premise hardware appliances guarantee ',
        highlight: 'FIPS 140-3 and NERC CIP compliance with zero public cloud ingress'
      }
    ],
    customRecommendations: {
      tierLow: {
        title: 'Industrial OT AI Safety & SCADA Audit',
        desc: 'Air-gapped security validation and predictive asset maintenance proof-of-value.'
      },
      tierMid: {
        title: 'Autonomous Grid Telemetry & Maintenance Co-Engineering',
        desc: 'Integration of closed-loop diagnostic agents with plant historian databases and dispatch control.'
      },
      tierHigh: {
        title: 'Autonomous Sovereign Utility & Resource Grid',
        desc: 'Enterprise-wide intelligent power balancing, predictive extraction agents, and real-time ESG lineage.'
      }
    }
  }
];

export const TransformationDiagnostic: React.FC<DiagnosticProps> = ({
  theme = 'dark',
  onRequestBriefing
}) => {
  const [selectedSector, setSelectedSector] = useState(SECTOR_PROFILES[0].id);
  const [strategyScore, setStrategyScore] = useState<number>(2); // 1 to 4
  const [dataScore, setDataScore] = useState<number>(2);
  const [automationScore, setAutomationScore] = useState<number>(1);
  const [governanceScore, setGovernanceScore] = useState<number>(2);

  const isLight = theme === 'light';

  // Get active sector profile
  const activeProfile = SECTOR_PROFILES.find(p => p.id === selectedSector) || SECTOR_PROFILES[0];

  // Compute readiness index
  const totalScore = strategyScore + dataScore + automationScore + governanceScore;
  const percentage = Math.round((totalScore / 16) * 100);

  const getTier = () => {
    if (percentage < 40) {
      return { 
        title: 'Fragmented Legacy Core', 
        color: isLight ? 'text-amber-600' : 'text-amber-400', 
        reco: activeProfile.customRecommendations.tierLow.title,
        desc: activeProfile.customRecommendations.tierLow.desc
      };
    }
    if (percentage < 75) {
      return { 
        title: 'Emerging Automation Silo', 
        color: isLight ? 'text-orange-600' : 'text-orange-400', 
        reco: activeProfile.customRecommendations.tierMid.title,
        desc: activeProfile.customRecommendations.tierMid.desc
      };
    }
    return { 
      title: 'AI-Native Scaling Candidate', 
      color: isLight ? 'text-emerald-600' : 'text-emerald-400', 
      reco: activeProfile.customRecommendations.tierHigh.title,
      desc: activeProfile.customRecommendations.tierHigh.desc
    };
  };

  const tier = getTier();
  const bottlenecks = activeProfile.bottlenecks({
    strategy: strategyScore,
    data: dataScore,
    auto: automationScore,
    gov: governanceScore
  });

  const handleBooking = () => {
    const summary = `Sector: ${activeProfile.name.toUpperCase()}, AI-Readiness: ${percentage}%, Tier: ${tier.title}, Recommended: ${tier.reco}, Framework: ${activeProfile.complianceFramework}`;
    onRequestBriefing(summary);
  };

  return (
    <div className={`p-6 sm:p-10 rounded-3xl border relative overflow-hidden transition-all duration-300 ${
      isLight 
        ? 'bg-white/95 border-slate-300 shadow-2xl text-slate-800' 
        : 'bg-zinc-950/90 border-white/15 shadow-2xl text-zinc-200'
    }`}>
      {/* Background grain */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.03] bg-grain" />

      {/* Analog Hardware Bezel Screws */}
      <div className="absolute top-3 left-3 w-3 h-3 rounded-full analog-screw hidden sm:block" />
      <div className="absolute top-3 right-3 w-3 h-3 rounded-full analog-screw hidden sm:block" />
      <div className="absolute bottom-3 left-3 w-3 h-3 rounded-full analog-screw hidden sm:block" />
      <div className="absolute bottom-3 right-3 w-3 h-3 rounded-full analog-screw hidden sm:block" />

      {/* Top Analog Hardware I/O Port Interface Strip (Clutter-free, no connector name labels) */}
      <div className={`mb-8 p-3 rounded-2xl border flex flex-wrap items-center justify-between gap-4 ${
        isLight ? 'analog-port-plate-light border-slate-300' : 'analog-port-plate-dark border-white/15'
      }`}>
        <div className="flex items-center gap-4">
          {/* RJ-45 Hardware Port Cavity with active link LED */}
          <div className="w-8 h-6 rounded-md analog-port-cavity flex items-center justify-center p-1">
            <div className="flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_6px_rgba(52,211,153,0.9)]" />
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
            </div>
          </div>

          {/* USB-C Port Cavity */}
          <div className="w-7 h-3 rounded-full analog-port-cavity flex items-center justify-center">
            <span className="w-3 h-0.5 bg-amber-400/80 rounded-xs" />
          </div>

          {/* 3.5mm Color-Coded Analog Telemetry Jacks */}
          <div className="hidden sm:flex items-center gap-1.5 border-l border-white/10 pl-3">
            <div className="w-3.5 h-3.5 rounded-full border-2 border-rose-400 bg-black flex items-center justify-center shadow-xs">
              <div className="w-1 h-1 rounded-full bg-black" />
            </div>
            <div className="w-3.5 h-3.5 rounded-full border-2 border-cyan-400 bg-black flex items-center justify-center shadow-xs">
              <div className="w-1 h-1 rounded-full bg-black" />
            </div>
            <div className="w-3.5 h-3.5 rounded-full border-2 border-lime-400 bg-black flex items-center justify-center shadow-xs">
              <div className="w-1 h-1 rounded-full bg-black" />
            </div>
          </div>
        </div>

        {/* Digital Calibration Matrix Badge */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-black/60 border border-white/10 text-[10px] font-mono">
            <span className="text-zinc-400">CLK:</span>
            <span className="text-orange-400 font-bold">144.00 MHz</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full tactile-pip-active" />
            <span className={`text-[10px] font-mono font-bold ${isLight ? 'text-emerald-700' : 'text-emerald-400'}`}>
              CALIBRATED
            </span>
          </div>
        </div>
      </div>

      {/* Header */}
      <div className="max-w-3xl mb-8 space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-400 font-mono text-[11px] tracking-widest">
          <Sparkles className="w-3.5 h-3.5" />
          <span>EXECUTIVE READINESS ASSESSMENT</span>
        </div>
        <h3 className={`text-2xl sm:text-4xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          AI Transformation Diagnostic
        </h3>
        <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          Calibrate institutional maturity across four deterministic pillars. All findings, benchmarks, failure mode models, and remediation blueprints dynamically reconfigure based on your selected industry vertical.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start relative z-10">
        
        {/* Left Side: Assessment Controls (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          
          {/* Step 1: Industry Sector Selector */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className={`block text-xs font-mono tracking-wider font-bold ${
                isLight ? 'text-slate-800' : 'text-zinc-300'
              }`}>
                01. Select Institutional Sector
              </label>
              <span className={`text-[11px] font-mono ${isLight ? 'text-slate-600 font-semibold' : 'text-orange-400'}`}>
                Active: {activeProfile.defaultFocus}
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              {SECTOR_PROFILES.map((s) => {
                const Icon = s.icon;
                const active = selectedSector === s.id;
                return (
                  <button
                    key={s.id}
                    onClick={() => setSelectedSector(s.id)}
                    className={`p-3.5 rounded-2xl text-left transition-all duration-200 cursor-pointer flex flex-col justify-between gap-3 relative overflow-hidden ${
                      active
                        ? isLight
                          ? 'tactile-btn-active-light text-slate-900 border-orange-500/50'
                          : 'tactile-btn-active-dark text-white border-orange-500/50'
                        : isLight 
                          ? 'tactile-btn-inactive-light text-slate-800 border-slate-300' 
                          : 'tactile-btn-inactive-dark text-zinc-300'
                    }`}
                  >
                    <div className="flex items-center justify-between w-full">
                      <Icon className={`w-4 h-4 ${active ? 'text-orange-400' : 'text-orange-500'}`} />
                      {/* Realistic Hardware LED Indicator Pip */}
                      <span className={`w-2 h-2 rounded-full transition-all duration-300 ${
                        active ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                      }`} />
                    </div>
                    <span className="text-xs font-bold leading-tight line-clamp-2">{s.name}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Step 2: 4 Core Pillar Assessment Steppers */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className={`block text-xs font-mono tracking-wider font-bold ${
                isLight ? 'text-slate-800' : 'text-zinc-300'
              }`}>
                02. Assess Organizational Maturity ({activeProfile.name})
              </label>
              {/* Speaker Grille Accent */}
              <div className="hidden sm:flex items-center gap-1">
                {[...Array(6)].map((_, i) => (
                  <span key={i} className="w-1.5 h-1.5 rounded-full tactile-grille-dot" />
                ))}
              </div>
            </div>

            {/* Pillar 1: Strategy Formulation */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'bg-slate-50 border-slate-300' : 'bg-zinc-900/70 border-white/15'
            }`}>
              <div className="flex items-center justify-between text-xs mb-3">
                <span className={`font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  {activeProfile.pillar1Label}
                </span>
                <div className="flex items-center gap-1.5">
                  <span className={`w-1.5 h-1.5 rounded-full ${strategyScore > 1 ? 'tactile-pip-active' : 'tactile-pip-inactive-dark'}`} />
                  <span className="font-mono text-orange-400 font-bold text-[11px]">Level {strategyScore} / 4</span>
                </div>
              </div>
              
              {/* Realistic Hardware Radio Well */}
              <div className={`flex w-full p-1.5 rounded-2xl gap-1.5 ${isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'}`}>
                {[1, 2, 3, 4].map((level) => {
                  const isSelected = strategyScore === level;
                  return (
                    <button
                      key={level}
                      onClick={() => setStrategyScore(level)}
                      className={`flex-1 py-2 px-2 rounded-xl text-center transition-all duration-200 cursor-pointer flex flex-col items-center justify-center gap-1.5 relative ${
                        isSelected
                          ? isLight ? 'tactile-btn-active-light text-slate-900' : 'tactile-btn-active-dark text-white'
                          : isLight ? 'tactile-btn-inactive-light text-slate-800' : 'tactile-btn-inactive-dark text-zinc-300'
                      }`}
                    >
                      <div className="flex items-center gap-1">
                        <span className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                          isSelected ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                        }`} />
                        <span className="text-xs font-mono font-bold">L{level}</span>
                      </div>
                    </button>
                  );
                })}
              </div>
              <div className="flex justify-between text-[11px] font-mono font-medium mt-2 text-[#2D3748]">
                <span>{activeProfile.pillar1Range[0]}</span>
                <span>{activeProfile.pillar1Range[1]}</span>
              </div>
            </div>

            {/* Pillar 2: Private Data & Knowledge Fabric */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'bg-slate-50 border-slate-300' : 'bg-zinc-900/70 border-white/15'
            }`}>
              <div className="flex items-center justify-between text-xs mb-3">
                <span className={`font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  {activeProfile.pillar2Label}
                </span>
                <div className="flex items-center gap-1.5">
                  <span className={`w-1.5 h-1.5 rounded-full ${dataScore > 1 ? 'tactile-pip-active' : 'tactile-pip-inactive-dark'}`} />
                  <span className="font-mono text-orange-400 font-bold text-[11px]">Level {dataScore} / 4</span>
                </div>
              </div>
              
              {/* Realistic Hardware Radio Well */}
              <div className={`flex w-full p-1.5 rounded-2xl gap-1.5 ${isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'}`}>
                {[1, 2, 3, 4].map((level) => {
                  const isSelected = dataScore === level;
                  return (
                    <button
                      key={level}
                      onClick={() => setDataScore(level)}
                      className={`flex-1 py-2 px-2 rounded-xl text-center transition-all duration-200 cursor-pointer flex flex-col items-center justify-center gap-1.5 relative ${
                        isSelected
                          ? isLight ? 'tactile-btn-active-light text-slate-900' : 'tactile-btn-active-dark text-white'
                          : isLight ? 'tactile-btn-inactive-light text-slate-800' : 'tactile-btn-inactive-dark text-zinc-300'
                      }`}
                    >
                      <div className="flex items-center gap-1">
                        <span className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                          isSelected ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                        }`} />
                        <span className="text-xs font-mono font-bold">L{level}</span>
                      </div>
                    </button>
                  );
                })}
              </div>
              <div className="flex justify-between text-[11px] font-mono font-medium mt-2 text-[#2D3748]">
                <span>{activeProfile.pillar2Range[0]}</span>
                <span>{activeProfile.pillar2Range[1]}</span>
              </div>
            </div>

            {/* Pillar 3: Multi-Agent Automation */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'bg-slate-50 border-slate-300' : 'bg-zinc-900/70 border-white/15'
            }`}>
              <div className="flex items-center justify-between text-xs mb-3">
                <span className={`font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  {activeProfile.pillar3Label}
                </span>
                <div className="flex items-center gap-1.5">
                  <span className={`w-1.5 h-1.5 rounded-full ${automationScore > 1 ? 'tactile-pip-active' : 'tactile-pip-inactive-dark'}`} />
                  <span className="font-mono text-orange-400 font-bold text-[11px]">Level {automationScore} / 4</span>
                </div>
              </div>
              
              {/* Realistic Hardware Radio Well */}
              <div className={`flex w-full p-1.5 rounded-2xl gap-1.5 ${isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'}`}>
                {[1, 2, 3, 4].map((level) => {
                  const isSelected = automationScore === level;
                  return (
                    <button
                      key={level}
                      onClick={() => setAutomationScore(level)}
                      className={`flex-1 py-2 px-2 rounded-xl text-center transition-all duration-200 cursor-pointer flex flex-col items-center justify-center gap-1.5 relative ${
                        isSelected
                          ? isLight ? 'tactile-btn-active-light text-slate-900' : 'tactile-btn-active-dark text-white'
                          : isLight ? 'tactile-btn-inactive-light text-slate-800' : 'tactile-btn-inactive-dark text-zinc-300'
                      }`}
                    >
                      <div className="flex items-center gap-1">
                        <span className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                          isSelected ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                        }`} />
                        <span className="text-xs font-mono font-bold">L{level}</span>
                      </div>
                    </button>
                  );
                })}
              </div>
              <div className="flex justify-between text-[11px] font-mono font-medium mt-2 text-[#2D3748]">
                <span>{activeProfile.pillar3Range[0]}</span>
                <span>{activeProfile.pillar3Range[1]}</span>
              </div>
            </div>

            {/* Pillar 4: Fiduciary & Governance Controls */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'bg-slate-50 border-slate-300' : 'bg-zinc-900/70 border-white/15'
            }`}>
              <div className="flex items-center justify-between text-xs mb-3">
                <span className={`font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  {activeProfile.pillar4Label}
                </span>
                <div className="flex items-center gap-1.5">
                  <span className={`w-1.5 h-1.5 rounded-full ${governanceScore > 1 ? 'tactile-pip-active' : 'tactile-pip-inactive-dark'}`} />
                  <span className="font-mono text-orange-400 font-bold text-[11px]">Level {governanceScore} / 4</span>
                </div>
              </div>
              
              {/* Realistic Hardware Radio Well */}
              <div className={`flex w-full p-1.5 rounded-2xl gap-1.5 ${isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'}`}>
                {[1, 2, 3, 4].map((level) => {
                  const isSelected = governanceScore === level;
                  return (
                    <button
                      key={level}
                      onClick={() => setGovernanceScore(level)}
                      className={`flex-1 py-2 px-2 rounded-xl text-center transition-all duration-200 cursor-pointer flex flex-col items-center justify-center gap-1.5 relative ${
                        isSelected
                          ? isLight ? 'tactile-btn-active-light text-slate-900' : 'tactile-btn-active-dark text-white'
                          : isLight ? 'tactile-btn-inactive-light text-slate-800' : 'tactile-btn-inactive-dark text-zinc-300'
                      }`}
                    >
                      <div className="flex items-center gap-1">
                        <span className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                          isSelected ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                        }`} />
                        <span className="text-xs font-mono font-bold">L{level}</span>
                      </div>
                    </button>
                  );
                })}
              </div>
              <div className="flex justify-between text-[11px] font-mono font-medium mt-2 text-[#2D3748]">
                <span>{activeProfile.pillar4Range[0]}</span>
                <span>{activeProfile.pillar4Range[1]}</span>
              </div>
            </div>

          </div>

        </div>

        {/* Right Side: Instant Diagnostic Output & Engagement Path (5 cols) */}
        <div className={`lg:col-span-5 p-6 sm:p-7 rounded-3xl border flex flex-col justify-between ${
          isLight ? 'bg-slate-100/90 border-slate-300' : 'bg-zinc-900/90 border-white/15'
        }`}>
          
          <div className="space-y-5">
            <div className="flex items-center justify-between border-b border-white/15 pb-4">
              <span className={`text-xs font-mono tracking-wider font-bold ${
                isLight ? 'text-slate-800' : 'text-zinc-300'
              }`}>
                Readiness Index ({activeProfile.name.split('&')[0].trim()})
              </span>
              <span className={`text-xs font-mono font-bold px-2.5 py-1 rounded bg-black/40 border border-white/10 ${tier.color}`}>
                {tier.title}
              </span>
            </div>

            {/* Score Display */}
            <div className="flex items-baseline gap-3">
              <span className={`text-5xl font-black font-mono tracking-tight ${
                isLight ? 'text-slate-900' : 'text-zinc-100'
              }`}>
                {percentage}%
              </span>
              <span className={`text-xs font-mono font-semibold ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                AI-Native Index Score
              </span>
            </div>

            {/* Progress Bar */}
            <div className="w-full h-2.5 rounded-full bg-zinc-800 overflow-hidden border border-white/10">
              <div 
                className="h-full bg-gradient-to-r from-orange-500 to-amber-400 transition-all duration-500"
                style={{ width: `${percentage}%` }}
              />
            </div>

            {/* Sector Compliance & Multiplier Badges */}
            <div className="grid grid-cols-2 gap-2 pt-1 text-[11px] font-mono">
              <div className={`p-2 rounded-xl border flex flex-col ${isLight ? 'bg-white border-slate-300 text-slate-800' : 'bg-black/50 border-white/10 text-zinc-300'}`}>
                <span className="text-orange-400 font-bold text-[10px]">Compliance Mandate</span>
                <span className="font-semibold line-clamp-1">{activeProfile.complianceFramework}</span>
              </div>
              <div className={`p-2 rounded-xl border flex flex-col ${isLight ? 'bg-white border-slate-300 text-slate-800' : 'bg-black/50 border-white/10 text-zinc-300'}`}>
                <span className="text-orange-400 font-bold text-[10px]">Impact Multiplier</span>
                <span className="font-semibold line-clamp-1">{activeProfile.multiplier}</span>
              </div>
            </div>

            {/* Strategic Diagnostic Findings (Differentiated Per Industry) */}
            <div className="space-y-3 pt-2">
              <div className={`text-xs font-mono font-bold ${
                isLight ? 'text-slate-800' : 'text-zinc-300'
              }`}>
                Sector Failure Modes & Key Bottlenecks:
              </div>
              
              <ul className="space-y-2.5 text-xs">
                {bottlenecks.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2.5">
                    {item.iconType === 'alert' ? (
                      <AlertCircle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                    ) : (
                      <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                    )}
                    <span className={isLight ? 'text-slate-800' : 'text-zinc-300'}>
                      {item.text}
                      <strong className={isLight ? 'text-slate-950 font-bold' : 'text-white font-bold'}>
                        {item.highlight}
                      </strong>.
                    </span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Recommended Engagement Blueprint */}
            <div className="p-4 rounded-2xl bg-orange-500/10 border border-orange-500/30">
              <div className="text-[11px] font-mono tracking-wider text-orange-400 font-bold mb-1">
                Customized Industry Roadmap ({activeProfile.name}):
              </div>
              <div className={`text-sm font-bold mb-1 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                {tier.reco}
              </div>
              <div className={`text-xs font-normal leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                {tier.desc}
              </div>
            </div>
          </div>

          {/* Action Button */}
          <div className="pt-6">
            <button
              onClick={handleBooking}
              className="w-full py-3.5 px-5 rounded-full font-bold text-xs tracking-widest bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-lg shadow-orange-500/30 transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <span>Request {activeProfile.name.split('&')[0].trim()} Diagnostic Briefing</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <div className={`text-[11px] text-center font-mono font-semibold mt-2 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Confidential advisory consultation • {activeProfile.complianceFramework.split(',')[0]} compliant
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
