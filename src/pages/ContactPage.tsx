import React from 'react';
import { MessageSquare, PhoneCall, Landmark, Radar, Cpu } from 'lucide-react';
import { ContactSection } from '../components/ContactSection';

interface ContactPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

const ENTRY_POINTS: { icon: React.ComponentType<{ className?: string }>; title: string; body: string }[] = [
  {
    icon: PhoneCall,
    title: 'Book a Discovery Call',
    body: 'A straightforward 45-minute conversation with a human. We map your current situation and tell you honestly whether — and how — agentic AI fits.',
  },
  {
    icon: Landmark,
    title: 'Board-Level Briefing',
    body: 'A governed, approval-gated discovery for boards and leadership teams — no product demo, real questions about risk, governance, and sequencing.',
  },
  {
    icon: Radar,
    title: 'AI Readiness Assessment',
    body: 'A sector-aware diagnostic scoring your operating model across strategy, data, technology, people, and governance — with a 90-day pilot path.',
  },
  {
    icon: Cpu,
    title: 'AI Company Builder License',
    body: 'Interested in running your own governed AI workforce? License the same engine that runs LightSpeed, self-hosted and provider-agnostic.',
  },
];

/**
 * /contact — the "Start a Conversation" multi-entry-point page. Four distinct
 * ways to begin, one human in the loop underneath.
 */
export const ContactPage: React.FC<ContactPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      {/* Page Intro */}
      <header className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-24 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
          <MessageSquare className="w-3.5 h-3.5" aria-hidden="true" />
          <span>CONTACT // START A CONVERSATION</span>
        </div>
        <h1 className={`mt-4 text-3xl sm:text-5xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}>
          Talk to a Human First
        </h1>
        <p className={`mt-4 max-w-2xl text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          Every conversation starts with a person, not a chatbot. Tell us where your organisation is
          today — we will be honest about whether we can help and exactly what it takes to start.
          Responses within 12 business hours.
        </p>
      </header>

      {/* Entry points */}
      <section aria-label="Ways to start a conversation" className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-10 pb-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {ENTRY_POINTS.map((point, idx) => {
            const Icon = point.icon;
            return (
              <a
                key={point.title}
                href="#contact"
                className={`rounded-3xl p-6 border transition-all h-full block group ${
                  isLight
                    ? 'bg-white/95 border-slate-300 text-slate-900 shadow-md hover:shadow-xl hover:-translate-y-0.5'
                    : 'bg-zinc-950/80 border-white/15 text-zinc-100 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
                }`}
              >
                <span aria-hidden="true" className="inline-flex w-9 h-9 items-center justify-center rounded-xl bg-ls-red/10 text-ls-red">
                  <Icon className="w-4 h-4" />
                </span>
                <h2 className="mt-4 font-display font-bold text-sm sm:text-base tracking-tight">{point.title}</h2>
                <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-slate-700' : 'text-zinc-300'
                }`}>
                  {point.body}
                </p>
                <span className={`mt-4 inline-flex items-center gap-1.5 text-[11px] font-mono font-bold tracking-widest ${
                  isLight ? 'text-slate-500' : 'text-zinc-400'
                } group-hover:text-ls-red`}>
                  START →
                </span>
              </a>
            );
          })}
        </div>
      </section>

      <ContactSection theme={theme} />
    </>
  );
};

export default ContactPage;
