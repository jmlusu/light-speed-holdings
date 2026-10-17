import React from 'react';

interface ScrimPanelProps {
  theme: 'light' | 'dark';
  /** Hero claims panel and chapter rail get a backdrop blur; section panels stay flat (perf). */
  blur?: boolean;
  className?: string;
  children: React.ReactNode;
}

/**
 * Translucent content panel that keeps DOM text legible over the WebGL stage.
 * Light: white wash. Dark: slate wash. `backdrop-blur` is reserved for the hero
 * claims panel — section scrims stay flat so we do not stack large blur layers.
 */
export const ScrimPanel: React.FC<ScrimPanelProps> = ({ theme, blur = false, className = '', children }) => {
  const isLight = theme === 'light';
  return (
    <div
      className={`rounded-3xl border p-6 sm:p-8 ${blur ? 'backdrop-blur-xl' : ''} ${
        isLight
          ? 'bg-ls-white/85 border-ls-grey-dark/25 text-ls-navy'
          : 'bg-ls-slate/85 border-ls-white/10 text-ls-white'
      } ${className}`}
    >
      {children}
    </div>
  );
};

export default ScrimPanel;
