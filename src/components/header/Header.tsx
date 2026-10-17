/**
 * Header Component
 *
 * Global site header with logo, navigation, and primary CTA
 * Directive §9, §34 — Primary navigation and CTA system
 */

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Logo } from '@lightspeed/design-system';
import { ctasRegistry, getPrimaryCTA } from '@lightspeed/data/ctas';
import { tokens } from '@lightspeed/design-system/tokens';

const NAV_ITEMS = [
  { path: '/', label: 'Home' },
  { path: '/what-we-do', label: 'What We Do' },
  { path: '/ai-company-builder', label: 'AI Company Builder' },
  { path: '/solutions', label: 'Solutions' },
  { path: '/use-cases', label: 'Use Cases' },
  { path: '/sectors', label: 'Sectors' },
  { path: '/insights', label: 'Insights' },
  { path: '/about', label: 'About' },
];

export const Header: React.FC = () => {
  const location = useLocation();
  const primaryCTA = getPrimaryCTA();
  const isDark = document.documentElement.classList.contains('dark');

  const headerStyle: React.CSSProperties = {
    position: 'sticky',
    top: 0,
    zIndex: 100,
    backgroundColor: isDark ? tokens.colors.deepMineral : tokens.colors.morningMist,
    borderBottom: `1px solid ${isDark ? tokens.colors.grey[800] : tokens.colors.grey[200]}`,
    transition: 'background-color 0.2s ease, border-color 0.2s ease',
  };

  const navStyle: React.CSSProperties = {
    maxWidth: tokens.spacing.container.maxWidth,
    margin: '0 auto',
    padding: `${tokens.spacing[4]} ${tokens.spacing[12]}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  };

  const navLinksStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: tokens.spacing[8],
  };

  const linkStyle = (isActive: boolean): React.CSSProperties => ({
    color: isActive
      ? (isDark ? tokens.colors.cyan : tokens.colors.navy)
      : (isDark ? tokens.colors.grey[400] : tokens.colors.grey[600]),
    textDecoration: 'none',
    fontFamily: tokens.typography.fontFamily.sans,
    fontWeight: 400,
    fontSize: tokens.typography.fontSize.body,
    transition: 'color 0.2s ease',
    padding: `${tokens.spacing[1]} ${tokens.spacing[2]}`,
    borderRadius: tokens.radius.small,
  });

  return (
    <header style={headerStyle} role="banner">
      <nav style={navStyle} aria-label="Main navigation">
        <Link
          to="/"
          className="header__logo"
          aria-label="LightSpeed Holdings - Home"
          style={{ flexShrink: 0 } as React.CSSProperties}
        >
          <Logo variant="full" size="md" />
        </Link>

        <div style={navLinksStyle} role="navigation" aria-label="Primary">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              style={linkStyle(location.pathname === item.path)}
              aria-current={location.pathname === item.path ? 'page' : undefined}
            >
              {item.label}
            </Link>
          ))}
        </div>

        <Link
          to={primaryCTA.href}
          className="header__cta"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: `${tokens.spacing[2]} ${tokens.spacing[4]}`,
            fontFamily: tokens.typography.fontFamily.sans,
            fontWeight: tokens.typography.fontWeight.bold,
            fontSize: tokens.typography.fontSize.body,
            color: tokens.colors.white,
            backgroundColor: tokens.colors.red,
            borderRadius: tokens.radius.small,
            textDecoration: 'none',
            transition: 'background-color 0.2s ease, box-shadow 0.2s ease',
            boxShadow: `0 4px 14px ${tokens.colors.red}4D`,
          } as React.CSSProperties}
        >
          {primaryCTA.label}
        </Link>
      </nav>
    </header>
  );
};

export default Header;
