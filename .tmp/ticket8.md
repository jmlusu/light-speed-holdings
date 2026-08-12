## Question

Wire onboarding approval through the existing HITL gate (`ApprovalGate` / 5-tier decision engine) so it appears in the dashboard Approvals tab with WS alerts.

Current approval flow:
- `orchestrator/approvals.yaml` stores requests with id, action, agent_id, tier, status, expires_at
- `HITLGate.request_and_wait()` creates Future, non-blocking
- `ApprovalGate` evaluates against tier rules (`orchestrator/tier_rules.py`)
- Dashboard `/api/approvals` lists pending; `/api/approvals/{id}/approve|reject` mutates YAML
- WS `broadcast_approval_alert()` pushes to connected clients

Onboarding integration:
- When flow reaches `approval` state, create approval request in `approvals.yaml` with:
  - `action`: "agent_onboarding"
  - `agent_id`: the new agent's id
  - `tier`: 2 (standard) or 3 (if sensitive tools)
  - `payload`: { request_id, role, department, registry_entry }
  - `expires_at`: +48h (configurable)
- CTO/human-ceo approves via dashboard or CLI
- On approval: flow transitions to `generating` → `testing` → `active`
- On rejection: flow goes to `archived` with reason
- Expiry sweep (Sprint 7 HITL expiry) moves stale PENDING to EXPIRED

**Blocked by: Map the onboarding stack to the SOP's 8 steps (#24)**
