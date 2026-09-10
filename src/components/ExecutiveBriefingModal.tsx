import React, { useState, useEffect } from 'react';
import { X, Shield, Send, CheckCircle2, ArrowRight, Building2, User, Mail, Phone, Calendar } from 'lucide-react';

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => {
      // Keep feedback visible
    }, 500);
  };

  const isLight = theme === 'light';

  return (
    <div className="fixed inset-0 z-[1000] flex items-center justify-center p-3 sm:p-6 pt-16 sm:pt-20 bg-black/80 backdrop-blur-md animate-in fade-in overflow-y-auto">
      <div 
        className={`relative w-full max-w-2xl rounded-3xl border shadow-2xl overflow-hidden max-h-[90vh] flex flex-col ${
          isLight 
            ? 'bg-white text-slate-900 border-slate-300' 
            : 'bg-zinc-950 text-zinc-100 border-white/15'
        }`}
      >
        {/* Modal Header */}
        <div className={`flex items-center justify-between p-6 border-b shrink-0 relative z-10 ${
          isLight ? 'border-slate-200 bg-slate-50/80' : 'border-white/10 bg-zinc-900/60'
        }`}>
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-orange-500 to-amber-500 flex items-center justify-center text-white shadow-xs">
              <Shield className="w-4 h-4" />
            </div>
            <div>
              <div className={`text-sm font-black tracking-widest font-mono ${
                isLight ? 'text-slate-900' : 'text-white'
              }`}>
                LIGHTSPEED HOLDINGS
              </div>
              <div className={`text-[11px] font-mono font-medium ${
                isLight ? 'text-slate-700' : 'text-zinc-400'
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
            className={`relative z-50 p-2 rounded-full transition-all cursor-pointer border shrink-0 ${
              isLight 
                ? 'hover:bg-slate-200 text-slate-700 hover:text-slate-900 border-slate-300 bg-white shadow-xs' 
                : 'hover:bg-white/20 text-zinc-300 hover:text-white border-white/20 bg-zinc-900/80 shadow-md'
            }`}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6">
          {submitted ? (
            <div className="py-12 text-center space-y-4">
              <div className="w-16 h-16 rounded-full bg-orange-500/20 text-orange-500 border border-orange-500/40 flex items-center justify-center mx-auto">
                <CheckCircle2 className="w-8 h-8" />
              </div>
              <h3 className={`text-2xl font-black tracking-tight ${
                isLight ? 'text-slate-900' : 'text-white'
              }`}>
                Briefing Requested Successfully
              </h3>
              <p className={`text-justify text-sm max-w-md mx-auto leading-relaxed ${
                isLight ? 'text-slate-800' : 'text-zinc-300'
              }`}>
                Our Senior Managing Partners have received your confidential inquiry. We will contact you within 12 business hours to schedule an executive diagnostic session.
              </p>
              <div className="pt-4">
                <button
                  onClick={() => {
                    setSubmitted(false);
                    onClose();
                  }}
                  className="px-6 py-2.5 rounded-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs tracking-widest cursor-pointer shadow-md shadow-orange-500/25"
                >
                  Return to Platform
                </button>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${
                    isLight ? 'text-slate-800' : 'text-zinc-300'
                  }`}>
                    Executive Name *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Dr. K. Mlangeni"
                    value={formData.fullName}
                    onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                      isLight 
                        ? 'border-slate-300 bg-slate-100 text-slate-900 placeholder:text-slate-500 shadow-inner' 
                        : 'border-white/20 bg-zinc-900 text-white placeholder:text-zinc-400 shadow-inner'
                    }`}
                  />
                </div>

                <div>
                  <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${
                    isLight ? 'text-slate-800' : 'text-zinc-300'
                  }`}>
                    Executive Title *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Managing Director / Chief Information Officer"
                    value={formData.executiveTitle}
                    onChange={(e) => setFormData({ ...formData, executiveTitle: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                      isLight 
                        ? 'border-slate-300 bg-slate-100 text-slate-900 placeholder:text-slate-500 shadow-inner' 
                        : 'border-white/20 bg-zinc-900 text-white placeholder:text-zinc-400 shadow-inner'
                    }`}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${
                    isLight ? 'text-slate-800' : 'text-zinc-300'
                  }`}>
                    Institutional Entity *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Reserve Bank / Standard Bank / Revenue Authority"
                    value={formData.organization}
                    onChange={(e) => setFormData({ ...formData, organization: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                      isLight 
                        ? 'border-slate-300 bg-slate-100 text-slate-900 placeholder:text-slate-500 shadow-inner' 
                        : 'border-white/20 bg-zinc-900 text-white placeholder:text-zinc-400 shadow-inner'
                    }`}
                  />
                </div>

                <div>
                  <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${
                    isLight ? 'text-slate-800' : 'text-zinc-300'
                  }`}>
                    Work Email *
                  </label>
                  <input
                    type="email"
                    required
                    placeholder="name@institution.com"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                      isLight 
                        ? 'border-slate-300 bg-slate-100 text-slate-900 placeholder:text-slate-500 shadow-inner' 
                        : 'border-white/20 bg-zinc-900 text-white placeholder:text-zinc-400 shadow-inner'
                    }`}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${
                    isLight ? 'text-slate-800' : 'text-zinc-300'
                  }`}>
                    Direct Contact Number
                  </label>
                  <input
                    type="tel"
                    placeholder="+265 ... / +27 ..."
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                      isLight 
                        ? 'border-slate-300 bg-slate-100 text-slate-900 placeholder:text-slate-500 shadow-inner' 
                        : 'border-white/20 bg-zinc-900 text-white placeholder:text-zinc-400 shadow-inner'
                    }`}
                  />
                </div>

                <div>
                  <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${
                    isLight ? 'text-slate-800' : 'text-zinc-300'
                  }`}>
                    Target Engagement Scope
                  </label>
                  <select
                    value={formData.scope}
                    onChange={(e) => setFormData({ ...formData, scope: e.target.value })}
                    className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                      isLight 
                        ? 'border-slate-300 bg-slate-100 text-slate-900 shadow-inner' 
                        : 'border-white/20 bg-zinc-900 text-white shadow-inner'
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
                <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${
                  isLight ? 'text-slate-800' : 'text-zinc-300'
                }`}>
                  Strategic Scope & Context
                </label>
                <textarea
                  rows={3}
                  placeholder="Outline your primary strategic bottlenecks, legacy IT dependencies, or compliance requirements..."
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors resize-none font-medium ${
                    isLight 
                      ? 'border-slate-300 bg-slate-100 text-slate-900 placeholder:text-slate-500 shadow-inner' 
                      : 'border-white/20 bg-zinc-900 text-white placeholder:text-zinc-400 shadow-inner'
                  }`}
                />
              </div>

              <div className="pt-2 flex items-center justify-between">
                <div className={`text-[10px] font-mono font-bold ${
                  isLight ? 'text-slate-700' : 'text-zinc-400'
                }`}>
                  Guaranteed confidentiality • Fiduciary NDA standard
                </div>
                <button
                  type="submit"
                  className="px-6 py-3 rounded-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs tracking-widest transition-all flex items-center gap-2 cursor-pointer shadow-md shadow-orange-500/20"
                >
                  <span>Submit Confidential Request</span>
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
