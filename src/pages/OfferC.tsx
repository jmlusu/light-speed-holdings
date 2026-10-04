import React from 'react';
import { Hero } from '../components/Hero';
import { KPIBand } from '../components/KPIBand';
import { TrustStrip } from '../components/TrustStrip';
import '../../brand/tokens/brand-tokens.css';

export const OfferC: React.FC = () => {
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
            NGO Monitoring & Evaluation
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
            Offer C — Agentic M&E for development programs: data collection, validation, reporting
          </p>
        </div>
      </header>

      <main style={{ padding: 'var(--spacing-64, 64px) var(--spacing-48, 48px)' }}>
        <div style={{ maxWidth: 'var(--layout-web-max-width, 1200px)', margin: '0 auto' }}>
          <section style={{ marginBottom: 'var(--spacing-64, 64px)' }}>
            <h2 style={{ fontFamily: 'var(--font-display, Arial)', fontWeight: 700, fontSize: 'var(--size-title-lg, 28pt)', color: 'var(--color-navy, #070A40)', margin: '0 0 var(--spacing-24, 24px)' }}>
              Capabilities
            </h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 'var(--spacing-24, 24px)' }}>
              {[
                'Mobile data collection agents (offline-first)',
                'Form validation & data quality checks',
                'Real-time dashboard for program officers',
                'Automated indicator calculation',
                'Beneficiary feedback loops',
                'Geospatial data integration',
                'Compliance audit trails (donor-ready)',
                'Multi-country, multi-language support',
              ].map((item, i) => (
                <article key={i} style={{ backgroundColor: 'var(--color-white, #FFFFFF)', border: '1px solid var(--color-grey-light-text, #9CA3AF)', borderRadius: 'var(--radius-medium, 8px)', padding: 'var(--spacing-24, 24px)', display: 'flex', alignItems: 'flex-start', gap: 'var(--spacing-12, 12px)' }}>
                  <span style={{ flexShrink: 0, width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--color-cyan, #00BFFF)', marginTop: '6px' }}></span>
                  <span style={{ fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body, 14pt)', color: 'var(--color-grey-dark, #6B7280)' }}>{item}</span>
                </article>
              ))}
            </div>
          </section>

          <KPIBand />
          <TrustStrip />

          <section style={{ marginTop: 'var(--spacing-64, 64px)', textAlign: 'center' }}>
            <h2 style={{ fontFamily: 'var(--font-display, Arial)', fontWeight: 700, fontSize: 'var(--size-title-lg, 28pt)', color: 'var(--color-navy, #070A40)', margin: '0 0 var(--spacing-16, 16px)' }}>
              Deploy M&E Agents for Your Program
            </h2>
            <p style={{ fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body-lg, 16pt)', color: 'var(--color-grey-dark, #6B7280)', margin: '0 0 var(--spacing-32, 32px)', maxWidth: '600px', marginLeft: 'auto', marginRight: 'auto' }}>
              From baseline to endline — governed agents that donors trust.
            </p>
            <a href="/contact" style={{ display: 'inline-flex', alignItems: 'center', padding: 'var(--spacing-12, 12px) var(--spacing-24, 24px)', fontFamily: 'var(--font-display, Arial)', fontWeight: 700, fontSize: 'var(--size-subtitle, 16pt)', color: 'var(--color-white, #FFFFFF)', backgroundColor: 'var(--color-red, #E63946)', borderRadius: 'var(--radius-medium, 8px)', textDecoration: 'none' }}>
              Get Started →
            </a>
          </section>
        </div>
      </main>

      <footer style={{ backgroundColor: 'var(--color-navy, #070A40)', color: 'var(--color-white, #FFFFFF)', padding: 'var(--spacing-48, 48px)', textAlign: 'center' }}>
        <p style={{ fontFamily: 'var(--font-caption, Arial)', fontSize: 'var(--size-caption, 12pt)', color: 'var(--color-grey-light-text, #9CA3AF)', margin: 0 }}>
          LightSpeed Holdings Limited™ &copy; {new Date().getFullYear()} — <a href="/" style={{ color: 'var(--color-cyan, #00BFFF)' }}>lightspeedholdings.com</a>
        </p>
      </footer>
    </>
  );
};

export default OfferC;
