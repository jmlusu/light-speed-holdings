# Research Brief — Cutting AI Costs With Open Source in Resource-Constrained Africa

**Date:** 2026-10-12 · **Author:** Agentic Research Lead (Pharos) · **Status:** DRAFT for editorial use
**Purpose:** Grounding document for a future CEO-voice article. Every claim below carries provenance: `[repo: path]` (verified this session unless noted) or `[ext: URL, fetched 2026-10-12]`. Numbers not evidenced in the repo are listed as gaps, not asserted.

---

## 1. First-party open-source inventory

The Lightspeed operating stack is built almost entirely on permissive-licensed open source, with two structural honesty notes: (a) **this repository is currently proprietary** — `license = "Proprietary — All Rights Reserved. Apache 2.0 at v1.0."` `[repo: pyproject.toml]` — so the article's open-source argument is about the *foundation* we build on, not our own code (yet); (b) `uv.lock` contains **zero** license fields (verified: 0 matches), so Python dependency licenses are not recorded in-repo; npm licenses are.

| Layer | Components (verified) | License evidence |
|---|---|---|
| Python core `[repo: pyproject.toml]` | Python ≥3.12, Typer CLI, FastAPI, Uvicorn, Jinja2, Pydantic ≥2.8, PyYAML, jsonschema, rich, cryptography ≥42, httpx, apscheduler, beautifulsoup4, python-docx | Per-package licenses not in `uv.lock` (0 license fields) — status: **unrecorded in-repo** |
| ML/data `[repo: pyproject.toml]` | sentence-transformers ≥3.0, numpy, psutil | Same as above |
| Observability `[repo: pyproject.toml]` | OpenTelemetry API/SDK ≥1.25, prometheus-client ≥0.19 | Same as above |
| Dev tooling `[repo: pyproject.toml, .pre-commit-config.yaml]` | ruff v0.16.1, mypy (mirrors-mypy v2.3.0), bandit, safety, pre-commit, hypothesis, pre-commit-hooks v4.6.0 | ruff MIT, mypy MIT, pre-commit MIT (ecosystem-standard; not lockfile-verified) |
| Frontend `[repo: package.json, package-lock.json]` | Vite 6.1, React 18.3, React Router 7.18, Tailwind CSS 4.0, TypeScript 5.7, Vitest 5.0, Playwright, recharts, lucide-react | 292 license fields in `package-lock.json` (verified): react **MIT**, tailwindcss **MIT**, vite **MIT**, vitest **MIT**, typescript **Apache-2.0** |
| LLM runtime OSS `[repo: src/ai_company/llm/providers/]` | `ollama.py` (default `http://localhost:11434`, default model `llama3.1-8b-32k`, lines 18–34), `llamacpp.py`, `openai_compatible.py`, `base.py` | Ollama MIT, llama.cpp MIT (upstream) |
| Containers `[repo: Dockerfile]` | Multi-stage `python:3.12-slim` + uv, non-root `appuser`, EXPOSE 8420, healthcheck | Base images: Docker/Python licenses (upstream) |
| 4-gate quality | Gates: lint (ruff), typecheck (mypy), test (pytest, ubuntu+windows matrix) `[repo: .github/workflows/ci.yml]` + bandit security gate in pre-commit `[repo: AGENTS.md §5]` | bandit Apache-2.0 |

**Stack posture (qualitative):** one Python CLI + one FastAPI dashboard + one Vite/React SPA + Jinja2 generation — no paid SaaS in the runtime path. python-pptx appears only as a dev extra, imported solely by `scripts/build/generate-milestones-deck.py:6-8`; zero pptx imports under `src/`.

## 2. Cost-architecture logic (qualitative — no dollar claims)

Repo evidence supports a *mechanism* argument, not a *savings* argument:

1. **Provider-agnostic routing with local fallback.** `ModelRouter` in `llm/client.py` routes across `openai_compatible`, `ollama`, and `llamacpp` providers; adding or swapping a provider is a config decision, not a code rewrite. Local models carry **$0.00 marginal token cost by accounting convention** — `cost_tracker.py` prices them at zero with the comment "Ollama / local models — effectively free" (~line 64) `[repo: src/ai_company/llm/cost_tracker.py]`. Hedge for publication: this is a *ledger convention*, not measured savings.
2. **Cost controls are code, not policy.** `MODEL_COSTS` table ($/1M-token, sourced to "public pricing pages as of 2025" — dated), daily and per-task budget caps, `TokenBucket` rate limiting, `ResponseCache` (deduplicates repeated calls), `PromptCompressor` (shrinks input tokens), and retry capped at 5 attempts behind a thread-safe `CircuitBreaker` (`llm/circuit_breaker.py`) so retry storms cannot amplify spend `[repo: src/ai_company/llm/]`.
3. **Human approval gates bound blast radius.** Five tiers — `ApprovalTier(IntEnum)`: AUTO_APPROVE=0, NOTIFY=1, SINGLE_APPROVER=2, TWO_PERSON=3, CEO_ONLY=4 `[repo: src/ai_company/orchestrator/tier_rules.py:4-8, 24-34, 202-234]`; gate implementation referenced by the site-claims ledger as `src/ai_company/executor/hitl_gate.py`.
4. **Security/RBAC is first-party.** `security/{rbac,pii_detector,memory_encryption,encryption_key_manager,content_filter,command_safety}.py` `[repo: src/ai_company/security/]`.
5. **Scale context (canonical, ledger-supplied — not re-counted this session):** 90 agents (89 AI + 1 human CEO) across 20 departments `[company-registry.yaml]`; 144 verified agent configurations; 2,373 regression tests as of 2026-09-10 `[results/use-case-fact-pack.md:79]` — caveat: that count mixes 2,211 static `def test_` matches with 25 parametrized cases; SHA-256 audit trails and zero-cloud/offline-first are **design/implementation claims** (hedge: not externally audited; offline stance is soft-evidenced only by the cost-tracker comment).

## 3. External facts (8, all fetched 2026-10-12)

| # | Fact | Source | One-line caveat |
|---|---|---|---|
| 1 | OpenAI released `gpt-oss-120b`/`gpt-oss-20b` under **Apache 2.0** (2025-08-05); 20b natively quantized runs in **16GB** memory, 120b in 80GB | [openai.com/index/introducing-gpt-oss/](https://openai.com/index/introducing-gpt-oss/) | Vendor announcement; hardware figures are vendor-stated |
| 2 | gpt-oss is **not served via the OpenAI API**; runs on vLLM/Ollama/llama.cpp on infrastructure you control | [help.openai.com/en/articles/11870455](https://help.openai.com/en/articles/11870455-openai-open-weight-models-gpt-oss) | Vendor docs; terms change without notice |
| 3 | Cheapest tracked open-weight API: gpt-oss-20b on Groq at **$0.075/$0.30 per 1M tokens** (in/out); gpt-oss-120b $0.15/$0.60; DeepSeek V4 Flash (MIT) $0.30/$1.20 | [llmcostlab.com](https://llmcostlab.com/) article published 2026-09-28, prices re-read 2026-10-02 | Third-party commercial price tracker; per-token prices move weekly |
| 4 | Africa AI market projected **~$6.4B by end-2025**; open source framed as the democratizing, cost-effective pathway for the continent | [Linux Foundation blog, 2025-09-29](https://linuxfoundation.org/blog/) | Advocacy blog; market projection, not audited |
| 5 | Malawi **data-only mobile broadband basket = 8.45% of GNI per capita (2025)** | ITU ICT Price Baskets 2008–2025 via [statorigin.org](https://statorigin.org/stat/stat_81KWB2MBHXWRMD4MRCXJ41K5MW) | Secondary mirror of the ITU dataset; original Excel not re-opened |
| 6 | Malawi: individuals using the internet **28% (2022)**; fixed broadband basket **63.7% of GNI p.c.** | [ITU Malawi ICT profile (ddd_MWI.pdf)](https://www.itu.int/en/ITU-D/Statistics/Documents/DDD/ddd_MWI.pdf) | 2022 vintage — predates recent cheap-bundle rollouts |
| 7 | Malawi: 4GB monthly bundle ≈ **6,000 MWK (~$3.54)** vs min wage 50,000 MWK (~$29), Apr 2024; rural internet 13.5% vs urban 40.7% | [Freedom House, Freedom on the Net 2024 — Malawi](https://freedomhouse.org/index.php/country/malawi/freedom-net/2024) | Advocacy-org report citing ITU/NSO/World Bank; FX conversions approximate |
| 8 | Peer-studyable precedent: **Arapai** offline-first LLM architecture ran all inference locally on CPU-only legacy hardware (1–3s responses; 120 students, 9 instructors under limited connectivity) | [arXiv:2603.03339 (2026)](https://arxiv.gg/abs/2603.03339) | Single education-domain preprint; not peer-reviewed at time of fetch |

## 4. Gap list — numbers we cannot assert

Do **not** publish these without new evidence:

- **$ saved vs. cloud APIs, % cost reduction from local models, cost per workflow in USD** — no measured before/after exists in-repo; `MODEL_COSTS` is a pricing ledger, not billing evidence.
- **Monthly token volume / spend aggregates** — `cost_tracker.py` writes JSONL but no published aggregate was located.
- **Bandwidth-savings percentages; local-inference latency on Malawi hardware** — unmeasured here.
- **"2,373 tests" as a live figure** — dated 2026-09-10 and definition-dependent (see §2).
- **Pricing (MWK 3,500,000 ≈ $2,000 + $200/mo; MVP MWK 150,000 ≈ $85)** — offer language only; not market-validated.
- **SADC readiness / AU strategy framing** — proposal and drafted-submission status only; no filed/approved artifact exists.
- **"Zero-cloud," "offline-first," "SHA-256 audit trails" as operational guarantees** — design stance/implementation claims; soft evidence only. Per AGENTS.md §15.6: where cause or status cannot be established from evidence, say so.
- **No paid client deliveries** — the J&S StopOver Bar engagement `[docs/Pharos/case-study-pipeline.md:7-12]` is a real-SME case pipeline, not a revenue claim.

## 5. Recommended angle and claim-ready sentences

**Angle:** In Malawi the binding constraint is not token prices — it's that connectivity itself costs 8.45% of GNI per capita and rural internet sits at 13.5%. The open-source cost argument is therefore architectural, not arithmetic: *route to local models where the marginal token is free by design, rent open-weight APIs where competition has already capped prices (gpt-oss-20b at $0.075/$0.30), and spend the difference on the constraints that actually bind.* Honesty badge: Lightspeed has mechanisms and inventories, **not yet published savings measurements** — the article argues from architecture and external price evidence, and says so.

**Claim sentences (verbatim, provenance inline):**

1. "Our stack runs on permissive-licensed open source end to end — MIT-licensed React, Vite and Tailwind on the frontend, Apache-2.0 TypeScript, and Ollama plus llama.cpp providers behind a single model router — while our own codebase remains proprietary today, with Apache 2.0 targeted at v1.0. `[repo: package-lock.json; pyproject.toml; src/ai_company/llm/providers/]`"
2. "Local inference is priced at zero in our cost ledger by convention — a deliberate architecture choice, not a measured saving — because models served through Ollama or llama.cpp carry no per-token charge. `[repo: src/ai_company/llm/cost_tracker.py ~line 64]`"
3. "Since OpenAI put gpt-oss-20b under Apache 2.0 in August 2025, hosted versions trade at $0.075 per million input tokens on Groq — a price set by open weights and host competition, not by a vendor's list price. `[ext: openai.com/index/introducing-gpt-oss/, 2025-08-05; llmcostlab.com, fetched 2026-10-12 — tracker figure, moves]`"
4. "In Malawi a 4GB mobile bundle costs about 6,000 kwacha — roughly 12% of the minimum monthly wage — and ITU puts the data-only basket at 8.45% of GNI per capita, which is why every megabyte our agents don't send over the network is a real cost, not an optimization. `[ext: freedomhouse.org Malawi FTN 2024; ITU ICT Price Baskets 2025 via statorigin.org, fetched 2026-10-12]`"
5. "Researchers have already shown offline-first LLM inference holding 1–3 second response times on legacy CPU-only hardware with no cloud dependency — the pattern Lightspeed's provider-agnostic routing is built to exploit. `[ext: arXiv:2603.03339, fetched 2026-10-12 — preprint caveat]`"

**Before publication:** re-verify Fact 3 prices (weekly volatility), refresh or drop the 2022 ITU figures, and keep the §4 gap list out of any headline claim.
