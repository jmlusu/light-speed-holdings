const { chromium } = require("playwright");

/* Phase 5 QA probe: journey instrumentation client (spec §39/§40).
   Captures POSTs to /api/journey-events (404 in dev is expected — the client
   must fail silently) and asserts the whitelisted content events fire with
   sessionId/timestamp/route intact and zero uncaught page errors. */
async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

  const posts = [];
  const pageErrors = [];
  page.on("request", (req) => {
    if (req.url().includes("/api/journey-events") && req.method() === "POST") {
      try {
        const body = JSON.parse(req.postData() || "[]");
        posts.push(...(Array.isArray(body) ? body : [body]));
      } catch {
        posts.push({ parseError: true });
      }
    }
  });
  page.on("pageerror", (err) => pageErrors.push(String(err)));

  const waitFlush = () => page.waitForTimeout(5600);

  await page.goto("http://localhost:3001/", { waitUntil: "load", timeout: 30000 });
  await waitFlush();
  await page.goto("http://localhost:3001/solutions#ai-company-builder", { waitUntil: "load", timeout: 30000 });
  await waitFlush();
  await page.goto("http://localhost:3001/sectors#financial-services", { waitUntil: "load", timeout: 30000 });
  await waitFlush();
  await page.goto("http://localhost:3001/proof", { waitUntil: "load", timeout: 30000 });
  await waitFlush();
  await page.goto("http://localhost:3001/insights", { waitUntil: "load", timeout: 30000 });
  await waitFlush();

  const types = posts.map((p) => p.eventType);
  const sessions = new Set(posts.map((p) => p.sessionId));
  const results = {
    capturedPosts: posts.length,
    hasPageView: types.includes("page_view"),
    hasSolutionView: types.includes("solution_view") && posts.some((p) => p.eventType === "solution_view" && p.solution === "ai-company-builder"),
    hasSectorView: types.includes("sector_view") && posts.some((p) => p.eventType === "sector_view" && p.sector === "financial-services"),
    hasProofView: types.includes("proof_view") && posts.some((p) => p.eventType === "proof_view" && p.journeyStage === "consideration"),
    hasInsightView: types.includes("insight_view") && posts.some((p) => p.eventType === "insight_view" && p.contentType === "index"),
    envelopeValid: posts.every((p) => typeof p.sessionId === "string" && p.sessionId.length > 0 && typeof p.timestamp === "string" && typeof p.route === "string"),
    stableSession: sessions.size === 1 && !sessions.has(undefined),
    noPageErrors: pageErrors.length === 0,
    pageErrors,
  };

  console.log(JSON.stringify(results, null, 2));
  await browser.close();
  const ok = results.capturedPosts > 0 && results.hasPageView && results.hasSolutionView &&
    results.hasSectorView && results.hasProofView && results.hasInsightView &&
    results.envelopeValid && results.stableSession && results.noPageErrors;
  process.exit(ok ? 0 : 2);
}
main().catch((e) => { console.error(e); process.exit(1); });
