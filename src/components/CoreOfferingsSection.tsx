import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Network } from 'lucide-react';
import { OfferingDetailCard } from './OfferingDetailCard';
import { SynergyMatrix } from './SynergyMatrix';

interface CoreCapability {
  id: string;
  title: string;
  shortTitle: string;
  eyebrow: string;
  tagline: string;
  desc: string;
  metrics: string;
  inputContract: string;
  outputContract: string;
  upstreamSource: string;
  downstreamTarget: string;
  governance: string;
  deliverables: string[];
}

interface CoreOfferingsSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
  activePillar: number;
  onSelectPillar: (idx: number) => void;
}

const coreCapabilities: CoreCapability[] = [
  {
    id: 'strategy',
    title: 'Strategy & Operating Models',
    shortTitle: 'Strategy',
    eyebrow: 'CORE OFFERING 01 // EXECUTIVE ARCHITECTURE',
    tagline: 'Executable Business Rules & Capital Allocation',
    desc: 'We work with Chairpersons, CEOs, and Executive Committees across SADC to turn strategy into executable business rules. You get machine-readable policies, budget controls, and approval workflows instead of 200-page slide decks that gather dust.',
    metrics: '5-Tier HITL Approval Gates',
    inputContract: 'Board Mandates, Statutory Frameworks, Capital Budgets, Operating Model',
    outputContract: 'Executable Policy Rules, Token Budgets, Approval Gate Definitions',
    upstreamSource: 'Live performance data and model drift feedback from Offering 04 (Execution)',
    downstreamTarget: 'Feeds policy constraints and data access rules directly to Offering 02 (Intelligence) and 03 (Autonomous Systems)',
    governance: 'Basel IV / King IV / SADC Regulatory Compliant',
    deliverables: [
      'Operations Audit & Latency Map',
      'Approval Gate Definitions & Risk Matrix',
      'AI Investment Case & ROI Roadmap',
      'Data Residency & Compliance Blueprint'
    ]
  },
  {
    id: 'intelligence',
    title: 'Private Intelligence & Knowledge Graphs',
    shortTitle: 'Private Intelligence',
    eyebrow: 'CORE OFFERING 02 // DATA SYSTEMS',
    tagline: 'Private Knowledge Graphs & Semantic Search',
    desc: 'We convert scattered enterprise data, regulatory filings, shipping manifests, and legacy databases into a private, searchable knowledge graph. Your data stays inside your perimeter with zero leakage to external cloud services.',
    metrics: 'Registry-Verified Data Retrieval & Lineage',
    inputContract: 'Unstructured Documents, ERP Databases, Mainframes, Regulatory Filings',
    outputContract: 'Private Enterprise Knowledge Graph, Semantic Search, Verified Data Lineage',
    upstreamSource: 'Governed by data boundary policies defined in Offering 01 (Strategy)',
    downstreamTarget: 'Supplies verified, air-gapped contextual data to Offering 03 (Autonomous Systems)',
    governance: 'On-Site Data / Air-Gapped On-Premise',
    deliverables: [
      'Private Knowledge Graph Systems',
      'Document Ingestion & Classification Engines',
      'Verified Data Lineage & Provenance Tracking',
      'Air-Gapped On-Site Model Clusters & Local Inference'
    ]
  },
  {
    id: 'systems',
    title: 'Autonomous Systems & Agent Fleets',
    shortTitle: 'Autonomous Systems',
    eyebrow: 'CORE OFFERING 03 // AGENT ARCHITECTURE',
    tagline: 'Structured Multi-Agent Team Engineering',
    desc: 'We build teams of specialized AI agents, each with strict boundaries: limited tools, set budgets, and full audit trails. Every action is logged, checked, and executed through a structured workflow. No black boxes, no unreviewed outputs.',
    metrics: '144 Verified Agent Configurations in Production',
    inputContract: 'Policy bounds from Offering 01 and contextual knowledge from Offering 02',
    outputContract: 'Structured Transaction Payloads, Reconciled Ledgers, Exception Alerts',
    upstreamSource: 'Driven by Strategy policies (01) and grounded in Intelligence graphs (02)',
    downstreamTarget: 'Dispatches validated payloads to Offering 04 (Execution & Settlement)',
    governance: 'OpenCode Canonical 7-Tool Permission Gates',
    deliverables: [
      'Multi-Agent Hierarchies & Task Workflows',
      'Tool Budgets & Rate Limiters',
      'Consensus Checkers & Safety Guardrails',
      'Continuous Model Drift & Performance Monitoring'
    ]
  },
  {
    id: 'execution',
    title: 'Execution, Governance & Settlement',
    shortTitle: 'Execution & Settlement',
    eyebrow: 'CORE OFFERING 04 // CORE INTEGRATION',
    tagline: 'Legacy System Integration & Instant Settlement',
    desc: 'We connect your existing banking cores, customs systems, and supply chain software to fast API event streams. Every transaction requires human approval before it writes to the core system. Every write is logged to an unchangeable audit trail.',
    metrics: '5-Tier Human Approval Gates & Registry-Verified Audit Trails',
    inputContract: 'Validated agent payloads from Offering 03 and Human Approval tokens',
    outputContract: 'Live Core Settlement, Customs EDI Filings, Immutable Audit Trails',
    upstreamSource: 'Receives transaction payloads from Offering 03; enforces human approval gates',
    downstreamTarget: 'Streams performance KPIs, recovered revenue, and drift telemetry back to Offering 01 (Strategy)',
    governance: 'Immutable SHA-256 / WCO SAFE / SADC EDI Standard',
    deliverables: [
      'Legacy Core API Modernization Connectors',
      'SADC Regional Payment & Customs EDI Connectors',
      'Automated Settlement & Human Approval Gates',
      'Zero-Trust Immutable Audit Logging'
    ]
  }
];

export const CoreOfferingsSection: React.FC<CoreOfferingsSectionProps> = ({
  theme,
  onRequestBriefing,
  activePillar,
  onSelectPillar
}) => {
  const isLight = theme === 'light';
  const [selectedSynergy, setSelectedSynergy] = useState<string>('strategy-intelligence');

  return (
    <section id="capabilities" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      <div className="max-w-3xl mb-12 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
          <Network className="w-3.5 h-3.5" />
          <span>INTEGRATED ARCHITECTURE</span>
        </div>
        <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}>
          Four Connected Core Offerings
        </h2>
        <p className={`text-justify text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          We do not sell standalone tools or chatbots. We build a closed-loop system where strategy compiles into private knowledge graphs, structured AI teams, and audited core execution.
        </p>
      </div>

      {/* 4 Core Offerings Tab Switcher */}
      <div className={`p-2 rounded-3xl mb-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 ${
        isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'
      }`}>
        {coreCapabilities.map((cap, idx) => (
          <button
            key={cap.id}
            onClick={() => onSelectPillar(idx)}
            className={`p-4 rounded-2xl text-left transition-all duration-200 cursor-pointer relative overflow-hidden group ${
              activePillar === idx
                ? isLight
                  ? 'tactile-btn-active-light text-slate-900 border-ls-red/50 shadow-md'
                  : 'tactile-btn-active-dark text-white border-ls-red/50 shadow-lg'
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
                    ? 'bg-ls-red/20 text-ls-red'
                    : 'bg-black/5 text-zinc-500'
                }`}>
                  OFFERING 0{idx + 1}
                </span>
              </div>
              <span className={`text-[10px] font-mono font-medium ${
                activePillar === idx ? 'text-ls-red font-bold' : 'text-zinc-500'
              }`}>
                {idx === 0 ? 'GOVERN' : idx === 1 ? 'SYNTHESIZE' : idx === 2 ? 'ORCHESTRATE' : 'SETTLE'}
              </span>
            </div>
            <span className="text-sm font-bold tracking-wide block font-display leading-tight">{cap.shortTitle}</span>
            <p className={`text-justify text-[11px] mt-1.5 line-clamp-2 ${
              activePillar === idx
                ? isLight ? 'text-slate-800 font-medium' : 'text-zinc-200'
                : 'text-zinc-500'
            }`}>
              {cap.tagline}
            </p>
          </button>
        ))}
      </div>

      {/* Active Core Offering Deep-Dive View */}
      <OfferingDetailCard
        theme={theme}
        onRequestBriefing={onRequestBriefing}
        offering={coreCapabilities[activePillar]}
        activePillar={activePillar}
        totalPillars={coreCapabilities.length}
        onSelectPillar={onSelectPillar}
      />

      {/* SYNERGY MATRIX */}
      <SynergyMatrix
        theme={theme}
        selectedSynergy={selectedSynergy}
        onSelectSynergy={setSelectedSynergy}
      />

      {/* Comparative Table */}
      <div className="mt-8 pt-8 border-t border-slate-200 dark:border-white/10">
        <div className="flex items-center justify-between mb-4">
          <span className={`text-xs font-mono font-bold tracking-wider ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
            Disconnected Point-Tools vs. Connected Suite
          </span>
          <span className="text-[10px] font-mono text-ls-red font-bold">
            Zero Cloud SaaS Leakage
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className={`border-b ${isLight ? 'border-slate-300 bg-slate-100/80 text-slate-800' : 'border-white/10 bg-zinc-900/50 text-zinc-300'}`}>
                <th className="p-3 font-mono font-bold">Offering Layer</th>
                <th className="p-3 font-mono font-bold text-rose-500">Fragmented Point Solution</th>
                <th className="p-3 font-mono font-bold text-ls-cyan">Lightspeed Connected Architecture</th>
              </tr>
            </thead>
            <tbody className={`divide-y ${isLight ? 'divide-slate-200 text-slate-700' : 'divide-white/10 text-zinc-300'}`}>
              <tr>
                <td className="p-3 font-bold font-mono text-ls-red">01. Strategy</td>
                <td className="p-3">Static PowerPoint slide decks, 9-month review cycles, zero computable rules.</td>
                <td className="p-3 font-medium text-ls-cyan dark:text-ls-cyan">Executable policy rules, dynamic budgets, live board models.</td>
              </tr>
              <tr>
                <td className="p-3 font-bold font-mono text-ls-red">02. Intelligence</td>
                <td className="p-3">Siloed data lakes, public LLM APIs risking trade secrets and residency.</td>
                <td className="p-3 font-medium text-ls-cyan dark:text-ls-cyan">On-site knowledge graphs with verified data lineage.</td>
              </tr>
              <tr>
                <td className="p-3 font-bold font-mono text-ls-red">03. Autonomous Systems</td>
                <td className="p-3">Unbounded chatbots prone to hallucinations and tool abuse.</td>
                <td className="p-3 font-medium text-ls-cyan dark:text-ls-cyan">Structured agent fleets bound to 7 canonical tools and strict workflows.</td>
              </tr>
              <tr>
                <td className="p-3 font-bold font-mono text-ls-red">04. Execution & Governance</td>
                <td className="p-3">Manual data re-entry, paper-based settlement, post-facto audit trails.</td>
                <td className="p-3 font-medium text-ls-cyan dark:text-ls-cyan">Direct core API event rails, human approval gates, immutable audit logs.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </section>
  );
};
