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
    heading: 'WHAT WE DO',
    links: [
      { name: 'All Capabilities & Catalog', to: '/what-we-do' },
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
      { name: 'Interactive Lab', to: '/ai-company-builder' },
      { name: 'Technology', to: '/technology' },
      { name: 'Book a Briefing', to: '/contact' },
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
      { name: 'Proof & Evidence', to: '/proof' },
      { name: 'Insights // Pharos', to: '/insights' },
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
   {
     heading: 'EXPLORE',
     links: [
       { name: 'Why LightSpeed', to: '/why' },
       { name: 'How We Help', to: '/how-we-help' },
       { name: 'Process', to: '/process' },
       { name: 'FAQ', to: '/faq' },
       { name: 'Resources', to: '/resources' },
       { name: 'Events', to: '/events' },
       { name: 'News', to: '/news' },
       { name: 'Careers', to: '/careers' },
       { name: 'Geography', to: '/geography' },
       { name: 'Leadership', to: '/leadership' },
       { name: 'Partnerships', to: '/partnerships' },
       { name: 'Deliverables', to: '/deliverables' },
       { name: 'Outcomes', to: '/outcomes' },
       { name: 'Trust', to: '/trust' },
     ],
   },
 ];

export const SiteFooter: React.FC<SiteFooterProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <footer
      className={`px-4 sm:px-8 pt-14 pb-10 max-w-7xl mx-auto w-full border-t mt-16 sm:mt-20 ${
        isLight ? 'border-ls-grey-dark' : 'border-ls-white/15'
      }`}
    >
      <div className="flex flex-wrap items-start justify-between gap-x-8 gap-y-6 pb-10 mb-10 border-b ${
        isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'
      }">
        <div>
          <div className="inline-flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-full border border-ls-white/30 bg-ls-red flex items-center justify-center text-ls-white shadow-md">
              <span className="font-black text-sm tracking-widest font-sans">LS</span>
            </div>
            <div className="flex flex-col">
              <span className={`text-xs font-black tracking-widest font-sans ${
                isLight ? 'text-ls-navy' : 'text-ls-white'
              }`}>
                LightSpeed Holdings™
              </span>
              <span className={`text-[10px] font-body tracking-wider font-bold ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                LILONGWE, MALAWI // ASPIRE. ACT. ACHIEVE.
              </span>
            </div>
          </div>
          <p className={`mt-4 max-w-sm text-xs leading-relaxed ${
            isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
          }`}>
            LightSpeed Holdings Limited builds and governs agentic AI systems for organizations — proving the model in Malawi first, then across SADC and beyond.
          </p>
        </div>

        <div className={`text-xs leading-relaxed max-w-xs ${
          isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
        }`}>
          <span className={`font-body text-[10px] font-bold tracking-widest text-ls-red`}>NORTH STAR</span>
          <p className="mt-2">Malawi first. Prove it. Then the world.</p>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-x-6 gap-y-10">
        {/* Link columns */}
        {COLUMNS.map((col) => (
          <nav key={col.heading} aria-label={col.heading}>
            <h3 className={`text-[10px] font-body font-bold tracking-widest ${
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
                      isLight ? 'text-ls-grey-dark hover:text-ls-red' : 'text-ls-grey-light-text hover:text-ls-red'
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

      <div className={`mt-12 pt-6 border-t flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] font-body ${
        isLight ? 'border-ls-grey-dark text-ls-grey-dark' : 'border-ls-white/10 text-ls-grey-light-text'
      }`}>
        <span>© {new Date().getFullYear()} LightSpeed Holdings Limited. All rights reserved.</span>
        <span className="font-bold tracking-wider">'PROOF, THEN SCALE.' — MALAWI FIRST.</span>
      </div>
    </footer>
  );
};

export default SiteFooter;
