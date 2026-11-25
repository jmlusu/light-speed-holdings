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
    question: 'How would you describe your current data architecture and governance?',
    description:
      'Evaluates data structure, access, governance, and readiness for agent-supported workflows.',
    options: [
      {
        label: 'Fragmented / Silos (Foundational)',
        description:
          'Data sits in spreadsheets, local drives, and disconnected SaaS tools without a common schema.',
        level: 'Foundational',
        recommendation:
          'Unify your data and establish a central knowledge base that can support vector search.',
      },
      {
        label: 'Centralized but Static (Developing)',
        description:
          'You have a data warehouse or central ERP, but access is manual and governance is inconsistent.',
        level: 'Developing',
        recommendation:
          'Define data governance policies and API access for future agent use.',
      },
      {
        label: 'Governed & Accessible (Advanced)',
        description:
          'Structured data is accessible through APIs under defined access controls and compliance policies.',
        level: 'Advanced',
        recommendation:
          'Prepare for agent grounding by mapping domain-specific knowledge graphs.',
      },
      {
        label: 'Sovereign & Agent-Ready (Optimized)',
        description:
          'Real-time governed pipelines include residency controls, audit records, and semantic indexing.',
        level: 'Optimized',
        recommendation:
          'Deploy retrieval-augmented generation (RAG) and multi-agent memory systems.',
      },
    ],
  },
  {
    id: 'infrastructure-integration',
    title: 'Core Infrastructure & Integration',
    eyebrow: 'DOMAIN 02 / 05',
    icon: Cpu,
    question: 'What is the state of your technology stack and API readiness?',
    description: 'Evaluates integration readiness, system architecture, and deployment constraints.',
    options: [
      {
        label: 'Legacy / Manual (Foundational)',
        description:
          'Core systems run on-premises, lack modern APIs, and depend on manual data entry.',
        level: 'Foundational',
        recommendation: 'Add an API gateway layer around legacy systems.',
      },
      {
        label: 'Cloud-Hybrid / Partial APIs (Developing)',
        description:
          'You mix cloud and legacy systems. Some APIs exist, but integration needs custom middleware.',
        level: 'Developing',
        recommendation:
          'Standardize integration patterns and use an enterprise service bus or iPaaS.',
      },
      {
        label: 'API-First / Cloud-Native (Advanced)',
        description: 'You use microservices, documented APIs, and CI/CD pipelines.',
        level: 'Advanced',
        recommendation: 'Add agent tool interfaces to existing API endpoints.',
      },
      {
        label: 'Event-Driven / Composable (Optimized)',
        description: 'Your architecture supports real-time, event-driven agent orchestration.',
        level: 'Optimized',
        recommendation:
          'Implement coordinated agent teams using Model Context Protocol (MCP) toolsets.',
      },
    ],
  },
  {
    id: 'governance-haomtgv',
    title: 'Governance, Risk & Compliance',
    eyebrow: 'DOMAIN 03 / 05',
    icon: ShieldCheck,
    question: 'How prepared is your organisation to govern autonomous AI systems?',
    description: 'Evaluates policy, oversight, risk controls, and audit readiness.',
    options: [
      {
        label: 'Unregulated / Ad-hoc (Foundational)',
        description:
          'You have no formal AI policy. Staff use public AI tools without data controls.',
        level: 'Foundational',
        recommendation:
          'Establish an AI acceptable-use policy and data loss prevention (DLP) controls now.',
      },
      {
        label: 'Exploratory Guidelines (Developing)',
        description:
          'Basic IT policies exist, but you have no framework for agent autonomy or human review.',
        level: 'Developing',
        recommendation:
          'Form an AI steering committee and define risk tiers for automated decisions.',
      },
      {
        label: 'Structured AI Policy (Advanced)',
        description:
          'You have a formal AI governance framework with GDPR or local data-protection compliance mapping.',
        level: 'Advanced',
        recommendation:
          'Enforce policies through technical guardrails and automated audit logging.',
      },
      {
        label: 'Continuous Audit / Cryptographic (Optimized)',
        description:
          'You use real-time compliance monitoring, cryptographic audit records, and tiered human approval.',
        level: 'Optimized',
        recommendation:
          "Scale deployment with LightSpeed's HAOMTGV five-tier approval matrix.",
      },
    ],
  },
  {
    id: 'talent-change',
    title: 'Talent, Culture & Leadership',
    eyebrow: 'DOMAIN 04 / 05',
    icon: Users,
    question: 'How ready is your organisation for AI-native workflows?',
    description: 'Evaluates leadership alignment, skills, and operating culture.',
    options: [
      {
        label: 'Skeptical / Unaware (Foundational)',
        description:
          'Leadership sees AI as hype or a threat. Staff lack basic AI literacy.',
        level: 'Foundational',
        recommendation:
          'Run executive briefings and baseline AI literacy training for all staff.',
      },
      {
        label: 'Experimenting / Pockets (Developing)',
        description:
          'Separate teams use AI tools without a central strategy or training programme.',
        level: 'Developing',
        recommendation:
          'Build an enterprise AI training plan and identify internal AI champions.',
      },
      {
        label: 'Strategic Alignment (Advanced)',
        description:
          'You have executive sponsorship, a dedicated budget, and teams working across departments.',
        level: 'Advanced',
        recommendation:
          'Move from isolated use cases to an AI-native operating model.',
      },
      {
        label: 'AI-Native Culture (Optimized)',
        description: 'AI forms part of core KPIs. Staff know how to work with agent systems.',
        level: 'Optimized',
        recommendation:
          'Improve human-agent working protocols and continue refining system performance.',
      },
    ],
  },
  {
    id: 'automation-potential',
    title: 'Agentic Workflow Potential',
    eyebrow: 'DOMAIN 05 / 05',
    icon: Zap,
    question: 'Where does your organisation stand on autonomous agent workflows?',
    description: 'Evaluates automation maturity and potential for governed agent workflows.',
    options: [
      {
        label: 'No Automation (Foundational)',
        description: 'People route work and make every decision manually.',
        level: 'Foundational',
        recommendation:
          'Identify high-volume, low-complexity tasks for basic RPA or scripts.',
      },
      {
        label: 'Rule-Based Automation (Developing)',
        description:
          'You use RPA or rigid if/then workflows without generative capabilities.',
        level: 'Developing',
        recommendation:
          'Add language-model routing and document understanding to rigid workflows.',
      },
      {
        label: 'Cognitive Assistants (Advanced)',
        description:
          'Copilots and chatbots assist people, but people still perform every action.',
        level: 'Advanced',
        recommendation:
          'Pilot bounded workflows where agents execute actions under human review.',
      },
      {
        label: 'Multi-Agent Orchestration (Optimized)',
        description:
          'You are ready to deploy, or already use, agents that plan, execute, and coordinate work.',
        level: 'Optimized',
        recommendation:
          'Implement the full HAOMTGV architecture for enterprise orchestration.',
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
    badge: 'bg-ls-cyan/10 text-ls-cyan-ink dark:text-ls-cyan',
    text: 'text-ls-cyan-ink dark:text-ls-cyan',
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
              <div className="flex flex-col items-end gap-1.5">
                <span className={`text-[10px] font-bold font-body tracking-widest uppercase ${
                  isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
                }`}>
                  DOMAIN {currentStep + 1} OF {DOMAINS.length}
                </span>
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
                    OVERALL READINESS
                  </span>
                </div>
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
                        ? 'bg-ls-white shadow-[inset_0_1px_1px_rgba(255,255,255,0.9),0_3px_10px_rgba(7,10,64,0.06)] hover:bg-ls-grey-light/50'
                        : 'bg-ls-navy/60 shadow-[inset_0_1px_1px_rgba(255,255,255,0.15),0_3px_10px_rgba(0,0,0,0.3)] hover:bg-ls-white/5'
                    }`}
                  >
                    <div className={`mt-0.5 w-5 h-5 rounded-full flex items-center justify-center shrink-0 transition-colors ${
                      isSelected
                        ? 'bg-ls-red text-ls-white shadow-[0_0_10px_rgba(230,57,70,0.5)]'
                        : isLight
                        ? 'bg-ls-grey-light/50'
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
                  currentStep === 0 ? 'opacity-30 cursor-not-allowed' : ''
                }`}
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Previous Domain</span>
              </button>

              <button
                type="button"
                onClick={handleNext}
                disabled={selectedOptionIndex === undefined}
                className={`btn-milled btn-milled-primary px-7 py-3 rounded-full font-bold text-xs tracking-widest uppercase transition-all flex items-center gap-2.5 ${
                  selectedOptionIndex === undefined ? 'opacity-40 cursor-not-allowed' : ''
                }`}
              >
                <span>{currentStep === DOMAINS.length - 1 ? 'Analyze Readiness Profile' : 'Next Domain'}</span>
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
                    <span>DIAGNOSTIC COMPLETE</span>
                  </div>
                  <h2 className={`font-display font-bold text-2xl sm:text-3xl tracking-tight ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}>
                    Organizational Readiness Profile
                  </h2>
                </div>

                <button
                  type="button"
                  onClick={handleReset}
                  className="btn-milled btn-milled-secondary px-4 py-2 rounded-full text-xs font-bold tracking-wider transition-colors cursor-pointer inline-flex items-center gap-2"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Retake Assessment</span>
                </button>
              </div>

              <p className={`text-sm sm:text-base leading-relaxed ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                Your answers show a readiness profile across five domains. Compare the results with HAOMTGV to identify where you can reduce operational delays and introduce governed agent workflows.
              </p>
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
                  <strong>Disclaimer:</strong> This diagnostic gives a preliminary qualitative view of your organisation’s readiness. Use it for discovery. It is not a final architecture, a guaranteed ROI, or a production deployment plan.
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
                    Schedule a two-week Advisory Architecture Sprint or an Executive Briefing session.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={handleRequestBriefing}
                  className="btn-milled btn-milled-primary px-8 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase transition-all cursor-pointer shrink-0 flex items-center gap-2.5"
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
