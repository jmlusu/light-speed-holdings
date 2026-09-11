import React, { useState } from 'react';
import { CheckCircle2 } from 'lucide-react';

interface SectorExpertiseSectionProps {
  theme: 'light' | 'dark';
}

type BadgeTone = 'cyan' | 'slate';

interface IndustrySector {
  /** Short label used on the tab button. */
  tab: string;
  title: string;
  /** One-line opportunity framing — never a delivery claim. */
  subtitle: string;
  description: string;
  useCases: string[];
  badge: string;
  badgeTone: BadgeTone;
  note?: string;
}

const industriesData: Record<string, IndustrySector> = {
  agriculture: {
    tab: 'Agriculture',
    title: 'Agriculture & Agritech',
    subtitle: 'Agentic weather, soil, and mobile-money micro-loan risk workflows for smallholder farmers and agri-businesses.',
    description: 'Weather data, soil analysis, and mobile-money micro-loan risk assessments — agentic AI workflows that help smallholder farmers make better decisions and help agri-businesses manage supply chains. Designed for offline-first environments where connectivity is intermittent.',
    useCases: [
      'Agentic weather + soil advisory for smallholder farmers (modelled on Ulangizi-style chatbot patterns)',
      'Mobile-money micro-loan risk assessment for agricultural cooperatives',
      'Supply chain monitoring and procurement automation for agri-businesses'
    ],
    badge: 'In pilot / Fieldable 2026',
    badgeTone: 'cyan'
  },
  health: {
    tab: 'Health & M&E',
    title: 'Public Health & M&E',
    subtitle: 'Clinic supply-chain monitoring, anomaly-triggered auto-procurement, and donor-ready M&E reporting — designed to move from weeks to hours.',
    description: 'Monitor clinic supply chains, auto-generate procurement requests on anomaly detection, and produce donor-ready M&E reports from Kobo and DHIS2 data. The pipeline from field collection to boardroom reporting is designed to move from weeks to hours.',
    useCases: [
      'Clinic supply chain monitoring with Z-score anomaly detection and auto-procurement',
      'Donor-ready quarterly and annual M&E reports from Kobo/DHIS2 data',
      'Interactive program dashboards (mobile-friendly, NGO-grade)',
      'Citizen-query agents for public health information'
    ],
    badge: 'In pilot (composing evidence)',
    badgeTone: 'cyan',
    note: 'No confirmed partnership with any named health organization has been signed.'
  },
  'financial-inclusion': {
    tab: 'Financial Inclusion',
    title: 'Financial Inclusion (VSLA / SACCO / Mobile Money)',
    subtitle: 'Agentic workflows over mobile-money rails for informal savings groups, micro-finance institutions, and reconciliation.',
    description: 'Agentic workflows over Airtel Money and TNM Mpamba rails, serving informal savings groups (VSLA/SACCO) and micro-finance institutions. Micro-loan risk assessment for smallholder farmers, automated savings tracking, and mobile-money reconciliation — built for the dual-economy reality of Southern Africa.',
    useCases: [
      'Agentic workflows over Airtel Money and TNM Mpamba rails',
      'Automated savings tracking for VSLA/SACCO groups',
      'Micro-loan risk assessment for smallholder farmers',
      'Mobile-money reconciliation and reporting'
    ],
    badge: 'In pilot (use case in active development)',
    badgeTone: 'cyan',
    note: 'This is a use case that development organizations working in financial inclusion are actively seeking; no signed engagement exists.'
  },
  sme: {
    tab: 'SME & Services',
    title: 'SME & Services',
    subtitle: 'A “Company-in-a-Box” lightweight agent set for Malawian SMEs that need full capability without a full team.',
    description: 'A “Company-in-a-Box” lightweight agent set — Marketing, Sales, Compliance, Finance, HR — for Malawian SMEs that cannot afford a full team but need full capability. From the bar that runs AI-powered inventory and pricing to the lodge that automates bookings and guest communications.',
    useCases: [
      'AI-powered inventory, sales, and profitability monitoring (demonstrated in-house at J&S StopOver Bar)',
      'Booking and guest communication automation for hospitality',
      'Lightweight agent sets for Marketing, Sales, Compliance, Finance, HR',
      'WhatsApp-native customer service for SMEs'
    ],
    badge: 'Fieldable 2026',
    badgeTone: 'cyan'
  },
  government: {
    tab: 'Government',
    title: 'Government / Public Sector',
    subtitle: 'Citizen-query, legislative summarisation, project monitoring, and compliance reporting — auditable and approval-gated.',
    description: 'Citizen-query agents, legislative summarisation, project monitoring, and compliance reporting — built for the governance-first standards that Malawi’s DPA and SADC’s digital transformation agenda demand. Every action is auditable. Every approval is gated.',
    useCases: [
      'Compliance monitoring and regulatory reporting for government agencies',
      'Contract review and legal document analysis at scale',
      'Citizen-query agents for public service information',
      'Legislative summarisation and policy analysis',
      'HR and personnel management automation'
    ],
    badge: 'In active development',
    badgeTone: 'slate',
    note: 'Governance framework mapped to Malawi DPA and SADC standards. National AI Strategy consultation submission published.'
  },
  finance: {
    tab: 'Finance',
    title: 'Finance / Compliance',
    subtitle: 'Automated audit reconciliation, KYC assistance, and cross-border trade documentation support for financial institutions.',
    description: 'Automated audit reconciliation, KYC assistance, and cross-border trade documentation support for banks, cooperatives, and trade organizations — grounded in the 5-tier approval matrix that maps to financial services authorisation levels.',
    useCases: [
      'Continuous compliance monitoring and risk analysis',
      'Audit preparation with immutable audit trails',
      'Cross-border trade documentation support'
    ],
    badge: 'In pilot (sector targeting)',
    badgeTone: 'cyan'
  },
  'supply-chain': {
    tab: 'Supply Chain',
    title: 'Supply Chain / Logistics',
    subtitle: 'Corridor routing and ledger-auditing agents for corridor traders and logistics companies.',
    description: 'Corridor routing and ledger-auditing agents for corridor traders and logistics companies along the Nacala and Beira corridors.',
    useCases: [
      'Corridor routing and dispatch coordination',
      'Ledger auditing and reconciliation agents',
      'Border pre-clearance and documentation automation'
    ],
    badge: 'In active development (sector targeting)',
    badgeTone: 'slate'
  }
};

export const SectorExpertiseSection: React.FC<SectorExpertiseSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const [selectedIndustry, setSelectedIndustry] = useState<string>('agriculture');

  const badgeClasses = (tone: BadgeTone) =>
tone === 'slate'
            ? 'border-slate-400/40 bg-slate-400/10 text-slate-400'
      : 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan';

  return (
    <section id="authority" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
        <div className="space-y-2 max-w-2xl">
          <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
            SEVEN VERTICALS // HONESTLY POSITIONED
          </span>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Built for Regulated Scale
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Designed for African environments where connectivity is limited, data rules are strict, and regulatory scrutiny is non-negotiable. Every vertical below is positioned honestly — pilot, fieldable, or in active development.
          </p>
        </div>

        <div className={`flex flex-wrap p-1.5 rounded-2xl gap-2 ${
          isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'
        }`}>
          {Object.keys(industriesData).map((key) => {
            const ind = industriesData[key];
            const isSelected = selectedIndustry === key;
            return (
              <button
                key={key}
                onClick={() => setSelectedIndustry(key)}
                className={`px-4 py-2 rounded-xl text-xs font-mono font-bold tracking-wider transition-all duration-200 cursor-pointer flex items-center gap-2 ${
                  isSelected
                    ? isLight ? 'tactile-btn-active-light text-slate-900 border-ls-red/50' : 'tactile-btn-active-dark text-white border-ls-red/50'
                    : isLight
                      ? 'tactile-btn-inactive-light text-slate-700'
                      : 'tactile-btn-inactive-dark text-zinc-300'
                }`}
              >
                <span className={`w-2 h-2 rounded-full transition-all duration-300 ${
                  isSelected ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                }`} />
                <span>{ind.tab}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Selected Sector Deep-Dive Card */}
      {(() => {
        const ind = industriesData[selectedIndustry];
        return (
          <div className={`p-8 sm:p-10 rounded-3xl border ${
            isLight ? 'bg-white/95 border-slate-300 shadow-xl text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-2xl text-zinc-300'
          }`}>
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              <div className="lg:col-span-7 space-y-4">
                <span className={`inline-flex items-center rounded-full border px-2.5 py-1 font-mono text-[10px] font-bold tracking-widest ${badgeClasses(ind.badgeTone)}`}>
                  {ind.badge}
                </span>
                <h3 className={`text-2xl sm:text-3xl font-black tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{ind.title}</h3>
                <p className={`text-justify text-sm font-semibold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>{ind.subtitle}</p>
                <p className={`text-justify text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>{ind.description}</p>
                {ind.note && (
                  <p className={`text-justify text-xs leading-relaxed font-mono ${isLight ? 'text-slate-600' : 'text-zinc-500'}`}>
                    {ind.note}
                  </p>
                )}
              </div>

              <div className="lg:col-span-5 space-y-3">
                <span className={`text-xs font-mono font-bold block ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                  Key Use Cases:
                </span>
                {ind.useCases.map((useCase, uIdx) => (
                  <div
                    key={uIdx}
                    className={`p-3.5 rounded-2xl border text-xs flex items-start gap-2.5 font-medium ${
                      isLight ? 'bg-slate-50 border-slate-300 text-slate-800' : 'border-white/15 bg-white/[0.05] text-zinc-300'
                    }`}
                  >
                    <CheckCircle2 className="w-4 h-4 text-ls-cyan shrink-0 mt-0.5" />
                    <span>{useCase}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
      })()}
    </section>
  );
};
