import React, { useState } from 'react';
import {
  Globe2,
  MapPin,
  Clock,
  CheckCircle2,
  ArrowRight,
  Sparkles,
  Radio,
  Server,
  ShieldCheck,
  Zap,
  Activity,
  Compass
} from 'lucide-react';
import {
  StatusLedPip
} from './TactileHardwareElements';

interface InteractiveTimelineMapProps {
  theme?: 'light' | 'dark';
  onNavigate: (route: string) => void;
  onOpenContactModal: (intent?: string) => void;
}

export const InteractiveTimelineMap: React.FC<InteractiveTimelineMapProps> = ({
  theme = 'dark',
  onNavigate,
  onOpenContactModal
}) => {
  const isLight = theme === 'light';
  const [selectedMilestone, setSelectedMilestone] = useState<number>(2); // Default to 2026
  const [selectedNode, setSelectedNode] = useState<string>('lilongwe');
  const [activeView, setActiveView] = useState<'timeline' | 'map'>('map');

  const milestones = [
    {
      year: '2024',
      quarter: 'Q1–Q4',
      title: 'Genesis in Lilongwe & Sovereign Charter',
      desc: 'LightSpeed Holdings Limited founded in Lilongwe by Jack Mlusu. Established baseline sovereign compute architecture and rejected extractive cloud dependency.',
      badge: 'FOUNDATIONAL GENESIS',
      kpi: 'Lilongwe HQ Active • 100% On-Soil Models'
    },
    {
      year: '2025',
      quarter: 'Q1–Q4',
      title: 'The Pharos Doctrine & Financial Settlement',
      desc: 'Architected OpenCode multi-agent framework, Tier-1 to Tier-5 HITL cryptographic governance gates, and sub-30s Airtel & TNM Mpamba mobile settlement integrations.',
      badge: 'GOVERNANCE & RAILS',
      kpi: '<30s Settlement • 0 Hallucinations'
    },
    {
      year: '2026',
      quarter: 'ACTIVE NOW',
      title: 'SADC Multi-Agent Swarm Constellation',
      desc: 'Continental scaling of autonomous agent swarms across banking, agriculture, and government ministries. Launch of AI Company Builder platform.',
      badge: 'REGIONAL EXPANSION',
      kpi: '7 Sovereign Nodes • 99.98% Uptime'
    },
    {
      year: '2027',
      quarter: 'ROADMAP',
      title: 'Indigenous Dialect & Cross-Border SADC Trade',
      desc: 'Deep integration of localized tokenizers for Chichewa, Tumbuka, and Swahili with SADC cross-border customs & trade clearance automation.',
      badge: 'INDIGENOUS NLP',
      kpi: '12 National Dialects • Instant Customs'
    },
    {
      year: '2028',
      quarter: 'VISION',
      title: 'Pan-African Sovereign Compute Constellation',
      desc: 'Distributed sovereign edge clusters operating from Cape to Cairo, powering Africa’s leading corporate and public sector institutions.',
      badge: 'CONTINENTAL PERMANENCE',
      kpi: '54 Nation Sovereign Federation'
    }
  ];

  const regionalNodes: Record<string, {
    city: string;
    country: string;
    coords: { x: number; y: number };
    type: string;
    latency: string;
    status: string;
    details: string;
    dialect: string;
  }> = {
    lilongwe: {
      city: 'Lilongwe (Central Command HQ)',
      country: 'Malawi',
      coords: { x: 58, y: 35 },
      type: 'Primary Sovereign Operations & Orchestration Hub',
      latency: '1.2 ms',
      status: 'OPERATIONAL (NOMINAL)',
      details: 'High-density GPU cluster, 24/7 fiduciary oversight, primary OpenCode message bus.',
      dialect: 'Chichewa, English (Official SADC)'
    },
    blantyre: {
      city: 'Blantyre Finance Node',
      country: 'Malawi',
      coords: { x: 60, y: 44 },
      type: 'Fintech & Mobile Settlement Cluster',
      latency: '3.8 ms',
      status: 'OPERATIONAL',
      details: 'Direct interconnect with Reserve Bank of Malawi RTGS, Airtel Money, and TNM Mpamba.',
      dialect: 'Chichewa, Sena'
    },
    lusaka: {
      city: 'Lusaka Agri-Trade Node',
      country: 'Zambia',
      coords: { x: 42, y: 38 },
      type: 'Agricultural Value Chain & Minerals Gateway',
      latency: '11.4 ms',
      status: 'OPERATIONAL',
      details: 'Grain commodity routing, cross-border logistics clearing, copper belt supply analytics.',
      dialect: 'Bemba, Nyanja, Tonga'
    },
    harare: {
      city: 'Harare Sovereign Node',
      country: 'Zimbabwe',
      coords: { x: 50, y: 52 },
      type: 'Industrial Automation & Energy Dispatch',
      latency: '14.2 ms',
      status: 'OPERATIONAL',
      details: 'Hydropower optimization, regional power pool telemetry, SME growth agent swarms.',
      dialect: 'Shona, Ndebele'
    },
    gaborone: {
      city: 'Gaborone Institutional Node',
      country: 'Botswana',
      coords: { x: 30, y: 68 },
      type: 'Public Sector Governance & Compliance',
      latency: '18.1 ms',
      status: 'ACTIVE STAGING',
      details: 'SADC Secretariat policy alignment, sovereign mineral audit logging.',
      dialect: 'Setswana, English'
    },
    maputo: {
      city: 'Maputo Maritime Port Node',
      country: 'Mozambique',
      coords: { x: 62, y: 72 },
      type: 'Port Logistics & Customs Automation',
      latency: '16.5 ms',
      status: 'ACTIVE STAGING',
      details: 'Corridor container routing, multi-lingual customs clearance, maritime security.',
      dialect: 'Portuguese, Changana'
    },
    johannesburg: {
      city: 'Johannesburg Interconnect',
      country: 'South Africa',
      coords: { x: 45, y: 76 },
      type: 'High-Throughput Exchange Gateway',
      latency: '19.4 ms',
      status: 'OPERATIONAL',
      details: 'Direct peering with continental fiber trunks and regional banking consortiums.',
      dialect: 'Zulu, Xhosa, Afrikaans, English'
    }
  };

  const currentNode = regionalNodes[selectedNode];

  return (
    <div className={`rounded-3xl relative overflow-hidden transition-all text-left p-6 sm:p-10 ${
      isLight ? 'neu-card-light' : 'neu-card-dark'
    }`}>
      {/* Top Header Strip */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-2xl flex items-center justify-center shrink-0 ${
            isLight ? 'neu-inset-light text-amber-600' : 'neu-inset-dark text-amber-400'
          }`}>
            <Globe2 className="w-5 h-5 text-amber-500" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <StatusLedPip status="emerald" isLight={isLight} />
              <span className="text-[11px] font-mono font-bold tracking-widest text-amber-500 uppercase">
                INTERACTIVE TIMELINE &amp; SADC GEO-SOVEREIGNTY MAP
              </span>
            </div>
            <span className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Clickable Milestones • Live Node Latency • Geographic Infrastructure
            </span>
          </div>
        </div>

        {/* View Switcher */}
        <div className="flex items-center gap-2">
          <div className={`flex items-center p-1 rounded-2xl ${
            isLight ? 'neu-inset-light' : 'neu-inset-dark'
          }`}>
            <button
              onClick={() => setActiveView('map')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeView === 'map'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              SADC Node Map
            </button>
            <button
              onClick={() => setActiveView('timeline')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeView === 'timeline'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              2024–2028 Timeline
            </button>
          </div>
        </div>
      </div>

      {/* Main Narrative Headline */}
      <div className="relative z-10 max-w-4xl space-y-4 mb-10">
        <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-mono font-semibold ${
          isLight ? 'neu-pill-light text-amber-700' : 'neu-pill-dark text-amber-400'
        }`}>
          <Compass className="w-3.5 h-3.5 text-amber-500" />
          <span>Regional Physical Infrastructure</span>
        </div>

        <h2 className={`text-2xl sm:text-4xl lg:text-5xl font-extrabold font-display tracking-tight leading-tight ${
          isLight ? 'text-slate-900' : 'text-zinc-50'
        }`}>
          A Living Network Across SADC—<span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">Engineered for Permanence</span>
        </h2>

        <p className={`text-sm sm:text-base md:text-lg leading-relaxed font-sans ${
          isLight ? 'text-slate-700' : 'text-zinc-300'
        }`}>
          Select any node on the regional map or click through our milestone roadmap to inspect live compute telemetry, dialect tokenizers, and sovereign settlement capabilities.
        </p>
      </div>

      {/* View: SADC Node Map */}
      {activeView === 'map' && (
        <div className="space-y-6 relative z-10 mb-10">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">

            {/* Interactive Schematic SADC Map Viewport */}
            <div className={`lg:col-span-7 p-6 rounded-2xl relative aspect-[4/3] flex flex-col justify-between overflow-hidden ${
              isLight ? 'neu-well-light' : 'neu-well-dark'
            }`}>
              {/* Map Background Grid */}
              <div className="absolute inset-0 pharos-stone-masonry opacity-40 pointer-events-none" />

              {/* SADC Region Schematic SVG Canvas */}
              <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100">
                {/* Connecting sovereign trunk lines */}
                <line x1="58" y1="35" x2="60" y2="44" stroke="#e63946" strokeWidth="0.8" strokeDasharray="1,1" />
                <line x1="58" y1="35" x2="42" y2="38" stroke="#e63946" strokeWidth="0.8" strokeDasharray="1,1" />
                <line x1="58" y1="35" x2="50" y2="52" stroke="#e63946" strokeWidth="0.8" strokeDasharray="1,1" />
                <line x1="50" y1="52" x2="62" y2="72" stroke="#e63946" strokeWidth="0.6" strokeDasharray="1,1" />
                <line x1="50" y1="52" x2="30" y2="68" stroke="#e63946" strokeWidth="0.6" strokeDasharray="1,1" />
                <line x1="30" y1="68" x2="45" y2="76" stroke="#e63946" strokeWidth="0.6" strokeDasharray="1,1" />

                {/* Node Markers */}
                {Object.entries(regionalNodes).map(([key, node]) => {
                  const isSelected = selectedNode === key;
                  return (
                    <g key={key} onClick={() => setSelectedNode(key)} className="cursor-pointer">
                      {isSelected && (
                        <circle
                          cx={node.coords.x}
                          cy={node.coords.y}
                          r="5"
                          fill="none"
                          stroke="#e63946"
                          strokeWidth="0.5"
                          className="animate-ping"
                        />
                      )}
                      <circle
                        cx={node.coords.x}
                        cy={node.coords.y}
                        r={isSelected ? "3" : "2"}
                        fill={isSelected ? "#e63946" : (isLight ? "#64748b" : "#94a3b8")}
                      />
                      <text
                        x={node.coords.x + 3.5}
                        y={node.coords.y + 1}
                        fontSize="3.2"
                        fontFamily="monospace"
                        fontWeight={isSelected ? "bold" : "normal"}
                        fill={isSelected ? "#e63946" : (isLight ? "#334155" : "#cbd5e1")}
                      >
                        {node.city.split(' ')[0]}
                      </text>
                    </g>
                  );
                })}
              </svg>

              {/* Map Footer Info */}
              <div className="relative z-10 text-[10px] font-mono text-zinc-400 flex justify-between items-end">
                <span>GRID: SADC HIGH-SPEED SOVEREIGN FIBER</span>
                <span className="text-amber-500 font-bold">CLICK PINS TO INSPECT</span>
              </div>
            </div>

            {/* Node Detail Telemetry Panel */}
            <div className={`lg:col-span-5 p-6 rounded-2xl space-y-4 ${
              isLight ? 'neu-convex-light' : 'neu-convex-dark'
            }`}>
              <div className="flex items-center justify-between pb-3 border-b border-zinc-500/15">
                <div className="flex items-center gap-2">
                  <MapPin className="w-5 h-5 text-amber-500" />
                  <h3 className={`text-base font-bold font-display ${
                    isLight ? 'text-slate-900' : 'text-zinc-100'
                  }`}>
                    {currentNode.city}
                  </h3>
                </div>
                <span className="text-[10px] font-mono px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-500 font-bold border border-emerald-500/20">
                  {currentNode.status}
                </span>
              </div>

              <div className="space-y-2 text-xs font-mono">
                <div>
                  <span className="text-zinc-500">NODE CLASS: </span>
                  <span className="text-amber-600 dark:text-amber-400 font-semibold">{currentNode.type}</span>
                </div>
                <div>
                  <span className="text-zinc-500">LATENCY TO HQ: </span>
                  <span className="text-emerald-500 font-bold">{currentNode.latency}</span>
                </div>
                <div>
                  <span className="text-zinc-500">REGIONAL DIALECTS: </span>
                  <span className={isLight ? 'text-slate-800' : 'text-zinc-200'}>{currentNode.dialect}</span>
                </div>
              </div>

              <p className={`text-xs sm:text-sm leading-relaxed pt-2 border-t border-zinc-500/10 ${
                isLight ? 'text-slate-600' : 'text-zinc-400'
              }`}>
                {currentNode.details}
              </p>

              {/* Node selection buttons */}
              <div className="flex flex-wrap gap-1.5 pt-2">
                {Object.keys(regionalNodes).map((key) => (
                  <button
                    key={key}
                    onClick={() => setSelectedNode(key)}
                    className={`px-2.5 py-1 rounded-lg text-[10px] font-mono font-bold uppercase transition-all cursor-pointer ${
                      selectedNode === key
                        ? (isLight ? 'bg-amber-500 text-slate-950 shadow-sm' : 'bg-amber-500 text-slate-950')
                        : (isLight ? 'neu-inset-light text-slate-600' : 'neu-inset-dark text-zinc-400')
                    }`}
                  >
                    {key}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* View: 2024-2028 Timeline */}
      {activeView === 'timeline' && (
        <div className="space-y-6 relative z-10 mb-10">
          <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
            {milestones.map((m, idx) => {
              const isSelected = selectedMilestone === idx;
              return (
                <button
                  key={m.year}
                  onClick={() => setSelectedMilestone(idx)}
                  className={`p-4 rounded-2xl text-left transition-all cursor-pointer flex flex-col justify-between ${
                    isSelected
                      ? (isLight ? 'neu-pressed-light border-amber-500/50' : 'neu-pressed-dark border-amber-500/50')
                      : (isLight ? 'neu-convex-light' : 'neu-convex-dark')
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-sm font-mono font-extrabold text-amber-500">
                        {m.year}
                      </span>
                      <span className="text-[9px] font-mono text-zinc-400">
                        {m.quarter}
                      </span>
                    </div>
                    <div className={`text-xs font-bold font-display line-clamp-2 ${
                      isSelected ? 'text-amber-600 dark:text-amber-400' : (isLight ? 'text-slate-900' : 'text-zinc-100')
                    }`}>
                      {m.title}
                    </div>
                  </div>
                  <div className="text-[10px] font-mono text-emerald-500 font-semibold mt-2">
                    {m.badge}
                  </div>
                </button>
              );
            })}
          </div>

          {/* Active Milestone Card */}
          <div className={`p-6 sm:p-8 rounded-2xl ${isLight ? 'neu-well-light' : 'neu-well-dark'}`}>
            <div className="flex flex-wrap items-center justify-between gap-4 mb-3 pb-3 border-b border-zinc-500/15">
              <div>
                <span className="text-2xl sm:text-3xl font-mono font-extrabold text-amber-500">
                  {milestones[selectedMilestone].year} • {milestones[selectedMilestone].quarter}
                </span>
                <h3 className={`text-lg sm:text-xl font-bold font-display mt-1 ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  {milestones[selectedMilestone].title}
                </h3>
              </div>

              <span className={`px-3.5 py-1.5 rounded-full text-xs font-mono font-bold ${
                isLight ? 'bg-amber-100 text-amber-800 border border-amber-300' : 'bg-amber-950/50 text-amber-400 border border-amber-800/40'
              }`}>
                {milestones[selectedMilestone].kpi}
              </span>
            </div>

            <p className={`text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700' : 'text-zinc-300'
            }`}>
              {milestones[selectedMilestone].desc}
            </p>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-4 pt-5 border-t ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => onOpenContactModal('Request SADC Node Integration & Telemetry')}
            className="neu-btn-amber px-6 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 cursor-pointer"
          >
            <span>Deploy SADC Node</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => onNavigate('work')}
            className={`px-5 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 cursor-pointer ${
              isLight ? 'neu-btn-light text-slate-900' : 'neu-btn-dark text-zinc-200'
            }`}
          >
            <ShieldCheck className="w-4 h-4 text-amber-500" />
            <span>Review Proof &amp; Deployments</span>
          </button>
        </div>

        <button
          onClick={() => onNavigate('technology')}
          className="text-xs font-mono font-bold text-amber-500 hover:text-amber-400 transition-colors py-2 px-3 flex items-center gap-1.5 cursor-pointer"
        >
          <span>SADC Interconnect Protocol</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
