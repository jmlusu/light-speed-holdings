# REA Feasibility — Internal Use Cases (Lightspeed Holdings Engineering)

**Date:** 2026-10-17
**Author:** CTO / VP-Engineering stream
**Audience:** Executive team; feeds the consolidated feasibility verdict
**Scope:** Internal-only applications of Reverse Engineer Anything (REA, `morluto/rea`) inside Lightspeed Holdings. Client-facing product offerings are assessed in a separate stream's file in this same directory. All capability facts cite the shared brief `reports/rea-feasibility/00-rea-capabilities.md` (source IDs S1–S17 as defined there).

**Estate assessed:** `ai-company` Python package v0.6.0 (Python ≥3.12, Typer CLI, FastAPI CEO Dashboard), repo-root Vite/React SPA (production at `lightspeedholdings.vercel.app`), Docker/Compose delivery, ~90 generated agent cards in `.opencode/agents/` from `company-registry.yaml` via Jinja2, 12 GitHub Actions workflows, 6 required checks on `main`, pre-commit ruff/mypy/bandit. Engineering roles referenced: `lead_backend`, `lead_frontend`, `integration_engineer`, `qa_lead`, `test_engineering_lead`, `release_manager`, `platform_engineer`, `devops_lead`, `red_team_engineer`, plus security roles (owned by the security stream).

---

## 1. Competitive intelligence (public web)

REA's website target returns page structure, scripts, network observations, and requested screenshots using a Chrome-family browser (00 §1). Technically this is one of the cheapest target classes.

**However:** this is the highest *legal* risk of any internal use case. Reverse-engineering a competitor's public site for product insight is only defensible under authorization, contractual right, or narrow statutory exemption — and the boundary (public accessibility ≠ authorization to reverse-engineer) is exactly the kind of question the legal/CLO stream owns. Per that boundary: **this study does not assess legality**; the only actionable statement is that authorization is required before any such run, and site ToS/robots/crawl-policy review is a legal deliverable, not an engineering one.

**Internal rating: Medium value / Low effort / Medium–High legal risk — do not start until legal guidance lands.** If legal later clears a narrow posture (e.g., only vendors we already hold contracts with, under their partnership terms), the technical cost is trivial; the gate is legal, not technical.

## 2. Legacy and third-party system documentation for integrations

Our `integration_engineer` lane (WhatsApp Business API, CRM, payment gateways, NGO data connectors incl. Kobo/DHIS2/Google Sheets flows per `company-registry.yaml`) repeatedly hits opaque third-party clients: legacy Windows installers, closed .NET desktop utilities, mobile APKs used by field partners. Today these get documented by hand — screenshotted, guessed at, re-learned per engagement.

REA-relevant target classes for this work:

| Target | Why it fits | Extra requirements (00 §1) |
|---|---|---|
| .NET assemblies | Metadata, CIL, build comparisons; **static only, never loads the assembly** | none |
| Android APKs | Manifest, decompiled classes, references | headless JADX + full JDK (Windows x64 OK) |
| JavaScript / Electron | Modules, IPC, routes; **no native engine, never executes the app** | none |
| SQLite databases | Tables, indexes, triggers, sample rows | Node ≥24.15 or 26+ native SQLite |
| Native binaries | Pseudocode/strings for old Windows utilities | Ghidra (Windows = **experimental P0, read-only** — 00 §2/§5) |

Caveats: many of our partners' systems are unknown-tech-stack to this study (UNVERIFIED which are .NET vs Access-era vs web wrappers); each engagement needs **written authorization from the system owner** before analysis, and Evidence bundles can reach hundreds of MB (00 §4) — client-confidential artifacts must stay on-operator-disk under the data policy (results still flow to whatever model provider drives the agent — 00 §3, fact 9).

**Internal rating: High value / Medium–High effort / Medium risk (authorization + confidentiality).** Highest strategic value after UC-A because it compresses per-engagement discovery time on Offer B/C integration work — but it is per-client, not a reusable internal asset.

## 3. Own-builds QA and verification

**This is the highest value / lowest risk / lowest effort internal use case**, and the one that exercises the toolchain end-to-end with zero authorization exposure (we own every byte under analysis).

Concrete targets on our own estate:

1. **Published wheel** (`ai-company` 0.6.0): install from PyPI-equivalent artifact or local `uv build` output; verify entry points, subcommand surface (`ai-company --help`), and that the wheel contains what `src/ai_company/` says it contains — unexpected binaries or data files in a shipped wheel are exactly the class of defect a human review misses.
2. **Vite production build** (`dist/` from `npm run build`, deployed via Vercel): REA's JS workflow analyzes directories statically and *never executes the app* (00 §1) — modules, routes, and the third-party dependency graph of our own bundle, without touching production.
3. **Generated agent cards** (~90 files in `.opencode/agents/`): diff-by-inspection against `company-registry.yaml` + template expectations — a structural consistency check our generator tests don't fully cover.
4. **SQLite StateStore** files used by the orchestrator (`data/orchestrator/…`): schema inventory (tables, indexes, triggers) against what the code believes the schema is — drift detection for a file-backed store.
5. **Docker image**: layers and contents vs `Dockerfile` intent — catches accidental secret/file inclusion before it ships.

Why this ranks first: it needs no external party's permission, no legal review, no client data, and on Windows it needs **no Ghidra at all** (JS/SQLite/.NET static targets don't require a native engine — 00 §1, and Windows Ghidra is experimental P0 anyway). It produces a repeatable pre-release checklist that `qa_lead` / `test_engineering_lead` / `release_manager` can own, aligned with our existing red/green baseline gate (ruff + mypy + pytest) rather than replacing it — REA covers *artifact shape*, CI covers *source correctness*.

**Internal rating: High value / Low–Medium effort / Low risk.**

## 4. Security self-assessment

Not duplicated here. The security/CISO stream's file in this same directory owns threat-model depth, dependency/supply-chain posture, and red-team angles (we have a `red_team_engineer` role in AI Research). One engineering-owned note only: bandit + the existing pre-commit/CI security hooks already gate *source*; REA's unique security-relevant capability on our estate would be **shipped-artifact inspection** (wheel/image contents, unexpected network endpoints in our own bundle) — which is the same machinery as UC-A, just pointed at the security checklist. Recommend the security stream fold "own-artifact inspection" into its verdict rather than re-run tool setup.

**Internal rating: Medium–High value (via UC-A reuse) / Medium effort / Medium risk (model-provider egress of any findings) — owned by the security stream.**

## 5. Web analysis of `lightspeedholdings.vercel.app` and third-party JS

We own the deployment; this is authorized by definition. One website-target run against the production URL gives:

- Full page structure and script inventory of what we actually serve (vs what we think we serve).
- **Third-party JS dependency surface**: scripts, CDNs, and network observations — a concrete supply-chain inventory. Our package.json pins React 18.3, Vite 6, Tailwind 4, recharts, lucide-react, Playwright, `@vercel/blob`, nodemailer — but *runtime-loaded* third parties (analytics, fonts, embeds) only show up in a live fetch, not in the manifest.
- Requested screenshots for a regression baseline we don't currently keep.

Effort is low (Chrome-family browser only; no native engine). Risk is low (our own public property). One constraint: run against the deployed URL, not localhost — dev-cold-start and port quirks (AGENTS.md §16) don't apply to Vercel-hosted production, and the analysis target should be the artifact users actually receive.

**Internal rating: High value / Low effort / Low risk.**

## 6. NGO-sector low-bandwidth / offline legacy maintenance (Malawi context)

Malawi and SADC NGO partners frequently run aging offline-first software: Windows utilities, local SQLite/Excel data stores, APK-based data-collection apps (e.g., KoboCollect-class tooling), and thin-documented connectors to DHIS2. REA's static .NET, APK, Electron, and SQLite targets map directly onto this — and *static* analysis never executes the target (00 §1), which matters for untrusted field-collected binaries.

Strategic read: this is **not yet an internal tool** — there is no named client target, no authorization, and no engagement on the books for it in this study (UNVERIFIED demand). It is a *capability thesis* for Offer B/C integration engagements: "we can document your legacy system in days, not weeks." Building it out before the first paying engagement inverts the build order. Recommendation: treat as a **backlog item gated on the first qualified partner engagement**, informed by UC-C lessons.

**Internal rating: Medium–High value (regional differentiation) / High effort / Medium risk (per-client authorization, offline data handling).**

## 7. Workflow integration

### 7.1 Workstation: yes

One pinned install on the CTO/lead-engineering workstation, MCP-registered into OpenCode, approval-gated setup (`npx rea-agents setup` previews config changes and requires approval — 00 §1) — this matches our existing HITL ApprovalGate pattern rather than fighting it. Version pin is mandatory: upstream ships multiple releases per week (6.5.0 on 2026-10-14; breaking-surface migrations documented, e.g. 6.2 — 00 §5). Pin `rea-agents` exactly; upgrades are deliberate, not ambient.

Prerequisite gate: Node 22.19+ / 24.11+ / 26+ (00 §1, fact 2). Our frontend toolchain already sits in the Node 22+ family (`@types/node` ^22), but the exact workstation Node version is **UNVERIFIED until checked at setup time** — first line of the week-1 runbook.

Windows profile: JS/Electron, .NET, SQLite, websites all work without a native engine. Native-binary work stays blocked-on-experimental (Ghidra P0 read-only) until either upstream hardens Windows support or a Linux analysis box is provisioned — do not plan engagements that need deep Windows-native PE work yet.

### 7.2 CI: no — explicitly rejected

We will **not** wire REA into GitHub Actions or the 6 required checks on `main`. Reasons, in priority order:

1. **Evidence volume.** A single analysis can emit hundreds of MB of Evidence (00 §4, fact 6); CI artifact storage and runner egress budgets are not sized for this, and our current pipelines are sized for lint/type/test in minutes, not investigation bundles.
2. **Nondeterminism vs. gates.** Required checks must be deterministic pass/fail. REA output is investigative narrative + structured Evidence whose *quality* depends on model-provider behavior — unsuitable as a merge gate and corrosive to the red/green baseline our `qa_lead` maintains.
3. **Model-provider egress in CI.** REA analysis results flow to the agent's model provider (00 §3, fact 9). Running that in CI introduces third-party egress of *our own pre-release artifacts* plus API-key handling for a non-essential pipeline stage — attack-surface expansion for zero gating benefit.
4. **Upstream cadence tax.** Multiple releases per week + documented breaking migrations (00 §5) would turn CI into a standing patch obligation. A pinned workstation install amortizes that to one human decision.
5. **Not a sandbox** (00 §3, fact 8). Adding a broad-surface local-analysis tool to shared CI runners contradicts our least-privilege posture on the build fleet.

**Fit:** pre-release manual audit by `qa_lead` / `test_engineering_lead` / `release_manager` using the pinned workstation install; results summarized into `reports/` as release evidence. If a later phase wants automation, it is a *scheduled human-triggered* job on an isolated workstation, never a PR-blocking check.

### 7.3 OpenCode MCP wiring

Target agent roles for first access: `lead_backend`, `lead_frontend`, `qa_lead`, `integration_engineer` (UC-A/B/C owners), with `test_engineering_lead` as the Evidence-paging discipline owner. Tool vocabulary constraint: agent cards are generated with the canonical 7 tools; MCP tools surface through OpenCode's MCP layer, not by editing generated cards — no registry churn required for a workstation-local MCP server.

## 8. Verdict and ranked backlog

### Use-case summary table

| ID | Use case | Value | Effort | Risk | Verdict |
|----|----------|-------|--------|------|---------|
| UC-A | Own-builds QA/verification (wheel, dist/, agent cards, SQLite, image) | **High** | Low–Med | Low | **Start here** |
| UC-B | Website + third-party JS inventory of production site | **High** | Low | Low | Week-1 follow-on |
| UC-C | Legacy/third-party system documentation for integrations | **High** | Med–High | Med (authorization) | Gated on client authorization |
| UC-D | NGO-sector low-bandwidth legacy maintenance | Med–High | High | Med | Gated on first qualified engagement |
| UC-E | Competitive intelligence (public web) | Med | Low | **Med–High (legal)** | Blocked pending legal/CLO guidance |
| UC-F | Security self-assessment | Med–High | Med | Med (egress) | Owned by security stream; reuse UC-A machinery |
| UC-G | Workflow integration | enabler | Low | Low | Workstation yes / CI no (§7) |

### Ranked backlog (top 5)

| Rank | Item | Est. effort | Value delivered |
|------|------|-------------|-----------------|
| 1 | **UC-A pilot**: REA against our own `ai-company` wheel + Vite `dist/` + a sample of generated agent cards; document findings and Windows quirks | **8–16 h (~1–2 engineer-days)** | First evidence that the toolchain works on our estate; defect-finding on shipped artifacts; zero external dependency |
| 2 | **UC-B inventory**: one website-target run against `lightspeedholdings.vercel.app` — script/dependency/network report | **4–8 h (~0.5–1 day)** | Concrete third-party JS supply-chain list; production-vs-manifest drift check |
| 3 | **UC-G setup**: verify Node ≥22.19, pin `rea-agents@6.5.0` (or current stable at install date), MCP-register into OpenCode, write 1-page operator runbook incl. Evidence-paging rules and the CI-exclusion rationale | **~8 h (1 day)** | Durable, gated workstation capability; prevents ambient-version drift |
| 4 | **UC-C authorization-gated pilot** (post-legal/engagement): one legacy partner client under written authorization — .NET or APK static documentation | **16–24 h (2–3 days)** once authorized | Template for integration-engagement discovery compression |
| 5 | **UC-D scope study** (research only, no build): NGO-sector offline-legacy demand interviews + target-class fit map | **8–16 h (1–2 days)** | Evidence for whether to productize UC-C into an offer line |

### Start here — week-1 recommendation

**Begin with UC-A (rank 1), day 1.** No permission needed, no legal exposure, no Ghidra, no CI changes. Sequence:

1. Confirm workstation Node ≥22.19 (upgrade path if not).
2. `npx -y rea-agents@<pinned> analyze` against a locally built `ai-company` wheel and the Vite `dist/` directory — static JS and package-structure targets, no native engine.
3. Record Evidence volume, paging behavior, and any Windows-specific failures in a short runbook note (feeds UC-G).
4. Days 2–3: UC-B against the production URL; days 4–5: finish the UC-G pin + runbook so the capability is durable before the team expands access.

Do **not** start with UC-E (blocked on legal) or UC-D (no engagement yet). Do **not** open a CI PR.

---

*End of file. Cross-references: `00-rea-capabilities.md` (shared facts); security stream's file in this directory (UC-F depth); client-offerings stream's file (out of scope here).*
