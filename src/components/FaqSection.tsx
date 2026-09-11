import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';

interface FaqSectionProps {
  theme: 'light' | 'dark';
}

const FAQ_ITEMS = [
  {
    q: "What is the purpose of the Templates & Deliverables section?",
    a: "The templates give you production-ready blueprints for agent systems, task workflows, data residency, and compliance. You can use them as starting points to deploy verified AI systems instead of spending months on requirements documents."
  },
  {
    q: "Are these templates static documents or executable artifacts?",
    a: "They are executable. Unlike consulting decks, these templates define tool boundaries, budget limits, audit logging, and API patterns you can provision and run inside your own infrastructure."
  },
  {
    q: "What is LightSpeed's core proposition?",
    a: "From Malawi, we help organizations turn strategy, data, and AI into working systems. We combine local expertise, regional relevance, and global engineering standards into a single operating stack."
  },
  {
    q: "What is structured multi-agent fleet engineering?",
    a: "Unlike consumer chatbots that can make things up or run unauthorized actions, our AI agents are limited to specific tools, rate limits, and human approval gates. Every action is logged to an unchangeable audit trail."
  },
  {
    q: "How does LightSpeed ensure data residency and privacy?",
    a: "Your data never leaves your infrastructure. We build on-site AI systems and knowledge graphs inside your perimeter, meeting local compliance and banking regulations."
  },
  {
    q: "How fast can you integrate with legacy systems?",
    a: "During the 90-Day Pilot, we build API connectors that link your legacy systems to modern event streams. Transaction times typically drop from hours or days to under a second."
  },
  {
    q: "Why do conventional transformations fail?",
    a: "Most consultancies deliver slide decks with no working code. Data stays trapped in silos. We replace that with executable strategy backed by live systems you can see working."
  },
  {
    q: "How does an organization transition from these templates to full deployment?",
    a: "We follow a 3-phase path: a 2-week advisory sprint to map your needs, a 90-day pilot with your team building live systems, then full deployment with ongoing monitoring and support."
  },
  {
    q: "Will your AI work on my phone, on Malawi's internet?",
    a: "Yes — by design. Our platform runs offline-first with local-model fallback (Ollama), WhatsApp-native flows that need no app download, and a PWA that queues actions when you lose signal and syncs on reconnect. We test on 3G and weaker connections because that is how Malawi and most of SADC actually connects."
  },
  {
    q: "Where does my data go? Does it leave Malawi?",
    a: "Your data stays on your infrastructure. Sovereign, in-country processing is the default. Every cross-border data flow to an LLM provider is documented in our G1–G4 governance gate process, routed to the most privacy-preserving option, and Malawi's Data Protection Act 2017/2024 and GDPR are built in from day one. We never use your data to train models."
  },
  {
    q: "Won't this rip out what we already use — or become a system we have to maintain forever?",
    a: "No rip-and-replace. We integrate with your existing systems via API connectors in a 90-day pilot. Your data, dashboards, and deliverables stay yours — no vendor lock-in. Agent cost is variable and transparent, not a fixed overhead you have to maintain, and we hold ourselves to the same discipline: our own engineering debt is tracked and paid down on a regular cadence."
  },
  {
    q: "We tried AI before and it failed. Why would this be different?",
    a: "Most AI failures in the region are governance failures, not technology failures — a chatbot that hallucinates, a tool that violates data sovereignty, a system with no audit trail. We are governance-first: 5-tier human-in-the-loop approvals, immutable audit trails, risk-classified agent tiers, and circuit breakers. We never fabricate proof — every claim carries its honest status."
  }
];

export const FaqSection: React.FC<FaqSectionProps> = ({ theme }) => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  const isLight = theme === 'light';

  const toggle = (idx: number) => {
    setOpenIndex((prev) => (prev === idx ? null : idx));
  };

  return (
    <section id="faq" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
        <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
          CLARITY & ASSURANCE
        </span>
        <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}>
          Frequently Asked Questions
        </h2>
        <p className={`text-justify text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          Straight answers on security, structure, and timelines for enterprise AI integration.
        </p>
      </div>

      <div className="max-w-4xl mx-auto space-y-6">
        {FAQ_ITEMS.map((faq, idx) => {
          const isOpen = openIndex === idx;
          const answerId = `faq-answer-${idx}`;
          const questionId = `faq-question-${idx}`;

          return (
            <div
              key={idx}
              className={`rounded-3xl border transition-all duration-200 ${
                isLight ? 'bg-white/95 border-slate-300 shadow-sm' : 'bg-zinc-950/80 border-white/15'
              } ${isOpen ? 'border-l-4 border-l-ls-red' : ''}`}
            >
              <button
                type="button"
                id={questionId}
                aria-expanded={isOpen}
                aria-controls={answerId}
                onClick={() => toggle(idx)}
                className={`w-full flex items-center justify-between gap-4 p-6 sm:p-8 text-left cursor-pointer transition-colors duration-200 ${
                  isLight ? 'hover:bg-slate-50' : 'hover:bg-zinc-900'
                }`}
              >
                <h3 className={`text-lg sm:text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  {faq.q}
                </h3>
                <ChevronDown
                  className={`shrink-0 w-5 h-5 transition-transform duration-200 ${
                    isLight ? 'text-slate-500' : 'text-zinc-400'
                  } ${isOpen ? 'rotate-180' : ''}`}
                  aria-hidden="true"
                />
              </button>
              <div
                id={answerId}
                role="region"
                aria-labelledby={questionId}
                className="grid transition-all duration-200"
                style={{ gridTemplateRows: isOpen ? '1fr' : '0fr' }}
              >
                <div className="overflow-hidden">
                  <p className={`text-justify text-sm leading-relaxed px-6 sm:px-8 pb-6 sm:pb-8 pt-0 ${isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'}`}>
                    {faq.a}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};
