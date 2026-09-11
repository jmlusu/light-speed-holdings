import React from 'react';
import {
  Activity,
  ArrowRight,
  CheckCircle2,
  Coins,
  FileCheck,
  GitMerge,
  ShieldCheck,
} from 'lucide-react';
import { AcousticVentGrille } from '../components/TactileHardwareElements';

interface EvidencePageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

interface Metric {
  value: string;
  label: string;
  source: string;
}

interface Method {
  icon: React.ComponentType<{ className?: string }>;
  step: string;
  title: string;
  detail: string;
}

const METRICS: Metric[] = [
  {
    value: '144',
    label: 'Verified Agent Configurations',
    source: 'company-registry.yaml',
  },
  {
    value: '2,373',
    label: 'Automated Regression Tests',
    source: 'pytest suite',
  },
  {
    value: '20',
    label: 'Departments Modeled',
    source: 'company-registry.yaml',
  },
  {
    value: '5-TIER',
    label: 'Human Approval Gates',
    source: 'ApprovalGate matrix',
  },
];

const METHODS: Method[] = [
  {
    icon: GitMerge,
    step: '01',
    title: 'AST-only knowledge graph',
    detail: 'Rebuilt post-commit by graphify. Structure only — no transcript dumping, no API cost.',
  },
  {
    icon: FileCheck,
    step: '02',
    title: 'Four-gate CI on every patch',
    detail: 'ruff + mypy + bandit + 2,373 pytest gates must pass before a change lands.',
  },
  {
    icon: Coins,
    step: '03',
    title: 'Per-request cost tracking',
    detail: 'An OpenAI-compatible usage ledger records token and spend per request.',
  },
  {
    icon: ShieldCheck,
    step: '04',
    title: 'Human approval + expiry sweep',
    detail: 'HITL approval gates and ApprovalGate expiry sweeps are reported on the control plane.',
  },
];

const HONESTY_POLICY: string[] = [
  'We publish the tests that gate our own work.',
  'Claims are labeled Proven in-house vs. In pilot — we do not blur them.',
  'Benchmarks are dated and regenerated on every release.',
];

interface ProofCardData {
  id: string;
  title: string;
  badge: string;
  text: string;
  tone: 'cyan' | 'slate';
  featured?: boolean;
}

const PROOF_CASES: ProofCardData[] = [
  {
    id: 'PC-01',
    title: 'J&S StopOver Bar — SME AI Transformation',
    badge: 'Proven in-house — live proof, not a paid client.',
    tone: 'cyan',
    featured: true,
    text: 'A real, non-tech SME in Malawi running agentic decision support: inventory, sales, shortage detection, cash reconciliation, procurement triggers, and profitability tracking. The world\'s smallest AI-native bar — a genuinely African SME AI transformation case, built in-house and documented openly.',
  },
  {
    id: 'PC-04',
    title: 'Lightspeed Holdings — The Meta Case Study',
    badge: 'Proven in-house.',
    tone: 'cyan',
    text: 'The company is its own first customer. 144 agents across 20 departments, five-tier HITL approvals, immutable audit trails, RACI matrices, and governance controls mapped to regulatory requirements — operating daily. Not a demo; an operating company that builds the tooling it uses.',
  },
  {
    id: 'PC-02',
    title: 'Health / M&E — Clinic Supply Chain Monitoring',
    badge: 'In pilot (composing evidence).',
    tone: 'cyan',
    text: 'Agentic workflows for monitoring clinic supply chains and auto-generating procurement requests on anomaly detection (dashboard Z-score triggers). No confirmed partnership with any named health organization has been signed.',
  },
  {
    id: 'PC-03',
    title: 'VSLA / SACCO / Mobile Money — Financial Inclusion',
    badge: 'In pilot (use case in active development).',
    tone: 'cyan',
    text: 'Agentic workflows over mobile-money rails (Airtel Money, TNM Mpamba) for informal savings groups and micro-finance institutions. No signed engagement exists.',
  },
  {
    id: 'PC-05',
    title: 'Chichewa AI / Ministry of Agriculture — Farmer Advisory',
    badge: 'In pilot.',
    tone: 'cyan',
    text: 'Building the foundation for farmer advisory, citizen-query, and public-service agents in partnership with the Ministry of Agriculture. The capability is in pilot development.',
  },
];

const POLICY_ITEMS: ProofCardData[] = [
  {
    id: 'POL-01',
    title: 'Citizen-Inquiry Lighthouse (Proposed)',
    badge: 'In pilot (proposed — not yet launched).',
    tone: 'cyan',
    text: 'LightSpeed is prepared to pilot a high-visibility lighthouse use case — a citizen-inquiry or legislative-summary agent — with a non-commercial partner, as part of the National AI Strategy consultation. Proposed, not yet launched.',
  },
  {
    id: 'POL-02',
    title: 'Governance Controls as National Template',
    badge: 'Proven in-house.',
    tone: 'cyan',
    text: 'LightSpeed already operates the governance pattern it proposes as a national template: 5-tier approvals, immutable audit trails, RACI matrices, risk-classified agent tiers, and 4-gate client onboarding (G1–G4). Offered as a template for Malawi\'s Department of E-Government and MACRA, and as a reference model for SADC harmonisation.',
  },
  {
    id: 'POL-03',
    title: 'Capacity Building',
    badge: 'In active development.',
    tone: 'slate',
    text: 'Training and certification programmes in partnership with Malawian universities (MUBAS, UNIMA) to build a sovereign agentic-AI talent pipeline for Malawi and the SADC region.',
  },
  {
    id: 'SADC',
    title: 'National AI Strategy + SADC Framework',
    badge: 'Published (National AI Strategy) / In active development (SADC Framework).',
    tone: 'slate',
    text: 'The SADC Agentic AI Governance Framework is the region\'s first operational governance standard for autonomous agentic AI — authored by the CEO and submitted to SADC Member State digital ministers and telecom regulators (MACRA, CRASA), central banks, and regional development banks. The National AI Strategy consultation submission has been published, proposing lighthouse use cases and governance architecture for the Department of E-Government.',
  },
];

const ProofCard: React.FC<{ card: ProofCardData; isLight: boolean; featured?: boolean }> = ({
  card,
  isLight,
  featured = false,
}) => {
  const badgeClasses =
    card.tone === 'slate'
      ? 'border-slate-400/40 bg-slate-400/10 text-slate-400'
      : 'border-ls-cyan/40 bg-ls-cyan/10 text-ls-cyan';

  return (
    <div
      className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 flex flex-col ${
        featured ? 'md:col-span-2' : ''
      } ${isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'}`}
    >
      {/* Hardware corner screws */}
      <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
      <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="font-mono text-[10px] sm:text-[11px] font-bold tracking-widest text-ls-red">
          {card.id}
        </span>
        <span
          className={`rounded-full border px-2.5 py-1 font-mono text-[9px] sm:text-[10px] font-bold tracking-widest ${badgeClasses}`}
        >
          {card.badge}
        </span>
      </div>

      <h3 className={`mt-4 text-base sm:text-lg font-black tracking-tight ${isLight ? 'text-slate-900' : 'text-white'}`}>
        {card.title}
      </h3>
      <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700 font-medium' : 'text-zinc-400'}`}>
        {card.text}
      </p>
    </div>
  );
};

/**
 * Evidence route: a dedicated, traceable proof page. Every figure maps to a
 * file, a test, or a governance gate that runs inside this repository.
 */
export const EvidencePage: React.FC<EvidencePageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      {/* Page Intro */}
      <header className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-24 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
          <Activity className="w-3.5 h-3.5" aria-hidden="true" />
          <span>EVIDENCE &amp; RESULTS</span>
        </div>
        <h1 className={`mt-4 text-3xl sm:text-5xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}>
          Built in the Open. Measured by Machine.
        </h1>
        <p className={`mt-4 max-w-2xl text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          Every number below traces to a file, a test, or a governance gate that runs in our own
          repository — published, dated, and regenerated on every release.
        </p>
      </header>

      {/* Metrics Band */}
      <section
        aria-labelledby="evidence-metrics-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-4"
      >
        <h2 id="evidence-metrics-heading" className="sr-only">
          Verified platform metrics
        </h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {METRICS.map((metric) => (
            <div
              key={metric.label}
              className={`relative overflow-hidden rounded-3xl p-6 text-center ${
                isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
              }`}
            >
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              <div className={`font-mono text-4xl sm:text-5xl font-black tracking-tight ${
                isLight ? 'text-slate-900' : 'text-white'
              }`}>
                {metric.value}
              </div>
              <div className="mt-3 font-mono text-[10px] sm:text-[11px] font-bold uppercase tracking-widest text-ls-red">
                {metric.label}
              </div>
              <div className={`mt-2 font-mono text-[10px] tracking-wide ${
                isLight ? 'text-slate-500' : 'text-zinc-500'
              }`}>
                {metric.source}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* How We Measure — Mono Panel */}
      <section
        aria-labelledby="evidence-method-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20"
      >
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
            METHOD
          </span>
          <h2
            id="evidence-method-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}
          >
            How We Measure
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Four automated loops keep this page honest between releases.
          </p>
        </div>

        <div className={`relative overflow-hidden rounded-3xl p-6 sm:p-10 shadow-2xl ${
          isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
        }`}>
          {/* Hardware corner screws */}
          <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

          {/* Console header bar */}
          <div className="flex items-center justify-between pb-3.5 mb-6 border-b border-black/10 dark:border-white/10 px-1">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-ls-red shadow-[0_0_8px_rgba(230,57,70,0.9)]" />
              <span className="font-mono text-xs font-bold tracking-wider">
                MEASUREMENT CONSOLE // CONTINUOUS
              </span>
            </div>
            <AcousticVentGrille variant="strip" isLight={isLight} />
          </div>

          <ol className="space-y-3">
            {METHODS.map((method) => {
              const Icon = method.icon;
              return (
                <li
                  key={method.step}
                  className={`rounded-2xl p-4 sm:p-5 ${isLight ? 'hardware-well-light' : 'hardware-well-dark'}`}
                >
                  <div className="flex items-start gap-4">
                    <span className="font-mono text-xs font-bold text-ls-red pt-0.5">{method.step}</span>
                    <span aria-hidden="true" className="pt-0.5">
                      <Icon className="w-5 h-5 shrink-0 text-ls-cyan" />
                    </span>
                    <div className="flex-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <h3 className={`text-sm sm:text-base font-bold tracking-tight ${
                          isLight ? 'text-slate-900' : 'text-zinc-100'
                        }`}>
                          {method.title}
                        </h3>
                        <span className="rounded-full border border-ls-cyan/40 bg-ls-cyan/10 px-2 py-0.5 font-mono text-[9px] font-bold tracking-widest text-ls-cyan">
                          PROVEN IN-HOUSE
                        </span>
                      </div>
                      <p className={`mt-1 text-xs sm:text-sm leading-relaxed ${
                        isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
                      }`}>
                        {method.detail}
                      </p>
                    </div>
                  </div>
                </li>
              );
            })}
          </ol>
        </div>
      </section>

      {/* Proof Cases — Honesty-Badged */}
      <section
        aria-labelledby="evidence-proof-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
            PROOF // HONESTY-BADGED
          </span>
          <h2
            id="evidence-proof-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}
          >
            Proof Cases &amp; Pilots
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Nothing has been delivered to paying clients yet. Every proof point below carries its honest status.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {PROOF_CASES.map((proof) => (
            <ProofCard key={proof.id} card={proof} isLight={isLight} featured={proof.featured} />
          ))}
        </div>
      </section>

      {/* Policy Track — Regional Governance */}
      <section
        aria-labelledby="evidence-policy-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
            POLICY // REGIONAL GOVERNANCE
          </span>
          <h2
            id="evidence-policy-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}
          >
            Shaping the Policy That Governs AI
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            LightSpeed does not only build agentic AI — it shapes the policy that governs it across Malawi and SADC.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {POLICY_ITEMS.map((item) => (
            <ProofCard key={item.id} card={item} isLight={isLight} />
          ))}
        </div>
      </section>

      {/* Honesty Policy Strip */}
      <section
        aria-labelledby="evidence-honesty-heading"
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20 border-t ${
          isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
        }`}
      >
        <h2
          id="evidence-honesty-heading"
          className="mb-6 font-mono text-xs font-bold tracking-widest text-ls-red"
        >
          HONESTY POLICY
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {HONESTY_POLICY.map((statement) => (
            <div
              key={statement}
              className={`rounded-2xl p-5 ${isLight ? 'hardware-well-light' : 'hardware-well-dark'}`}
            >
              <CheckCircle2 className="w-4 h-4 text-ls-cyan" aria-hidden="true" />
              <p className={`mt-3 font-mono text-xs sm:text-sm leading-relaxed ${
                isLight ? 'text-slate-800' : 'text-ls-cyan'
              }`}>
                {statement}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Closing CTA */}
      <section
        aria-labelledby="evidence-cta-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pb-20 sm:pb-28"
      >
        <h2 id="evidence-cta-heading" className="sr-only">
          Request the evidence pack
        </h2>
        <div className="text-center">
          <button
            type="button"
            onClick={() => onRequestBriefing('Evidence pack: metrics, test suite, registry')}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-ls-red px-8 py-4 font-bold text-xs tracking-widest text-white shadow-lg shadow-ls-red/25 transition-all hover:bg-ls-red/90 active:scale-98 cursor-pointer"
          >
            <span>Request the Evidence Pack</span>
            <ArrowRight className="w-4 h-4" aria-hidden="true" />
          </button>
        </div>
      </section>
    </>
  );
};

export default EvidencePage;
