import React from 'react';
import { Hero } from '../components/Hero';
import { FeatureGrid } from '../components/FeatureGrid';
import { KPIBand } from '../components/KPIBand';
import { TrustStrip } from '../components/TrustStrip';
import { Playground } from '../components/Playground';
import '../../brand/tokens/brand-tokens.css';

export const Build: React.FC = () => {
  return (
    <>
      <header
        className="ls-page-header"
        style={{
          backgroundColor: 'var(--color-navy, #070A40)',
          color: 'var(--color-white, #FFFFFF)',
          padding: 'var(--spacing-96, 96px) var(--spacing-48, 48px)',
          textAlign: 'center',
        }}
      >
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          <h1
            className="ls-page-header__title"
            style={{
              fontFamily: 'var(--font-display, Arial)',
              fontWeight: 700,
              fontSize: 'var(--size-display-xl, 36pt)',
              lineHeight: 1.1,
              margin: '0 0 var(--spacing-16, 16px)',
            }}
          >
            Build Your Agent Company
          </h1>
          <p
            className="ls-page-header__subtitle"
            style={{
              fontFamily: 'var(--font-body, Arial)',
              fontWeight: 400,
              fontSize: 'var(--size-body-lg, 16pt)',
              lineHeight: 1.6,
              color: 'var(--color-cyan, #00BFFF)',
              margin: 0,
            }}
          >
            Offer A — Turnkey AI-native organization: registry, governance, orchestration
          </p>
        </div>
      </header>

      <main>
        <Hero />
        <FeatureGrid />
        <KPIBand />
        <TrustStrip />
        <Playground />
      </main>

      <footer
        style={{
          backgroundColor: 'var(--color-navy, #070A40)',
          color: 'var(--color-white, #FFFFFF)',
          padding: 'var(--spacing-48, 48px)',
          textAlign: 'center',
        }}
      >
        <p style={{ fontFamily: 'var(--font-caption, Arial)', fontSize: 'var(--size-caption, 12pt)', color: 'var(--color-grey-light-text, #9CA3AF)', margin: 0 }}>
          LightSpeed Holdings Limited™ &copy; {new Date().getFullYear()} — <a href="/" style={{ color: 'var(--color-cyan, #00BFFF)' }}>lightspeedholdings.vercel.app</a>
        </p>
      </footer>
    </>
  );
};

export default Build;
