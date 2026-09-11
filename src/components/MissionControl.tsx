import React from 'react';
import { 
  Compass, 
  Shield, 
  BookOpen, 
  Award, 
  CheckCircle2, 
  Palette, 
  FileText,
  ExternalLink,
  Layers
} from 'lucide-react';

export const MissionControl: React.FC = () => {
  const brandColors = [
    { name: 'Navy Primary', hex: '#070A40', text: '#FFFFFF', usage: 'Headlines, primary brand surfaces' },
    { name: 'Red Accent', hex: '#E63946', text: '#FFFFFF', usage: 'Signal waves, key highlights, CTAs' },
    { name: 'Cyan Accent', hex: '#00BFFF', text: '#070A40', usage: 'Shield base, interactive links, highlights' },
    { name: 'Light Grey', hex: '#F2F2F2', text: '#070A40', usage: 'Backgrounds, cards, callouts' },
    { name: 'Dark Grey', hex: '#6B7280', text: '#FFFFFF', usage: 'Secondary text, muted labels' }
  ];

  const constitutionArticles = [
    {
      num: 'Article I',
      title: 'Human CEO Sovereignty & Strategic Vision',
      desc: 'The Human CEO (Jack Mlusu) is the ultimate fiduciary authority. All autonomous agent hierarchies derive their operating mandates, resource allocations, and operational boundaries from CEO directives.'
    },
    {
      num: 'Article II',
      title: 'Canonical Tool Vocabulary (7 OpenCode Tools)',
      desc: 'All 144 agents operate strictly within the canonical toolset: read, edit, grep, list, bash, webfetch, and task. Unknown or deprecated tools are strictly rejected by the ToolRunner at runtime.'
    },
    {
      num: 'Article III',
      title: '5-Tier Constitutional Approval Gate',
      desc: 'Privileged operations follow strict multi-party authorization: Tier 1 (Auto), Tier 2 (Single Manager), Tier 3 (Dual CTO+CISO), Tier 4 (Executive C-Suite), and Tier 5 (CEO exclusive for capital > $10k).'
    },
    {
      num: 'Article IV',
      title: 'Immutable Audit Trail & MessageBus',
      desc: 'All dispatches, escalations, task completions, and permission elevations are recorded in JSONL streams. The orchestrator inbox (.opencode/inbox.json) enforces deterministic task state transitions.'
    },
    {
      num: 'Article V',
      title: 'Multi-Tier Model Routing & Cost Efficiency',
      desc: 'Autonomous tasks route dynamically across Tier 1 (Fast Big Pickle / Flash), Tier 2 (Standard), and Tier 3 (Reasoning), ensuring LLM spend remains below 1% of the annual budget cap.'
    },
    {
      num: 'Article VI',
      title: 'Regional AI Thought Leadership (Pharos)',
      desc: 'LightSpeed Holdings champions sovereign, ethical, and enterprise-grade Agentic AI across Malawi and the SADC region through policy development, talent upskilling, and enterprise transformation.'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-[#070a40] via-[#0c143d] to-[#070a24] p-6 rounded-2xl border border-[#1e2a58] shadow-lg shadow-black/40">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-[#00bfff]/20 text-[#00bfff] border border-[#00bfff]/40">
                CORPORATE CONSTITUTION & BRAND
              </span>
              <span className="text-xs text-slate-400">Est. 2026</span>
            </div>
            <h2 className="text-2xl font-black text-white mt-1.5 tracking-tight font-display">
              LIGHTSPEED HOLDINGS LIMITED
            </h2>
            <p className="text-justify text-sm font-semibold text-[#00bfff] tracking-widest mt-0.5">
              ASPIRE. ACT. ACHIEVE.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#00bfff]/30 to-[#e63946]/30 border border-[#00bfff]/50 flex items-center justify-center shadow-lg shadow-[#00bfff]/20">
              <Shield className="w-6 h-6 text-[#00bfff]" />
            </div>
          </div>
        </div>
      </div>

      {/* Grid: Constitution & Brand Tokens */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Constitution */}
        <div className="lg:col-span-2 bg-[#0b102f] border border-[#1b2554] rounded-2xl p-5 shadow-md">
          <div className="flex items-center justify-between pb-3 border-b border-[#1b2554] mb-4">
            <div className="flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-[#00bfff]" />
              <h3 className="text-sm font-bold text-white tracking-wider font-display">
                Autonomous Company Constitution & Core Directives
              </h3>
            </div>
            <span className="text-xs text-slate-400 font-mono">v2.4 Ratified</span>
          </div>

          <div className="space-y-3.5">
            {constitutionArticles.map((art) => (
              <div key={art.num} className="p-3.5 rounded-xl bg-[#0e163b] border border-[#1e2a58] text-xs">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-bold text-[#00bfff] tracking-wider bg-[#070a40] px-1.5 py-0.2 rounded border border-[#00bfff]/30">
                    {art.num}
                  </span>
                  <h4 className="font-bold text-white text-xs">{art.title}</h4>
                </div>
                <p className="text-justify text-slate-300 leading-relaxed mt-1">
                  {art.desc}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Brand System & Tokens */}
        <div className="space-y-6">
          {/* Brand Colors */}
          <div className="bg-[#0b102f] border border-[#1b2554] rounded-2xl p-5 shadow-md">
            <div className="flex items-center gap-2 pb-3 border-b border-[#1b2554] mb-4">
              <Palette className="w-4 h-4 text-[#e63946]" />
              <h3 className="text-sm font-bold text-white tracking-wider font-display">
                Design System Color Tokens
              </h3>
            </div>

            <div className="space-y-2.5">
              {brandColors.map((color) => (
                <div key={color.name} className="flex items-center gap-3 p-2 rounded-xl bg-[#0e163b] border border-[#1e2a58]">
                  <div
                    className="w-8 h-8 rounded-lg border border-white/20 shadow-sm flex-shrink-0"
                    style={{ backgroundColor: color.hex }}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-white text-xs">{color.name}</span>
                      <span className="font-mono text-[10px] text-slate-400">{color.hex}</span>
                    </div>
                    <p className="text-justify text-[10px] text-slate-400 truncate">{color.usage}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Core Corporate Information */}
          <div className="bg-[#0b102f] border border-[#1b2554] rounded-2xl p-5 shadow-md text-xs space-y-3">
            <h3 className="text-sm font-bold text-white tracking-wider font-display pb-2 border-b border-[#1b2554]">
              Corporate Registry Info
            </h3>

            <div className="flex justify-between text-slate-400">
              <span>Legal Entity:</span>
              <span className="font-semibold text-white">LIGHTSPEED HOLDINGS LIMITED</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Headquarters:</span>
              <span className="font-semibold text-white">Lilongwe, Malawi</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>CEO & Founder:</span>
              <span className="font-semibold text-[#00bfff]">Jack Mlusu</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Agentic Fleet:</span>
              <span className="font-semibold text-emerald-400">144 Active Manifests</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Governance Stack:</span>
              <span className="font-semibold text-slate-200">OpenCode v2 + HITL</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
