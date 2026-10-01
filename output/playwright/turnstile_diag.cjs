const { chromium } = require('playwright');
const fs = require('fs');

const env = fs.readFileSync('.env', 'utf8').split(/\r?\n/);
const sitekey = env.find((l) => l.startsWith('VITE_TURNSTILE_SITE_KEY='))?.slice(24).trim();

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

  const net = [];
  page.on('response', (r) => {
    if (r.url().includes('cloudflare') || r.url().includes('turnstile')) {
      net.push(`${r.status()} ${r.url().slice(0, 90)}`);
    }
  });
  page.on('requestfailed', (r) => {
    if (r.url().includes('cloudflare') || r.url().includes('turnstile')) {
      net.push(`FAILED ${r.failure()?.errorText} ${r.url().slice(0, 90)}`);
    }
  });
  const logs = [];
  page.on('console', (m) => logs.push(`${m.type()}: ${m.text().slice(0, 120)}`));
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message.slice(0, 150)));

  await page.goto('http://localhost:4173/insights', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(6000);

  const manual = await page.evaluate((key) => {
    return new Promise((resolve) => {
      const div = document.createElement('div');
      div.style.width = '300px';
      div.style.height = '65px';
      document.body.appendChild(div);
      if (typeof window.turnstile?.render !== 'function') {
        resolve({ renderAvailable: false, api: typeof window.turnstile });
        return;
      }
      let done = false;
      const finish = (extra) => {
        if (done) return;
        done = true;
        setTimeout(() => {
          resolve({
            renderAvailable: true,
            widgetId: window.turnstile.render(div, { sitekey: key, callback: () => {}, 'error-callback': () => {} }),
            ...extra,
            containerChildren: div.childElementCount,
            containerHTML: div.innerHTML.slice(0, 200),
            iframesInDiv: div.querySelectorAll('iframe').length,
            iframesDoc: document.querySelectorAll('iframe').length,
          });
        }, 6000);
      };
      // capture async error-callback from a fresh render with logging
      const div2 = document.createElement('div');
      div2.style.width = '300px';
      div2.style.height = '65px';
      document.body.appendChild(div2);
      let errMsg = null;
      let cbToken = null;
      const id = window.turnstile.render(div2, {
        sitekey: key,
        callback: (t) => { cbToken = t ? `len=${t.length}` : 'empty'; },
        'error-callback': (e) => { errMsg = String(e); },
      });
      setTimeout(() => {
        if (done) return;
        done = true;
        resolve({
          renderAvailable: true,
          widgetId: id,
          errorCallback: errMsg,
          callbackToken: cbToken,
          containerChildren: div2.childElementCount,
          containerHTML: div2.innerHTML.slice(0, 200),
          iframesInDiv: div2.querySelectorAll('iframe').length,
          iframesDoc: document.querySelectorAll('iframe').length,
        });
      }, 8000);
    });
  }, sitekey);

  console.log('NET:', JSON.stringify(net, null, 1));
  console.log('MANUAL:', JSON.stringify(manual, null, 1));
  console.log('LOGS:', JSON.stringify(logs.slice(0, 15), null, 1));
  await browser.close();
})();
