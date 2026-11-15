import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '@/components/site/Logo.tsx';

interface SiteFooterProps {
  theme: 'light' | 'dark';
}

interface FooterLink {
  name: string;
  to: string;
  external?: boolean;
}

interface FooterColumn {
  heading: string;
  links: FooterLink[];
}

const COLUMNS: FooterColumn[] = [
  {
    heading: 'CAPABILITIES',
    links: [
      { name: 'What We Do', to: '/what-we-do' },
      { name: 'AI Company Builder', to: '/ai-company-builder' },
      { name: 'HAOMTGV Framework', to: '/haomtgv' },
      { name: 'Agent Registry', to: '/agent-registry' },
      { name: 'AI Assessment', to: '/ai-assessment' },
      { name: 'Operating Model', to: '/what-we-do' },
      { name: 'AI Venture Studio', to: '/ai-company-builder' },
    ],
  },
  {
    heading: 'RESEARCH & COMPANY',
    links: [
      { name: 'Pharos', to: '/insights' },
      { name: 'Who We Are', to: '/about' },
      { name: 'Frequently Asked Questions', to: '/faq' },
      { name: 'Contact', to: '/contact' },
      { name: 'Privacy Policy', to: '/legal/privacy' },
      { name: 'Terms of Service', to: '/legal/terms' },
    ],
  },
  {
    heading: 'CONNECT',
    links: [
      { name: 'Facebook', to: 'https://facebook.com', external: true },
      { name: 'X', to: 'https://x.com', external: true },
      { name: 'Instagram', to: 'https://instagram.com', external: true },
      { name: 'LinkedIn', to: 'https://linkedin.com', external: true },
    ],
  },
];

export const SiteFooter: React.FC<SiteFooterProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <footer className={`w-full pt-20 pb-12 mt-0 border-t relative overflow-hidden transition-colors duration-300 backdrop-blur-md shadow-2xl ${
      isLight
        ? 'bg-[#F2F2F2] border-slate-300 text-[#070A40]'
        : 'bg-[#070A40] border-ls-cyan/30 text-white shadow-[0_-10px_30px_rgba(0,0,0,0.8)]'
    }`}>
      {/* Background Architectural Sector Image (Uniform with Home Page Sections) */}
      <div className="absolute inset-0 pointer-events-none select-none overflow-hidden z-0">
        <img
          src="/src/assets/images/before_after_sector_bg_light_1793889809250.jpg"
          alt="LightSpeed Footer Architectural Sector Background"
          className="w-full h-full object-cover object-center transition-all duration-700 opacity-65 dark:opacity-75 filter saturate-110 brightness-100"
          loading="lazy"
        />
        {/* Uniform Atmospheric Scrim Overlay */}
        <div
          className={`absolute inset-0 transition-colors duration-500 ${
            isLight
              ? 'bg-gradient-to-b from-[#F2F2F2]/70 via-[#F2F2F2]/45 to-[#F2F2F2]/75'
              : 'bg-gradient-to-b from-[#070A40]/75 via-[#070A40]/50 to-[#070A40]/80'
          }`}
        />
      </div>

      <div className="px-6 lg:px-12 max-w-7xl mx-auto w-full relative z-10">
        {/* Top Header Block with Imposing Straight Divider */}
        <div className={`flex flex-wrap items-start justify-between gap-x-12 gap-y-10 pb-16 border-b ${
          isLight ? 'border-slate-300/60' : 'border-ls-cyan/20'
        }`}>
          <div className="max-w-sm">
            <div className="inline-flex items-center gap-3">
              <Link to="/" className="flex items-center gap-3 group cursor-pointer border-none">
                <Logo size={40} theme={theme} instance="repeat" />
              </Link>
              <div className="flex flex-col">
                <span className={`text-sm font-bold tracking-widest uppercase font-sans ${
                  isLight ? 'text-[#070A40]' : 'text-white'
                }`}>
                  LightSpeed Holdings Limited™
                </span>
                <span className={`text-[10px] tracking-[0.2em] font-bold font-mono ${
                  isLight ? 'text-ls-red' : 'text-ls-cyan'
                }`}>
                  LILONGWE, MALAWI // ASPIRE. ACT. ACHIEVE.
                </span>
              </div>
            </div>
            <p className={`mt-6 text-sm leading-relaxed font-sans ${
              isLight ? 'text-slate-600' : 'text-[#9CA3AF]'
            }`}>
              LightSpeed Holdings Limited™ is an AI-Native Company Builder transforming human intent into governed, intelligent, and executable business operations.
            </p>
          </div>

          <div className={`flex flex-col gap-3 p-5 border rounded-xl backdrop-blur-md transition-colors duration-300 ${
            isLight
              ? 'border-slate-300 bg-white/60 shadow-sm'
              : 'border-ls-cyan/30 bg-[#070A40]/80'
          }`}>
            <div className="flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full shadow-[0_0_8px] ${
                isLight ? 'bg-ls-red shadow-ls-red/40' : 'bg-ls-cyan shadow-[#00BFFF]'
              }`} />
              <span className={`text-[10px] font-bold tracking-[0.2em] uppercase font-sans ${
                isLight ? 'text-ls-red' : 'text-ls-cyan'
              }`}>
                North Star
              </span>
            </div>
            <p className={`text-xl font-bold leading-tight font-sans ${
              isLight ? 'text-[#070A40]' : 'text-white'
            }`}>
              We build AI-native companies.
            </p>
            <div className={`text-[10px] font-mono tabular-nums pt-1 border-t ${
              isLight ? 'border-slate-200 text-slate-500' : 'border-white/10 text-[#9CA3AF]'
            }`}>
              FRAMEWORK: HAOMTGV // GOV: TIER-5 VERIFIED
            </div>
          </div>
        </div>

        {/* Sharp Column Divisions */}
        <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-0 py-16 border-b ${
          isLight ? 'border-slate-300/60' : 'border-white/10'
        }`}>
          {COLUMNS.map((col, idx) => (
            <nav
              key={col.heading}
              aria-label={col.heading}
              className={`p-4 sm:p-6 border-b sm:border-b-0 ${
                isLight ? 'border-slate-200' : 'border-white/10'
              } ${
                idx !== COLUMNS.length - 1 ? `sm:border-r ${isLight ? 'border-slate-200' : 'border-white/10'}` : ''
              }`}
            >
              <h3 className="text-[11px] font-bold tracking-[0.2em] text-ls-red uppercase mb-6 font-sans flex items-center gap-2">
                <span className="w-1 h-3 bg-ls-red inline-block" />
                {col.heading}
              </h3>
              <ul className="space-y-3.5">
                {col.links.map((link) => (
                  <li key={link.name}>
                    {link.external ? (
                      <a
                        href={link.to}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={`text-[13px] font-normal transition-colors cursor-pointer border-b border-transparent block py-0.5 ${
                          isLight
                            ? 'text-slate-600 hover:text-ls-red hover:border-ls-red'
                            : 'text-[#9CA3AF] hover:text-ls-cyan hover:border-ls-cyan'
                        }`}
                      >
                        {link.name}
                      </a>
                    ) : (
                      <Link
                        to={link.to}
                        className={`text-[13px] font-normal transition-colors cursor-pointer border-b border-transparent block py-0.5 ${
                          isLight
                            ? 'text-slate-600 hover:text-ls-red hover:border-ls-red'
                            : 'text-[#9CA3AF] hover:text-ls-cyan hover:border-ls-cyan'
                        }`}
                      >
                        {link.name}
                      </Link>
                    )}
                  </li>
                ))}
              </ul>
            </nav>
          ))}
        </div>

        {/* Bottom Legal & Telemetry Metadata */}
        <div className={`pt-10 flex flex-col md:flex-row items-center justify-between gap-6 text-[11px] ${
          isLight ? 'text-slate-500' : 'text-[#9CA3AF]'
        }`}>
          <div className="flex flex-col gap-1 text-center md:text-left font-sans">
            <span className={isLight ? 'text-slate-700' : 'text-slate-300'}>© {new Date().getFullYear()} LightSpeed Holdings Limited. All rights reserved.</span>
            <span className={isLight ? 'text-slate-500' : 'text-slate-500'}>Illustrations and architectural diagrams are original vector artwork created in-house.</span>
          </div>
          <div className={`flex items-center gap-4 font-mono text-[10px] tracking-wider uppercase ${
            isLight ? 'text-ls-red' : 'text-ls-cyan'
          }`}>
            <span className="inline-flex items-center gap-1.5">
              <span className={`w-1.5 h-1.5 shadow-[0_0_6px] ${
                isLight ? 'bg-ls-red shadow-ls-red/40' : 'bg-ls-cyan shadow-[#00BFFF]'
              }`} />
              ACTIVE OPERATING MODEL
            </span>
            <span className={isLight ? 'text-slate-300' : 'text-white/20'}>|</span>
            <span className={`font-bold tracking-widest uppercase ${
              isLight ? 'text-[#070A40]' : 'text-white'
            }`}>AI-Native Operations.</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default SiteFooter;
