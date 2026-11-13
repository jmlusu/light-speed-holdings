import React, { useState } from 'react';
import { FileCheck } from 'lucide-react';
import { SectionHeading } from './site/SectionHeading';
import { Icon3D, Icon3DName } from './common';

interface ApprovalTier {
  tier: number;
  code: string;
  name: string;
  scope: string;
  authority: string;
  auditLevel: string;
  description: string;
  icon3d: Icon3DName;
}

const TIERS: ApprovalTier[] = [
  {
    tier: 1,
    code: 'AUTO_APPROVE (0)',
    name: 'Operational Auto-Execution',
    scope: 'Routine data formatting, low-risk classification, and internal summarization.',
    authority: 'Fully Autonomous Agent (Zero Human Gate)',
    auditLevel: 'Automated Log & Telemetry',
    description: 'Executed instantly by specialized agents under strict deterministic sandbox rules.',
    icon3d: 'lightning',
  },
  {
    tier: 2,
    code: 'SUPERVISED (1)',
    name: 'Supervised Recommendation',
    scope: 'Drafting reports, code generation, and moderate operational recommendations.',
    authority: 'Junior Operator Review',
    auditLevel: 'Standard Timestamp & Diff Review',
    description: 'Agent prepares complete draft artifacts requiring single-click human sign-off.',
    icon3d: 'documents',
  },
  {
    tier: 3,
    code: 'TACTICAL_GATE (2)',
    name: 'Tactical Decision Gate',
    scope: 'Resource allocation, workflow overrides, and departmental integrations.',
    authority: 'Department Lead / Manager',
    auditLevel: 'Structured Audit Trail & Rationale Log',
    description: 'Requires explicit human authorization before agent proceeds with transactional actions.',
    icon3d: 'orchestration',
  },
  {
    tier: 4,
    code: 'STRATEGIC_GATE (3)',
    name: 'Strategic Authority Gate',
    scope: 'Financial commitments, external partnerships, and policy modifications.',
    authority: 'Executive Sponsor / Director',
    auditLevel: 'Cryptographic Sign-Off & Compliance Tag',
    description: 'High-impact boundary requiring verified executive credentials and multi-factor validation.',
    icon3d: 'safe',
  },
  {
    tier: 5,
    code: 'CEO_ONLY (4)',
    name: 'Absolute Sovereign Control',
    scope: 'Venture launch, core governance reset, and irreversible system architecture changes.',
    authority: 'Chief Executive Officer / Board',
    auditLevel: 'Immutable Board Ledger & Compliance Archive',
    description: 'The ultimate human accountability anchor. No autonomous agent can bypass Tier 5.',
    icon3d: 'verification',
  },
];

interface HumanApprovalMatrixProps {
  theme?: 'light' | 'dark';
}

export const HumanApprovalMatrix: React.FC<HumanApprovalMatrixProps> = ({ theme = 'dark' }) => {
  const [selectedTier, setSelectedTier] = useState<number>(5);
  const isLight = theme === 'light';
  const current = TIERS.find((t) => t.tier === selectedTier) || TIERS[4];

  return (
    <section id="governance-matrix" className={`py-24 px-6 lg:px-12 relative transition-colors duration-150 border-t border-b border-white/10 ${
      isLight ? 'bg-ls-grey-light text-ls-navy' : 'bg-[#070A40] text-white'
    }`}>
      <div className="max-w-7xl mx-auto w-full">
        <SectionHeading
          theme={theme}
          eyebrow="HUMAN-IN-THE-LOOP GOVERNANCE"
          title="The Five-Tier Human Approval Matrix"
          lead="LightSpeed ensures human authority remains unmistakable. Autonomous agents operate strictly within bounded guardrails backed by immutable decision gates from AUTO_APPROVE (0) to CEO_ONLY (4)."
        />

        {/* Interactive Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mt-12">
          
          {/* Tier Selector Buttons */}
          <div className="lg:col-span-5 space-y-3">
            {TIERS.map((tier) => {
              const isSelected = tier.tier === selectedTier;
              return (
                <button
                  key={tier.tier}
                  onClick={() => setSelectedTier(tier.tier)}
                  className={`w-full text-left p-4 transition-colors flex items-center justify-between border cursor-pointer ${
                    isSelected
                      ? isLight 
                        ? 'bg-ls-navy text-white border-ls-navy shadow-[4px_4px_0px_#E63946]' 
                        : 'bg-[#05072B] text-white border-ls-cyan shadow-[4px_4px_0px_#00BFFF]'
                      : isLight 
                        ? 'bg-white text-ls-navy border-slate-300 hover:border-ls-navy' 
                        : 'bg-[#070A40]/70 text-slate-300 border-white/15 hover:border-white/40'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon3D name={tier.icon3d} size="xs" />
                    <span className={`w-7 h-7 flex items-center justify-center font-mono text-xs font-bold tabular-nums border shrink-0 ${
                      isSelected 
                        ? isLight ? 'bg-ls-red border-ls-red text-white' : 'bg-ls-cyan border-ls-cyan text-ls-navy' 
                        : isLight ? 'bg-slate-100 border-slate-300 text-ls-navy' : 'bg-white/5 border-white/10 text-slate-400'
                    }`}>
                      0{tier.tier}
                    </span>
                    <div>
                      <h4 className={`text-sm font-bold font-sans ${isSelected ? 'text-white' : (isLight ? 'text-ls-navy' : 'text-white')}`}>
                        {tier.name}
                      </h4>
                      <p className={`text-xs font-mono ${isSelected ? (isLight ? 'text-white/80' : 'text-slate-300') : (isLight ? 'text-slate-500' : 'text-slate-400')}`}>
                        {tier.code} — {tier.authority}
                      </p>
                    </div>
                  </div>
                  <span className={`text-xs font-mono font-bold uppercase tracking-wider ${isSelected ? (isLight ? 'text-white' : 'text-ls-cyan') : (isLight ? 'text-slate-400' : 'text-slate-500')}`}>
                    {isSelected ? 'SELECTED' : 'VIEW'}
                  </span>
                </button>
              );
            })}
          </div>

          {/* Detailed Inspector Card */}
          <div className={`lg:col-span-7 p-8 border relative overflow-hidden ${
            isLight ? 'bg-white border-slate-300 shadow-[6px_6px_0px_#070A40]' : 'bg-[#05072B] border-white/20 shadow-[6px_6px_0px_#00BFFF]'
          }`}>

            <div className="relative z-10 space-y-6 text-left font-sans">
              <div className="flex items-center justify-between pb-3 border-b border-white/10">
                <div className="flex items-center gap-3">
                  <Icon3D name={current.icon3d} size="sm" />
                  <span className={`text-xs font-mono font-bold uppercase tracking-widest px-3 py-1 border ${
                    isLight ? 'bg-ls-red/10 border-ls-red text-ls-red' : 'bg-ls-cyan/20 border-ls-cyan text-ls-cyan'
                  }`}>
                    Tier 0{current.tier} Protocol [{current.code}]
                  </span>
                </div>
              </div>

              <div>
                <h3 className={`text-2xl font-bold mb-2 font-sans ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                  {current.name}
                </h3>
                <p className={`text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-slate-300'}`}>
                  {current.description}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                <div className={`p-4 border ${isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/40 border-white/10'}`}>
                  <span className={`text-[10px] font-mono uppercase tracking-wider block mb-1 font-bold ${isLight ? 'text-slate-500' : 'text-slate-400'}`}>
                    Operational Scope
                  </span>
                  <p className={`text-xs font-semibold ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                    {current.scope}
                  </p>
                </div>

                <div className={`p-4 border ${isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/40 border-white/10'}`}>
                  <span className={`text-[10px] font-mono uppercase tracking-wider block mb-1 font-bold ${isLight ? 'text-slate-500' : 'text-slate-400'}`}>
                    Decision Authority
                  </span>
                  <p className="text-xs font-bold text-ls-red font-mono">
                    {current.authority}
                  </p>
                </div>
              </div>

              <div className={`p-4 border flex items-center justify-between ${
                isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/40 border-white/10'
              }`}>
                <div className="flex items-center gap-3">
                  <FileCheck className="w-5 h-5 text-ls-cyan" />
                  <div>
                    <span className={`text-[10px] font-mono block uppercase ${isLight ? 'text-slate-500' : 'text-slate-400'}`}>
                      Audit & Accountability Mechanism
                    </span>
                    <span className={`text-xs font-medium font-sans ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                      {current.auditLevel}
                    </span>
                  </div>
                </div>
                <span className={`text-[10px] font-mono font-bold px-2.5 py-1 border ${
                  isLight ? 'bg-ls-navy text-white border-ls-navy' : 'bg-ls-cyan/20 border-ls-cyan text-ls-cyan'
                }`}>
                  GATE VERIFIED
                </span>
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
};

export default HumanApprovalMatrix;
