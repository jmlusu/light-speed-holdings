# ADR-022: Migrate enquiry function from Node.js to Edge runtime

- **Status:** Accepted
- **Date:** 2026-09-16

## Context

After deploying the enquiry backend (B-1, ADR-020) to Vercel, all Node.js serverless functions on the project hang indefinitely — zero bytes, connection never completes. Edge functions on the same project respond instantly. Region pinning (cpt1, iad1, none) makes no difference. The issue is project-level: Vercel's Node.js runtime provisioning for this specific Hobby-plan project is broken. A dependency-free `api/ping.ts` (Node.js) hangs; an identical `api/ping-edge.ts` (Edge) returns 200 in under 2 seconds.

Vercel support would be needed to diagnose the Node.js runtime issue, but this blocks the enquiry form indefinitely.

## Decision

Migrate `api/enquiry.ts` from Node.js to **Edge runtime** (`export const config = { runtime: 'edge' }`). Replace `node:crypto` (`createHash`) with the Web Crypto API (`crypto.subtle.digest`). Keep the Resend HTTP API (already HTTP-native, works on Edge). Keep `@vercel/blob` (confirmed Edge-compatible by vendor docs).

This is a minimal, surgical change: only the runtime declaration and the hash implementation change. All other logic (validation, rate limit, Turnstile, idempotency, audit, Resend send) remains identical.

## Consequences

+ Enquiry form works immediately on the existing Vercel project — no new project, no support ticket.
- Edge functions run at the network edge (global) instead of a single region — slightly higher cold-start cost per unique region, acceptable at enquiry volume.
- Edge runtime cannot use Node.js APIs — future additions (e.g., filesystem, TCP sockets) must use Web API equivalents or be routed through a separate Node.js function.
- The `node:crypto` hash is replaced by `crypto.subtle.digest` (Web Crypto) — identical SHA-256 output, no behavioral change.
