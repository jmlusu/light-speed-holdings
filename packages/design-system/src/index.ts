/**
 * Design System — Main Export
 *
 * Canonical entry point for all design system components, tokens, hooks, and utilities
 */

// Tokens
export * from './tokens';
export { tokens } from './tokens';

// Components
export { Button } from './components/Button/Button';
export type { ButtonProps } from './components/Button/Button';

export { Card } from './components/Card/Card';
export type { CardProps } from './components/Card/Card';

export { Badge } from './components/Badge/Badge';
export type { BadgeProps, BadgeVariant } from './components/Badge/Badge';

export { Heading } from './components/Heading/Heading';
export type { HeadingProps, HeadingLevel } from './components/Heading/Heading';

export { Text } from './components/Text/Text';
export type { TextProps, TextVariant } from './components/Text/Text';

export { Section } from './components/Section/Section';
export type { SectionProps } from './components/Section/Section';

export { Container } from './components/Container/Container';
export type { ContainerProps, ContainerSize } from './components/Container/Container';

export { Grid } from './components/Grid/Grid';
export type { GridProps } from './components/Grid/Grid';

export { Stack } from './components/Stack/Stack';
export type { StackProps, StackDirection, StackGap } from './components/Stack/Stack';

export { Logo } from './components/Logo/Logo';
export type { LogoProps, LogoVariant } from './components/Logo/Logo';

// Hooks
export { useTheme } from './hooks/useTheme';
export { useMediaQuery } from './hooks/useMediaQuery';
export { useReducedMotion } from './hooks/useReducedMotion';

// Utils
export { cn } from './utils/cn';
export { formatters } from './utils/formatters';
