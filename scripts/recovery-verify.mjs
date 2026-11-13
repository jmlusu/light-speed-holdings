/**
 * Recovery route + interaction verification (Playwright).
 * Read-only against a running preview server (default http://localhost:1440).
 * Writes screenshots to docs/recovery/screenshots/ and prints a JSON summary.
 */
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const BASE = process.env.VERIFY_BASE_URL || 'http://localhost:1440';
const OUT = resolve(process.cwd(), 'docs', 'recovery', 'screenshots');
mkdirSync(OUT, { recursive: true });

const routes = [
  '/', '/what-we-do', '/pharos', '/venture-studio', '/ai-company-builder', '/haomtgv',
  '/solutions', '/sectors', '/use-cases', '/ai-assessment', '/faq', '/insights',
  '/about', '/contact', '/legal/privacy', '/legal/terms',
  '/architecture', '/build', '/offer-a', '/offer-b', '/offer-c', '/offer-d', '/offer-e',
  '/proof', '/ask', '/faqs', '/definitely-not-a-route',
];

const results = [];
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();

for (const route of routes) {
  const consoleErrors = [];
  const pageErrors = [];
  const failedRequests = [];
  const onConsole = (m) => { if (m.type() === 'error') consoleErrors.push(m.text()); };
  const onPageError = (e) => pageErrors.push(String(e));
  const onFailed = (r) => failedRequests.push(`${r.failure()?.errorText || 'fail'} ${r.url()}`);
  page.on('console', onConsole);
  page.on('pageerror', onPageError);
  page.on('requestfailed', onFailed);

  let status = null;
  let finalUrl = null;
  let hasMain = false;
  let heading = null;
  let title = null;
  try {
    const resp = await page.goto(BASE + route, { waitUntil: 'networkidle', timeout: 30000 });
    status = resp ? resp.status() : null;
    await page.waitForTimeout(400);
    finalUrl = new URL(page.url()).pathname;
    hasMain = (await page.locator('#main-content').count()) > 0;
    heading = (await page.locator('#main-content h1').first().textContent().catch(() => null)) || null;
    title = await page.title();
    const slug = route === '/' ? 'home' : route.replace(/^\//, '').replace(/[^a-z0-9]+/gi, '-');
    await page.screenshot({ path: resolve(OUT, `${slug}.png`), fullPage: false });
  } catch (err) {
    pageErrors.push(`NAV_ERROR ${String(err)}`);
  } finally {
    page.off('console', onConsole);
    page.off('pageerror', onPageError);
    page.off('requestfailed', onFailed);
  }
  results.push({ route, status, finalUrl, hasMain, heading, title, consoleErrors, pageErrors, failedRequests });
}

// ---- Interaction checks (home) ----
const interactions = {};
try {
  await page.goto(BASE + '/', { waitUntil: 'networkidle' });
  // HumanApprovalMatrix: tier buttons update the inspector heading
  const matrix = page.locator('#governance-matrix');
  interactions.matrixPresent = (await matrix.count()) > 0;
  if (interactions.matrixPresent) {
    const buttons = matrix.locator('button');
    interactions.matrixButtonCount = await buttons.count();
    await buttons.first().click();
    await page.waitForTimeout(200);
    interactions.matrixInspectorAfterTier1 = (await matrix.locator('h3').first().textContent())?.trim() || null;
    await buttons.nth(4).click();
    await page.waitForTimeout(200);
    interactions.matrixInspectorAfterTier5 = (await matrix.locator('h3').first().textContent())?.trim() || null;
    await page.screenshot({ path: resolve(OUT, 'interaction-approval-matrix.png') });
  }
  // BackToTop: hidden at top, visible after scroll, returns to top on click
  const backToTop = page.getByRole('button', { name: /back to top of page/i });
  interactions.backToTopCount = await backToTop.count();
  if (interactions.backToTopCount > 0) {
    interactions.backToTopVisibleAtTop = await backToTop.evaluate((el) => getComputedStyle(el).opacity);
    await page.evaluate(() => window.scrollTo(0, 1600));
    await page.waitForTimeout(500);
    interactions.backToTopVisibleAfterScroll = await backToTop.evaluate((el) => getComputedStyle(el).opacity);
    await page.screenshot({ path: resolve(OUT, 'interaction-backtotop.png') });
    await backToTop.click();
    await page.waitForTimeout(1200);
    interactions.scrollYAfterBackToTop = await page.evaluate(() => Math.round(window.scrollY));
  }
} catch (err) {
  interactions.error = String(err);
}

// ---- Interaction checks (FAQ page) ----
const faqInteractions = {};
try {
  await page.goto(BASE + '/faq', { waitUntil: 'networkidle' });
  const search = page.getByPlaceholder(/Search questions/i);
  faqInteractions.searchPresent = (await search.count()) > 0;
  faqInteractions.initialCards = await page.locator('main .grid > div').count();
  if (faqInteractions.searchPresent) {
    await search.fill('data');
    await page.waitForTimeout(400);
    faqInteractions.afterSearchData = await page.locator('main .grid > div').count();
    await page.screenshot({ path: resolve(OUT, 'interaction-faq-search.png') });
    await search.fill('');
    await page.waitForTimeout(300);
  }
  const readBtn = page.getByRole('button', { name: /read answer/i }).first();
  if (await readBtn.count()) {
    await readBtn.click();
    await page.waitForTimeout(300);
    faqInteractions.evidenceVisible = (await page.getByText(/Evidence:/i).count()) > 0;
    await page.screenshot({ path: resolve(OUT, 'interaction-faq-expand.png') });
  }
} catch (err) {
  faqInteractions.error = String(err);
}

// ---- Theme toggle check ----
const themeCheck = {};
try {
  await page.goto(BASE + '/', { waitUntil: 'networkidle' });
  const before = await page.evaluate(() => document.documentElement.classList.contains('dark'));
  const toggle = page.getByRole('button', { name: /theme|dark mode|light mode/i }).first();
  if (await toggle.count()) {
    await toggle.click();
    await page.waitForTimeout(400);
    themeCheck.after = await page.evaluate(() => document.documentElement.classList.contains('dark'));
    themeCheck.changed = themeCheck.after !== before;
    await page.screenshot({ path: resolve(OUT, 'interaction-theme-toggle.png') });
  } else {
    themeCheck.toggleFound = false;
  }
} catch (err) {
  themeCheck.error = String(err);
}

await browser.close();

const summary = { base: BASE, routeCount: routes.length, results, interactions, faqInteractions, themeCheck };
console.log(JSON.stringify(summary, null, 2));
