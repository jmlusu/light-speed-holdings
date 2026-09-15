#!/usr/bin/env node
/**
 * LightSpeed visual_check — Playwright-based screenshot + layout QA probe.
 *
 * Part of the ls-artifact-qa skill. Takes an HTML file or URL, screenshots it at
 * one or more viewports, and reports layout signals (horizontal overflow,
 * missing alt text, empty headings) as JSON.
 *
 * Usage:
 *   node visual_check.js <file-or-url> [--viewport 1280x800] [--out out.png] [--json report.json]
 *
 * Requires the dev dependency `playwright` (declared in the repo package.json).
 * Chromium must be downloaded once: `npx playwright install chromium`.
 */

const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

function parseArgs(argv) {
  const args = { viewports: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--viewport") {
      const [w, h] = argv[++i].split("x").map(Number);
      args.viewports.push({ width: w, height: h });
    } else if (a === "--out") {
      args.out = argv[++i];
    } else if (a === "--json") {
      args.json = argv[++i];
    } else {
      args.target = a;
    }
  }
  if (!args.viewports.length) args.viewports = [{ width: 1280, height: 800 }];
  return args;
}

function toFileUrl(p) {
  return "file:///" + path.resolve(p).replace(/\\/g, "/");
}

(async () => {
  const args = parseArgs(process.argv.slice(2));
  if (!args.target) {
    console.error("Usage: node visual_check.js <file|url> [--viewport WxH] [--out png] [--json json]");
    process.exit(1);
  }

  const browser = await chromium.launch();
  const findings = { target: args.target, checks: [] };

  try {
    for (const vp of args.viewports) {
      const page = await browser.newPage({ viewport: vp });
      const url = /^https?:\/\//.test(args.target) ? args.target : toFileUrl(args.target);
      await page.goto(url, { waitUntil: "networkidle" });

      const report = await page.evaluate(() => {
        const doc = document.documentElement;
        const overflow = doc.scrollWidth - doc.clientWidth;
        const imgs = [...document.querySelectorAll("img")];
        const missingAlt = imgs.filter((i) => !i.hasAttribute("alt"));
        const headings = [...document.querySelectorAll("h1,h2,h3")];
        const emptyHeadings = headings.filter((h) => !(h.textContent || "").trim());
        return {
          viewport: { width: doc.clientWidth, height: doc.clientHeight },
          scrollWidth: doc.scrollWidth,
          scrollHeight: doc.scrollHeight,
          horizontalOverflowPx: overflow,
          imgCount: imgs.length,
          missingAltCount: missingAlt.length,
          headingCount: headings.length,
          emptyHeadingCount: emptyHeadings.length,
        };
      });

      const outPath = args.out
        ? args.out.replace(/\.png$/, `-${vp.width}x${vp.height}.png`)
        : null;
      if (outPath) await page.screenshot({ path: outPath, fullPage: true });

      const entry = { viewport: vp, ...report, screenshot: outPath };
      findings.checks.push(entry);
      console.log(JSON.stringify(entry, null, 2));
      await page.close();
    }
  } finally {
    await browser.close();
  }

  if (args.json) {
    fs.writeFileSync(args.json, JSON.stringify(findings, null, 2), "utf-8");
  }

  const failed = findings.checks.some(
    (c) => c.horizontalOverflowPx > 0 || c.missingAltCount > 0 || c.emptyHeadingCount > 0
  );
  process.exit(failed ? 2 : 0);
})();
