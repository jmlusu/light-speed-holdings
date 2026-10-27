#!/usr/bin/env node
/**
 * Generate transparent SVG + PNG variants for every LightSpeed Holdings logo.
 *
 * The rule: create a transparent twin ONLY where the existing file is opaque.
 * That is why `dark-bg`, `light-bg`, `mark` and `mark-mono` get a
 * `-transparent.png` but no `-transparent.svg` (their SVGs already have no
 * background), while `avatar`, `favicon`, `full` and `og` get both.
 *
 * Nothing existing is overwritten. This script is additive by construction.
 *
 * Usage:
 *   node scripts/build/generate-logo-variants.mjs --gate     # validate the renderer only
 *   node scripts/build/generate-logo-variants.mjs            # generate all variants
 *   node scripts/build/generate-logo-variants.mjs --dry-run  # report, write nothing
 */

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import sharp from "sharp";

const ROOT = path.resolve(import.meta.dirname, "..", "..");
const LOGO = path.join(ROOT, "brand", "logo");

const DRY = process.argv.includes("--dry-run");
const GATE = process.argv.includes("--gate");

/** Artwork background colour used by the opaque logo canvases (ADR-027). */
const ARTWORK_BG = "#02062F";

/**
 * Every concept in brand/logo/. `opaque` means the SVG carries a full-canvas
 * background rect and therefore needs a `-transparent.svg` twin.
 * `png` is the existing raster sibling used to validate the renderer.
 *
 * `hasTransparentPng` marks a concept whose transparent raster already exists
 * and is canonical (`logo-dark-bg-transparent.png`) — regenerating it would
 * overwrite a committed asset, which this script must never do.
 */
const CONCEPTS = [
  { key: "avatar", size: [1024, 1024], svg: "logo-avatar.svg", opaque: true, png: "logo-avatar.png" },
  { key: "dark-bg", size: [1254, 1254], svg: "logo-dark-bg.svg", opaque: false, png: "logo-dark-bg-transparent.png", hasTransparentPng: true },
  { key: "favicon", size: [512, 512], svg: "logo-favicon.svg", opaque: true, png: "logo-favicon.png" },
  { key: "full", size: [1254, 1254], svg: "logo-full.svg", opaque: true, png: "logo-full.png" },
  { key: "light-bg", size: [1254, 1254], svg: "logo-light-bg.svg", opaque: false, png: "logo-light-bg.png" },
  { key: "mark", size: [609, 388], svg: "logo-mark.svg", opaque: false, png: "logo-mark.png" },
  { key: "mark-mono", size: [609, 388], svg: "logo-mark-mono.svg", opaque: false, png: "logo-mark-mono.png" },
  { key: "og", size: [1200, 630], svg: "logo-og.svg", opaque: true, png: "logo-og.png" },
];

/**
 * Wordmark band per concept, used as an ink probe. These are in each file's own
 * viewBox space: the 1254-square lockups put the wordmark at y=686..1020, while
 * `og` composes that artwork into 1200x630 at scale 0.587713, which lands the
 * wordmark around y=350..528.
 */
const WORDMARK_BAND = {
  full: [686, 1020],
  "light-bg": [686, 1020],
  "dark-bg": [686, 1020],
  og: [340, 550],
};

// --- tiny SVG helpers -------------------------------------------------------

function read(file) {
  return fs.readFileSync(path.join(LOGO, file), "utf8");
}

function write(file, data) {
  const abs = path.join(LOGO, file);
  // Additive-only, enforced rather than promised: never overwrite a committed
  // asset. This is what stops a re-run from clobbering logo-dark-bg-transparent.png.
  if (fs.existsSync(abs) && isTracked(path.relative(ROOT, abs).split(path.sep).join("/"))) {
    throw new Error(`${file} is a committed asset — refusing to overwrite (additive-only policy)`);
  }
  if (DRY) {
    console.log(`  would write ${file} (${typeof data === "string" ? data.length + " chars" : data.length + " bytes"})`);
    return;
  }
  fs.writeFileSync(abs, data);
}

function isTracked(relPath) {
  try {
    execFileSync("git", ["ls-files", "--error-unmatch", "--", relPath], { cwd: ROOT, stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

function parse(svg, file) {
  const open = svg.match(/<svg\b[^>]*>/);
  if (!open) throw new Error(`${file}: no <svg> root element`);
  const start = svg.indexOf(open[0]);
  const end = svg.lastIndexOf("</svg>");
  if (end < start) throw new Error(`${file}: unbalanced <svg>`);
  return { root: open[0], inner: svg.slice(start + open[0].length, end) };
}

/** Remove the single full-canvas background rect, asserting it exists exactly once. */
function stripBackground(inner, size, file) {
  const [w, h] = size;
  const re = new RegExp(
    `<rect\\s+width="${w}"\\s+height="${h}"\\s+fill="[^"]+"\\s*/>\\s*`
  );
  const hits = inner.match(new RegExp(re.source, "g")) ?? [];
  if (hits.length !== 1) {
    throw new Error(
      `${file}: expected exactly 1 full-canvas background rect (${w}x${h}), found ${hits.length}`
    );
  }
  return inner.replace(re, "");
}

function rootTag(size) {
  const [w, h] = size;
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" ` +
    `viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">`
  );
}

// --- rendering --------------------------------------------------------------

async function render(svgText, size, { background } = {}) {
  let img = sharp(Buffer.from(svgText), { density: 72 });
  if (background) {
    // sharp requires a colour object or string here. An [r,g,b] array is NOT
    // accepted and silently falls back to black, which quietly ruins every
    // comparison against a light-background reference.
    const bg = Array.isArray(background)
      ? { r: background[0], g: background[1], b: background[2] }
      : background;
    img = img.flatten({ background: bg });
  }
  return img.resize(size[0], size[1], { fit: "fill" }).png({ compressionLevel: 9 }).toBuffer();
}

async function rawRgba(buffer) {
  return sharp(buffer).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
}

/** Mean absolute per-channel difference over pixels the reference actually covers. */
async function diff(rendered, reference, size) {
  const a = await rawRgba(rendered);
  const b = await rawRgba(await sharp(reference).resize(size[0], size[1], { fit: "fill" }).png().toBuffer());
  const A = a.data, B = b.data;
  const sum = [0, 0, 0];
  let n = 0, max = 0;
  for (let i = 0; i < A.length; i += 4) {
    if (B[i + 3] < 250) continue; // reference has no information here
    for (let k = 0; k < 3; k++) {
      const d = Math.abs(A[i + k] - B[i + k]);
      sum[k] += d;
      if (d > max) max = d;
    }
    n++;
  }
  return { mean: sum.map((s) => s / n), max, n };
}

/**
 * Fraction of pixels inside a horizontal band that differ from the given
 * background colour. Deliberately background-relative rather than
 * "brightness > x": `light-bg` draws its wordmark in navy (#070A40), which is
 * dark on light and would score as zero ink against a brightness test.
 */
async function bandInk(buffer, size, band, background) {
  const { data } = await rawRgba(buffer);
  const [r0, g0, b0] = background;
  const [y0, y1] = band;
  let ink = 0, total = 0;
  for (let y = y0; y < Math.min(y1, size[1]); y++) {
    for (let x = 0; x < size[0]; x++) {
      const i = (y * size[0] + x) * 4;
      total++;
      if (
        Math.abs(data[i] - r0) > 40 ||
        Math.abs(data[i + 1] - g0) > 40 ||
        Math.abs(data[i + 2] - b0) > 40
      ) ink++;
    }
  }
  return total ? ink / total : 0;
}

/** Silhouette IoU: structural agreement with the ink mask, ignoring colour and AA. */
async function silhouetteIoU(rendered, reference, size, background) {
  const bg = Array.isArray(background)
    ? { r: background[0], g: background[1], b: background[2] }
    : background;
  const grey = async (buf) =>
    (
      await sharp(buf)
        .flatten({ background: bg })
        .resize(size[0], size[1], { fit: "fill" })
        .greyscale()
        .raw()
        .toBuffer({ resolveWithObject: true })
    ).data;
  const a = await grey(rendered);
  const b = await grey(await sharp(reference).png().toBuffer());
  let inter = 0, union = 0;
  for (let i = 0; i < a.length; i++) {
    const ia = a[i] < 200, ib = b[i] < 200;
    if (ia && ib) inter++;
    if (ia || ib) union++;
  }
  return union ? inter / union : 1;
}

/** True when the reference PNG is fully opaque, i.e. carries a baked background. */
async function isOpaquePng(file) {
  const { channels } = await sharp(file).metadata();
  if (channels < 4) return true;
  const stats = await sharp(file).stats();
  return stats.channels[3].min >= 250;
}

/**
 * Background colour of a PNG, sampled from its four real corner pixels.
 * Downscaling to a thumbnail and reading the corners does NOT work here: the
 * artwork dominates a 4x4 reduction and every background comes back
 * contaminated (logo-mark.png reads [160,184,220] instead of white).
 */
async function cornerColour(file) {
  const { width, height } = await sharp(file).metadata();
  const pts = [
    [0, 0],
    [width - 1, 0],
    [0, height - 1],
    [width - 1, height - 1],
  ];
  const seen = new Map();
  for (const [left, top] of pts) {
    const { data } = await sharp(file)
      .extract({ left, top, width: 1, height: 1 })
      .removeAlpha()
      .raw()
      .toBuffer({ resolveWithObject: true });
    const key = `${data[0]},${data[1]},${data[2]}`;
    seen.set(key, (seen.get(key) ?? 0) + 1);
  }
  const [winner] = [...seen.entries()].sort((a, b) => b[1] - a[1])[0];
  return winner.split(",").map(Number);
}

// --- renderer gate ----------------------------------------------------------

/**
 * Prove sharp reproduces the committed rasters before any new asset is trusted.
 * The wordmarks are drawn as masked rects, so a renderer without mask support
 * would silently delete the company name — the band-ink probe catches exactly
 * that failure.
 *
 * The comparison is like-for-like, which is the whole point: a transparent SVG
 * is composited onto the reference PNG's *own* baked background before diffing,
 * so `light-bg` (navy wordmark on white) and `mark` (colour on white) are
 * compared on equal terms rather than against a guessed canvas colour.
 */
async function gate() {
  console.log("RENDERER GATE — sharp vs committed PNG siblings (like-for-like)");
  console.log("-".repeat(96));
  const failures = [];
  let worstOverall = 0;

  for (const c of CONCEPTS) {
    if (!c.png) continue;
    const svgPath = path.join(LOGO, c.svg);
    const pngPath = path.join(LOGO, c.png);
    if (!fs.existsSync(svgPath) || !fs.existsSync(pngPath)) continue;

    const refOpaque = await isOpaquePng(pngPath);
    // Composite onto the reference's own baked background when it has one;
    // otherwise use the artwork canvas (white glyphs need navy to be visible).
    const bg = refOpaque ? await cornerColour(pngPath) : null;
    const compareBg = bg ?? ARTWORK_BG;

    const rendered = await render(read(c.svg), c.size, { background: compareBg });

    const { mean, max, n } = await diff(rendered, pngPath, c.size);
    const worst = Math.max(...mean);
    const iou = await silhouetteIoU(rendered, pngPath, c.size, compareBg);
    worstOverall = Math.max(worstOverall, worst);

    const mode = refOpaque ? (c.opaque ? "opaque↔opaque" : "svg→ref-bg ") : "alpha↔alpha ";
    let ink = "";
    const band = WORDMARK_BAND[c.key];
    if (band) {
      const f = await bandInk(rendered, c.size, band, compareBg);
      ink = ` bandInk=${(f * 100).toFixed(2)}%`;
      // The decisive probe: masked wordmark glyphs either render or they do not.
      // A renderer that drops masks scores 0.00% here.
      if (f < 0.005) failures.push(`${c.key}: wordmark band has no ink — masked glyphs dropped`);
    }

    // Two independent criteria, both documented rather than tuned to pass:
    //   silhouette IoU >= 0.97  — the artwork lands in the right place at the
    //                             right shape (this is what catches a renderer
    //                             that drops masked paths)
    //   worst-channel mean <= 4 — colour agreement; the committed `mark` and
    //                             `light-bg` rasters were produced by a
    //                             different process, so glyph-edge AA differs by
    //                             a couple of levels and nothing more
    const structural = iou >= 0.97;
    const colour = worst <= 4;
    const ok = structural && colour ? "PASS" : "FAIL";
    if (ok === "FAIL") {
      if (!structural) failures.push(`${c.key}: silhouette IoU ${iou.toFixed(4)} < 0.97`);
      if (!colour) failures.push(`${c.key}: mean abs diff ${mean.map((v) => v.toFixed(2)).join("/")} > 4`);
    }
    console.log(
      `  ${c.svg.padEnd(22)} ${mode} mean=[${mean.map((v) => v.toFixed(2)).join(", ")}] ` +
        `max=${String(max).padStart(3)} px=${String(n).padStart(7)} iou=${iou.toFixed(4)}${ink.padEnd(15)} ${ok}`
    );
  }

  console.log("-".repeat(96));
  if (failures.length) {
    console.log(`GATE: FAIL (worst mean ${worstOverall.toFixed(2)}/255)`);
    for (const f of failures) console.log("  - " + f);
    process.exitCode = 1;
  } else {
    console.log(
      `GATE: PASS — worst mean ${worstOverall.toFixed(2)}/255 vs committed rasters; wordmarks intact.`
    );
  }
  return failures.length === 0;
}

// --- no-background concept --------------------------------------------------

/**
 * `logo-no-background` has only a JPEG whose transparency is a checkerboard
 * baked into the pixels — it can never be transparent. Build the real thing
 * from the vector mark, matching the JPG's framing: the mark spans 76.27% of
 * the 1024x1024 canvas (measured x 122..902, y 262..761) and is centred.
 */
const NO_BG = { canvas: 1024, widthRatio: 0.7627 };

function buildNoBackgroundSvg() {
  const { root, inner } = parse(read("logo-mark.svg"), "logo-mark.svg");
  const vb = root.match(/viewBox="([^"]+)"/);
  if (!vb) throw new Error("logo-mark.svg: no viewBox");
  const [vx, vy, vw, vh] = vb[1].trim().split(/\s+/).map(Number);

  const targetW = NO_BG.widthRatio * NO_BG.canvas;
  const s = targetW / vw;
  const tx = (NO_BG.canvas - targetW) / 2 - vx * s;
  const ty = (NO_BG.canvas - vh * s) / 2 - vy * s;

  return {
    svg:
      `${rootTag([NO_BG.canvas, NO_BG.canvas])}\n` +
      `  <title>LightSpeed Holdings - no-background mark</title>\n` +
      `  <g transform="translate(${tx.toFixed(3)},${ty.toFixed(3)}) scale(${s.toFixed(6)})">\n` +
      `${inner}\n  </g>\n</svg>\n`,
    expected: [targetW, vh * s],
  };
}

// --- main -------------------------------------------------------------------

async function main() {
  const ok = await gate();
  console.log();
  if (GATE || !ok) {
    if (!ok) console.log("Refusing to generate from an unvalidated renderer.");
    return;
  }

  const written = [];

  // 1. Transparent SVGs for the concepts whose SVG is opaque.
  for (const c of CONCEPTS) {
    if (!c.opaque) continue;
    const file = `logo-${c.key}-transparent.svg`;
    const { root, inner } = parse(read(c.svg), c.svg);
    const stripped = stripBackground(inner, c.size, c.svg);
    if (stripped === inner) throw new Error(`${c.svg}: background rect not removed`);
    write(file, `${root}\n${stripped}\n</svg>\n`);
    written.push(file);
  }

  // 3. The no-background concept: a real vector, plus its raster.
  const noBg = buildNoBackgroundSvg();
  write("logo-no-background.svg", noBg.svg);
  written.push("logo-no-background.svg");

  // 4. Transparent PNGs, rendered from vector at each concept's native size.
  //    `dark-bg` is skipped: its transparent raster is already canonical and
  //    this script must not regenerate (overwrite) a committed asset.
  const pngSources = CONCEPTS.filter((c) => !c.hasTransparentPng).map((c) => ({
    size: c.size,
    svg: c.opaque ? `logo-${c.key}-transparent.svg` : c.svg,
    out: `logo-${c.key}-transparent.png`,
  }));
  pngSources.push({
    size: [NO_BG.canvas, NO_BG.canvas],
    svg: "logo-no-background.svg",
    out: "logo-no-background.png",
  });

  for (const s of pngSources) {
    const buf = await render(read(s.svg), s.size);
    write(s.out, buf);
    written.push(`${s.out} (${s.size[0]}x${s.size[1]})`);
  }

  console.log();
  console.log(`${DRY ? "WOULD WRITE" : "WROTE"} ${written.length} files in brand/logo/:`);
  for (const w of written) console.log("  " + w);
}

main().catch((err) => {
  console.error("FAILED:", err.message);
  process.exitCode = 1;
});
