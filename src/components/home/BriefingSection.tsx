import React from 'react';
import { CtaBand } from '../site/CtaBand';

interface BriefingSectionProps {
  theme: 'light' | 'dark';
}

/**
 * Chapter 07 — wraps the shared CtaBand in the chapter section so the rail can
 * target it. CtaBand deliberately receives NO `id` prop: the id lives on this
 * section only.
 */
export const BriefingSection: React.FC<BriefingSectionProps> = ({ theme }) => (
  <section
    id="briefing"
    aria-label="Executive briefing"
    tabIndex={-1}
    className="scroll-mt-28"
  >
    <CtaBand theme={theme} />
  </section>
);

export default BriefingSection;
