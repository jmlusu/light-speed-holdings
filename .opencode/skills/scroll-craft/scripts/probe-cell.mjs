import { chromium } from "playwright-core";

const url = process.argv[2] || "http://localhost:4500";
const browser = await chromium.launch({
  executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
});
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: "networkidle" });

const sy = Number(process.argv[3]);
const needle = process.argv[4] || "";
await page.evaluate((sy) => {
  window.scrollTo({ top: sy, behavior: "instant" });
  return new Promise((r) => setTimeout(r, 120));
}, sy);

await page.evaluate(() => {
  document.querySelectorAll("body *").forEach((el) => {
    if (getComputedStyle(el).position !== "fixed") return;
    if (el.closest("[data-sc-world],[data-sc-world-copy]")) return;
    el.setAttribute("data-sc-shot-fixed", "");
  });
});
await page.addStyleTag({
  content: "[data-sc-cue],[data-sc-cue] *,[data-sc-copy],[data-sc-copy] *,[data-sc-shot-fixed]{visibility:hidden!important}",
});
const bare = (await page.screenshot({ type: "jpeg", quality: 80 })).toString("base64");
await page.evaluate(() => {
  const t = [...document.querySelectorAll("style")].pop();
  if (t && t.textContent.includes("data-sc-cue")) t.remove();
  document.querySelectorAll("[data-sc-shot-fixed]").forEach((el) => el.removeAttribute("data-sc-shot-fixed"));
});

const out = await page.evaluate(async ({ b64, dpr, needle }) => {
  const img = new Image();
  img.src = "data:image/jpeg;base64," + b64;
  await img.decode();
  const c = document.createElement("canvas");
  const g = c.getContext("2d", { willReadFrequently: true });
  const lum = (r, gr, b) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(gr) + 0.0722 * f(b);
  };
  const ratio = (a, b) => (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);

  const els = [...document.querySelectorAll("[data-sc-cue],[data-sc-copy]")].filter((el) =>
    (el.textContent || "").replace(/\s+/g, " ").trim().startsWith(needle));
  if (!els.length) return { error: "no match for: " + needle };
  const el = els[0];
  const r = el.getBoundingClientRect();
  const vl = Math.max(0, r.left), vt = Math.max(0, r.top);
  const vr = Math.min(innerWidth, r.right), vb = Math.min(innerHeight, r.bottom);
  const x = vl * dpr, y2 = vt * dpr;
  const w = Math.min((vr - vl) * dpr, img.width - x), h = Math.min((vb - vt) * dpr, img.height - y2);
  c.width = 32; c.height = 16;
  g.drawImage(img, x, y2, w, h, 0, 0, 32, 16);
  const d = g.getImageData(0, 0, 32, 16).data;
  let maxL = 0, maxXY = [0, 0], maxRGB = [0, 0, 0], minL = 1, sum = 0, n = 0;
  const cells = [];
  for (let i = 0; i < 16; i++) {
    const row = [];
    for (let j = 0; j < 32; j++) {
      const k = (i * 32 + j) * 4;
      const L = lum(d[k], d[k + 1], d[k + 2]);
      if (L > maxL) { maxL = L; maxXY = [j, i]; maxRGB = [d[k], d[k + 1], d[k + 2]]; }
      if (L < minL) minL = L;
      sum += L; n++;
      row.push(L > 0.05 ? "#" : L > 0.02 ? "+" : L > 0.01 ? "." : " ");
    }
    cells.push(row.join(""));
  }
  const soft = lum(0x9a, 0x9b, 0xa1);
  const white = lum(0xf4, 0xf2, 0xef);
  return {
    txt: (el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 40),
    rect: { top: +r.top.toFixed(0), left: +r.left.toFixed(0), w: +r.width.toFixed(0), h: +r.height.toFixed(0) },
    maxL: +maxL.toFixed(4), maxCell: maxXY, maxRGB,
    meanL: +(sum / n).toFixed(4),
    ratio_vs_white: +ratio(white, maxL).toFixed(2),
    ratio_vs_soft: +ratio(soft, maxL).toFixed(2),
    grid: cells,
  };
}, { b64: bare, dpr: 2, needle });

console.log(JSON.stringify(out, null, 2));
await browser.close();