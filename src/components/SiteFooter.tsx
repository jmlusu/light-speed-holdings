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
    heading: 'LIGHTSPEED',
    links: [
      { name: 'Home', to: '/' },
      { name: 'What We Do', to: '/what-we-do' },
      { name: 'AI Company Builder', to: '/ai-company-builder' },
      { name: 'Solutions', to: '/solutions' },
      { name: 'Sectors', to: '/sectors' },
    ],
  },
  {
    heading: 'PROOF & INSIGHTS',
    links: [
      { name: 'Proof', to: '/proof' },
      { name: 'Insights', to: '/insights' },
      { name: 'About', to: '/about' },
    ],
  },
  {
    heading: 'CONNECT',
    links: [
      { name: 'Contact', to: '/contact' },
      { name: 'Ask LightSpeed', to: '/ask' },
      { name: 'Book a Briefing', to: '/contact' },
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
  const borderCls = isLight ? 'border-ls-grey-dark' : 'border-ls-white/15';
  const borderClsSub = isLight ? 'border-ls-grey-dark/10' : 'border-ls-white/10';
  const textCls = isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text';
  const textClsMuted = isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text';
  const linkCls = isLight
    ? 'text-ls-grey-dark hover:text-ls-red'
    : 'text-ls-grey-light-text hover:text-ls-red';
  const brandCls = isLight ? 'text-ls-navy' : 'text-ls-white';
  const tagCls = isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text';

  return (
    <footer className={`px-4 sm:px-8 pt-14 pb-10 max-w-7xl mx-auto w-full border-t mt-16 sm:mt-20 ${borderCls}`}>
      <div className={`flex flex-wrap items-start justify-between gap-x-8 gap-y-6 pb-10 mb-10 border-b ${borderClsSub}`}>
        <div>
          <div className="inline-flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-full border border-ls-white/30 bg-ls-red flex items-center justify-center text-ls-white shadow-md">
              <span className="font-black text-sm tracking-widest font-sans">LS</span>
            </div>
            <div className="flex flex-col">
              <span className={`text-xs font-black tracking-widest font-sans ${brandCls}`}>
                LightSpeed Holdings™
              </span>
              <span className={`text-[10px] font-body tracking-wider font-bold ${tagCls}`}>
                LILONGWE, MALAWI // ASPIRE. ACT. ACHIEVE.
              </span>
            </div>
          </div>
          <p className={`mt-4 max-w-sm text-xs leading-relaxed ${textCls}`}>
            LightSpeed Holdings Limited builds and governs agentic AI systems for organizations — proving the model in Malawi first, then across SADC and beyond.
          </p>
        </div>

        <div className={`text-xs leading-relaxed max-w-xs ${textCls}`}>
          <span className={`font-body text-[10px] font-bold tracking-widest text-ls-red`}>NORTH STAR</span>
          <p className="mt-2">Malawi first. Prove it. Then the world.</p>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-x-6 gap-y-10">
        {COLUMNS.map((col) => (
          <nav key={col.heading} aria-label={col.heading}>
            <h3 className={`text-[10px] font-body font-bold tracking-widest text-ls-red`}>
              {col.heading}
            </h3>
            <ul className="mt-4 space-y-2.5">
              {col.links.map((link) => (
                <li key={link.name}>
                  <Link to={link.to} className={`text-xs font-medium transition-colors cursor-pointer ${linkCls}`}>
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        ))}
      </div>

      <div className={`mt-12 pt-6 border-t flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] font-body ${borderCls} ${textClsMuted}`}>
        <span>LightSpeed Holdings Limited. All rights reserved.</span>
        <span className="font-bold tracking-wider">PROOF, THEN SCALE. - MALAWI FIRST.</span>
      </div>
    </footer>
  );
};

export default SiteFooter;
