/**
 * Design Tokens — Colors
 *
 * Single source of truth from brand/tokens/brand-tokens.json
 * Directive §5, §7
 */

export const colors = {
  // Brand Colors (Canonical)
  navy: '#070A40',
  red: '#E63946',
  cyan: '#00BFFF',
  morningMist: '#F7F8F9',
  deepMineral: '#121518',
  white: '#FFFFFF',

  // Supporting Neutrals
  grey: {
    50: '#F9FAFB',
    100: '#F2F2F2',
    200: '#E5E7EB',
    300: '#D1D5DB',
    400: '#9CA3AF',
    500: '#6B7280',
    600: '#4B5563',
    700: '#374151',
    800: '#1F2937',
    900: '#111827',
  },

  // Semantic Colors (Light Mode)
  light: {
    bgPrimary: '#F7F8F9',      // morningMist
    bgSurface: '#FFFFFF',      // white
    bgSurfaceElevated: '#FFFFFF',
    textPrimary: '#070A40',    // navy
    textSecondary: '#6B7280',  // grey-500
    textMuted: '#9CA3AF',      // grey-400
    borderDefault: '#E5E7EB',  // grey-200
    borderSubtle: '#F2F2F2',   // grey-100
    borderEmphasis: '#070A40', // navy
    borderFocus: '#00BFFF',    // cyan
    focusRing: '#00BFFF',      // cyan
  },

  // Semantic Colors (Dark Mode)
  dark: {
    bgPrimary: '#121518',      // deepMineral
    bgSurface: '#070A40',      // navy
    bgSurfaceElevated: '#1A1E24',
    textPrimary: '#FFFFFF',    // white
    textSecondary: '#9CA3AF',  // grey-400
    textMuted: '#6B7280',      // grey-500
    borderDefault: '#374151',  // grey-700
    borderSubtle: '#1F2937',   // grey-800
    borderEmphasis: '#00BFFF', // cyan
    borderFocus: '#00BFFF',    // cyan
    focusRing: '#00BFFF',      // cyan
  },

  // Honesty Badge Colors (from siteContent.ts TONE_STYLES)
  honesty: {
    proven: {
      border: 'rgba(0, 191, 255, 0.4)',
      background: 'rgba(0, 191, 255, 0.1)',
      text: '#00BFFF',
    },
    pilot: {
      border: 'rgba(230, 57, 70, 0.4)',
      background: 'rgba(230, 57, 70, 0.1)',
      text: '#E63946',
    },
    fieldable: {
      border: 'rgba(156, 163, 175, 0.4)',
      background: 'rgba(156, 163, 175, 0.1)',
      text: '#9CA3AF',
    },
    development: {
      border: 'rgba(107, 114, 128, 0.4)',
      background: 'rgba(107, 114, 128, 0.1)',
      text: '#6B7280',
    },
  },

  // Status Colors
  status: {
    success: '#00BFFF',   // cyan (not green - cyan is our trust signal)
    warning: '#E63946',   // red
    error: '#E63946',     // red
    info: '#00BFFF',      // cyan
  },

  // CTA Colors
  cta: {
    primary: {
      background: '#E63946',  // red
      text: '#FFFFFF',
      hover: 'rgba(230, 57, 70, 0.9)',
      shadow: 'rgba(230, 57, 70, 0.3)',
    },
    secondary: {
      border: '#070A40',      // navy (light) / #FFFFFF (dark)
      text: '#070A40',        // navy (light) / #FFFFFF (dark)
      hoverBackground: 'rgba(7, 10, 64, 0.05)',
    },
  },
} as const;

export type Colors = typeof colors;
