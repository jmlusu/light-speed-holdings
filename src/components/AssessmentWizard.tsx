import React, { useState } from 'react';
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  Database,
  Cpu,
  ShieldCheck,
  Users,
  Zap,
  RotateCcw,
  Sparkles,
  Info,
  ShieldAlert,
} from 'lucide-react';
import { Reveal } from './Reveal';

interface AssessmentWizardProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export type ReadinessLevel = 'Foundational' | 'Developing' | 'Advanced' | 'Optimized';

export interface QuestionOption {
  label: string;
  description: string;
  level: ReadinessLevel;
  recommendation: string;
}

export interface AssessmentDomain {
  id: string;
  title: string;
  eyebrow: string;
  icon: React.ComponentType<{ className?: string }>;
  question: string;
  description: string;
  options: QuestionOption[];
}

export const DOMAINS: AssessmentDomain[] = [
  {
    id: 'data-sovereignty',
    title: 'Data Maturity & Sovereignty',
    eyebrow: 'DOMAIN 01 / 05',
    icon: Database,
    question:
      'How would you describe your organization’s current data infrastructure and access governance?',
    description:
      'Evaluates operational data availability, structured pipelines, access controls, and localized data sovereignty posture.',
    options: [
      {
        label: 'Foundational — Fragmented & Siloed Data',
        description:
          'Data is stored across legacy databases or spreadsheets with manual access requests and limited central governance.',
        level: 'Foundational',
        recommendation:
          'Establish unified data schemas, localized storage policies, and centralized role-based access controls.',
      },
      {
        label: 'Developing — Centralized Storage, Manual APIs',
        description:
          'Core operational data is centralized in data warehouses with basic access controls, but real-time API access remains restricted.',
        level: 'Developing',
        recommendation:
          'Expose secure REST/GraphQL endpoints and event streams to enable real-time agentic data queries.',
      },
      {
        label: 'Advanced — API-First Architecture & Structured Streams',
        description:
          'Well-structured data pipelines with role-based access controls, event streams, and defined data ownership across departments.',
        level: 'Advanced',
        recommendation:
          'Integrate cryptographic audit logging and localized sovereignty boundaries for sensitive operational data.',
      },
      {
        label: 'Optimized — Governed Real-Time Data & Cryptographic Trails',
        description:
          'Governed, real-time data layer with cryptographic audit trails, localized data sovereignty controls, and automated compliance policy enforcement.',
        level: 'Optimized',
        recommendation:
          'Maintain append-only SHA-256 sealed audit trails and zero-cloud PII boundary controls for sensitive workflows.',
      },
    ],
  },
  {
    id: 'infrastructure-integration',
    title: 'Infrastructure & Integration',
    eyebrow: 'DOMAIN 02 / 05',
    icon: Cpu,
    question:
      'What is the readiness of your core systems to integrate with autonomous or semi-autonomous AI agents?',
    description:
      'Evaluates core IT architecture, API ecosystem, event queues, and deployment environment readiness.',
    options: [
      {
        label: 'Foundational — Legacy Monoliths & Batch Operations',
        description:
          'Legacy or monolithic systems requiring custom scrapers, batch files, or manual data entry with no webhooks or REST APIs.',
        level: 'Foundational',
        recommendation:
          'Implement API wrapper layers or microservice gateways around legacy core systems.',
      },
      {
        label: 'Developing — Hybrid Cloud & Webhook Integrations',
        description:
          'Mixed environment with several cloud services offering REST APIs, but integration requires custom middleware and manual triggers.',
        level: 'Developing',
        recommendation:
          'Deploy deterministic MessageBus queues and standardize tool interfaces for multi-agent routing.',
      },
      {
        label: 'Advanced — Event-Driven Queue & Microservices',
        description:
          'API-first architecture with event-driven message queues, microservices, and containerized deployment pipelines.',
        level: 'Advanced',
        recommendation:
          'Incorporate latency-aware agent routing and local Ollama model options for zero-API-cost execution.',
      },
      {
        label: 'Optimized — Sovereign MessageBus & Multi-Provider Stack',
        description:
          'Modular, hybrid-cloud or sovereign edge infrastructure with secure MessageBus orchestration, rate-limited agent tools, and multi-provider failover.',
        level: 'Optimized',
        recommendation:
          'Scale agentic throughput with automated health checks, circuit breakers, and rate-aware model selection.',
      },
    ],
  },
  {
    id: 'governance-haomtgv',
    title: 'Governance & HAOMTGV Alignment',
    eyebrow: 'DOMAIN 03 / 05',
    icon: ShieldCheck,
    question:
      'How are decision rights, approval gates, and accountability currently structured for automated operations?',
    description:
      'Evaluates Human-in-the-Loop (HITL) frameworks, risk classifications, sign-off hierarchies, and compliance controls.',
    options: [
      {
        label: 'Foundational — Informal & Ad-Hoc Approvals',
        description:
          'Ad-hoc decision-making with informal approval steps and no formal AI risk classification or audit logging.',
        level: 'Foundational',
        recommendation:
          'Define formal risk classification tiers for all automated tasks and mandate human sign-off for financial/regulatory actions.',
      },
      {
        label: 'Developing — Documented Approval Workflows',
        description:
          'Documented departmental approval workflows with basic sign-off requirements, but AI usage is ad-hoc or unmonitored.',
        level: 'Developing',
        recommendation:
          'Implement explicit 5-tier Human-in-the-Loop approval gating mapped to organizational authorization levels.',
      },
      {
        label: 'Advanced — Risk-Classified HITL Approval Gates',
        description:
          'Formal risk classification tiers for automated tasks with human-in-the-Loop sign-off for critical financial or regulatory actions.',
        level: 'Advanced',
        recommendation:
          'Enforce append-only SHA-256 audit sealing on all human sign-offs and automated expiry sweeps on stale approvals.',
      },
      {
        label: 'Optimized — 5-Tier Gated Matrix & Cryptographic Audit',
        description:
          'Multi-tier Human-in-the-Loop (HITL) approval matrix (Tier 1 Auto to Tier 5 Executive) with append-only cryptographically sealed audit trails.',
        level: 'Optimized',
        recommendation:
          'Sustain continuous regulatory compliance monitoring and automated audit preparation packages for institutional review.',
      },
    ],
  },
  {
    id: 'talent-change',
    title: 'Talent & Change Readiness',
    eyebrow: 'DOMAIN 04 / 05',
    icon: Users,
    question:
      'How prepared is your leadership and workforce to direct and collaborate with AI agentic teams?',
    description:
      'Evaluates organizational capacity, prompt engineering skills, agent delegation fluency, and change management.',
    options: [
      {
        label: 'Foundational — Ad-Hoc Assistant Awareness',
        description:
          'Limited internal familiarity with agentic workflows; AI is viewed primarily as an experimental search or drafting assistant.',
        level: 'Foundational',
        recommendation:
          'Conduct executive briefing sessions and foundational agent delegation workshops for key department leads.',
      },
      {
        label: 'Developing — Specialized IT & Analytics Adoption',
        description:
          'Specific teams (e.g. IT, Analytics) utilize AI tooling, but broader business units lack structured agent delegation frameworks.',
        level: 'Developing',
        recommendation:
          'Establish departmental agent champions and formal RACI matrices for human-AI task ownership.',
      },
      {
        label: 'Advanced — Departmental Agent Delegation',
        description:
          'Department leads understand role-scoped agent delegation and actively manage hybrid human-AI workflows for routine tasks.',
        level: 'Advanced',
        recommendation:
          'Expand agentic capacity across cross-departmental workflows and establish continuous feedback loops.',
      },
      {
        label: 'Optimized — Executive AI-Native Operating Culture',
        description:
          'Executive leadership actively stewards an AI-native operating model with clear RACI matrices for human authority and agent delegation.',
        level: 'Optimized',
        recommendation:
          'Institutionalize university and talent pipelines to continuously train and certify sovereign AI workforce engineers.',
      },
    ],
  },
  {
    id: 'automation-potential',
    title: 'Automation & Agentic Potential',
    eyebrow: 'DOMAIN 05 / 05',
    icon: Zap,
    question:
      'Which best describes the current state of process automation and workflow orchestration in your key operating units?',
    description:
      'Evaluates current manual overhead, workflow collapsing opportunities, and multi-agent coordination potential.',
    options: [
      {
        label: 'Foundational — Manual Handoffs & Siloed Spreadsheets',
        description:
          'High volume of repetitive manual tasks in email, spreadsheets, and chat; workflows rely on individual memory and manual handoffs.',
        level: 'Foundational',
        recommendation:
          'Identify top 3 high-friction, repetitive workflows for initial Workflow Collapsing and agentic automation.',
      },
      {
        label: 'Developing — Linear Scripts & Basic RPA',
        description:
          'Linear RPA or rule-based scripts handle specific back-office tasks, but cross-departmental coordination remains manual.',
        level: 'Developing',
        recommendation:
          'Transition linear scripts into autonomous, role-scoped agent units governed by approval gates.',
      },
      {
        label: 'Advanced — Governed Departmental Agent Workflows',
        description:
          'Governed multi-step agentic workflows execute routine departmental processes with automated escalation for edge cases.',
        level: 'Advanced',
        recommendation:
          'Collapse multi-departmental approval chains into instant, orchestrated execution paths under executive oversight.',
      },
      {
        label: 'Optimized — Fully Orchestrated Multi-Agent Topology',
        description:
          'Fully orchestrated, context-aware agent topologies executing end-to-end business functions under continuous human oversight and real-time KPI tracking.',
        level: 'Optimized',
        recommendation:
          'Explore venture builder scaling and licensing options to deploy governed AI workforces as core business capabilities.',
      },
    ],
  },
];

export const LEVEL_BADGE_STYLES: Record<ReadinessLevel, { badge: string; text: string }> = {
  Foundational: {
    badge: 'bg-ls-navy/10 text-ls-navy dark:bg-ls-white/10 dark:text-ls-white',
    text: 'text-ls-navy dark:text-ls-white',
  },
  Developing: {
    badge: 'bg-ls-cyan/10 text-ls-cyan',
    text: 'text-ls-cyan',
  },
  Advanced: {
    badge: 'bg-ls-red/10 text-ls-red',
    text: 'text-ls-red',
  },
  Optimized: {
    badge: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400',
    text: 'text-emerald-600 dark:text-emerald-400',
  },
};

export const AssessmentWizard: React.FC<AssessmentWizardProps> = ({
  theme,
  onRequestBriefing,
}) => {
  const isLight = theme === 'light';
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, number>>({});
  const [isCompleted, setIsCompleted] = useState<boolean>(false);

  const activeDomain = DOMAINS[currentStep];
  const selectedOptionIndex = selectedAnswers[activeDomain?.id];

  const handleSelectOption = (index: number) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [activeDomain.id]: index,
    }));
  };

  const handleNext = () => {
    if (selectedOptionIndex === undefined) return;
    if (currentStep < DOMAINS.length - 1) {
      setCurrentStep((prev) => prev + 1);
    } else {
      setIsCompleted(true);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
    }
  };

  const handleReset = () => {
    setSelectedAnswers({});
    setCurrentStep(0);
    setIsCompleted(false);
  };

  // Compile summary text for the briefing modal
  const generateSummaryPayload = (): string => {
    const lines = DOMAINS.map((domain) => {
      const idx = selectedAnswers[domain.id];
      const opt = idx !== undefined ? domain.options[idx] : undefined;
      return `- ${domain.title}: ${opt?.level ?? 'Not Assessed'}`;
    });

    return `AI READINESS DIAGNOSTIC SUMMARY:\n${lines.join('\n')}\n\nRequesting confidential Executive Advisory Briefing to review detailed diagnostic results and explore targeted architecture options.`;
  };

  const handleRequestBriefing = () => {
    const payload = generateSummaryPayload();
    onRequestBriefing?.(payload);
  };

  const cardBgCls = isLight
    ? 'bg-ls-white/95 shadow-md'
    : 'bg-ls-navy/80 shadow-xl';

  return (
    <div className="w-full max-w-5xl mx-auto">
      {!isCompleted ? (
        /* WIZARD QUESTIONNAIRE VIEW */
        <Reveal key={`step-${currentStep}`}>
          <div className={`rounded-3xl p-6 sm:p-10 ${cardBgCls}`}>
            {/* Progress Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 mb-8">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-ls-red/10 flex items-center justify-center text-ls-red">
                  {React.createElement(activeDomain.icon, { className: 'w-5 h-5' })}
                </div>
                <div>
                  <span className="font-body text-[10px] font-bold tracking-widest text-ls-red uppercase block">
                    {activeDomain.eyebrow}
                  </span>
                  <h2 className={`font-display font-bold text-xl sm:text-2xl tracking-tight ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}>
                    {activeDomain.title}
                  </h2>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="flex items-center gap-3">
                <div className="w-32 sm:w-44 h-2 rounded-full bg-ls-grey-light dark:bg-ls-white/10 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-ls-cyan to-ls-red transition-all duration-300 rounded-full"
                    style={{ width: `${((currentStep + 1) / DOMAINS.length) * 100}%` }}
                  />
                </div>
                <span className={`text-xs font-bold font-body tracking-wider ${
                  isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
                }`}>
                  {currentStep + 1} / {DOMAINS.length}
                </span>
              </div>
            </div>

            {/* Question Title & Lead */}
            <div className="mb-8">
              <h3 className={`text-base sm:text-lg font-bold leading-snug mb-2 ${
                isLight ? 'text-ls-navy' : 'text-ls-white'
              }`}>
                {activeDomain.question}
              </h3>
              <p className={`text-xs sm:text-sm leading-relaxed ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                {activeDomain.description}
              </p>
            </div>

            {/* Options List */}
            <div className="space-y-3.5 mb-8">
              {activeDomain.options.map((option, idx) => {
                const isSelected = selectedOptionIndex === idx;
                const levelStyle = LEVEL_BADGE_STYLES[option.level];

                return (
                  <button
                    key={option.level}
                    type="button"
                    onClick={() => handleSelectOption(idx)}
                    className={`btn-milled w-full text-left p-4 sm:p-5 rounded-2xl transition-all duration-200 cursor-pointer flex items-start gap-4 group ${
                      isSelected
                        ? isLight
                          ? 'bg-ls-navy/10 shadow-[inset_0_1px_2px_rgba(255,255,255,0.9),0_6px_18px_rgba(230,57,70,0.25)]'
                          : 'bg-ls-white/20 shadow-[inset_0_1px_1.5px_rgba(255,255,255,0.3),0_6px_18px_rgba(230,57,70,0.35)]'
                        : isLight
                        ? 'bg-ls-white shadow-[inset_0_1px_1px_rgba(255,255,255,0.9),0_3px_10px_rgba(7,10,64,0.06)] hover:bg-ls-grey-light-text/30'
                        : 'bg-ls-navy/60 shadow-[inset_0_1px_1px_rgba(255,255,255,0.15),0_3px_10px_rgba(0,0,0,0.3)] hover:bg-ls-white/5'
                    }`}
                  >
                    <div className={`mt-0.5 w-5 h-5 rounded-full flex items-center justify-center shrink-0 transition-colors ${
                      isSelected
                        ? 'bg-ls-red text-ls-white shadow-[0_0_10px_rgba(230,57,70,0.5)]'
                        : isLight
                        ? 'bg-ls-grey-light-text/30'
                        : 'bg-ls-white/10'
                    }`}>
                      {isSelected && <CheckCircle2 className="w-3.5 h-3.5" />}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2 mb-1 flex-wrap">
                        <span className={`font-bold text-sm tracking-tight ${
                          isSelected
                            ? isLight ? 'text-ls-navy font-extrabold' : 'text-ls-white font-extrabold'
                            : isLight ? 'text-ls-navy' : 'text-ls-white'
                        }`}>
                          {option.label}
                        </span>
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wider uppercase ${levelStyle.badge}`}>
                          {option.level}
                        </span>
                      </div>
                      <p className={`text-xs leading-relaxed ${
                        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                      }`}>
                        {option.description}
                      </p>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Navigation Buttons */}
            <div className="flex items-center justify-between pt-6">
              <button
                type="button"
                onClick={handleBack}
                disabled={currentStep === 0}
                className={`btn-milled btn-milled-secondary px-5 py-2.5 rounded-full text-xs font-bold tracking-wider transition-all flex items-center gap-2 cursor-pointer ${
                  isLight
                    ? 'border border-ls-navy/25 text-ls-navy hover:bg-ls-navy/5'
                    : 'border border-ls-white/20 text-ls-white hover:bg-ls-white/5'
                } ${currentStep === 0 ? 'opacity-30 cursor-not-allowed' : ''}`}
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Back</span>
              </button>

              <button
                type="button"
                onClick={handleNext}
                disabled={selectedOptionIndex === undefined}
                className={`btn-milled btn-milled-primary bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 hover:bg-ls-red/90 px-7 py-3 rounded-full font-bold text-xs tracking-widest uppercase transition-all flex items-center gap-2.5 ${
                  selectedOptionIndex === undefined ? 'opacity-40 cursor-not-allowed' : ''
                }`}
              >
                <span>{currentStep === DOMAINS.length - 1 ? 'View Diagnostic Summary' : 'Next Domain'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </Reveal>
      ) : (
        /* DIAGNOSTIC SUMMARY VIEW */
        <Reveal>
          <div className="space-y-8">
            {/* Header Banner */}
            <div className={`rounded-3xl p-6 sm:p-10 ${cardBgCls}`}>
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 mb-6">
                <div>
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-ls-red/10 text-ls-red text-[11px] font-bold tracking-widest uppercase mb-3">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>DIAGNOSTIC READOUT COMPLETE</span>
                  </div>
                  <h2 className={`font-display font-bold text-2xl sm:text-3xl tracking-tight ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}>
                    Your AI Readiness Posture Summary
                  </h2>
                </div>

                <button
                  type="button"
                  onClick={handleReset}
                  className="btn-milled btn-milled-secondary border border-ls-navy/25 text-ls-navy hover:bg-ls-navy/5 dark:border-ls-white/20 dark:text-ls-white px-4 py-2 rounded-full text-xs font-bold tracking-wider transition-colors cursor-pointer inline-flex items-center gap-2"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Retake Assessment</span>
                </button>
              </div>

              {/* High-Level HAOMTGV Strategic Synthesis */}
              <div className="p-5 sm:p-6 rounded-2xl bg-ls-cyan/10 text-xs sm:text-sm leading-relaxed space-y-2">
                <span className="font-body text-[10px] font-bold tracking-widest text-ls-cyan uppercase block">
                  HAOMTGV STRATEGIC SYNTHESIS
                </span>
                <p className={`font-medium ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                  Your organization demonstrates a clear diagnostic posture across the 5 domains. Alignment with LightSpeed’s Human-led, Agentic Operating Model (HAOMTGV) highlights target opportunities to collapse operational latency and establish cryptographically governed agent workflows.
                </p>
              </div>
            </div>

            {/* Domain Readiness Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {DOMAINS.map((domain) => {
                const idx = selectedAnswers[domain.id];
                const option = idx !== undefined ? domain.options[idx] : domain.options[0];
                const levelStyle = LEVEL_BADGE_STYLES[option.level];

                return (
                  <div
                    key={domain.id}
                    className={`rounded-3xl p-6 flex flex-col justify-between gap-4 ${cardBgCls}`}
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-3">
                        <div className="flex items-center gap-2.5">
                          <div className="w-8 h-8 rounded-xl bg-ls-cyan/10 flex items-center justify-center text-ls-cyan">
                            {React.createElement(domain.icon, { className: 'w-4 h-4' })}
                          </div>
                          <h3 className={`font-display font-bold text-base tracking-tight ${
                            isLight ? 'text-ls-navy' : 'text-ls-white'
                          }`}>
                            {domain.title}
                          </h3>
                        </div>

                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wider uppercase shrink-0 ${levelStyle.badge}`}>
                          {option.level}
                        </span>
                      </div>

                      <p className={`text-xs leading-relaxed mb-4 ${
                        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                      }`}>
                        {option.description}
                      </p>
                    </div>

                    <div className="pt-3">
                      <span className="font-body text-[9px] font-bold tracking-widest text-ls-red uppercase block mb-1">
                        RECOMMENDED ACTION
                      </span>
                      <p className={`text-xs font-medium leading-relaxed ${
                        isLight ? 'text-ls-navy' : 'text-ls-white'
                      }`}>
                        {option.recommendation}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Disclaimer & Final Advisory CTA Box */}
            <div className={`rounded-3xl p-6 sm:p-8 space-y-6 ${cardBgCls}`}>
              {/* Strict Claims Disclaimer */}
              <div className="flex items-start gap-3 p-4 rounded-2xl bg-amber-500/10 text-amber-700 dark:text-amber-300 text-xs leading-relaxed">
                <Info className="w-4 h-4 shrink-0 mt-0.5 text-amber-600 dark:text-amber-400" />
                <p>
                  <strong>Disclaimer:</strong> This diagnostic summary provides a preliminary qualitative read of your organization’s readiness. It is a discovery tool and does not constitute a finalized architectural blueprint, guaranteed ROI, or production-ready deployment plan.
                </p>
              </div>

              {/* Advisory Briefing CTA */}
              <div className="flex flex-col sm:flex-row items-center justify-between gap-6 pt-2">
                <div className="space-y-1 text-center sm:text-left">
                  <h4 className={`font-display font-bold text-lg ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}>
                    Discuss Your Readout with Senior Partners
                  </h4>
                  <p className={`text-xs ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}>
                    Schedule a 2-week Advisory Architecture Sprint or Executive Briefing session.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={handleRequestBriefing}
                  className="btn-milled btn-milled-primary bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 hover:bg-ls-red/90 px-8 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase transition-all cursor-pointer shrink-0 flex items-center gap-2.5"
                >
                  <span>Request Executive Advisory Briefing</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </Reveal>
      )}
    </div>
  );
};

export default AssessmentWizard;
