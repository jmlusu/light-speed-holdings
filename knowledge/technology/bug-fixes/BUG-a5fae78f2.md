# fix(site): give enquiry failures actionable copy and log the Turnstile reason

**ID:** BUG-a5fae78f2
**Date:** 2026-10-26
**Resolved:** unresolved (fix in review; not merged or deployed)
**Commit:** a5fae78f29e0954c261919a2fae908990ccf2729
**Issue:** none - found while diagnosing 403 responses from the production contact form

## Original Issue Body

No issue was filed. The production contact form at
https://lightspeedholdings.vercel.app/contact failed every submission with one
sentence: "We could not send that right now. Please try again."

That sentence covered every failure mode, so a rejected security check looked
identical to a mail outage, a validation error, or a rate limit - for the
visitor and for the operator. The API answered
`{"error":{"code":"verification_failed"}}` with no `message`, and
`verifyTurnstile` returned a bare boolean, so nothing recorded why Cloudflare
had rejected the token.

## Root Cause (filled by the resolving engineer)

1. Client copy: `ContactSection` rendered
   `data?.error?.message ?? ENQUIRY_GENERIC_ERROR`. The handler returns codes,
   not messages, so the fallback sentence was always used.
2. Server diagnostics: `verifyTurnstile` collapsed every outcome to `false` -
   bad token, bad secret, action mismatch, hostname mismatch, network error.
   The rejection reason never reached the log.

The production failure itself (a `TURNSTILE_SECRET_KEY` that Cloudflare rejects
with `invalid-input-secret`, proven by calling siteverify directly with the
configured value) is a separate configuration defect. This change does not fix
it; it makes the failure legible.

## Fix (filled by the resolving engineer)

- `api/enquiry.ts`: `verifyTurnstile` returns `true` or a reason string
  (`invalid_token`, `verify_failed: <error-codes>`, `action_mismatch`,
  `hostname_mismatch`, `fetch_error: ...`, `http_error_<status>`). The handler
  logs it as `[enquiry] turnstile rejected: <reason>` and still answers with the
  code only - the reason names our own configuration and stays server-side.
- `src/lib/enquiry.ts`: `ENQUIRY_ERROR_COPY` and `enquiryErrorMessage(code)` map
  each handler code to copy a visitor can act on. Unknown codes fall back to the
  existing generic sentence.
- `src/components/ContactSection.tsx`: use the mapped copy, still preferring an
  API-supplied `message` if one is ever returned. Add `hidden` to the honeypot
  so it is not rendered (it was a 1x1 element parked offscreen).

## Files Changed

- `api/enquiry.ts`
- `src/lib/enquiry.ts`
- `src/components/ContactSection.tsx`
- `src/__tests__/enquiry-error-copy.test.ts` (new)

## Diagnostic Commands

```powershell
# API contract against the local dev server on :1441
curl.exe -sS -o - -w "|%{http_code}" -X POST http://localhost:1441/api/enquiry `
  -H "Content-Type: application/json" --data-binary "@payload.json"

# Cloudflare siteverify, called directly with the configured secret
curl.exe -sS -X POST https://challenges.cloudflare.com/turnstile/v0/siteverify `
  -H "Content-Type: application/x-www-form-urlencoded" --data-binary "@siteverify.txt"

bun run build
bun run test
python scripts/test/check-vercelignore.py
python scripts/test/check-site-form-backend.py
```

## Verification

- Handler matrix on the local dev server: `pong 200`, `invalid_json 400`,
  `validation_failed 400` (with field list), `verification_required 403`,
  `verification_failed 403`, honeypot `200 skipped`, wrong method `405`.
- Browser run against `http://localhost:1441/contact`: 837-character token, API
  answered `403 {"error":{"code":"verification_failed"}}` with no reason, the
  screen showed "The security check was rejected. Refresh the page and try
  again.", the server log recorded
  `[enquiry] turnstile rejected: verify_failed: invalid-input-secret`, and the
  nodemailer stub recorded zero messages.
- `bun run build` passed (tsc + vite build); `bun run test` passed 16 files /
  144 tests; both site guards passed.
- Production was not tested with a valid submission: that sends a real email and
  was not authorised.

## Link an Issue

No issue was filed. If this becomes tracked, add `Closes #N` to a future commit.
