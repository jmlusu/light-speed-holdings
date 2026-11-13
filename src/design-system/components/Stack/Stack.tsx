/**
 * Stack Component
 *
 * Vertical or horizontal stack with consistent spacing
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export type StackDirection = 'vertical' | 'horizontal';
export type StackGap = keyof typeof tokens.spacing | 'component' | 'tight' | 'loose';

export interface StackProps extends React.HTMLAttributes<HTMLDivElement> {
  direction?: StackDirection;
  gap?: StackGap;
  align?: 'start' | 'center' | 'end' | 'stretch';
  justify?: 'start' | 'center' | 'end' | 'between' | 'around';
  wrap?: boolean;
  divider?: React.ReactNode;
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
  loose: '32px',
};

const directionMap: Record<StackDirection, React.CSSProperties['flexDirection']> = {
  vertical: 'column',
  horizontal: 'row',
};

export const Stack = React.forwardRef<HTMLDivElement, StackProps>(
  (
    {
      direction = 'vertical',
      gap = 'component',
      align = 'stretch',
      justify = 'start',
      wrap = false,
      divider,
      className = '',
      children,
      style,
      ...props
    },
    ref
  ) => {
    const gapValue = gapValues[gap] || tokens.spacing[6];

    const stackStyle: React.CSSProperties = {
      display: 'flex',
      flexDirection: directionMap[direction],
      flexWrap: wrap ? 'wrap' : 'nowrap',
      alignItems: align,
      justifyContent: justify,
      gap: gapValue,
      ...style,
    };

    const childrenArray = React.Children.toArray(children);

    return (
      <div
        ref={ref}
        className={className}
        style={stackStyle}
        {...props}
      >
        {childrenArray.map((child, index) => (
          <React.Fragment key={index}>
            {child}
            {divider && index < childrenArray.length - 1 && divider}
          </React.Fragment>
        ))}
      </div>
    );
  }
);

Stack.displayName = 'Stack';

export default Stack;
