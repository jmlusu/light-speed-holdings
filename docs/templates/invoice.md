# Invoice

**Light Speed Holdings**
AI Company Builder — Malawi

---

**Invoice #:** {{ invoice_number }}
**Date:** {{ date }}
**Due:** {{ due_date }}

---

**Bill To:** {{ client_name }}
**Contact:** {{ client_contact }}
**Currency:** {{ currency }}

---

## Service Delivered

**Service:** {{ service_name }}
**Offer:** {{ offer_id }}
**Project:** {{ project_id }}

| Item | Description | Amount |
|------|-------------|--------|
{% for item in line_items %}
| {{ item.description }} | {{ item.detail }} | {{ item.amount }} |
{% endfor %}

**Subtotal:** {{ subtotal }}
**Tax (if applicable):** {{ tax }}
**Total Due:** {{ total }}

---

## Payment Status

| Installment | Amount | Status | Date |
|-------------|--------|--------|------|
| Upfront (50%) | {{ upfront_amount }} | {{ upfront_status }} | {{ upfront_date }} |
| Delivery (50%) | {{ delivery_amount }} | {{ delivery_status }} | {{ delivery_date }} |

---

## Payment Methods

- **Airtel Money:** {{ airtel_number }}
- **TNM Mpamba:** {{ tnm_number }}
- **Bank Transfer:** {{ bank_details }}
- **PayChangu:** {{ paychangu_link }}

**Reference:** {{ payment_reference }}

---

## Notes

- All prices exclude ad spend and third-party licensing
- 30-day support included post-delivery
- Questions? Contact {{ company_email }}

---

**Light Speed Holdings** | {{ company_email }} | {{ company_phone }}
