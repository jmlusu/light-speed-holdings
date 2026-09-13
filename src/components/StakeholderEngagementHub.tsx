import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  Building2, 
  GraduationCap, 
  ShieldCheck, 
  Landmark, 
  Globe2, 
  Handshake, 
  ArrowRight, 
  CheckCircle2, 
  Send,
  FileText,
  Compass,
  Sparkles,
  Lock,
  ChevronRight,
  Terminal,
  Cpu
} from 'lucide-react';
import { StatusLedPip, MachineScrewHead } from './TactileHardwareElements';

interface StakeholderEngagementHubProps {
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export interface StakeholderOffer {
  id: string;
  category: string;
  badge: string;
  title: string;
  audience: string;
  icon: React.ReactNode;
  summary: string;
  offers: string[];
  deliverables: string[];
  ctaText: string;
  recommendedIntent: string;
}

export const STAKEHOLDER_OFFERS: StakeholderOffer[] = [
  {
    id: 'executives',
    category: 'Corporate & C-Suite',
    badge: 'EXECUTIVE LEADERSHIP',
    title: 'Enterprise Transformation & Executive AI Advisory',
    audience: 'CEOs, COOs, CFOs, Board Risk Committees & Commercial Banks',
    icon: <Building2 className="w-6 h-6 text-amber-500" />,
    summary: 'Guiding commercial enterprises and regional financial institutions from slide-deck paralysis into computable, high-assurance multi-agent execution with zero unverified writes.',
    offers: [
      '2-Week Executive Advisory & Capital Allocation Sprint',
      'Fiduciary Board Governance Charter & Human-in-the-Loop Matrix',
      'Legacy Mainframe/Core Banking AI Event Gateway'
    ],
    deliverables: [
      'Computable Net Sovereign Value (NSV) financial model',
      'Air-gapped on-soil compute cluster TCO blueprint',
      'SADC Banking Act compliance audit clearance'
    ],
    ctaText: 'Request Executive Consulting Offer',
    recommendedIntent: 'Consulting Offer & Strategy Advisory'
  },
  {
    id: 'academics',
    category: 'Academics & Higher Ed',
    badge: 'RESEARCH & HIGHER EDUCATION',
    title: 'University Research Partnerships & Indigenous NLP Labs',
    audience: 'University Chancellors, Computer Science Faculty & SADC Researchers',
    icon: <GraduationCap className="w-6 h-6 text-amber-500" />,
    summary: 'Partnering with Malawian and regional academic institutions to develop open-access Chichewa/Tumbuka NLP corpora, sovereign model benchmarks, and student agent engineering fellowships.',
    offers: [
      'Joint Sovereign AI Research Lab Setup & Compute Allocation',
      'Bilingual Bantu Language Dataset & Model Benchmarks',
      'OpenCode Multi-Agent Systems Curriculum & Fellowships'
    ],
    deliverables: [
      'Co-authored peer-reviewed research publications',
      'Air-gapped GPU compute credits for university researchers',
      'SADC AI talent incubation & graduate pipeline'
    ],
    ctaText: 'Partner with Academic Lab',
    recommendedIntent: 'Academic AI Research & University Collaboration'
  },
  {
    id: 'regulators',
    category: 'Regulators & Statutory',
    badge: 'REGULATORY COMPLIANCE',
    title: 'Regulatory Sandboxes & Fiduciary Audit Frameworks',
    audience: 'Reserve Bank of Malawi (RBM), MACRA, CFTC & Data Protection Authority',
    icon: <ShieldCheck className="w-6 h-6 text-amber-500" />,
    summary: 'Providing regulators with turnkey cryptographic verification tools, sandbox testing protocols, and automated statutory audit trails for autonomous financial and telecom agents.',
    offers: [
      'Regulatory AI Sandbox Architecture & Stress-Testing Harness',
      'Malawi Data Protection Act 2017/2024 Audit Verification CLI',
      'Central Bank Algorithmic Risk Assessment & Kill-Switch Spec'
    ],
    deliverables: [
      'Tamper-proof Merkle-tree cryptographic audit logs',
      'Statutory compliance mapping for sovereign jurisdictions',
      '5-tier Human-in-the-Loop escalation protocol'
    ],
    ctaText: 'Schedule Regulatory Briefing',
    recommendedIntent: 'Regulatory Compliance & Governance Audit (RBM/MACRA/DPA)'
  },
  {
    id: 'government',
    category: 'Government Agencies',
    badge: 'NATIONAL INFRASTRUCTURE',
    title: 'National AI Infrastructure & Sovereign E-Government',
    audience: 'Ministries of ICT, National Planning Commission, Revenue Authority (MRA)',
    icon: <Landmark className="w-6 h-6 text-amber-500" />,
    summary: 'Deploying secure, on-soil, air-gapped compute infrastructure that accelerates Malawi Vision 2063, automates customs manifest audits, and enhances public service delivery.',
    offers: [
      'Sovereign On-Soil Air-Gapped Data Center Architecture',
      'MRA Customs & Border Control Cargo Manifest Auditor',
      'Citizen Service Conversational Triage in Local Languages'
    ],
    deliverables: [
      '100% in-country data residency guarantees',
      'Automated cross-examination of shipping manifests',
      'Inter-ministerial data governance standards'
    ],
    ctaText: 'Engage Government Solutions',
    recommendedIntent: 'Government National AI Deployment & E-Gov'
  },
  {
    id: 'ngos',
    category: 'NGOs & Field Implementers',
    badge: 'DEVELOPMENT IMPACT',
    title: 'Field Telemetry, M&E Automation & DHIS2 Sync',
    audience: 'International & Local NGOs, Health Programs, Agricultural Cooperatives',
    icon: <Globe2 className="w-6 h-6 text-amber-500" />,
    summary: 'Equiping field teams and health surveillance assistants with offline-first mobile data capture, automated Kobo/DHIS2 pipelines, and instant donor-compliant reporting.',
    offers: [
      'Offline-First KoboToolbox & DHIS2 Field Synchronizers',
      'Agricultural Extension Voice Bot on WhatsApp (Chichewa)',
      'Automated Narrative & Visual Donor Report Generator'
    ],
    deliverables: [
      'Zero-data-loss offline mobile synchronization',
      'Automated drug stock-out & crop disease alerts',
      'Turnkey quarterly/annual donor report templates'
    ],
    ctaText: 'Request NGO Pilot Program',
    recommendedIntent: 'NGO Field Telemetry & M&E Automation'
  },
  {
    id: 'donors',
    category: 'Donor Community',
    badge: 'SUSTAINABLE CAPITAL',
    title: 'Donor Capacity Building & High-Impact Grant Execution',
    audience: 'USAID, EU Delegation, UNDP, World Bank, FCDO & Philanthropies',
    icon: <Handshake className="w-6 h-6 text-amber-500" />,
    summary: 'Co-engineering sustainable, localized AI solutions that maximize grant efficiency, eliminate expensive foreign software vendor lock-in, and build permanent local capacity.',
    offers: [
      'Sustainable AI Grant Delivery & Co-Engineering Framework',
      'Local Capacity Building & Open-Source Agent Ecosystems',
      'Rigorous M&E Impact Verification & Real-Time Dashboards'
    ],
    deliverables: [
      'Measurable unit cost reductions in development delivery',
      'Full technical IP transfer to Malawian institutions',
      'Verifiable field impact metrics & real-time telemetry'
    ],
    ctaText: 'Submit Grant / Program Inquiry',
    recommendedIntent: 'Donor Community Co-Engineering & Grant Delivery'
  }
];

export const StakeholderEngagementHub: React.FC<StakeholderEngagementHubProps> = ({
  onOpenContactModal,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';
  const [activeTab, setActiveTab] = useState<string>('executives');

  const selectedOffer = STAKEHOLDER_OFFERS.find(o => o.id === activeTab) || STAKEHOLDER_OFFERS[0];

  return (
    <section id="engagement" className={`py-20 px-4 sm:px-8 max-w-7xl mx-auto w-full transition-colors ${
      isLight ? 'text-slate-900' : 'text-zinc-100'
    }`}>
      {/* SECTION HEADER */}
      <div className="text-center max-w-3xl mx-auto mb-14 space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-[10px] font-mono font-extrabold uppercase tracking-widest bg-amber-500/20 text-amber-500 border border-amber-500/30">
          <StatusLedPip status="emerald" isLight={isLight} />
          <span>SOVEREIGN CONSULTING &amp; INSTITUTIONAL OFFERS</span>
        </div>

        <h2 className={`text-2xl sm:text-4xl font-extrabold font-display leading-tight tracking-tight ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          Leading AI Thought &amp; Consulting in Malawi
        </h2>

        <p className={`text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-300'}`}>
          LightSpeed Holdings serves as the definitive sovereign partner for Executives, Academics, Regulators, Government Agencies, NGOs, and the Donor Community across Malawi and the SADC corridor.
        </p>
      </div>

      {/* STAKEHOLDER SELECTOR TABS */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 mb-10">
        {STAKEHOLDER_OFFERS.map((offer) => {
          const isActive = offer.id === activeTab;
          return (
            <button
              key={offer.id}
              onClick={() => setActiveTab(offer.id)}
              className={`p-3.5 rounded-2xl border text-left transition-all flex flex-col justify-between gap-3 cursor-pointer ${
                isActive
                  ? 'bg-amber-500 text-slate-950 border-amber-400 shadow-xl scale-[1.02] font-bold'
                  : isLight
                    ? 'bg-white border-slate-200 hover:border-amber-400 text-slate-700'
                    : 'bg-zinc-900/80 border-zinc-800 hover:border-zinc-700 text-zinc-300'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className={isActive ? 'text-slate-950' : 'text-amber-500'}>
                  {offer.icon}
                </span>
                <span className={`text-[9px] font-mono font-extrabold px-1.5 py-0.5 rounded ${
                  isActive ? 'bg-slate-950 text-amber-400' : 'bg-amber-500/10 text-amber-400'
                }`}>
                  OFFER
                </span>
              </div>
              <div>
                <span className={`text-[9px] font-mono uppercase block ${isActive ? 'text-slate-800' : 'text-zinc-400'}`}>
                  {offer.category}
                </span>
                <span className="text-xs font-bold font-display line-clamp-1">
                  {offer.badge}
                </span>
              </div>
            </button>
          );
        })}
      </div>

      {/* ACTIVE STAKEHOLDER DETAIL CARD */}
      <div className={`p-6 sm:p-10 rounded-3xl border relative overflow-hidden transition-all ${
        isLight
          ? 'bg-white border-slate-300 shadow-2xl'
          : 'bg-gradient-to-br from-[#0c101c] via-zinc-950 to-[#090d16] border-amber-500/30 shadow-2xl'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-4 left-4" />
        <MachineScrewHead isLight={isLight} className="absolute top-4 right-4" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-4 left-4" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-4 right-4" />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
          
          {/* Left Column: Scope & Overview */}
          <div className="lg:col-span-7 space-y-5 text-left">
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-3 py-1 rounded-full text-[10px] font-mono font-bold uppercase tracking-widest bg-amber-500 text-slate-950">
                {selectedOffer.badge}
              </span>
              <span className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-amber-300'}`}>
                TARGET AUDIENCE: {selectedOffer.audience}
              </span>
            </div>

            <h3 className={`text-2xl sm:text-3xl font-extrabold font-display leading-tight ${
              isLight ? 'text-slate-900' : 'text-zinc-100'
            }`}>
              {selectedOffer.title}
            </h3>

            <p className={`text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
              {selectedOffer.summary}
            </p>

            {/* Core Consulting Offers */}
            <div className="space-y-2 pt-2">
              <span className="text-xs font-mono font-bold text-amber-500 uppercase tracking-wider block">
                Structured Engagement Packages:
              </span>
              <div className="grid grid-cols-1 gap-2">
                {selectedOffer.offers.map((pkg, idx) => (
                  <div 
                    key={idx}
                    className={`p-3 rounded-xl border flex items-center gap-3 text-xs font-mono ${
                      isLight ? 'bg-slate-50 border-slate-200 text-slate-800' : 'bg-zinc-900/60 border-zinc-800 text-zinc-200'
                    }`}
                  >
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span className="font-semibold">{pkg}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column: Deliverables & Direct Contact CTA */}
          <div className="lg:col-span-5 space-y-6">
            <div className={`p-6 rounded-2xl border space-y-4 ${
              isLight ? 'bg-amber-50/80 border-amber-200' : 'bg-zinc-900/90 border-amber-500/20'
            }`}>
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-extrabold text-amber-500 uppercase tracking-wider">
                  VERIFIED DELIVERABLE SPEC
                </span>
                <StatusLedPip status="emerald" isLight={isLight} />
              </div>

              <ul className="space-y-2.5 text-xs font-mono">
                {selectedOffer.deliverables.map((deliv, idx) => (
                  <li key={idx} className="flex items-start gap-2.5">
                    <Sparkles className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
                    <span className={isLight ? 'text-slate-800' : 'text-zinc-200'}>{deliv}</span>
                  </li>
                ))}
              </ul>

              <div className="pt-2 border-t border-amber-500/20">
                <button
                  onClick={() => onOpenContactModal(selectedOffer.recommendedIntent)}
                  className="w-full py-3.5 px-6 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 flex items-center justify-center gap-2 active:scale-95 cursor-pointer"
                >
                  <Send className="w-4 h-4" />
                  <span>{selectedOffer.ctaText}</span>
                </button>
              </div>
            </div>

            <p className={`text-[11px] font-mono text-center ${isLight ? 'text-slate-500' : 'text-zinc-500'}`}>
              Sovereign in-country delivery // Full compliance with Malawi Data Protection Act 2017/2024
            </p>
          </div>

        </div>
      </div>
    </section>
  );
};
