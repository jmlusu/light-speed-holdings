import React from 'react';

interface SiteFooterProps {
  theme: 'light' | 'dark';
}

export const SiteFooter: React.FC<SiteFooterProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <footer className={`py-12 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono ${
      isLight ? 'border-slate-200 text-slate-700' : 'border-white/15 text-zinc-300'
    }`}>
      <div>
        © {new Date().getFullYear()} LIGHTSPEED HOLDINGS LIMITED. All rights reserved. AI Transformation for SADC.
      </div>
      <div className={`flex items-center gap-4 ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
        <a href="#operating-model" className="hover:text-orange-500 font-medium">Model</a>
        <a href="#capabilities" className="hover:text-orange-500 font-medium">Capabilities</a>
        <a href="#diagnostic" className="hover:text-orange-500 font-medium">Diagnostic</a>
        <a href="#templates" className="hover:text-orange-500 font-medium">Templates</a>
        <a href="#publications" className="hover:text-orange-500 font-medium">Publications</a>
        <a href="#faq" className="hover:text-orange-500 font-medium">FAQ</a>
        <a href="#contact" className="hover:text-orange-500 font-medium">Contact</a>
      </div>
    </footer>
  );
};
