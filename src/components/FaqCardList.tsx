import React, { useState } from 'react';
import { Card } from '@lightspeed/design-system';
import { faqs } from '../data/faqs';
import { ChevronDown, Search, ShieldCheck } from 'lucide-react';

interface FaqCardListProps {
  theme: 'light' | 'dark';
}

export const FaqCardList: React.FC<FaqCardListProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const [searchQuery, setSearchQuery] = useState('');
  const [openIds, setOpenIds] = useState<Record<string, boolean>>({});

  const toggleFaq = (id: string) => {
    setOpenIds(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const filteredFaqs = faqs.filter(faq => 
    faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.registryId.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="w-full space-y-8">
      {/* Search Bar */}
      <div className="max-w-xl mx-auto relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
          <Search className="w-4 h-4" />
        </div>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search questions, registry IDs, or topics..."
          className={`w-full pl-11 pr-4 py-3.5 rounded-2xl text-sm font-sans transition-all outline-none ${
            isLight
              ? 'bg-white text-ls-navy border border-slate-300 shadow-sm focus:border-ls-cyan'
              : 'bg-slate-900/90 text-white border border-white/10 focus:border-ls-cyan shadow-lg'
          }`}
        />
      </div>

      {/* FAQ Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredFaqs.map((faq) => {
          const isOpen = openIds[faq.id] ?? false;
          return (
            <Card
              key={faq.id}
              variant="elevated"
              padding="lg"
              hover={true}
              className={`flex flex-col justify-between transition-all rounded-3xl ${
                isLight
                  ? 'bg-white border border-slate-200/90 shadow-sm hover:shadow-md'
                  : 'bg-ls-navy/85 border border-white/10 shadow-xl hover:border-ls-cyan/40'
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-3 mb-4">
                  <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-mono font-bold uppercase tracking-wider ${
                    isLight ? 'bg-cyan-50 text-cyan-700 border border-cyan-200' : 'bg-cyan-950/60 text-cyan-300 border border-cyan-800/40'
                  }`}>
                    <ShieldCheck className="w-3.5 h-3.5" />
                    Registry: {faq.registryId.toUpperCase()}
                  </span>
                  <span className={`text-[11px] font-mono ${isLight ? 'text-slate-500' : 'text-slate-400'}`}>
                    {faq.evidence.length} Evidence Source{faq.evidence.length === 1 ? '' : 's'}
                  </span>
                </div>

                <h3
                  onClick={() => toggleFaq(faq.id)}
                  className={`text-lg sm:text-xl font-bold font-display tracking-tight cursor-pointer flex items-center justify-between gap-4 select-none ${
                    isLight ? 'text-ls-navy hover:text-ls-red' : 'text-white hover:text-ls-cyan'
                  }`}
                >
                  <span>{faq.question}</span>
                  <ChevronDown className={`w-5 h-5 shrink-0 transition-transform duration-300 ${isOpen ? 'rotate-180 text-ls-cyan' : 'text-slate-400'}`} />
                </h3>

                {(isOpen || searchQuery.length > 0) && (
                  <div className="mt-4 pt-4 border-t border-slate-200 dark:border-white/10 animate-in fade-in duration-200 space-y-3">
                    <p className={`text-sm sm:text-base leading-relaxed ${isLight ? 'text-slate-700' : 'text-slate-200'}`}>
                      {faq.answer}
                    </p>

                    {/* Evidence Sources footer */}
                    <div className="pt-2 flex flex-wrap items-center gap-1.5 text-[11px] font-mono">
                      <span className={isLight ? 'text-slate-400 font-bold' : 'text-slate-500 font-bold'}>Evidence:</span>
                      {faq.evidence.map((ev, i) => (
                        <span key={i} className={`px-2 py-0.5 rounded text-[10px] ${
                          ev.status === 'verified'
                            ? isLight ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-emerald-950/60 text-emerald-300 border border-emerald-800/40'
                            : 'bg-amber-50 text-amber-700 border border-amber-200'
                        }`}>
                          {ev.source} ({ev.status})
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {!isOpen && searchQuery.length === 0 && (
                <button
                  onClick={() => toggleFaq(faq.id)}
                  className={`mt-6 pt-3 text-xs font-bold tracking-widest uppercase flex items-center gap-1.5 transition-colors cursor-pointer ${
                    isLight ? 'text-ls-red hover:text-ls-navy' : 'text-ls-cyan hover:text-white'
                  }`}
                >
                  <span>Read Answer</span>
                  <ChevronDown className="w-3.5 h-3.5" />
                </button>
              )}
            </Card>
          );
        })}
      </div>

      {filteredFaqs.length === 0 && (
        <div className={`text-center py-16 rounded-3xl ${isLight ? 'bg-white border border-slate-200' : 'bg-ls-navy/60 border border-white/10'}`}>
          <p className={`text-sm ${isLight ? 'text-slate-600' : 'text-slate-400'}`}>
            No frequently asked questions match &ldquo;{searchQuery}&rdquo;. Try another search term or contact our team directly.
          </p>
        </div>
      )}
    </div>
  );
};

export default FaqCardList;
