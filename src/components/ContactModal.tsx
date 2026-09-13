import React, { useState } from 'react';
import { X, Send, CheckCircle2, Sparkles, Building2, ShieldCheck, Mail, User, Globe2 } from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille 
} from './TactileHardwareElements';

interface ContactModalProps {
  isOpen: boolean;
  onClose: () => void;
  prefilledIntent?: string;
  prefilledSummary?: string;
  theme?: 'light' | 'dark';
}

export const ContactModal: React.FC<ContactModalProps> = ({
  isOpen,
  onClose,
  prefilledIntent = 'Start a Conversation',
  prefilledSummary = '',
  theme = 'dark'
}) => {
  if (!isOpen) return null;

  const isLight = theme === 'light';

  const [intent, setIntent] = useState<string>(prefilledIntent);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    organization: '',
    role: '',
    timeline: 'Within 30 Days',
    notes: prefilledSummary
  });
  const [submitted, setSubmitted] = useState<boolean>(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in font-sans">
      <div className={`relative w-full max-w-xl rounded-3xl border p-6 sm:p-8 shadow-2xl max-h-[90vh] overflow-y-auto transition-all ${
        isLight
          ? 'chassis-milled-light text-slate-900 shadow-slate-400/50'
          : 'chassis-milled-dark text-zinc-100 shadow-black/80'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className={`absolute top-4 right-8 p-1.5 rounded-lg border transition-all ${
            isLight
              ? 'flight-deck-well-light hover:border-slate-400 text-slate-700'
              : 'flight-deck-well-dark hover:border-zinc-600 text-zinc-300'
          }`}
        >
          <X className="w-4 h-4" />
        </button>

        {!submitted ? (
          <div>
            <div className="mb-6 pt-1">
              <div className="flex items-center gap-2 mb-2">
                <StatusLedPip status="emerald" isLight={isLight} />
                <span className="text-[10px] font-mono font-extrabold uppercase tracking-wider text-amber-500">
                  DIRECT EXECUTIVE & STAKEHOLDER INGEST // LILONGWE HQ
                </span>
              </div>
              <h2 className={`text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                Engage LightSpeed Holdings
              </h2>
              <p className={`text-xs mt-1 leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                Direct engagement portal for C-Suite Executives, Academics, Regulators, Government Agencies, NGOs, and the Donor Community across Malawi &amp; SADC.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 text-xs">
              
              {/* Stakeholder Category Picker */}
              <div>
                <label className={`block font-mono uppercase mb-1.5 font-bold text-[11px] ${isLight ? 'text-slate-700' : 'text-amber-400'}`}>
                  1. Select Stakeholder Group
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {[
                    { id: 'Executive / Corporate', label: 'Executives & C-Suite', icon: '🏢' },
                    { id: 'Academic / University', label: 'Academics & Research', icon: '🎓' },
                    { id: 'Regulator / Statutory', label: 'Regulators & RBM/MACRA', icon: '⚖️' },
                    { id: 'Government Agency', label: 'Government Agencies', icon: '🏛️' },
                    { id: 'NGO / Civil Society', label: 'NGOs & Development', icon: '🌍' },
                    { id: 'Donor Community', label: 'Donor Community', icon: '🤝' }
                  ].map((cat) => {
                    const isSelected = formData.role.includes(cat.id) || intent.includes(cat.id);
                    return (
                      <button
                        key={cat.id}
                        type="button"
                        onClick={() => {
                          setFormData(prev => ({ ...prev, role: `${cat.id}` }));
                          setIntent(`Consulting & Engagement Offer — ${cat.label}`);
                        }}
                        className={`p-2 rounded-xl border text-left transition-all text-[11px] font-mono flex items-center gap-1.5 cursor-pointer ${
                          isSelected 
                            ? 'bg-amber-500/20 border-amber-500 text-amber-300 font-bold shadow-sm' 
                            : isLight 
                              ? 'bg-white border-slate-300 hover:border-amber-400 text-slate-700' 
                              : 'bg-zinc-900 border-zinc-700 hover:border-zinc-500 text-zinc-300'
                        }`}
                      >
                        <span>{cat.icon}</span>
                        <span className="truncate">{cat.label}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Intent Selector */}
              <div>
                <label className={`block font-mono uppercase mb-1 font-bold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  2. Engagement &amp; Offer Focus
                </label>
                <select
                  value={intent}
                  onChange={(e) => setIntent(e.target.value)}
                  className={`w-full border rounded-xl px-3 py-2.5 font-mono text-xs focus:outline-none focus:border-amber-500 ${
                    isLight
                      ? 'flight-deck-well-light border-slate-300 text-slate-900'
                      : 'flight-deck-well-dark border-zinc-700 text-zinc-200'
                  }`}
                >
                  <option value="Consulting Offer & Strategy Advisory">Executive Consulting Offer & Strategy Advisory</option>
                  <option value="Academic AI Research & University Collaboration">Academic AI Research & University Collaboration</option>
                  <option value="Regulatory Compliance & Governance Audit (RBM/MACRA/DPA)">Regulatory Compliance & Governance Audit (RBM/MACRA/DPA)</option>
                  <option value="Government National AI Deployment & E-Gov">Government National AI Deployment & E-Gov</option>
                  <option value="NGO Field Telemetry & M&E Automation">NGO Field Telemetry & M&E Automation</option>
                  <option value="Donor Community Co-Engineering & Grant Delivery">Donor Community Co-Engineering & Grant Delivery</option>
                  <option value="AI Company Builder Platform License">AI Company Builder Platform License</option>
                  <option value="General Leadership Enquiries">General Leadership Enquiries</option>
                </select>
              </div>

              {/* Name & Email */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className={`block font-mono uppercase mb-1 font-bold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                    Principal Name *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="Dr. Kondwani Banda"
                    value={formData.name}
                    onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                    className={`w-full border rounded-xl px-3 py-2.5 font-mono text-xs focus:outline-none focus:border-amber-500 ${
                      isLight
                        ? 'flight-deck-well-light border-slate-300 text-slate-900 placeholder:text-slate-400'
                        : 'flight-deck-well-dark border-zinc-700 text-zinc-200 placeholder:text-zinc-600'
                    }`}
                  />
                </div>
                <div>
                  <label className={`block font-mono uppercase mb-1 font-bold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                    Official Email *
                  </label>
                  <input
                    type="email"
                    required
                    placeholder="name@organization.mw"
                    value={formData.email}
                    onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                    className={`w-full border rounded-xl px-3 py-2.5 font-mono text-xs focus:outline-none focus:border-amber-500 ${
                      isLight
                        ? 'flight-deck-well-light border-slate-300 text-slate-900 placeholder:text-slate-400'
                        : 'flight-deck-well-dark border-zinc-700 text-zinc-200 placeholder:text-zinc-600'
                    }`}
                  />
                </div>
              </div>

              {/* Organization & Role */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className={`block font-mono uppercase mb-1 font-bold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                    Enterprise / Entity
                  </label>
                  <input
                    type="text"
                    placeholder="Ministry / Bank / Telecom"
                    value={formData.organization}
                    onChange={(e) => setFormData(prev => ({ ...prev, organization: e.target.value }))}
                    className={`w-full border rounded-xl px-3 py-2.5 font-mono text-xs focus:outline-none focus:border-amber-500 ${
                      isLight
                        ? 'flight-deck-well-light border-slate-300 text-slate-900 placeholder:text-slate-400'
                        : 'flight-deck-well-dark border-zinc-700 text-zinc-200 placeholder:text-zinc-600'
                    }`}
                  />
                </div>
                <div>
                  <label className={`block font-mono uppercase mb-1 font-bold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                    Role / Title
                  </label>
                  <input
                    type="text"
                    placeholder="Director of IT / CEO / Partner"
                    value={formData.role}
                    onChange={(e) => setFormData(prev => ({ ...prev, role: e.target.value }))}
                    className={`w-full border rounded-xl px-3 py-2.5 font-mono text-xs focus:outline-none focus:border-amber-500 ${
                      isLight
                        ? 'flight-deck-well-light border-slate-300 text-slate-900 placeholder:text-slate-400'
                        : 'flight-deck-well-dark border-zinc-700 text-zinc-200 placeholder:text-zinc-600'
                    }`}
                  />
                </div>
              </div>

              {/* Project Scope */}
              <div>
                <label className={`block font-mono uppercase mb-1 font-bold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  Operational Scope & Architecture Objectives
                </label>
                <textarea
                  rows={3}
                  placeholder="Detail your operational constraints, target SLA requirements, or sovereign deployment specs..."
                  value={formData.notes}
                  onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                  className={`w-full border rounded-xl p-3 font-mono text-xs focus:outline-none focus:border-amber-500 ${
                    isLight
                      ? 'flight-deck-well-light border-slate-300 text-slate-900 placeholder:text-slate-400'
                      : 'flight-deck-well-dark border-zinc-700 text-zinc-200 placeholder:text-zinc-600'
                  }`}
                ></textarea>
              </div>

              {/* Submit Button */}
              <div className="pt-2">
                <button
                  type="submit"
                  className="w-full py-3.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono uppercase text-xs tracking-wider transition-all flex items-center justify-center gap-2 shadow-lg shadow-amber-500/20 active:scale-95"
                >
                  <Send className="w-4 h-4" />
                  <span>Transmit Telemetry to LightSpeed Command</span>
                </button>
              </div>

            </form>
          </div>
        ) : (
          <div className="text-center py-8 space-y-4">
            <div className="p-4 rounded-2xl bg-emerald-500/10 text-emerald-500 border border-emerald-500/30 w-fit mx-auto">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <div className="flex items-center justify-center gap-2">
              <StatusLedPip status="emerald" isLight={isLight} />
              <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                Transmission Dispatched
              </h3>
            </div>
            <p className={`text-xs max-w-sm mx-auto leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-300'}`}>
              Confirmed, {formData.name}. Your dispatch for <strong>"{intent}"</strong> has been logged to the secure queue of LightSpeed Holdings Limited.
            </p>
            <div className="pt-4">
              <button
                onClick={() => {
                  setSubmitted(false);
                  onClose();
                }}
                className="px-6 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono text-xs uppercase tracking-wider transition-all active:scale-95"
              >
                Return to Command Deck
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
};
