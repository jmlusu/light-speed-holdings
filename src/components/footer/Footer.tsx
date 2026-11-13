/**
 * Footer Component
 *
 * Global site footer with logo and generic navigation links.
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { Logo } from '@lightspeed/design-system';
import { companyIdentity } from '@lightspeed/data/company';
import { tokens } from '@lightspeed/design-system/tokens';

const FOOTER_NAV = {
  links: [
    { label: 'What We Do', href: '/what-we-do' },
    { label: 'AI Company Builder', href: '/ai-company-builder' },
    { label: 'HAOMTGV Framework', href: '/haomtgv' },
    { label: 'Agent Registry', href: '/agent-registry' },
    { label: 'AI Assessment', href: '/ai-assessment' },
    { label: 'Operating Model', href: '/what-we-do' },
    { label: 'Pharos', href: '/insights' },
    { label: 'Who We Are', href: '/about' },
    { label: 'Frequently Asked Questions', href: '/faq' },
    { label: 'Contact', href: '/contact' },
    { label: 'Privacy Policy', href: '/legal/privacy' },
    { label: 'Terms of Service', href: '/legal/terms' },
    { label: 'AI Venture Studio', href: '/ai-company-builder' },
  ],
  social: [
    { label: 'Facebook', href: '#' },
    { label: 'X', href: '#' },
    { label: 'Instagram', href: '#' },
    { label: 'LinkedIn', href: '#' },
  ],
};

interface FooterProps {
  theme?: 'light' | 'dark';
}

export const Footer: React.FC<FooterProps> = ({ theme }) => {
  const isDark = theme ? theme === 'dark' : (typeof document !== 'undefined' && document.documentElement.classList.contains('dark'));

  const footerStyle: React.CSSProperties = {
    backgroundColor: isDark ? tokens.colors.navy : tokens.colors.navy,
    color: tokens.colors.white,
    padding: `${tokens.spacing[16]} ${tokens.spacing[12]} ${tokens.spacing[8]}`,
  };

  const containerStyle: React.CSSProperties = {
    maxWidth: tokens.spacing.container.maxWidth,
    margin: '0 auto',
    display: 'flex',
    flexDirection: 'column',
    gap: tokens.spacing[8],
  };

  const linkStyle: React.CSSProperties = {
    color: tokens.colors.grey[400],
    textDecoration: 'none',
    fontFamily: tokens.typography.fontFamily.sans,
    fontSize: tokens.typography.fontSize.bodySm,
    transition: 'color 0.2s ease',
  };

  return (
    <footer style={footerStyle} role="contentinfo">
      <div style={containerStyle}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: tokens.spacing[6] }}>
          <Logo variant="dark" size="md" />
          <nav aria-label="Footer Navigation">
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'row', flexWrap: 'wrap', gap: tokens.spacing[6] }}>
              {FOOTER_NAV.links.map((item) => (
                <li key={item.label}>
                  <Link to={item.href} style={linkStyle}>{item.label}</Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>
        <div style={{ borderTop: `1px solid ${tokens.colors.grey[800]}`, paddingTop: tokens.spacing[4], display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: tokens.spacing[4] }}>
          <p style={{
            fontFamily: tokens.typography.fontFamily.sans,
            fontSize: tokens.typography.fontSize.caption,
            color: tokens.colors.grey[400],
            margin: 0,
          }}>
            {companyIdentity.trademarkDomain} &copy; {new Date().getFullYear()}
          </p>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'row', flexWrap: 'wrap', gap: tokens.spacing[6] }}>
            {FOOTER_NAV.social.map((item) => (
              <li key={item.label}>
                <a href={item.href} style={linkStyle}>{item.label}</a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
