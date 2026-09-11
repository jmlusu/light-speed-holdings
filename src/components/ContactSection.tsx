import React, { useState } from 'react';
import { ShieldCheck, Clock, Globe2, Send, CheckCircle2 } from 'lucide-react';
import { AcousticVentGrille } from './TactileHardwareElements';

interface ContactSectionProps {
  theme: 'light' | 'dark';
}

export const ContactSection: React.FC<ContactSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const [contactSubmitted, setContactSubmitted] = useState<boolean>(false);
  const [contactFormData, setContactFormData] = useState({
    name: '',
    title: '',
    organization: '',
    email: '',
    scope: 'Advisory Architecture Sprint (2 Weeks)',
    objective: '',
    timeline: 'Within 30 days'
  });

  const handleContactSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setContactSubmitted(true);
  };

  return (
    <section id="contact" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">

        <div className="lg:col-span-5 space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest font-bold">
            <span>START A CONVERSATION</span>
          </div>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Tell Us Where You Are
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            We will be honest about whether we can help — and exactly what it takes to start. A human reviews every submission and responds within 12 business hours.
          </p>

          <div className={`space-y-4 pt-4 border-t ${isLight ? 'border-slate-200' : 'border-white/15'}`}>
            <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
              <ShieldCheck className="w-4 h-4 text-ls-cyan shrink-0" />
              <span>Strict non-disclosure agreement standard</span>
            </div>
            <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
              <Clock className="w-4 h-4 text-ls-red shrink-0" />
              <span>Executive response within 12 business hours</span>
            </div>
            <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
              <Globe2 className="w-4 h-4 text-ls-cyan shrink-0" />
              <span>Offices in Southern Africa and International Advisory Network</span>
            </div>
          </div>
        </div>

        <div className="lg:col-span-7">
          <div className={`p-8 sm:p-10 rounded-3xl relative overflow-hidden shadow-2xl ${
            isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
          }`}>
            {/* Hardware Screws */}
            <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
            <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
            <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
            <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

            {/* Console Header Bar */}
            <div className="flex items-center justify-between pb-3.5 mb-6 border-b border-black/10 dark:border-white/10 px-1">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-ls-red shadow-[0_0_8px_rgba(230,57,70,0.9)]" />
                <span className="font-mono text-xs font-bold tracking-wider">
                  CONVERSATION CONSOLE
                </span>
              </div>
              <AcousticVentGrille variant="strip" isLight={isLight} />
            </div>

            {contactSubmitted ? (
              <div className="py-12 text-center space-y-4">
                <div className="w-16 h-16 rounded-full bg-ls-cyan/20 text-ls-cyan border border-ls-cyan/40 flex items-center justify-center mx-auto shadow-[0_0_15px_rgba(16,185,129,0.3)]">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <h3 className={`text-2xl font-black tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  Message Received
                </h3>
                <p className={`text-justify text-sm max-w-md mx-auto leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                  Thank you. A human will review your message and contact you directly within 12 business hours.
                </p>
                <button
                  onClick={() => setContactSubmitted(false)}
                  className="px-6 py-2.5 rounded-xl bg-ls-red text-white font-bold text-xs tracking-wider cursor-pointer shadow-md hover:bg-ls-red transition-all"
                >
                  Submit Another Inquiry
                </button>
              </div>
            ) : (
              <form onSubmit={handleContactSubmit} className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
<label htmlFor="ct-executive-name" className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
  Executive Name *
</label>
<input
  id="ct-executive-name"
  type="text"
  required
                      placeholder="e.g. Dr. K. Mlangeni"
                      value={contactFormData.name}
                      onChange={(e) => setContactFormData({ ...contactFormData, name: e.target.value })}
                      className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-ls-red transition-colors font-medium ${
                        isLight
                          ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-zinc-400 shadow-inner'
                          : 'bg-ls-navy border-white/20 text-white placeholder:text-zinc-400 shadow-inner'
                      }`}
                    />
                  </div>
                  <div>
<label htmlFor="ct-executive-title" className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
  Executive Title *
</label>
<input
  id="ct-executive-title"
  type="text"
  required
                      placeholder="e.g. Chief Executive Officer"
                      value={contactFormData.title}
                      onChange={(e) => setContactFormData({ ...contactFormData, title: e.target.value })}
                      className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-ls-red transition-colors font-medium ${
                        isLight
                          ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-zinc-400 shadow-inner'
                          : 'bg-ls-navy border-white/20 text-white placeholder:text-zinc-400 shadow-inner'
                      }`}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
<label htmlFor="ct-organization" className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
  Institution / Entity *
</label>
<input
  id="ct-organization"
  type="text"
  required
                      placeholder="e.g. Your Organisation"
                      value={contactFormData.organization}
                      onChange={(e) => setContactFormData({ ...contactFormData, organization: e.target.value })}
                      className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-ls-red transition-colors font-medium ${
                        isLight
                          ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-zinc-400 shadow-inner'
                          : 'bg-ls-navy border-white/20 text-white placeholder:text-zinc-400 shadow-inner'
                      }`}
                    />
                  </div>
                  <div>
<label htmlFor="ct-email" className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
  Official Email *
</label>
<input
  id="ct-email"
  type="email"
  required
                      placeholder="executive@institution.com"
                      value={contactFormData.email}
                      onChange={(e) => setContactFormData({ ...contactFormData, email: e.target.value })}
                      className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-ls-red transition-colors font-medium ${
                        isLight
                          ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-zinc-400 shadow-inner'
                          : 'bg-ls-navy border-white/20 text-white placeholder:text-zinc-400 shadow-inner'
                      }`}
                    />
                  </div>
                </div>

                <div>
<label htmlFor="ct-scope" className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
  Target Engagement Model
</label>
<select
  id="ct-scope"
                    value={contactFormData.scope}
                    onChange={(e) => setContactFormData({ ...contactFormData, scope: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-ls-red transition-colors font-medium ${
                      isLight
                        ? 'bg-slate-100/90 border-slate-300 text-slate-900 shadow-inner'
                        : 'bg-ls-navy border-white/20 text-white shadow-inner'
                    }`}
                  >
                    <option value="Advisory Architecture Sprint (2 Weeks)">Advisory Architecture Sprint (2 Weeks)</option>
                    <option value="Co-Engineered Pilot (90 Days)">Co-Engineered Pilot (90 Days)</option>
                    <option value="Enterprise Deployment">Enterprise Deployment</option>
                    <option value="Executive Boardroom Briefing">Executive Boardroom Briefing</option>
                  </select>
                </div>

                <div>
<label htmlFor="ct-objective" className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
  Strategic Objectives & Context
</label>
<textarea
  id="ct-objective"
  rows={3}
                    placeholder="Describe your current bottlenecks, regulatory constraints, or legacy IT dependencies..."
                    value={contactFormData.objective}
                    onChange={(e) => setContactFormData({ ...contactFormData, objective: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-ls-red transition-colors resize-none font-medium ${
                      isLight
                        ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-zinc-400 shadow-inner'
                        : 'bg-ls-navy border-white/20 text-white placeholder:text-zinc-400 shadow-inner'
                    }`}
                  />
                </div>

                <div className="pt-2">
                  <button
                    type="submit"
                    className="w-full py-3.5 rounded-xl bg-ls-red text-white font-bold text-xs tracking-widest transition-all flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-ls-red/25 active:scale-98"
                  >
                    <span>Send — Start the Conversation</span>
                    <Send className="w-3.5 h-3.5" />
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>

      </div>
    </section>
  );
};
