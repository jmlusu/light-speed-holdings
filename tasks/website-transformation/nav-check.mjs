import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto('http://localhost:1440/', { waitUntil: 'networkidle' });
const navItems = await page.locator('nav a, nav button').allTextContents();
console.log('NAV_ITEMS:', JSON.stringify(navItems));
const assessmentCta = await page.locator('nav a[href="/ai-assessment"]').count();
console.log('ASSESSMENT_CTA_COUNT:', assessmentCta);
const startConv = await page.locator('nav a[href="/contact"]').count();
console.log('START_CONVERSATION_CTA_COUNT:', startConv);
await browser.close();
