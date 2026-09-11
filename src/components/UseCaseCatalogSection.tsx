import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  BookOpen, 
  Search, 
  Filter, 
  CheckCircle2, 
  AlertTriangle, 
  Lock, 
  Coins, 
  ArrowRight, 
  Building2, 
  Sprout, 
  Activity, 
  Landmark, 
  Layers, 
  Globe2, 
  ShieldCheck, 
  Clock, 
  Tag, 
  Sparkles, 
  Download, 
  ExternalLink,
  ChevronRight,
  Info
} from 'lucide-react';
import { 
  CATALOG_POSITIONING, 
  CATALOG_METHOD, 
  OFFER_FAMILIES, 
  ENTERPRISE_CAPABILITIES, 
  CATALOG_INDUSTRIES, 
  PLATFORM_SCENARIOS, 
  CATALOG_PROOF_POINTS, 
  CATALOG_POLICIES 
} from '../data/useCaseCatalogData';
import { HonestyBadge } from '../types';

interface UseCaseCatalogSectionProps {
  theme?: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const UseCaseCatalogSection: React.FC<UseCaseCatalogSectionProps> = ({
  theme = 'dark',
  onRequestBriefing
}) => {
  const isLight = theme === 'light';

  const [activeTab, setActiveTab] = useState<'offers' | 'industries' | 'scenarios' | 'proof' | 'method'>('offers');
  const [selectedOfferLetter, setSelectedOfferLetter] = useState<string>('all');
  const [selectedHonestyFilter, setSelectedHonestyFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const renderHonestyBadge = (badge: HonestyBadge) => {
    switch (badge) {
      case 'Proven in-house':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-purple-500/10 text-purple-400 border border-purple-500/30">
            <ShieldCheck className="w-3 h-3" />
            <span>Proven in-house</span>
          </span>
        );
      case 'Live proof':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
            <span>Live Proof (SME)</span>
          </span>
        );
      case 'Fieldable in 2026':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-blue-500/10 text-blue-400 border border-blue-500/30">
            <Clock className="w-3 h-3 text-blue-400" />
            <span>Fieldable in 2026</span>
          </span>
        );
      case 'In active development':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30">
            <AlertTriangle className="w-3 h-3 text-amber-400" />
            <span>In Active Development</span>
          </span>
        );
      case 'Published':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-teal-500/10 text-teal-400 border border-teal-500/30">
            <Globe2 className="w-3 h-3 text-teal-400" />
            <span>Published Policy</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-orange-500/10 text-orange-400 border border-orange-500/30">
            <Sparkles className="w-3 h-3 text-orange-400" />
            <span>{badge}</span>
          </span>
        );
    }
  };

  const filteredOffers = useMemo(() => {
    return OFFER_FAMILIES.filter((offer) => {
      const matchesLetter = selectedOfferLetter === 'all' || offer.letter === selectedOfferLetter;
      const matchesHonesty = selectedHonestyFilter === 'all' || offer.honestyBadge === selectedHonestyFilter;
      const matchesSearch = searchQuery === '' || 
        offer.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        offer.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        offer.deliverables.some(d => d.name.toLowerCase().includes(searchQuery.toLowerCase()) || d.description.toLowerCase().includes(searchQuery.toLowerCase()));
      
      return matchesLetter && matchesHonesty && matchesSearch;
    });
  }, [selectedOfferLetter, selectedHonestyFilter, searchQuery]);

  return (
    <section id="use-case-catalog" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full relative z-10 border-t ${
      isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
    }`}>
      {/* SECTION HEADER */}
      <div className="space-y-4 mb-10 text-left">
        <div className="flex flex-wrap items-center gap-3">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-400 font-mono text-[11px] font-bold tracking-widest shadow-xs">
            <BookOpen className="w-3.5 h-3.5 text-orange-500" />
            <span>MASTER USE CASE CATALOG v1</span>
          </div>

          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 font-mono text-[10px] font-bold tracking-widest">
            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
            <span>100% HONESTY-BADGED // NO FABRICATED METRICS</span>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
          <div className="space-y-2 max-w-3xl">
            <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display leading-tight ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              Service Offers, Industry Solutions &amp; <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 via-amber-500 to-amber-300">
                Governed Agentic AI Architecture
              </span>
            </h2>
            <p className={`text-justify text-sm sm:text-base font-medium leading-relaxed ${
              isLight ? 'text-slate-700' : 'text-zinc-300'
            }`}>
              {CATALOG_POSITIONING.positioningLine} Explore the 5 service offer families, 5 SADC industry verticals, 8 platform scenarios, and verified proof points anchored in dual MWK / USD pricing.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <button
              onClick={() => onRequestBriefing?.('Use Case Catalog & Pricing Engagement')}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-mono font-bold bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-lg shadow-orange-500/20 transition-all cursor-pointer"
            >
              <span>Book Discovery Call</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* HONESTY CLASSIFICATION BANNER */}
      <div className={`p-4 sm:p-5 rounded-2xl border mb-8 flex flex-col md:flex-row items-start md:items-center gap-4 ${
        isLight ? 'bg-amber-50/80 border-amber-200 text-amber-900' : 'bg-amber-950/20 border-amber-500/30 text-amber-200'
      }`}>
        <div className="w-9 h-9 rounded-xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0">
          <Info className="w-5 h-5" />
        </div>
        <div className="text-xs leading-relaxed space-y-1">
          <strong className="font-mono text-amber-400 uppercase tracking-wide block font-bold">
            HONESTY CLASSIFICATION GUARANTEE
          </strong>
          <p className="text-justify font-medium">
            {CATALOG_POSITIONING.honestyClassification}
          </p>
        </div>
      </div>

      {/* FILTER & TABS TOOLBAR */}
      <div className={`p-2 rounded-2xl border mb-8 space-y-3 ${
        isLight ? 'bg-slate-100 border-slate-300' : 'bg-zinc-900/90 border-zinc-800'
      }`}>
        {/* Main Category Tabs */}
        <div className="flex flex-wrap items-center justify-between gap-2 border-b pb-2 border-white/10">
          <div className="flex flex-wrap items-center gap-1.5">
            {[
              { id: 'offers', label: '01. Service Offers (A–E)', icon: Coins },
              { id: 'industries', label: '02. SADC Industry Verticals', icon: Sprout },
              { id: 'scenarios', label: '03. Platform Scenarios (FOW)', icon: Layers },
              { id: 'proof', label: '04. Proof & Policy Points', icon: ShieldCheck },
              { id: 'method', label: '05. The Method & Governance', icon: Landmark }
            ].map((tab) => {
              const IconComp = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                    isActive 
                      ? 'bg-orange-500 text-white shadow-md' 
                      : isLight 
                        ? 'text-slate-700 hover:bg-white/80' 
                        : 'text-zinc-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  <IconComp className="w-3.5 h-3.5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>

          {/* Search Box */}
          <div className="relative w-full sm:w-64">
            <Search className="w-3.5 h-3.5 text-zinc-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search catalog..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={`w-full pl-9 pr-3 py-1.5 rounded-xl text-xs font-mono border focus:outline-none focus:border-orange-500 transition-all ${
                isLight 
                  ? 'bg-white border-slate-300 text-slate-900' 
                  : 'bg-black/50 border-white/10 text-white'
              }`}
            />
          </div>
        </div>

        {/* Secondary Sub-Filters for Offers */}
        {activeTab === 'offers' && (
          <div className="flex flex-wrap items-center justify-between gap-3 text-xs font-mono pt-1">
            <div className="flex items-center gap-1.5">
              <span className="text-zinc-400 text-[11px] font-bold">Offer Family:</span>
              {['all', 'A', 'B', 'C', 'D', 'E'].map((letter) => (
                <button
                  key={letter}
                  onClick={() => setSelectedOfferLetter(letter)}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition-all cursor-pointer ${
                    selectedOfferLetter === letter
                      ? 'bg-orange-500/20 text-orange-400 border border-orange-500/40'
                      : 'text-zinc-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  {letter === 'all' ? 'All (A–E)' : `Offer ${letter}`}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-2">
              <span className="text-zinc-400 text-[11px]">Pricing Anchor:</span>
              <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[10px] font-bold border border-emerald-500/30">
                Dual MWK / ~USD
              </span>
            </div>
          </div>
        )}
      </div>

      {/* CONTENT PANELS */}
      <AnimatePresence mode="wait">
        {/* TAB 1: SERVICE OFFERS (A–E) */}
        {activeTab === 'offers' && (
          <motion.div
            key="offers"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className="space-y-8"
          >
            {filteredOffers.map((family) => (
              <div 
                key={family.id}
                className={`p-6 sm:p-8 rounded-3xl border relative overflow-hidden transition-all ${
                  isLight 
                    ? 'bg-white border-slate-300 shadow-md hover:shadow-lg' 
                    : 'bg-zinc-950 border-white/15 shadow-2xl'
                }`}
              >
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 border-b border-white/10 mb-6">
                  <div className="space-y-2">
                    <div className="flex items-center gap-3">
                      <span className="w-9 h-9 rounded-2xl bg-orange-500 text-white font-mono font-black text-lg flex items-center justify-center shadow-md">
                        {family.letter}
                      </span>
                      <h3 className={`text-2xl font-black font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                        Offer {family.letter} — {family.title}
                      </h3>
                      {renderHonestyBadge(family.honestyBadge)}
                    </div>
                    <p className={`text-sm font-semibold text-orange-500`}>
                      "{family.tagline}"
                    </p>
                    <p className={`text-justify text-xs leading-relaxed max-w-3xl ${isLight ? 'text-slate-600' : 'text-zinc-300'}`}>
                      {family.description}
                    </p>
                  </div>

                  <div className="shrink-0 font-mono text-xs space-y-2 lg:text-right">
                    <div className="text-zinc-400 text-[11px]">
                      <strong className="text-white block font-bold">TARGET CLIENTS:</strong>
                      {family.targetClients.join(', ')}
                    </div>
                    <button
                      onClick={() => onRequestBriefing?.(`Inquiry regarding Offer ${family.letter}: ${family.title}`)}
                      className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono font-bold bg-orange-500/15 text-orange-400 hover:bg-orange-500 hover:text-white transition-all cursor-pointer border border-orange-500/30"
                    >
                      <span>Inquire Offer {family.letter}</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

                {/* DELIVERABLES TABLE */}
                <div className="overflow-x-auto mb-6">
                  <table className="w-full text-left border-collapse text-xs font-mono">
                    <thead>
                      <tr className={`border-b text-[11px] ${isLight ? 'border-slate-200 text-slate-500' : 'border-white/10 text-zinc-400'}`}>
                        <th className="py-3 px-4 font-bold">Deliverable Code &amp; Name</th>
                        <th className="py-3 px-4 font-bold">Description</th>
                        <th className="py-3 px-4 font-bold text-right">Local (MWK)</th>
                        <th className="py-3 px-4 font-bold text-right">Global (~USD)</th>
                        <th className="py-3 px-4 font-bold">Turnaround</th>
                        <th className="py-3 px-4 font-bold">Governance Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/10">
                      {family.deliverables.map((d) => (
                        <tr 
                          key={d.id}
                          className={`transition-colors ${
                            d.blocked 
                              ? isLight ? 'bg-amber-50/50' : 'bg-amber-950/10' 
                              : isLight ? 'hover:bg-slate-50' : 'hover:bg-white/5'
                          }`}
                        >
                          <td className="py-4 px-4 font-bold text-orange-400 shrink-0">
                            {d.name}
                          </td>
                          <td className={`py-4 px-4 text-[11px] ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                            {d.description}
                            {d.hostingFee && (
                              <div className="text-[10px] text-emerald-400 font-bold mt-1">
                                {d.hostingFee}
                              </div>
                            )}
                          </td>
                          <td className="py-4 px-4 font-bold text-white text-right shrink-0">
                            {d.priceMwk}
                          </td>
                          <td className="py-4 px-4 font-bold text-emerald-400 text-right shrink-0">
                            {d.priceUsd}
                          </td>
                          <td className="py-4 px-4 text-zinc-400 text-[11px] shrink-0">
                            {d.turnaround}
                          </td>
                          <td className="py-4 px-4 shrink-0">
                            {d.blocked ? (
                              <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-bold">
                                <Lock className="w-3 h-3 text-amber-400" />
                                <span>BLOCKED: {d.blockedReason}</span>
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold">
                                <CheckCircle2 className="w-3 h-3" />
                                <span>Ready to Deploy</span>
                              </span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* GOVERNANCE & PRICING NOTES */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                  <div className={`p-3.5 rounded-2xl border ${
                    isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/30 border-white/10'
                  }`}>
                    <strong className="text-orange-400 block mb-1 font-bold">GOVERNANCE NOTE:</strong>
                    <p className={`text-[11px] ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                      {family.governanceNote}
                    </p>
                  </div>

                  <div className={`p-3.5 rounded-2xl border ${
                    isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/30 border-white/10'
                  }`}>
                    <strong className="text-emerald-400 block mb-1 font-bold">PRICING TERMS:</strong>
                    <p className={`text-[11px] ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                      {family.pricingNote}
                    </p>
                  </div>
                </div>
              </div>
            ))}

            {/* ENTERPRISE TRANSFORMATION LINE */}
            <div className={`p-6 sm:p-8 rounded-3xl border ${
              isLight ? 'bg-slate-900 text-white border-slate-800' : 'bg-zinc-950 border-orange-500/30'
            }`}>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div>
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-500/20 text-orange-400 font-mono text-[10px] font-bold mb-2">
                    <Building2 className="w-3 h-3" />
                    <span>ENTERPRISE TRANSFORMATION CONSULTANCY</span>
                  </div>
                  <h3 className="text-2xl font-black font-display">
                    Enterprise Transformation Line (Custom Capability)
                  </h3>
                  <p className="text-xs text-zinc-400 mt-1 max-w-2xl">
                    In active development for organizations requiring custom multi-agent integration, forward-deployed engineering capacity, or co-build venture models.
                  </p>
                </div>

                {renderHonestyBadge('In active development')}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 font-mono text-xs">
                {ENTERPRISE_CAPABILITIES.map((cap, idx) => (
                  <div key={idx} className="p-4 rounded-2xl bg-black/40 border border-white/10 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <strong className="text-orange-400 font-bold">{cap.name}</strong>
                      <span className="text-[10px] text-amber-400 px-1.5 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">
                        Active Dev
                      </span>
                    </div>
                    <p className="text-zinc-300 text-[11px] leading-relaxed">
                      {cap.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        {/* TAB 2: SADC INDUSTRY VERTICALS */}
        {activeTab === 'industries' && (
          <motion.div
            key="industries"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-6"
          >
            {CATALOG_INDUSTRIES.map((ind) => (
              <div 
                key={ind.id}
                className={`p-6 sm:p-8 rounded-3xl border flex flex-col justify-between space-y-6 ${
                  isLight ? 'bg-white border-slate-300 shadow-md' : 'bg-zinc-950 border-white/15'
                }`}
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between gap-3">
                    <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {ind.title}
                    </h3>
                    {renderHonestyBadge(ind.honestyBadge)}
                  </div>

                  <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                    {ind.description}
                  </p>

                  <div className="space-y-2">
                    <span className="font-mono text-[11px] font-bold text-orange-400 uppercase tracking-wide block">
                      KEY AGENTIC USE CASES:
                    </span>
                    <ul className="space-y-2 font-mono text-xs">
                      {ind.keyUseCases.map((uc, idx) => (
                        <li key={idx} className="flex items-start gap-2 text-zinc-300 text-[11px]">
                          <span className="text-orange-500 shrink-0">▸</span>
                          <span>{uc}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className={`p-3 rounded-2xl border text-[11px] font-mono ${
                  isLight ? 'bg-slate-50 border-slate-200 text-slate-700' : 'bg-black/30 border-white/10 text-zinc-400'
                }`}>
                  <strong className="text-amber-400 block mb-0.5">HONESTY STATUS NOTE:</strong>
                  {ind.honestyNote}
                </div>
              </div>
            ))}
          </motion.div>
        )}

        {/* TAB 3: PLATFORM SCENARIOS (FOW-01..08) */}
        {activeTab === 'scenarios' && (
          <motion.div
            key="scenarios"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
          >
            {PLATFORM_SCENARIOS.map((scenario) => (
              <div 
                key={scenario.id}
                className={`p-5 rounded-3xl border flex flex-col justify-between space-y-4 ${
                  isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-zinc-950 border-white/15'
                }`}
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="px-2.5 py-1 rounded-lg bg-orange-500/10 text-orange-400 border border-orange-500/30 font-mono text-xs font-bold">
                      {scenario.code}
                    </span>
                    {renderHonestyBadge(scenario.honestyBadge)}
                  </div>

                  <h4 className={`text-base font-bold font-display leading-tight ${isLight ? 'text-slate-900' : 'text-white'}`}>
                    {scenario.title}
                  </h4>

                  <span className="text-[11px] font-mono text-amber-400 font-semibold block">
                    {scenario.subtitle}
                  </span>

                  <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-300'}`}>
                    {scenario.description}
                  </p>
                </div>

                <div className="pt-3 border-t border-white/10 font-mono text-[10px] text-zinc-400">
                  <strong className="text-white block font-bold">TARGET DEPLOYMENT:</strong>
                  {scenario.targetAudience}
                </div>
              </div>
            ))}
          </motion.div>
        )}

        {/* TAB 4: PROOF & POLICY POINTS */}
        {activeTab === 'proof' && (
          <motion.div
            key="proof"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className="space-y-8"
          >
            {/* PROOF POINTS */}
            <div className="space-y-4">
              <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                Verified Field Proof &amp; Pilot Implementations
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {CATALOG_PROOF_POINTS.map((proof) => (
                  <div 
                    key={proof.id}
                    className={`p-6 rounded-3xl border space-y-4 flex flex-col justify-between ${
                      isLight ? 'bg-white border-slate-300 shadow-md' : 'bg-zinc-950 border-white/15'
                    }`}
                  >
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-[11px] font-mono font-bold text-orange-400 uppercase">
                          {proof.category}
                        </span>
                        {renderHonestyBadge(proof.honestyBadge)}
                      </div>

                      <h4 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                        {proof.title}
                      </h4>

                      <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-300'}`}>
                        {proof.description}
                      </p>
                    </div>

                    <div className="space-y-2 pt-3 border-t border-white/10 font-mono text-[11px]">
                      <div>
                        <strong className="text-orange-400 block font-bold">WHAT IT PROVES:</strong>
                        <span className="text-zinc-300">{proof.whatItMonitorsOrProves}</span>
                      </div>
                      <div>
                        <strong className="text-emerald-400 block font-bold">WHY IT MATTERS:</strong>
                        <span className="text-zinc-400 text-[10px]">{proof.whyItMatters}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* POLICY TRACK */}
            <div className="space-y-4 pt-6 border-t border-white/10">
              <h3 className={`text-xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                SADC AI Governance &amp; Pharos Policy Track
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {CATALOG_POLICIES.map((pol) => (
                  <div 
                    key={pol.id}
                    className={`p-6 rounded-3xl border space-y-3 ${
                      isLight ? 'bg-white border-slate-300' : 'bg-zinc-950 border-white/15'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <Landmark className="w-5 h-5 text-orange-400" />
                      {renderHonestyBadge(pol.honestyBadge)}
                    </div>

                    <h4 className={`text-base font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {pol.title}
                    </h4>

                    <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                      {pol.summary}
                    </p>

                    <p className="text-zinc-400 text-[11px] font-mono pt-2 border-t border-white/10">
                      {pol.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        {/* TAB 5: THE METHOD & GOVERNANCE */}
        {activeTab === 'method' && (
          <motion.div
            key="method"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
            className={`p-6 sm:p-8 rounded-3xl border space-y-8 ${
              isLight ? 'bg-white border-slate-300' : 'bg-zinc-950 border-white/15'
            }`}
          >
            <div>
              <span className="font-mono text-xs font-bold text-orange-500 uppercase tracking-wider block mb-1">
                OPERATING ARCHITECTURE
              </span>
              <h3 className={`text-2xl font-black font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                {CATALOG_METHOD.title}
              </h3>
              <p className={`text-sm mt-2 max-w-3xl leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                {CATALOG_METHOD.summary}
              </p>
            </div>

            {/* Pipeline Flow */}
            <div className={`p-4 rounded-2xl border font-mono text-xs ${
              isLight ? 'bg-orange-50 border-orange-200 text-orange-900' : 'bg-orange-950/20 border-orange-500/30 text-orange-300'
            }`}>
              <strong className="block text-orange-400 font-bold mb-1">CANONICAL DELIVERY PIPELINE:</strong>
              {CATALOG_METHOD.pipeline}
            </div>

            {/* Governance Pillars */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 font-mono text-xs">
              {CATALOG_METHOD.governancePillars.map((p, idx) => (
                <div key={idx} className="p-4 rounded-2xl bg-black/30 border border-white/10 space-y-2">
                  <div className="flex items-center gap-2 text-orange-400 font-bold">
                    <ShieldCheck className="w-4 h-4" />
                    <span>{p.title}</span>
                  </div>
                  <p className="text-zinc-300 text-[11px] leading-relaxed">
                    {p.description}
                  </p>
                </div>
              ))}
            </div>

            {/* Sovereignty */}
            <div className={`p-5 rounded-2xl border ${
              isLight ? 'bg-slate-50 border-slate-200' : 'bg-black/40 border-white/10'
            }`}>
              <strong className="text-emerald-400 font-mono text-xs block font-bold mb-1">
                SOVEREIGNTY &amp; OFFLINE-FIRST COMPLIANCE:
              </strong>
              <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                {CATALOG_METHOD.sovereignty}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
};
