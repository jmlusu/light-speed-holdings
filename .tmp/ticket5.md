## Question

Agree the Org Health backend contract: module location, `/api/org-health` response shape, and history persistence approach.

Decisions needed:
- Module: new `src/ai_company/dashboard/org_health.py` or extend `data_service.py`?
- Endpoint: `GET /api/org-health` returning `{ score, components[], bands, trend[], collected_at }`
- History: reuse `KPIHistoryStore` (add score as a virtual KPI) or new SQLite table?
- WS broadcast: fire `_broadcast_kpis` with `org_health` payload?

Response shape sketch:
```json
{
  "score": 78,
  "band": "amber",
  "components": [
    {"name": "department_kpi_health", "value": 85, "weight": 0.30, "sub_score": 85},
    {"name": "task_success_rate", "value": 92, "weight": 0.25, "sub_score": 92},
    ...
  ],
  "trend": [
    {"timestamp": "2026-08-10T00:00:00Z", "score": 75},
    {"timestamp": "2026-08-11T00:00:00Z", "score": 78}
  ],
  "collected_at": "2026-08-12T12:00:00Z"
}
```

**Blocked by: Choose the Org Health score composition and config schema (#26)**
