/**
 * PageContainer Component
 *
 * Max-width wrapper with consistent padding and background
 * Directive §7, §33
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export type PageContainerSize = 'default' | 'narrow' | 'wide' | 'full';

export interface PageContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: PageContainerSize;
  padding?: boolean;
  background?: 'page' | 'surface' | 'transparent';
}

export const PageContainer = React.forwardRef<HTMLDivElement, PageContainerProps>(
  (
    {
      size = 'default',
      padding = true,
      background = 'page',
      className = '',
      children,
      style,
      ...props
    },
    ref
  ) => {
    const isDark = document.documentElement.classList.contains('dark');
    const colorTokens = tokens.colors;

    const sizeStyles: Record<PageContainerSize, React.CSSProperties> = {
      default: { maxWidth: tokens.spacing.container.maxWidth },
      narrow: { maxWidth: '720px' },
      wide: { maxWidth: '1400px' },
      full: { maxWidth: '100%' },
    };

    const backgroundStyles: Record<string, React.CSSProperties> = {
      page: { backgroundColor: isDark ? colorTokens.deepMineral : colorTokens.morningMist },
      surface: { backgroundColor: isDark ? colorTokens.navy : colorTokens.white },
      transparent: { backgroundColor: 'transparent' },
    };

    const paddingStyle: React.CSSProperties = padding
      ? {
          paddingLeft: tokens.spacing[12],
          paddingRight: tokens.spacing[12],
        }
      : {};

    const combinedStyle: React.CSSProperties = {
      width: '100%',
      margin: '0 auto',
      boxSizing: 'border-box',
      minHeight: '100%',
      ...sizeStyles[size],
      ...backgroundStyles[background],
      ...paddingStyle,
      ...style,
    };

    return (
      <div
        ref={ref}
        className={className}
        style={combinedStyle}
        {...props}
      >
        {children}
      </div>
    );
  }
);

PageContainer.displayName = 'PageContainer';

export default PageContainer;
