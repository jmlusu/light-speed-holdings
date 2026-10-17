/* Site-wide visual verification sweep (REBUILD_DIRECTIVE §16/§20).
 * Checks every route in light+dark at desktop+mobile: console errors,
 * horizontal overflow, missing alt, empty headings, h1 count, theme
 * application, internal link targets. Screenshots: desktop (all routes,
 * both themes) + mobile (key routes, both themes).
 * Usage: node output/playwright/site_sweep.js */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = 'http://localhost:4173';
const OUT = __dirname;
const ROUTES = [
  ['home', '/'],
  ['what-we-do', '/what-we-do'],
  ['ai-company-builder', '/ai-company-builder'],
  ['solutions', '/solutions'],
  ['sectors', '/sectors'],
  ['proof', '/proof'],
  ['insights', '/insights'],
  ['about', '/about'],
  ['contact', '/contact'],
  ['ask', '/ask'],
  ['legal-privacy', '/legal/privacy'],
  ['legal-terms', '/legal/terms'],
];
const VALID_PATHS = new Set(ROUTES.map(([, p]) => p));
const VIEWPORTS = [
  { name: 'desktop', width: 1280, height: 800 },
  { name: 'mobile', width: 390, height: 844 },
];
const THEMES = ['light', 'dark'];
const MOBILE_SHOT = new Set(['home', 'what-we-do', 'sectors', 'contact']);

(async () => {
  const browser = await chromium.launch();
  const findings = [];

  for (const vp of VIEWPORTS) {
    for (const theme of THEMES) {
      const context = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
        reducedMotion: 'reduce',
        colorScheme: theme,
      });
      await context.addInitScript((t) => {
        try { localStorage.setItem('lightspeed_theme', t); } catch (e) { /* noop */ }
      }, theme);

      for (const [name, route] of ROUTES) {
        const page = await context.newPage();
        const consoleErrors = [];
        const pageErrors = [];
        page.on('console', (m) => {
          if (m.type() === 'error') consoleErrors.push(m.text());
        });
        page.on('pageerror', (e) => pageErrors.push(String(e)));

        const rec = { route: name, path: route, viewport: vp.name, theme, consoleErrors, pageErrors };
        try {
          const resp = await page.goto(BASE + route, { waitUntil: 'networkidle', timeout: 20000 });
          rec.status = resp ? resp.status() : null;
          await page.waitForTimeout(300);
          Object.assign(rec, await page.evaluate(({ valid }) => {
            const validSet = new Set(valid);
            const doc = document.documentElement;
            const imgsNoAlt = [...document.querySelectorAll('img:not([alt])')]
              .map((i) => i.currentSrc || i.src || '(no src)').slice(0, 10);
            const emptyHeadings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')]
              .filter((h) => !(h.textContent || '').trim()).length;
            const badLinks = [...new Set([...document.querySelectorAll('a[href]')]
              .map((a) => a.getAttribute('href'))
              .filter((h) => h && h.startsWith('/') && !h.startsWith('//'))
              .map((h) => h.split('#')[0]))]
              .filter((h) => h && !validSet.has(h));
            return {
              darkApplied: doc.classList.contains('dark'),
              title: document.title,
              metaDescription: (document.querySelector('meta[name="description"]') || {}).content || null,
              h1Count: document.querySelectorAll('h1').length,
              overflowPx: Math.max(0, doc.scrollWidth - window.innerWidth),
              imgsNoAlt,
              emptyHeadings,
              badLinks,
              lang: doc.getAttribute('lang'),
            };
          }, { valid: [...VALID_PATHS] }));
          rec.themeApplied = rec.darkApplied === (theme === 'dark');

          const wantShot = vp.name === 'desktop' || MOBILE_SHOT.has(name);
          if (wantShot && rec.status === 200) {
            const file = path.join(OUT, `${name}-${theme}-${vp.name}.png`);
            await page.screenshot({ path: file, fullPage: true });
            rec.screenshot = path.basename(file);
          }
        } catch (err) {
          rec.error = String(err);
        }
        findings.push(rec);
        process.stdout.write(`${vp.name}/${theme}/${name} `);
      }
      await context.close();
    }
  }

  await browser.close();
  const report = { generatedAt: new Date().toISOString(), base: BASE, findings };
  fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 2));

  const problems = findings.filter((f) =>
    f.error || f.status !== 200 || (f.overflowPx > 1) || f.imgsNoAlt?.length ||
    f.emptyHeadings > 0 || f.h1Count !== 1 || !f.themeApplied ||
    f.pageErrors.length || f.consoleErrors.length || f.badLinks?.length);
  console.log(`\n\n${findings.length} page-loads, ${problems.length} with findings:`);
  for (const p of problems) {
    console.log(`- ${p.viewport}/${p.theme}/${p.route}:` +
      (p.error ? ` ERROR ${p.error}` : '') +
      (p.status !== 200 ? ` status=${p.status}` : '') +
      (p.overflowPx > 1 ? ` overflow=${p.overflowPx}px` : '') +
      (p.imgsNoAlt?.length ? ` imgNoAlt=${p.imgsNoAlt.length}` : '') +
      (p.emptyHeadings > 0 ? ` emptyHeadings=${p.emptyHeadings}` : '') +
      (p.h1Count !== 1 ? ` h1=${p.h1Count}` : '') +
      (!p.themeApplied ? ' themeNotApplied' : '') +
      (p.pageErrors.length ? ` pageErrors=${JSON.stringify(p.pageErrors).slice(0, 300)}` : '') +
      (p.consoleErrors.length ? ` consoleErrors=${JSON.stringify(p.consoleErrors).slice(0, 300)}` : '') +
      (p.badLinks?.length ? ` badLinks=${JSON.stringify(p.badLinks)}` : ''));
  }
})();
