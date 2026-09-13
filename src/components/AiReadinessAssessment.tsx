import React, { useState } from 'react';
import { 
  Sparkles, 
  CheckCircle2, 
  ArrowRight, 
  RotateCcw, 
  Brain, 
  ShieldCheck, 
  Database, 
  Workflow, 
  Users, 
  Compass,
  Download,
  Activity,
  Cpu
} from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille, 
  ChassisPanel 
} from './TactileHardwareElements';

interface AiReadinessAssessmentProps {
  onOpenContactModal: (intent?: string, summary?: string) => void;
  theme?: 'light' | 'dark';
}

export const AiReadinessAssessment: React.FC<AiReadinessAssessmentProps> = ({
  onOpenContactModal,
  theme = 'dark'
}) => {
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [answers, setAnswers] = useState<Record<string, number>>({
    strategy: 3,
    data: 2,
    technology: 3,
    people: 2,
    governance: 2,
    automation: 3
  });
  const [completed, setCompleted] = useState<boolean>(false);
  const isLight = theme === 'light';

  const questions = [
    {
      id: 'strategy',
      title: '01. AI & EXECUTIVE STRATEGY',
      question: 'Does your executive leadership have a documented, budget-allocated 12–36 month AI strategy?',
      options: [
        { label: 'No formal AI discussions or budget allocation.', score: 1 },
        { label: 'Ad-hoc exploration by individual teams without central oversight.', score: 2 },
        { label: 'Executive sponsorship with committed pilot project funding.', score: 4 },
        { label: 'Formal board-approved AI-native enterprise strategy and sovereign roadmap.', score: 5 }
      ]
    },
    {
      id: 'data',
      title: '02. DATA ARCHITECTURE & SEMANTIC READINESS',
      question: 'How structured and accessible is your enterprise data for real-time model retrieval (RAG)?',
      options: [
        { label: 'Siloed paper or unstructured files across legacy spreadsheets.', score: 1 },
        { label: 'Central SQL database, but fragmented schemas and no unified taxonomy.', score: 2 },
        { label: 'Cloud data warehouse with authenticated API access.', score: 4 },
        { label: 'Unified semantic fabric with real-time vector graphs and streaming feeds.', score: 5 }
      ]
    },
    {
      id: 'technology',
      title: '03. CLOUD & INFRASTRUCTURE INTEGRATION',
      question: 'Can your IT infrastructure support asynchronous sub-agent task queues and secure model proxies?',
      options: [
        { label: 'Legacy on-premise servers with restricted or zero API connectivity.', score: 1 },
        { label: 'Hybrid cloud infrastructure with manual deployment runs.', score: 2 },
        { label: 'Cloud-native microservices with containerized application stacks.', score: 4 },
        { label: 'Sovereign cloud with zero-trust API orchestration bus and hardware guards.', score: 5 }
      ]
    },
    {
      id: 'people',
      title: '04. WORKFORCE & OPERATING MODEL ALIGNMENT',
      question: 'How prepared is your workforce to operate alongside autonomous AI sub-agents?',
      options: [
        { label: 'Skeptical or untrained regarding AI operating tools.', score: 1 },
        { label: 'Using basic consumer chatbots (ChatGPT) in isolated personal contexts.', score: 2 },
        { label: 'Formal internal prompt engineering and tool delegation training underway.', score: 4 },
        { label: 'Human + AI hybrid workforce with defined sub-agent role permissions.', score: 5 }
      ]
    },
    {
      id: 'governance',
      title: '05. AI GOVERNANCE & RISK CONTROL',
      question: 'Do you have human-in-the-loop (HITL) permission tiers and audit logging for automated decisions?',
      options: [
        { label: 'No formal AI governance, telemetry, or risk policy in place.', score: 1 },
        { label: 'Basic access control rules and standard IT passwords.', score: 2 },
        { label: 'Draft AI usage guidelines without automated audit enforcement.', score: 3 },
        { label: 'Tiered permission gates (Tier 1 Auto → Tier 5 Executive) with 100% auditable evidence.', score: 5 }
      ]
    },
    {
      id: 'automation',
      title: '06. PROCESS REDESIGN & WORKFLOW COLLAPSE',
      question: 'Are your core operational workflows designed for multi-step automated execution?',
      options: [
        { label: '100% manual email, paper signatures, and physical routing chains.', score: 1 },
        { label: 'Basic email notifications and isolated point-to-point scripts.', score: 2 },
        { label: 'RPA software handling routine data entry tasks.', score: 3 },
        { label: 'Collapsed autonomous workflows with sub-minute execution SLAs.', score: 5 }
      ]
    }
  ];

  const handleSelectOption = (questionId: string, score: number) => {
    setAnswers(prev => ({ ...prev, [questionId]: score }));
    if (currentStep < questions.length - 1) {
      setCurrentStep(prev => prev + 1);
    } else {
      setCompleted(true);
    }
  };

  // Calculate scores (percentages out of max score 5 per dimension)
  const strategyPct = Math.round((answers.strategy / 5) * 100);
  const dataPct = Math.round((answers.data / 5) * 100);
  const techPct = Math.round((answers.technology / 5) * 100);
  const peoplePct = Math.round((answers.people / 5) * 100);
  const govPct = Math.round((answers.governance / 5) * 100);
  const autoPct = Math.round((answers.automation / 5) * 100);

  const overallScore = Math.round((strategyPct + dataPct + techPct + peoplePct + govPct + autoPct) / 6);

  const summaryString = `AI Readiness Score: ${overallScore}/100 (Strategy: ${strategyPct}%, Data: ${dataPct}%, Tech: ${techPct}%, People: ${peoplePct}%, Governance: ${govPct}%, Automation: ${autoPct}%)`;

  return (
    <section id="resources" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto font-sans">
      
      {/* Title & Classification */}
      <div className="text-center max-w-3xl mx-auto mb-14">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider mb-4 border select-none">
          <StatusLedPip status="emerald" isLight={isLight} />
          <span className={`text-[10px] font-mono tracking-widest ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
            DIAGNOSTIC INSTRUMENT // READINESS AUDIT CALIBRATOR
          </span>
        </div>
        <h2 className={`text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-display mb-4 leading-normal sm:leading-tight break-words ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          Is Your Organisation <span className="inline-block pb-1.5 pr-1 text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">AI-Ready?</span>
        </h2>
        <p className={`text-base leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
          Evaluate your enterprise across 6 strategic telemetry dimensions in 2 minutes to calibrate your custom AI Readiness Score and deployment roadmap.
        </p>
      </div>

      {/* Strategic Readiness & Diagnostic Infographic Radar Display */}
      <div className={`max-w-3xl mx-auto relative rounded-3xl overflow-hidden mb-10 border shadow-2xl p-6 sm:p-8 ${
        isLight ? 'bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 border-slate-300 text-white' : 'bg-gradient-to-br from-[#0c0f1d] via-[#060810] to-[#04060a] border-amber-500/30 text-white'
      }`}>
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <StatusLedPip status="emerald" isLight={false} />
              <span className="text-[10px] font-mono text-amber-400 font-bold uppercase tracking-widest">[ DIAGNOSTIC RADAR // SIX-AXIS ASSESSMENT ]</span>
            </div>
            <h3 className="text-lg sm:text-xl font-bold font-display text-white">Institutional AI Telemetry Radar</h3>
            <p className="text-xs text-zinc-400 font-mono mt-0.5">Real-time evaluation across SADC regional compliance, sovereign compute, and 5-tier gates.</p>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-mono">
            <Activity className="w-3.5 h-3.5" />
            <span>CALIBRATION ACTIVE</span>
          </div>
        </div>

        {/* Six Strategic Axes Visualizer */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {[
            { dim: '01. STRATEGY', metric: 'Sovereign Alignment', status: 'AUDIT READY' },
            { dim: '02. DATA FABRIC', metric: 'Air-Gapped SADC Residency', status: 'IN-COUNTRY' },
            { dim: '03. COMPUTE', metric: 'Tier-III On-Prem Racks', status: 'SOVEREIGN' },
            { dim: '04. WORKFORCE', metric: 'Human-in-the-Loop Guilds', status: 'TRAINED' },
            { dim: '05. GOVERNANCE', metric: '5-Tier HITL Gates', status: 'ACTIVE' },
            { dim: '06. AGENT SWARM', metric: '144 Canonical Tools', status: 'SANDBOXED' }
          ].map((item, idx) => (
            <div key={idx} className="p-3 rounded-xl bg-black/40 border border-white/10 flex flex-col justify-between">
              <span className="text-[9px] font-mono font-bold text-amber-400">{item.dim}</span>
              <span className="text-xs font-mono text-zinc-200 mt-1 font-semibold">{item.metric}</span>
              <span className="text-[9px] font-mono text-emerald-400 mt-1.5 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                {item.status}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Main Diagnostic Chassis */}
      <div className={`max-w-3xl mx-auto p-6 sm:p-9 rounded-3xl border shadow-2xl relative overflow-hidden transition-all ${
        isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />
        
        {!completed ? (
          <div>
            {/* Step header telemetry */}
            <div className={`flex items-center justify-between text-xs font-mono mb-6 pb-4 border-b ${
              isLight ? 'text-slate-500 border-slate-300' : 'text-zinc-400 border-zinc-800'
            }`}>
              <div className="flex items-center gap-2">
                <StatusLedPip status="amber" isLight={isLight} />
                <span className="text-amber-500 font-extrabold">STAGE {currentStep + 1} OF {questions.length}</span>
              </div>
              <span className="font-bold tracking-wider">{questions[currentStep].title}</span>
            </div>

            {/* Question */}
            <h3 className={`text-xl font-bold font-display mb-6 ${
              isLight ? 'text-slate-900' : 'text-zinc-100'
            }`}>
              {questions[currentStep].question}
            </h3>

            {/* Options */}
            <div className="space-y-3 mb-8">
              {questions[currentStep].options.map((opt, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSelectOption(questions[currentStep].id, opt.score)}
                  className={`w-full p-4 rounded-2xl text-left text-xs font-medium border transition-all flex items-center justify-between group relative overflow-hidden ${
                    isLight 
                      ? 'flight-deck-well-light text-slate-800 hover:border-amber-500 hover:bg-amber-50' 
                      : 'flight-deck-well-dark text-zinc-200 hover:border-amber-500/60 hover:bg-zinc-900'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-lg bg-amber-500/10 text-amber-500 font-mono font-bold flex items-center justify-center text-[10px] shrink-0 border border-amber-500/20">
                      0{idx + 1}
                    </span>
                    <span className="font-mono">{opt.label}</span>
                  </div>
                  <ArrowRight className={`w-4 h-4 transition-all group-hover:translate-x-1 shrink-0 ${
                    isLight ? 'text-slate-400 group-hover:text-amber-600' : 'text-zinc-500 group-hover:text-amber-400'
                  }`} />
                </button>
              ))}
            </div>

            {/* Back button */}
            {currentStep > 0 && (
              <button
                onClick={() => setCurrentStep(prev => prev - 1)}
                className={`text-xs font-mono uppercase font-bold tracking-wider ${
                  isLight ? 'text-slate-500 hover:text-slate-900' : 'text-zinc-400 hover:text-zinc-100'
                }`}
              >
                ← REVERT TO PREVIOUS STAGE
              </button>
            )}
          </div>
        ) : (
          <div className="space-y-8 animate-in fade-in duration-300">
            
            {/* Score Chassis Banner */}
            <div className={`text-center p-6 rounded-2xl border relative overflow-hidden ${
              isLight 
                ? 'flight-deck-well-light border-amber-400' 
                : 'flight-deck-well-dark border-amber-500/40 bg-zinc-950'
            }`}>
              <div className="flex items-center justify-center gap-2 mb-1">
                <StatusLedPip status="emerald" isLight={isLight} />
                <span className={`text-xs font-mono uppercase font-bold tracking-widest ${
                  isLight ? 'text-amber-700' : 'text-amber-400'
                }`}>
                  CALIBRATED AI READINESS METRIC
                </span>
              </div>
              <div className="text-5xl font-extrabold font-mono text-amber-500 my-2">
                {overallScore} <span className={`text-xl ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>/ 100</span>
              </div>
              <p className={`text-xs max-w-md mx-auto leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                {overallScore >= 70 
                  ? 'High Readiness: Your organization is prime for immediate AI Company Builder deployment.'
                  : overallScore >= 40
                  ? 'Moderate Readiness: Solid foundational elements, but key data and governance gaps need structuring.'
                  : 'Early Readiness: Urgent priority to modernize strategy and data architecture before agentic scaling.'}
              </p>
            </div>

            {/* Breakdown Bars with Hardware Pips */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              
              <div className={`p-4 rounded-2xl border ${isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'}`}>
                <div className="flex items-center justify-between text-xs mb-1.5 font-mono">
                  <div className="flex items-center gap-2">
                    <StatusLedPip status="emerald" isLight={isLight} />
                    <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>Executive Strategy</span>
                  </div>
                  <span className="font-bold text-amber-500">{strategyPct}%</span>
                </div>
                <div className={`w-full h-2 rounded-full overflow-hidden ${isLight ? 'bg-slate-300' : 'bg-zinc-800'}`}>
                  <div className="h-full bg-amber-500 rounded-full" style={{ width: `${strategyPct}%` }}></div>
                </div>
              </div>

              <div className={`p-4 rounded-2xl border ${isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'}`}>
                <div className="flex items-center justify-between text-xs mb-1.5 font-mono">
                  <div className="flex items-center gap-2">
                    <StatusLedPip status="emerald" isLight={isLight} />
                    <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>Data Architecture</span>
                  </div>
                  <span className="font-bold text-amber-500">{dataPct}%</span>
                </div>
                <div className={`w-full h-2 rounded-full overflow-hidden ${isLight ? 'bg-slate-300' : 'bg-zinc-800'}`}>
                  <div className="h-full bg-amber-500 rounded-full" style={{ width: `${dataPct}%` }}></div>
                </div>
              </div>

              <div className={`p-4 rounded-2xl border ${isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'}`}>
                <div className="flex items-center justify-between text-xs mb-1.5 font-mono">
                  <div className="flex items-center gap-2">
                    <StatusLedPip status="emerald" isLight={isLight} />
                    <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>Technology & Cloud</span>
                  </div>
                  <span className="font-bold text-amber-500">{techPct}%</span>
                </div>
                <div className={`w-full h-2 rounded-full overflow-hidden ${isLight ? 'bg-slate-300' : 'bg-zinc-800'}`}>
                  <div className="h-full bg-amber-500 rounded-full" style={{ width: `${techPct}%` }}></div>
                </div>
              </div>

              <div className={`p-4 rounded-2xl border ${isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'}`}>
                <div className="flex items-center justify-between text-xs mb-1.5 font-mono">
                  <div className="flex items-center gap-2">
                    <StatusLedPip status="emerald" isLight={isLight} />
                    <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>People & Culture</span>
                  </div>
                  <span className="font-bold text-amber-500">{peoplePct}%</span>
                </div>
                <div className={`w-full h-2 rounded-full overflow-hidden ${isLight ? 'bg-slate-300' : 'bg-zinc-800'}`}>
                  <div className="h-full bg-amber-500 rounded-full" style={{ width: `${peoplePct}%` }}></div>
                </div>
              </div>

              <div className={`p-4 rounded-2xl border ${isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'}`}>
                <div className="flex items-center justify-between text-xs mb-1.5 font-mono">
                  <div className="flex items-center gap-2">
                    <StatusLedPip status="emerald" isLight={isLight} />
                    <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>Governance & Risk</span>
                  </div>
                  <span className="font-bold text-amber-500">{govPct}%</span>
                </div>
                <div className={`w-full h-2 rounded-full overflow-hidden ${isLight ? 'bg-slate-300' : 'bg-zinc-800'}`}>
                  <div className="h-full bg-amber-500 rounded-full" style={{ width: `${govPct}%` }}></div>
                </div>
              </div>

              <div className={`p-4 rounded-2xl border ${isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'}`}>
                <div className="flex items-center justify-between text-xs mb-1.5 font-mono">
                  <div className="flex items-center gap-2">
                    <StatusLedPip status="emerald" isLight={isLight} />
                    <span className={isLight ? 'text-slate-700' : 'text-zinc-300'}>Workflow Collapse</span>
                  </div>
                  <span className="font-bold text-amber-500">{autoPct}%</span>
                </div>
                <div className={`w-full h-2 rounded-full overflow-hidden ${isLight ? 'bg-slate-300' : 'bg-zinc-800'}`}>
                  <div className="h-full bg-amber-500 rounded-full" style={{ width: `${autoPct}%` }}></div>
                </div>
              </div>

            </div>

            {/* Actions */}
            <div className={`pt-4 border-t flex flex-col sm:flex-row items-center justify-between gap-4 ${
              isLight ? 'border-slate-300' : 'border-zinc-800'
            }`}>
              <button
                onClick={() => {
                  setCompleted(false);
                  setCurrentStep(0);
                }}
                className={`flex items-center gap-2 text-xs font-mono uppercase font-bold tracking-wider ${
                  isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white'
                }`}
              >
                <RotateCcw className="w-4 h-4" />
                <span>Re-Calibrate Assessment</span>
              </button>

              <button
                onClick={() => onOpenContactModal('Request an AI Assessment', summaryString)}
                className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 active:scale-95"
              >
                <span>Engage Strategic Architecture Team</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>

          </div>
        )}

      </div>

    </section>
  );
};
