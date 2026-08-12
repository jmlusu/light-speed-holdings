## Question

Define the agent onboarding flow state machine and CLI command chain.

State machine (from SOP mapping):
- `requested` — human creates staffing request
- `config_review` — HR defines role, writes draft registry entry
- `security_review` — CTO reviews permissions/tools/hierarchy
- `generating` — `ai-company generate --dry-run` then `ai-company generate`
- `testing` — `pytest && ruff check src/ && mypy src/`
- `approval` — HITL approval via `ApprovalGate` (tier 2+), appears in dashboard Approvals
- `active` — agent deployed, verified via `ai-company agents list`
- `archived` — if rejected or abandoned

CLI chain: `ai-company hr onboard --wizard` (interactive) or subcommands:
- `ai-company hr onboard request --role --department --reports-to`
- `ai-company hr onboard review <request-id>` (HR config)
- `ai-company hr onboard security <request-id>` (CTO sign-off)
- `ai-company hr onboard generate <request-id>`
- `ai-company hr onboard test <request-id>`
- `ai-company hr onboard approve <request-id>` (triggers HITL)
- `ai-company hr onboard activate <request-id>`

Dashboard status: new "Onboarding" tab or panel on Agents page showing requests in each state.

**Blocked by: Map the onboarding stack to the SOP's 8 steps (#24)**
