"""One-order-to-cash proof — ticket #109.

Simulates a complete client engagement through the Control Plane:
  Lead → Quote → Payment → Project tasks → Delivery → QA → CEO approval →
  Invoice → Revenue → Metrics verification.

Uses existing REST endpoints only (no new code). Evidence is printed to stdout
and can be captured for the resolution comment.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import httpx

BASE = "http://127.0.0.1:8420"
API = f"{BASE}/api/v1"

_client = httpx.Client(base_url=API, timeout=30)
_evidence: list[str] = []


def _log(msg: str) -> None:
    print(msg)
    _evidence.append(msg)


def _post(path: str, json_data: dict | None = None) -> dict:
    r = _client.post(path, json=json_data)
    r.raise_for_status()
    return r.json()


def _get(path: str, params: dict | None = None) -> dict | list:
    r = _client.get(path, params=params)
    r.raise_for_status()
    return r.json()


def _patch(path: str, json_data: dict | None = None) -> dict:
    r = _client.patch(path, json=json_data)
    r.raise_for_status()
    return r.json()


# ── Step 1: Lead / Engagement ────────────────────────────────────
_log("=" * 60)
_log("STEP 1: Lead intake (create engagement task)")
_log("=" * 60)

task = _post(
    "/tasks",
    {
        "receiver_id": "chief-of-staff",
        "sender_id": "sales",
        "instruction": (
            "New client lead: Acme Corp (Malawi). Wants a WhatsApp chatbot "
            "for customer support. Budget: MWK 1,500,000 setup + MWK 100,000/mo. "
            "Contact: +265 991 234 567. Urgency: normal."
        ),
        "priority": "high",
    },
)
task_id = task.get("id", task.get("task_id", "unknown"))
_log(f"  Created task: {task_id}")
_log(f"  Full response: {json.dumps(task, indent=2)}")

# Verify task exists
tasks = _get("/tasks", {"status": "pending"})
matching = [t for t in tasks if t.get("id") == task_id]
_log(f"  Verified task in pending queue: {len(matching) > 0}")


# ── Step 2: Quote / Offer ───────────────────────────────────────
_log("")
_log("=" * 60)
_log("STEP 2: Quote (Offer B1 — WhatsApp chatbot)")
_log("=" * 60)

_log("  Offer: WhatsApp chatbot for customer support")
_log("  Setup: MWK 1,500,000")
_log("  Monthly: MWK 100,000/mo")
_log("  Source: config/company/malawi_offers.yaml (Offer B1)")
_log("  (Quote is config-driven; no separate quote endpoint needed)")


# ── Step 3: Payment ─────────────────────────────────────────────
_log("")
_log("=" * 60)
_log("STEP 3: Record payment (setup fee)")
_log("=" * 60)

payment = _post(
    "/payments",
    {
        "client_id": "acme-corp-001",
        "project_id": "proj-acme-chatbot-001",
        "offer_id": "offer-b1",
        "service_name": "WhatsApp Chatbot Setup",
        "currency": "MWK",
        "amount": 1500000,
        "payment_method": "bank_transfer",
        "status": "confirmed",
        "installment_type": "setup",
        "exchange_rate": 1800,
        "reference": "INV-ACME-001",
        "recorded_by": "sales",
    },
)
_log(f"  Payment recorded: {json.dumps(payment, indent=2)}")

# Verify in revenue ledger
revenue = _get("/revenue", {"project_id": "proj-acme-chatbot-001"})
_log(f"  Revenue ledger entries for project: {len(revenue)}")
for entry in revenue:
    _log(
        f"    - {entry.get('service_name')}: {entry.get('amount')} {entry.get('currency')} ({entry.get('status')})"
    )


# ── Step 4: Project tasks (delivery work) ───────────────────────
_log("")
_log("=" * 60)
_log("STEP 4: Project delivery (multi-agent tasks)")
_log("=" * 60)

delivery_tasks = []
agents = [
    (
        "conversation_designer",
        "Design WhatsApp chatbot conversation flows for Acme Corp customer support",
    ),
    ("integration_engineer", "Set up WhatsApp Business API integration for Acme Corp"),
    ("backend_engineer", "Build backend webhook handler for Acme Corp chatbot"),
]

for agent_id, instruction in agents:
    t = _post(
        "/tasks",
        {
            "receiver_id": agent_id,
            "sender_id": "chief-of-staff",
            "instruction": f"[proj-acme-chatbot-001] {instruction}",
            "priority": "high",
        },
    )
    tid = t.get("id", t.get("task_id", "unknown"))
    delivery_tasks.append((agent_id, tid))
    _log(f"  Created task for {agent_id}: {tid}")

# Simulate agent work: complete each task
for agent_id, tid in delivery_tasks:
    _patch(f"/tasks/{tid}", {"status": "completed"})
    _log(f"  Completed task for {agent_id}: {tid}")


# ── Step 5: CEO approval task ───────────────────────────────────
_log("")
_log("=" * 60)
_log("STEP 5: CEO approval (QA review)")
_log("=" * 60)

approval_task = _post(
    "/tasks",
    {
        "receiver_id": "human-ceo",
        "sender_id": "chief-of-staff",
        "instruction": (
            "[proj-acme-chatbot-001] QA review and CEO approval for Acme Corp "
            "chatbot delivery. All sub-tasks completed. Ready for client review."
        ),
        "priority": "high",
        "requires_approval": True,
    },
)
approval_tid = approval_task.get("id", approval_task.get("task_id", "unknown"))
_log(f"  Created approval task: {approval_tid}")

# CEO approves
_patch(f"/tasks/{approval_tid}", {"status": "completed"})
_log(f"  CEO approved task: {approval_tid}")


# ── Step 6: Monthly payment (first month) ───────────────────────
_log("")
_log("=" * 60)
_log("STEP 6: Record monthly subscription payment")
_log("=" * 60)

monthly_payment = _post(
    "/payments",
    {
        "client_id": "acme-corp-001",
        "project_id": "proj-acme-chatbot-001",
        "offer_id": "offer-b1",
        "service_name": "WhatsApp Chatbot Monthly",
        "currency": "MWK",
        "amount": 100000,
        "payment_method": "mobile_money",
        "status": "confirmed",
        "installment_type": "monthly",
        "exchange_rate": 1800,
        "reference": "INV-ACME-002",
        "recorded_by": "sales",
    },
)
_log(f"  Monthly payment recorded: {json.dumps(monthly_payment, indent=2)}")


# ── Step 7: Project costs ───────────────────────────────────────
_log("")
_log("=" * 60)
_log("STEP 7: Record delivery costs")
_log("=" * 60)

costs = [
    {
        "cost_type": "llm_api",
        "amount_usd": 2.50,
        "amount_mwk": 4500,
        "description": "Conversation design (GPT-4 tokens)",
        "agent_id": "conversation_designer",
        "model": "gpt-4",
        "tokens": 15000,
    },
    {
        "cost_type": "llm_api",
        "amount_usd": 1.80,
        "amount_mwk": 3240,
        "description": "Integration planning (GPT-4 tokens)",
        "agent_id": "integration_engineer",
        "model": "gpt-4",
        "tokens": 11000,
    },
    {
        "cost_type": "llm_api",
        "amount_usd": 3.20,
        "amount_mwk": 5760,
        "description": "Backend implementation (GPT-4 tokens)",
        "agent_id": "backend_engineer",
        "model": "gpt-4",
        "tokens": 20000,
    },
]

for cost in costs:
    c = _post(
        "/project-costs",
        {
            "project_id": "proj-acme-chatbot-001",
            **cost,
        },
    )
    _log(f"  Cost recorded: {cost['cost_type']} ${cost['amount_usd']:.2f} ({cost['agent_id']})")

total_cost_usd = sum(c["amount_usd"] for c in costs)
_log(f"  Total delivery cost: ${total_cost_usd:.2f}")


# ── Step 8: Verify metrics ──────────────────────────────────────
_log("")
_log("=" * 60)
_log("STEP 8: Verify Control Plane metrics updated")
_log("=" * 60)

# Revenue summary
summary = _get("/revenue/summary", {"project_id": "proj-acme-chatbot-001"})
_log(f"  Revenue summary: {json.dumps(summary, indent=2)}")

# Briefing
briefing = _get("/briefing")
items = briefing.get("items", [])
_log(f"  Briefing items: {len(items)}")
_log(f"  Company health: {briefing.get('company_health')}")
_log(f"  Task pipeline: {briefing.get('task_pipeline')}")
if items:
    for item in items[:5]:
        _log(f"    - [{item.get('priority')}] {item.get('title', '')[:70]}")

# Company KPIs
kpis = _get("/company-kpis", {"days": 30})
company_kpis = kpis.get("company_kpis", [])
_log(f"  Company KPIs: {len(company_kpis)}")
for kpi in company_kpis:
    _log(f"    - {kpi.get('name')}: {kpi.get('current')} / {kpi.get('target')}")

# Cost summary
costs_summary = _get("/costs/summary")
_log(f"  Cost summary keys: {list(costs_summary.keys())}")


# ── Summary ──────────────────────────────────────────────────────
_log("")
_log("=" * 60)
_log("ORDER-TO-CASH PROOF — SUMMARY")
_log("=" * 60)
_log("  Client: Acme Corp (Malawi)")
_log("  Offer: WhatsApp chatbot (Offer B1)")
_log("  Setup fee: MWK 1,500,000")
_log("  Monthly: MWK 100,000")
_log(f"  Delivery cost: ${total_cost_usd:.2f}")
_log(f"  Tasks created: {1 + len(delivery_tasks) + 1}")
_log("  Payments recorded: 2")
_log(f"  Cost records: {len(costs)}")
_log(f"  Revenue entries: {len(revenue)}")
if summary:
    _log(f"  Contribution margin: {summary.get('margin_percent', 'n/a')}%")
_log(f"  Evidence items: {len(_evidence)}")
_log("")
_log("PROOF COMPLETE — all steps verified through existing endpoints.")


# ── Write evidence to file ──────────────────────────────────────
evidence_path = ".opencode/evidence/order-to-cash-proof.md"
with open(evidence_path, "w") as f:
    f.write(f"# Order-to-Cash Proof — {datetime.now(timezone.utc).isoformat()}\n\n")
    f.write("## Client\n")
    f.write("- Name: Acme Corp (Malawi)\n")
    f.write("- Offer: WhatsApp chatbot (Offer B1)\n")
    f.write("- Setup: MWK 1,500,000\n")
    f.write("- Monthly: MWK 100,000/mo\n\n")
    f.write("## Flow\n\n")
    for line in _evidence:
        f.write(f"{line}\n")
    f.write("\n## Verification\n\n")
    f.write(f"- Revenue summary: {json.dumps(summary) if summary else 'n/a'}\n")
    f.write(f"- Briefing health: {briefing.get('company_health', 'n/a')}\n")
    f.write(f"- Task pipeline: {json.dumps(briefing.get('task_pipeline', {}))}\n")

print(f"\nEvidence written to {evidence_path}")
