# Creative Production Architecture

**Status:** Phase 2 of the Creative Engine Consolidation — implemented and tested.
**Code:** `src/ai_company/creative/` · **Tests:** `tests/unit/test_creative_pipeline.py` (32 tests, 97% coverage)

This document defines the consolidated creative production architecture: the
structured creative brief, the execution manifest, the Creative Director as
orchestration entry point, model routing through the existing router, and the
replaceable tool adapters. It reuses existing infrastructure — no duplicate
apps, orchestrators, or routing systems were built.

---

## 1. Architecture overview

```
                        ┌──────────────────────────────┐
   creative brief ─────►│  Creative Director (entry)   │  agent: creative-director
   (5-question intake)  │  ai_company.creative         │  skill: ls-creative-director
                        └──────────────┬───────────────┘
                                       │ route_brief()
              ┌────────────────────────┼─────────────────────────┐
              ▼                        ▼                         ▼
   ┌──────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
   │ Skill chain      │   │ ModelRouter.resolve()│   │ Knowledge checks     │
   │ ls-design-system │   │ (existing router)    │   │ source_research      │
   │ + production     │   │ provider/model/tier  │   │ links to research/   │
   │ + ls-artifact-qa │   └──────────────────────┘   │ and knowledge/       │
   └──────────────────┘                              └──────────────────────┘
                                       │
                              ExecutionManifest (routed)
                                       │ run_production()
                        ┌──────────────▼───────────────┐
                        │ AdapterRegistry.select()     │
                        │ presentation │ opendesign │   │
                        │ comfyui (probed, not wired)  │
                        └──────────────┬───────────────┘
                                       │ produce() → output/creative/<run_id>/
                        ┌──────────────▼───────────────┐
                        │ QA gate (default_qa / plug)  │  verdict: pass | fail
                        └──────────────┬───────────────┘
                                       │ pass only
                        ┌──────────────▼───────────────┐
                        │ Human approval gate          │  approver = Human CEO
                        │ QA pass is NOT approval      │
                        └──────────────┬───────────────┘
                                       ▼
                     manifest.json persisted per run (approved/rejected/failed)
```

## 2. Components

| Component | File | Responsibility |
|---|---|---|
| Brief + manifest contracts | `creative/models.py` | `CreativeBrief`, `ExecutionManifest`, lifecycle enums |
| Routing | `creative/routing.py` | Skill chain, specialist assignment, `ModelRouter` integration, knowledge warnings |
| Tool adapters | `creative/adapters.py` | Replaceable backends behind one interface; local availability probes |
| Pipeline | `creative/pipeline.py` | Route → produce → QA → approval stage machine; failure/rerun handling |
| Persistence | `creative/store.py` | One run directory per manifest: `output/creative/<run_id>/manifest.json` |

### Existing infrastructure reused (not rebuilt)

| Existing system | How it is used |
|---|---|
| `ai_company.model_router.ModelRouter` | Sole model routing system. `resolve(agent_name=specialist, agent_type="Specialist", priority, task_prompt)` returns provider/model/tier/reason; per-agent overrides and budget degradation apply unchanged. |
| `company/agent-registry.json` | Agent-name validation for specialists; source of per-agent model overrides. |
| `ai_company.presentation.pipeline` | The wired deck renderer (Marp + PptxGenJS JSON, brand tokens enforced). |
| `ls-*` skill system | The routing table names the real skills (`ls-design-system`, production skill, `ls-artifact-qa`) that agents load at run time. |
| Executor `HITLGate` | Standard human-approval requester when runs execute under the daemon (Phase 3 wiring). |
| Registry (`company-registry.yaml`) | Creative Director and all specialists already registered; **no registry changes were made** (registry baseline gate preserved). |

## 3. The creative brief

`CreativeBrief` mirrors the `ls-creative-director` intake contract. Required
fields enforce the five questions; the rest have honest defaults.

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Short label for the deliverable |
| `artifact_type` | yes | `website \| deck \| whitepaper \| campaign \| ad \| diagram \| infographic \| docs` |
| `audience` | yes | Who consumes it, what they care about |
| `objective` | yes | The behaviour change the artifact must cause |
| `core_thesis` | yes | The core message, 1–2 sentences |
| `narrative_arc` | no | Hook → proof → evidence → close |
| `visual_language` / `brand_base` | no | Default: LightSpeed design system (never invent colors/fonts) |
| `structure`, `channels`, `cta` | no | Handoff detail for production skills |
| `qa_scope` | no | Defaults to visual/brand/ux/content/accessibility |
| `source_research` | no | Repo-relative research paths (knowledge workflow link, §6) |
| `format_hint` | no | e.g. `deck_type`: `investor_pitch \| board_meeting \| keynote \| training` |

## 4. The execution manifest

`ExecutionManifest` is created at intake and **persisted after every stage
transition**, so interrupted, failed, and approved runs are all inspectable.

| Field | Meaning |
|---|---|
| `run_id`, `created_at`, `updated_at` | `cr-<UTC stamp>-<rand>` identity |
| `status` | `created → routed → producing → qa → awaiting_approval → approved \| rejected`, or `failed` |
| `brief` | Full brief snapshot |
| `chain` | Skill chain: `brand_base` + one `primary` + `support[]` + `qa_gate` |
| `agents` | `director=creative-director`, `specialist`, `specialist_known` |
| `route` | Provider/model/tier/reason from `ModelRouter.resolve()` |
| `adapters[]` | Availability snapshot of every registered backend (evidence of limitations) |
| `outputs[]` | Files written under the run directory |
| `qa` | Verdict + per-check results + notes |
| `approval` | Status, who decided, when, `qa_passed` (kept separate from approval) |
| `warnings[]` | Knowledge/registry/parking warnings |
| `errors[]` | Production failures (adapter exceptions, missing adapter) |
| `retry_of` | Links a rerun back to the failed run it replaces |

Lifecycle rules enforced in code:

1. Production never starts without a routed manifest.
2. QA runs on every produced artifact; **QA failure stops the run** — the
   approval gate is never offered (`approval.status` stays `pending`).
3. Approval only happens after QA passes, and is recorded separately
   (`qa_passed: true` ≠ `status: approved`). The approver callable represents
   the Human CEO; without an approver the run parks at `awaiting_approval`.
4. Any adapter exception or missing adapter marks the run `failed` with the
   error recorded; a rerun creates a **new** run with `retry_of` set.

## 5. Routing table (Creative Director → specialist)

Mirrors the `ls-creative-director` routing table; specialists are validated
against `company/agent-registry.json` (a test enforces this against the real
registry).

| Brief says | Primary skill | Support | Specialist |
|---|---|---|---|
| Website / landing / web app | `ls-frontend-design` | `ls-diagramming`, `ls-visual-storytelling` | `lead-frontend` |
| Deck / keynote / pitch / board | `ls-presentation-design` | `ls-diagramming`, `ls-visual-storytelling` | `product-marketing-manager` |
| Whitepaper / report / proposal | `ls-document-design` | `ls-diagramming`, `ls-visual-storytelling` | `thought-leadership-author` |
| Campaign (LinkedIn/X/IG/FB) | `ls-social-media-design` | `ls-visual-storytelling`, `ls-brand-advertising` | `social-media-manager` |
| Ads / banners / posters | `ls-brand-advertising` | `ls-social-media-design` | `content-creator` |
| Architecture / process diagram | `ls-diagramming` | — | `technical-documentation-lead` |
| Infographic / data story | `ls-visual-storytelling` | `ls-diagramming` | `content-creator` |
| Docs / knowledge base | `ls-documentation-engineering` | — | `technical-documentation-lead` |

Every chain loads `ls-design-system` first and gates on `ls-artifact-qa` last.

## 6. Knowledge workflow connection

Content-heavy artifact types (`whitepaper`, `campaign`, `docs`, `infographic`)
are checked at routing time:

- No `source_research` linked → manifest warning: research from `research/`
  or `knowledge/` must be attached before production; production skills must
  not invent facts.
- A linked path that does not exist → warning naming the missing path.
- Existing linked paths → accepted silently.

Light artifacts (`deck`, `ad`, `diagram`, `website`) do not force research
links; the warning is advisory, never a silent drop.

## 7. Model routing integration

`route_brief()` resolves the route through the **existing** `ModelRouter` only:

- `agent_name=<specialist>` → honors per-agent overrides from
  `company/agent-registry.json`.
- `agent_type="Specialist"` + priority → tier rules in `company/models.yaml`
  (medium → `standard`, high → `premium`).
- `task_prompt` → domain-aware and task-type detection unchanged.
- Resolution is offline-safe: `resolve()` reads config only; no network.

A routing failure becomes a manifest warning (`model route unresolved: …`),
never an exception — the run remains inspectable and retryable.

## 8. Tool adapters

Interface: `supports(artifact)` + `availability()` (local probe) + `wired`
(can this pipeline produce today) + `produce(brief, out_dir)`.

| Adapter | Supports | Probe | Wired | MVP position |
|---|---|---|---|---|
| `presentation` | `deck` | none needed (pure Python) | **yes** | The MVP production backend: Marp `.md` + PptxGenJS `.json`, brand tokens `#070A40 / #DC3641 / #00BFFF` enforced |
| `opendesign` | website, deck, whitepaper, ad, diagram, infographic | `shutil.which("od")` | no | Optional. If operational, production is delegated to `ls-od-*` agent skills; if not, artifacts fall through to the specialist agent. Never an MVP dependency. |
| `comfyui` | infographic, ad, website | loopback TCP `127.0.0.1:8188` (0.4 s timeout, no external traffic) | no | Optional. Media generation runs through the media-generation owner agent. Never an MVP dependency. |

Selection: first registered adapter that supports the artifact, probes
available, **and** is wired. If none qualifies, the run fails with an
availability record (every adapter's status is on the manifest either way).
A broken probe is recorded as `probe failed: …` — it never kills the run.

Constraints honored: no paid APIs, no new credentials, no third-party data
transmission; probes are local only.

## 9. QA and human approval

Two gates, recorded separately:

1. **QA gate** (`default_qa`, pluggable per run):
   - `outputs_exist` — every recorded output exists and is non-empty
   - `no_legacy_red` — no readable output carries the legacy `#E63946`
   - `brand_tokens` — canonical `#DC3641` detected (`skipped` + note for
     palette-free artifacts)
   This is the deterministic offline floor. Deeper visual/UX/accessibility
   review is the `ls-artifact-qa` gate run by the specialist agent (Phase 3
   executor wiring).
2. **Human approval gate** — the approver callable represents the Human CEO.
   Policy encoded in `run_production()`:
   - QA fail → gate never offered.
   - QA pass + no approver → parked at `awaiting_approval` with a warning.
   - Approver decision → `approved` or `rejected`, with who/when/note.

When runs execute under the executor daemon (Phase 3), the approval request
goes through the existing `HITLGate` so the dashboard approval flow applies
unchanged; the manifest remains the record of the decision.

## 10. Persistence and reruns

```
output/creative/
└── cr-20261112-101530-ab12cd/
    ├── manifest.json          # full ExecutionManifest
    ├── deck_board_meeting_….md
    └── deck_board_meeting_….json
```

- `save_manifest` / `load_manifest` / `list_runs` in `creative/store.py`.
- Failure and its rerun both persist: rerun with `retry_of=<failed run_id>`.
- The manifest is the audit artifact for acceptance evidence (run trace, QA
  evidence, approval record, failure/rerun demo).

## 11. Current limitations (honest scope)

- **Wired production backend: decks only.** Website/whitepaper/campaign/etc.
  routing, QA and approval are implemented, but their production path is the
  specialist agent (LLM) — exercised in Phase 3's vertical slice, not in the
  offline pipeline.
- **OpenDesign/ComfyUI are probed, not wired** — if present, delegation happens
  at agent level, not inside `run_production()`.
- **Deep artifact QA** (contrast, overflow, alt text, heading order) remains the
  `ls-artifact-qa` skill executed by agents; `default_qa` is the offline floor.
- **HITLGate/CLI wiring** for interactive approval lands in Phase 3.

## 12. Phase 3 (next)

1. Run the MVP vertical slice: brief → interpretation → specialist routing →
   brand context → production → QA → human approval → saved output + manifest.
2. Demonstrate failure handling and rerun with both manifests retained.
3. Produce the workflow execution trace and architecture diagram deliverables.
4. Wire approval through `HITLGate` and add the `creative` CLI surface.
