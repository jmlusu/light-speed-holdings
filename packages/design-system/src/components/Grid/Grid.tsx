/**
 * Grid Component
 *
 * Responsive grid layout with design system spacing
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export interface GridProps extends React.HTMLAttributes<HTMLDivElement> {
  columns?: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;
  columnsTablet?: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;
  columnsDesktop?: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;
  gap?: keyof typeof tokens.spacing | 'component' | 'tight';
  gapTablet?: keyof typeof tokens.spacing | 'component' | 'tight';
  gapDesktop?: keyof typeof tokens.spacing | 'component' | 'tight';
}

const gapValues: Record<string, string> = {
  '1': '4px',
  '2': '8px',
  '3': '12px',
  '4': '16px',
  '6': '24px',
  '8': '32px',
  '12': '48px',
  '16': '64px',
  '24': '96px',
  component: '24px',
  tight: '12px',
};

export const Grid = React.forwardRef<HTMLDivElement, GridProps>(
  (
    {
      columns = 1,
      columnsTablet,
      columnsDesktop,
      gap = 'component',
      gapTablet,
      gapDesktop,
      className = '',
      children,
      style,
      ...props
    },
    ref
  ) => {
    const baseGap = gapValues[gap] || tokens.spacing[6];
    const tabletGap = gapTablet ? gapValues[gapTablet] || tokens.spacing[6] : baseGap;
    const desktopGap = gapDesktop ? gapValues[gapDesktop] || tokens.spacing[6] : baseGap;

    const gridStyle: React.CSSProperties = {
      display: 'grid',
      gridTemplateColumns: `repeat(${columns}, 1fr)`,
      gap: baseGap,
      ...style,
    };

    // Responsive grid via CSS custom properties for media queries
    const responsiveStyle: React.CSSProperties = {
      ...gridStyle,
      '--grid-columns': String(columns),
      '--grid-gap': baseGap,
      '--grid-columns-tablet': String(columnsTablet || columns),
      '--grid-gap-tablet': tabletGap,
      '--grid-columns-desktop': String(columnsDesktop || columnsTablet || columns),
      '--grid-gap-desktop': desktopGap,
    } as React.CSSProperties;

    return (
      <div
        ref={ref}
        className={className}
        style={responsiveStyle}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Grid.displayName = 'Grid';

export default Grid;
