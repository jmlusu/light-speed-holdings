import React from 'react';

export interface DomainTileProps {
  title: string;
  description?: string;
  to?: string;
  theme: 'light' | 'dark';
  active?: boolean;
  badge?: string;
}

export const DomainTile: React.FC<DomainTileProps> = ({
  title,
  description,
  to,
  theme,
  active = false,
  badge,
}) => {
  const isLight = theme === 'light';
  const titleColor = isLight ? 'text-ls-navy' : 'text-ls-white';

  return (
    <div>
      <h3 className={titleColor}>{title}</h3>
      {description && <p className="text-sm">{description}</p>}
      {badge && (
        <span className="inline-flex items-center gap-1 rounded-full border text-xs font-bold bg-ls-cyan/10 text-ls-cyan">
          {badge}
        </span>
      )}
    </div>
  );
};