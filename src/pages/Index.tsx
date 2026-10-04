import React from 'react';
import { Hero } from '../components/Hero';
import { FeatureGrid } from '../components/FeatureGrid';
import { KPIBand } from '../components/KPIBand';
import { TrustStrip } from '../components/TrustStrip';
import { LeadershipStrip } from '../components/LeadershipStrip';
import { Playground } from '../components/Playground';
import '../../brand/tokens/brand-tokens.css';

export const Index: React.FC = () => {
  return (
    <>
      <header
        className="ls-site-header"
        style={{
          position: 'sticky',
          top: 0,
          zIndex: 100,
          backgroundColor: 'var(--color-white, #FFFFFF)',
          borderBottom: '1px solid var(--color-grey-light-text, #9CA3AF)',
        } as React.CSSProperties}
      >
        <nav
          className="ls-nav"
          style={{
            maxWidth: 'var(--layout-web-max-width, 1200px)',
            margin: '0 auto',
            padding: 'var(--spacing-16, 16px) var(--spacing-48, 48px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          } as React.CSSProperties}
        >
          <a href="/" className="ls-nav__logo" aria-label="LightSpeed Holdings - Home" style={{ flexShrink: 0 } as React.CSSProperties}>
            <img
              src="/brand/logos/fulllogo/fulllogo.png"
              alt="LightSpeed Holdings Limited™"
              style={{ height: '40px', width: 'auto' } as React.CSSProperties}
              loading="lazy"
            />
          </a>
          <div
            className="ls-nav__links"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--spacing-32, 32px)',
            } as React.CSSProperties}
          >
            <a href="/architecture" className="ls-nav__link" style={{ color: 'var(--color-navy, #070A40)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontWeight: 400, fontSize: 'var(--size-body, 14pt)', transition: 'color 0.2s ease' } as React.CSSProperties}>
              Architecture
            </a>
            <a href="/build" className="ls-nav__link" style={{ color: 'var(--color-navy, #070A40)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontWeight: 400, fontSize: 'var(--size-body, 14pt)', transition: 'color 0.2s ease' } as React.CSSProperties}>
              Build
            </a>
            <a href="/offers" className="ls-nav__link" style={{ color: 'var(--color-navy, #070A40)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontWeight: 400, fontSize: 'var(--size-body, 14pt)', transition: 'color 0.2s ease' } as React.CSSProperties}>
              Offers
            </a>
            <a href="/docs" className="ls-nav__link" style={{ color: 'var(--color-navy, #070A40)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontWeight: 400, fontSize: 'var(--size-body, 14pt)', transition: 'color 0.2s ease' } as React.CSSProperties}>
              Docs
            </a>
          </div>
          <a
            href="/build"
            className="ls-nav__cta"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: 'var(--spacing-8, 8px) var(--spacing-16, 16px)',
              fontFamily: 'var(--font-display, Arial)',
              fontWeight: 700,
              fontSize: 'var(--size-body, 14pt)',
              color: 'var(--color-white, #FFFFFF)',
              backgroundColor: 'var(--color-red, #E63946)',
              borderRadius: 'var(--radius-small, 4px)',
              textDecoration: 'none',
              transition: 'background-color 0.2s ease',
            } as React.CSSProperties}
          >
            Start Free
          </a>
        </nav>
      </header>

      <main id="main-content">
        <Hero />
        <FeatureGrid />
        <KPIBand />
        <TrustStrip />
        <LeadershipStrip />
        <Playground />
      </main>

      <footer
        className="ls-site-footer"
        style={{
          backgroundColor: 'var(--color-navy, #070A40)',
          color: 'var(--color-white, #FFFFFF)',
          padding: 'var(--spacing-64, 64px) var(--spacing-48, 48px) var(--spacing-32, 32px)',
        } as React.CSSProperties}
      >
        <div style={{ maxWidth: 'var(--layout-web-max-width, 1200px)', margin: '0 auto' } as React.CSSProperties}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--spacing-48, 48px)', marginBottom: 'var(--spacing-48, 48px)' } as React.CSSProperties}>
            <div style={{ flex: '1 1 200px', minWidth: '200px' } as React.CSSProperties}>
              <img
                src="/brand/logos/fulllogo/fulllogo_transparent.png"
                alt="LightSpeed Holdings Limited™"
                style={{ height: '48px', width: 'auto', marginBottom: 'var(--spacing-16, 16px)' } as React.CSSProperties}
              />
              <p style={{ fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)', lineHeight: 1.6, color: 'var(--color-grey-light-text, #9CA3AF)', margin: 0 } as React.CSSProperties}>
                ASPIRE. ACT. ACHIEVE.
              </p>
            </div>
            <nav style={{ flex: '1 1 150px', minWidth: '150px' } as React.CSSProperties}>
              <h4 style={{ fontFamily: 'var(--font-display, Arial)', fontWeight: 700, fontSize: 'var(--size-body, 14pt)', margin: '0 0 var(--spacing-16, 16px)' } as React.CSSProperties}>Product</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 'var(--spacing-8, 8px)' } as React.CSSProperties}>
                <li><a href="/build" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>Build Agent Company</a></li>
                <li><a href="/architecture" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>Architecture</a></li>
                <li><a href="/docs" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>Documentation</a></li>
                <li><a href="/cli" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>CLI Reference</a></li>
              </ul>
            </nav>
            <nav style={{ flex: '1 1 150px', minWidth: '150px' } as React.CSSProperties}>
              <h4 style={{ fontFamily: 'var(--font-display, Arial)', fontWeight: 700, fontSize: 'var(--size-body, 14pt)', margin: '0 0 var(--spacing-16, 16px)' } as React.CSSProperties}>Offers</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 'var(--spacing-8, 8px)' } as React.CSSProperties}>
                <li><a href="/offer-a" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>Offer A: Website/Branding</a></li>
                <li><a href="/offer-b" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>Offer B: WhatsApp/AI Chat</a></li>
                <li><a href="/offer-c" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>Offer C: NGO M&E</a></li>
                <li><a href="/offer-e" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>Offer E: Platform Licensing</a></li>
              </ul>
            </nav>
            <nav style={{ flex: '1 1 150px', minWidth: '150px' } as React.CSSProperties}>
              <h4 style={{ fontFamily: 'var(--font-display, Arial)', fontWeight: 700, fontSize: 'var(--size-body, 14pt)', margin: '0 0 var(--spacing-16, 16px)' } as React.CSSProperties}>Company</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 'var(--spacing-8, 8px)' } as React.CSSProperties}>
                <li><a href="/about" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>About</a></li>
                <li><a href="/leadership" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>Leadership</a></li>
                <li><a href="/blog" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>Blog</a></li>
                <li><a href="/contact" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-sm, 13pt)' } as React.CSSProperties}>Contact</a></li>
              </ul>
            </nav>
          </div>
          <div
            className="ls-footer__bottom"
            style={{
              borderTop: '1px solid var(--color-grey-dark, #6B7280)',
              paddingTop: 'var(--spacing-24, 24px)',
              display: 'flex',
              flexWrap: 'wrap',
              justifyContent: 'space-between',
              alignItems: 'center',
              gap: 'var(--spacing-16, 16px)',
            } as React.CSSProperties}
          >
            <p style={{ fontFamily: 'var(--font-caption, Arial)', fontSize: 'var(--size-caption, 12pt)', color: 'var(--color-grey-light-text, #9CA3AF)', margin: 0 } as React.CSSProperties}>
              LightSpeed Holdings Limited™ &copy; {new Date().getFullYear()}
            </p>
            <div style={{ display: 'flex', gap: 'var(--spacing-24, 24px)' } as React.CSSProperties}>
              <a href="https://linkedin.com/company/lightspeedholdings" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontSize: 'var(--size-caption, 12pt)' } as React.CSSProperties}>LinkedIn</a>
              <a href="https://twitter.com/lightspeedhq" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontSize: 'var(--size-caption, 12pt)' } as React.CSSProperties}>X / Twitter</a>
              <a href="mailto:jmlusu@gmail.com" style={{ color: 'var(--color-grey-light-text, #9CA3AF)', textDecoration: 'none', fontSize: 'var(--size-caption, 12pt)' } as React.CSSProperties}>Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
};

export default Index;
