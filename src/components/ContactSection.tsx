import React, { useCallback, useRef, useState } from 'react';
import { ShieldCheck, Clock, Globe2, Send, CheckCircle2, MessageCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import { useTurnstile } from '../hooks/useTurnstile';
import { ENQUIRY_SLA_COPY, ENQUIRY_GENERIC_ERROR, enquiryErrorMessage, enquiryPayload } from '../lib/enquiry';
import { trackJourneyEvent } from '../hooks/useJourneyEvents';

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
  { id: 1, key: 'DISCOVER', name: 'Discover', description: 'Tell us who you are and where your organisation stands today.' },
  { id: 2, key: 'DIAGNOSE', name: 'Diagnose', description: 'Choose the engagement model and describe the constraints you want us to examine.' },
  { id: 3, key: 'DESIGN', name: 'Design', description: 'Set your timeline so we can propose a realistic starting point.' },
  { id: 4, key: 'BUILD', name: 'Build', description: 'Review your entries before we prepare your brief.' },
  { id: 5, key: 'GOVERN', name: 'Govern', description: 'Confirm your request. A person reviews every enquiry before we respond.' }
];

export const ContactSection: React.FC<ContactSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const [contactSubmitted, setContactSubmitted] = useState<boolean>(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [referenceId, setReferenceId] = useState<string | null>(null);
  const [honeypot, setHoneypot] = useState('');
  const [currentStep, setCurrentStep] = useState(1);
  const startedRef = useRef(false);
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
    scope: '',
    objective: '',
    timeline: ''
  });

  const goToStep = (step: number) => {
    if (step >= 1 && step <= steps.length) setCurrentStep(step);
  };
  const nextStep = () => goToStep(currentStep + 1);
  const prevStep = () => goToStep(currentStep - 1);

  const canAdvance = (): boolean => {
    switch (currentStep) {
      case 1:
        return Boolean(contactFormData.name && contactFormData.organization && contactFormData.email);
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
      if (canAdvance()) {
        if (currentStep === 1 && !startedRef.current) {
          startedRef.current = true;
          trackJourneyEvent({ eventType: 'contact_started', journeyStage: 'conversion' });
        }
        nextStep();
      }
      return;
    }
    if (!startedRef.current) {
      startedRef.current = true;
      trackJourneyEvent({ eventType: 'contact_started', journeyStage: 'conversion' });
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
              message: contactFormData.objective,
              title: contactFormData.title,
              timeline: contactFormData.timeline
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
        trackJourneyEvent({ eventType: 'contact_completed', journeyStage: 'conversion' });
      } else {
        const data = (await res.json().catch(() => null)) as {
          error?: { code?: string; message?: string };
        } | null;
        setSubmitError(data?.error?.message ?? enquiryErrorMessage(data?.error?.code));
      }
    } catch {
      setSubmitError(ENQUIRY_GENERIC_ERROR);
    } finally {
      setSubmitting(false);
      reset();
    }
  };

  const activeStep = steps[currentStep - 1];

  const fieldInputClass = `w-full px-3.5 py-2.5 rounded-xl text-xs outline-none focus:ring-1 focus:ring-ls-red transition-all font-medium ${
    isLight
      ? 'bg-ls-grey-light/90 text-ls-navy placeholder:text-ls-navy/50 shadow-inner'
      : 'bg-ls-navy text-ls-white placeholder:text-ls-white/50 shadow-inner'
  }`;
  const labelClass = `block text-[11px] font-body tracking-wider mb-1 font-bold ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`;

  return (
    <section id="contact" className={`py-24 px-6 lg:px-12 max-w-7xl mx-auto w-full ${
      isLight ? 'text-ls-navy' : 'text-ls-white'
    }`}>
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">

        <div className="lg:col-span-5 space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-ls-red/10 text-ls-red font-body text-[11px] tracking-widest font-bold">
            <span>CONTACT</span>
          </div>
          <h1 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-ls-navy' : 'text-ls-white'
          }`}>
            Start the Conversation
          </h1>
          <p className={`text-left text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
          }`}>
            Tell us where your organisation stands today. We will tell you whether we can help and what you need to start.
          </p>

          <div className="space-y-4 pt-4">
            <div className={`inline-flex items-center gap-3 text-xs font-medium ${isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'}`}>
              <Clock className="w-4 h-4 text-ls-red shrink-0" />
              <span>{ENQUIRY_SLA_COPY}</span>
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
            <div className="flex items-center justify-between pb-3.5 mb-6 px-1">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-ls-red shadow-[0_0_8px_rgba(230,57,70,0.9)]" />
                <span className="font-body text-xs font-bold tracking-wider">
                  CONVERSATION CONSOLE
                </span>
              </div>
            </div>

            {contactSubmitted ? (
              <div className="py-12 text-center space-y-4">
                <div className="w-16 h-16 rounded-full bg-ls-cyan/20 text-ls-cyan flex items-center justify-center mx-auto shadow-[0_0_15px_rgba(0,191,255,0.3)]">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <h3 className={`text-2xl font-black tracking-tight ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                  Inquiry Received
                </h3>
                <p className={`text-left text-sm max-w-md mx-auto leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  We have securely routed your message to the LightSpeed Holdings executive team. A person will review it and respond within two business days to arrange a confidential briefing.
                </p>
                {referenceId ? (
                  <p className={`text-xs font-mono ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                    Reference: {referenceId}
                  </p>
                ) : null}
                <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
                  <a
                    href="/"
                    className="btn-milled btn-milled-primary px-6 py-2.5 rounded-xl bg-ls-red text-ls-white font-bold text-xs tracking-wider cursor-pointer shadow-md hover:bg-ls-red/90 transition-all"
                  >
                    Back to Home
                  </a>
                  <a
                    href="/contact"
                    onClick={(e) => {
                      e.preventDefault();
                      setContactSubmitted(false);
                      setReferenceId(null);
                      setSubmitError(null);
                      setCurrentStep(1);
                    }}
                    className={`btn-milled btn-milled-secondary px-6 py-2.5 rounded-xl font-bold text-xs tracking-wider cursor-pointer transition-all ${
                      isLight ? 'text-ls-navy hover:bg-ls-grey-light' : 'text-ls-white hover:bg-ls-white/10'
                    }`}
                  >
                    Book a Consultation Call
                  </a>
                </div>
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
                          className={`btn-milled ${isActive ? 'btn-milled-primary' : 'btn-milled-secondary'} px-2.5 py-1.5 rounded-lg text-[10px] font-body font-bold tracking-wider transition-all cursor-pointer ${
                            isActive
                              ? 'bg-ls-red/15 text-ls-red'
                              : isDone
                                ? 'bg-ls-cyan/10 text-ls-cyan'
                                : isLight
                                  ? 'bg-ls-grey-light/60 text-ls-grey-dark'
                                  : 'bg-ls-navy/60 text-ls-grey-light-text'
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
                    Step {activeStep.id} of 5: {activeStep.key}
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
                    className="absolute left-[-9999px] w-px h-px opacity-0 hidden"
                  />

                  {/* Step 1: DISCOVER */}
                  {currentStep === 1 && (
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                          <label htmlFor="ct-full-name" className={labelClass}>Full Name *</label>
                          <input
                            id="ct-full-name"
                            type="text"
                            required
                            placeholder="Jane Mbewe"
                            value={contactFormData.name}
                            onChange={(e) => setContactFormData({ ...contactFormData, name: e.target.value })}
                            className={fieldInputClass}
                          />
                        </div>
                        <div>
                          <label htmlFor="ct-title" className={labelClass}>Title</label>
                          <input
                            id="ct-title"
                            type="text"
                            placeholder="Director of Operations"
                            value={contactFormData.title}
                            onChange={(e) => setContactFormData({ ...contactFormData, title: e.target.value })}
                            className={fieldInputClass}
                          />
                        </div>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                          <label htmlFor="ct-organization" className={labelClass}>Institution / Company *</label>
                          <input
                            id="ct-organization"
                            type="text"
                            required
                            placeholder="LightSpeed Holdings"
                            value={contactFormData.organization}
                            onChange={(e) => setContactFormData({ ...contactFormData, organization: e.target.value })}
                            className={fieldInputClass}
                          />
                        </div>
                        <div>
                          <label htmlFor="ct-email" className={labelClass}>Work Email *</label>
                          <input
                            id="ct-email"
                            type="email"
                            required
                            placeholder="you@company.com"
                            value={contactFormData.email}
                            onChange={(e) => setContactFormData({ ...contactFormData, email: e.target.value })}
                            className={fieldInputClass}
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Step 2: DIAGNOSE */}
                  {currentStep === 2 && (
                    <div className="space-y-4">
                      <div>
                        <label htmlFor="ct-scope" className={labelClass}>Primary Engagement Model *</label>
                        <select
                          id="ct-scope"
                          required
                          value={contactFormData.scope}
                          onChange={(e) => setContactFormData({ ...contactFormData, scope: e.target.value })}
                          className={fieldInputClass}
                        >
                          <option value="">Select a model...</option>
                          <option value="AI-Native Company Building">AI-Native Company Building</option>
                          <option value="Intelligent Workflow Automation">Intelligent Workflow Automation</option>
                          <option value="Agentic Systems & Orchestration">Agentic Systems & Orchestration</option>
                          <option value="Enterprise AI Integration">Enterprise AI Integration</option>
                          <option value="Organizational Memory & Knowledge">Organizational Memory & Knowledge</option>
                          <option value="AI Governance & Decision Infrastructure">AI Governance & Decision Infrastructure</option>
                          <option value="AI Readiness Assessment">AI Readiness Assessment</option>
                          <option value="Other / Not sure yet">Other / Not sure yet</option>
                        </select>
                      </div>
                      <div>
                        <label htmlFor="ct-objective" className={labelClass}>Strategic Objective & Friction Points *</label>
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

                  {/* Step 3: DESIGN */}
                  {currentStep === 3 && (
                    <div>
                      <label htmlFor="ct-timeline" className={labelClass}>Estimated Deployment Timeline</label>
                      <select
                        id="ct-timeline"
                        value={contactFormData.timeline}
                        onChange={(e) => setContactFormData({ ...contactFormData, timeline: e.target.value })}
                        className={fieldInputClass}
                      >
                        <option value="">Select timeline...</option>
                        <option value="Immediate (0-30 days)">Immediate (0-30 days)</option>
                        <option value="Short-term (1-3 months)">Short-term (1-3 months)</option>
                        <option value="Medium-term (3-6 months)">Medium-term (3-6 months)</option>
                        <option value="Long-term (6-12 months)">Long-term (6-12 months)</option>
                        <option value="Exploratory / No fixed date">Exploratory / No fixed date</option>
                      </select>
                    </div>
                  )}

                  {/* Step 4: BUILD (review) */}
                  {currentStep === 4 && (
                    <dl className={`space-y-3 text-xs rounded-xl p-4 ${
                      isLight ? 'bg-ls-grey-light/50' : 'bg-ls-navy/60'
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
                          <dd className={`${isLight ? 'text-ls-navy' : 'text-ls-white'} break-words`}>{value || '–'}</dd>
                        </div>
                      ))}
                    </dl>
                  )}

                  {/* Step 5: GOVERN (submit) */}
                  {currentStep === 5 && (
                    <div className="space-y-3">
                      <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                        A person reviews every enquiry. Turnstile verifies the request. We use your details only to respond to this conversation.
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
                          className={`btn-milled btn-milled-secondary inline-flex items-center gap-1.5 px-5 py-3 rounded-xl font-bold text-xs tracking-wider transition-all cursor-pointer ${
                            isLight
                              ? 'text-ls-navy hover:bg-ls-grey-light'
                              : 'text-ls-white hover:bg-ls-white/5'
                          }`}
                        >
                          <ChevronLeft className="w-3.5 h-3.5" />
                          Previous
                        </button>
                      )}
                      <button
                        type="submit"
                        disabled={submitting || (currentStep < 5 && !canAdvance())}
                        className="btn-milled btn-milled-primary flex-1 py-3.5 rounded-xl bg-ls-red text-ls-white font-bold text-xs tracking-widest transition-all flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-ls-red/25 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {currentStep < 5 ? (
                          <>
                            <span>Continue: {steps[currentStep].name}</span>
                            <ChevronRight className="w-3.5 h-3.5" />
                          </>
                        ) : (
                          <>
                            <span>{submitting ? 'Sending…' : 'Send: Start the Conversation'}</span>
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
