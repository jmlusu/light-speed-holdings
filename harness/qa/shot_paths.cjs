const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const targets = [
    { width: 1280, height: 800, name: "paths-desktop" },
    { width: 390, height: 844, name: "paths-mobile" },
  ];
  for (const vp of targets) {
    const page = await browser.newPage({ viewport: vp });
    await page.goto("http://localhost:3001/", { waitUntil: "networkidle" });
    const el = page.locator("#paths");
    await el.scrollIntoViewIfNeeded();
    await page.waitForTimeout(600);
    await el.screenshot({ path: `C:/Users/jmlus/light-speed-holdings/harness/qa/${vp.name}.png` });
    console.log(vp.name + " ok");
    await page.close();
  }
  await browser.close();
})();
