import React, { useState } from 'react';
import {
  Brain,
  Bot,
  GitBranch,
  HardDrive,
  Wrench,
  ShieldCheck,
  TrendingUp,
  ArrowRight,
  Shield,
  Lock,
  CheckCircle2,
  FileCheck,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../components/site/SectionHeading';
import { useSectionReveal } from '../hooks/useSectionReveal';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { HaomtgvInfographic } from '../components/haomtgv/HaomtgvInfographic';
import { HaomtgvGlyphGallery } from '../components/haomtgv/HaomtgvGlyphGallery';
import { HaomtgvUnifiedArchitecture } from '../components/haomtgv/HaomtgvUnifiedArchitecture';
import { HaomtgvPipelineDiagram } from '../components/haomtgv/HaomtgvPipelineDiagram';
import { CTAS } from '../data/ctas';

interface HaomtgvPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

const APPROVAL_TIERS = [
  {
    tier: 1,
    name: 'Operational Auto-Execution',
    scope: 'Routine data formatting, low-risk classification, and internal summarization.',
    authority: 'Fully Autonomous Agent (Zero Human Gate)',
    auditLevel: 'Automated Log & Telemetry',
    description: 'Executed instantly by specialized agents under strict deterministic sandbox rules.',
    riskLevel: 'Negligible',
    badgeColor: 'text-cyan-400 bg-cyan-950/40',
  },
  {
    tier: 2,
    name: 'Supervised Recommendation',
    scope: 'Drafting reports, code generation, and moderate operational recommendations.',
    authority: 'Junior Operator Review',
    auditLevel: 'Standard Timestamp & Diff Review',
    description: 'Agent prepares complete draft artifacts requiring single-click human sign-off.',
    riskLevel: 'Low',
    badgeColor: 'text-cyan-400 bg-cyan-950/40',
  },
  {
    tier: 3,
    name: 'Tactical Decision Gate',
    scope: 'Resource allocation, workflow overrides, and departmental integrations.',
    authority: 'Department Lead / Manager',
    auditLevel: 'Structured Audit Trail & Rationale Log',
    description: 'Requires explicit human authorization before agent proceeds with transactional actions.',
    riskLevel: 'Moderate',
    badgeColor: 'text-cyan-300 bg-cyan-950/60',
  },
  {
    tier: 4,
    name: 'Strategic Authority Gate',
    scope: 'Financial commitments, external partnerships, and policy modifications.',
    authority: 'Executive Sponsor / Director',
    auditLevel: 'Cryptographic Sign-Off & Compliance Tag',
    description: 'High-impact boundary requiring verified executive credentials and multi-factor validation.',
    riskLevel: 'High',
    badgeColor: 'text-ls-red bg-ls-red/10',
  },
  {
    tier: 5,
    name: 'Absolute Sovereign Control',
    scope: 'Venture launch, core governance reset, and irreversible system architecture changes.',
    authority: 'Chief Executive Officer / Board',
    auditLevel: 'Immutable Board Ledger & Compliance Archive',
    description: 'The ultimate human accountability anchor. No autonomous agent can bypass Tier 5.',
    riskLevel: 'Critical',
    badgeColor: 'text-ls-red bg-ls-red/20',
  },
];

const WORKFLOW_STEPS = [
  {
    step: '01',
    layer: 'Human Authority',
    letter: 'H',
    title: 'Strategic Intent & Boundary Definition',
    desc: 'Human directors define commercial objectives, acceptable risk limits, and budget parameters.',
    actor: 'Human CEO / Executive',
  },
  {
    step: '02',
    layer: 'Orchestration',
    letter: 'O',
    title: 'Deterministic DAG Decomposition',
    desc: 'The orchestrator translates human intent into a directed task graph with explicit checkpoints.',
    actor: 'Workflow State Engine',
  },
  {
    step: '03',
    layer: 'Persistent Memory',
    letter: 'M',
    title: 'Contextual Knowledge Retrieval',
    desc: 'Context vectors, compliance rules, and historical precedence are queried from isolated memory.',
    actor: 'Tenant Vector Store',
  },
  {
    step: '04',
    layer: 'Configurable Agents',
    letter: 'A',
    title: 'Role-Bounded Task Execution',
    desc: 'Specialized agents execute scoped computational tasks, generating structured artifacts and diffs.',
    actor: 'Configurable Agent Team',
  },
  {
    step: '05',
    layer: 'Sandboxed Tools',
    letter: 'T',
    title: 'Controlled External Invocation',
    desc: 'Sandboxed APIs and containerized kernels execute external transactions under credential limits.',
    actor: 'Sandboxed Tool Proxy',
  },
  {
    step: '06',
    layer: 'Transverse Governance',
    letter: 'G',
    title: 'Human Gatekeeper Authorization',
    desc: 'Automated policy validation inspects outputs; decisions matching Tiers 2-5 require human sign-off.',
    actor: 'Human Approval Matrix',
  },
  {
    step: '07',
    layer: 'Measured Value',
    letter: 'V',
    title: 'Outcome Feedback & Strategy Refinement',
    desc: 'Verified ROI, latency reduction, and quality metrics are delivered back to human leadership.',
    actor: 'Empirical Audit Engine',
  },
];

const BRAND_BAR = ['#070A40', '#DC3641', '#00BFFF'];

export const HaomtgvPage: React.FC<HaomtgvPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const [selectedTier, setSelectedTier] = useState<number>(4);

  // Section Reveal hooks for staged, premium entry
  const heroReveal = useSectionReveal<HTMLElement>({ threshold: 0.05, immediate: true });
  const paradigmReveal = useSectionReveal<HTMLElement>({ threshold: 0.1 });
  const dimensionsReveal = useSectionReveal<HTMLElement>({ threshold: 0.08 });
  const governanceReveal = useSectionReveal<HTMLElement>({ threshold: 0.1 });
  const workflowReveal = useSectionReveal<HTMLElement>({ threshold: 0.08 });
  const visualsReveal = useSectionReveal<HTMLDivElement>({ threshold: 0.08 });
  const ctaReveal = useSectionReveal<HTMLElement>({ threshold: 0.12 });
  const relatedReveal = useSectionReveal<HTMLElement>({ threshold: 0.1 });

  const activeTier =
    APPROVAL_TIERS.find((t) => t.tier === selectedTier) || APPROVAL_TIERS[3];

  return (
    <div
      className={`min-h-screen ${
        isLight ? 'bg-ls-grey-light text-ls-navy' : 'bg-ls-navy-dark text-ls-white'
      }`}
    >
      {/* 1. EXECUTIVE HERO SECTION */}
      <section
        ref={heroReveal.ref}
        className={`relative overflow-hidden ${
          isLight
            ? 'bg-gradient-to-b from-ls-navy via-ls-navy to-ls-navy-dark text-ls-white'
            : 'bg-gradient-to-b from-ls-navy-dark via-ls-navy to-[#050B1A] text-ls-white'
        }`}
      >
        {/* Brand bar */}
        <div aria-hidden="true" className="absolute top-0 left-0 right-0 h-1 flex z-30">
          {BRAND_BAR.map((color) => (
            <div key={color} className="flex-1" style={{ backgroundColor: color }} />
          ))}
        </div>

        {/* Ambient background depth grid */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 opacity-15"
          style={{
            backgroundImage:
              'radial-gradient(circle at 1px 1px, rgba(0,191,255,0.4) 1px, transparent 0)',
            backgroundSize: '40px 40px',
          }}
        />

        <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-12 pt-24 sm:pt-32 pb-20 sm:pb-28">
          <div className="max-w-4xl mx-auto text-center space-y-6">
            <div
              className={heroReveal.getRevealClass(
                'fade',
                1,
                'inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-ls-red/10 text-ls-red font-body font-bold text-xs tracking-widest uppercase'
              )}
            >
              <span>OPERATING ARCHITECTURE</span>
            </div>

            <h1
              id="haomtgv-title"
              className={heroReveal.getRevealClass(
                'up',
                2,
                'text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight font-display text-ls-white'
              )}
            >
              H-A-O-M-T-G-V
            </h1>

            <p
              className={heroReveal.getRevealClass(
                'up',
                3,
                'text-xl sm:text-2xl font-bold font-display text-ls-cyan tracking-wide'
              )}
            >
              Human Authority. Governed Agents. Measured Value.
            </p>

            <p
              className={heroReveal.getRevealClass(
                'fade',
                4,
                'text-base sm:text-lg leading-relaxed text-ls-grey-light-text max-w-3xl mx-auto font-body'
              )}
            >
              The foundational operating system behind the LightSpeed AI-Native Company Builder.
              Machines execute bounded, specialized tasks; human directors retain sovereign
              decision authority. Seven interconnected dimensions orchestrated into an auditable,
              scalable enterprise engine.
            </p>

            {/* Official Tagline Badge */}
            <div className={heroReveal.getRevealClass('fade', 4, 'pt-2')}>
              <span className="inline-block text-xs font-mono font-bold tracking-[0.3em] text-ls-white/80 uppercase px-4 py-1.5 rounded-md bg-white/5">
                ASPIRE. ACT. ACHIEVE.
              </span>
            </div>

            {/* Action buttons */}
            <div
              className={heroReveal.getRevealClass(
                'up',
                5,
                'pt-6 flex flex-wrap items-center justify-center gap-4'
              )}
            >
              <button
                type="button"
                onClick={() =>
                  onRequestBriefing?.(
                    'HAOMTGV Operating Architecture Briefing: Request for Enterprise Blueprint'
                  )
                }
                className="inline-flex items-center gap-2.5 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90 hover:scale-[1.02] active:scale-[0.98]"
              >
                Request Architecture Briefing
                <ArrowRight className="w-4 h-4" aria-hidden="true" />
              </button>
              <a
                href="#dimensions-explorer"
                className="inline-flex items-center gap-2 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase text-ls-cyan bg-ls-cyan/10 transition-all hover:bg-ls-cyan/20 active:scale-[0.98]"
              >
                Explore 7 Dimensions
              </a>
              <a
                href="#governance-matrix"
                className="inline-flex items-center gap-2 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase text-ls-white bg-white/10 transition-all hover:bg-white/15 active:scale-[0.98]"
              >
                Approval Matrix
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* 2. THE ARCHITECTURAL PARADIGM: WHY HAOMTGV MATTERS */}
      <section
        ref={paradigmReveal.ref}
        className={`py-16 sm:py-24 ${
          isLight ? 'bg-ls-white' : 'bg-ls-navy/60'
        }`}
      >
        <div className="max-w-7xl mx-auto px-6 lg:px-12">
          <div className={paradigmReveal.getRevealClass('fade', 1)}>
            <SectionHeading
              theme={theme}
              eyebrow="THE ARCHITECTURAL PARADIGM"
              title="Beyond Black-Box Prompts: Governed Enterprise Execution"
              lead="Traditional AI deployments fail because they treat large language models as unconstrained chatbots. HAOMTGV treats AI as a governed execution layer constrained by deterministic orchestration and sovereign human oversight."
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-12">
            {/* Unbounded Chaos */}
            <div className={paradigmReveal.getRevealClass('up', 2, 'h-full')}>
              <div
                className={`rounded-2xl p-8 h-full flex flex-col justify-between ${
                  isLight
                    ? 'bg-slate-100 text-slate-800 shadow-sm'
                    : 'bg-ls-navy-dark/90 text-slate-200 shadow-xl'
                }`}
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-bold tracking-widest text-ls-red uppercase">
                      UNBOUNDED AI EXPERIMENTATION
                    </span>
                    <span className="text-xs font-mono text-slate-500">Traditional Approach</span>
                  </div>
                  <h3 className="text-2xl font-bold font-display tracking-tight text-ls-red">
                    The High-Risk Black Box
                  </h3>
                  <p className="text-sm leading-relaxed text-slate-400">
                    Deploying generic chatbots with unstructured prompt instructions and direct
                    database access introduces unvetted hallucination risk, compliance breaches, and
                    cost blowouts.
                  </p>
                  <ul className="space-y-2.5 pt-2 text-xs text-slate-400 font-body">
                    <li className="flex items-start gap-2">
                      <span className="text-ls-red font-bold">✕</span>
                      <span>Uncontrolled model autonomy with zero hard decision gates</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-ls-red font-bold">✕</span>
                      <span>Ephemeral context loss across multi-step enterprise workflows</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-ls-red font-bold">✕</span>
                      <span>Direct credential exposure and unvetted API execution</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-ls-red font-bold">✕</span>
                      <span>No cryptographic audit trails or regulatory accountability</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Governed HAOMTGV */}
            <div className={paradigmReveal.getRevealClass('up', 3, 'h-full')}>
              <div
                className={`rounded-2xl p-8 h-full flex flex-col justify-between ${
                  isLight
                    ? 'bg-ls-white text-ls-navy shadow-lg shadow-ls-cyan/5'
                    : 'bg-ls-navy/90 text-ls-white shadow-2xl shadow-ls-cyan/10'
                }`}
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-bold tracking-widest text-ls-cyan uppercase">
                      GOVERNED HAOMTGV OPERATING SYSTEM
                    </span>
                    <span className="text-xs font-mono text-ls-cyan font-bold">LightSpeed Standard</span>
                  </div>
                  <h3 className="text-2xl font-bold font-display tracking-tight text-ls-cyan">
                    Deterministic, Scalable Control
                  </h3>
                  <p className="text-sm leading-relaxed text-slate-300">
                    A multi-layered architecture where human authority runs through every phase,
                    governance permeates every tool call, and business outcomes are measured
                    empirically.
                  </p>
                  <ul className="space-y-2.5 pt-2 text-xs text-slate-300 font-body">
                    <li className="flex items-start gap-2">
                      <span className="text-ls-cyan font-bold">✓</span>
                      <span>Pinnacle Human Authority with non-negotiable sovereign veto</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-ls-cyan font-bold">✓</span>
                      <span>Configurable AI agent teams scaling from 1 to N+ specialized roles</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-ls-cyan font-bold">✓</span>
                      <span>Deterministic DAG orchestration with persistent tenant memory</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-ls-cyan font-bold">✓</span>
                      <span>Transverse Five-Tier Human Approval Matrix with SHA-256 state receipts</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. UNIFIED INTERACTIVE 7-DIMENSION ARCHITECTURE EXPLORER */}
      <section
        id="dimensions-explorer"
        ref={dimensionsReveal.ref}
        className={`py-20 sm:py-28 ${
          isLight ? 'bg-slate-100' : 'bg-ls-navy-dark'
        }`}
      >
        <div className="max-w-7xl mx-auto px-6 lg:px-12">
          <div className={dimensionsReveal.getRevealClass('fade', 1)}>
            <SectionHeading
              theme={theme}
              eyebrow="THE SEVEN DIMENSIONS"
              title="Unified Operating Architecture"
              lead="An integrated architectural view of the seven HAOMTGV dimensions: Human Authority at the sovereign pinnacle, continuous Governance spanning every layer, deterministic core execution, and empirical Value closing the strategic feedback loop."
            />
          </div>

          <div className={dimensionsReveal.getRevealClass('up', 2, 'mt-12')}>
            <HaomtgvUnifiedArchitecture theme={theme} />
          </div>
        </div>
      </section>

      {/* 4. TRANSVERSE GOVERNANCE & 5-TIER HUMAN APPROVAL MATRIX */}
      <section
        id="governance-matrix"
        ref={governanceReveal.ref}
        className={`py-20 sm:py-28 ${
          isLight ? 'bg-ls-white' : 'bg-ls-navy/80'
        }`}
      >
        <div className="max-w-7xl mx-auto px-6 lg:px-12">
          <div className={governanceReveal.getRevealClass('fade', 1)}>
            <SectionHeading
              theme={theme}
              eyebrow="CONTINUOUS GOVERNANCE FABRIC"
              title="The Five-Tier Human Approval Matrix"
              lead="Governance in HAOMTGV is not an afterthought or a final checkpoint. It is a continuous, transverse control fabric spanning every dimension. High-risk decisions are cryptographically gated by human authorities."
            />
          </div>

          {/* Interactive Tier Matrix */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-12 items-start">
            {/* Tier Selector Buttons */}
            <div className={governanceReveal.getRevealClass('up', 2, 'lg:col-span-5 space-y-3')}>
              {APPROVAL_TIERS.map((tier) => {
                const isSelected = tier.tier === selectedTier;
                return (
                  <button
                    key={tier.tier}
                    onClick={() => setSelectedTier(tier.tier)}
                    type="button"
                    className={`w-full text-left p-4 rounded-2xl transition-all cursor-pointer flex items-center justify-between ${
                      isSelected
                        ? tier.tier >= 4
                          ? 'bg-ls-red/15 text-ls-white shadow-lg shadow-ls-red/10'
                          : 'bg-cyan-950/60 text-ls-white shadow-lg shadow-ls-cyan/10'
                        : isLight
                        ? 'bg-slate-100 text-slate-800 hover:bg-slate-200/70'
                        : 'bg-ls-navy-dark/60 text-slate-400 hover:text-white hover:bg-ls-navy/70'
                    }`}
                  >
                    <div className="flex items-center gap-4">
                      <span
                        className={`w-9 h-9 rounded-xl flex items-center justify-center font-mono text-xs font-bold ${
                          isSelected
                            ? tier.tier >= 4
                              ? 'bg-ls-red text-white'
                              : 'bg-ls-cyan text-ls-navy'
                            : 'bg-slate-800 text-slate-300'
                        }`}
                      >
                        0{tier.tier}
                      </span>
                      <div>
                        <h4 className="text-sm font-bold tracking-tight text-ls-white">
                          {tier.name}
                        </h4>
                        <p className="text-xs text-slate-400 truncate max-w-[240px]">
                          {tier.authority}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span
                        className={`text-[10px] font-mono px-2 py-0.5 rounded ${tier.badgeColor}`}
                      >
                        {tier.riskLevel}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Detailed Inspector Card */}
            <div
              className={governanceReveal.getRevealClass(
                'up',
                3,
                `lg:col-span-7 rounded-3xl p-8 shadow-2xl relative overflow-hidden longform-contrast-layer`
              )}
            >
              <div className="absolute top-0 right-0 p-6 opacity-10 pointer-events-none">
                <Shield className="w-36 h-36 text-ls-cyan" />
              </div>

              <div className="relative z-10 space-y-6">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-xs font-mono font-bold text-ls-cyan uppercase tracking-widest px-3 py-1 bg-ls-cyan/10 rounded-md">
                    Tier 0{activeTier.tier} Governance Protocol
                  </span>
                  <span className="text-xs text-slate-400 flex items-center gap-1.5 font-mono">
                    <Lock className="w-3.5 h-3.5 text-ls-red" />
                    <span>Cryptographic Decision Gate</span>
                  </span>
                </div>

                <div>
                  <h3 className={`text-2xl font-bold font-display tracking-tight mb-2 ${
                    isLight ? 'text-ls-navy' : 'text-white'
                  }`}>
                    {activeTier.name}
                  </h3>
                  <p
                    className={`text-sm sm:text-base leading-relaxed ${
                      isLight ? 'text-slate-800' : 'text-slate-200'
                    }`}
                  >
                    {activeTier.description}
                  </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
                  <div
                    className={`p-4 rounded-xl ${
                      isLight
                        ? 'bg-slate-50 border border-slate-200'
                        : 'bg-ls-navy/60 border border-white/10'
                    }`}
                  >
                    <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1 font-mono">
                      Operational Scope
                    </span>
                    <p className={`text-sm font-semibold ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {activeTier.scope}
                    </p>
                  </div>

                  <div
                    className={`p-4 rounded-xl ${
                      isLight
                        ? 'bg-slate-50 border border-slate-200'
                        : 'bg-ls-navy/60 border border-white/10'
                    }`}
                  >
                    <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1 font-mono">
                      Decision Authority
                    </span>
                    <p className="text-sm font-semibold text-ls-cyan">{activeTier.authority}</p>
                  </div>
                </div>

                <div
                  className={`p-4 rounded-xl flex flex-wrap items-center justify-between gap-4 ${
                    isLight
                      ? 'bg-slate-50 border border-slate-200'
                      : 'bg-ls-navy/60 border border-white/10'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <FileCheck className="w-5 h-5 text-ls-cyan shrink-0" />
                    <div>
                      <span className="text-xs text-slate-400 block font-mono">
                        Audit & Accountability Mechanism
                      </span>
                      <span className={`text-sm font-medium ${isLight ? 'text-slate-900' : 'text-white'}`}>
                        {activeTier.auditLevel}
                      </span>
                    </div>
                  </div>
                  <span className="text-xs font-mono px-2.5 py-1 bg-emerald-950 text-emerald-300 rounded">
                    SHA-256 Ledger Verified
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. END-TO-END ORCHESTRATION CYCLE (HOW THE 7 LAYERS COLLABORATE) */}
      <section
        ref={workflowReveal.ref}
        className={`py-20 sm:py-28 ${
          isLight ? 'bg-slate-100' : 'bg-ls-navy-dark'
        }`}
      >
        <div className="max-w-7xl mx-auto px-6 lg:px-12">
          <div className={workflowReveal.getRevealClass('fade', 1)}>
            <SectionHeading
              theme={theme}
              eyebrow="CLOSED-LOOP EXECUTION"
              title="How the Architecture Executes Work"
              lead="A real-world walkthrough illustrating how strategic human intent cascades through orchestration, memory, configurable agents, and tools under continuous governance to deliver verified value."
            />
            <div className="mt-12">
              <HaomtgvPipelineDiagram theme={theme} />
            </div>
          </div>

          <div className="mt-12 space-y-4">
            {WORKFLOW_STEPS.map((step, idx) => {
              const isGov = step.letter === 'G';
              const delayIndex = (((idx % 6) + 1) as 1 | 2 | 3 | 4 | 5 | 6);
              return (
                <div
                  key={step.step}
                  className={workflowReveal.getRevealClass(
                    'up',
                    delayIndex,
                    `rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 transition-all ${
                      isGov
                        ? 'bg-ls-red/10 shadow-md'
                        : isLight
                        ? 'bg-ls-white shadow-sm'
                        : 'bg-ls-navy/80 shadow-md'
                    }`
                  )}
                >
                  <div className="flex items-center gap-4">
                    <span className="font-mono text-xs font-bold text-slate-500">
                      {step.step}
                    </span>
                    <span
                      className={`w-9 h-9 rounded-xl flex items-center justify-center font-display font-black text-sm ${
                        isGov
                          ? 'bg-ls-red text-white'
                          : 'bg-ls-cyan text-ls-navy'
                      }`}
                    >
                      {step.letter}
                    </span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`text-xs font-mono font-bold uppercase ${
                            isGov ? 'text-ls-red' : 'text-ls-cyan'
                          }`}
                        >
                          {step.layer}
                        </span>
                        <span className="text-[10px] text-slate-500 font-mono">
                          • {step.actor}
                        </span>
                      </div>
                      <h4 className="text-base font-bold font-display tracking-tight text-ls-white">
                        {step.title}
                      </h4>
                    </div>
                  </div>
                  <p
                    className={`text-xs md:max-w-md ${
                      isLight ? 'text-slate-600' : 'text-slate-300'
                    }`}
                  >
                    {step.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* 6. CANONICAL MEDIA VISUALS: GLYPHS & INFOGRAPHIC */}
      <div ref={visualsReveal.ref} className="space-y-0">
        <div className={visualsReveal.getRevealClass('fade', 1)}>
          <HaomtgvGlyphGallery theme={theme} />
        </div>
        <div className={visualsReveal.getRevealClass('up', 2)}>
          <HaomtgvInfographic theme={theme} />
        </div>
      </div>

      {/* 7. STRATEGIC CTA BAND */}
      <section
        ref={ctaReveal.ref}
        className={`py-20 ${
          isLight ? 'bg-ls-navy text-ls-white' : 'bg-ls-navy text-ls-white'
        }`}
      >
        <div className="max-w-4xl mx-auto px-6 text-center space-y-6">
          <span
            className={ctaReveal.getRevealClass(
              'fade',
              1,
              'text-xs font-mono font-bold tracking-widest text-ls-red uppercase block'
            )}
          >
            ENTERPRISE DEPLOYMENT
          </span>
          <h2
            className={ctaReveal.getRevealClass(
              'up',
              2,
              'text-3xl sm:text-5xl font-black font-display tracking-tight text-ls-white'
            )}
          >
            Ready to Deploy Governed AI in Your Organization?
          </h2>
          <p
            className={ctaReveal.getRevealClass(
              'fade',
              3,
              'text-sm sm:text-base leading-relaxed text-ls-grey-light-text max-w-2xl mx-auto font-body'
            )}
          >
            Schedule an architectural briefing with LightSpeed leadership. We will evaluate your
            workflows, map them to the HAOMTGV operating model, and demonstrate how configurable
            agent teams operate under sovereign human governance.
          </p>

          <div
            className={ctaReveal.getRevealClass(
              'up',
              4,
              'pt-4 flex flex-wrap items-center justify-center gap-4'
            )}
          >
            <button
              type="button"
              onClick={() =>
                onRequestBriefing?.(
                  'HAOMTGV Architecture: Executive Implementation Discussion'
                )
              }
              className="inline-flex items-center gap-2.5 px-8 py-4 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-xl shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90 hover:scale-[1.02] active:scale-[0.98]"
            >
              {CTAS.primary.label}
              <ArrowRight className="w-4 h-4" aria-hidden="true" />
            </button>
            <Link
              to="/ai-company-builder"
              className="inline-flex items-center gap-2 px-7 py-4 rounded-full font-bold text-xs tracking-widest uppercase text-ls-white bg-white/10 transition-all hover:bg-white/15 active:scale-[0.98]"
            >
              Explore AI Company Builder
            </Link>
          </div>
        </div>
      </section>

      {/* Brand Color Bar */}
      <div aria-hidden="true" className="h-1 flex">
        {BRAND_BAR.map((color) => (
          <div key={color} className="flex-1" style={{ backgroundColor: color }} />
        ))}
      </div>

      {/* 8. RELATED ARCHITECTURAL LINKS */}
      <section ref={relatedReveal.ref} className={relatedReveal.getRevealClass('fade', 1)}>
        <RelatedLinks
          theme={theme}
          links={[
            { to: '/sectors', label: 'Sectors' },
            { to: '/solutions', label: 'Solutions' },
            { to: '/what-we-do', label: 'What We Do' },
            { to: '/insights', label: 'Pharos Insights' },
          ]}
        />
      </section>
    </div>
  );
};

export default HaomtgvPage;
