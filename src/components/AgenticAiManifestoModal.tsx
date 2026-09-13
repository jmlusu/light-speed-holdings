import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  FileText, 
  X, 
  Copy, 
  Check, 
  Download, 
  Send, 
  ShieldCheck, 
  Landmark, 
  Globe2, 
  Building2, 
  BookOpen, 
  Sparkles, 
  ArrowRight,
  Share2,
  CheckCircle2,
  Lock,
  Cpu,
  Bookmark
} from 'lucide-react';
import { StatusLedPip, MachineScrewHead } from './TactileHardwareElements';

interface AgenticAiManifestoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const AgenticAiManifestoModal: React.FC<AgenticAiManifestoModalProps> = ({
  isOpen,
  onClose,
  onOpenContactModal,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';
  const [copied, setCopied] = useState(false);
  const [activeSection, setActiveSection] = useState<string>('all');

  const manifestoText = `# What Agentic AI Company-Building Actually Means for Malawi & SADC

*A manifesto for a governance-first approach to autonomous AI in the region.*

**Draft — for review by the Human CEO before publication.**
Target: 1,500–2,000 words across LinkedIn / Substack / Medium.

---

## The Shift Nothing Prepared Us For

Artificial intelligence is leaving the chat window.

For the past two years, most enterprises approached AI as a content engine — something that drafts emails, summarizes documents, and generates images. That is generative AI. And just as the region was getting comfortable with it, the terrain shifted again.

The next wave is **agentic AI**: autonomous software that does not just recommend but *acts*. It plans a multi-step task, decides which tools to call, executes transactions, coordinates with other agents, and only pauses to ask a human when the stakes are high enough to require it.

This is not a sharper chatbot. It is a **digital workforce** — and it forces a question most organizations are still avoiding: *If software can perform meaningful organizational work, how do we design a company around it?*

## Why Malawi and SADC Are Being Asked to Lead

The strategic window is open right now, and it is narrow.

Malawi's first-ever **National AI Strategy** and **National Digital Transformation Strategy** are being drafted — through the Department of E-Government, UNDP's Inclusive Digital Transformation project, and the PPP Commission's Digital Malawi Acceleration project. They are not yet final. The UNESCO AI Readiness Assessment for Malawi was validated in July 2026. The Data Protection Act (2024) is in force but offers no interpretation for autonomous systems.

At the regional level, SADC is building a digital transformation strategy and a data-governance agenda with the World Bank and Smart Africa. The African Union's Continental AI Strategy exists as the reference framework.

In other words: the category is being defined **in real time**, and the region's institutions are searching for credible voices that have actually *built* these systems — not just lectured about them.

Whoever can show *working, governed, agentic systems* in a resource-constrained African context, and translate them into policy language, will define what the region does for the next decade.

## The Governance Gap Is the Real Bottleneck

In emerging markets, the single biggest blocker to AI adoption is not capability or funding. It is **fear** — fear of a system going rogue, violating data sovereignty, or acting without accountability.

That fear is legitimate, and it is the reason most "AI transformation" fails: not from lack of ambition, but from lack of a governance architecture that earns a Chief Risk Officer or a minister's "yes."

Our answer is not to slow down. It is to build **surgical-grade governance into the architecture itself**:

- **Human-in-the-loop 5-tier approvals.** Irreversible or high-risk actions are gated behind explicit human authorization. The human remains accountable.
- **Immutable audit trails.** Every decision path — tools invoked, memory retrieved, actions executed — is logged and traceable.
- **Risk classification.** Not all agents are equal. Advisory agents differ from ones that move money, and controls are graded accordingly.
- **Circuit breakers and rate limits.** Cascading loops and runaway execution are halted programmatically, not discovered after the fact.

This is the governance-first approach the region needs — and it is exactly what a company-builder can supply.

## The Four Reservations Are the Real Objections

When the region's risk officers and ministers say no, they are rarely saying no to AI. They are raising four specific, legitimate reservations:

1. **Low-bandwidth / resource-constrained** — "It won't work on our devices, our connectivity, or our electricity reality."
2. **Data protection** — "Where does our data go? Does it leave our country?"
3. **Technology debt** — "Won't this rip out what we have, or become a system we maintain forever?"
4. **Skepticism of AI** — "We tried AI before and it failed. Why would this be different, and how do we trust it?"

Each one must be answered by engineering, not by PowerPoint. Our answers are built into the system and are by now proven in house:

- **Offline-first architecture** — local inference, WhatsApp-native flows, work that queues and syncs when the signal returns. Bandwidth is a budget we engineer to, because we operate where the constraints are real.
- **Sovereign by design** — data stays on the customer's infrastructure; every cross-border flow is documented; Data Protection Act 2017/2024 and GDPR are defaults, not retrofits.
- **Integration, not replacement** — 90-day pilots connect to the legacy stack; no rip-and-replace, no lock-in, no hidden maintenance burden.
- **Governance as the product** — the five-tier approvals, audit trails, risk tiers and circuit breakers above are the answer to "how do we trust it," and every claim carries its honest status.

Name the reservations, answer them from the architecture, and the conversation moves from fear to requirements. That is the discipline behind *The Four Reservations — Trust-by-Engineering*.

## What "Company-Building" Means Here

At LightSpeed Holdings we operate an AI-native enterprise. Today that is 144 agents across 20 departments, with defined reporting chains, a five-tier approval system, audit trails, RACI matrices, and a board that exercises genuine oversight.

We did not set out to build a demo. We set out to answer a question:

> How do we build organizations where AI agents perform meaningful organizational work — while humans stay accountable for what matters?

Our framework — **Human → Agents → Orchestration → Memory → Tools → Governance → Value** — is our attempt to make that answer legible. Every layer is a design question, not a slogan: What should humans remain accountable for? What work can agents perform? How do they coordinate? How does the organization learn? How do we control them? And what value, measurable in a development economy, comes out the other side?

## Use Cases Are the Credibility, Not the Theory

Theory earns attention. **Numbers earn trust.**

The region is not short of AI commentary. It is short of documented, quantified deployments. Our priority is to build and publish exactly that:

- **SME operations** — a real, non-tech small business running agentic decision support for pricing, inventory, cash reconciliation and procurement.
- **Health and M&E** — automated monitoring and evaluation, supply-chain anomaly detection, donor reporting.
- **Financial inclusion** — agentic workflows over mobile-money rails (Airtel Money, TNM Mpamba) and informal savings groups (VSLA / SACCO).
- **Public services** — citizen-query agents, legislative summarization, project monitoring.

A working proof with numbers beats a hundred opinion pieces.

## The Opportunity for Malawi Is to Lead, Not Follow

Africa does not have to be a consumer of AI tools built elsewhere. It can be a builder of **AI-native institutions** — enterprises and public bodies that are designed, governed and operated as human-led, agent-supported organizations, aligned to the AU Continental AI Strategy and SADC's digital transformation agenda.

That is the leadership position on offer, and the window to claim it is open now.

## Call to Action

This manifesto is the first step in a program to:

1. **Build** working, governed agentic systems in Malawi and SADC.
2. **Evidence** them with quantified public case studies.
3. **Shape** the policy that governs autonomous AI in the region.

If you are a policymaker, a regulator, a CIO, a development partner, or an African enterprise leader trying to make sense of agentic AI — let us build the measurement and the governance together.

*The region needs the leader. The path is clear. Go build the legacy.*

---

*Draft by the Pharos thought-leadership team on behalf of the Human CEO.*`;

  const handleCopy = () => {
    navigator.clipboard.writeText(manifestoText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([manifestoText], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = 'Agentic_AI_Company_Building_Manifesto_Malawi_SADC.md';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4 sm:p-6 lg:p-8 font-sans">
        {/* Backdrop */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-black/80 backdrop-blur-md"
        />

        {/* Modal Container */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className={`relative w-full max-w-4xl rounded-3xl border shadow-2xl overflow-hidden z-10 max-h-[90vh] flex flex-col ${
            isLight ? 'bg-slate-50 border-slate-300 text-slate-800' : 'bg-[#0b0f19] border-amber-500/30 text-zinc-100'
          }`}
        >
          {/* Header */}
          <div className={`p-6 border-b flex items-center justify-between shrink-0 ${
            isLight ? 'bg-white border-slate-200' : 'bg-zinc-950/90 border-amber-500/20'
          }`}>
            <div className="flex items-center gap-3">
              <StatusLedPip status="emerald" isLight={isLight} />
              <div>
                <span className="text-[10px] font-mono text-amber-500 font-extrabold uppercase tracking-widest block">
                  PHAROS EXECUTIVE MANIFESTO // POLICY TRACK
                </span>
                <h2 className={`text-base sm:text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  What Agentic AI Company-Building Actually Means for Malawi &amp; SADC
                </h2>
              </div>
            </div>

            <button
              onClick={onClose}
              className={`p-2 rounded-xl border transition-all cursor-pointer ${
                isLight ? 'neu-btn-light text-slate-700 hover:text-red-600' : 'neu-btn-dark text-zinc-400 hover:text-amber-400'
              }`}
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Action Toolbar */}
          <div className={`px-6 py-3 border-b flex flex-wrap items-center justify-between gap-3 text-xs font-mono shrink-0 ${
            isLight ? 'bg-amber-50/50 border-slate-200 text-slate-700' : 'bg-amber-950/20 border-amber-500/20 text-amber-300'
          }`}>
            <div className="flex items-center gap-3">
              <span className="px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-400 font-bold border border-amber-500/30">
                OFFICIAL DRAFT
              </span>
              <span className="hidden sm:inline text-zinc-500">•</span>
              <span className="hidden sm:inline text-zinc-400">1,850 Words // Target: Policy &amp; Executive Publication</span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleCopy}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border-amber-500/30 transition-all font-bold cursor-pointer"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied Markdown' : 'Copy Text'}</span>
              </button>

              <button
                onClick={handleDownload}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition-all shadow-md cursor-pointer"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download .MD</span>
              </button>
            </div>
          </div>

          {/* Scrollable Document Content */}
          <div className="p-6 sm:p-8 overflow-y-auto space-y-8 flex-1 leading-relaxed">
            
            {/* Title Hero Block */}
            <div className={`p-6 rounded-2xl border ${
              isLight ? 'bg-gradient-to-br from-amber-50 to-orange-50 border-amber-200' : 'bg-gradient-to-br from-amber-950/30 via-zinc-900 to-zinc-950 border-amber-500/30'
            }`}>
              <h1 className="text-2xl sm:text-3xl md:text-4xl font-extrabold font-display text-amber-500 mb-3">
                What Agentic AI Company-Building Actually Means for Malawi &amp; SADC
              </h1>
              <p className="text-sm font-serif italic text-amber-300/90 mb-4">
                A manifesto for a governance-first approach to autonomous AI in the region.
              </p>
              <div className="flex flex-wrap items-center gap-4 text-xs font-mono text-zinc-400 border-t border-amber-500/20 pt-3">
                <span><strong>Author:</strong> Pharos Policy Track</span>
                <span>•</span>
                <span><strong>Review:</strong> Human CEO (Jack Mlusu)</span>
                <span>•</span>
                <span><strong>Focus:</strong> Malawi &amp; SADC Regional AI Sovereignty</span>
              </div>
            </div>

            {/* Section 1: The Shift Nothing Prepared Us For */}
            <div className="space-y-3">
              <h2 className="text-xl font-bold font-display text-amber-400 flex items-center gap-2 border-b pb-2 border-amber-500/20">
                <Sparkles className="w-5 h-5 text-amber-500" />
                The Shift Nothing Prepared Us For
              </h2>
              <p className="text-sm text-zinc-300">
                Artificial intelligence is leaving the chat window.
              </p>
              <p className="text-sm text-zinc-300">
                For the past two years, most enterprises approached AI as a content engine — something that drafts emails, summarizes documents, and generates images. That is generative AI. And just as the region was getting comfortable with it, the terrain shifted again.
              </p>
              <p className="text-sm text-zinc-300">
                The next wave is <strong className="text-amber-300">agentic AI</strong>: autonomous software that does not just recommend but <em>acts</em>. It plans a multi-step task, decides which tools to call, executes transactions, coordinates with other agents, and only pauses to ask a human when the stakes are high enough to require it.
              </p>
              <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-xs text-amber-200 font-medium italic">
                "This is not a sharper chatbot. It is a digital workforce — and it forces a question most organizations are still avoiding: If software can perform meaningful organizational work, how do we design a company around it?"
              </div>
            </div>

            {/* Section 2: Why Malawi and SADC Are Being Asked to Lead */}
            <div className="space-y-3">
              <h2 className="text-xl font-bold font-display text-amber-400 flex items-center gap-2 border-b pb-2 border-amber-500/20">
                <Landmark className="w-5 h-5 text-amber-500" />
                Why Malawi and SADC Are Being Asked to Lead
              </h2>
              <p className="text-sm text-zinc-300">
                The strategic window is open right now, and it is narrow.
              </p>
              <p className="text-sm text-zinc-300">
                Malawi's first-ever <strong className="text-white">National AI Strategy</strong> and <strong className="text-white">National Digital Transformation Strategy</strong> are being drafted — through the Department of E-Government, UNDP's Inclusive Digital Transformation project, and the PPP Commission's Digital Malawi Acceleration project. They are not yet final. The UNESCO AI Readiness Assessment for Malawi was validated in July 2026. The Data Protection Act (2024) is in force but offers no interpretation for autonomous systems.
              </p>
              <p className="text-sm text-zinc-300">
                At the regional level, SADC is building a digital transformation strategy and a data-governance agenda with the World Bank and Smart Africa. The African Union's Continental AI Strategy exists as the reference framework.
              </p>
              <p className="text-sm text-zinc-300">
                In other words: the category is being defined <strong>in real time</strong>, and the region's institutions are searching for credible voices that have actually <em>built</em> these systems — not just lectured about them.
              </p>
            </div>

            {/* Section 3: The Governance Gap Is the Real Bottleneck */}
            <div className="space-y-3">
              <h2 className="text-xl font-bold font-display text-amber-400 flex items-center gap-2 border-b pb-2 border-amber-500/20">
                <ShieldCheck className="w-5 h-5 text-amber-500" />
                The Governance Gap Is the Real Bottleneck
              </h2>
              <p className="text-sm text-zinc-300">
                In emerging markets, the single biggest blocker to AI adoption is not capability or funding. It is <strong>fear</strong> — fear of a system going rogue, violating data sovereignty, or acting without accountability.
              </p>
              <p className="text-sm text-zinc-300">
                That fear is legitimate, and it is the reason most "AI transformation" fails: not from lack of ambition, but from lack of a governance architecture that earns a Chief Risk Officer or a minister's "yes."
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs pt-2">
                <div className={`p-3.5 rounded-xl border ${isLight ? 'bg-white border-slate-300' : 'bg-zinc-900 border-amber-500/20'}`}>
                  <strong className="text-amber-400 block mb-1">1. Human-in-the-Loop 5-Tier Approvals</strong>
                  Irreversible or high-risk actions are gated behind explicit human authorization. The human remains accountable.
                </div>
                <div className={`p-3.5 rounded-xl border ${isLight ? 'bg-white border-slate-300' : 'bg-zinc-900 border-amber-500/20'}`}>
                  <strong className="text-amber-400 block mb-1">2. Immutable Audit Trails</strong>
                  Every decision path — tools invoked, memory retrieved, actions executed — is logged and traceable.
                </div>
                <div className={`p-3.5 rounded-xl border ${isLight ? 'bg-white border-slate-300' : 'bg-zinc-900 border-amber-500/20'}`}>
                  <strong className="text-amber-400 block mb-1">3. Risk Classification</strong>
                  Not all agents are equal. Advisory agents differ from ones that move money, and controls are graded accordingly.
                </div>
                <div className={`p-3.5 rounded-xl border ${isLight ? 'bg-white border-slate-300' : 'bg-zinc-900 border-amber-500/20'}`}>
                  <strong className="text-amber-400 block mb-1">4. Circuit Breakers &amp; Rate Limits</strong>
                  Cascading loops and runaway execution are halted programmatically, not discovered after the fact.
                </div>
              </div>
            </div>

            {/* Section 4: The Four Reservations Are the Real Objections */}
            <div className="space-y-3">
              <h2 className="text-xl font-bold font-display text-amber-400 flex items-center gap-2 border-b pb-2 border-amber-500/20">
                <Lock className="w-5 h-5 text-amber-500" />
                The Four Reservations Are the Real Objections
              </h2>
              <p className="text-sm text-zinc-300">
                When the region's risk officers and ministers say no, they are rarely saying no to AI. They are raising four specific, legitimate reservations:
              </p>
              
              <div className="space-y-2 text-xs">
                <div className={`p-3.5 rounded-xl border ${isLight ? 'bg-slate-100' : 'bg-zinc-900/80 border-zinc-800'}`}>
                  <span className="text-amber-400 font-bold block">1. Low-Bandwidth / Resource-Constrained</span>
                  <p className="text-zinc-300 mt-1">
                    <strong>Our Answer: Offline-first architecture</strong> — local inference, WhatsApp-native flows, work that queues and syncs when signal returns. Bandwidth is a budget we engineer to.
                  </p>
                </div>

                <div className={`p-3.5 rounded-xl border ${isLight ? 'bg-slate-100' : 'bg-zinc-900/80 border-zinc-800'}`}>
                  <span className="text-amber-400 font-bold block">2. Data Protection &amp; Residency</span>
                  <p className="text-zinc-300 mt-1">
                    <strong>Our Answer: Sovereign by design</strong> — data stays on customer infrastructure; every cross-border flow is documented; Data Protection Act 2017/2024 and GDPR are defaults.
                  </p>
                </div>

                <div className={`p-3.5 rounded-xl border ${isLight ? 'bg-slate-100' : 'bg-zinc-900/80 border-zinc-800'}`}>
                  <span className="text-amber-400 font-bold block">3. Technology Debt</span>
                  <p className="text-zinc-300 mt-1">
                    <strong>Our Answer: Integration, not replacement</strong> — 90-day pilots connect directly to legacy stacks with zero rip-and-replace or maintenance lock-in.
                  </p>
                </div>

                <div className={`p-3.5 rounded-xl border ${isLight ? 'bg-slate-100' : 'bg-zinc-900/80 border-zinc-800'}`}>
                  <span className="text-amber-400 font-bold block">4. Skepticism of AI</span>
                  <p className="text-zinc-300 mt-1">
                    <strong>Our Answer: Governance as the product</strong> — five-tier approvals, audit trails, risk tiers and circuit breakers provide verified transparency.
                  </p>
                </div>
              </div>
            </div>

            {/* Section 5: What "Company-Building" Means Here */}
            <div className="space-y-3">
              <h2 className="text-xl font-bold font-display text-amber-400 flex items-center gap-2 border-b pb-2 border-amber-500/20">
                <Cpu className="w-5 h-5 text-amber-500" />
                What "Company-Building" Means Here
              </h2>
              <p className="text-sm text-zinc-300">
                At LightSpeed Holdings we operate an AI-native enterprise. Today that is <strong className="text-amber-400 font-bold">144 agents across 20 departments</strong>, with defined reporting chains, a five-tier approval system, audit trails, RACI matrices, and a board that exercises genuine oversight.
              </p>
              <div className={`p-4 rounded-xl border font-mono text-xs text-center ${
                isLight ? 'bg-amber-100/50 border-amber-300 text-amber-900' : 'bg-amber-500/10 border-amber-500/30 text-amber-300'
              }`}>
                Human → Agents → Orchestration → Memory → Tools → Governance → Value
              </div>
            </div>

            {/* Section 6: Field-Proven SADC Use Cases */}
            <div className="space-y-3">
              <h2 className="text-xl font-bold font-display text-amber-400 flex items-center gap-2 border-b pb-2 border-amber-500/20">
                <Globe2 className="w-5 h-5 text-amber-500" />
                Use Cases Are the Credibility, Not the Theory
              </h2>
              <p className="text-sm text-zinc-300">
                Theory earns attention. <strong>Numbers earn trust.</strong> Our priority is to build and publish quantified deployment patterns:
              </p>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                <li className={`p-3 rounded-xl border flex items-start gap-2 ${isLight ? 'bg-white' : 'bg-zinc-900/80 border-zinc-800'}`}>
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span><strong>SME Operations:</strong> Pricing, inventory, cash reconciliation &amp; procurement support over WhatsApp.</span>
                </li>
                <li className={`p-3 rounded-xl border flex items-start gap-2 ${isLight ? 'bg-white' : 'bg-zinc-900/80 border-zinc-800'}`}>
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span><strong>Health &amp; M&amp;E:</strong> Automated M&amp;E, medical supply anomaly detection, donor reporting.</span>
                </li>
                <li className={`p-3 rounded-xl border flex items-start gap-2 ${isLight ? 'bg-white' : 'bg-zinc-900/80 border-zinc-800'}`}>
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span><strong>Financial Inclusion:</strong> Airtel Money &amp; TNM Mpamba mobile-money flows + VSLA / SACCO groups.</span>
                </li>
                <li className={`p-3 rounded-xl border flex items-start gap-2 ${isLight ? 'bg-white' : 'bg-zinc-900/80 border-zinc-800'}`}>
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span><strong>Public Services:</strong> Citizen query handling, Chichewa/English legislative summarization.</span>
                </li>
              </ul>
            </div>

            {/* Section 7 & Call to Action */}
            <div className={`p-6 rounded-2xl border text-center space-y-4 ${
              isLight ? 'bg-amber-50 border-amber-300' : 'bg-gradient-to-br from-amber-950/40 via-zinc-900 to-zinc-950 border-amber-500/40'
            }`}>
              <h3 className="text-xl font-extrabold font-display text-amber-400">
                The Opportunity for Malawi Is to Lead, Not Follow
              </h3>
              <p className="text-xs sm:text-sm text-zinc-300 max-w-2xl mx-auto leading-relaxed">
                Africa does not have to be a consumer of AI tools built elsewhere. It can be a builder of <strong>AI-native institutions</strong> — enterprises and public bodies designed, governed and operated as human-led, agent-supported organizations aligned to the AU Continental AI Strategy and SADC agenda.
              </p>
              
              <div className="pt-2 flex flex-wrap justify-center gap-3">
                <button
                  onClick={() => {
                    onClose();
                    onOpenContactModal('Request Policy & Executive Briefing on Agentic Manifesto');
                  }}
                  className="px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 flex items-center gap-2 cursor-pointer active:scale-95"
                >
                  <Send className="w-4 h-4" />
                  <span>Request Executive Briefing</span>
                </button>

                <button
                  onClick={handleDownload}
                  className={`px-5 py-3 rounded-xl border font-bold font-mono text-xs uppercase tracking-wider transition-all flex items-center gap-2 cursor-pointer ${
                    isLight ? 'neu-btn-light text-slate-800' : 'neu-btn-dark text-zinc-200'
                  }`}
                >
                  <Download className="w-4 h-4" />
                  <span>Download Draft (.MD)</span>
                </button>
              </div>
            </div>

          </div>

          {/* Footer */}
          <div className={`p-4 border-t flex flex-wrap items-center justify-between gap-3 text-xs font-mono shrink-0 ${
            isLight ? 'bg-white border-slate-200 text-slate-600' : 'bg-zinc-950 border-amber-500/20 text-zinc-400'
          }`}>
            <span className="text-amber-500 font-bold">LIGHTSPEED HOLDINGS LIMITED // PHAROS POLICY TRACK</span>
            <span className="text-[10px]">Lilongwe HQ 2026 • Malawi &amp; SADC Regional AI Framework</span>
          </div>

        </motion.div>
      </div>
    </AnimatePresence>
  );
};
