import React, { useCallback, useState, useEffect } from 'react';
import { X, Shield, Send, CheckCircle2, ArrowRight, Building2, User, Mail, Phone, Calendar, MessageCircle } from 'lucide-react';
import { useTurnstile } from '../hooks/useTurnstile';
import { ENQUIRY_SLA_COPY, ENQUIRY_GENERIC_ERROR, enquiryPayload } from '../lib/enquiry';
import { Icon3D } from './common';

interface ExecutiveBriefingModalProps {
  isOpen: boolean;
  onClose: () => void;
  prefillSummary?: string;
  theme?: 'light' | 'dark';
}

export const ExecutiveBriefingModal: React.FC<ExecutiveBriefingModalProps> = ({
  isOpen,
  onClose,
  prefillSummary = '',
  theme = 'dark'
}) => {
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [honeypot, setHoneypot] = useState('');
  const [turnstileToken, setTurnstileToken] = useState<string | null>(null);
  const { containerRef, siteKey, reset } = useTurnstile(
    'briefing',
    useCallback((token: string) => setTurnstileToken(token), [])
  );
  const whatsappNumber = import.meta.env.VITE_WHATSAPP_NUMBER as string | undefined;
  const [formData, setFormData] = useState({
    fullName: '',
    executiveTitle: '',
    organization: '',
    email: '',
    phone: '',
    scope: 'Advisory Architecture Sprint (2 Weeks)',
    timeframe: 'Immediate (Next 30 Days)',
    notes: prefillSummary
  });

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting) return;
    setSubmitting(true);
    setSubmitError(null);
    try {
      const res = await fetch('/api/enquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
          enquiryPayload(
            {
              form: 'briefing',
              name: formData.fullName,
              organization: formData.organization,
              email: formData.email,
              enquiryType: 'Executive boardroom briefing',
              message: formData.notes || `${formData.scope}: ${formData.timeframe}`,
              phone: formData.phone
            },
            turnstileToken,
            honeypot
          )
        )
      });
      if (res.status === 201) {
        setSubmitted(true);
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

  const isLight = theme === 'light';

  return (
    <div className="fixed inset-0 z-[1000] flex items-center justify-center p-3 sm:p-6 pt-16 sm:pt-20 bg-[#070A40]/80 backdrop-blur-md animate-in fade-in overflow-y-auto">
      <div
        className={`relative w-full max-w-2xl border-2 border-ls-cyan shadow-[8px_8px_0px_#070A40] overflow-hidden max-h-[90vh] flex flex-col ${
          isLight
            ? 'bg-ls-white text-ls-navy'
            : 'bg-[#070A40] text-ls-white'
        }`}
      >
        {/* Modal Header */}
        <div className={`flex items-center justify-between p-6 shrink-0 relative z-10 border-b border-white/10 ${
          isLight ? 'bg-ls-grey-light' : 'bg-[#05072B]'
        }`}>
          <div className="flex items-center gap-3">
            <div className="flex items-center shrink-0">
              <Icon3D name="security" size="sm" isInteractive />
            </div>
            <div>
              <div className={`text-sm font-bold tracking-widest font-sans ${
                isLight ? 'text-ls-navy' : 'text-ls-white'
              }`}>
                LightSpeed Holdings
              </div>
              <div className={`text-[11px] font-sans font-medium ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                Confidential Executive Advisory Briefing Request
              </div>
            </div>
          </div>

          <button
            onClick={onClose}
            type="button"
            aria-label="Close modal"
            title="Close modal"
            className={`w-9 h-9 border border-white/20 flex items-center justify-center transition-colors cursor-pointer shrink-0 ${
              isLight
                ? 'bg-ls-white text-ls-grey-dark hover:bg-ls-red hover:text-white'
                : 'bg-white/5 text-white hover:bg-ls-red hover:text-white'
            }`}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6">
          {submitted ? (
            <div className="py-12 text-center space-y-4">
              <div className="flex items-center justify-center mx-auto mb-2">
                <Icon3D name="verification" size="hero" isInteractive />
              </div>
              <h3 className={`text-2xl font-black tracking-tight ${
                isLight ? 'text-ls-navy' : 'text-ls-white'
              }`}>
                Briefing Requested Successfully
              </h3>
              <p className={`text-justify text-sm max-w-md mx-auto leading-relaxed ${
                isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
              }`}>
                Our Senior Managing Partners have received your confidential inquiry. We will contact you within two business days to schedule an executive diagnostic session.
              </p>
              <div className="pt-4">
                <button
                  onClick={() => {
                    setSubmitted(false);
                    setSubmitError(null);
                    onClose();
                  }}
                  className="btn-milled btn-milled-primary px-7 py-3 rounded-full font-bold text-xs tracking-widest cursor-pointer"
                >
                  Return to Platform
                </button>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
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
              {siteKey ? <div ref={containerRef} className="scale-90 origin-left" /> : null}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className={`block text-[11px] font-body tracking-wider mb-1 font-bold ${
                    isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
                  }`}>
                    Executive Name *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Dr. K. Mlangeni"
                    value={formData.fullName}
                    onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl text-xs outline-none focus:ring-1 focus:ring-ls-red transition-all font-medium ${
                      isLight
                        ? 'bg-ls-grey-light text-ls-navy placeholder:text-ls-grey-dark shadow-inner'
                        : 'bg-ls-navy text-ls-white placeholder:text-ls-grey-light-text shadow-inner'
                    }`}
                  />
                </div>

                <div>
                  <label className={`block text-[11px] font-body tracking-wider mb-1 font-bold ${
                    isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
                  }`}>
                    Executive Title *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Managing Director / Chief Information Officer"
                    value={formData.executiveTitle}
                    onChange={(e) => setFormData({ ...formData, executiveTitle: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl text-xs outline-none focus:ring-1 focus:ring-ls-red transition-all font-medium ${
                      isLight
                        ? 'bg-ls-grey-light text-ls-navy placeholder:text-ls-grey-dark shadow-inner'
                        : 'bg-ls-navy text-ls-white placeholder:text-ls-grey-light-text shadow-inner'
                    }`}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className={`block text-[11px] font-body tracking-wider mb-1 font-bold ${
                    isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
                  }`}>
                    Institutional Entity *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Reserve Bank / Standard Bank / Revenue Authority"
                    value={formData.organization}
                    onChange={(e) => setFormData({ ...formData, organization: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl text-xs outline-none focus:ring-1 focus:ring-ls-red transition-all font-medium ${
                      isLight
                        ? 'bg-ls-grey-light text-ls-navy placeholder:text-ls-grey-dark shadow-inner'
                        : 'bg-ls-navy text-ls-white placeholder:text-ls-grey-light-text shadow-inner'
                    }`}
                  />
                </div>

                <div>
                  <label className={`block text-[11px] font-body tracking-wider mb-1 font-bold ${
                    isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
                  }`}>
                    Work Email *
                  </label>
                  <input
                    type="email"
                    required
                    placeholder="name@institution.com"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl text-xs outline-none focus:ring-1 focus:ring-ls-red transition-all font-medium ${
                      isLight
                        ? 'bg-ls-grey-light text-ls-navy placeholder:text-ls-grey-dark shadow-inner'
                        : 'bg-ls-navy text-ls-white placeholder:text-ls-grey-light-text shadow-inner'
                    }`}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className={`block text-[11px] font-body tracking-wider mb-1 font-bold ${
                    isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
                  }`}>
                    Direct Contact Number
                  </label>
                  <input
                    type="tel"
                    placeholder="+265 ... / +27 ..."
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl text-xs outline-none focus:ring-1 focus:ring-ls-red transition-all font-medium ${
                      isLight
                        ? 'bg-ls-grey-light text-ls-navy placeholder:text-ls-grey-dark shadow-inner'
                        : 'bg-ls-navy text-ls-white placeholder:text-ls-grey-light-text shadow-inner'
                    }`}
                  />
                </div>

                <div>
                  <label className={`block text-[11px] font-body tracking-wider mb-1 font-bold ${
                    isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
                  }`}>
                    Target Engagement Scope
                  </label>
                  <select
                    value={formData.scope}
                    onChange={(e) => setFormData({ ...formData, scope: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl text-xs outline-none focus:ring-1 focus:ring-ls-red transition-all font-medium ${
                      isLight
                        ? 'bg-ls-grey-light text-ls-navy shadow-inner'
                        : 'bg-ls-navy text-ls-white shadow-inner'
                    }`}
                  >
                    <option value="Advisory Architecture Sprint (2 Weeks)">Advisory Architecture Sprint (2 Weeks)</option>
                    <option value="Co-Engineered Pilot (90 Days)">Co-Engineered Pilot (90 Days)</option>
                    <option value="Full Sovereign Enterprise Deployment">Full Sovereign Enterprise Deployment</option>
                    <option value="Boardroom Strategy Keynote / Briefing">Boardroom Strategy Keynote / Briefing</option>
                  </select>
                </div>
              </div>

              <div>
                <label className={`block text-[11px] font-body tracking-wider mb-1 font-bold ${
                  isLight ? 'text-ls-navy' : 'text-ls-grey-light-text'
                }`}>
                  Strategic Scope & Context
                </label>
                <textarea
                  rows={3}
                  placeholder="Outline your primary strategic bottlenecks, legacy IT dependencies, or compliance requirements..."
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  className={`w-full px-3.5 py-2.5 rounded-xl text-xs outline-none focus:ring-1 focus:ring-ls-red transition-all resize-none font-medium ${
                    isLight
                      ? 'bg-ls-grey-light text-ls-navy placeholder:text-ls-grey-dark shadow-inner'
                      : 'bg-ls-navy text-ls-white placeholder:text-ls-grey-light-text shadow-inner'
                  }`}
                />
              </div>

              {submitError && (
                <p role="alert" className="text-sm font-medium text-ls-red/85">
                  {submitError}
                </p>
              )}
              <div className="pt-2 flex items-center justify-between flex-wrap gap-3">
                <div className="space-y-1">
                  <div className={`text-[10px] font-body font-bold ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}>
                    Guaranteed confidentiality • Fiduciary NDA standard
                  </div>
                  <div className={`text-[10px] font-medium ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                    {ENQUIRY_SLA_COPY}
                  </div>
                  {whatsappNumber ? (
                    <a
                      href={`https://wa.me/${whatsappNumber}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-[10px] font-bold text-ls-cyan inline-flex items-center gap-1 hover:underline"
                    >
                      <MessageCircle className="w-3 h-3" />
                      Prefer WhatsApp? Chat to us.
                    </a>
                  ) : null}
                </div>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-8 py-3.5 font-bold text-xs tracking-widest transition-colors flex items-center gap-2.5 cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed shrink-0 bg-ls-red hover:bg-white hover:text-ls-navy text-white border border-ls-red hover:border-white shadow-[4px_4px_0px_#070A40] uppercase font-sans"
                >
                  <span>{submitting ? 'Sending…' : 'Submit Confidential Request'}</span>
                  <Send className="w-3.5 h-3.5" />
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
