const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  const resp = await page.goto('http://localhost:4173/insights', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(15000);

  const state = await page.evaluate(() => {
    const iframes = [...document.querySelectorAll('iframe')].map((f) => ({
      src: (f.src || '').slice(0, 60),
      visible: f.offsetParent !== null,
      w: f.offsetWidth,
      h: f.offsetHeight,
    }));
    const sub = [...document.querySelectorAll('button')].find((x) => /subscribe/i.test(x.textContent || ''));
    const form = sub ? sub.closest('form') : null;
    const hidden = form ? form.querySelector('div.hidden') : null;
    return {
      iframeCount: iframes.length,
      iframes,
      hiddenContainerFound: !!hidden,
      hiddenContainerChildren: hidden ? hidden.childElementCount : -1,
      hiddenContainerHTML: hidden ? hidden.innerHTML.length : -1,
      turnstileGlobal: typeof window.turnstile,
      subscribeDisabled: sub ? sub.disabled : null,
      h1: document.querySelectorAll('h1').length,
      title: document.title,
    };
  });

  console.log(JSON.stringify({ status: resp.status(), errors, ...state }, null, 2));
  await page.screenshot({ path: 'output/playwright/insights-turnstile-after-fix.png', fullPage: false });
  await browser.close();
})();
