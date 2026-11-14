#!/usr/bin/env node
/**
 * Generate AVIF variants for the site's committed content imagery.
 *
 * Context: 35 image references under `src/assets/images/` were written as plain
 * string literals, so Vite never emitted them and they 404 in production. They are
 * also raw 750-900 KB JPEGs, which is far outside the per-kind budgets in
 * `docs/IMAGE_STRATEGY.md` (hero <= 150 KB, thumbnail <= 30 KB). The fix is not to
 * copy the raw files into `public/`: it is to publish derivatives that are inside
 * budget, and keep the committed JPEGs as the source of record.
 *
 * This script is the "opt-in maintenance script (sharp-based, committed variants)"
 * required by Decision 2 of the `#385` decision record. Outputs are committed to
 * git; the deploy is a static Vercel SPA with no image transform service.
 *
 * Guarantees:
 *   - additive only: an existing output is never overwritten without `--force`;
 *   - deterministic: same source bytes produce the same variant bytes;
 *   - budgeted: any variant above its `budgetKb` fails the run, so the budget is
 *     enforced where the bytes are made rather than discovered in review;
 *   - non-destructive: source JPEGs under `src/assets/images/` are read, never
 *     moved or deleted.
 *
 * Usage:
 *   node scripts/maintenance/generate-media-variants.mjs --dry-run   # report, write nothing
 *   node scripts/maintenance/generate-media-variants.mjs             # write missing variants
 *   node scripts/maintenance/generate-media-variants.mjs --force     # regenerate in place
 */

import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";

const ROOT = path.resolve(import.meta.dirname, "..", "..");
const SOURCE_DIR = path.join(ROOT, "src", "assets", "images");
const OUTPUT_DIR = path.join(ROOT, "public", "assets", "images");

const DRY = process.argv.includes("--dry-run");
const FORCE = process.argv.includes("--force");

/**
 * Per-variant ceiling in KB. These 35 images are full-width section and card
 * imagery, so they sit under the hero budget rather than the thumbnail one.
 * A variant above this fails the run: raise it only with a documented reason,
 * because the ceiling is the whole point of publishing derivatives.
 */
const BUDGET_KB = 150;

/** Encoder settings. AVIF at quality 50 measured 39-87 KB on this source set. */
const AVIF = { quality: 50, effort: 4 };

/**
 * Every committed source raster that the site renders, without extension. Each
 * name matches a file at `src/assets/images/<name>.jpg`. Adding an image to the
 * site means adding its stem here, generating, committing the variant, then
 * referencing `/assets/images/<name>.avif`.
 */
const SOURCES = [
  "agent_network_topology_1793816821318",
  "audience_business_leaders_1793515174408",
  "audience_partners_1793515174751",
  "audience_policy_makers_1793515176396",
  "audience_researchers_1793515174898",
  "before_after_sector_bg_daytime_1793890712154",
  "before_after_sector_bg_light_1793889809250",
  "cap1_company_building_1793817051020",
  "cap2_workflow_automation_1793817065625",
  "cap3_agentic_orchestration_1793817079580",
  "cap4_integration_pure_1793817124475",
  "cap5_organizational_memory_1793817139478",
  "cap6_governance_infrastructure_1793817153646",
  "cta_pathway_destination_1793817195986",
  "hero_cinematic_landscape_day",
  "hero_cinematic_landscape_night_1793514971805",
  "identity_triptych_foundations_1793818127924",
  "modular_agent_architecture_1793818142394",
  "pharos_africa_infrastructure_1793514971621",
  "pharos_ai_governance_1793514972204",
  "pharos_ai_orchestration_1793514971486",
  "pharos_article_thumb_cost_1793817753722",
  "pharos_article_thumb_gov_1793817768084",
  "pharos_article_thumb_sadc_1793817783127",
  "pharos_canonical_architecture_1793817675241",
  "pharos_cta_pure_1793817814419",
  "pharos_editorial_hero_1793817662034",
  "philosophy_triptych_clean_1793818099752",
  "solution_agentic_automation_1793514973368",
  "solution_company_builder_1793514972767",
  "solution_market_intelligence_1793514973546",
  "solution_workflow_collapsing_1793514973725",
  "val_prop_bg_night_1793997847272",
  "whitepaper_a_cover_clean_1793817703115",
  "whitepaper_b_cover_clean_1793817739118",
];

const kb = (bytes) => bytes / 1024;

const main = async () => {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const failures = [];
  let written = 0;
  let skipped = 0;
  let totalBytes = 0;

  for (const stem of SOURCES) {
    const source = path.join(SOURCE_DIR, `${stem}.jpg`);
    const target = path.join(OUTPUT_DIR, `${stem}.avif`);

    if (!fs.existsSync(source)) {
      failures.push(`${stem}: source missing at src/assets/images/${stem}.jpg`);
      continue;
    }

    if (fs.existsSync(target) && !FORCE) {
      skipped += 1;
      totalBytes += fs.statSync(target).size;
      console.log(`  skip  ${stem}.avif (exists; use --force to regenerate)`);
      continue;
    }

    const buffer = await sharp(source)
      .rotate() // honour EXIF orientation before it is stripped
      .avif(AVIF)
      .toBuffer();

    const sizeKb = kb(buffer.length);
    const sourceKb = kb(fs.statSync(source).size);
    const verdict = sizeKb > BUDGET_KB ? `OVER BUDGET (${BUDGET_KB} KB)` : "ok";
    console.log(
      `  ${DRY ? "would write" : "write"} ${stem}.avif  ${sourceKb.toFixed(0)} KB -> ${sizeKb.toFixed(0)} KB  ${verdict}`,
    );

    if (sizeKb > BUDGET_KB) {
      failures.push(`${stem}: ${sizeKb.toFixed(0)} KB exceeds the ${BUDGET_KB} KB budget`);
    }
    if (!DRY) {
      fs.writeFileSync(target, buffer);
      written += 1;
    }
    totalBytes += buffer.length;
  }

  console.log(
    `\n${SOURCES.length} sources: ${written} written, ${skipped} skipped, ` +
      `${(totalBytes / 1024 / 1024).toFixed(2)} MB total variant weight.`,
  );

  if (failures.length > 0) {
    console.error(`\n${failures.length} problem(s):`);
    for (const failure of failures) console.error(`  - ${failure}`);
    process.exitCode = 1;
  }
};

await main();
