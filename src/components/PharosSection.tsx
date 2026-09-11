import React from 'react';
import { Download } from 'lucide-react';

interface PharosSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

const whitepapers = [
  {
    tome: 'TOME I',
    greekNumeral: 'A // 01',
    tag: 'EXECUTIVE DISPATCH',
    title: 'Collapsing Strategy into Real-Time Execution',
    epigraph: 'Why consulting slide decks fail, and what replaces them.',
    desc: 'Why conventional management consulting decks fail to deliver, and how closed-loop systems connect boardroom strategy with real-time operational delivery.',
    author: 'LightSpeed Advisory Practice',
    readTime: '12 min read',
    downloads: '1,420 Executive Downloads',
    focus: 'Strategy & Architecture'
  },
  {
    tome: 'TOME II',
    greekNumeral: 'B // 02',
    tag: 'ON-SITE COMPUTE',
    title: 'Air-Gapped Data Systems & Regional Compliance',
    epigraph: 'On-soil compute that meets strict regulatory requirements without sacrificing AI performance.',
    desc: 'How to build on-site, air-gapped AI clusters that comply with national banking acts and SADC data residency mandates while maintaining full reasoning capabilities.',
    author: 'Systems & Infrastructure Group',
    readTime: '15 min read',
    downloads: '980 Executive Downloads',
    focus: 'On-Premises Architecture'
  },
  {
    tome: 'TOME III',
    greekNumeral: 'C // 03',
    tag: 'SYSTEMS ENGINEERING',
    title: 'Controlling Multi-Agent Systems with Cryptographic Gates',
    epigraph: 'Hard bounds and human-in-the-loop gates that prevent agent drift.',
    desc: 'How to constrain autonomous AI agents to specific tools, rate limits, and cryptographic human approval gates so every action is bounded and verified.',
    author: 'AI Engineering Division',
    readTime: '18 min read',
    downloads: '2,150 Technical Downloads',
    focus: 'Agent Verification'
  },
  {
    tome: 'TOME IV',
    greekNumeral: 'D // 04',
    tag: 'REGULATORY TREATISE',
    title: 'High-Assurance Compute for Central Banks',
    epigraph: 'Provable settlement rails and AML verification under strict jurisdictional requirements.',
    desc: 'How to build provable cryptographic audit trails for automated currency issuance, letters of credit, and cross-border customs declarations.',
    author: 'Regulatory Institute',
    readTime: '20 min read',
    downloads: '1,840 Central Bank Downloads',
    focus: 'Monetary & Audit Proofs'
  }
];

export const PharosSection: React.FC<PharosSectionProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  return (
    <section id="publications" className={`py-28 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t relative overflow-hidden ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      {/* Subtle stone masonry background pattern */}
      <div className="absolute inset-0 pharos-stone-masonry pointer-events-none opacity-40" />

      {/* Pharos Header */}
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

          <p className={`text-justify text-sm sm:text-base leading-relaxed max-w-3xl ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Our publication series gives boards, central banks, and government ministries clear, actionable guidance on AI strategy, data residency, and governance. Each piece is written for executives, not engineers, and focuses on what works in production, not what sounds good on a slide.
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
                  <span className="text-zinc-400">Isle Coordinates:</span>
                  <span className="font-bold text-amber-400">31.2140 N, 29.8850 E</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-400">Optical Reach:</span>
                  <span className="font-bold text-emerald-400">300 Stadia (~55 km)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-400">Emission Spectrum:</span>
                  <span className="font-bold text-orange-400">589nm Solar Amber</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-400">Guiding Purpose:</span>
                  <span className={`font-bold ${isLight ? 'text-slate-800' : 'text-white'}`}>Board-Level Clarity</span>
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
                <span className="font-semibold text-zinc-400">{wp.readTime}</span>
              </div>

              {/* Subtitle & Tag */}
              <div className="flex items-center justify-between text-[10px] font-mono">
                <span className="text-orange-500 font-bold">{wp.tag}</span>
                <span className="text-zinc-400">{wp.greekNumeral}</span>
              </div>

              {/* Title */}
              <h3 className={`text-base sm:text-lg font-bold tracking-tight leading-snug group-hover:text-amber-500 transition-colors ${
                isLight ? 'text-slate-900' : 'text-zinc-100'
              }`}>
                {wp.title}
              </h3>

              {/* Epigraph / Quote */}
              <blockquote className="text-xs italic border-l-2 pl-3 py-0.5 border-amber-400 text-zinc-400">
                "{wp.epigraph}"
              </blockquote>

              {/* Detailed Description */}
              <p className="text-justify text-xs leading-relaxed text-zinc-400">
                {wp.desc}
              </p>
            </div>

            {/* Treatise Footer */}
            <div className={`pt-4 border-t flex items-center justify-between text-xs ${
              isLight ? 'border-black/10' : 'border-white/10'
            }`}>
              <span className="text-[10px] font-mono font-medium text-zinc-400">
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
  );
};
