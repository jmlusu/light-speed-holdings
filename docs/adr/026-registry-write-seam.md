# ADR-026: Registry Write Seam — All Registry Mutation Through One Front Door

**Status:** Accepted
**Date:** 2026-10-13
**Deciders:** CEO (Human), Platform Engineering
**Technical Domain:** Agent Registry

## Context

`company-registry.yaml` is the single source of truth for every agent in the
company (roles, permissions, reporting lines). Everything else is derived:

- `.opencode/agents/*.md` — generated agent cards (via `AgentGenerator`).
- `company/agent-registry.json` — runtime projection consumed by the executor,
  model router, dashboard KPIs, mobile API, and CLI (via `registry/sync.py`).

Three violations let the derived copies drift away from the master:

1. **The dashboard wrote JSON directly.**
   `PATCH /agents/{name}/reports-to` (`dashboard/api.py`) loaded
   `company/agent-registry.json`, mutated a `reportsTo` field in Python, and
   saved it back. The next `sync_registry()` call silently reverted the change.

2. **The "regenerate" step was a no-op.** After the JSON write, the endpoint
   called `AgentGenerator().generate_all()`, which reads the **YAML** — the file
   it had just not touched. The runtime saw the new JSON; the generated `.md`
   cards still reflected the stale YAML. Split-brain.

3. **Detection was name-set only.** `verify_sync()` compared agent name sets
   between YAML and JSON. A mismatched `reportsTo`, `department`, or `tools`
   list went unnoticed. CI's `generated-check` job only diffed `.md` files;
   `repo-audit.yml` read both registries but never cross-compared them. Nothing
   failed the build when YAML and JSON disagreed.

The only sanctioned mutation pattern already in the codebase was onboarding
(`hr/onboarding.py`): backup YAML → mutate → `generate_all()` → `sync_registry()`
→ rollback on failure. But it was not shared, and the dashboard had no path to
use it.

## Decision

### 1. One write module: `registry/writer.py`

Every mutation to `company-registry.yaml` goes through a semantic function in
the new `registry/writer.py`. The first function is:

```
set_reports_to(agent_ref, manager_ref) -> dict
```

- Accepts hyphenated (dashboard JSON) or underscored (YAML id) references.
- Validates before touching disk: agent exists, manager exists (or virtual
  root `board`/`__root__`), no self-assign, no reporting-line cycle.
- Pipeline: fresh YAML load → backup → mutate + `yaml.dump(sort_keys=False)` →
  `AgentGenerator().generate_all()` → `sync_registry()`.
- On any failure after the backup, restores the YAML backup and re-raises.

The interface is the test surface. New semantic functions
(`set_department`, `add_agent`, …) are added here as the dashboard needs them —
not as raw "dump this dict" helpers.

### 2. Deep `verify_sync()`

`registry/sync.py::verify_sync()` now does a field-by-field compare when the
name sets match: every JSON agent must equal `_agent_yaml_to_json()` output for
its YAML source. Drift like a directly-edited `reportsTo` now surfaces as a
named, field-level error.

### 3. CI gate

The `generated-check` job in `.github/workflows/ci.yml` runs `verify_sync()`
and fails the build with `::error::` annotations when YAML and JSON disagree.
(Side effect: the long-standing "ci.yml never validates agent registry" warning
in `repo-audit.yml` now resolves to `ok`.)

### 4. Dashboard PATCH routed through the seam

The `PATCH /agents/{name}/reports-to` endpoint keeps its RBAC dependency and
input validation, then delegates to `set_reports_to()`. The direct JSON
load/mutate/save block and the no-op `generate_all()` call are deleted.

### 5. YAML dump strategy

Full `yaml.dump(..., sort_keys=False, allow_unicode=True)` — same as onboarding
already does. The registry has no comments; its YAML anchors (`&id001` at the
`tools` lists) expand into equivalent plain data on dump. Functionally
identical output; authoring-order keys preserved.

## Consequences

- **Positive:** one source of truth with one write path; the dashboard,
  generated cards, and runtime JSON cannot diverge after a write; CI fails
  loudly on any future bypass; a regression test asserts the regenerated `.md`
  reflects write-API changes (the split-brain bug cannot silently return).
- **Negative / risk:** onboarding still has its own inline registry-mutation
  flow (`hr/onboarding.py:449-493`) rather than routing through `writer.py`.
  This is deferred as tech debt — the flows are correct today, just duplicated.
  YAML formatting changes (anchor expansion) the first time a write happens;
  this shows up as a one-time diff, functionally a no-op.
- **Neutral:** virtual root `board` is preserved as the stored manager value;
  `__root__` is accepted as an alias. PATCH request/response shapes are
  unchanged; only the write path underneath moved.

## Links

- ADR-002 / ADR-003 / ADR-005: registry and message-bus persistence background.
- ADR-017: ApprovalGate invariant dashboard bypass — **related but separate**;
  this ADR does not address the approval-gate inline reimplementation.
- Source of truth declaration: `registry/sync.py` module docstring,
  `registry/loader.py`, `generator.py`, `cli/main.py:306`.
- Evidence: `tests/unit/test_registry_writer.py` (13 tests),
  `tests/unit/test_registry.py::TestRegistrySync` (read-only guardrails).
- Onboarding pattern this mirrors: `hr/onboarding.py:449-493`.
