import { chromium } from "playwright";

const BASE = "http://localhost:1440/";
const results = [];
const consoleErrors = [];
const failedRequests = [];

function ok(name, pass, detail) {
  results.push({ name, pass, detail });
  console.log(`${pass ? "PASS" : "FAIL"}  ${name}${detail ? " — " + detail : ""}`);
}

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

page.on("console", (msg) => {
  if (msg.type() === "error") consoleErrors.push(msg.text());
});
page.on("requestfailed", (req) => {
  failedRequests.push(`${req.method()} ${req.url()} :: ${req.failure()?.errorText}`);
});
page.on("response", (res) => {
  if (res.status() >= 400) failedRequests.push(`HTTP ${res.status()} ${res.url()}`);
});

await page.goto(BASE, { waitUntil: "networkidle", timeout: 30000 });
await page.waitForTimeout(800);

// All brand logo images on live home page
const logos = page.locator('img[data-ls-image-type="brand-mark"], img[src*="/brand/logo/"]');
const logoCount = await logos.count();
ok("brand logo images present", logoCount > 0, `count=${logoCount}`);

const logoInfo = [];
for (let i = 0; i < logoCount; i++) {
  const el = logos.nth(i);
  const info = await el.evaluate((n) => ({
    src: n.getAttribute("src"),
    alt: n.getAttribute("alt"),
    instance: n.getAttribute("data-ls-logo-instance"),
    naturalWidth: n.naturalWidth,
    naturalHeight: n.naturalHeight,
    complete: n.complete,
    rect: (() => { const r = n.getBoundingClientRect(); return { w: r.width, h: r.height, top: r.top }; })(),
  }));
  logoInfo.push(info);
  console.log(`  logo[${i}]`, JSON.stringify(info));
}

// Header = first logo (FloatingNav, instance=first); Footer = last (instance=repeat)
const headerLogo = logoInfo.find((l) => l.instance === "first") || logoInfo[0];
const footerLogo = logoInfo.find((l) => l.instance === "repeat") || logoInfo[logoInfo.length - 1];

ok(
  "header logo uses new flat system path",
  headerLogo && /^\/brand\/logo\/logo-full\.(svg|png)$/.test(headerLogo.src),
  `src=${headerLogo?.src}`
);
ok(
  "header logo loaded (natural size > 0)",
  headerLogo && headerLogo.naturalWidth > 0 && headerLogo.naturalHeight > 0,
  `natural=${headerLogo?.naturalWidth}x${headerLogo?.naturalHeight}`
);
ok("header logo visible (rect > 0)", headerLogo && headerLogo.rect.w > 0 && headerLogo.rect.h > 0, `rect=${JSON.stringify(headerLogo?.rect)}`);

ok(
  "footer logo uses new flat system path",
  footerLogo && /^\/brand\/logo\/logo-full\.(svg|png)$/.test(footerLogo.src),
  `src=${footerLogo?.src}`
);
ok(
  "footer logo loaded (natural size > 0)",
  footerLogo && footerLogo.naturalWidth > 0 && footerLogo.naturalHeight > 0,
  `natural=${footerLogo?.naturalWidth}x${footerLogo?.naturalHeight}`
);
ok("footer logo visible (rect > 0)", footerLogo && footerLogo.rect.w > 0 && footerLogo.rect.h > 0, `rect=${JSON.stringify(footerLogo?.rect)}`);

// Brand red #DC3641
const red = await page.evaluate(() => {
  const hits = [];
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch { continue; }
    for (const rule of rules) {
      const t = rule.cssText || "";
      if (/dc3641/i.test(t)) hits.push(t.slice(0, 100));
    }
  }
  const root = getComputedStyle(document.documentElement);
  const lsRed =
    root.getPropertyValue("--ls-red").trim() ||
    root.getPropertyValue("--color-ls-red").trim() ||
    root.getPropertyValue("--color-red").trim();
  // sample a CTA button if present
  const cta = document.querySelector('a[class*="cta"], button[class*="cta"], a[href*="briefing"], a[href*="contact"]');
  const ctaBg = cta ? getComputedStyle(cta).backgroundColor : null;
  return { ruleHits: hits.length, lsRed, ctaBg, sample: hits.slice(0, 2) };
});
ok("brand red #DC3641 in stylesheets", red.ruleHits > 0, `ruleHits=${red.ruleHits}`);
ok("--ls-red / --color-red resolves to #DC3641", /^#dc3641$/i.test(red.lsRed), `value=${red.lsRed || "(empty)"}`);

// No legacy paths in DOM
const legacy = await page.evaluate(() => {
  const html = document.documentElement.innerHTML;
  return {
    fulllogo: /fulllogo/i.test(html),
    icononly: /icononly/i.test(html),
    brandLogosPlural: /brand\/logos\//.test(html),
  };
});
ok("no fulllogo in DOM", !legacy.fulllogo, JSON.stringify(legacy));
ok("no icononly in DOM", !legacy.icononly);
ok("no /brand/logos/ (plural) in DOM", !legacy.brandLogosPlural);

// Screenshots
const firstLogoEl = logos.first();
if (await firstLogoEl.count()) {
  const box = await firstLogoEl.boundingBox();
  if (box && box.width > 0 && box.height > 0) {
    await page.screenshot({
      path: "C:\\Users\\jmlus\\AppData\\Local\\Temp\\opencode\\ws-e-header.png",
      clip: { x: Math.max(0, box.x - 16), y: Math.max(0, box.y - 16), width: Math.min(box.width + 32, 400), height: Math.min(box.height + 32, 80) },
    });
    console.log("saved header screenshot");
  }
}
const lastLogoEl = logos.last();
if (await lastLogoEl.count()) {
  const box = await lastLogoEl.boundingBox();
  if (box && box.width > 0 && box.height > 0) {
    await page.screenshot({
      path: "C:\\Users\\jmlus\\AppData\\Local\\Temp\\opencode\\ws-e-footer.png",
      clip: { x: Math.max(0, box.x - 16), y: Math.max(0, box.y - 16), width: Math.min(box.width + 32, 400), height: Math.min(box.height + 32, 80) },
    });
    console.log("saved footer screenshot");
  }
}
await page.screenshot({ path: "C:\\Users\\jmlus\\AppData\\Local\\Temp\\opencode\\ws-e-index-full.png", fullPage: false });
console.log("saved full viewport screenshot");

// Console + network
ok("no console errors", consoleErrors.length === 0, consoleErrors.slice(0, 5).join(" | ") || "clean");
// filter noisy favicon/analytics if any
const realFails = failedRequests.filter((f) => !/favicon|analytics|plausible|doubleclick/i.test(f));
ok("no failed brand/API requests", realFails.length === 0, realFails.slice(0, 8).join(" | ") || "clean");

const fails = results.filter((r) => !r.pass);
console.log("\n=== SUMMARY ===");
console.log(`pass=${results.length - fails.length} fail=${fails.length}`);
if (fails.length) {
  fails.forEach((f) => console.log(`  FAIL: ${f.name} — ${f.detail}`));
  process.exitCode = 1;
}
await browser.close();
