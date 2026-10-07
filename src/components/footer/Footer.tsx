/**
 * Footer Component
 *
 * Global site footer with logo, navigation links, legal, and social
 * Directive §9, §34
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { Logo } from '@lightspeed/design-system';
import { companyIdentity } from '@lightspeed/data/company';
import { tokens } from '@lightspeed/design-system/tokens';

const FOOTER_NAV = {
  product: [
    { label: 'AI Company Builder', href: '/ai-company-builder' },
    { label: 'Solutions', href: '/solutions' },
    { label: 'Use Cases', href: '/use-cases' },
    { label: 'Sectors', href: '/sectors' },
    { label: 'Insights', href: '/insights' },
  ],
  company: [
    { label: 'About', href: '/about' },
    { label: 'Leadership', href: '/about#leadership' },
    { label: 'Careers', href: '/contact' },
    { label: 'Contact', href: '/contact' },
  ],
  legal: [
    { label: 'Privacy', href: '/legal/privacy' },
    { label: 'Terms', href: '/legal/terms' },
  ],
  social: [
    { label: 'LinkedIn', href: 'https://linkedin.com/company/lightspeedholdings', external: true },
    { label: 'X / Twitter', href: 'https://twitter.com/lightspeedhq', external: true },
    { label: 'Email', href: 'mailto:contact@lightspeedholdings.com', external: true },
  ],
};

export const Footer: React.FC = () => {
  const isDark = document.documentElement.classList.contains('dark');

  const footerStyle: React.CSSProperties = {
    backgroundColor: isDark ? tokens.colors.navy : tokens.colors.navy,
    color: tokens.colors.white,
    padding: `${tokens.spacing[16]} ${tokens.spacing[12]} ${tokens.spacing[8]}`,
  };

  const containerStyle: React.CSSProperties = {
    maxWidth: tokens.spacing.container.maxWidth,
    margin: '0 auto',
  };

  const gridStyle: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: tokens.spacing[12],
    marginBottom: tokens.spacing[12],
  };

  const navStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: tokens.spacing[2],
  };

  const linkStyle: React.CSSProperties = {
    color: tokens.colors.grey[400],
    textDecoration: 'none',
    fontFamily: tokens.typography.fontFamily.sans,
    fontSize: tokens.typography.fontSize.bodySm,
    transition: 'color 0.2s ease',
  };

  const headingStyle: React.CSSProperties = {
    fontFamily: tokens.typography.fontFamily.sans,
    fontWeight: tokens.typography.fontWeight.bold,
    fontSize: tokens.typography.fontSize.body,
    margin: `0 0 ${tokens.spacing[4]}`,
  };

  const bottomStyle: React.CSSProperties = {
    borderTop: `1px solid ${tokens.colors.grey[700]}`,
    paddingTop: tokens.spacing[6],
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: tokens.spacing[4],
  };

  const socialStyle: React.CSSProperties = {
    display: 'flex',
    gap: tokens.spacing[6],
  };

  return (
    <footer style={footerStyle} role="contentinfo">
      <div style={containerStyle}>
        <div style={gridStyle}>
          <div style={{ flex: '1 1 200px', minWidth: '200px' }}>
            <Logo variant="dark" size="md" style={{ marginBottom: tokens.spacing[4] }} />
            <p style={{
              fontFamily: tokens.typography.fontFamily.sans,
              fontSize: tokens.typography.fontSize.bodySm,
              lineHeight: 1.6,
              color: tokens.colors.grey[400],
              margin: 0,
            }}>
              {companyIdentity.tagline}
            </p>
          </div>

          <nav style={navStyle} aria-label="Product">
            <h4 style={headingStyle}>Product</h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: tokens.spacing[2] }}>
              {FOOTER_NAV.product.map((item) => (
                <li key={item.href}>
                  <Link to={item.href} style={linkStyle}>{item.label}</Link>
                </li>
              ))}
            </ul>
          </nav>

          <nav style={navStyle} aria-label="Company">
            <h4 style={headingStyle}>Company</h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: tokens.spacing[2] }}>
              {FOOTER_NAV.company.map((item) => (
                <li key={item.href}>
                  <Link to={item.href} style={linkStyle}>{item.label}</Link>
                </li>
              ))}
            </ul>
          </nav>

          <nav style={navStyle} aria-label="Legal">
            <h4 style={headingStyle}>Legal</h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: tokens.spacing[2] }}>
              {FOOTER_NAV.legal.map((item) => (
                <li key={item.href}>
                  <Link to={item.href} style={linkStyle}>{item.label}</Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>

        <div style={bottomStyle}>
          <p style={{
            fontFamily: tokens.typography.fontFamily.sans,
            fontSize: tokens.typography.fontSize.caption,
            color: tokens.colors.grey[400],
            margin: 0,
          }}>
            {companyIdentity.trademarkDomain} &copy; {new Date().getFullYear()}
          </p>
          <div style={socialStyle}>
            {FOOTER_NAV.social.map((item) => (
              <a
                key={item.label}
                href={item.href}
                target={item.external ? '_blank' : undefined}
                rel={item.external ? 'noopener noreferrer' : undefined}
                style={{
                  color: tokens.colors.grey[400],
                  textDecoration: 'none',
                  fontSize: tokens.typography.fontSize.caption,
                  transition: 'color 0.2s ease',
                }}
              >
                {item.label}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
