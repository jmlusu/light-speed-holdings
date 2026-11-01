import React from 'react';

/**
 * Inline line-style icon set (stroke = currentColor, no fill).
 *
 * The redesign spec calls for inline SVG line icons tinted cyan, not an icon
 * font or a sprite, so every glyph stays themeable, crisp at 2x and free of an
 * extra network request.
 */

export interface IconProps {
  className?: string;
}

const svgProps = {
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.4,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
  'aria-hidden': true,
  focusable: false,
};

/** Cog + spokes — agentic automation. */
export const AutomationIcon: React.FC<IconProps> = ({ className }) => (
  <svg {...svgProps} className={className}>
    <circle cx="12" cy="12" r="3.1" />
    <path d="M12 3.4v2.1M12 18.5v2.1M3.4 12h2.1M18.5 12h2.1M5.9 5.9l1.5 1.5M16.6 16.6l1.5 1.5M18.1 5.9l-1.5 1.5M7.4 16.6l-1.5 1.5" />
  </svg>
);

/** Two linked rings — systems integration. */
export const IntegrationIcon: React.FC<IconProps> = ({ className }) => (
  <svg {...svgProps} className={className}>
    <path d="M9.2 7.2H7.4a4.8 4.8 0 0 0 0 9.6h1.8" />
    <path d="M14.8 7.2h1.8a4.8 4.8 0 0 1 0 9.6h-1.8" />
    <path d="M8.4 12h7.2" />
  </svg>
);

/** Shield + check — governance and compliance. */
export const GovernanceIcon: React.FC<IconProps> = ({ className }) => (
  <svg {...svgProps} className={className}>
    <path d="M12 3.3 5.4 6v6c0 3.9 2.9 6.8 6.6 8.5 3.7-1.7 6.6-4.6 6.6-8.5V6L12 3.3Z" />
    <path d="m9.2 12.1 2 2 3.6-4" />
  </svg>
);

/** Bars + axis — data and analytics. */
export const DataIcon: React.FC<IconProps> = ({ className }) => (
  <svg {...svgProps} className={className}>
    <path d="M4 19.6h16" />
    <path d="M7.2 19.6v-5.4M12 19.6V8.4M16.8 19.6v-8.2" />
  </svg>
);

/** Stacked layers — AI company builder. */
export const BuilderIcon: React.FC<IconProps> = ({ className }) => (
  <svg {...svgProps} className={className}>
    <path d="m12 3.6 8 4.2-8 4.2-8-4.2 8-4.2Z" />
    <path d="m4 12.3 8 4.2 8-4.2" />
    <path d="m4 16.4 8 4.2 8-4.2" />
  </svg>
);

/** Arrow used by ArrowLink and the pill CTAs. */
export const ArrowRightIcon: React.FC<IconProps> = ({ className }) => (
  <svg {...svgProps} className={className}>
    <path d="M4.5 12h14" />
    <path d="m12.8 6.3 5.7 5.7-5.7 5.7" />
  </svg>
);
