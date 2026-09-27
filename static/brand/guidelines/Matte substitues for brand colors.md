/* ==========================================================================
   LightSpeed Holdings — Premium Matte Design System
   ========================================================================== */

:root {
  /* Core Brand Matte Substitutes */
  --brand-navy-matte: #1b223c;       /* Original #070A40 */
  --brand-red-matte: #cd535b;        /* Original #E63946 */
  --brand-cyan-matte: #5a9eb5;       /* Original #00BFFF */

  /* Neutral Muted Tones */
  --neutral-dark-grey: #5c626d;      /* Original #6B7280 */
  --neutral-light-grey: #8a919b;     /* Original #9CA3AF */

  /* Light Theme Mapping (Default) */
  --site-bg: #ecece8;                /* Original Light Surface Grey #F2F2F2 */
  --card-bg: #f9f9f7;                /* Original Pure White #FFFFFF */
  --text-primary: #1b223c;           /* High-contrast matte text */
  --text-secondary: #5c626d;         /* Subheadings and captions */
  --border-color: #8a919b33;         /* Muted pewter with 20% opacity */

  /* Interactive States */
  --cta-bg: #cd535b;
  --cta-text: #f9f9f7;
  --link-color: #5a9eb5;

  /* Smooth UI Transitions */
  --transition-smooth: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Optional Dark Mode Override Utility
   Triggered automatically by user system preference or a .dark class on <body> */
@media (prefers-color-scheme: dark) {
  :root {
    --site-bg: #131728;              /* Deepened ink for dark mode backing */
    --card-bg: #1b223c;              /* Matte Navy acts as the container surface */
    --text-primary: #f9f9f7;         /* Soft silk text to avoid glare */
    --text-secondary: #8a919b;       /* Muted pewter text */
    --border-color: #5c626d4d;       /* Charcoal slate with 30% opacity */

    --cta-bg: #cd535b;               /* Red stays consistent, glows softly on dark */
    --cta-text: #f9f9f7;
    --link-color: #5a9eb5;
  }
}

/* ==========================================================================
   Structural Layout & Resets
   ========================================================================== */

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: var(--site-bg);
  color: var(--text-primary);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  transition: var(--transition-smooth);
}

/* ==========================================================================
   Component UI Classes (Matte Best Practices)
   ========================================================================== */

/* Typography Typography Examples */
h1, h2, h3 {
  color: var(--text-primary);
  font-weight: 700;
  letter-spacing: -0.02em;
}

p, span {
  color: var(--text-secondary);
}

/* Matte Container Cards (Zero harsh box-shadows to ensure flat matte texture) */
.matte-card {
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  transition: var(--transition-smooth);
}

/* Interactive Matte CTA Buttons */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: var(--cta-bg);
  color: var(--cta-text);
  font-weight: 600;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: var(--transition-smooth);
}

/* Micro-interaction for flat design (Changes opacity/scale instead of adding glow) */
.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(0);
}

/* Matte Inline Text Links */
.matte-link {
  color: var(--link-color);
  text-decoration: none;
  border-bottom: 1.5px solid transparent;
  transition: var(--transition-smooth);
}

.matte-link:hover {
  border-bottom-color: var(--link-color);
}
