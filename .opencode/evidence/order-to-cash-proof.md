# Order-to-Cash Proof — 2026-08-17T08:29:47.735723+00:00

## Client
- Name: Acme Corp (Malawi)
- Offer: WhatsApp chatbot (Offer B1)
- Setup: MWK 1,500,000
- Monthly: MWK 100,000/mo

## Flow

============================================================
STEP 1: Lead intake (create engagement task)
============================================================
  Created task: db70f4f5-dd45-4d43-ae9c-a43460ca472f
  Full response: {
  "id": "db70f4f5-dd45-4d43-ae9c-a43460ca472f",
  "sender_id": "sales",
  "receiver_id": "chief-of-staff",
  "instruction": "New client lead: Acme Corp (Malawi). Wants a WhatsApp chatbot for customer support. Budget: MWK 1,500,000 setup + MWK 100,000/mo. Contact: +265 991 234 567. Urgency: normal.",
  "status": "pending",
  "priority": "high",
  "created_at": "2026-08-17T08:29:46.229344+00:00",
  "completed_at": "",
  "result": ""
}
  Verified task in pending queue: True

============================================================
STEP 2: Quote (Offer B1 — WhatsApp chatbot)
============================================================
  Offer: WhatsApp chatbot for customer support
  Setup: MWK 1,500,000
  Monthly: MWK 100,000/mo
  Source: config/company/malawi_offers.yaml (Offer B1)
  (Quote is config-driven; no separate quote endpoint needed)

============================================================
STEP 3: Record payment (setup fee)
============================================================
  Payment recorded: {
  "id": "REV-A74213C0D9D2",
  "status": "recorded",
  "timestamp": "2026-08-17T08:29:46.263376+00:00",
  "amount": 1500000.0,
  "currency": "MWK"
}
  Revenue ledger entries for project: 3
    - WhatsApp Chatbot Setup: 1500000.0 MWK (confirmed)
    - WhatsApp Chatbot Monthly: 100000.0 MWK (confirmed)
    - WhatsApp Chatbot Setup: 1500000.0 MWK (confirmed)

============================================================
STEP 4: Project delivery (multi-agent tasks)
============================================================
  Created task for conversation_designer: d086d083-d16d-431a-94c0-f818e7fbcfd6
  Created task for integration_engineer: 1ac2a3f2-5d97-414e-8edb-bfe3ac58a4be
  Created task for backend_engineer: 3ce24e9c-add1-43fb-adb4-b7e62bde0923
  Completed task for conversation_designer: d086d083-d16d-431a-94c0-f818e7fbcfd6
  Completed task for integration_engineer: 1ac2a3f2-5d97-414e-8edb-bfe3ac58a4be
  Completed task for backend_engineer: 3ce24e9c-add1-43fb-adb4-b7e62bde0923

============================================================
STEP 5: CEO approval (QA review)
============================================================
  Created approval task: d7fa3731-aaed-4617-a6f8-64add6f0c692
  CEO approved task: d7fa3731-aaed-4617-a6f8-64add6f0c692

============================================================
STEP 6: Record monthly subscription payment
============================================================
  Monthly payment recorded: {
  "id": "REV-38E1B02E9755",
  "status": "recorded",
  "timestamp": "2026-08-17T08:29:46.411341+00:00",
  "amount": 100000.0,
  "currency": "MWK"
}

============================================================
STEP 7: Record delivery costs
============================================================
  Cost recorded: llm_api $2.50 (conversation_designer)
  Cost recorded: llm_api $1.80 (integration_engineer)
  Cost recorded: llm_api $3.20 (backend_engineer)
  Total delivery cost: $7.50

============================================================
STEP 8: Verify Control Plane metrics updated
============================================================
  Revenue summary: {
  "total_revenue_mwk": 3200000.0,
  "total_revenue_usd": 1777.78,
  "total_costs_usd": 15.0,
  "contribution_margin": 1762.78,
  "margin_percent": 99.2,
  "transaction_count": 4,
  "cost_count": 6
}
  Briefing items: 0
  Company health: 70
  Task pipeline: {'pending': 2, 'in_progress': 0, 'completed': 15, 'failed': 0}
  Company KPIs: 0
  Cost summary keys: ['total_budget', 'total_spent', 'llm_spend', 'budget_utilization', 'avg_cost_per_task', 'total_tasks', 'completed_tasks', 'per_agent_costs', 'cost_trend']

============================================================
ORDER-TO-CASH PROOF — SUMMARY
============================================================
  Client: Acme Corp (Malawi)
  Offer: WhatsApp chatbot (Offer B1)
  Setup fee: MWK 1,500,000
  Monthly: MWK 100,000
  Delivery cost: $7.50
  Tasks created: 5
  Payments recorded: 2
  Cost records: 3
  Revenue entries: 3
  Contribution margin: 99.2%
  Evidence items: 77

PROOF COMPLETE — all steps verified through existing endpoints.

## Verification

- Revenue summary: {"total_revenue_mwk": 3200000.0, "total_revenue_usd": 1777.78, "total_costs_usd": 15.0, "contribution_margin": 1762.78, "margin_percent": 99.2, "transaction_count": 4, "cost_count": 6}
- Briefing health: 70
- Task pipeline: {"pending": 2, "in_progress": 0, "completed": 15, "failed": 0}
