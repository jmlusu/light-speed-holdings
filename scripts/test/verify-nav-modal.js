/* Playwright nav/modal verification — ECL fix-website-dev-server-brand-tokens-mime-bug
 * T006 (dev 1441) / T007 (preview 1440): 19 checks, must all pass.
 *
 * Usage: node scripts/test/verify-nav-modal.js [baseUrl]   (default http://localhost:1441)
 * Exit code 0 = 19/19 pass, 1 = any failure.
 */
import { chromium } from 'playwright';

const BASE = process.argv[2] || 'http://localhost:1441';
const NAV_LINKS = [
  'Home', 'AI Company Builder', 'Solutions', 'Use Cases',
  'Sectors', 'Insights', 'About', 'Contact',
];

const results = [];
function record(name, pass, detail) {
  results.push({ name, pass: !!pass, detail: detail || '' });
  console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}${detail ? ` — ${detail}` : ''}`);
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

  const consoleErrors = [];
  const mimeErrors = [];
  const failedRequests = [];
  const badResponses = [];

  page.on('console', (msg) => {
    if (msg.type() !== 'error') return;
    const text = msg.text();
    if (/favicon/i.test(text)) return;
    consoleErrors.push(text);
    if (/MIME type|Failed to load module script|module script/i.test(text)) mimeErrors.push(text);
  });
  page.on('requestfailed', (req) => {
    if (/favicon/i.test(req.url())) return;
    failedRequests.push(`${req.method()} ${req.url()} :: ${req.failure() && req.failure().errorText}`);
  });
  page.on('response', (res) => {
    if (res.status() >= 400 && !/favicon/i.test(res.url())) {
      badResponses.push(`${res.status()} ${res.url()}`);
    }
  });

  const response = await page.goto(BASE, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(500);

  // ── A. Mount + MIME (core of the brand-tokens fix) ────────────────────────
  const rootChildren = await page.evaluate(
    () => document.getElementById('root')?.childElementCount || 0,
  );
  record('01 React mounted (#root has children)', rootChildren > 0, `children=${rootChildren}`);

  const mainInfo = await page.evaluate(() => {
    const el = document.getElementById('main-content');
    return { exists: !!el, children: el ? el.childElementCount : 0 };
  });
  record('02 #main-content rendered with content', mainInfo.exists && mainInfo.children > 0,
    JSON.stringify(mainInfo));

  const title = await page.title();
  record('03 document.title set by React', /^LIGHTSPEED HOLDINGS/.test(title), title);

  record('04 HTTP status < 400', !!response && response.status() < 400,
    response ? String(response.status()) : 'no response');

  record('05 zero module/MIME script errors', mimeErrors.length === 0,
    mimeErrors.slice(0, 2).join(' | ') || 'none');

  record('06 zero console errors', consoleErrors.length === 0,
    consoleErrors.slice(0, 2).join(' | ') || 'none');

  record('07 zero failed requests / bad responses',
    failedRequests.length === 0 && badResponses.length === 0,
    [...failedRequests, ...badResponses].slice(0, 2).join(' | ') || 'none');

  const tokens = await page.evaluate(() => {
    const cs = getComputedStyle(document.documentElement);
    return {
      navy: cs.getPropertyValue('--ls-navy').trim().toLowerCase(),
      red: cs.getPropertyValue('--ls-red').trim().toLowerCase(),
      cyan: cs.getPropertyValue('--ls-cyan').trim().toLowerCase(),
    };
  });
  record('08 brand token --ls-navy applied', tokens.navy === '#070a40', JSON.stringify(tokens));
  record('09 brand token --ls-red applied', tokens.red === '#e63946', `--ls-red=${tokens.red}`);
  record('10 brand token --ls-cyan applied', tokens.cyan === '#00bfff', `--ls-cyan=${tokens.cyan}`);

  const ctaBg = await page.evaluate(() => {
    const btns = [...document.querySelectorAll('button')];
    const cta = btns.find((b) => b.textContent.trim() === 'Start a Conversation');
    return cta ? getComputedStyle(cta).backgroundColor : null;
  });
  record('11 Tailwind brand color utility resolves (CTA = ls-red)',
    ctaBg === 'rgb(230, 57, 70)', `background=${ctaBg}`);

  // ── B. Navigation ─────────────────────────────────────────────────────────
  const headerOk = await page.evaluate(() => !!document.querySelector('header.fixed'));
  record('12 FloatingNav header present', headerOk);

  const linkTexts = await page.evaluate(() =>
    [...document.querySelectorAll('header nav a')].map((a) => a.textContent.trim()));
  const missing = NAV_LINKS.filter((n) => !linkTexts.includes(n));
  record('13 all 8 nav links rendered', missing.length === 0,
    missing.length ? `missing: ${missing.join(', ')}` : `found ${linkTexts.length}`);

  const ctaLabel = await page.evaluate(() => {
    const btns = [...document.querySelectorAll('button')];
    const cta = btns.find((b) => b.textContent.trim() === 'Start a Conversation');
    return cta ? cta.textContent.trim() : null;
  });
  record('14 primary CTA label correct', ctaLabel === 'Start a Conversation', String(ctaLabel));

  const ariaLabels = await page.evaluate(() =>
    [...document.querySelectorAll('header button')].map((b) => b.getAttribute('aria-label') || ''));
  record('15 governance + theme + menu controls present',
    ariaLabels.includes('Governance framework')
      && ariaLabels.some((l) => /Mode$/.test(l))
      && ariaLabels.includes('Toggle navigation menu'),
    JSON.stringify(ariaLabels));

  const skip = await page.evaluate(() => {
    const a = document.querySelector('a.skip-link');
    return a ? { href: a.getAttribute('href'), text: a.textContent.trim() } : null;
  });
  record('16 skip link targets #main-content',
    !!skip && skip.href === '#main-content' && /Skip to content/i.test(skip.text),
    JSON.stringify(skip));

  // ── C. Governance modal ───────────────────────────────────────────────────
  await page.click('header button[aria-label="Governance framework"]');
  await page.waitForTimeout(300);

  const modal = await page.evaluate(() => {
    const overlay = [...document.querySelectorAll('div.fixed.inset-0')].find((d) =>
      d.textContent.includes('HAOMTGV Governance Framework'));
    if (!overlay) return { open: false };
    const panel = overlay.querySelector('div.rounded-lg');
    const h2 = overlay.querySelector('h2');
    const cs = h2 ? getComputedStyle(h2) : null;
    const pcs = panel ? getComputedStyle(panel) : null;
    return {
      open: true,
      heading: h2 ? h2.textContent.trim() : null,
      headingVisible: !!(h2 && h2.offsetParent !== null),
      headingColor: cs ? cs.backgroundColor === 'rgba(0, 0, 0, 0)' && cs.color : null,
      panelOverflowY: pcs ? pcs.overflowY : null,
      panelMaxHeight: pcs ? pcs.maxHeight : null,
      hasClose: [...overlay.querySelectorAll('button')]
        .some((b) => b.textContent.includes('Close Governance Framework')),
    };
  });
  record('17 governance modal opens with heading',
    modal.open && modal.heading === 'HAOMTGV Governance Framework' && modal.headingVisible,
    JSON.stringify({ heading: modal.heading, visible: modal.headingVisible }));
  record('18 modal heading readable (white on navy) + panel scrollable',
    modal.headingColor === 'rgb(255, 255, 255)'
      && modal.panelOverflowY === 'auto'
      && modal.panelMaxHeight !== 'none',
    JSON.stringify({ color: modal.headingColor, overflowY: modal.panelOverflowY, maxHeight: modal.panelMaxHeight }));

  await page.click('button:has-text("Close Governance Framework")');
  await page.waitForTimeout(300);
  const closed = await page.evaluate(() =>
    ![...document.querySelectorAll('div.fixed.inset-0')]
      .some((d) => d.textContent.includes('HAOMTGV Governance Framework')));
  record('19 modal closes', closed);

  await browser.close();

  const passed = results.filter((r) => r.pass).length;
  console.log(`\n${passed}/${results.length} checks passed — ${BASE}`);
  if (passed !== results.length) {
    console.log('FAILURES:');
    results.filter((r) => !r.pass).forEach((r) => console.log(`  - ${r.name}: ${r.detail}`));
    process.exit(1);
  }
})().catch((err) => {
  console.error('SUITE ERROR:', err && err.message ? err.message : err);
  process.exit(1);
});
