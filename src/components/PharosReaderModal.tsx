import React, { useState } from 'react';
import { X, Download, Clock, Calendar, Share2, Shield, Info } from 'lucide-react';

interface Publication {
  id: string;
  title: string;
  subtitle: string;
  category: string;
  readTime: string;
  date: string;
  abstract: string;
  content: string[];
}

interface PharosReaderModalProps {
  publication: Publication | null;
  isOpen: boolean;
  onClose: () => void;
  theme?: 'light' | 'dark';
}

export const PharosReaderModal: React.FC<PharosReaderModalProps> = ({
  publication,
  isOpen,
  onClose,
  theme = 'dark',
}) => {
  const [downloadNotice, setDownloadNotice] = useState<string | null>(null);
  const [copyStatus, setCopyStatus] = useState<string | null>(null);

  if (!isOpen || !publication) return null;

  const isLight = theme === 'light';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-in fade-in duration-200">
      <div
        className={`rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden relative ${
          isLight ? 'bg-ls-white text-ls-navy' : 'bg-slate-900 text-white'
        }`}
      >
        {/* Modal Header */}
        <div
          className={`px-8 py-6 flex items-center justify-between shrink-0 ${
            isLight ? 'bg-ls-grey-light/80' : 'bg-slate-950'
          }`}
        >
          <div>
            <span
              className={`text-xs font-semibold uppercase tracking-widest ${
                isLight ? 'text-cyan-700' : 'text-cyan-400'
              }`}
            >
              Pharos Insights · {publication.category}
            </span>
            <h2 className={`text-xl font-bold mt-1 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
              {publication.title}
            </h2>
          </div>
          <button
            onClick={onClose}
            className={`btn-milled p-2.5 rounded-full transition-all cursor-pointer ${
              isLight
                ? 'bg-ls-white text-ls-navy shadow-[inset_0_1px_1px_rgba(255,255,255,0.8),0_2px_6px_rgba(7,10,64,0.08)] hover:bg-ls-navy/10'
                : 'bg-slate-800 text-slate-300 hover:text-white shadow-[inset_0_1px_1px_rgba(255,255,255,0.2),0_2px_6px_rgba(0,0,0,0.4)]'
            }`}
            aria-label="Close reader"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body / Reader Content */}
        <div
          className={`p-8 overflow-y-auto space-y-6 ${
            isLight ? 'text-ls-navy' : 'text-slate-300'
          }`}
        >
          {/* Metadata bar */}
          <div
            className={`flex flex-wrap items-center gap-6 pb-6 text-xs ${
              isLight ? 'text-ls-grey-dark' : 'text-slate-400'
            }`}
          >
            <span className="flex items-center gap-1.5">
              <Calendar className={`w-4 h-4 ${isLight ? 'text-cyan-700' : 'text-cyan-400'}`} /> {publication.date}
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className={`w-4 h-4 ${isLight ? 'text-cyan-700' : 'text-cyan-400'}`} /> {publication.readTime}
            </span>
            <span className="flex items-center gap-1.5">
              <Shield className={`w-4 h-4 ${isLight ? 'text-cyan-700' : 'text-cyan-400'}`} /> Foundational Research
            </span>
          </div>

          <div>
            <h3 className={`text-lg font-bold font-display mb-2.5 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
              Executive Abstract
            </h3>
            <div
              className={`text-sm sm:text-base leading-relaxed p-5 rounded-2xl ${
                isLight
                  ? 'bg-cyan-50/90 text-slate-800 border border-cyan-200/80 shadow-sm'
                  : 'bg-cyan-950/50 text-slate-100 border border-cyan-500/30 shadow-md'
              }`}
            >
              {publication.abstract}
            </div>
          </div>

          <div className="p-6 sm:p-8 rounded-2xl longform-contrast-layer space-y-4">
            <h3 className={`text-lg font-bold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>
              Research Analysis &amp; Findings
            </h3>
            <div className="space-y-4">
              {publication.content.map((paragraph, index) => (
                <p
                  key={index}
                  className={`text-sm sm:text-base leading-relaxed ${isLight ? 'text-slate-800' : 'text-slate-100'}`}
                >
                  {paragraph}
                </p>
              ))}
            </div>
          </div>

          <div
            className={`p-6 rounded-xl flex flex-col sm:flex-row items-center justify-between gap-4 mt-8 ${
              isLight
                ? 'bg-ls-grey-light/70'
                : 'bg-slate-950'
            }`}
          >
            <div>
              <h4 className={`text-sm font-bold ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                Download Complete Whitepaper
              </h4>
              <p className={`text-xs ${isLight ? 'text-ls-grey-dark' : 'text-slate-400'}`}>
                Full PDF report export endpoint will be enabled in the OpenCode environment.
              </p>
              {downloadNotice && (
                <p className="text-xs text-cyan-600 dark:text-cyan-400 mt-1 flex items-center gap-1">
                  <Info className="w-3.5 h-3.5 shrink-0" />
                  {downloadNotice}
                </p>
              )}
            </div>
            <button
              onClick={() => {
                setDownloadNotice('PDF report generation endpoint is scheduled for OpenCode integration.');
                setTimeout(() => setDownloadNotice(null), 4000);
              }}
              className="btn-milled btn-milled-primary px-6 py-3 rounded-full text-xs font-bold transition-all flex items-center gap-2 shrink-0 cursor-pointer"
            >
              <Download className="w-4 h-4" /> PDF Report (OpenCode Integration)
            </button>
          </div>
        </div>

        {/* Modal Footer */}
        <div
          className={`px-8 py-4 flex items-center justify-between text-xs shrink-0 ${
            isLight
              ? 'bg-ls-grey-light/80 text-ls-grey-dark'
              : 'bg-slate-950 text-slate-500'
          }`}
        >
          <span>LightSpeed Holdings Limited™ · Pharos Insights</span>
          <button
            onClick={() => {
              if (navigator?.clipboard?.writeText) {
                navigator.clipboard.writeText(window.location.href);
              }
              setCopyStatus('Link copied');
              setTimeout(() => setCopyStatus(null), 2500);
            }}
            className={`btn-milled btn-milled-secondary px-4 py-2 rounded-full flex items-center gap-1.5 cursor-pointer text-xs`}
          >
            <Share2 className="w-3.5 h-3.5" /> {copyStatus || 'Share Article'}
          </button>
        </div>
      </div>
    </div>
  );
};
