import { test, expect } from '@playwright/test';

const ROUTES = [
  '/',
  '/about/',
  '/agents/',
  '/case-study/',
  '/changelog/',
  '/contact/',
  '/docs/',
  '/features/',
  '/how-it-works/',
  '/platform/',
  '/pricing/',
  '/privacy/',
  '/research/',
  '/security/',
  '/solutions/',
  '/solutions/assessment/',
  '/solutions/enterprise/',
  '/solutions/managed-platform/',
  '/404.html',
];

const VIEWPORTS = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1440, height: 900 },
];

const BASE_URL = 'http://127.0.0.1:4321';

for (const viewport of VIEWPORTS) {
  for (const route of ROUTES) {
    test(`${viewport.name} - ${route}`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto(`${BASE_URL}${route}`, { waitUntil: 'networkidle', timeout: 15000 });
      await page.waitForLoadState('domcontentloaded');

      // Check 1: No unresolved --ls-* custom properties
      const unresolvedVars = await page.evaluate(() => {
        const unresolved = [];
        const sheets = Array.from(document.styleSheets);
        sheets.forEach(sheet => {
          try {
            Array.from(sheet.cssRules || []).forEach(rule => {
              if (rule.style) {
                for (let i = 0; i < rule.style.length; i++) {
                  const prop = rule.style[i];
                  const val = rule.style.getPropertyValue(prop);
                  if (val.includes('var(--ls-') && !val.match(/var\(--ls-(ink|ink-muted|text-secondary|accent|accent-hover|accent-2|accent-2-hover|cream|sage|pearl|warm|white|divider|card-border|ok|warn|nav-h|max|inner|gutter|radius-pill|radius-card|radius-md|radius-video|radius-method|shadow-video|shadow-dropdown|shadow-card|shadow-faq|font-sans|font-mono|font-serif|edge)\)/)) {
                    unresolved.push({ selector: rule.selectorText, property: prop, value: val });
                  }
                }
              }
            });
          } catch (e) {
            // cross-origin or inaccessible sheet
          }
        });
        return unresolved;
      });
      expect(unresolvedVars.length).toBe(0);

      // Check 2: No rounded-full on interactive elements
      const roundedFull = await page.evaluate(() => {
        const bad = [];
        const elements = document.querySelectorAll('button, a[class*="btn"], a[href], [role="button"], .badge, .pill, .chip, [class*="rounded-full"]');
        elements.forEach(el => {
          const classes = el.className || '';
          const style = window.getComputedStyle(el);
          if (classes.includes('rounded-full') || style.borderRadius === '9999px' || style.borderRadius.includes('9999')) {
            bad.push({ tag: el.tagName, classes: classes.substring(0, 200) });
          }
        });
        return bad;
      });
      expect(roundedFull.length).toBe(0);

      // Check 3: No horizontal overflow
      const hasOverflow = await page.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
      });
      expect(hasOverflow).toBe(false);
    });
  }
}