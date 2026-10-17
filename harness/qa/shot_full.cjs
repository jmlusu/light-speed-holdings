const { chromium } = require("playwright");

// Usage: node shot_full.cjs <url> <WxH> <out.png>
(async () => {
  const [url, vp, out] = process.argv.slice(2);
  const [width, height] = vp.split("x").map(Number);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height } });
  // "networkidle" never settles: Cloudflare Turnstile retries DNS-failing hosts in-page.
  await page.goto(url, { waitUntil: "load", timeout: 30000 });
  await page.waitForTimeout(1500);
  // Scroll through the page so every Reveal crosses its in-view threshold.
  await page.evaluate(async () => {
    const step = window.innerHeight * 0.7;
    for (let y = 0; y < document.body.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 180));
    }
    window.scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 400));
  });
  await page.waitForTimeout(600);
  await page.screenshot({ path: out, fullPage: true });
  const hidden = await page.evaluate(() =>
    Array.from(document.querySelectorAll("main *")).filter((el) => {
      const s = getComputedStyle(el);
      return s.opacity === "0" && el.getBoundingClientRect().height > 40;
    }).length
  );
  console.log(JSON.stringify({ screenshot: out, stillHiddenAbove40px: hidden }));
  await browser.close();
})();
