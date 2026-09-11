import React, { useState } from 'react';
import { CheckCircle2 } from 'lucide-react';

interface SectorExpertiseSectionProps {
  theme: 'light' | 'dark';
}

const industriesData: Record<string, {
  title: string;
  subtitle: string;
  description: string;
  citation: string;
  impact: string[];
}> = {
  finance: {
    title: 'Commercial Banking & Financial Services',
    subtitle: 'Trade finance automation, liquidity reconciliation, and cross-border settlement.',
    description: 'Tier-1 commercial lenders and central banks use LightSpeed to automate letter of credit verification, cross-border treasury balancing across SADC corridors, and continuous AML anomaly detection.',
    citation: 'SADC Regional Banking Architecture Standard',
    impact: [
      'Letter of credit reconciliation compressed from 72 hours to 14 minutes.',
      'Real-time AML/Sanction anomaly detection with 100% audit precision.',
      'Automated multi-currency treasury balancing across Southern African corridors.'
    ]
  },
  government: {
    title: 'Revenue Authorities & Customs Services',
    subtitle: 'Border intelligence, manifest classification, and tariff enforcement.',
    description: 'National ministries and customs authorities use our private edge AI to audit cross-border cargo manifests, catch fraudulent tariff classifications, and eliminate physical inspection bottlenecks.',
    citation: 'National Customs Framework',
    impact: [
      '$14.2M in previously undetected import duties recovered in 90 days.',
      'Cargo clearance throughput increased by 400% across key border posts.',
      'Data residency guaranteed through on-site inference clusters.'
    ]
  },
  logistics: {
    title: 'Supply Chain, Mining & Commodity Logistics',
    subtitle: 'Predictive corridor dispatch, demurrage reduction, and port coordination.',
    description: 'Commodity extractors, port operators, and freight networks use LightSpeed to coordinate 400+ unit transport fleets, predict border delays, and cut demurrage costs.',
    citation: 'Pan-African Mineral Logistics Corridor',
    impact: [
      'Demurrage wait times along Dar es Salaam and Beira corridors reduced by 64%.',
      '4.8M liters of transport fuel saved through predictive routing.',
      'Automated bills-of-lading ingestion and instant customs pre-clearance.'
    ]
  },
  multilateral: {
    title: 'Development Finance & Multilaterals',
    subtitle: 'Program monitoring, grant evaluation, and disbursement oversight.',
    description: 'International development banks and bilateral agencies use our verification systems to audit field milestones and prevent fund diversion on capital deployments.',
    citation: 'Multilateral Oversight Protocol',
    impact: [
      'Continuous satellite and telemetry verification of infrastructure milestones.',
      'Fund disbursement checks reducing diversion risk to near-zero.',
      'Automated donor-grade impact reports generated from ground data.'
    ]
  }
};

const caseStudies = [
  {
    sector: 'COMMERCIAL BANKING',
    client: 'Regional Tier-1 Bank (Southern & Eastern Africa)',
    problem: 'Manual trade finance reconciliation took 72 hours per letter of credit, creating massive merchant bottlenecks and foreign currency exposure.',
    intervention: 'Built a 4-agent pipeline (Ingest, Verification, Sanction Sweep, Swift Dispatch) with human approval gates at every step.',
    outcome: 'Reduced letter of credit issuance time from 72 hours to 14 minutes with 100% compliance audit match.'
  },
  {
    sector: 'NATIONAL REVENUE AUTHORITY',
    client: 'National Taxation & Customs Service',
    problem: 'Cross-border cargo manifest discrepancies resulted in millions in uncollected tariffs and multi-day border queues.',
    intervention: 'Deployed computer vision and manifest cross-examination running local models at border control points.',
    outcome: 'Recovered $14.2M in previously missed duty within 90 days; border clearance throughput increased by 400%.'
  },
  {
    sector: 'COMMODITY LOGISTICS',
    client: 'Export Mineral Logistics Fleet (Central & Southern Africa)',
    problem: 'Fragmented warehouse receipts, volatile corridor delays, and disjointed transport fleets caused massive demurrage penalties at regional ports.',
    intervention: 'Built an autonomous logistics coordination pipeline with predictive border wait times and automated clearing manifests.',
    outcome: 'Corridor transit times reduced by 3.8 days; fleet fuel consumption decreased by 18% across 400+ transport units.'
  }
];

export const SectorExpertiseSection: React.FC<SectorExpertiseSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const [selectedIndustry, setSelectedIndustry] = useState<string>('finance');

  return (
    <section id="authority" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
        <div className="space-y-2 max-w-2xl">
          <span className="text-xs font-mono font-bold tracking-widest text-orange-500">
            PROVEN IN DEMANDING ENVIRONMENTS
          </span>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Built for Regulated Scale
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Tested in African and international environments where connectivity is limited, data rules are strict, and regulatory scrutiny is non-negotiable.
          </p>
        </div>

        <div className={`flex flex-wrap p-1.5 rounded-2xl gap-2 ${
          isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'
        }`}>
          {Object.keys(industriesData).map((key) => {
            const isSelected = selectedIndustry === key;
            return (
              <button
                key={key}
                onClick={() => setSelectedIndustry(key)}
                className={`px-4 py-2 rounded-xl text-xs font-mono font-bold tracking-wider transition-all duration-200 cursor-pointer flex items-center gap-2 ${
                  isSelected
                    ? isLight ? 'tactile-btn-active-light text-slate-900 border-orange-500/50' : 'tactile-btn-active-dark text-white border-orange-500/50'
                    : isLight
                      ? 'tactile-btn-inactive-light text-slate-700'
                      : 'tactile-btn-inactive-dark text-zinc-300'
                }`}
              >
                <span className={`w-2 h-2 rounded-full transition-all duration-300 ${
                  isSelected ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                }`} />
                <span>{key}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Selected Sector Deep-Dive Card */}
      {(() => {
        const ind = industriesData[selectedIndustry];
        return (
          <div className={`p-8 sm:p-10 rounded-3xl border mb-12 ${
            isLight ? 'bg-white/95 border-slate-300 shadow-xl text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-2xl text-zinc-300'
          }`}>
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              <div className="lg:col-span-7 space-y-4">
                <span className="text-xs font-mono text-orange-500 font-bold">
                  {ind.citation}
                </span>
                <h3 className={`text-2xl sm:text-3xl font-black tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{ind.title}</h3>
                <p className={`text-justify text-sm font-semibold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>{ind.subtitle}</p>
                <p className={`text-justify text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>{ind.description}</p>
              </div>

              <div className="lg:col-span-5 space-y-3">
                <span className={`text-xs font-mono font-bold block ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                  Verified Production Impact:
                </span>
                {ind.impact.map((imp, iIdx) => (
                  <div
                    key={iIdx}
                    className={`p-3.5 rounded-2xl border text-xs flex items-start gap-2.5 font-medium ${
                      isLight ? 'bg-slate-50 border-slate-300 text-slate-800' : 'border-white/15 bg-white/[0.05] text-zinc-300'
                    }`}
                  >
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                    <span>{imp}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
      })()}

      {/* Case Studies Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {caseStudies.map((cs, cIdx) => (
          <div
            key={cIdx}
            className={`p-6 rounded-3xl border flex flex-col justify-between space-y-4 ${
              isLight ? 'bg-slate-50 border-slate-300' : 'bg-zinc-900/70 border-white/15'
            }`}
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between text-[11px] font-mono">
                <span className="text-orange-500 font-bold">{cs.sector}</span>
                <span className={`font-semibold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>PRODUCTION</span>
              </div>
              <div className={`text-sm font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{cs.client}</div>
              <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                <strong className={`font-semibold ${isLight ? 'text-slate-900' : 'text-zinc-200'}`}>Challenge:</strong> {cs.problem}
              </p>
              <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                <strong className={`font-semibold ${isLight ? 'text-slate-900' : 'text-zinc-200'}`}>LIGHTSPEED Solution:</strong> {cs.intervention}
              </p>
            </div>

            <div className="pt-3 border-t border-white/10 text-xs font-mono text-emerald-500 font-bold">
              Outcome: {cs.outcome}
            </div>
          </div>
        ))}
      </div>

    </section>
  );
};
