import { chromium } from "playwright-core";

const url = process.argv[2] || "http://localhost:4500";
const browser = await chromium.launch({
  executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
});
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: "networkidle" });

const meta = await page.evaluate(() => {
  const join = document.getElementById("join");
  const foot = document.querySelector(".foot");
  const stage = document.querySelector("#join [data-sc-stage]");
  const st = stage.getBoundingClientRect();
  const foo = foot.getBoundingClientRect();
  return {
    joinTop: join.offsetTop, joinH: join.getBoundingClientRect().height,
    vh: innerHeight, scrollH: document.documentElement.scrollHeight,
    stageRect: { top: st.top, bottom: st.bottom, h: st.height },
    footRect: { top: foo.top, bottom: foo.bottom, left: foo.left, right: foo.right, w: foo.width, h: foo.height },
  };
});

const results = [];
for (const frac of [0.0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]) {
  const sy = Math.round(meta.joinTop + (meta.joinH - meta.vh) * frac);
  const row = await page.evaluate(async (sy) => {
    window.scrollTo({ top: sy, behavior: "instant" });
    await new Promise((r) => setTimeout(r, 120));
    const foot = document.querySelector(".foot");
    const r = foot.getBoundingClientRect();
    const stage = document.querySelector("#join [data-sc-stage]");
    const sr = stage.getBoundingClientRect();
    return { sy, scrollY: window.scrollY, footRect: { top: r.top, bottom: r.bottom, left: r.left, right: r.right }, stageRect: { top: sr.top, bottom: sr.bottom } };
  }, sy);
  if (row.footRect.top < -5 || row.footRect.top > meta.vh + 5) {
    results.push({ skipped: true, ...row });
    continue;
  }

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

  const sample = await page.evaluate(async ({ b64, rect, dpr }) => {
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
    const vl = Math.max(0, rect.left), vt = Math.max(0, rect.top);
    const vr = Math.min(innerWidth, rect.right), vb = Math.min(innerHeight, rect.bottom);
    const x = vl * dpr, y2 = vt * dpr;
    const w = Math.min((vr - vl) * dpr, img.width - x), h = Math.min((vb - vt) * dpr, img.height - y2);
    c.width = 32; c.height = 16;
    g.drawImage(img, x, y2, w, h, 0, 0, 32, 16);
    const d = g.getImageData(0, 0, 32, 16).data;
    let maxL = 0, maxXY = [0, 0], minL = 1, sum = 0, n = 0;
    for (let k = 0; k < d.length; k += 4) {
      const L = lum(d[k], d[k + 1], d[k + 2]);
      if (L > maxL) { maxL = L; maxXY = [(k / 4) % 32, Math.floor((k / 4) / 32)]; }
      if (L < minL) minL = L;
      sum += L; n++;
    }
    const soft = lum(0x9a, 0x9b, 0xa1);
    const white = lum(0xf4, 0xf2, 0xef);
    return {
      maxL: +maxL.toFixed(4), maxCell: maxXY, minL: +minL.toFixed(4), meanL: +(sum / n).toFixed(4),
      ratio_vs_soft: +ratio(soft, maxL).toFixed(2),
      ratio_vs_white: +ratio(white, maxL).toFixed(2),
    };
  }, { b64: bare, rect: row.footRect, dpr: 2 });

  results.push({ sy, footTop: +row.footRect.top.toFixed(0), ...sample });
}

console.log(JSON.stringify({ meta, results }, null, 2));
await browser.close();