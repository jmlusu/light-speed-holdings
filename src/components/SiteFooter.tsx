import React from 'react';
import { Link } from 'react-router-dom';

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
        Ac {new Date().getFullYear()} LIGHTSPEED HOLDINGS LIMITED. All rights reserved. AI for Organizations Everywhere.
      </div>
      <div className={`flex flex-wrap items-center gap-x-4 gap-y-1 ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
        <Link to="/capabilities" className="hover:text-ls-red font-medium">Overview</Link>
        <Link to="/capabilities/offerings" className="hover:text-ls-red font-medium">Core Offerings</Link>
        <Link to="/capabilities/diagnostic" className="hover:text-ls-red font-medium">Diagnostic</Link>
        <Link to="/industries" className="hover:text-ls-red font-medium">Industries</Link>
        <Link to="/evidence" className="hover:text-ls-red font-medium">Evidence</Link>
        <Link to="/engagement" className="hover:text-ls-red font-medium">Engagement</Link>
        <Link to="/about" className="hover:text-ls-red font-medium">About</Link>
        <Link to="/insights" className="hover:text-ls-red font-medium">Insights</Link>
        <Link to="/contact" className="hover:text-ls-red font-medium">Contact</Link>
      </div>
    </footer>
  );
};
