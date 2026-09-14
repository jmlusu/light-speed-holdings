import React, { useState } from 'react';
import {
  FileText,
  BookOpen,
  Globe2,
  Brain,
  ArrowRight,
  Download,
  ExternalLink,
  Sparkles,
  Bookmark,
  Compass,
  ShieldCheck,
  Layers,
  Radio,
  Eye,
  Flame,
  Anchor,
  ArrowUpRight,
  CheckCircle2,
  ChevronRight,
  Landmark,
  FileCheck
} from 'lucide-react';
import {
  StatusLedPip,
  MachineScrewHead,
  AcousticVentGrille,
  ChassisPanel
} from './TactileHardwareElements';
import pharosBeaconLake from '../assets/images/pharos_beacon_lake_1789078282970.jpg';
import { AgenticAiManifestoModal } from './AgenticAiManifestoModal';

interface PharosSectionProps {
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const PharosSection: React.FC<PharosSectionProps> = ({
  onOpenContactModal,
  theme = 'dark'
}) => {
  const [activeTab, setActiveTab] = useState<'doctrine' | 'treatises' | 'research' | 'dispatches'>('doctrine');
  const [isManifestoOpen, setIsManifestoOpen] = useState<boolean>(false);
  const isLight = theme === 'light';

  const tomes = [
    {
      tome: 'TOME I',
      greekNumeral: 'Α // 01',
      tag: 'EXECUTIVE THESIS',
      title: 'The AI-Native Enterprise: Collapsing Strategy into Real-Time Execution',
      epigraph: 'Guiding enterprise navigation past the shoals of static consulting slide decks into dynamic computable topologies.',
      desc: 'Why conventional management consulting slide decks fail to deliver, and how closed-loop cognitive topologies bridge boardroom intent with real-time operational delivery.',
      author: 'LightSpeed Fiduciary Practice',
      readTime: '12 min read',
      classification: 'RESTRICTED // BOARD-LEVEL BRIEF',
      downloads: '1,420 Executive Downloads',
      focus: 'Autonomous Strategy Topology'
    },
    {
      tome: 'TOME II',
      greekNumeral: 'Β // 02',
      tag: 'SOVEREIGN INTELLIGENCE',
      title: 'Sovereign Data Fabrics & Regional Compliance in the SADC Corridor',
      epigraph: 'Illuminating on-soil air-gapped compute architectures that withstand regulatory and data residency storms.',
      desc: 'Architecting air-gapped, on-soil inference clusters that comply strictly with national banking acts and SADC regional data residency mandates without sacrificing frontier reasoning capabilities.',
      author: 'Sovereign Systems & Infrastructure Group',
      readTime: '15 min read',
      classification: 'SOVEREIGN // REGIONAL POLICY',
      downloads: '980 Executive Downloads',
      focus: 'On-Premises African Sovereignty'
    },
    {
      tome: 'TOME III',
      greekNumeral: 'Γ // 03',
      tag: 'SYSTEMS ARCHITECTURE',
      title: 'Deterministic Fiduciary Controls in Multi-Agent Swarms',
      epigraph: 'Mathematical bounds and cryptographic human-in-the-loop gates preventing agentic drift and hallucination.',
      desc: 'A mathematical and architectural specification for bounding autonomous AI agents to canonical tools, rate limits, and cryptographic human-in-the-loop approval gates.',
      author: 'AI Engineering Division',
      readTime: '18 min read',
      classification: 'TECHNICAL SPEC // SPEC-902',
      downloads: '2,150 Technical Downloads',
      focus: 'Agentic DAG Verification'
    },
    {
      tome: 'TOME IV',
      greekNumeral: 'Δ // 04',
      tag: 'REGULATORY SPECIFICATION',
      title: 'The Alexandria Protocol: Air-Gapped High-Assurance Compute for Central Banks',
      epigraph: 'Deterministic settlement rails and anti-money laundering verification under sovereign jurisdictional bounds.',
      desc: 'Formulating provable cryptographic audit trails for automated foreign currency issuance, letters of credit, and cross-border customs declarations.',
      author: 'Sovereign Regulatory Institute',
      readTime: '20 min read',
      classification: 'CONFIDENTIAL // MONETARY CORE',
      downloads: '1,840 Central Bank Downloads',
      focus: 'Monetary & Fiduciary Proofs'
    }
  ];

  const articles = [
    {
      title: 'Why African Companies Should Skip the Copilot Era',
      category: 'Agentic AI Strategy',
      readTime: '6 min read',
      author: 'Jack Mlusu, Founder & CEO',
      excerpt: 'While Western enterprises retrofit legacy SaaS with simple chat copilots, African enterprises have an unprecedented leapfrogging opportunity to build fully agentic, autonomous AI operating models directly from the bedrock.',
      date: 'September 2026',
      status: 'emerald' as const
    },
    {
      title: 'The Rise of the AI-Native Enterprise in Africa',
      category: 'Enterprise Architecture',
      readTime: '8 min read',
      author: 'LightSpeed Holdings Research',
      excerpt: 'How collapsing manual organizational hierarchies into sub-agent swarms creates 10x operational throughput for growth enterprises in Malawi and across the SADC economic corridor.',
      date: 'August 2026',
      status: 'emerald' as const
    },
    {
      title: 'What Agentic AI Means for African Governments & E-Gov',
      category: 'Sovereign AI Policy',
      readTime: '10 min read',
      author: 'Pharos Policy Track',
      excerpt: 'Evaluating human-in-the-loop (HITL) risk tiering, Chichewa language preservation, and SADC digital model laws in official national strategy submissions.',
      date: 'July 2026',
      status: 'emerald' as const
    }
  ];

  const researchReports = [
    {
      title: '2026–2027 SADC AI Readiness & Infrastructure Report',
      type: 'Macro Report',
      pages: '48 Pages PDF',
      summary: 'Comprehensive analysis of compute infrastructure, mobile money APIs, legal model laws, and talent density across 16 SADC member states.',
      badge: 'SADC Operator Edition',
      classification: 'SOVEREIGN // DECLASSIFIED'
    },
    {
      title: 'The African Agentic AI Use-Case Index',
      type: 'Technical Monograph',
      pages: '32 Pages PDF',
      summary: 'Cataloguing 50+ field-proven deployment patterns across AgriTech, FinTech, E-Gov, and Healthcare in East & Southern Africa.',
      badge: 'Field Validated',
      classification: 'TELEMETRY // INDEX-04'
    }
  ];

  return (
    <section id="pharos" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto font-sans">

      {/* Title & Classification */}
      <div className="text-center max-w-4xl mx-auto mb-12">
        <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider mb-5 border select-none transition-colors">
          <StatusLedPip status="emerald" isLight={isLight} />
          <span className={`text-[11px] font-mono tracking-widest ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
            PHAROS STATION // OPTICAL BEACON &amp; CORE PHILOSOPHY
          </span>
          <span className="hidden sm:inline text-zinc-500">•</span>
          <span className="hidden sm:inline text-[10px] text-amber-500 font-mono">
            EST. ALEXANDRIA c. 280 BC // LILONGWE HQ 2026
          </span>
        </div>

        <h1 className={`text-2xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight font-display mb-6 leading-normal sm:leading-tight break-words ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          Pharos: <span className="inline-block pb-1.5 text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">LightSpeed Insights</span>
        </h1>

        <p className={`text-base sm:text-lg leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
          Erected on the limestone bedrock of the island of Pharos in Alexandria, Egypt, the ancient Lighthouse stood as humanity's supreme beacon of guidance—projecting radiant light across treacherous shoals into safe harbor. In today's turbulent storm of AI hype, ephemeral copilots, and predatory SaaS leakages, <strong className="text-amber-500 font-bold">PHAROS</strong> anchors our core thesis: providing boards, central banks, and sovereign institutions with mathematical clarity, operational permanence, and dedicated operator-partnership.
        </p>
      </div>

      {/* Strategic Infographic Banner: Pharos Sovereign Beacon */}
      <div className="relative rounded-3xl overflow-hidden mb-12 border border-zinc-800 shadow-2xl group">
        <img
          src={pharosBeaconLake}
          alt="Pharos Sovereign Optical Beacon"
          className="w-full h-[280px] sm:h-[400px] object-cover brightness-[0.75] contrast-[1.1] transition-transform duration-700 group-hover:scale-105"
          referrerPolicy="no-referrer"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent p-6 sm:p-8 flex flex-col justify-end">
          <div className="flex items-center gap-2 mb-1">
            <StatusLedPip status="amber" isLight={isLight} />
            <span className="text-[10px] font-mono text-amber-400 font-bold uppercase tracking-widest">[ PHAROS STATION // OPTICAL TELEMETRY ]</span>
          </div>
          <h2 className="text-xl sm:text-3xl font-bold font-display text-white">Sovereign Beacon &amp; Legal Framework Treatise Repository</h2>
          <p className="text-xs sm:text-sm text-zinc-300 font-mono mt-1">Guiding regional enterprise navigation past ephemeral AI hype into verifiable, air-gapped computational permanence.</p>
        </div>
      </div>

      {/* FEATURED MANIFESTO BANNER */}
      <div className={`mb-12 p-6 sm:p-8 rounded-3xl border relative overflow-hidden transition-all ${
        isLight ? 'bg-gradient-to-r from-amber-50 via-orange-50 to-amber-100 border-amber-300 shadow-xl' : 'bg-gradient-to-r from-zinc-950 via-amber-950/30 to-zinc-950 border-amber-500/40 shadow-2xl'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 relative z-10">
          <div className="space-y-3 max-w-3xl">
            <div className="flex items-center gap-2.5">
              <span className="px-3 py-1 rounded-full text-[10px] font-mono font-bold uppercase tracking-widest bg-amber-500 text-slate-950 shadow-sm">
                FEATURED EXECUTIVE MANIFESTO
              </span>
              <span className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-amber-300'}`}>
                POLICY TRACK // MALAWI &amp; SADC 2026
              </span>
            </div>

            <h2 className={`text-xl sm:text-2xl lg:text-3xl font-extrabold font-display leading-tight ${
              isLight ? 'text-slate-900' : 'text-zinc-100'
            }`}>
              What Agentic AI Company-Building Actually Means for Malawi &amp; SADC
            </h2>

            <p className={`text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
              A manifesto for a governance-first approach to autonomous AI in the region. Addressing the 5-tier human-in-the-loop approvals, National AI Strategy alignment, and the Four Reservations (Trust-by-Engineering).
            </p>

            <div className="flex flex-wrap items-center gap-4 text-xs font-mono text-amber-500">
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>Human CEO Reviewed</span>
              </span>
              <span>•</span>
              <span>144 Agent Architecture</span>
              <span>•</span>
              <span>1,850 Words Full Policy Text</span>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0 w-full lg:w-auto">
            <button
              onClick={() => setIsManifestoOpen(true)}
              className="px-6 py-3.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 flex items-center justify-center gap-2 active:scale-95 cursor-pointer"
            >
              <FileCheck className="w-4 h-4" />
              <span>Read Full Manifesto</span>
            </button>
            <button
              onClick={() => onOpenContactModal('Request Executive Briefing on Agentic AI Manifesto')}
              className={`px-5 py-3.5 rounded-xl border font-bold font-mono text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-2 cursor-pointer ${
                isLight ? 'neu-btn-light text-slate-800' : 'neu-btn-dark text-zinc-200'
              }`}
            >
              <span>Request Briefing</span>
            </button>
          </div>
        </div>
      </div>

      {/* Selector Hardware Tabs */}
      <div className="flex justify-center mb-10 overflow-x-auto pb-2 scrollbar-none">
        <div className={`p-1.5 rounded-2xl border inline-flex gap-1.5 sm:gap-2 ${
          isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
        }`}>
          <button
            onClick={() => setActiveTab('doctrine')}
            className={`flex items-center gap-2 px-4 sm:px-6 py-2.5 rounded-xl text-xs font-mono font-bold uppercase transition-all whitespace-nowrap ${
              activeTab === 'doctrine'
                ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20'
                : isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Flame className="w-3.5 h-3.5" />
            <span>The Alexandria Thesis</span>
          </button>

          <button
            onClick={() => setActiveTab('treatises')}
            className={`flex items-center gap-2 px-4 sm:px-6 py-2.5 rounded-xl text-xs font-mono font-bold uppercase transition-all whitespace-nowrap ${
              activeTab === 'treatises'
                ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20'
                : isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>Pharos Treatises (Tomes I–IV)</span>
          </button>

          <button
            onClick={() => setActiveTab('research')}
            className={`flex items-center gap-2 px-4 sm:px-6 py-2.5 rounded-xl text-xs font-mono font-bold uppercase transition-all whitespace-nowrap ${
              activeTab === 'research'
                ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20'
                : isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Radio className="w-3.5 h-3.5" />
            <span>SADC Sovereign Reports</span>
          </button>

          <button
            onClick={() => setActiveTab('dispatches')}
            className={`flex items-center gap-2 px-4 sm:px-6 py-2.5 rounded-xl text-xs font-mono font-bold uppercase transition-all whitespace-nowrap ${
              activeTab === 'dispatches'
                ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20'
                : isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Executive Dispatches</span>
          </button>
        </div>
      </div>

      {/* TAB 1: THE ALEXANDRIA THESIS & CORE DOCTRINE */}
      {activeTab === 'doctrine' && (
        <div className="space-y-12">

          {/* Hero Lore + Optical Station Telemetry */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">

            {/* Philosophical Narrative Card */}
            <div className={`lg:col-span-7 p-8 sm:p-10 rounded-3xl border relative overflow-hidden flex flex-col justify-between ${
              isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
            }`}>
              <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
              <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />

              <div className="space-y-5">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/30 text-xs font-mono font-bold">
                  <Compass className="w-3.5 h-3.5" />
                  <span>FOUNDATIONAL THESIS // 280 BC – PRESENT</span>
                </div>

                <h3 className={`text-2xl sm:text-3xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Reclaiming the African Legacy of the Guiding Beacon
                </h3>

                <div className={`space-y-4 text-sm sm:text-base leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-300'}`}>
                  <p>
                    Modern technological discourse frequently presumes that African enterprise must always be the consumer of foreign digital frameworks. But history remembers that the ancient world’s supreme navigational achievement—the <strong>Pharos of Alexandria</strong>—was engineered on African soil. Rising over 100 meters above the Mediterranean, its bronze-reflected flame illuminated safe passage for international fleets across submerged limestone shoals.
                  </p>
                  <p>
                    Today, the enterprise landscape is adrift in a different kind of fog: ephemeral chatbot copilots, vendor lock-in, uncalibrated hallucinations, and offshore data extraction. <strong>LightSpeed Holdings Limited</strong> exists to reject passive consumption. We do not operate as an ivory-tower observer or academic authority; we operate as an <strong>AI-Native Operator &amp; Partner</strong>.
                  </p>
                  <p className="border-l-2 border-amber-500 pl-4 italic text-amber-500 font-medium">
                    "We do not sell ephemeral consulting slides. We man the beacon, fuel the furnace, calibrate the telemetry, and steer alongside our partners through uncharted technological waters into sovereign autonomous execution."
                  </p>
                </div>
              </div>

              <div className={`mt-8 pt-6 border-t flex flex-wrap items-center justify-between gap-4 text-xs font-mono ${
                isLight ? 'border-slate-300 text-slate-600' : 'border-zinc-800 text-zinc-400'
              }`}>
                <div className="flex items-center gap-2">
                  <StatusLedPip status="emerald" isLight={isLight} />
                  <span>DOCTRINE: DETERMINISTIC CLARITY</span>
                </div>
                <button
                  onClick={() => onOpenContactModal('Discuss the Pharos Doctrine with Leadership')}
                  className="text-amber-500 font-extrabold hover:text-amber-400 flex items-center gap-1.5 uppercase tracking-wider text-xs"
                >
                  <span>Engage Leadership on Pharos</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Lake Malawi Optical Station Telemetry */}
            <div className={`lg:col-span-5 p-6 sm:p-7 rounded-3xl border relative overflow-hidden flex flex-col justify-between ${
              isLight ? 'bg-white/90 border-slate-300 text-slate-800 shadow-xl' : 'bg-zinc-950/80 border-amber-500/30 text-zinc-300 shadow-2xl'
            }`}>
              <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
              <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />

              <div className="space-y-4">
                {/* Pharos Beacon Optical Station Telemetry Display */}
                <div className="relative rounded-2xl overflow-hidden border border-amber-500/30 p-5 bg-gradient-to-br from-[#1a0507] via-[#160808] to-[#040403] shadow-inner flex flex-col justify-between min-h-[190px]">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/30 flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-ping" />
                      589nm SODIUM OPTICAL BEAM
                    </span>
                    <span className="text-[9px] font-mono text-zinc-400">LAT: 14.004° S, 34.301° E</span>
                  </div>

                  <div className="my-4">
                    <div className="h-1.5 w-full bg-black/60 rounded-full overflow-hidden border border-amber-500/30">
                      <div className="h-full bg-gradient-to-r from-amber-500 to-amber-300 w-4/5 animate-pulse" />
                    </div>
                    <div className="flex items-center justify-between text-[10px] font-mono text-amber-300/80 mt-1">
                      <span>BEAM RANGE: 42 KM (LAKE MALAWI)</span>
                      <span>DIVERGENCE: 0.4 MRAD</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-[11px] font-mono text-amber-300 border-t border-amber-500/20 pt-2">
                    <span className="font-bold flex items-center gap-1.5">
                      LAKE MALAWI // PHAROS STATION
                    </span>
                    <span className="text-emerald-400 text-[10px]">
                      STATUS: EMITTING
                    </span>
                  </div>
                </div>

                {/* Telemetry Details */}
                <div className="space-y-3 pt-2">
                  <div className="flex items-center justify-between border-b border-amber-500/20 pb-2">
                    <div className="flex items-center gap-2">
                      <StatusLedPip status="emerald" isLight={isLight} />
                      <span className="font-mono text-xs font-bold tracking-wider text-amber-500">
                        BEACON SPECIFICATION RIG
                      </span>
                    </div>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold">
                      RADIANT // ONLINE
                    </span>
                  </div>

                  <div className="space-y-2 text-xs font-mono">
                    <div className={`flex justify-between p-2 rounded-lg ${isLight ? 'bg-slate-100' : 'bg-zinc-900/80'}`}>
                      <span className="text-zinc-500">Ancient Archetype:</span>
                      <span className="font-bold text-amber-500">Pharos of Alexandria (280 BC)</span>
                    </div>
                    <div className={`flex justify-between p-2 rounded-lg ${isLight ? 'bg-slate-100' : 'bg-zinc-900/80'}`}>
                      <span className="text-zinc-500">Headquarters Coordinates:</span>
                      <span className="font-bold text-emerald-500">13.9899° S, 33.7741° E (Lilongwe)</span>
                    </div>
                    <div className={`flex justify-between p-2 rounded-lg ${isLight ? 'bg-slate-100' : 'bg-zinc-900/80'}`}>
                      <span className="text-zinc-500">Sovereign Jurisdiction:</span>
                      <span className="font-bold text-amber-400">Malawi &amp; 16 SADC States</span>
                    </div>
                    <div className={`flex justify-between p-2 rounded-lg ${isLight ? 'bg-slate-100' : 'bg-zinc-900/80'}`}>
                      <span className="text-zinc-500">Role in Enterprise:</span>
                      <span className="font-bold text-amber-500">AI-Native Operator &amp; Partner</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-amber-500/20 flex items-center justify-between">
                <span className="text-[11px] font-mono text-zinc-400">Fiduciary Telemetry Core</span>
                <button
                  onClick={() => onOpenContactModal('Request Telemetry Rig Specification')}
                  className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold font-mono text-xs uppercase tracking-wider transition-all shadow-md active:scale-95"
                >
                  Request Dossier
                </button>
              </div>
            </div>
          </div>

          {/* The Four Pillars of the Pharos Doctrine */}
          <div className="space-y-6">
            <div className="text-center max-w-2xl mx-auto">
              <h3 className={`text-2xl sm:text-3xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                The Four Pillars of the Pharos Doctrine
              </h3>
              <p className={`text-sm mt-2 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                How the architecture of the ancient wonder governs our operational engagements today.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

              {/* Pillar 1 */}
              <div className={`p-6 rounded-3xl border relative overflow-hidden space-y-3 ${
                isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
              }`}>
                <div className="w-10 h-10 rounded-2xl bg-amber-500/10 text-amber-500 border border-amber-500/30 flex items-center justify-center">
                  <Eye className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono text-amber-500 font-bold tracking-widest uppercase">PILLAR I // THE MIRROR</span>
                <h4 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Unflinching Clarity
                </h4>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Like the vast bronze parabolic mirrors of Alexandria, we reject opaque black-box systems. Every agent workflow produces deterministic DAG telemetry, cryptographic audit logs, and measurable financial ROI.
                </p>
              </div>

              {/* Pillar 2 */}
              <div className={`p-6 rounded-3xl border relative overflow-hidden space-y-3 ${
                isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
              }`}>
                <div className="w-10 h-10 rounded-2xl bg-amber-500/10 text-amber-500 border border-amber-500/30 flex items-center justify-center">
                  <Anchor className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono text-amber-500 font-bold tracking-widest uppercase">PILLAR II // THE HARBOR</span>
                <h4 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Safe Sovereign Harbor
                </h4>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Navigating enterprise data away from offshore extraction into sovereign, air-gapped on-soil compute clusters that respect national data residency laws and institutional privacy.
                </p>
              </div>

              {/* Pillar 3 */}
              <div className={`p-6 rounded-3xl border relative overflow-hidden space-y-3 ${
                isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
              }`}>
                <div className="w-10 h-10 rounded-2xl bg-amber-500/10 text-amber-500 border border-amber-500/30 flex items-center justify-center">
                  <Layers className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono text-amber-500 font-bold tracking-widest uppercase">PILLAR III // BEDROCK</span>
                <h4 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Architectural Permanence
                </h4>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  The ancient Pharos stood for over a millennium because its foundations were locked into coastal bedrock. We construct agentic operating systems designed to outlast transient tech hype cycles.
                </p>
              </div>

              {/* Pillar 4 */}
              <div className={`p-6 rounded-3xl border relative overflow-hidden space-y-3 ${
                isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
              }`}>
                <div className="w-10 h-10 rounded-2xl bg-amber-500/10 text-amber-500 border border-amber-500/30 flex items-center justify-center">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono text-amber-500 font-bold tracking-widest uppercase">PILLAR IV // THE WATCH</span>
                <h4 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Operator &amp; Partner
                </h4>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  We never abandon our clients to raw software. As an AI-Native Operator &amp; Partner, we co-engineer, govern, calibrate, and scale autonomous workloads alongside your leadership.
                </p>
              </div>

            </div>
          </div>

        </div>
      )}

      {/* TAB 2: THE 4 PHAROS TREATISES (TOMES I - IV) */}
      {activeTab === 'treatises' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {tomes.map((tome, idx) => (
            <div
              key={idx}
              className={`p-7 sm:p-8 rounded-3xl border relative overflow-hidden flex flex-col justify-between space-y-6 transition-all group ${
                isLight ? 'chassis-milled-light hover:border-amber-500' : 'chassis-milled-dark hover:border-amber-500/50'
              }`}
            >
              <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
              <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />

              <div className="space-y-4">
                <div className="flex items-center justify-between text-xs font-mono border-b pb-3 border-amber-500/20">
                  <span className="px-2.5 py-0.5 rounded-full bg-amber-500/15 text-amber-500 border border-amber-500/30 font-bold">
                    {tome.tome} • {tome.greekNumeral}
                  </span>
                  <span className={isLight ? 'text-slate-500' : 'text-zinc-400'}>{tome.readTime}</span>
                </div>

                <div className="text-[11px] font-mono text-amber-500 font-bold uppercase tracking-wider">
                  {tome.tag} // {tome.focus}
                </div>

                <h3 className={`text-xl sm:text-2xl font-bold font-display leading-snug group-hover:text-amber-500 transition-colors ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  {tome.title}
                </h3>

                <p className={`text-xs italic border-l-2 border-amber-500 pl-3 leading-relaxed ${
                  isLight ? 'text-slate-700 font-medium' : 'text-amber-200/90'
                }`}>
                  "{tome.epigraph}"
                </p>

                <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  {tome.desc}
                </p>
              </div>

              <div className="space-y-3 pt-4 border-t border-amber-500/20">
                <div className={`p-2.5 rounded-xl border flex items-center justify-between text-[11px] font-mono ${
                  isLight ? 'flight-deck-well-light text-slate-700' : 'flight-deck-well-dark text-zinc-400'
                }`}>
                  <span>CLASSIFICATION:</span>
                  <span className="text-amber-500 font-bold">{tome.classification}</span>
                </div>

                <div className="flex items-center justify-between pt-1">
                  <span className="text-[11px] font-mono text-zinc-400">{tome.downloads}</span>
                  <button
                    onClick={() => onOpenContactModal(`Request Pharos Treatise: ${tome.tome} - ${tome.title}`)}
                    className="flex items-center gap-2 px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold font-mono text-xs uppercase tracking-wider transition-all shadow-md active:scale-95"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Request Treatise PDF</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* TAB 3: SADC SOVEREIGN RESEARCH REPORTS */}
      {activeTab === 'research' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {researchReports.map((rep, idx) => (
            <div
              key={idx}
              className={`p-8 rounded-3xl border relative overflow-hidden space-y-5 ${
                isLight ? 'chassis-milled-light border-amber-500/50' : 'chassis-milled-dark border-amber-500/40'
              }`}
            >
              <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
              <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
              <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
              <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

              <div className="flex items-center justify-between pt-1">
                <div className="flex items-center gap-2">
                  <StatusLedPip status="emerald" isLight={isLight} />
                  <span className="px-3 py-1 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/30 text-xs font-mono font-bold">
                    {rep.badge}
                  </span>
                </div>
                <span className="text-xs font-mono text-zinc-400">{rep.pages}</span>
              </div>

              <h3 className={`text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                {rep.title}
              </h3>
              <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-300'}`}>
                {rep.summary}
              </p>

              <div className={`p-3.5 rounded-xl border flex items-center justify-between text-xs font-mono ${
                isLight ? 'flight-deck-well-light text-slate-700' : 'flight-deck-well-dark text-zinc-400'
              }`}>
                <span>CLASSIFICATION:</span>
                <span className="text-amber-500 font-bold">{rep.classification}</span>
              </div>

              <div className={`pt-4 border-t flex items-center justify-between ${
                isLight ? 'border-slate-300' : 'border-zinc-800'
              }`}>
                <span className="text-xs font-mono text-zinc-400">LightSpeed Holdings Monograph</span>
                <button
                  onClick={() => onOpenContactModal(`Download ${rep.title}`)}
                  className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 active:scale-95"
                >
                  <Download className="w-4 h-4" />
                  <span>Request Full PDF</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* TAB 4: EXECUTIVE DISPATCHES */}
      {activeTab === 'dispatches' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {articles.map((art, idx) => (
            <div
              key={idx}
              className={`p-6 sm:p-7 rounded-3xl border relative overflow-hidden flex flex-col justify-between transition-all ${
                isLight ? 'chassis-milled-light' : 'chassis-milled-dark hover:border-amber-500/40'
              }`}
            >
              <MachineScrewHead isLight={isLight} className="absolute top-2.5 left-2.5" />
              <MachineScrewHead isLight={isLight} className="absolute top-2.5 right-2.5" />

              <div>
                <div className="flex items-center justify-between text-[10px] font-mono text-amber-500 mb-3 pt-2">
                  <div className="flex items-center gap-1.5">
                    <StatusLedPip status="emerald" isLight={isLight} />
                    <span className="font-bold tracking-wider uppercase">{art.category}</span>
                  </div>
                  <span className={isLight ? 'text-slate-500' : 'text-zinc-400'}>{art.readTime}</span>
                </div>
                <h3 className={`text-lg font-bold font-display mb-3 leading-snug ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  {art.title}
                </h3>
                <p className={`text-xs leading-relaxed mb-6 ${
                  isLight ? 'text-slate-600' : 'text-zinc-400'
                }`}>
                  {art.excerpt}
                </p>
              </div>

              <div className={`pt-4 border-t flex items-center justify-between text-xs font-mono ${
                isLight ? 'border-slate-300 text-slate-600' : 'border-zinc-800 text-zinc-400'
              }`}>
                <span className="text-[11px] truncate max-w-[150px]">{art.author}</span>
                <button
                  onClick={() => setIsManifestoOpen(true)}
                  className="text-amber-500 font-extrabold hover:text-amber-400 flex items-center gap-1 uppercase tracking-wider text-[11px] cursor-pointer"
                >
                  <span>Read Manifesto</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Strategic Call to Action Banner */}
      <div className={`mt-16 p-8 sm:p-10 rounded-3xl border text-center relative overflow-hidden ${
        isLight ? 'bg-gradient-to-br from-amber-50 to-orange-50 border-amber-300' : 'bg-gradient-to-br from-zinc-900 via-amber-950/20 to-zinc-900 border-amber-500/30'
      }`}>
        <div className="max-w-2xl mx-auto space-y-4">
          <div className="w-12 h-12 mx-auto rounded-2xl bg-amber-500/20 text-amber-500 border border-amber-500/40 flex items-center justify-center">
            <Flame className="w-6 h-6 animate-pulse" />
          </div>
          <h3 className={`text-2xl sm:text-3xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
            Anchor Your Enterprise in Sovereign AI Guidance
          </h3>
          <p className={`text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
            Move beyond superficial copilots. Partner with LightSpeed Holdings Limited to architect, govern, and deploy autonomous, verifiable agentic operating models on your sovereign terms.
          </p>
          <div className="pt-2 flex justify-center gap-3">
            <button
              onClick={() => setIsManifestoOpen(true)}
              className="px-5 py-3 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-400 border border-amber-500/40 font-bold font-mono text-xs uppercase tracking-wider transition-all inline-flex items-center gap-2 cursor-pointer active:scale-95"
            >
              <FileCheck className="w-4 h-4" />
              <span>Read Manifesto</span>
            </button>
            <button
              onClick={() => onOpenContactModal('Engage LightSpeed Leadership on Pharos Architecture')}
              className="px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 inline-flex items-center gap-2 cursor-pointer active:scale-95"
            >
              <span>Initiate Executive Consultation</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Manifesto Reader Modal */}
      <AgenticAiManifestoModal
        isOpen={isManifestoOpen}
        onClose={() => setIsManifestoOpen(false)}
        onOpenContactModal={onOpenContactModal}
        theme={theme}
      />

    </section>
  );
};

// Backwards compatibility export
export { PharosSection as InsightsResearchSection };
