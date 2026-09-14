# Security Checklist (Phase 14 — Section 46)

## Secure Headers
- [ ] HTTP Strict Transport Security (HSTS) — max-age=31536000; includeSubDomains
- [ ] X-Frame-Options — DENY or SAMEORIGIN
- [ ] X-Content-Type-Options — nosniff
- [ ] X-XSS-Protection — 1; mode=block (legacy browsers)
- [ ] Referrer-Policy — strict-origin-when-cross-origin
- [ ] Content-Security-Policy — strict policy with appropriate exceptions
- [ ] Permissions-Policy — camera, microphone, geolocation restrictions

## HTTPS Everywhere
- [ ] HTTPS enforced for all pages and assets
- [ ] HSTS preload list included
- [ ] No mixed content (all resources loaded over HTTPS)
- [ ] SSL/TLS configuration: TLS 1.2+ only, disable SSL 3.0/ TLS 1.0/ 1.1
- [ ] Let's Encrypt or equivalent certificate auto-renewal configured

## Form Validation
### Client-Side
- [ ] All form fields have HTML5 validation (required, pattern, min/max)
- [ ] Real-time feedback on user input
- [ ] Focus management on error revelation
- [ ] Error messages are descriptive and actionable
- [ ] Focus trap on modals/dialogs

### Server-Side
- [ ] All form data validated on server before processing
- [ ] Input sanitization — prevent XSS and injection attacks
- [ ] Rate limiting on form submissions (e.g., max 5 submissions/minute per IP)
- [ ] CSRF protection on all forms
- [ ] Validation errors do not expose internal system information

## Spam Protection
- [ ] Turnstile (or hCaptcha) configured for all forms
- [ ] Honeypot field hidden from visual but present in HTML
- [ ] JavaScript-dependent spam checks as secondary layer
- [ ] Rate limiting per IP/submission type
- [ ] Akismet or similar anti-spam service for contact forms

## Dependency Auditing
- [ ] Regular vulnerability scans (weekly/on PR)
- [ ] Dependabot/renovate configured for auto-updates
- [ ] Known vulnerable dependencies blocked from merge
- [ ] Runtime dependency versions pinned in lockfile
- [ ] Peer dependency conflicts resolved

## Secrets Management
- [ ] Never commit .env or any secret files to git (.gitignored)
- [ ] API keys stored in environment variables only
- [ ] Keys rotated every 90 days (scheduled)
- [ ] Immediate key rotation on suspected compromise
- [ ] No hardcoded credentials in source code, templates, or comments
- [ ] Secrets manager used for production (Vercel secrets, GitHub Actions secrets, etc.)

## Least-Privilege Access
- [ ] Dashboard RBAC: run < approve < admin key hierarchy
- [ ] Dashboard CORS restricted to allowlist (no wildcard *)
- [ ] File permissions: company/ 700, company/*.yaml 600, .opencode/inbox.json 600
- [ ] Dashboard service runs as non-root user
- [ ] No admin capabilities exposed to run-key users
- [ ] Network access restricted to necessary endpoints only

## Network Security
- [ ] TLS termination at CDN/proxy (nginx/Caddy)
- [ ] WAF (Web Application Firewall) in front of dashboard
- [ ] Rate limiting on API endpoints
- [ ] Dashboard access restricted to internal network/VPN where appropriate
- [ ] Outbound connections monitored and restricted

## Never Expose
- [ ] API keys (in client code, URLs, or error messages)
- [ ] Internal infrastructure details
- [ ] Private model endpoints
- [ ] Administrative interfaces
- [ ] Agent configuration or internal state
