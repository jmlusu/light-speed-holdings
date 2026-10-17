/**
 * Section Component
 *
 * Page section with consistent spacing and layout
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export interface SectionProps extends React.HTMLAttributes<HTMLDivElement> {
  id?: string;
  label?: string;
  theme?: 'light' | 'dark';
  scrim?: boolean;
  narrow?: boolean;
  wide?: boolean;
}

export const Section = React.forwardRef<HTMLDivElement, SectionProps>(
  (
    {
      id,
      label,
      theme,
      scrim = true,
      narrow = false,
      wide = false,
      className = '',
      children,
      style,
      ...props
    },
    ref
  ) => {
    const isDark = theme === 'dark' || document.documentElement.classList.contains('dark');
    const colorTokens = tokens.colors;

    const containerMaxWidth = narrow
      ? '720px'
      : wide
        ? '1400px'
        : tokens.spacing.container.maxWidth;

    const sectionStyle: React.CSSProperties = {
      position: 'relative',
      paddingTop: tokens.spacing[16],
      paddingBottom: tokens.spacing[16],
      paddingLeft: tokens.spacing[12],
      paddingRight: tokens.spacing[12],
      ...style,
    };

    const containerStyle: React.CSSProperties = {
      maxWidth: containerMaxWidth,
      margin: '0 auto',
      width: '100%',
    };

    const labelStyle: React.CSSProperties = {
      display: 'inline-flex',
      alignItems: 'center',
      gap: tokens.spacing[2],
      padding: `${tokens.spacing[2]} ${tokens.spacing[4]}`,
      borderRadius: tokens.radius.full,
      fontFamily: tokens.typography.fontFamily.sans,
      fontSize: tokens.typography.fontSize.overline,
      fontWeight: tokens.typography.fontWeight.bold,
      border: `1px solid ${isDark ? 'rgba(0, 191, 255, 0.3)' : 'rgba(230, 57, 70, 0.3)'}`,
      backgroundColor: isDark ? 'rgba(0, 191, 255, 0.1)' : 'rgba(230, 57, 70, 0.1)',
      color: isDark ? tokens.colors.cyan : tokens.colors.red,
      marginBottom: tokens.spacing[6],
    };

    return (
      <section
        ref={ref}
        id={id}
        className={className}
        style={sectionStyle}
        {...props}
      >
        {scrim && (
          <div
            className="fixed inset-0 z-[-1] pointer-events-none"
            aria-hidden="true"
            style={{
              backgroundColor: isDark ? colorTokens.deepMineral : colorTokens.morningMist,
            }}
          />
        )}
        <div style={containerStyle}>
          {label && (
            <div style={labelStyle}>
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: isDark ? tokens.colors.cyan : tokens.colors.red }} aria-hidden="true" />
              {label.toUpperCase()}
            </div>
          )}
          {children}
        </div>
      </section>
    );
  }
);

Section.displayName = 'Section';

export default Section;
