#!/usr/bin/env node
/**
 * scrollcraft tab-focus check: tab through every focusable anchor with real
 * (trusted) key presses and assert each stop shows a visible focus ring.
 *
 *   node tab-focus.mjs --url http://localhost:4500
 *   node tab-focus.mjs --url http://localhost:4500 --reduced-motion
 *
 * Uses the INSTALLED Chrome (same rule as shoot.mjs).
 */
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

let chromium;
try {
  ({ chromium } = createRequire(path.join(process.cwd(), "package.json"))("playwright-core"));
} catch {
  console.error("playwright-core not found. Run this in the build project after:\n  npm i playwright-core");
  process.exit(1);
}

const argv = process.argv.slice(2);
const arg = (n, d) => { const i = argv.indexOf(n); return i > -1 && argv[i + 1] ? argv[i + 1] : d; };
const has = (n) => argv.includes(n);

const URL = arg("--url", "http://localhost:4500");
const W = parseInt(arg("--width", "1440"), 10);
const H = parseInt(arg("--height", "900"), 10);
const REDUCED = has("--reduced-motion");

const CHROME = [
  process.env.SCROLLCRAFT_CHROME,
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/Applications/Chromium.app/Contents/MacOS/Chromium",
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
  "/usr/bin/google-chrome",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser",
  "/snap/bin/chromium",
].find((p) => p && fs.existsSync(p));

if (!CHROME) {
  console.error("No installed Chrome found. Set SCROLLCRAFT_CHROME to its path.");
  process.exit(1);
}

const browser = await chromium.launch({ executablePath: CHROME, headless: true });
const page = await browser.newPage({
  viewport: { width: W, height: H },
  deviceScaleFactor: 1,
  reducedMotion: REDUCED ? "reduce" : "no-preference",
});

await page.goto(URL, { waitUntil: "networkidle" });

const expected = await page.evaluate(() => {
  const tabbables = () =>
    [...document.querySelectorAll(
      'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )].filter((e) => {
      if (e.matches(":disabled")) return false;
      if (e.hidden) return false;
      const st = getComputedStyle(e);
      return st.display !== "none" && st.visibility !== "hidden";
    });
  return tabbables().length;
});

const results = [];
const seen = new Set();
let wrapped = false;
let seenAny = false;

for (let i = 0; i < expected * 2 + 4; i++) {
  await page.keyboard.press("Tab");
  await page.waitForTimeout(120); // let focus-driven cue/scroll settle

  const state = await page.evaluate(() => {
    const el = document.activeElement;
    if (!el || el === document.body) return null;
    const s = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const tabbables = [...document.querySelectorAll(
      'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )].filter((e) => {
      if (e.matches(":disabled")) return false;
      if (e.hidden) return false;
      const st = getComputedStyle(e);
      return st.display !== "none" && st.visibility !== "hidden";
    });
    return {
      idx: tabbables.indexOf(el),
      tag: el.tagName.toLowerCase(),
      text: (el.textContent || el.value || "").trim().slice(0, 50),
      href: el.getAttribute("href") || "",
      focusVisible: typeof el.matches === "function" ? el.matches(":focus-visible") : false,
      outline: {
        style: s.outlineStyle,
        width: s.outlineWidth,
        color: s.outlineColor,
      },
      boxShadow: s.boxShadow,
      rect: { top: r.top, left: r.left, w: r.width, h: r.height },
      inViewport: r.width > 1 && r.height > 1 &&
        r.top >= -1 && r.bottom <= window.innerHeight + 60 &&
        r.left >= -1 && r.right <= window.innerWidth + 60,
    };
  });

  if (!state) {
    if (seenAny) { wrapped = true; break; }
    results.push({ i, dead: true });
    continue;
  }
  seenAny = true;
  if (state.idx === -1 || seen.has(state.idx)) { wrapped = true; break; }
  seen.add(state.idx);
  results.push({ i, ...state });
  if (seen.size >= expected) break;
}

let failures = 0;
console.log(`expected focusable: ${expected}, stops hit: ${results.filter((r) => !r.dead).length}`);
for (const r of results) {
  if (r.dead) { console.log(`${r.i}. (focus on body / dead stop)`); failures++; continue; }

  const ring =
    (r.outline.style !== "none" && parseFloat(r.outline.width) > 0 &&
      r.outline.color !== "transparent" && !r.outline.color.startsWith("rgba(0, 0, 0, 0)"))
      ? `outline ${r.outline.width} ${r.outline.color}`
      : (r.boxShadow && r.boxShadow !== "none" ? `box-shadow ${r.boxShadow.slice(0, 60)}` : null);
  const focusableOk = r.focusVisible;
  const ok = !!ring && r.inViewport;
  if (!ok) failures++;
  console.log(
    `${r.i}. <${r.tag}> "${r.text}" focus-visible=${focusableOk} viewport=${r.inViewport ? "ok" : "OFF"} ring=${ring || "NONE"}${ok ? "" : "  <<< FAIL"}`
  );
}

console.log(failures === 0 ? "\nFOCUS CHECK PASS" : `\nFOCUS CHECK FAIL (${failures})`);
await browser.close();
process.exit(failures === 0 ? 0 : 1);