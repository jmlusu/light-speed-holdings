import { chromium } from "playwright-core";

const url = process.argv[2] || "http://localhost:4500";
const browser = await chromium.launch({
  executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
});
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: "networkidle" });

const probe = await page.evaluate(async () => {
  const join = document.getElementById("join");
  if (!join) return { err: "no #join" };
  window.scrollTo(0, join.offsetTop + join.getBoundingClientRect().height - innerHeight * 0.96);
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));

  const foot = document.querySelector(".foot");
  if (!foot) return { err: "no .foot" };
  const r = foot.getBoundingClientRect();

  const scrim = document.querySelector("#join .sc-scrim--band");
  const sc = scrim ? getComputedStyle(scrim) : null;
  const stage = foot.closest("[data-sc-stage]") || foot.closest(".sc-stage");
  const st = stage ? getComputedStyle(stage) : null;

  return {
    rect: { left: r.left, top: r.top, right: r.right, bottom: r.bottom, w: r.width, h: r.height },
    scrimBg: sc ? sc.backgroundImage : "(no scrim element)",
    scrimAlpha: sc ? sc.opacity : null,
    stagePos: st ? st.position : null,
    stageHeight: st ? st.height : null,
    footZ: getComputedStyle(foot).zIndex,
    footColor: getComputedStyle(foot).color,
    nameColor: getComputedStyle(document.querySelector(".foot__name")).color,
    hasCopy: foot.hasAttribute("data-sc-copy"),
    viewport: [innerWidth, innerHeight],
  };
});

if (probe.err) {
  console.log(JSON.stringify(probe));
  await browser.close();
  process.exit(1);
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
  let maxL = 0, minL = 1, sum = 0, n = 0;
  for (let k = 0; k < d.length; k += 4) {
    const L = lum(d[k], d[k + 1], d[k + 2]);
    if (L > maxL) maxL = L;
    if (L < minL) minL = L;
    sum += L; n++;
  }
  const soft = lum(0x9a, 0x9b, 0xa1);       // #9a9ba1 ink-soft
  const white = lum(0xf4, 0xf2, 0xef);      // #f4f2ef ink
  return {
    maxL: +maxL.toFixed(4), minL: +minL.toFixed(4), meanL: +(sum / n).toFixed(4),
    ratio_vs_soft: +ratio(soft, maxL).toFixed(2),
    ratio_vs_white: +ratio(white, maxL).toFixed(2),
  };
}, { b64: bare, rect: probe.rect, dpr: 2 });

console.log(JSON.stringify({ probe, sample }, null, 2));
await browser.close();