# Digital Asset Register — LIGHTSPEED HOLDINGS

**Owner:** `social_media_manager` (registry `company-registry.yaml:928`). **Reconciled (2026-09-19):** [#189](https://github.com/jmlusu/light-speed-holdings/issues/189) was a governance decision record, not a mandate to remove the agent; `social_media_manager` has been committed since `f7dfc8aa` (tracked on `development`/`main`) and is confirmed as the designated owner of this register.
**Status:** Active — accounts blocked by [#194](https://github.com/jmlusu/light-speed-holdings/issues/194) until Phase 0/1 of `docs/marketing/digital-identity-setup.md` completes. **Domain control unresolved:** `lightspeedholdings.com` resolves to Afternic marketplace nameservers (for-sale lander, null MX) — see [#194](https://github.com/jmlusu/light-speed-holdings/issues/194).
**Purpose:** Single source of truth for every platform account: ownership, 2FA state, and provisioning status.
**Security:** No passwords or secrets live in this file. Credentials belong in the password manager only.

Update the `Status` column as provisioning moves through the [phase plan](digital-identity-setup.md#phase-plan). When a platform ships, set `Status: Live` and add the public URL to the `URL` column.

## Platform matrix

| Platform | URL | Username / Handle | Email | Owner | 2FA | Status | Administrators | Profile image | Cover image | Category | Biography | Website | Business-manager relationship | Launch status |
|----------|-----|-------------------|-------|-------|-----|--------|----------------|---------------|-------------|----------|-----------|---------|-------------------------------|---------------|
| Facebook | — | Lightspeed Holdings Limited | info.lightspeed@gmail.com | Company | Yes | Pending (#194) | TBD | Lightspeed logo | Branded cover (AI. STRATEGY. TRANSFORMATION.) | Consulting / IT / Business Service | Master description → FB variant | lightspeedholdings.com | Meta Business Suite | Draft |
| Instagram | — | @lightspeedholdings | info.lightspeed@gmail.com | Company | Yes | Pending (#194) | TBD | Lightspeed logo | — | Professional/Business | Master description → IG variant | lightspeedholdings.com | Meta Business Suite | Draft |
| X | — | @lightspeedholdings | info.lightspeed@gmail.com | Company | Yes | Pending (#194) | TBD | Lightspeed logo | Branded header | Professional → Business | Master description → X variant | lightspeedholdings.com | — | Draft |
| LinkedIn | — | LightSpeed Holdings Limited | info.lightspeed@gmail.com | Company | Yes | Pending (#194) | Founder as admin | Lightspeed logo | Branded cover | AI / Management Consulting / Technology | Master description → LinkedIn variant | lightspeedholdings.com | LinkedIn company administration | Draft |
| TikTok | — | @lightspeedholdings | info.lightspeed@gmail.com | Company | Yes | Pending (#194) | TBD | Lightspeed logo | — | Business Account | Master description → TikTok variant | lightspeedholdings.com | TikTok Business Center | Draft |
| YouTube | — | LightSpeed Holdings (@lightspeedholdings) | info.lightspeed@gmail.com | Company | Yes | Pending (#194) | TBD | Lightspeed logo | Branded banner | Company channel | Master description → YouTube variant | lightspeedholdings.com | Google business ownership | Draft |
| Threads | — | @lightspeedholdings | info.lightspeed@gmail.com | Company | Yes | Pending (#194) | TBD | Lightspeed logo | — | Company | Master description → Threads variant | lightspeedholdings.com | — | Reserved (Tier 3 — claim now, activate later) |
| Substack | — | @lightspeedholdings | info.lightspeed@gmail.com | Company | Yes | Pending (#194) | TBD | Lightspeed logo | Branded cover | Publication — long-form archive / discovery | Master description → Substack variant | lightspeedholdings.com | — | Draft (delivery stays on Resend; see [#192](https://github.com/jmlusu/light-speed-holdings/issues/192)) |
| Resend | resend.com | — | info.lightspeed@gmail.com | Company | Yes | Account created; sending domain unverified (#194) | Founder | — | — | Email delivery (broadcast + contacts/segments) | — | resend.com | — | Blocked — requires a verified company sending domain |

## Identity standard

- **Name:** LIGHTSPEED HOLDINGS LIMITED (brand: LIGHTSPEED)
- **Username:** `@lightspeedholdings` (fallback `@lightspeedholdingsmw` → `@lightspeedhq`)
- **Tagline:** ASPIRE. ACT. ACHIEVE.
- **Positioning:** AI. Strategy. Transformation.

## Reserve list

Claim for brand protection (do not necessarily use): `lightspeedholdings`, `lightspeedholdingsmw`, `lightspeedhq`, `lightspeedai`, `lightspeedafrica`.

## Change log

| Date | Change |
|------|--------|
| 2026-09-19 | #189 conflict resolved — `social_media_manager` confirmed as register owner (agent committed in `f7dfc8aa`); stale "uncommitted / ownership unresolved" banner removed. Live handles continue to be recorded in the `URL` column per the `Live` status rule. |
| 2026-09-17 | Register created from `social-media/LIGHTSPEED-SOCIAL-MEDIA-SETUP.md` (normalized to `docs/marketing/`). All platforms Pending — blocked by #194. |
| 2026-09-17 | Broken #194 links fixed; Substack + Resend rows added (#192/#194); domain-control blocker recorded. Owner left as `social_media_manager` pending the #189 conflict. |
