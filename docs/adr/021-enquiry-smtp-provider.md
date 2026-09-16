# ADR-021: Switch enquiry email delivery from Resend to generic SMTP

- **Status:** Accepted
- **Date:** 2026-09-16

## Context

The v1 enquiry backend (B-1, PR #263) integrated Resend as the email delivery provider. After launch the owner has no verified sending domain (the intended domain `lightspeedholdings.com` is parked/not in production), so Resend cannot send from a branded address. Requiring a domain purchase before the enquiry form works delays first value.

## Decision

Replace the Resend-specific API integration with **nodemailer** using generic SMTP credentials. The serverless function reads `SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURE`, `SMTP_USER`, `SMTP_PASS`, `ENQUIRY_FROM_EMAIL`, and `ENQUIRY_TO_EMAIL` from environment variables. This lets the owner point the function at any SMTP-capable mailbox (Gmail app password, Outlook, Zoho, ISP relay) without buying or verifying a domain first.

Defaults: `ENQUIRY_FROM_EMAIL` falls back to `SMTP_USER` (the authenticated identity), so only `TO` needs to be a different address. `SMTP_PORT` defaults to 587, `SMTP_SECURE` to false.

## Consequences

+ No domain purchase required to reach a 201 on the enquiry form.
+ Works with free-tier mailbox providers that support SMTP + app passwords.
- Uses per-request TCP transport instead of a shared HTTP API — slightly higher latency under load, acceptable at enquiry volume.
- The Resend primary / Brevo fallback contract from T5 (issue #256) is replaced by the generic SMTP path. Brevo can be re-introduced later via an SMTP relay if needed.
- Requires `SMTP_HOST`/`SMTP_USER`/`SMTP_PASS` env vars to be set before the function returns anything other than 500 `not_configured`.
