import React from 'react';
import { ScrimPanel } from './ScrimPanel';

interface HomeSectionProps {
  id: string;
  /** Accessible name — SectionHeading renders no id, so aria-labelledby targets do not exist. */
  label: string;
  theme: 'light' | 'dark';
  /** Wrap children in a translucent scrim. Off for sections with their own solid panel. */
  scrim?: boolean;
  className?: string;
  children: React.ReactNode;
}

/**
 * Chapter shell for the homepage: a `<section>` with a stable id for the
 * chapter rail, `scroll-mt` so native #hash jumps clear the fixed nav, and
 * `tabIndex={-1}` so the rail can move focus after a smooth scroll.
 */
export const HomeSection: React.FC<HomeSectionProps> = ({
  id,
  label,
  theme,
  scrim = true,
  className = '',
  children,
}) => (
  <section
    id={id}
    aria-label={label}
    tabIndex={-1}
    className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 scroll-mt-28 ${className}`}
  >
    {scrim ? <ScrimPanel theme={theme}>{children}</ScrimPanel> : children}
  </section>
);

export default HomeSection;
