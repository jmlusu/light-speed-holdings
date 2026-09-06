import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { parse } from "yaml";

interface Agent { id: string; type: string; department?: string; }
interface Registry { company?: { name?: string; agents?: Agent[] } }

const ROOT = resolve(import.meta.dirname ?? ".", "../..");
const REGISTRY_PATH = resolve(ROOT, "company-registry.yaml");
const CHANGELOG_PATH = resolve(ROOT, "CHANGELOG.md");

function main() {
  const raw = readFileSync(REGISTRY_PATH, "utf-8");
  const data = parse(raw) as Registry;
  const agents = data?.company?.agents ?? [];
  const byType = agents.reduce<Record<string, number>>((acc, a) => { acc[a.type] = (acc[a.type] ?? 0) + 1; return acc; }, {});
  const byDept = agents.reduce<Record<string, number>>((acc, a) => {
    const d = a.department ?? "Unknown"; acc[d] = (acc[d] ?? 0) + 1; return acc;
  }, {});
  let changelogHead = "";
  try { changelogHead = readFileSync(CHANGELOG_PATH, "utf-8").slice(0, 2000); } catch {}

  const meta = {
    generatedAt: new Date().toISOString(),
    company: data?.company?.name ?? "Light Speed Holdings",
    agents: {
      total: agents.length,
      byType,
      byDept,
    },
    stack: {
      generator: "src/ai_company/generator.py",
      messageBus: "src/ai_company/orchestrator/message_bus.py",
      dashboard: "src/ai_company/dashboard/app.py",
    },
    changelogHead,
    version: process.env.npm_package_version ?? "0.0.1",
  };

  const outDir = resolve(import.meta.dirname ?? ".", "../public");
  mkdirSync(outDir, { recursive: true });
  writeFileSync(resolve(outDir, "product-meta.json"), JSON.stringify(meta, null, 2), "utf-8");

  // Also emit src/content/product.json for MDX import (content layer)
  const contentDir = resolve(import.meta.dirname ?? ".", "../src/content");
  mkdirSync(contentDir, { recursive: true });
  writeFileSync(resolve(contentDir, "product.json"), JSON.stringify(meta, null, 2), "utf-8");

  console.log(`[export-product-meta] ${agents.length} agents → public/product-meta.json + src/content/product.json`);
}

main();
