/**
 * Design Tokens — Typography
 *
 * Source: brand/tokens/brand-tokens.json
 * Directive §5, §7
 *
 * Font Family: Arial (system font for performance and credibility)
 */

export const typography = {
  fontFamily: {
    sans: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
    mono: '"SF Mono", "Fira Code", Monaco, monospace',
  },

  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    black: 900,
  },

  fontSize: {
    displayXl: '36pt',   // 48px - Hero headlines, cover titles
    titleXl: '32pt',     // 42.7px - Major section titles
    titleLg: '28pt',     // 37.3px - Section titles
    titleMd: '24pt',     // 32px - Subsection titles
    titleSm: '18pt',     // 24px - Card titles
    subtitle: '16pt',    // 21.3px - Lead paragraphs, intros
    bodyLg: '16pt',      // 21.3px - Body text (comfortable reading)
    body: '14pt',        // 18.7px - Default body text
    bodySm: '13pt',      // 17.3px - Secondary body
    caption: '12pt',     // 16px - Captions, footnotes, disclaimers
    overline: '11pt',    // 14.7px - Uppercase labels, badges
  },

  lineHeight: {
    tight: 1.1,
    snug: 1.15,
    normal: 1.25,
    relaxed: 1.5,
    loose: 1.6,
  },

  letterSpacing: {
    tight: '-0.02em',
    normal: '0',
    wide: '0.02em',
    wider: '0.1em',  // For uppercase labels
  },

  // Semantic Typography Styles
  styles: {
    displayXl: {
      fontSize: '36pt',
      lineHeight: 1.1,
      fontWeight: 700,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
      letterSpacing: '-0.02em',
    },
    titleXl: {
      fontSize: '32pt',
      lineHeight: 1.15,
      fontWeight: 700,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
      letterSpacing: '-0.02em',
    },
    titleLg: {
      fontSize: '28pt',
      lineHeight: 1.2,
      fontWeight: 700,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
      letterSpacing: '-0.02em',
    },
    titleMd: {
      fontSize: '24pt',
      lineHeight: 1.25,
      fontWeight: 700,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
      letterSpacing: '-0.02em',
    },
    titleSm: {
      fontSize: '18pt',
      lineHeight: 1.3,
      fontWeight: 700,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
    },
    subtitle: {
      fontSize: '16pt',
      lineHeight: 1.5,
      fontWeight: 400,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
    },
    bodyLg: {
      fontSize: '16pt',
      lineHeight: 1.6,
      fontWeight: 400,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
    },
    body: {
      fontSize: '14pt',
      lineHeight: 1.6,
      fontWeight: 400,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
    },
    bodySm: {
      fontSize: '13pt',
      lineHeight: 1.5,
      fontWeight: 400,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
    },
    caption: {
      fontSize: '12pt',
      lineHeight: 1.4,
      fontWeight: 400,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
    },
    overline: {
      fontSize: '11pt',
      lineHeight: 1.3,
      fontWeight: 700,
      fontFamily: 'Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif',
      textTransform: 'uppercase',
      letterSpacing: '0.1em',
    },
  },
} as const;

export type Typography = typeof typography;
