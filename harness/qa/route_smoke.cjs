const { chromium } = require("playwright");

/* Phase 6 T072 route smoke: every App.tsx route (12) + one insight article.
   Fails on HTTP != 200 or uncaught page errors; reports h1/title for the
   "direct-entry routes are understandable" DoD check. */
const ROUTES = [
  "/",
  "/what-we-do",
  "/ai-company-builder",
  "/solutions",
  "/sectors",
  "/proof",
  "/insights",
  "/insights/sadc-ai-opportunity",
  "/about",
  "/contact",
  "/ask",
  "/legal/privacy",
  "/legal/terms",
];

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  const pageErrors = [];
  page.on("pageerror", (e) => pageErrors.push(String(e)));

  const results = {};
  for (const route of ROUTES) {
    const resp = await page.goto("http://localhost:3001" + route, { waitUntil: "load", timeout: 30000 });
    await page.waitForTimeout(600);
    const info = await page.evaluate(() => ({
      h1: [...document.querySelectorAll("h1")].map((h) => (h.textContent || "").trim()).filter(Boolean),
      title: document.title.trim(),
      main: !!document.querySelector("main"),
      primaryLink: !!document.querySelector('a[href="/contact"]'),
    }));
    results[route] = {
      status: resp ? resp.status() : 0,
      h1Count: info.h1.length,
      h1: info.h1[0] ? info.h1[0].slice(0, 60) : null,
      title: info.title ? info.title.slice(0, 70) : null,
      main: info.main,
      contactPathPresent: info.primaryLink,
    };
  }
  results.__pageErrors = pageErrors;
  console.log(JSON.stringify(results, null, 2));
  await browser.close();
  const statusesOk = ROUTES.every((r) => results[r].status === 200);
  const h1Ok = ROUTES.every((r) => results[r].h1Count >= 1);
  const titlesOk = ROUTES.every((r) => results[r].title);
  process.exit(statusesOk && h1Ok && titlesOk && pageErrors.length === 0 ? 0 : 2);
}
main().catch((e) => { console.error(e); process.exit(1); });
