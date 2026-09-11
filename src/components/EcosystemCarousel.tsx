import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  ChevronLeft, 
  ChevronRight, 
  Pause, 
  Play, 
  Building2, 
  Landmark, 
  GraduationCap, 
  Globe, 
  ShieldCheck,
  Sparkles,
  ArrowRight,
  Layers,
  Activity
} from 'lucide-react';
import { AcousticVentGrille } from './TactileHardwareElements';

interface EcosystemItem {
  id: string;
  name: string;
  fullName: string;
  role: string;
  category: 'multilateral' | 'government' | 'industry' | 'academia';
  tag: string;
  standardsNote: string;
  badgeColor: string;
}

interface EcosystemCarouselProps {
  theme?: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const EcosystemCarousel: React.FC<EcosystemCarouselProps> = ({
  theme = 'dark',
  onRequestBriefing
}) => {
  const isLight = theme === 'light';

  const ecosystemData: EcosystemItem[] = [
    {
      id: 'undp',
      name: 'UNDP Malawi',
      fullName: 'United Nations Development Programme',
      role: 'Innovation & Digital Transformation Dialogue',
      category: 'multilateral',
      tag: 'Donor Co-Design',
      standardsNote: 'Co-designing vernacular digital inclusion frameworks and agricultural resilience telemetry for rural smallholders.',
      badgeColor: 'border-blue-500/30 text-blue-400 bg-blue-500/10'
    },
    {
      id: 'worldbank',
      name: 'World Bank Malawi',
      fullName: 'World Bank Group — Southern Africa Digital Economy',
      role: 'Digital Economy & Agricultural Resiliency',
      category: 'multilateral',
      tag: 'Multilateral Exchange',
      standardsNote: 'Technical exchange on digital public infrastructure (DPI), mobile money interoperability, and SME credit ledger generation.',
      badgeColor: 'border-sky-500/30 text-sky-400 bg-sky-500/10'
    },
    {
      id: 'minag',
      name: 'Ministry of Agriculture',
      fullName: 'Government of Malawi — Ministry of Agriculture (MinAg)',
      role: 'Vernacular Extension Advisory Frameworks',
      category: 'government',
      tag: 'Government Collaboration',
      standardsNote: 'Piloting Chichewa-first agricultural extension NLU models across Lilongwe, Dedza, and Thyolo agricultural cooperatives.',
      badgeColor: 'border-emerald-500/30 text-emerald-400 bg-emerald-500/10'
    },
    {
      id: 'macra',
      name: 'MACRA',
      fullName: 'Malawi Communications Regulatory Authority',
      role: 'Telecommunications & AI Data Governance',
      category: 'government',
      tag: 'Statutory Regulator',
      standardsNote: 'Strict alignment with the Malawi Data Protection Act 2017/2024 ensuring 100% on-soil data residency and zero telemetry leakage.',
      badgeColor: 'border-orange-500/30 text-orange-400 bg-orange-500/10'
    },
    {
      id: 'ictam',
      name: 'ICTAM',
      fullName: 'Information and Communications Technology Association of Malawi',
      role: 'National Technology Policy & Ethics Working Groups',
      category: 'industry',
      tag: 'Industry Peak Body',
      standardsNote: 'Active corporate member shaping ethical sovereign AI deployment benchmarks and digital workforce upskilling protocols.',
      badgeColor: 'border-amber-500/30 text-amber-400 bg-amber-500/10'
    },
    {
      id: 'mhub',
      name: 'mHub Malawi',
      fullName: 'mHub Tech Hub & Innovation Incubator',
      role: 'Tech Ecosystem Incubation & Developer Networks',
      category: 'industry',
      tag: 'Ecosystem Partner',
      standardsNote: 'Collaborative hackathons, OpenCode agent workshops, and junior developer mentorship across Lilongwe and Blantyre.',
      badgeColor: 'border-purple-500/30 text-purple-400 bg-purple-500/10'
    },
    {
      id: 'comesa',
      name: 'COMESA / IDEA',
      fullName: 'Common Market for Eastern and Southern Africa / Digital Free Trade',
      role: 'Regional Cross-Border Trade & Customs Standards',
      category: 'multilateral',
      tag: 'Regional Standards',
      standardsNote: 'Harmonizing digital trade protocols, EDI shipping manifest verification, and cross-border transport corridor telemetry.',
      badgeColor: 'border-teal-500/30 text-teal-400 bg-teal-500/10'
    },
    {
      id: 'academia',
      name: 'MUBAS & UNIMA',
      fullName: 'Malawi University of Business & Applied Sciences & University of Malawi',
      role: 'AI Engineering & Applied Research Collaboration',
      category: 'academia',
      tag: 'Academic Synergy',
      standardsNote: 'Applied computational linguistics research on Chichewa grammar trees, low-resource speech synthesis, and local LLM fine-tuning.',
      badgeColor: 'border-indigo-500/30 text-indigo-400 bg-indigo-500/10'
    }
  ];

  const [activeCategory, setActiveCategory] = useState<'all' | 'multilateral' | 'government' | 'industry' | 'academia'>('all');
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState<boolean>(true);
  const [itemsPerView, setItemsPerView] = useState<number>(3);
  const containerRef = useRef<HTMLDivElement>(null);

  const filteredItems = activeCategory === 'all' 
    ? ecosystemData 
    : ecosystemData.filter(item => item.category === activeCategory);

  // Responsive items per view
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 640) {
        setItemsPerView(1);
      } else if (window.innerWidth < 1024) {
        setItemsPerView(2);
      } else {
        setItemsPerView(3);
      }
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const maxIndex = Math.max(0, filteredItems.length - itemsPerView);

  // Keep currentIndex bounded when filter changes
  useEffect(() => {
    setCurrentIndex(0);
  }, [activeCategory]);

  // Auto-play interval
  useEffect(() => {
    if (!isAutoPlaying || maxIndex === 0) return;
    const interval = setInterval(() => {
      setCurrentIndex(prev => (prev >= maxIndex ? 0 : prev + 1));
    }, 4500);
    return () => clearInterval(interval);
  }, [isAutoPlaying, maxIndex, filteredItems.length]);

  const handlePrev = () => {
    setCurrentIndex(prev => (prev <= 0 ? maxIndex : prev - 1));
  };

  const handleNext = () => {
    setCurrentIndex(prev => (prev >= maxIndex ? 0 : prev + 1));
  };

  return (
    <section 
      id="ecosystem-dialogue"
      aria-label="Institutional Ecosystem Dialogue and Standards Alignment"
      className={`py-12 border-y relative z-10 transition-colors ${
        isLight ? 'bg-slate-100/80 border-slate-300' : 'bg-black/50 border-white/10'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-8">
        
        {/* Carousel Header & Controls */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-6">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2 font-mono text-[10px] tracking-widest text-orange-500 font-bold">
              <span className="w-2 h-2 rounded-full bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.8)] animate-pulse" />
              <span className="uppercase">INSTITUTIONAL ECOSYSTEM DIALOGUE & STANDARDS ALIGNMENT</span>
            </div>
            <h3 className={`text-xl sm:text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
              Sovereign SADC Institutional Synergy & Regulatory Dialogue
            </h3>
            <p className={`text-xs ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Framed for SADC Data Sovereignty • Active technical exchange & standards alignment across government, multilaterals, and research hubs.
            </p>
          </div>

          {/* Right Toolbar: Category Filter & Play/Pause/Nav */}
          <div className="flex flex-wrap items-center gap-2.5">
            
            {/* Category Filter Pills */}
            <div className={`flex items-center p-1 rounded-xl border ${
              isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/90 border-white/10'
            }`}>
              {[
                { key: 'all', label: 'All Stakeholders' },
                { key: 'government', label: 'Government & Regulators' },
                { key: 'multilateral', label: 'Multilaterals' },
                { key: 'industry', label: 'Industry' },
                { key: 'academia', label: 'Academia' }
              ].map(cat => (
                <button
                  key={cat.key}
                  onClick={() => setActiveCategory(cat.key as any)}
                  className={`px-2.5 py-1 rounded-lg text-[10px] font-mono font-bold transition-all cursor-pointer ${
                    activeCategory === cat.key
                      ? 'bg-orange-500 text-white shadow-xs'
                      : isLight 
                        ? 'text-slate-600 hover:text-slate-900' 
                        : 'text-zinc-400 hover:text-white'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>

            {/* Hardware-styled Carousel Nav Buttons */}
            <div className={`flex items-center gap-1 p-1 rounded-xl border ${
              isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/90 border-white/10'
            }`}>
              <button
                onClick={() => setIsAutoPlaying(!isAutoPlaying)}
                aria-label={isAutoPlaying ? 'Pause carousel auto-rotation' : 'Play carousel auto-rotation'}
                className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                  isLight ? 'hover:bg-slate-100 text-slate-700' : 'hover:bg-white/10 text-zinc-300'
                }`}
                title={isAutoPlaying ? 'Pause rotation' : 'Resume rotation'}
              >
                {isAutoPlaying ? <Pause className="w-3.5 h-3.5 text-orange-500" /> : <Play className="w-3.5 h-3.5" />}
              </button>

              <div className="w-[1px] h-4 bg-black/10 dark:bg-white/10" />

              <button
                onClick={handlePrev}
                aria-label="Previous ecosystem partner slide"
                className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                  isLight ? 'hover:bg-slate-100 text-slate-700' : 'hover:bg-white/10 text-zinc-300'
                }`}
              >
                <ChevronLeft className="w-3.5 h-3.5" />
              </button>

              <button
                onClick={handleNext}
                aria-label="Next ecosystem partner slide"
                className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                  isLight ? 'hover:bg-slate-100 text-slate-700' : 'hover:bg-white/10 text-zinc-300'
                }`}
              >
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>

          </div>
        </div>

        {/* Carousel Slider Window */}
        <div 
          ref={containerRef}
          onMouseEnter={() => setIsAutoPlaying(false)}
          onMouseLeave={() => setIsAutoPlaying(true)}
          className="relative overflow-hidden py-1"
        >
          <motion.div
            className="flex gap-4"
            animate={{
              x: `calc(-${currentIndex * (100 / itemsPerView)}% - ${currentIndex * (16 / itemsPerView)}px)`
            }}
            transition={{ type: 'spring', stiffness: 260, damping: 30 }}
          >
            {filteredItems.map((item) => (
              <div
                key={item.id}
                style={{ flex: `0 0 calc(${100 / itemsPerView}% - ${(16 * (itemsPerView - 1)) / itemsPerView}px)` }}
                className="shrink-0"
              >
                <div
                  className={`h-full p-5 rounded-2xl border flex flex-col justify-between transition-all duration-300 relative overflow-hidden group hover:-translate-y-0.5 ${
                    isLight 
                      ? 'bg-white border-slate-300 hover:border-orange-500/60 shadow-md text-slate-800' 
                      : 'bg-zinc-950/80 border-white/10 hover:border-orange-500/50 shadow-xl text-zinc-200'
                  }`}
                >
                  {/* Subtle Top Indicator Accent */}
                  <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-orange-500/40 via-amber-500/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

                  <div className="space-y-3">
                    {/* Top Row: Category Icon & Tag */}
                    <div className="flex items-center justify-between gap-2">
                      <span className={`text-[9px] font-mono px-2 py-0.5 rounded-full border font-bold uppercase tracking-wider ${item.badgeColor}`}>
                        {item.tag}
                      </span>
                      <div className="flex items-center gap-1.5 text-zinc-400">
                        {item.category === 'government' && <Landmark className="w-3.5 h-3.5 text-orange-400" />}
                        {item.category === 'multilateral' && <Globe className="w-3.5 h-3.5 text-blue-400" />}
                        {item.category === 'industry' && <Building2 className="w-3.5 h-3.5 text-purple-400" />}
                        {item.category === 'academia' && <GraduationCap className="w-3.5 h-3.5 text-indigo-400" />}
                      </div>
                    </div>

                    {/* Partner Name & Subtitle */}
                    <div>
                      <h4 className={`text-base font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'} group-hover:text-orange-500 transition-colors`}>
                        {item.name}
                      </h4>
                      <p className={`text-[11px] font-mono mt-0.5 leading-snug ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                        {item.fullName}
                      </p>
                    </div>

                    {/* Core Role */}
                    <div className={`p-2 rounded-xl text-xs font-semibold leading-snug ${
                      isLight ? 'bg-slate-100 text-slate-900' : 'bg-white/5 text-zinc-200'
                    }`}>
                      {item.role}
                    </div>

                    {/* Standards / Alignment Details */}
                    <p className={`text-justify text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                      {item.standardsNote}
                    </p>
                  </div>

                  {/* Footer Action Trigger */}
                  <div className="pt-3 mt-3 border-t border-black/10 dark:border-white/10 flex items-center justify-between">
                    <span className="text-[10px] font-mono text-zinc-500 flex items-center gap-1">
                      <ShieldCheck className="w-3 h-3 text-emerald-500" />
                      <span>SADC Standard</span>
                    </span>

                    <button
                      onClick={() => onRequestBriefing?.(`Inquiry on institutional alignment and standards collaboration with ${item.name}`)}
                      className="text-[11px] font-mono font-bold text-orange-500 hover:text-orange-400 flex items-center gap-1 cursor-pointer transition-colors"
                    >
                      <span>Engage Protocol</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </motion.div>
        </div>

        {/* Carousel Pagination Indicator Dots */}
        <div className="flex items-center justify-between pt-4 mt-2">
          <span className="text-[10px] font-mono text-zinc-500">
            Showing slide {currentIndex + 1} of {Math.max(1, maxIndex + 1)} ({filteredItems.length} institutional entities)
          </span>

          <div className="flex items-center gap-1.5">
            {Array.from({ length: maxIndex + 1 }).map((_, dotIdx) => (
              <button
                key={dotIdx}
                onClick={() => setCurrentIndex(dotIdx)}
                aria-label={`Go to slide ${dotIdx + 1}`}
                className={`h-1.5 rounded-full transition-all cursor-pointer ${
                  currentIndex === dotIdx
                    ? 'w-6 bg-orange-500 shadow-[0_0_6px_rgba(249,115,22,0.8)]'
                    : isLight 
                      ? 'w-1.5 bg-slate-300 hover:bg-slate-400' 
                      : 'w-1.5 bg-white/20 hover:bg-white/40'
                }`}
              />
            ))}
          </div>
        </div>

      </div>
    </section>
  );
};
