# Quotation

**Light Speed Holdings**
AI Company Builder — Malawi

---

**Quotation #:** {{ quotation_number }}
**Date:** {{ date }}
**Valid until:** {{ valid_until }}

---

**Client:** {{ client_name }}
**Contact:** {{ client_contact }}
**Currency:** {{ currency }}

---

## Scope of Work

**Service:** {{ service_name }}
**Offer:** {{ offer_id }}
**Description:** {{ description }}

| Item | Quantity | Unit Price | Amount |
|------|----------|------------|--------|
{% for item in line_items %}
| {{ item.description }} | {{ item.quantity }} | {{ item.unit_price }} | {{ item.amount }} |
{% endfor %}

**Subtotal:** {{ subtotal }}
**Tax (if applicable):** {{ tax }}
**Total:** {{ total }}

---

## Payment Terms

- **50% upfront** ({{ upfront_amount }}) — due before work begins
- **50% on delivery** ({{ delivery_amount }}) — due upon client approval

**Payment Methods:**
- Airtel Money: {{ airtel_number }}
- TNM Mpamba: {{ tnm_number }}
- Bank Transfer: {{ bank_details }}
- PayChangu: {{ paychangu_link }}

---

## Validity

This quotation is valid for **30 days** from the date above. Scope changes require a change order at MWK 60,000/hour.

---

**Prepared by:** {{ prepared_by }}
**Light Speed Holdings** | {{ company_email }} | {{ company_phone }}
