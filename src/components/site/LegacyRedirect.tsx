import React from 'react';
import { Link, Navigate, useLocation } from 'react-router-dom';

export interface LegacyRedirectProps { to: string; label: string; }
export interface LegacyRedirectNoticeProps { from: string; label?: string; to: string; }

export const LegacyRedirect: React.FC<LegacyRedirectProps> = ({ to, label }) => {
  const { pathname } = useLocation();
  return <Navigate to={to} replace state={{ legacyFrom: pathname, legacyLabel: label }} />;
};

export const LegacyRedirectNotice: React.FC<LegacyRedirectNoticeProps> = ({ from, label, to }) => (
  <div role="status" aria-live="polite" data-testid="legacy-redirect-notice"
    className="mb-6 rounded-2xl border border-ls-cyan/40 bg-ls-cyan/10 px-5 py-4 font-body text-sm text-ls-navy dark:text-white">
    <p className="font-bold">
      You followed an old link to {label ? <strong>{label}</strong> : <code>{from}</code>} ({from}). It has moved.
    </p>
    <p className="mt-1">
      This is the current home for that content:{' '}
      <Link to={to} className="font-bold underline">{to}</Link>
    </p>
  </div>
);
