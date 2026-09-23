import { chromium } from 'playwright';

const base = 'http://localhost:4173';
const pages = [
  { name: 'home', path: '/', width: 1440, height: 900 },
  { name: 'contact', path: '/contact', width: 1440, height: 900 },
  { name: 'about', path: '/about', width: 1440, height: 900 },
  { name: 'contact-mobile', path: '/contact', width: 390, height: 844 },
  { name: 'about-mobile', path: '/about', width: 390, height: 844 },
];

const browser = await chromium.launch();
for (const p of pages) {
  const ctx = await browser.newContext({ viewport: { width: p.width, height: p.height } });
  const page = await ctx.newPage();
  await page.goto(base + p.path, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(800);
  await page.screenshot({ path: `.qa-screenshots/${p.name}.png`, fullPage: true });
  console.log('shot', p.name);
  await ctx.close();
}
await browser.close();
