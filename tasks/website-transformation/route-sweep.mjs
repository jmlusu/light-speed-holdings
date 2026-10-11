import { chromium } from 'playwright';

const base = 'http://localhost:1440';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

const results = [];
async function check(path, expectPath, expectText) {
  const url = base + path;
  await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
  await page.waitForTimeout(500); // let client router settle
  const finalPath = new URL(page.url()).pathname;
  const bodyText = await page.locator('body').innerText().catch(() => '');
  const navLinks = await page.locator('nav a, header a').allTextContents().catch(() => []);
  const footerLinks = await page.locator('footer a').allTextContents().catch(() => []);
  const pathOk = expectPath ? finalPath === expectPath : true;
  const textOk = expectText ? bodyText.includes(expectText) : true;
  results.push({
    path,
    finalPath,
    pathOk,
    textOk,
    matched: expectText ? (textOk ? 'yes' : 'no') : 'n/a',
    navCount: navLinks.length,
    navSample: navLinks.slice(0, 10).join(' | '),
    footerHasProof: footerLinks.some(l => l.toLowerCase().includes('proof')),
    footerHasAssessment: footerLinks.some(l => l.toLowerCase().includes('assessment')),
    title: await page.title(),
  });
}

await check('/proof', '/use-cases', 'Use Cases');
await check('/ask', '/contact', 'Contact');
await check('/architecture', '/', '');
await check('/nonexistent-page-xyz', '/nonexistent-page-xyz', '');
await check('/', '/', 'LightSpeed');
await check('/use-cases', '/use-cases', 'Use Cases');
await check('/ai-assessment', '/ai-assessment', '');
await check('/about', '/about', '');

console.log(JSON.stringify(results, null, 2));
await browser.close();
