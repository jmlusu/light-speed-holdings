const { chromium } = require("playwright");

/* Phase 6 T072 WCAG AA contrast spot check (heuristic):
   walks text-bearing elements, computes effective background (first opaque
   ancestor), skips anything over images/gradients, flags ratio < 4.5
   (normal) / < 3.0 (large: >=24px or >=18.66px bold). */
const ROUTES = ["/", "/what-we-do", "/ai-company-builder", "/solutions", "/sectors", "/proof", "/insights", "/about", "/contact"];

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  const all = [];

  for (const route of ROUTES) {
    await page.goto("http://localhost:3001" + route, { waitUntil: "load", timeout: 30000 });
    await page.waitForTimeout(800);
    const fails = await page.evaluate(() => {
      const parse = (c) => {
        const m = (c || "").match(/rgba?\(([^)]+)\)/);
        if (!m) return null;
        const p = m[1].split(",").map((x) => parseFloat(x));
        return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
      };
      const lum = ({ r, g, b }) => {
        const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
      };
      const ratio = (f, b) => {
        const l1 = lum(f), l2 = lum(b);
        return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
      };
      const effBg = (el) => {
        let n = el;
        while (n && n !== document.documentElement) {
          const s = getComputedStyle(n);
          if (s.backgroundImage && s.backgroundImage !== "none") return null;
          const c = parse(s.backgroundColor);
          if (c && c.a >= 0.95) return c;
          n = n.parentElement;
        }
        return { r: 255, g: 255, b: 255, a: 1 };
      };
      const out = [];
      const seen = new Set();
      for (const el of document.querySelectorAll("body *")) {
        const direct = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
        if (!direct) continue;
        const s = getComputedStyle(el);
        if (s.display === "none" || s.visibility === "hidden" || parseFloat(s.opacity) < 0.5) continue;
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) continue;
        const fg = parse(s.color);
        const bg = effBg(el);
        if (!fg || !bg || fg.a < 0.95) continue;
        const size = parseFloat(s.fontSize);
        const weight = parseInt(s.fontWeight) || 400;
        const large = size >= 24 || (size >= 18.66 && weight >= 700);
        const r = ratio(fg, bg);
        const need = large ? 3 : 4.5;
        if (r < need) {
          const key = `${s.color}|${el.tagName}|${(el.textContent || "").trim().slice(0, 30)}`;
          if (seen.has(key)) continue;
          seen.add(key);
          out.push({
            ratio: Math.round(r * 100) / 100, need,
            fg: s.color, bg: `rgb(${bg.r}, ${bg.g}, ${bg.b})`,
            tag: el.tagName, cls: (el.className || "").toString().slice(0, 50),
            text: (el.textContent || "").trim().slice(0, 45),
          });
        }
      }
      return out;
    });
    if (fails.length) all.push({ route, fails });
  }
  console.log(JSON.stringify(all, null, 2));
  await browser.close();
  process.exit(all.length === 0 ? 0 : 2);
}
main().catch((e) => { console.error(e); process.exit(1); });
