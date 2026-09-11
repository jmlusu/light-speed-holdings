import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  FileText, 
  ShieldCheck, 
  Landmark, 
  CheckCircle2, 
  Scale, 
  AlertTriangle, 
  Download, 
  ArrowRight, 
  Globe2, 
  Cpu, 
  Lock, 
  Key, 
  FileCheck, 
  Sparkles, 
  Building2, 
  Copy, 
  Check, 
  Send, 
  ExternalLink,
  BookOpen
} from 'lucide-react';
import { AcousticVentGrille } from './TactileHardwareElements';

interface NationalAiStrategySubmissionProps {
  theme?: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const NationalAiStrategySubmission: React.FC<NationalAiStrategySubmissionProps> = ({
  theme = 'dark',
  onRequestBriefing
}) => {
  const isLight = theme === 'light';

  const [activeTab, setActiveTab] = useState<'overview' | 'tiered-governance' | 'identity-audit' | 'sovereignty' | 'partnership' | 'full-draft'>('overview');
  const [activeTier, setActiveTier] = useState<number>(3);
  const [copiedState, setCopiedState] = useState<boolean>(false);
  const [downloadedState, setDownloadedState] = useState<boolean>(false);

  const tiers = [
    {
      tier: 1,
      risk: 'Advisory',
      example: 'Content aggregation, policy drafting, research summarization',
      control: 'Human output confirmation required prior to publication or dissemination.',
      badgeColor: 'border-blue-500/30 text-blue-400 bg-blue-500/10',
      technicalNote: 'Zero autonomous side-effects. Read-only context window.'
    },
    {
      tier: 2,
      risk: 'Automated workflow',
      example: 'Routine database updates, catalog sync, internal logistics alerts',
      control: 'Real-time telemetry logging with automated rate limiters.',
      badgeColor: 'border-emerald-500/30 text-emerald-400 bg-emerald-500/10',
      technicalNote: 'Bounded API scopes with deterministic token budgets.'
    },
    {
      tier: 3,
      risk: 'Direct execution',
      example: 'Financial disbursements, health records modification, statutory filings',
      control: 'Mandatory Human-in-the-Loop (HITL) cryptographic authorization checkpoints.',
      badgeColor: 'border-orange-500/30 text-orange-400 bg-orange-500/10',
      technicalNote: 'Dual-key PKI signatures & tamper-evident audit logs.'
    },
    {
      tier: 4,
      risk: 'Critical infrastructure',
      example: 'National grid management, telecom switching, water distribution',
      control: 'Decision-support only; autonomous execution strictly prohibited.',
      badgeColor: 'border-red-500/30 text-red-400 bg-red-500/10',
      technicalNote: 'Air-gapped operational technology boundaries.'
    }
  ];

  const fullDraftText = `NATIONAL AI STRATEGY & DIGITAL TRANSFORMATION COMMENTS
Formal Stakeholder Submission Draft
Channel: Department of E-Government / UNDP Inclusive Digital Transformation Project
Submitter: Jack Mlusu, Founder & CEO, LightSpeed Holdings (Pharos Policy Track)
Status: DRAFT for validation against live consultation format before filing

EXECUTIVE SUMMARY
Malawi has a once-in-a-generation opportunity to make its National AI Strategy a practical, implementation-ready instrument — not another aspirational document. This submission addresses a gap current drafts do not yet cover: agentic AI. Generative AI policies govern content; agentic AI (autonomous, tool-using, executing systems) governs actions. Malawi's strategy should anticipate this wave now, while frameworks are still being written.

THREE RECOMMENDATIONS:

1. Adopt a Tiered, Human-in-the-Loop Governance Model
Classify agentic uses by risk and require explicit human authorization for irreversible or high-risk actions:
- Tier 1 (Advisory): content aggregation, drafting -> human output confirmation
- Tier 2 (Automated workflow): routine DB updates, internal logistics -> real-time logging
- Tier 3 (Direct execution): financial disbursements, health records -> mandatory HITL checkpoints
- Tier 4 (Critical infrastructure): grid/telecom/water -> decision-support only, no autonomy
Why: Malawi's Data Protection Act (2024) is in force but not AI-specific. A tiered model gives regulators and the private sector a clear, resource-appropriate baseline for autonomous systems.

2. Require Machine-Readable Identity and Audit Trails for Agents
Mandate that deployed commercial agents carry a cryptographic credential bound to a registered legal entity, and that High/Critical-tier systems write to tamper-evident, append-only audit logs.
Why: Traceability is the foundation of accountability and the precondition for public trust. LightSpeed Holdings already operates this pattern in production (5-tier approvals, audit trails, RACI matrices) and can share it as a template.

3. Anchor Data Sovereignty and Localized Capability
Prioritize in-country processing for state, health, and primary financial data; encourage open-weight, locally hosted models and air-gapped inference for low-connectivity resilience; and invest in local skills (multi-agent orchestration, governance, local-language alignment — Chichewa, English).

OFFERED AS A CONTINUING PARTNER:
LightSpeed Holdings is prepared to:
- Contribute governance controls running in production as a national reference template;
- Pilot a high-visibility lighthouse use case (e.g. citizen-inquiry or legislative-summary agent) with a non-commercial partner;
- Support capacity building — training, certification, university partnerships — to build a sovereign agentic-AI talent pipeline.

CONCLUSION
The window is open now. Malawi can lead SADC not by consuming AI but by defining how a resource-constrained economy builds and governs AI-native institutions. We ask that agentic-AI governance be included in the final Strategy, and we stand ready to help make it operational.`;

  const handleCopyText = () => {
    navigator.clipboard.writeText(fullDraftText);
    setCopiedState(true);
    setTimeout(() => setCopiedState(false), 3000);
  };

  const handleDownloadDraft = () => {
    const blob = new Blob([fullDraftText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Malawi_National_AI_Strategy_Submission_Jack_Mlusu_LightSpeed.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setDownloadedState(true);
    setTimeout(() => setDownloadedState(false), 3000);
  };

  return (
    <section id="national-ai-strategy-comments" className={`py-20 px-4 sm:px-8 max-w-7xl mx-auto w-full relative z-10 border-t ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      {/* Header Badge & Title */}
      <div className="space-y-4 mb-10 text-left">
        <div className="flex flex-wrap items-center gap-3">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-400 font-mono text-[11px] font-bold tracking-widest shadow-xs">
            <Landmark className="w-3.5 h-3.5 text-orange-500" />
            <span>NATIONAL AI STRATEGY &amp; DIGITAL TRANSFORMATION</span>
          </div>

          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 font-mono text-[10px] font-bold tracking-widest">
            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
            <span>DEPARTMENT OF E-GOVERNMENT // UNDP CONSULTATION DRAFT</span>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
          <div className="space-y-2 max-w-3xl">
            <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display leading-tight ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              Formal Stakeholder Submission: <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 via-amber-500 to-amber-300">
                Governing Action, Not Just Content
              </span>
            </h2>
            <p className={`text-justify text-sm sm:text-base font-medium leading-relaxed ${
              isLight ? 'text-slate-700' : 'text-zinc-300'
            }`}>
              Authored by <strong className="text-orange-500">Jack Mlusu</strong> (Founder &amp; CEO, LightSpeed Holdings) under the Pharos policy track for the Malawi Department of E-Government &amp; UNDP Inclusive Digital Transformation project.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <button
              onClick={handleDownloadDraft}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-mono font-bold bg-orange-500/15 text-orange-400 hover:bg-orange-500 hover:text-white transition-all cursor-pointer border border-orange-500/30"
            >
              {downloadedState ? <Check className="w-4 h-4 text-emerald-400" /> : <Download className="w-4 h-4" />}
              <span>{downloadedState ? 'Draft Exported' : 'Export Submission Draft'}</span>
            </button>

            <button
              onClick={() => onRequestBriefing?.('National AI Strategy Stakeholder Submission Briefing')}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-mono font-bold bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-lg shadow-orange-500/20 transition-all cursor-pointer"
            >
              <span>Consult Policy Lead</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className={`p-1.5 rounded-2xl border flex flex-wrap gap-1.5 mb-8 ${
        isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900/90 border-zinc-800'
      }`}>
        {[
          { id: 'overview', label: '01. Executive Summary', icon: FileText },
          { id: 'tiered-governance', label: '02. Tiered HITL Model', icon: Scale },
          { id: 'identity-audit', label: '03. Identity & Audit Trails', icon: Key },
          { id: 'sovereignty', label: '04. Data Sovereignty', icon: Globe2 },
          { id: 'partnership', label: '05. Partner Offerings', icon: Building2 },
          { id: 'full-draft', label: '06. Complete Draft Text', icon: BookOpen }
        ].map((tab) => {
          const IconComponent = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                isActive 
                  ? 'bg-orange-500 text-white shadow-md' 
                  : isLight 
                    ? 'text-slate-700 hover:bg-white/80' 
                    : 'text-zinc-400 hover:text-white hover:bg-white/5'
              }`}
            >
              <IconComponent className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab Panels */}
      <AnimatePresence mode="wait">
        {/* TAB 1: EXECUTIVE SUMMARY */}
        {activeTab === 'overview' && (
          <motion.div
            key="overview"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className="space-y-8"
          >
            <div className={`p-6 sm:p-8 rounded-3xl border relative overflow-hidden ${
              isLight ? 'bg-white border-slate-300 shadow-lg' : 'bg-zinc-950 border-white/15 shadow-2xl'
            }`}>
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                <div className="lg:col-span-7 space-y-4">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-orange-500 animate-pulse" />
                    <span className="font-mono text-xs text-orange-500 font-bold uppercase tracking-wider">
                      THE CORE POLICY GAP: GOVERNING ACTIONS VS. CONTENT
                    </span>
                  </div>

                  <h3 className={`text-2xl sm:text-3xl font-black font-display leading-tight ${
                    isLight ? 'text-slate-900' : 'text-white'
                  }`}>
                    Generative AI governs content; <br />
                    <span className="text-orange-500">Agentic AI governs actions.</span>
                  </h3>

                  <p className={`text-justify text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                    Malawi has a once-in-a-generation opportunity to make its National AI Strategy a practical, implementation-ready instrument — not another aspirational document. Most global policy drafts focus on Generative AI (LLM output, hallucinations, copyright). However, the upcoming wave is <strong>Agentic AI</strong>: autonomous systems equipped with computational tools that interact directly with databases, execute financial disbursements, and modify public records.
                  </p>

                  <p className={`text-justify text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                    Malawi's strategy must anticipate this shift now while regulatory frameworks are actively being written across SADC.
                  </p>
                </div>

                <div className="lg:col-span-5">
                  <div className={`p-5 rounded-2xl border space-y-4 ${
                    isLight ? 'bg-orange-50/50 border-orange-200' : 'bg-orange-950/20 border-orange-500/30'
                  }`}>
                    <div className="flex items-center gap-2 text-orange-400 font-mono text-xs font-bold">
                      <Sparkles className="w-4 h-4" />
                      <span>THE THREE POLICY PILLARS</span>
                    </div>

                    <div className="space-y-3 font-mono text-xs">
                      <div className="p-3 rounded-xl bg-black/20 border border-orange-500/20 flex items-start gap-2.5">
                        <span className="font-bold text-orange-400">01</span>
                        <div>
                          <strong className="block text-white">Tiered HITL Governance</strong>
                          <span className="text-zinc-400 text-[11px]">Classify agent actions by risk; mandate human sign-off for Tier 3/4.</span>
                        </div>
                      </div>

                      <div className="p-3 rounded-xl bg-black/20 border border-orange-500/20 flex items-start gap-2.5">
                        <span className="font-bold text-orange-400">02</span>
                        <div>
                          <strong className="block text-white">Cryptographic Machine Identity</strong>
                          <span className="text-zinc-400 text-[11px]">Bind agents to legal entities with tamper-evident audit logs.</span>
                        </div>
                      </div>

                      <div className="p-3 rounded-xl bg-black/20 border border-orange-500/20 flex items-start gap-2.5">
                        <span className="font-bold text-orange-400">03</span>
                        <div>
                          <strong className="block text-white">Data Sovereignty &amp; Local Skills</strong>
                          <span className="text-zinc-400 text-[11px]">On-soil compute for state data &amp; Chichewa/English NLU alignment.</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* TAB 2: TIERED GOVERNANCE MODEL */}
        {activeTab === 'tiered-governance' && (
          <motion.div
            key="tiered-governance"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className="space-y-6"
          >
            <div className={`p-6 rounded-3xl border ${isLight ? 'bg-white border-slate-300' : 'bg-zinc-950 border-white/15'}`}>
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                <div>
                  <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                    Recommendation 1: Tiered, Human-in-the-Loop (HITL) Model
                  </h3>
                  <p className={`text-xs mt-1 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                    Provides a resource-appropriate baseline for autonomous systems aligned with Malawi's Data Protection Act (2024).
                  </p>
                </div>

                <div className="flex items-center gap-2 font-mono text-xs">
                  <span className="text-zinc-400">Select Tier:</span>
                  {tiers.map((t) => (
                    <button
                      key={t.tier}
                      onClick={() => setActiveTier(t.tier)}
                      className={`px-2.5 py-1 rounded-lg font-bold transition-all cursor-pointer ${
                        activeTier === t.tier
                          ? 'bg-orange-500 text-white shadow-sm'
                          : 'bg-black/30 text-zinc-400 hover:text-white border border-white/10'
                      }`}
                    >
                      Tier {t.tier}
                    </button>
                  ))}
                </div>
              </div>

              {/* Interactive Risk Matrix Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-xs font-mono">
                  <thead>
                    <tr className={`border-b text-[11px] ${isLight ? 'border-slate-200 text-slate-500' : 'border-white/10 text-zinc-400'}`}>
                      <th className="py-3 px-4 font-bold">Tier</th>
                      <th className="py-3 px-4 font-bold">Risk Classification</th>
                      <th className="py-3 px-4 font-bold">Example Operational Use</th>
                      <th className="py-3 px-4 font-bold">Mandated Regulatory Control</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/10">
                    {tiers.map((t) => {
                      const isSelected = activeTier === t.tier;
                      return (
                        <tr
                          key={t.tier}
                          onClick={() => setActiveTier(t.tier)}
                          className={`transition-colors cursor-pointer ${
                            isSelected 
                              ? isLight ? 'bg-orange-50/80 font-semibold' : 'bg-orange-500/10' 
                              : isLight ? 'hover:bg-slate-50' : 'hover:bg-white/5'
                          }`}
                        >
                          <td className="py-4 px-4 font-bold text-orange-500">Tier {t.tier}</td>
                          <td className="py-4 px-4">
                            <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${t.badgeColor}`}>
                              {t.risk}
                            </span>
                          </td>
                          <td className={`py-4 px-4 ${isLight ? 'text-slate-800' : 'text-zinc-200'}`}>{t.example}</td>
                          <td className="py-4 px-4 font-bold text-amber-400">{t.control}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {/* Active Tier Technical Deep Dive */}
              {tiers.find(t => t.tier === activeTier) && (
                <div className={`mt-6 p-4 rounded-2xl border flex items-start gap-3 ${
                  isLight ? 'bg-slate-50 border-slate-200' : 'bg-zinc-900/80 border-white/10'
                }`}>
                  <div className="w-8 h-8 rounded-xl bg-orange-500/10 border border-orange-500/20 flex items-center justify-center shrink-0 text-orange-500 mt-0.5">
                    <ShieldCheck className="w-4 h-4" />
                  </div>
                  <div className="space-y-1">
                    <span className="font-mono text-xs font-bold text-orange-500 block">
                      TIER {activeTier} TECHNICAL SPECIFICATION &amp; GUARDRAIL
                    </span>
                    <p className={`text-xs ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                      {tiers.find(t => t.tier === activeTier)?.technicalNote}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {/* TAB 3: MACHINE IDENTITY & AUDIT TRAILS */}
        {activeTab === 'identity-audit' && (
          <motion.div
            key="identity-audit"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-6"
          >
            <div className={`p-6 rounded-3xl border space-y-4 ${isLight ? 'bg-white border-slate-300' : 'bg-zinc-950 border-white/15'}`}>
              <div className="w-10 h-10 rounded-2xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-500 font-bold">
                <Key className="w-5 h-5" />
              </div>
              <h3 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                Cryptographic Machine-Readable Identity
              </h3>
              <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                Mandate that deployed commercial agents carry a verifiable cryptographic credential bound to a registered legal entity (Registrar of Companies / MRA / MACRA).
              </p>
              <div className="p-3.5 rounded-2xl bg-black/30 border border-white/10 font-mono text-xs space-y-2">
                <div className="text-orange-400 font-bold text-[11px]">AGENT PKI HEADER SPECIFICATION</div>
                <div className="text-zinc-400 text-[10px] space-y-1">
                  <div>X-Agent-ID: ls-malawi-agent-842</div>
                  <div>X-Legal-Entity: LightSpeed Holdings Ltd (LL-2024-88)</div>
                  <div>X-HITL-Signature: SHA256:e3b0c44298fc1c149afbf4c8996fb...</div>
                </div>
              </div>
            </div>

            <div className={`p-6 rounded-3xl border space-y-4 ${isLight ? 'bg-white border-slate-300' : 'bg-zinc-950 border-white/15'}`}>
              <div className="w-10 h-10 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold">
                <FileCheck className="w-5 h-5" />
              </div>
              <h3 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                Tamper-Evident Append-Only Audit Logs
              </h3>
              <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                High and Critical tier systems must write state transitions to append-only logs. Traceability is the foundation of accountability and public trust.
              </p>
              <div className="p-3.5 rounded-2xl bg-black/30 border border-white/10 font-mono text-xs space-y-2">
                <div className="text-emerald-400 font-bold text-[11px]">LIGHTSPEED PRODUCTION REFERENCE</div>
                <p className="text-zinc-400 text-[11px]">
                  LightSpeed operates this exact 5-tier approval pattern in production with RACI matrices and state hashes, available as a national reference template.
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* TAB 4: DATA SOVEREIGNTY */}
        {activeTab === 'sovereignty' && (
          <motion.div
            key="sovereignty"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className={`p-6 sm:p-8 rounded-3xl border ${isLight ? 'bg-white border-slate-300' : 'bg-zinc-950 border-white/15'}`}
          >
            <h3 className={`text-xl font-bold font-display mb-4 ${isLight ? 'text-slate-900' : 'text-white'}`}>
              Recommendation 3: Anchor Data Sovereignty &amp; Localized Capability
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
              <div className="p-4 rounded-2xl bg-black/20 border border-white/10 space-y-2">
                <Globe2 className="w-5 h-5 text-orange-400" />
                <h4 className="font-bold text-white text-sm">On-Soil Data Residency</h4>
                <p className="text-zinc-400 text-[11px] leading-relaxed">
                  Prioritize in-country processing for state, health, and primary financial data under national sovereignty bounds.
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-black/20 border border-white/10 space-y-2">
                <Cpu className="w-5 h-5 text-emerald-400" />
                <h4 className="font-bold text-white text-sm">Air-Gapped Inference</h4>
                <p className="text-zinc-400 text-[11px] leading-relaxed">
                  Encourage open-weight locally hosted models to ensure system resilience during regional undersea cable outages.
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-black/20 border border-white/10 space-y-2">
                <Lock className="w-5 h-5 text-amber-400" />
                <h4 className="font-bold text-white text-sm">Vernacular Alignment</h4>
                <p className="text-zinc-400 text-[11px] leading-relaxed">
                  Invest in local talent pipelines for multi-agent orchestration and Chichewa / English bilingual model alignment.
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* TAB 5: PARTNER OFFERINGS */}
        {activeTab === 'partnership' && (
          <motion.div
            key="partnership"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className={`p-6 sm:p-8 rounded-3xl border ${isLight ? 'bg-white border-slate-300' : 'bg-zinc-950 border-white/15'}`}
          >
            <div className="flex items-center gap-2 mb-2 text-orange-400 font-mono text-xs font-bold">
              <Building2 className="w-4 h-4" />
              <span>OFFERED AS A CONTINUING PARTNER // LIGHTSPEED HOLDINGS</span>
            </div>

            <h3 className={`text-xl font-bold font-display mb-6 ${isLight ? 'text-slate-900' : 'text-white'}`}>
              Three Direct Contributions to the E-Government / UNDP Initiative
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
              <div className="p-5 rounded-2xl border border-orange-500/20 bg-orange-500/5 space-y-2">
                <span className="font-mono text-orange-400 font-bold text-sm block">01. Production Template</span>
                <strong className="block text-white text-sm font-display">Governance Controls Reference</strong>
                <p className="text-zinc-300 text-[11px] leading-relaxed">
                  Contribute our production-tested 5-tier approval frameworks, RACI matrices, and audit tools as a national reference standard.
                </p>
              </div>

              <div className="p-5 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 space-y-2">
                <span className="font-mono text-emerald-400 font-bold text-sm block">02. Lighthouse Pilot</span>
                <strong className="block text-white text-sm font-display">Citizen Inquiry / Legislative Agent</strong>
                <p className="text-zinc-300 text-[11px] leading-relaxed">
                  Co-pilot a high-visibility public lighthouse project (e.g., citizen parliamentary bill summary agent) with a non-commercial partner.
                </p>
              </div>

              <div className="p-5 rounded-2xl border border-amber-500/20 bg-amber-500/5 space-y-2">
                <span className="font-mono text-amber-400 font-bold text-sm block">03. Capacity Building</span>
                <strong className="block text-white text-sm font-display">University &amp; Talent Certification</strong>
                <p className="text-zinc-300 text-[11px] leading-relaxed">
                  Support national training programs, multi-agent certifications, and university partnerships to build a sovereign AI workforce.
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* TAB 6: COMPLETE DRAFT TEXT */}
        {activeTab === 'full-draft' && (
          <motion.div
            key="full-draft"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className="space-y-4"
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs font-bold text-orange-500">
                FORMAL STAKEHOLDER SUBMISSION DRAFT TEXT
              </span>
              <button
                onClick={handleCopyText}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-white/10 hover:bg-white/20 text-white transition-all cursor-pointer"
              >
                {copiedState ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedState ? 'Copied to Clipboard' : 'Copy Text'}</span>
              </button>
            </div>

            <pre className={`p-6 rounded-3xl border font-mono text-xs leading-relaxed whitespace-pre-wrap overflow-x-auto ${
              isLight ? 'bg-slate-900 text-slate-100 border-slate-800' : 'bg-black text-zinc-300 border-white/15'
            }`}>
              {fullDraftText}
            </pre>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
};
