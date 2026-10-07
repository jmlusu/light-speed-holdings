/**
 * Container Component
 *
 * Max-width wrapper with consistent padding
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export type ContainerSize = 'default' | 'narrow' | 'wide' | 'full';

export interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: ContainerSize;
  padding?: boolean;
}

export const Container = React.forwardRef<HTMLDivElement, ContainerProps>(
  (
    {
      size = 'default',
      padding = true,
      className = '',
      children,
      style,
      ...props
    },
    ref
  ) => {
    const sizeStyles: Record<ContainerSize, React.CSSProperties> = {
      default: { maxWidth: tokens.spacing.container.maxWidth },
      narrow: { maxWidth: '720px' },
      wide: { maxWidth: '1400px' },
      full: { maxWidth: '100%' },
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
      ...sizeStyles[size],
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

Container.displayName = 'Container';

export default Container;
