#!/usr/bin/env node
/**
 * LightSpeed visual_check — Playwright-based screenshot + layout QA probe.
 *
 * Part of the ls-artifact-qa skill. Takes an HTML file or URL, screenshots it at
 * one or more viewports, and reports layout signals (horizontal overflow,
 * missing alt text, empty headings, alt quality, decorative images, logo context) as JSON.
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

// Generic words that indicate poor alt text quality
const GENERIC_ALT_WORDS = new Set([
  "image", "photo", "picture", "screenshot", "screencapture",
  "diagram", "chart", "graph", "graphic", "illustration",
  "logo", "icon", "iconic", "symbol", "badge",
  "visual", "visualization", "figure", "fig",
  "img", "pic", "snap", "shot"
]);

function hasNounAndVerbPhrase(text) {
  // Simple heuristic: at least 3 words, and not all words are generic
  const words = text.trim().toLowerCase().split(/\s+/);
  if (words.length < 3) return false;
  const nonGeneric = words.filter(w => !GENERIC_ALT_WORDS.has(w));
  return nonGeneric.length >= 2; // At least 2 meaningful words
}

function checkAltQuality(alt) {
  const failures = [];
  const lower = alt.toLowerCase().trim();

  if (lower.length < 10) {
    failures.push("too_short");
  }

  // Check for generic words
  const words = lower.split(/\s+/);
  const hasGeneric = words.some(w => GENERIC_ALT_WORDS.has(w));
  if (hasGeneric) {
    failures.push("generic_words");
  }

  if (!hasNounAndVerbPhrase(alt)) {
    failures.push("insufficient_descriptiveness");
  }

  return failures;
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

        // Image analysis
        const imgs = [...document.querySelectorAll("img")];
        const missingAlt = imgs.filter((i) => !i.hasAttribute("alt"));

        // Image type classification
        const typedImages = imgs.filter((i) => i.hasAttribute("data-ls-image-type"));
        const untypedImages = imgs.filter((i) => !i.hasAttribute("data-ls-image-type"));
        const validTypes = new Set(["screenshot", "diagram", "metrics", "brand-mark", "illustration"]);
        const invalidTypes = typedImages.filter((i) => !validTypes.has(i.getAttribute("data-ls-image-type")));

        // Decorative images (brand-mark used for branding only)
        const decorativeImages = typedImages.filter((i) => i.getAttribute("data-ls-image-type") === "brand-mark" && i.hasAttribute("aria-hidden"));
        const decorativeWithAlt = decorativeImages.filter((i) => i.hasAttribute("alt") && i.getAttribute("alt").trim() !== "");

        // Informative images missing alt
        const informativeTypes = new Set(["screenshot", "diagram", "metrics", "illustration"]);
        const informativeImages = typedImages.filter((i) => informativeTypes.has(i.getAttribute("data-ls-image-type")));
        const informativeMissingAlt = informativeImages.filter((i) => !i.hasAttribute("alt"));

        // Alt text quality for informative images
        let altQualityFailures = 0;
        informativeImages.forEach((img) => {
          if (img.hasAttribute("alt")) {
            const failures = checkAltQuality(img.getAttribute("alt"));
            if (failures.length > 0) altQualityFailures++;
          }
        });

        // Brand logo context
        const logoImages = typedImages.filter((i) => i.getAttribute("data-ls-image-type") === "brand-mark");
        let logoAltMismatch = 0;
        let firstLogoSeen = false;
        logoImages.forEach((img) => {
          const instance = img.getAttribute("data-ls-logo-instance");
          if (instance === "first") {
            if (!img.hasAttribute("alt") || img.getAttribute("alt") !== "LightSpeed Holdings Limited") {
              logoAltMismatch++;
            }
            firstLogoSeen = true;
          } else if (instance === "repeat") {
            if (!img.hasAttribute("aria-hidden") || img.getAttribute("aria-hidden") !== "true") {
              logoAltMismatch++;
            }
          } else {
            // No instance marker = ambiguous
            logoAltMismatch++;
          }
        });

        // Headings
        const headings = [...document.querySelectorAll("h1,h2,h3")];
        const emptyHeadings = headings.filter((h) => !(h.textContent || "").trim());

        return {
          viewport: { width: doc.clientWidth, height: doc.clientHeight },
          scrollWidth: doc.scrollWidth,
          scrollHeight: doc.scrollHeight,
          horizontalOverflowPx: overflow,
          imgCount: imgs.length,
          missingAltCount: missingAlt.length,
          untypedImageCount: untypedImages.length,
          invalidImageTypeCount: invalidTypes.length,
          decorativeWithAltCount: decorativeWithAlt.length,
          informativeMissingAltCount: informativeMissingAlt.length,
          altQualityFailures,
          logoAltMismatchCount: logoAltMismatch,
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
    (c) =>
      c.horizontalOverflowPx > 0 ||
      c.missingAltCount > 0 ||
      c.emptyHeadingCount > 0 ||
      c.untypedImageCount > 0 ||
      c.invalidImageTypeCount > 0 ||
      c.decorativeWithAltCount > 0 ||
      c.informativeMissingAltCount > 0 ||
      c.altQualityFailures > 0 ||
      c.logoAltMismatchCount > 0
  );
  process.exit(failed ? 2 : 0);
})();