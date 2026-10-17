import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto('http://localhost:1440/ai-assessment', { waitUntil: 'networkidle' });
await page.waitForTimeout(1200); // modal auto-opens
const bodyText = await page.locator('body').innerText();
console.log('HAS_NEW_HEADING:', bodyText.includes('Confidential AI Readiness Assessment Request'));
console.log('HAS_OLD_HEADING:', bodyText.includes('Executive Briefing'));
console.log('HAS_BOARDROOM_OPTION:', bodyText.includes('Boardroom Strategy Keynote'));
await page.screenshot({ path: 'tasks/website-transformation/ai-assessment-modal.png', fullPage: false });
await browser.close();
