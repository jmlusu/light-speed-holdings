import { chromium } from 'playwright';
const BASE = 'http://localhost:1440';
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
const out = {};

// --- /insights with domcontentloaded (networkidle blocked by Turnstile/CF challenge) ---
const errs = [];
page.on('pageerror', (e) => errs.push(String(e)));
const resp = await page.goto(BASE + '/insights', { waitUntil: 'domcontentloaded', timeout: 30000 });
out.insights = {
  status: resp ? resp.status() : null,
  hasMain: (await page.locator('#main-content').count()) > 0,
  h1: (await page.locator('#main-content h1').first().textContent().catch(() => null)),
  articleCards: await page.locator('a[href^="/insights/"]').count(),
};
await page.screenshot({ path: 'docs/recovery/screenshots/insights-domcontentloaded.png' });

// --- BackToTop precise check ---
await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 30000 });
await page.waitForTimeout(600);
await page.evaluate(() => window.scrollTo(0, 0));
await page.waitForTimeout(500);
const btn = page.getByRole('button', { name: /back to top of page/i });
out.backToTop = {};
out.backToTop.count = await btn.count();
out.backToTop.classAtTop = await btn.getAttribute('class');
out.backToTop.opacityAtTop = await btn.evaluate((el) => getComputedStyle(el).opacity);
out.backToTop.pointerAtTop = await btn.evaluate((el) => getComputedStyle(el).pointerEvents);
await page.evaluate(() => window.scrollTo(0, 1800));
await page.waitForTimeout(700);
out.backToTop.opacityAfterScroll = await btn.evaluate((el) => getComputedStyle(el).opacity);
out.backToTop.ariaAfterScroll = await btn.getAttribute('aria-label');
out.backToTop.scrollYBeforeClick = await page.evaluate(() => Math.round(window.scrollY));
await page.screenshot({ path: 'docs/recovery/screenshots/backtotop-visible.png' });
await btn.click();
await page.waitForTimeout(1500);
out.backToTop.scrollYAfterClick = await page.evaluate(() => Math.round(window.scrollY));
out.backToTop.focusedId = await page.evaluate(() => document.activeElement?.id || null);

// --- Homepage matrix: verify it replaced the static approximation ---
const matrix = page.locator('#governance-matrix');
out.matrix = {
  present: (await matrix.count()) > 0,
  hasTierButtons: await matrix.locator('button').count(),
  codesRendered: await matrix.locator('text=CEO_ONLY (4)').count(),
};

out.pageErrors = errs;
console.log(JSON.stringify(out, null, 2));
await browser.close();
