import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Globe2, 
  ShieldCheck, 
  Cpu, 
  Layers, 
  Lock, 
  Activity, 
  CheckCircle2, 
  Sparkles, 
  Landmark, 
  Building2, 
  HeartHandshake, 
  Store,
  Terminal,
  ArrowUpRight,
  Shield,
  Key
} from 'lucide-react';
import { StatusBadge } from './ui/StatusBadge';

interface SovereignConstellationProps {
  theme?: 'light' | 'dark';
  onExploreMethod?: () => void;
  onRequestBriefing?: (topic?: string) => void;
}

interface NodeData {
  id: string;
  name: string;
  category: 'geography' | 'institution';
  subhead: string;
  coordinates: string;
  governance: string;
  status: 'active-governed' | 'pilot-node' | 'sovereign-core';
  telemetry: {
    latency: string;
    protocol: string;
    compliance: string;
    agentFleet: string;
  };
  desc: string;
  pos: { x: number; y: number }; // Percentage coordinates in canvas
}

export const SovereignConstellation: React.FC<SovereignConstellationProps> = ({
  theme = 'dark',
  onExploreMethod,
  onRequestBriefing
}) => {
  const isLight = theme === 'light';
  const [selectedNodeId, setSelectedNodeId] = useState<string>('malawi');
  const [activeFilter, setActiveFilter] = useState<'all' | 'geography' | 'institution'>('all');

  const nodes: NodeData[] = [
    {
      id: 'malawi',
      name: 'Lilongwe & Blantyre (Malawi)',
      category: 'geography',
      subhead: 'Sovereign Innovation & Command Hub',
      coordinates: '13.9626° S, 33.7741° E',
      governance: 'Malawi DPA 2017/2024 On-Soil Mandate',
      status: 'sovereign-core',
      telemetry: {
        latency: '< 12ms Local Mesh',
        protocol: 'Air-Gapped Sovereign Mesh',
        compliance: 'Malawi DPA 2017/2024 & MACRA Aligned',
        agentFleet: '144 Canonical Personas'
      },
      desc: 'The primary cradle of LightSpeed Holdings where the 144-agent orchestration platform is proven in-house and sovereign offline-first architectures are engineered for Southern Africa.',
      pos: { x: 50, y: 48 }
    },
    {
      id: 'zambia',
      name: 'Lusaka & Copperbelt (Zambia)',
      category: 'geography',
      subhead: 'Mineral Logistics & Trade Corridor',
      coordinates: '15.3875° S, 28.3228° E',
      governance: 'COMESA Harmonized Trade Protocol',
      status: 'active-governed',
      telemetry: {
        latency: '24ms Corridor Transit',
        protocol: 'Demurrage Mitigation DAG',
        compliance: 'Zambia Data Protection Act 2021',
        agentFleet: 'Corridor Logistics Agents'
      },
      desc: 'Autonomous cross-border logistics and mineral shipment reconciliation connecting inland extraction hubs to regional maritime ports with real-time bill-of-lading verification.',
      pos: { x: 26, y: 32 }
    },
    {
      id: 'zimbabwe',
      name: 'Harare & Beira Link (Zimbabwe)',
      category: 'geography',
      subhead: 'Agribusiness & Transit Gateway',
      coordinates: '17.8252° S, 31.0335° E',
      governance: 'SADC Cross-Border Transit Standard',
      status: 'active-governed',
      telemetry: {
        latency: '18ms Regional Link',
        protocol: 'Commodity Receipt Telemetry',
        compliance: 'Cyber & Data Protection Act',
        agentFleet: 'Agri-Warehouse Arbiters'
      },
      desc: 'Precision agricultural commodity verification, automated warehouse receipts, and multimodal transit tracking across the Beira and Nacala trade corridors.',
      pos: { x: 38, y: 72 }
    },
    {
      id: 'southafrica',
      name: 'Johannesburg (South Africa)',
      category: 'geography',
      subhead: 'SADC Power Pool & Financial Gateway',
      coordinates: '26.2041° S, 28.0473° E',
      governance: 'King IV / POPIA / Basel IV Enclave',
      status: 'active-governed',
      telemetry: {
        latency: '31ms SADC Backbone',
        protocol: 'ISO 20022 Financial Adapter',
        compliance: 'POPIA & SARB Fiduciary Rules',
        agentFleet: 'Liquidity & Trade Arbiters'
      },
      desc: 'Integration gateway with Tier-1 pan-African capital markets, Southern African Power Pool (SAPP) smart grid load dispatch, and ISO 20022 liquidity balancing.',
      pos: { x: 74, y: 78 }
    },
    {
      id: 'government',
      name: 'National Ministries & Regulators',
      category: 'institution',
      subhead: 'MinAg • MACRA • Revenue Authorities',
      coordinates: 'Sovereign Institutional Mesh',
      governance: 'Statutory Policy-as-Code Enclave',
      status: 'pilot-node',
      telemetry: {
        latency: 'Zero Cloud Egress',
        protocol: 'On-Soil Model Enclave',
        compliance: 'National Sovereign Data Protocol',
        agentFleet: 'Customs & Policy Evaluators'
      },
      desc: 'Active stakeholder dialogue and pilot frameworks with the Ministry of Agriculture, MACRA, and national revenue authorities for manifest auditing and agricultural extension.',
      pos: { x: 76, y: 24 }
    },
    {
      id: 'enterprise',
      name: 'Commercial Banks & Corporations',
      category: 'institution',
      subhead: 'Trade Finance & Mobile Money Networks',
      coordinates: 'Tier-1 Enterprise Infrastructure',
      governance: '5-Tier Cryptographic Approval Gates',
      status: 'active-governed',
      telemetry: {
        latency: '< 14 Min Settlement DAG',
        protocol: 'Airtel / TNM / PayChangu Rails',
        compliance: 'Central Bank KYC / AML Rules',
        agentFleet: 'Reconciliation & Swift Agents'
      },
      desc: 'Autonomous multi-currency liquidity balancing, letter of credit reconciliation, and WhatsApp-native customer conversational agents integrated directly with local payment rails.',
      pos: { x: 22, y: 64 }
    },
    {
      id: 'donors',
      name: 'Multilaterals & Donor Agencies',
      category: 'institution',
      subhead: 'UNDP • World Bank • Fiduciary M&E',
      coordinates: 'Development Capital Telemetry',
      governance: 'Anti-Diversion Covenant Enforcement',
      status: 'pilot-node',
      telemetry: {
        latency: 'Deterministic Verification',
        protocol: 'Kobo / DHIS2 Offline Adapter',
        compliance: 'Donor Grant Fiduciary Standards',
        agentFleet: 'M&E Telemetry Arbiters'
      },
      desc: 'Offline-first monitoring and evaluation pipelines integrating KoboToolbox and DHIS2 data streams with autonomous fiduciary audit checks and cryptographic disbursement logs.',
      pos: { x: 80, y: 52 }
    },
    {
      id: 'smes',
      name: 'SMEs, Cooperatives & VSLAs',
      category: 'institution',
      subhead: 'Village Savings & Agricultural Groups',
      coordinates: 'Grassroots Community Network',
      governance: 'Offline-First Local Ledger Security',
      status: 'pilot-node',
      telemetry: {
        latency: 'Store-and-Forward Mesh',
        protocol: 'WhatsApp / Chichewa NLU',
        compliance: 'Micro-Finance Regulatory Act',
        agentFleet: 'Micro-Ledger Bookkeepers'
      },
      desc: 'Grassroots financial inclusion and commercial enablement via Chichewa/English WhatsApp assistants, automated VSLA ledger reconciliation, and micro-merchant tooling.',
      pos: { x: 28, y: 16 }
    }
  ];

  const selectedNode = nodes.find(n => n.id === selectedNodeId) || nodes[0];

  const links = [
    { from: 'malawi', to: 'zambia' },
    { from: 'malawi', to: 'zimbabwe' },
    { from: 'malawi', to: 'southafrica' },
    { from: 'malawi', to: 'government' },
    { from: 'malawi', to: 'enterprise' },
    { from: 'malawi', to: 'donors' },
    { from: 'malawi', to: 'smes' },
    { from: 'zambia', to: 'smes' },
    { from: 'zimbabwe', to: 'enterprise' },
    { from: 'southafrica', to: 'donors' },
    { from: 'government', to: 'donors' }
  ];

  const filteredNodes = nodes.filter(n => {
    if (activeFilter === 'all') return true;
    return n.category === activeFilter;
  });

  return (
    <div className={`p-6 sm:p-10 rounded-3xl border relative overflow-hidden transition-all duration-300 ${
      isLight ? 'bg-gradient-to-br from-white via-slate-50 to-orange-50/20 border-slate-300 shadow-2xl text-slate-800' : 'bg-gradient-to-br from-[#0D0D18] via-[#12131F] to-black border-white/15 shadow-2xl text-zinc-100'
    }`}>
      {/* Structural Hardware Fasteners */}
      <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-black/10 dark:border-white/10">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.9)] animate-pulse" />
            <span className="text-xs font-mono font-bold tracking-widest text-emerald-500 uppercase">
              SIGNATURE ARCHITECTURAL MOTIF // SADC SOVEREIGN CONSTELLATION
            </span>
          </div>
          <h3 className={`text-2xl sm:text-3xl font-black font-display tracking-tight ${isLight ? 'text-slate-900' : 'text-white'}`}>
            Regional Nodes & Governed Arcs
          </h3>
          <p className={`text-justify text-justify text-xs sm:text-sm max-w-2xl ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
            Interactive topology map visualizing how LightSpeed's 144-agent orchestration platform connects Southern African geographies and institutions under strict Human-In-The-Loop (HITL) governance.
          </p>
        </div>

        {/* Filter Controls */}
        <div className={`inline-flex p-1 rounded-full border self-start md:self-auto ${
          isLight ? 'bg-slate-100 border-slate-300' : 'bg-black/40 border-white/10'
        }`}>
          {(['all', 'geography', 'institution'] as const).map((filter) => (
            <button
              key={filter}
              onClick={() => setActiveFilter(filter)}
              className={`px-3 py-1 rounded-full text-[10px] font-mono font-bold uppercase transition-all cursor-pointer ${
                activeFilter === filter
                  ? 'bg-orange-500 text-white shadow-xs'
                  : isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white'
              }`}
            >
              {filter === 'all' ? 'All Nodes (8)' : filter === 'geography' ? 'Geographies (4)' : 'Institutions (4)'}
            </button>
          ))}
        </div>
      </div>

      {/* Main Interactive Stage */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 pt-6 items-center">
        
        {/* Left / Center: Interactive Constellation Visual Stage (7 Cols) */}
        <div className="lg:col-span-7 relative min-h-[420px] sm:min-h-[480px] rounded-2xl border overflow-hidden p-4 flex items-center justify-center bg-black/40 border-white/10 backdrop-blur-md">
          
          {/* Subtle Grid Backdrop */}
          <div className="absolute inset-0 bg-[radial-gradient(#f97316_1px,transparent_1px)] [background-size:24px_24px] opacity-15 pointer-events-none" />
          
          {/* Central Human-In-The-Loop (HITL) Governed Safety Ring */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none flex items-center justify-center">
            {/* Outer Breathing Ring */}
            <div className="w-52 h-52 sm:w-64 sm:h-64 rounded-full border border-orange-500/20 animate-ping opacity-25" />
            <div className="w-40 h-40 sm:w-48 sm:h-48 rounded-full border border-dashed border-emerald-500/30 absolute animate-spin [animation-duration:45s]" />
            <div className="w-28 h-28 sm:w-32 sm:h-32 rounded-full bg-orange-500/5 border border-orange-500/40 absolute flex flex-col items-center justify-center p-2 text-center backdrop-blur-xs">
              <ShieldCheck className="w-4 h-4 text-emerald-400 mb-0.5" />
              <span className="text-[8px] font-mono font-bold text-orange-400 tracking-wider">HITL GATE</span>
              <span className="text-[7px] font-mono text-zinc-400">H-A-O-M-T-G-V</span>
            </div>
          </div>

          {/* SVG Governed Arcs Linking Nodes */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="arcGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#f97316" stopOpacity="0.6" />
                <stop offset="100%" stopColor="#10b981" stopOpacity="0.4" />
              </linearGradient>
              <linearGradient id="pulseGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#10b981" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#f97316" stopOpacity="0.8" />
              </linearGradient>
            </defs>

            {links.map((link, idx) => {
              const fromNode = nodes.find(n => n.id === link.from);
              const toNode = nodes.find(n => n.id === link.to);
              if (!fromNode || !toNode) return null;

              const isHighlighted = selectedNodeId === link.from || selectedNodeId === link.to;

              return (
                <g key={idx}>
                  <line
                    x1={`${fromNode.pos.x}%`}
                    y1={`${fromNode.pos.y}%`}
                    x2={`${toNode.pos.x}%`}
                    y2={`${toNode.pos.y}%`}
                    stroke={isHighlighted ? 'url(#pulseGradient)' : '#ffffff'}
                    strokeOpacity={isHighlighted ? 0.8 : 0.15}
                    strokeWidth={isHighlighted ? 2 : 1}
                    strokeDasharray={isHighlighted ? '4,4' : 'none'}
                    className={isHighlighted ? 'animate-pulse' : ''}
                  />
                  {isHighlighted && (
                    <circle r="3" fill="#10b981">
                      <animateMotion
                        path={`M ${fromNode.pos.x * 4} ${fromNode.pos.y * 4} L ${toNode.pos.x * 4} ${toNode.pos.y * 4}`}
                        dur="3s"
                        repeatCount="indefinite"
                      />
                    </circle>
                  )}
                </g>
              );
            })}
          </svg>

          {/* Render Constellation Interactive Node Buttons */}
          {filteredNodes.map((node) => {
            const isSelected = selectedNodeId === node.id;
            const isCore = node.id === 'malawi';

            return (
              <motion.button
                key={node.id}
                onClick={() => setSelectedNodeId(node.id)}
                whileHover={{ scale: 1.08 }}
                whileTap={{ scale: 0.95 }}
                style={{
                  position: 'absolute',
                  left: `${node.pos.x}%`,
                  top: `${node.pos.y}%`,
                  transform: 'translate(-50%, -50%)'
                }}
                className={`group z-20 flex flex-col items-center gap-1 cursor-pointer focus:outline-none`}
              >
                {/* Visual Node Core Orb */}
                <div className={`relative rounded-full flex items-center justify-center transition-all duration-300 ${
                  isCore 
                    ? 'w-11 h-11 bg-gradient-to-tr from-orange-500 to-amber-400 text-white shadow-[0_0_20px_rgba(249,115,22,0.8)] border-2 border-white ring-4 ring-orange-500/30' 
                    : isSelected
                      ? 'w-9 h-9 bg-emerald-500 text-white shadow-[0_0_16px_rgba(16,185,129,0.8)] border-2 border-white'
                      : 'w-7 h-7 bg-zinc-900/90 text-zinc-300 border border-white/30 hover:border-orange-400 hover:text-white hover:bg-zinc-800'
                }`}>
                  {isCore ? (
                    <Globe2 className="w-5 h-5 animate-spin [animation-duration:30s]" />
                  ) : node.category === 'geography' ? (
                    <Building2 className="w-3.5 h-3.5" />
                  ) : node.id === 'government' ? (
                    <Landmark className="w-3.5 h-3.5" />
                  ) : node.id === 'donors' ? (
                    <HeartHandshake className="w-3.5 h-3.5" />
                  ) : (
                    <Store className="w-3.5 h-3.5" />
                  )}

                  {/* Pulsing indicator on selected */}
                  {isSelected && (
                    <span className="absolute -inset-1 rounded-full border border-emerald-400 animate-ping opacity-75" />
                  )}
                </div>

                {/* Node Pill Label */}
                <div className={`px-2 py-0.5 rounded-full text-[9px] font-mono font-bold whitespace-nowrap shadow-md transition-all ${
                  isSelected
                    ? 'bg-emerald-500 text-white border border-emerald-300'
                    : isCore
                      ? 'bg-orange-500 text-white border border-orange-300'
                      : 'bg-black/70 text-zinc-300 border border-white/20 group-hover:text-white group-hover:border-orange-400'
                }`}>
                  {node.name.split(' ')[0]}
                </div>
              </motion.button>
            );
          })}

          {/* Bottom HUD Legend */}
          <div className="absolute bottom-3 left-3 right-3 flex flex-wrap items-center justify-between gap-2 p-2 rounded-xl bg-black/70 backdrop-blur-md border border-white/10 text-[9px] font-mono text-zinc-400 pointer-events-none">
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1.5 text-orange-400">
                <span className="w-2 h-2 rounded-full bg-orange-500" /> Sovereign Hub
              </span>
              <span className="flex items-center gap-1.5 text-emerald-400">
                <span className="w-2 h-2 rounded-full bg-emerald-500" /> Governed Regional Node
              </span>
              <span className="flex items-center gap-1.5 text-amber-300">
                <span className="w-2 h-2 rounded-full bg-amber-400" /> Stakeholder Pilot
              </span>
            </div>
            <span className="text-zinc-400 font-bold hidden sm:inline">CLICK ANY NODE TO INSPECT TELEMETRY</span>
          </div>

        </div>

        {/* Right: Selected Node Detailed Telemetry & Policy Enclave (5 Cols) */}
        <div className="lg:col-span-5 space-y-4">
          <AnimatePresence mode="wait">
            <motion.div
              key={selectedNode.id}
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -16 }}
              transition={{ duration: 0.3 }}
              className={`p-5 sm:p-6 rounded-2xl border relative overflow-hidden space-y-4 ${
                isLight ? 'bg-white border-slate-300 shadow-lg' : 'bg-black/60 border-white/15 shadow-xl'
              }`}
            >
              {/* Node Status Badge & Category Header */}
              <div className="flex items-center justify-between gap-2 border-b border-black/10 dark:border-white/10 pb-3">
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded ${
                    selectedNode.category === 'geography'
                      ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                      : 'bg-purple-500/10 text-purple-400 border border-purple-500/20'
                  }`}>
                    {selectedNode.category === 'geography' ? 'SADC GEOGRAPHY NODE' : 'INSTITUTIONAL MESH'}
                  </span>
                </div>

                <StatusBadge 
                  tier={
                    selectedNode.status === 'sovereign-core' 
                      ? 'proven-in-house' 
                      : selectedNode.status === 'active-governed' 
                        ? 'fieldable-2026' 
                        : 'pilot'
                  }
                  size="sm"
                />
              </div>

              {/* Node Title & Subhead */}
              <div>
                <h4 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                  {selectedNode.name}
                </h4>
                <p className="text-xs font-mono text-orange-500 font-bold mt-0.5">
                  {selectedNode.subhead}
                </p>
              </div>

              {/* Description Paragraph */}
              <p className={`text-justify text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                {selectedNode.desc}
              </p>

              {/* Telemetry Matrix Strip */}
              <div className={`p-3.5 rounded-xl border space-y-2 font-mono text-[11px] ${
                isLight ? 'bg-slate-50 border-slate-200 text-slate-800' : 'bg-white/[0.04] border-white/10 text-zinc-300'
              }`}>
                <div className="flex justify-between items-center">
                  <span className="text-zinc-400">Coordinates:</span>
                  <span className="font-bold text-orange-400">{selectedNode.coordinates}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-zinc-400">Data Jurisdiction:</span>
                  <span className="font-bold text-emerald-400">{selectedNode.governance}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-zinc-400">Node Latency:</span>
                  <span className={`font-bold ${isLight ? 'text-slate-900' : 'text-white'}`}>{selectedNode.telemetry.latency}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-zinc-400">Protocol Rails:</span>
                  <span className="font-bold text-amber-400">{selectedNode.telemetry.protocol}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-zinc-400">Active Persona Fleet:</span>
                  <span className="font-bold text-blue-400">{selectedNode.telemetry.agentFleet}</span>
                </div>
              </div>

              {/* Governance Proof Point */}
              <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/25 flex items-start gap-2 text-emerald-400 text-xs">
                <ShieldCheck className="w-4 h-4 shrink-0 mt-0.5 text-emerald-400" />
                <span className="text-[11px] leading-snug">
                  <strong>Sovereign Green Light:</strong> {selectedNode.telemetry.compliance}. Zero unencrypted public SaaS transit.
                </span>
              </div>

              {/* Action Trigger */}
              <div className="pt-1 flex items-center gap-2">
                <button
                  onClick={() => onRequestBriefing?.(`Discovery Call for ${selectedNode.name} (${selectedNode.subhead})`)}
                  className="flex-1 py-2.5 px-4 rounded-xl text-xs font-bold font-mono tracking-wider bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-md shadow-orange-500/25 transition-all cursor-pointer flex items-center justify-center gap-1.5"
                >
                  <span>Book Consultation for this Node</span>
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </button>
              </div>

            </motion.div>
          </AnimatePresence>
        </div>

      </div>
    </div>
  );
};
