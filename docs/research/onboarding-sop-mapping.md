# Research: Onboarding stack vs. SOP-HR-001 mapping

Mapping `docs/sop-hr-onboarding.md` (8-step? actually §5 has 7 steps) onto the
current implementation, plus a gap list (wayfinder ticket #24).

## Step → implementation map

| SOP Step | Current implementation | Files | Gap |
|----------|------------------------|-------|-----|
| 1. Identify staffing need | Staffing request is documented in the SOP; no CLI form | `docs/sop-hr-onboarding.md` §5.1 | No `ai-company hr onboard request` command forms this input today |
| 2. Define agent role | Agent entry lives in **`company-registry.yaml`** (YAML) | `company-registry.yaml`, `registry/loader.py` | SOP text still says `company/agent-registry.json`; doc mismatch |
| 3. Security review | Permissions reviewed by the registry loader / model; no gated CLI sign-off | `registry/loader.py`, `cli/security.py`, `cli/validate.py` | No `ai-company hr onboard security <id>` step persists a sign-off record |
| 4. Validate + Generate | `ai-company generate --dry-run` then `ai-company generate` → `AgentGenerator` | `src/ai_company/generator.py`, `cli/agents.py`, `cli/company.py` | Matches SOP exactly |
| 5. Run tests | `pytest && ruff check src/ && mypy src/` | `pyproject.toml`, CI `ci.yml` | Matches |
| 6. Human approval | `ai-company orchestrator approval` flows through HITL `ApprovalGate` + 5-tier decision engine, appears in dashboard Approvals | `executor/hitl_gate.py`, `decision/engine.py`, `cli/orchestrator.py`, `cli/governance.py`, `dashboard/api.py` (/approvals) | Matches conceptually; no explicit "submit onboarding for approval" command |
| 7. Verify deployment | `ai-company agents list` shows deployed agents | `cli/agents.py` | Matches |

## Key gaps

1. **No onboarding state machine / CLI chain** (`hr onboard ...`). The `#28`
   grilling ticket owns introducing that chain (requested → config_review →
   security_review → generating → testing → approval → active → archived).
2. **Doc drift:** SOP references `company/agent-registry.json`; actual source is
   `company-registry.yaml`.
3. **No persisted approval record** for step 6 — approval is file/YAML based.
4. **No dedicated "Onboarding" dashboard panel** today.

## Verdict for #28 / #29 / #30

The existing registry → generator → HITL pipeline already covers SOP steps 2,
4, 5, 7 directly. The onboarding flow tickets (#28, #29, #30) are about adding the
orchestrating state machine + dashboard status + the `hr onboard` CLI chain —
i.e., wiring the gaps, not rebuilding the pipeline.

Artifact for wayfinder #24 — mapping + gap list complete.
