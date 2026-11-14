import React from 'react';

interface ScrimPanelProps {
  theme: 'light' | 'dark';
  blur?: boolean;
  className?: string;
  children: React.ReactNode;
}

/**
 * Transparent content container adhering to the critical rule:
 * background: transparent, border: none, box-shadow: none.
 * Only text and images inside are visible.
 */
export const ScrimPanel: React.FC<ScrimPanelProps> = ({ className = '', children }) => {
  return (
    <div
      className={`p-0 bg-transparent shadow-none border-none ${className}`}
      style={{ background: 'transparent', boxShadow: 'none' }}
    >
      {children}
    </div>
  );
};

export default ScrimPanel;
