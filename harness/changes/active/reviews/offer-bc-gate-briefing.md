**Offer B/C Gate-Conflict Briefing**

---

### Summary

A conflict exists between three sources of governance logic concerning Offer B and Offer C client‑onboarding. The policy document and the runtime code still treat Offer B and Offer C as blocked, while the governing YAML configuration (`malawi_offers.yaml`) already marks both offers as `governance_state: approved` and sets `service_level_liability_cap.status` to `ratified` with an empty `blocked_offers` list. The hard‑coded `BLOCKED_OFFERS = frozenset({"offer_b", "offer_c"})` in `client_intake.py` continues to raise `GovernanceGateError` for any engagement attempt, creating a mismatch between declared governance state and enforced runtime behavior.

---

### Three Sources

| # | Source | Exact Relevant Text |
|---|--------|---------------------|
| **1** | `docs/legal/client-onboarding-policy.md:36‑41` | “**Offer B** (BPA/Chatbots) … **blocked** … **Offer C** (Data & Reporting) … **blocked** … **Offers B and C remain BLOCKED** until `service_level_liability_cap.status` transitions to `ratified` in `malawi_offers.yaml.” (line 41) |
| **2** | `config/company/malawi_offers.yaml:24‑31/75‑76` | • Offer B: `governance_state: "approved"` (line 24) <br>• Offer C: `governance_state: "approved"` (line 33) <br>• `service_level_liability_cap:` `status: "ratified"` (line 76), `blocked_offers: []` (line 78) |
| **3** | `src/ai_company/services/client_intake.py:44` | `BLOCKED_OFFERS = frozenset({"offer_b", "offer_c"})` — the runtime block that prevents `create_engagement` for these offers (line 44). |

---

### Exact Inconsistency

The policy + code maintain a block on Offer B and Offer C **until** `service_level_liability_cap.status` becomes `ratified`. However, the YAML source of truth already records that status as `ratified` (as of 2026‑08‑12) and sets `blocked_offers: []`. Consequently, the governance condition is technically satisfied, yet the hard‑coded `BLOCKED_OFFERS` frozenset in the service layer still blocks any attempt to create a client engagement for Offer B or Offer C, producing a `GovernanceGateError`.

---

### Options (A/B/C)

| Option | Pro (one sentence) | Con (one sentence) |
|---|---|---|
| **A: Keep block** (policy + code remain; no change unless re‑approved) | Maintains the existing safety gate, preventing accidental client work on high‑risk offers until formal re‑approval. | Perpetuates an inconsistency with the ratified YAML state, leaving the block in place despite governance already being met. |
| **B: Open the code gate** (remove `offer_b`/`offer_c` from `BLOCKED_OFFERS` and update policy docs) | Aligns runtime enforcement with the already‑ratified governance state, enabling Offer B/C engagements immediately. | Removes a defensive guard without a fresh governance review, risking client onboarding before all stakeholder approvals are formally re‑signed. |
| **C: Re‑ratify explicitly in policy + yaml** (add explicit approval flag, no code change) | Makes the unblocking intention explicit in both policy and config, preserving the code guard while documenting the new status. | Requires updating two documents (policy table and YAML) and does not automatically lift the code‑level block; a separate code change would still be needed. |

---

### Pros & Cons per Option

- **Option A (Keep block):**
  - *Pro:* Keeps the existing safety gate, preventing accidental client work on high‑risk offers until formal re‑approval.
  - *Con:* Perpetuates an inconsistency with the ratified YAML state, leaving the block in place despite governance already being met.

- **Option B (Open the code gate):**
  - *Pro:* Aligns runtime enforcement with the already‑ratified governance state, enabling Offer B/C engagements immediately.
  - *Con:* Removes a defensive guard without a fresh governance review, risking client onboarding before all stakeholder approvals are formally re‑signed.

- **Option C (Re‑ratify explicitly):**
  - *Pro:* Makes the unblocking intention explicit in both policy and config, preserving the code guard while documenting the new status.
  - *Con:* Requires updating two documents (policy table and YAML) and does not automatically lift the code‑level block; a separate code change would still be needed.

---

### Recommendation (deferred)

Since the user selected **“briefing only, defer decision,”** no code or policy change is executed here. The briefing is provided for CEO/CLO review to determine whether to keep the block (Option A), open the code gate (Option B), or re‑ratify explicitly (Option C). The recommended next step is for the CEO and CLO to evaluate the pros and cons against current risk tolerance and decide which option, if any, to implement.
