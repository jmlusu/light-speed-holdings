# Research: Implementing Google's WikiSkill Framework at Lightspeed Holdings

Review report compiled 2026-09-13 by a 5-subagent team (see §8 Methodology). Scope:
overview, capabilities, and pros/cons of implementing the **WikiSkill** framework
(Google Research, Tang et al., arXiv:2608.27454, Aug 2026) on the Lightspeed AI
Company Builder runtime.

## Verdict (one line)

**Adopt the wiki layer and loop mechanics in a scoped 90-day pilot on deterministic
k-dense-* skills, with HITL-gated, versioned, eval-gated skill edits — do NOT run
unrestricted autonomous skill evolution.** The current architecture makes trace capture,
daemon cadence, and LLM routing nearly free; the blockers are a missing skill-benchmark
corpus for gating, skills-as-reviewed-code conventions, and governance/privacy exposure
from persistent execution traces.

---

## 1. Overview of the WikiSkill Framework

WikiSkill co-evolves agent skills with a persistent, compounding knowledge base ("wiki"),
inspired by Karpathy's LLM Wiki. Its thesis: prior skill-evolution methods (EvoSkill,
Trace2Skill, SkillOpt) scatter insights across proposal histories; WikiSkill adds a durable
structured knowledge layer between raw experience and executable procedures.

**Three layers:**

| Layer | Role | Lifecycle |
|-------|------|-----------|
| `raw/` | Immutable execution traces (reasoning, tool calls, outputs, final answers) | Never modified |
| `wiki/` | Persistent knowledge: `patterns/` (root-cause analsis + workarounds per failure/success pattern), `logs.md` (iteration history), `skill-impact.md` (per-proposal audit: diff, validation score, Accepted/Rejected) | **Never rolled back**; monotonic |
| `skills/` | Executable skills: `SKILL.md` (frontmatter + instructions) + `PURPOSE.md` (maps skill back to motivating wiki patterns + evolution history) | Gated; rolled back on rejection |

**Four-component loop (Algorithm 1):**
1. **Inference Agent** — rolls out training tasks with active skills injected into its
   system prompt (no wiki access during training; the paper's ablation shows wiki access
   there *hurts* because traces become less diagnostic).
2. **Wiki Maintainer** — samples ≤8 traces/iteration (≤5 failures, ≤3 successes), performs
   root-cause analysis, patches pattern pages + index + logs.
3. **Skill Proposer** — multi-turn ReAct agent (~10–20 turns) that reads wiki index +
   skill-impact history + traces, emits **one atomic proposal** (create / patch / no-op).
4. **Gating & Rollback** — accepts a candidate only if validation score **strictly beats**
   the running best; on rejection the skills roll back but the wiki retains the rejected
   diff (asymmetric rollback) so failed interventions are not re-proposed.

**Relation to prior work:** EvoSkill (bounded frontier + flat feedback history),
Trace2Skill (per-trajectory analyst calls + hierarchical merging), SkillOpt (six-stage
pipeline on a single monolithic skill), and SkillWiki (Huang et al., a broader versioned/
provenance-aware skill *infrastructure* vision, 99/125 artifact-conversion feasibility).
WikiSkill is the concrete, evaluated trace→wiki→skill loop; it also claims ~O(1) optimizer
API calls per iteration vs O(N_train/B) for EvoSkill/SkillOpt.

## 2. Capabilities (measured results)

**Benchmarks** — 5 models × 5 tasks (LiveMath, SealQA web search, SpreadSheet, OfficeQA
long-context, ALFWorld embodied); train/val/test splits. Headline average (no-skill → WikiSkill):
- Gemini-3.5-Flash **49.5% → 68.1%**; Qwen-3.6-27B **39.4% → 63.3%**; Gemma-4-31B 41.3% → 54.9%;
  Qwen-3.5-9B 29.9% → 47.4%; Qwen-3.5-4B 26.2% → 38.5%.
- Flagship per-task: LiveMath 33.0 → 72.6 and SpreadSheet 50.5 → 76.6 (Gemini-3.5-Flash);
  Qwen-3.6-27B SpreadSheet 40.8 → 81.7; ALFWorld 52.8 → 77.6.
- Beat the best competing method by **3.3–12.0 points per model**; gains scaled with model size
  (+12.3/+17.5/+23.9 pts at 4B/9B/27B).

**Two findings most relevant to Lightspeed:**
- *Skills substitute for scale/cost:* Qwen-3.5-9B + skills (47.4%) beat Qwen-3.6-27B without
  (39.4%). Smaller, cheaper models can match larger ones when evolved skills are loaded.
  (Gemini-3.5-Flash, Lightspeed's fast-tier fallback in `company/models.yaml`, is a paper model.)
- *Cross-model transfer exists but is not guaranteed:* transferred skills often beat
  self-evolved ones (Qwen-27B skills lift Qwen-9B ALFWorld to 70.2% vs 63.4% self), but
  **negative transfer exists** — Qwen-4B SpreadSheet skills drop Gemini-3.5-Flash from 50.5%
  to 18.1%. Transferability must be verified per model/task, not assumed.

**Ablations:** persistent wiki accumulation is critical (+15.0 avg when the Maintainer/
Proposer can read it); giving the Inference Agent wiki access during training hurts (63.7 →
60.9). Early stop at validation = 1.0 (e.g., Gemini ALFWorld flatline is early-stop, not failure).

## 3. Fit: Wiki Layer vs Lightspeed Knowledge Infrastructure

**Already overlapping stores:** MemoryEngine (`src/ai_company/memory/engine.py`, 6 types;
`consolidate_all()` digests episodic→semantic/procedural ≈ wiki pattern pages;
ADR-019 governs pin/supersede/staleness). Auto-evolve harness (`harness/evolution/`)
already mines archives for Repeated Failures / Verification Gaps / User Corrections /
Reusable Constraints and scores proposals (≥80 accept) — a pattern-distillation loop that
evolves ECL rules, not skills. PostmortemStore + audit trail + ADRs hold root-cause and
decision rationale.

**Genuine gaps WikiSkill would fill:**
- No indexed pattern catalog — `memory/procedural.json` is empty (3 bytes); auto-capture
  produces thin heuristics, not reusable how-to knowledge.
- No skill-impact tracking — nothing links knowledge to the skill that used it.
- No compound trace→pattern→skill pipeline; postmortem lessons and auto-evolve constraints
  are captured but never fed back into skills (PHASE-5 plan item 5 still planned).

**Risk:** a 6th knowledge store worsens retrieval ambiguity across memory + graph +
harness + ADRs + postmortems. **Recommendation: evolve, don't adopt a new store.**
Add a `pattern` layer to the MemoryEngine fed by postmortem lessons, auto-evolve
constraints, and error-recovery traces, plus a skill-impact index; reuse ADR-019 governance
instead of a parallel never-reset wiki.

## 4. Fit: Skill Evolution vs Lightspeed Skills Ecosystem

**Current state:** 99 skill dirs under `.agents/skills/` + 2 in `.opencode/skills/` —
k-dense-* deterministic wrappers (22), ls-* creative stack (11, requiring human art
direction + `ls-artifact-qa` gatekeeper), pharos-* (8), ponytail-* (6), process disciplines,
meta-skills. Governance is **namespace-based and manual**: skill name ≠ `task` `subagent_type`
(dispatch guardrails), `description` is the routing contract, `skill-check` is a read-only
validator, authoring is 100% manual ("treat skills as code; tag, branch, review").
PURPOSE.md has no repo analogue — provenance lives in frontmatter + git history.

**Assessment:**
- *Complementary in theory, conflicting in practice.* The proposer loop adds the layer the
  repo gestures at, but **auto-editing bypasses skills-as-reviewed-code and the
  description-routing contract** that skill-check and `subagents-vs-skills.md` protect.
- *Best candidates:* k-dense-* wrappers (deterministic, script-backed, measurable outputs —
  a Maintainer can extract endpoint quirks without brand judgment).
- *Worst candidates:* ls-* creative stack (human art direction; brand tokens are human-owned),
  pharos-* (voice/brand authority), meta-skills (self-modifying governance).
- *Eval gating infeasible today:* no `harness/eval/` directory, no per-skill benchmark split;
  the org evaluates model quality (2223 tests validate *code*, not agent behavior). Building
  the validation split is the heavy prerequisite.

## 5. Engineering Feasibility

### Cheap to reuse (Phase 1)
- **Raw trace layer ≈ free:** audit writer is append-only, hash-chained JSONL (`audit/`);
  `Executor` writes `results/{task_id}/loop_result.json`; CostTracker records per-iteration
  token/cost. That is WikiSkill's immutable `raw/`, already bounded (4096-char payload caps).
- **Daemon cadence slots in:** `ExecutorDaemon` runs KPI + governance + expiry schedulers;
  a maintain/propose/gate cadence is another `run_due()` call.
- **Outer-loop harness precedent exists:** `executor/ab_testing.py` records ExperimentMetrics
  per randomized variant — near-identical to skill-impact-after-gating.
- **LLM routing:** model router already provides tiers/failover/circuit breakers; Gemini-3.5-Flash
  is the configured fast-tier fallback, and unlike the paper, this org tracks cost.

### Expensive to build (Phase 2)
- **Skill benchmark corpus (the blocker, effort L):** needs held-out task sets + scoring
  rubrics per skill domain for strict gating.
- **Patch-safe skills:** `.opencode/agents/*.md` (288 files) are template-generated and
  drift-checked in CI; `.agents/skills/` are hand-authored markdown with no automated
  patching path.
- **Long-task limit:** `AgentLoop` hard-caps at 10 iterations; wiki consolidation of
  long traces is untested (a paper limitation too).

### Build vs reuse (t-shirt)

| Component | Status | Effort |
|---|---|---|
| Raw trace capture | Reuse audit + loop artifacts + CostTracker | S (augment) |
| Wiki schema/patterns | Build (`wiki/{patterns,logs.md,skill-impact.md}`) | M |
| Wiki Maintainer agent | Build (reuse AgentLoop/MessageBus) | M |
| Skill Proposer agent | Build | M |
| Gating harness + benchmark split | **Build** (new corpus; reuse pytest/ECL gate concepts) | **L** |
| Skill-impact tracker | Build (extend `ab_testing` + CostTracker) | S |
| Wiki retention/bloat control | Build (mirror `ConsolidationScheduler`) | S |
| MessageBus Inference phase | Reuse (add task metadata) | S |
| LLM routing for skill-scoped models | Reuse (extend `models.yaml`) | S |

## 6. Governance, Privacy & Security Implications

- **Data-protection exposure:** WikiSkill's `raw/` persists every prompt, tool call and
  output — exactly the client/confidential data Lightspeed promises never to retain or
  train on (client-facing catalog: "no client data used to train models"; sovereign
  in-country processing). For Malawi DPA 2024 (MACRA-enforced) and GDPR-linked work these
  are **personal-data processing**, and immutable/never-compacted retention defeats
  data minimization and deletion rights. Raw layer must be classified `RESTRICTED`, excluded
  from client workloads, scrubbed/pseudonymized before distillation, and pass the documented
  G1–G4 cross-border gates.
- **Retention conflict:** the org's pattern is bounded retention (audit 180d, memory 730d,
  approval/suspend 30d, ADR-019 TTL/staleness/supersede). A never-reset monotonic wiki is
  the inverse. Register `raw/`/`wiki/` as governed stores with retention + anonymize
  actions; port ADR-019 newest-wins/pinned-curator as the compaction analogue the paper lacks.
- **Skill supply-chain / prompt-injection:** auto-edited SKILL.md is a *prompt-injection
  vector injected into every future run at scale* — it bypasses the effective-agent-skills
  §11 audit checklist. Required: versioned, diff-reviewed, sandbox-tested edits; proposals
  validated against the canonical 7-tool vocabulary; injection-pattern filters; provenance
  from skill text back to trace IDs; no auto-derived `bash`/`webfetch` instructions without
  escalation.
- **HITL gating under the 5-tier matrix:** writing a SKILL.md = code/config change → **Tier 2
  (single approver) minimum**; skills touching security/legal/compliance or containing
  command execution → Tier 3–4. The Skill Proposer itself is a registry change needing CTO
  sign-off; its edits must route through ApprovalGate (30-day retention + expiry sweep).
- **Auditability:** every wiki write and skill edit must emit append-only `AuditEvent`s
  (new `SKILL_EDITED` type; provenance = proposer, trace IDs, content hashes); rejected
  proposals stay searchable; skills git-versioned.

## 7. Summary: Pros, Cons, Recommendation

### Pros
1. **Proven gains:** consistent 3–24 pt accuracy lifts across 5 models/benchmarks; strict
   gating protects against regression.
2. **Skills substitute for scale** → real cost-containment lever for a cost-tracked org
   (demote premium tasks to the fast tier); Gemini-3.5-Flash is a paper-tested model.
3. **Compounding institutional knowledge:** fills the empty procedural/pattern store and
   ties knowledge to skill impact — survives agent turnover; complements the existing
   auto-evolve + postmortem loops.
4. **Low marginal cost of Phase 1:** trace capture, daemon cadence, skill-impact tracker,
   retention control all reuse existing audit/dashboard/external-loop primitives.
5. **Aligned with existing infrastructure:** MemoryEngine (wiki analog), ab_testing
   (outer-loop harness), ApprovalGate (gating), ECL (governance cadence).

### Cons
1. **No skill-benchmark corpus exists** — strict validation gating cannot run today;
   building it is the dominant cost (skilled eval engineer, per-skill rubrics).
2. **Auto-editing conflicts with skills-as-reviewed-code + the description-routing
   contract**; an agent silently patching a `description` breaks discovery and the
   subagent-vs-skill namespace guardrail.
3. **Persistent traces violate data-minimization** and Lightspeed's no-retention promises;
   a never-reset wiki inverts the org's bounded-retention governance. Malawi DPA 2024 /
   GDPR deletion rights require scrubbing + compaction → which weakens the core "wiki
   never resets" premise.
4. **Prompt-injection / supply-chain surface** scales with autonomous skill editing.
5. **Known paper gaps:** skill retrieval untested at library scale, strict-gating rejects
   neutral-but-better updates, unbounded wiki bloat, long tasks untested, no injected
   `bash`/`webfetch`-safety, and **negative cross-model transfer** (a skill that helps one
   model can hurt another).
6. **Skills are not currently patch-safe** (template-generated agent cards are CI-drift-gated).

### Recommendation (phased)
- **Pilot (0–90 days), scoped:** one deterministic domain (2–3 k-dense-* wrappers), a
  hand-curated ~30-task benchmark with binary scoring, `ab_testing` as the outer-loop
  harness, governance cadence for maintain/propose/gate. Confine to **internal, non-client
  workloads**.
- **Mandatory guardrails:** raw-layer scrub + `RESTRICTED` classification; Tier-2+ HITL-gated,
  versioned skill edits routed through ApprovalGate; retention/supersession mechanism before
  any client (NGO/WhatsApp/egov) data enters the wiki; `SKILL_EDITED` audit events; skill
  proposals validated against the canonical 7-tool vocabulary.
- **Grow the wiki need not = grow the skill set:** prefer a MemoryEngine `pattern` layer +
  skill-impact index over a parallel never-reset wiki store; reuse ADR-019 governance.
- **Defer/avoid:** full autonomous evolution of ls-*, pharos-*, meta-skills and skills that
  carry `bash`/`webfetch` instructions, until an eval harness + injection-scan gates +
  compaction exist. If no compaction mechanism can be guaranteed, reject rather than adopt.

## 8. Methodology & Sources

Produced by 5 parallel subagents via the `task` tool, each returning a review section:
`agentic-research-lead` (overview/capabilities), `knowledge-manager` (knowledge-infrastructure
fit), `learning-development-lead` (skills-ecosystem fit), `vp-engineering` (engineering
feasibility with file-path and t-shirt estimates), `data-privacy-officer` (governance/privacy/
security). Synthesized as one report; no code changed — **decision/investigation only**.
An ECL change would be required before implementation (spans >2 files; touches architecture).

Sources: arXiv:2608.27454 (primary) ·
the-decoder.com/google-gives-ai-agents-their-own-wiki-so-they-can-learn-from-mistakes-and-successes ·
reworked.co/knowledge-findability/google-researchers-give-ai-agents-a-wiki-so-they-stop-repeating-mistakes ·
emergentmind.com/topics/wikiskill ·
huggingface.co/papers/2608.27454 ·
repo: AGENTS.md, docs/STATUS.md, docs/ECL.md, docs/adr/019-memory-knowledge-governance.md,
src/ai_company/{memory,audit,executor,llm}/**, harness/evolution/, .agents/skills/.
