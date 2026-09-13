import React from 'react';
import { Link } from 'react-router-dom';

interface SiteFooterProps {
  theme: 'light' | 'dark';
}

interface FooterColumn {
  heading: string;
  links: { name: string; to: string }[];
}

const COLUMNS: FooterColumn[] = [
  {
    heading: 'SOLUTIONS',
    links: [
      { name: 'Agentic AI', to: '/solutions/agentic-ai' },
      { name: 'Digital Transformation', to: '/solutions/digital-transformation' },
      { name: 'Data & Intelligence', to: '/solutions/data-intelligence' },
      { name: 'Intelligent Automation', to: '/solutions/automation' },
      { name: 'Strategy & Advisory', to: '/solutions/strategy-advisory' },
      { name: 'AI Governance & Policy', to: '/technology#governance' },
    ],
  },
  {
    heading: 'INDUSTRIES',
    links: [
      { name: 'Government', to: '/industries/government' },
      { name: 'Development & Donor', to: '/industries/development' },
      { name: 'Financial Services', to: '/industries/financial-services' },
      { name: 'Healthcare', to: '/industries/healthcare' },
      { name: 'Agriculture', to: '/industries/agriculture' },
    ],
  },
  {
    heading: 'AI COMPANY BUILDER',
    links: [
      { name: 'Overview', to: '/ai-company-builder' },
      { name: 'Technology', to: '/technology' },
      { name: 'Start a Conversation', to: '/contact' },
    ],
  },
  {
    heading: 'TECHNOLOGY',
    links: [
      { name: 'Architecture', to: '/technology#architecture' },
      { name: 'Technical Proof', to: '/technology#proof' },
      { name: 'Security & Governance', to: '/technology#governance' },
    ],
  },
  {
    heading: 'COMPANY',
    links: [
      { name: 'About', to: '/about' },
      { name: 'Work', to: '/work' },
      { name: 'Insights', to: '/insights' },
      { name: 'Contact', to: '/contact' },
    ],
  },
  {
    heading: 'LEGAL',
    links: [
      { name: 'Privacy Policy', to: '/legal/privacy' },
      { name: 'Terms of Service', to: '/legal/terms' },
    ],
  },
];

export const SiteFooter: React.FC<SiteFooterProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <footer
      className={`px-4 sm:px-8 pt-14 pb-10 max-w-7xl mx-auto w-full border-t mt-16 sm:mt-20 ${
        isLight ? 'border-slate-200' : 'border-white/15'
      }`}
    >
      <div className="flex flex-wrap items-start justify-between gap-x-8 gap-y-6 pb-10 mb-10 border-b ${
        isLight ? 'border-slate-200' : 'border-white/10'
      }">
        <div>
          <div className="inline-flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-full border border-white/30 bg-ls-red flex items-center justify-center text-white shadow-md">
              <span className="font-black text-sm tracking-widest font-sans">LS</span>
            </div>
            <div className="flex flex-col">
              <span className={`text-xs font-black tracking-widest font-sans ${
                isLight ? 'text-slate-900' : 'text-zinc-100'
              }`}>
                LightSpeed Holdings™
              </span>
              <span className={`text-[10px] font-mono tracking-wider font-bold ${
                isLight ? 'text-slate-500' : 'text-zinc-500'
              }`}>
                LILONGWE, MALAWI // ASPIRE. ACT. ACHIEVE.
              </span>
            </div>
          </div>
          <p className={`mt-4 max-w-sm text-xs leading-relaxed ${
            isLight ? 'text-slate-600' : 'text-zinc-400'
          }`}>
            LightSpeed Holdings Limited builds and governs agentic AI systems for organizations — proving the model in Malawi first, then across SADC and beyond.
          </p>
        </div>

        <div className={`text-xs leading-relaxed max-w-xs ${
          isLight ? 'text-slate-600' : 'text-zinc-400'
        }`}>
          <span className={`font-mono text-[10px] font-bold tracking-widest text-ls-red`}>NORTH STAR</span>
          <p className="mt-2">Malawi first. Prove it. Then the world.</p>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-x-6 gap-y-10">
        {/* Link columns */}
        {COLUMNS.map((col) => (
          <nav key={col.heading} aria-label={col.heading}>
            <h3 className={`text-[10px] font-mono font-bold tracking-widest ${
              isLight ? 'text-ls-red' : 'text-ls-red'
            }`}>
              {col.heading}
            </h3>
            <ul className="mt-4 space-y-2.5">
              {col.links.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.to}
                    className={`text-xs font-medium transition-colors cursor-pointer ${
                      isLight ? 'text-slate-700 hover:text-ls-red' : 'text-zinc-300 hover:text-ls-red'
                    }`}
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        ))}
      </div>

      <div className={`mt-12 pt-6 border-t flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] font-mono ${
        isLight ? 'border-slate-200 text-slate-500' : 'border-white/10 text-zinc-500'
      }`}>
        <span>© {new Date().getFullYear()} LightSpeed Holdings Limited. All rights reserved.</span>
        <span className="font-bold tracking-wider">'PROOF, THEN SCALE.' — MALAWI FIRST.</span>
      </div>
    </footer>
  );
};

export default SiteFooter;
