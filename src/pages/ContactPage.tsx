import React from 'react';
import { MessageSquare } from 'lucide-react';
import { ContactSection } from '../components/ContactSection';

interface ContactPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

/**
 * Contact route: a short briefing-oriented intro above the full executive
 * contact section (which owns its own submit state).
 */
export const ContactPage: React.FC<ContactPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      {/* Page Intro */}
      <header className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-24 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
          <MessageSquare className="w-3.5 h-3.5" aria-hidden="true" />
          <span>CONTACT / EXECUTIVE BRIEFING</span>
        </div>
        <h1 className={`mt-4 text-3xl sm:text-5xl font-black tracking-tight font-display ${
          isLight ? 'text-slate-900' : 'text-white'
        }`}>
          Talk to the Team That Runs 144 Agents
        </h1>
        <p className={`mt-4 max-w-2xl text-sm sm:text-base leading-relaxed ${
          isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
        }`}>
          Book a confidential 45-minute briefing with our managing partners. We will map your
          operational bottlenecks and tell you honestly whether governed on-site AI is the right fit.
        </p>
      </header>

      <ContactSection theme={theme} />
    </>
  );
};

export default ContactPage;
