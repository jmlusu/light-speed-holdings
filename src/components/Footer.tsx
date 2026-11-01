/**
 * Footer — Global site footer with logo, navigation links, legal, and social.
 * Session 7 of the LightSpeed redesign.
 * Directive §7, §9
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { Linkedin, X, Youtube } from 'lucide-react';
import LogoLockup from '@/components/site/LogoLockup';
import { company } from '../data/siteContent';

/** Footer column structure matching canonical IA. */
const FooterColumn = {
  product: [
    { name: 'Home', to: '/' },
    { name: 'What We Do', to: '/what-we-do' },
    { name: 'AI Company Builder', to: '/ai-company-builder' },
    { name: 'Solutions', to: '/solutions' },
    { name: 'Sectors', to: '/sectors' },
    { name: 'Use Cases', to: '/use-cases' },
  ],
  company: [
    { name: 'About', to: '/about' },
    { name: 'Leadership', to: '/about#leadership' },
    { name: 'Careers', to: '/contact' },
  ],
  legal: [
    { name: 'Privacy Policy', to: '/legal/privacy' },
    { name: 'Terms of Service', to: '/legal/terms' },
  ],
};

/** Footer component — dark navy with logo lockup, link columns, legal row, social. */
export const Footer: React.FC<{ theme: 'light' | 'dark' }> = ({ theme }) => {
  const isDark = theme === 'dark';
  const navyBg = isDark ? '#070A40' : '#070A40';
  const whiteFg = '#FFFFFF';
  const greyFg = isDark ? '#9CA3AF' : '#6B7280';
  const cyanFg = '#00BFFF';
  const redFg = '#DC3641';

  return (
    <footer
      style={{
        backgroundColor: navyBg,
        color: whiteFg,
        padding: '16px 0 24px',
        borderTop: '1px solid rgba(255,255,255,0.1)',
      }}
      role='contentinfo'
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-8">
        <div className="flex flex-col sm:flex-row items-start justify-between gap-8 sm:gap-12">

          {/* Logo + tagline column */}
          <div className="flex flex-col items-start gap-4 sm:items-start sm:text-left">
            <div className="inline-flex items-center gap-2">
              <LogoLockup size={36} showText theme={theme} instance="repeat" />
            </div>
            <p
              style={{
                fontFamily: 'Arial, sans-serif',
                fontSize: '10px',
                fontWeight: 900,
                letterSpacing: '1px',
                color: greyFg,
                margin: 0,
                textTransform: 'uppercase',
              }}
            >
              LightSpeed Holdings™
            </p>
            <p
              style={{
                fontFamily: 'Arial, sans-serif',
                fontSize: '[10px]',
                lineHeight: 1.6,
                color: greyFg,
                margin: '8px 0 0',
              }}
            >
              {company.tagline}
            </p>
            <p
              style={{
                fontFamily: 'Arial, sans-serif',
                fontSize: '11px',
                color: greyFg,
                margin: '12px 0 0',
              }}
            >
              {company.location}
            </p>
          </div>

          {/* Product column */}
          <nav aria-label="Product" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <h4
              style={{
                fontFamily: 'Arial, sans-serif',
                fontSize: '10px',
                fontWeight: 700,
                letterSpacing: '1px',
                color: cyanFg,
                textTransform: 'uppercase',
                marginBottom: '8px',
              }}
            >
              Product
            </h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {FooterColumn.product.map((item) => (
                <li key={item.to}>
                  <Link
                    to={item.to}
                    style={{
                      fontFamily: 'Arial, sans-serif',
                      fontSize: '11px',
                      color: greyFg,
                      textDecoration: 'none',
                      transition: 'color 0.2s ease',
                    }}
                  >
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          {/* Company column */}
          <nav aria-label="Company" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <h4
              style={{
                fontFamily: 'Arial, sans-serif',
                fontSize: '10px',
                fontWeight: 700,
                letterSpacing: '1px',
                color: cyanFg,
                textTransform: 'uppercase',
                marginBottom: '8px',
              }}
            >
              Company
            </h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {FooterColumn.company.map((item) => (
                <li key={item.to}>
                  <Link
                    to={item.to}
                    style={{
                      fontFamily: 'Arial, sans-serif',
                      fontSize: '11px',
                      color: greyFg,
                      textDecoration: 'none',
                      transition: 'color 0.2s ease',
                    }}
                  >
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          {/* Legal column */}
          <nav aria-label="Legal" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <h4
              style={{
                fontFamily: 'Arial, sans-serif',
                fontSize: '10px',
                fontWeight: 700,
                letterSpacing: '1px',
                color: cyanFg,
                textTransform: 'uppercase',
                marginBottom: '8px',
              }}
            >
              Legal
            </h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {FooterColumn.legal.map((item) => (
                <li key={item.to}>
                  <Link
                    to={item.to}
                    style={{
                      fontFamily: 'Arial, sans-serif',
                      fontSize: '11px',
                      color: greyFg,
                      textDecoration: 'none',
                      transition: 'color 0.2s ease',
                    }}
                  >
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

        </div>

        {/* Legal row with year + AI-native sentence + social */}
        <div
          style={{
            marginTop: '24px',
            paddingTop: '24px',
            borderTop: '1px solid rgba(255,255,255,0.1)',
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'space-between',
            alignItems: 'center',
            gap: '16px',
            marginBottom: '24px',
          }}
        >
          <p
            style={{
              fontFamily: 'Arial, sans-serif',
              fontSize: '10px',
              color: greyFg,
              margin: 0,
            }}
          >
            {company.legalName}. All rights reserved© {new Date().getFullYear()}.
          </p>

          <p
            style={{
              fontFamily: 'Arial, sans-serif',
              fontSize: '10px',
              color: greyFg,
              margin: '4px 0 0',
            }}
          >
            Illustrations on this site are original vector artwork created in-house.
          </p>

          <div
            style={{
              display: 'flex',
              gap: '12px',
            }}
          >
            <a
              href="https://linkedin.com/company/lightspeedholdings"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-[10px] font-bold tracking-wider transition-colors hover:text-ls-red"
            >
              <Linkedin className="w-4 h-4" />
              linkedin
            </a>
            <a
              href="https://twitter.com/lightspeedhq"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-[10px] font-bold tracking-wider transition-colors hover:text-ls-red"
            >
              <X className="w-4 h-4" />
              x
            </a>
            <a
              href="https://youtube.com/@lightspeedholdings"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-[10px] font-bold tracking-wider transition-colors hover:text-ls-red"
            >
              <Youtube className="w-4 h-4" />
              youtube
            </a>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;
