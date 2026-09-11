import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  ShieldCheck, 
  Sparkles, 
  BookOpen, 
  Download, 
  ArrowRight, 
  ExternalLink, 
  CheckCircle2, 
  Building2, 
  Landmark, 
  HeartHandshake, 
  Store,
  FileText,
  Clock,
  Coins,
  Cpu,
  Layers,
  Activity,
  ArrowUpRight
} from 'lucide-react';
import { StatusBadge, HonestyTier } from './ui/StatusBadge';
import { AcousticVentGrille } from './TactileHardwareElements';
import pharosBeaconLake from '../assets/images/pharos_beacon_lake_1789078282970.jpg';

interface ProofShowcaseProps {
  theme?: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const ProofShowcase: React.FC<ProofShowcaseProps> = ({
  theme = 'dark',
  onRequestBriefing
}) => {
  const isLight = theme === 'light';
  const [activeTab, setActiveTab] = useState<'pilots' | 'publications' | 'ecosystem'>('pilots');
  const [downloadedTome, setDownloadedTome] = useState<string | null>(null);

  // Honest Pilot Work & Demonstrable Case Studies
  const pilotCases: {
    id: string;
    title: string;
    stakeholder: string;
    tier: HonestyTier;
    sector: string;
    problem: string;
    intervention: string;
    statusSummary: string;
    deliverableState: string;
  }[] = [
    {
      id: 'chichewa-minag',
      title: 'Chichewa Agricultural NLU & Extension Diagnostic',
      stakeholder: 'Ministry of Agriculture Dialogue & Smallholder Cooperatives',
      tier: 'pilot',
      sector: 'AGRICULTURE & AGRITECH',
      problem: 'Agricultural extension officers face a 1:2,500 farmer ratio in rural districts; crop disease identification and weather guidance is slow to reach smallholders in vernacular Chichewa.',
      intervention: 'Engineered a bilingual (Chichewa/English) speech-to-text and vision diagnostic pipeline capable of running on low-bandwidth WhatsApp and offline-first mobile channels.',
      statusSummary: 'Currently in prototype field testing with extension officer datasets and crop imagery.',
      deliverableState: 'Pilot in Progress — vernacular fine-tuning on Malawi agricultural nomenclature.'
    },
    {
      id: 'sacco-vsla',
      title: 'VSLA & SACCO Autonomous Ledger & Micro-Reconciliation',
      stakeholder: 'Rural Village Savings & Microfinance Associations',
      tier: 'in-development',
      sector: 'FINANCIAL INCLUSION',
      problem: 'Paper ledger discrepancies, manual cash box counting, and lack of verifiable credit histories lock millions of rural community members out of formal financing.',
      intervention: 'Constructed an offline-first cryptographic ledger with SMS and WhatsApp voice entries, automating group share-out calculations and generating verifiable credit audit trails.',
      statusSummary: 'Core smart-ledger state machine built; testing reconciliation against Airtel Money and TNM Mpamba APIs.',
      deliverableState: 'In Active Development — scheduled for community field trials in 2026.'
    },
    {
      id: 'js-stopover',
      title: 'J&S StopOver Lodge — Commercial Operations Automation',
      stakeholder: 'J&S StopOver (Malawi Hospitality & Commercial SME)',
      tier: 'proven-in-house',
      sector: 'SME & COMMERCIAL SERVICES',
      problem: 'Manual booking reconciliation, fragmented guest communication, and disjointed supplier ordering caused operational overhead and booking delays.',
      intervention: 'Deployed an integrated autonomous guest concierge on WhatsApp, automated booking calendars, PayChangu payment link dispatch, and automated inventory reordering.',
      statusSummary: 'Fully operational production deployment serving real daily guests and supplier workflows.',
      deliverableState: 'Proven In-House & Live SME Proof — 100% operational in Malawi.'
    },
    {
      id: 'in-house-144',
      title: '144-Agent Sovereign Company Orchestration Engine',
      stakeholder: 'LightSpeed Holdings (Internal Operations)',
      tier: 'proven-in-house',
      sector: 'AGENTIC COMPANY BUILDING',
      problem: 'Traditional corporate operations require massive administrative headcount to coordinate multi-department workflows, leading to coordination drag.',
      intervention: 'Built and operating our full 144-agent enterprise hierarchy (from Executive Committee down to Specialists) via YAML registries, OpenCode cards, and DAG task buses.',
      statusSummary: 'Daily internal operations, automated code auditing, design systems, and compliance checks run on this platform.',
      deliverableState: 'Proven In-House — the operational heartbeat of LightSpeed Holdings.'
    }
  ];

  // Pharos Thought Leadership Publications
  const publications = [
    {
      id: 'sadc-governance-framework-doc',
      number: 'EXECUTIVE SUBMISSION // 2026',
      title: 'SADC Agentic AI Governance Framework: Policy Briefing & Executive Submission',
      tag: 'PHAROS POLICY TRACK',
      desc: 'Authored by Jack Mlusu, Founder & CEO. A unified operational and regulatory standard for SADC digital/ICT ministers, MACRA, CRASA, and central banks.',
      pages: '36 Pages',
      readTime: '16 min read',
      citation: 'Author: Jack Mlusu, Founder & CEO, LightSpeed Holdings',
      anchor: '#sadc-governance-framework'
    },
    {
      id: 'monitor-sep-2026',
      number: 'ISSUE 09 // 2026',
      title: 'Malawi Agentic AI Monitor: The SADC Leapfrog Thesis',
      tag: 'MONTHLY REGIONAL MONITOR',
      desc: 'Our flagship monthly research document examining how Southern Africa is bypassing legacy ERP bloat for autonomous, sovereign agent architectures.',
      pages: '28 Pages',
      readTime: '14 min read',
      citation: 'LightSpeed Sovereign Research Group'
    },
    {
      id: 'haomtgv-paper',
      number: 'TREATISE I',
      title: 'The H-A-O-M-T-G-V Governance Framework for Central Banks & Regulators',
      tag: 'REGULATORY SPECIFICATION',
      desc: 'A mathematical and institutional blueprint for bounding autonomous AI fleets to 5-tier cryptographic approval gates and air-gapped data residency.',
      pages: '42 Pages',
      readTime: '22 min read',
      citation: 'Published for SADC Central Banking Dialogue'
    },
    {
      id: 'dpa-compliance-guide',
      number: 'PRACTICE GUIDE',
      title: 'Navigating the Malawi Data Protection Act (2017/2024) in the Age of LLMs',
      tag: 'COMPLIANCE ROADMAP',
      desc: 'Practical technical guidance for compliance officers and enterprise architects ensuring on-soil data residency and zero cross-border telemetry leakage.',
      pages: '34 Pages',
      readTime: '18 min read',
      citation: 'Malawi DPA & GDPR Cross-Mapping'
    }
  ];

  // Real Ecosystem Dialogue & Standards Alignment
  const ecosystemPartners = [
    { name: 'UNDP Malawi', role: 'Digital Innovation & Development Dialogue', badge: 'Ecosystem Dialogue' },
    { name: 'World Bank Malawi', role: 'Financial Inclusion & Agribusiness Focus', badge: 'Technical Exchange' },
    { name: 'Ministry of Agriculture (MinAg)', role: 'Smallholder Extension & Crop Telemetry', badge: 'Pilot Collaboration' },
    { name: 'MACRA', role: 'Communications & Data Protection Alignment', badge: 'Regulatory Standards' },
    { name: 'ICTAM', role: 'ICT Association of Malawi Industry Body', badge: 'Corporate Member' },
    { name: 'mHub Malawi', role: 'Tech Ecosystem & Innovation Hub', badge: 'Community Partner' },
    { name: 'COMESA / IDEA', role: 'Cross-Border Digital Trade Protocol', badge: 'Trade Standard' },
    { name: 'MUBAS & UNIMA', role: 'Applied AI & Vernacular Language Research', badge: 'Academic Synergy' }
  ];

  const handleDownload = (pubId: string) => {
    setDownloadedTome(pubId);
    setTimeout(() => setDownloadedTome(null), 3000);
  };

  return (
    <section id="proof" className="py-20 px-4 sm:px-8 max-w-7xl mx-auto w-full relative z-10">
      
      {/* Header & Honesty Ladder Anchor */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.9)] animate-pulse" />
            <span className="text-xs font-mono font-bold tracking-widest text-orange-500 uppercase">
              HONESTY LADDER // VERIFIED PROOF & ECOSYSTEM
            </span>
          </div>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Proof, Pilots & Regional Authority
          </h2>
          <p className={`text-justify text-justify text-xs sm:text-sm max-w-3xl leading-relaxed ${
            isLight ? 'text-slate-700' : 'text-zinc-300'
          }`}>
            We believe in radical honesty. Products and pilots are in active development or proven on our own operations. We never present early-stage work as delivered enterprise outcomes.
          </p>
        </div>

        {/* Tab Switcher */}
        <div className={`inline-flex p-1 rounded-full border self-start md:self-auto ${
          isLight ? 'bg-slate-100 border-slate-300' : 'bg-black/60 border-white/10'
        }`}>
          {[
            { id: 'pilots', label: 'Pilots & Case Proofs' },
            { id: 'publications', label: 'Pharos Research' },
            { id: 'ecosystem', label: 'Ecosystem & Standards' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-1.5 rounded-full text-xs font-mono font-bold tracking-wider transition-all cursor-pointer ${
                activeTab === tab.id
                  ? 'bg-orange-500 text-white shadow-md'
                  : isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab 1: Pilots & Grounded Case Proofs */}
      {activeTab === 'pilots' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {pilotCases.map((pilot) => (
            <motion.div
              key={pilot.id}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`p-6 sm:p-7 rounded-3xl border relative overflow-hidden flex flex-col justify-between ${
                isLight ? 'bg-white border-slate-300 shadow-lg text-slate-800' : 'bg-black/60 border-white/15 shadow-xl text-zinc-200'
              }`}
            >
              {/* Top Hardware Screws */}
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              <div className="space-y-4">
                {/* Header & Status Badge */}
                <div className="flex items-center justify-between gap-2 border-b border-black/10 dark:border-white/10 pb-3">
                  <span className="text-[10px] font-mono text-orange-400 font-bold uppercase tracking-wider">
                    {pilot.sector}
                  </span>
                  <StatusBadge tier={pilot.tier} size="sm" />
                </div>

                {/* Title & Stakeholder */}
                <div>
                  <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                    {pilot.title}
                  </h3>
                  <p className="text-xs font-mono text-[#2D3748] mt-1">
                    Stakeholder: {pilot.stakeholder}
                  </p>
                </div>

                {/* Problem / Need */}
                <div className="space-y-1">
                  <span className="text-[11px] font-mono font-bold text-zinc-400 uppercase">Context & Challenge:</span>
                  <p className={`text-justify text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                    {pilot.problem}
                  </p>
                </div>

                {/* Technical Intervention */}
                <div className="space-y-1">
                  <span className="text-[11px] font-mono font-bold text-orange-400 uppercase">Technical Intervention:</span>
                  <p className={`text-justify text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                    {pilot.intervention}
                  </p>
                </div>

                {/* Current State / Grounding */}
                <div className="p-3 rounded-2xl bg-orange-500/10 border border-orange-500/20 text-orange-400 text-xs">
                  <div className="flex items-center gap-1.5 font-bold font-mono text-[10px] uppercase mb-0.5">
                    <Activity className="w-3.5 h-3.5" />
                    <span>State of Verification:</span>
                  </div>
                  <p className="text-[11px] text-zinc-300">
                    {pilot.deliverableState}
                  </p>
                </div>
              </div>

              {/* Action Trigger */}
              <div className="pt-4 mt-4 border-t border-black/10 dark:border-white/10 flex items-center justify-between">
                <span className="text-[10px] font-mono text-[#2D3748]">
                  Verified via Honesty Ladder
                </span>
                <button
                  onClick={() => onRequestBriefing?.(`Requesting technical review for pilot: ${pilot.title}`)}
                  className="inline-flex items-center gap-1.5 text-xs font-mono font-bold text-orange-400 hover:text-orange-300 transition-colors cursor-pointer"
                >
                  <span>Request Technical Dossier</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

            </motion.div>
          ))}
        </div>
      )}

      {/* Tab 2: Pharos Thought Leadership Publications */}
      {activeTab === 'publications' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            
            {/* Left Pharos Visual Beacon Card */}
            <div className="lg:col-span-4 relative rounded-3xl overflow-hidden border border-amber-500/30 shadow-2xl">
              <img 
                src={pharosBeaconLake} 
                alt="Pharos Beacon on Lake Malawi" 
                referrerPolicy="no-referrer"
                className="w-full h-80 object-cover object-center"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent pointer-events-none" />
              
              <div className="absolute bottom-4 left-4 right-4 space-y-2 text-white">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/30 text-amber-200 border border-amber-500/40 font-bold">
                  PHAROS RESEARCH TOWER
                </span>
                <h4 className="text-lg font-bold font-display leading-snug">
                  Illuminating Sovereign AI Policy for SADC
                </h4>
                <p className="text-xs text-zinc-300 leading-snug">
                  Authored in Lilongwe, providing mathematical rigor and policy translation for boards navigating AI transformation.
                </p>
              </div>
            </div>

            {/* Right Publications List */}
            <div className="lg:col-span-8 space-y-4">
              {publications.map((pub) => (
                <div
                  key={pub.id}
                  className={`p-5 sm:p-6 rounded-2xl border transition-all ${
                    isLight ? 'bg-white border-slate-300 shadow-md text-slate-800' : 'bg-black/60 border-white/15 shadow-lg text-zinc-200'
                  }`}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono font-bold text-amber-400">
                        {pub.number}
                      </span>
                      <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-orange-500/10 text-orange-400 border border-orange-500/20 font-bold">
                        {pub.tag}
                      </span>
                    </div>
                    <div className="flex items-center gap-3 text-[10px] font-mono text-zinc-400">
                      <span>{pub.pages}</span>
                      <span>•</span>
                      <span>{pub.readTime}</span>
                    </div>
                  </div>

                  <h3 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'} mb-1.5`}>
                    {pub.title}
                  </h3>

                  <p className={`text-justify text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'} mb-4`}>
                    {pub.desc}
                  </p>

                  <div className="flex items-center justify-between pt-3 border-t border-black/10 dark:border-white/10">
                    <span className="text-[10px] font-mono text-[#2D3748]">
                      {pub.citation}
                    </span>

                    <div className="flex items-center gap-2">
                      {(pub as any).anchor && (
                        <a
                          href={(pub as any).anchor}
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-orange-500/15 text-orange-400 hover:bg-orange-500 hover:text-white transition-all cursor-pointer border border-orange-500/30"
                        >
                          <span>Explore Framework</span>
                          <ArrowRight className="w-3.5 h-3.5" />
                        </a>
                      )}

                      <button
                        onClick={() => handleDownload(pub.id)}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-amber-500/15 text-amber-400 hover:bg-amber-500 hover:text-white transition-all cursor-pointer border border-amber-500/30"
                      >
                        {downloadedTome === pub.id ? (
                          <>
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                            <span>Dossier Dispatched</span>
                          </>
                        ) : (
                          <>
                            <Download className="w-3.5 h-3.5" />
                            <span>Download Research Tome</span>
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

          </div>
        </div>
      )}

      {/* Tab 3: Real Ecosystem & Standards Alignment */}
      {activeTab === 'ecosystem' && (
        <div className="space-y-6">
          <div className={`p-6 sm:p-8 rounded-3xl border ${
            isLight ? 'bg-white border-slate-300 shadow-xl' : 'bg-black/60 border-white/15 shadow-2xl'
          }`}>
            <div className="max-w-3xl mb-6">
              <h3 className={`text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                SADC Ecosystem Dialogue & Standards Alignment
              </h3>
              <p className={`text-justify text-justify text-xs sm:text-sm mt-1 leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                We maintain active dialogue, technical exchange, and standards alignment with key institutional and technology stakeholders across Malawi and the SADC corridor.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {ecosystemPartners.map((item, idx) => (
                <div
                  key={idx}
                  className={`p-4 rounded-2xl border flex flex-col justify-between space-y-3 ${
                    isLight ? 'bg-slate-50 border-slate-200' : 'bg-white/[0.04] border-white/10'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[9px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 font-bold">
                        {item.badge}
                      </span>
                      <Building2 className="w-3.5 h-3.5 text-zinc-400" />
                    </div>
                    <h4 className={`text-sm font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {item.name}
                    </h4>
                  </div>
                  <p className={`text-justify text-justify text-[11px] leading-snug ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                    {item.role}
                  </p>
                </div>
              ))}
            </div>

            <div className="mt-6 p-4 rounded-2xl bg-black/40 border border-white/10 text-center text-xs font-mono text-zinc-400">
              Honesty notice: All entity references indicate active technical dialogue, regulatory alignment, or collaborative research agendas — never unauthorized client endorsements.
            </div>
          </div>
        </div>
      )}

    </section>
  );
};
