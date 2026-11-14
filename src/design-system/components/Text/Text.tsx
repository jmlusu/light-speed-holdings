/**
 * Text Component
 *
 * Semantic text with design system typography
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export type TextVariant = 'body' | 'lead' | 'caption' | 'overline' | 'subtitle';

export interface TextProps extends React.HTMLAttributes<HTMLParagraphElement | HTMLSpanElement> {
  variant?: TextVariant;
  as?: React.ElementType;
  muted?: boolean;
  secondary?: boolean;
}

export const Text = React.forwardRef<HTMLParagraphElement, TextProps>(
  (
    {
      variant = 'body',
      as,
      muted = false,
      secondary = false,
      className = '',
      children,
      style,
      ...props
    },
    ref
  ) => {
    const Component = as || (variant === 'caption' || variant === 'overline' ? 'span' : 'p');

    const variantStyles: Record<TextVariant, React.CSSProperties> = {
      body: tokens.typography.styles.body,
      lead: tokens.typography.styles.subtitle,
      caption: tokens.typography.styles.caption,
      overline: tokens.typography.styles.overline,
      subtitle: tokens.typography.styles.subtitle,
    };

    const isDark = document.documentElement.classList.contains('dark');
    const colorTokens = tokens.colors;

    let color: string = isDark ? colorTokens.dark.textPrimary : colorTokens.light.textPrimary;
    if (muted) color = isDark ? colorTokens.dark.textMuted : colorTokens.light.textMuted;
    else if (secondary) color = isDark ? colorTokens.dark.textSecondary : colorTokens.light.textSecondary;

    const combinedStyle: React.CSSProperties = {
      ...variantStyles[variant],
      color,
      margin: 0,
      ...style,
    };

    return (
      <Component
        ref={ref}
        className={className}
        style={combinedStyle}
        {...props}
      >
        {children}
      </Component>
    );
  }
);

Text.displayName = 'Text';

export default Text;
