## Destination

A signed-off implementation spec/plan covering three features, produced by resolving the decision tickets below:

1. **Dashboard Org Health score** — a 0–100 live-telemetry composite with configurable weights and a persisted trend (hero gauge on `/` + history sparkline).
2. **Agent onboarding flow** — a CLI-driven state machine from request → security review → registry/generator → tests → HITL approval → activation, with dashboard status visibility.
3. **Company-KPIs UI wiring** — company-KPI cards + the Org Health gauge on the main Dashboard (`/`).

A later sprint executes the spec.

## Notes

- **Domain**: Python 3.12 CLI (Typer) at `ai-company/`; registry YAML → Jinja2 → `.opencode/agents/*.md`; MessageBus JSON task queue; FastAPI dashboard + WebSocket; SQLite write-through + JSON stores; Windows platform. 127 agents deployed; 30 CLI commands; 1860+ tests green; ruff + mypy clean.
- **Skills every session should consult**: grilling, domain-modeling, prototype, research, executing-plans, tdd, incremental-implementation, security-and-hardening, code-review-and-quality, git-workflow-and-versioning, planning-and-task-breakdown.
- **Standing preferences (charting decisions Q1–Q9)**:
  - Destination: signed-off spec/plan, not implementation (Q1).
  - New standalone map (Q2).
  - Org Health = live telemetry composite: dept KPI health + task success + agent utilization + escalations/approvals + budget (Q3).
  - Onboarding = CLI chain + dashboard status (Q4).
  - Org Health display = hero gauge + history/trend (Q5).
  - Org Health weights = configurable via `config/company/org-health.yaml` (Q6).
  - Onboarding = full lifecycle to deployed agent (registry + generator) (Q7).
  - HITL approval = reuse existing ApprovalGate/5-tier decision engine (Q8).
  - Company-KPIs UI = main Dashboard gets KPI cards + Org Health gauge (Q9).

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->

## Not yet specified

- Exact "no-source KPI" rendering treatment (graduates with prototype).
- Onboarding tab vs Agents-page panel (graduates with flow state machine).
- Score trend persistence details (graduates with backend contract).
- Test/isolation strategy for score + onboarding (temp inbox fixtures etc.) — graduates last.

## Out of scope

- Implementing the features (destination is the spec).
- New agent types/registry expansion.
- Data sources for KPI-001/002/005 (revenue ledger, surveys) — separate effort.
- Dashboard UI redesign beyond the hero.

## Tickets

Child issues (blocking wired by body convention: "Blocked by: <Name> (#N)").

- [ ] Inventory dashboard telemetry sources for the Org Health score (research)
- [ ] Map the onboarding stack to the SOP's 8 steps (research)
- [ ] Map the dashboard frontend for gauge and KPI cards (research)
- [ ] Choose the Org Health score composition and config schema (grilling)
- [ ] Agree the Org Health backend contract and history persistence (grilling)
- [ ] Define the agent onboarding flow state machine and CLI chain (grilling)
- [ ] Decide the onboarding registry/generator integration (grilling)
- [ ] Wire onboarding approval through the existing HITL gate (grilling)
- [ ] Prototype the CEO dashboard hero: Org Health gauge + company-KPI cards (prototype)
