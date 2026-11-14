import React from 'react';
import { ScrimPanel } from './ScrimPanel';

interface HomeSectionProps {
  id: string;
  label: string;
  theme: 'light' | 'dark';
  scrim?: boolean;
  className?: string;
  bgImage?: string;
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
}

export const HomeSection: React.FC<HomeSectionProps> = ({
  id,
  label,
  theme,
  scrim = true,
  className = '',
  bgImage,
  variant = 'primary',
  children,
}) => {
  const isLight = theme === 'light';
  const bgClass = variant === 'secondary'
    ? (isLight ? 'bg-[#F2F2F2] text-ls-navy' : 'bg-[#1A1D21] text-white')
    : (isLight ? 'bg-[#F7F8F9] text-ls-navy' : 'bg-[#121518] text-white');

  return (
    <section
      id={id}
      aria-label={label}
      tabIndex={-1}
      className={`relative w-full py-[100px] px-6 lg:px-12 scroll-mt-28 overflow-hidden transition-colors ${bgClass} ${className}`}
    >
      {bgImage && (
        <div
          className="absolute inset-0 z-0 pointer-events-none"
          style={{
            backgroundImage: `url(${bgImage})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            opacity: 0.12,
          }}
        />
      )}
      <div className="relative z-10 max-w-7xl mx-auto w-full">
        {scrim ? <ScrimPanel theme={theme}>{children}</ScrimPanel> : children}
      </div>
    </section>
  );
};

export default HomeSection;
