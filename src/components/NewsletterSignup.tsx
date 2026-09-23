import React, { useCallback, useState } from 'react';
import { Send, CheckCircle2, Mail } from 'lucide-react';
import { useTurnstile } from '../hooks/useTurnstile';
import { ENQUIRY_GENERIC_ERROR, enquiryPayload } from '../lib/enquiry';

interface NewsletterSignupProps {
  theme: 'light' | 'dark';
  id?: string;
}

/**
 * Newsletter lead capture. Posts to /api/enquiry with form: contact and
 * enquiryType: Newsletter subscription so the edge Turnstile action stays
 * within EXPECTED_ACTIONS (contact | briefing).
 */
export const NewsletterSignup: React.FC<NewsletterSignupProps> = ({ theme, id }) => {
  const isLight = theme === 'light';
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [honeypot, setHoneypot] = useState('');
  const [turnstileToken, setTurnstileToken] = useState<string | null>(null);
  const [formData, setFormData] = useState({ name: '', email: '' });
  const { containerRef, siteKey, reset } = useTurnstile(
    'contact',
    useCallback((token: string) => setTurnstileToken(token), [])
  );

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
              form: 'contact',
              name: formData.name,
              organization: 'Newsletter subscriber',
              email: formData.email,
              enquiryType: 'Newsletter subscription',
              message: 'Opted in to LightSpeed newsletter updates.'
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

  if (submitted) {
    return (
      <section
        id={id}
        aria-labelledby={id ? `${id}-heading` : undefined}
        className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-10 ${
          isLight ? 'text-ls-navy' : 'text-ls-white'
        }`}
      >
        <div
          className={`rounded-3xl border p-6 sm:p-8 flex items-start gap-4 ${
            isLight ? 'bg-ls-cyan/10 border-ls-cyan/40' : 'bg-ls-cyan/10 border-ls-cyan/30'
          }`}
        >
          <CheckCircle2 className="w-6 h-6 text-ls-cyan shrink-0" aria-hidden="true" />
          <div>
            <h2
              id={id ? `${id}-heading` : undefined}
              className="font-display font-bold text-lg sm:text-xl"
            >
              You are on the list
            </h2>
            <p className={`mt-1 text-sm ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              We will send evidence-led updates on agentic AI governance and AI-native transformation.
              No noise.
            </p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section
      id={id}
      aria-labelledby={id ? `${id}-heading` : undefined}
      className={`px-4 sm:px-8 max-w-7xl mx-auto w-full py-10 border-t ${
        isLight ? 'border-ls-grey-dark/40 text-ls-navy' : 'border-ls-white/10 text-ls-white'
      }`}
    >
      <div className="rounded-3xl border p-6 sm:p-10 bg-ls-navy text-ls-white border-ls-white/15 shadow-xl">
        <div className="max-w-2xl mx-auto text-center space-y-5">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-body text-[11px] tracking-widest font-bold">
            <Mail className="w-3.5 h-3.5" aria-hidden="true" />
            <span>NEWSLETTER</span>
          </div>
          <h2 id={id ? `${id}-heading` : undefined} className="text-2xl sm:text-3xl font-black tracking-tight font-display">
            Stay Ahead of the Canon
          </h2>
          <p className="text-sm sm:text-base leading-relaxed text-ls-grey-light-text">
            Research notes, governance frameworks, and operating updates — written for boards, not engineers.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4 text-left max-w-lg mx-auto">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <label className="block">
                <span className="block text-[11px] font-bold tracking-widest text-ls-grey-light-text mb-1.5">
                  NAME
                </span>
                <input
                  type="text"
                  required
                  autoComplete="name"
                  value={formData.name}
                  onChange={(e) => setFormData((f) => ({ ...f, name: e.target.value }))}
                  className="w-full rounded-xl border border-ls-white/20 bg-ls-white/5 px-4 py-3 text-sm text-ls-white placeholder:text-ls-grey-light-text/70 focus:outline-none focus:border-ls-cyan"
                  placeholder="Your name"
                />
              </label>
              <label className="block">
                <span className="block text-[11px] font-bold tracking-widest text-ls-grey-light-text mb-1.5">
                  EMAIL
                </span>
                <input
                  type="email"
                  required
                  autoComplete="email"
                  value={formData.email}
                  onChange={(e) => setFormData((f) => ({ ...f, email: e.target.value }))}
                  className="w-full rounded-xl border border-ls-white/20 bg-ls-white/5 px-4 py-3 text-sm text-ls-white placeholder:text-ls-grey-light-text/70 focus:outline-none focus:border-ls-cyan"
                  placeholder="you@company.com"
                />
              </label>
            </div>

            <div className="sr-only" aria-hidden="true">
              <label>
                Website
                <input
                  type="text"
                  tabIndex={-1}
                  autoComplete="off"
                  value={honeypot}
                  onChange={(e) => setHoneypot(e.target.value)}
                />
              </label>
            </div>
            <div ref={containerRef} className="hidden" />

            {submitError && (
              <p role="alert" className="text-xs text-ls-red font-medium">
                {submitError}
              </p>
            )}

            <button
              type="submit"
              disabled={submitting || Boolean(siteKey && !turnstileToken)}
              className="inline-flex w-full items-center justify-center gap-2.5 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? 'Subscribing…' : 'Subscribe'}
              <Send className="w-3.5 h-3.5" aria-hidden="true" />
            </button>
            <p className="text-center text-[11px] text-ls-grey-light-text">
              We respond to qualified enquiries within two business days. Unsubscribe anytime.
            </p>
          </form>
        </div>
      </div>
    </section>
  );
};

export default NewsletterSignup;
