const { chromium } = require("playwright");

// Usage: node shot_element.cjs <url> <selector> <WxH> <out.png>
(async () => {
  const [url, selector, vp, out] = process.argv.slice(2);
  const [width, height] = vp.split("x").map(Number);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height } });
  await page.goto(url, { waitUntil: "networkidle" });
  const el = page.locator(selector).first();
  await el.scrollIntoViewIfNeeded();
  await page.waitForTimeout(900);
  await el.screenshot({ path: out });
  const info = await el.evaluate((node) => ({
    tag: node.tagName,
    text: (node.innerText || "").slice(0, 600),
    links: Array.from(node.querySelectorAll("a")).map(
      (a) => a.textContent.trim().replace(/\s+/g, " ") + " -> " + a.getAttribute("href")
    ),
    contrast: getComputedStyle(node).color,
  }));
  console.log(JSON.stringify(info, null, 2));
  await browser.close();
})();
