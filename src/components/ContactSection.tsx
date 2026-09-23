import React, { useCallback, useState } from 'react';
import { ShieldCheck, Clock, Globe2, Send, CheckCircle2, MessageCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import { AcousticVentGrille } from './TactileHardwareElements';
import { useTurnstile } from '../hooks/useTurnstile';
import { ENQUIRY_SLA_COPY, ENQUIRY_GENERIC_ERROR, enquiryPayload } from '../lib/enquiry';

interface ContactSectionProps {
  theme: 'light' | 'dark';
}

interface ContactStep {
  id: number;
  key: string;
  name: string;
  description: string;
}

const steps: ContactStep[] = [
  { id: 1, key: 'DISCOVER', name: 'Discover', description: 'Tell us who you are and where your organisation sits today.' },
  { id: 2, key: 'DIAGNOSE', name: 'Diagnose', description: 'Share the engagement model and the bottlenecks you want us to examine.' },
  { id: 3, key: 'DESIGN', name: 'Design', description: 'Set the timeline so we can shape a realistic starting point.' },
  { id: 4, key: 'BUILD', name: 'Build', description: 'Review everything you have entered before we prepare your brief.' },
  { id: 5, key: 'GOVERN', name: 'Govern', description: 'Submit securely — a human reviews every enquiry under our governance standard.' }
];

export const ContactSection: React.FC<ContactSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const [contactSubmitted, setContactSubmitted] = useState<boolean>(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [referenceId, setReferenceId] = useState<string | null>(null);
  const [honeypot, setHoneypot] = useState('');
  const [currentStep, setCurrentStep] = useState(1);
  const [turnstileToken, setTurnstileToken] = useState<string | null>(null);
  const { containerRef, siteKey, reset } = useTurnstile(
    'contact',
    useCallback((token: string) => setTurnstileToken(token), [])
  );
  const whatsappNumber = import.meta.env.VITE_WHATSAPP_NUMBER as string | undefined;
  const [contactFormData, setContactFormData] = useState({
    name: '',
    title: '',
    organization: '',
    email: '',
    scope: 'Advisory Architecture Sprint (2 Weeks)',
    objective: '',
    timeline: 'Within 30 days'
  });

  const goToStep = (step: number) => {
    if (step >= 1 && step <= steps.length) setCurrentStep(step);
  };
  const nextStep = () => goToStep(currentStep + 1);
  const prevStep = () => goToStep(currentStep - 1);

  const canAdvance = (): boolean => {
    switch (currentStep) {
      case 1:
        return Boolean(contactFormData.name && contactFormData.title && contactFormData.organization && contactFormData.email);
      case 2:
        return Boolean(contactFormData.scope && contactFormData.objective.trim());
      default:
        return true;
    }
  };

  const handleContactSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting) return;
    if (currentStep < 5) {
      if (canAdvance()) nextStep();
      return;
    }
    setSubmitting(true);
    setSubmitError(null);
    try {
      const res = await fetch('/api/enquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
          enquiryPayload(
            {
              form: 'contact',
              name: contactFormData.name,
              organization: contactFormData.organization,
              email: contactFormData.email,
              enquiryType: contactFormData.scope,
              message: contactFormData.objective
            },
            turnstileToken,
            honeypot
          )
        )
      });
      if (res.status === 201) {
        const data = (await res.json()) as { referenceId?: string };
        setReferenceId(data.referenceId ?? null);
        setContactSubmitted(true);
      } else {
        const data = (await res.json().catch(() => null)) as { error?: { message?: string } } | null;
        setSubmitError(data?.error?.message ?? ENQUIRY_GENERIC_ERROR);
      }
    } catch {
      setSubmitError(ENQUIRY_GENERIC_ERROR);
    } finally {
      setSubmitting(false);
      reset();
    }
  };

  const activeStep = steps[currentStep - 1];

  const fieldInputClass = `w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-ls-red transition-colors font-medium ${
    isLight
      ? 'bg-ls-grey-light/90 border-ls-grey-dark text-ls-navy placeholder:text-ls-grey-light-text shadow-inner'
      : 'bg-ls-navy border-ls-white/20 text-ls-white placeholder:text-ls-grey-light-text shadow-inner'
  }`;
  const labelClass = `block text-[11px] font-body tracking-wider mb-1 font-bold ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`;

  return (
    <section id="contact" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
      isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80'
    }`}>
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">

        <div className="lg:col-span-5 space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-body text-[11px] tracking-widest font-bold">
            <span>START A CONVERSATION</span>
          </div>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-ls-navy' : 'text-ls-white'
          }`}>
            Tell Us Where You Are
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
          }`}>
            We will be honest about whether we can help — and exactly what it takes to start. A human reviews every submission and responds within 12 business hours.
          </p>

          <div className={`space-y-4 pt-4 border-t ${isLight ? 'border-ls-grey-dark' : 'border-ls-white/15'}`}>
            <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'}`}>
              <ShieldCheck className="w-4 h-4 text-ls-cyan shrink-0" />
              <span>Strict non-disclosure agreement standard</span>
            </div>
            <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'}`}>
              <Clock className="w-4 h-4 text-ls-red shrink-0" />
              <span>Executive response within two business days</span>
            </div>
            <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'}`}>
              <Globe2 className="w-4 h-4 text-ls-cyan shrink-0" />
              <span>Offices in Southern Africa and International Advisory Network</span>
            </div>
          </div>
        </div>

        <div className="lg:col-span-7">
          <div className={`p-8 sm:p-10 rounded-3xl relative overflow-hidden shadow-2xl ${
            isLight ? 'hardware-chassis-light text-ls-navy' : 'hardware-chassis-dark text-ls-grey-light-text'
          }`}>
            {/* Hardware Screws */}
            <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
            <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
            <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
            <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

            {/* Console Header Bar */}
            <div className="flex items-center justify-between pb-3.5 mb-6 border-b border-ls-navy/10 dark:border-ls-white/10 px-1">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-ls-red shadow-[0_0_8px_rgba(230,57,70,0.9)]" />
                <span className="font-body text-xs font-bold tracking-wider">
                  CONVERSATION CONSOLE
                </span>
              </div>
              <AcousticVentGrille variant="strip" isLight={isLight} />
            </div>

            {contactSubmitted ? (
              <div className="py-12 text-center space-y-4">
                <div className="w-16 h-16 rounded-full bg-ls-cyan/20 text-ls-cyan border border-ls-cyan/40 flex items-center justify-center mx-auto shadow-[0_0_15px_rgba(0,191,255,0.3)]">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <h3 className={`text-2xl font-black tracking-tight ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                  Message Received
                </h3>
                <p className={`text-justify text-sm max-w-md mx-auto leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  Thank you. A human will review your message and contact you directly within two business days.
                </p>
                {referenceId ? (
                  <p className={`text-xs font-mono ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                    Reference: {referenceId}
                  </p>
                ) : null}
                <button
                  onClick={() => {
                    setContactSubmitted(false);
                    setReferenceId(null);
                    setSubmitError(null);
                    setCurrentStep(1);
                  }}
                  className="px-6 py-2.5 rounded-xl bg-ls-red text-ls-white font-bold text-xs tracking-wider cursor-pointer shadow-md hover:bg-ls-red transition-all"
                >
                  Submit Another Inquiry
                </button>
              </div>
            ) : (
              <>
                {/* 5-Step Engagement Stepper */}
                <ol className="flex flex-wrap items-center gap-1.5 mb-6" aria-label="Engagement intake progress">
                  {steps.map((step) => {
                    const isActive = step.id === currentStep;
                    const isDone = step.id < currentStep;
                    return (
                      <li key={step.key}>
                        <button
                          type="button"
                          onClick={() => goToStep(step.id)}
                          aria-current={isActive ? 'step' : undefined}
                          className={`px-2.5 py-1.5 rounded-lg text-[10px] font-body font-bold tracking-wider border transition-all cursor-pointer ${
                            isActive
                              ? 'bg-ls-red/15 border-ls-red text-ls-red'
                              : isDone
                                ? 'bg-ls-cyan/10 border-ls-cyan/40 text-ls-cyan'
                                : isLight
                                  ? 'bg-ls-grey-light/60 border-ls-grey-dark/50 text-ls-grey-dark'
                                  : 'bg-ls-navy/60 border-ls-white/15 text-ls-grey-light-text'
                          }`}
                        >
                          {step.id}. {step.key}
                        </button>
                      </li>
                    );
                  })}
                </ol>

                <div className="mb-5">
                  <p className={`text-[11px] font-body font-bold tracking-widest uppercase ${isLight ? 'text-ls-red' : 'text-ls-red'}`}>
                    Step {activeStep.id} of 5 — {activeStep.key}
                  </p>
                  <p className={`text-sm font-medium mt-1 ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                    {activeStep.description}
                  </p>
                </div>

                <form onSubmit={handleContactSubmit} className="space-y-4">
                  <input
                    type="text"
                    name="website"
                    value={honeypot}
                    onChange={(e) => setHoneypot(e.target.value)}
                    tabIndex={-1}
                    autoComplete="off"
                    aria-hidden="true"
                    className="absolute left-[-9999px] w-px h-px opacity-0"
                  />

                  {/* Step 1 — DISCOVER */}
                  {currentStep === 1 && (
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                          <label htmlFor="ct-executive-name" className={labelClass}>Executive Name *</label>
                          <input
                            id="ct-executive-name"
                            type="text"
                            required
                            placeholder="e.g. Dr. K. Mlangeni"
                            value={contactFormData.name}
                            onChange={(e) => setContactFormData({ ...contactFormData, name: e.target.value })}
                            className={fieldInputClass}
                          />
                        </div>
                        <div>
                          <label htmlFor="ct-executive-title" className={labelClass}>Executive Title *</label>
                          <input
                            id="ct-executive-title"
                            type="text"
                            required
                            placeholder="e.g. Chief Executive Officer"
                            value={contactFormData.title}
                            onChange={(e) => setContactFormData({ ...contactFormData, title: e.target.value })}
                            className={fieldInputClass}
                          />
                        </div>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                          <label htmlFor="ct-organization" className={labelClass}>Institution / Entity *</label>
                          <input
                            id="ct-organization"
                            type="text"
                            required
                            placeholder="e.g. Your Organisation"
                            value={contactFormData.organization}
                            onChange={(e) => setContactFormData({ ...contactFormData, organization: e.target.value })}
                            className={fieldInputClass}
                          />
                        </div>
                        <div>
                          <label htmlFor="ct-email" className={labelClass}>Official Email *</label>
                          <input
                            id="ct-email"
                            type="email"
                            required
                            placeholder="executive@institution.com"
                            value={contactFormData.email}
                            onChange={(e) => setContactFormData({ ...contactFormData, email: e.target.value })}
                            className={fieldInputClass}
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Step 2 — DIAGNOSE */}
                  {currentStep === 2 && (
                    <div className="space-y-4">
                      <div>
                        <label htmlFor="ct-scope" className={labelClass}>Target Engagement Model</label>
                        <select
                          id="ct-scope"
                          value={contactFormData.scope}
                          onChange={(e) => setContactFormData({ ...contactFormData, scope: e.target.value })}
                          className={fieldInputClass}
                        >
                          <option value="Advisory Architecture Sprint (2 Weeks)">Advisory Architecture Sprint (2 Weeks)</option>
                          <option value="Co-Engineered Pilot (90 Days)">Co-Engineered Pilot (90 Days)</option>
                          <option value="Enterprise Deployment">Enterprise Deployment</option>
                          <option value="Executive Boardroom Briefing">Executive Boardroom Briefing</option>
                        </select>
                      </div>
                      <div>
                        <label htmlFor="ct-objective" className={labelClass}>Strategic Objectives & Context</label>
                        <textarea
                          id="ct-objective"
                          rows={4}
                          required
                          placeholder="Describe your current bottlenecks, regulatory constraints, or legacy IT dependencies..."
                          value={contactFormData.objective}
                          onChange={(e) => setContactFormData({ ...contactFormData, objective: e.target.value })}
                          className={`${fieldInputClass} resize-none`}
                        />
                      </div>
                    </div>
                  )}

                  {/* Step 3 — DESIGN */}
                  {currentStep === 3 && (
                    <div>
                      <label htmlFor="ct-timeline" className={labelClass}>Preferred Timeline</label>
                      <select
                        id="ct-timeline"
                        value={contactFormData.timeline}
                        onChange={(e) => setContactFormData({ ...contactFormData, timeline: e.target.value })}
                        className={fieldInputClass}
                      >
                        <option value="Within 30 days">Within 30 days</option>
                        <option value="This quarter">This quarter</option>
                        <option value="Next quarter">Next quarter</option>
                        <option value="Exploring only">Exploring only</option>
                      </select>
                    </div>
                  )}

                  {/* Step 4 — BUILD (review) */}
                  {currentStep === 4 && (
                    <dl className={`space-y-3 text-xs rounded-xl border p-4 ${
                      isLight ? 'border-ls-grey-dark/50 bg-ls-grey-light/50' : 'border-ls-white/10 bg-ls-navy/60'
                    }`}>
                      {[
                        ['Name', contactFormData.name],
                        ['Title', contactFormData.title],
                        ['Institution', contactFormData.organization],
                        ['Email', contactFormData.email],
                        ['Engagement Model', contactFormData.scope],
                        ['Timeline', contactFormData.timeline],
                        ['Objectives', contactFormData.objective]
                      ].map(([label, value]) => (
                        <div key={label} className="flex flex-col sm:flex-row sm:gap-3">
                          <dt className={`font-bold tracking-wider uppercase shrink-0 sm:w-32 ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>{label}</dt>
                          <dd className={`${isLight ? 'text-ls-navy' : 'text-ls-white'} break-words`}>{value || '—'}</dd>
                        </div>
                      ))}
                    </dl>
                  )}

                  {/* Step 5 — GOVERN (submit) */}
                  {currentStep === 5 && (
                    <div className="space-y-3">
                      <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                        Submission is governed: a human reviews every enquiry, Turnstile verifies the request, and your details are used only to respond to this conversation.
                      </p>
                      {siteKey ? <div ref={containerRef} className="scale-90 origin-left" /> : null}
                    </div>
                  )}

                  {submitError && (
                    <p role="alert" className="text-sm font-medium text-ls-red">
                      {submitError}
                    </p>
                  )}

                  {/* Navigation */}
                  <div className="pt-2 space-y-3">
                    <div className="flex items-center gap-3">
                      {currentStep > 1 && (
                        <button
                          type="button"
                          onClick={prevStep}
                          className={`inline-flex items-center gap-1.5 px-5 py-3 rounded-xl font-bold text-xs tracking-wider border transition-all cursor-pointer ${
                            isLight
                              ? 'border-ls-grey-dark text-ls-navy hover:bg-ls-grey-light'
                              : 'border-ls-white/25 text-ls-white hover:bg-ls-white/5'
                          }`}
                        >
                          <ChevronLeft className="w-3.5 h-3.5" />
                          Previous
                        </button>
                      )}
                      <button
                        type="submit"
                        disabled={submitting || (currentStep < 5 && !canAdvance())}
                        className="flex-1 py-3.5 rounded-xl bg-ls-red text-ls-white font-bold text-xs tracking-widest transition-all flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-ls-red/25 active:scale-98 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {currentStep < 5 ? (
                          <>
                            <span>Next Step</span>
                            <ChevronRight className="w-3.5 h-3.5" />
                          </>
                        ) : (
                          <>
                            <span>{submitting ? 'Sending…' : 'Send — Start the Conversation'}</span>
                            <Send className="w-3.5 h-3.5" />
                          </>
                        )}
                      </button>
                    </div>
                    <p className={`text-xs font-medium ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                      {ENQUIRY_SLA_COPY}
                    </p>
                    {whatsappNumber ? (
                      <a
                        href={`https://wa.me/${whatsappNumber}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs font-bold text-ls-cyan inline-flex items-center gap-1.5 hover:underline"
                      >
                        <MessageCircle className="w-3.5 h-3.5" />
                        Prefer WhatsApp? Chat to us.
                      </a>
                    ) : null}
                  </div>
                </form>
              </>
            )}
          </div>
        </div>

      </div>
    </section>
  );
};
