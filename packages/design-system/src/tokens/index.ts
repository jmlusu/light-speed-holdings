/**
 * Design Tokens — Barrel Export
 *
 * Single entry point for all design tokens
 * Directive §7 — ONE machine-readable token source
 */

export * from './colors';
export * from './typography';
export * from './spacing';
export * from './visual';

import { colors } from './colors';
import { typography } from './typography';
import { spacing } from './spacing';
import { shadows, radius, breakpoints, motion } from './visual';

export const tokens = {
  colors,
  typography,
  spacing,
  shadows,
  radius,
  breakpoints,
  motion,
} as const;

export type Tokens = typeof tokens;
