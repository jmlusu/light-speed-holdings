import { spawn } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

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
const RESULTS_DIR = 'audit-results';
const REPORT_FILE = path.join(RESULTS_DIR, 'baseline-report.json');

if (!fs.existsSync(RESULTS_DIR)) {
  fs.mkdirSync(RESULTS_DIR, { recursive: true });
}

function runDevServer() {
  return new Promise((resolve, reject) => {
    const child = spawn('npm', ['run', 'dev', '--', '--port', '4321', '--host', '127.0.0.1'], {
      cwd: process.cwd(),
      stdio: ['ignore', 'pipe', 'pipe'],
      shell: true,
    });

    let started = false;
    child.stdout.on('data', (data) => {
      const str = data.toString();
      if (str.includes('Local') && str.includes('4321') && !started) {
        started = true;
        setTimeout(resolve, 2000);
      }
    });
    child.stderr.on('data', (data) => {
      console.error('[dev]', data.toString());
    });
    child.on('error', reject);
    child.on('close', (code) => {
      if (!started) reject(new Error(`Dev server exited with code ${code}`));
    });

    setTimeout(() => {
      if (!started) reject(new Error('Dev server startup timeout'));
    }, 30000);
  });
}

async function auditPage(page, route, viewportName) {
  const results = {
    route,
    viewport: viewportName,
    checks: {},
    errors: [],
  };

  try {
    await page.goto(`${BASE_URL}${route}`, { waitUntil: 'networkidle', timeout: 15000 });
    await page.waitForLoadState('domcontentloaded');

    // Check 1: No unresolved --ls-* custom properties in computed styles
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
    results.checks.unresolvedVars = { pass: unresolvedVars.length === 0, count: unresolvedVars.length, details: unresolvedVars };

    // Check 2: No rounded-full on buttons/CTAs/badges/pills/chips
    const roundedFullElements = await page.evaluate(() => {
      const bad = [];
      const elements = document.querySelectorAll('button, a[class*="btn"], a[href], [role="button"], .badge, .pill, .chip, [class*="rounded-full"]');
      elements.forEach(el => {
        const classes = el.className || '';
        const style = window.getComputedStyle(el);
        if (classes.includes('rounded-full') || style.borderRadius === '9999px' || style.borderRadius.includes('9999')) {
          bad.push({ tag: el.tagName, classes: classes.substring(0, 200), role: el.getAttribute('role') || '' });
        }
      });
      return bad;
    });
    results.checks.roundedFullOnInteractive = { pass: roundedFullElements.length === 0, count: roundedFullElements.length, details: roundedFullElements };

    // Check 3: Mono-caps micro-labels where uppercase tracking eyebrows used to be
    // Heuristic: look for elements with uppercase tracking-wide/wider that are likely section headers/labels
    const eyebrowCandidates = await page.evaluate(() => {
      const candidates = [];
      const elements = document.querySelectorAll('h2, h3, h4, .eyebrow, .label, [class*="uppercase"], [class*="tracking"]');
      elements.forEach(el => {
        const classes = el.className || '';
        const style = window.getComputedStyle(el);
        const text = el.textContent?.trim() || '';
        if ((classes.includes('uppercase') || classes.includes('tracking-wide') || classes.includes('tracking-wider')) && text.length > 0 && text.length < 80) {
          candidates.push({
            tag: el.tagName,
            classes: classes.substring(0, 200),
            text: text.substring(0, 100),
            hasMonoCap: classes.includes('mono-cap') || el.classList.contains('font-mono'),
            fontFamily: style.fontFamily,
            textTransform: style.textTransform,
            letterSpacing: style.letterSpacing,
          });
        }
      });
      return candidates;
    });
    // This is informational - we expect some uppercase tracking in current baseline
    results.checks.eyebrowCandidates = { count: eyebrowCandidates.length, details: eyebrowCandidates };

    // Check 4: No horizontal overflow
    const hasOverflow = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    results.checks.horizontalOverflow = { pass: !hasOverflow, hasOverflow };

    // Check 5: Contrast spot-checks on text/secondary pairs
    const contrastChecks = await page.evaluate(() => {
      function getLuminance(r, g, b) {
        const a = [r, g, b].map(v => {
          v /= 255;
          return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
        });
        return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
      }
      function contrastRatio(l1, l2) {
        return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
      }
      function parseColor(str) {
        const m = str.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
        if (m) return [parseInt(m[1]), parseInt(m[2]), parseInt(m[3])];
        return null;
      }

      const checks = [];
      const elements = document.querySelectorAll('p, li, span, a, h1, h2, h3, h4, h5, h6');
      elements.forEach(el => {
        const style = window.getComputedStyle(el);
        const color = parseColor(style.color);
        const bg = parseColor(style.backgroundColor);
        if (color && bg) {
          const l1 = getLuminance(...color);
          const l2 = getLuminance(...bg);
          const ratio = contrastRatio(l1, l2);
          if (ratio < 4.5) {
            checks.push({
              tag: el.tagName,
              classes: el.className?.substring(0, 100) || '',
              text: el.textContent?.trim().substring(0, 50) || '',
              ratio: Math.round(ratio * 100) / 100,
              color: style.color,
              bg: style.backgroundColor,
            });
          }
        }
      });
      return checks;
    });
    results.checks.contrast = { pass: contrastChecks.length === 0, count: contrastChecks.length, details: contrastChecks.slice(0, 20) };

  } catch (e) {
    results.errors.push(e.message);
  }

  return results;
}

async function main() {
  console.log('Starting dev server...');
  const devProcess = spawn('npm', ['run', 'dev', '--', '--port', '4321', '--host', '127.0.0.1'], {
    cwd: process.cwd(),
    stdio: ['ignore', 'pipe', 'pipe'],
    shell: true,
  });

  await new Promise((resolve, reject) => {
    let started = false;
    devProcess.stdout.on('data', (data) => {
      const str = data.toString();
      if (str.includes('Local') && str.includes('4321') && !started) {
        started = true;
        setTimeout(resolve, 2000);
      }
    });
    devProcess.stderr.on('data', (data) => console.error('[dev]', data.toString()));
    devProcess.on('error', reject);
    setTimeout(() => { if (!started) reject(new Error('Dev server startup timeout')); }, 30000);
  });

  console.log('Dev server ready. Running audit...');
  const { chromium } = await import('playwright');
  const browser = await chromium.launch({ headless: true });
  const allResults = [];

  try {
    for (const viewport of VIEWPORTS) {
      console.log(`\n=== Viewport: ${viewport.name} (${viewport.width}x${viewport.height}) ===`);
      const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height } });

      for (const route of ROUTES) {
        const page = await context.newPage();
        const result = await auditPage(page, route, viewport.name);
        allResults.push(result);

        const status = Object.entries(result.checks)
          .filter(([k, v]) => typeof v === 'object' && 'pass' in v)
          .map(([k, v]) => v.pass ? '✓' : '✗')
          .join(' ');
        console.log(`  ${route} [${status}]`);

        if (result.errors.length) console.log(`    ERRORS: ${result.errors.join(', ')}`);

        await page.close();
      }
      await context.close();
    }
  } finally {
    await browser.close();
    devProcess.kill('SIGTERM');
  }

  // Summary
  const summary = {
    timestamp: new Date().toISOString(),
    totalPages: ROUTES.length * VIEWPORTS.length,
    passed: 0,
    failed: 0,
    byCheck: {},
  };

  const checkNames = ['unresolvedVars', 'roundedFullOnInteractive', 'horizontalOverflow', 'contrast'];
  checkNames.forEach(name => {
    summary.byCheck[name] = { pass: 0, fail: 0 };
  });

  allResults.forEach(r => {
    checkNames.forEach(name => {
      const check = r.checks[name];
      if (check && typeof check.pass === 'boolean') {
        if (check.pass) summary.byCheck[name].pass++;
        else summary.byCheck[name].fail++;
      }
    });
  });

  console.log('\n=== BASELINE SUMMARY ===');
  console.log(JSON.stringify(summary, null, 2));

  fs.writeFileSync(REPORT_FILE, JSON.stringify({ summary, results: allResults }, null, 2));
  console.log(`\nFull report written to ${REPORT_FILE}`);

  process.exit(summary.byCheck.unresolvedVars.fail > 0 ||
               summary.byCheck.roundedFullOnInteractive.fail > 0 ||
               summary.byCheck.horizontalOverflow.fail > 0 ? 1 : 0);
}

main().catch(e => {
  console.error('Audit failed:', e);
  process.exit(1);
});